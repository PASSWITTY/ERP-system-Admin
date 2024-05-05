from flask import request, Response, json, jsonify
from resources.password.crypt_password import hash_password, unhash_password
from main import mysql, app
from resources.payload.payload import Localtime
from resources.middleware.tokens.jwt import sign_token, refresh_token, sign_permissions

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