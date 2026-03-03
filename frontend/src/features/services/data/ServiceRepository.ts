import { AgriculturalService } from "../domain/AgriculturalService";

const API_URL = "/servicos";

export class ServiceRepository {
  async getServices(): Promise<AgriculturalService[]> {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("Failed to fetch services");
    return response.json();
  }

  async getServiceById(id: string): Promise<AgriculturalService | undefined> {
    const response = await fetch(`${API_URL}/${id}`);
    if (!response.ok) {
      if (response.status === 404) return undefined;
      throw new Error("Failed to fetch service");
    }
    return response.json();
  }

  async addService(service: Omit<AgriculturalService, "id">): Promise<AgriculturalService> {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(service),
    });
    if (!response.ok) throw new Error("Failed to add service");
    return response.json();
  }

  async updateService(id: string, service: Partial<AgriculturalService>): Promise<AgriculturalService | undefined> {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(service),
    });
    if (!response.ok) throw new Error("Failed to update service");
    return response.json();
  }

  async deleteService(id: string): Promise<boolean> {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "DELETE",
    });
    return response.ok;
  }
}
