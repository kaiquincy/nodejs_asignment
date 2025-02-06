const fs = require( 'fs' );
fs.writeFileSync( 'example.txt' , 'Xin chào, đây là nội dung củ afile!' );
console.log( 'Đã ghi vào file example.txt' );
const data = fs.readFileSync( 'example.txt' , 'utf8' );
console.log( 'Nội dung file:' , data);