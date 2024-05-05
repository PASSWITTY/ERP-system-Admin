from flask import json, jsonify
from main import mysql
from resources.payload.payload import Localtime
from resources.logs.logger import ErrorLogger
from resources.transactions.transaction import Transaction
from resources.alphanumeric.generate import UniqueNumber

class TaxExpenseIncurred():
    
    #API to incur tax charges
    def record_tax(self, details):
        if details == None:
            message = {"status":402,
                       "error":"tx_i001",
                       "description":"All details are required!"}
            ErrorLogger().logError(message) 
            return message

        amountpaid = details["amount"]
        global_id = details["global_id"]
        entry_id = details["entry_id"]
        
        date_created = Localtime().gettime()

        # Open A connection to the database
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       "error":"tx_i002",
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message) 
            return message

        try:  
             #get tax rate used. get tax type from config files
            cur.execute("""SELECT tax_rate FROM tax_rates WHERE status =1 AND id =3 """)
            get_tax_rate= cur.fetchone()                 
            if get_tax_rate:
                tax_rate = float(get_tax_rate["tax_rate"])  
            else:
                message = {'status':400,
                           "error":"tx_i003",
                           'description':"Tax rate is not defined!"}
                return message

            amount = (amountpaid * (tax_rate / 100))
            
            #get tax expense account
            cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number=9""")
            tax_expense_ac = cur.fetchone()                        
            if tax_expense_ac:
                tax_expense_account = tax_expense_ac["account_number"]
            else:
                message = {'status':404,
                           "error":"tx_i004",
                           'description':"Default tax expense account has not been setup!"}
                ErrorLogger().logError(message) 
                return message
            
            #get tax payable account
            cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number=10""")
            tax_payable_acc = cur.fetchone()                        
            if tax_payable_acc:
                tax_payable_account = tax_payable_acc["account_number"]
            else:
                message = {'status':404,
                           "error":"tx_i005",
                           'description':"Default tax payable account has not been setup!"}
                ErrorLogger().logError(message) 
                return message
 

            # Start of transaction posting - Debit tax expense Account with tax amount to be paid
            transaction_name = 'Tax'
            # if customer langauge is English, get english description
            description = 'Tax expense of Ksh ' + str(amount)
            # if customer langauge is Kiswahili, get swahili description
            layer4_id = UniqueNumber().transactionsdebitcreditId()

            transaction_data = {"global_id": global_id,
                                "entry_id": entry_id,
                                "sub_entry_id":'',
                                "type":43,
                                "account_number": tax_expense_account,
                                "amount": amount,
                                "transaction_name": transaction_name,
                                "description": description,
                                "settlement_date": date_created,
                                "layer4_id": layer4_id
                                }

            # Debit tax expense account
            debit_trans = Transaction().debit_on_debit_account(transaction_data)
            # End of transaction posting

            # Start of transaction posting - Credit tax payable account with tax amount due
            transaction_name = 'Tax incured'
            # if customer langauge is English, get english description
            description = 'Tax charges of Ksh ' + str(amount)
            # if customer langauge is Kiswahili, get swahili description

            transaction_data = {"global_id": global_id,
                                "entry_id": entry_id,
                                "sub_entry_id":'',
                                "type":44,
                                "account_number": tax_payable_account,
                                "amount": amount,
                                "transaction_name": transaction_name,
                                "description": description,
                                "settlement_date": date_created,
                                "layer4_id": layer4_id
                                }

            # Credit tax payable account with tax amount 
            credit_trans = Transaction().credit_on_credit_account(transaction_data)
            # End of transaction posting
            
            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                message = {
                            "status": 200,
                            "tax_expense_account_trans": debit_trans,
                            "tax_payable_account_trans": credit_trans
                    }
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
                    "error":"tx_i006",
                    "bank_account_transaction_status":debit_trans,
                    "shareholder_account_transaction_status":credit_trans}
                ErrorLogger().logError(message) 
                return message

        # Error handling
        except Exception as error:
            message = {'status':501,
                       "error":"tx_i007",
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 
        finally:
            cur.close()