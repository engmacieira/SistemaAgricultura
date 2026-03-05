from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import date, datetime
from typing import List, Dict, Any
from ..models.produtor_model import ProdutorModel
from ..models.servico_model import ServicoModel
from ..models.execucao_model import ExecucaoModel
from ..models.pagamento_model import PagamentoModel

class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_summary_counts(self) -> Dict[str, Any]:
        total_producers = self.db.query(ProdutorModel).filter(ProdutorModel.is_deleted == False).count()
        total_services = self.db.query(ServicoModel).filter(ServicoModel.is_deleted == False).count()
        pending_executions = self.db.query(ExecucaoModel).filter(
            ExecucaoModel.status == "Pendente",
            ExecucaoModel.is_deleted == False
        ).count()
        
        financials = self.db.query(
            func.sum(PagamentoModel.amount - PagamentoModel.paidAmount).label("total_pending"),
            func.sum(PagamentoModel.paidAmount).label("total_paid")
        ).filter(PagamentoModel.is_deleted == False).first()

        return {
            "totalProducers": total_producers,
            "totalServices": total_services,
            "pendingExecutions": pending_executions,
            "totalPendingAmount": financials.total_pending or 0.0,
            "totalPaidAmount": financials.total_paid or 0.0
        }

    def get_monthly_financials(self) -> List[Dict[str, Any]]:
        # Last 6 months
        # Note: This is a simplified version, ideally we would group by month
        # Since SQLite is used, we'll use strftime if needed or just python logic
        # For now, let's get all payments and group them in use cases or here
        
        # Simple query for now, might need optimization
        results = self.db.query(
            func.strftime("%Y-%m", PagamentoModel.dueDate).label("month"),
            func.sum(PagamentoModel.amount - PagamentoModel.paidAmount).label("pending"),
            func.sum(PagamentoModel.paidAmount).label("paid")
        ).filter(PagamentoModel.is_deleted == False).group_by("month").order_by("month").limit(6).all()

        return [{"month": r.month, "pending": r.pending, "paid": r.paid} for r in results]

    def get_service_distribution(self) -> List[Dict[str, Any]]:
        results = self.db.query(
            ExecucaoModel.serviceName,
            func.count(ExecucaoModel.id).label("count")
        ).filter(ExecucaoModel.is_deleted == False).group_by(ExecucaoModel.serviceName).all()
        
        return [{"name": r.serviceName, "value": r.count} for r in results]

    def get_recent_activities(self) -> List[Dict[str, Any]]:
        # Get last 5 executions
        executions = self.db.query(ExecucaoModel).filter(
            ExecucaoModel.is_deleted == False
        ).order_by(ExecucaoModel.date.desc()).limit(5).all()
        
        activities = []
        for e in executions:
            activities.append({
                "id": e.id,
                "type": "Agendamento",
                "description": f"{e.serviceName} - {e.producerName}",
                "date": e.date,
                "status": e.status,
                "amount": e.totalValue
            })
            
        # Sort by date
        activities.sort(key=lambda x: x["date"], reverse=True)
        return activities[:5]
