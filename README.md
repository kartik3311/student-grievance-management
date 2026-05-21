# Travel Package Booking Management System

A compact MERN stack project based on the make-up exam prompt. Users can register, login securely, create travel package bookings, view booking details, update or cancel bookings, track booking status, and logout.

## Tech Stack

- MongoDB with Mongoose
- Express.js
- React with Vite
- Node.js
- bcrypt for password hashing
- JSON Web Token for authentication

## Folder Structure

```text
travel-package-booking-management/
  backend/
    config/
      db.js
    controllers/
      authController.js
      bookingController.js
    middleware/
      authMiddleware.js
    models/
      Booking.js
      User.js
    routes/
      authRoutes.js
      bookingRoutes.js
    .env.example
    package.json
    server.js
  frontend/
    src/
      components/
        ProtectedRoute.jsx
      context/
        AuthContext.jsx
      pages/
        Dashboard.jsx
        Login.jsx
        Register.jsx
      api.js
      App.jsx
      index.css
      main.jsx
    .env.example
    index.html
    package.json
    vite.config.js
```

## Backend Setup

1. Open a terminal in `backend`.
2. Install packages:

```bash
npm install
```

3. Create `.env` from `.env.example`:

```powershell
Copy-Item .env.example .env
```

4. Use values like:

```bash
PORT=5000
MONGO_URI=mongodb://127.0.0.1:27017/travel_booking_db
JWT_SECRET=replace_this_with_a_long_secret_key
```

5. Start MongoDB locally.
6. Run the backend:

```bash
npm run dev
```

The backend runs at `http://localhost:5000`.

## Frontend Setup

1. Open another terminal in `frontend`.
2. Install packages:

```bash
npm install
```

3. Optional `.env`:

```bash
VITE_API_URL=http://localhost:5000/api
```

4. Run the frontend:

```bash
npm run dev
```

The frontend runs at `http://localhost:5173`.

## MongoDB Schema

### User

- `name`
- `email` unique
- `password` hashed
- `mobileNumber`

### Booking

- `destinationName`
- `travelDate`
- `numberOfTravelers`
- `packageType`: `Silver`, `Gold`, `Platinum`
- `price`
- `bookingStatus`: `Pending`, `Confirmed`, `Cancelled`
- `contactAddress`
- `userId`

## API Routes

### Auth

- `POST /api/register`
- `POST /api/login`

### Bookings

All booking routes require:

```text
Authorization: Bearer YOUR_TOKEN
```

- `POST /api/bookings`
- `GET /api/bookings`
- `GET /api/bookings/:id`
- `PUT /api/bookings/:id`
- `DELETE /api/bookings/:id`

## Example Request Bodies

Register:

```json
{
  "name": "Kartik",
  "email": "kartik@example.com",
  "password": "123456",
  "mobileNumber": "9876543210"
}
```

Create booking:

```json
{
  "destinationName": "Goa",
  "travelDate": "2026-06-15",
  "numberOfTravelers": 2,
  "packageType": "Gold",
  "price": 42000,
  "contactAddress": "Sector 62, Noida"
}
```

Update booking:

```json
{
  "destinationName": "Goa",
  "travelDate": "2026-06-15",
  "numberOfTravelers": 3,
  "packageType": "Platinum",
  "price": 69000,
  "bookingStatus": "Confirmed",
  "contactAddress": "Sector 62, Noida"
}
```

## Notes

- Passwords are hashed using bcrypt before storage.
- Login returns a JWT token.
- The frontend stores the logged-in user in `localStorage`.
- Protected routes are enforced on both frontend and backend.
- Each user can only view and modify their own bookings.

## Render Deployment

### Backend Web Service

```text
Root Directory: backend
Build Command: npm install
Start Command: npm start
```

Environment variables:

```text
MONGO_URI=your MongoDB Atlas connection string
JWT_SECRET=any long secret text
```

### Frontend Static Site

```text
Root Directory: frontend
Build Command: npm install && npm run build
Publish Directory: dist
```

Environment variable:

```text
VITE_API_URL=https://your-backend-name.onrender.com/api
```

React Router rewrite:

```text
Source: /*
Destination: /index.html
Action: Rewrite
```
