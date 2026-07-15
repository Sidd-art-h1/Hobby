import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { signin, signup, getMyProfile } from "../api/endpoints";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("hobby_token"));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadProfile = useCallback(async () => {
    try {
      const res = await getMyProfile();
      setUser(res.data);
    } catch {
      setUser(null);
      setToken(null);
      localStorage.removeItem("hobby_token");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (token) {
      loadProfile();
    } else {
      setLoading(false);
    }
  }, [token, loadProfile]);

  const login = async (email, password) => {
    const res = await signin({ email, password });
    localStorage.setItem("hobby_token", res.data.token);
    setToken(res.data.token);
    await loadProfile();
    return res.data;
  };

  const register = async (payload) => {
    const res = await signup(payload);
    localStorage.setItem("hobby_token", res.data.token);
    setToken(res.data.token);
    await loadProfile();
    return res.data;
  };

  const logout = () => {
    localStorage.removeItem("hobby_token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ token, user, setUser, loading, login, register, logout, refreshProfile: loadProfile }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
