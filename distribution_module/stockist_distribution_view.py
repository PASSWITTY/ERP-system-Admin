from flask import request, Response, json, jsonify
from main import mysql, app
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime

class StockistDistribution():
          
    def list_available_stock_to_dispatch(self, user):
        
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
            stock_state = request_data["stock_state"]
            cur.execute("""SELECT id, global_id, products_in_transit_id, distribution_center_id, model_id, imei_1, imei_2, qr_code_id, warranty_period, received_date, stock_state, remarks, created_date, created_by FROM mobile_phones_transit_stock_received WHERE stock_state = %s AND status = %s """, (stock_state, status))
            products_received = cur.fetchall()            
            if products_received:
                response_array = []
                
                for transit in products_received:
                    
                    created_by_id = transit["created_by"]
                    model_id = transit["model_id"]
                    distribution_center_id = transit["distribution_center_id"]
                    
                    cur.execute("""SELECT id, first_name, last_name FROM user_details WHERE user_id = %s """, (created_by_id))
                    user_details = cur.fetchone()
                    if user_details:
                        first_name = user_details['first_name']
                        last_name = user_details['last_name']
                        user_name = first_name + '' + last_name
                    else:
                        user_name = ''
                        
                    #fetch distribution center details
                    cur.execute("""SELECT name FROM distribution_centers WHERE id = %s """, (distribution_center_id))
                    user_details = cur.fetchone()            
                    if user_details:
                        distribution_center_name = user_details["name"]
                       
                    else:
                        distribution_center_name = ''
                        message = {"description":"Failed to fetch distribution center details!",
                                "status":201}
                        return message
                        
                    cur.execute("""SELECT id, name, ram, internal_storage, main_camera, front_camera, processor, display FROM product_mobile_phones_models WHERE id = %s """, (model_id))
                    phone_modeldetails = cur.fetchone()
                    if phone_modeldetails:
                            
                        model_name = phone_modeldetails['name']
                        ram = phone_modeldetails['ram']
                        internal_storage = phone_modeldetails['internal_storage']
                        main_camera = phone_modeldetails['main_camera']
                        front_camera = phone_modeldetails['front_camera']
                        display = phone_modeldetails['display']
                        processor = phone_modeldetails['processor']
                    else:
                        model_name = ''
                        
                    global_id = transit["global_id"]
                    products_in_transit_id = transit["products_in_transit_id"] 
                    distribution_center_id = transit["distribution_center_id"] 
                    model_id = transit["model_id"]
                    imei_1 = transit["imei_1"]
                    imei_2 = transit["imei_2"]
                    qr_code_id = transit["qr_code_id"]
                    warranty_period = transit["warranty_period"]
                    received_date = transit["received_date"]
                    remarks = transit["remarks"]
                    created_date = transit["created_date"]
                    created_by_id = created_by_id
                    
                    stock_state = transit["stock_state"]
                    if int(stock_state) ==1:
                        this_stock_state = "Available"
                    else:
                        this_stock_state = "Dispatched" 
                                        
                    response = {
                        
                        "id": transit['id'],
                        "global_id": global_id,
                        "products_in_transit_id": products_in_transit_id,
                        "distribution_center_id": distribution_center_id,
                        "model_id": model_id,
                        "imei_1": imei_1,
                        "imei_2": imei_2,
                        "model_name":model_name,
                        "ram":ram,
                        "internal_storage":internal_storage,
                        "main_camera":main_camera,
                        "front_camera":front_camera,
                        "display":display,
                        "processor":processor,
                        "qr_code_id": qr_code_id,
                        "warranty_period":warranty_period,
                        "distribution_center_name":distribution_center_name,
                        "received_date":received_date,
                        "remarks": remarks,
                        "state":this_stock_state,
                        "created_date": created_date,
                        "created_by_id": created_by_id,
                        "user_name":user_name
                        
                    }
                    response_array.append(response)
            
            
                message = {'status':200,
                            'response':response_array, 
                            'description':'Products available were fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'Failed to fetch products available records !'
                        }   
                return jsonify(message), 201  
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve products available from database.' + format(error)}
            ErrorLogger().logError(message),
            return jsonify(message), 501  
        finally:
            cur.close()
            
    def create_manager_dispatch(self, user):
        #Get the request data 
        request_data = request.get_json()       
        
        validated_data = request_data
        # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
        # if error_messages:
        #     return jsonify({"error": error_messages}), 400
        
        mobilephone_stock_received_id = validated_data["mobilephone_stock_received_id"]
        distribution_center_id = validated_data["distribution_center_id"]
        manager_id = validated_data["manager_id"]
        stockist_dispatch_date = validated_data["stockist_dispatch_date"]
        stockist_remarks = validated_data["stockist_remarks"]
        
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
            #fetch received stock details
            stock_state = 1 #1 means stock is available. 2 means stock was dispatched
            cur.execute("""SELECT global_id FROM mobile_phones_transit_stock_received WHERE stock_state = %s AND id = %s """, (stock_state, mobilephone_stock_received_id))
            purchased = cur.fetchone()            
            if purchased:
                global_id = purchased["global_id"]
            else:
                message = {"description":"Global id not fetched for mobile phones stock received",
                           "status":201}
                return message
           
            stock_state = 0 #'pending receive'
            status = 2 #pending approval
            created_date = Localtime().gettime()
            created_by = user['id']

            #store supplier details request
            cur.execute("""INSERT INTO mobile_phones_manager_stock (mobilephone_stock_received_id, global_id, distribution_center_id, manager_id, stockist_dispatch_date, stock_state, stockist_remarks, created_date, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                                   (mobilephone_stock_received_id, global_id, distribution_center_id, manager_id, stockist_dispatch_date, stock_state, stockist_remarks, created_date, created_by, status))
            mysql.get_db().commit()
            cur.close()
            
            message = {"description":"Mobile phone was dispatched to manager successfully",
                       "status":200}
            return message

        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a02',
                       'description':'Failed to dispatched mobile phone to manager. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()
          
    def list_manager_dispatched_stock(self, user):
        
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
        
            payload = []
            cur.execute("""SELECT id, mobilephone_stock_received_id, global_id, distribution_center_id, manager_id, manager_received_date, stockist_dispatch_date, stock_state, stockist_remarks, created_date, created_by FROM mobile_phones_manager_stock WHERE status = %s """, (status))
            phone_devices = cur.fetchall()            
            if phone_devices:
                for phone_device in phone_devices:
                
                    manager_id = phone_device['manager_id']
                    distribution_center_id = phone_device['distribution_center_id']
                    mobilephone_stock_received_id = phone_device['mobilephone_stock_received_id']
                    stockist_remarks = phone_device['stockist_remarks']
                    created_by = phone_device['created_by']
                    stock_state = int(phone_device['stock_state'])
                    if stock_state == 0:
                        stock_status = "Not Received"
                    elif stock_state == 1:
                        stock_status = "Received Not Dispatched"
                    
                    elif stock_state == 2:
                        stock_status = "Received and Dispatched"
                    else:
                        stock_status = ""
                    
                    #fetch stock received details
                    cur.execute("""SELECT model_id, imei_1, imei_2, qr_code_id, warranty_period FROM mobile_phones_transit_stock_received WHERE id = %s """, (mobilephone_stock_received_id))
                    stock_details = cur.fetchone()            
                    if stock_details:
                        model_id = stock_details["model_id"]
                        imei_1 = stock_details["imei_1"]
                        imei_2 = stock_details["imei_2"]
                        qr_code_id = stock_details["qr_code_id"]
                        warranty_period = stock_details["warranty_period"]
                        
                    else:
                        model_id = ''
                        imei_1 = ''
                        imei_2 = ''
                        qr_code_id = ''
                        message = {"description":"Failed to mobile phone model details!",
                                    "status":201}
                        return message
                    
                    #fetch model details 
                    cur.execute("""SELECT name, ram, internal_storage, main_camera, front_camera, display, processor FROM product_mobile_phones_models WHERE id = %s """, (model_id))
                    model_details = cur.fetchone()            
                    if model_details:
                        ram = model_details["ram"]
                        model_name = model_details["name"]
                        internal_storage = model_details["internal_storage"]
                        main_camera = model_details["main_camera"]
                        front_camera = model_details["front_camera"]
                        display = model_details["display"]
                        processor = model_details["processor"]
                    else:
                        ram = ''
                        
                        
                    #fetch manager details
                    cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s """, (manager_id))
                    user_details = cur.fetchone()            
                    if user_details:
                        first_name = user_details["first_name"]
                        last_name = user_details["last_name"]
                        manager_name = str(first_name) + ' ' + str(last_name)
                    else:
                        manager_name = ''
                        message = {"description":"Failed to fetch manager details!",
                                "status":201}
                        return message
                    
                    #fetch stockist details
                    cur.execute("""SELECT first_name, last_name FROM user_details WHERE created_by = %s """, (created_by))
                    stockist_details = cur.fetchone()            
                    if stockist_details:
                        first_name = stockist_details["first_name"]
                        last_name = stockist_details["last_name"]
                        stockist_name = str(first_name) + ' ' + str(last_name)
                    
                        #fetch distribution center details
                    cur.execute("""SELECT name FROM distribution_centers WHERE id = %s """, (distribution_center_id))
                    distribution_center_details = cur.fetchone()            
                    if distribution_center_details:
                        distribution_center_name = distribution_center_details["name"]
                        
                    else:
                        distribution_center_name = ''
                        message = {"description":"Failed to fetch distribution center details!",
                                "status":201}
                        return message
                
                    response = {
                        "id": phone_device['id'],
                        "mobilephone_stock_received_id": mobilephone_stock_received_id,
                        "global_id": phone_device['global_id'],
                        "distribution_center_id": distribution_center_id,
                        "distribution_center_name":distribution_center_name,
                        "model_id":model_id,
                        "model_name":model_name,
                        "imei_1":imei_1,
                        "imei_2":imei_2,
                        "qr_code_id":qr_code_id,
                        "warranty_period":warranty_period,
                        "ram":ram,
                        "internal_storage":internal_storage,
                        "main_camera":main_camera,
                        "front_camera":front_camera,
                        "display":display,
                        "processor":processor,
                        "manager_id": phone_device['manager_id'],
                        "manager_name":manager_name,
                        "stockist_remarks":stockist_remarks,
                        "manager_received_date": phone_device['manager_received_date'],
                        "stockist_dispatch_date": phone_device['stockist_dispatch_date'],
                        "stock_state": stock_state,
                        "stock_status": stock_status,
                        "created_date": phone_device['created_date'],
                        "created_by_id": phone_device['created_by'],
                        "stockist_name":stockist_name
                    }
                    payload.append(response)
                message = {'status':200,
                           'response':payload, 
                           'description':'Mobile phones dispatched to manager were fetched successfully!'
                        }   
                return jsonify(message), 200
        
            else:                
                message = {'status':404,
                            'error':'sp_a04',
                            'description':'Failed to fetch mobile phones dispatched to manager!'
                        }   
                return jsonify(message), 404             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve mobile phone dispatched to manager record from database.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message) 
        finally:
            cur.close()
       
    def approve_manager_dispatched_stock(self, user):
        request_data = request.get_json() 
               
        if request_data == None:
            message = {'status':402,
                       'error':'sp_a06',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message)

        id = request_data["id"]

        approved_by = user["id"]
        created_date = Localtime().gettime()
        
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a07',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)

        try:  
            
            cur.execute("""SELECT mobilephone_stock_received_id FROM mobile_phones_manager_stock WHERE status = 2 AND id = %s""", [id])
            stockreceived = cur.fetchone()
            if stockreceived:
                mobilephone_stock_received_id = stockreceived["mobilephone_stock_received_id"]
                
            else:
                trans_message = {"description":"Manager dispatch record was not found!",
                                  "status":404}
                return jsonify(trans_message), 404 
         
            #update mobile phone device stock state to 2 to mean it has been dispatched by stockist
            cur.execute("""UPDATE mobile_phones_transit_stock_received set stock_state = 2 WHERE id = %s """, ([mobilephone_stock_received_id]))
            mysql.get_db().commit()       
            rowcount = cur.rowcount
            if rowcount:   
                status = 1
                
                cur.execute("""UPDATE mobile_phones_manager_stock set approved_date = %s, approved_by =%s, status = %s WHERE status = 2 AND id = %s """, (created_date, approved_by, status, id))
                mysql.get_db().commit() 
                rowcount = cur.rowcount
                if rowcount:
                    trans_message = {"description":"Mobile phone dispatch to manager was approved successfully!",
                                     "status":200}
                    return trans_message 
                else:
                    trans_message = {"description":"Mobile phone dispatch record was not found!",
                                     "status":404}
                    return trans_message
                    
            else:
                message = {'status':500,
                            'error':'sp_a20',
                            'description':'Failed to approve mobile phone dispatch to manager!'}
                ErrorLogger().logError(message)
                return jsonify(message)
                    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a09',
                       'description':'Failed to approve mobile phone dispatch to manager!. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()
            
    # def manager_received_dispatched_stock(self, user):
    #     #Get the request data 
    #     request_data = request.get_json()       
        
    #     validated_data = request_data
    #     # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
    #     # if error_messages:
    #     #     return jsonify({"error": error_messages}), 400
        
    #     manager_remarks = validated_data["manager_remarks"]
    #     id = validated_data["id"]
    #     manager_received_date = request_data["manager_received_date"]
        
    #     # Open A connection to the database
    #     try:
    #         cur =  mysql.get_db().cursor()
    #     except:
    #         message = {'status':500,
    #                    'error':'sp_a11',
    #                    'description':"Couldn't connect to the Database!"}
    #         ErrorLogger().logError(message)
    #         return message
    #     #Save data to the database
        
    #     try:
    #         stock_state = 1 #'stock received and is available'
            
    #         created_date = Localtime().gettime()
    #         created_by = user['id']

    #         #store manager received stock details
            
    #         cur.execute("""UPDATE mobile_phones_manager_stock set manager_remarks = %s, manager_received_date =%s, stock_state = %s, update_date = %s, updated_by = %s WHERE stock_state = 0 AND id = %s """, (manager_remarks, manager_received_date, stock_state, created_date, created_by, id))
    #         mysql.get_db().commit()
    #         rowcount = cur.rowcount
    #         if rowcount:
    #             message = {"description":"Mobile phone was received by manager successfully",
    #                         "status":200}
    #             return message
    #         else:
    #             message = {"description":"Mobile phone record was not found!",
    #                         "status":404}
    #             return message

    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501, 
    #                    'error':'sp_a02',
    #                    'description':'Manager failed to receive mobile phone!. Error description ' + format(error)}
    #         ErrorLogger().logError(message)
    #         return jsonify(message) 
    #     finally:
    #         cur.close()

     
   