from flask import Blueprint

from inventory_module.mobilephone_receive_transit_stock_view import ReceiveTransitStock
from flask_jwt_extended import current_user, jwt_required

mobilephones_receive_transit_stock_bp = Blueprint("mobilephone_receive_transit_stock_blueprint", __name__)

@mobilephones_receive_transit_stock_bp.route("/receive-stock", methods=["POST"])
@jwt_required()
def receive_stock():
    user = current_user
    return ReceiveTransitStock().receive_stock(user)

@mobilephones_receive_transit_stock_bp.route("/list-received-stock", methods=["POST"])
@jwt_required()
def list_received_stock():
    user = current_user
    return ReceiveTransitStock().list_received_stock(user)

@mobilephones_receive_transit_stock_bp.route("/get-received-stock-details", methods=["POST"])
@jwt_required()
def get_received_stock_details():
    user = current_user
    return ReceiveTransitStock().get_received_stock_details(user)

@mobilephones_receive_transit_stock_bp.route("/approve-received-stock", methods=["POST"])
@jwt_required()
def approve_received_stock():
    user = current_user
    return ReceiveTransitStock().approve_received_stock(user)

@mobilephones_receive_transit_stock_bp.route("/list-devices", methods=["POST"])
@jwt_required()
def list_devices():
    user = current_user
    return ReceiveTransitStock().list_devices(user)





    


    

