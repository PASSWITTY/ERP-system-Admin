from flask import Blueprint

from distribution_module.agents_distribution_view import AgentsDistribution
from flask_jwt_extended import current_user, jwt_required

agents_distribution_bp = Blueprint("agents_distribution_blueprint", __name__)

@agents_distribution_bp.route("/dispatch-stock", methods=["POST"])
@jwt_required()
def dispatch_stock():
    user = current_user
    return AgentsDistribution().dispatch_stock(user)

@agents_distribution_bp.route("/list-dispatched-stock", methods=["POST"])
@jwt_required()
def list_dispatched_stock():
    user = current_user
    return AgentsDistribution().list_dispatched_stock(user)

@agents_distribution_bp.route("/get-dispatched-stock-details", methods=["POST"])
@jwt_required()
def get_dispatched_stock_details():
    user = current_user
    return AgentsDistribution().get_dispatched_stock_details(user)

@agents_distribution_bp.route("/approve-dispatched-stock", methods=["POST"])
@jwt_required()
def approve_dispatched_stock():
    user = current_user
    return AgentsDistribution().approve_dispatched_stock(user)


@agents_distribution_bp.route("/receive-dispatched-stock", methods=["POST"])
@jwt_required()
def receive_dispatched_stock():
    user = current_user
    return AgentsDistribution().receive_dispatched_stock(user)



    


    

