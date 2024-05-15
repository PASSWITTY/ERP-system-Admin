from flask import Blueprint

from sales_module.mobilephone_cash_sales_view import MobilePhoneCashSales
from flask_jwt_extended import current_user, jwt_required

mobilephone_cash_sales_bp = Blueprint("mobilephone_cashsales_blueprint", __name__)

@mobilephone_cash_sales_bp.route("/create-cash-sales", methods=["POST"])
@jwt_required()
def create_cash_sales():
    user = current_user
    return MobilePhoneCashSales().create_cash_sales(user)

@mobilephone_cash_sales_bp.route("/list-cash-sales", methods=["POST"])
@jwt_required()
def list_cash_sales():
    user = current_user
    return MobilePhoneCashSales().list_cash_sales(user)

@mobilephone_cash_sales_bp.route("/get-cash-sales-details", methods=["POST"])
@jwt_required()
def get_cash_sales_details():
    user = current_user
    return MobilePhoneCashSales().get_cash_sales_details(user)

@mobilephone_cash_sales_bp.route("/approve-cash-sales", methods=["POST"])
@jwt_required()
def approve_cash_sales():
    user = current_user
    return MobilePhoneCashSales().approve_cash_sales(user)

