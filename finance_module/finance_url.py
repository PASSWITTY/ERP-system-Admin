from flask import Blueprint

from finance_module.finance_view import Finance
from flask_jwt_extended import current_user, jwt_required

finance_bp = Blueprint("finance_blueprint", __name__)

@finance_bp.route("/create-capital-injection", methods=["POST"])
@jwt_required()
def create_capital_injection():
    user = current_user
    return Finance().create_capital_injection(user)

@finance_bp.route("/list-capital-injection-entries", methods=["POST"])
@jwt_required()
def list_capital_injection_entries():
    user = current_user
    return Finance().list_capital_injection_entries(user)

@finance_bp.route("/get-capital-injection-details", methods=["POST"])
@jwt_required()
def get_capital_injection_details():
    user = current_user
    return Finance().get_capital_injection_details(user)

@finance_bp.route("/approve-capital-injection", methods=["POST"])
@jwt_required()
def approve_capital_injection():
    user = current_user
    return Finance().approve_capital_injection(user)







    


    

