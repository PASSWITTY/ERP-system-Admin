from flask import request, Response, json, jsonify
from main import mysql, app
from accounts_module.accounts_model import Account
from resources.alphanumeric.generate import UniqueNumber
from resources.logs.logger import ErrorLogger
from resources.suppliers.suppliers import Supplier
from resources.inventory.inventory import Inventory
from resources.payload.payload import Localtime

class Suppliers():
          
    def create_inventory_supplier(self, user):
        #Get the request data 
        request_data = request.get_json()       
        
        validated_data = request_data
        # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
        # if error_messages:
        #     return jsonify({"error": error_messages}), 400
        
        business_name = validated_data["business_name"]
        trading_name = validated_data["trading_name"]
        company_mobile_number = validated_data["company_mobile_number"]
        company_alternative_mobile_number = validated_data["company_alternative_mobile_number"]
        address = validated_data["address"]
        postal_code = validated_data["postal_code"]
        country = validated_data["country"]
        city = validated_data["city"]
        registration_number = validated_data["registration_number"]
        tax_id = validated_data["tax_id"]
        company_email = validated_data["company_email"]
        website = validated_data["company_website"]
        contact_persons = json.dumps(validated_data["contact_persons"])
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a11',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
        #Save data to the database
        
        try:
            status = 2 #pending approval
            created_date = Localtime().gettime()
            created_by = user['id']

            #store supplier details request
            cur.execute("""INSERT INTO suppliers (business_name, trading_name, company_mobile_number, company_alternative_mobile_number, company_email, website, address, postal_code, country, city, created_date, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                 (business_name, trading_name, company_mobile_number, company_alternative_mobile_number, company_email, website, address, postal_code, country, city, created_date, created_by, status))
            mysql.get_db().commit()
            
            rowcount = cur.rowcount
            if rowcount: 
                supplier_id = cur.lastrowid
                
                supplier_contact_persons = json.loads(contact_persons)                
                for contact_person in supplier_contact_persons:

                    title = contact_person["title"]
                    first_name = contact_person["first_name"]
                    last_name = contact_person["last_name"]
                    mobile_number = contact_person["mobile_number"]
                    alternative_mobile_number = contact_person["alternative_mobile_number"]
                    email = contact_person["email"]
                    
                    #save contact details
                    cur.execute("""INSERT INTO supplier_contact (supplier_id, title, first_name, last_name, mobile_number, alternative_mobile_number, email, created_date, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                                (supplier_id, title, first_name, last_name, mobile_number, alternative_mobile_number, email, created_date, created_by, status))
                    mysql.get_db().commit()
                    
                    
                #Create supplier payable account
                accountName = business_name
                type_Id = 9 #payable account type
                categoryId = 14 #account category 
                sub_category = 0
                mainaccount = 0
                openingBalance = 0     
                notes = ''
                owner_id = supplier_id
                entity_id = 0
                description = ''
                referenceNumber = ''
                
                account = {
                    "name":accountName, 
                    "accountType":type_Id, 
                    "accountCategory":categoryId, 
                    "accountSubCategory":sub_category,
                    "main_account":mainaccount,
                    "opening_balance":openingBalance, 
                    "owner_id":owner_id, 
                    "entity_id":entity_id, 
                    "notes":notes, 
                    "description":description, 
                    "reference_number":referenceNumber,
                    "user_id":created_by,
                    "status":1}
            
                payable_account_res = Account().create_new_account(account)
                    
                #Create supplier prepayment account
                accountName = business_name
                type_Id = 4 #prepaid expenses account type
                categoryId = 9 #prepaid expenses account category 
                sub_category = 0
                mainaccount = 0
                openingBalance = 0     
                notes = ''
                owner_id = supplier_id
                entity_id = 0
                description = ''
                referenceNumber = ''
                
                account = {
                    "name":accountName, 
                    "accountType":type_Id, 
                    "accountCategory":categoryId, 
                    "accountSubCategory":sub_category,
                    "main_account":mainaccount,
                    "opening_balance":openingBalance, 
                    "owner_id":owner_id, 
                    "entity_id":entity_id, 
                    "notes":notes, 
                    "description":description, 
                    "reference_number":referenceNumber,
                    "user_id":created_by,
                    "status":1}
            
                prepaid_account_res = Account().create_new_account(account)
                    
                cur.close()
            
            message = {"description":"Supplier was created successfully",
                       "status":200}
            return message
                        

        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a02',
                       'description':'Failed to create a supplier. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
  
    def list_inventory_suppliers(self, user):
        
        request_data = request.get_json() 
        if request_data == None:
            message = {'status':402,
                       'error':'sp_a03',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message)
       
        try:
            cur = mysql.get_db().cursor()
                    
        except:
            message = {'status':500,
                        'error':'sp_a14',
                        'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
                
        try:
            status = int(request_data["status"])
        
            cur.execute("""SELECT * from suppliers WHERE status= %s ORDER BY date_created DESC""", [status])
            results = cur.fetchall()    
            if results:
                trans = []
                no = 0

                for result in results:
                    created_by_id = result['created_by']
                    
                    cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s """, [created_by_id])
                    createdby_details = cur.fetchone()            
                    created_by = createdby_details['first_name'] + " " + createdby_details['last_name']
                    no = no + 1
                    res = {
                        "id": result['id'],
                        "no":no,
                        "business_name": result['business_name'],
                        "trading_name": result['trading_name'], 
                        "company_email": result['company_email'],
                        "company_mobile_number": result['company_mobile_number'],
                        "country": result['country'],
                        "address": result['address'],
                        "postal_code": result['postal_code'],
                        "datecreated": result['date_created'],
                        "createdby": created_by,                  
                        "created_by_id": created_by_id                  
                    }
                    trans.append(res)
                
                message = {'status':200,
                            'response':trans,
                            'description':'Supplier records were fetched successfully!'
                        }   
                return jsonify(message)             
            
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'Failed to fetch suppliers!'
                        }   
                ErrorLogger().logError(message)
                return jsonify(message) 
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve supplier record from database.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  

    def get_inventory_supplier_details(self, user):
        
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
            cur.execute("""SELECT * FROM suppliers WHERE id = %s""", (id))
            supplier = cur.fetchone()
            if supplier:  
                created_by_id = supplier['created_by']
                supplier_id = supplier['id']
                
                cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id= %s""", (created_by_id))
                userdetails = cur.fetchone()
                if userdetails:
                    created_by = userdetails['first_name'] + " " + userdetails['last_name']
                else:
                    created_by = ''
                
                contact_persons = []
                cur.execute("""SELECT * FROM supplier_contact WHERE supplier_id = %s""", (supplier_id))
                supplier_contacts = cur.fetchall()
                if supplier_contacts:  
                    for supplier_contact in supplier_contacts:
                        title = supplier_contact['title']
                        first_name = supplier_contact['first_name']
                        last_name = supplier_contact['last_name']
                        mobile_number = supplier_contact['mobile_number']
                        alternative_mobile_number = supplier_contact['alternative_mobile_number']
                        email = supplier_contact['email']
                        status = supplier_contact['status']
                        created_date = supplier_contact['created_date']
                        if int(status) ==1:
                            this_status = 'Active',
                        elif int(status) ==2:
                            this_status = 'Pending Approval',
                        else:
                            this_status = 'Not Active'
                        
                        response = {
                            "title":title,
                            "first_name":first_name,
                            "last_name":last_name,
                            "mobile_number":mobile_number,
                            "alternative_mobile_number":alternative_mobile_number,
                            "email":email,
                            "created_date":created_date,
                            "status":this_status
                            
                        }
                        contact_persons.append(response)
                        

                trans = {
                    "id": supplier['id'],
                    "business_name": supplier['business_name'],          
                    "trading_name": supplier['mobile_number'],
                    "company_mobile_number": supplier['company_mobile_number'],
                    "company_alternative_mobile_number": supplier['company_alternative_mobile_number'],
                    "company_email": supplier['company_email'],
                    "tax_id": supplier['tax_id'],
                    "registration_number": supplier['registration_number'],
                    "website": supplier['website'],
                    "country": supplier['country'],
                    "city": supplier['city'],
                    "address": supplier['address'],
                    "postal_code": supplier['postal_code'],
                    "created_date": supplier['created_date'],
                    "createdby": created_by,                  
                    "created_by_id": created_by_id,
                    "contact_persons":contact_persons               
                }
                
                #The response object
                         
                return trans
            else:
                message = 'No record was found!'
                return message 
                         
    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'description':'Failed to retrieve record from database.'+ format(error)}
            return jsonify(message)  
        finally:
            cur.close()
            
    # def approve_inventory_supplier(self, user):
    #     request_data = request.get_json()        
    #     if request_data == None:
    #         message = {'status':402,
    #                    'error':'sp_a06',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)

    #     id = request_data["id"]
        
    #     try:
    #         cur = mysql.get_db().cursor()
    #     except:
    #         message = {'status':500,
    #                    'error':'sp_a07',
    #                    'description':"Couldn't connect to the Database!"}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)

    #     try:  
    #         user_id = user['id']             
    #         cur.execute("""SELECT * FROM suppliers WHERE status =0 AND id = %s""", [id])
    #         supp = cur.fetchone()
    #         if supp:

    #             #Create supplier payable account
    #             accountName = supp["name"]
    #             type_Id = 8
    #             categoryId = 10
    #             sub_category = 0
    #             mainaccount = 0
    #             openingBalance = 0     
    #             notes = ''
    #             owner_id = id
    #             entity_id = 0
    #             description = ''
    #             referenceNumber = ''
                
    #             account = {
    #                    "name":accountName, 
    #                    "accountType":type_Id, 
    #                    "accountCategory":categoryId, 
    #                    "accountSubCategory":sub_category,
    #                    "main_account":mainaccount,
    #                    "opening_balance":openingBalance, 
    #                    "owner_id":owner_id, 
    #                    "entity_id":entity_id, 
    #                    "notes":notes, 
    #                    "description":description, 
    #                    "reference_number":referenceNumber,
    #                    "user_id":user_id,
    #                    "status":1}
            
    #             account_res = Account().create_new_account(account)
                

    #             details = {
    #                 "id":request_data["id"],
    #                 "user_id":user["id"]
    #             }
    #             supplier_res = Supplier().supplier_approve(details)
    #             if (supplier_res["status"] == 200):
                    
    #                 api_response = {'status':200,
    #                                 'description':'Task was completed successfully!'}

    #                 return jsonify(api_response)
                
    #             else:
    #                 message = {'status':500,
    #                            'error':'sp_a20',
    #                            'description':'Task was not completed successfully!'}
    #                 ErrorLogger().logError(message)
    #                 return jsonify(message)
                    
             
    #         else:
    #             message = {'status':500,
    #                        'error':'sp_a08',
    #                        'description':'Task was not completed successfully!'}
    #             ErrorLogger().logError(message)
    #             return jsonify(message)

    
    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'error':'sp_a09',
    #                    'description':'Failed to approve supplier record. Error description ' + format(error)}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)  
    #     finally:
    #         cur.close()
            
    # def inventory_item_purchase(self, user):
    #     #Get the request data 
    #     request_data = request.form        
    #     if request_data == None:
    #         message = {'status':402,
    #                    'error':'sp_a10',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)
        
    #     supplier_id = request_data["supplier_id"]
    #     item_id = request_data["item_id"]
    #     bank_account_number = request_data["bank_account_number"]       
    #     stock_account_number = request_data["stock_account_number"]       
    #     payable_account_number = request_data["payable_account_number"]       
    #     price_per_item = float(request_data["price_per_item"])
    #     quantity = float(request_data["quantity"])
    #     purchase_date = request_data["purchase_date"] 
    #     transaction_id = request_data["transaction_id"] 
    #     narrative = request_data["narrative"] 
    #     reference = request_data["reference"] 
    #     total_price =  quantity * price_per_item
        
    #      #Try except block to handle execute task
    #     try:
    #         details = {
    #             "supplier_id":supplier_id,
    #             "item_id":item_id,
    #             "bank_account_number":bank_account_number,
    #             "stock_account_number":stock_account_number,
    #             "payable_account_number":payable_account_number,
    #             "price_per_item":price_per_item,
    #             "quantity":quantity,
    #             "purchase_date":purchase_date,
    #             "total_price":total_price,
    #             "transaction_id":transaction_id,
    #             "narrative":narrative,
    #             "reference":reference,
    #             "user_id":user['id']
    #         }
    #         api_res = Inventory.purchase_inventory(self, details)            
    #         return jsonify(api_res)                


    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501, 
    #                    'error':'sp_a11',
    #                    'description':'Failed to create a inventory purchase record. Error description ' + format(error)}
    #         ErrorLogger().logError(message)
    #         return jsonify(message) 
        
    
    # def get_inventory_items_purchase_details(self, user):
    #     request_data = request.get_json()   

    #     if request_data == None:
    #         message = {'status':402,
    #                    'error':'sp_a10',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)

    #     id = int(request_data["id"]) 
        
    #     try:
    #         cur = mysql.get_db().cursor()
    #     except:
    #         message = {'status':500,
    #                    'error':'sp_a28',
    #                    'description':"Couldn't connect to the Database!"}
    #         ErrorLogger().logError(message)
    #         return message
                    
    #     try:    
    #         cur.execute("""SELECT * from inventory_items_purchased WHERE id = %s """, (id))
    #         result = cur.fetchone()    
    #         if result:
                
    #                 created_by_id = result['created_by']
    #                 item_id = result['item_id']
    #                 supplier_id = result['supplier_id']
    #                 bank_account_number = result['bank_account_number']
    #                 stock_account_number = result['stock_account_number']
    #                 payable_account_number = result['payable_account_number']
                    
    #                 cur.execute("""SELECT first_name, last_name FROM administrator_details WHERE user_id = %s """, [created_by_id])
    #                 createdby_details = cur.fetchone()            
    #                 created_by = createdby_details['first_name'] + " " + createdby_details['last_name']
                    
    #                 cur.execute("""SELECT item_name FROM inventory_items WHERE id = %s """, [item_id])
    #                 item_details = cur.fetchone()            
    #                 item_name = item_details['item_name']
                    

    #                 cur.execute("""SELECT name FROM suppliers WHERE id = %s """, [supplier_id])
    #                 supp_details = cur.fetchone()            
    #                 supplier_name = supp_details['name']

    #                 cur.execute("""SELECT name FROM accounts WHERE number = %s """, [bank_account_number])
    #                 bnk_details = cur.fetchone()            
    #                 bank_account_name = bnk_details['name']
                    
    #                 cur.execute("""SELECT name FROM accounts WHERE number = %s """, [stock_account_number])
    #                 stc_details = cur.fetchone()            
    #                 stock_account_name = stc_details['name']
                    
    #                 cur.execute("""SELECT name FROM accounts WHERE number = %s """, [payable_account_number])
    #                 payable_details = cur.fetchone()            
    #                 payable_account_name = payable_details['name']
                    
    #                 trans = {
    #                     "id": result['id'],
    #                     "item_name": item_name,
    #                     "item_id": item_id,
    #                     "quantity": float(result['quantity']),
    #                     "price_per_item": float(result['price_per_item']),
    #                     "total_price": float(result['total_price']),
    #                     "supplier_name": supplier_name,
    #                     "bank_account_name": bank_account_name, 
    #                     "stock_account_name": stock_account_name, 
    #                     "payable_account_name": payable_account_name, 
    #                     "reference": result['reference'],
    #                     "narrative": result['narrative'],
    #                     "transaction_id": result['transaction_id'],
    #                     "payable_account_name": payable_account_name, 
    #                     "datecreated": result['date_created'],
    #                     "global_id": result['global_id'],
    #                     "purchase_date": result['purchase_date'],
    #                     "date_created": result['date_created'],
    #                     "createdby": created_by,
    #                     "created_by_id": created_by_id                    
    #                 } 
                    
    #                 message = {'status':200,
    #                            'response':trans,
    #                            'description':'Inventory purchased record was found!'}
    #                 return message
            
    #         else:                
    #             message = {'status':201,
    #                        'error':'sp_a04',
    #                        'description':'Task was not completed successfully!'
    #                        }   
    #             ErrorLogger().logError(message)
    #             return jsonify(message)

    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'error':'sp_a05',
    #                    'description':'Failed to retrieve inventory purchased record from database.' + format(error)}
    #         ErrorLogger().logError(message)
    #         return jsonify(message) 
    #     finally:
    #         cur.close()
 
    # def get_inventory_items_purchases(self, user, id):
            
    #     if id == None:
    #         message = {'status':402,
    #                    'error':'sp_a10',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)
        
    #     id = int(id)
        
    #     try:
    #         cur = mysql.get_db().cursor()
    #     except:
    #         message = {'status':500,
    #                    'error':'sp_a28',
    #                    'description':"Couldn't connect to the Database!"}
    #         ErrorLogger().logError(message)
    #         return message
        
    #     try:
    #         if id ==1 or id ==0:
    #             # details = {"id":id}
    #             # api_res = Inventory().inventory_items_purchase_list(details) 
    #             cur.execute("""SELECT * from inventory_items_purchased WHERE status = %s ORDER BY date_created DESC""", [id])
    #             results = cur.fetchall()    
    #             if results:
    #                 no = 0
    #                 trans = []
                    
    #                 for result in results:
    #                     created_by_id = result['created_by']
    #                     item_id = result['item_id']
    #                     supplier_id = result['supplier_id']
    #                     bank_account_number = result['bank_account_number']
    #                     stock_account_number = result['stock_account_number']
    #                     payable_account_number = result['payable_account_number']
                        
    #                     cur.execute("""SELECT first_name, last_name FROM administrator_details WHERE user_id = %s """, [created_by_id])
    #                     createdby_details = cur.fetchone()            
    #                     created_by = createdby_details['first_name'] + " " + createdby_details['last_name']
                        
    #                     cur.execute("""SELECT item_name FROM inventory_items WHERE id = %s """, [item_id])
    #                     item_details = cur.fetchone()            
    #                     item_name = item_details['item_name']
                        

    #                     cur.execute("""SELECT name FROM suppliers WHERE id = %s """, [supplier_id])
    #                     supp_details = cur.fetchone()            
    #                     supplier_name = supp_details['name']

    #                     cur.execute("""SELECT name FROM accounts WHERE number = %s """, [bank_account_number])
    #                     bnk_details = cur.fetchone()            
    #                     bank_account_name = bnk_details['name']
                        
    #                     cur.execute("""SELECT name FROM accounts WHERE number = %s """, [stock_account_number])
    #                     stc_details = cur.fetchone()            
    #                     stock_account_name = stc_details['name']
                        
    #                     cur.execute("""SELECT name FROM accounts WHERE number = %s """, [payable_account_number])
    #                     payable_details = cur.fetchone()            
    #                     payable_account_name = payable_details['name']
    #                     no = no + 1
    #                     res = {
    #                         "id": result['id'],
    #                         "no":no,
    #                         "item_name": item_name,
    #                         "item_id": item_id,
    #                         "quantity": float(result['quantity']),
    #                         "price_per_item": float(result['price_per_item']),
    #                         "total_price": float(result['total_price']),
    #                         "supplier_name": supplier_name,
    #                         "bank_account_name": bank_account_name, 
    #                         "stock_account_name": stock_account_name, 
    #                         "payable_account_name": payable_account_name, 
    #                         "reference": result['reference'],
    #                         "narrative": result['narrative'],
    #                         "transaction_id": result['transaction_id'],
    #                         "datecreated": result['date_created'],
    #                         "global_id": result['global_id'],
    #                         "purchase_date": result['purchase_date'],
    #                         "date_created": result['date_created'],
    #                         "createdby": created_by,                  
    #                         "created_by_id": created_by_id                  
    #                     }
    #                     trans.append(res)
                    
    #                 message = {'status':200,
    #                            'response':trans,
    #                            'description':'Inventory purchased records were found!'}
    #                 return message
    #             else:
    #                 message = {"status description":"Inventory purchased records were not found!",
    #                            'error':'sp_a29',
    #                            "status":402}
    #                 ErrorLogger().logError(message)
    #                 return message
                
            
    #         else:                
    #             message = {'status':201,
    #                        'error':'sp_a04',
    #                        'description':'Task was not completed successfully!'
    #                        }   
    #             ErrorLogger().logError(message)
    #             return jsonify(message)

    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'error':'sp_a30',
    #                    'description':'Failed to get Inventory purchased record from database. ' + format(error)}
    #         ErrorLogger().logError(message)
    #         return message  
    #     finally:
    #         cur.close()

    # def approve_inventory_item_purchase(self, user):
    #     request_data = request.get_json()   

    #     if request_data == None:
    #         message = {'status':402,
    #                    'error':'sp_a10',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)

    #     id = int(request_data["id"])       

    #     try:
    #         cur = mysql.get_db().cursor()
    #     except:
    #         message = {'status':500,
    #                    'error':'sp_a07',
    #                    'description':"Couldn't connect to the Database!"}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)

    #     try:    
    #         if id >0:
                
    #             cur.execute("""SELECT * FROM inventory_items_purchased WHERE status =0 AND id = %s""", [id])
    #             inv = cur.fetchone()
    #             if inv:
    #                 item_id = inv["item_id"]
    #                 supplier_id = inv["supplier_id"]
    #                 amount = float(inv["total_price"])
    #                 global_id = inv["global_id"]
    #                 bank_account_number = inv["bank_account_number"]

    #                 #Increase inventory stock account
    #                 #Get inventory account
    #                 cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =2 AND owner_id = %s """, [item_id])
    #                 get_inventory_account = cur.fetchone() 
    #                 if get_inventory_account:
    #                     inventory_account = get_inventory_account["number"]

    #                 #Get supplier payable account
    #                 cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =8 AND owner_id = %s """, [supplier_id])
    #                 get_payable_account = cur.fetchone()                
    #                 if get_payable_account:
    #                     payable_account = get_payable_account["number"]
                     
    #                 details = {
    #                     "id":request_data["id"],
    #                     "user_id":user["id"],
    #                     "global_id":global_id,
    #                     "inventory_account":inventory_account,
    #                     "payable_account":payable_account,
    #                     "amount":amount,
    #                 }      
                       

    #                 inventory_purchase = Inventory().inventory_purchase_approve(details)
    #                 if int(inventory_purchase["status"]) == 200:

    #                     #Call API for Inventory Payment
    #                     payment_details = {
    #                             "id":details["id"],
    #                             "global_id":global_id,
    #                             "bank_account_number":bank_account_number,
    #                             "payable_account_number":payable_account,
    #                             "amount":amount
    #                     }
    #                     inventory_payment = Inventory().inventory_payment(payment_details)
    #                     if int(inventory_payment["status"]) == 200:
    #                         message = {
    #                                     "status":200,
    #                                     "description":"Transaction was approved successfully!"
    #                                 }
    #                         return jsonify(message) 
                        
    #                     else:
    #                         message = {
    #                                     "status":201,
    #                                     "description":"Transaction failed! Task was not completed successfully!"
    #                                 }
    #                     return jsonify(message) 
                        
                    
    #                 else:
    #                     message = {
    #                     "status":201,
    #                     "description":"Transaction failed! Task was not completed successfully!"
    #                 }
    #                 return jsonify(message) 

    #             else:
    #                 message = {
    #                     "status":201,
    #                     "description":"Transaction failed! Task was not completed successfully!"
    #                 }
    #                 return jsonify(message)  

    #         else:
    #             message = {
    #                 "status":201,
    #                 "description":"Transaction failed! Task was not completed successfully!"
    #                 }

    #             return jsonify(message)
            
    
    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'description':'Transaction failed. Error description ' + format(error)}
    #         return jsonify(message)  
    #     finally:
    #         cur.close()
                
    # def inventory_item_credit_purchase(self, user):
    #         #Get the request data 
    #     request_data = request.form     
    #     if request_data == None:

    #         message = {'status':402,
    #                    'error':'sp_a06',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)

        
    #     supplier_id = request_data["supplier_id"]
    #     supplier_payable_account = request_data["supplier_account"]
    #     item_id = request_data["item_id"]
    #     inventory_stock_account = request_data["stock_account"]     
    #     price_per_item = float(request_data["price_per_item"])
    #     quantity = float(request_data["quantity"])        
    #     purchase_date = request_data["purchase_date"] 
        
    #     invoice_id = request_data["invoice_id"] 
    #     reference = request_data["reference"] 
    #     narrative = request_data["narrative"] 
        
        
    #     amount =  quantity * price_per_item
        
    #      #Try except block to handle execute task
    #     try:
    #         details = {
    #             "supplier_id":supplier_id,
    #             "supplier_payable_account":supplier_payable_account,                
    #             "inventory_stock_account":inventory_stock_account,
    #             "item_id":item_id,
    #             "price_per_item":price_per_item,
    #             "quantity":quantity,
    #             "purchase_date":purchase_date,
    #             "total_price":amount,
                
    #             "invoice_id":invoice_id,
    #             "reference":reference,
    #             "narrative":narrative,
                
    #             "user_id":user['id']
    #         }
            
    #         api_response = Inventory().credit_purchase_inventory(details)            
    #         return jsonify(api_response)

    #     except Exception as error:
    #         message = {'status':501,
    #                    'error':'sp_a05',
    #                    'description':'Failed to create transaction in the database.' + format(error)}
    #         ErrorLogger().logError(message)
    #         return jsonify(message) 
        
    # def get_inventory_items_credit_purchases(self, user, id):
            
    #     if id == None:
    #         message = {'status':402,
    #                    'error':'sp_a06',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)

    #     id = int(id)
        
    #     try:
    #         if id ==1 or id ==0:
    #             details = {
    #                 "id":id,
    #             }
    #             api_response = Inventory().inventory_items_credit_purchase_list(details)
    #             return jsonify(api_response)
    #         else:
      
    #             message = {
    #                 "status":201,
    #                 "response":[],
    #                 "description":"Transaction failed! Task was not completed successfully!"
    #                 }

    #             return message


    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'description':'Failed to insert record to database' + format(error)}
    #         return message
    
    # def get_inventory_unpaid_supplier_invoices(self, user, id):
            
    #     if id == None:
    #         message = {'status':402,
    #                    'error':'sp_a06',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)

    #     id = int(id)
        
    #     try:
    #         if id ==1 or id ==0:
    #             details = {
    #                 "id":id,
    #             }
    #             api_response = Inventory().unpaid_supplier_invoice_list(details)
    #             return jsonify(api_response)
    #         else:
      
    #             message = {
    #                 "status":201,
    #                 "response":[],
    #                 "description":"Transaction failed! Task was not completed successfully!"
    #                 }

    #             return message


    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'description':'Failed to insert record to database' + format(error)}
    #         return message
        
    # def get_inventory_items_credit_purchase_details(self, user):
    #     request_data = request.get_json()   

    #     if request_data == None:
    #         message = {'status':402,
    #                    'error':'sp_a10',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)

    #     id = int(request_data["id"]) 
        
    #     try:
    #         cur = mysql.get_db().cursor()
    #     except:
    #         message = {'status':500,
    #                    'error':'sp_a28',
    #                    'description':"Couldn't connect to the Database!"}
    #         ErrorLogger().logError(message)
    #         return message
                    
    #     try:            
                
    #         cur.execute("""SELECT * from inventory_credit_purchases WHERE id = %s ORDER BY date_created DESC""", (id)) 
    #         result = cur.fetchone()    
    #         if result:
                
    #                 created_by_id = result['created_by']
    #                 item_id = result['inventory_id']
    #                 supplier_id = result['supplier_id']
    #                 # bank_account_number = result['bank_account_number']
    #                 stock_account_number = result['inventory_stock_account']
    #                 payable_account_number = result['supplier_payable_account']
                    
    #                 cur.execute("""SELECT first_name, last_name FROM administrator_details WHERE user_id = %s """, [created_by_id])
    #                 createdby_details = cur.fetchone()            
    #                 created_by = createdby_details['first_name'] + " " + createdby_details['last_name']
                    
    #                 cur.execute("""SELECT item_name FROM inventory_items WHERE id = %s """, [item_id])
    #                 item_details = cur.fetchone()            
    #                 item_name = item_details['item_name']
                    

    #                 cur.execute("""SELECT name FROM suppliers WHERE id = %s """, [supplier_id])
    #                 supp_details = cur.fetchone()            
    #                 supplier_name = supp_details['name']

                    
    #                 cur.execute("""SELECT name FROM accounts WHERE number = %s """, [stock_account_number])
    #                 stc_details = cur.fetchone()            
    #                 stock_account_name = stc_details['name']
                    
    #                 cur.execute("""SELECT name FROM accounts WHERE number = %s """, [payable_account_number])
    #                 payable_details = cur.fetchone()            
    #                 payable_account_name = payable_details['name']
                    
    #                 quantity = float(result['quantity'])
    #                 quantity = round(quantity, 2)
                    
    #                 amount = float(result['amount'])
    #                 amount = round(amount, 4)
                    
    #                 amount_due = float(result['amount_due'])
    #                 amount_due = round(amount_due, 4)
                    
    #                 amount_paid = float(result['amount_paid'])
    #                 amount_paid = round(amount_paid, 4)
                    
    #                 trans = {
    #                     "id": result['id'],
    #                     "item_name": item_name,
    #                     "item_id": item_id,
    #                     "quantity": float(result['quantity']),
    #                     "price_per_item": float(result['price_per_item']),
    #                     "total_price": amount,
    #                     "amount_due": amount_due,
    #                     "amount_paid": amount_paid,
    #                     "supplier_name": supplier_name,
    #                     "stock_account_name": stock_account_name, 
    #                     "payable_account_name": payable_account_name, 
    #                     "reference": result['reference'],
    #                     "narrative": result['narrative'],
    #                     "invoice_id": result['invoice_id'],
    #                     "payable_account_name": payable_account_name, 
    #                     "datecreated": result['date_created'],
    #                     "global_id": result['global_id'],
    #                     "purchase_date": result['purchase_date'],
    #                     "date_created": result['date_created'],
    #                     "createdby": created_by,
    #                     "created_by_id": created_by_id                    
    #                 } 
                    
    #                 message = {'status':200,
    #                            'response':trans,
    #                            'description':'Inventory credit purchase record was found!'}
    #                 return message
            
    #         else:                
    #             message = {'status':201,
    #                        'error':'sp_a04',
    #                        'description':'Task was not completed successfully!'
    #                        }   
    #             ErrorLogger().logError(message)
    #             return jsonify(message)

    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'error':'sp_a05',
    #                    'description':'Failed to retrieve inventory credit purchase record from database.' + format(error)}
    #         ErrorLogger().logError(message)
    #         return jsonify(message) 
    #     finally:
    #         cur.close()
            
    # def approve_inventory_item_credit_purchase(self, user):
    #     request_data = request.get_json()   

    #     if request_data == None:
    #         message = {'status':402,
    #                    'error':'sp_a06',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)

    #     id = int(request_data["id"])       

    #     try:
    #         cur = mysql.get_db().cursor()
    #     except:
    #         message = {'status':500,
    #                    'error':'sp_a07',
    #                    'description':"Couldn't connect to the Database!"}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)

    #     try:    
    #         if id >0:
                
    #             cur.execute("""SELECT * FROM inventory_credit_purchases WHERE status =0 AND id = %s""", [id])
    #             inv = cur.fetchone()
    #             if inv:
    #                 item_id = inv["inventory_id"]
    #                 supplier_id = inv["supplier_id"]
    #                 amount = float(inv["amount"])
    #                 global_id = inv["global_id"]
    #                 inventory_account = inv["inventory_stock_account"]
    #                 payable_account = inv["supplier_payable_account"]
                    
    #                 details = {
    #                     "id":request_data["id"],
    #                     "user_id":user["id"],
    #                     "global_id":global_id,
    #                     "inventory_account":inventory_account,
    #                     "payable_account":payable_account,
    #                     "amount":amount,
    #                 }            

    #                 api_response = Inventory().inventory_credit_purchase_approve(details)
    #                 return jsonify(api_response) 

    #             else:
    #                 message = {
    #                 "status":201,
    #                 "description":"Transaction failed! Task was not completed successfully!"
    #                 }

    #                 return message

    #         else:
    #             message = {
    #                 "status":201,
    #                 "description":"Transaction failed! Task was not completed successfully!"
    #                 }

    #             return message 
            
    
    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'description':'Failed to insert record to database' + format(error)}
    #         return message
        
    # def pay_supplier_invoice(self, user):
    #         #Get the request data 
    #     request_data = request.form       
    #     if request_data == None:
    #         message = {'status':402,
    #                    'error':'sp_a01',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)            
    #         return jsonify(message)
        
    #     paid_amount = float(request_data["paid_amount"])
    #     reference = request_data["reference"]
    #     narrative = request_data["narrative"]
    #     entry_id = request_data["entry_id"]
    #     bank_account_number = request_data["bank_account_number"]
    #     user_id = user['id']
        
        
    #      #Try except block to handle execute task
    #     try:
            
    #         details = {
    #             "entry_id":entry_id,
    #             "paid_amount":paid_amount,
    #             "reference":reference,
    #             "narrative":narrative,
    #             "bank_account_number":bank_account_number,
    #             "user_id":user_id
    #         }
    #         api_res = Supplier().pay_supplier_invoice_draft(details)            
    #         return jsonify(api_res)                

    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501, 
    #                    'error':'sp_a02',
    #                    'description':'Failed to pay supplier invoice. Error description ' + format(error)}
    #         ErrorLogger().logError(message)
    #         return jsonify(message) 
          
    # def get_supplier_invoice_payment(self, user, id):
            
    #     if id == None:
    #         message = {'status':402,
    #                    'error':'sp_a10',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)
        
    #     id = int(id)
        
    #     try:
    #         cur = mysql.get_db().cursor()
    #     except:
    #         message = {'status':500,
    #                    'error':'sp_a28',
    #                    'description':"Couldn't connect to the Database!"}
    #         ErrorLogger().logError(message)
    #         return message
        
    #     try:
    #         if id ==1 or id ==0:
    #             # details = {"id":id}
    #             # api_res = Inventory().inventory_items_purchase_list(details)
    #             cur.execute("""SELECT * from inventory_credit_paid WHERE status = %s ORDER BY date_created DESC""", [id]) 
    #             results = cur.fetchall()    
    #             if results:
    #                 no = 0
    #                 trans = []
                    
    #                 for result in results:
    #                     entry_id = result['id']                        
    #                     created_by_id = result['created_by']
    #                     credit_purchase_id = result['credit_purchase_id']
    #                     amount_paid = float(result['amount_paid'])
    #                     amount_paid = round(amount_paid,2)
                        
    #                     bank_account_number = result['bank_account']
    #                     payable_account_number = result['supplier_account']
    #                     reference = result['reference']
    #                     narrative = result['narrative']
    #                     date_created = result['date_created']
    #                     global_id = result['global_id']                        
                        
    #                     cur.execute("""SELECT * from inventory_credit_purchases WHERE id = %s """, [credit_purchase_id])
    #                     purch = cur.fetchone()  
    #                     if purch:                            
    #                         item_id = purch['inventory_id']
    #                         supplier_id = purch['supplier_id']
    #                         stock_account_number = purch['inventory_stock_account']
    #                         quantity = float(purch['quantity'])
    #                         price_per_item = float(purch['price_per_item'])
    #                         total_price = float(purch['amount'])
    #                         invoice_id = purch['invoice_id']
    #                         purchase_date = purch['purchase_date']
                        
    #                     cur.execute("""SELECT first_name, last_name FROM administrator_details WHERE user_id = %s """, [created_by_id])
    #                     createdby_details = cur.fetchone()            
    #                     created_by = createdby_details['first_name'] + " " + createdby_details['last_name']
                        
    #                     cur.execute("""SELECT item_name FROM inventory_items WHERE id = %s """, [item_id])
    #                     item_details = cur.fetchone()            
    #                     item_name = item_details['item_name']
                        
    #                     cur.execute("""SELECT name FROM suppliers WHERE id = %s """, [supplier_id])
    #                     supp_details = cur.fetchone()            
    #                     supplier_name = supp_details['name']

    #                     cur.execute("""SELECT name FROM accounts WHERE number = %s """, [bank_account_number])
    #                     bnk_details = cur.fetchone()            
    #                     bank_account_name = bnk_details['name']
                        
    #                     cur.execute("""SELECT name FROM accounts WHERE number = %s """, [stock_account_number])
    #                     stc_details = cur.fetchone()            
    #                     stock_account_name = stc_details['name']
                        
    #                     cur.execute("""SELECT name FROM accounts WHERE number = %s """, [payable_account_number])
    #                     payable_details = cur.fetchone()            
    #                     payable_account_name = payable_details['name']
    #                     no = no + 1
    #                     res = {
    #                         "id": entry_id,
    #                         "no":no,
    #                         "item_name": item_name,
    #                         "item_id": item_id,
    #                         "quantity": quantity,
    #                         "price_per_item": price_per_item,
    #                         "total_price": total_price,
    #                         "amount_paid":amount_paid,
    #                         "supplier_name": supplier_name,
    #                         "bank_account_name": bank_account_name, 
    #                         "stock_account_name": stock_account_name, 
    #                         "payable_account_name": payable_account_name, 
    #                         "reference": reference,
    #                         "narrative": narrative,
    #                         "invoice_id": invoice_id,
    #                         "datecreated": date_created,
    #                         "global_id": global_id,
    #                         "purchase_date": purchase_date,
    #                         "createdby": created_by,                  
    #                         "created_by_id": created_by_id                  
    #                     }
    #                     trans.append(res)
                    
    #                 message = {'status':200,
    #                            'response':trans,
    #                            'description':'Invoice payment records were found!'}
    #                 return message
    #             else:
    #                 message = {"status description":"Invoice payment records were not found!",
    #                            'error':'sp_a29',
    #                            "status":402}
    #                 ErrorLogger().logError(message)
    #                 return message
                
            
    #         else:                
    #             message = {'status':201,
    #                        'error':'sp_a04',
    #                        'description':'Task was not completed successfully!'
    #                        }   
    #             ErrorLogger().logError(message)
    #             return jsonify(message)

    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'error':'sp_a30',
    #                    'description':'Failed to get Invoice payment records from database. ' + format(error)}
    #         ErrorLogger().logError(message)
    #         return message  
    #     finally:
    #         cur.close()
            
    # def get_supplier_invoice_payment_details(self, user):
            
    #     request_data = request.get_json()   

    #     if request_data == None:
    #         message = {'status':402,
    #                    'error':'sp_a10',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)

    #     id = int(request_data["id"]) 
        
    #     try:
    #         cur = mysql.get_db().cursor()
    #     except:
    #         message = {'status':500,
    #                    'error':'sp_a28',
    #                    'description':"Couldn't connect to the Database!"}
    #         ErrorLogger().logError(message)
    #         return message
        
    #     try:
            
    #         # details = {"id":id}
    #         # api_res = Inventory().inventory_items_purchase_list(details)
    #         cur.execute("""SELECT * from inventory_credit_paid WHERE id = %s """, [id])
    #         result = cur.fetchone() 
    #         if result:                   
    #             created_by_id = result['created_by']
    #             credit_purchase_id = result['credit_purchase_id']
    #             amount_paid = float(result['amount_paid'])
    #             amount_paid = round(amount_paid,2)
                
    #             bank_account_number = result['bank_account']
    #             payable_account_number = result['supplier_account']
    #             reference = result['reference']
    #             narrative = result['narrative']
    #             date_created = result['date_created']
    #             global_id = result['global_id']                        
                    
    #             cur.execute("""SELECT * from inventory_credit_purchases WHERE id = %s """, [credit_purchase_id])
    #             purch = cur.fetchone()  
    #             if purch:                            
    #                 item_id = purch['inventory_id']
    #                 supplier_id = purch['supplier_id']
    #                 stock_account_number = purch['inventory_stock_account']
    #                 quantity = float(purch['quantity'])
    #                 price_per_item = float(purch['price_per_item'])
    #                 total_price = float(purch['amount'])
    #                 invoice_id = purch['invoice_id']
    #                 purchase_date = purch['purchase_date']
                    
    #             cur.execute("""SELECT first_name, last_name FROM administrator_details WHERE user_id = %s """, [created_by_id])
    #             createdby_details = cur.fetchone()            
    #             created_by = createdby_details['first_name'] + " " + createdby_details['last_name']
                
    #             cur.execute("""SELECT item_name FROM inventory_items WHERE id = %s """, [item_id])
    #             item_details = cur.fetchone()            
    #             item_name = item_details['item_name']
                
    #             cur.execute("""SELECT name FROM suppliers WHERE id = %s """, [supplier_id])
    #             supp_details = cur.fetchone()            
    #             supplier_name = supp_details['name']

    #             cur.execute("""SELECT name FROM accounts WHERE number = %s """, [bank_account_number])
    #             bnk_details = cur.fetchone()            
    #             bank_account_name = bnk_details['name']
                
    #             cur.execute("""SELECT name FROM accounts WHERE number = %s """, [stock_account_number])
    #             stc_details = cur.fetchone()            
    #             stock_account_name = stc_details['name']
                
    #             cur.execute("""SELECT name FROM accounts WHERE number = %s """, [payable_account_number])
    #             payable_details = cur.fetchone()            
    #             payable_account_name = payable_details['name']
                
    #             res = {
    #                 "id": id,
                    
    #                 "item_name": item_name,
    #                 "item_id": item_id,
    #                 "quantity": quantity,
    #                 "price_per_item": price_per_item,
    #                 "total_price": total_price,
    #                 "amount_paid":amount_paid,
    #                 "supplier_name": supplier_name,
    #                 "bank_account_name": bank_account_name, 
    #                 "stock_account_name": stock_account_name, 
    #                 "payable_account_name": payable_account_name, 
    #                 "reference": reference,
    #                 "narrative": narrative,
    #                 "invoice_id": invoice_id,
    #                 "date_created": date_created,
    #                 "global_id": global_id,
    #                 "purchase_date": purchase_date,
    #                 "createdby": created_by,                  
    #                 "created_by_id": created_by_id                  
    #             }
                    
                
    #             message = {'status':200,
    #                         'response':res,
    #                         'description':'Invoice payment record was found!'}
    #             return message
    #         else:
    #             message = {"status description":"Invoice payment record was not found!",
    #                         'error':'sp_a29',
    #                         "status":402}
    #             ErrorLogger().logError(message)
    #             return message
            

    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'error':'sp_a30',
    #                    'description':'Failed to get Invoice payment record from database. ' + format(error)}
    #         ErrorLogger().logError(message)
    #         return message  
    #     finally:
    #         cur.close()
            
    # def approve_supplier_invoice_payment(self, user):
        # request_data = request.get_json()   

        # if request_data == None:
        #     message = {'status':402,
        #                'error':'sp_a10',
        #                'description':'Request data is missing some details!'}
        #     ErrorLogger().logError(message)
        #     return jsonify(message)

        # id = int(request_data["id"])       

        # try:
        #     cur = mysql.get_db().cursor()
        # except:
        #     message = {'status':500,
        #                'error':'sp_a07',
        #                'description':"Couldn't connect to the Database!"}
        #     ErrorLogger().logError(message)
        #     return jsonify(message)

        # try:    
        #     cur.execute("""SELECT * FROM inventory_credit_paid WHERE status =0 AND id = %s""", [id])
        #     inv = cur.fetchone()
        #     if inv:
        #         amount = float(inv["amount_paid"])
        #         global_id = inv["global_id"]
        #         bank_account_number = inv["bank_account"]
        #         payable_account = inv["supplier_account"]
        #         user_id = user["id"]
                
        #         #Call API for invoice Payment
        #         payment_details = {
        #                 "id":id,
        #                 "global_id":global_id,
        #                 "bank_account_number":bank_account_number,
        #                 "payable_account_number":payable_account,
        #                 "amount":amount,
        #                 "user_id":user_id
        #         }
        #         inventory_payment = Supplier().approve_invoice_payment(payment_details)
        #         if int(inventory_payment["status"]) == 200:
        #             message = {
        #                         "status":200,
        #                         "description":"Transaction was approved successfully!"
        #                     }
        #             return jsonify(message) 
                
        #         else:
        #             message = {
        #                         "status":201,
        #                         "description":"Transaction failed! Task was not completed successfully!"
        #                     }
        #         return jsonify(message) 
                    
            
        #     else:
        #         message = {
        #             "status":201,
        #             "description":"Transaction failed! Task was not completed successfully!"
        #         }
        #         return jsonify(message)  
            
        # #Error handling
        # except Exception as error:
        #     message = {'status':501,
        #                'description':'Transaction failed. Error description ' + format(error)}
        #     return jsonify(message)  
        # finally:
        #     cur.close()