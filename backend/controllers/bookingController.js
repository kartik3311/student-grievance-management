import Booking from "../models/Booking.js";

const requiredBookingFields = [
  "destinationName",
  "travelDate",
  "numberOfTravelers",
  "packageType",
  "price",
  "contactAddress"
];

const hasMissingFields = (payload) => {
  return requiredBookingFields.some((field) => {
    return payload[field] === undefined || payload[field] === null || payload[field] === "";
  });
};

export const createBooking = async (req, res) => {
  try {
    if (hasMissingFields(req.body)) {
      return res.status(400).json({ message: "Please fill all booking fields" });
    }

    const booking = await Booking.create({
      ...req.body,
      userId: req.user._id
    });

    res.status(201).json(booking);
  } catch (error) {
    res.status(500).json({ message: "Could not create booking" });
  }
};

export const getBookings = async (req, res) => {
  try {
    const bookings = await Booking.find({ userId: req.user._id }).sort({
      createdAt: -1
    });

    res.json(bookings);
  } catch (error) {
    res.status(500).json({ message: "Could not fetch bookings" });
  }
};

export const getBookingById = async (req, res) => {
  try {
    const booking = await Booking.findOne({
      _id: req.params.id,
      userId: req.user._id
    });

    if (!booking) {
      return res.status(404).json({ message: "Booking not found" });
    }

    res.json(booking);
  } catch (error) {
    res.status(500).json({ message: "Could not fetch booking" });
  }
};

export const updateBooking = async (req, res) => {
  try {
    const booking = await Booking.findOne({
      _id: req.params.id,
      userId: req.user._id
    });

    if (!booking) {
      return res.status(404).json({ message: "Booking not found" });
    }

    const allowedFields = [
      "destinationName",
      "travelDate",
      "numberOfTravelers",
      "packageType",
      "price",
      "bookingStatus",
      "contactAddress"
    ];

    allowedFields.forEach((field) => {
      if (req.body[field] !== undefined && req.body[field] !== "") {
        booking[field] = req.body[field];
      }
    });

    const updatedBooking = await booking.save();

    res.json(updatedBooking);
  } catch (error) {
    res.status(500).json({ message: "Could not update booking" });
  }
};

export const deleteBooking = async (req, res) => {
  try {
    const booking = await Booking.findOne({
      _id: req.params.id,
      userId: req.user._id
    });

    if (!booking) {
      return res.status(404).json({ message: "Booking not found" });
    }

    await booking.deleteOne();

    res.json({ message: "Booking deleted" });
  } catch (error) {
    res.status(500).json({ message: "Could not delete booking" });
  }
};
