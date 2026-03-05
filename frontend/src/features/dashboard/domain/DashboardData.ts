export interface DashboardSummary {
    totalProducers: number;
    totalServices: number;
    pendingExecutions: number;
    totalPendingAmount: number;
    totalPaidAmount: number;
}

export interface MonthlyFinancial {
    month: string;
    pending: number;
    paid: number;
}

export interface ServiceDistribution {
    name: string;
    value: number;
}

export interface RecentActivity {
    id: string;
    type: string;
    description: string;
    date: string;
    status: string;
    amount?: number;
}

export interface DashboardData {
    summary: DashboardSummary;
    monthlyFinancial: MonthlyFinancial[];
    serviceDistribution: ServiceDistribution[];
    recentActivities: RecentActivity[];
}
