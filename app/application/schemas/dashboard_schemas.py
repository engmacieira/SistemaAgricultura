from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class DashboardSummary(BaseModel):
    totalProducers: int
    totalServices: int
    pendingExecutions: int
    totalPendingAmount: float
    totalPaidAmount: float

class MonthlyFinancial(BaseModel):
    month: str
    pending: float
    paid: float

class ServiceDistribution(BaseModel):
    name: str
    value: int

class RecentActivity(BaseModel):
    id: str
    type: str  # 'Agendamento' ou 'Pagamento'
    description: str
    date: date
    status: str
    amount: Optional[float] = None

class DashboardData(BaseModel):
    summary: DashboardSummary
    monthlyFinancial: List[MonthlyFinancial]
    serviceDistribution: List[ServiceDistribution]
    recentActivities: List[RecentActivity]
