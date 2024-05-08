from flask import Blueprint

from payments_module.payments_view import Payments
from flask_jwt_extended import current_user, jwt_required

payments_bp = Blueprint("payments_blueprint", __name__)

@payments_bp.route("/list-payments-modes", methods=["POST"])
@jwt_required()
def list_payments_modes():
    user = current_user
    return Payments().list_payments_modes(user)







    


    

