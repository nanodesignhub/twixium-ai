import os
import sys
# DON\'T CHANGE THIS LINE
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template, send_from_directory, jsonify, request, logging
from flask_sqlalchemy import SQLAlchemy
from src.models.user_model import db, User
from src.routes.auth import auth_bp
from src.routes.content import content_bp
from src.routes.social import social_bp
from src.routes.admin import admin_bp
from src.routes.init import init_bp
from src.models.admin_models import update_user_model
import logging
from datetime import timedelta

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///twixium.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure logging
logging.basicConfig(level=logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(content_bp, url_prefix="/api/content")
app.register_blueprint(social_bp, url_prefix="/api/social")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(init_bp)

# Create database tables
with app.app_context():
    db.create_all()
    # Update user model with role field if needed
    update_user_model()
    # Create admin user
    from src.routes.admin import create_admin_user
    create_admin_user()

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/signup")
def signup():
    return send_from_directory("static", "signup.html")

@app.route("/login")
def login():
    return send_from_directory("static", "login.html")

@app.route("/dashboard")
def dashboard():
    return send_from_directory("static", "dashboard.html")

@app.route("/admin")
def admin_dashboard():
    return send_from_directory("static", "admin.html")

@app.route("/admin-login")
def admin_login():
    return send_from_directory("static", "admin-login.html")

@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

@app.route("/api/health")
def health_check():
    return jsonify({"status": "healthy"})

@app.errorhandler(404)
def not_found(e):
    return send_from_directory("static", "index.html")

@app.errorhandler(500)
def server_error(e):
    app.logger.error(f"Server error: {str(e)}")
    return jsonify({"error": "Internal server error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


