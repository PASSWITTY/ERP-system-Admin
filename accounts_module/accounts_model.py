from flask import request, Response, jsonify, json
from main import mysql,app
from resources.alphanumeric.generate import UniqueNumber
from resources.accounts.accounts_class import Accounts
from resources.payload.payload import Localtime
from resources.logs.logger import ErrorLogger

class Account():    

    def get_accounts_types(self, user, id):

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a02',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)
        # print("select")
        try:
            cur.execute("""SELECT * FROM accounts_types WHERE status =%s ORDER BY id ASC""", [id])
            results = cur.fetchall()
            if results:
                accounts = []

                for account in results:
                    res = {
                        "account_id": account['id'],
                        "name": account['name']
                    }
                    accounts.append(res)
                    # print(res)

                #The response object
                message = {'status':200,
                           'response':accounts,
                           'description':'Account types were fetched successfully'}

                return jsonify(message)
            else:
                message = {'status':404,
                           'error':'aa_a02',
                           'description':'No record was found!'}
                ErrorLogger().logError(message)
                return jsonify(message)

    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'aa_a03',
                       'description':'Failed to retrieve account types record from database. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()

    def get_accounts_categories(self, user, id):

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a04',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)
        # print("select")
        try:
            cur.execute("""SELECT * FROM accounts_categories WHERE status =%s ORDER BY id ASC""", [id])
            results = cur.fetchall()
            if results:          
                accounts = []

                for account in results:
                    res = {
                        "category_id": account['id'],
                        "type_id": account['second_layer_id'],
                        "name": account['name']
                    }
                    accounts.append(res)
                    # print(res)

                #The response object
                message = {'status':200,
                           'response':accounts,
                           'description':'Accounts category item records were found'}

                return jsonify(message)
            else:
                message = {'status':404,
                           'error':'aa_a05',
                           'description':'No accounts category record was found!'
                           }
                ErrorLogger().logError(message)
                return jsonify(message)

    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'aa_a06',
                       'description':'Failed to retrieve accounts category records from database. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()

    def get_accounts_sub_categories(self, user, id):

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a07',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)
        # print("select")
        try:
            cur.execute("""SELECT * FROM accounts_sub_categories WHERE status = %s ORDER BY id ASC""", [id])
            results = cur.fetchall()
            if results:          
                sub_cats = []

                for account in results:
                    res = {
                        "id": account['id'],
                        "category_id":account['category_id'],
                        "name": account['name']
                    }
                    sub_cats.append(res)
                    # print(res)

                #The response object
                message = {'status':200,
                           'response':sub_cats,
                           'description':'Accounts sub category item records were found'}

                return jsonify(message)
            else:
                message = {'status':404,
                           'error':'aa_a08',
                           'description':'No accounts sub category record was found!'
                           }
                ErrorLogger().logError(message)
                return jsonify(message)

    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'aa_a09',
                       'description':'Failed to retrieve accounts sub category records from database. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()
    
    def create_account(self, user):
        account = request.form.to_dict()
       
        
        if account == None:
            message = {'status':402,
                       'error':'aa_a10',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message)

        #Try except block to handle execute task
        try:
            account["user_id"] = user["id"]
            account["owner_id"] = ''
            account["entity_id"] = 0
            account["status"] = 0
            
            api_response = Account().create_new_account(account)
            if int(api_response["status"] == 200):
                
                message = {"description":"Account was created successfully",
                           "status":200}
                return jsonify(message)
            else:
                message = {'status':201,
                           'error':'aa_a11',
                           'description':api_response["description"]}
                ErrorLogger().logError(message)
                return jsonify(message)
            
        except Exception as error:
            message = {'status':501,
                       'error':'aa_a12',
                       'description':'Account creation process failed! Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)
             
    def create_new_account(self, account):
        
        if account == None:
            message = {'status':402,
                       'error':'aa_a13',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message
    
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
        
        
         #Try except block to handle execute task
        try:
            # print("accountNumber")
            message = Accounts().create_account(account)

            if int(message["status"]) == 200:
                res = {
                       "account_number":accountNumber, 
                       "account_id":accountId
                    }

                message = {"description":"Account was created successfully",
                           "response":res,
                           "status":200}
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
        
    def setup_default_accounts(self, user):
        details_data = request.form
            
        if details_data == None:
            message = {'status':402,
                       'error':'aa_a32',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message
        
        created_by = user["id"]
        default_bank_account = details_data["default_bank_account"]            
        default_bank_suspense_account = details_data["default_bank_suspense_account"]
        default_mpesa_c2b_utility_account = details_data["default_mpesa_c2b_utility_account"]
       
        default_mpesa_c2b_utility_suspense_account = details_data["default_mpesa_c2b_utility_suspense_account"]
        default_mpesa_b2c_utility_account = details_data["default_mpesa_b2c_utility_account"]
        default_mpesa_b2c_realized_income_account = details_data["default_mpesa_b2c_realized_income_account"]
        default_mpesa_b2c_charges_expense_account = details_data["default_mpesa_b2c_charges_expense_account"]
        default_mpesa_b2c_charges_payable_account = details_data["default_mpesa_b2c_charges_payable_account"]
        default_tax_expense_account = details_data["default_tax_expense_account"]
        default_tax_payable_account = details_data["default_tax_payable_account"]
        default_petty_cash_account = details_data["default_petty_cash_account"]
                
                
        #Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)
        
        #Try except block to handle execute task
        try:
            
            date_setup = Localtime().gettime()
            if default_bank_account != '':
                
                cur.execute("""SELECT default_type_number FROM default_accounts WHERE id = 1 and default_status = 1""")
                account = cur.fetchone()
                if account:
                    pass
                else:
                    
                    cur.execute("""SELECT type, number FROM accounts WHERE id = %s""",(default_bank_account))
                    acc_details = cur.fetchone()
                    if acc_details:
                        account_type = acc_details["type"]
                        account_number = acc_details["number"]
                        
                        cur.execute("""UPDATE default_accounts set default_status = 2, account_type_id = %s, account_number = %s, date_added = %s, added_by = %s WHERE id = 1""", (account_type, account_number, date_setup, created_by))
                        mysql.get_db().commit()
            
            if default_bank_suspense_account != '':
                cur.execute("""SELECT default_status FROM default_accounts WHERE id = 2 and default_status = 1""")
                account = cur.fetchone()
                if account:
                    pass
                else:
                    
                    cur.execute("""SELECT type, number FROM accounts WHERE id = %s""",[default_bank_suspense_account])
                    bnk_suspense_acc_details = cur.fetchone()
                    if bnk_suspense_acc_details:
                        bnk_suspense_account_type = bnk_suspense_acc_details["type"]
                        bnk_suspense_account_number = bnk_suspense_acc_details["number"]
                    
                        cur.execute("""UPDATE default_accounts set default_status = 2, account_type_id = %s, account_number = %s, date_added = %s, added_by = %s WHERE id = 2""", (bnk_suspense_account_type, bnk_suspense_account_number, date_setup, created_by))
                        mysql.get_db().commit()
            
            if default_mpesa_c2b_utility_account != '':
                cur.execute("""SELECT default_status FROM default_accounts WHERE id = 3 and default_status = 1""")
                account = cur.fetchone()
                if account:
                    pass
                else:
                    
                    cur.execute("""SELECT type, number FROM accounts WHERE id = %s""",[default_mpesa_c2b_utility_account])
                    acc_details = cur.fetchone()
                    if acc_details:
                        account_type = acc_details["type"]
                        account_number = acc_details["number"]
                        
                        cur.execute("""UPDATE default_accounts set default_status = 2, account_type_id = %s, account_number = %s, date_added = %s, added_by = %s WHERE id = 3""", (account_type, account_number, date_setup, created_by))
                        mysql.get_db().commit()
            
            if default_mpesa_c2b_utility_suspense_account != '':
                cur.execute("""SELECT default_status FROM default_accounts WHERE id = 4 and default_status = 1""")
                account = cur.fetchone()
                if account:
                    pass
                else:
                    
                    cur.execute("""SELECT type, number FROM accounts WHERE id = %s""",[default_mpesa_c2b_utility_suspense_account])
                    acc_details = cur.fetchone()
                    if acc_details:
                        account_type = acc_details["type"]
                        account_number = acc_details["number"]
                        
                        cur.execute("""UPDATE default_accounts set default_status = 2, account_type_id = %s, account_number = %s, date_added = %s, added_by = %s WHERE id = 4""", (account_type, account_number, date_setup, created_by))
                        mysql.get_db().commit()
                        
                        
            
            if default_mpesa_b2c_utility_account != '':
                cur.execute("""SELECT default_status FROM default_accounts WHERE id = 5 and default_status = 1""")
                account = cur.fetchone()
                if account:
                    pass
                else:
                    
                    cur.execute("""SELECT type, number FROM accounts WHERE id = %s""",[default_mpesa_b2c_utility_account])
                    acc_details = cur.fetchone()
                    if acc_details:
                        account_type = acc_details["type"]
                        account_number = acc_details["number"]
                        
                        cur.execute("""UPDATE default_accounts set default_status = 2, account_type_id = %s, account_number = %s, date_added = %s, added_by = %s WHERE id = 5""", (account_type, account_number, date_setup, created_by))
                        mysql.get_db().commit()
                    
                    
            
            if default_mpesa_b2c_realized_income_account != '':
                cur.execute("""SELECT default_status FROM default_accounts WHERE id = 5 and default_status = 1""")
                account = cur.fetchone()
                if account:
                    pass
                else:
                    
                    cur.execute("""SELECT type, number FROM accounts WHERE id = %s""",[default_mpesa_b2c_realized_income_account])
                    acc_details = cur.fetchone()
                    if acc_details:
                        account_type = acc_details["type"]
                        account_number = acc_details["number"]
                        
                        cur.execute("""UPDATE default_accounts set default_status = 2, account_type_id = %s, account_number = %s, date_added = %s, added_by = %s WHERE id = 6""", (account_type, account_number, date_setup, created_by))
                        mysql.get_db().commit()
            
            if default_mpesa_b2c_charges_expense_account != '':
                cur.execute("""SELECT default_status FROM default_accounts WHERE id = 7 and default_status = 1""")
                account = cur.fetchone()
                if account:
                    pass
                else:
                    
                    cur.execute("""SELECT type, number FROM accounts WHERE id = %s""",[default_mpesa_b2c_charges_expense_account])
                    acc_details = cur.fetchone()
                    if acc_details:
                        account_type = acc_details["type"]
                        account_number = acc_details["number"]
                        
                        cur.execute("""UPDATE default_accounts set default_status = 2, account_type_id = %s, account_number = %s, date_added = %s, added_by = %s WHERE id = 7""", (account_type, account_number, date_setup, created_by))
                        mysql.get_db().commit()
                        
            if default_mpesa_b2c_charges_payable_account != '':
                cur.execute("""SELECT default_status FROM default_accounts WHERE id = 8 and default_status = 1""")
                account = cur.fetchone()
                if account:
                    pass
                else:
                    
                    cur.execute("""SELECT type, number FROM accounts WHERE id = %s""",[default_mpesa_b2c_charges_payable_account])
                    acc_details = cur.fetchone()
                    if acc_details:
                        account_type = acc_details["type"]
                        account_number = acc_details["number"]
                        
                        cur.execute("""UPDATE default_accounts set default_status = 2, account_type_id = %s, account_number = %s, date_added = %s, added_by = %s WHERE id = 8""", (account_type, account_number, date_setup, created_by))
                        mysql.get_db().commit()
                        
                        
            
            if default_tax_expense_account != '':
                cur.execute("""SELECT default_status FROM default_accounts WHERE id = 9 and default_status = 1""")
                account = cur.fetchone()
                if account:
                    pass
                else:
                    
                    cur.execute("""SELECT type, number FROM accounts WHERE id = %s""",[default_tax_expense_account])
                    acc_details = cur.fetchone()
                    if acc_details:
                        account_type = acc_details["type"]
                        account_number = acc_details["number"]
                        
                        cur.execute("""UPDATE default_accounts set default_status = 2, account_type_id = %s, account_number = %s, date_added = %s, added_by = %s WHERE id = 9""", (account_type, account_number, date_setup, created_by))
                        mysql.get_db().commit()
                        
                        
            
            if default_tax_payable_account != '':
                cur.execute("""SELECT default_status FROM default_accounts WHERE id = 10 and default_status = 1""")
                account = cur.fetchone()
                if account:
                    pass
                else:
                    
                    cur.execute("""SELECT type, number FROM accounts WHERE id = %s""",[default_tax_payable_account])
                    acc_details = cur.fetchone()
                    if acc_details:
                        account_type = acc_details["type"]
                        account_number = acc_details["number"]
                        
                        cur.execute("""UPDATE default_accounts set default_status = 2, account_type_id = %s, account_number = %s, date_added = %s, added_by = %s WHERE id = 10""", (account_type, account_number, date_setup, created_by))
                        mysql.get_db().commit()
            
            if default_petty_cash_account != '':
                cur.execute("""SELECT default_status FROM default_accounts WHERE id = 11 and default_status = 1""")
                account = cur.fetchone()
                if account:
                    pass
                else:
                    
                    cur.execute("""SELECT type, number FROM accounts WHERE id = %s""",[default_petty_cash_account])
                    acc_details = cur.fetchone()
                    if acc_details:
                        account_type = acc_details["type"]
                        account_number = acc_details["number"]
                        
                        cur.execute("""UPDATE default_accounts set default_status = 2, account_type_id = %s, account_number = %s, date_added = %s, added_by = %s WHERE id = 11""", (account_type, account_number, date_setup, created_by))
                        mysql.get_db().commit()

            message = {'status':200,
                       'description':'Default Account setup process was successful!'}
          
            return message

        except Exception as error:
            message = {'status':501,
                       'error':'aa_a35',
                       'description':'Default Account setup process failed! Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        
    def get_accounts(self,user, id):

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a17',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)
        
        try:
            cur.execute("""SELECT * FROM accounts WHERE status = %s ORDER BY id ASC""", [id])
            results = cur.fetchall() 
            if results:           

                accounts = []
                count = 0
                for account in results:
                    #get created by name
                    createdby_id = account['createdby']
                    cur.execute("""SELECT first_name, last_name FROM administrator_details WHERE user_id= %s""", [createdby_id])
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
                            'description':'Account record was found!'}

                return jsonify(message)

            else:
                message = {'status':404,
                           'error':'aa_a18',
                           'description':'No account record was found!'}
                ErrorLogger().logError(message)
                return jsonify(message)

    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'aa_a19',
                       'description':'Failed to retrieve accounts record from database.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()

    def get_account(self, user, id):       
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a20',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)
    
        try:
            cur.execute("""SELECT * FROM accounts WHERE number = %s""", [id])
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
                cur.execute("""SELECT first_name, last_name FROM administrator_details WHERE user_id= %s""", [createdby_id])
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
                    "last_amount": account['last_amount'],
                    "number": account['number'],
                    "mainaccount": account['mainaccount'],
                    "description": account['description'],
                    "notes": account['notes'],
                    "balance": float(account['balance']),
                    "datecreated": account['datecreated'],
                    "createdby": user_name,
                    "createdby_id": createdby_id,

                }
          

                #The response object
                message = {"description":"Account details record was found",
                           "response":res,
                           "status":200}
                return message
            
            else:
                message = {"description":"Account details record was not found",
                           'error':'aa_a21',
                           "status":201}
                ErrorLogger().logError(message)
                return message

        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'aa_a22',
                       'description':'Account details record fetching failed! Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()

    def get_default_accounts(self,user, id):
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a23',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)
       
        try:
            cur.execute("""SELECT d.id, a.id as accountid, d.default_name, a.name, a.reference_no, a.type, a.type_name, a.category_name, a.currency, a.number, a.mainaccount, a.description, a.notes, a.balance, a.datecreated, a.createdby FROM default_accounts As d INNER JOIN accounts AS a ON d.account_number = a.number WHERE d.default_status = %s """, [id])
            results = cur.fetchall()
         
            accounts = []

            for account in results:
                res = {
                    "id": account['id'],
                    "accountid": account['accountid'],
                    "defaultname": account['default_name'],
                    "accountname": account['name'],
                    "referenceno": account['reference_no'],
                    "type": account['type'],
                    "type_name": account['type_name'],
                    "category_name": account['category_name'],
                    "currency": account['currency'],
                    "number": account['number'],
                    "mainaccount": account['mainaccount'],
                    "description": account['description'],
                    "notes": account['notes'],
                    "balance": account['balance'],
                    "datecreated": account['datecreated'],
                    "createdby": account['createdby'],

                }
                accounts.append(res)
                # print(res)

            #The response object
            message = {'status':200,
                        'response':accounts,
                        'description':'Account record was found!'}

            return jsonify(message)
    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'aa_a24',
                       'description':'Account details record fetching failed! Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()

    def approve_new_account(self, user):
        #Get the request data from the front-end
        # account = request.form
        account = request.get_json()

        if account == None:
            message = {'status':402,
                       'error':'aa_a25',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message)

        account_id = account["id"]
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a26',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)

        #Try exept block to handle the insert opeartion
        try:   
            dateApproved = Localtime().gettime()
            approvedBy = user["id"]        
            cur.execute("""UPDATE accounts set status=1, approvedon = %s, approvedby =%s WHERE id = %s""", ([dateApproved, approvedBy, account_id]))
            mysql.get_db().commit()

            message = {'status':200,
                       'description':'Record was approved successfully!'}
            return jsonify(message)

        except Exception as error:         
            message = {'status':501,
                       'error':'aa_a27',
                        'description':'Failed to approve new account.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
                cur.close()

    def get_specific_accounts(self,user):
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
            cur.execute("""SELECT * FROM accounts WHERE category_id = %s AND status = %s """, [type, status])
            results = cur.fetchall()
            cur.close()

            wallets = []
            for account in results:
                res = {
                    "accountid": account['id'],
                    "accountname": account['name'],
                    "referenceno": account['reference_no'],
                    "type": account['type'],
                    "currency": account['currency'],
                    "number": account['number'],
                    "mainaccount": account['mainaccount'],
                    "description": account['description'],
                    "notes": account['notes'],
                    "balance": account['balance'],
                    "datecreated": account['datecreated'],
                    "createdby": account['createdby'],

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
                       'description':'Account details record fetching failed! Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()

    def get_specific_accounts_by_type(self,user):
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
                    "accountid": account['id'],
                    "accountname": account['name'],
                    "referenceno": account['reference_no'],
                    "type": account['type'],
                    "currency": account['currency'],
                    "number": account['number'],
                    "mainaccount": account['mainaccount'],
                    "description": account['description'],
                    "notes": account['notes'],
                    "balance": account['balance'],
                    "datecreated": account['datecreated'],
                    "createdby": account['createdby'],

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
                       'description':'Account details record fetching failed! Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()
            
    def get_specific_account(self,user, state, type, id):

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a30',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)
       
        try:
            cur.execute("""SELECT * FROM accounts WHERE status = %s AND account_category = %s AND owner_id = %s""", [state,type,id])
            results = cur.fetchall()
            cur.close()

            wallets = []
            for account in results:
                res = {
                    "accountid": account['id'],
                    "accountname": account['name'],
                    "referenceno": account['reference_no'],
                    "currency": account['currency'],
                    "actualbalance": account['actual_balance'],
                    "availablebalance": account['available_balance'],                    

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
                       'error':'aa_a31',
                       'description':'Account details record fetching failed! Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()
 
    def approve_default_account(self, user):
            #Get the request data from the front-end
        # account = request.form
        account = request.get_json()

        if account == None:
            message = {'status':402,
                       'error':'aa_a33',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message)

        entryid = account["id"]
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a34',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)

        #Try exept block to handle the insert opeartion
        try:   
            dateApproved = Localtime().gettime()
            approvedBy = user["id"]        
            cur.execute("""UPDATE default_accounts set default_status=1, add_approved_on = %s, add_approved_by =%s WHERE id = %s""", ([dateApproved, approvedBy, entryid]))
            mysql.get_db().commit()

            message = {'status':200,
                       'description':'Record was approved successfully!'}
            return jsonify(message)

        except Exception as error:         
            message = {'status':501,
                       'error':'aa_a35',
                        'description':'Failed to approve new account.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
                cur.close()

    def get_funds_transfer_accounts(self,user):
        details = request.get_json()
        if details == None:
            message = {'status':402,
                       'error':'aa_a36',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return jsonify(message)

        status = details["status"]
        
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'aa_a37',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return jsonify(message)
        # print("select")
        try:
            bank_accs = 1
            momo_accs = 3
            petty_accs = 4
            expenses_accs = 14
            shareholders_accs = 12
            partner_payable_accs = 19

            
            cur.execute("""SELECT * FROM accounts WHERE category_id = %s OR category_id = %s  OR category_id = %s OR category_id = %s OR category_id = %s OR category_id = %s AND status = %s """, [bank_accs, momo_accs, petty_accs, shareholders_accs, expenses_accs, partner_payable_accs, status])
            results = cur.fetchall()
            cur.close()

            wallets = []
            for account in results:
                res = {
                    "accountid": account['id'],
                    "accountname": account['name'],
                    "referenceno": account['reference_no'],
                    "type": account['type'],
                    "currency": account['currency'],
                    "number": account['number'],
                    "mainaccount": account['mainaccount'],
                    "description": account['description'],
                    "notes": account['notes'],
                    "balance": account['balance'],
                    "datecreated": account['datecreated'],
                    "createdby": account['createdby'],

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
                       'error':'aa_a38',
                       'description':'Account details record fetching failed! Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()