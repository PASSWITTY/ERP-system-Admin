from flask import Response, jsonify, json
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
            
    #API to record a debit on a credit account and a credit on a debit account transactions
    def cash_stock_purchase_approve(self, details):
        if details == None:
            message = {'status':402,
                       'error':'ci_b10',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)            
            return message

        id = details["id"]
        approved_by = details["user_id"]
        
        global_id = details["global_id"]
        total_amount = details["amount"]
        bank_account_number = details["bank_account_number"]
        payable_account_number = details["payable_account_number"]
        settlement_date = details["settlement_date"]
        transaction_id = details["transaction_id"]
        product_details = details["product_details"]
     
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'ci_b11',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message       
        try:
            
            models_processed = 0
            for product_detail in product_details:
                
                model_id = product_detail['model_id']
                quantity = float(product_detail["quantity"])
                price_per_unit = float(product_detail["price_per_unit"])
                amount = quantity * price_per_unit
                
                cur.execute("""SELECT number FROM accounts WHERE type_id=2 AND owner_id = %s""", [model_id])
                get_stock_account = cur.fetchone()
                if get_stock_account:
                    stock_account = get_stock_account["number"]
                else:
                    message = {
                    "status":201,
                    "message":"Product does not have stock account"
                    }
                    return message
                    
                
                #Start of transaction posting - Debit supplier payable account with stock purchase amount
                transaction_name = 'Cash stock purchase'
                description = 'Stock purchase of Ksh. ' + str(amount) + ' Transaction Id ' + str(transaction_id)
            
                
                trans_uuid_ = str(uuid.uuid4())
                trans_uuid = trans_uuid_.replace("-", "" )
                trans_uuid = str(trans_uuid)
                layer1_id = 't0' + str(trans_uuid[-12:])

                transaction_data = {"global_id":global_id, 
                                    "entry_id":id, 
                                    "sub_entry_id":'', 
                                    "type":3,
                                    "account_number":stock_account, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":settlement_date,
                                    "layer1_id":layer1_id
                                    }
                
                #Debit stock account with stock purchase amount
                debit_trans1 = Transaction().debit_on_debit_account(transaction_data)
                #End of transaction posting

            
                #Start of transaction posting - Credit payable account with stock purchase amount
            
                transaction_name = 'Cash stock purchase'
                description = 'Stock purchase of Ksh. ' + str(amount) + ' Transaction Id ' + str(transaction_id)

                transaction_data = {"global_id":global_id, 
                                    "entry_id":id, 
                                    "sub_entry_id":'',
                                    "type":4,
                                    "account_number":payable_account_number, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":settlement_date,
                                    "layer1_id":layer1_id
                                    }
                
                #Credit stock account with stock purchase amount
                credit_trans1 = Transaction().credit_on_credit_account(transaction_data)
                #End of transaction posting
            
                if ((int(debit_trans1["status"]) == 200) and (int(credit_trans1["status"]) == 200)):
                    pass  
            
                else:    
                    #Reverse the failed transaction
                    if int(debit_trans1["status"]) == 200 and int(credit_trans1["status"]) != 200:
                        #Rollback this debit transaction
                        data = debit_trans1["data"]
                        trans_id = debit_trans1["data"]["trans_id"]
                        amount = float(debit_trans1["data"]["amount"])
                        if amount >0 and trans_id is not None:
                            #Delete this specific debit transaction
                            rollback_debit_trans1 = Transaction().debit_on_debit_account_rollback(data)
                        else:
                            pass
                    
                    if int(credit_trans1["status"]) == 200 and int(debit_trans1["status"]) != 200:
                        #Rollback this credit transaction

                        data = credit_trans1["data"]
                        trans_id = credit_trans1["data"]["trans_id"]
                        amount = float(credit_trans1["data"]["amount"])
                        if amount >0 and trans_id is not None:
                            #Delete this specific credit transaction
                            rollback_credit_trans1 = Transaction().credit_on_credit_account_rollback(data)
                        else:
                            pass
                            

                # message = {
                #     "status":201,
                #     "payable_account_transaction_status":debit_trans,
                #     "bank_account_transaction_status":credit_trans}
                # return message 
                
                #Start of transaction posting - Debit supplier payable account with stock purchase amount
                transaction_name = 'Cash stock purchase'
                description = 'Stock purchase of Ksh. ' + str(amount) + ' Transaction Id ' + str(transaction_id)
            
                
                trans_uuid_ = str(uuid.uuid4())
                trans_uuid = trans_uuid_.replace("-", "" )
                trans_uuid = str(trans_uuid)
                layer1_id = 't0' + str(trans_uuid[-12:])

                transaction_data = {"global_id":global_id, 
                                    "entry_id":id, 
                                    "sub_entry_id":'', 
                                    "type":5,
                                    "account_number":payable_account_number, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":settlement_date,
                                    "layer1_id":layer1_id
                                    }
                
                #Debit supplier payable account with stock purchase amount
                debit_trans2 = Transaction().debit_on_credit_account(transaction_data)
                #End of transaction posting

            
                #Start of transaction posting - Credit bank account with stock purchase amount
            
                transaction_name = 'Cash stock purchase'
                description = 'Stock purchase of Ksh. ' + str(amount) + ' Transaction Id ' + str(transaction_id)

                transaction_data = {"global_id":global_id, 
                                    "entry_id":id, 
                                    "sub_entry_id":'',
                                    "type":6,
                                    "account_number":bank_account_number, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":settlement_date,
                                    "layer1_id":layer1_id
                                    }
            
                #Credit bank account with stock purchase amount
                credit_trans2 = Transaction().credit_on_debit_account(transaction_data)
                #End of transaction posting
                
                if ((int(debit_trans2["status"]) == 200) and (int(credit_trans2["status"]) == 200)):
                    pass 
            
                else:    
                    #Reverse the failed transaction
                    if int(debit_trans2["status"]) == 200 and int(credit_trans2["status"]) != 200:
                        #Rollback this debit transaction
                        data = debit_trans2["data"]
                        trans_id = debit_trans2["data"]["trans_id"]
                        amount = float(debit_trans2["data"]["amount"])
                        if amount >0 and trans_id is not None:
                            #Delete this specific debit transaction
                            rollback_debit_trans2 = Transaction().debit_on_credit_account_rollback(data)
                        else:
                            pass
                    
                    if int(credit_trans2["status"]) == 200 and int(debit_trans2["status"]) != 200:
                        #Rollback this credit transaction

                        data = credit_trans2["data"]
                        trans_id = credit_trans2["data"]["trans_id"]
                        amount = float(credit_trans2["data"]["amount"])
                        if amount >0 and trans_id is not None:
                            #Delete this specific credit transaction
                            rollback_credit_trans2 = Transaction().credit_on_debit_account_rollback(data)
                        else:
                            pass
                        
                models_processed = models_processed + 1
                    
            if models_processed > 0:
                dateapproved = Localtime().gettime()
                #update capital injection status
                cur.execute("""UPDATE cash_stock_purchases set status=1, approved_date = %s, approved_by = %s WHERE id = %s """, ([dateapproved, approved_by, id]))
                mysql.get_db().commit() 
                

                message = {"stock_account_transaction_status":debit_trans1,
                           "supplier_account_transaction_status":credit_trans1,
                           "supplier_account_transaction_status":debit_trans2,
                           "bank_account_transaction_status":credit_trans2,
                           "description":"Cash stock purchase transaction was approved successfully!",
                           "status":200}
                return message
            else:
                message = {"stock_account_transaction_status":debit_trans1,
                           "supplier_account_transaction_status":credit_trans1,
                           "supplier_account_transaction_status":debit_trans2,
                           "bank_account_transaction_status":credit_trans2,
                           "description":"Failed to approve cash stock purchase transaction!",
                           "status":201}
                return message
                
                
        except Exception as error:
            message = {'status':501,
                       'error':'ci_b11',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()


    #API to record a debit on a debit account and a credit on a credit account transactions
    def transit_stock_approve(self, details):
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
        payable_account_number = details["payable_account_number"]
        settlement_date = details["settlement_date"]
        transaction_id = details["transaction_id"]
        dateapproved = Localtime().gettime()
     
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'ci_b11',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message       
        try:
            #Check if there was transport cost incurred
            if amount > 0:
                #fetch default transpot cost of service account
                cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number= 6""")
                cog_ac = cur.fetchone()
                if cog_ac:
                    cog_transport_account = cog_ac["account_number"]
                else:
                    message = {
                           "description":"Default transport cost of service account has not been setup!", 
                           "status":201
                           }
                    return message
                
                
                #Start of transaction posting - Debit transport cost of service account with transport amount
                transaction_name = 'Transport cost'
                description = 'Transport cost of Ksh. ' + str(amount) + ' Transaction Id ' + str(transaction_id)
            
                
                trans_uuid_ = str(uuid.uuid4())
                trans_uuid = trans_uuid_.replace("-", "" )
                trans_uuid = str(trans_uuid)
                layer1_id = 't0' + str(trans_uuid[-12:])

                transaction_data = {"global_id":global_id, 
                                    "entry_id":id, 
                                    "sub_entry_id":'', 
                                    "type":7,
                                    "account_number":cog_transport_account, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":settlement_date,
                                    "layer1_id":layer1_id
                                    }
                
                #Debit cog transport account with transport cost
                debit_trans1 = Transaction().debit_on_debit_account(transaction_data)
                #End of transaction posting

                #Start of transaction posting - Credit transporter payable account with transport cost
                transaction_name = 'Transport cost incurred'
                description = 'Transport cost of Ksh. ' + str(amount) + ' Transaction Id ' + str(transaction_id)

                transaction_data = {"global_id":global_id, 
                                    "entry_id":id, 
                                    "sub_entry_id":'',
                                    "type":8,
                                    "account_number":payable_account_number, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":settlement_date,
                                    "layer1_id":layer1_id
                                    }
                
                #Credit transporter payable account with transport cost
                credit_trans1 = Transaction().credit_on_credit_account(transaction_data)
                #End of transaction posting
            
                if ((int(debit_trans1["status"]) == 200) and (int(credit_trans1["status"]) == 200)):
                    pass  
            
                else:    
                    #Reverse the failed transaction
                    if int(debit_trans1["status"]) == 200 and int(credit_trans1["status"]) != 200:
                        #Rollback this debit transaction
                        data = debit_trans1["data"]
                        trans_id = debit_trans1["data"]["trans_id"]
                        amount = float(debit_trans1["data"]["amount"])
                        if amount >0 and trans_id is not None:
                            #Delete this specific debit transaction
                            rollback_debit_trans1 = Transaction().debit_on_debit_account_rollback(data)
                        else:
                            pass
                    
                    if int(credit_trans1["status"]) == 200 and int(debit_trans1["status"]) != 200:
                        #Rollback this credit transaction

                        data = credit_trans1["data"]
                        trans_id = credit_trans1["data"]["trans_id"]
                        amount = float(credit_trans1["data"]["amount"])
                        if amount >0 and trans_id is not None:
                            #Delete this specific credit transaction
                            rollback_credit_trans1 = Transaction().credit_on_credit_account_rollback(data)
                        else:
                            pass
                            

                # message = {
                #     "status":201,
                #     "payable_account_transaction_status":debit_trans,
                #     "bank_account_transaction_status":credit_trans}
                # return message 
                
                #Start of transaction posting - Debit transporter payable account with transport cost
                transaction_name = 'Transport cost paid'
                description = 'Transport cost paid. Ksh. ' + str(amount) + ' Transaction Id ' + str(transaction_id)
            
                trans_uuid_ = str(uuid.uuid4())
                trans_uuid = trans_uuid_.replace("-", "" )
                trans_uuid = str(trans_uuid)
                layer1_id = 't0' + str(trans_uuid[-12:])

                transaction_data = {"global_id":global_id, 
                                    "entry_id":id, 
                                    "sub_entry_id":'', 
                                    "type":9,
                                    "account_number":payable_account_number, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":settlement_date,
                                    "layer1_id":layer1_id
                                    }
                
                #Debit transporter payable account with transport cost
                debit_trans2 = Transaction().debit_on_credit_account(transaction_data)
                #End of transaction posting

                #Start of transaction posting - Credit bank account with transport cost
            
                transaction_name = 'Transport cost paid'
                description = 'Transport cost paid. Ksh. ' + str(amount) + ' Transaction Id ' + str(transaction_id)

                transaction_data = {"global_id":global_id, 
                                    "entry_id":id, 
                                    "sub_entry_id":'',
                                    "type":10,
                                    "account_number":bank_account_number, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":settlement_date,
                                    "layer1_id":layer1_id
                                    }
            
                #Credit bank account with transport cost
                credit_trans2 = Transaction().credit_on_debit_account(transaction_data)
                #End of transaction posting
                
                if ((int(debit_trans2["status"]) == 200) and (int(credit_trans2["status"]) == 200)):
                    pass 
            
                else:    
                    #Reverse the failed transaction
                    if int(debit_trans2["status"]) == 200 and int(credit_trans2["status"]) != 200:
                        #Rollback this debit transaction
                        data = debit_trans2["data"]
                        trans_id = debit_trans2["data"]["trans_id"]
                        amount = float(debit_trans2["data"]["amount"])
                        if amount >0 and trans_id is not None:
                            #Delete this specific debit transaction
                            rollback_debit_trans2 = Transaction().debit_on_credit_account_rollback(data)
                        else:
                            pass
                    
                    if int(credit_trans2["status"]) == 200 and int(debit_trans2["status"]) != 200:
                        #Rollback this credit transaction

                        data = credit_trans2["data"]
                        trans_id = credit_trans2["data"]["trans_id"]
                        amount = float(credit_trans2["data"]["amount"])
                        if amount >0 and trans_id is not None:
                            #Delete this specific credit transaction
                            rollback_credit_trans2 = Transaction().credit_on_debit_account_rollback(data)
                        else:
                            pass
                        
               
                #update capital injection status
                cur.execute("""UPDATE products_in_transit set status=1, approved_date = %s, approved_by = %s WHERE id = %s """, ([dateapproved, approved_by, id]))
                mysql.get_db().commit() 
                rowcount = cur.rowcount
                if rowcount:
                    message = {"cogtransport_account_transaction_status":debit_trans1,
                               "transporter_account_transaction_status":credit_trans1,
                               "transporter_account_transaction_status":debit_trans2,
                               "bank_account_transaction_status":credit_trans2,
                               "description":"Transit stock transaction was approved successfully!",
                               "status":200}
                    return message
            else:
                
                #update capital injection status
                cur.execute("""UPDATE products_in_transit set status=1, approved_date = %s, approved_by = %s WHERE id = %s """, ([dateapproved, approved_by, id]))
                mysql.get_db().commit() 
                rowcount = cur.rowcount
                if rowcount:
                    message = {
                               "description":"Transit stock transaction was approved successfully!",
                               "status":200}
                    return message
                
                
        except Exception as error:
            message = {'status':501,
                       'error':'ci_b11',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()