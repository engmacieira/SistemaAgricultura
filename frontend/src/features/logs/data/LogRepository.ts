import { SystemLog } from "../domain/SystemLog";

const API_URL = "/logs";

export class LogRepository {
  async getLogs(): Promise<SystemLog[]> {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("Failed to fetch logs");
    return response.json();
  }

  async addLog(log: Omit<SystemLog, "id" | "timestamp">): Promise<void> {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(log),
    });
    if (!response.ok) throw new Error("Failed to add log");
  }
}

export const logRepository = new LogRepository();
