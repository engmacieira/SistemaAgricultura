from sqlalchemy.orm import Session
from app.infrastructure.repositories.dashboard_repository import DashboardRepository
from ..schemas.dashboard_schemas import (
    DashboardData, DashboardSummary, MonthlyFinancial, 
    ServiceDistribution, RecentActivity
)
from typing import List

class DashboardUseCases:
    def __init__(self, db: Session):
        self.repository = DashboardRepository(db)

    def get_dashboard_data(self) -> DashboardData:
        summary_data = self.repository.get_summary_counts()
        monthly_financials_data = self.repository.get_monthly_financials()
        service_distribution_data = self.repository.get_service_distribution()
        recent_activities_data = self.repository.get_recent_activities()

        return DashboardData(
            summary=DashboardSummary(**summary_data),
            monthlyFinancial=[MonthlyFinancial(**item) for item in monthly_financials_data],
            serviceDistribution=[ServiceDistribution(**item) for item in service_distribution_data],
            recentActivities=[RecentActivity(**item) for item in recent_activities_data]
        )
