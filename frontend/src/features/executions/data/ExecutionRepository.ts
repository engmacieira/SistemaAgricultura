import { Execution } from "../domain/Execution";

const API_URL = "/execucoes";

export class ExecutionRepository {
  async getExecutions(): Promise<Execution[]> {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("Failed to fetch executions");
    return response.json();
  }

  async addExecution(execution: Omit<Execution, "id">): Promise<Execution> {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(execution),
    });
    if (!response.ok) throw new Error("Failed to add execution");
    return response.json();
  }

  async updateExecution(id: string, execution: Partial<Execution>): Promise<Execution | undefined> {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(execution),
    });
    if (!response.ok) throw new Error("Failed to update execution");
    return response.json();
  }

  async deleteExecution(id: string): Promise<boolean> {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "DELETE",
    });
    return response.ok;
  }
}
