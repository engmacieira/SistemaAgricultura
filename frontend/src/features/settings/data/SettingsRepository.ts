import { apiFetch } from "../../../core/api";

const ADMIN_PATH = "/admin";
const CONFIG_PATH = "/admin/configuracoes";

class SettingsRepository {
  async getUnits(): Promise<string[]> {
    try {
      const config = await apiFetch(CONFIG_PATH);
      return config.unidades_medida || [];
    } catch (error) {
      console.error("Failed to fetch units:", error);
      return [];
    }
  }

  async addUnit(unit: string): Promise<string[]> {
    const config = await apiFetch(CONFIG_PATH);
    const units = config.unidades_medida || [];
    if (!units.includes(unit)) {
      units.push(unit);
      await apiFetch(CONFIG_PATH, {
        method: "PUT",
        body: JSON.stringify({ ...config, unidades_medida: units }),
      });
    }
    return units;
  }

  async removeUnit(unit: string): Promise<string[]> {
    const config = await apiFetch(CONFIG_PATH);
    const units = (config.unidades_medida || []).filter((u: string) => u !== unit);
    await apiFetch(CONFIG_PATH, {
      method: "PUT",
      body: JSON.stringify({ ...config, unidades_medida: units }),
    });
    return units;
  }

  async performBackup(): Promise<void> {
    await apiFetch(`${ADMIN_PATH}/backup`, {
      method: "POST",
    });
  }

  async performRestore(): Promise<void> {
    await apiFetch(`${ADMIN_PATH}/restaurar`, {
      method: "POST",
      body: JSON.stringify({ file_url: "" }),
    });
  }
}

export const settingsRepository = new SettingsRepository();
