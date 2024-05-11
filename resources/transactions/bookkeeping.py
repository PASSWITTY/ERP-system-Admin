from flask import Response, jsonify
from main import mysql, app
from datetime import datetime
from resources.alphanumeric.generate import UniqueNumber
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.transactions.transaction import Transaction
import uuid

class DebitCredit():

    #API to record a debit on a debit account and a credit on a credit account transactions
    def capital_injection_approve(self, details):
        if details == None:
            message = {'status':402,
                       'error':'ci_b10',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)            
            return message

        id = details["id"]
        approved_by = details["user_id"]
        
        global_id = details["global_id"]
        amount = details["amount"]
        bank_account_number = details["bank_account_number"]
        shareholder_account_number = details["shareholder_account_number"]
        settlement_date = details["settlement_date"]
        transaction_id = details["transaction_id"]

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'ci_b11',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message       
        try: 
                
            #Start of transaction posting - Debit Bank Account with amount
            transaction_name = 'Capital injection'
            description = 'Capital injection of Ksh. ' + str(amount) + ' Transaction Id ' + str(transaction_id)
          
            
            trans_uuid_ = str(uuid.uuid4())
            trans_uuid = trans_uuid_.replace("-", "" )
            trans_uuid = str(trans_uuid)
            layer1_id = 't0' + str(trans_uuid[-12:])

            transaction_data = {"global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'', 
                                "type":1,
                                "account_number":bank_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer1_id":layer1_id
                                }
            
            #Debit Bank Accont with deposit amount
            debit_trans = Transaction().debit_on_debit_account(transaction_data)
            #End of transaction posting

            
            #Start of transaction posting - Credit Shareholder Account with amount
        
            transaction_name = 'Capital injection'
            description = 'Capital injection of Ksh. ' + str(amount) + ' Transaction Id ' + str(transaction_id)

            transaction_data = {"global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":2,
                                "account_number":shareholder_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer1_id":layer1_id
                                }
            
            #Credit Shareholder Account with deposit amount
            credit_trans = Transaction().credit_on_credit_account(transaction_data)
            #End of transaction posting
            
            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                dateapproved = Localtime().gettime()
                #update capital injection status
                cur.execute("""UPDATE accounting_capital_injection_entries set status=1, approved_date = %s, approved_by = %s WHERE id = %s """, ([dateapproved, approved_by, id]))
                mysql.get_db().commit() 
                

                message = {"bank_account_transaction_status":debit_trans,
                           "shareholder_account_transaction_status":credit_trans,
                           "description":"Capital injection transaction was approved successfully!",
                           "status":200}
                return message  
            
            else:    
                #Reverse the failed transaction
                if int(debit_trans["status"]) == 200 and int(credit_trans["status"]) != 200:
                    #Rollback this debit transaction
                    data = debit_trans["data"]
                    trans_id = debit_trans["data"]["trans_id"]
                    amount = float(debit_trans["data"]["amount"])
                    if amount >0 and trans_id is not None:
                        #Delete this specific debit transaction
                        rollback_debit_trans = Transaction().debit_on_debit_account_rollback(data)
                    else:
                        pass
                
                if int(credit_trans["status"]) == 200 and int(debit_trans["status"]) != 200:
                    #Rollback this credit transaction

                    data = credit_trans["data"]
                    trans_id = credit_trans["data"]["trans_id"]
                    amount = float(credit_trans["data"]["amount"])
                    if amount >0 and trans_id is not None:
                        #Delete this specific credit transaction
                        rollback_credit_trans = Transaction().credit_on_credit_account_rollback(data)
                    else:
                        pass
                            

                message = {
                    "status":201,
                    "bank_account_transaction_status":debit_trans,
                    "shareholder_account_transaction_status":credit_trans}
                return message
            
        except Exception as error:
            message = {'status':501,
                       'error':'ci_b11',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()
