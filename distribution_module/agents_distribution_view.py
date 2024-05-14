from flask import request, Response, json, jsonify
from main import mysql, app
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime

class AgentsDistribution():
          
    def dispatch_stock(self, user):
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
            purchased = cur.fetchone()            
            if purchased:
                global_id = purchased["global_id"]
            else:
                message = {"description":"Global id not fetched from teamleaders stock received",
                           "status":201}
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
            
            message = {"description":"Mobile phone was dispatched to agent successfully",
                       "status":200}
            return message
                        

        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a02',
                       'description':'Failed to dispatched mobile phone to agent. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message) 
  
    def list_dispatched_stock(self, user):
        
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
        
            cur.execute("""SELECT id, mobilephone_teamleaderstock_id, global_id, distribution_center_id, agent_id, agent_received_date, teamleader_dispatch_date, stock_state, agent_remarks, teamleader_remarks, created_date, created_by FROM mobile_phones_agents_stock WHERE status = %s """, (status))
            phone_devices = cur.fetchall()            
            if phone_devices:
                mobile_phones = []
                
                for phone_device in phone_devices:
                    agent_id = phone_device['agent_id']
                    distribution_center_id = phone_device['distribution_center_id']
                    mobilephone_teamleaderstock_id = phone_device['mobilephone_teamleaderstock_id']
                    teamleader_remarks = phone_device['teamleader_remarks']
                    agent_remarks = phone_device['agent_remarks']
                    agent_received_date = phone_device['agent_received_date']
                    teamleader_dispatch_date = phone_device['teamleader_dispatch_date']
                    stock_state = phone_device['stock_state'],
                    created_date = phone_device['created_date']
                    created_by = phone_device['created_by']
                                        
                    #get stock received id from team leaders stocks
                    cur.execute("""SELECT mobilephone_managerstock_id FROM mobile_phones_teamleader_stock WHERE id = %s """, (mobilephone_teamleaderstock_id))
                    stockreceived = cur.fetchone() 
                    if stockreceived:
                        mobilephone_managerstock_id = stockreceived["mobilephone_managerstock_id"]
                    else:
                        mobilephone_managerstock_id = 0
                        message = {"description":"Failed to fetch teamleader stock received id from team leader stock details!",
                                   "status":201}
                        return message
                    
                    #get stock received id from managers stocks
                    cur.execute("""SELECT mobilephone_stock_received_id FROM mobile_phones_manager_stock WHERE id = %s """, (mobilephone_managerstock_id))
                    stockreceived = cur.fetchone() 
                    if stockreceived:
                        mobilephone_stock_received_id = stockreceived["mobilephone_stock_received_id"]
                    else:
                        mobilephone_stock_received_id = 0
                        message = {"description":"Failed to fetch stock received id from managers stock details!",
                                   "status":201}
                        return message
                    
                    #fetch stock received details
                    cur.execute("""SELECT model_id, imei_1, imei_2 FROM mobile_phones_transit_stock_received WHERE id = %s """, (mobilephone_stock_received_id))
                    user_details = cur.fetchone()            
                    if user_details:
                        model_id = user_details["model_id"]
                        imei_1 = user_details["imei_1"]
                        imei_2 = user_details["imei_2"]
                    else:
                        model_id = ''
                        imei_1 = ''
                        imei_2 = ''
                        message = {"description":"Failed to mobile phone model details!",
                                   "status":201}
                        return message
                    
                    #fetch manager details
                    cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s """, (agent_id))
                    user_details = cur.fetchone()            
                    if user_details:
                        first_name = user_details["first_name"]
                        last_name = user_details["last_name"]
                        agent_name = str(first_name) + ' ' + str(last_name)
                    else:
                        agent_name = ''
                        message = {"description":"Failed to fetch team leader details!",
                                "status":201}
                        return message
                    
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
                    
                    response = {
                        "id": phone_device['id'],
                        "mobilephone_teamleaderstock_id": mobilephone_teamleaderstock_id,
                        "global_id": phone_device['global_id'],
                        "distribution_center_id": distribution_center_id,
                        "distribution_center_name":distribution_center_name,
                        "model_id":model_id,
                        "imei_1":imei_1,
                        "imei_2":imei_2,
                        "agent_id": phone_device['agent_id'],
                        "agent_name":agent_name,
                        "teamleader_remarks":teamleader_remarks,
                        "agent_remarks":agent_remarks,
                        "agent_received_date": agent_received_date,
                        "teamleader_dispatch_date": teamleader_dispatch_date,
                        "stock_state": stock_state,
                        "created_date": created_date,
                        "created_by_id": created_by
                    }
                    mobile_phones.append(response)
            
                message = {'status':200,
                            'response':mobile_phones, 
                            'description':'Mobile phone dispatched to agent was fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'Failed to fetch mobile phone dispatched to agent!'
                        }   
                return jsonify(message), 201             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve mobile phone dispatched to agent record from database.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        
    def get_dispatched_stock_details(self, user):

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
        
            cur.execute("""SELECT id, mobilephone_teamleaderstock_id, global_id, distribution_center_id, agent_id, agent_received_date, teamleader_dispatch_date, stock_state, agent_remarks, teamleader_remarks, created_date, created_by FROM mobile_phones_agents_stock WHERE id = %s """, (id))
            phone_device = cur.fetchone()            
            if phone_device:
               
                    agent_id = phone_device['agent_id']
                    distribution_center_id = phone_device['distribution_center_id']
                    mobilephone_teamleaderstock_id = phone_device['mobilephone_teamleaderstock_id']
                    teamleader_remarks = phone_device['teamleader_remarks']
                    agent_remarks = phone_device['agent_remarks']
                    agent_received_date = phone_device['agent_received_date']
                    teamleader_dispatch_date = phone_device['teamleader_dispatch_date']
                    stock_state = phone_device['stock_state'],
                    created_date = phone_device['created_date']
                    created_by = phone_device['created_by']
                                        
                    #get stock received id from team leaders stocks
                    cur.execute("""SELECT mobilephone_managerstock_id FROM mobile_phones_teamleader_stock WHERE id = %s """, (mobilephone_teamleaderstock_id))
                    stockreceived = cur.fetchone() 
                    if stockreceived:
                        mobilephone_managerstock_id = stockreceived["mobilephone_managerstock_id"]
                    else:
                        mobilephone_managerstock_id = 0
                        message = {"description":"Failed to fetch teamleader stock received id from team leader stock details!",
                                   "status":201}
                        return message
                    
                    #get stock received id from managers stocks
                    cur.execute("""SELECT mobilephone_stock_received_id FROM mobile_phones_manager_stock WHERE id = %s """, (mobilephone_managerstock_id))
                    stockreceived = cur.fetchone() 
                    if stockreceived:
                        mobilephone_stock_received_id = stockreceived["mobilephone_stock_received_id"]
                    else:
                        mobilephone_stock_received_id = 0
                        message = {"description":"Failed to fetch stock received id from managers stock details!",
                                   "status":201}
                        return message
                    
                    #fetch stock received details
                    cur.execute("""SELECT model_id, imei_1, imei_2 FROM mobile_phones_transit_stock_received WHERE id = %s """, (mobilephone_stock_received_id))
                    user_details = cur.fetchone()            
                    if user_details:
                        model_id = user_details["model_id"]
                        imei_1 = user_details["imei_1"]
                        imei_2 = user_details["imei_2"]
                    else:
                        model_id = ''
                        imei_1 = ''
                        imei_2 = ''
                        message = {"description":"Failed to mobile phone model details!",
                                   "status":201}
                        return message
                    
                    #fetch manager details
                    cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s """, (agent_id))
                    user_details = cur.fetchone()            
                    if user_details:
                        first_name = user_details["first_name"]
                        last_name = user_details["last_name"]
                        agent_name = str(first_name) + ' ' + str(last_name)
                    else:
                        agent_name = ''
                        message = {"description":"Failed to fetch team leader details!",
                                "status":201}
                        return message
                    
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
                    
                    response = {
                        "id": phone_device['id'],
                        "mobilephone_teamleaderstock_id": mobilephone_teamleaderstock_id,
                        "global_id": phone_device['global_id'],
                        "distribution_center_id": distribution_center_id,
                        "distribution_center_name":distribution_center_name,
                        "model_id":model_id,
                        "imei_1":imei_1,
                        "imei_2":imei_2,
                        "agent_id": phone_device['agent_id'],
                        "agent_name":agent_name,
                        "teamleader_remarks":teamleader_remarks,
                        "agent_remarks":agent_remarks,
                        "agent_received_date": agent_received_date,
                        "teamleader_dispatch_date": teamleader_dispatch_date,
                        "stock_state": stock_state,
                        "created_date": created_date,
                        "created_by_id": created_by
                    }
                    
            
                    message = {'status':200,
                                'response':response, 
                                'description':'Mobile phone dispatched to agent was fetched successfully!'
                            }   
                    return jsonify(message), 200
            
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'Failed to fetch mobile phone dispatched to agent!'
                        }   
                return jsonify(message), 201             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve mobile phone dispatched to agent record from database.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message) 
       
    def approve_dispatched_stock(self, user):
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
            
            cur.execute("""SELECT mobilephone_teamleaderstock_id FROM mobile_phones_agents_stock WHERE id = %s""", [id])
            stockreceived = cur.fetchone()
            if stockreceived:
                mobilephone_teamleaderstock_id = stockreceived["mobilephone_teamleaderstock_id"]
                
            else:
                mobilephone_teamleaderstock_id = 0
         
            #update mobile phone device stock state to 2 to mean it has been dispatched by team leader to agents
            cur.execute("""UPDATE mobile_phones_teamleader_stock set stock_state = 2 WHERE id = %s """, ([mobilephone_teamleaderstock_id]))
            mysql.get_db().commit()       
            rowcount = cur.rowcount
            if rowcount:   
                status = 1
                
                cur.execute("""UPDATE mobile_phones_agents_stock set approved_date = %s, approved_by =%s, status = %s WHERE id = %s """, (created_date, approved_by, status, id))
                mysql.get_db().commit() 
                 
                trans_message = {"description":"Mobile phone dispatch to agent was approved successfully!",
                                 "status":200}
                return trans_message 
                
            else:
                message = {'status':500,
                            'error':'sp_a20',
                            'description':'Failed to approve mobile phone dispatch to agent!'}
                ErrorLogger().logError(message)
                return jsonify(message)
                    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a09',
                       'description':'Failed to approve mobile phone dispatch to agent!. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()

    def receive_dispatched_stock(self, user):
        #Get the request data 
        request_data = request.get_json()       
        
        validated_data = request_data
        # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
        # if error_messages:
        #     return jsonify({"error": error_messages}), 400
        
        id = validated_data["id"]
        agent_remarks = validated_data["agent_remarks"]
        agent_received_date = request_data["agent_received_date"]
        
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

            #store supplier details request
            
            cur.execute("""UPDATE mobile_phones_agents_stock set agent_remarks = %s, agent_received_date =%s, stock_state = %s, update_date = %s, updated_by = %s WHERE id = %s """, (agent_remarks, agent_received_date, stock_state, created_date, created_by, id))
            mysql.get_db().commit()
            cur.close()
            
            message = {"description":"Mobile phone was received by agent successfully",
                       "status":200}
            return message
                        

        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a02',
                       'description':'Agent failed to receive mobile phone!. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)
   