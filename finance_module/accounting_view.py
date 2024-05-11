from flask import request, Response, json, jsonify
from main import mysql, app
from accounting_module.accounting_model import Account
from resources.alphanumeric.generate import UniqueNumber
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime

class Accounting():
  
    def create_account(self, user):
        account = request.get_json()
       
        if account == None:
            message = {'status':402,
                       'error':'aa_a10',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message)

        #Try except block to handle execute task
        try:
            account["user_id"] = user["id"]
            account["owner_id"] = ''
            account["entity_id"] = 0
            account["status"] = 0
            
            api_response = Account().create_new_account(account)
            if int(api_response["status"] == 200):
                
                message = {"description":"Account was created successfully",
                           "status":200}
                return jsonify(message)
            else:
                message = {'status':201,
                           'error':'aa_a11',
                           'description':api_response["description"]}
                ErrorLogger().logError(message)
                return jsonify(message)
            
        except Exception as error:
            message = {'status':501,
                       'error':'aa_a12',
                       'description':'Account creation process failed! Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message) 
        


     
   