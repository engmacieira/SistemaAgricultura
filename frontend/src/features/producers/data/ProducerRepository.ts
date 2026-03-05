import { Producer } from "../domain/Producer";
import { apiFetch } from "../../../core/api";

const PATH = "/produtores";

export class ProducerRepository {
  async getProducers(page: number = 1, size: number = 10, sortBy: string = "name", order: string = "asc"): Promise<{ items: Producer[], total: number, pages: number }> {
    const params = new URLSearchParams({
      page: page.toString(),
      size: size.toString(),
      sort_by: sortBy,
      order: order
    });
    return apiFetch(`${PATH}/?${params.toString()}`);
  }

  async getProducerById(id: string): Promise<Producer | undefined> {
    try {
      return await apiFetch(`${PATH}/${id}`);
    } catch (error) {
      return undefined;
    }
  }

  async addProducer(producer: Omit<Producer, "id">): Promise<Producer> {
    return apiFetch(`${PATH}/`, {
      method: "POST",
      body: JSON.stringify(producer),
    });
  }

  async updateProducer(id: string, producer: Partial<Producer>): Promise<Producer | undefined> {
    return apiFetch(`${PATH}/${id}`, {
      method: "PUT",
      body: JSON.stringify(producer),
    });
  }

  async deleteProducer(id: string): Promise<boolean> {
    try {
      await apiFetch(`${PATH}/${id}`, {
        method: "DELETE",
      });
      return true;
    } catch (error) {
      return false;
    }
  }
}
