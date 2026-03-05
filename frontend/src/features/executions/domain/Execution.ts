export interface Execution {
  id: string;
  producerId: string;
  producerName: string;
  serviceId: string;
  serviceName: string;
  date: string;
  quantity: number;
  unit: string;
  totalValue: number;
  status: "Agendado" | "Em Andamento" | "Concluído" | "Cancelado";
  is_deleted?: boolean;
}
