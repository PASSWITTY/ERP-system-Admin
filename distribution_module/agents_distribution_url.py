from flask import Blueprint

from distribution_module.agents_distribution_view import AgentsDistribution
from flask_jwt_extended import current_user, jwt_required

agents_distribution_bp = Blueprint("agents_distribution_blueprint", __name__)

@agents_distribution_bp.route("/list-stock-to-receive", methods=["POST"])
@jwt_required()
def list_stock_to_receive():
    user = current_user
    return AgentsDistribution().list_stock_to_receive(user)

@agents_distribution_bp.route("/list-stock-available", methods=["POST"])
@jwt_required()
def list_stock_available():
    user = current_user
    return AgentsDistribution().list_stock_available(user)

@agents_distribution_bp.route("/agent-receive-dispatched-stock", methods=["POST"])
@jwt_required()
def agent_receive_dispatched_stock():
    user = current_user
    return AgentsDistribution().agent_receive_dispatched_stock(user)





    


    

