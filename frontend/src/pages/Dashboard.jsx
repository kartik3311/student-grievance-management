import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiRequest } from "../api.js";
import { useAuth } from "../context/AuthContext.jsx";

const emptyForm = {
  destinationName: "",
  travelDate: "",
  numberOfTravelers: "1",
  packageType: "Silver",
  price: "",
  bookingStatus: "Pending",
  contactAddress: ""
};

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [form, setForm] = useState(emptyForm);
  const [bookings, setBookings] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const fetchBookings = async () => {
    try {
      const data = await apiRequest("/bookings");
      setBookings(data);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  const summary = useMemo(() => {
    return bookings.reduce(
      (totals, booking) => {
        totals.count += 1;
        totals.travelers += Number(booking.numberOfTravelers || 0);
        totals.value += Number(booking.price || 0);
        return totals;
      },
      { count: 0, travelers: 0, value: 0 }
    );
  }, [bookings]);

  const clearMessages = () => {
    setError("");
    setSuccess("");
  };

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    clearMessages();

    const payload = {
      ...form,
      numberOfTravelers: Number(form.numberOfTravelers),
      price: Number(form.price)
    };

    try {
      if (editingId) {
        await apiRequest(`/bookings/${editingId}`, {
          method: "PUT",
          body: JSON.stringify(payload)
        });
        setSuccess("Booking updated successfully");
      } else {
        await apiRequest("/bookings", {
          method: "POST",
          body: JSON.stringify(payload)
        });
        setSuccess("Booking added successfully");
      }

      setForm(emptyForm);
      setEditingId(null);
      fetchBookings();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleEdit = (booking) => {
    setEditingId(booking._id);
    setForm({
      destinationName: booking.destinationName,
      travelDate: booking.travelDate?.slice(0, 10) || "",
      numberOfTravelers: String(booking.numberOfTravelers),
      packageType: booking.packageType,
      price: String(booking.price),
      bookingStatus: booking.bookingStatus,
      contactAddress: booking.contactAddress
    });
    clearMessages();
  };

  const handleDelete = async (id) => {
    clearMessages();

    try {
      await apiRequest(`/bookings/${id}`, { method: "DELETE" });
      setSuccess("Booking deleted successfully");
      fetchBookings();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setForm(emptyForm);
    clearMessages();
  };

  return (
    <main className="dashboard-page">
      <header className="dashboard-header">
        <div>
          <p>Welcome, {user?.name}</p>
          <h1>Travel Package Booking Dashboard</h1>
        </div>
        <button type="button" className="secondary-button" onClick={handleLogout}>
          Logout
        </button>
      </header>

      <section className="summary-strip" aria-label="Booking summary">
        <div>
          <span>Total Bookings</span>
          <strong>{summary.count}</strong>
        </div>
        <div>
          <span>Travelers</span>
          <strong>{summary.travelers}</strong>
        </div>
        <div>
          <span>Total Value</span>
          <strong>Rs. {summary.value.toLocaleString("en-IN")}</strong>
        </div>
      </section>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <section className="dashboard-grid">
        <div className="panel">
          <h2>{editingId ? "Update Booking" : "Add Booking"}</h2>

          <form onSubmit={handleSubmit} className="form">
            <label>
              Destination Name
              <input
                type="text"
                name="destinationName"
                value={form.destinationName}
                onChange={handleChange}
                placeholder="Goa"
                required
              />
            </label>

            <label>
              Travel Date
              <input
                type="date"
                name="travelDate"
                value={form.travelDate}
                onChange={handleChange}
                required
              />
            </label>

            <label>
              Number of Travelers
              <input
                type="number"
                min="1"
                name="numberOfTravelers"
                value={form.numberOfTravelers}
                onChange={handleChange}
                required
              />
            </label>

            <label>
              Package Type
              <select name="packageType" value={form.packageType} onChange={handleChange}>
                <option value="Silver">Silver</option>
                <option value="Gold">Gold</option>
                <option value="Platinum">Platinum</option>
              </select>
            </label>

            <label>
              Price
              <input
                type="number"
                min="0"
                name="price"
                value={form.price}
                onChange={handleChange}
                placeholder="25000"
                required
              />
            </label>

            {editingId && (
              <label>
                Booking Status
                <select
                  name="bookingStatus"
                  value={form.bookingStatus}
                  onChange={handleChange}
                >
                  <option value="Pending">Pending</option>
                  <option value="Confirmed">Confirmed</option>
                  <option value="Cancelled">Cancelled</option>
                </select>
              </label>
            )}

            <label>
              Contact Address
              <textarea
                name="contactAddress"
                value={form.contactAddress}
                onChange={handleChange}
                placeholder="Full pickup or communication address"
                rows="4"
                required
              />
            </label>

            <div className="button-row">
              <button type="submit">{editingId ? "Update" : "Book Package"}</button>
              {editingId && (
                <button type="button" className="secondary-button" onClick={handleCancelEdit}>
                  Cancel
                </button>
              )}
            </div>
          </form>
        </div>

        <div className="panel">
          <div className="list-header">
            <h2>My Bookings</h2>
            <span className="record-count">{bookings.length} record(s)</span>
          </div>

          <div className="booking-list">
            {bookings.length === 0 ? (
              <p className="empty-text">No bookings created yet.</p>
            ) : (
              bookings.map((booking) => (
                <article className="booking-card" key={booking._id}>
                  <div className="card-top">
                    <div>
                      <h3>{booking.destinationName}</h3>
                      <p>{booking.packageType} package</p>
                    </div>
                    <span className={`status ${booking.bookingStatus.toLowerCase()}`}>
                      {booking.bookingStatus}
                    </span>
                  </div>

                  <div className="booking-details">
                    <span>Travel Date</span>
                    <strong>{new Date(booking.travelDate).toLocaleDateString("en-IN")}</strong>
                    <span>Travelers</span>
                    <strong>{booking.numberOfTravelers}</strong>
                    <span>Price</span>
                    <strong>Rs. {Number(booking.price).toLocaleString("en-IN")}</strong>
                    <span>Address</span>
                    <strong>{booking.contactAddress}</strong>
                  </div>

                  <div className="button-row">
                    <button type="button" onClick={() => handleEdit(booking)}>
                      Edit
                    </button>
                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDelete(booking._id)}
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
