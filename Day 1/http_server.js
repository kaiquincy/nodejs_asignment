const http = require( 'http' );
const server = http.createServer( ( req, res) => {
res.writeHead( 200, {'Content-Type' : 'text/html' });
res.end( `<h1>Chào mừng!</h1><p>Bạn đang sử  dụng trình duyệt:
${req.headers['user-agent' ]}</p>` );
});
server.listen( 3000, () => {
console.log( 'Máy chủ  chạy tại http://localhost:3000' );
});