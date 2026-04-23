import express from "express";
import {
  createGrievance,
  deleteGrievance,
  getGrievanceById,
  getGrievances,
  searchGrievances,
  updateGrievance
} from "../controllers/grievanceController.js";
import protect from "../middleware/authMiddleware.js";

const router = express.Router();

router.use(protect);

router.get("/search", searchGrievances);
router.route("/").post(createGrievance).get(getGrievances);
router
  .route("/:id")
  .get(getGrievanceById)
  .put(updateGrievance)
  .delete(deleteGrievance);

export default router;
