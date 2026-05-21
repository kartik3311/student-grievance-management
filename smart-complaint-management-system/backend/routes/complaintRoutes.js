const express = require("express");
const {
  analyzeComplaint,
  createComplaint,
  deleteComplaint,
  getComplaints,
  searchComplaints,
  updateComplaintStatus
} = require("../controllers/complaintController");
const protect = require("../middleware/authMiddleware");

const router = express.Router();

router.use(protect);

router.post("/", createComplaint);
router.get("/", getComplaints);
router.get("/search", searchComplaints);
router.put("/:id", updateComplaintStatus);
router.delete("/:id", deleteComplaint);
router.post("/:id/analyze", analyzeComplaint);

module.exports = router;
