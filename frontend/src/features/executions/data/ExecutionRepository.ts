import { Execution } from "../domain/Execution";
import { apiFetch } from "../../../core/api";

const PATH = "/execucoes";

export class ExecutionRepository {
  async getExecutions(): Promise<Execution[]> {
    return apiFetch(PATH);
  }

  async addExecution(execution: Omit<Execution, "id">): Promise<Execution> {
    return apiFetch(PATH, {
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
