from flask import json, jsonify
from main import mysql
from dateutil.relativedelta import relativedelta    
from datetime import datetime, timedelta
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.alphanumeric.generate import UniqueNumber
from resources.transactions.transaction import Transaction
from resources.loans.loan_charges import LoanCharges

class PostDemandNote(): 
                
    def principal_demand_note_posting(self, details):
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       'error':'cr_d204',
                       "status": 402}
            ErrorLogger().logError(message) 
            return message

        receivable_account = details["receivable_account"]
        loan_asset_account = details["loan_asset_account"]        
        loan_id = details["loan_id"]
        global_id = details["global_id"] 
        principal_demandnote_id = details["principal_demandnote_id"]
        amount = float(details["amount"])
        amount = round(amount, 12) 
        datecreated = Localtime().gettime()
        
        smse = {'this sms':'This demand note 6 ' + loan_id}
        ErrorLogger().logError(smse)

        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       'error':'cr_d205',
                       "status": 500}
            ErrorLogger().logError(message) 
            return message

        #Try except block to handle execute task
        try:
            
            #Start of transaction posting - Debit Customer Receivable Account with demand amount

            transaction_name = 'Principal Demand Note'
            #if customer langauge is English, get english description 
            description = 'Loan principal demand note of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 
            layer4_id = UniqueNumber().transactionsdebitcreditId() 

            transaction_data = {"global_id":global_id, 
                                "entry_id":loan_id, 
                                "sub_entry_id":'',
                                "type":33,
                                "account_number":receivable_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":datecreated,
                                "layer4_id":layer4_id
                                }
            
            #Debit Customer Receivable Account with Principal demand note amount
            debit_trans = Transaction().debit_on_debit_account(transaction_data)
            #End of transaction posting

            #Start of transaction posting - Credit Loan Asset Account with demand amount

            transaction_name = 'Principal Demand Note'
            #if customer langauge is English, get english description 
            description = 'Loan principal demand note of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 


            transaction_data = {"global_id":global_id, 
                                "entry_id":loan_id, 
                                "sub_entry_id":'',
                                "type":34,
                                "account_number":loan_asset_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":datecreated,
                                "layer4_id":layer4_id
                                }
            
            #Credit Loan Asset Account with Principal demand note amount
            credit_trans = Transaction().credit_on_debit_account(transaction_data)
            #End of transaction posting

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                
                #Update demand note details, principal posted true
                cur.execute("""UPDATE loan_demand_note_details set posted = 1 WHERE id = %s""", (principal_demandnote_id))
                mysql.get_db().commit()
                
                message = {
                        "receivable_account_status":debit_trans,
                        "loan_asset_account_status":credit_trans,
                        "description":"Loan principal demand note was posted successfully",
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
                        rollback_credit_trans = Transaction().credit_on_debit_account_rollback(data)
                    else:
                        pass
                            
                message = {
                        "receivable_account_status":debit_trans,
                        "loan_asset_account_status":credit_trans,
                        'error':'cr_d206',
                        "status":201}
                ErrorLogger().logError(message) 
                return message

        except Exception as error:
            message = {'status':501,
                       'error':'cr_d207',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 
        finally:
            cur.close()
                        
    def interest_demand_note_posting(self, details):
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       'error':'cr_d208',
                       "status": 402}
            ErrorLogger().logError(message) 
            return message
     
        receivable_account = details["receivable_account"]
        interest_earned_account = details["interest_earned_account"]
        interest_demandnote_id = details["interest_demandnote_id"]
        main_demandnote_id = details["main_demandnote_id"]
        loan_id = details["loan_id"]
    
        global_id = details["global_id"]       
        amount = float(details["amount"])
        amount = round(amount, 12) 
        datecreated = Localtime().gettime()

        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       'error':'cr_d209',
                       "status": 500}
            ErrorLogger().logError(message) 
            return message
        smse = {'this sms':'This demand note 7 ' + loan_id}
        ErrorLogger().logError(smse) 
        #Try except block to handle execute task
        try:
            
            #Start of transaction posting - Debit Customer Receivable Account with demand amount

            transaction_name = 'Interest Demand Note'
            #if customer langauge is English, get english description 
            description = 'Loan interest demand note of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 
            layer4_id = UniqueNumber().transactionsdebitcreditId() 

            transaction_data = {"global_id":global_id, 
                                "entry_id":loan_id, 
                                "sub_entry_id":'',
                                "type":35,
                                "account_number":receivable_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":datecreated,
                                "layer4_id":layer4_id
                                }
            
            #Debit Customer Receivable Account with Principal demand note amount
            debit_trans = Transaction().debit_on_debit_account(transaction_data)
            #End of transaction posting
            
            #Start of transaction posting - Credit Interest Earned Account with demand amount

            transaction_name = 'Interest Demand Note'
            #if customer langauge is English, get english description 
            description = 'Loan interest demand note of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 


            transaction_data = {"global_id":global_id, 
                                "entry_id":loan_id, 
                                "sub_entry_id":'',
                                "type":36,
                                "account_number":interest_earned_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":datecreated,
                                "layer4_id":layer4_id
                                }
            
            #Credit Loan Asset Account with Principal demand note amount
            credit_trans =  Transaction().credit_on_credit_account(transaction_data)
            #End of transaction posting

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                
                #Update demand note details, interest posted true
                cur.execute("""UPDATE loan_demand_note_details set posted = 1, amount = amount + %s, amount_due = amount_due + %s WHERE id = %s""", (amount, amount, interest_demandnote_id))
                mysql.get_db().commit()
                
                cur.execute("""UPDATE loan_demand_notes set posted = 1, amount = amount + %s, amount_due = amount_due + %s WHERE id = %s""", (amount, amount, main_demandnote_id))
                mysql.get_db().commit()
            
                message = {
                        "receivable_account_status":debit_trans,
                        "interest_earned_account_status":credit_trans,
                        "description":"Loan interest demand note was posted successfully",
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
                    'error':'cr_d210',
                    "receivable_account_status":debit_trans,
                    "interest_earned_account_status":credit_trans}
                ErrorLogger().logError(message) 
                return message

        except Exception as error:
            message = {'status':501,
                       'error':'cr_d211',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 
        finally:
            cur.close()
            
    
    