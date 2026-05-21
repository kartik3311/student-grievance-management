# AI-Based Smart Complaint Management System

A MERN stack project for the AI308B ESE AIML case study. The app allows users/admins to register complaints, track complaints, filter by category/location, update status, delete complaints, and generate AI-based complaint analysis using an OpenRouter/OpenAI-compatible API.

## Tech Stack

- MongoDB + Mongoose
- Express.js
- React + Vite
- Node.js
- JWT authentication
- bcrypt password hashing
- OpenRouter/OpenAI-compatible AI API

## Backend APIs

### Auth

- `POST /api/register`
- `POST /api/signup`
- `POST /api/login`

### Complaints

- `POST /api/complaints`
- `GET /api/complaints`
- `GET /api/complaints/search?location=Ghaziabad`
- `PUT /api/complaints/:id`
- `DELETE /api/complaints/:id`
- `POST /api/complaints/:id/analyze`

### AI

- `POST /api/ai/analyze`

## Setup

```powershell
cd backend
npm install
Copy-Item .env.example .env
npm run dev
```

Add your MongoDB Atlas URI and OpenRouter API key in `backend/.env`.

```powershell
cd frontend
npm install
npm run dev
```

## Render Deployment

Backend web service:

- Root Directory: `backend`
- Build Command: `npm install`
- Start Command: `npm start`

Frontend static site:

- Root Directory: `frontend`
- Build Command: `npm install && npm run build`
- Publish Directory: `dist`
- Environment Variable: `VITE_API_URL=https://your-backend.onrender.com/api`
