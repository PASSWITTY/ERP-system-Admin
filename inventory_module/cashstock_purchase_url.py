from flask import Blueprint

from inventory_module.cashstock_purchase_view import CashStockPurchase
from flask_jwt_extended import current_user, jwt_required

cashstock_purchase_bp = Blueprint("cashstock_purchase_blueprint", __name__)

@cashstock_purchase_bp.route("/create-cash-stock-purchase", methods=["POST"])
@jwt_required()
def create_cash_stock_purchase():
    user = current_user
    return CashStockPurchase().create_cash_stock_purchase(user)

@cashstock_purchase_bp.route("/list-cash-stock-purchase", methods=["POST"])
@jwt_required()
def list_cash_stock_purchase():
    user = current_user
    return CashStockPurchase().list_cash_stock_purchase(user)

@cashstock_purchase_bp.route("/get-cash-stock-purchase-details", methods=["POST"])
@jwt_required()
def get_cash_stock_purchase_details():
    user = current_user
    return CashStockPurchase().get_cash_stock_purchase_details(user)

@cashstock_purchase_bp.route("/approve-cash-stock-purchase", methods=["POST"])
@jwt_required()
def approve_cash_stock_purchase():
    user = current_user
    return CashStockPurchase().approve_cash_stock_purchase(user)





    


    

