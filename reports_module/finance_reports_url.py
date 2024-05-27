from flask import Blueprint

from reports_module.finance_reports_model import FinanceReports
from flask_jwt_extended import current_user, jwt_required

finance_reports_bp = Blueprint("finance_reports_blueprint", __name__)

@finance_reports_bp.route("/get-assets-accounts", methods=["POST"])
# @jwt_required(refresh=True)
@jwt_required()
def get_assets_accounts():
    user = current_user
    return FinanceReports().get_assets_accounts(user)

@finance_reports_bp.route("/get-liability-accounts", methods=["POST"])
# @jwt_required(refresh=True)
@jwt_required()
def get_liability_accounts():
    user = current_user
    return FinanceReports().get_liability_accounts(user)

@finance_reports_bp.route("/get-equity-accounts", methods=["POST"])
# @jwt_required(refresh=True)
@jwt_required()
def get_equity_accounts():
    user = current_user
    return FinanceReports().get_equity_accounts(user)


@finance_reports_bp.route("/get-profit-loss", methods=["POST"])
# @jwt_required(refresh=True)
@jwt_required()
def get_profit_loss():
    user = current_user
    return FinanceReports().get_profit_loss(user)


@finance_reports_bp.route("/get-shareholder-equity", methods=["POST"])
# @jwt_required(refresh=True)
@jwt_required()
def get_shareholder_equity():
    user = current_user
    return FinanceReports().get_shareholder_equity(user)


@finance_reports_bp.route("/get-shareholder-funds", methods=["POST"])
# @jwt_required(refresh=True)
@jwt_required()
def get_shareholder_funds():
    user = current_user
    return FinanceReports().get_shareholder_funds(user)


