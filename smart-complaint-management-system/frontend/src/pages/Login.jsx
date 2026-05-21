import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiRequest } from "../api.js";
import { useAuth } from "../context/AuthContext.jsx";

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await apiRequest("/login", {
        method: "POST",
        body: JSON.stringify(form)
      });
      login(data);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <section className="auth-panel">
        <p className="eyebrow">AI-Based Complaint System</p>
        <h1>Login</h1>
        <p>Access protected complaint tracking and AI recommendation modules.</p>

        {error && <div className="error-message">{error}</div>}

        <form className="form" onSubmit={handleSubmit}>
          <label>
            Email
            <input
              name="email"
              type="text"
              value={form.email}
              onChange={handleChange}
              placeholder="Enter email"
              required
            />
          </label>

          <label>
            Password
            <input
              name="password"
              type="password"
              value={form.password}
              onChange={handleChange}
              placeholder="Enter password"
              required
            />
          </label>

          <button type="submit" disabled={loading}>
            {loading ? "Checking..." : "Login"}
          </button>
        </form>

        <p className="switch-link">
          New user? <Link to="/register">Create account</Link>
        </p>
      </section>
    </main>
  );
};

export default Login;
