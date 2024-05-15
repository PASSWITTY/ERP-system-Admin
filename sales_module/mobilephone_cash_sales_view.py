from flask import request, Response, json, jsonify
from main import mysql, app
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from accounting_module.accounting_view import Accounting
from resources.accounts.accounts_class import Accounts

class MobilePhoneCashSales():
          
    def create_cash_sales(self, user):
        #Get the request data 
        request_data = request.get_json()       
        
        validated_data = request_data
        # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
        # if error_messages:
        #     return jsonify({"error": error_messages}), 400
        
        sales_date = validated_data["sales_date"]
        payment_mothod = validated_data["payment_mothod"]
        customer_name = validated_data["customer_name"]
        customer_number = validated_data["customer_mobile_number"]
        customer_email = validated_data["customer_email"]
        product_details = json.dumps(validated_data["product_details"])
        
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
            #Get sales agent distribution center details
            agent_id = user['id']
            cur.execute("""SELECT distribution_center_id FROM user_details WHERE user_id = %s """, (agent_id))
            agent_details = cur.fetchone()
            if agent_details:
                distribution_center_id = agent_details["distribution_center_id"]
            else:
                distribution_center_id = ''
                message = {"description":"Agent does not belong to a distribution center",
                           "status":404}
                return message
            
            total_sales_amount = 0
            total_net_sales_amount = 0
            total_buying_price_amount = 0
            total_discount_amount = 0
            
            
            phone_model_details = json.loads(product_details)                
            for phone_model_detail in phone_model_details:
                model_id = phone_model_detail["model_id"]
                imei_1 = phone_model_detail["imei_1"]
                quantity = float(phone_model_detail["quantity"])
                
                #get specific phone global_id
                cur.execute("""SELECT global_id FROM mobile_phones_transit_stock_received WHERE imei_1 = %s """, (imei_1))
                phone_details = cur.fetchone() 
                if phone_details:
                    global_id = phone_details["global_id"]
                else:
                    global_id = ''
                    message = {"description":"This phone does not have global id",
                               "status":404}
                    return message
                
                #get specific phone buying price
                cur.execute("""SELECT price_per_unit FROM cash_stock_purchase_models WHERE model_id = %s AND global_id = %s """, (model_id, global_id))
                get_phone_buying_price = cur.fetchone() 
                if get_phone_buying_price:
                    price_per_unit = float(get_phone_buying_price["price_per_unit"])
                else:
                    price_per_unit = ''
                    message = {"description":"This phone does not have global id",
                               "status":404}
                    return message
                
                cur.execute("""SELECT id, price_amount, discount_amount, final_price FROM distribution_center_mobilephone_model_prices WHERE status =1 AND model_id = %s AND distribution_center_id = %s """, (model_id, distribution_center_id))
                get_phone_model_price = cur.fetchone() 
                if get_phone_model_price:
                    price_amount = float(get_phone_model_price["price_amount"])
                    discount_amount = float(get_phone_model_price["discount_amount"])
                    final_price = float(get_phone_model_price["final_price"])
                else:
                    price_amount = 0
                    discount_amount = 0
                    final_price = 0
                    
                total_sellingprice_per_model = price_amount * quantity
                total_discount_amount_per_model = discount_amount * quantity
                total_final_price_per_model = final_price * quantity
                
                total_buyingprice_per_model = price_per_unit * quantity
                
                total_sales_amount = total_sales_amount + total_sellingprice_per_model
                total_net_sales_amount = total_net_sales_amount + total_final_price_per_model
                total_buying_price_amount = total_buying_price_amount + total_buyingprice_per_model
                total_discount_amount = total_discount_amount + total_discount_amount_per_model 
                                
                    
            status = 2 #pending approval
            created_date = Localtime().gettime()
            
            #fetch default bank account
            ##########################UPDATE THIS TO => fetch cash and cash equivalent account as per PAYMENT METHOD SELECTED. 
            bnk_acc_response = Accounts().bnk_account()
            if int(bnk_acc_response["status"]) == 200:
                bank_account = bnk_acc_response["data"]
            else:
                message = {'status':501,
                            'description':"Couldn't fetch default bank account!"}
                
                return message
            
            
            #Fetch default receivable account
            rec_acc_response = Accounts().receivable_account()
            if int(rec_acc_response["status"]) == 200:
                receivable_account = rec_acc_response["data"]
            else:
                message = {'status':501,
                            'description':"Couldn't fetch default receivable account!"}
                
                return message
            
            #Fetch default tax expense account
            tax_expense_response = Accounts().receivable_account()
            if int(tax_expense_response["status"]) == 200:
                tax_expense_account = tax_expense_response["data"]
            else:
                message = {'status':501,
                            'description':"Couldn't fetch default tax expense account!"}
                
                return message
            
            #Fetch default tax payable account
            tax_payable_response = Accounts().taxpayable_account()
            if int(tax_payable_response["status"]) == 200:
                tax_payable_account = tax_payable_response["data"]
            else:
                message = {'status':501,
                            'description':"Couldn't fetch default tax payable account!"}
                
                return message
            
            
            #mobile phone cash sales
            cur.execute("""INSERT INTO mobile_phone_cash_sales (distribution_center_id, agent_id,        total_buying_price, total_selling_price,        total_discount, total_net_sales_amount, sales_date, payment_mothod, customer_name, customer_number, customer_email, bank_account, receivable_account, tax_expense_account, tax_payable_account, created_date, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                               (distribution_center_id, agent_id, total_buying_price_amount,  total_sales_amount, total_discount_amount, total_net_sales_amount, sales_date, payment_mothod, customer_name, customer_number, customer_email, bank_account, receivable_account, tax_expense_account, tax_payable_account, created_date,   agent_id, status))
            mysql.get_db().commit()
            rowcount = cur.rowcount
            if rowcount:
            
                message = {"description":"Mobile phone cash sales was created successfully",
                        "status":200}
                return message
            else:
                message = {"description":"Failed to create mobile phone cash sales",
                           "status":501}
                return message
                
        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a02',
                       'description':'Failed to create a mobile phone cash sales. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()
  
    def list_cash_sales(self, user):
        
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
            status = request_data["status"]
        
            cur.execute("""SELECT id, product_sub_category_id, name, ram, internal_storage, main_camera, front_camera, display, processor, operating_system, connectivity, colors, battery, image_path, date_created, created_by FROM product_mobile_phones_models WHERE status = %s """, (status))
            phone_models = cur.fetchall()            
            if phone_models:
                mobile_phone_models = []
                
                for phone_model in phone_models:
                    response = {
                        "id": phone_model['id'],
                        "product_sub_category_id": phone_model['product_sub_category_id'],
                        "name": phone_model['name'],
                        "ram": phone_model['ram'],
                        "internal_storage": phone_model['internal_storage'],
                        "main_camera": phone_model['main_camera'],
                        "front_camera": phone_model['front_camera'],
                        "display": phone_model['display'],
                        "processor": phone_model['processor'],
                        "operating_system": phone_model['operating_system'],
                        "connectivity": phone_model['connectivity'],
                        "colors": phone_model['colors'],
                        "battery": phone_model['battery'],
                        "image_path": phone_model['image_path'],
                        "date_created": phone_model['date_created'],
                        "created_by_id": phone_model['created_by']
                    }
                    mobile_phone_models.append(response)
            
            
                message = {'status':200,
                            'response':mobile_phone_models, 
                            'description':'Mobile phone model records were fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'Failed to fetch mobile phone model!'
                        }   
                return jsonify(message), 201             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve mobile phone model record from database.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        
    def get_cash_sales_details(self, user):
        
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
            
            cur.execute("""SELECT * FROM product_mobile_phones_models WHERE id = %s""", [id])
            phone_model = cur.fetchone()
            if phone_model:  
                created_by_id = phone_model['created_by']
                
                cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id= %s""", (created_by_id))
                userdetails = cur.fetchone()
                if userdetails:
                    created_by_name = userdetails['first_name'] + " " + userdetails['last_name']
                else:
                    created_by_name = ''

                trans = {
                    "id": phone_model['id'],
                    "name": phone_model['name'],   
                    "ram": phone_model['ram'],
                    "internal_storage": phone_model['internal_storage'],
                    "main_camera": phone_model['main_camera'],
                    "front_camera": phone_model['front_camera'],
                    "display": phone_model['display'],
                    "processor": phone_model['processor'],
                    "operating_system": phone_model['operating_system'],
                    "connectivity": phone_model['connectivity'],
                    "colors": phone_model['colors'],
                    "battery": phone_model['battery'],
                    "image_path": phone_model['image_path'],
                    "date_created": phone_model['date_created'],
                    "created_by_id": created_by_name             
                }
                         
                return trans
            
            else:
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'Failed to fetch mobile phone model!'
                        }   
                return jsonify(message), 201 
                

        #Error handling
        except Exception as error:
            message = {'status':501,
                       'description':'Failed to retrieve record from database.'+ format(error)}
            return jsonify(message)  
        finally:
            cur.close()
            
    def approve_cash_sales(self, user):
        request_data = request.get_json() 
               
        if request_data == None:
            message = {'status':402,
                       'error':'sp_a06',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message)

        id = request_data["id"]

        approved_by = user["id"]
        dateapproved = Localtime().gettime()
        
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a07',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)

        try:  
            cur.execute("""SELECT name, created_by FROM product_mobile_phones_models WHERE id = %s""", [id])
            phonemodel = cur.fetchone()
            if phonemodel:
                model_name = phonemodel["name"]
                created_by = phonemodel["created_by"]
                
            #update phone model status
            cur.execute("""UPDATE product_mobile_phones_models set status=1, date_approved = %s, approved_by = %s WHERE status =2 AND id = %s """, ([dateapproved, approved_by, id]))
            mysql.get_db().commit()       
            rowcount = cur.rowcount
            if rowcount:   
                
                #Create model stock account
                accountName = model_name
                type_Id = 2 #Inventory account type
                categoryId = 5 #goods category 
                sub_category = 0
                mainaccount = 0
                openingBalance = 0     
                notes = ''
                owner_id = id
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
            
                stock_account_res = Accounting().create_new_account(account) 
                # api_response = Accounting().create_new_account(request_data) 
                
                
                #Create model cost of goods sold account
                accountName = model_name
                type_Id = 21 #Cost of goods sold account type
                categoryId = 24 #Cost of good sold category 
                sub_category = 0
                mainaccount = 0
                openingBalance = 0     
                notes = ''
                owner_id = id
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
            
                cog_account_res = Accounting().create_new_account(account)
                
                #Create model discount expense account
                accountName = model_name
                type_Id = 19 #Discount expense account type
                categoryId = 23 #Discount expense account category 
                sub_category = 0
                mainaccount = 0
                openingBalance = 0     
                notes = ''
                owner_id = id
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
            
                discount_account_res = Accounting().create_new_account(account)
                

                trans_message = {"description":"Mobile phone model was approved successfully!",
                                 "status":200}
                return jsonify(trans_message), 200
                
            else:
                message = {'status':500,
                           'description':'Mobile phone model was not found!'}
                return jsonify(message), 500
                    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a09',
                       'description':'Failed to approve phone model record. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message), 501  
        finally:
            cur.close()

     
   