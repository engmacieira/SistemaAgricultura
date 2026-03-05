import React, { useEffect, useState } from "react";
import { Execution } from "../domain/Execution";
import { ExecutionRepository } from "../data/ExecutionRepository";
import { ProducerRepository } from "../../producers/data/ProducerRepository";
import { ServiceRepository } from "../../services/data/ServiceRepository";
import { Producer } from "../../producers/domain/Producer";
import { AgriculturalService } from "../../services/domain/AgriculturalService";
import { Button } from "../../../shared/components/Button";
import { Modal } from "../../../shared/components/Modal";
import { Calendar as CalendarIcon, ChevronLeft, ChevronRight, Plus } from "lucide-react";
import { cn } from "../../../core/utils";

const repository = new ExecutionRepository();
const producerRepository = new ProducerRepository();
const serviceRepository = new ServiceRepository();

export function SchedulesPage() {
  const [executions, setExecutions] = useState<Execution[]>([]);
  const [producersList, setProducersList] = useState<Producer[]>([]);
  const [servicesList, setServicesList] = useState<AgriculturalService[]>([]);
  const [loading, setLoading] = useState(true);

  // Calendar State
  const [currentDate, setCurrentDate] = useState(new Date());

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  // Form State
  const [formData, setFormData] = useState({
    producerId: "",
    serviceId: "",
    date: new Date().toISOString().split("T")[0],
    quantity: 1,
    totalValue: 0,
    status: "Agendado" as "Agendado" | "Em Andamento" | "Concluído" | "Cancelado",
  });

  const fetchExecutions = async () => {
    setLoading(true);
    const [result, resultProducers, resultServices] = await Promise.all([
      repository.getExecutions({ limit: 1000, show_completed: true }), // Show all in calendar
      producerRepository.getProducers(1, 1000),
      serviceRepository.getServices(0, 1000),
    ]);
    setExecutions(result.items);
    setProducersList(resultProducers.items.filter(p => p.status === "Ativo"));
    setServicesList(resultServices.items.filter(s => s.active));
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

  const handleDayClick = (date: Date) => {
    // Adjust for local timezone to get YYYY-MM-DD
    const localDate = new Date(date.getTime() - (date.getTimezoneOffset() * 60000))
      .toISOString()
      .split("T")[0];

    setFormData({
      producerId: producersList[0]?.id || "",
      serviceId: servicesList[0]?.id || "",
      date: localDate,
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

    await fetchExecutions();
    setIsSubmitting(false);
    setIsModalOpen(false);
    setEditingId(null);
  };

  // Calendar Helpers
  const getDaysInMonth = (year: number, month: number) => new Date(year, month + 1, 0).getDate();
  const getFirstDayOfMonth = (year: number, month: number) => new Date(year, month, 1).getDay();

  const prevMonth = () => setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  const nextMonth = () => setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  const goToToday = () => setCurrentDate(new Date());

  const monthYear = new Intl.DateTimeFormat("pt-BR", { month: "long", year: "numeric" }).format(currentDate);
  const daysInMonth = getDaysInMonth(currentDate.getFullYear(), currentDate.getMonth());
  const firstDayOfMonth = getFirstDayOfMonth(currentDate.getFullYear(), currentDate.getMonth());

  const days = [];
  // Days from previous month to fill the first week
  const prevMonthDays = getDaysInMonth(currentDate.getFullYear(), currentDate.getMonth() - 1);
  for (let i = firstDayOfMonth - 1; i >= 0; i--) {
    days.push({ day: prevMonthDays - i, currentMonth: false, date: new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, prevMonthDays - i) });
  }

  // Days of current month
  for (let i = 1; i <= daysInMonth; i++) {
    days.push({ day: i, currentMonth: true, date: new Date(currentDate.getFullYear(), currentDate.getMonth(), i) });
  }

  // Days from next month to fill the last week (total 42 cells for 6 weeks layout)
  const remainingCells = 42 - days.length;
  for (let i = 1; i <= remainingCells; i++) {
    days.push({ day: i, currentMonth: false, date: new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, i) });
  }

  const getSchedulesForDate = (date: Date) => {
    const dateString = new Date(date.getTime() - (date.getTimezoneOffset() * 60000)).toISOString().split("T")[0];
    return executions.filter(e => e.date === dateString);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Concluído": return "bg-green-100 text-green-800 border-green-200";
      case "Em Andamento": return "bg-blue-100 text-blue-800 border-blue-200";
      case "Agendado": return "bg-yellow-100 text-yellow-800 border-yellow-200";
      case "Cancelado": return "bg-red-100 text-red-800 border-red-200";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-gray-200 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">Agendamentos</h1>
          <p className="text-lg text-gray-600 mt-2">Visualize e gerencie o cronograma de serviços.</p>
        </div>
        <Button size="lg" className="shrink-0 gap-2" onClick={() => handleDayClick(new Date())}>
          <Plus className="h-5 w-5" />
          Novo Agendamento
        </Button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        {/* Calendar Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-gray-50/50">
          <div className="flex items-center gap-4">
            <h2 className="text-xl font-bold text-gray-900 capitalize italic">{monthYear}</h2>
            <div className="flex items-center gap-1 bg-white border border-gray-300 rounded-md p-1">
              <button
                onClick={prevMonth}
                className="p-1.5 hover:bg-gray-100 rounded-md transition-colors text-gray-600"
                title="Mês Anterior"
              >
                <ChevronLeft className="h-5 w-5" />
              </button>
              <button
                onClick={goToToday}
                className="px-3 py-1 text-sm font-bold hover:bg-gray-100 rounded-md transition-colors text-gray-700"
              >
                Hoje
              </button>
              <button
                onClick={nextMonth}
                className="p-1.5 hover:bg-gray-100 rounded-md transition-colors text-gray-600"
                title="Próximo Mês"
              >
                <ChevronRight className="h-5 w-5" />
              </button>
            </div>
          </div>
          <div className="hidden md:flex items-center gap-4 text-sm font-medium text-gray-500">
            <div className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-yellow-400" /> Agendado</div>
            <div className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-blue-500" /> Em Andamento</div>
            <div className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-green-500" /> Concluído</div>
          </div>
        </div>

        {/* Calendar Grid */}
        <div className="grid grid-cols-7 border-b border-gray-200">
          {["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"].map(day => (
            <div key={day} className="py-2.5 text-center text-sm font-bold text-gray-500 uppercase tracking-wider bg-gray-50">
              {day}
            </div>
          ))}
        </div>

        <div className="grid grid-cols-7 auto-rows-[120px]">
          {days.map((d, i) => {
            const schedules = getSchedulesForDate(d.date);
            const isToday = d.date.toDateString() === new Date().toDateString();

            return (
              <div
                key={i}
                className={cn(
                  "border-r border-b border-gray-100 p-2 transition-colors relative group cursor-pointer hover:bg-gray-50/80",
                  !d.currentMonth && "bg-gray-50/30 text-gray-400"
                )}
                onClick={() => handleDayClick(d.date)}
              >
                <div className="flex justify-between items-start mb-1">
                  <span className={cn(
                    "inline-flex items-center justify-center w-7 h-7 text-sm font-bold rounded-full",
                    isToday ? "bg-blue-600 text-white" : "text-gray-700 group-hover:bg-gray-200"
                  )}>
                    {d.day}
                  </span>
                </div>

                <div className="space-y-1 overflow-y-auto max-h-[80px] scrollbar-hide">
                  {schedules.map(s => (
                    <div
                      key={s.id}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleEditClick(s);
                      }}
                      className={cn(
                        "text-[10px] leading-tight px-1.5 py-1 rounded border truncate font-bold transition-all hover:scale-105 active:scale-95 shadow-sm",
                        getStatusColor(s.status)
                      )}
                      title={`${s.producerName} - ${s.serviceName}`}
                    >
                      {s.producerName}
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingId ? "Editar Agendamento" : "Novo Agendamento"}
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="block text-sm font-bold text-gray-900">Produtor</label>
              <select
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
              <label className="block text-sm font-bold text-gray-900">Serviço</label>
              <select
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
              <label className="block text-sm font-bold text-gray-900">Data do Serviço</label>
              <input
                name="date"
                type="date"
                required
                value={formData.date}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-bold text-gray-900">
                Quantidade ({servicesList.find(s => s.id === formData.serviceId)?.unit || "Unidade"})
              </label>
              <input
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
              <label className="block text-sm font-bold text-gray-900">Valor Total (R$)</label>
              <input
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
              <label className="block text-sm font-bold text-gray-900">Status</label>
              <select
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
