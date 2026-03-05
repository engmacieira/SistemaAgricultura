import { User } from "../../auth/domain/User";
import { apiFetch } from "../../../core/api";

const PATH = "/usuarios";

export class UserManagementRepository {
  async getUsers(skip: number = 0, limit: number = 10, sortBy: string = "name", order: string = "asc"): Promise<{ items: User[], total: number }> {
    return apiFetch(`${PATH}?skip=${skip}&limit=${limit}&sort_by=${sortBy}&order=${order}`);
  }

  async addUser(user: Omit<User, "id">): Promise<User> {
    return apiFetch(PATH, {
      method: "POST",
      body: JSON.stringify(user),
    });
  }

  async updateUser(id: string, user: Partial<User>): Promise<User | undefined> {
    return apiFetch(`${PATH}/${id}`, {
      method: "PUT",
      body: JSON.stringify(user),
    });
  }

  async deleteUser(id: string): Promise<boolean> {
    try {
      await apiFetch(`${PATH}/${id}`, {
        method: "DELETE",
      });
      return true;
    } catch {
      return false;
    }
  }
}

export const userManagementRepository = new UserManagementRepository();
