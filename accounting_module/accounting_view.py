from flask import request, Response, json, jsonify
from main import mysql, app
from resources.accounts.accounts_class import Accounts
from resources.alphanumeric.generate import UniqueNumber
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime

class Accounting():
  
    def create_account(self, user):
        request_data = request.get_json()
       
        
        if request_data == None:
            message = {'status':402,
                       'error':'aa_a10',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message), 402

        #Try except block to handle execute task
        try:
            request_data["user_id"] = user["id"]
            request_data["owner_id"] = ''
            request_data["entity_id"] = 0
            request_data["status"] = 2
            
            api_response = Accounting().create_new_account(request_data)
            if int(api_response["status"] == 200):
                
                message = {"description":"Account was created successfully",
                           "status":200}
                return jsonify(message)
            else:
                message = {'status':201,
                           'error':'aa_a11',
                           'description':api_response["description"]}
                ErrorLogger().logError(message)
                return jsonify(message), 201
            
        except Exception as error:
            message = {'status':501,
                       'error':'aa_a12',
                       'description':'Account creation process failed! Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message), 501
        
    def create_new_account(self, account):
        
        if account == None:
            message = {'status':402,
                       'error':'aa_a13',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message, 402
    
        accountName = account["name"]
        if account["accountType"] != '':
            type_Id = int(account["accountType"])
        else:
            type_Id = 0
            
        categoryId = account["accountCategory"]
        sub_category = account["accountSubCategory"]
        mainaccount = account["main_account"]
        openingBalance = float(account["opening_balance"])     
        owner_id = account["owner_id"]
        entity_id = account["entity_id"]
        notes = account["notes"]
        description = account["description"]
        referenceNumber = account["reference_number"]
        user_id = account["user_id"]
        status = account["status"]

        typeId = type_Id     
        accountNumber = Accounts().accountNumber(typeId) 
        accountId = UniqueNumber().accountId()
        
        account = {"id":accountId, 
                   "account_number":accountNumber,  
                   "name":accountName, 
                   "accountTypeId":type_Id, 
                   "accountCategoryId":categoryId, 
                   "accountSubCategoryId":sub_category,
                   "main_account":mainaccount,
                   "opening_balance":openingBalance, 
                   "ownerid":owner_id, 
                   "entityid":entity_id, 
                   "notes":notes, 
                   "description":description, 
                   "reference_number":referenceNumber,
                   "createdby":user_id, 
                   "status":status}
        
        
         #Try except block to handle executable task
        try:
            
            api_message = Accounts().create_account(account)

            if int(api_message["status"]) == 200:
                
                response = {"account_number":accountNumber, 
                            "account_id":accountId
                    }
               
                message = {"description":"Account was created successfully",
                           "response":response,
                           "status":200
                           }
                
                return message
            else:
                message = {'status':201,
                           'error':'aa_a15',
                           'description':'Account creation process failed!'}
                ErrorLogger().logError(message)
               
                return message

        except Exception as error:
            message = {'status':501,
                       'error':'aa_a16',
                       'description':'Account creation process failed! Error description ' + format(error)}
            ErrorLogger().logError(message)
          
            return message
        
    def approve_new_account(self, user):

        request_data = request.get_json()

        if request_data == None:
            message = {'status':402,
                       'error':'aa_a25',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message)

        account_id = request_data["id"]
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a26',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)

        #Try except block to handle the update operation
        try:   
            dateApproved = Localtime().gettime()
            approvedBy = user["id"]        
            cur.execute("""UPDATE accounts set status=1, approvedon = %s, approvedby =%s WHERE id = %s""", ([dateApproved, approvedBy, account_id]))
            mysql.get_db().commit()

            message = {'status':200,
                       'description':'Account was approved successfully!'}
            return jsonify(message)

        except Exception as error:         
            message = {'status':501,
                       'error':'aa_a27',
                        'description':'Failed to approve new account.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
                cur.close()

    def list_accounts(self,user):
        request_data = request.get_json()
        
        if request_data == None:
            message = {'status':402,
                       'error':'aa_a10',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message), 402
        
        
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a17',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message), 500
        
        try:
            status = request_data['status']
            cur.execute("""SELECT * FROM accounts WHERE status = %s ORDER BY id ASC""", (status))
            results = cur.fetchall() 
            if results:           

                accounts = []
                count = 0
                for account in results:
                    #get created by name
                    createdby_id = account['createdby']
                    cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id= %s""", [createdby_id])
                    userdetails = cur.fetchone()
                    if userdetails:
                        user_name = userdetails['first_name'] + " " + userdetails['last_name']
        
                    count = count + 1
                    res = {
                        "count":count,
                        "id": account['id'],
                        "accountname": account['name'],
                        "referenceno": account['reference_no'],
                        "type": account['type'],
                        "category_name": account['category_name'],
                        "currency": account['currency'],
                        "number": account['number'],
                        "mainaccount": account['mainaccount'],
                        "description": account['description'],
                        "notes": account['notes'],
                        "balance": float(account['balance']),
                        "datecreated": account['datecreated'],
                        "createdby": user_name,

                    }
                    accounts.append(res)
                message = {'status':200,
                            'response':accounts,
                            'description':'Account record was fetched successfully!'}

                return jsonify(message), 200

            else:
                message = {'status':404,
                           'error':'aa_a18',
                           'description':'No account record was found!'}
                ErrorLogger().logError(message)
                return jsonify(message), 404

    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'aa_a19',
                       'description':'Failed to retrieve accounts record from database.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message), 501  
        finally:
            cur.close()
            
    def get_account_details(self, user):   
        request_data = request.get_json()
        
        if request_data == None:
            message = {'status':402,
                       'error':'aa_a25',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message)
            
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a20',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)
    
        try:
            account_number = request_data['number']
            cur.execute("""SELECT * FROM accounts WHERE number = %s""", [account_number])
            account = cur.fetchone()
            if account:
                createdby_id = account['createdby']
                type_name = account['type_name']
                category_name = account['category_name']
                
                currency_id = account['currency']
                
                cur.execute("""SELECT currency_name FROM currency WHERE id = %s""", [currency_id])
                curr = cur.fetchone()
                if curr:
                    currency_name = curr["currency_name"]
                else:
                    currency_name = ''

                #get created by name
                cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id= %s""", [createdby_id])
                userdetails = cur.fetchone()
                if userdetails:
                    user_name = userdetails['first_name'] + " " + userdetails['last_name']
                else:
                    user_name = ''

                
                res = {
                    "id": account['id'],
                    "accountname": account['name'],
                    "referenceno": account['reference_no'],
                    "type": account['type_name'],
                    "class": account['class_name'], 
                    "type_name": account['type_name'],
                    "category_name": account['category_name'],       
                    "sub_category_name": account['sub_category_name'],       
                    "currency": currency_name,
                    "last_transaction_id": account['last_transaction_id'],
                    "last_amount": float(account['last_amount']),
                    "number": account['number'],
                    "mainaccount": account['mainaccount'],
                    "description": account['description'],
                    "notes": account['notes'],
                    "balance": float(account['balance']),
                    "datecreated": account['datecreated'],
                    "createdby": user_name,
                    "createdby_id": createdby_id

                }
          

                #The response object
                message = {"description":"Account details record was found",
                           "response":res,
                           "status":200}
                # return message
                return jsonify(message),200
            
            else:
                message = {"description":"Account details record was not found",
                           'error':'aa_a21',
                           "status":201}
                ErrorLogger().logError(message)
                # return message
                return jsonify(message),201

        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'aa_a22',
                       'description':'Account details record fetching failed! Error description ' + format(error)}
            ErrorLogger().logError(message)
            # return message 
            return jsonify(message),501
        finally:
            cur.close()
            
    def list_account_types(self, user):
        request_data = request.get_json()
        
        if request_data == None:
            message = {'status':402,
                       'error':'aa_a10',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message), 402
        
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a02',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message), 500
       
        try:
            status = request_data["status"]
            
            cur.execute("""SELECT * FROM accounts_types WHERE status =%s ORDER BY id ASC""", [status])
            results = cur.fetchall()
            if results:
                accounts = []

                for account in results:
                    res = {
                        "account_id": account['id'],
                        "name": account['name']
                    }
                    accounts.append(res)
                  
                #The response object
                message = {'status':200,
                           'response':accounts,
                           'description':'Account types were fetched successfully'}

                return jsonify(message), 200
            else:
                message = {'status':404,
                           'error':'aa_a02',
                           'description':'No record was found!'}
                ErrorLogger().logError(message)
                return jsonify(message), 404

    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'aa_a03',
                       'description':'Failed to retrieve account types record from database. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message), 501
        finally:
            cur.close()

    def list_account_categories(self, user):
        request_data = request.get_json()
        
        if request_data == None:
            message = {'status':402,
                       'error':'aa_a10',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message), 402
        
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a04',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message), 500
        
        try:
            status = request_data["status"]
            
            cur.execute("""SELECT * FROM accounts_categories WHERE status =%s ORDER BY id ASC""", [status])
            results = cur.fetchall()
            if results:          
                accounts = []

                for account in results:
                    type_id = account['second_layer_id']
                    
                    cur.execute("""SELECT name FROM accounts_types WHERE id =%s""", [type_id])
                    get_type = cur.fetchone()
                    if get_type:
                        type_name = get_type['name']
                    else:
                        type_name = ''
                    
                    res = {
                        "category_id": account['id'],
                        "name": account['name'],
                        "type_id": type_id,
                        "type_name": type_name
                    }
                    accounts.append(res)
                 
                #The response object
                message = {'status':200,
                           'response':accounts,
                           'description':'Accounts category item records were found'}

                return jsonify(message), 200
            else:
                message = {'status':404,
                           'error':'aa_a05',
                           'description':'No accounts category record was found!'
                           }
                ErrorLogger().logError(message)
                return jsonify(message), 404

    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'aa_a06',
                       'description':'Failed to retrieve accounts category records from database. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message), 501  
        finally:
            cur.close()


    def list_specific_accounts_by_type(self,user):
        details = request.get_json()
        if details == None:
            message = {'status':402,
                       'error':'aa_a25',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message)

        type = details["type"]
        status = details["status"]
        

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a28',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)
        # print("select")
        try:
            cur.execute("""SELECT * FROM accounts WHERE type_id = %s AND status = %s """, [type, status])
            results = cur.fetchall()
            cur.close()

            wallets = []
            for account in results:
                res = {
                    "account_id": account['id'],
                    "account_name": account['name'],
                    "reference_number": account['reference_no'],
                    "type": account['type'],
                    "account_number": account['number'],
                    "balance": float(account['balance'])

                }
                wallets.append(res)
              
            #The response object
            message = {'status':200,
                        'response':wallets,
                        'description':'Account record was found!'}

            return jsonify(message)
    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'aa_a29',
                       'description':'Failed to fetch account details! Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()