import { Execution } from "../../executions/domain/Execution";

export interface Request {
    id: string;
    producerId: string;
    producerName: string;
    data_solicitacao: string; // Formato YYYY-MM-DD
    prioridade: number;       // 1 (Normal), 2 (Urgente)
    status: "PENDENTE" | "EM_ANDAMENTO" | "CONCLUIDO" | "CANCELADO";
    observacoes?: string;
    execucoes?: Execution[];  // Relação 1:N que o backend nos envia
}