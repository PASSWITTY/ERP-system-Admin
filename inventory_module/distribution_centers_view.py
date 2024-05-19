from flask import request, Response, json, jsonify
from main import mysql, app
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime

class DistributionCenter():
          
    def create_distribution_center(self, user):
        #Get the request data 
        request_data = request.get_json()       
        
        validated_data = request_data
        # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
        # if error_messages:
        #     return jsonify({"error": error_messages}), 400
        
        name = validated_data["name"]
        address = validated_data["address"]
        city = validated_data["city"]
        building = validated_data["building"]
        shop_number = validated_data["shop_number"]
        physical_location = validated_data["physical_location"]
        country = validated_data["country"]
        county = validated_data["county"]
        postal_code = validated_data["postal_code"]
        mobile_number = validated_data["mobile_number"]
        telephone_number = validated_data["telephone_number"]
        email = validated_data["email"]
        distribution_center_type_id = validated_data["distribution_center_type_id"]
        region = validated_data["region"]
        notes = validated_data["region"]
        
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

            #store supplier details request
            cur.execute("""INSERT INTO distribution_centers (name, address, city, building, shop_number ,physical_location, country, county, postal_code, mobile_number, telephone_number, email, distribution_center_type_id, region, notes, created_date, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                            (name, address, city, building, shop_number ,physical_location, country, county, postal_code, mobile_number, telephone_number, email, distribution_center_type_id, region, notes, created_date, created_by, status))
            mysql.get_db().commit()
            cur.close()
            
            message = {"description":"Distribution center was created successfully",
                       "status":200}
            return message
                        

        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a02',
                       'description':'Failed to create a Distribution center. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message), 501  
  
    def list_distribution_center(self, user):
        
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
            number = 0
            cur.execute("""SELECT id, name, address, city, building, shop_number, physical_location, country, county, postal_code, mobile_number, telephone_number, email, distribution_center_type_id, region, notes, created_date, created_by FROM distribution_centers WHERE status = %s """, (status))
            centers = cur.fetchall()            
            if centers:
                response_array = []
                number = number + 1
                
                for center in centers:
                    
                    created_by_id = center['created_by']
                    cur.execute("""SELECT id, first_name, last_name FROM user_details WHERE user_id = %s """, (created_by_id))
                    user_details = cur.fetchone()  
                    if user_details:
                        first_name = user_details["first_name"]
                        last_name = user_details["last_name"]
                        user_name = first_name + '' + last_name
                    else:
                        user_name = ''
                    
                    response = {
                        "id": center['id'],
                        "number":number,
                        "name": center['name'],
                        "address": center['address'],
                        "city": center['city'],
                        "building": center['building'],
                        "shop_number": center['shop_number'],
                        "physical_location": center['physical_location'],
                        "country": center['country'],
                        "county": center['county'],
                        "postal_code": center['postal_code'],
                        "mobile_number": center['mobile_number'],
                        "telephone_number": center['telephone_number'],
                        "email": center['email'],
                        "distribution_center_type_id": center['distribution_center_type_id'],
                        "region": center['region'],
                        "notes": center['notes'],
                        "created_date": center['created_date'],
                        "created_by_id": center['created_by'],
                        "user_name":user_name
                    }
                    response_array.append(response)
            
            
                message = {'status':200,
                            'response':response_array, 
                            'description':'Distribution center records were fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'Failed to fetch Distribution centers!'
                        }   
                return jsonify(message), 201             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve Distribution center record from database.' + format(error)}
            ErrorLogger().logError(message),
            return jsonify(message), 501  
        finally:
            cur.close()
        
    def get_distribution_center(self, user):
        
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
        
            cur.execute("""SELECT name, address, city, building, shop_number, physical_location, country, county, postal_code, mobile_number, telephone_number, email, distribution_center_type_id, region, notes, created_date, created_by FROM distribution_centers WHERE id = %s """, (id))
            center = cur.fetchone()            
            if center:
                
                response = {
                    "id": id,
                    "name": center['name'],
                    "address": center['address'],
                    "city": center['city'],
                    "building": center['building'],
                    "shop_number": center['shop_number'],
                    "physical_location": center['physical_location'],
                    "country": center['country'],
                    "county": center['county'],
                    "postal_code": center['postal_code'],
                    "mobile_number": center['mobile_number'],
                    "telephone_number": center['telephone_number'],
                    "email": center['email'],
                    "distribution_center_type_id": center['distribution_center_type_id'],
                    "region": center['region'],
                    "notes": center['notes'],
                    "created_date": center['created_date'],
                    "created_by_id": center['created_by']
                }
                
                return response
                
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'Failed to fetch Distribution center records!'
                        }   
                return jsonify(message), 201             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve Distribution center record from database.' + format(error)}
            ErrorLogger().logError(message),
            return jsonify(message), 501
        finally:
            cur.close()
             
    def approve_distribution_center(self, user):
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
            #update distribution center status
            cur.execute("""UPDATE distribution_centers set status=1, approved_date = %s, approved_by = %s WHERE status = 2 AND id = %s """, ([dateapproved, approved_by, id]))
            mysql.get_db().commit()       
            rowcount = cur.rowcount
            if rowcount:     
                trans_message = {"description":"Distribution center was approved successfully!",
                                 "status":200}
                return jsonify(trans_message), 200
                
            else:
                message = {'status':404,
                           'description':'Distribution center record was not found!'}
                return jsonify(message), 404
                    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a09',
                       'description':'Failed to approve distribution center record. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()

    def list_distribution_center_types(self, user):
        
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
            
            cur.execute("""SELECT id, name, date_created FROM distribution_center_types WHERE status = %s """, (status))
            centers = cur.fetchall()            
            if centers:
                response_array = []
                
                for center in centers:
                    response = {
                        "id": center['id'],
                        "name": center['name'],
                        "date_created": center['date_created']
                    }
                    response_array.append(response)
            
                message = {'status':200,
                            'response':response_array, 
                            'description':'Distribution center type records were fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'Failed to fetch Distribution center types!'
                        }   
                return jsonify(message), 201             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve Distribution center record from database.' + format(error)}
            ErrorLogger().logError(message),
            return jsonify(message), 501 
        finally:
            cur.close()
