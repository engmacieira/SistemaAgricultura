export interface SystemLog {
  id: string;
  timestamp: string;
  userId: string;
  userName: string;
  action: "CRIAR" | "EDITAR" | "EXCLUIR" | "LOGIN" | "LOGOUT" | "BACKUP" | "RESTAURAR";
  entity: string;
  details: string;
  dados_anteriores?: string | null;
  dados_novos?: string | null;
}
