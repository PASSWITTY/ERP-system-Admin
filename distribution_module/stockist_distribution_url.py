from flask import Blueprint

from distribution_module.stockist_distribution_view import StockistDistribution
from flask_jwt_extended import current_user, jwt_required

stockist_distribution_bp = Blueprint("stockist_distribution_blueprint", __name__)

@stockist_distribution_bp.route("/list-available-stock-to-dispatch", methods=["POST"])
@jwt_required()
def list_available_stock_to_dispatch():
    user = current_user
    return StockistDistribution().list_available_stock_to_dispatch(user)

@stockist_distribution_bp.route("/create-manager-dispatch", methods=["POST"])
@jwt_required()
def create_manager_dispatch():
    user = current_user
    return StockistDistribution().create_manager_dispatch(user)

@stockist_distribution_bp.route("/list-manager-dispatched-stock", methods=["POST"])
@jwt_required()
def list_manager_dispatched_stock():
    user = current_user
    return StockistDistribution().list_manager_dispatched_stock(user)

# @stockist_distribution_bp.route("/get-manager-dispatched-stock-details", methods=["POST"])
# @jwt_required()
# def get_manager_dispatched_stock_details():
#     user = current_user
#     return StockistDistribution().get_manager_dispatched_stock_details(user)

@stockist_distribution_bp.route("/approve-manager-dispatched-stock", methods=["POST"])
@jwt_required()
def approve_manager_dispatched_stock():
    user = current_user
    return StockistDistribution().approve_manager_dispatched_stock(user)





    


    

