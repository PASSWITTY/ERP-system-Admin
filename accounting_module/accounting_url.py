from flask import Blueprint

from accounting_module.accounting_view import Accounting
from flask_jwt_extended import current_user, jwt_required

accounting_bp = Blueprint("accounting_blueprint", __name__)

@accounting_bp.route("/create-account", methods=["POST"])
@jwt_required()
def create_account():
    user = current_user
    return Accounting().create_account(user)

@accounting_bp.route("/list-accounts", methods=["POST"])
@jwt_required()
def list_accounts():
    user = current_user
    return Accounting().list_accounts(user)

@accounting_bp.route("/get-account-details", methods=["POST"])
@jwt_required()
def get_account_details():
    user = current_user
    return Accounting().get_account_details(user)

@accounting_bp.route("/approve-account", methods=["POST"])
@jwt_required()
def approve_new_account():
    user = current_user
    return Accounting().approve_new_account(user)

@accounting_bp.route("/list-account-types", methods=["POST"])
@jwt_required()
def list_account_types():
    user = current_user
    return Accounting().list_account_types(user)

@accounting_bp.route("/list-account-categories", methods=["POST"])
@jwt_required()
def list_account_categories():
    user = current_user
    return Accounting().list_account_categories(user)







    


    

