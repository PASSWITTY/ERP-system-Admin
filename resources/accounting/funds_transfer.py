from flask import Response, json, jsonify
from main import mysql
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.alphanumeric.generate import UniqueNumber
from resources.transactions.transaction import Transaction


class FundsTransfer():
  
    #API to create un-approved funds transfer 
    def funds_transfer_draft(self, details):
        if details == None:
            message = {'status':402,
                       'error':'ci_b01',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)            
            return message
     
        debit_account = details["debit_account"]
        credit_account = details["credit_account"]
        amount = float(details["amount"])
        amount = round(amount, 12)
        transactionID = details["transactionID"]
        reference = details["reference"]
        valueDate = details["valueDate"]
        narrative = details["narrative"]
        created_by = details["created_by"]
        globalId = details["globalId"]

        # Open A connection to the database
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'ci_b02',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message

        try:
            status = 0 #Zero is unapproved
            dateCreated = Localtime().gettime()

            #store user request
            cur.execute("""INSERT INTO accounting_funds_transfer_entries (global_id, debit_account, credit_account, settlement_date, amount, transaction_reference, transaction_id, narrative, date_created, created_by, status)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (globalId, debit_account, credit_account, valueDate, amount, reference, transactionID, narrative, dateCreated, created_by, status))
            mysql.get_db().commit()
            
            message = {"description":"Transaction was posted successfully",
                       "status":200}
            return message

        except Exception as error:
            message = {'status':501,
                       'error':'ci_b03',
                       'description':'Failed to create funds transfer record. ' + format(error)}
            ErrorLogger().logError(message)
            return message
        finally:
            cur.close()

    #API to approve funds transfer transaction
    def funds_transfer_approve(self, details):
        if details == None:
            message = {'status':402,
                       'error':'ci_b10',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)            
            return message

        id = details["id"]
        approved_by = details["user_id"]
        dateapproved = Localtime().gettime()        
        global_id = details["global_id"]
        amount = details["amount"]
        debit_account = details["debit_account_number"]
        credit_account = details["credit_account_number"]
        settlement_date = details["settlement_date"]
        

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'ci_b11',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message    
        
        cur.execute("""SELECT type FROM accounts WHERE number = %s """, [debit_account])
        get_debit_acc = cur.fetchone()       
        if get_debit_acc:          
            debit_account_type = int(get_debit_acc['type'])
            
        cur.execute("""SELECT type FROM accounts WHERE number = %s """, [credit_account])
        get_credit_acc = cur.fetchone()       
        if get_credit_acc:          
            credit_account_type = int(get_credit_acc['type'])
               
        try: 
            #Debit transaction
            
            #Start of transaction posting - Debit Account with amount
            transaction_name = 'Funds Transfer'
            description = 'Funds Transfer of Ksh. ' + str(amount)
            layer4_id = UniqueNumber.transactionsdebitcreditId(self)

            #account is debit
            if debit_account_type <= 7 or debit_account_type in [15, 16, 18, 19]:
                transaction_data = {"global_id":global_id, 
                                    "entry_id":id, 
                                    "sub_entry_id":'', 
                                    "type":69,
                                    "account_number":debit_account, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":settlement_date,
                                    "layer4_id":layer4_id
                                    }
                #Debit debit Account with deposit amount
                debit_trans = Transaction().debit_on_debit_account(transaction_data)
                #End of transaction posting
            else:
                #account is credit
                transaction_data = {"global_id":global_id, 
                                    "entry_id":id, 
                                    "sub_entry_id":'', 
                                    "type":70,
                                    "account_number":debit_account, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":settlement_date,
                                    "layer4_id":layer4_id
                                    }
                #Debit debit Account with deposit amount
                debit_trans = Transaction().debit_on_credit_account(transaction_data)
                #End of transaction posting
                
            #Credit transaction
                
            #Start of transaction posting - Credit Account with amount        
            transaction_name = 'Funds Transfer'
            description = 'Funds Transfer of Ksh. ' + str(amount)

            #account is debit
            if credit_account_type <= 7 or credit_account_type in [15, 16, 18]:
                transaction_data = {"global_id":global_id, 
                                    "entry_id":id, 
                                    "sub_entry_id":'',
                                    "type":71,
                                    "account_number":credit_account, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":settlement_date,
                                    "layer4_id":layer4_id
                                    }
                
                #Credit credit Account with deposit amount
                credit_trans = Transaction().credit_on_debit_account(transaction_data)
                #End of transaction posting
            
            else:
                #account is credit
                transaction_data = {"global_id":global_id, 
                                    "entry_id":id, 
                                    "sub_entry_id":'',
                                    "type":72,
                                    "account_number":credit_account, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":settlement_date,
                                    "layer4_id":layer4_id
                                    }
                
                #Credit credit Account with deposit amount
                credit_trans = Transaction().credit_on_credit_account(transaction_data)
                #End of transaction posting
                
            
            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                
                #update capital injection status
                cur.execute("""UPDATE accounting_funds_transfer_entries set status=1, date_approved = %s, approved_by = %s WHERE id = %s """, ([dateapproved, approved_by, id]))
                mysql.get_db().commit() 
                

                message = {"debit_account_transaction_status":debit_trans,
                           "credit_account_transaction_status":credit_trans,
                           "description":"Funds transfer transaction was approved successfully!",
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
                        if debit_account_type <= 7 or debit_account_type in [15, 16, 18]:
                            rollback_debit_trans = Transaction().debit_on_debit_account_rollback(data)
                        else:
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
                        if debit_account_type <= 7 or debit_account_type in [15, 16, 18]:
                            rollback_credit_trans = Transaction().credit_on_debit_account_rollback(data)
                        else:
                            rollback_credit_trans = Transaction().credit_on_credit_account_rollback(data)
                    else:
                        pass
                            

                message = {
                    "status":201,
                    "debit_account_transaction_status":debit_trans,
                    "credit_account_transaction_status":credit_trans}
                return message
            
        except Exception as error:
            message = {'status':501,
                       'error':'ci_b11',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()