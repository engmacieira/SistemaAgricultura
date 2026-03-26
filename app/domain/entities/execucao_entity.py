from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Execucao:
    id: str
    solicitacaoId: str      # ✅ NOVO: O vínculo com a Fila de Espera (Parent ID)
    serviceId: str          
    serviceName: str        
    date: date              
    quantity: float         
    unit: str               
    valor_unitario: float   # ✅ NOVO: Qual era o preço da hora/hectare neste dia?
    totalValue: float       # (quantity * valor_unitario)
    status: str             # Ex: 'REGISTRADA', 'FATURADA'
    operador_maquina: Optional[str] = None # ✅ NOVO: Para saber quem dirigiu o trator
    is_deleted: bool = False