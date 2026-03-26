from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, case
from datetime import date, datetime
from typing import List, Dict, Any

from ..models.produtor_model import ProdutorModel
from ..models.servico_model import ServicoModel
from ..models.execucao_model import ExecucaoModel
from ..models.pagamento_model import PagamentoModel
from ..models.solicitacao_model import SolicitacaoModel  # ✅ NOVO IMPORT

class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_summary_counts(self) -> Dict[str, Any]:
        total_producers = self.db.query(ProdutorModel).filter(ProdutorModel.is_deleted == False).count()
        total_services = self.db.query(ServicoModel).filter(ServicoModel.is_deleted == False).count()
        
        # ✅ REFATORAÇÃO: A "Fila de Espera" agora é contabilizada pelas Solicitações Pendentes
        pending_executions = self.db.query(SolicitacaoModel).filter(
            SolicitacaoModel.status == "PENDENTE",
            SolicitacaoModel.is_deleted == False
        ).count()
        
        financials = self.db.query(
            func.sum(PagamentoModel.amount - PagamentoModel.paidAmount).label("total_pending"),
            func.sum(PagamentoModel.paidAmount).label("total_paid")
        ).filter(PagamentoModel.is_deleted == False).first()

        return {
            "totalProducers": total_producers,
            "totalServices": total_services,
            "pendingExecutions": pending_executions, # Mantemos o nome da chave para não quebrar o Frontend
            "financials": {
                "totalPending": float(financials.total_pending or 0),
                "totalPaid": float(financials.total_paid or 0)
            }
        }

    def get_revenue_by_month(self) -> List[Dict[str, Any]]:
        # A lógica financeira continua a mesma, pois o PagamentoModel não mudou sua base.
        results = self.db.query(
            func.strftime("%Y-%m", PagamentoModel.dueDate).label("month"),
            func.sum(PagamentoModel.amount - PagamentoModel.paidAmount).label("pending"),
            func.sum(PagamentoModel.paidAmount).label("paid")
        ).filter(PagamentoModel.is_deleted == False).group_by("month").order_by("month").limit(6).all()

        return [{"month": r.month, "pending": r.pending, "paid": r.paid} for r in results]

    def get_service_distribution(self) -> List[Dict[str, Any]]:
        # Continua a buscar na Execucao, pois é lá que sabemos o que realmente foi feito.
        results = self.db.query(
            ExecucaoModel.serviceName,
            func.count(ExecucaoModel.id).label("count")
        ).filter(ExecucaoModel.is_deleted == False).group_by(ExecucaoModel.serviceName).all()
        
        return [{"name": r.serviceName, "value": r.count} for r in results]

    def get_recent_activities(self) -> List[Dict[str, Any]]:
        # ✅ REFATORAÇÃO: Usamos o `joinedload` para trazer a Solicitação (mãe) junto com a Execução (filha)
        # de forma otimizada (numa só query), para podermos aceder ao `producerName`.
        executions = self.db.query(ExecucaoModel).options(joinedload(ExecucaoModel.solicitacao)).filter(
            ExecucaoModel.is_deleted == False
        ).order_by(ExecucaoModel.date.desc()).limit(5).all()
        
        activities = []
        for e in executions:
            # Pegamos o nome do produtor lá na classe Solicitação
            producer_name = e.solicitacao.producerName if e.solicitacao else "Desconhecido"
            
            activities.append({
                "id": e.id,
                "type": "Serviço Realizado", # Mudei a label de "Agendamento" para refletir o real
                "description": f"{e.serviceName} - {producer_name}",
                "date": e.date.isoformat() if hasattr(e.date, 'isoformat') else str(e.date),
                "status": e.status
            })
            
        return activities