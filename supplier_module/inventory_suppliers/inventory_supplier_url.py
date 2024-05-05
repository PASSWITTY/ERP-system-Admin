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

# @inventory_supplier_bp.route("/get-inventory-supplier-details", methods=["POST"])
# @jwt_required()
# def get_inventory_supplier_details():
#     user = current_user
#     return Suppliers().get_inventory_supplier_details(user)

# @inventory_supplier_bp.route("/approve-inventory-supplier", methods=["POST"])
# @jwt_required()
# def approve_inventory_supplier():
#     user = current_user
#     return Suppliers().approve_inventory_supplier(user)

# @inventory_supplier_bp.route("/inventory-item-purchase", methods=["POST"])
# @jwt_required()
# def inventory_item_purchase():
#     user = current_user
#     return Suppliers().inventory_item_purchase(user)

# @inventory_supplier_bp.route("/get-inventory-items-purchases/<q>", methods=["GET"])
# @jwt_required()
# def get_inventory_items_purchases(q):
#     user = current_user
#     return Suppliers().get_inventory_items_purchases(user, q)

# @inventory_supplier_bp.route("/get-inventory-items-purchase-details", methods=["POST"])
# @jwt_required()
# def get_inventory_items_purchase_details():
#     user = current_user
#     return Suppliers().get_inventory_items_purchase_details(user)

# @inventory_supplier_bp.route("/approve-inventory-item-purchase", methods=["POST"])
# @jwt_required()
# def approve_inventory_item_purchase():
#     user = current_user
#     return Suppliers().approve_inventory_item_purchase(user)


# @inventory_supplier_bp.route("/inventory-item-credit-purchase", methods=["POST"])
# @jwt_required()
# def inventory_item_credit_purchase():
#     user = current_user
#     return Suppliers().inventory_item_credit_purchase(user)

# @inventory_supplier_bp.route("/get-inventory-items-credit-purchases/<q>", methods=["GET"])
# @jwt_required()
# def get_inventory_items_credit_purchases(q):
#     user = current_user
#     return Suppliers().get_inventory_items_credit_purchases(user, q)

# @inventory_supplier_bp.route("/get-inventory-unpaid-supplier-invoices/<q>", methods=["GET"])
# @jwt_required()
# def get_inventory_unpaid_supplier_invoices(q):
#     user = current_user
#     return Suppliers().get_inventory_unpaid_supplier_invoices(user, q)


# @inventory_supplier_bp.route("/get-inventory-items-credit-purchase-details", methods=["POST"])
# @jwt_required()
# def get_inventory_items_credit_purchase_details():
#     user = current_user
#     return Suppliers().get_inventory_items_credit_purchase_details(user)

# @inventory_supplier_bp.route("/approve-inventory-item-credit-purchase", methods=["POST"])
# @jwt_required()
# def approve_inventory_item_credit_purchase():
#     user = current_user
#     return Suppliers().approve_inventory_item_credit_purchase(user)


# @inventory_supplier_bp.route("/pay-supplier-invoice", methods=["POST"])
# @jwt_required()
# def pay_supplier_invoice():
#     user = current_user
#     return Suppliers().pay_supplier_invoice(user)

# @inventory_supplier_bp.route("/get-supplier-invoice-payment/<q>", methods=["GET"])
# @jwt_required()
# def get_supplier_invoice_payment(q):
#     user = current_user
#     return Suppliers().get_supplier_invoice_payment(user, q)

# @inventory_supplier_bp.route("/get-supplier-invoice-payment-details", methods=["POST"])
# @jwt_required()
# def get_supplier_invoice_payment_details():
#     user = current_user
#     return Suppliers().get_supplier_invoice_payment_details(user)

# @inventory_supplier_bp.route("/approve-supplier-invoice-payment", methods=["POST"])
# @jwt_required()
# def approve_supplier_invoice_payment():
#     user = current_user
#     return Suppliers().approve_supplier_invoice_payment(user)





    


    

