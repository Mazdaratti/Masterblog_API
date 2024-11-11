"""
Flask Application for the Masterblog API
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from storage.storage import Storage
from blogmanager import BlogManager
from backend.storage.data import PATH

app = Flask(__name__)
CORS(app)

# Initialize storage and manager instances
storage = Storage(PATH)
manager = BlogManager(storage)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Retrieve all blog posts.

    Returns:
        JSON response with the list of all posts.
    """
    posts = manager.get_all_posts()
    return jsonify(posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Add a new blog post.

    JSON Payload:
        - title: The title of the post.
        - content: The content of the post.
        - author: The author of the post.

    Returns:
        JSON response with the created post data or an error message.
    """
    new_post = request.get_json()
    if not new_post:
        return jsonify({"error": "Invalid JSON format"}), 400

    error = manager.validate_data(new_post)
    if error:
        return jsonify(error), 400

    created_post = manager.add_post(new_post)
    return jsonify(created_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a blog post by ID.

    Args:
        post_id (int): The ID of the post to delete.

    Returns:
        JSON response with a success or error message.
    """
    success = manager.delete_post(post_id)
    if success:
        return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'}), 200
    return jsonify({'error': f'There is no post with id {post_id}.'}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update a blog post by ID.

    Args:
        post_id (int): The ID of the post to update.

    Returns:
        JSON response with the updated post data or an error message.
    """
    data = request.get_json()
    updated_post = manager.update_post(post_id, data)
    if updated_post:
        return jsonify(updated_post), 200
    return jsonify({'error': f'There is no post with id {post_id}.'}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search for posts based on query parameters.

    Returns:
        JSON response with a list of posts that match the search criteria.
    """
    query = {key: value for key, value in request.args.items() if key in BlogManager.FIELDS}
    results = manager.search_posts(query)
    return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
