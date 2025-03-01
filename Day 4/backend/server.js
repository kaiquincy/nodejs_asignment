require( "dotenv").config();
const express = require( "express");
const mongoose = require( "mongoose");
const cors = require( "cors");
const userRoutes = require( "./routes/userRoutes");
const authRoutes = require( "./routes/authRoutes");
const app = express();
app.use(express.json());
app.use(cors());
// Kế t nố i MongoDB
mongoose.connect(process.env.DB_URL, {
 useNewUrlParser: true,
 useUnifiedTopology: true,
})
.then( ()  => console.log( "MongoDB connected"))
.catch( err => console.log( "MongoDB connection error:", err));
// Định tuyế n API
app.use( "/api/users", userRoutes);
app.use( "/api/auth", authRoutes);
const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log( `Server running on port ${PORT}` ));