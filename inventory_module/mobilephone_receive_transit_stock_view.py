from flask import request, Response, json, jsonify
from main import mysql, app
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.transactions.bookkeeping import DebitCredit
import uuid

class ReceiveTransitStock():
          
    def receive_stock(self, user):
        #Get the request data 
        request_data = request.get_json()       
        
        validated_data = request_data
        # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
        # if error_messages:
        #     return jsonify({"error": error_messages}), 400
        
       
        products_in_transit_id = validated_data["products_in_transit_id"]
        distribution_center_id = validated_data["distribution_center_id"]
        model_id = validated_data["model_id"]
        imei_1 = validated_data["imei_1"] 
        imei_2 = validated_data["imei_2"] 
        qr_code_id = validated_data["qr_code_id"] 
        received_date = validated_data["received_date"]     
        remarks = validated_data["remarks"] 
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a11',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message, 500
        #Save data to the database
        
        try:
            stock_state = 1 #available at warehouse
            status = 2 #pending approval
            created_date = Localtime().gettime()
            created_by = user['id']
            
            #fetch stock on transit details
            cur.execute("""SELECT global_id FROM products_in_transit WHERE status =1 AND id = %s """, (products_in_transit_id))
            purchase = cur.fetchone()            
            if purchase:
                global_id = purchase["global_id"]
            else:
                message = {"description":"Global id not fetched for products in transit",
                           "status":201}
                return message
                
            #receive stock on transit
            cur.execute("""INSERT INTO mobile_phones_transit_stock_received (global_id, products_in_transit_id, distribution_center_id, model_id, imei_1, imei_2, qr_code_id, received_date, stock_state, remarks, created_date, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                                            (global_id, products_in_transit_id, distribution_center_id, model_id, imei_1, imei_2, qr_code_id, received_date, stock_state, remarks, created_date, created_by, status))
            mysql.get_db().commit()
            cur.close()
            
            message = {"description":"Transit stock was received successfully",
                       "status":200}
            return message
                        

        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a02',
                       'description':'Failed to receive transit stock. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message), 501  
  
    def list_received_stock(self, user):
        
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
            
            cur.execute("""SELECT id, global_id, products_in_transit_id, distribution_center_id, model_id, imei_1, imei_2, qr_code_id, received_date, stock_state, remarks, created_date, created_by FROM mobile_phones_transit_stock_received WHERE status = %s """, (status))
            products_received = cur.fetchall()            
            if products_received:
                response_array = []
                
                for transit in products_received:
                    global_id = transit["global_id"]
                    products_in_transit_id = transit["products_in_transit_id"] 
                    distribution_center_id = transit["distribution_center_id"] 
                    model_id = transit["model_id"]
                    imei_1 = transit["imei_1"]
                    imei_2 = transit["imei_2"]
                    qr_code_id = transit["qr_code_id"]
                    received_date = transit["received_date"]
                    remarks = transit["remarks"]
                    created_date = transit["created_date"]
                    created_by_id = transit["created_by"]
                    
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
                        "qr_code_id": qr_code_id,
                        "received_date":received_date,
                        "remarks": remarks,
                        "state":this_stock_state,
                        "created_date": created_date,
                        "created_by_id": created_by_id
                        
                    }
                    response_array.append(response)
            
            
                message = {'status':200,
                            'response':response_array, 
                            'description':'Products received were fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'Failed to fetch products received records !'
                        }   
                return jsonify(message), 201             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve products received from database.' + format(error)}
            ErrorLogger().logError(message),
            return jsonify(message), 501  
        
    def get_received_stock_details(self, user):
        
        request_data = request.get_json() 
        
        if request_data == None:
            message = {'status':402,
                       'error':'sp_a03',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message), 402
        
        id = request_data["id"]
        
        try:
            cur = mysql.get_db().cursor()
                    
        except:
            message = {'status':500,
                        'error':'sp_a14',
                        'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message, 500
                
        try:
            cur.execute("""SELECT global_id, products_in_transit_id, distribution_center_id, model_id, imei_1, imei_2, qr_code_id, received_date, stock_state, remarks, created_date, created_by FROM mobile_phones_transit_stock_received WHERE id = %s """, (id))
            product_received = cur.fetchone()            
            if product_received:
            
                global_id = product_received["global_id"]
                products_in_transit_id = product_received["products_in_transit_id"] 
                distribution_center_id = product_received["distribution_center_id"] 
                model_id = product_received["model_id"]
                imei_1 = product_received["imei_1"]
                imei_2 = product_received["imei_2"]
                qr_code_id = product_received["qr_code_id"]
                received_date = product_received["received_date"]
                remarks = product_received["remarks"]
                created_date = product_received["created_date"]
                created_by_id = product_received["created_by"]
                
                stock_state = product_received["stock_state"]
                if int(stock_state) ==1:
                    this_stock_state = "Available"
                else:
                    this_stock_state = "Dispatched" 
                                    
                response = {
                    
                    "id": id,
                    "global_id": global_id,
                    "products_in_transit_id": products_in_transit_id,
                    "distribution_center_id": distribution_center_id,
                    "model_id": model_id,
                    "imei_1": imei_1,
                    "imei_2": imei_2,
                    "qr_code_id": qr_code_id,
                    "received_date":received_date,
                    "remarks": remarks,
                    "state":this_stock_state,
                    "created_date": created_date,
                    "created_by_id": created_by_id
                    
                }
            
                return response
                
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'Failed to fetch products received details!'
                        }   
                return jsonify(message), 201             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to fetch products received details.' + format(error)}
            ErrorLogger().logError(message),
            return jsonify(message), 501
             
    def approve_received_stock(self, user):
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
            
            cur.execute("""SELECT global_id, products_in_transit_id, model_id FROM mobile_phones_transit_stock_received WHERE id = %s """, (id))
            product_intransit = cur.fetchone() 
            if product_intransit:    
                products_in_transit_id = product_intransit["products_in_transit_id"]  
                model_id = product_intransit["model_id"]  
            else:
                message = {
                            "description":"Failed to fetch products in transit id!",
                            "status":200}
                return message
            
            #update mobile phones products received status
            cur.execute("""UPDATE mobile_phones_transit_stock_received set status=1, approved_date = %s, approved_by = %s WHERE status = 2 AND id = %s """, ([dateapproved, approved_by, id]))
            mysql.get_db().commit() 
            rowcount = cur.rowcount
            if rowcount:
                #update quantity balance of the products in transit
                cur.execute("""UPDATE products_in_transit_models set quantity_received = quantity_received + 1 WHERE products_in_transit_id = %s AND model_id = %s""", ([products_in_transit_id, model_id]))
                mysql.get_db().commit()
        
                message = {
                            "description":"Products received was approved successfully!",
                            "status":200}
                return message
                
            else:
                message = {'status':201,
                            'description':'Products received record was not found!'}
                return jsonify(message)
           
                
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a09',
                       'description':'Failed to approve products received record. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()

     
   