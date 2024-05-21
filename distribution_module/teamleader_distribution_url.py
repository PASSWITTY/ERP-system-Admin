from flask import Blueprint

from distribution_module.teamleader_distribution_view import TeamLeaderDistribution
from flask_jwt_extended import current_user, jwt_required

teamleader_distribution_bp = Blueprint("teamleader_distribution_blueprint", __name__)


@teamleader_distribution_bp.route("/list-stock-to-receive", methods=["POST"])
@jwt_required()
def list_stock_to_receive():
    user = current_user
    return TeamLeaderDistribution().list_stock_to_receive(user)

@teamleader_distribution_bp.route("/list-stock-available", methods=["POST"])
@jwt_required()
def list_stock_available():
    user = current_user
    return TeamLeaderDistribution().list_stock_available(user)

@teamleader_distribution_bp.route("/teamleader-receive-dispatched-stock", methods=["POST"])
@jwt_required()
def teamleader_receive_dispatched_stock():
    user = current_user
    return TeamLeaderDistribution().teamleader_receive_dispatched_stock(user)

@teamleader_distribution_bp.route("/create-agent-dispatch", methods=["POST"])
@jwt_required()
def create_agent_dispatch():
    user = current_user
    return TeamLeaderDistribution().create_agent_dispatch(user)

@teamleader_distribution_bp.route("/list-agent-dispatched-stock", methods=["POST"])
@jwt_required()
def list_agent_dispatched_stock():
    user = current_user
    return TeamLeaderDistribution().list_agent_dispatched_stock(user)

# @teamleader_distribution_bp.route("/get-teamleader-dispatched-stock-details", methods=["POST"])
# @jwt_required()
# def get_teamleader_dispatched_stock_details():
#     user = current_user
#     return TeamLeaderDistribution().get_teamleader_dispatched_stock_details(user)

@teamleader_distribution_bp.route("/approve-agent-dispatched-stock", methods=["POST"])
@jwt_required()
def approve_agent_dispatched_stock():
    user = current_user
    return TeamLeaderDistribution().approve_agent_dispatched_stock(user)


# @teamleader_distribution_bp.route("/dispatch-stock", methods=["POST"])
# @jwt_required()
# def dispatch_stock():
#     user = current_user
#     return TeamLeaderDistribution().dispatch_stock(user)

# @teamleader_distribution_bp.route("/list-dispatched-stock", methods=["POST"])
# @jwt_required()
# def list_dispatched_stock():
#     user = current_user
#     return TeamLeaderDistribution().list_dispatched_stock(user)

# @teamleader_distribution_bp.route("/get-dispatched-stock-details", methods=["POST"])
# @jwt_required()
# def get_dispatched_stock_details():
#     user = current_user
#     return TeamLeaderDistribution().get_dispatched_stock_details(user)

# @teamleader_distribution_bp.route("/approve-dispatched-stock", methods=["POST"])
# @jwt_required()
# def approve_dispatched_stock():
#     user = current_user
#     return TeamLeaderDistribution().approve_dispatched_stock(user)


# @teamleader_distribution_bp.route("/receive-dispatched-stock", methods=["POST"])
# @jwt_required()
# def receive_dispatched_stock():
#     user = current_user
#     return TeamLeaderDistribution().receive_dispatched_stock(user)



    


    

