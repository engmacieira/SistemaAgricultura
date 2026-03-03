import { AgriculturalService } from "../domain/AgriculturalService";
import { apiFetch } from "../../../core/api";

const PATH = "/servicos";

export class ServiceRepository {
  async getServices(): Promise<AgriculturalService[]> {
    return apiFetch(PATH);
  }

  async getServiceById(id: string): Promise<AgriculturalService | undefined> {
    try {
      return await apiFetch(`${PATH}/${id}`);
    } catch (error) {
      return undefined;
    }
  }

  async addService(service: Omit<AgriculturalService, "id">): Promise<AgriculturalService> {
    return apiFetch(PATH, {
      method: "POST",
      body: JSON.stringify(service),
    });
  }

  async updateService(id: string, service: Partial<AgriculturalService>): Promise<AgriculturalService | undefined> {
    return apiFetch(`${PATH}/${id}`, {
      method: "PUT",
      body: JSON.stringify(service),
    });
  }

  async deleteService(id: string): Promise<boolean> {
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
