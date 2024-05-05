from flask import Blueprint

from accounts_module.accounts_model import Account
from flask_jwt_extended import current_user, jwt_required


accounts_bp = Blueprint("accounts_blueprint", __name__)

@accounts_bp.route("/create_account", methods=["POST"])
@jwt_required()
def create_account():
    user = current_user
    return Account().create_account(user)

@accounts_bp.route("/get-accounts-types/<q>", methods=["GET"])
@jwt_required()
def get_accounts_types(q):
    user = current_user
    return Account().get_accounts_types(user, q)

@accounts_bp.route("/get-accounts-categories/<q>", methods=["GET"])
@jwt_required()
def get_accounts_categories(q):
    user = current_user
    return Account().get_accounts_categories(user, q)

@accounts_bp.route("/get-accounts-sub-categories/<q>", methods=["GET"])   
@jwt_required()
def get_accounts_sub_categories(q):
    user = current_user
    return Account().get_accounts_sub_categories(user, q)

@accounts_bp.route("/get-accounts/<q>", methods=["GET"])
@jwt_required()
def get_accounts(q):
    user = current_user
    return Account().get_accounts(user, q)

@accounts_bp.route("/get-account/<id>", methods=["GET"])
@jwt_required()
def get_account(id):
    user = current_user
    return Account().get_account(user, id)

@accounts_bp.route("/approve-new-account", methods=["POST"])
@jwt_required()
def approve_new_account():
    user = current_user
    return Account().approve_new_account(user)

@accounts_bp.route("/approve-default-account", methods=["POST"])
@jwt_required()
def approve_default_account():
    user = current_user
    return Account().approve_default_account(user)

@accounts_bp.route("/get-default-accounts/<q>", methods=["GET"])
@jwt_required()
def get_default_accounts(q):
    user = current_user
    return Account().get_default_accounts(user, q)

@accounts_bp.route("/setup-default-accounts", methods=["POST"])
@jwt_required()
def setup_default_accounts():
    user = current_user
    return Account().setup_default_accounts(user)
    
@accounts_bp.route("/get-specific-accounts", methods=["POST"])
@jwt_required()
def get_specific_accounts():
    user = current_user
    return Account().get_specific_accounts(user)

@accounts_bp.route("/get-specific-accounts-by-type", methods=["POST"])
@jwt_required()
def get_specific_accounts_by_type():
    user = current_user
    return Account().get_specific_accounts_by_type(user)

@accounts_bp.route("/get-funds-transfer-accounts", methods=["POST"])
@jwt_required()
def get_funds_transfer_accounts():
    user = current_user
    return Account().get_funds_transfer_accounts(user)

@accounts_bp.route("/get-specific-account/<q>/<y>/<z>", methods=["GET"])
@jwt_required()
def get_specific_account(q, y, z):
    user = current_user
    return Account().get_specific_account(user, q, y, z)



    



    