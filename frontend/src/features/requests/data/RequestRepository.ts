import { Request } from "../domain/Request";
import { apiFetch } from "../../../core/api";

const PATH = "/solicitacoes";

export class RequestRepository {
    async getRequests(params: {
        skip?: number;
        limit?: number;
        status_filtro?: string;
    } = {}): Promise<Request[]> {
        const query = new URLSearchParams();
        if (params.skip !== undefined) query.append("skip", params.skip.toString());
        if (params.limit !== undefined) query.append("limit", params.limit.toString());
        if (params.status_filtro) query.append("status_filtro", params.status_filtro);

        return apiFetch(`${PATH}/?${query.toString()}`);
    }

    async getRequestById(id: string): Promise<Request> {
        return apiFetch(`${PATH}/${id}`);
    }

    async addRequest(request: Omit<Request, "id" | "status" | "execucoes">): Promise<Request> {
        return apiFetch(`${PATH}/`, {
            method: "POST",
            body: JSON.stringify(request),
        });
    }

    async updateRequest(id: string, request: Partial<Request>): Promise<Request | undefined> {
        return apiFetch(`${PATH}/${id}`, {
            method: "PUT",
            body: JSON.stringify(request),
        });
    }

    async deleteRequest(id: string): Promise<void> {
        return apiFetch(`${PATH}/${id}`, {
            method: "DELETE",
        });
    }
}