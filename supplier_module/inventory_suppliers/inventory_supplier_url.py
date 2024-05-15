from flask import Blueprint

from supplier_module.inventory_suppliers.inventory_supplier_view import Suppliers
from flask_jwt_extended import current_user, jwt_required

inventory_supplier_bp = Blueprint("inventory_supplier_blueprint", __name__)

@inventory_supplier_bp.route("/create-inventory-supplier", methods=["POST"])
@jwt_required()
def create_inventory_supplier():
    user = current_user
    return Suppliers().create_inventory_supplier(user)

@inventory_supplier_bp.route("/list-inventory-suppliers", methods=["POST"])
@jwt_required()
def list_inventory_suppliers():
    user = current_user
    return Suppliers().list_inventory_suppliers(user)

@inventory_supplier_bp.route("/get-inventory-supplier-details", methods=["POST"])
@jwt_required()
def get_inventory_supplier_details():
    user = current_user
    return Suppliers().get_inventory_supplier_details(user)

@inventory_supplier_bp.route("/approve-inventory-supplier", methods=["POST"])
@jwt_required()
def approve_inventory_supplier():
    user = current_user
    return Suppliers().approve_inventory_supplier(user)

