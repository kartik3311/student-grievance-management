import mongoose from "mongoose";

const bookingSchema = new mongoose.Schema(
  {
    destinationName: {
      type: String,
      required: true,
      trim: true
    },
    travelDate: {
      type: Date,
      required: true
    },
    numberOfTravelers: {
      type: Number,
      required: true,
      min: 1
    },
    packageType: {
      type: String,
      enum: ["Silver", "Gold", "Platinum"],
      required: true
    },
    price: {
      type: Number,
      required: true,
      min: 0
    },
    bookingStatus: {
      type: String,
      enum: ["Pending", "Confirmed", "Cancelled"],
      default: "Pending"
    },
    contactAddress: {
      type: String,
      required: true,
      trim: true
    },
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true
    }
  },
  { timestamps: true }
);

const Booking = mongoose.model("Booking", bookingSchema);

export default Booking;
