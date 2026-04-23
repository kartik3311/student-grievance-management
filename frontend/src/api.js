const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

export const apiRequest = async (path, options = {}) => {
  const student = JSON.parse(localStorage.getItem("student") || "null");
  const headers = {
    "Content-Type": "application/json",
    ...options.headers
  };

  if (student?.token) {
    headers.Authorization = `Bearer ${student.token}`;
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
