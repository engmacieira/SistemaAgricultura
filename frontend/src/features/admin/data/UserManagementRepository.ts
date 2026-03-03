import { User } from "../../auth/domain/User";
import { apiFetch } from "../../../core/api";

const PATH = "/usuarios";

export class UserManagementRepository {
  async getUsers(): Promise<User[]> {
    return apiFetch(PATH);
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
