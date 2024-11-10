from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]
FIELDS = {'title', 'content'}


def get_post_by_id(post_id: int) -> dict | None:
    """
    Retrieves a post by its ID.

    Args:
        post_id (int): The ID of the post to retrieve.

    Returns:
        dict | None: The post data if found, otherwise None.
    """
    return next((post for post in POSTS if post['id'] == post_id), None)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


def generate_id():
    """Generates unique post id based on highest post id in the database"""
    return max(post['id'] for post in POSTS) + 1 if POSTS else 1


@app.route('/api/posts', methods=['POST'])
def add_post():
    new_post = request.get_json()

    if new_post is None:
        return jsonify({"error": "Invalid JSON format"}), 400

    missing_fields = [field for field in FIELDS if not new_post.get(field)]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    new_post['id'] = generate_id()
    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = get_post_by_id(post_id)

    if post is None:
        return jsonify({'error': f'There is no post with id {post_id}.'}), 404

    POSTS.remove(post)

    return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = get_post_by_id(post_id)

    if post is None:
        return jsonify({'error': f'There is no post with id {post_id}.'}), 404

    data = request.get_json(post_id)
    post['title'] = data.get('title', post['title'])
    post['content'] = data.get('content', post['content'])
    return jsonify(post), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
