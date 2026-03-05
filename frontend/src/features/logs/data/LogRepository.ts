import { SystemLog } from "../domain/SystemLog";
import { apiFetch } from "../../../core/api";

const PATH = "/logs";

export interface PaginatedLogResponse {
  items: SystemLog[];
  total: number;
  page: number;
  pages: number;
}

export class LogRepository {
  async getLogs(
    skip: number = 0,
    limit: number = 10,
    sortBy: string = "timestamp",
    order: string = "desc",
    search: string = ""
  ): Promise<PaginatedLogResponse> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
      sort_by: sortBy,
      order: order,
      search: search
    });
    return apiFetch(`${PATH}?${params.toString()}`);
  }

  async addLog(log: Omit<SystemLog, "id" | "timestamp">): Promise<void> {
    await apiFetch(PATH, {
      method: "POST",
      body: JSON.stringify(log),
    });
  }
}

export const logRepository = new LogRepository();
