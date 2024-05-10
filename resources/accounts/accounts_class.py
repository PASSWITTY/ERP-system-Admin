from flask import request, Response, json, jsonify
import os
from main import mysql, app
from datetime import datetime
from resources.payload.payload import Localtime
from resources.logs.logger import ErrorLogger


class Accounts():
    
    def get_loan_asset_account(self, details):
        #Get the request data

        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       "status": 402}
            return message
        
        customer_id = details["customer_id"]
        loan_id = details["loan_id"]
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "status": 500}
            return message
        
        #Get loan asset account
        cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =5 AND owner_id = %s AND entity_id = %s """, (customer_id, loan_id))
        get_loan_asset_account = cur.fetchone() 
        if get_loan_asset_account:
            loan_asset_account = get_loan_asset_account["number"]
            message =  {'status':200,
                        'data':loan_asset_account,                             
                        }
            return message
        
        else:
            loan_asset_account = 0
            message = {'status':402,
                        'error':'cr_d03',
                        'data':loan_asset_account,
                        'description':'Task was not successful. Asset loan account is missing',                               
                        }
            ErrorLogger().logError(message) 
            return message
    
    def get_receivable_account(self, details):
        #Get the request data

        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       "status": 402}
            return message
        
        customer_id = details["customer_id"]
        loan_id = details["loan_id"]
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "status": 500}
            return message
        
        #Get Customer Receivable Account - Check if customer receivable account exists for this specific loan product          
        cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =3 AND owner_id = %s AND entity_id = %s""", (customer_id, loan_id))
        get_receivable_account = cur.fetchone() 
        if get_receivable_account:
            receivable_account = get_receivable_account["number"]
            message =  {'status':200,
                        'data':receivable_account,                             
                        }
            return message
        
        else:
            receivable_account = 0
            message = {'status':402,
                        'error':'cr_d08',
                        'data':receivable_account,
                        'description':'Task was not successful. Receivable account is missing',                               
                        }
            ErrorLogger().logError(message) 
            return message

    def get_interest_earned_account(self, details):
        #Get the request data

        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       "status": 402}
            return message
        
        interest_id = details["interest_id"]
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "status": 500}
            return message
        
        #Get interest earned income account
        cur.execute("""SELECT number FROM accounts WHERE status =1 AND sub_category_id=2 AND type =14 AND owner_id = %s """, [interest_id])
        get_interest_earned_account = cur.fetchone() 
        if get_interest_earned_account:
            interest_earned_account = get_interest_earned_account["number"]
            message =  {'status':200,
                        'data':interest_earned_account,                             
                        }
            return message
        
        else:
            interest_earned_account = 0
            message = {'status':402,
                        'error':'cr_d09',
                        'data':interest_earned_account,
                        'description':'Task was not successful. Interest Earned Account is missing',                               
                        }
            ErrorLogger().logError(message) 
            return message
        
    def create_account(self, account):
        #Get the request data from frontend
        # account = request.get_json()

        if account == None:
            message = {"description":"Transaction is missing some details!", 
                       "status": 402}
            return message

        accountId = account["id"]
        accountNumber = account["account_number"] 
        accountName = account["name"]
        typeId = int(account.get("accountTypeId"))
        categoryId = account.get("accountCategoryId")
        subCategoryId = account.get("accountSubCategoryId")
        mainaccount = account.get("main_account")
        openingBalance = float(account["opening_balance"])    
        ownerid = account["ownerid"]
        entityid = account["entityid"]    
        notes = account["notes"]
        description = account["description"]
        referenceNumber = account["reference_number"]        
             
        createdby = account["createdby"]
        status = account["status"]
                    
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "status": 500}
            return message
         #Try except block to handle the insert opeartion
        try:
            #Get default currency
            cur.execute("""SELECT id FROM currency WHERE default_currency =1""")
            curr_res = cur.fetchall()
           
            for default_curr in curr_res:
                currency = default_curr['id']  

            #get account type name
            cur.execute("""SELECT a.name, a.id, p.id AS class_id, p.main_type_name AS class_name FROM accounts_types as a INNER JOIN account_main_types As p ON a.first_layer_id = p.id WHERE a.id= %s""", [typeId])
            typedetails = cur.fetchone()
            typeName = typedetails['name']   
            classId = typedetails['class_id']  
            className = typedetails['class_name'] 
            type = typedetails['id']
            
            
            #get account category
            cur.execute("""SELECT name FROM accounts_categories WHERE id= %s""", [categoryId])
            catdetails = cur.fetchone()
            categoryName = catdetails['name']     
            dateCreated = datetime.now()
            
            cur.execute("""INSERT INTO accounts (id, name, reference_no, balance, number, type, type_name, type_id, category_name, category_id, sub_category_id, class_name, class_id, owner_id, entity_id, currency, mainaccount, description, notes, datecreated, createdby, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",  (accountId, accountName, referenceNumber, openingBalance, accountNumber, type, typeName, typeId, categoryName, categoryId, subCategoryId, className, classId, ownerid, entityid, currency, mainaccount, description, notes, dateCreated, createdby, status))
            mysql.get_db().commit()
          
            message = {"description":"Account was created successfully",
                       "status":200}
            return message

        except Exception as error:
            message = {"status":501,
                       "description":"Transaction execution failed. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            cur.close()
    
    def accountNumber(self, typeId):       
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)
        
        typeId = int(typeId)
    
        try:  

            if typeId ==1:#generate Cash-and-cash-equivalent account

                cur.execute("""SELECT number FROM generate_bank_account_numbers ORDER BY number DESC LIMIT 1""")
                acc_num = cur.fetchone()
                if acc_num == None:

                    cur.execute("""SELECT start FROM accounts_series where id=1""")
                    acc_series= cur.fetchone()
                    if acc_series:
                        account_number = acc_series["start"]

                    date_created = Localtime().gettime()
                    cur.execute("""INSERT INTO generate_bank_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                    mysql.get_db().commit() 
                    account_number = str(cur.lastrowid)
                    cur.close()
                else:
                    account_number = int(acc_num["number"]) + 1
                    date_created = Localtime().gettime()
                    cur.execute("""INSERT INTO generate_bank_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                    mysql.get_db().commit() 
                    account_number = str(cur.lastrowid)

            elif typeId ==2:#generate inventory account

                cur.execute("""SELECT number FROM generate_inventory_account_numbers ORDER BY number DESC LIMIT 1""")
                acc_num = cur.fetchone()
                if acc_num == None:

                    cur.execute("""SELECT start FROM accounts_series where id=2""")
                    acc_series= cur.fetchone()
                    if acc_series:
                        account_number = acc_series["start"]

                    date_created = Localtime().gettime()
                    cur.execute("""INSERT INTO generate_inventory_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                    mysql.get_db().commit() 
                    account_number = str(cur.lastrowid)
                    cur.close()
                else:
                    account_number = int(acc_num["number"]) + 1
                    date_created = Localtime().gettime()
                    cur.execute("""INSERT INTO generate_inventory_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                    mysql.get_db().commit() 
                    account_number = str(cur.lastrowid)
            
            elif typeId ==3:#generate receivable account

                cur.execute("""SELECT number FROM generate_receivable_account_numbers ORDER BY number DESC LIMIT 1""")
                acc_num = cur.fetchone()
                if acc_num == None:

                    cur.execute("""SELECT start FROM accounts_series where id=3""")
                    acc_series= cur.fetchone()
                    if acc_series:
                        account_number = acc_series["start"]

                    date_created = Localtime().gettime()
                    cur.execute("""INSERT INTO generate_receivable_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                    mysql.get_db().commit() 
                    account_number = str(cur.lastrowid)
                    cur.close()
                else:
                    account_number = int(acc_num["number"]) + 1
                    date_created = Localtime().gettime()
                    cur.execute("""INSERT INTO generate_receivable_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                    mysql.get_db().commit() 
                    account_number = str(cur.lastrowid)
            
            elif typeId ==4:#generate prepaid expenses account
                
                cur.execute("""SELECT number FROM generate_prepaidexpenses_account_numbers ORDER BY number DESC LIMIT 1""")
                acc_num = cur.fetchone()
                if acc_num == None:

                    cur.execute("""SELECT start FROM accounts_series where id=4""")
                    acc_series= cur.fetchone()
                    if acc_series:
                        account_number = acc_series["start"]

                    date_created = Localtime().gettime()
                    cur.execute("""INSERT INTO generate_prepaidexpenses_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                    mysql.get_db().commit() 
                    account_number = str(cur.lastrowid)
                    cur.close()
                else:
                    account_number = int(acc_num["number"]) + 1
                    date_created = Localtime().gettime()
                    cur.execute("""INSERT INTO generate_prepaidexpenses_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                    mysql.get_db().commit() 
                    account_number = str(cur.lastrowid)
            
            elif typeId ==5:#generate loan marketable securities account
                pass
                # cur.execute("""SELECT number FROM generate_loanportfolio_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=5""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_loanportfolio_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_loanportfolio_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)

            elif typeId ==6:#generate property equipment account
                pass
                # cur.execute("""SELECT number FROM generate_othercurrentasset_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=6""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_othercurrentasset_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_othercurrentasset_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)

            elif typeId ==7:#generate intangible assets account
                pass
                # cur.execute("""SELECT number FROM generate_fixedasset_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=7""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_fixedasset_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_fixedasset_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)

            elif typeId ==8:#generate other investments account
                pass
                # cur.execute("""SELECT number FROM generate_payable_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=8""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_payable_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_payable_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)

            elif typeId ==9:#generate payable account
                
                cur.execute("""SELECT number FROM generate_payable_account_numbers ORDER BY number DESC LIMIT 1""")
                acc_num = cur.fetchone()
                if acc_num == None:

                    cur.execute("""SELECT start FROM accounts_series where id=9""")
                    acc_series= cur.fetchone()
                    if acc_series:
                        account_number = acc_series["start"]

                    date_created = Localtime().gettime()
                    cur.execute("""INSERT INTO generate_payable_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                    mysql.get_db().commit() 
                    account_number = str(cur.lastrowid)
                    cur.close()
                else:
                    account_number = int(acc_num["number"]) + 1
                    date_created = Localtime().gettime()
                    cur.execute("""INSERT INTO generate_payable_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                    mysql.get_db().commit() 
                    account_number = str(cur.lastrowid)
            
            #There is not type 10
            elif typeId ==11:#generate short term loan account

                cur.execute("""SELECT number FROM generate_shorttermloan_account_numbers ORDER BY number DESC LIMIT 1""")
                acc_num = cur.fetchone()
                if acc_num == None:

                    cur.execute("""SELECT start FROM accounts_series where id=11""")
                    acc_series= cur.fetchone()
                    if acc_series:
                        account_number = acc_series["start"]

                    date_created = Localtime().gettime()
                    cur.execute("""INSERT INTO generate_shorttermloan_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                    mysql.get_db().commit() 
                    account_number = str(cur.lastrowid)
                    cur.close()
                else:
                    account_number = int(acc_num["number"]) + 1
                    date_created = Localtime().gettime()
                    cur.execute("""INSERT INTO generate_shorttermloan_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                    mysql.get_db().commit() 
                    account_number = str(cur.lastrowid)

            elif typeId ==12:#generate long term loan account
                
                cur.execute("""SELECT number FROM generate_longtermloan_account_numbers ORDER BY number DESC LIMIT 1""")
                acc_num = cur.fetchone()
                if acc_num == None:

                    cur.execute("""SELECT start FROM accounts_series where id=12""")
                    acc_series= cur.fetchone()
                    if acc_series:
                        account_number = acc_series["start"]

                    date_created = Localtime().gettime()
                    cur.execute("""INSERT INTO generate_longtermloan_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                    mysql.get_db().commit() 
                    account_number = str(cur.lastrowid)
                    cur.close()
                else:
                    account_number = int(acc_num["number"]) + 1
                    date_created = Localtime().gettime()
                    cur.execute("""INSERT INTO generate_longtermloan_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                    mysql.get_db().commit() 
                    account_number = str(cur.lastrowid)

            elif typeId ==13:#generate accrued expenses account
                pass
                # cur.execute("""SELECT number FROM generate_shareholders_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=13""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_shareholders_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_shareholders_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)

            elif typeId ==14:#generate customer prepayments account
                pass
                # cur.execute("""SELECT number FROM generate_income_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=14""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_income_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_income_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)

            elif typeId ==15:#generate other long term liabilities account
                pass
                # cur.execute("""SELECT number FROM generate_costofgoods_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=15""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_costofgoods_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_costofgoods_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)

            elif typeId ==16:#generate equity account
                pass
                # cur.execute("""SELECT number FROM generate_expenses_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=16""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_expenses_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_expenses_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)

            elif typeId ==17:#generate retained earnings account
                pass
                # cur.execute("""SELECT number FROM generate_otherincome_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=17""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_otherincome_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_otherincome_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid) 
            
            elif typeId ==18:#generate income account
                pass
                # cur.execute("""SELECT number FROM generate_otherexpenses_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=18""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_otherexpenses_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_otherexpenses_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                    
            elif typeId ==19:#generate discounts account
                pass
                # cur.execute("""SELECT number FROM generate_nonposting_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=19""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_nonposting_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_nonposting_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)

            elif typeId ==21:#generate expenses account
                pass
                # cur.execute("""SELECT number FROM generate_nonposting_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=19""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_nonposting_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_nonposting_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)

            elif typeId ==22:#generate other expenses account
                pass
                # cur.execute("""SELECT number FROM generate_nonposting_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=19""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_nonposting_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_nonposting_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
            
            elif typeId ==23:#generate other income account
                pass
                # cur.execute("""SELECT number FROM generate_nonposting_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=19""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_nonposting_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_nonposting_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)

            elif typeId ==24:#generate tax expenses account
                pass
                # cur.execute("""SELECT number FROM generate_nonposting_account_numbers ORDER BY number DESC LIMIT 1""")
                # acc_num = cur.fetchone()
                # if acc_num == None:

                #     cur.execute("""SELECT start FROM accounts_series where id=19""")
                #     acc_series= cur.fetchone()
                #     if acc_series:
                #         account_number = acc_series["start"]

                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_nonposting_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                #     cur.close()
                # else:
                #     account_number = int(acc_num["number"]) + 1
                #     date_created = Localtime().gettime()
                #     cur.execute("""INSERT INTO generate_nonposting_account_numbers (number, date_created) VALUES (%s, %s)""",(account_number, date_created))
                #     mysql.get_db().commit() 
                #     account_number = str(cur.lastrowid)
                
            return account_number
        except Exception as error:
            message = {"status":501,
                       "description":"Error generating account number. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            cur.close() 
    
    def bnk_account(self):
    
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()            
        except:
            message = {"status":500,
                       "data":0,
                       "description":"Couldn't connect to the Database!"}
            return message

        try:
            cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number= 1""")
            bnk_ac = cur.fetchone()
            if bnk_ac:
                bnk_bank_account = bnk_ac["account_number"]

                message = {"description":"Default Bank Account was found!", 
                           "data":bnk_bank_account,
                           "status":200
                           }

                return message
            else:
                message = {
                           "description":"Default bank account has not been setup!", 
                           "status":201
                           }
                return message
             
        except Exception as error:
            message = {"status":501,
                       "description":"Transaction failed! Error description " + format(error)}
            return message
        finally:
            cur.close()
            
    def b2c_account(self):

        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()            
        except:
            message = {"status":500,
                       "data":0,
                       "description":"Couldn't connect to the Database!"}
            return message

        try:
            cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number= 5""")
            bnk_ac = cur.fetchone()
            if bnk_ac:
                b2c_bank_account = bnk_ac["account_number"]

                message = {"description":"Default B2C Utility Account was found!", 
                           "data":b2c_bank_account,
                           "status":200
                           }

                return message
            else:
                message = {
                           "description":"Default B2C utility account has not been setup!", 
                           "status":201
                           }
                return message
             
        except Exception as error:
            message = {"status":501,
                       "description":"Transaction failed! Error description " + format(error)}
            return message
        finally:
            cur.close()

    def c2b_paybill_account(self):
    
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()            
        except:
            message = {"status":500,
                       "description":"Couldn't connect to the Database!"}
            return message

        try:
            cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number=3""")
            def_ac = cur.fetchone()
            if def_ac:
                c2b_utility_account = def_ac["account_number"]

                message = {"description":"Default C2B Utility Account was Fetched!", 
                           "data":c2b_utility_account,
                           "status":200}

                return message
            else:
                message = {"description":"Default C2B Utility Account has not been setup!", 
                           "status":201}
                return message
             
        except Exception as error:
            message = {"status":501,
                       "description":"Transaction failed! Error description " + format(error)}
            return message
        finally:
            cur.close()
            
    def c2b_till_account(self):
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()            
        except:
            message = {"status":500,
                       "description":"Couldn't connect to the Database!"}
            return message

        try:
            cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number=17""")
            def_ac = cur.fetchone()
            if def_ac:
                c2b_till_account = def_ac["account_number"]

                message = {"description":"Default C2B Till Account was Fetched!", 
                           "data":c2b_till_account,
                           "status":200}

                return message
            else:
                message = {"description":"Default C2B Till Account has not been setup!", 
                           "status":201}
                return message
             
        except Exception as error:
            message = {"status":501,
                       "description":"Transaction failed! Error description " + format(error)}
            return message
        finally:
            cur.close()
    
    def c2b_suspense_account(self):
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()            
        except:
            message = {"status":500,
                       "description":"Couldn't connect to the Database!"}
            return message

        try:
            cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number=4""")
            def_ac = cur.fetchone()
            if def_ac:
                c2b_utility_account = def_ac["account_number"]

                message = {"description":"Default C2B Utility Suspense Account was Fetched!", 
                           "data":c2b_utility_account,
                           "status":200}

                return message
            else:
                message = {"description":"Default C2B Utility Suspense Account has not been setup!", 
                           "status":201}
                return message
             
        except Exception as error:
            message = {"status":501,
                       "description":"Transaction failed! Error description " + format(error)}
            return message
        finally:
            cur.close()
            
    def b2c_payable_account(self):
            
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()            
        except:
            message = {"status":500,
                       "description":"Couldn't connect to the Database!"}
            return message

        try:
            cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number=8""")
            def_ac = cur.fetchone()
            if def_ac:
                b2c_payable_account = def_ac["account_number"]

                message = {"description":"Default B2C Payable Account was Fetched!", 
                           "data":b2c_payable_account,
                           "status":200}

                return message
            else:
                message = {"description":"Default B2C Payable Account has not been setup!", 
                           "status":201}
                return message
             
        except Exception as error:
            message = {"status":501,
                       "description":"Transaction failed! Error description " + format(error)}
            return message
        finally:
            cur.close()
            
    def b2c_income_account(self):
            
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()            
        except:
            message = {"status":500,
                       "description":"Couldn't connect to the Database!"}
            return message

        try:
            cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number=6""")
            def_ac = cur.fetchone()
            if def_ac:
                b2c_income_account = def_ac["account_number"]

                message = {"description":"Default B2C Earned Income Account was Fetched!", 
                           "data":b2c_income_account,
                           "status":200}

                return message
            else:
                message = {"description":"Default B2C Income Account has not been setup!", 
                           "status":201}
                return message
             
        except Exception as error:
            message = {"status":501,
                       "description":"Transaction failed! Error description " + format(error)}
            return message
        finally:
            cur.close()
        
    def mpesa_account(self):
    
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()            
        except:
            message = {"status":500,
                       "data":0,
                       "description":"Couldn't connect to the Database!"}
            return message

        try:
            #Mpesa mobile number account used to track mpesa transactions
            cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number= 13""")
            momo_ac = cur.fetchone()
            if momo_ac:
                momo_ac_account = momo_ac["account_number"]

                message = {"description":"Default Mpesa Account was found!", 
                           "data":momo_ac_account,
                           "status":200
                           }

                return message
            else:
                message = {
                           "description":"Default Mpesa account has not been setup!", 
                           "status":201
                           }
                return message
             
        except Exception as error:
            message = {"status":501,
                       "description":"Transaction failed! Error description " + format(error)}
            return message
        finally:
            cur.close()
            
    def airtime_stock_account(self):
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()            
        except:
            message = {"status":500,
                       "data":0,
                       "description":"Couldn't connect to the Database!"}
            return message

        try:
            cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number= 14""")
            ac = cur.fetchone()
            if ac:
                ac_no = ac["account_number"]

                message = {"description":"Default airtime stock account was found!", 
                           "data":ac_no,
                           "status":200
                           }

                return message
            else:
                message = {
                           "description":"Default airtime stock account has not been setup!", 
                           "status":201
                           }
                return message
             
        except Exception as error:
            message = {"status":501,
                       "description":"Transaction failed! Error description " + format(error)}
            return message
        finally:
            cur.close()
              
    def airtime_cog_account(self):
            
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()            
        except:
            message = {"status":500,
                       "data":0,
                       "description":"Couldn't connect to the Database!"}
            return message

        try:
            cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number= 15""")
            ac = cur.fetchone()
            if ac:
                ac_no = ac["account_number"]

                message = {"description":"Default airtime cog account was found!", 
                           "data":ac_no,
                           "status":200
                           }

                return message
            else:
                message = {
                           "description":"Default airtime cog account has not been setup!", 
                           "status":201
                           }
                return message
             
        except Exception as error:
            message = {"status":501,
                       "description":"Transaction failed! Error description " + format(error)}
            return message
        finally:
            cur.close()
            
    def airtime_income_realized_account(self):
            
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()            
        except:
            message = {"status":500,
                       "data":0,
                       "description":"Couldn't connect to the Database!"}
            return message

        try:
            cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number= 18""")
            ac = cur.fetchone()
            if ac:
                ac_no = ac["account_number"]

                message = {"description":"Default airtime income realized account was found!", 
                           "data":ac_no,
                           "status":200
                           }

                return message
            else:
                message = {
                           "description":"Default airtime income realized account has not been setup!", 
                           "status":201
                           }
                return message
             
        except Exception as error:
            message = {"status":501,
                       "description":"Transaction failed! Error description " + format(error)}
            return message
        finally:
            cur.close()
            
    def airtime_income_earned_account(self):
            
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()            
        except:
            message = {"status":500,
                       "data":0,
                       "description":"Couldn't connect to the Database!"}
            return message

        try:
            cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number= 16""")
            ac = cur.fetchone()
            if ac:
                ac_no = ac["account_number"]

                message = {"description":"Default airtime income earned account was found!", 
                           "data":ac_no,
                           "status":200
                           }

                return message
            else:
                message = {
                           "description":"Default airtime income earned account has not been setup!", 
                           "status":201
                           }
                return message
             
        except Exception as error:
            message = {"status":501,
                       "description":"Transaction failed! Error description " + format(error)}
            return message
        finally:
            cur.close()


    