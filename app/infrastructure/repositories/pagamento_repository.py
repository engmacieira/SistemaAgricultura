from typing import List
from typing import List, Optional
from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models.pagamento_model import PagamentoModel, TransacaoPagamentoModel
from app.domain.entities.pagamento_entity import Pagamento, TransacaoPagamento

class PagamentoRepository(BaseRepository[PagamentoModel, Pagamento]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, PagamentoModel)

    def get_all(self) -> List[Pagamento]:
        models = self.db.query(self.model).filter(self.model.is_deleted == False).all()
        return [m.to_entity() for m in models]

    def get_by_id(self, id: str) -> Optional[Pagamento]:
        model = self.db.query(self.model).filter(self.model.id == id, self.model.is_deleted == False).first()
        return model.to_entity() if model else None

    def get_all_paginated(self, skip: int = 0, limit: int = 10, sort_by: str = "dueDate", order: str = "desc", search: str = "") -> List[Pagamento]:
        query = self.db.query(self.model).filter(self.model.is_deleted == False)
        
        if search:
            query = query.filter(self.model.producerName.ilike(f"%{search}%"))
            
        # Sorting
        column = getattr(self.model, sort_by, self.model.dueDate)
        if order.lower() == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())
            
        models = query.offset(skip).limit(limit).all()
        return [m.to_entity() for m in models]

    def count_filtered(self, search: str = "") -> int:
        query = self.db.query(self.model).filter(self.model.is_deleted == False)
        if search:
            query = query.filter(self.model.producerName.ilike(f"%{search}%"))
        return query.count()

    def get_debts_by_producer(self, search: str = "") -> List[dict]:
        from sqlalchemy import func
        # Only pending or partial payments that are not deleted
        query = self.db.query(
            self.model.producerName,
            func.sum(self.model.amount - self.model.paidAmount).label("totalDebt"),
            func.count(self.model.id).label("paymentCount")
        ).filter(
            self.model.is_deleted == False,
            self.model.status != "Pago"
        )
        
        if search:
            query = query.filter(self.model.producerName.ilike(f"%{search}%"))
            
        results = query.group_by(self.model.producerName).all()
        
        return [
            {
                "producerName": r.producerName,
                "totalDebt": float(r.totalDebt),
                "paymentCount": int(r.paymentCount)
            } for r in results
        ]

    def delete(self, id: str) -> bool:
        obj = self.db.query(self.model).filter(self.model.id == id).first()
        if obj:
            obj.is_deleted = True
            self.db.commit()
            return True
        return False

    def get_history(self, pagamento_id: str) -> List[TransacaoPagamento]:
        models = self.db.query(TransacaoPagamentoModel).filter(TransacaoPagamentoModel.pagamentoId == pagamento_id).all()
        return [m.to_entity() for m in models]

    def create_transaction(self, data: dict) -> TransacaoPagamento:
        model = TransacaoPagamentoModel(**data)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.to_entity()
    async def _update_pagamento_totals(self, pagamento_id: str):
        """Recalculate paidAmount and status based on transactions"""
        from sqlalchemy import func
        pagamento = self.db.query(PagamentoModel).filter(PagamentoModel.id == pagamento_id).first()
        if not pagamento:
            return

        total_paid = self.db.query(func.sum(TransacaoPagamentoModel.amount)).filter(
            TransacaoPagamentoModel.pagamentoId == pagamento_id
        ).scalar() or 0.0

        pagamento.paidAmount = total_paid
        
        if total_paid >= pagamento.amount:
            pagamento.status = "Pago"
            # Update last payment date if available
            last_date = self.db.query(func.max(TransacaoPagamentoModel.date)).filter(
                TransacaoPagamentoModel.pagamentoId == pagamento_id
            ).scalar()
            pagamento.paymentDate = last_date
        elif total_paid > 0:
            pagamento.status = "Parcial"
        else:
            pagamento.status = "Pendente"
            pagamento.paymentDate = None
            
        self.db.commit()

    def update_transaction(self, transaction_id: str, data: dict) -> Optional[TransacaoPagamento]:
        model = self.db.query(TransacaoPagamentoModel).filter(TransacaoPagamentoModel.id == transaction_id).first()
        if not model:
            return None
        
        pagamento_id = model.pagamentoId
        for key, value in data.items():
            setattr(model, key, value)
        
        self.db.commit()
        
        # Sync parent payment
        import asyncio
        # We are in a sync context here, but using async helper if needed. 
        # Actually _update_pagamento_totals is defined as async but uses self.db.query (sync).
        # Let's make it sync to match the rest of the file.
        self._sync_update_pagamento_totals(pagamento_id)
        
        return model.to_entity()

    def delete_transaction(self, transaction_id: str) -> bool:
        model = self.db.query(TransacaoPagamentoModel).filter(TransacaoPagamentoModel.id == transaction_id).first()
        if not model:
            return False
        
        pagamento_id = model.pagamentoId
        self.db.delete(model)
        self.db.commit()
        
        self._sync_update_pagamento_totals(pagamento_id)
        return True

    def get_by_filters(self, start_date: Optional[str] = None, end_date: Optional[str] = None, producer_names: Optional[List[str]] = None) -> List[Pagamento]:
        from datetime import datetime
        query = self.db.query(self.model).filter(self.model.is_deleted == False)
        
        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            query = query.filter(self.model.dueDate >= start)
        
        if end_date:
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            query = query.filter(self.model.dueDate <= end)
            
        if producer_names and len(producer_names) > 0:
            query = query.filter(self.model.producerName.in_(producer_names))
            
        models = query.order_by(self.model.dueDate.asc()).all()
        return [m.to_entity() for m in models]

    def _sync_update_pagamento_totals(self, pagamento_id: str):
        from sqlalchemy import func
        pagamento = self.db.query(PagamentoModel).filter(PagamentoModel.id == pagamento_id).first()
        if not pagamento:
            return

        total_paid = self.db.query(func.sum(TransacaoPagamentoModel.amount)).filter(
            TransacaoPagamentoModel.pagamentoId == pagamento_id
        ).scalar() or 0.0

        pagamento.paidAmount = total_paid
        
        if total_paid >= pagamento.amount:
            pagamento.status = "Pago"
            last_date = self.db.query(func.max(TransacaoPagamentoModel.date)).filter(
                TransacaoPagamentoModel.pagamentoId == pagamento_id
            ).scalar()
            pagamento.paymentDate = last_date
        elif total_paid > 0:
            pagamento.status = "Parcial"
        else:
            pagamento.status = "Pendente"
            pagamento.paymentDate = None
            
        self.db.commit()
