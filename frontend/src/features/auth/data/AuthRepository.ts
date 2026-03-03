import { User } from "../domain/User";

const API_URL = "/auth";

export class AuthRepository {
  async login(email: string, password: string): Promise<User | null> {
    const response = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) return null;
    return response.json();
  }

  async logout(): Promise<void> {
    await fetch(`${API_URL}/logout`, {
      method: "POST",
    });
  }
}

export const authRepository = new AuthRepository();
