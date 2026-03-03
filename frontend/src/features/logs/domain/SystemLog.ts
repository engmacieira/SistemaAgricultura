export interface SystemLog {
  id: string;
  timestamp: string;
  userId: string;
  userName: string;
  action: "CRIAR" | "EDITAR" | "EXCLUIR" | "LOGIN" | "LOGOUT" | "BACKUP" | "RESTAURAR";
  entity: "Produtor" | "Serviço" | "Execução" | "Pagamento" | "Usuário" | "Sistema";
  details: string;
}
