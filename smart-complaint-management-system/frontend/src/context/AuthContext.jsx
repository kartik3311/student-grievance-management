import { createContext, useContext, useMemo, useState } from "react";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState(() => {
    return JSON.parse(localStorage.getItem("smartComplaintAuth") || "null");
  });

  const login = (userData) => {
    localStorage.setItem("smartComplaintAuth", JSON.stringify(userData));
    setAuth(userData);
  };

  const logout = () => {
    localStorage.removeItem("smartComplaintAuth");
    setAuth(null);
  };

  const value = useMemo(
    () => ({
      auth,
      isAuthenticated: Boolean(auth?.token),
      login,
      logout
    }),
    [auth]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
