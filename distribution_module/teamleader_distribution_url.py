from flask import Blueprint

from products_module.products_view import Products
from flask_jwt_extended import current_user, jwt_required

products_bp = Blueprint("products_blueprint", __name__)

@products_bp.route("/create-phone-model", methods=["POST"])
@jwt_required()
def create_phone_model():
    user = current_user
    return Products().create_phone_model(user)

@products_bp.route("/list-phone-models", methods=["POST"])
@jwt_required()
def list_phone_models():
    user = current_user
    return Products().list_phone_models(user)

@products_bp.route("/get-phone-model-details", methods=["POST"])
@jwt_required()
def get_phone_model_details():
    user = current_user
    return Products().get_phone_model_details(user)

@products_bp.route("/approve-phone-model", methods=["POST"])
@jwt_required()
def approve_phone_model():
    user = current_user
    return Products().approve_phone_model(user)

# @products_bp.route("/inventory-item-purchase", methods=["POST"])
# @jwt_required()
# def inventory_item_purchase():
#     user = current_user
#     return Suppliers().inventory_item_purchase(user)

# @products_bp.route("/get-inventory-items-purchases/<q>", methods=["GET"])
# @jwt_required()
# def get_inventory_items_purchases(q):
#     user = current_user
#     return Suppliers().get_inventory_items_purchases(user, q)

# @products_bp.route("/get-inventory-items-purchase-details", methods=["POST"])
# @jwt_required()
# def get_inventory_items_purchase_details():
#     user = current_user
#     return Suppliers().get_inventory_items_purchase_details(user)

# @products_bp.route("/approve-inventory-item-purchase", methods=["POST"])
# @jwt_required()
# def approve_inventory_item_purchase():
#     user = current_user
#     return Suppliers().approve_inventory_item_purchase(user)


# @products_bp.route("/inventory-item-credit-purchase", methods=["POST"])
# @jwt_required()
# def inventory_item_credit_purchase():
#     user = current_user
#     return Suppliers().inventory_item_credit_purchase(user)

# @products_bp.route("/get-inventory-items-credit-purchases/<q>", methods=["GET"])
# @jwt_required()
# def get_inventory_items_credit_purchases(q):
#     user = current_user
#     return Suppliers().get_inventory_items_credit_purchases(user, q)

# @products_bp.route("/get-inventory-unpaid-supplier-invoices/<q>", methods=["GET"])
# @jwt_required()
# def get_inventory_unpaid_supplier_invoices(q):
#     user = current_user
#     return Suppliers().get_inventory_unpaid_supplier_invoices(user, q)


# @products_bp.route("/get-inventory-items-credit-purchase-details", methods=["POST"])
# @jwt_required()
# def get_inventory_items_credit_purchase_details():
#     user = current_user
#     return Suppliers().get_inventory_items_credit_purchase_details(user)

# @products_bp.route("/approve-inventory-item-credit-purchase", methods=["POST"])
# @jwt_required()
# def approve_inventory_item_credit_purchase():
#     user = current_user
#     return Suppliers().approve_inventory_item_credit_purchase(user)


# @products_bp.route("/pay-supplier-invoice", methods=["POST"])
# @jwt_required()
# def pay_supplier_invoice():
#     user = current_user
#     return Suppliers().pay_supplier_invoice(user)

# @products_bp.route("/get-supplier-invoice-payment/<q>", methods=["GET"])
# @jwt_required()
# def get_supplier_invoice_payment(q):
#     user = current_user
#     return Suppliers().get_supplier_invoice_payment(user, q)

# @products_bp.route("/get-supplier-invoice-payment-details", methods=["POST"])
# @jwt_required()
# def get_supplier_invoice_payment_details():
#     user = current_user
#     return Suppliers().get_supplier_invoice_payment_details(user)

# @products_bp.route("/approve-supplier-invoice-payment", methods=["POST"])
# @jwt_required()
# def approve_supplier_invoice_payment():
#     user = current_user
#     return Suppliers().approve_supplier_invoice_payment(user)





    


    

