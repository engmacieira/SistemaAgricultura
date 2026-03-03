import React, { useEffect, useState } from "react";
import { Payment } from "../domain/Payment";
import { PaymentRepository } from "../data/PaymentRepository";
import { Button } from "../../../shared/components/Button";
import { DataTable } from "../../../shared/components/DataTable";
import { Modal } from "../../../shared/components/Modal";
import { Search, DollarSign, Edit } from "lucide-react";

const repository = new PaymentRepository();

export function PaymentsPage() {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [modalTitle, setModalTitle] = useState("");

  // Form State
  const [formData, setFormData] = useState({
    dueDate: "",
    paymentDate: "",
    amount: 0,
    status: "Pendente" as "Pendente" | "Pago" | "Atrasado",
  });

  const fetchPayments = async () => {
    setLoading(true);
    const data = await repository.getPayments();
    setPayments(data);
    setLoading(false);
  };

  useEffect(() => {
    fetchPayments();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ 
      ...prev, 
      [name]: name === "amount" ? parseFloat(value) || 0 : value 
    }));
  };

  const handleRegisterPaymentClick = (payment: Payment) => {
    setFormData({
      dueDate: payment.dueDate,
      paymentDate: new Date().toISOString().split("T")[0],
      amount: payment.amount,
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
      status: payment.status,
    });
    setEditingId(payment.id);
    setModalTitle("Editar Pagamento");
    setIsModalOpen(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    if (editingId) {
      await repository.updatePayment(editingId, {
        ...formData,
        paymentDate: formData.paymentDate || undefined,
      });
    }
    
    await fetchPayments(); // Refresh list
    
    setIsSubmitting(false);
    setIsModalOpen(false);
    setEditingId(null);
  };

  const filteredPayments = payments.filter((p) =>
    p.producerName.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Pago":
        return "bg-green-100 text-green-800 border-green-300";
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
        const date = new Date(item.dueDate);
        date.setMinutes(date.getMinutes() + date.getTimezoneOffset());
        return new Intl.DateTimeFormat("pt-BR").format(date);
      },
    },
    {
      header: "Data Pagamento",
      accessorKey: "paymentDate",
      cell: (item: Payment) => {
        if (!item.paymentDate) return "-";
        const date = new Date(item.paymentDate);
        date.setMinutes(date.getMinutes() + date.getTimezoneOffset());
        return new Intl.DateTimeFormat("pt-BR").format(date);
      },
    },
    {
      header: "Valor",
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
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={(e) => {
              e.stopPropagation();
              handleEditClick(item);
            }}
            className="h-8 w-8 p-0 text-blue-600 hover:text-blue-800 hover:bg-blue-50"
            title="Editar Pagamento"
          >
            <Edit className="h-4 w-4" />
          </Button>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-gray-300 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">Controle de Pagamentos</h1>
          <p className="text-lg text-gray-600 mt-2">Gerencie os recebimentos dos serviços prestados.</p>
        </div>
        <Button size="lg" className="shrink-0 gap-2">
          <DollarSign className="h-5 w-5" />
          Novo Recebimento
        </Button>
      </div>

      <div className="flex items-center gap-4 bg-white p-4 rounded-lg border border-gray-300 shadow-sm">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500" />
          <input
            type="text"
            placeholder="Buscar por produtor..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="h-12 w-full rounded-md border border-gray-300 pl-12 pr-4 text-base font-medium text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {loading ? (
        <div className="flex h-64 items-center justify-center rounded-lg border border-gray-300 bg-white">
          <div className="text-xl font-bold text-gray-500 animate-pulse">Carregando pagamentos...</div>
        </div>
      ) : (
        <DataTable data={filteredPayments} columns={columns} />
      )}

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
              <label htmlFor="amount" className="block text-sm font-bold text-gray-900">Valor (R$)</label>
              <input
                id="amount"
                name="amount"
                type="number"
                step="0.01"
                min="0"
                required
                value={formData.amount}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="status" className="block text-sm font-bold text-gray-900">Status</label>
              <select
                id="status"
                name="status"
                value={formData.status}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 bg-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="Pendente">Pendente</option>
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
              {isSubmitting ? "Salvar" : "Salvar"}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
