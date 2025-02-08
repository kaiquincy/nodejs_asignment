const express = require( 'express' );
const app = express();
const PORT = 3000;
app.use(express.json());
app.get( '/' , (req, res) => {
res.send( 'Chào mừng đế n với API củ a chúng tôi!' );
});
app.listen(PORT, () => {
    console.log( `Server chạy tại http://localhost:${PORT}` );
});