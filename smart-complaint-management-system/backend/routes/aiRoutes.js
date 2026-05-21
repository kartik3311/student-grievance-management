const express = require("express");
const { analyzeComplaintFromBody } = require("../controllers/aiController");
const protect = require("../middleware/authMiddleware");

const router = express.Router();

router.post("/analyze", protect, analyzeComplaintFromBody);

module.exports = router;
