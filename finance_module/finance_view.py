from flask import request, Response, json, jsonify
from main import mysql, app
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.transactions.bookkeeping import DebitCredit
import uuid

class Finance():
  
    def create_capital_injection(self, user):
        #Get the request data
        request_data = request.get_json()      
        if request_data == None:
            message = {'status':402,
                       'error':'ci_a01',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)            
            return jsonify(message)
  
        bankAccount = request_data["bank_account_number"]
        shareholderAccount = request_data["shareholder_account_number"]
        amount = float(request_data["amount"])
        transactionID = request_data["transaction_id"]
        reference = request_data["reference"]
        valueDate = request_data["value_date"]
        narrative = request_data["narrative"]
        created_by = user['id']

        trans_uuid_ = str(uuid.uuid4())
        trans_uuid = trans_uuid_.replace("-", "" )
        trans_uuid = str(trans_uuid)
        globalId = 'zz' + str(trans_uuid[-12:])
        
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
            status = 2
            created_date = Localtime().gettime()

            #store user request
            cur.execute("""INSERT INTO accounting_capital_injection_entries (global_id, bank_account, shareholder_account, settlement_date, amount, transaction_reference, transaction_id, narrative, created_date, created_by, status)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (globalId, bankAccount, shareholderAccount, valueDate, amount, reference, transactionID, narrative, created_date, created_by, status))
            mysql.get_db().commit()
            
            message = {"description":"Transaction was posted successfully",
                       "status":200}
            return message

        except Exception as error:
            message = {'status':501, 
                       'error':'ci_a03',
                       'description':'Failed to create capital injection record. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  

    def list_capital_injection_entries(self, user):
        request_data = request.get_json()
        if request_data == None:
            message = {'status':402,
                       'error':'ci_a04',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)            
            return jsonify(message)
        
            
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                    'error':'ci_b05',
                    'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)
            
        try:
            status = request_data['status']
            cur.execute("""SELECT * from accounting_capital_injection_entries WHERE status= %s ORDER BY created_date DESC""", [status])
            results = cur.fetchall()   
            if results:
                no = 0
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
                    cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s """, [created_by_id])
                    createdby_details = cur.fetchone()            
                    created_by = createdby_details['first_name'] + " " + createdby_details['last_name']
                    no = no + 1
                    res = {
                        "id": result['id'],
                        "no":no,
                        "globalId": result['global_id'],
                        "bank_account": bankAccount,
                        "transaction_id": result['transaction_id'],
                        "shareholder_account": shareholderAccount,
                        "settlement_date": result['settlement_date'],
                        "amount": float(result['amount']),                    
                        "reference": result['transaction_reference'],
                        "narrative": result['narrative'],                                               
                        "datecreated": result['created_date'], 
                        "createdby": created_by,                    
                        "created_by_id": created_by_id                  
                    }
                    trans.append(res)
                
                #The response object
                message = {'status':200,
                            'description':'Capital injection records were fetched successfully!',
                            'response':trans}
                return message
            else:
                message = {'status':201,
                            'error':'ci_a05',
                            'description':'Failed to fetch Capital Injection records were!'
                        }   
                ErrorLogger().logError(message)
                return jsonify(message) 
    
        except Exception as error:
            message = {'status':501,
                    'error':'ci_b09',
                    'description':'Failed to fetch capital injection records.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close() 
        
    def get_capital_injection_details(self, user):            
        request_data = request.get_json()

        if request_data == None:
            message = {'status':402,
                       'description':'Request data is missing some details!'}
            return jsonify(message)

        id = request_data["id"]

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)
        
        try:
            cur.execute("""SELECT * from accounting_capital_injection_entries WHERE id = %s""", [id])
            result = cur.fetchone()   
            if result:                
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
                cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s """, [created_by_id])
                createdby_details = cur.fetchone()            
                created_by = createdby_details['first_name'] + " " + createdby_details['last_name']

                res = {
                    "id": result['id'],
                    "globalId": result['global_id'],
                    "bank_account": bankAccount,
                    "shareholder_account": shareholderAccount,
                    "settlement_date": result['settlement_date'],
                    "transaction_id": result['transaction_id'],                    
                    "amount": float(result['amount']),                    
                    "reference": result['transaction_reference'],
                    "narrative": result['narrative'],
                    "createdby": created_by,                    
                    "datecreated": result['created_date']                    
                }
                   
            
                message = {'status':200,
                           'description':'Records were found!',
                           'response':res}
                return jsonify(message)
            else:
                message = {'status':404,
                           'description':'No record was found!'
                           }
                return jsonify(message)                
    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'description':'Failed to retrieve record from database.'+ format(error)}
            return jsonify(message)  
        finally:
            cur.close() 

    def approve_capital_injection(self, user):
        data = request.get_json()        
        if data == None:
            message = {'status':402,
                       'error':'ci_a06',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)            
            return jsonify(message)

        id = data["id"]
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'ci_a07',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)
        try:  
            if id: 
                
                cur.execute("""SELECT global_id, bank_account, shareholder_account, amount, settlement_date, transaction_id FROM accounting_capital_injection_entries WHERE status =2 AND id = %s """, [id])
                entry = cur.fetchone()   
                if entry:
                        global_id = entry['global_id']         
                        bank_account_number = entry['bank_account'] 
                        shareholder_account_number = entry['shareholder_account'] 
                        amount = float(entry['amount']) 
                        settlement_date = entry['settlement_date'] 
                        transaction_id = entry['transaction_id'] 

                        details = {
                            "id":id,
                            "user_id":user["id"],
                            "global_id":global_id,
                            "bank_account_number":bank_account_number,
                            "shareholder_account_number":shareholder_account_number,
                            "amount":amount,                
                            "settlement_date":settlement_date,
                            "transaction_id":transaction_id

                        }
                        
                        api_message = DebitCredit().capital_injection_approve(details)  
                        if int(api_message["status"]) == 200:
                            message = {'status':200,
                                       'description':'Record was approved successfully!'}
                            return jsonify(message)  
                        else:              
                            return jsonify(api_message)
                       
                else:
                    message = {'status':201,
                               'description':'Capital injection record was not found!'}
                    return jsonify(message), 201 
            else:
                message = {'status':500,
                           'error':'ci_a09',
                           'description':'Failed to approve capital injection transaction!'}
                ErrorLogger().logError(message)
                return jsonify(message), 500
                      
    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'ci_a10',
                       'description':'Failed to approve capital injection record. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()
        


     
   