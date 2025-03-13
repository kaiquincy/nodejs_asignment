// Import thư viện
const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const path = require("path");

// Khởi tạo ứng dụng
const app = express();
const PORT = 3000;

// Kết nối MongoDB
mongoose.connect("mongodb://localhost:27017/TreeShop", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

// Định nghĩa Schema
const treeSchema = new mongoose.Schema({
    treename: { type: String, required: true },
    description: { type: String, required: true },
    image: String,
});
const Tree = mongoose.model("TreeCollection", treeSchema);

// Cấu hình EJS
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

// Trang chủ
app.get("/", async (req, res) => {
    const trees = await Tree.find();
    res.render("index", { trees });
});

// Trang About Me
app.get("/about", (req, res) => {
    res.render("about");
});

// Thêm cây mới
app.post("/add", async (req, res) => {
    const { treename, description, image } = req.body;
    if (!treename || !description) {
        return res.send("Tree Name and Description are required!");
    }
    await Tree.create({ treename, description, image });
    res.redirect("/");
});

// Xóa toàn bộ dữ liệu
app.post("/reset", async (req, res) => {
    await Tree.deleteMany({});
    res.redirect("/");
});

// Xóa một cây theo ID
app.post("/delete/:id", async (req, res) => {
    await Tree.findByIdAndDelete(req.params.id);
    res.redirect("/");
});

// Hiển thị trang chỉnh sửa cây
app.get("/edit/:id", async (req, res) => {
    const tree = await Tree.findById(req.params.id);
    res.render("edit", { tree });
});

// Cập nhật thông tin cây
app.post("/update/:id", async (req, res) => {
    const { treename, description, image } = req.body;
    await Tree.findByIdAndUpdate(req.params.id, { treename, description, image });
    res.redirect("/");
});

// Lắng nghe kết nối
app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});