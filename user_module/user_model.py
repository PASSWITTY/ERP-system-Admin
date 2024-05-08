from flask import request, Response, json, jsonify
from resources.password.crypt_password import hash_password, unhash_password
from main import mysql, app
from resources.payload.payload import Localtime
from resources.middleware.tokens.jwt import sign_token, refresh_token, sign_permissions
from resources.logs.logger import ErrorLogger

class User():

    def login(self):
        # Get the user data recieved from the front-end
        user = request.get_json()

        if user == None:
            message = {'status':402,
                       'description':'Request data is missing some details!'}
            return jsonify(message)
        
        username = user["email"]
        password = user["password"]

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)

        try:
            # Query to get the user.
            user_exists = cur.execute("""SELECT email FROM users WHERE email = %s""", [username])

            if user_exists:
                cur.execute( """SELECT id, email, hash_password, user_type FROM users WHERE email = %s""", [username])
                found_user = cur.fetchone()
                
                user_id = found_user['id']
                username = found_user['email']
                hashed = found_user['hash_password'].encode()
                user_type = int(found_user['user_type'])
                
                
                if unhash_password(password.encode(), hashed):
                     
                    cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s""", [user_id])
                    staff_details = cur.fetchone()
                    if staff_details:
                        first_name = staff_details['first_name']
                        last_name = staff_details['last_name']
                    else:
                        first_name = ''
                        last_name = ''

                    try:
                        access_token, refresh_token = sign_token({'username': username,'user_id': user_id,'user_type': user_type})
                        
                    except Exception as e:                        
                        return json.jsonify(str(e)), 500
                    
                    # cur.execute("""SELECT currency_code FROM currency WHERE default_currency = 1""") 
                    # curr_res = cur.fetchone()
                    # if curr_res:
                    #     currency = curr_res["currency_code"] 
                    # else:
                    currency = "KES" #Default kenyan currency
                        

                    user_details = {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user_id": user_id,
                        "user_type": user_type,
                        "currency":currency,
                        "user_firstName": first_name,
                        "user_lastName": last_name,
                        "user_email":'',
                        "username":'',
                        "message":"Logged in Successfully!"
                       
                    }

                    return jsonify(user_details), 200

                else:
                    message = {"description":"Invalid credentials!"}
                    return jsonify(message), 201
                    
            else:
                message = {"description":"User record not found!"}
                return jsonify(message), 404

        except Exception as error:
            message = {"description":"Transaction failed. Error description " + format(error)}
            return jsonify(message), 501  
        finally:
            cur.close()
            
    def renew_token(self):
        try:
            auth = refresh_token()
            # print(auth.encode())
            message = {"auth":auth, "status":200}
            return jsonify(message)
            
        except Exception as e:            
            return json.jsonify(str(e)), 500
        
    def change_password(self):
        user_details = request.get_json()

        if user_details == None:
            return Response(status=402)

        username = user_details["username"]
        pwd = user_details["password"]


        # Test DB connection
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)

        try:
            # Hash the password before saving it
            password = hash_password(pwd.encode())
            
            # dateCreated = Localtime().gettime()
            
            cur.execute("""UPDATE users set password = %s WHERE username = %s """, (password, username))
            mysql.get_db().commit() 
       
            message = {"status":200,
                       "description":"Password was updated successfully!"}
            return jsonify(message)

        except Exception as error:
            message = {'status':501,
                       'description':'Transaction failed. Error description ' + format(error)}
            return jsonify(message)  
        finally:
            cur.close()
            
    def list_user_categories(self, user):
        
        request_data = request.get_json() 
        
        if request_data == None:
            message = {'status':402,
                       'error':'sp_a03',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message), 402
       
        try:
            cur = mysql.get_db().cursor()
                    
        except:
            message = {'status':500,
                        'error':'sp_a14',
                        'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message, 500
                
        try:
            status = request_data["status"]
        
            cur.execute("""SELECT id, name, created_date, created_by FROM user_categories WHERE status = %s """, (status))
            user_categories = cur.fetchall()            
            if user_categories:
                response_array = []
                
                for user_categorie in user_categories:
                    response = {
                        "id": user_categorie['id'],
                        "name": user_categorie['name'],
                        "created_date": user_categorie['created_date'],
                        "created_by_id": user_categorie['created_by']
                    }
                    response_array.append(response)
            
            
                message = {'status':200,
                            'response':response_array, 
                            'description':'User categories records were fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'User categories records were not found!'
                        }   
                return jsonify(message), 201             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve user categories record from database.' + format(error)}
            ErrorLogger().logError(message),
            return jsonify(message), 501  
        


    def create_user(self, user):
        #Get the request data 
        request_data = request.get_json()       
        
        validated_data = request_data
        # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
        # if error_messages:
        #     return jsonify({"error": error_messages}), 400
        
        first_name = validated_data["first_name"]
        middle_name = validated_data["middle_name"]
        last_name = validated_data["last_name"]
        user_categories = validated_data["user_categories"]
        mobile_number = validated_data["mobile_number"]
        email = validated_data["email_address"]
        gender = validated_data["gender"]
        marital_status = validated_data["marital_status"]
        other_mobile_number = validated_data["alternative_mobile_number"]
        id_number = validated_data["id_number"]
        address = validated_data["address"]
        postal_code = validated_data["postal_code"]
        country = validated_data["country"]
        county = validated_data["county"]
        town = validated_data["city"]
        kra_pin = validated_data["kra_pin"]
        nhif_number = validated_data["nhif_number"]
        nssf_number = validated_data["nssf_number"]
        id_front = validated_data["id_front"]
        id_back = validated_data["id_back"]
        selfie = validated_data["selfie"]
        username = validated_data["username"]
        confirm_password = validated_data["confirm_password"]
        
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
            
            #administrator and stockist
            if ((int(user_categories) == 1) or (int(user_categories) == 2)):
                user_type = 2
                
            elif ((int(user_categories) == 3) or (int(user_categories) == 4) or (int(user_categories) == 4)):
                user_type = 1
            
            else:
                user_type = 0

            
            #store new user details
            
            password = hash_password(confirm_password.encode())
            
            cur.execute("""INSERT INTO users (username, email,       contact, user_type, hash_password, status) VALUES (%s, %s, %s, %s, %s, %s)""", 
                                             (username, email, mobile_number, user_type,      password, status))
            mysql.get_db().commit()
            rowcount = cur.rowcount
            if rowcount:
                user_id = cur.lastrowid
                cur.execute("""INSERT INTO user_details (first_name, middle_name, last_name, user_id, id_number, gender, mobile_number, other_mobile_number, marital_status, country, county, town, address, postal_code, kra_pin, nssf_number, nhif_number, id_front, id_back, selfie, date_created, created_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                        (first_name, middle_name, last_name, user_id, id_number, gender, mobile_number, other_mobile_number, marital_status, country, county, town, address, postal_code, kra_pin, nssf_number, nhif_number, id_front, id_back, selfie, date_created, created_by))
                mysql.get_db().commit()
                cur.close()
                
                message = {"description":"New user was created successfully",
                           "status":200}
                return message
            else:
                message = {"description":"Failed to create new user!",
                           "status":201}
                return message, 201

        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a02',
                       'description':'Failed to create a new user. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message), 501 
        
        
    def list_users(self, user):
        
        request_data = request.get_json() 
        
        if request_data == None:
            message = {'status':402,
                       'error':'sp_a03',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message), 402
       
        try:
            cur = mysql.get_db().cursor()
                    
        except:
            message = {'status':500,
                        'error':'sp_a14',
                        'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message, 500
                
        try:
            status = request_data["status"]
        
            cur.execute("""SELECT id, username, email, contact, user_type FROM users WHERE status = %s """, (status))
            users = cur.fetchall()            
            if users:
                response_array = []
                
                for user in users:
                    user_id = user['id']
                    
                    cur.execute("""SELECT first_name, middle_name, last_name, id_number, gender, mobile_number, other_mobile_number, marital_status, country, county, town, address, postal_code, kra_pin, nssf_number, nhif_number, id_front, id_back, selfie, date_created, created_by FROM user_details WHERE user_id = %s """, (user_id))
                    user_details = cur.fetchone() 
                    if user_details:
                        response = {
                            "id": user['id'],
                            "username": user['username'],
                            "email": user['email'],
                            "contact": user['contact'],
                            "user_type": user['user_type'],
                            "first_name": user_details['first_name'],
                            "middle_name": user_details['middle_name'],
                            "last_name": user_details['last_name'],
                            "id_number": user_details['id_number'],
                            "gender": user_details['gender'],
                            "mobile_number": user_details['mobile_number'],
                            "other_mobile_number": user_details['other_mobile_number'],
                            "marital_status": user_details['marital_status'],
                            "country": user_details['country'],
                            "county": user_details['county'],
                            "town": user_details['town'],
                            "address": user_details['address'],
                            "postal_code": user_details['postal_code'],
                            "kra_pin": user_details['kra_pin'],
                            "nssf_number": user_details['nssf_number'],
                            "nhif_number": user_details['nhif_number'],
                            "id_front": user_details['id_front'],
                            "id_back": user_details['id_back'],
                            "selfie": user_details['selfie'],
                            "date_created": user_details['date_created'],
                            "created_by_id": user_details['created_by']
                        }
                        response_array.append(response)
                    else:
                        message = {'status':201,
                            'response':response_array, 
                            'description':'Failed to fetch user records!'
                        }   
                        return jsonify(message), 201
                        
            
            
                message = {'status':200,
                            'response':response_array, 
                            'description':'User records were fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'User records were not found!'
                        }   
                return jsonify(message), 201             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve user record from database.' + format(error)}
            ErrorLogger().logError(message),
            return jsonify(message), 501
        
        
    def get_user_details(self, user):
        
        request_data = request.get_json() 
        
        if request_data == None:
            message = {'status':402,
                       'error':'sp_a03',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message), 402
       
        try:
            cur = mysql.get_db().cursor()
                    
        except:
            message = {'status':500,
                        'error':'sp_a14',
                        'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message, 500
                
        try:
            id = request_data["id"]
        
            cur.execute("""SELECT id, username, email, contact, user_type FROM users WHERE id = %s """, (id))
            user = cur.fetchone()            
            if user:
                user_id = user['id']
                username = user['username']
                    
                cur.execute("""SELECT first_name, middle_name, last_name, id_number, gender, mobile_number, other_mobile_number, marital_status, country, county, town, address, postal_code, kra_pin, nssf_number, nhif_number, id_front, id_back, selfie, date_created, created_by FROM user_details WHERE user_id = %s """, (user_id))
                user_details = cur.fetchone() 
                if user_details:
                    response = {
                        "id": user['id'],
                        "username": username,
                        "email": user['email'],
                        "contact": user['contact'],
                        "user_type": user['user_type'],
                        "first_name": user_details['first_name'],
                        "middle_name": user_details['middle_name'],
                        "last_name": user_details['last_name'],
                        "id_number": user_details['id_number'],
                        "gender": user_details['gender'],
                        "mobile_number": user_details['mobile_number'],
                        "other_mobile_number": user_details['other_mobile_number'],
                        "marital_status": user_details['marital_status'],
                        "country": user_details['country'],
                        "county": user_details['county'],
                        "town": user_details['town'],
                        "address": user_details['address'],
                        "postal_code": user_details['postal_code'],
                        "kra_pin": user_details['kra_pin'],
                        "nssf_number": user_details['nssf_number'],
                        "nhif_number": user_details['nhif_number'],
                        "id_front": user_details['id_front'],
                        "id_back": user_details['id_back'],
                        "selfie": user_details['selfie'],
                        "date_created": user_details['date_created'],
                        "created_by_id": user_details['created_by']
                    }
                    
                    return response
                        
                else:
                    message = {'status':201,
                        'response':response, 
                        'description':'Failed to fetch user records!'
                    }   
                    return jsonify(message), 201
                        
            
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'User record was not found!'
                        }   
                return jsonify(message), 201             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to fetch user record from database.' + format(error)}
            ErrorLogger().logError(message),
            return jsonify(message), 501