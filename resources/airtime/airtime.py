from flask import Response, json, jsonify
from main import mysql
from datetime import datetime
from resources.transactions.transaction import Transaction
from resources.payload.payload import Localtime
from resources.alphanumeric.generate import UniqueNumber
from accounts_module.accounts_model import Account
from resources.accounts.accounts_class import Accounts
from resources.logs.logger import ErrorLogger


from decimal import Decimal

class AirtimeWallet():

    #API to approve airtime wallet topup when airtime dealer has been paid  
    def approve_airtime_wallet_topup(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a16',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]
        approved_by = details["user_id"]
        mpesa_account_number = details["mpesa_account_number"]
        airtime_stock_account_number = details["airtime_stock_account_number"]
        amount = float(details["amount"])
        settlement_date = details["settlement_date"]
        
        date_approved = Localtime().gettime()

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a17',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
       
        try: 
            
            #Start of transaction - Increase airtime stock Account Balance
            global_id = UniqueNumber().globalIdentifier()
            
            transaction_name = 'Airtime Wallet Topup'
            description = 'Airtime wallet topup with Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            layer4_id = UniqueNumber.transactionsdebitcreditId(self)
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":65,
                                "account_number":airtime_stock_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id

                                }
                            
            #Debit airtime stock account with amount sent to airtime dealer
            debit_trans = Transaction.debit_on_debit_account(self, transaction_data)
            #End of transaction - Increase stock account
            
            #Start of transaction - Decrease Mpesa Account Balance
                       
            transaction_name = 'Airtime Wallet Topup'
            description = 'Airtime wallet topup with Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":66,
                                "account_number":mpesa_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id
                                }
                            
            #Credit Mpesa account with amount sent to airtime agent
            credit_trans = Transaction.credit_on_debit_account(self, transaction_data)
            #End of transaction - Decrease bank account

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                
                #update account status
                cur.execute("""UPDATE airtime_wallet_topup set status=1, date_approved = %s, approved_by =%s WHERE id = %s""", ([date_approved, approved_by, id]))
                mysql.get_db().commit()

                message = {'status':200,
                           "airtime_stock_account_transaction_status":debit_trans,
                           "mpesa_account_transaction_status":credit_trans,
                           'description':'Airtime wallet topup was approved successfully'}
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
                           "error":"sp_a37",
                           "status":201,
                           "description":"Airtime wallet topup approval was not successful!",
                           "airtime_stock_account_transaction_status":debit_trans,
                           "mpesa_account_transaction_status":credit_trans}
                
                ErrorLogger().logError(message)
                return message
            
            
        #Error handling
        except Exception as error:         
            message = {'status':501,
                       'error':'sp_a18',
                       'description':'Failed to approve airtime wallet topup record. Error description ' + format(error)}            
            ErrorLogger().logError(message)
            return message
        finally:
                cur.close()
                        
    #API to deduct wallet balance and increase airtime earned income account balances after okoa airtime loan is created
    def airtime_wallet_withdraw(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a16',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]
        customer_id = details["customer_id"]
        amount = float(details["amount"])
        settlement_date = details["settlement_date"]
        wallet_account_number = details["wallet_account_number"]
        
        airtimeincome_acc = Accounts().airtime_income_earned_account()
        if int(airtimeincome_acc["status"]) == 200:
            airtime_income_earned_account_number = airtimeincome_acc["data"]
        else:
            message = {'status':402,
                        'description':"Couldn't fetch default airtime stock account!"}
            ErrorLogger().logError(message)                                
            return message
        
        
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a17',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
       
        try: 
            
            #Start of transaction - Decrease airtime stock Account Balance
            global_id = UniqueNumber().globalIdentifier()
            
            transaction_name = 'Airtime Topup'
            description = 'Airtime topup with Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            layer4_id = UniqueNumber.transactionsdebitcreditId(self)
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":customer_id,
                                "type":78,
                                "account_number":wallet_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id

                                }
                            
            #Debit airtime stock account with amount sent to airtime dealer
            debit_trans = Transaction.debit_on_credit_account(self, transaction_data)
            #End of transaction - Increase stock account
            
            #Start of transaction - Decrease Mpesa Account Balance
                       
            transaction_name = 'Airtime Topup'
            description = 'Airtime topup with Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":customer_id,
                                "type":79,
                                "account_number":airtime_income_earned_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id
                                }
                            
            #Credit Mpesa account with amount sent to airtime agent
            credit_trans = Transaction.credit_on_credit_account(self, transaction_data)
            #End of transaction - Decrease bank account

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
            
                message = {'status':200,
                           "wallet_account_transaction_status":debit_trans,
                           "airtime_earned_income_account_transaction_status":credit_trans,
                           'description':'Airtime wallet withdraw was successful'}
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
                        rollback_debit_trans = Transaction().debit_on_credit_account_rollback(data)
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
                           "error":"sp_a37",
                           "status":201,
                           "description":"Airtime wallet withdraw was successful!",
                           "wallet_account_transaction_status":debit_trans,
                           "airtime_earned_income_account_transaction_status":credit_trans}
                
                ErrorLogger().logError(message)
                return message
            
            
        #Error handling
        except Exception as error:         
            message = {'status':501,
                       'error':'sp_a18',
                       'description':'Failed to process transaction record. Error description ' + format(error)}            
            ErrorLogger().logError(message)
            return message
        finally:
                cur.close()
                
    #API to record Airtime Stock Reduced and Airtime cost of goods sold
    def airtime_stock_deducted(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a16',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]
        airtime_amount = float(details["amount"])
        settlement_date = details["settlement_date"]
        airtime_margin = 0.94 #Actual airtime deducted by dealer from airtime wallet changed from 0.94 to 0.95 back to 0.94
        amount = airtime_amount * airtime_margin
        
        airtime_cog_acc = Accounts().airtime_cog_account()
        if int(airtime_cog_acc["status"]) == 200:
            airtime_cog_account_number = airtime_cog_acc["data"]
        else:
            message = {'status':402,
                        'description':"Couldn't fetch default airtime cog account!"}
            ErrorLogger().logError(message)                                
            return message
        
        airtime_stk_acc = Accounts().airtime_stock_account()
        if int(airtime_stk_acc["status"]) == 200:
            airtime_stock_account_number = airtime_stk_acc["data"]
        else:
            message = {'status':402,
                        'description':"Couldn't fetch default airtime cog account!"}
            ErrorLogger().logError(message)                                
            return message

        
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a17',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
       
        try: 
            
            #Start of transaction - Increase airtime cost of goods sold Account Balance
            global_id = UniqueNumber().globalIdentifier()
            
            transaction_name = 'Airtime sold'
            description = 'Airtime CoG of Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            layer4_id = UniqueNumber.transactionsdebitcreditId(self)
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":80,
                                "account_number":airtime_cog_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id

                                }
                            
            #Debit airtime COG account with amount of airtime paid by customer
            debit_trans = Transaction.debit_on_debit_account(self, transaction_data)
            #End of transaction - Increase COG account
            
            #Start of transaction - Increase Income Account Balance
                       
            transaction_name = 'Airtime sold'
            description = 'Airtime sales of Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":81,
                                "account_number":airtime_stock_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id
                                }
                            
            #Credit airtime sales account with amount paid by customer
            credit_trans = Transaction.credit_on_debit_account(self, transaction_data)
            #End of transaction - Increase airtime sales account

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
            
                message = {'status':200,
                           "airtime_cog_account_transaction_status":debit_trans,
                           "airtime_stock_account_transaction_status":credit_trans,
                           'description':'Airtime sale was recorded successfully!'}
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
                           "error":"sp_a37",
                           "status":201,
                           "description":"Airtime sale was not recorded!",
                           "airtime_cog_account_transaction_status":debit_trans,
                           "airtime_stock_account_transaction_status":credit_trans}
                
                ErrorLogger().logError(message)
                return message
            
            
        #Error handling
        except Exception as error:         
            message = {'status':501,
                       'error':'sp_a18',
                       'description':'Failed to process transaction record. Error description ' + format(error)}            
            ErrorLogger().logError(message)
            return message
        finally:
                cur.close()
                
    #API to record Airtime paid for using cash
    def airtime_paid_in_cash(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a16',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]
        amount = float(details["amount"])
        settlement_date = details["settlement_date"]
     
        
        mpesa_till_acc = Accounts().c2b_till_account()
        if int(mpesa_till_acc["status"]) == 200:
            mpesa_till_account_number = mpesa_till_acc["data"]
        else:
            message = {'status':402,
                        'description':"Couldn't fetch default airtime cog account!"}
            ErrorLogger().logError(message)                                
            return message
        
        airtime_income_realized_acc = Accounts().airtime_income_realized_account()
        if int(airtime_income_realized_acc["status"]) == 200:
            airtime_income_realized_account_number = airtime_income_realized_acc["data"]
        else:
            message = {'status':402,
                        'description':"Couldn't fetch default airtime cog account!"}
            ErrorLogger().logError(message)                                
            return message

        
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a17',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
       
        try: 
            
            #Start of transaction - Increase airtime cost of goods sold Account Balance
            global_id = UniqueNumber().globalIdentifier()
            
            transaction_name = 'Airtime sold'
            description = 'Airtime sales of Kes' + str(amount)
            settlement_date = settlement_date
            layer4_id = UniqueNumber.transactionsdebitcreditId(self)
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":84,
                                "account_number":mpesa_till_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id

                                }
                            
            #Debit airtime COG account with amount of airtime paid by customer
            debit_trans = Transaction.debit_on_debit_account(self, transaction_data)
            #End of transaction - Increase COG account
            
            #Start of transaction - Increase Income Account Balance
                       
            transaction_name = 'Airtime sold'
            description = 'Airtime sales of Kes' + str(amount)
            settlement_date = settlement_date
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":85,
                                "account_number":airtime_income_realized_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id
                                }
                            
            #Credit airtime sales account with amount paid by customer
            credit_trans = Transaction.credit_on_credit_account(self, transaction_data)
            #End of transaction - Increase airtime sales account

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
            
                message = {'status':200,
                           "mpesa_till_account_transaction_status":debit_trans,
                           "airtime_income_realized_account_transaction_status":credit_trans,
                           'description':'Airtime sale was recorded successfully!'}
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
                           "error":"sp_a37",
                           "status":201,
                           "description":"Airtime sale was not recorded!",
                           "mpesa_till_account_transaction_status":debit_trans,
                           "airtime_income_realized_account_transaction_status":credit_trans}
                
                ErrorLogger().logError(message)
                return message
            
            
        #Error handling
        except Exception as error:         
            message = {'status':501,
                       'error':'sp_a18',
                       'description':'Failed to process transaction record. Error description ' + format(error)}            
            ErrorLogger().logError(message)
            return message
        finally:
                cur.close()