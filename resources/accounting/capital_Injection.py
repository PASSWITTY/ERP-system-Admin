from flask import Response, json, jsonify
from main import mysql
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.alphanumeric.generate import UniqueNumber
from resources.transactions.transaction import Transaction


class Capital_Injection():
  
    #API to create un-approved capital injection 
    def capital_injection_draft(self, details):
        if details == None:
            message = {'status':402,
                       'error':'ci_b01',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)            
            return message
     
        bankAccount = details["bankAccount"]
        shareholderAccount = details["shareholderAccount"]
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
            cur.execute("""INSERT INTO accounting_capital_injection_entries (global_id, bank_account, shareholder_account, settlement_date, amount, transaction_reference, transaction_id, narrative, date_created, created_by, status)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (globalId, bankAccount, shareholderAccount, valueDate, amount, reference, transactionID, narrative, dateCreated, created_by, status))
            mysql.get_db().commit()
            
            message = {"description":"Transaction was posted successfully",
                       "status":200}
            return message

        except Exception as error:
            message = {'status':501,
                       'error':'ci_b03',
                       'description':'Failed to create capital injection record. ' + format(error)}
            ErrorLogger().logError(message)
            return message
        finally:
            cur.close()

    #API to retrieve capital injection transactions by status
    def capital_injection_entries(self, details):
        if details == None:
            message = {'status':500,
                       'error':'ci_b04',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message

        id = details["id"]
    
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'ci_b05',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
        try:

            cur.execute("""SELECT * from accounting_capital_injection_entries WHERE status= %s """, [id])
            results = cur.fetchall()   
            if results:
                
                trans = []
                for result in results:
                    bnk_acc_id = result['bank_account']    
                       
                    cur.execute("""SELECT name FROM accounts WHERE number =%s""", [bnk_acc_id])
                    bnk_acc_details = cur.fetchone()   
                                     
                    if bnk_acc_details:   
                        bankAccount = bnk_acc_details["name"] 
                        
                    else:
                        message = {'status':201,
                                   'error':'ci_b06', 
                                   'description':'Bank account number was not found!'}
                        ErrorLogger().logError(message)
                        return message


                    shares_acc_id = result["shareholder_account"],
                    cur.execute("""SELECT name FROM accounts WHERE number = %s """, [shares_acc_id])
                    shares_acc_details = cur.fetchone()       
                    if shares_acc_details:          
                        shareholderAccount = shares_acc_details['name'] 
                    else:
                        message = {'status':201,
                                   'error':'ci_b07', 
                                   'description':'Share holder account number was not found!'}
                        ErrorLogger().logError(message)
                        return message    
                    
                    created_by_id = result['created_by']
                    cur.execute("""SELECT first_name, last_name FROM administrator_details WHERE user_id = %s """, [created_by_id])
                    createdby_details = cur.fetchone()            
                    created_by = createdby_details['first_name'] + " " + createdby_details['last_name']

                    res = {
                        "transId": result['id'],
                        "globalId": result['global_id'],
                        "bank_account": bankAccount,
                        "shareholder_account": shareholderAccount,
                        "settlement_date": result['settlement_date'],
                        "amount": result['amount'],                    
                        "reference": result['transaction_reference'],
                        "narrative": result['narrative'],
                        "createdby": created_by,                    
                        "datecreated": result['date_created']                    
                    }
                    trans.append(res)
                
                #The response object
                message = {'status':200,
                           'description':'Capital injection entries were found!',
                           'response':trans}
                return message
            else:                
                message = {'status':404,
                           'error':'ci_b08', 
                           'description':'Capital injection entries were not found!',
                           'response':[]}
                return message
            
        except Exception as error:
            message = {'status':501,
                       'error':'ci_b09',
                       'description':'Failed to retrieve capital injection records from database.' + format(error)}
            ErrorLogger().logError(message)
            return message  
        finally:
            cur.close()

    #API to approve capital injection transaction
    def capital_injection_approve(self, details):
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
        bank_account_number = details["bank_account_number"]
        shareholder_account_number = details["shareholder_account_number"]
        settlement_date = details["settlement_date"]

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
            description = 'Capital injection of Ksh. ' + str(amount)
            layer4_id = UniqueNumber.transactionsdebitcreditId(self)

            transaction_data = {"global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'', 
                                "type":1,
                                "account_number":bank_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id
                                }
            
            #Debit Bank Accont with deposit amount
            debit_trans = Transaction().debit_on_debit_account(transaction_data)
            #End of transaction posting

            
            #Start of transaction posting - Credit Shareholder Account with amount
        
            transaction_name = 'Capital injection'
            description = 'Capital injection of Ksh. ' + str(amount)

            transaction_data = {"global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":2,
                                "account_number":shareholder_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id
                                }
            
            #Credit Shareholder Account with deposit amount
            credit_trans = Transaction().credit_on_credit_account(transaction_data)
            #End of transaction posting
            
            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                
                #update capital injection status
                cur.execute("""UPDATE accounting_capital_injection_entries set status=1, date_approved = %s, approved_by = %s WHERE id = %s """, ([dateapproved, approved_by, id]))
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