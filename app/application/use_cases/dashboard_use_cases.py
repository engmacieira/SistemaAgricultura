from sqlalchemy.orm import Session
from app.infrastructure.repositories.dashboard_repository import DashboardRepository
from ..schemas.dashboard_schemas import (
    DashboardData, DashboardSummary, MonthlyFinancial, 
    ServiceDistribution, RecentActivity
)

class DashboardUseCases:
    def __init__(self, db: Session):
        self.repository = DashboardRepository(db)

    def get_dashboard_data(self) -> DashboardData:
        summary_data = self.repository.get_summary_counts()
        # Ajustado para o nome do método que criamos no repositório
        monthly_financials_data = self.repository.get_revenue_by_month() 
        service_distribution_data = self.repository.get_service_distribution()
        recent_activities_data = self.repository.get_recent_activities()

        # ✅ REFATORAÇÃO: Mapeando os dados aninhados do Repositório para o seu Schema
        summary = DashboardSummary(
            totalProducers=summary_data["totalProducers"],
            totalServices=summary_data["totalServices"],
            pendingExecutions=summary_data["pendingExecutions"],
            totalPendingAmount=summary_data["financials"]["totalPending"],
            totalPaidAmount=summary_data["financials"]["totalPaid"]
        )

        return DashboardData(
            summary=summary,
            monthlyFinancial=[MonthlyFinancial(**item) for item in monthly_financials_data],
            serviceDistribution=[ServiceDistribution(**item) for item in service_distribution_data],
            recentActivities=[RecentActivity(**item) for item in recent_activities_data]
        )