const pool = require('../server'); // Import the MySQL connection pool

class Post {
    static async create(postData) {
        const { user_id, content } = postData;
        const [result] = await pool.promise().query(
            'INSERT INTO posts (user_id, content) VALUES (?, ?)',
            [user_id, content]
        );
        return { id: result.insertId, ...postData };
    }

    static async findById(id) {
        const [rows] = await pool.promise().query('SELECT * FROM posts WHERE id = ?', [id]);
        return rows[0];
    }

    static async findAll() {
        const [rows] = await pool.promise().query('SELECT * FROM posts');
        return rows;
    }

    static async update(id, postData) {
        const { content } = postData;
        const [result] = await pool.promise().query(
            'UPDATE posts SET content = ? WHERE id = ?',
            [content, id]
        );
        return result.affectedRows > 0;
    }

    static async delete(id) {
        const [result] = await pool.promise().query('DELETE FROM posts WHERE id = ?', [id]);
        return result.affectedRows > 0;
    }
}

module.exports = Post;