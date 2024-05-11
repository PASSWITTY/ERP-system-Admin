from flask import Blueprint

from accounting_module.accounting_view import Accounting
from flask_jwt_extended import current_user, jwt_required

accounting_bp = Blueprint("accounting_blueprint", __name__)

@accounting_bp.route("/create-account", methods=["POST"])
@jwt_required()
def create_account():
    user = current_user
    return Accounting().create_account(user)







    


    

