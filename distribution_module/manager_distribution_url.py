from flask import Blueprint

from distribution_module.manager_distribution_view import ManagerDistribution
from flask_jwt_extended import current_user, jwt_required

manager_distribution_bp = Blueprint("manager_distribution_blueprint", __name__)

@manager_distribution_bp.route("/dispatch-stock", methods=["POST"])
@jwt_required()
def dispatch_stock():
    user = current_user
    return ManagerDistribution().dispatch_stock(user)

@manager_distribution_bp.route("/list-dispatched-stock", methods=["POST"])
@jwt_required()
def list_dispatched_stock():
    user = current_user
    return ManagerDistribution().list_dispatched_stock(user)

@manager_distribution_bp.route("/get-dispatched-stock-details", methods=["POST"])
@jwt_required()
def get_dispatched_stock_details():
    user = current_user
    return ManagerDistribution().get_dispatched_stock_details(user)

@manager_distribution_bp.route("/approve-dispatched-stock", methods=["POST"])
@jwt_required()
def approve_dispatched_stock():
    user = current_user
    return ManagerDistribution().approve_dispatched_stock(user)


@manager_distribution_bp.route("/receive-dispatched-stock", methods=["POST"])
@jwt_required()
def receive_dispatched_stock():
    user = current_user
    return ManagerDistribution().receive_dispatched_stock(user)



    


    

