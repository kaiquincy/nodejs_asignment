const http = require( 'http' );
const server = http.createServer( ( req, res) => {
    res.writeHead( 200, {'Content-Type' : 'application/json' });
    const response = { message: 'Xin chào từ API Node.js!' , path:
    req.url };
    res.end( JSON.stringify(response));
    });
    server.listen( 4000, () => {
    console.log( 'API chạy tại http://localhost:4000' );
    });