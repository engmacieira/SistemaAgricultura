import { Producer } from "../domain/Producer";
import { apiFetch } from "../../../core/api";

const PATH = "/produtores";

export class ProducerRepository {
  async getProducers(): Promise<Producer[]> {
    return apiFetch(PATH);
  }

  async getProducerById(id: string): Promise<Producer | undefined> {
    try {
      return await apiFetch(`${PATH}/${id}`);
    } catch (error) {
      return undefined;
    }
  }

  async addProducer(producer: Omit<Producer, "id">): Promise<Producer> {
    return apiFetch(PATH, {
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
