const mongoose = require("mongoose");

const complaintSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, "Name is required"],
      trim: true
    },
    email: {
      type: String,
      required: [true, "Email is required"],
      lowercase: true,
      trim: true,
      match: [/^\S+@\S+\.\S+$/, "Please enter a valid email"]
    },
    title: {
      type: String,
      required: [true, "Complaint title is required"],
      trim: true
    },
    description: {
      type: String,
      required: [true, "Complaint description is required"],
      trim: true
    },
    category: {
      type: String,
      required: [true, "Complaint category is required"],
      trim: true
    },
    location: {
      type: String,
      required: [true, "Location is required"],
      trim: true
    },
    status: {
      type: String,
      enum: ["Pending", "In Progress", "Resolved", "Rejected"],
      default: "Pending"
    },
    aiAnalysis: {
      urgency: { type: String, default: "Medium" },
      department: { type: String, default: "General Administration" },
      summary: { type: String, default: "" },
      response: { type: String, default: "" }
    },
    createdBy: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User"
    }
  },
  { timestamps: true }
);

module.exports = mongoose.model("Complaint", complaintSchema);
