const Complaint = require("../models/Complaint");
const { analyzeComplaintText } = require("./aiController");

const createComplaint = async (req, res, next) => {
  try {
    const complaint = await Complaint.create({
      ...req.body,
      createdBy: req.user?._id
    });

    res.status(201).json({
      message: "Complaint stored successfully.",
      complaint
    });
  } catch (error) {
    next(error);
  }
};

const getComplaints = async (req, res, next) => {
  try {
    const { category, status } = req.query;
    const query = {};

    if (category) {
      query.category = new RegExp(category, "i");
    }

    if (status) {
      query.status = status;
    }

    const complaints = await Complaint.find(query).sort({ createdAt: -1 });
    res.json(complaints);
  } catch (error) {
    next(error);
  }
};

const searchComplaints = async (req, res, next) => {
  try {
    const { location, category } = req.query;
    const query = {};

    if (location) {
      query.location = new RegExp(location, "i");
    }

    if (category) {
      query.category = new RegExp(category, "i");
    }

    const complaints = await Complaint.find(query).sort({ createdAt: -1 });
    res.json(complaints);
  } catch (error) {
    next(error);
  }
};

const updateComplaintStatus = async (req, res, next) => {
  try {
    const complaint = await Complaint.findByIdAndUpdate(
      req.params.id,
      { status: req.body.status },
      { new: true, runValidators: true }
    );

    if (!complaint) {
      return res.status(404).json({ message: "Complaint not found." });
    }

    res.json({
      message: "Complaint status updated successfully.",
      complaint
    });
  } catch (error) {
    next(error);
  }
};

const deleteComplaint = async (req, res, next) => {
  try {
    const complaint = await Complaint.findByIdAndDelete(req.params.id);

    if (!complaint) {
      return res.status(404).json({ message: "Complaint not found." });
    }

    res.json({ message: "Complaint removed successfully." });
  } catch (error) {
    next(error);
  }
};

const analyzeComplaint = async (req, res, next) => {
  try {
    const complaint = await Complaint.findById(req.params.id);

    if (!complaint) {
      return res.status(404).json({ message: "Complaint not found." });
    }

    const aiAnalysis = await analyzeComplaintText(complaint);
    complaint.aiAnalysis = aiAnalysis;
    await complaint.save();

    res.json({
      message: "AI complaint analysis completed.",
      complaint
    });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  analyzeComplaint,
  createComplaint,
  deleteComplaint,
  getComplaints,
  searchComplaints,
  updateComplaintStatus
};
