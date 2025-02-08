const express = require( 'express' );
const fs = require( 'fs' ).promises;

const path = require( 'path' );
const app = express();
const PORT = 3000;
app.use(express.json());
const DATA_FILE = path.join(__dirname, 'data' , 'data.json' );
const readData = async () => {
try {
    const data = await fs.readFile(DATA_FILE, 'utf8' );
    return JSON.parse(data);
} catch (err) {
    return [];
}
};
const writeData = async (data) => {
    await fs.writeFile(DATA_FILE, JSON.stringify(data, null, 2), 'utf8' );
};

app.listen(PORT, () => {
    console.log( `Server chạy tại http://localhost:${PORT}` );
});

app.get( '/data' , async (req, res) => {
    const data = await readData();
    res.json(data);
    });

app.post( '/data' , async (req, res) => {
    const newData = req.body;
    const data = await readData();
    const newId = data.length > 0 ? Math.max(...data.map( item => item.id)) + 1 : 1;
    const newItem = { id: newId, ...newData };
    data.push(newItem);
    await writeData(data);
    res.json({ message: 'Ghi dữ liệu thành công' , data: newItem });
});


app.put( '/data/:id' , async (req, res) => {
    const id = parseInt(req.params.id);
    const updatedData = req.body;
    const data = await readData();
    const index = data.findIndex( item => item.id === id);
    if (index === -1) {
        return res.status( 404).json({ message: 'Không tìm thấ y dữ liệu'});
    }
    data[index] = { ...data[index], ...updatedData };
    await writeData(data);
    res.json({ message: 'Cập nhật thành công' , data: data[index] });
});


app.delete( '/data/:id' , async (req, res) => {
    const id = parseInt(req.params.id);
    const data = await readData();
    const newData = data.filter( item => item.id !== id);
    if (data.length === newData.length) {
    return res.status( 404).json({ message: 'Không tìm thấ y dữ liệu'});
    }
    await writeData(newData);
    res.json({ message: 'Xóa thành công'  });
});