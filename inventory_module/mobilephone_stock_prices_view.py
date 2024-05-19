from flask import request, Response, json, jsonify
from main import mysql, app
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.transactions.bookkeeping import DebitCredit
import uuid

class StockPrice():
          
    def update_stock_price(self, user):
        #Get the request data 
        request_data = request.get_json()       
        
        validated_data = request_data
        # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
        # if error_messages:
        #     return jsonify({"error": error_messages}), 400
        
        model_id = validated_data["model_id"]
        distribution_center_id = validated_data["distribution_center_id"]
        price_amount = float(validated_data["price_amount"].replace(",", ""))
        discount_amount = float(validated_data["discount_amount"].replace(",", ""))
   
    
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
            status = 2 #pending approval
            created_date = Localtime().gettime()
            created_by = user['id']
            
            final_price = (price_amount - discount_amount)
            
            #Update phone model price per distribution center
            cur.execute("""INSERT INTO distribution_center_mobilephone_model_prices (model_id, distribution_center_id, price_amount, discount_amount, final_price, created_date, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE price_amount = VALUES(price_amount), discount_amount = VALUES(discount_amount), final_price = VALUES(final_price)""", 
                                                                          (model_id, distribution_center_id, price_amount, discount_amount, final_price, created_date, created_by, status))
            mysql.get_db().commit()
            rowcount = cur.rowcount
            if rowcount:
                
                message = {"description":"Distribution center phone model price was updated",
                           "status":200}
                return jsonify(message), 200
            else:
                message = {"description":"Failed to update distribution center phone model price",
                           "status":501}
                return jsonify(message), 501
                       
        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a02',
                       'description':'Failed to update distribution center price. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message), 501
        finally:
            cur.close()  
  
    def list_stock_prices(self, user):
        
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
            
            cur.execute("""SELECT id, model_id, distribution_center_id, price_amount, discount_amount, final_price, created_date, created_by FROM distribution_center_mobilephone_model_prices WHERE status = %s """, (status))
            prices = cur.fetchall()            
            if prices:
                response_array = []
                
                for price in prices:
                    model_id = price["model_id"]
                    distribution_center_id = price["distribution_center_id"] 
                    price_amount = float(price["price_amount"]) 
                    discount_amount = float(price["discount_amount"])
                    final_price = float(price["final_price"])
                    created_date = price["created_date"]
                    created_by_id = price["created_by"]
                    
                    cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s """, (created_by_id))
                    user_details = cur.fetchone()
                    if user_details:
                        first_name = user_details['first_name']
                        last_name = user_details['last_name']
                        
                        created_by_name = first_name + ' ' + last_name
                    else:
                        created_by_name = ''
                        message = {'status':404,
                                   'description':'Failed to fetch user details!'
                        }   
                        return jsonify(message), 404
                    
                    response = {
                        
                        "model_id": model_id,
                        "distribution_center_id": distribution_center_id,
                        "price_amount": price_amount,
                        "discount_amount": discount_amount,
                        "final_price": final_price,
                        "created_date": created_date,
                        "created_by_name": created_by_name
                        
                    }
                    response_array.append(response)
            
                message = {'status':200,
                            'response':response_array, 
                            'description':'Mobile phone model price records were fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':404,
                            'error':'sp_a04',
                            'description':'Failed to fetch mobile phone model price records!'
                        }   
                return jsonify(message), 404             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve mobile phone model price record from database.' + format(error)}
            ErrorLogger().logError(message),
            return jsonify(message), 501  
        finally:
            cur.close()
        
    def get_stock_price_details(self, user):
        
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
            
            cur.execute("""SELECT id, model_id, distribution_center_id, price_amount, discount_amount, final_price, created_date, created_by FROM distribution_center_mobilephone_model_prices WHERE id = %s """, (id))
            price = cur.fetchone()            
            if price:
                
                    model_id = price["model_id"]
                    distribution_center_id = price["distribution_center_id"] 
                    price_amount = float(price["price_amount"]) 
                    discount_amount = float(price["discount_amount"])
                    final_price = float(price["final_price"])
                    created_date = price["created_date"]
                    created_by_id = price["created_by"]
                    
                    cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s """, (created_by_id))
                    user_details = cur.fetchone()
                    if user_details:
                        first_name = user_details['first_name']
                        last_name = user_details['last_name']
                        
                        created_by_name = first_name + ' ' + last_name
                    else:
                        created_by_name = ''
                        message = {'status':404,
                                   'description':'Failed to fetch user details!'
                        }   
                        return jsonify(message), 404
                    
                    response = {
                        "model_id": model_id,
                        "distribution_center_id": distribution_center_id,
                        "price_amount": price_amount,
                        "discount_amount": discount_amount,
                        "final_price": final_price,
                        "created_date": created_date,
                        "created_by_name": created_by_name
                    }
            
                    message = {'status':200,
                                'response':response, 
                                'description':'Mobile phone model price record was fetched successfully!'
                            }   
                    return jsonify(message), 200
            
            else:                
                message = {'status':404,
                            'error':'sp_a04',
                            'description':'Failed to fetch mobile phone model price record!'
                        }   
                return jsonify(message), 404             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve mobile phone model price record from database.' + format(error)}
            ErrorLogger().logError(message),
            return jsonify(message), 501 
        finally:
            cur.close()
             
    def approve_stock_price(self, user):
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
            #update cash stock purchase details
            cur.execute("""UPDATE distribution_center_mobilephone_model_prices set status=1, approved_date = %s, approved_by = %s WHERE status = 2 AND id = %s """, ([dateapproved, approved_by, id]))
            mysql.get_db().commit() 
            rowcount = cur.rowcount
            if rowcount:
                message = {'status':200,
                            'description':'Model price update was approved successfully!'}
                return jsonify(message), 200  
            else:              
                message = {'status':404,
                            'description':'Model price update record was not found!'}
                return jsonify(message), 404
                    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a09',
                       'description':'Failed to approve price update record. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message), 501
        finally:
            cur.close()

     
   