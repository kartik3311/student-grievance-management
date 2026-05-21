import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiRequest } from "../api.js";
import { useAuth } from "../context/AuthContext.jsx";

const emptyForm = {
  name: "",
  email: "",
  title: "",
  description: "",
  category: "Water Supply",
  location: "",
  status: "Pending"
};

const statusOptions = ["Pending", "In Progress", "Resolved", "Rejected"];

const Dashboard = () => {
  const navigate = useNavigate();
  const { auth, logout } = useAuth();
  const [form, setForm] = useState(emptyForm);
  const [complaints, setComplaints] = useState([]);
  const [filters, setFilters] = useState({ category: "", location: "" });
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const stats = useMemo(() => {
    return {
      total: complaints.length,
      pending: complaints.filter((item) => item.status === "Pending").length,
      resolved: complaints.filter((item) => item.status === "Resolved").length
    };
  }, [complaints]);

  const fetchComplaints = async () => {
    try {
      const query = new URLSearchParams();
      if (filters.location) query.set("location", filters.location);
      if (filters.category) query.set("category", filters.category);

      const endpoint = query.toString()
        ? `/complaints/search?${query.toString()}`
        : "/complaints";
      const data = await apiRequest(endpoint);
      setComplaints(data);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchComplaints();
  }, []);

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setMessage("");
    setLoading(true);

    try {
      await apiRequest("/complaints", {
        method: "POST",
        body: JSON.stringify(form)
      });
      setMessage("Complaint stored successfully.");
      setForm(emptyForm);
      await fetchComplaints();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (id, status) => {
    setError("");
    setMessage("");

    try {
      await apiRequest(`/complaints/${id}`, {
        method: "PUT",
        body: JSON.stringify({ status })
      });
      setMessage("Complaint status updated successfully.");
      await fetchComplaints();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id) => {
    setError("");
    setMessage("");

    try {
      await apiRequest(`/complaints/${id}`, { method: "DELETE" });
      setMessage("Complaint removed successfully.");
      await fetchComplaints();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleAnalyze = async (complaint) => {
    setError("");
    setMessage("");

    try {
      const data = await apiRequest(`/complaints/${complaint._id}/analyze`, {
        method: "POST"
      });
      setSelectedAnalysis(data.complaint);
      await fetchComplaints();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <main className="dashboard-page">
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">Welcome, {auth?.name}</p>
          <h1>Smart Complaint Dashboard</h1>
        </div>
        <button type="button" className="secondary-button" onClick={handleLogout}>
          Logout
        </button>
      </header>

      <section className="stats-row">
        <div>
          <span>Total Complaints</span>
          <strong>{stats.total}</strong>
        </div>
        <div>
          <span>Pending</span>
          <strong>{stats.pending}</strong>
        </div>
        <div>
          <span>Resolved</span>
          <strong>{stats.resolved}</strong>
        </div>
      </section>

      {message && <div className="success-message">{message}</div>}
      {error && <div className="error-message">{error}</div>}

      <section className="dashboard-grid">
        <div className="panel">
          <h2>Complaint Registration Form</h2>
          <form className="form" onSubmit={handleSubmit}>
            <label>
              Name
              <input name="name" value={form.name} onChange={handleChange} required />
            </label>

            <label>
              Email
              <input
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
                required
              />
            </label>

            <label>
              Complaint Title
              <input name="title" value={form.title} onChange={handleChange} required />
            </label>

            <label>
              Complaint Category
              <select name="category" value={form.category} onChange={handleChange}>
                <option>Water Supply</option>
                <option>Electricity</option>
                <option>Sanitation</option>
                <option>Roads</option>
                <option>Other</option>
              </select>
            </label>

            <label>
              Location
              <input name="location" value={form.location} onChange={handleChange} required />
            </label>

            <label>
              Complaint Description
              <textarea
                name="description"
                value={form.description}
                onChange={handleChange}
                rows="5"
                required
              />
            </label>

            <button type="submit" disabled={loading}>
              {loading ? "Submitting..." : "Submit Complaint"}
            </button>
          </form>
        </div>

        <div className="panel">
          <h2>Search & Filter Section</h2>
          <div className="filter-row">
            <input
              placeholder="Search by location"
              value={filters.location}
              onChange={(event) => setFilters({ ...filters, location: event.target.value })}
            />
            <select
              value={filters.category}
              onChange={(event) => setFilters({ ...filters, category: event.target.value })}
            >
              <option value="">All Categories</option>
              <option>Water Supply</option>
              <option>Electricity</option>
              <option>Sanitation</option>
              <option>Roads</option>
              <option>Other</option>
            </select>
            <button type="button" onClick={fetchComplaints}>
              Apply
            </button>
          </div>

          <h2>Complaint List Page</h2>
          <div className="complaint-list">
            {complaints.length === 0 ? (
              <p className="empty-text">No complaints found.</p>
            ) : (
              complaints.map((complaint) => (
                <article className="complaint-card" key={complaint._id}>
                  <div className="card-top">
                    <div>
                      <h3>{complaint.title}</h3>
                      <p>{complaint.name} · {complaint.location}</p>
                    </div>
                    <span className={`status ${complaint.status.toLowerCase().replace(" ", "-")}`}>
                      {complaint.status}
                    </span>
                  </div>
                  <p>{complaint.description}</p>
                  <div className="meta-row">
                    <span>{complaint.category}</span>
                    <span>{complaint.email}</span>
                  </div>

                  {complaint.aiAnalysis?.response && (
                    <div className="analysis-mini">
                      <strong>AI:</strong> {complaint.aiAnalysis.department} ·{" "}
                      {complaint.aiAnalysis.urgency}
                    </div>
                  )}

                  <div className="button-row">
                    <select
                      value={complaint.status}
                      onChange={(event) =>
                        handleStatusUpdate(complaint._id, event.target.value)
                      }
                    >
                      {statusOptions.map((status) => (
                        <option key={status}>{status}</option>
                      ))}
                    </select>
                    <button type="button" onClick={() => handleAnalyze(complaint)}>
                      AI Analyze
                    </button>
                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDelete(complaint._id)}
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))
            )}
          </div>
        </div>
      </section>

      <section className="panel ai-panel">
        <h2>AI Analysis Result Display</h2>
        {selectedAnalysis ? (
          <div className="analysis-grid">
            <div>
              <span>Urgency</span>
              <strong>{selectedAnalysis.aiAnalysis.urgency}</strong>
            </div>
            <div>
              <span>Responsible Department</span>
              <strong>{selectedAnalysis.aiAnalysis.department}</strong>
            </div>
            <div>
              <span>Complaint Summary</span>
              <p>{selectedAnalysis.aiAnalysis.summary}</p>
            </div>
            <div>
              <span>Auto Response</span>
              <p>{selectedAnalysis.aiAnalysis.response}</p>
            </div>
          </div>
        ) : (
          <p className="empty-text">Click AI Analyze on a complaint to generate results.</p>
        )}
      </section>
    </main>
  );
};

export default Dashboard;
