const express = require("express");
const { loginUser, registerUser } = require("../controllers/authController");

const router = express.Router();

router.post("/signup", registerUser);
router.post("/register", registerUser);
router.post("/login", loginUser);

module.exports = router;
