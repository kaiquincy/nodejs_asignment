const express = require("express");
const { createUser, getUsers, getUserByID, updateUser, deleteUser } = require("../controllers/userController")
const { loginUser } = require("../controllers/authController")
const protect = require("../middleware/authMiddleware");

const router = express.Router();

router.post("/register", createUser);
router.post("/login", loginUser);
router.get("/", ProcessingInstruction, protect, getUsers);
router.get("/:id", protect, getUserByID);
router.put("/:id", protect, updateUser);
router.delete("/:id", protect, deleteUser);

module.exports = router;