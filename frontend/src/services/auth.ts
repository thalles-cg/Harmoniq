const API_URL = import.meta.env["VITE_API_URL"];

export async function buscarUsuarioAutenticado() {
  const token = localStorage.getItem("access_token");

  if (!token) {
    return null;
  }

  const response = await fetch(`${API_URL}/usuarios/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    localStorage.removeItem("access_token");
    return null;
  }

  return response.json();
}

export function obterToken() {
  return localStorage.getItem("access_token");
}

export function logout() {
  localStorage.removeItem("access_token");
}