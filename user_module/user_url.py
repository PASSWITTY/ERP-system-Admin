from flask import Blueprint

from user_module.user_model import User
from flask_jwt_extended import current_user, jwt_required

user_bp = Blueprint("user_blueprint", __name__)

@user_bp.route("/login", methods=["POST"])
def login():
    return User().login()

@user_bp.route("/update-password", methods=["POST"])
def change_password():
    return User().change_password()

@user_bp.route("/renew-token", methods=["POST"])
@jwt_required(refresh=True)
def renew_token():
    user = current_user
    return User().renew_token()

@user_bp.route("/list-user-categories", methods=["POST"])
@jwt_required()
def list_user_categories():
    user = current_user
    return User().list_user_categories(user)


@user_bp.route("/create-user", methods=["POST"])
@jwt_required()
def create_user():
    user = current_user
    return User().create_user(user)

@user_bp.route("/list-users", methods=["POST"])
@jwt_required()
def list_users():
    user = current_user
    return User().list_users(user)

@user_bp.route("/get-user-details", methods=["POST"])
@jwt_required()
def get_user_details():
    user = current_user
    return User().get_user_details(user)