from flask import request, Response, json, jsonify
from main import mysql, app
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.alphanumeric.generate import UniqueNumber
from accounting_module.accounting_view import Accounting

class Suppliers():
          
    def create_inventory_supplier(self, user):
        #Get the request data 
        request_data = request.get_json()       
        
        validated_data = request_data
        # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
        # if error_messages:
        #     return jsonify({"error": error_messages}), 400
        
        business_name = validated_data["business_name"]
        trading_name = validated_data["trading_name"]
        company_mobile_number = validated_data["company_mobile_number"]
        company_alternative_mobile_number = validated_data["company_alternative_mobile_number"]
        address = validated_data["address"]
        postal_code = validated_data["postal_code"]
        country = validated_data["country"]
        city = validated_data["city"]
        registration_number = validated_data["registration_number"]
        tax_id = validated_data["tax_id"]
        company_email = validated_data["company_email"]
        website = validated_data["company_website"]
        contact_persons = json.dumps(validated_data["contact_persons"])
        
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
            created_date = Localtime().gettime()
            created_by = user['id']

            #store supplier details request
            cur.execute("""INSERT INTO suppliers (business_name, trading_name, company_mobile_number, company_alternative_mobile_number, company_email, website, address, postal_code, country, city, created_date, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                 (business_name, trading_name, company_mobile_number, company_alternative_mobile_number, company_email, website, address, postal_code, country, city, created_date, created_by, status))
            mysql.get_db().commit()
            
            rowcount = cur.rowcount
            if rowcount: 
                supplier_id = cur.lastrowid
                
                supplier_contact_persons = json.loads(contact_persons)                
                for contact_person in supplier_contact_persons:

                    title = contact_person["title"]
                    first_name = contact_person["first_name"]
                    last_name = contact_person["last_name"]
                    mobile_number = contact_person["mobile_number"]
                    alternative_mobile_number = contact_person["alternative_mobile_number"]
                    email = contact_person["email"]
                    
                    supplierId = UniqueNumber().supplierId()
                    #save contact details
                    cur.execute("""INSERT INTO supplier_contact (id, supplier_id, title, first_name, last_name, mobile_number, alternative_mobile_number, email, created_date, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                        (supplierId, supplier_id, title, first_name, last_name, mobile_number, alternative_mobile_number, email, created_date, created_by, status))
                    mysql.get_db().commit()
                
            message = {"description":"Supplier was created successfully",
                       "status":200}
            return message
                        

        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a02',
                       'description':'Failed to create a supplier. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()
  
    def list_inventory_suppliers(self, user):
        
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
        
            cur.execute("""SELECT * from suppliers WHERE status= %s ORDER BY created_date DESC""", [status])
            results = cur.fetchall()    
            if results:
                trans = []
                no = 0

                for result in results:
                    created_by_id = result['created_by']
                    supplier_id = result['id']
                    
                    #select supplier payable account. Payable account is type 9
                    cur.execute("""SELECT * FROM accounts WHERE type_id = 9 AND owner_id = %s """, [supplier_id])
                    payable_acc_details = cur.fetchone() 
                    if payable_acc_details:
                        payable_account_number = payable_acc_details["number"]
                        payable_account_name = payable_acc_details["name"]
                        payable_account_balance = float(payable_acc_details["balance"])
                        payable_acc_currency = payable_acc_details["currency"]
                        if payable_acc_currency ==1:
                            payable_account_currency = "Kes"
                        else:
                            payable_account_currency = ""
                    else:
                        payable_account_number = ''
                        payable_account_name = ''
                        payable_account_balance = ''
                        payable_account_currency = ''
                        
                    
                    
                    #select supplier prepaid account. Supplier prepaid account is type 4
                    cur.execute("""SELECT * FROM accounts WHERE type_id = 4 AND owner_id = %s """, [supplier_id])
                    prepaid_acc_details = cur.fetchone() 
                    if prepaid_acc_details:
                        prepaid_account_number = prepaid_acc_details["number"]
                        prepaid_account_name = prepaid_acc_details["name"]
                        prepaid_account_balance = float(prepaid_acc_details["balance"])
                        prepaid_acc_currency = prepaid_acc_details["currency"]
                        if prepaid_acc_currency ==1:
                            prepaid_account_currency = "Kes"
                        else:
                            prepaid_account_currency = ""
                    else:
                        prepaid_account_number = ''
                        prepaid_account_name = ''
                        prepaid_account_balance = ''
                        prepaid_account_currency = ''
                    
                    cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s """, [created_by_id])
                    createdby_details = cur.fetchone()  
                              
                    created_by = createdby_details['first_name'] + " " + createdby_details['last_name']
                    no = no + 1
                    res = {
                        "id": result['id'],
                        "no":no,
                        "business_name": result['business_name'],
                        "trading_name": result['trading_name'], 
                        "company_email": result['company_email'],
                        "company_mobile_number": result['company_mobile_number'],
                        "country": result['country'],
                        "address": result['address'],
                        "postal_code": result['postal_code'],
                        "created_date": result['created_date'],
                        "createdby": created_by,                  
                        "created_by_id": created_by_id,
                        "payable_account":{
                            "account_number":payable_account_number,
                            "account_name":payable_account_name,
                            "account_balance":payable_account_balance,
                            "account_currency":payable_account_currency,
                        },
                        "prepaid_account":{
                            "account_number":prepaid_account_number,
                            "account_name":prepaid_account_name,
                            "account_balance":prepaid_account_balance,
                            "account_currency":prepaid_account_currency,
                        }                   
                    }
                    trans.append(res)
                
                message = {'status':200,
                            'response':trans,
                            'description':'Supplier records were fetched successfully!'
                        }   
                return jsonify(message)             
            
            else:                
                message = {'status':201,
                            'error':'sp_a04',
                            'description':'Failed to fetch suppliers!'
                        }   
                ErrorLogger().logError(message)
                return jsonify(message) 
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve supplier record from database.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()

    def get_inventory_supplier_details(self, user):
        
        request_data = request.get_json()

        if request_data == None:
            message = {'status':402,
                       'description':'Request data is missing some details!'}
            return jsonify(message)

        id = request_data["id"]

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)
        
        try:
            cur.execute("""SELECT * FROM suppliers WHERE id = %s""", (id))
            supplier = cur.fetchone()
            if supplier:  
                created_by_id = supplier['created_by']
                supplier_id = supplier['id']
                
                cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id= %s""", (created_by_id))
                userdetails = cur.fetchone()
                if userdetails:
                    created_by = userdetails['first_name'] + " " + userdetails['last_name']
                else:
                    created_by = ''
                
                contact_persons = []
                cur.execute("""SELECT * FROM supplier_contact WHERE supplier_id = %s""", (supplier_id))
                supplier_contacts = cur.fetchall()
                if supplier_contacts:  
                    for supplier_contact in supplier_contacts:
                        title = supplier_contact['title']
                        first_name = supplier_contact['first_name']
                        last_name = supplier_contact['last_name']
                        mobile_number = supplier_contact['mobile_number']
                        alternative_mobile_number = supplier_contact['alternative_mobile_number']
                        email = supplier_contact['email']
                        status = supplier_contact['status']
                        created_date = supplier_contact['created_date']
                        if int(status) ==1:
                            this_status = 'Active',
                        elif int(status) ==2:
                            this_status = 'Pending Approval',
                        else:
                            this_status = 'Not Active'
                        
                        response = {
                            "title":title,
                            "first_name":first_name,
                            "last_name":last_name,
                            "mobile_number":mobile_number,
                            "alternative_mobile_number":alternative_mobile_number,
                            "email":email,
                            "created_date":created_date,
                            "status":this_status
                            
                        }
                        contact_persons.append(response)
                        

                trans = {
                    "id": supplier['id'],
                    "business_name": supplier['business_name'],          
                    "trading_name": supplier['mobile_number'],
                    "company_mobile_number": supplier['company_mobile_number'],
                    "company_alternative_mobile_number": supplier['company_alternative_mobile_number'],
                    "company_email": supplier['company_email'],
                    "tax_id": supplier['tax_id'],
                    "registration_number": supplier['registration_number'],
                    "website": supplier['website'],
                    "country": supplier['country'],
                    "city": supplier['city'],
                    "address": supplier['address'],
                    "postal_code": supplier['postal_code'],
                    "created_date": supplier['created_date'],
                    "createdby": created_by,                  
                    "created_by_id": created_by_id,
                    "contact_persons":contact_persons               
                }
                
                #The response object
                         
                return trans
            else:
                message = 'No record was found!'
                return message 
                         
    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'description':'Failed to retrieve record from database.'+ format(error)}
            return jsonify(message)  
        finally:
            cur.close()
            
    def approve_inventory_supplier(self, user):
        request_data = request.get_json()        
        if request_data == None:
            message = {'status':402,
                       'error':'sp_a06',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message)

        id = request_data["id"]
        
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'sp_a07',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)

        try:  
            user_id = user['id']             
            cur.execute("""SELECT business_name, created_by FROM suppliers WHERE status =2 AND id = %s""", [id])
            supplier = cur.fetchone()
            if supplier:
                business_name = supplier["business_name"]
                created_by = supplier["created_by"]
                
                approved_date = Localtime().gettime()
                
                cur.execute("""UPDATE suppliers set status=1, approved_date = %s, approved_by = %s WHERE id = %s """, (approved_date, user_id, id))
                mysql.get_db().commit()
                rowcount = cur.rowcount
                if rowcount:     
                
                    #Create supplier payable account
                    accountName = business_name
                    type_Id = 9 #payable account type
                    categoryId = 14 #account category 
                    sub_category = 0
                    mainaccount = 0
                    openingBalance = 0     
                    notes = ''
                    owner_id = id
                    entity_id = 0
                    description = ''
                    referenceNumber = ''
                    
                    account = {
                        "name":accountName, 
                        "accountType":type_Id, 
                        "accountCategory":categoryId, 
                        "accountSubCategory":sub_category,
                        "main_account":mainaccount,
                        "opening_balance":openingBalance, 
                        "owner_id":owner_id, 
                        "entity_id":entity_id, 
                        "notes":notes, 
                        "description":description, 
                        "reference_number":referenceNumber,
                        "user_id":created_by,
                        "status":1}
                    
                    payable_account_res = Accounting().create_new_account(account) 
                    
                    
                    #Create supplier prepayment account
                    accountName = business_name
                    type_Id = 4 #prepaid expenses account type
                    categoryId = 9 #prepaid expenses account category 
                    sub_category = 0
                    mainaccount = 0
                    openingBalance = 0     
                    notes = ''
                    owner_id = id
                    entity_id = 0
                    description = ''
                    referenceNumber = ''
                    
                    account = {
                        "name":accountName, 
                        "accountType":type_Id, 
                        "accountCategory":categoryId, 
                        "accountSubCategory":sub_category,
                        "main_account":mainaccount,
                        "opening_balance":openingBalance, 
                        "owner_id":owner_id, 
                        "entity_id":entity_id, 
                        "notes":notes, 
                        "description":description, 
                        "reference_number":referenceNumber,
                        "user_id":created_by,
                        "status":1}
                
                    prepaid_account_res = Accounting().create_new_account(account)       

                    trans_message = {"description":"Supplier was approved successfully!",
                                    "status":200}
                    return jsonify(trans_message), 200
             
            else:
                message = {'status':201,
                           'description':'Supplier record was not found!'}
                return jsonify(message), 201

    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a09',
                       'description':'Failed to approve supplier record. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message), 501  
        finally:
            cur.close()
            
