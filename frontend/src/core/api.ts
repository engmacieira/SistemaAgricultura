export const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function apiFetch(path: string, options: RequestInit = {}) {
    const url = `${API_BASE_URL}${path.startsWith("/") ? "" : "/"}${path}`;

    const response = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
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

    return response.json();
}
