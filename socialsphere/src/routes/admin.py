from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from src.models.user_model import db, User
from src.models.admin_models import AdminDashboard, UserManagement, SubscriptionManagement, PaymentManagement, SettingsManagement

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("You do not have administrative access.")
        return redirect(url_for("auth_bp.login"))
    return render_template("admin.html")

@admin_bp.route("/users")
@login_required
def admin_users():
    if not current_user.is_admin:
        flash("You do not have administrative access.")
        return redirect(url_for("auth_bp.login"))
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@admin_bp.route("/subscriptions")
@login_required
def admin_subscriptions():
    if not current_user.is_admin:
        flash("You do not have administrative access.")
        return redirect(url_for("auth_bp.login"))
    # Placeholder for subscription data
    return jsonify({"message": "Subscription data will be displayed here."})

@admin_bp.route("/payments")
@login_required
def admin_payments():
    if not current_user.is_admin:
        flash("You do not have administrative access.")
        return redirect(url_for("auth_bp.login"))
    # Placeholder for payment data
    return jsonify({"message": "Payment data will be displayed here."})

@admin_bp.route("/settings")
@login_required
def admin_settings():
    if not current_user.is_admin:
        flash("You do not have administrative access.")
        return redirect(url_for("auth_bp.login"))
    # Placeholder for settings data
    return jsonify({"message": "Settings will be managed here."})

# Admin user creation function (for initial setup)
def create_admin_user():
    with admin_bp.app.app_context():
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@twixium.ai")
        admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")

        if not User.query.filter_by(email=admin_email).first():
            admin_user = User(email=admin_email, is_admin=True)
            admin_user.set_password(admin_password)
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user {admin_email} created.")
        else:
            print(f"Admin user {admin_email} already exists.")



