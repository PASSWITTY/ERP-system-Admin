from flask import request, Response, json, jsonify
from main import mysql, app
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.transactions.bookkeeping import DebitCredit
from resources.accounts.accounts_class import Accounts

class MobilePhoneCashSales():
          
    def create_cash_sales(self, user):
        #Get the request data 
        request_data = request.get_json()       
        
        validated_data = request_data
        # validated_data, error_messages = self.reg_supplier.serialize_register_data(data)
        # if error_messages:
        #     return jsonify({"error": error_messages}), 400
        
        sales_date = validated_data["sales_date"]
        payment_mothod = validated_data["payment_mothod"]
        customer_name = validated_data["customer_name"]
        customer_number = validated_data["customer_mobile_number"]
        customer_email = validated_data["customer_email"]
        sales_remarks = validated_data["sales_remarks"]
        product_details = json.dumps(validated_data["product_details"])
        
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
            #Get sales agent distribution center details
            agent_id = user['id']
            cur.execute("""SELECT distribution_center_id FROM user_details WHERE user_id = %s """, (agent_id))
            agent_details = cur.fetchone()
            if agent_details:
                distribution_center_id = agent_details["distribution_center_id"]
            else:
                distribution_center_id = ''
                message = {"description":"Agent does not belong to a distribution center",
                           "status":404}
                return message
            
            total_sales_amount = 0
            total_net_sales_amount = 0
            total_buying_price_amount = 0
            total_discount_amount = 0
            
            
            phone_model_details = json.loads(product_details)                
            for phone_model_detail in phone_model_details:
                model_id = phone_model_detail["model_id"]
                imei_1 = phone_model_detail["imei_1"]
                quantity = 1
                
                #get specific phone global_id
                cur.execute("""SELECT global_id FROM mobile_phones_transit_stock_received WHERE imei_1 = %s """, (imei_1))
                phone_details = cur.fetchone() 
                if phone_details:
                    global_id = phone_details["global_id"]
                else:
                    global_id = ''
                    message = {"description":"This phone does not have global id",
                               "status":404}
                    return message
                
                #get specific phone buying price
                
                cur.execute("""SELECT price_per_unit FROM cash_stock_purchase_models WHERE model_id = %s AND global_id = %s """, (model_id, global_id))
                get_phone_buying_price = cur.fetchone() 
                if get_phone_buying_price:
                    price_per_unit = float(get_phone_buying_price["price_per_unit"])
                else:
                    price_per_unit = 0
                    message = {"description":"This phone does not have global id",
                               "status":404}
                    return message
                
                cur.execute("""SELECT id, price_amount, discount_amount, final_price FROM distribution_center_mobilephone_model_prices WHERE status =1 AND model_id = %s AND distribution_center_id = %s """, (model_id, distribution_center_id))
                get_phone_model_price = cur.fetchone() 
                if get_phone_model_price:
                    price_amount = float(get_phone_model_price["price_amount"])
                    discount_amount = float(get_phone_model_price["discount_amount"])
                    final_price = float(get_phone_model_price["final_price"])
                else:
                    price_amount = 0
                    discount_amount = 0
                    final_price = 0
                    
                total_sellingprice_per_model = price_amount * quantity
                total_discount_amount_per_model = discount_amount * quantity
                total_final_price_per_model = final_price * quantity
                
                total_buyingprice_per_model = price_per_unit * quantity
                
                total_sales_amount = total_sales_amount + total_sellingprice_per_model
                total_net_sales_amount = total_net_sales_amount + total_final_price_per_model
                total_buying_price_amount = total_buying_price_amount + total_buyingprice_per_model
                total_discount_amount = total_discount_amount + total_discount_amount_per_model 
                       
                    
            status = 2 #pending approval
            created_date = Localtime().gettime()
            
            #fetch default bank account
            ##########################UPDATE THIS TO => fetch cash and cash equivalent account as per PAYMENT METHOD SELECTED. 
            bnk_acc_response = Accounts().bnk_account()
            if int(bnk_acc_response["status"]) == 200:
                bank_account = bnk_acc_response["data"]
            else:
                message = {'status':501,
                            'description':"Couldn't fetch default bank account!"}
                return message
            
            #Fetch default receivable account
            rec_acc_response = Accounts().receivable_account()
            if int(rec_acc_response["status"]) == 200:
                receivable_account = rec_acc_response["data"]
            else:
                message = {'status':501,
                            'description':"Couldn't fetch default receivable account!"}
                return message
            
            #Fetch default tax expense account
            tax_expense_response = Accounts().receivable_account()
            if int(tax_expense_response["status"]) == 200:
                tax_expense_account = tax_expense_response["data"]
            else:
                message = {'status':501,
                            'description':"Couldn't fetch default tax expense account!"}
                return message
            
            #Fetch default tax payable account
            tax_payable_response = Accounts().taxpayable_account()
            if int(tax_payable_response["status"]) == 200:
                tax_payable_account = tax_payable_response["data"]
            else:
                message = {'status':501,
                            'description':"Couldn't fetch default tax payable account!"}
                return message
            
            #mobile phone cash sales
            cur.execute("""INSERT INTO mobile_phone_cash_sales (distribution_center_id, agent_id,        total_buying_price, total_selling_price,        total_discount, total_net_sales_amount, sales_date, payment_mothod, customer_name, customer_number, customer_email, bank_account, receivable_account, tax_expense_account, tax_payable_account, sales_remarks, created_date, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                               (distribution_center_id, agent_id, total_buying_price_amount,  total_sales_amount, total_discount_amount, total_net_sales_amount, sales_date, payment_mothod, customer_name, customer_number, customer_email, bank_account, receivable_account, tax_expense_account, tax_payable_account, sales_remarks, created_date,   agent_id, status))
            mysql.get_db().commit()
            rowcount = cur.rowcount
            if rowcount:
                mobile_phone_cash_sales_id = cur.lastrowid
                
                for mobilephone_model_detail in phone_model_details:
                    
                    model_id = mobilephone_model_detail["model_id"]
                    imei_1 = mobilephone_model_detail["imei_1"] 
                    mobilephone_agentstock_id = mobilephone_model_detail["mobilephone_agentstock_id"]
                    quantity = 1
                
                    #get mobile phone tax percentage amount 
                    cur.execute("""SELECT vat_percent_amount FROM product_mobile_phones_models WHERE id = %s """, (model_id))
                    vat_details = cur.fetchone()
                    if vat_details:
                        vat_percentage_amount = float(vat_details["vat_percent_amount"])
                    else:
                        message = {"description":"This phone model does not have VAT percentage amount set",
                                   "status":404}
                        return message
                        
                    #get specific phone global_id
                    cur.execute("""SELECT global_id, imei_2, qr_code_id, warranty_period FROM mobile_phones_transit_stock_received WHERE imei_1 = %s """, (imei_1))
                    phone_details = cur.fetchone() 
                    if phone_details:
                        global_id = phone_details["global_id"]
                        imei_2 = phone_details["imei_2"]
                        qr_code_id = phone_details["qr_code_id"]
                        warranty_period = phone_details["warranty_period"]
                    else:
                        global_id = ''
                        imei_2 = ''
                        qr_code_id = ''
                        warranty_period = ''
                        
                        message = {"description":"This phone does not have global id",
                                   "status":404}
                        return message
                
                    #get specific phone buying price
                    cur.execute("""SELECT price_per_unit FROM cash_stock_purchase_models WHERE model_id = %s AND global_id = %s """, (model_id, global_id))
                    get_phone_buying_price = cur.fetchone() 
                    if get_phone_buying_price:
                        price_per_unit = float(get_phone_buying_price["price_per_unit"])
                    else:
                        price_per_unit = ''
                        message = {"description":"This phone does not have global id",
                                "status":404}
                        return message
                    
                    cur.execute("""SELECT id, price_amount, discount_amount, final_price FROM distribution_center_mobilephone_model_prices WHERE status =1 AND model_id = %s AND distribution_center_id = %s """, (model_id, distribution_center_id))
                    get_phone_model_price = cur.fetchone() 
                    if get_phone_model_price:
                        price_amount = float(get_phone_model_price["price_amount"])
                        discount_amount = float(get_phone_model_price["discount_amount"])
                        final_price = float(get_phone_model_price["final_price"])
                        vat_amount = (final_price * vat_percentage_amount) / 100
                    else:
                        price_amount = 0
                        discount_amount = 0
                        final_price = 0
                        vat_amount = 0
                    
                    acc_details = {
                            "model_id":model_id
                            }
                   
                    #fetch stock account per model 
                    get_stock_Account = Accounts().get_stock_account(acc_details)
                    if int(get_stock_Account["status"]) == 200:
                        stock_account = get_stock_Account["data"]
                    else:
                        stock_account = ''
                        message = {'status':402,
                                'description':"Couldn't fetch stock account!"}
                        ErrorLogger().logError(message)                                
                        return message
                    
                    #fetch cost of service per model 
                    
                    get_cog_Account = Accounts().get_cog_account(acc_details)
                    if int(get_cog_Account["status"]) == 200:
                        cost_of_service_account = get_cog_Account["data"]
                    else:
                        cost_of_service_account = ''
                        message = {'status':402,
                                   'description':"Couldn't fetch cog account!"}
                        ErrorLogger().logError(message)                                
                        return message
                    
                    #fetch income account per model 
                    get_income_Account = Accounts().get_income_account(acc_details)
                    if int(get_income_Account["status"]) == 200:
                        income_account = get_income_Account["data"]
                    else:
                        income_account = ''
                        message = {'status':402,
                                'description':"Couldn't fetch income account!"}
                        ErrorLogger().logError(message)                                
                        return message
                    
                    
                    #fetch discount account per model 
                    get_discount_Account = Accounts().get_discount_account(acc_details)
                    if int(get_discount_Account["status"]) == 200:
                        discount_account = get_discount_Account["data"]
                    else:
                        discount_account = ''
                        message = {'status':402,
                                'description':"Couldn't fetch discount account!"}
                        ErrorLogger().logError(message)                                
                        return message
                    
                    #mobile phone device cash sales
                    cur.execute("""INSERT INTO mobile_phone_cash_sales_model_details (mobilephone_agentstock_id, mobile_phone_cash_sales_id, global_id, model_id, imei_1, imei_2, qr_code_id, stock_account, cost_of_service_account, income_account, discount_account,   buying_price, selling_price,       discount, final_price, vat_amount, warranty_period) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                                                     (mobilephone_agentstock_id, mobile_phone_cash_sales_id, global_id, model_id, imei_1, imei_2, qr_code_id, stock_account, cost_of_service_account, income_account, discount_account, price_per_unit, price_amount, discount_amount, final_price, vat_amount, warranty_period))
                    mysql.get_db().commit()
                 
                message = {"description":"Mobile phone cash sales was created successfully",
                        "status":200}
                return message
            else:
                message = {"description":"Failed to create mobile phone cash sales",
                           "status":501}
                return message
                
        #Error handling
        except Exception as error:
            message = {'status':501, 
                       'error':'sp_a02',
                       'description':'Failed to create a mobile phone cash sales. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        finally:
            cur.close()
  
    def list_cash_sales(self, user):
        
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
        
            cur.execute("""SELECT id, distribution_center_id, agent_id, total_buying_price, total_selling_price, total_discount, total_net_sales_amount, sales_date, payment_mothod, customer_name, customer_number, customer_email, bank_account, receivable_account, tax_expense_account, tax_payable_account, sales_remarks, created_date, created_by FROM mobile_phone_cash_sales WHERE status = %s """, (status))
            sales = cur.fetchall()            
            if sales:
                mobile_sales = []
                
                for sale in sales:
                    id = sale['id']
                    total_buying_price = float(sale['total_buying_price'])
                    total_selling_price = float(sale['total_selling_price'])
                    total_discount = float(sale['total_discount'])
                    total_net_sales_amount = float(sale['total_net_sales_amount'])
                    
                    device_sales_details = []
                    cur.execute("""SELECT id, global_id, model_id, imei_1, imei_2, qr_code_id, stock_account, cost_of_service_account, income_account, discount_account, buying_price, selling_price, discount, final_price, vat_amount, warranty_period FROM mobile_phone_cash_sales_model_details WHERE mobile_phone_cash_sales_id = %s """, (id))
                    sales_details = cur.fetchall()
                    if sales_details:
                        for sales_detail in sales_details:
                            global_id = sales_detail["global_id"]
                            model_id = sales_detail["model_id"]
                            imei_1 = sales_detail["imei_1"]
                            imei_2 = sales_detail["imei_2"]
                            qr_code_id = sales_detail["qr_code_id"]
                            stock_account = sales_detail["stock_account"]
                            cost_of_service_account = sales_detail["cost_of_service_account"]
                            income_account = sales_detail["income_account"]
                            discount_account = sales_detail["discount_account"]
                            buying_price = float(sales_detail["buying_price"])
                            selling_price = float(sales_detail["selling_price"])
                            discount = float(sales_detail["discount"])
                            final_price = float(sales_detail["final_price"])
                            vat_amount = float(sales_detail["vat_amount"])
                            warranty_period = sales_detail["warranty_period"]
                            
                            sales_details_res = {
                                "global_id":global_id,
                                "model_id":model_id,
                                "imei_1":imei_1,
                                "imei_2":imei_2,
                                "qr_code_id":qr_code_id,
                                "stock_account":stock_account,
                                "cost_of_service_account":cost_of_service_account,
                                "income_account":income_account,
                                "discount_account":discount_account,
                                "buying_price":buying_price,
                                "discount_account":discount_account,
                                "selling_price":selling_price,
                                "discount":discount,
                                "final_price":final_price,
                                "vat_amount":vat_amount,
                                "warranty_period":warranty_period
                            }
                            device_sales_details.append(sales_details_res)
                    
                    response = {
                        "id": sale['id'],
                        "distribution_center_id": sale['distribution_center_id'],
                        "agent_id": sale['agent_id'],
                        "total_buying_price": total_buying_price,
                        "total_selling_price": total_selling_price,
                        "total_discount": total_discount,
                        "total_net_sales_amount": total_net_sales_amount,
                        "sales_date": sale['sales_date'],
                        "payment_mothod": sale['payment_mothod'],
                        "customer_name": sale['customer_name'],
                        "customer_number": sale['customer_number'],
                        "customer_email": sale['customer_email'],
                        "bank_account": sale['bank_account'],
                        "receivable_account": sale['receivable_account'],
                        "tax_expense_account":sale['tax_expense_account'],
                        "tax_payable_account":sale['tax_payable_account'],
                        "sales_remarks":sale['sales_remarks'],
                        "created_date": sale['created_date'],
                        "created_by_id": sale['created_by'],
                        "device_sales_details":device_sales_details
                    }
                    mobile_sales.append(response)
            
            
                message = {'status':200,
                            'response':mobile_sales, 
                            'description':'Mobile phone sales records were fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':404,
                            'error':'sp_a04',
                            'description':'Failed to fetch mobile phone sales records!'
                        }   
                return jsonify(message), 404             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve mobile phone sales record from database.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)  
        
    def get_cash_sales_details(self, user):
        
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
        
            cur.execute("""SELECT id, distribution_center_id, agent_id, total_buying_price, total_selling_price, total_discount, total_net_sales_amount, sales_date, payment_mothod, customer_name, customer_number, customer_email, bank_account, receivable_account, tax_expense_account, tax_payable_account, sales_remarks, created_date, created_by FROM mobile_phone_cash_sales WHERE id = %s """, (id))
            sale = cur.fetchone()            
            if sale:
                
                id = sale['id']
                total_buying_price = float(sale['total_buying_price'])
                total_selling_price = float(sale['total_selling_price'])
                total_discount = float(sale['total_discount'])
                total_net_sales_amount = float(sale['total_net_sales_amount'])
                
                device_sales_details = []
                cur.execute("""SELECT id, global_id, model_id, imei_1, imei_2, qr_code_id, stock_account, cost_of_service_account, income_account, discount_account, buying_price, selling_price, discount, final_price, vat_amount, warranty_period FROM mobile_phone_cash_sales_model_details WHERE mobile_phone_cash_sales_id = %s """, (id))
                sales_details = cur.fetchall()
                if sales_details:
                    for sales_detail in sales_details:
                        global_id = sales_detail["global_id"]
                        model_id = sales_detail["model_id"]
                        imei_1 = sales_detail["imei_1"]
                        imei_2 = sales_detail["imei_2"]
                        qr_code_id = sales_detail["qr_code_id"]
                        stock_account = sales_detail["stock_account"]
                        cost_of_service_account = sales_detail["cost_of_service_account"]
                        income_account = sales_detail["income_account"]
                        discount_account = sales_detail["discount_account"]
                        buying_price = float(sales_detail["buying_price"])
                        selling_price = float(sales_detail["selling_price"])
                        discount = float(sales_detail["discount"])
                        final_price = float(sales_detail["final_price"])
                        vat_amount = float(sales_detail["vat_amount"])
                        warranty_period = sales_detail["warranty_period"]
                        
                        sales_details_res = {
                            "global_id":global_id,
                            "model_id":model_id,
                            "imei_1":imei_1,
                            "imei_2":imei_2,
                            "qr_code_id":qr_code_id,
                            "stock_account":stock_account,
                            "cost_of_service_account":cost_of_service_account,
                            "income_account":income_account,
                            "discount_account":discount_account,
                            "buying_price":buying_price,
                            "discount_account":discount_account,
                            "selling_price":selling_price,
                            "discount":discount,
                            "final_price":final_price,
                            "vat_amount":vat_amount,
                            "warranty_period":warranty_period
                        }
                        device_sales_details.append(sales_details_res)
                
                response = {
                    "id": sale['id'],
                    "distribution_center_id": sale['distribution_center_id'],
                    "agent_id": sale['agent_id'],
                    "total_buying_price": total_buying_price,
                    "total_selling_price": total_selling_price,
                    "total_discount": total_discount,
                    "total_net_sales_amount": total_net_sales_amount,
                    "sales_date": sale['sales_date'],
                    "payment_mothod": sale['payment_mothod'],
                    "customer_name": sale['customer_name'],
                    "customer_number": sale['customer_number'],
                    "customer_email": sale['customer_email'],
                    "bank_account": sale['bank_account'],
                    "receivable_account": sale['receivable_account'],
                    "tax_expense_account":sale['tax_expense_account'],
                    "tax_payable_account":sale['tax_payable_account'],
                    "sales_remarks":sale['sales_remarks'],
                    "created_date": sale['created_date'],
                    "created_by_id": sale['created_by'],
                    "device_sales_details":device_sales_details
                }
        
                message = {'status':200,
                            'response':response, 
                            'description':'Mobile phone sales record was fetched successfully!'
                        }   
                return jsonify(message), 200
            
            else:                
                message = {'status':404,
                            'error':'sp_a04',
                            'description':'Failed to fetch mobile phone sales record!'
                        }   
                return jsonify(message), 404             
             
            
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a05',
                       'description':'Failed to retrieve mobile phone sales record from database.' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message)
            
    def approve_cash_sales(self, user):
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
            
            #select sales record details 
            cur.execute("""SELECT id, distribution_center_id, agent_id, total_buying_price, total_selling_price, total_discount, total_net_sales_amount, sales_date, payment_mothod, customer_name, customer_number, customer_email, bank_account, receivable_account, tax_expense_account, tax_payable_account, created_date, created_by FROM mobile_phone_cash_sales WHERE id = %s """, (id))
            sale = cur.fetchone()            
            if sale:
                transaction_id = 'Cash Sale'
                agent_id = sale["created_by"]
                distribution_center_id = sale["distribution_center_id"]
                sales_date = sale["sales_date"]
                bank_account = sale["bank_account"]
                receivable_account = sale["receivable_account"]
                tax_expense_account = sale["tax_expense_account"]
                tax_payable_account = sale["tax_payable_account"]
                
                #fetch sales agents details
                cur.execute("""SELECT first_name, last_name FROM user_details WHERE user_id = %s""", [agent_id])
                agent_details = cur.fetchone()
                if agent_details:
                    first_name = agent_details["first_name"]
                    last_name = agent_details["last_name"]
                    agent_name = first_name + ' ' + last_name
                    
                
                #select sales record details per model
                total_vat_amount = 0
                cur.execute("""SELECT id, mobilephone_agentstock_id, global_id, model_id, imei_1, imei_2, qr_code_id, stock_account, cost_of_service_account, income_account, discount_account, buying_price, selling_price, discount, final_price, vat_amount, warranty_period FROM mobile_phone_cash_sales_model_details WHERE mobile_phone_cash_sales_id = %s """, (id))
                models_sales_details = cur.fetchall()            
                if models_sales_details:
                    for model_sales_details in models_sales_details:
                        mobilephone_agentstock_id = model_sales_details["mobilephone_agentstock_id"]
                        global_id = model_sales_details["global_id"]
                        model_id = model_sales_details["model_id"]
                        global_id = model_sales_details["global_id"]
                        imei_1 = model_sales_details["imei_1"]
                        imei_2 = model_sales_details["imei_2"]
                        qr_code_id = model_sales_details["qr_code_id"]
                        stock_account = model_sales_details["stock_account"]
                        cost_of_service_account = model_sales_details["cost_of_service_account"]
                        income_account = model_sales_details["income_account"]
                        discount_account = model_sales_details["discount_account"]
                        buying_price = float(model_sales_details["buying_price"])
                        selling_price = float(model_sales_details["selling_price"])
                        discount = float(model_sales_details["discount"])
                        final_price = float(model_sales_details["final_price"])
                        vat_amount = float(model_sales_details["vat_amount"])
                        
                        total_vat_amount = total_vat_amount + vat_amount
                    
                        #Remove product from distribution center and indicate product sold on agents stock table
                        cur.execute("""UPDATE mobile_phones_agents_stock set stock_state=2 WHERE status =1 AND stock_state = 1 AND id = %s """, (mobilephone_agentstock_id))
                        mysql.get_db().commit()       
                        rowcount = cur.rowcount
                        if rowcount:
                    
                            #debit receivable account - credit revenue account 
                            #gross sales 
                      
                            details = {
                                "id":id,
                                "user_id":user["id"],
                                "global_id":global_id,
                                "amount":selling_price,
                                "receivable_account":receivable_account,
                                "income_account":income_account,
                                "settlement_date":sales_date,
                                "transaction_id":transaction_id

                            }
                            
                            debit_receivable_credit_revenue_message = DebitCredit().mobilephone_sale_debitreceivable_creditrevenue(details) 
                            
                            #debit bank account - credit receivable account
                            #net sales 
                            
                            details = {
                                "id":id,
                                "user_id":user["id"],
                                "global_id":global_id,
                                "amount":final_price,
                                "bank_account":bank_account,
                                "receivable_account":receivable_account,
                                "settlement_date":sales_date,
                                "transaction_id":transaction_id

                            }
                            
                            debit_bank_credit_receivable_message = DebitCredit().mobilephone_sale_debitbank_creditreceivable(details) 
                            
                            
                            #debit cog account -  credit stock account
                            #buying_price 
                            details = {
                                "id":id,
                                "user_id":user["id"],
                                "global_id":global_id,
                                "amount":buying_price,
                                "cost_of_service_account":cost_of_service_account,
                                "stock_account":stock_account,
                                "settlement_date":sales_date,
                                "transaction_id":transaction_id

                            }
                            
                            debit_cog_credit_stock_message = DebitCredit().mobilephone_sale_debitcog_creditstock(details) 
                            
                            #debit discount account - credit receivable account
                            #discount amount 
                            
                            if discount > 0:
                                details = {
                                "id":id,
                                "user_id":user["id"],
                                "global_id":global_id,
                                "amount":discount,
                                "discount_account":discount_account,
                                "receivable_account":receivable_account,
                                "settlement_date":sales_date,
                                "transaction_id":transaction_id

                                }
                            
                                debit_discount_credit_receivable_message = DebitCredit().mobilephone_sale_debitdiscount_creditreceivable(details) 
                                
            
            #compute tax per model, get total tax for the receipt then post.
            #debit tax expense account - credit tax payable account
            #16% of net sales
            
            
            details = {
                "id":id,
                "user_id":user["id"],
                "global_id":global_id,
                "amount":total_vat_amount,
                "tax_expense_account":tax_expense_account,
                "tax_payable_account":tax_payable_account,
                "settlement_date":sales_date,
                "transaction_id":transaction_id

            }
            
            debit_taxexpense_credit_taxpayable_message = DebitCredit().mobilephone_sale_debittaxepense_credittaxpayable(details) 
            
            
            cur.execute("""UPDATE mobile_phone_cash_sales set status=1, approved_date = %s, approved_by = %s WHERE status =2 AND id = %s """, ([dateapproved, approved_by, id]))
            mysql.get_db().commit()       
            rowcount = cur.rowcount
            if rowcount:   
                
                trans_message = {"description":"Mobile phone sales was approved successfully!",
                                 "status":200}
                return jsonify(trans_message), 200
                
            else:
                message = {'status':404,
                           'description':'Mobile phone sales record was not found!'}
                return jsonify(message), 404
                    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'sp_a09',
                       'description':'Failed to approve phone model sales record. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return jsonify(message), 501  
        finally:
            cur.close()

     
   