import { Producer } from "../domain/Producer";

const API_URL = "/produtores";

export class ProducerRepository {
  async getProducers(): Promise<Producer[]> {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("Failed to fetch producers");
    return response.json();
  }

  async getProducerById(id: string): Promise<Producer | undefined> {
    const response = await fetch(`${API_URL}/${id}`);
    if (!response.ok) {
      if (response.status === 404) return undefined;
      throw new Error("Failed to fetch producer");
    }
    return response.json();
  }

  async addProducer(producer: Omit<Producer, "id">): Promise<Producer> {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(producer),
    });
    if (!response.ok) throw new Error("Failed to add producer");
    return response.json();
  }

  async updateProducer(id: string, producer: Partial<Producer>): Promise<Producer | undefined> {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(producer),
    });
    if (!response.ok) throw new Error("Failed to update producer");
    return response.json();
  }

  async deleteProducer(id: string): Promise<boolean> {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "DELETE",
    });
    return response.ok;
  }
}
