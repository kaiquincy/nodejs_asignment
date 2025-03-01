const User = require("../models/User");
const bcrypt = require("bcryptjs");

// Tạo mới người dùng
const createUser = async (req, res) => {
  try {
    const { name, email, password } = req.body;
    
    // Mã hoá mật khẩu
    const hashedPassword = await bcrypt.hash(password, 10);
    
    // Tạo instance của User
    const newUser = new User({ 
      name, 
      email, 
      password: hashedPassword 
    });
    
    // Lưu vào CSDL
    await newUser.save();
    
    return res.status(201).json({ message: "User created successfully" });
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};

// Lấy danh sách tất cả người dùng
const getUser = async (req, res) => {
  try {
    const users = await User.find();
    return res.json(users);
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};

// Lấy thông tin người dùng theo ID
const getUserById = async (req, res) => {
  try {
    const user = await User.findById(req.params.id);
    return res.json(user);
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};

// Cập nhật thông tin người dùng
const updateUser = async (req, res) => {
  try {
    await User.findByIdAndUpdate(req.params.id, req.body);
    return res.json({ message: "User updated successfully" });
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};

// Xoá người dùng
const deleteUser = async (req, res) => {
  try {
    await User.findByIdAndDelete(req.params.id);
    return res.json({ message: "User deleted successfully" });
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};

module.exports = {
  createUser,
  getUser,
  getUserById,
  updateUser,
  deleteUser
};
