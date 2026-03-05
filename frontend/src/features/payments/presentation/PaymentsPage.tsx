import React, { useEffect, useState, useCallback } from "react";
import { PaymentRepository } from "../data/PaymentRepository";
import { Button } from "../../../shared/components/Button";
import { DataTable } from "../../../shared/components/DataTable";
import { Modal } from "../../../shared/components/Modal";
import { Pagination } from "../../../shared/components/Pagination";
import { Search, DollarSign, Edit, History, Trash2, FileText, ChevronDown, ChevronUp } from "lucide-react";
import { Payment, PaymentTransaction } from "../domain/Payment";

const repository = new PaymentRepository();

export function PaymentsPage() {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [page, setPage] = useState(0);
  const [sortConfig, setSortConfig] = useState<{ sortBy: string; order: "asc" | "desc" }>({
    sortBy: "dueDate",
    order: "desc",
  });

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [modalTitle, setModalTitle] = useState("");

  // History Modal State
  const [isHistoryModalOpen, setIsHistoryModalOpen] = useState(false);
  const [history, setHistory] = useState<PaymentTransaction[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [selectedPaymentName, setSelectedPaymentName] = useState("");
  const [selectedPaymentId, setSelectedPaymentId] = useState<string | null>(null);

  // Transaction Edit State
  const [editingTransaction, setEditingTransaction] = useState<PaymentTransaction | null>(null);
  const [isTrxModalOpen, setIsTrxModalOpen] = useState(false);
  const [trxFormData, setTrxFormData] = useState({ amount: 0, date: "" });

  // Form State
  const [formData, setFormData] = useState({
    dueDate: "",
    paymentDate: "",
    amount: 0,
    paidAmount: 0,
    amountToPay: 0,
    status: "Pendente" as "Pendente" | "Parcial" | "Pago" | "Atrasado",
  });

  const fetchPayments = useCallback(async () => {
    setLoading(true);
    try {
      const data = await repository.getPayments(page, 10, sortConfig.sortBy, sortConfig.order, searchTerm);
      setPayments(data.items);
      setTotal(data.total);
    } catch (error) {
      console.error("Erro ao buscar pagamentos", error);
    } finally {
      setLoading(false);
    }
  }, [page, sortConfig, searchTerm]);

  useEffect(() => {
    fetchPayments();
  }, [fetchPayments]);

  const handleSort = (column: string) => {
    setSortConfig((prev) => ({
      sortBy: column,
      order: prev.sortBy === column && prev.order === "asc" ? "desc" : "asc",
    }));
    setPage(0);
  };

  const handlePageChange = (newPage: number) => {
    setPage(newPage);
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    setPage(0);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "amount" || name === "amountToPay" ? parseFloat(value) || 0 : value
    }));
  };

  const handleRegisterPaymentClick = (payment: Payment) => {
    const remaining = payment.amount - (payment.paidAmount || 0);
    setFormData({
      dueDate: payment.dueDate,
      paymentDate: new Date().toISOString().split("T")[0],
      amount: payment.amount,
      paidAmount: payment.paidAmount || 0,
      amountToPay: remaining,
      status: "Pago",
    });
    setEditingId(payment.id);
    setModalTitle("Registrar Pagamento");
    setIsModalOpen(true);
  };

  const handleEditClick = (payment: Payment) => {
    setFormData({
      dueDate: payment.dueDate,
      paymentDate: payment.paymentDate || "",
      amount: payment.amount,
      paidAmount: payment.paidAmount || 0,
      amountToPay: 0,
      status: payment.status,
    });
    setEditingId(payment.id);
    setModalTitle("Editar Pagamento");
    setIsModalOpen(true);
  };

  const handleDeleteClick = async (id: string) => {
    if (window.confirm("Tem certeza que deseja excluir este pagamento?")) {
      await repository.deletePayment(id);
      fetchPayments();
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      if (editingId) {
        if (modalTitle === "Registrar Pagamento") {
          await repository.payPayment(editingId, formData.amountToPay, formData.paymentDate || undefined);
        } else {
          await repository.updatePayment(editingId, {
            ...formData,
            paymentDate: formData.paymentDate || undefined,
          });
        }
      }
      setIsModalOpen(false);
      setEditingId(null);
      fetchPayments();
    } catch (error) {
      console.error("Erro ao salvar pagamento", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleViewHistory = async (payment: Payment) => {
    setSelectedPaymentName(payment.producerName);
    setSelectedPaymentId(payment.id);
    setHistoryLoading(true);
    setIsHistoryModalOpen(true);
    try {
      const data = await repository.getPaymentHistory(payment.id);
      setHistory(data);
    } catch (error) {
      console.error("Erro ao carregar histórico", error);
    } finally {
      setHistoryLoading(false);
    }
  };

  const refreshHistory = async () => {
    if (!selectedPaymentId) return;
    setHistoryLoading(true);
    try {
      const data = await repository.getPaymentHistory(selectedPaymentId);
      setHistory(data);
      fetchPayments(); // Sync main list totals
    } catch (error) {
      console.error("Erro ao recarregar histórico", error);
    } finally {
      setHistoryLoading(false);
    }
  };

  const handleEditTrx = (trx: PaymentTransaction) => {
    setEditingTransaction(trx);
    setTrxFormData({
      amount: trx.amount,
      date: trx.date
    });
    setIsTrxModalOpen(true);
  };

  const handleDeleteTrx = async (trxId: string) => {
    if (window.confirm("Deseja realmente excluir este registro de pagamento parcial?")) {
      try {
        await repository.deleteTransaction(trxId);
        refreshHistory();
      } catch (error) {
        console.error("Erro ao excluir transação", error);
      }
    }
  };

  const handleTrxSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingTransaction) return;

    try {
      await repository.updateTransaction(editingTransaction.id, trxFormData);
      setIsTrxModalOpen(false);
      refreshHistory();
    } catch (error) {
      console.error("Erro ao atualizar transação", error);
    }
  };

  // Report State
  const [isReportOpen, setIsReportOpen] = useState(false);
  const [reportData, setReportData] = useState<{ records: any[], totalGeneral: number } | null>(null);
  const [reportLoading, setReportLoading] = useState(false);
  const [reportSearchTerm, setReportSearchTerm] = useState("");

  const fetchReport = useCallback(async (search: string = "") => {
    setReportLoading(true);
    try {
      const data = await repository.getDebtsByProducer(search);
      setReportData(data);
    } catch (error) {
      console.error("Erro ao carregar relatório", error);
    } finally {
      setReportLoading(false);
    }
  }, []);

  const handleToggleReport = () => {
    if (!isReportOpen) {
      setReportSearchTerm("");
      fetchReport("");
    }
    setIsReportOpen(!isReportOpen);
  };

  const handleReportSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setReportSearchTerm(value);
    // Debounce or immediate? Let's do immediate for responsiveness since it's a specific search
    fetchReport(value);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Pago":
        return "bg-green-100 text-green-800 border-green-300";
      case "Parcial":
        return "bg-blue-100 text-blue-800 border-blue-300";
      case "Pendente":
        return "bg-yellow-100 text-yellow-800 border-yellow-300";
      case "Atrasado":
        return "bg-red-100 text-red-800 border-red-300";
      default:
        return "bg-gray-100 text-gray-800 border-gray-300";
    }
  };

  const columns = [
    { header: "Produtor", accessorKey: "producerName" },
    { header: "Serviço Ref.", accessorKey: "serviceName" },
    {
      header: "Vencimento",
      accessorKey: "dueDate",
      cell: (item: Payment) => {
        const date = new Date(item.dueDate + "T00:00:00");
        return new Intl.DateTimeFormat("pt-BR").format(date);
      },
    },
    {
      header: "Data Pagamento",
      accessorKey: "paymentDate",
      cell: (item: Payment) => {
        if (!item.paymentDate) return "-";
        const date = new Date(item.paymentDate + "T00:00:00");
        return new Intl.DateTimeFormat("pt-BR").format(date);
      },
    },
    {
      header: "Valor Total",
      accessorKey: "amount",
      cell: (item: Payment) => (
        <span className="font-mono font-bold text-gray-900">
          {new Intl.NumberFormat("pt-BR", {
            style: "currency",
            currency: "BRL",
          }).format(item.amount)}
        </span>
      ),
    },
    {
      header: "Valor Pago",
      accessorKey: "paidAmount",
      cell: (item: Payment) => (
        <button
          onClick={() => handleViewHistory(item)}
          className="flex items-center gap-1 font-mono font-medium text-green-700 hover:text-green-900 hover:underline transition-colors"
          title="Ver histórico de pagamentos"
        >
          {new Intl.NumberFormat("pt-BR", {
            style: "currency",
            currency: "BRL",
          }).format(item.paidAmount || 0)}
          <History className="h-3 w-3" />
        </button>
      ),
    },
    {
      header: "Saldo",
      accessorKey: "balance",
      cell: (item: Payment) => {
        const balance = item.amount - (item.paidAmount || 0);
        return (
          <span className={`font-mono font-bold ${balance > 0 ? "text-red-600" : "text-gray-500"}`}>
            {new Intl.NumberFormat("pt-BR", {
              style: "currency",
              currency: "BRL",
            }).format(balance)}
          </span>
        );
      },
    },
    {
      header: "Status",
      accessorKey: "status",
      cell: (item: Payment) => (
        <span
          className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wider border ${getStatusColor(
            item.status
          )}`}
        >
          {item.status}
        </span>
      ),
    },
    {
      header: "Ações",
      accessorKey: "actions",
      cell: (item: Payment) => (
        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            size="sm"
            disabled={item.status === "Pago"}
            onClick={(e) => {
              e.stopPropagation();
              handleRegisterPaymentClick(item);
            }}
          >
            Registrar Pagamento
          </Button>
        </div>
      ),
    },
  ];

  const totalPages = Math.ceil(total / 10);

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-gray-300 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">Controle de Pagamentos</h1>
          <p className="text-lg text-gray-600 mt-2">Gerencie os recebimentos dos serviços prestados.</p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="lg"
            className="shrink-0 gap-2 text-blue-700 border-blue-300"
            onClick={handleToggleReport}
          >
            <FileText className="h-5 w-5" />
            Relatório de Débitos
            {isReportOpen ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          </Button>
          <Button size="lg" className="shrink-0 gap-2">
            <DollarSign className="h-5 w-5" />
            Novo Recebimento
          </Button>
        </div>
      </div>

      {isReportOpen && (
        <div className="bg-blue-50 border border-blue-100 rounded-xl p-6 space-y-4 animate-in slide-in-from-top-4 duration-300">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <h2 className="text-xl font-bold text-blue-900 flex items-center gap-2">
              <FileText className="h-6 w-6" />
              Débitos em Aberto por Produtor
            </h2>
            <div className="relative max-w-sm w-full">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-blue-400" />
              <input
                type="text"
                placeholder="Filtrar por produtor no relatório..."
                value={reportSearchTerm}
                onChange={handleReportSearch}
                className="h-10 w-full rounded-md border border-blue-200 pl-10 pr-4 text-sm font-medium text-blue-900 placeholder-blue-300 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          {reportLoading ? (
            <div className="h-32 flex items-center justify-center">
              <span className="text-blue-600 animate-pulse font-medium">Gerando relatório...</span>
            </div>
          ) : reportData ? (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {reportData.records.map((record, idx) => (
                  <div key={idx} className="bg-white p-4 rounded-lg border border-blue-100 shadow-sm flex justify-between items-center">
                    <div>
                      <h3 className="font-bold text-gray-900">{record.producerName}</h3>
                      <p className="text-sm text-gray-500">{record.paymentCount} pagamento(s) pendente(s)</p>
                    </div>
                    <div className="text-right">
                      <span className="text-lg font-mono font-bold text-red-600">
                        {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(record.totalDebt)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
              <div className="bg-blue-900 text-white p-6 rounded-lg flex justify-between items-center shadow-md">
                <span className="text-xl font-bold italic tracking-wide">SOMATÓRIO TOTAL DE DÉBITOS</span>
                <span className="text-3xl font-mono font-extrabold">
                  {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(reportData.totalGeneral)}
                </span>
              </div>
            </div>
          ) : (
            <p className="text-blue-600 italic">Nenhum débito encontrado.</p>
          )}
        </div>
      )}

      <div className="flex items-center gap-4 bg-white p-4 rounded-lg border border-gray-300 shadow-sm">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500" />
          <input
            type="text"
            placeholder="Buscar por produtor..."
            value={searchTerm}
            onChange={handleSearchChange}
            className="h-12 w-full rounded-md border border-gray-300 pl-12 pr-4 text-base font-medium text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <div className="space-y-4">
        {loading ? (
          <div className="flex h-64 items-center justify-center rounded-lg border border-gray-300 bg-white shadow-inner">
            <div className="text-xl font-bold text-gray-500 animate-pulse">Carregando pagamentos...</div>
          </div>
        ) : (
          <>
            <DataTable
              data={payments}
              columns={columns}
              onSort={handleSort}
              sortConfig={sortConfig}
            />
            <Pagination
              currentPage={page}
              totalPages={totalPages}
              onPageChange={handlePageChange}
              className="mt-6"
            />
          </>
        )}
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={modalTitle}
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label htmlFor="dueDate" className="block text-sm font-bold text-gray-900">Data de Vencimento</label>
              <input
                id="dueDate"
                name="dueDate"
                type="date"
                required
                value={formData.dueDate}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="paymentDate" className="block text-sm font-bold text-gray-900">Data do Pagamento</label>
              <input
                id="paymentDate"
                name="paymentDate"
                type="date"
                value={formData.paymentDate}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="amount" className="block text-sm font-bold text-gray-900">
                {modalTitle === "Registrar Pagamento" ? "Valor Total (R$)" : "Valor (R$)"}
              </label>
              <input
                id="amount"
                name="amount"
                type="number"
                step="0.01"
                min="0"
                readOnly={modalTitle === "Registrar Pagamento"}
                required
                value={formData.amount}
                onChange={handleInputChange}
                className={`h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 ${modalTitle === "Registrar Pagamento" ? "bg-gray-100" : ""}`}
              />
            </div>

            {modalTitle === "Registrar Pagamento" && (
              <>
                <div className="space-y-2">
                  <label className="block text-sm font-bold text-gray-900">Já Pago (R$)</label>
                  <div className="h-12 w-full rounded-md border border-gray-300 px-4 flex items-center bg-gray-100 text-base font-medium text-green-700">
                    {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(formData.paidAmount)}
                  </div>
                </div>

                <div className="space-y-2">
                  <label htmlFor="amountToPay" className="block text-sm font-bold text-gray-900 text-blue-700">Valor a Pagar Agora (R$)</label>
                  <input
                    id="amountToPay"
                    name="amountToPay"
                    type="number"
                    step="0.01"
                    min="0.01"
                    max={formData.amount - formData.paidAmount}
                    required
                    value={formData.amountToPay}
                    onChange={handleInputChange}
                    className="h-12 w-full rounded-md border-2 border-blue-500 px-4 text-lg font-bold text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <p className="text-xs text-gray-500 italic">Saldo devedor: {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(formData.amount - formData.paidAmount)}</p>
                </div>
              </>
            )}

            <div className="space-y-2">
              <label htmlFor="status" className="block text-sm font-bold text-gray-900">Status</label>
              <select
                id="status"
                name="status"
                disabled={modalTitle === "Registrar Pagamento"}
                value={formData.status}
                onChange={handleInputChange}
                className={`h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 bg-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 ${modalTitle === "Registrar Pagamento" ? "bg-gray-100" : ""}`}
              >
                <option value="Pendente">Pendente</option>
                <option value="Parcial">Parcial</option>
                <option value="Pago">Pago</option>
                <option value="Atrasado">Atrasado</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end gap-4 pt-6 border-t border-gray-200 mt-8">
            <Button
              type="button"
              variant="ghost"
              onClick={() => setIsModalOpen(false)}
              disabled={isSubmitting}
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              disabled={isSubmitting}
            >
              {isSubmitting ? "Salvando..." : "Salvar Alterações"}
            </Button>
          </div>
        </form>
      </Modal>

      <Modal
        isOpen={isHistoryModalOpen}
        onClose={() => setIsHistoryModalOpen(false)}
        title={`Histórico de Pagamentos - ${selectedPaymentName}`}
      >
        <div className="space-y-4">
          {historyLoading ? (
            <div className="flex h-32 items-center justify-center">
              <div className="text-gray-500 animate-pulse font-bold">Carregando histórico...</div>
            </div>
          ) : history.length === 0 ? (
            <div className="text-center py-8 text-gray-500 italic">Nenhum pagamento registrado ainda.</div>
          ) : (
            <div className="overflow-hidden rounded-lg border border-gray-200">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-bold text-gray-900 uppercase tracking-wider">Data</th>
                    <th className="px-6 py-3 text-right text-xs font-bold text-gray-900 uppercase tracking-wider">Valor</th>
                    <th className="px-6 py-3 text-center text-xs font-bold text-gray-900 uppercase tracking-wider">Ações</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {history.map((tx) => (
                    <tr key={tx.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">
                        {new Intl.DateTimeFormat("pt-BR").format(new Date(tx.date + "T00:00:00"))}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-mono font-bold text-green-700">
                        {new Intl.NumberFormat("pt-BR", {
                          style: "currency",
                          currency: "BRL",
                        }).format(tx.amount)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                        <div className="flex items-center justify-center gap-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleEditTrx(tx)}
                            className="h-8 w-8 p-0 text-blue-600 hover:text-blue-800 hover:bg-blue-50"
                            title="Editar registro"
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDeleteTrx(tx.id)}
                            className="h-8 w-8 p-0 text-red-600 hover:text-red-800 hover:bg-red-50"
                            title="Excluir registro"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          <div className="flex justify-end pt-4">
            <Button onClick={() => setIsHistoryModalOpen(false)}>Fechar</Button>
          </div>
        </div>
      </Modal>

      <Modal
        isOpen={isTrxModalOpen}
        onClose={() => setIsTrxModalOpen(false)}
        title="Editar Registro de Pagamento"
      >
        <form onSubmit={handleTrxSubmit} className="space-y-6">
          <div className="grid grid-cols-1 gap-6">
            <div className="space-y-2">
              <label htmlFor="trxDate" className="block text-sm font-bold text-gray-900">Data do Pagamento</label>
              <input
                id="trxDate"
                type="date"
                required
                value={trxFormData.date}
                onChange={(e) => setTrxFormData(prev => ({ ...prev, date: e.target.value }))}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="trxAmount" className="block text-sm font-bold text-gray-900">Valor Pago (R$)</label>
              <input
                id="trxAmount"
                type="number"
                step="0.01"
                min="0.01"
                required
                value={trxFormData.amount}
                onChange={(e) => setTrxFormData(prev => ({ ...prev, amount: parseFloat(e.target.value) || 0 }))}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div className="flex justify-end gap-4 pt-6 border-t border-gray-200 mt-8">
            <Button
              type="button"
              variant="ghost"
              onClick={() => setIsTrxModalOpen(false)}
            >
              Cancelar
            </Button>
            <Button type="submit">
              Salvar Alterações
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
