from flask import Response, json, jsonify
from main import mysql
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.alphanumeric.generate import UniqueNumber
from resources.transactions.transaction import Transaction


class AccountStatementReport():
  
    #API to generate sms wallet account statement
    def sms_statement(self, details):
        if details == None:
            message = {'status':402,
                       'error':'stm_06',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message
     
        account_number = details["account_number"]
        account_type = details["account_type"]
        account_name = details["account_name"]

        account_details = {
            "account_name":account_name,
            "account_number":account_number
        }
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'stm_07',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message

        try:
            trans = []
            # trans_no = 0
            cur.execute("""SELECT settlement_date, id, transaction_type, description, debit_amount, credit_amount, balance_after FROM transactions WHERE status =1 AND account_number = %s ORDER BY id DESC LIMIT 10""", [account_number])
            transactions = cur.fetchall() 
            cur.close()
            if transactions:       
                
                for transaction in transactions:

                    value_date = transaction["settlement_date"].strftime('%d-%m-%Y') 
                    # trans_no = trans_no + 1
                    type = int(transaction["transaction_type"])
                    
                    if type == 12:
                        transaction_name = "Loan disbursement"
                        
                    elif type == 13:
                        transaction_name = "Wallet Withdraw"
                    
                    elif type == 17:
                            transaction_name = "Mpesa Charges"
                            
                    elif type == 59:
                        transaction_name = "Charge Payment"
                    
                    elif type == 20:
                        transaction_name = "Wallet Deposit"
                    
                    elif type == 21:
                        transaction_name = "Principal Payment"
                    
                    elif type == 23:
                        transaction_name = "Interest Payment"
                    
                    elif type == 29:
                        transaction_name = "Charge Payment"
                    
                    elif type == 47:
                        transaction_name = "Rollover Fee Payment"
                    
                    elif type == 51:
                        transaction_name = "Fine Payment"
                    
                    elif type == 55:
                        transaction_name = "Charge Payment"
                    else:
                        transaction_name = ""
                        
                    
                    increase_amount = float(transaction["debit_amount"])
                    if increase_amount > 0:
                        amount = round(increase_amount,2)
                        
                    decrease_amount = float(transaction["credit_amount"])
                    if decrease_amount > 0:
                        amount = round(decrease_amount,2)
                    

                    if account_type <= 7 or account_type in [15, 16, 18]:

                        payload = {
                            # "value_date":value_date,
                            # "transaction_id":transaction["id"],
                            # "transaction_name":transaction["transaction_name"],
                            # "description":transaction["description"],
                            # "increase_amount":float(transaction["debit_amount"]),
                            # "decrease_amount":float(transaction["credit_amount"]),
                            # "balance":float(transaction["balance_after"]),
                            "sms":f"{value_date} {transaction_name} {amount}\n" 
                        }
                        trans.append(payload) 

                    else:
                        payload = {
                            # "value_date":value_date,
                            # "transaction_id":transaction["id"],
                            # "transaction_name":transaction["transaction_name"],
                            # "description":transaction["description"],
                            # "decrease_amount":float(transaction["credit_amount"]),
                            # "increase_amount":float(transaction["debit_amount"]),                            
                            # "balance":float(transaction["balance_after"]),
                            "sms":f"{value_date} {transaction_name} {amount}\n"
                        }
                        trans.append(payload)
                if trans  !='':
                    sms_message = ''
                    for sms in trans:
                        sms_message += sms["sms"]
                else:
                    sms_message = "Your wallet account does not have any transaction"
                
                message = {"status":200,
                           "description":"Account found",
                           "account_details":account_details,
                           "transactions":sms_message
                           }
                return message
            else:
                message = {"status":201,
                           'error':'stm_08',
                           "description":"Transactions not found",
                           "account_details":account_details,
                           }
                ErrorLogger().logError(message)
                return message

        except Exception as error:
            message = {'status':501,
                       'error':'stm_09',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message
        
        
    #API to generate customer mobile wallet account statement
    def mobile_statement(self, details):
        if details == None:
            message = {'status':402,
                       'error':'stm_06',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message
     
        account_number = details["account_number"]
        account_type = details["account_type"]
        account_name = details["account_name"]
        start_date = details["start_date"]
        end_date = details["end_date"]


        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'stm_07',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message

        try:
            trans = []
            # trans_no = 0
            try:
                cur.execute("""SELECT settlement_date, id, transaction_type, transaction_name, description, debit_amount, credit_amount, balance_after FROM transactions WHERE status =1 AND account_number = %s ORDER BY id DESC""", (account_number))
                transactions = cur.fetchall() 
                if transactions:       
                    
                    for transaction in transactions:
                    
                        value_date = transaction["settlement_date"].strftime('%Y-%m-%d %H:%M:%S') 
                        # trans_no = trans_no + 1
                        type = int(transaction["transaction_type"])
                        
                        if type == 12:
                            transaction_name = "Loan disbursement"
                            transaction_type = "credit"
                            
                        elif type == 13:
                            transaction_name = "Wallet Withdraw"
                            transaction_type = "debit"
                            
                        
                        elif type == 17:
                            transaction_name = "Mpesa Charges"
                            transaction_type = "debit"

                        
                        elif type == 59:
                            transaction_name = "Charge Payment"
                            transaction_type = "debit"

                        
                        elif type == 20:
                            transaction_name = "Wallet Deposit"
                            transaction_type = "credit"

                        
                        elif type == 21:
                            transaction_name = "Principal Payment"
                            transaction_type = "debit"

                        
                        elif type == 23:
                            transaction_name = "Interest Payment"
                            transaction_type = "debit"

                        
                        elif type == 29:
                            transaction_name = "Charge Payment"
                            transaction_type = "debit"

                        
                        elif type == 47:
                            transaction_name = "Rollover Fee Payment"
                            transaction_type = "debit"

                        
                        elif type == 51:
                            transaction_name = "Fine Payment"
                            transaction_type = "debit"

                        
                        elif type == 55:
                            transaction_name = "Charge Payment"
                            transaction_type = "debit"

                        else:
                            transaction_name = ''
                            transaction_type = ''
                            
                            
                        
                        increase_amount = float(transaction["debit_amount"])
                        if increase_amount > 0:
                            amount = round(increase_amount,4)
                            
                        decrease_amount = float(transaction["credit_amount"])
                        if decrease_amount > 0:
                            amount = round(decrease_amount,4)
                            
                        balance = float(transaction["balance_after"])
                        balance = round(balance,4)
                        
                    
                        payload = {
                            "id":transaction["id"],                                             
                            "name":transaction_name,
                            "type":transaction_type,
                            "amount": amount,                        
                            "balance": balance,
                            "description":transaction["description"],                       
                            "value_date":value_date
                        
                        }
                        trans.append(payload)
                        
                        
                    if trans  !='':
                        
                        sms_message = trans
                    else:
                        sms_message = "Your wallet account does not have any transaction"
                    
                    message = {"status":200,
                            "description":"Account statement details were found",
                            "wallet_transactions":sms_message
                            }
                    return message
                else:
                    message = {"status":201,
                               'error':'stm_08',
                               "description":"Wallet does not have transactions",
                               "wallet_transactions":[]
                            }
                    ErrorLogger().logError(message)
                    return message
            except:
                message = {"status":201,
                           "description":"Wallet does not have transactions",
                           "wallet_transactions":[]
                            }
                ErrorLogger().logError(message)
                return message
                

        except Exception as error:
            message = {'status':501,
                       'error':'stm_09',
                       'wallet_transactions':[],
                       'description':'Transaction had an error. Error description ' + format(error)}                       
            ErrorLogger().logError(message) 
            return message
        finally:
            cur.close()