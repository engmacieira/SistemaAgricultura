import React, { useEffect, useState } from "react";
import { Request } from "../domain/Request";
import { RequestRepository } from "../data/RequestRepository";
import { ExecutionRepository } from "../../executions/data/ExecutionRepository";
import { ProducerRepository } from "../../producers/data/ProducerRepository";
import { ServiceRepository } from "../../services/data/ServiceRepository";
import { Producer } from "../../producers/domain/Producer";
import { AgriculturalService } from "../../services/domain/AgriculturalService";
import { Button } from "../../../shared/components/Button";
import { Modal } from "../../../shared/components/Modal";
import { Plus, CheckCircle, Clock, XCircle, Play, AlertTriangle } from "lucide-react";

const requestRepository = new RequestRepository();
const executionRepository = new ExecutionRepository();
const producerRepository = new ProducerRepository();
const serviceRepository = new ServiceRepository();

type TabStatus = "PENDENTE" | "EM_ANDAMENTO" | "CONCLUIDO" | "CANCELADO";

export function RequestsPage() {
    const [requests, setRequests] = useState<Request[]>([]);
    const [producersList, setProducersList] = useState<Producer[]>([]);
    const [servicesList, setServicesList] = useState<AgriculturalService[]>([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState<TabStatus>("PENDENTE");

    // Modais
    const [isRequestModalOpen, setIsRequestModalOpen] = useState(false);
    const [isExecutionModalOpen, setIsExecutionModalOpen] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Pedido selecionado para Dar Baixa
    const [selectedRequest, setSelectedRequest] = useState<Request | null>(null);

    // Form State (Nova Solicitação)
    const [requestForm, setRequestForm] = useState({
        producerId: "",
        data_solicitacao: new Date().toISOString().split("T")[0],
        prioridade: 1,
        observacoes: "",
    });

    // Form State (Dar Baixa / Execução)
    const [executionForm, setExecutionForm] = useState({
        serviceId: "",
        date: new Date().toISOString().split("T")[0],
        quantity: 1,
        unit: "Horas",
        valor_unitario: 0,
        operador_maquina: "",
    });

    const fetchData = async () => {
        setLoading(true);
        try {
            // ✅ Busca os pedidos da fila baseados na aba atual
            const data = await requestRepository.getRequests({ status_filtro: activeTab });
            setRequests(data);

            // Carrega dependências apenas se estiverem vazias
            if (producersList.length === 0) {
                const prods = await producerRepository.getProducers(0, 1000);
                setProducersList(prods.items || prods || []);
            }
            if (servicesList.length === 0) {
                const servs = await serviceRepository.getServices(0, 1000);
                setServicesList(servs.items || servs || []);
            }
        } catch (error) {
            console.error("Erro ao buscar dados:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, [activeTab]);

    // --- HANDLERS DA FILA DE ESPERA ---
    const handleRequestSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        try {
            const producer = producersList.find(p => p.id === requestForm.producerId);
            await requestRepository.addRequest({
                ...requestForm,
                producerName: producer?.name || "Desconhecido"
            });
            setIsRequestModalOpen(false);
            fetchData();
        } catch (error) {
            console.error("Erro ao salvar:", error);
        } finally {
            setIsSubmitting(false);
        }
    };

    const mudarStatus = async (id: string, novoStatus: TabStatus) => {
        try {
            await requestRepository.updateRequest(id, { status: novoStatus });
            fetchData();
        } catch (error) {
            console.error("Erro ao mudar status:", error);
        }
    };

    // --- HANDLERS DE EXECUÇÃO (DAR BAIXA) ---
    const openExecutionModal = (request: Request) => {
        setSelectedRequest(request);
        setIsExecutionModalOpen(true);
    };

    const handleExecutionSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        try {
            const service = servicesList.find(s => s.id === executionForm.serviceId);
            // Calcula o valor total antes de enviar
            const totalValue = executionForm.quantity * executionForm.valor_unitario;

            await executionRepository.addExecution({
                solicitacaoId: selectedRequest!.id,
                serviceId: executionForm.serviceId,
                serviceName: service?.name || "Desconhecido",
                date: executionForm.date,
                quantity: executionForm.quantity,
                unit: executionForm.unit,
                valor_unitario: executionForm.valor_unitario,
                totalValue: totalValue,
                status: "REGISTRADA",
                operador_maquina: executionForm.operador_maquina,
            });

            // A nossa regra no backend já muda o status para CONCLUIDO e gera o pagamento!
            setIsExecutionModalOpen(false);
            // Voltamos a aba para Concluído para o usuário ver a mágica feita
            setActiveTab("CONCLUIDO");
        } catch (error) {
            console.error("Erro ao dar baixa:", error);
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleServiceSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const sId = e.target.value;
        const serv = servicesList.find(s => s.id === sId);
        setExecutionForm({
            ...executionForm,
            serviceId: sId,
            unit: serv?.unit || "Horas",
            valor_unitario: serv?.basePrice || 0
        });
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Fila de Espera (Serviços)</h1>
                    <p className="text-gray-500">Gerencie as solicitações dos produtores e dê baixa nos serviços.</p>
                </div>
                <Button onClick={() => setIsRequestModalOpen(true)}>
                    <Plus className="w-4 h-4 mr-2" />
                    Nova Solicitação
                </Button>
            </div>

            {/* --- NAVEGAÇÃO POR ABAS --- */}
            <div className="border-b border-gray-200">
                <nav className="-mb-px flex space-x-8">
                    {[
                        { id: "PENDENTE", label: "Pendentes", icon: Clock },
                        { id: "EM_ANDAMENTO", label: "Em Andamento", icon: Play },
                        { id: "CONCLUIDO", label: "Concluídos", icon: CheckCircle },
                        { id: "CANCELADO", label: "Cancelados", icon: XCircle },
                    ].map((tab) => {
                        const Icon = tab.icon;
                        const isActive = activeTab === tab.id;
                        return (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id as TabStatus)}
                                className={`
                  flex items-center whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm
                  ${isActive
                                        ? "border-blue-500 text-blue-600"
                                        : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"}
                `}
                            >
                                <Icon className={`w-5 h-5 mr-2 ${isActive ? "text-blue-500" : "text-gray-400"}`} />
                                {tab.label}
                            </button>
                        );
                    })}
                </nav>
            </div>

            {/* --- LISTAGEM DE CARDS --- */}
            {loading ? (
                <div className="text-center py-10 text-gray-500">Carregando fila...</div>
            ) : requests.length === 0 ? (
                <div className="text-center py-10 text-gray-500 bg-white rounded-lg shadow border border-gray-100">
                    Nenhuma solicitação encontrada nesta aba.
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {requests.map((req) => (
                        <div key={req.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 flex flex-col">
                            <div className="flex justify-between items-start mb-4">
                                <h3 className="text-lg font-bold text-gray-900">{req.producerName}</h3>
                                {req.prioridade === 2 && (
                                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                        <AlertTriangle className="w-3 h-3 mr-1" /> Urgente
                                    </span>
                                )}
                            </div>

                            <div className="text-sm text-gray-600 space-y-2 flex-grow">
                                <p><strong>Data do Pedido:</strong> {new Date(req.data_solicitacao).toLocaleDateString()}</p>
                                {req.observacoes && (
                                    <p className="bg-gray-50 p-2 rounded border border-gray-100 mt-2">
                                        <span className="font-semibold block mb-1">Obs da Secretaria:</span>
                                        {req.observacoes}
                                    </p>
                                )}
                            </div>

                            {/* Botões de Ação Dinâmicos baseados na Aba */}
                            <div className="mt-6 pt-4 border-t border-gray-100 flex gap-2">
                                {activeTab === "PENDENTE" && (
                                    <>
                                        <Button variant="outline" className="flex-1" onClick={() => mudarStatus(req.id, "EM_ANDAMENTO")}>
                                            Iniciar
                                        </Button>
                                        <Button variant="ghost" className="text-red-600" onClick={() => mudarStatus(req.id, "CANCELADO")}>
                                            Cancelar
                                        </Button>
                                    </>
                                )}

                                {activeTab === "EM_ANDAMENTO" && (
                                    <Button className="w-full bg-green-600 hover:bg-green-700" onClick={() => openExecutionModal(req)}>
                                        <CheckCircle className="w-4 h-4 mr-2" />
                                        Dar Baixa no Serviço
                                    </Button>
                                )}

                                {activeTab === "CONCLUIDO" && (
                                    <p className="text-sm text-green-600 font-medium w-full text-center">
                                        ✓ Serviço faturado com sucesso.
                                    </p>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* --- MODAL: CRIAR SOLICITAÇÃO (FILA) --- */}
            <Modal isOpen={isRequestModalOpen} onClose={() => setIsRequestModalOpen(false)} title="Nova Solicitação na Fila">
                <form onSubmit={handleRequestSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Produtor</label>
                        <select
                            required
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                            value={requestForm.producerId}
                            onChange={(e) => setRequestForm({ ...requestForm, producerId: e.target.value })}
                        >
                            <option value="">Selecione um produtor</option>
                            {producersList.map((p) => (
                                <option key={p.id} value={p.id}>{p.name}</option>
                            ))}
                        </select>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Data do Pedido</label>
                            <input
                                type="date"
                                required
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                value={requestForm.data_solicitacao}
                                onChange={(e) => setRequestForm({ ...requestForm, data_solicitacao: e.target.value })}
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Prioridade</label>
                            <select
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                value={requestForm.prioridade}
                                onChange={(e) => setRequestForm({ ...requestForm, prioridade: Number(e.target.value) })}
                            >
                                <option value={1}>Normal</option>
                                <option value={2}>Urgente</option>
                            </select>
                        </div>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Observações (O que ele precisa?)</label>
                        <textarea
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                            rows={3}
                            value={requestForm.observacoes}
                            onChange={(e) => setRequestForm({ ...requestForm, observacoes: e.target.value })}
                        />
                    </div>
                    <div className="flex justify-end gap-2 mt-6">
                        <Button type="button" variant="ghost" onClick={() => setIsRequestModalOpen(false)}>Cancelar</Button>
                        <Button type="submit" disabled={isSubmitting}>{isSubmitting ? "Salvando..." : "Adicionar à Fila"}</Button>
                    </div>
                </form>
            </Modal>

            {/* --- MODAL: DAR BAIXA (CRIAR EXECUÇÃO) --- */}
            <Modal isOpen={isExecutionModalOpen} onClose={() => setIsExecutionModalOpen(false)} title="Dar Baixa em Serviço">
                <form onSubmit={handleExecutionSubmit} className="space-y-4">
                    <div className="bg-blue-50 p-3 rounded border border-blue-100 mb-4">
                        <p className="text-sm text-blue-800">
                            <strong>Faturando serviço para:</strong> {selectedRequest?.producerName}
                        </p>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700">Qual serviço foi realizado?</label>
                        <select
                            required
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                            value={executionForm.serviceId}
                            onChange={handleServiceSelect}
                        >
                            <option value="">Selecione um serviço</option>
                            {servicesList.map((s) => (
                                <option key={s.id} value={s.id}>{s.name} ({s.unit}) - R$ {s.basePrice}</option>
                            ))}
                        </select>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Data Realizada</label>
                            <input
                                type="date"
                                required
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                value={executionForm.date}
                                onChange={(e) => setExecutionForm({ ...executionForm, date: e.target.value })}
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Operador / Máquina</label>
                            <input
                                type="text"
                                placeholder="Ex: João / Trator 01"
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                value={executionForm.operador_maquina}
                                onChange={(e) => setExecutionForm({ ...executionForm, operador_maquina: e.target.value })}
                            />
                        </div>
                    </div>

                    <div className="grid grid-cols-3 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Qtd.</label>
                            <input
                                type="number"
                                step="0.01"
                                required
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                value={executionForm.quantity}
                                onChange={(e) => setExecutionForm({ ...executionForm, quantity: Number(e.target.value) })}
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Unidade</label>
                            <input type="text" disabled className="mt-1 block w-full rounded-md border-gray-200 bg-gray-50" value={executionForm.unit} />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Valor Unit. (R$)</label>
                            <input
                                type="number"
                                step="0.01"
                                required
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                value={executionForm.valor_unitario}
                                onChange={(e) => setExecutionForm({ ...executionForm, valor_unitario: Number(e.target.value) })}
                            />
                        </div>
                    </div>

                    <div className="mt-4 p-4 bg-gray-50 rounded text-right">
                        <span className="text-gray-600">Total a Faturar: </span>
                        <span className="text-xl font-bold text-gray-900">
                            R$ {(executionForm.quantity * executionForm.valor_unitario).toFixed(2)}
                        </span>
                    </div>

                    <div className="flex justify-end gap-2 mt-6">
                        <Button type="button" variant="ghost" onClick={() => setIsExecutionModalOpen(false)}>Cancelar</Button>
                        <Button type="submit" disabled={isSubmitting} className="bg-green-600 hover:bg-green-700">
                            {isSubmitting ? "Processando..." : "Confirmar e Gerar Pagamento"}
                        </Button>
                    </div>
                </form>
            </Modal>
        </div>
    );
}