from flask import Response, jsonify
from main import mysql, app
from datetime import datetime
from resources.alphanumeric.generate import UniqueNumber
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.inventory.inventory import Inventory

class Sms_tasks():
    # def send_installment_remainder_sms(self):
    #     try: 
    #         # Open A connection to the database
    #         try:
    #             cur =  mysql.get_db().cursor()
    #         except:
    #             message = {'status':500,
    #                        'description':"Couldn't connect to the Database!"}
    #             return message

    #         #select all scheduled sms and send them
    #         date_created = Localtime().getdate()
   
    #         sms_date = date_created.strftime('%Y-%m-%d')
    #         sms_time = '08:00:00'
     
    #         timenow = sms_date + ' ' + sms_time
            
    #         cur.execute("""SELECT id, customer_id, msisdn, sms_content FROM installment_remainder_sms WHERE send_sms_at >= %s AND status =0""", (timenow))
    #         get_sms = cur.fetchall()
    #         if get_sms:
    #             for sms in get_sms:
    #                 id = sms["id"]
    #                 customer_id = sms["customer_id"]
    #                 msisdn = sms["msisdn"]
    #                 sms_content = sms["sms_content"]                    

    #                 cur.execute("""UPDATE installment_remainder_sms set status = 9 WHERE id = %s""", (id))
    #                 mysql.get_db().commit()
                                        
    #                 global_id = UniqueNumber.globalIdentifier(self) 

    #                 cur.execute("""SELECT inventory_id, price_per_item FROM sms_details WHERE status =1 ORDER BY id DESC LIMIT 1 """)
    #                 sms_details = cur.fetchone() 
    #                 if sms_details:
    #                     cost_per_item = float(sms_details["price_per_item"])
    #                     inventory_id = sms_details["inventory_id"]
    #                 else:
    #                     res = {"status":401,
    #                            "description":"Task was not successful. Price per sms was not found!"}
    #                     ErrorLogger().logError(res) 
    #                     return res

    #                 sms_details = {
    #                                 "entry_id":customer_id, 
    #                                 "date_consumed":date_created, 
    #                                 "global_id":global_id,
    #                                 "msisdn":msisdn,
    #                                 "content":sms_content, 
    #                                 "inventory_id":inventory_id,     
    #                                 "cost_per_item":cost_per_item,                                
    #                                 "type": "installment_remainder"
    #                                 }                    
    #                 sms_response = Inventory().sms_inventory_consumed(sms_details)
    #                 if int(sms_response["status"]) == 200:
                        
    #                     #update sms details change status
    #                     cur.execute("""UPDATE installment_remainder_sms set status = 1 WHERE id = %s""", (id))
    #                     mysql.get_db().commit()
                        
    #             message = {
    #                     "status":200,
    #                     "description":"Installment remainder sms was send successfully"
    #             }
    #             return message
    #         else:
    #             message = {
    #                     "status":201,
    #                     "description":"Installment remainder sms was not send!"
    #             }
    #             return message


    #     # Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'description':'Send installment remainder sms Transaction had an error. Error description ' + format(error)}
    #         ErrorLogger().logError(message) 
    #         return message 
    #     finally:
    #         cur.close()
            
    # def send_rollover_installment_remainder_sms(self):
    #     try: 
    #         # Open A connection to the database
    #         try:
    #             cur =  mysql.get_db().cursor()
    #         except:
    #             message = {'status':500,
    #                        'description':"Couldn't connect to the Database!"}
    #             return message

    #         #select all scheduled sms and send them
    #         date_created = Localtime().getdate()
   
    #         sms_date = date_created.strftime('%Y-%m-%d')
    #         sms_time = '08:00:00'
     
    #         timenow = sms_date + ' ' + sms_time
            
    #         cur.execute("""SELECT id, customer_id, msisdn, sms_content FROM rollover_fee_installment_remainder_sms WHERE send_sms_at >= %s AND status =0""", (timenow))
    #         get_sms = cur.fetchall()
    #         if get_sms:
    #             for sms in get_sms:
    #                 id = sms["id"]
    #                 customer_id = sms["customer_id"]
    #                 msisdn = sms["msisdn"]
    #                 sms_content = sms["sms_content"]                    

    #                 cur.execute("""UPDATE rollover_fee_installment_remainder_sms  set status = 9 WHERE id = %s""", (id))
    #                 mysql.get_db().commit()
                                        
    #                 global_id = UniqueNumber.globalIdentifier(self) 

    #                 cur.execute("""SELECT inventory_id, price_per_item FROM sms_details WHERE status =1 ORDER BY id DESC LIMIT 1 """)
    #                 sms_details = cur.fetchone() 
    #                 if sms_details:
    #                     cost_per_item = float(sms_details["price_per_item"])
    #                     inventory_id = sms_details["inventory_id"]
    #                 else:
    #                     res = {"status":401,
    #                            "description":"Task was not successful. Price per sms was not found!"}
    #                     ErrorLogger().logError(res) 
    #                     return res

    #                 sms_details = {
    #                                 "entry_id":customer_id, 
    #                                 "date_consumed":date_created, 
    #                                 "global_id":global_id,
    #                                 "msisdn":msisdn,
    #                                 "content":sms_content, 
    #                                 "inventory_id":inventory_id,     
    #                                 "cost_per_item":cost_per_item,                                
    #                                 "type": "installment_remainder"
    #                                 }                    
    #                 sms_response = Inventory().sms_inventory_consumed(sms_details)
    #                 if int(sms_response["status"]) == 200:
                        
    #                     #update sms details change status
    #                     cur.execute("""UPDATE rollover_fee_installment_remainder_sms  set status = 1, date_updated = %s WHERE id = %s""", (date_created, id))
    #                     mysql.get_db().commit()
                        
    #             message = {
    #                     "status":200,
    #                     "description":"Rollover fee installment remainder sms was send successfully"
    #             }
    #             return message
    #         else:
    #             message = {
    #                     "status":201,
    #                     "description":"Rollover fee installment remainder sms was not send!"
    #             }
    #             return message


    #     # Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'description':'Send rollover installment remainder sms Transaction had an error. Error description ' + format(error)}
    #         ErrorLogger().logError(message) 
    #         return message 
    #     finally:
    #         cur.close()



    def send_loan_payment_remainder_sms(self):
        try: 
            # Open A connection to the database
            try:
                cur =  mysql.get_db().cursor()
            except:
                message = {'status':500,
                           'description':"Couldn't connect to the Database!"}
                return message

            date_created = Localtime().gettime()  
            now = datetime.strptime(date_created, '%Y-%m-%d %H:%M:%S')

            
            cur.execute("""SELECT id, loan_id, msisdn, sms_content FROM sms_loan_payment_remainder WHERE sent_sms_date <= %s AND status =0""", (now))
            get_sms = cur.fetchall()
            if get_sms:
                for sms in get_sms:
                    id = sms["id"]
                    loan_id = sms["loan_id"]
                    msisdn = sms["msisdn"]
                    sms_content = sms["sms_content"]                    

                    cur.execute("""UPDATE sms_loan_payment_remainder  set status = 9 WHERE id = %s""", (id))
                    mysql.get_db().commit()
                                        
                    global_id = UniqueNumber.globalIdentifier(self) 

                    cur.execute("""SELECT inventory_id, price_per_item FROM sms_details WHERE status =1 ORDER BY id DESC LIMIT 1 """)
                    sms_details = cur.fetchone() 
                    if sms_details:
                        cost_per_item = float(sms_details["price_per_item"])
                        inventory_id = sms_details["inventory_id"]
                    else:
                        res = {"status":401,
                               "description":"Task was not successful. Price per sms was not found!"}
                        ErrorLogger().logError(res) 
                        return res

                    sms_details = {
                                    "entry_id":loan_id, 
                                    "date_consumed":date_created, 
                                    "global_id":global_id,
                                    "msisdn":msisdn,
                                    "content":sms_content, 
                                    "inventory_id":inventory_id,     
                                    "cost_per_item":cost_per_item,                                
                                    "type": "installment_remainder"
                                    }                    
                    sms_response = Inventory().sms_inventory_consumed(sms_details)
                    if int(sms_response["status"]) == 200:
                        
                        #update sms details change status
                        cur.execute("""UPDATE sms_loan_payment_remainder  set status = 1, date_updated = %s WHERE id = %s""", (date_created, id))
                        mysql.get_db().commit()
                        
                message = {
                        "status":200,
                        "description":"Loan payment remainder sms was send successfully"
                }
                return message
            else:
                message = {
                        "status":201,
                        "description":"Loan payment remainder sms was not send!"
                }
                return message


        # Error handling
        except Exception as error:
            message = {'status':501,
                       'description':'Send loan payment remainder sms had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 
        finally:
            cur.close()
            
            
    def send_reducing_balance_loan_payment_remainder_sms(self):
        try: 
            # Open A connection to the database
            try:
                cur =  mysql.get_db().cursor()
            except:
                message = {'status':500,
                           'description':"Couldn't connect to the Database!"}
                return message

            #select all scheduled sms and send them
            date_created = Localtime().getdate()
               
            cur.execute("""SELECT id, loan_id, msisdn, sms_content FROM sms_loan_payment_remainder WHERE daemon = 1 AND status =0""")
            get_sms = cur.fetchall()
            if get_sms:
                for sms in get_sms:
                    id = sms["id"]
                    loan_id = sms["loan_id"]
                    msisdn = sms["msisdn"]
                    sms_content = sms["sms_content"]                    

                    cur.execute("""UPDATE sms_loan_payment_remainder  set status = 9 WHERE id = %s""", (id))
                    mysql.get_db().commit()
                                        
                    global_id = UniqueNumber.globalIdentifier(self) 

                    cur.execute("""SELECT inventory_id, price_per_item FROM sms_details WHERE status =1 ORDER BY id DESC LIMIT 1 """)
                    sms_details = cur.fetchone() 
                    if sms_details:
                        cost_per_item = float(sms_details["price_per_item"])
                        inventory_id = sms_details["inventory_id"]
                    else:
                        res = {"status":401,
                               "description":"Task was not successful. Price per sms was not found!"}
                        ErrorLogger().logError(res) 
                        return res

                    sms_details = {
                                    "entry_id":loan_id, 
                                    "date_consumed":date_created, 
                                    "global_id":global_id,
                                    "msisdn":msisdn,
                                    "content":sms_content, 
                                    "inventory_id":inventory_id,     
                                    "cost_per_item":cost_per_item,                                
                                    "type": "installment_remainder"
                                    }                    
                    sms_response = Inventory().sms_inventory_consumed(sms_details)
                    if int(sms_response["status"]) == 200:
                        
                        #update sms details change status
                        cur.execute("""UPDATE sms_loan_payment_remainder set status = 1, date_updated = %s WHERE id = %s""", (date_created, id))
                        mysql.get_db().commit()
                        
                message = {
                        "status":200,
                        "description":"Group Loan payment remainder sms was send successfully"
                }
                return message
            else:
                message = {
                        "status":201,
                        "description":"Group Loan payment remainder sms was not send!"
                }
                return message


        # Error handling
        except Exception as error:
            message = {'status':501,
                       'description':'Send loan payment remainder sms had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 
        finally:
            cur.close()