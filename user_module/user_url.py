from flask import Blueprint

from user_module.user_model import User
from flask_jwt_extended import current_user, jwt_required

user_bp = Blueprint("user_blueprint", __name__)

@user_bp.route("/login", methods=["POST"])
def login():
    return User().login()

@user_bp.route("/update_password", methods=["POST"])
def change_password():
    return User().change_password()

@user_bp.route("/renew-token", methods=["POST"])
@jwt_required(refresh=True)
def renew_token():
    user = current_user
    return User().renew_token()