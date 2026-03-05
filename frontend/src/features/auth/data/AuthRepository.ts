import { apiFetch } from "../../../core/api";
import { User } from "../domain/User";

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

const AUTH_PATH = "/usuarios";

export class AuthRepository {
  async login(email: string, password: string): Promise<LoginResponse | null> {
    try {
      const response = await apiFetch(`${AUTH_PATH}/login`, {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      return response as LoginResponse;
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
