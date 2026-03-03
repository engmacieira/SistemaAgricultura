import { SystemLog } from "../domain/SystemLog";
import { apiFetch } from "../../../core/api";

const PATH = "/logs";

export class LogRepository {
  async getLogs(): Promise<SystemLog[]> {
    return apiFetch(PATH);
  }

  async addLog(log: Omit<SystemLog, "id" | "timestamp">): Promise<void> {
    await apiFetch(PATH, {
      method: "POST",
      body: JSON.stringify(log),
    });
  }
}

export const logRepository = new LogRepository();
