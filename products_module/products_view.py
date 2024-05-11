from flask import request, Response, json, jsonify
from main import mysql, app
from resources.alphanumeric.generate import UniqueNumber
from resources.logs.logger import ErrorLogger
from resources.suppliers.suppliers import Supplier
from resources.inventory.inventory import Inventory
from resources.payload.payload import Localtime

class Products():
          
    def create_phone_model(self, user):
        #Get the request data 
        request_data = request.get_json()       
        
        validated_data = request_data
        # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
        # if error_messages:
        #     return jsonify({"error": error_messages}), 400
        
        product_sub_category_id = validated_data["product_sub_category_id"]
        name = validated_data["phone_name"]
        ram = validated_data["ram"]
        internal_storage = validated_data["internal_storage"]
        main_camera = validated_data["main_camera"]
        front_camera = validated_data["front_camera"]
        display = validated_data["display"]
        processor = validated_data["processor"]
        operating_system = validated_data["operating_system"]
        connectivity = validated_data["connectivity"]
        colors = validated_data["colors"]
        battery = validated_data["battery"]
        image_path = validated_data["image_path"]
        
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
            date_created = Localtime().gettime()
            created_by = user['id']

            #store supplier details request
            cur.execute("""INSERT INTO product_mobile_phones_models (product_sub_category_id, name, ram, internal_storage, main_camera, front_camera, display, processor, operating_system, connectivity, colors, battery, image_path, date_created, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                                    (product_sub_category_id, name, ram, internal_storage, main_camera, front_camera, display, processor, operating_system, connectivity, colors, battery, image_path, date_created, created_by, status))
            mysql.get_db().commit()
            cur.close()
            
            message = {"description":"Mobile phone model was created successfully",
                       "status":200}
            return message
                        

        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a02',
                       'description':'Failed to create a mobile phone model. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
  
    def list_phone_models(self, user):
        
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
            id = request_data["id"]
        
            
            cur.execute("""SELECT id, product_sub_category_id, name, ram, internal_storage, main_camera, front_camera, display, processor, operating_system, connectivity, colors, battery, image_path, date_created, created_by FROM product_mobile_phones_models WHERE status = %s """, (id))
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
        
    def get_phone_model_details(self, user):
        
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
            
    def approve_phone_model(self, user):
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
            cur.execute("""SELECT name, created_by FROM product_mobile_phones_models WHERE status =2 AND id = %s""", [id])
            phonemodel = cur.fetchone()
            if phonemodel:
                model_name = phonemodel["name"]
                created_by = phonemodel["created_by"]
                
            #update phone model status
            cur.execute("""UPDATE product_mobile_phones_models set status=1, date_approved = %s, approved_by = %s WHERE id = %s """, ([dateapproved, approved_by, id]))
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
            
                stock_account_res = Account().create_new_account(account)  
                
                
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
            
                cog_account_res = Account().create_new_account(account)
                

                trans_message = {"description":"Mobile phone model was approved successfully!",
                                "status":200}
                return trans_message 
                
            else:
                message = {'status':500,
                            'error':'sp_a20',
                            'description':'Mobile phone model was not approved!'}
                ErrorLogger().logError(message)
                return jsonify(message)
                    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a09',
                       'description':'Failed to approve phone model record. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()

     
   