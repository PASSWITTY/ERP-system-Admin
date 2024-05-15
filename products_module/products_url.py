from flask import Blueprint

from products_module.products_view import Products
from flask_jwt_extended import current_user, jwt_required

products_bp = Blueprint("products_blueprint", __name__)

@products_bp.route("/create-phone-model", methods=["POST"])
@jwt_required()
def create_phone_model():
    user = current_user
    return Products().create_phone_model(user)

@products_bp.route("/list-phone-models", methods=["POST"])
@jwt_required()
def list_phone_models():
    user = current_user
    return Products().list_phone_models(user)

@products_bp.route("/get-phone-model-details", methods=["POST"])
@jwt_required()
def get_phone_model_details():
    user = current_user
    return Products().get_phone_model_details(user)

@products_bp.route("/approve-phone-model", methods=["POST"])
@jwt_required()
def approve_phone_model():
    user = current_user
    return Products().approve_phone_model(user)

