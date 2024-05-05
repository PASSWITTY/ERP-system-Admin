from json import detect_encoding
from flask import jsonify, json
import os, requests
from main import mysql, app
from resources.transactions.transaction import Transaction
from resources.alphanumeric.generate import UniqueNumber
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
import math

class Inventory():
  
    #API to create un-approved inventory item 
    def create_inventory_item_draft(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a10',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message
     
        itemId = details["itemId"]
        itemName = details["itemName"]
        location = details["location"]
        unitofmeasure = details["unitofmeasure"]
        quantity = float(details["quantity"])
        user_id = details["user_id"]

        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return message

        try:
            status = 0
            datecreated = Localtime().gettime() 

            #store inventory details
            cur.execute("""INSERT INTO inventory_items (id, item_name, item_location, unit_of_measure, quantity, date_created, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (itemId, itemName, location, unitofmeasure, quantity, datecreated, user_id, status))
            mysql.get_db().commit()
            
            message = {"description":"Inventory item was created successfully",
                       "status":200}
            return message

        except Exception as error:
            message = {'status':501,
                       'description':'Failed to create inventory item purchase record. ' + format(error)}
            return message
        finally:
            cur.close()

   #API to retrieve inventory items by status
    def inventory_items_list(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a10',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]
        
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a11',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
        try:            
            cur.execute("""SELECT * from inventory_items WHERE status= %s """, [id])
            results = cur.fetchall()    
            if results:
                trans = []                
                no = 0
                for result in results:
                    created_by_id = result['created_by']
                    
                    cur.execute("""SELECT first_name, last_name FROM administrator_details WHERE user_id = %s """, [created_by_id])
                    createdby_details = cur.fetchone()      
                    if createdby_details:      
                        created_by = createdby_details['first_name'] + " " + createdby_details['last_name']
                    else:
                        created_by = ''
                    no = no + 1
                    res = {
                        "no": no,
                        "id": result['id'],
                        "name": result['item_name'],
                        "location": result['item_location'],
                        "unit_of_measure": result['unit_of_measure'],
                        "quantity": float(result['quantity']),
                        "datecreated": result['date_created'],
                        "createdby": created_by,              
                        "created_by_id": created_by_id              
                    }
                    trans.append(res)
                          
                message = {'status':200, 
                           'response':trans,
                           'description':'Inventory details record was fetched successfully'}
                ErrorLogger().logError(message)
                return message
            else:
                message = {'status':404, 
                           'error':'sp_a13',
                           'description':'Inventory details record was not found'}
                ErrorLogger().logError(message)
                return message

        except Exception as error:
            message = {'status':501,
                       'error':'sp_a14',
                       'description':'Failed to get inventory record. ' + format(error)}
            ErrorLogger().logError(message)
            return message
        finally:
            cur.close()

    #API to retrieve inventory item details by id
    def inventory_items_details(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a15',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]
        
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a16',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
        try:            
            cur.execute("""SELECT * from inventory_items WHERE id= %s """, [id])
            result = cur.fetchone()    
            if result:            

                created_by_id = result['created_by']
                
                cur.execute("""SELECT first_name, last_name FROM administrator_details WHERE user_id = %s """, [created_by_id])
                createdby_details = cur.fetchone()      
                if createdby_details:      
                    created_by = createdby_details['first_name'] + " " + createdby_details['last_name']
                else:
                    created_by = ''

                res = {
                    "id": result['id'],
                    "name": result['item_name'],
                    "location": result['item_location'],
                    "unit_of_measure": result['unit_of_measure'],
                    "quantity": float(result['quantity']),
                    "datecreated": result['date_created'],
                    "createdby": created_by,              
                    "created_by_id": created_by_id              
                }
                          
                message = {'status':200, 
                           'response':res,
                           'description':'Inventory details record was fetched successfully'}
                ErrorLogger().logError(message)
                return message
            else:
                message = {'status':404, 
                           'error':'sp_a18',
                           'description':'Inventory details record was not found'}
                ErrorLogger().logError(message)
                return message

        except Exception as error:
            message = {'status':501,
                       'error':'sp_a19',
                       'description':'Failed to get inventory record. ' + format(error)}
            ErrorLogger().logError(message)
            return message
        finally:
            cur.close()

     #API to approve an inventory item
    def inventory_item_approve(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a20',
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
                       'error':'sp_a21',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
       
        try:  
            #update inventory item status
            cur.execute("""UPDATE inventory_items set status=1, date_approved = %s, approved_by = %s WHERE id = %s """, ([dateapproved, approved_by, id]))
            mysql.get_db().commit() 
            
            message = {"description":"Inventory item was approved successfully!",
                       "status":200}
            ErrorLogger().logError(message)
            return message       
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a23',
                       'description':'Failed to approve inventory record. ' + format(error)}
            ErrorLogger().logError(message)
            return message
        finally:
            cur.close()

    #API to create un-approved inventory purchase 
    def purchase_inventory(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a24',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)            
            return message
     
        supplier_id = details["supplier_id"]
        item_id = details["item_id"]
        bank_account_number = details["bank_account_number"]
        stock_account_number = details["stock_account_number"]
        payable_account_number = details["payable_account_number"]
        price_per_item = details["price_per_item"]
        price_per_item = round(price_per_item, 12)
        quantity = details["quantity"]
        quantity = round(quantity, 12)
        purchase_date = details["purchase_date"]
        total_price = details["total_price"]
        transaction_id = details["transaction_id"]
        narrative = details["narrative"]
        reference = details["reference"]
        total_price = round(total_price, 12)
        user_id = details["user_id"]

        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a25',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message

        try:
            status = 0
            date_created = Localtime().gettime() 
            global_id = UniqueNumber.globalIdentifier(self)            

            #store supplier details request
            cur.execute("""INSERT INTO inventory_items_purchased (item_id, quantity, price_per_item, total_price, supplier_id, transaction_id, narrative, reference, bank_account_number, stock_account_number, payable_account_number, global_id, purchase_date, date_created, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                                 (item_id, quantity, price_per_item, total_price, supplier_id, transaction_id, narrative, reference, bank_account_number, stock_account_number, payable_account_number, global_id, purchase_date, date_created, user_id,    status))
            mysql.get_db().commit()
            
            message = {"description":"Inventory was purchased successfully",
                       "status":200}
            ErrorLogger().logError(message)
            return message

        except Exception as error:
            message = {'status':501,
                       'error':'sp_a26',
                       'description':'Failed to purchase inventory. ' + format(error)}
            ErrorLogger().logError(message)
            return message
        finally:
            cur.close()

    #API to retrieve inventory items purchase list
    def inventory_items_purchase_list(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a27',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]    
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a28',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
        try:
            cur.execute("""SELECT * from inventory_items_purchased WHERE status = %s """, [id])
            results = cur.fetchall()    
            if results:
                trans = []
                
                for result in results:
                    created_by_id = result['created_by']
                    item_id = result['item_id']
                    supplier_id = result['supplier_id']
                    bank_account_number = result['bank_account_number']
                    stock_account_number = result['stock_account_number']
                    payable_account_number = result['payable_account_number']
                    
                    cur.execute("""SELECT first_name, last_name FROM administrator_details WHERE user_id = %s """, [created_by_id])
                    createdby_details = cur.fetchone()            
                    created_by = createdby_details['first_name'] + " " + createdby_details['last_name']
                    
                    cur.execute("""SELECT item_name FROM inventory_items WHERE id = %s """, [item_id])
                    item_details = cur.fetchone()            
                    item_name = item_details['item_name']
                    

                    cur.execute("""SELECT name FROM suppliers WHERE id = %s """, [supplier_id])
                    supp_details = cur.fetchone()            
                    supplier_name = supp_details['name']

                    cur.execute("""SELECT name FROM accounts WHERE number = %s """, [bank_account_number])
                    bnk_details = cur.fetchone()            
                    bank_account_name = bnk_details['name']
                    
                    cur.execute("""SELECT name FROM accounts WHERE number = %s """, [stock_account_number])
                    stc_details = cur.fetchone()            
                    stock_account_name = stc_details['name']
                    
                    cur.execute("""SELECT name FROM accounts WHERE number = %s """, [payable_account_number])
                    payable_details = cur.fetchone()            
                    payable_account_name = payable_details['name']
                    
                    res = {
                        "id": result['id'],
                        "item_name": item_name,
                        "item_id": item_id,
                        "quantity": float(result['quantity']),
                        "price_per_item": float(result['price_per_item']),
                        "total_price": float(result['total_price']),
                        "supplier_name": supplier_name,
                        "bank_account_name": bank_account_name, 
                        "stock_account_name": stock_account_name, 
                        "payable_account_name": payable_account_name, 
                        "datecreated": result['date_created'],
                        "global_id": result['global_id'],
                        "purchase_date": result['purchase_date'],
                        "date_created": result['date_created'],
                        "createdby": created_by                  
                    }
                    trans.append(res)
                
                message = {'status':200,
                           'response':trans,
                           'description':'Inventory purchased records were found!'}
                return message
            else:
                message = {"status description":"Inventory purchased records were not found!",
                           'error':'sp_a29',
                           "status":402}
                ErrorLogger().logError(message)
                return message  

        except Exception as error:
            message = {'status':501,
                       'error':'sp_a30',
                       'description':'Failed to get Inventory purchased record from database. ' + format(error)}
            ErrorLogger().logError(message)
            return message  
        finally:
            cur.close()

    #API to approve inventory purchase   
    def inventory_purchase_approve(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a31',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]
        approved_by = details["user_id"]

        global_id = details["global_id"]
        inventory_account = details["inventory_account"]
        payable_account = details["payable_account"]
        amount = details["amount"]

        dateapproved = Localtime().gettime()

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a32',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
       
        try:

            #Start of transaction - Increase stock account                
            transaction_name = 'Inventory Purchase'
            description = 'Inventory purchase of Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            layer4_id = UniqueNumber().transactionsdebitcreditId()
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":5,
                                "account_number":inventory_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id
                                }
                            
            #Debit inventory account with cost of inventory
            debit_trans = Transaction.debit_on_debit_account(self, transaction_data)
            #End of transaction - Increase stock account

            #Start of transaction - Increase Supplier Payable Account
            transaction_name = 'Purchase Purchase'
            description = 'Inventory purchase of Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":6,
                                "account_number":payable_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id
                                }
            #MOVE to another class
            #Credit Supplier payable account with cost of inventory
            credit_trans = Transaction.credit_on_credit_account(self, transaction_data)
            #End of transaction - Increase payable account

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                #update invenotory purchase status
                cur.execute("""UPDATE inventory_items_purchased set status=1, date_approved = %s, approved_by = %s WHERE id = %s """, ([dateapproved, approved_by, id]))
                mysql.get_db().commit() 
                

                trans_message = {"stock_account_transaction_status":debit_trans,
                                 "supplier_account_transaction_status":credit_trans,
                                 "description":"Inventory purchase was approved successfully!",
                                 "status":200}
                return trans_message        
            
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
                    'error':'sp_a33',
                    "stock_account_transaction_status":debit_trans,
                    "supplier_account_transaction_status":credit_trans}
                ErrorLogger().logError(message)
                return message
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a34',
                       'description':'Failed to approve inventory purchase record. ' + format(error)}
            ErrorLogger().logError(message)
            return message  
        finally:
            cur.close()

    #API to pay inventory purchased 
    def inventory_payment(self, payment_details):
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
            
            transaction_name = 'Payment for Inventory'
            description = 'Inventory payment of Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            layer4_id = UniqueNumber.transactionsdebitcreditId(self)
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":7,
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
                       
            transaction_name = 'Payment for Inventory'
            description = 'Inventory payment of Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":8,
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
                message = {"supplier_payable_transaction_status":debit_trans,
                           "bank_account_transaction_status":credit_trans,
                           "description":"Inventory payment was successful!",
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
                           "description":"Inventory payment was not successful!",
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

    #API to create un-approved inventory purchased on credit
    def credit_purchase_inventory(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a39',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message
     
        supplier_id = details["supplier_id"]
        supplier_payable_account = details["supplier_payable_account"]
        inventory_stock_account = details["inventory_stock_account"]

        inventory_id = details["item_id"]
        price_per_item = details["price_per_item"]
        price_per_item = round(price_per_item, 12)
        quantity = details["quantity"]
        quantity = round(quantity, 12)
        purchase_date = details["purchase_date"]
        
        invoice_id = details["invoice_id"]
        reference = details["reference"]
        narrative = details["narrative"]
        
        
        total_price = details["total_price"]
        amount = round(total_price, 12)
        created_by = details["user_id"]

        # Open A connection to the database
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a40',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message

        try:
            status = 0
            amount_paid = 0
            date_created = Localtime().gettime()
            global_id = UniqueNumber.globalIdentifier(self) 

            #store purchase details request
            cur.execute("""INSERT INTO inventory_credit_purchases (global_id, supplier_payable_account, supplier_id, inventory_stock_account, inventory_id, price_per_item, quantity, amount, amount_paid, amount_due, invoice_id, reference, narrative, purchase_date, date_created, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                                  (global_id, supplier_payable_account, supplier_id, inventory_stock_account, inventory_id, price_per_item, quantity, amount, amount_paid,     amount, invoice_id, reference, narrative, purchase_date, date_created, created_by, status))
            mysql.get_db().commit()
            
            message = {"description":"Inventory was purchased successfully",
                       "status":200}
            return message

        except Exception as error:
            message = {'status':501,
                       'error':'sp_a41',
                       'description':'Failed to insert record to database' + format(error)}
            ErrorLogger().logError(message)
            return message
        finally:
            cur.close()
            
    #API to retrieve inventory items purchased on credit
    def inventory_items_credit_purchase_list(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a42',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]    
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a43',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
        try:            

            cur.execute("""SELECT * from inventory_credit_purchases WHERE status = %s """, [id])
            results = cur.fetchall()    
            if results:
                no = 0
                trans = []
             
                for result in results:
                    created_by_id = result['created_by']
                    item_id = result['inventory_id']
                    supplier_id = result['supplier_id']
                    supplier_account = result['supplier_payable_account']
                    inventory_stock_account = result['inventory_stock_account']
                    
                    cur.execute("""SELECT first_name, last_name FROM administrator_details WHERE user_id = %s """, [created_by_id])
                    createdby_details = cur.fetchone()            
                    created_by = createdby_details['first_name'] + " " + createdby_details['last_name']

                    cur.execute("""SELECT item_name FROM inventory_items WHERE id = %s """, [item_id])
                    item_details = cur.fetchone()            
                    item_name = item_details['item_name']

                    cur.execute("""SELECT name FROM suppliers WHERE id = %s """, [supplier_id])
                    supp_details = cur.fetchone()            
                    supplier_name = supp_details['name']

                    cur.execute("""SELECT name FROM accounts WHERE number = %s """, [inventory_stock_account])
                    stk_details = cur.fetchone()            
                    stock_account_name = stk_details['name']

                    cur.execute("""SELECT name FROM accounts WHERE number = %s """, [supplier_account])
                    sp_details = cur.fetchone()            
                    supplier_account_name = sp_details['name']
                    no = no + 1
                    res = {
                        "id": result['id'],
                        "no":no,
                        "item_name": item_name,
                        "stock_account_name": stock_account_name, 
                        "supplier_name": supplier_name,
                        "supplier_account_name": supplier_account_name,
                        "quantity": result['quantity'],
                        "price_per_item": result['price_per_item'],
                        "total_price": float(result['amount']),
                        "amount_due": float(result['amount_due']),
                        "amount_paid": float(result['amount_paid']),
                        "global_id": result['global_id'],
                        "purchase_date": result['purchase_date'],
                        "invoice_id": result['invoice_id'],
                        "reference": result['reference'],
                        "narrative": result['narrative'],
                        "date_created": result['date_created'],
                        "createdby": created_by                  
                    }
                    trans.append(res)

                message = {"status":200,
                           "response":trans,
                           "description":"Records were fetched successfully"
                          }          
                return message
            else:
                message = {"status":201,
                           'error':'sp_a44',
                           "description":"Transaction failed! Records were not fetched!"
                          }   
                ErrorLogger().logError(message)       
                return message 

        except Exception as error:
            message = {'status':501,
                       'error':'sp_a45',
                       'description':'Transaction failed! Records were not fetched!' + format(error)}
            ErrorLogger().logError(message) 
            return message
        finally:
            cur.close()
            
    
    #API to retrieve unpaid supplier invoices
    def unpaid_supplier_invoice_list(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a42',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]    
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a43',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
        try:            

            cur.execute("""SELECT * from inventory_credit_purchases WHERE amount_due > 0 AND status = %s """, [id])
            results = cur.fetchall()    
            if results:
                no = 0
                trans = []
             
                for result in results:
                    created_by_id = result['created_by']
                    item_id = result['inventory_id']
                    supplier_id = result['supplier_id']
                    supplier_account = result['supplier_payable_account']
                    inventory_stock_account = result['inventory_stock_account']
                    
                    cur.execute("""SELECT first_name, last_name FROM administrator_details WHERE user_id = %s """, [created_by_id])
                    createdby_details = cur.fetchone()            
                    created_by = createdby_details['first_name'] + " " + createdby_details['last_name']

                    cur.execute("""SELECT item_name FROM inventory_items WHERE id = %s """, [item_id])
                    item_details = cur.fetchone()            
                    item_name = item_details['item_name']

                    cur.execute("""SELECT name FROM suppliers WHERE id = %s """, [supplier_id])
                    supp_details = cur.fetchone()            
                    supplier_name = supp_details['name']

                    cur.execute("""SELECT name FROM accounts WHERE number = %s """, [inventory_stock_account])
                    stk_details = cur.fetchone()            
                    stock_account_name = stk_details['name']

                    cur.execute("""SELECT name FROM accounts WHERE number = %s """, [supplier_account])
                    sp_details = cur.fetchone()            
                    supplier_account_name = sp_details['name']
                    no = no + 1
                    price_per_item = float(result['price_per_item'])
                    price_per_item = round(price_per_item, 2)
                    
                    quantity = float(result['quantity'])
                    quantity = round(quantity, 2)
                    
                    amount = float(result['amount'])
                    amount = round(amount, 4)
                    
                    amount_due = float(result['amount_due'])
                    amount_due = round(amount_due, 4)
                    
                    amount_paid = float(result['amount_paid'])
                    amount_paid = round(amount_paid, 4)
                    
                    res = {
                        "id": result['id'],
                        "no":no,
                        "item_name": item_name,
                        "stock_account_name": stock_account_name, 
                        "supplier_name": supplier_name,
                        "supplier_account_name": supplier_account_name,
                        "quantity": quantity,
                        "price_per_item": price_per_item,
                        "total_price": amount,
                        "amount_due": amount_due,
                        "amount_paid": amount_paid,
                        "global_id": result['global_id'],
                        "purchase_date": result['purchase_date'],
                        "invoice_id": result['invoice_id'],
                        "reference": result['reference'],
                        "narrative": result['narrative'],
                        "date_created": result['date_created'],
                        "createdby": created_by                  
                    }
                    trans.append(res)

                message = {"status":200,
                           "response":trans,
                           "description":"Records were fetched successfully"
                          }          
                return message
            else:
                message = {"status":201,
                           'error':'sp_a44',
                           "description":"Transaction failed! Records were not fetched!"
                          }   
                ErrorLogger().logError(message)       
                return message 

        except Exception as error:
            message = {'status':501,
                       'error':'sp_a45',
                       'description':'Transaction failed! Records were not fetched!' + format(error)}
            ErrorLogger().logError(message) 
            return message
        finally:
            cur.close()
            
    #API to approve inventory credit purchase   
    def inventory_credit_purchase_approve(self, details):
        if details == None:
            message = {'status':402,
                       'error':'sp_a46',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]
        approved_by = details["user_id"]
        global_id = details["global_id"]
        inventory_account = details["inventory_account"]
        payable_account = details["payable_account"]
        amount = details["amount"]

        dateapproved = Localtime().gettime()

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a47',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
       
        try:

            #Start of transaction - Increase stock account                
            transaction_name = 'Inventory Credit Purchase'
            description = 'Inventory Credit Purchase of Ksh. ' + str(amount)
            settlement_date = Localtime().gettime()
            layer4_id = UniqueNumber.transactionsdebitcreditId(self)
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":27,
                                "account_number":inventory_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id
                                }
                            
            #Debit inventory account with cost of inventory
            debit_trans = Transaction.debit_on_debit_account(self, transaction_data)
            #End of transaction - Increase stock account

            #Start of transaction - Increase Supplier Payable Account
            transaction_name = 'Purchase of SMS'
            description = 'Inventory Credit Purchase of Ksh. ' + str(amount)
            settlement_date = Localtime().gettime()
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":28,
                                "account_number":payable_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id
                                }
            #MOVE to another class
            #Credit Supplier payable account with cost of inventory
            credit_trans = Transaction.credit_on_credit_account(self, transaction_data)
            #End of transaction - Increase payable account

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):

                #update inventory creit purchase status
                cur.execute("""UPDATE inventory_credit_purchases set status=1, date_approved = %s, approved_by = %s WHERE id = %s """, (dateapproved, approved_by, id))
                mysql.get_db().commit() 
                
                trans_message = {"description":"Inventory purchase was approved successfully!",
                                 "data":[{"stock_account_status":debit_trans, "supplier_account_status":credit_trans}],
                                 "status":200}
                return trans_message   
            
            else:                    
                #Reverse the failed transaction

                if int(debit_trans["status"]) == 200:
                    #Rollback this debit transaction
                    data = debit_trans["data"]
                    trans_id = debit_trans["data"]["trans_id"]
                    amount = float(debit_trans["data"]["amount"])
                    if amount >0 and trans_id is not None:
                        #Delete this specific debit transaction
                        rollback_debit_trans = Transaction().debit_on_debit_account_rollback(data)
                    else:
                        pass
                
                if int(credit_trans["status"]) == 200:
                    #Rollback this credit transaction
                    data = credit_trans["data"]
                    trans_id = credit_trans["data"]["trans_id"]
                    amount = float(credit_trans["data"]["amount"])
                    if amount >0 and trans_id is not None:
                        #Delete this specific credit transaction
                        rollback_credit_trans = Transaction().credit_on_credit_account_rollback(data)
                    else:
                        pass   
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a48',
                       'description':'Failed to insert record to database' + format(error)}
            ErrorLogger().logError(message)
            return message
        finally:
            cur.close()

    #API to consumer sms inventory 
    def sms_inventory_consumed(self, sms_details):

        if sms_details == None:
            message = {"status":402,
                       'error':'sp_a50',
                       "description":"All details are required!"}
            ErrorLogger().logError(message) 
            return message

        entry_id = sms_details["entry_id"]
        date_consumed = sms_details["date_consumed"]
        global_id = sms_details["global_id"]
        msisdn = sms_details["msisdn"]
        content = sms_details["content"]        
        inventory_id = sms_details["inventory_id"]
        cost_per_item = float(sms_details["cost_per_item"])
        message_type = sms_details["type"]
              
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a51',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message) 
            return message

        try:
            
            #Get sms cost of service account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =15 AND owner_id = %s """, [inventory_id])
            get_sms_cos_account = cur.fetchone() 
            if get_sms_cos_account:
                sms_cost_of_service_account = get_sms_cos_account["number"]
            else:
                message = {"status":402,
                           'error':'sp_a52',
                           "description":"Task was not successful. Sms cost of service account is missing!"}
                ErrorLogger().logError(message) 
                return message
            
            #Get sms stock account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =2 AND owner_id = %s """, [inventory_id])
            get_sms_stock_account = cur.fetchone() 
            
            if get_sms_stock_account:
                sms_stock_account = get_sms_stock_account["number"]   
            else:
               
                message = {"status":402,
                           'error':'sp_a53',
                           "description":"Task was not successful. Sms stock account is missing!"}
                ErrorLogger().logError(message) 
                return message
            
            cost_per_unit = cost_per_item
            sms_content_id = 1
            sms_length = len(content)
            maximum_length = 160

            number_of_sms = (sms_length / maximum_length)
            number_of_sms = math.ceil(number_of_sms)

            total_price = (number_of_sms * cost_per_unit)
            date_created = Localtime().gettime()
            
                  
            cur.execute("""INSERT INTO sms_consumed (global_id, cost_per_sms, number_of_sms, total_price, sms_content_id, sms_length, date_consumed, enrty_id, date_created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                                    (global_id, cost_per_unit, number_of_sms, total_price, sms_content_id, sms_length, date_consumed, entry_id, date_created))
            
            mysql.get_db().commit()

            #Start of transaction posting - Debit SMS cost of service Accont with sms cost amount
           
            transaction_name = 'Sms consumed'
            #if customer langauge is English, get english description 
            description = "Sms consumed on entry number " + str(entry_id)
            #if customer langauge is Kiswahili, get swahili description 
            layer4_id = UniqueNumber().transactionsdebitcreditId()
            transaction_data = {"global_id":global_id, 
                                "entry_id":entry_id, 
                                "sub_entry_id":'',
                                "type":9,
                                "account_number":sms_cost_of_service_account, 
                                "amount":total_price, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":date_created,
                                "layer4_id":layer4_id
                                }
        
            #Debit sms Cost of service Accont with sms cost
            debit_trans = Transaction().debit_on_debit_account(transaction_data)
            #End of transaction posting

            #Start of transaction posting - Credit sms stock account with sms cost

            transaction_name = 'Sms consumed'
            #if customer langauge is English, get english description 
            description = "Sms consumed on entry number " + str(entry_id)
            #if customer langauge is Kiswahili, get swahili description 

            transaction_data = {"global_id":global_id, 
                                "entry_id":entry_id, 
                                "sub_entry_id":'',
                                "type":10,
                                "account_number":sms_stock_account, 
                                "amount":total_price, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":date_created,
                                "layer4_id":layer4_id
                                }
            
            #Credit Customer Wallet with Principal amount
            credit_trans = Transaction().credit_on_debit_account(transaction_data)
            #End of transaction posting
            
            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):

                details = {
                    "msisdn":msisdn,
                    "content":content,
                    "type": message_type,
                    "global_id":global_id,
                }
                deliver_sms = Inventory().deliver_sms(details)

                message = {
                           "sms_cog_account_status":debit_trans,
                           "Sms_stock_account_status":credit_trans,
                           "description":"Sms consumption was recorded successfully",
                           "status":200
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
                        rollback_credit_trans = Transaction().credit_on_debit_account_rollback(data)
                    else:
                        pass
                
                message = {
                           "sms_cog_account_status":debit_trans,
                           "Sms_stock_account_status":credit_trans,
                           "status":201,
                           'error':'sp_a54',
                           }
                ErrorLogger().logError(message)
                return message

        except Exception as error:
            message = {'status':501,
                       'error':'sp_a55',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message
          
          
    def deliver_sms(self, details):
        try:

            msisdn = details['msisdn']
            content = details['content']
            sms_type = details['type']
            
        
            if 'global_id' in details.keys():
                global_id = details['global_id']
            else:                
                global_id = ''
                            
            # Open A connection to the database
            try:
                cur =  mysql.get_db().cursor()
            except:
                message = {'status':500,
                           'error':'sp_a56',
                           'description':"Couldn't connect to the Database!"}
                ErrorLogger().logError(message) 
                return message
            
            send_date = Localtime().gettime()            
            
            url = app.config['SMS_API_URL']            
            content = content[0:400]
            
            payload = {
                "SenderId": app.config['SMS_SENDER_ID'],
                "MessageParameters": [{"Number": msisdn, "Text": content}],
                "ApiKey": app.config['SMS_API_KEY'],
                "ClientId": app.config['SMS_CLIENT_ID'],
            }
            headers = {
                'Content-Type': "application/json",
                'AccessKey': app.config['SMS_ACCESS_KEY'],
            }
            res = requests.request("POST", url, data=json.dumps(payload), headers=headers)
            json_res = json.loads(res.text)
        
            if json_res['ErrorCode'] == 0:
                status = 1
                reference_id = UniqueNumber().smsReferenceId()
                if global_id == '':
                    global_id = reference_id
                    
                cur.execute('''INSERT INTO sms_log (id, global_id, type,     msisdn, message, created_at, status) VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                                         (reference_id, global_id, sms_type, msisdn, content, send_date,  status))
                mysql.get_db().commit()
                record = cur.rowcount
                if not record:
                    response = {
                        'description': "SMS sending successful but could not be saved!",
                        'status': 201,
                        'error':'sp_a58',
                    }
                else:
                    response = {
                        'description': "SMS sending successful and saved!",
                        'status': 200
                    }
                return response                
                
            else: 
                status = 0
                reference_id = UniqueNumber().smsReferenceId()
                if global_id == '':
                    global_id = reference_id
                    
                cur.execute("""INSERT INTO sms_log (id, global_id, type,     msisdn, message, created_at, status) VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                                         (reference_id, global_id, sms_type, msisdn, content, send_date,  status))
                mysql.get_db().commit()

                record = cur.rowcount
                response = {
                    'description': "SMS sending failed",
                    'status': 201,
                    'error':'sp_a56'
                }
                # log details 
                log_file = os.path.join(app.config["UPLOAD_FOLDER"] + "/logs/sms_log.json")
                with open(log_file, "a") as file:
                    file.write(f"\n{send_date}: #{reference_id} {response}")
                return response


        # Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a57',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 
        finally:
            cur.close()
