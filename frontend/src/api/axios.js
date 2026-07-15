import axios from "axios";

// Backend runs on port 6767 per application.properties (server.port=6767)
export const BASE_URL = "http://localhost:6767";

const api = axios.create({
  baseURL: BASE_URL,
});

// Backend's jwtValidator does `jwt.substring(7)` to strip "Bearer ",
// so the header MUST be sent as "Bearer <token>".
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("hobby_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401 || err.response?.status === 403) {
      // Token missing/invalid/expired — force back to login
      localStorage.removeItem("hobby_token");
      if (!window.location.pathname.startsWith("/login")) {
        window.location.href = "/login";
      }
    }
    return Promise.reject(err);
  }
);

export default api;
