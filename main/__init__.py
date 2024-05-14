import os
from sched import scheduler
from flask import Flask
from flask_cors import CORS

# from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from datetime import timedelta
from flask_jwt_extended import JWTManager
from scheduler.celeryapp import make_celery
from dotenv import load_dotenv 
load_dotenv('.env')

app = Flask(__name__)

app.config['APP_URL'] = os.environ.get('APP_URL')
app.config['DEBUG'] = os.environ.get('DEBUG')

# App Configurations
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('MYSQL_DATABASE_HOST')
app.config['MYSQL_DATABASE_USER'] = os.environ.get('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.environ.get('MYSQL_DATABASE_NAME')
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
# sms config
app.config['SMS_API_KEY'] = os.environ.get('SMS_API_KEY')
app.config['SMS_CLIENT_ID'] = os.environ.get('SMS_CLIENT_ID')
app.config['SMS_ACCESS_KEY'] = os.environ.get('SMS_ACCESS_KEY')
app.config['SMS_SENDER_ID'] = os.environ.get('SMS_SENDER_ID')
app.config['SMS_API_URL'] = os.environ.get('SMS_API_URL')


jwt = JWTManager(app)
CORS(app)

mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)

from user_module.user_url import user_bp
from supplier_module.inventory_suppliers.inventory_supplier_url import inventory_supplier_bp
from products_module.products_url import products_bp
from inventory_module.distribution_centers_url import distribution_center_bp  
from transport_module.transport_url import transport_bp
from payments_module.payments_url import payments_bp
from accounting_module.accounting_url import accounting_bp 
from finance_module.finance_url import finance_bp
from inventory_module.cashstock_purchase_url import cashstock_purchase_bp
from inventory_module.stockin_transit_url import stockin_transit_bp
from inventory_module.mobilephone_receive_transit_stock_url import mobilephones_receive_transit_stock_bp  
from distribution_module.manager_distribution_url import manager_distribution_bp
from distribution_module.teamleader_distribution_url import teamleader_distribution_bp
from distribution_module.agents_distribution_url import agents_distribution_bp



app.register_blueprint(user_bp, url_prefix="/api/v1/users") 
app.register_blueprint(inventory_supplier_bp, url_prefix="/api/v1/suppliers")
app.register_blueprint(products_bp, url_prefix="/api/v1/products")
app.register_blueprint(distribution_center_bp, url_prefix="/api/v1/distribution-centers") 
app.register_blueprint(transport_bp, url_prefix="/api/v1/transport")
app.register_blueprint(payments_bp, url_prefix="/api/v1/payments")
app.register_blueprint(accounting_bp, url_prefix="/api/v1/accounting") 
app.register_blueprint(finance_bp, url_prefix="/api/v1/finance")
app.register_blueprint(cashstock_purchase_bp, url_prefix="/api/v1/cashstock-purchase")
app.register_blueprint(stockin_transit_bp, url_prefix="/api/v1/transit-stock")
app.register_blueprint(manager_distribution_bp, url_prefix="/api/v1/manager-distribution")
app.register_blueprint(teamleader_distribution_bp, url_prefix="/api/v1/teamleader-distribution")
app.register_blueprint(agents_distribution_bp, url_prefix="/api/v1/agent-distribution")
app.register_blueprint(mobilephones_receive_transit_stock_bp, url_prefix="/api/v1/mobilephone-receive-transit-stock")

# Upload folder
app.config['UPLOAD_FOLDER'] = 'static/files'

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = {"id":identity['_id'], 'user_type': identity['_type']}
    return user

# celery task scheduling configs
app.config['CELERY_BACKEND'] = "redis://"
app.config['CELERY_BROKER_URL'] = "amqp://guest:guest@localhost:5672"

celery = make_celery(app)


