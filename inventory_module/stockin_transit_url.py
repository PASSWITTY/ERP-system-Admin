from flask import Blueprint

from inventory_module.stockin_transit_view import TransitStock
from flask_jwt_extended import current_user, jwt_required

stockin_transit_bp = Blueprint("stockin_transit_blueprint", __name__)

@stockin_transit_bp.route("/create-stock-transit", methods=["POST"])
@jwt_required()
def create_stock_transit():
    user = current_user
    return TransitStock().create_stock_transit(user)

@stockin_transit_bp.route("/list-stock-transit", methods=["POST"])
@jwt_required()
def list_stock_transit():
    user = current_user
    return TransitStock().list_stock_transit(user)

@stockin_transit_bp.route("/get-stock-transit-details", methods=["POST"])
@jwt_required()
def get_stock_transit_details():
    user = current_user
    return TransitStock().get_stock_transit_details(user)

@stockin_transit_bp.route("/approve-stock-transit", methods=["POST"])
@jwt_required()
def approve_stock_transit():
    user = current_user
    return TransitStock().approve_stock_transit(user)





    


    

