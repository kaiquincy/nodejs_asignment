const { MongoClient } = require('mongodb');

const url = 'mongodb://localhost:27017';
const dbName = 'eShop';

async function run() {
  const client = new MongoClient(url);

  try {
    // 1. Connect to MongoDB
    await client.connect();
    console.log("1. Connected to MongoDB server.");

    const db = client.db(dbName);
    const orders = db.collection('OrderCollection');

    await orders.deleteMany({});

    // 2. Insert many documents into OrderCollection
    const orderDocs = [
      {
        orderid: 1,
        products: [
          {
            product_id: "quanau",
            product_name: "quan au",
            size: "XL",
            price: 10,
            quantity: 1
          },
          {
            product_id: "somi",
            product_name: "ao so mi",
            size: "XL",
            price: 10.5,
            quantity: 2
          }
        ],
        total_amount: 31,  // 10 * 1 + 10.5 * 2 = 31
        delivery_address: "Hanoi"
      },
      {
        orderid: 2,
        products: [
          {
            product_id: "somi",
            product_name: "ao so mi",
            size: "L",
            price: 10.5,
            quantity: 1
          },
          {
            product_id: "quanau",
            product_name: "quan au",
            size: "M",
            price: 10,
            quantity: 3
          }
        ],
        total_amount: 40.5,  // 10.5 * 1 + 10 * 3 = 40.5
        delivery_address: "Ho Chi Minh"
      }
    ];

    const insertResult = await orders.insertMany(orderDocs);
    console.log(`2. Inserted orders with ids: ${Object.values(insertResult.insertedIds).join(', ')}\n`);

    // 3. Edit delivery_address by orderid (update orderid 1)
    const updateResult = await orders.updateOne(
      { orderid: 1 },
      { $set: { delivery_address: "Da Nang" } }
    );
    console.log(`3. Updated orderid 1's delivery address to Da Nang.\n`);

    // 4. Remove an order (remove orderid 2)
    const deleteResult = await orders.deleteOne({ orderid: 2 });
    console.log(`4. Removed order with orderid 2.\n`);

    // 5. Read all orders and display in a table
    const cursor = orders.find();
    let rowNumber = 1;
    const tableData = [];

    await cursor.forEach(order => {
      order.products.forEach(product => {
        const total = product.price * product.quantity;
        tableData.push({
          No: rowNumber,
          "Product name": product.product_name,
          Price: product.price,
          Quantity: product.quantity,
          Total: total
        });
        rowNumber++;
      });
    });

    console.log("5.Order details:");
    console.table(tableData);

    // 6. Calculate total amount
    const ordersList = await orders.find().toArray();
    const overallTotal = ordersList.reduce((sum, order) => sum + (order.total_amount || 0), 0);
    console.log(`Total amount: ${overallTotal}\n`);

    // 7. Count total quantity for product_id equal to "somi"
    let somiCount = 0;
    ordersList.forEach(order => {
      order.products.forEach(product => {
        if (product.product_id === "somi") {
          somiCount += product.quantity;
        }
      });
    });
    console.log(`7. Total quantity for product_id 'somi': ${somiCount}`);

  } catch (err) {
    console.error(err);
  } finally {
    // Close the connection
    await client.close();
    console.log("Connection closed.");
  }
}

run().catch(console.dir);
