
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

content_bp = Blueprint("content_bp", __name__)

@content_bp.route("/create", methods=["POST"])
@login_required
def create_content():
    data = request.get_json()
    title = data.get("title")
    body = data.get("body")

    if not title or not body:
        return jsonify({"error": "Title and body are required"}), 400

    # In a real application, you would save this content to a database
    # For now, we'll just return a success message
    return jsonify({"message": "Content created successfully", "title": title, "body": body}), 201

@content_bp.route("/my_content", methods=["GET"])
@login_required
def my_content():
    # In a real application, you would fetch content belonging to the current_user
    # For now, return dummy content
    dummy_content = [
        {"id": 1, "title": "My First Post", "body": "This is the body of my first post.", "author": current_user.email},
        {"id": 2, "title": "Another Idea", "body": "Here's another great idea for content.", "author": current_user.email}
    ]
    return jsonify(dummy_content), 200


