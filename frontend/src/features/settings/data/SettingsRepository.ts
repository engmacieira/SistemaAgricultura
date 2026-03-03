const API_URL = "/configuracoes";

class SettingsRepository {
  async getUnits(): Promise<string[]> {
    const response = await fetch(`${API_URL}/unidades`);
    if (!response.ok) throw new Error("Failed to fetch units");
    return response.json();
  }

  async addUnit(unit: string): Promise<string[]> {
    const response = await fetch(`${API_URL}/unidades`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ unit }),
    });
    if (!response.ok) throw new Error("Failed to add unit");
    return response.json();
  }

  async removeUnit(unit: string): Promise<string[]> {
    const response = await fetch(`${API_URL}/unidades/${unit}`, {
      method: "DELETE",
    });
    if (!response.ok) throw new Error("Failed to remove unit");
    return response.json();
  }

  async performBackup(): Promise<void> {
    const response = await fetch(`${API_URL}/backup`, {
      method: "POST",
    });
    if (!response.ok) throw new Error("Failed to perform backup");
  }

  async performRestore(): Promise<void> {
    const response = await fetch(`${API_URL}/restore`, {
      method: "POST",
    });
    if (!response.ok) throw new Error("Failed to perform restore");
  }
}

export const settingsRepository = new SettingsRepository();
