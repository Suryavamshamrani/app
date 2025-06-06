const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors'); // Make sure to install: npm install cors
const bodyParser = require('body-parser');
require('dotenv').config();
const mysql = require('mysql2');

const app = express();
const PORT = process.env.PORT || 5002;

// Middleware
app.use(cors()); // This will allow all origins. For production, you should restrict this.
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Routes
const userRoutes = require('./routes/users');
const postRoutes = require('./routes/posts');
app.use('/api/users', userRoutes);
app.use('/api/posts', postRoutes);

// Default route
app.get('/', (req, res) => {
  res.send('Node.js API for Social Media Platform');
});

// Connect to MongoDB
// Remove the MongoDB connection code
// mongoose.connect(process.env.MONGO_URI, {
//     useNewUrlParser: true,
//     useUnifiedTopology: true,
// })
// .then(() => console.log('MongoDB connected'))
// .catch(err => console.error(err));

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

// Create a MySQL connection pool
const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'your_mysql_user',
    password: process.env.DB_PASSWORD || 'your_mysql_password',
    database: process.env.DB_NAME || 'your_mysql_database',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

// Test MySQL connection
pool.getConnection((err, connection) => {
    if (err) {
        console.error('Error connecting to MySQL:', err.message);
        return;
    }
    console.log('Connected to MySQL database!');
    connection.release(); // Release the connection
});

// Export the pool for use in other modules
module.exports = pool;