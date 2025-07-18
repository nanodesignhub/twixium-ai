# src/main.py

import os
import logging
from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Import models and blueprints (using relative imports as main.py is inside src/)
from models.user_model import db, User
from models.admin_models import AdminDashboard, UserManagement, SubscriptionManagement, PaymentManagement, SettingsManagement, update_user_model
from routes.auth import auth_bp
from routes.admin import admin_bp, create_admin_user
from routes.content import content_bp
from routes.social import social_bp
from routes.init import init_bp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', template_folder='static')

# Load configuration from environment variables or .env file
# For production, ensure these are set in your DigitalOcean environment
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_very_secret_key_that_should_be_changed')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirect to login page if not authenticated

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(content_bp)
app.register_blueprint(social_bp)
app.register_blueprint(init_bp)

# Routes for static pages (handled by the init blueprint now, but keeping for clarity if specific routes are needed)
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/features')
def features():
    return send_from_directory('static', 'features.html')

@app.route('/how_it_works')
def how_it_works():
    return send_from_directory('static', 'how_it_works.html')

@app.route('/pricing')
def pricing():
    return send_from_directory('static', 'pricing.html')

@app.route('/testimonials')
def testimonials():
    return send_from_directory('static', 'testimonials.html')

@app.route('/login')
def login():
    return send_from_directory('static', 'login.html')

@app.route('/signup')
def signup():
    return send_from_directory('static', 'signup.html')

@app.route('/terms')
def terms():
    return send_from_directory('static', 'terms.html')

@app.route('/privacy')
def privacy():
    return send_from_directory('static', 'privacy.html')

@app.route('/accessibility')
def accessibility():
    return send_from_directory('static', 'accessibility.html')

@app.route('/dashboard')
@login_required # Protect this route
def dashboard():
    return send_from_directory('static', 'dashboard.html')

@app.route('/admin')
@login_required # Protect this route, consider adding admin-specific check
def admin_dashboard():
    return send_from_directory('static', 'admin.html')


# Error handling
@app.errorhandler(404)
def not_found(error):
    logger.error(f"404 Not Found: {request.url}")
    return send_from_directory('static', 'index.html'), 404 # Redirect to home or a custom 404 page

@app.errorhandler(500)
def internal_server_error(error):
    logger.exception(f"Server error: {error}")
    # In production, you might want to render a generic error page
    return "500 Internal Server Error: The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.", 500


# Ensure database tables are created and admin user is created on first run
# This block runs when the Flask app context is pushed, typically on startup
with app.app_context():
    db.create_all() # Create database tables if they don't exist
    create_admin_user() # Create default admin user if not exists

if __name__ == '__main__':
    app.run(debug=True)
