from flask import Blueprint

from transport_module.transport_view import Transport
from flask_jwt_extended import current_user, jwt_required

transport_bp = Blueprint("transport_blueprint", __name__)

@transport_bp.route("/list-transport-modes", methods=["POST"])
@jwt_required()
def list_transport_modes():
    user = current_user
    return Transport().list_transport_modes(user)







    


    

