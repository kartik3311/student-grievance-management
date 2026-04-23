import Grievance from "../models/Grievance.js";

export const createGrievance = async (req, res) => {
  try {
    const { title, description, category } = req.body;

    if (!title || !description || !category) {
      return res.status(400).json({ message: "Please fill all fields" });
    }

    const grievance = await Grievance.create({
      title,
      description,
      category,
      userId: req.user._id
    });

    res.status(201).json(grievance);
  } catch (error) {
    res.status(500).json({ message: "Could not create grievance" });
  }
};

export const getGrievances = async (req, res) => {
  try {
    const grievances = await Grievance.find({ userId: req.user._id }).sort({
      createdAt: -1
    });

    res.json(grievances);
  } catch (error) {
    res.status(500).json({ message: "Could not fetch grievances" });
  }
};

export const getGrievanceById = async (req, res) => {
  try {
    const grievance = await Grievance.findOne({
      _id: req.params.id,
      userId: req.user._id
    });

    if (!grievance) {
      return res.status(404).json({ message: "Grievance not found" });
    }

    res.json(grievance);
  } catch (error) {
    res.status(500).json({ message: "Could not fetch grievance" });
  }
};

export const updateGrievance = async (req, res) => {
  try {
    const { title, description, category, status } = req.body;

    const grievance = await Grievance.findOne({
      _id: req.params.id,
      userId: req.user._id
    });

    if (!grievance) {
      return res.status(404).json({ message: "Grievance not found" });
    }

    grievance.title = title || grievance.title;
    grievance.description = description || grievance.description;
    grievance.category = category || grievance.category;
    grievance.status = status || grievance.status;

    const updatedGrievance = await grievance.save();

    res.json(updatedGrievance);
  } catch (error) {
    res.status(500).json({ message: "Could not update grievance" });
  }
};

export const deleteGrievance = async (req, res) => {
  try {
    const grievance = await Grievance.findOne({
      _id: req.params.id,
      userId: req.user._id
    });

    if (!grievance) {
      return res.status(404).json({ message: "Grievance not found" });
    }

    await grievance.deleteOne();

    res.json({ message: "Grievance deleted" });
  } catch (error) {
    res.status(500).json({ message: "Could not delete grievance" });
  }
};

export const searchGrievances = async (req, res) => {
  try {
    const { title = "" } = req.query;

    const grievances = await Grievance.find({
      userId: req.user._id,
      title: { $regex: title, $options: "i" }
    }).sort({ createdAt: -1 });

    res.json(grievances);
  } catch (error) {
    res.status(500).json({ message: "Could not search grievances" });
  }
};
