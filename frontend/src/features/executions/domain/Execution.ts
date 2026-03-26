export interface Execution {
  id: string;
  solicitacaoId: string; // ✅ Vínculo com a Fila de Espera
  serviceId: string;
  serviceName: string;
  date: string;
  quantity: number;
  unit: string;
  valor_unitario: number; // ✅ Novo: Preço da hora/hectare
  totalValue: number;
  status: string; // Geralmente "REGISTRADA"
  operador_maquina?: string; // ✅ Novo
  is_deleted?: boolean;
}