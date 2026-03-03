import React, { useEffect, useState } from "react";
import { Execution } from "../domain/Execution";
import { ExecutionRepository } from "../data/ExecutionRepository";
import { ProducerRepository } from "../../producers/data/ProducerRepository";
import { ServiceRepository } from "../../services/data/ServiceRepository";
import { Producer } from "../../producers/domain/Producer";
import { AgriculturalService } from "../../services/domain/AgriculturalService";
import { Button } from "../../../shared/components/Button";
import { DataTable } from "../../../shared/components/DataTable";
import { Modal } from "../../../shared/components/Modal";
import { CalendarPlus, Search, Edit } from "lucide-react";

const repository = new ExecutionRepository();
const producerRepository = new ProducerRepository();
const serviceRepository = new ServiceRepository();

export function ExecutionsPage() {
  const [executions, setExecutions] = useState<Execution[]>([]);
  const [producersList, setProducersList] = useState<Producer[]>([]);
  const [servicesList, setServicesList] = useState<AgriculturalService[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  // Form State
  const [formData, setFormData] = useState({
    producerId: "",
    serviceId: "",
    date: new Date().toISOString().split("T")[0],
    quantity: 0,
    totalValue: 0,
    status: "Agendado" as "Agendado" | "Em Andamento" | "Concluído" | "Cancelado",
  });

  const fetchExecutions = async () => {
    setLoading(true);
    const [data, producersData, servicesData] = await Promise.all([
      repository.getExecutions(),
      producerRepository.getProducers(),
      serviceRepository.getServices(),
    ]);
    setExecutions(data);
    setProducersList(producersData.filter(p => p.status === "Ativo"));
    setServicesList(servicesData.filter(s => s.active));
    setLoading(false);
  };

  useEffect(() => {
    fetchExecutions();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    
    setFormData((prev) => {
      const newData = { 
        ...prev, 
        [name]: name === "quantity" || name === "totalValue" ? parseFloat(value) || 0 : value 
      };

      // Auto-calculate total value if service or quantity changes
      if (name === "serviceId" || name === "quantity") {
        const serviceId = name === "serviceId" ? value : prev.serviceId;
        const quantity = name === "quantity" ? (parseFloat(value) || 0) : prev.quantity;
        const service = servicesList.find(s => s.id === serviceId);
        
        if (service) {
          newData.totalValue = service.basePrice * quantity;
        }
      }

      return newData;
    });
  };

  const handleNewClick = () => {
    setFormData({
      producerId: producersList[0]?.id || "",
      serviceId: servicesList[0]?.id || "",
      date: new Date().toISOString().split("T")[0],
      quantity: 1,
      totalValue: servicesList[0]?.basePrice || 0,
      status: "Agendado",
    });
    setEditingId(null);
    setIsModalOpen(true);
  };

  const handleEditClick = (execution: Execution) => {
    setFormData({
      producerId: execution.producerId,
      serviceId: execution.serviceId,
      date: execution.date,
      quantity: execution.quantity,
      totalValue: execution.totalValue,
      status: execution.status,
    });
    setEditingId(execution.id);
    setIsModalOpen(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    const selectedProducer = producersList.find(p => p.id === formData.producerId);
    const selectedService = servicesList.find(s => s.id === formData.serviceId);

    const executionData = {
      ...formData,
      producerName: selectedProducer?.name || "Desconhecido",
      serviceName: selectedService?.name || "Desconhecido",
      unit: selectedService?.unit || "Unidade",
    };

    if (editingId) {
      await repository.updateExecution(editingId, executionData);
    } else {
      await repository.addExecution(executionData);
    }
    
    await fetchExecutions(); // Refresh list
    
    setIsSubmitting(false);
    setIsModalOpen(false);
    setEditingId(null);
  };

  const filteredExecutions = executions.filter((e) =>
    e.producerName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    e.serviceName.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Concluído":
        return "bg-green-100 text-green-800 border-green-300";
      case "Em Andamento":
        return "bg-blue-100 text-blue-800 border-blue-300";
      case "Agendado":
        return "bg-yellow-100 text-yellow-800 border-yellow-300";
      case "Cancelado":
        return "bg-red-100 text-red-800 border-red-300";
      default:
        return "bg-gray-100 text-gray-800 border-gray-300";
    }
  };

  const columns = [
    {
      header: "Data",
      accessorKey: "date",
      cell: (item: Execution) => {
        const date = new Date(item.date);
        // Adjust for timezone offset to display correct date
        date.setMinutes(date.getMinutes() + date.getTimezoneOffset());
        return new Intl.DateTimeFormat("pt-BR").format(date);
      },
    },
    { header: "Produtor", accessorKey: "producerName" },
    { header: "Serviço", accessorKey: "serviceName" },
    {
      header: "Quantidade",
      accessorKey: "quantity",
      cell: (item: Execution) => `${item.quantity} ${item.unit}`,
    },
    {
      header: "Valor Total",
      accessorKey: "totalValue",
      cell: (item: Execution) => (
        <span className="font-mono font-bold text-gray-900">
          {new Intl.NumberFormat("pt-BR", {
            style: "currency",
            currency: "BRL",
          }).format(item.totalValue)}
        </span>
      ),
    },
    {
      header: "Status",
      accessorKey: "status",
      cell: (item: Execution) => (
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
      cell: (item: Execution) => (
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={(e) => {
            e.stopPropagation();
            handleEditClick(item);
          }}
          className="h-8 w-8 p-0 text-blue-600 hover:text-blue-800 hover:bg-blue-50"
          title="Editar Execução"
        >
          <Edit className="h-4 w-4" />
        </Button>
      ),
    }
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-gray-300 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">Execuções e Agendamentos</h1>
          <p className="text-lg text-gray-600 mt-2">Acompanhe os serviços prestados e agendados para os produtores.</p>
        </div>
        <Button size="lg" className="shrink-0 gap-2" onClick={handleNewClick}>
          <CalendarPlus className="h-5 w-5" />
          Novo Agendamento
        </Button>
      </div>

      <div className="flex items-center gap-4 bg-white p-4 rounded-lg border border-gray-300 shadow-sm">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500" />
          <input
            type="text"
            placeholder="Buscar por produtor ou serviço..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="h-12 w-full rounded-md border border-gray-300 pl-12 pr-4 text-base font-medium text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {loading ? (
        <div className="flex h-64 items-center justify-center rounded-lg border border-gray-300 bg-white">
          <div className="text-xl font-bold text-gray-500 animate-pulse">Carregando execuções...</div>
        </div>
      ) : (
        <DataTable data={filteredExecutions} columns={columns} />
      )}

      <Modal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        title={editingId ? "Editar Agendamento" : "Novo Agendamento"}
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label htmlFor="producerId" className="block text-sm font-bold text-gray-900">Produtor</label>
              <select
                id="producerId"
                name="producerId"
                required
                value={formData.producerId}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 bg-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="" disabled>Selecione um produtor</option>
                {producersList.map(p => (
                  <option key={p.id} value={p.id}>{p.name} ({p.property})</option>
                ))}
              </select>
            </div>
            
            <div className="space-y-2">
              <label htmlFor="serviceId" className="block text-sm font-bold text-gray-900">Serviço</label>
              <select
                id="serviceId"
                name="serviceId"
                required
                value={formData.serviceId}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 bg-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="" disabled>Selecione um serviço</option>
                {servicesList.map(s => (
                  <option key={s.id} value={s.id}>{s.name} - R$ {s.basePrice}/{s.unit}</option>
                ))}
              </select>
            </div>

            <div className="space-y-2">
              <label htmlFor="date" className="block text-sm font-bold text-gray-900">Data do Serviço</label>
              <input
                id="date"
                name="date"
                type="date"
                required
                value={formData.date}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="quantity" className="block text-sm font-bold text-gray-900">
                Quantidade ({servicesList.find(s => s.id === formData.serviceId)?.unit || "Unidade"})
              </label>
              <input
                id="quantity"
                name="quantity"
                type="number"
                step="0.01"
                min="0.01"
                required
                value={formData.quantity}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="totalValue" className="block text-sm font-bold text-gray-900">Valor Total (R$)</label>
              <input
                id="totalValue"
                name="totalValue"
                type="number"
                step="0.01"
                min="0"
                required
                value={formData.totalValue}
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
                <option value="Agendado">Agendado</option>
                <option value="Em Andamento">Em Andamento</option>
                <option value="Concluído">Concluído</option>
                <option value="Cancelado">Cancelado</option>
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
              {isSubmitting ? "Salvando..." : "Salvar Agendamento"}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
