from flask import request, Response, json, jsonify
from main import mysql, app
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime

class TeamLeaderDistribution():
          
    def list_stock_to_receive(self, user):
        
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
            cur.execute("""SELECT id, global_id, mobilephone_managerstock_id, distribution_center_id, teamleader_id, manager_dispatch_date, teamleader_received_date, manager_remarks, teamleader_remarks, stock_state, created_date, created_by FROM mobile_phones_teamleader_stock WHERE stock_state = %s AND status = %s """, (stock_state, status))
            products_received = cur.fetchall()            
            if products_received:
                response_array = []
                
                for transit in products_received:
                    
                    global_id = transit["global_id"]
                    created_by_id = transit["created_by"]
                    teamleader_id = transit["teamleader_id"]
                    manager_dispatch_date = transit["manager_dispatch_date"]
                    teamleader_received_date = transit["teamleader_received_date"]
                    distribution_center_id = transit["distribution_center_id"]
                    manager_remarks = transit["manager_remarks"]
                    teamleader_remarks = transit["teamleader_remarks"]
                    mobilephone_managerstock_id = transit["mobilephone_managerstock_id"]
                    created_date = transit["created_date"]
                    
                    stock_state = transit["stock_state"]
                    if int(stock_state) ==0:
                        this_stock_state = "Not Received"
                        
                    elif int(stock_state) ==1:
                        this_stock_state = "Received Not Dispatched"
                        
                    elif int(stock_state) ==2:
                        this_stock_state = "Received and Dispatched"
                    else:
                        this_stock_state = ""
                    
                    #get manager stock details
                    cur.execute("""SELECT mobilephone_stock_received_id, manager_id FROM mobile_phones_manager_stock WHERE id = %s """, (mobilephone_managerstock_id))
                    model_details = cur.fetchone()            
                    if model_details:
                        mobilephone_stock_received_id = model_details["mobilephone_stock_received_id"]
                        manager_id = model_details["manager_id"]
                        
                    #get stock received details
                    cur.execute("""SELECT model_id, imei_1, imei_2, qr_code_id, warranty_period FROM mobile_phones_transit_stock_received WHERE id = %s """, (mobilephone_stock_received_id))
                    model_details = cur.fetchone()            
                    if model_details:
                        model_id = model_details["model_id"]
                        imei_1 = model_details["imei_1"]
                        imei_2 = model_details["imei_2"]
                        qr_code_id = model_details["qr_code_id"]
                        warranty_period = model_details["warranty_period"]
                    
                    cur.execute("""SELECT id, first_name, last_name FROM user_details WHERE user_id = %s """, (teamleader_id))
                    user_details = cur.fetchone()
                    if user_details:
                        first_name = user_details['first_name']
                        last_name = user_details['last_name']
                        user_name = first_name + '' + last_name
                    else:
                        user_name = ''
                        
                    cur.execute("""SELECT id, first_name, last_name FROM user_details WHERE user_id = %s """, (created_by_id))
                    manager_details = cur.fetchone()
                    if manager_details:
                        manager_first_name = manager_details['first_name']
                        manager_last_name = manager_details['last_name']
                        manager_user_name = manager_first_name + '' + manager_last_name
                    else:
                        manager_user_name = ''
                        
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
                                        
                    response = {
                        
                        "id": transit['id'],
                        "global_id": global_id,
                        "mobilephone_stock_received_id": mobilephone_stock_received_id,
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
                        "state":this_stock_state,
                        "created_date": created_date,
                        "created_by_id": created_by_id,
                        "teamleader_name":user_name,
                        "manager_user_name":manager_user_name,
                        "manager_id":manager_id,
                        "teamleader_id":teamleader_id,
                        "manager_dispatch_date":manager_dispatch_date,
                        "teamleader_received_date":teamleader_received_date,
                        "manager_remarks":manager_remarks,
                        "teamleader_remarks":teamleader_remarks
                        
                    }
                    response_array.append(response)
            
            
                message = {'status':200,
                            'response':response_array, 
                            'description':'Team leader stock to receive was fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':404,
                            'error':'sp_a04',
                            'description':'Failed to fetch Team leader stock to receive!'
                        }   
                return jsonify(message), 404  
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve Team leader stock to receive from database.' + format(error)}
            ErrorLogger().logError(message),
            return jsonify(message), 501  
        finally:
            cur.close()
    
    def list_stock_available(self, user):
        
        try:
            cur = mysql.get_db().cursor()
                    
        except:
            message = {'status':500,
                        'error':'sp_a14',
                        'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
                
        try:
            cur.execute("""SELECT id, global_id, mobilephone_managerstock_id, distribution_center_id, teamleader_id, manager_dispatch_date, teamleader_received_date, teamleader_remarks, manager_remarks, stock_state, created_date, created_by FROM mobile_phones_teamleader_stock WHERE stock_state = 1 AND status = 1 """)
            products_received = cur.fetchall()            
            if products_received:
                response_array = []
                
                for transit in products_received:
                    
                    global_id = transit["global_id"]
                    created_by_id = transit["created_by"]
                    teamleader_id = transit["teamleader_id"]
                    manager_dispatch_date = transit["manager_dispatch_date"]
                    teamleader_received_date = transit["teamleader_received_date"]
                    distribution_center_id = transit["distribution_center_id"]
                    teamleader_remarks = transit["teamleader_remarks"]
                    manager_remarks = transit["manager_remarks"]
                    mobilephone_managerstock_id = transit["mobilephone_managerstock_id"]
                    created_date = transit["created_date"]
                    
                    stock_state = transit["stock_state"]
                    if int(stock_state) ==0:
                        this_stock_state = "Not Received"
                        
                    elif int(stock_state) ==1:
                        this_stock_state = "Received Not Dispatched"
                        
                    elif int(stock_state) ==2:
                        this_stock_state = "Received and Dispatched"
                    else:
                        this_stock_state = ""
                        
                    #get manager stock details
                    cur.execute("""SELECT mobilephone_stock_received_id FROM mobile_phones_manager_stock WHERE id = %s """, (mobilephone_managerstock_id))
                    model_details = cur.fetchone()            
                    if model_details:
                        mobilephone_stock_received_id = model_details["mobilephone_stock_received_id"]
                    
                    #get stock received details
                    cur.execute("""SELECT model_id, imei_1, imei_2, qr_code_id, warranty_period FROM mobile_phones_transit_stock_received WHERE id = %s """, (mobilephone_stock_received_id))
                    model_details = cur.fetchone()            
                    if model_details:
                        model_id = model_details["model_id"]
                        imei_1 = model_details["imei_1"]
                        imei_2 = model_details["imei_2"]
                        qr_code_id = model_details["qr_code_id"]
                        warranty_period = model_details["warranty_period"]
                    
                    cur.execute("""SELECT id, first_name, last_name FROM user_details WHERE user_id = %s """, (created_by_id))
                    user_details = cur.fetchone()
                    if user_details:
                        first_name = user_details['first_name']
                        last_name = user_details['last_name']
                        manager_user_name = first_name + '' + last_name
                    else:
                        manager_user_name = ''
                        
                    cur.execute("""SELECT id, first_name, last_name FROM user_details WHERE user_id = %s """, (teamleader_id))
                    teamleader_details = cur.fetchone()
                    if teamleader_details:
                        teamleader_first_name = teamleader_details['first_name']
                        teamleader_last_name = teamleader_details['last_name']
                        teamleader_user_name = teamleader_first_name + '' + teamleader_last_name
                    else:
                        teamleader_user_name = ''
                        
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
                                        
                    response = {
                        
                        "id": transit['id'],
                        "global_id": global_id,
                        "mobilephone_stock_received_id": mobilephone_stock_received_id,
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
                        "state":this_stock_state,
                        "created_date": created_date,
                        "created_by_id": created_by_id,
                        "teamleader_user_name":teamleader_user_name,
                        "manager_user_name":manager_user_name,
                        "teamleader_id":teamleader_id,
                        "manager_dispatch_date":manager_dispatch_date,
                        "teamleader_received_date":teamleader_received_date,
                        "teamleader_remarks":teamleader_remarks,
                        "manager_remarks":manager_remarks
                        
                    }
                    response_array.append(response)
            
            
                message = {'status':200,
                            'response':response_array, 
                            'description':'Team leader stock available was fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':404,
                            'error':'sp_a04',
                            'description':'Failed to fetch Team leader available stock!'
                        }   
                return jsonify(message), 404  
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve Team leader stock available from database.' + format(error)}
            ErrorLogger().logError(message),
            return jsonify(message), 501  
        finally:
            cur.close()
            
    def teamleader_receive_dispatched_stock(self, user):
        #Get the request data 
        request_data = request.get_json()       
        
        validated_data = request_data
        # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
        # if error_messages:
        #     return jsonify({"error": error_messages}), 400
        
        teamleader_remarks = validated_data["teamleader_remarks"]
        id = validated_data["id"]
        teamleader_received_date = request_data["teamleader_received_date"]
        
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
            stock_state = 1 #'stock received and is available'
            
            created_date = Localtime().gettime()
            created_by = user['id']

            #store team leader received stock details
            
            cur.execute("""UPDATE mobile_phones_teamleader_stock set teamleader_remarks = %s, teamleader_received_date =%s, stock_state = %s, update_date = %s, updated_by = %s WHERE stock_state = 0 AND id = %s """, (teamleader_remarks, teamleader_received_date, stock_state, created_date, created_by, id))
            mysql.get_db().commit()
            rowcount = cur.rowcount
            if rowcount:
                message = {"description":"Mobile phone was received by Team leader successfully",
                            "status":200}
                return message
            else:
                message = {"description":"Mobile phone record was not found!",
                            "status":404}
                return message

        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a02',
                       'description':'Team leader failed to receive mobile phone!. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message) 
        finally:
            cur.close()
         
    def create_agent_dispatch(self, user):
        #Get the request data 
        request_data = request.get_json()       
        
        validated_data = request_data
        # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
        # if error_messages:
        #     return jsonify({"error": error_messages}), 400
        
        mobilephone_teamleaderstock_id = validated_data["mobilephone_teamleaderstock_id"]
        distribution_center_id = validated_data["distribution_center_id"]
        agent_id = validated_data["agent_id"]
        teamleader_dispatch_date = validated_data["teamleader_dispatch_date"]
        teamleader_remarks = validated_data["teamleader_remarks"]
        
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
            cur.execute("""SELECT global_id FROM mobile_phones_teamleader_stock WHERE id = %s """, (mobilephone_teamleaderstock_id))
            dispatch = cur.fetchone()            
            if dispatch:
                global_id = dispatch["global_id"]
            else:
                message = {"description":"Global id not fetched for team leader stock records",
                           "status":404}
                return message
           
            stock_state = 0 #'pending receive'
            status = 2 #pending approval
            created_date = Localtime().gettime()
            created_by = user['id']

            #store supplier details request
            cur.execute("""INSERT INTO mobile_phones_agents_stock (mobilephone_teamleaderstock_id, global_id, distribution_center_id, agent_id, teamleader_dispatch_date, stock_state, teamleader_remarks, created_date, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                                  (mobilephone_teamleaderstock_id, global_id, distribution_center_id, agent_id, teamleader_dispatch_date, stock_state, teamleader_remarks, created_date, created_by, status))
            mysql.get_db().commit()
            cur.close()
            
            message = {"description":"Mobile phone was dispatched to agents successfully",
                       "status":200}
            return message

        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a02',
                       'description':'Failed to dispatched mobile phone to agents. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()
  
    def list_agent_dispatched_stock(self, user):
        
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
        
            cur.execute("""SELECT id, mobilephone_teamleaderstock_id, global_id, distribution_center_id, agent_id, agent_received_date, teamleader_dispatch_date, stock_state, teamleader_remarks, created_date, created_by FROM mobile_phones_agents_stock WHERE status = %s """, (status))
            phone_devices = cur.fetchall()            
            if phone_devices:
                mobile_phones = []
                
                for phone_device in phone_devices:
                    agent_id = phone_device['agent_id']
                    created_by = phone_device['created_by']
                    distribution_center_id = phone_device['distribution_center_id']
                    mobilephone_teamleaderstock_id = phone_device['mobilephone_teamleaderstock_id']
                    teamleader_remarks = phone_device['teamleader_remarks']
                    agent_received_date = phone_device['agent_received_date']
                    teamleader_dispatch_date = phone_device['teamleader_dispatch_date']
                    stock_state = int(phone_device['stock_state'])
                    if stock_state == 0:
                        stock_status = "Not Received"
                    elif stock_state == 1:
                        stock_status = "Received Not Dispatched"
                    
                    elif stock_state == 2:
                        stock_status = "Received and Dispatched"
                    else:
                        stock_status = ""
                    
                    #fetch team leader stock details
                    cur.execute("""SELECT mobilephone_managerstock_id FROM mobile_phones_teamleader_stock WHERE id = %s """, (mobilephone_teamleaderstock_id))
                    teamleader_details = cur.fetchone()  
                    if teamleader_details:
                        mobilephone_managerstock_id = teamleader_details["mobilephone_managerstock_id"]
                        
                    #fetch manager stock details
                    cur.execute("""SELECT mobilephone_stock_received_id, manager_id FROM mobile_phones_manager_stock WHERE id = %s """, (mobilephone_managerstock_id))
                    manager_stock_details = cur.fetchone()  
                    if manager_stock_details:
                        mobilephone_stock_received_id = manager_stock_details["mobilephone_stock_received_id"]
                        manager_id = manager_stock_details["manager_id"]
                        
                                        
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
                    cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s """, (agent_id))
                    agent_details = cur.fetchone()            
                    if agent_details:
                        first_name = agent_details["first_name"]
                        last_name = agent_details["last_name"]
                        agent_name = str(first_name) + ' ' + str(last_name)
                    else:
                        agent_name = ''
                        message = {"description":"Failed to fetch agents details!",
                                "status":201}
                        return message
                    
                    #fetch agents details
                    cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s """, (created_by))
                    teamleader_details = cur.fetchone()            
                    if teamleader_details:
                        first_name = teamleader_details["first_name"]
                        last_name = teamleader_details["last_name"]
                        teamleader_name = str(first_name) + ' ' + str(last_name)
                    else:
                        teamleader_name = ''
                        message = {"description":"Failed to fetch agents details!",
                                "status":201}
                        return message
                    
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
                        "manager_id": manager_id,
                        "agent_id": agent_id,
                        "agent_name":agent_name,
                        "teamleader_name":teamleader_name,
                        "teamleader_remarks":teamleader_remarks,
                        "teamleader_dispatch_date": teamleader_dispatch_date,
                        "agent_received_date": agent_received_date,
                        "stock_state": stock_state,
                        "stock_status": stock_status,
                        "created_date": phone_device['created_date'],
                        "created_by_id": phone_device['created_by']
                    }
                    mobile_phones.append(response)
            
                message = {'status':200,
                            'response':mobile_phones, 
                            'description':'Mobile phone dispatched to agents was fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'Failed to fetch mobile phone dispatched to agents!'
                        }   
                return jsonify(message), 201             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve mobile phone dispatched to agents record from database.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message) 
        finally:
            cur.close() 
    
    def approve_agent_dispatched_stock(self, user):
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
            
            cur.execute("""SELECT mobilephone_teamleaderstock_id FROM mobile_phones_agents_stock WHERE status = 2 AND id = %s""", [id])
            stockreceived = cur.fetchone()
            if stockreceived:
                mobilephone_teamleaderstock_id = stockreceived["mobilephone_teamleaderstock_id"]
                
            else:
                mobilephone_teamleaderstock_id = 0
         
            #update mobile phone device stock state to 2 to mean it has been dispatched by team leader to agents
            #stock_state = 2 means team leader has disbursed their stock to agents
            cur.execute("""UPDATE mobile_phones_teamleader_stock set stock_state = 2 WHERE id = %s """, ([mobilephone_teamleaderstock_id]))
            mysql.get_db().commit()       
            rowcount = cur.rowcount
            if rowcount:   
                status = 1
                
                cur.execute("""UPDATE mobile_phones_agents_stock set approved_date = %s, approved_by =%s, status = %s WHERE status =2 AND id = %s """, (created_date, approved_by, status, id))
                mysql.get_db().commit() 
                rowcount = cur.rowcount
                if rowcount:
                    trans_message = {"description":"Mobile phone dispatch to agents was approved successfully!",
                                     "status":200}
                    return trans_message 
                else:
                    trans_message = {"description":"Mobile phone dispatch record was not found!",
                                     "status":201}
                    return trans_message
                    
            else:
                message = {'status':500,
                            'error':'sp_a20',
                            'description':'Failed to approve mobile phone dispatch to agents!'}
                ErrorLogger().logError(message)
                return jsonify(message)
                    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a09',
                       'description':'Failed to approve mobile phone dispatch to agents!. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
    # def dispatch_stock(self, user):
    #     #Get the request data 
    #     request_data = request.get_json()       
        
    #     validated_data = request_data
    #     # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
    #     # if error_messages:
    #     #     return jsonify({"error": error_messages}), 400
        
    #     mobilephone_managerstock_id = validated_data["mobilephone_managerstock_id"]
    #     distribution_center_id = validated_data["distribution_center_id"]
    #     teamleader_id = validated_data["teamleader_id"]
    #     manager_dispatch_date = validated_data["manager_dispatch_date"]
    #     manager_remarks = validated_data["manager_remarks"]
        
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
    #         #fetch received stock details
    #         cur.execute("""SELECT global_id FROM mobile_phones_manager_stock WHERE id = %s """, (mobilephone_managerstock_id))
    #         purchased = cur.fetchone()            
    #         if purchased:
    #             global_id = purchased["global_id"]
    #         else:
    #             message = {"description":"Global id not fetched from managers stock received",
    #                        "status":201}
    #             return message
           
    #         stock_state = 0 #'pending receive'
    #         status = 2 #pending approval
    #         created_date = Localtime().gettime()
    #         created_by = user['id']

    #         #store supplier details request
    #         cur.execute("""INSERT INTO mobile_phones_teamleader_stock (mobilephone_managerstock_id, global_id, distribution_center_id, teamleader_id, manager_dispatch_date, stock_state, manager_remarks, created_date, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
    #                                                                   (mobilephone_managerstock_id, global_id, distribution_center_id, teamleader_id, manager_dispatch_date, stock_state, manager_remarks, created_date, created_by, status))
    #         mysql.get_db().commit()
    #         cur.close()
            
    #         message = {"description":"Mobile phone was dispatched to team leader successfully",
    #                    "status":200}
    #         return message
                        

    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501, 
    #                    'error':'sp_a02',
    #                    'description':'Failed to dispatched mobile phone to team leader. Error description ' + format(error)}
    #         ErrorLogger().logError(message)
    #         return jsonify(message) 
  
    # def list_dispatched_stock(self, user):
        
    #     request_data = request.get_json() 
        
    #     if request_data == None:
    #         message = {'status':402,
    #                    'error':'sp_a03',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)
       
    #     try:
    #         cur = mysql.get_db().cursor()
                    
    #     except:
    #         message = {'status':500,
    #                     'error':'sp_a14',
    #                     'description':"Couldn't connect to the Database!"}
    #         ErrorLogger().logError(message)
    #         return message
                
    #     try:
    #         status = request_data["status"]
        
    #         cur.execute("""SELECT id, mobilephone_managerstock_id, global_id, distribution_center_id, teamleader_id, teamleader_received_date, manager_dispatch_date, stock_state, manager_remarks, created_date, created_by FROM mobile_phones_teamleader_stock WHERE status = %s """, (status))
    #         phone_devices = cur.fetchall()            
    #         if phone_devices:
    #             mobile_phones = []
                
    #             for phone_device in phone_devices:
    #                 teamleader_id = phone_device['teamleader_id']
    #                 distribution_center_id = phone_device['distribution_center_id']
    #                 mobilephone_managerstock_id = phone_device['mobilephone_managerstock_id']
    #                 manager_remarks = phone_device['manager_remarks']
                                        
    #                 #get stock received id from managers stocks
    #                 cur.execute("""SELECT mobilephone_stock_received_id FROM mobile_phones_manager_stock WHERE id = %s """, (mobilephone_managerstock_id))
    #                 stockreceived = cur.fetchone() 
    #                 if stockreceived:
    #                     mobilephone_stock_received_id = stockreceived["mobilephone_stock_received_id"]
    #                 else:
    #                     message = {"description":"Failed to fetch stock received id from managers stock details!",
    #                                "status":201}
    #                     return message
                        
    #                 #fetch stock received details
    #                 cur.execute("""SELECT model_id, imei_1, imei_2 FROM mobile_phones_transit_stock_received WHERE id = %s """, (mobilephone_stock_received_id))
    #                 user_details = cur.fetchone()            
    #                 if user_details:
    #                     model_id = user_details["model_id"]
    #                     imei_1 = user_details["imei_1"]
    #                     imei_2 = user_details["imei_2"]
    #                 else:
    #                     model_id = ''
    #                     imei_1 = ''
    #                     imei_2 = ''
    #                     message = {"description":"Failed to mobile phone model details!",
    #                                "status":201}
    #                     return message
                    
    #                 #fetch manager details
    #                 cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s """, (teamleader_id))
    #                 user_details = cur.fetchone()            
    #                 if user_details:
    #                     first_name = user_details["first_name"]
    #                     last_name = user_details["last_name"]
    #                     teamleader_name = str(first_name) + ' ' + str(last_name)
    #                 else:
    #                     teamleader_name = ''
    #                     message = {"description":"Failed to fetch team leader details!",
    #                             "status":201}
    #                     return message
                    
    #                  #fetch distribution center details
    #                 cur.execute("""SELECT name FROM distribution_centers WHERE id = %s """, (distribution_center_id))
    #                 user_details = cur.fetchone()            
    #                 if user_details:
    #                     distribution_center_name = user_details["name"]
                       
    #                 else:
    #                     distribution_center_name = ''
    #                     message = {"description":"Failed to fetch distribution center details!",
    #                             "status":201}
    #                     return message
                    
    #                 response = {
    #                     "id": phone_device['id'],
    #                     "mobilephone_managerstock_id": mobilephone_managerstock_id,
    #                     "global_id": phone_device['global_id'],
    #                     "distribution_center_id": distribution_center_id,
    #                     "distribution_center_name":distribution_center_name,
    #                     "model_id":model_id,
    #                     "imei_1":imei_1,
    #                     "imei_2":imei_2,
    #                     "teamleader_id": phone_device['teamleader_id'],
    #                     "teamleader_name":teamleader_name,
    #                     "manager_remarks":manager_remarks,
    #                     "teamleader_received_date": phone_device['teamleader_received_date'],
    #                     "manager_dispatch_date": phone_device['manager_dispatch_date'],
    #                     "stock_state": phone_device['stock_state'],
    #                     "created_date": phone_device['created_date'],
    #                     "created_by_id": phone_device['created_by']
    #                 }
    #                 mobile_phones.append(response)
            
    #             message = {'status':200,
    #                         'response':mobile_phones, 
    #                         'description':'Mobile phone dispatched to team leader was fetched successfully!'
    #                     }   
    #             return jsonify(message), 200
            
    #         else:                
    #             message = {'status':201,
    #                         'error':'sp_a04',
    #                         'description':'Failed to fetch mobile phone dispatched to team leaders!'
    #                     }   
    #             return jsonify(message), 201             
             
            
    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'error':'sp_a05',
    #                    'description':'Failed to retrieve mobile phone dispatched to team leader record from database.' + format(error)}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)  
        
    # def get_dispatched_stock_details(self, user):

    #     request_data = request.get_json() 
        
    #     if request_data == None:
    #         message = {'status':402,
    #                    'error':'sp_a03',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)
       
    #     try:
    #         cur = mysql.get_db().cursor()
                    
    #     except:
    #         message = {'status':500,
    #                     'error':'sp_a14',
    #                     'description':"Couldn't connect to the Database!"}
    #         ErrorLogger().logError(message)
    #         return message
                
    #     try:
    #         id = request_data["id"]
        
    #         cur.execute("""SELECT id, mobilephone_managerstock_id, global_id, distribution_center_id, teamleader_id, teamleader_received_date, manager_dispatch_date, stock_state, manager_remarks, created_date, created_by FROM mobile_phones_teamleader_stock WHERE id = %s """, (id))
    #         phone_device = cur.fetchone()            
    #         if phone_device:
               
    #                 teamleader_id = phone_device['teamleader_id']
    #                 distribution_center_id = phone_device['distribution_center_id']
    #                 mobilephone_managerstock_id = phone_device['mobilephone_managerstock_id']
    #                 manager_remarks = phone_device['manager_remarks']
                                        
    #                 #get stock received id from managers stocks
    #                 cur.execute("""SELECT mobilephone_stock_received_id FROM mobile_phones_manager_stock WHERE id = %s """, (mobilephone_managerstock_id))
    #                 stockreceived = cur.fetchone() 
    #                 if stockreceived:
    #                     mobilephone_stock_received_id = stockreceived["mobilephone_stock_received_id"]
    #                 else:
    #                     message = {"description":"Failed to fetch stock received id from managers stock details!",
    #                                "status":201}
    #                     return message
                        
    #                 #fetch stock received details
    #                 cur.execute("""SELECT model_id, imei_1, imei_2 FROM mobile_phones_transit_stock_received WHERE id = %s """, (mobilephone_stock_received_id))
    #                 user_details = cur.fetchone()            
    #                 if user_details:
    #                     model_id = user_details["model_id"]
    #                     imei_1 = user_details["imei_1"]
    #                     imei_2 = user_details["imei_2"]
    #                 else:
    #                     model_id = ''
    #                     imei_1 = ''
    #                     imei_2 = ''
    #                     message = {"description":"Failed to mobile phone model details!",
    #                                "status":201}
    #                     return message
                    
    #                 #fetch manager details
    #                 cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s """, (teamleader_id))
    #                 user_details = cur.fetchone()            
    #                 if user_details:
    #                     first_name = user_details["first_name"]
    #                     last_name = user_details["last_name"]
    #                     teamleader_name = str(first_name) + ' ' + str(last_name)
    #                 else:
    #                     teamleader_name = ''
    #                     message = {"description":"Failed to fetch team leader details!",
    #                             "status":201}
    #                     return message
                    
    #                  #fetch distribution center details
    #                 cur.execute("""SELECT name FROM distribution_centers WHERE id = %s """, (distribution_center_id))
    #                 user_details = cur.fetchone()            
    #                 if user_details:
    #                     distribution_center_name = user_details["name"]
                       
    #                 else:
    #                     distribution_center_name = ''
    #                     message = {"description":"Failed to fetch distribution center details!",
    #                             "status":201}
    #                     return message
                    
    #                 response = {
    #                     "id": phone_device['id'],
    #                     "mobilephone_managerstock_id": mobilephone_managerstock_id,
    #                     "global_id": phone_device['global_id'],
    #                     "distribution_center_id": distribution_center_id,
    #                     "distribution_center_name":distribution_center_name,
    #                     "model_id":model_id,
    #                     "imei_1":imei_1,
    #                     "imei_2":imei_2,
    #                     "teamleader_id": phone_device['teamleader_id'],
    #                     "teamleader_name":teamleader_name,
    #                     "manager_remarks":manager_remarks,
    #                     "teamleader_received_date": phone_device['teamleader_received_date'],
    #                     "manager_dispatch_date": phone_device['manager_dispatch_date'],
    #                     "stock_state": phone_device['stock_state'],
    #                     "created_date": phone_device['created_date'],
    #                     "created_by_id": phone_device['created_by']
    #                 }
                   
            
    #                 message = {'status':200,
    #                             'response':response, 
    #                             'description':'Mobile phone dispatched to team leader was fetched successfully!'
    #                         }   
    #                 return jsonify(message), 200
            
    #         else:                
    #             message = {'status':201,
    #                         'error':'sp_a04',
    #                         'description':'Failed to fetch mobile phone dispatched to team leader!'
    #                     }   
    #             return jsonify(message), 201             
             
            
    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'error':'sp_a05',
    #                    'description':'Failed to retrieve mobile phone dispatched to team leader record from database.' + format(error)}
    #         ErrorLogger().logError(message)
    #         return jsonify(message) 
       
    # def approve_dispatched_stock(self, user):
    #     request_data = request.get_json() 
               
    #     if request_data == None:
    #         message = {'status':402,
    #                    'error':'sp_a06',
    #                    'description':'Request data is missing some details!'}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)

    #     id = request_data["id"]

    #     approved_by = user["id"]
    #     created_date = Localtime().gettime()
        
    #     try:
    #         cur = mysql.get_db().cursor()
    #     except:
    #         message = {'status':500,
    #                    'error':'sp_a07',
    #                    'description':"Couldn't connect to the Database!"}
    #         ErrorLogger().logError(message)
    #         return jsonify(message)

    #     try:  
            
    #         cur.execute("""SELECT mobilephone_managerstock_id FROM mobile_phones_teamleader_stock WHERE id = %s""", [id])
    #         stockreceived = cur.fetchone()
    #         if stockreceived:
    #             mobilephone_managerstock_id = stockreceived["mobilephone_managerstock_id"]
                
    #         else:
    #             mobilephone_managerstock_id = 0
         
    #         status = 1 
    #         cur.execute("""UPDATE mobile_phones_teamleader_stock set approved_date = %s, approved_by =%s, status = %s WHERE status = 2 AND id = %s """, (created_date, approved_by, status, id))
    #         mysql.get_db().commit() 
    #         rowcount = cur.rowcount
    #         if rowcount:
    #             #update mobile phone device stock state to 2 to mean it has been dispatched by manager to team leader
    #             cur.execute("""UPDATE mobile_phones_manager_stock set stock_state = 2 WHERE id = %s """, ([mobilephone_managerstock_id]))
    #             mysql.get_db().commit()
        
    #             trans_message = {"description":"Mobile phone dispatch to team leader was approved successfully!",
    #                              "status":200}
    #             return jsonify(trans_message), 200 
    #         else:
    #             trans_message = {"description":"Mobile phone dispatch record was not found!",
    #                                 "status":404}
    #             return jsonify(trans_message), 404
                
    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'error':'sp_a09',
    #                    'description':'Failed to approve mobile phone dispatch to team leader!. Error description ' + format(error)}
    #         ErrorLogger().logError(message)
    #         return jsonify(message), 501
    #     finally:
    #         cur.close()
    
    # def receive_dispatched_stock(self, user):
    #     #Get the request data 
    #     request_data = request.get_json()       
        
    #     validated_data = request_data
    #     # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
    #     # if error_messages:
    #     #     return jsonify({"error": error_messages}), 400
        
    #     teamleader_remarks = validated_data["teamleader_remarks"]
    #     id = validated_data["id"]
    #     teamleader_received_date = request_data["teamleader_received_date"]
        
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

    #         #store team leader received stock details
            
    #         cur.execute("""UPDATE mobile_phones_teamleader_stock set teamleader_remarks = %s, teamleader_received_date =%s, stock_state = %s, update_date = %s, updated_by = %s WHERE stock_state = 0 AND id = %s """, (teamleader_remarks, teamleader_received_date, stock_state, created_date, created_by, id))
    #         mysql.get_db().commit()
    #         rowcount = cur.rowcount
    #         if rowcount:
            
    #             message = {"description":"Mobile phone was received by team leader successfully!",
    #                        "status":200}
    #             return message
    #         else:
    #             message = {"description":"Mobile phone record was not found!",
    #                        "status":404}
    #             return message

    #     #Error handling
    #     except Exception as error:
    #         message = {'status':501, 
    #                    'error':'sp_a02',
    #                    'description':'Team leader failed to receive mobile phone!. Error description ' + format(error)}
    #         ErrorLogger().logError(message)
    #         return jsonify(message) 


     
   