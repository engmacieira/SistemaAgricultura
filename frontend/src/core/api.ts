export const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function apiFetch(path: string, options: RequestInit = {}) {
    const url = `${API_BASE_URL}${path.startsWith("/") ? "" : "/"}${path}`;

    const headers: Record<string, string> = {
        "Content-Type": "application/json",
    };

    const token = localStorage.getItem("auth_token");
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
        ...options,
        headers: {
            ...headers,
            ...options.headers,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = typeof errorData.detail === 'object'
            ? JSON.stringify(errorData.detail)
            : errorData.detail || `HTTP error! status: ${response.status}`;
        throw new Error(errorMessage);
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
}
