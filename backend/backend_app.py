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
    Retrieve all blog posts with optional sorting by title, content, author, created, or updated.

    Query Parameters:
        - sort (str): Field to sort by.
                      Options are "title", "content", "author", "created", "updated".
        - direction (str): Sort direction.
                     Options are "asc" for ascending, "desc" for descending.

    Returns:
        JSON response with the list of sorted posts, or an error message if validation fails.
    """
    # Retrieve query parameters
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    # Get posts with sorting and validation
    result = manager.get_all_posts(sort=sort_field, direction=direction)

    # Check for errors in the result
    if "error" in result:
        return jsonify(result), 400  # Return a 400 response with the error message

    # Otherwise, return the posts
    return jsonify(result["posts"])


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Add a new blog post.

    JSON Payload:
        - title (str): The title of the post.
        - content (str): The content of the post.
        - author (str): The author of the post.

    Returns:
        JSON response with the created post data or an error message if validation fails.
    """
    new_post = request.get_json()
    if not new_post:
        return jsonify({"error": "Invalid JSON format"}), 400

    # Validate the data before adding
    error = manager.validate_data(new_post)
    if error:
        return jsonify(error), 400

    # Add the post to the storage
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
        return jsonify({'message': f'Post with ID {post_id} has been deleted successfully.'}), 200
    return jsonify({'error': f'No post found with ID {post_id}.'}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update an existing blog post by ID.

    Args:
        post_id (int): The ID of the post to update.

    Returns:
        JSON response with the updated post data or an error message if the post does not exist.
    """
    data = request.get_json()
    updated_post = manager.update_post(post_id, data)
    if updated_post:
        return jsonify(updated_post), 200
    return jsonify({'error': f'No post found with ID {post_id}.'}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search for posts based on query parameters such as title, content, or author.

    Query Parameters:
        - title (str): Search posts by title.
        - content (str): Search posts by content.
        - author (str): Search posts by author.

    Returns:
        JSON response with a list of posts that match the search criteria.
    """
    query = {key: value for key, value in request.args.items()
             if key in BlogManager.REQUIRED_FIELDS}
    results = manager.search_posts(query)
    return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
