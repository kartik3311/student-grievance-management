import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import Student from "../models/Student.js";

const createToken = (studentId) => {
  return jwt.sign({ id: studentId }, process.env.JWT_SECRET, {
    expiresIn: "7d"
  });
};

export const registerStudent = async (req, res) => {
  try {
    const { name, email, password } = req.body;

    if (!name || !email || !password) {
      return res.status(400).json({ message: "Please fill all fields" });
    }

    const existingStudent = await Student.findOne({ email });

    if (existingStudent) {
      return res.status(409).json({ message: "Duplicate email" });
    }

    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    const student = await Student.create({
      name,
      email,
      password: hashedPassword
    });

    res.status(201).json({
      _id: student._id,
      name: student.name,
      email: student.email,
      token: createToken(student._id)
    });
  } catch (error) {
    if (error.code === 11000) {
      return res.status(409).json({ message: "Duplicate email" });
    }

    res.status(500).json({ message: "Registration failed" });
  }
};

export const loginStudent = async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ message: "Please enter email and password" });
    }

    const student = await Student.findOne({ email });

    if (!student) {
      return res.status(401).json({ message: "Invalid login" });
    }

    const isPasswordCorrect = await bcrypt.compare(password, student.password);

    if (!isPasswordCorrect) {
      return res.status(401).json({ message: "Invalid login" });
    }

    res.json({
      _id: student._id,
      name: student.name,
      email: student.email,
      token: createToken(student._id)
    });
  } catch (error) {
    res.status(500).json({ message: "Login failed" });
  }
};
