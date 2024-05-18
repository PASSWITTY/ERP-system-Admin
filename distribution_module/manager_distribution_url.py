from flask import Blueprint

from distribution_module.manager_distribution_view import ManagerDistribution
from flask_jwt_extended import current_user, jwt_required

manager_distribution_bp = Blueprint("manager_distribution_blueprint", __name__)

@manager_distribution_bp.route("/list-stock-to-receive", methods=["POST"])
@jwt_required()
def list_stock_to_receive():
    user = current_user
    return ManagerDistribution().list_stock_to_receive(user)

@manager_distribution_bp.route("/list-stock-available", methods=["POST"])
@jwt_required()
def list_stock_available():
    user = current_user
    return ManagerDistribution().list_stock_available(user)

@manager_distribution_bp.route("/manager-received-dispatched-stock", methods=["POST"])
@jwt_required()
def manager_received_dispatched_stock():
    user = current_user
    return ManagerDistribution().manager_received_dispatched_stock(user)

@manager_distribution_bp.route("/create-teamleader-dispatch", methods=["POST"])
@jwt_required()
def create_teamleader_dispatch():
    user = current_user
    return ManagerDistribution().create_teamleader_dispatch(user)

@manager_distribution_bp.route("/list-teamleader-dispatched-stock", methods=["POST"])
@jwt_required()
def list_teamleader_dispatched_stock():
    user = current_user
    return ManagerDistribution().list_teamleader_dispatched_stock(user)

# @manager_distribution_bp.route("/get-teamleader-dispatched-stock-details", methods=["POST"])
# @jwt_required()
# def get_teamleader_dispatched_stock_details():
#     user = current_user
#     return ManagerDistribution().get_teamleader_dispatched_stock_details(user)

@manager_distribution_bp.route("/approve-teamleader-dispatched-stock", methods=["POST"])
@jwt_required()
def approve_teamleader_dispatched_stock():
    user = current_user
    return ManagerDistribution().approve_teamleader_dispatched_stock(user)






    


    

