import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { apiRequest } from "../api.js";
import { useAuth } from "../context/AuthContext.jsx";

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState(location.state?.message || "");

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    try {
      const data = await apiRequest("/login", {
        method: "POST",
        body: JSON.stringify(form)
      });

      login(data);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <main className="auth-page">
      <section className="auth-panel">
        <h1>Traveler Login</h1>
        <p>Login to manage bookings and keep travel plans moving.</p>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit} className="form">
          <label>
            Email
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              placeholder="Enter your email"
              required
            />
          </label>

          <label>
            Password
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
            />
          </label>

          <button type="submit">Login</button>
        </form>

        <p className="switch-link">
          New traveler? <Link to="/register">Create an account</Link>
        </p>
      </section>
    </main>
  );
};

export default Login;
