from dataclasses import dataclass
from datetime import date

@dataclass
class Execucao:
    id: str
    producerId: str
    producerName: str
    serviceId: str
    serviceName: str
    date: date
    quantity: float
    unit: str
    totalValue: float
    status: str
