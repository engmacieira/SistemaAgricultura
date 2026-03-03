import { User } from "../domain/User";
import { apiFetch } from "../../../core/api";

const AUTH_PATH = "/usuarios";

export class AuthRepository {
  async login(email: string, password: string): Promise<User | null> {
    try {
      return await apiFetch(`${AUTH_PATH}/login`, {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
    } catch (error) {
      console.error("Login error:", error);
      return null;
    }
  }

  async logout(): Promise<void> {
    // Backend logout not implemented or not needed for now
  }
}

export const authRepository = new AuthRepository();
