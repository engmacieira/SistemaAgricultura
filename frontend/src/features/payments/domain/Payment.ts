export interface Payment {
  id: string;
  executionId: string;
  producerName: string;
  serviceName: string;
  dueDate: string;
  paymentDate?: string;
  amount: number;
  status: "Pendente" | "Pago" | "Atrasado";
}
