import { Execution } from "../domain/Execution";
import { apiFetch } from "../../../core/api";

const PATH = "/execucoes";

export class ExecutionRepository {
  async getExecutions(params: {
    skip?: number;
    limit?: number;
    sort_by?: string;
    order?: string;
    show_completed?: boolean;
  } = {}): Promise<{ items: Execution[]; total: number }> {
    const query = new URLSearchParams();
    if (params.skip !== undefined) query.append("skip", params.skip.toString());
    if (params.limit !== undefined) query.append("limit", params.limit.toString());
    if (params.sort_by) query.append("sort_by", params.sort_by);
    if (params.order) query.append("order", params.order);
    if (params.show_completed !== undefined) query.append("show_completed", params.show_completed.toString());

    return apiFetch(`${PATH}/?${query.toString()}`);
  }

  async addExecution(execution: Omit<Execution, "id">): Promise<Execution> {
    return apiFetch(`${PATH}/`, {
      method: "POST",
      body: JSON.stringify(execution),
    });
  }

  async updateExecution(id: string, execution: Partial<Execution>): Promise<Execution | undefined> {
    return apiFetch(`${PATH}/${id}`, {
      method: "PUT",
      body: JSON.stringify(execution),
    });
  }

  async deleteExecution(id: string): Promise<boolean> {
    try {
      await apiFetch(`${PATH}/${id}`, {
        method: "DELETE",
      });
      return true;
    } catch {
      return false;
    }
  }
}
