const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

export const apiRequest = async (path, options = {}) => {
  const user = JSON.parse(localStorage.getItem("user") || "null");
  const headers = {
    "Content-Type": "application/json",
    ...options.headers
  };

  if (user?.token) {
    headers.Authorization = `Bearer ${user.token}`;
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || "Something went wrong");
  }

  return data;
};
