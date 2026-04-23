import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiRequest } from "../api.js";
import { useAuth } from "../context/AuthContext.jsx";

const emptyForm = {
  title: "",
  description: "",
  category: "Academic",
  status: "Pending"
};

const Dashboard = () => {
  const navigate = useNavigate();
  const { student, logout } = useAuth();
  const [form, setForm] = useState(emptyForm);
  const [grievances, setGrievances] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [searchTitle, setSearchTitle] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const fetchGrievances = async () => {
    try {
      const data = await apiRequest("/grievances");
      setGrievances(data);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchGrievances();
  }, []);

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const clearMessages = () => {
    setError("");
    setSuccess("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    clearMessages();

    try {
      if (editingId) {
        await apiRequest(`/grievances/${editingId}`, {
          method: "PUT",
          body: JSON.stringify(form)
        });
        setSuccess("Grievance updated successfully");
      } else {
        await apiRequest("/grievances", {
          method: "POST",
          body: JSON.stringify(form)
        });
        setSuccess("Grievance submitted successfully");
      }

      setForm(emptyForm);
      setEditingId(null);
      fetchGrievances();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleEdit = (grievance) => {
    setEditingId(grievance._id);
    setForm({
      title: grievance.title,
      description: grievance.description,
      category: grievance.category,
      status: grievance.status
    });
    clearMessages();
  };

  const handleDelete = async (id) => {
    clearMessages();

    try {
      await apiRequest(`/grievances/${id}`, { method: "DELETE" });
      setSuccess("Grievance deleted successfully");
      fetchGrievances();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleSearch = async (event) => {
    event.preventDefault();
    clearMessages();

    try {
      const data = await apiRequest(
        `/grievances/search?title=${encodeURIComponent(searchTitle)}`
      );
      setGrievances(data);
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
          <p>Welcome, {student?.name}</p>
          <h1>Student Grievance Dashboard</h1>
        </div>
        <button type="button" className="secondary-button" onClick={handleLogout}>
          Logout
        </button>
      </header>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <section className="dashboard-grid">
        <div className="panel">
          <h2>{editingId ? "Update Grievance" : "Submit Grievance"}</h2>

          <form onSubmit={handleSubmit} className="form">
            <label>
              Title
              <input
                type="text"
                name="title"
                value={form.title}
                onChange={handleChange}
                placeholder="Short title"
                required
              />
            </label>

            <label>
              Description
              <textarea
                name="description"
                value={form.description}
                onChange={handleChange}
                placeholder="Describe your issue"
                rows="5"
                required
              />
            </label>

            <label>
              Category
              <select name="category" value={form.category} onChange={handleChange}>
                <option value="Academic">Academic</option>
                <option value="Hostel">Hostel</option>
                <option value="Transport">Transport</option>
                <option value="Other">Other</option>
              </select>
            </label>

            {editingId && (
              <label>
                Status
                <select name="status" value={form.status} onChange={handleChange}>
                  <option value="Pending">Pending</option>
                  <option value="Resolved">Resolved</option>
                </select>
              </label>
            )}

            <div className="button-row">
              <button type="submit">{editingId ? "Update" : "Submit"}</button>
              {editingId && (
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => {
                    setEditingId(null);
                    setForm(emptyForm);
                  }}
                >
                  Cancel
                </button>
              )}
            </div>
          </form>
        </div>

        <div className="panel">
          <div className="list-header">
            <h2>My Grievances</h2>
            <form onSubmit={handleSearch} className="search-form">
              <input
                type="text"
                value={searchTitle}
                onChange={(event) => setSearchTitle(event.target.value)}
                placeholder="Search by title"
              />
              <button type="submit">Search</button>
              <button
                type="button"
                className="secondary-button"
                onClick={() => {
                  setSearchTitle("");
                  fetchGrievances();
                }}
              >
                Reset
              </button>
            </form>
          </div>

          <div className="grievance-list">
            {grievances.length === 0 ? (
              <p className="empty-text">No grievances found.</p>
            ) : (
              grievances.map((grievance) => (
                <article className="grievance-card" key={grievance._id}>
                  <div className="card-top">
                    <h3>{grievance.title}</h3>
                    <span className={`status ${grievance.status.toLowerCase()}`}>
                      {grievance.status}
                    </span>
                  </div>
                  <p>{grievance.description}</p>
                  <div className="meta-row">
                    <span>{grievance.category}</span>
                    <span>{new Date(grievance.date).toLocaleDateString()}</span>
                  </div>
                  <div className="button-row">
                    <button type="button" onClick={() => handleEdit(grievance)}>
                      Edit
                    </button>
                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDelete(grievance._id)}
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
    </main>
  );
};

export default Dashboard;
