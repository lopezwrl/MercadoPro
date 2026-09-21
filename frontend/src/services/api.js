const API_URL = "http://localhost:8000/api";

async function request(path, options = {}) {
  const token = localStorage.getItem("mercadopro_token");
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || "Não foi possível concluir a operação.");
  return data;
}

export const api = {
  login: (username, password) =>
    request("/auth/login", { method: "POST", body: JSON.stringify({ username, password }) }),
  me: () => request("/auth/me"),
  dashboard: () => request("/dashboard/summary")
};
