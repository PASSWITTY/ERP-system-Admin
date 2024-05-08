from flask import request, Response, json, jsonify
from main import mysql, app
from accounts_module.accounts_model import Account
from resources.alphanumeric.generate import UniqueNumber
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime

class Transport():
          
  
    def list_transport_modes(self, user):
        
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
        
            cur.execute("""SELECT id, name, created_date, created_by FROM transport_modes WHERE status = %s """, (status))
            transport_modes = cur.fetchall()            
            if transport_modes:
                response_array = []
                
                for transport_mode in transport_modes:
                    response = {
                        "id": transport_mode['id'],
                        "name": transport_mode['name'],
                        "created_date": transport_mode['created_date'],
                        "created_by": transport_mode['created_by']
                    }
                    response_array.append(response)
            
            
                message = {'status':200,
                            'response':response_array, 
                            'description':'Transport modes records were fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'Transport modes records were not found!'
                        }   
                return jsonify(message), 201             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve transport modes record from database.' + format(error)}
            ErrorLogger().logError(message),
            return jsonify(message), 501  
        


     
   