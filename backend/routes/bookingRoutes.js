import express from "express";
import {
  createBooking,
  deleteBooking,
  getBookingById,
  getBookings,
  updateBooking
} from "../controllers/bookingController.js";
import protect from "../middleware/authMiddleware.js";

const router = express.Router();

router.use(protect);
router.route("/").post(createBooking).get(getBookings);
router.route("/:id").get(getBookingById).put(updateBooking).delete(deleteBooking);

export default router;
