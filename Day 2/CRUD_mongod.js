const express = require( 'express' );
const mongoose = require( 'mongoose' );
const app = express();
const PORT = 3000;

// Middleware để  parse JSON
app.use(express.json());

// Kế t nố i MongoDB
mongoose.connect( 'mongodb://localhost:27017/productapi' , {
useNewUrlParser: true,
useUnifiedTopology: true
}).then( ()  => console.log( 'Kế t nố i thành công với MongoDB' ))
.catch( err => console.error( 'Lỗi kế t nố i' , err));

//Ðịnh nghĩa Schema và Model
const productSchema = new mongoose.Schema({
    name: String,
    price: Number
});
const Product = mongoose.model( 'Product' , productSchema);

//Lấy danh sách sản phẩm
app.get( '/products' , async (req, res) => {
    const products = await Product.find(); // Lấ y toàn bộ sả n phẩ m từ
   database
    res.json(products);
   });

//Lấy sản phẩm theo ID
app.get( '/products/:id' , async (req, res) => {
const product = await Product.findById(req.params.id); // Tìm sản phẩm theo ID
if (!product) return res.status( 404).json({ message: 'Sả n phẩ m khôngtồ n tại'  });
    res.json(product);
});

//Thêm sản phẩm mới
app.post( '/products' , async (req, res) => {
    const newProduct = new Product(req.body); // Tạo sả n phẩ m mới từ dữ liệu yêu cầ u
    await newProduct.save();
    res.status( 201).json(newProduct);
});

//Cập nhật sản phẩm
app.put( '/products/:id' , async (req, res) => {
    const updatedProduct = await Product.findByIdAndUpdate(req.params.id,
    req.body, { new: true });
    res.json(updatedProduct);
});

//Xóa sản phẩm
app.delete( '/products/:id' , async (req, res) => {
    await Product.findByIdAndDelete(req.params.id);
    res.json({ message: 'Sả n phẩ m đã bị xóa'  });
});

//Khởi động server
app.listen(PORT, () => console.log( `Server đang chạy tạihttp://localhost:${PORT}` ));