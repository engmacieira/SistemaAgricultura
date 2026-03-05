import { DashboardData } from "../domain/DashboardData";
import { apiFetch } from "../../../core/api";

const PATH = "/dashboard";

export class DashboardRepository {
    async getDashboardData(): Promise<DashboardData> {
        return apiFetch(`${PATH}/`);
    }
}
