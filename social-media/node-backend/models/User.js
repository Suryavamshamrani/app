const pool = require('../server'); // Import the MySQL connection pool

class User {
    static async findById(id) {
        const [rows] = await pool.promise().query('SELECT * FROM users WHERE id = ?', [id]);
        return rows[0];
    }

    static async findByEmail(email) {
        const [rows] = await pool.promise().query('SELECT * FROM users WHERE email = ?', [email]);
        return rows[0];
    }

    static async create(userData) {
        const { username, email, password } = userData;
        const [result] = await pool.promise().query(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            [username, email, password]
        );
        return { id: result.insertId, ...userData };
    }

    // Add other methods like update, delete, etc., as needed
}

module.exports = User;