from flask import Blueprint

from inventory_module.distribution_centers_view import DistributionCenter
from flask_jwt_extended import current_user, jwt_required

distribution_center_bp = Blueprint("distribution_center_blueprint", __name__)

@distribution_center_bp.route("/create-distribution-center", methods=["POST"])
@jwt_required()
def create_distribution_center():
    user = current_user
    return DistributionCenter().create_distribution_center(user)

@distribution_center_bp.route("/list-distribution-centers", methods=["POST"])
@jwt_required()
def list_distribution_center():
    user = current_user
    return DistributionCenter().list_distribution_center(user)

@distribution_center_bp.route("/get-distribution-center", methods=["POST"])
@jwt_required()
def get_distribution_center():
    user = current_user
    return DistributionCenter().get_distribution_center(user)

@distribution_center_bp.route("/approve-distribution-center", methods=["POST"])
@jwt_required()
def approve_distribution_center():
    user = current_user
    return DistributionCenter().approve_distribution_center(user)

@distribution_center_bp.route("/list-distribution-center-types", methods=["POST"])
@jwt_required()
def list_distribution_center_types():
    user = current_user
    return DistributionCenter().list_distribution_center_types(user)



    


    

