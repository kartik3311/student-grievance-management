import cors from "cors";
import dotenv from "dotenv";
import express from "express";
import connectDB from "./config/db.js";
import authRoutes from "./routes/authRoutes.js";
import grievanceRoutes from "./routes/grievanceRoutes.js";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

connectDB();

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.send("Student Grievance Management API is running");
});

app.use("/api", authRoutes);
app.use("/api/grievances", grievanceRoutes);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
