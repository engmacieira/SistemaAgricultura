import { User } from "../../auth/domain/User";

const API_URL = "/usuarios";

export class UserManagementRepository {
  async getUsers(): Promise<User[]> {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("Failed to fetch users");
    return response.json();
  }

  async addUser(user: Omit<User, "id">): Promise<User> {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(user),
    });
    if (!response.ok) throw new Error("Failed to add user");
    return response.json();
  }

  async updateUser(id: string, user: Partial<User>): Promise<User | undefined> {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(user),
    });
    if (!response.ok) throw new Error("Failed to update user");
    return response.json();
  }

  async deleteUser(id: string): Promise<boolean> {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "DELETE",
    });
    return response.ok;
  }
}

export const userManagementRepository = new UserManagementRepository();
