from flask import Blueprint

from inventory_module.mobilephone_stock_prices_view import StockPrice
from flask_jwt_extended import current_user, jwt_required

mobilephone_stock_price_bp = Blueprint("mobilephone_stock_price_blueprint", __name__)

@mobilephone_stock_price_bp.route("/update-stock-price", methods=["POST"])
@jwt_required()
def update_stock_price():
    user = current_user
    return StockPrice().update_stock_price(user)

@mobilephone_stock_price_bp.route("/list-stock-prices", methods=["POST"])
@jwt_required()
def list_stock_prices():
    user = current_user
    return StockPrice().list_stock_prices(user)

@mobilephone_stock_price_bp.route("/get-stock-price-details", methods=["POST"])
@jwt_required()
def get_stock_price_details():
    user = current_user
    return StockPrice().get_stock_price_details(user)

@mobilephone_stock_price_bp.route("/approve-stock-price", methods=["POST"])
@jwt_required()
def approve_stock_price():
    user = current_user
    return StockPrice().approve_stock_price(user)





    


    

