from flask import Response, json, jsonify
from main import mysql
from datetime import datetime
from resources.transactions.transaction import Transaction
from resources.payload.payload import Localtime
from resources.alphanumeric.generate import UniqueNumber
from resources.logs.logger import ErrorLogger


from decimal import Decimal

class Supplier():
  
    #API to create un-approved capital injection 
    def supplier_draft(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a10',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message
     
        supplierId = details["supplierId"]
        supplierName = details["supplierName"]
        directorDetails = details["directorDetails"]
        mobileNumber = details["mobileNumber"]
        email = details["email"]
        country = details["country"]
        city = details["city"]
        user_id = details["user_id"]

        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a11',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message

        try:
            status = 0
            datecreated = Localtime().gettime()

            #store supplier details request
            cur.execute("""INSERT INTO suppliers (id, name, director_details, mobile_number, email, country, city, date_created, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (supplierId, supplierName, directorDetails, mobileNumber, email, country, city, datecreated, user_id, status))
            mysql.get_db().commit()
            cur.close()
            
            message = {"description":"Supplier was created successfully",
                       "status":200}
            return message

        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a12',
                       'description':'Failed to retrieve record from database.' + format(error)}
            ErrorLogger().logError(message)
            return message
        finally:
            cur.close()


    #API to retrieve supplier details by id
    def supplier_details(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a13',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]
    
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a14',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
        try:

            cur.execute("""SELECT * FROM suppliers WHERE id = %s""", [id])
            supplier = cur.fetchone()
            if supplier:  
                created_by_id = supplier['created_by']
                
                cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id= %s""", (created_by_id))
                userdetails = cur.fetchone()
                if userdetails:
                    created_by = userdetails['first_name'] + " " + userdetails['last_name']
                else:
                    created_by = ''

                trans = {
                    "id": supplier['id'],
                    "name": supplier['name'],                       
                    "directors": json.loads(supplier['director_details']),
                    "mobileNumber": supplier['mobile_number'],
                    "email": supplier['email'],
                    "country": supplier['country'],
                    "city": supplier['city'],
                    "datecreated": supplier['date_created'],
                    "createdby": created_by,                  
                    "created_by_id": created_by_id               
                }
                
                #The response object
                         
                return trans
            else:
                message = 'No record was found!'
                return message

        except Exception as error:         
            message = {'status':501,
                       'error':'sp_a15',
                       'description':'Failed to approve supplier record. Error description ' + format(error)}            
            ErrorLogger().logError(message)
            return message
        finally:
                cur.close()

     #API to approve a supplier profile   
    def supplier_approve(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a16',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]
        approved_by = details["user_id"]
        dateapproved = Localtime().gettime()

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a17',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
       
        try: 
            #update account status
            cur.execute("""UPDATE suppliers set status=1, date_approved = %s, approved_by = %s WHERE id = %s """, ([dateapproved, approved_by, id]))
            mysql.get_db().commit()            

            trans_message = {"description":"Supplier was approved successfully!",
                             "status":200}
            return trans_message     
            
        #Error handling
        except Exception as error:         
            message = {'status':501,
                       'error':'sp_a18',
                       'description':'Failed to approve supplier record. Error description ' + format(error)}            
            ErrorLogger().logError(message)
            return message
        finally:
                cur.close()
                
    #API to pay supplier invoice
    def pay_supplier_invoice_draft(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a10',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message
     
        
        paid_amount = float(details["paid_amount"])
        reference = details["reference"]
        narrative = details["narrative"]
        bank_account = details["bank_account_number"]
        entry_id = details["entry_id"]
        user_id = details["user_id"]
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a11',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message

        try:
            status = 0
            date_created = Localtime().gettime()
            global_id = UniqueNumber().globalIdentifier()
            
            cur.execute("""SELECT * FROM inventory_credit_purchases WHERE id = %s""", [entry_id])
            params = cur.fetchone()
            if params:  
                supplier_account = params['supplier_payable_account']
            
            #store supplier details request
            cur.execute("""INSERT INTO inventory_credit_paid (global_id, credit_purchase_id, amount_paid, bank_account, supplier_account, reference, narrative, date_created, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                             (global_id, entry_id,           paid_amount, bank_account, supplier_account, reference, narrative, date_created, user_id,    status))
            mysql.get_db().commit()
            cur.close()
            
            message = {"description":"Invoice payment transaction was created successfully",
                       "status":200}
            return message

        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a12',
                       'description':'Failed to insert record into database.' + format(error)}
            ErrorLogger().logError(message)
            return message
        finally:
            cur.close()
            
    #API to approve invoice payment 
    def approve_invoice_payment(self, payment_details):
        if payment_details == None:
            message = {'status':402,
                       'error':'sp_a35',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)            
            return message

        id = payment_details["id"]
        global_id = payment_details["global_id"]
        bank_account_number = payment_details["bank_account_number"]
        payable_account_number = payment_details["payable_account_number"]
        amount = payment_details["amount"]
        approved_by = payment_details["user_id"]

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a36',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
       
        try:
            #Start of transaction - Decrease Supplier Payable Account Balance
            
            transaction_name = 'Invoice Payment'
            description = 'Supplier Invoice payment of Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            layer4_id = UniqueNumber.transactionsdebitcreditId(self)
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":63,
                                "account_number":payable_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id

                                }
                            
            #Debit Supplier payable account with payment made
            debit_trans = Transaction.debit_on_credit_account(self, transaction_data)
            #End of transaction - Decrease payable account
            
            #Start of transaction - Decrease Bank Account Balance
                       
            transaction_name = 'Invoice Payment'
            description = 'Supplier Invoice payment of Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":64,
                                "account_number":bank_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id
                                }
                            
            #Credit Bank account with amount paid for inventory paid
            credit_trans = Transaction.credit_on_debit_account(self, transaction_data)
            #End of transaction - Decrease bank account

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                dateapproved = Localtime().gettime()
                #update invoice payment status
                cur.execute("""UPDATE inventory_credit_paid set status=1, date_approved = %s, approved_by = %s WHERE id = %s """, ([dateapproved, approved_by, id]))
                mysql.get_db().commit() 
                
                message = {"supplier_payable_transaction_status":debit_trans,
                           "bank_account_transaction_status":credit_trans,
                           "description":"Invoice payment was successful!",
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
                           "error":"sp_a37",
                           "status":201,
                           "description":"Invoice payment was not successful!",
                           "supplier_payable_transaction_status":debit_trans,
                           "bank_account_transaction_status":credit_trans}
                
                ErrorLogger().logError(message)
                return message     
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a38',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()