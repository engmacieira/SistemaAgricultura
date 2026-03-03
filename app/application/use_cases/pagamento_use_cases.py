from typing import List, Dict, Any, Optional
from datetime import date

class PagamentoUseCases:
    def __init__(self, pagamento_repository):
        self.pagamento_repository = pagamento_repository

    def listar_pagamentos(self) -> List[Any]:
        return self.pagamento_repository.get_all()

    def obter_pagamento(self, pagamento_id: str) -> Any:
        pagamento = self.pagamento_repository.get_by_id(pagamento_id)
        if not pagamento:
            raise ValueError("Pagamento não encontrado")
        return pagamento

    def criar_pagamento(self, data: Dict[str, Any]) -> Any:
        return self.pagamento_repository.create(data)

    def atualizar_pagamento(self, pagamento_id: str, data: Dict[str, Any]) -> Any:
        self.obter_pagamento(pagamento_id)
        return self.pagamento_repository.update(pagamento_id, data)

    def registrar_pagamento(self, pagamento_id: str, data_pagamento: Optional[date] = None) -> Any:
        """Caso de uso específico para a ação de 'Registrar Pagamento' do frontend"""
        pagamento = self.obter_pagamento(pagamento_id)
        
        if pagamento.status == "Pago":
            raise ValueError("Este pagamento já foi realizado.")
            
        # Use data_pagamento if provided, otherwise use today's date
        final_data_pagamento = data_pagamento if data_pagamento is not None else date.today()

        dados_atualizados = {
            "status": "Pago",
            "paymentDate": final_data_pagamento
        }
        return self.pagamento_repository.update(pagamento_id, dados_atualizados)

    def deletar_pagamento(self, pagamento_id: str) -> bool:
        self.obter_pagamento(pagamento_id)
        return self.pagamento_repository.delete(pagamento_id)
