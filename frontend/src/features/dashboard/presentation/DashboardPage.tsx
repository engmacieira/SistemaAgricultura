import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Users, ClipboardList, AlertCircle, TrendingUp, DollarSign, ArrowUpRight, Calendar } from "lucide-react";
import { DashboardRepository } from "../data/DashboardRepository";
import { DashboardData } from "../domain/DashboardData";

const repository = new DashboardRepository();

export const DashboardPage: React.FC = () => {
    const [data, setData] = useState<DashboardData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const result = await repository.getDashboardData();
                setData(result);
            } catch (error) {
                console.error("Erro ao carregar dados do dashboard:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
            </div>
        );
    }

    if (!data) return <div>Erro ao carregar dados.</div>;

    return (
        <div className="p-6 space-y-6 bg-gray-50 min-h-screen">
            <header className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
                    <p className="text-gray-500">Bem-vindo de volta! Aqui está o resumo do seu sistema.</p>
                </div>
                <div className="bg-white p-2 rounded-lg shadow-sm border border-gray-100 flex items-center gap-2">
                    <Calendar size={20} className="text-green-600" />
                    <span className="text-sm font-medium text-gray-700">
                        {new Date().toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })}
                    </span>
                </div>
            </header>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <SummaryCard
                    title="Total Produtores"
                    value={data.summary.totalProducers}
                    icon={<Users className="text-blue-600" />}
                    trend="+5% este mês"
                    color="blue"
                    to="/produtores"
                />
                <SummaryCard
                    title="Serviços Ativos"
                    value={data.summary.totalServices}
                    icon={<ClipboardList className="text-green-600" />}
                    trend="Estável"
                    color="green"
                    to="/servicos"
                />
                <SummaryCard
                    title="Pendências"
                    value={data.summary.pendingExecutions}
                    icon={<AlertCircle className="text-orange-600" />}
                    trend={`${data.summary.pendingExecutions} aguardando`}
                    color="orange"
                    to="/execucoes"
                />
                <SummaryCard
                    title="Total Recebido"
                    value={`R$ ${data.summary.totalPaidAmount.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
                    icon={<DollarSign className="text-purple-600" />}
                    trend="Crescimento constante"
                    color="purple"
                    to="/pagamentos"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Financial Flow Chart */}
                <div className="lg:col-span-2 bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-xl font-bold text-gray-800">Fluxo Financeiro Mensal</h2>
                        <div className="flex gap-4">
                            <div className="flex items-center gap-2">
                                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                                <span className="text-xs text-gray-500 font-medium">Pago</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="w-3 h-3 rounded-full bg-orange-400"></div>
                                <span className="text-xs text-gray-500 font-medium">Pendente</span>
                            </div>
                        </div>
                    </div>

                    <div className="h-64 flex items-end gap-3 pb-8 relative">
                        {data.monthlyFinancial.length > 0 ? (
                            data.monthlyFinancial.map((item, index) => {
                                const total = item.paid + item.pending || 1;
                                const paidHeight = (item.paid / total) * 100;
                                const pendingHeight = (item.pending / total) * 100;

                                return (
                                    <div key={index} className="flex-1 flex flex-col items-center gap-2 group">
                                        <div className="w-full flex flex-col justify-end gap-0.5 h-full">
                                            <div
                                                className="w-full bg-orange-400 rounded-t-sm transition-all duration-300 group-hover:opacity-80"
                                                style={{ height: `${pendingHeight}%` }}
                                                title={`Pendente: R$ ${item.pending}`}
                                            ></div>
                                            <div
                                                className="w-full bg-green-500 rounded-b-sm transition-all duration-300 group-hover:opacity-80"
                                                style={{ height: `${paidHeight}%` }}
                                                title={`Pago: R$ ${item.paid}`}
                                            ></div>
                                        </div>
                                        <span className="text-[10px] text-gray-400 font-medium uppercase">{item.month}</span>
                                    </div>
                                );
                            })
                        ) : (
                            <div className="w-full h-full flex items-center justify-center text-gray-400 italic">
                                Nenhum dado financeiro disponível
                            </div>
                        )}
                        <div className="absolute inset-0 flex flex-col justify-between pointer-events-none -z-10 opacity-5">
                            {[1, 2, 3, 4].map(i => <div key={i} className="border-t border-gray-900 w-full"></div>)}
                        </div>
                    </div>
                </div>

                {/* Recent Activities */}
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                    <h2 className="text-xl font-bold text-gray-800 mb-6">Atividades Recentes</h2>
                    <div className="space-y-4">
                        {data.recentActivities.length > 0 ? (
                            data.recentActivities.map((activity) => (
                                <div key={activity.id} className="flex gap-4 p-3 hover:bg-gray-50 rounded-xl transition-colors">
                                    <div className={`p-2 rounded-lg shrink-0 ${activity.type === 'Agendamento' ? 'bg-blue-50 text-blue-600' : 'bg-green-50 text-green-600'
                                        }`}>
                                        {activity.type === 'Agendamento' ? <ClipboardList size={20} /> : <DollarSign size={20} />}
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm font-semibold text-gray-800 truncate">{activity.description}</p>
                                        <div className="flex items-center gap-2 mt-0.5">
                                            <span className="text-xs text-gray-400">{new Date(activity.date).toLocaleDateString('pt-BR')}</span>
                                            <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${activity.status === 'Pendente' ? 'bg-orange-50 text-orange-600' : 'bg-green-50 text-green-600'
                                                }`}>
                                                {activity.status}
                                            </span>
                                        </div>
                                    </div>
                                    {activity.amount && (
                                        <div className="text-sm font-bold text-gray-700 whitespace-nowrap">
                                            R$ {activity.amount.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                                        </div>
                                    )}
                                </div>
                            ))
                        ) : (
                            <div className="text-center py-8 text-gray-400 italic">Nenhuma atividade recente encontrada</div>
                        )}
                    </div>
                    <Link
                        to="/agendamentos"
                        className="block w-full mt-6 py-2.5 text-center text-sm font-semibold text-green-600 bg-green-50 rounded-xl hover:bg-green-100 transition-colors"
                    >
                        Ver todas as atividades
                    </Link>
                </div>
            </div>

            {/* Service Distribution */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                <h2 className="text-xl font-bold text-gray-800 mb-6">Distribuição por Serviço</h2>
                <div className="flex flex-wrap gap-4">
                    {data.serviceDistribution.length > 0 ? (
                        data.serviceDistribution.map((service, index) => (
                            <div key={index} className="flex-1 min-w-[200px] p-4 bg-gray-50 rounded-xl border border-gray-100 flex items-center justify-between">
                                <div>
                                    <p className="text-sm text-gray-500 font-medium mb-1">{service.name}</p>
                                    <p className="text-2xl font-bold text-gray-800">{service.value}</p>
                                </div>
                                <div className="p-3 bg-white rounded-full shadow-sm">
                                    <TrendingUp size={24} className="text-green-500" />
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className="w-full text-center py-4 text-gray-400 italic">Nenhuma distribuição de serviço encontrada</div>
                    )}
                </div>
            </div>
        </div>
    );
};

interface SummaryCardProps {
    title: string;
    value: string | number;
    icon: React.ReactNode;
    trend: string;
    color: 'blue' | 'green' | 'orange' | 'purple';
    to: string;
}

const SummaryCard: React.FC<SummaryCardProps> = ({ title, value, icon, trend, color, to }) => {
    const colorMap = {
        blue: 'bg-blue-50',
        green: 'bg-green-50',
        orange: 'bg-orange-50',
        purple: 'bg-purple-50',
    };

    return (
        <Link to={to} className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow relative overflow-hidden group block">
            <div className="absolute top-0 right-0 p-8 opacity-5 transform translate-x-4 -translate-y-4 group-hover:scale-110 transition-transform">
                {icon}
            </div>
            <div className="flex items-center gap-4 mb-4">
                <div className={`p-3 rounded-xl ${colorMap[color]}`}>
                    {icon}
                </div>
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider">{title}</h3>
            </div>
            <div>
                <p className="text-3xl font-extrabold text-gray-800 tracking-tight">{value}</p>
                <div className="flex items-center gap-1 mt-2">
                    <ArrowUpRight size={14} className="text-green-500" />
                    <span className="text-xs font-bold text-green-500">{trend}</span>
                </div>
            </div>
        </Link>
    );
};
