# Student Grievance Management System

A simple MERN stack project for beginners. Students can register, login, submit grievances, search them, update their status, and delete them.

## Tech Stack

- MongoDB with Mongoose
- Express.js
- React with Vite
- Node.js
- bcrypt for password hashing
- JSON Web Token for protected routes

## Folder Structure

```text
student-grievance-management/
  backend/
    config/
      db.js
    controllers/
      authController.js
      grievanceController.js
    middleware/
      authMiddleware.js
    models/
      Grievance.js
      Student.js
    routes/
      authRoutes.js
      grievanceRoutes.js
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

1. Open a terminal in the `backend` folder.
2. Install packages:

```bash
npm install
```

3. Create a `.env` file by copying `.env.example`:

PowerShell:

```powershell
Copy-Item .env.example .env
```

Then edit `.env`:

```bash
PORT=5000
MONGO_URI=mongodb://127.0.0.1:27017/student_grievance_db
JWT_SECRET=replace_this_with_a_long_secret_key
```

4. Make sure MongoDB is running locally.
5. Start the backend:

```bash
npm run dev
```

The backend will run at `http://localhost:5000`.

## Frontend Setup

1. Open another terminal in the `frontend` folder.
2. Install packages:

```bash
npm install
```

3. Optional: create a `.env` file from `.env.example`:

PowerShell:

```powershell
Copy-Item .env.example .env
```

Then edit `.env`:

```bash
VITE_API_URL=http://localhost:5000/api
```

4. Start the frontend:

```bash
npm run dev
```

The frontend will run at `http://localhost:5173`.

## API Routes

### Auth

- `POST /api/register`
- `POST /api/login`

### Grievances

All grievance routes need this header:

```text
Authorization: Bearer YOUR_TOKEN
```

- `POST /api/grievances`
- `GET /api/grievances`
- `GET /api/grievances/:id`
- `PUT /api/grievances/:id`
- `DELETE /api/grievances/:id`
- `GET /api/grievances/search?title=keyword`

## Example Request Bodies

Register:

```json
{
  "name": "Kartik",
  "email": "kartik@example.com",
  "password": "123456"
}
```

Create grievance:

```json
{
  "title": "Bus delay",
  "description": "The college bus arrives late every morning.",
  "category": "Transport"
}
```

Update grievance:

```json
{
  "title": "Bus delay",
  "description": "The college bus arrives late every morning.",
  "category": "Transport",
  "status": "Resolved"
}
```

## Beginner Notes

- The password is never saved directly. It is hashed with bcrypt before saving.
- Login returns a JWT token.
- The frontend stores the logged-in student in `localStorage`.
- The dashboard route is protected on the frontend.
- The backend also protects grievance APIs with JWT middleware.
- Each student only sees their own grievances.

## Deploy On Render

You need to upload this project to GitHub first. Do not upload `node_modules`.

### Backend Render Settings

Create a new **Web Service** on Render.

Use these settings:

```text
Root Directory: backend
Build Command: npm install
Start Command: npm start
```

Add these environment variables in Render:

```text
MONGO_URI=your MongoDB Atlas connection string
JWT_SECRET=any long secret text
```

Do not add `PORT`. Render provides it automatically.

After deploy, your backend URL will look like:

```text
https://your-backend-name.onrender.com
```

Test it by opening the backend URL in your browser. You should see:

```text
Student Grievance Management API is running
```

### Frontend Render Settings

Create a new **Static Site** on Render.

Use these settings:

```text
Root Directory: frontend
Build Command: npm install && npm run build
Publish Directory: dist
```

Add this environment variable:

```text
VITE_API_URL=https://your-backend-name.onrender.com/api
```

Replace `your-backend-name` with your real Render backend URL.

Because this React app uses React Router, add this rewrite in the Render Static Site settings:

```text
Source: /*
Destination: /index.html
Action: Rewrite
```
