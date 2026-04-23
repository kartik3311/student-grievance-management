import { createContext, useContext, useMemo, useState } from "react";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [student, setStudent] = useState(() => {
    return JSON.parse(localStorage.getItem("student") || "null");
  });

  const login = (studentData) => {
    localStorage.setItem("student", JSON.stringify(studentData));
    setStudent(studentData);
  };

  const logout = () => {
    localStorage.removeItem("student");
    setStudent(null);
  };

  const value = useMemo(() => ({ student, login, logout }), [student]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  return useContext(AuthContext);
};
