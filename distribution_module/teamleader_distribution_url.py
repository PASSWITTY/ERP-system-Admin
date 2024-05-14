from flask import Blueprint

from distribution_module.teamleader_distribution_view import TeamLeaderDistribution
from flask_jwt_extended import current_user, jwt_required

teamleader_distribution_bp = Blueprint("teamleader_distribution_blueprint", __name__)

@teamleader_distribution_bp.route("/dispatch-stock", methods=["POST"])
@jwt_required()
def dispatch_stock():
    user = current_user
    return TeamLeaderDistribution().dispatch_stock(user)

@teamleader_distribution_bp.route("/list-dispatched-stock", methods=["POST"])
@jwt_required()
def list_dispatched_stock():
    user = current_user
    return TeamLeaderDistribution().list_dispatched_stock(user)

@teamleader_distribution_bp.route("/get-dispatched-stock-details", methods=["POST"])
@jwt_required()
def get_dispatched_stock_details():
    user = current_user
    return TeamLeaderDistribution().get_dispatched_stock_details(user)

@teamleader_distribution_bp.route("/approve-dispatched-stock", methods=["POST"])
@jwt_required()
def approve_dispatched_stock():
    user = current_user
    return TeamLeaderDistribution().approve_dispatched_stock(user)


@teamleader_distribution_bp.route("/receive-dispatched-stock", methods=["POST"])
@jwt_required()
def receive_dispatched_stock():
    user = current_user
    return TeamLeaderDistribution().receive_dispatched_stock(user)



    


    

