const express = require('express');
const router = express.Router();
const Post = require('../models/Post'); // Import the Post model

// Create a new post
router.post('/', async (req, res) => {
    try {
        const { user_id, content, image_url } = req.body;
        const newPost = await Post.create(user_id, content, image_url);
        res.status(201).json(newPost);
    } catch (error) {
        console.error('Error creating post:', error);
        res.status(500).json({ message: 'Server error' });
    }
});

// Get all posts (or posts by a specific user)
router.get('/', async (req, res) => {
    try {
        const { user_id } = req.query;
        let posts;
        if (user_id) {
            posts = await Post.findByUserId(user_id);
        } else {
            posts = await Post.findAll();
        }
        res.status(200).json(posts);
    } catch (error) {
        console.error('Error fetching posts:', error);
        res.status(500).json({ message: 'Server error' });
    }
});

// Get a single post by ID
router.get('/:id', async (req, res) => {
    try {
        const post = await Post.findById(req.params.id);
        if (!post) {
            return res.status(404).json({ message: 'Post not found' });
        }
        res.status(200).json(post);
    } catch (error) {
        console.error('Error fetching post by ID:', error);
        res.status(500).json({ message: 'Server error' });
    }
});

// Update a post
router.put('/:id', async (req, res) => {
    try {
        const { content, image_url } = req.body;
        const updatedPost = await Post.update(req.params.id, content, image_url);
        if (!updatedPost) {
            return res.status(404).json({ message: 'Post not found' });
        }
        res.status(200).json(updatedPost);
    } catch (error) {
        console.error('Error updating post:', error);
        res.status(500).json({ message: 'Server error' });
    }
});

// Delete a post
router.delete('/:id', async (req, res) => {
    try {
        const success = await Post.delete(req.params.id);
        if (!success) {
            return res.status(404).json({ message: 'Post not found' });
        }
        res.status(204).send(); // No content for successful deletion
    } catch (error) {
        console.error('Error deleting post:', error);
        res.status(500).json({ message: 'Server error' });
    }
});

module.exports = router;