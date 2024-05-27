from flask import request, Response,jsonify, json
from main import mysql,app
import uuid
from decimal import Decimal
from datetime import datetime

class AssetsReports():    

    def get_assets_accounts(self, user, details):
           # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)

         #Try except block to handle data extraction
        try:                        
            #Get assets accounts            
            cash_accs = 1
            inventory = 2
            receivable = 3
            prepaid_expenses = 4
            marketable_securities = 5  
            property_equipments = 6
            intangible_assets = 7
            other_investments = 8

            total_asset_accounts = []
            assets_data = []

            status = details['status']

            #Get total asset Balance
            cur.execute("""SELECT sum(balance) totalassets FROM accounts WHERE balance > 0 AND status = %s AND (type = %s OR type = %s OR type = %s OR type = %s OR type = %s OR type = %s OR type = %s OR type = %s) ORDER BY type ASC""", [status, cash_accs, marketable_securities, inventory, receivable, property_equipments, intangible_assets, prepaid_expenses, other_investments])
            totalasset = cur.fetchone()

            total_assets = float(totalasset['totalassets'])

            cur.execute("""SELECT id, reference_no, number, name, balance FROM accounts WHERE balance > 0 AND status = %s AND (type = %s OR type = %s OR type = %s OR type = %s OR type = %s OR type = %s OR type = %s OR type = %s) ORDER BY type ASC""", [status, cash_accs, marketable_securities, inventory, receivable, property_equipments, intangible_assets, prepaid_expenses, other_investments])
            assets = cur.fetchall()

            assets_accounts = []
            for asset in assets:
                balance = float(asset['balance']) 
                res = {
                     "accountid": asset['id'],
                     "accountref": asset['reference_no'],
                     "accountnumber": asset['number'],
                     "accountname": asset['name'],
                     "balance": balance                  

                }
                assets_accounts.append(res)
                
            total_assets_value = {"totalAssets":total_assets}
            total_asset_accounts.append(total_assets_value)

            assets_data.append(assets_accounts)
            assets_data.append(total_asset_accounts)

            
            #The response object
            message = {'status':200,
                       'response':assets_data,
                       'description':'Report details was fetched successfully'}

            return message

        except Exception as error:
            message = {'status':501,
                       'response':[],
                       'description':'Failed to fetch asset accounts records. {}'.format(error)}
            return message
        finally:
            cur.close()

    