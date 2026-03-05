export interface Payment {
  id: string;
  executionId: string;
  producerName: string;
  serviceName: string;
  dueDate: string;
  paymentDate?: string;
  amount: number;
  paidAmount: number;
  is_deleted: boolean;
  status: "Pendente" | "Parcial" | "Pago" | "Atrasado";
}

export interface PaymentTransaction {
  id: string;
  pagamentoId: string;
  amount: number;
  date: string;
}
