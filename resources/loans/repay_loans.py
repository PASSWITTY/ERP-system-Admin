from flask import json, jsonify
from main import mysql
from resources.payload.payload import Localtime  
from resources.logs.logger import ErrorLogger
from resources.alphanumeric.generate import UniqueNumber
from resources.inventory.inventory import Inventory
from resources.loans.pay_demandnote import PayDemandNotes
from resources.loans.tax_incur_expense import TaxExpenseIncurred
from accounts_module.accounts_model import Account
from resources.loans.create_demandnote import CreateDemandNote
from datetime import datetime


class Repay_Loans():
    
    def system_initiated_defaulted_loanfine_repayment(self, details):
         #Get the request data 
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       "error":"il_r001",
                       "status": 402}
            ErrorLogger().logError(message)
            return message

        customer_id = details["customer_id"] 
        loan_type = int(details["loan_type"])
        wallet_account_number = details["wallet_account_number"] 
        deduct_amount = float(details["deduct_amount"]) 
        deposit_amount = float(details["wallet_balance"])         

        try:
            global_id = UniqueNumber.globalIdentifier(self) 
            #Check if wallet has the amount entered

            selfpayment_demandnotes = {
                "customer_id" :customer_id, 
                "loan_type":loan_type,
                "wallet_account_number": wallet_account_number,
                "global_id":global_id,
                "deduct_amount":deduct_amount,
                "deposit_amount":deposit_amount
            }
            
            #get request from customer for loan prepayment
            status_customer_update_prepayments_funds = Repay_Loans().customer_initiated_update_prepayment_funds(selfpayment_demandnotes)
            
            ### 1. Pay all defaulted loan fines due starting from the oldest
            status_customer_initiate_pay_defaultedloan_fines_demand_notes = Repay_Loans().customer_initiated_defaulted_loan_fine_repayment(selfpayment_demandnotes)
            
            ### 2. Pay all rollover fees due starting from the oldest
            # status_customer_initiate_pay_rollover_fee_demand_notes = Repay_Loans().customer_initiated_rolloverfee_repayment(selfpayment_demandnotes)           
            
            ### 3. Pay all demand notes due starting from the oldest
            # status_customer_initiate_pay_current_demand_notes = Repay_Loans().customer_initiated_demand_notes_repayment(selfpayment_demandnotes)

            message = {'status_customer_update_prepayments_funds': status_customer_update_prepayments_funds,
                       'status_customer_initiate_pay_defaultedloan_fines_demand_notes': status_customer_initiate_pay_defaultedloan_fines_demand_notes,
                    #    'status_customer_initiate_pay_rollover_fee_demand_notes': status_customer_initiate_pay_rollover_fee_demand_notes,
                    #    'status_customer_initiate_pay_current_demand_notes': status_customer_initiate_pay_current_demand_notes
                       }
            return message
            
            
        except Exception as error:
            message = {'status':501,
                       "error":"il_r002",
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 
    
    def system_initiated_rolloverfee_repayment(self, details):
         #Get the request data 
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       "error":"il_r001",
                       "status": 402}
            ErrorLogger().logError(message)
            return message

        customer_id = details["customer_id"] 
        loan_type = int(details["loan_type"])
        wallet_account_number = details["wallet_account_number"] 
        deduct_amount = float(details["deduct_amount"]) 
        deposit_amount = float(details["wallet_balance"])         

        try:
            global_id = UniqueNumber.globalIdentifier(self) 
            #Check if wallet has the amount entered

            selfpayment_demandnotes = {
                "customer_id" :customer_id, 
                "loan_type":loan_type,
                "wallet_account_number": wallet_account_number,
                "global_id":global_id,
                "deduct_amount":deduct_amount,
                "deposit_amount":deposit_amount
            }
            

            #get request from customer for loan prepayment
            status_customer_update_prepayments_funds = Repay_Loans().customer_initiated_update_prepayment_funds(selfpayment_demandnotes)
            
            ### 1. Pay all defaulted loan fines due starting from the oldest
            # status_customer_initiate_pay_defaultedloan_fines_demand_notes = Repay_Loans().customer_initiated_defaulted_loan_fine_repayment(selfpayment_demandnotes)
            
            ### 2. Pay all rollover fees due starting from the oldest
            status_customer_initiate_pay_rollover_fee_demand_notes = Repay_Loans().customer_initiated_rolloverfee_repayment(selfpayment_demandnotes)           
            
            ### 3. Pay all demand notes due starting from the oldest
            # status_customer_initiate_pay_current_demand_notes = Repay_Loans().customer_initiated_demand_notes_repayment(selfpayment_demandnotes)

            message = {'status_customer_update_prepayments_funds': status_customer_update_prepayments_funds,
                    #    'status_customer_initiate_pay_defaultedloan_fines_demand_notes': status_customer_initiate_pay_defaultedloan_fines_demand_notes,
                       'status_customer_initiate_pay_rollover_fee_demand_notes': status_customer_initiate_pay_rollover_fee_demand_notes,
                    #    'status_customer_initiate_pay_current_demand_notes': status_customer_initiate_pay_current_demand_notes
                       }
            return message
            
            
        except Exception as error:
            message = {'status':501,
                       "error":"il_r002",
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 
    
    def system_initiated_loan_demand_note_repayment(self, details):
         #Get the request data 
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       "error":"il_r001",
                       "status": 402}
            ErrorLogger().logError(message)
            return message

        customer_id = details["customer_id"] 
        loan_type = int(details["loan_type"])
        wallet_account_number = details["wallet_account_number"] 
        deduct_amount = float(details["deduct_amount"]) 
        deposit_amount = float(details["wallet_balance"])         

        try:
            global_id = UniqueNumber.globalIdentifier(self) 
            #Check if wallet has the amount entered

            selfpayment_demandnotes = {
                "customer_id" :customer_id, 
                "loan_type":loan_type,
                "wallet_account_number": wallet_account_number,
                "global_id":global_id,
                "deduct_amount":deduct_amount,
                "deposit_amount":deposit_amount
            }
            
            status_customer_update_prepayments_funds = Repay_Loans().customer_initiated_update_prepayment_funds(selfpayment_demandnotes)
            
            ### 1. Pay all defaulted loan fines due starting from the oldest
            # status_customer_initiate_pay_defaultedloan_fines_demand_notes = Repay_Loans().customer_initiated_defaulted_loan_fine_repayment(selfpayment_demandnotes)
            
            ### 2. Pay all rollover fees due starting from the oldest
            # status_customer_initiate_pay_rollover_fee_demand_notes = Repay_Loans().customer_initiated_rolloverfee_repayment(selfpayment_demandnotes)           
            
            ### 3. Pay all demand notes due starting from the oldest
            status_customer_initiate_pay_current_demand_notes = Repay_Loans().customer_initiated_demand_notes_repayment(selfpayment_demandnotes)

            # status_customer_initiate_generate_new_demand_notes = Repay_Loans().customer_initiated_demand_note_creation(selfpayment_demandnotes)
  
            # status_customer_initiate_pay_generated_demand_notes = Repay_Loans().customer_initiated_demand_notes_repayment(selfpayment_demandnotes)            # if status_customer_initiate_pay_current_notes['status_code'] == 200:
          
            message = {'status_customer_update_prepayments_funds': status_customer_update_prepayments_funds,
                    #    'status_customer_initiate_pay_defaultedloan_fines_demand_notes': status_customer_initiate_pay_defaultedloan_fines_demand_notes,
                    #    'status_customer_initiate_pay_rollover_fee_demand_notes': status_customer_initiate_pay_rollover_fee_demand_notes,
                       'status_customer_initiate_pay_current_demand_notes': status_customer_initiate_pay_current_demand_notes,
                    #    'status_customer_initiate_generate_new_demand_notes': status_customer_initiate_generate_new_demand_notes,
                    #    'status_customer_initiate_pay_generated_demand_notes': status_customer_initiate_pay_generated_demand_notes
                       }
            return message
            
            
        except Exception as error:
            message = {'status':501,
                       "error":"il_r002",
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message
          
    def customer_initiated_loan_repayment(self, details):
         #Get the request data 
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       "error":"il_r001",
                       "status": 402}
            ErrorLogger().logError(message)
            return message

        customer_id = details["customer_id"] 
        loan_type = int(details["loan_type"])
        wallet_account_number = details["wallet_account_number"] 
        deduct_amount = float(details["deduct_amount"]) 
        deposit_amount = float(details["wallet_balance"])         

        try:
            global_id = UniqueNumber.globalIdentifier(self) 
            #Check if wallet has the amount entered

            selfpayment_demandnotes = {
                "customer_id" :customer_id, 
                "loan_type":loan_type,
                "wallet_account_number": wallet_account_number,
                "global_id":global_id,
                "deduct_amount":deduct_amount,
                "deposit_amount":deposit_amount
            }
            
            #get request from customer for loan prepayment
            status_customer_update_prepayments_funds = Repay_Loans().customer_initiated_update_prepayment_funds(selfpayment_demandnotes)
            
            ### 1. Pay all defaulted loan fines due starting from the oldest
            status_customer_initiate_pay_defaultedloan_fines_demand_notes = Repay_Loans().customer_initiated_defaulted_loan_fine_repayment(selfpayment_demandnotes)
            
            ### 2. Pay all rollover fees due starting from the oldest
            status_customer_initiate_pay_rollover_fee_demand_notes = Repay_Loans().customer_initiated_rolloverfee_repayment(selfpayment_demandnotes)           
            
            ### 3. Pay all demand notes due starting from the oldest
            status_customer_initiate_pay_current_demand_notes = Repay_Loans().customer_initiated_demand_notes_repayment(selfpayment_demandnotes)

            # status_customer_initiate_generate_new_demand_notes = Repay_Loans().customer_initiated_demand_note_creation(selfpayment_demandnotes)
  
            # status_customer_initiate_pay_generated_demand_notes = Repay_Loans().customer_initiated_demand_notes_repayment(selfpayment_demandnotes)            # if status_customer_initiate_pay_current_notes['status_code'] == 200:
          
            message = {'status_customer_update_prepayments_funds': status_customer_update_prepayments_funds,
                       'status_customer_initiate_pay_defaultedloan_fines_demand_notes': status_customer_initiate_pay_defaultedloan_fines_demand_notes,
                       'status_customer_initiate_pay_rollover_fee_demand_notes': status_customer_initiate_pay_rollover_fee_demand_notes,
                       'status_customer_initiate_pay_current_demand_notes': status_customer_initiate_pay_current_demand_notes
                    #    'status_customer_initiate_generate_new_demand_notes': status_customer_initiate_generate_new_demand_notes,
                    #    'status_customer_initiate_pay_generated_demand_notes': status_customer_initiate_pay_generated_demand_notes
                       }
            return message
            
            
        except Exception as error:
            message = {'status':501,
                       "error":"il_r002",
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 
        
    def customer_initiated_update_prepayment_funds(self, selfpayment_demandnotes):
         #Get the request data 
        if selfpayment_demandnotes == None:
            message = {"description":"Transaction is missing some details!", 
                       "error":"il_r003",
                       "status": 402}
            ErrorLogger().logError(message) 
            return message

        customer_id = selfpayment_demandnotes["customer_id"] 
        wallet_account_number = selfpayment_demandnotes["wallet_account_number"] 
        deduct_amount = float(selfpayment_demandnotes["deduct_amount"]) 
        deduct_amount = round(deduct_amount, 12)

        deposit_amount = float(selfpayment_demandnotes["deposit_amount"])  
        deposit_amount = round(deposit_amount, 12)       
                
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "error":"il_r004",
                       "status": 500}
            ErrorLogger().logError(message) 
            return message
        
        try:       
            #insert into database, amount to use, and wallet balance                                
            date_created = Localtime().gettime()
            
            cur.execute("""SELECT id FROM loan_prepayment_funds WHERE customer_id = %s AND wallet_account_number = %s""", [customer_id, wallet_account_number]) 
            get_previous_request = cur.fetchone() 
            if get_previous_request:
                if deduct_amount >= deposit_amount:
                    deduct_amount = deposit_amount
                    cur.execute("""UPDATE loan_prepayment_funds set funds_to_use = %s, wallet_balance = %s, last_transaction_date = %s WHERE customer_id = %s""", (deduct_amount, deposit_amount, date_created, customer_id))
                    mysql.get_db().commit()

                    message = {"status":200,
                               "description":"Prepayment funds were updated successfully!"}
                    return message 

                else:
                    cur.execute("""UPDATE loan_prepayment_funds set funds_to_use = funds_to_use + %s, wallet_balance = %s, last_transaction_date = %s WHERE customer_id = %s""", (deduct_amount, deposit_amount, date_created, customer_id))
                    mysql.get_db().commit()

                    message = {"status":200,
                               "description":"Prepayment funds were updated successfully!"}
                    return message 

            else:        
                loanrepaymentfunds_id = UniqueNumber().loanRepaymentFundsId() 
                cur.execute("""INSERT INTO loan_prepayment_funds (id, customer_id, wallet_account_number, funds_to_use, wallet_balance, date_created, last_transaction_date) VALUES (%s, %s, %s, %s, %s, %s, %s)""",(loanrepaymentfunds_id, customer_id, wallet_account_number, deduct_amount, deposit_amount, date_created, date_created))
                mysql.get_db().commit()

                message = {"status":200,
                           "description":"Prepayment funds were created successfully!"}
                return message 
        
        except Exception as error:
            message = {"status":501,
                       "error":"il_r005",
                       "description":"Transaction execution failed. Error description" + format(error)}
            ErrorLogger().logError(message)            
            return message
        finally:
            cur.close()
    
    def customer_initiated_defaulted_loan_fine_repayment(self, selfpayment_demandnotes):
            #Get the request data 
        if selfpayment_demandnotes == None:
            message = {"description":"Transaction is missing some details!", 
                       "error":"il_r011",
                       "status": 402}
            ErrorLogger().logError(message)   
            return message

        customer_id = selfpayment_demandnotes["customer_id"] 
        global_id = selfpayment_demandnotes["global_id"]
       
        #Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "error":"il_r012",
                       "status": 500}
            ErrorLogger().logError(message)   
            return message
        
        #Get customer details
        cur.execute("""SELECT first_name, msisdn FROM customer_details WHERE id = %s """, [customer_id])
        get_customer = cur.fetchone()
        if get_customer:
            msisdn = get_customer["msisdn"]
            first_name = get_customer["first_name"]

        else:                
            message = {"description":"Customer details were not found! Transaction canceled!", 
                       "error":"il_r013",
                       "status":402}
            ErrorLogger().logError(message)   
            return message

        try:
            # global_id = UniqueNumber.globalIdentifier(self) 
            #Check if wallet has the amount entered           
            date_created = Localtime().gettime()
                
            defaulted_loan_fine_demandnote_pay = {
                                        "description":"Defaulted loan fine was not paid!",
                                        "status":201
                                       }
            
            totalloan_paid = 0
            cur.execute("""SELECT id, loan_id, amount_due FROM loan_defaulted_fines_demand_note_details WHERE status=1 AND customer_id = %s AND payment_in_progress =0 AND amount_due > 0 ORDER BY id ASC""", (customer_id))
            pending_defaulted_loan_fines = cur.fetchall() 
            if pending_defaulted_loan_fines:     
                for demand_note in pending_defaulted_loan_fines:
                    demandnote_id = demand_note['id']
                    loan_id = demand_note['loan_id']
                    demandnote_amount_due = float(demand_note['amount_due']) 
                    
                    #Update progress status
                    cur.execute("""UPDATE loan_defaulted_fines_demand_note_details set payment_in_progress =2 WHERE id = %s""", (demandnote_id))
                    mysql.get_db().commit()
                
                    if demandnote_amount_due >0:
                        
                        #Retrieve funds to use
                        cur.execute("""SELECT funds_to_use FROM loan_prepayment_funds WHERE customer_id = %s""", [customer_id]) 
                        getfunds_touse_details = cur.fetchone() 
                        if getfunds_touse_details:
                            funds_to_use = float(getfunds_touse_details["funds_to_use"])

                            if funds_to_use >0:
                                if demandnote_amount_due > funds_to_use:
                                    payment_amount = funds_to_use

                                elif demandnote_amount_due == funds_to_use:

                                    payment_amount = funds_to_use
                                    
                                elif demandnote_amount_due < funds_to_use and funds_to_use > 0:
                                    payment_amount = demandnote_amount_due
                                    
                                else:
                                    payment_amount = 0
                                
                                if payment_amount >0:
                                    
                                    #Call API to pay principal demand note
                                    details = {
                                        "demand_note_id":demandnote_id,
                                        "amount":payment_amount,
                                        "global_id":global_id,
                                        "customer_id":customer_id
                                    }
                                    totalloan_paid = totalloan_paid + payment_amount
                                  
                                    defaulted_loan_fine_demandnote_pay = Repay_Loans().pay_defaulted_loan_fine_demand_note(details)
                                
                            else:
                                pass

                    cur.execute("""UPDATE loan_defaulted_fines_demand_note_details SET payment_in_progress = 0 WHERE id = %s""",(demandnote_id))
                    mysql.get_db().commit()
            if totalloan_paid > 0:
                #CALL SMS API to notify customer of successful loan payment
                #Get inventory id to use -> get this from loan inventory settings
                cur.execute("""SELECT inventory_id, price_per_item FROM sms_details WHERE status =1 ORDER BY id DESC LIMIT 1 """)
                sms_details = cur.fetchone() 
                if sms_details:
                    cost_per_item = float(sms_details["price_per_item"])
                    inventory_id = sms_details["inventory_id"]
                else:
                    res = {"status":402,
                            "error":"il_r017",
                            "description":"Task was not successful. Price per sms was not found!"}
                    ErrorLogger().logError(res) 
                    return res
                
                try:
                    cur.execute("""SELECT (SUM(d.amount_due)) as amount_due FROM loan_defaulted_fines_demand_note_details As d INNER JOIN loans as l ON l.id = d.loan_id WHERE l.customer_id = %s AND d.amount_due > 0 AND d.status =1 """, [customer_id])
                    total_loans = cur.fetchone()
                    if total_loans:
                        totalloans = float(total_loans["amount_due"])
                except:
                    totalloans = 0
                
                #loan_id
                
                sms_message = f"Dear {first_name}, Ksh {totalloan_paid:,.2f} from your Wallet Account has been used to pay your defaulted loan fines.\n"
                if totalloans > 0:
                    sms_message += f"Total pending defaulted loan fine is Ksh {totalloans:,.2f}"
                else:
                    sms_message += "Defaulted loan fine has now been paid."

                sms_details = {
                                "entry_id":loan_id, 
                                "date_consumed":date_created, 
                                "global_id":global_id,
                                "msisdn":msisdn,
                                "content":sms_message, 
                                "inventory_id":inventory_id,   
                                "cost_per_item":cost_per_item,                                
                                "type": "loan_repayment"
                                }
                    
                    
                # sms_response = Inventory().sms_inventory_consumed(sms_details)
                        
                demand_notes_paid_api_responses = {"defaulted_loan_demand_note_payment_status":defaulted_loan_fine_demandnote_pay}
                return demand_notes_paid_api_responses    
            
            else:
                demand_notes_paid_api_responses = {"defaulted_loan_demand_note_payment_status":defaulted_loan_fine_demandnote_pay}
                return demand_notes_paid_api_responses             
            
        except Exception as error:
            message = {"status":501,
                       "error":"il_r018",
                       "description":"Transaction execution failed. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            cur.close()
    
    def customer_initiated_rolloverfee_repayment(self, selfpayment_demandnotes):
            #Get the request data 
        if selfpayment_demandnotes == None:
            message = {"description":"Transaction is missing some details!", 
                       "error":"il_r011",
                       "status": 402}
            ErrorLogger().logError(message)   
            return message

        customer_id = selfpayment_demandnotes["customer_id"] 
        global_id = selfpayment_demandnotes["global_id"]
       
        #Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "error":"il_r012",
                       "status": 500}
            ErrorLogger().logError(message)   
            return message
        
        #Get customer details
        cur.execute("""SELECT first_name, msisdn FROM customer_details WHERE id = %s """, [customer_id])
        get_customer = cur.fetchone()
        if get_customer:
            msisdn = get_customer["msisdn"]
            first_name = get_customer["first_name"]

        else:                
            message = {"description":"Customer details were not found! Transaction canceled!", 
                       "error":"il_r013",
                       "status":402}
            ErrorLogger().logError(message)   
            return message

        try:
            # global_id = UniqueNumber.globalIdentifier(self) 
            #Check if wallet has the amount entered           
            date_created = Localtime().gettime()
                
            rollover_fee_demandnote_pay = {
                                        "description":"Defaulted loan fine was not paid!",
                                        "status":201
                                       }
            
            totalloan_paid = 0

            cur.execute("""SELECT id, loan_id, type, amount_due FROM loan_rollover_fee_demand_note_details WHERE status=1 AND customer_id = %s AND payment_in_progress =0 AND amount_due > 0 ORDER BY id ASC""", (customer_id))
            pending_defaulted_loan_fines = cur.fetchall() 
            if pending_defaulted_loan_fines:     
                for demand_note in pending_defaulted_loan_fines:
                    demandnote_id = demand_note['id']
                    loan_id = demand_note['loan_id']
                    rollover_type = demand_note['type']
                    demandnote_amount_due = float(demand_note['amount_due']) 
                    
                    #Update progress status
                    cur.execute("""UPDATE loan_rollover_fee_demand_note_details set payment_in_progress =2 WHERE id = %s""", (demandnote_id))
                    mysql.get_db().commit()
                
                    if demandnote_amount_due >0:
                        
                        #Retrieve funds to use
                        cur.execute("""SELECT funds_to_use FROM loan_prepayment_funds WHERE customer_id = %s""", [customer_id]) 
                        getfunds_touse_details = cur.fetchone() 
                        if getfunds_touse_details:
                            funds_to_use = float(getfunds_touse_details["funds_to_use"])

                            if funds_to_use >0:
                                if demandnote_amount_due > funds_to_use:
                                    payment_amount = funds_to_use

                                elif demandnote_amount_due == funds_to_use:

                                    payment_amount = funds_to_use
                                    
                                elif demandnote_amount_due < funds_to_use and funds_to_use > 0:
                                    payment_amount = demandnote_amount_due
                                    
                                else:
                                    payment_amount = 0
                                
                                if payment_amount >0:
                                    
                                    #Call API to pay principal demand note
                                    details = {
                                        "demand_note_id":demandnote_id,
                                        "amount":payment_amount,
                                        "global_id":global_id,
                                        "customer_id":customer_id,
                                        "loan_id":loan_id,
                                        "rollover_type":rollover_type
                                    }
                                    totalloan_paid = totalloan_paid + payment_amount
                                    rollover_fee_demandnote_pay = Repay_Loans().pay_rollover_fee_demand_note(details)
                                
                            else:
                                pass
                    
                    cur.execute("""UPDATE loan_rollover_fee_demand_note_details SET payment_in_progress = 0 WHERE id = %s""",(demandnote_id))
                    mysql.get_db().commit()
                    
            if totalloan_paid > 0:
                #CALL SMS API to notify customer of successful loan payment
                #Get inventory id to use -> get this from loan inventory settings
                cur.execute("""SELECT inventory_id, price_per_item FROM sms_details WHERE status =1 ORDER BY id DESC LIMIT 1 """)
                sms_details = cur.fetchone() 
                if sms_details:
                    cost_per_item = float(sms_details["price_per_item"])
                    inventory_id = sms_details["inventory_id"]
                else:
                    res = {"status":402,
                            "error":"il_r017",
                            "description":"Task was not successful. Price per sms was not found!"}
                    ErrorLogger().logError(res) 
                    return res
                
                try:
                    cur.execute("""SELECT (SUM(d.amount_due)) as amount_due FROM loan_rollover_fee_demand_note_details As d INNER JOIN loans as l ON l.id = d.loan_id WHERE l.customer_id = %s AND d.amount_due > 0 AND d.status =1 """, [customer_id])
                    total_loans = cur.fetchone()
                    if total_loans:
                        totalloans = float(total_loans["amount_due"])
                except:
                    totalloans = 0
                
                #loan_id
                
                sms_message = f"Dear {first_name}, Ksh {totalloan_paid:,.2f} from your Wallet Account has been used to pay rollover fine.\n"
                if totalloans > 0:
                    sms_message += f"Total pending rollover fine is Ksh {totalloans:,.2f}"
                else:
                    sms_message += "Rollover fine has now been paid."

                sms_details = {
                                "entry_id":loan_id, 
                                "date_consumed":date_created, 
                                "global_id":global_id,
                                "msisdn":msisdn,
                                "content":sms_message, 
                                "inventory_id":inventory_id,   
                                "cost_per_item":cost_per_item,                                
                                "type": "loan_repayment"
                                }
                    
                    
                # sms_response = Inventory().sms_inventory_consumed(sms_details)
                        
                demand_notes_paid_api_responses = {"rollover_fee_demand_note_payment_status":rollover_fee_demandnote_pay}
                return demand_notes_paid_api_responses 
            
            else:
                demand_notes_paid_api_responses = {"rollover_fee_demand_note_payment_status":rollover_fee_demandnote_pay}
                return demand_notes_paid_api_responses                
            
        except Exception as error:
            message = {"status":501,
                       "error":"il_r018",
                       "description":"Transaction execution failed. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            cur.close()

    def customer_initiated_demand_notes_repayment(self, selfpayment_demandnotes):
        #Get the request data 
        if selfpayment_demandnotes == None:
            message = {"description":"Transaction is missing some details!", 
                       "error":"il_r011",
                       "status": 402}
            ErrorLogger().logError(message)   
            return message

        customer_id = selfpayment_demandnotes["customer_id"] 
        global_id = selfpayment_demandnotes["global_id"]
        loan_type = int(selfpayment_demandnotes["loan_type"])
       
        #Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "error":"il_r012",
                       "status": 500}
            ErrorLogger().logError(message)   
            return message
       
        #Get customer details
        cur.execute("""SELECT first_name, msisdn FROM customer_details WHERE id = %s """, [customer_id])
        get_customer = cur.fetchone()
        if get_customer:
            msisdn = get_customer["msisdn"]
            first_name = get_customer["first_name"]

        else:                
            message = {"description":"Customer details were not found! Transaction canceled!", 
                       "error":"il_r013",
                       "status":402}
            ErrorLogger().logError(message)   
            return message
        
        try:
            # global_id = UniqueNumber.globalIdentifier(self) 
            #Check if wallet has the amount entered           
            date_created = Localtime().gettime()
                
                
            #check if customer has any pending demand notes
            principal_demandnote_pay = {
                                        "description":"Loan principal was not paid!",
                                        "status":201
                                       }
            interest_demandnote_pay = {
                                        "description":"Loan interest was not paid!",
                                        "status":201
                                       }

            charge_demandnote_pay = {
                                      "description":"Loan charge was not paid!",
                                      "status":201
                                    }
            
            totalloan_paid = 0
            
            # cur.execute("""SELECT id FROM loans WHERE principal_amount_due > 0 OR interest_amount_due > 0 OR charge_amount_due > 0 AND status =1 AND customer_id = %s ORDER BY id ASC""", [customer_id])
            # total_loans = cur.fetchall()
            # if total_loans:
            #     for loan_item in total_loans:
            #         loan_id = loan_item['id']

            if loan_type ==1:
                cur.execute("""SELECT d.id, d.loan_id, d.amount_due FROM loan_demand_notes As d INNER JOIN loans As l ON d.loan_id = l.id WHERE d.status=1 AND d.customer_id = %s AND d.amount_due > 0 AND l.product_class =1 ORDER BY d.expected_payment_date ASC""", (customer_id))
                pending_demand_notes = cur.fetchall()
                
                if pending_demand_notes:
                    pass
                else:
            
                    cur.execute("""SELECT d.id, d.loan_id, d.amount_due FROM loan_demand_notes As d INNER JOIN loans As l ON d.loan_id = l.id WHERE d.status=1 AND d.customer_id = %s AND d.amount_due > 0 AND l.product_class =2 ORDER BY d.expected_payment_date ASC""", (customer_id))
                    pending_demand_notes = cur.fetchall()
                
            elif loan_type ==2:
                
                cur.execute("""SELECT d.id, d.loan_id, d.amount_due FROM loan_demand_notes As d INNER JOIN loans As l ON d.loan_id = l.id WHERE d.status=1 AND d.customer_id = %s AND d.amount_due > 0 AND l.product_class =2 ORDER BY d.expected_payment_date ASC""", (customer_id))
                pending_demand_notes = cur.fetchall()
                if pending_demand_notes:
                    pass
                else:
                    cur.execute("""SELECT d.id, d.loan_id, d.amount_due FROM loan_demand_notes As d INNER JOIN loans As l ON d.loan_id = l.id WHERE d.status=1 AND d.customer_id = %s AND d.amount_due > 0 ORDER BY d.expected_payment_date ASC""", (customer_id))
                    pending_demand_notes = cur.fetchall()
                    
            else:
                cur.execute("""SELECT d.id, d.loan_id, d.amount_due FROM loan_demand_notes As d INNER JOIN loans As l ON d.loan_id = l.id WHERE d.status=1 AND d.customer_id = %s AND d.amount_due > 0 ORDER BY d.expected_payment_date ASC""", (customer_id))
                pending_demand_notes = cur.fetchall()
                
            if pending_demand_notes:     
                for demand_note in pending_demand_notes:
                    demandnote_id = demand_note['id']
                    loan_id = demand_note['loan_id']
                    demandnote_amount_due = float(demand_note['amount_due']) 
                    
                    cur.execute("""UPDATE loan_demand_notes SET payment_in_progress = 1 WHERE id = %s""",(demandnote_id))
                    mysql.get_db().commit()
                
                    if demandnote_amount_due >0:
                       
                     
                        #Call specific demand note details pay against
                        cur.execute("""SELECT * FROM loan_demand_note_details WHERE amount_due >0 AND status = 1 AND demandnote_id = %s ORDER BY id ASC""", [demandnote_id]) 
                        pending_specific_demand_notes = cur.fetchall()
                        for specific_demand_note in pending_specific_demand_notes:                                   
                                specificdemandnote_id = specific_demand_note['id']
                                specificdemandnote_type = str(specific_demand_note['type'])
                                specificdemandnote_amount_due = float(specific_demand_note['amount_due'])
                                
                                
                                #Retrieve funds to use
                                cur.execute("""SELECT funds_to_use, wallet_balance FROM loan_prepayment_funds WHERE customer_id = %s""", [customer_id]) 
                                getfunds_touse_details = cur.fetchone() 
                                if getfunds_touse_details:
                                    funds_to_use = float(getfunds_touse_details["funds_to_use"])
                                    wallet_balance = float(getfunds_touse_details["wallet_balance"])

                                    if funds_to_use >0:
                                        if demandnote_amount_due > funds_to_use:
                                            payment_amount = funds_to_use
                                            
                                        elif demandnote_amount_due == funds_to_use:

                                            payment_amount = funds_to_use
                                            
                                        elif demandnote_amount_due < funds_to_use and funds_to_use > 0:
                                            if funds_to_use > wallet_balance:
                                                payment_amount = wallet_balance
                                            
                                            else:
                                                payment_amount = demandnote_amount_due
                                            
                                        else:
                                            payment_amount = 0
                                            
                                        if payment_amount >0:
                                            
                                            if specificdemandnote_amount_due > payment_amount:
                                                specificdemandnote_amount_topay = payment_amount

                                                if specificdemandnote_type == 'principal':
                                                    
                        
                                                    #Call API to pay principal demand note
                                                    details = {
                                                        "demand_note_id":specificdemandnote_id,
                                                        "amount":specificdemandnote_amount_topay,
                                                        "global_id":global_id,
                                                        "customer_id":customer_id
                                                    }
                                                    totalloan_paid = totalloan_paid + specificdemandnote_amount_topay
                                                    principal_demandnote_pay = Repay_Loans().pay_principal_demand_note(details)
                                                    
                                                elif specificdemandnote_type == 'interest':
                                                        
                                                        details = {
                                                            "demand_note_id":specificdemandnote_id,
                                                            "amount":specificdemandnote_amount_topay,
                                                            "global_id":global_id,
                                                            "customer_id":customer_id
                                                        }
                                                        totalloan_paid = totalloan_paid + specificdemandnote_amount_topay
                                                        interest_demandnote_pay = Repay_Loans().pay_interest_demand_note(details)
                                                    
                                                elif specificdemandnote_type == 'charge':
                                                        details = {
                                                            "demand_note_id":specificdemandnote_id,
                                                            "amount":specificdemandnote_amount_topay,
                                                            "global_id":global_id,
                                                            "customer_id":customer_id
                                                        }
                                                        totalloan_paid = totalloan_paid + specificdemandnote_amount_topay
                                                        charge_demandnote_pay = Repay_Loans().pay_charge_demand_note(details)

                                                else:
                                                    message = {"description":"Could not find demand note to be paid!", 
                                                                "error":"il_r014",
                                                                "status": 402}
                                                    ErrorLogger().logError(message)   
                                                    return message

                                            elif specificdemandnote_amount_due == payment_amount:
                                                    specificdemandnote_amount_topay = payment_amount
                                                    if specificdemandnote_type == 'principal':
                                                    
                                                        # print("Call API to pay principal demand note")
                                                        details = {
                                                            "demand_note_id":specificdemandnote_id,
                                                            "amount":specificdemandnote_amount_topay,
                                                            "global_id":global_id,
                                                            "customer_id":customer_id
                                                        }
                                                        totalloan_paid = totalloan_paid + specificdemandnote_amount_topay
                                                        principal_demandnote_pay = Repay_Loans().pay_principal_demand_note(details)

                                                        #if successful - reduce amount to deduct in the database
                                                    elif specificdemandnote_type == 'interest':
                                            
                                                        # print("Call API to pay interest demand note")
                                                        details = {
                                                            "demand_note_id":specificdemandnote_id,
                                                            "amount":specificdemandnote_amount_topay,
                                                            "global_id":global_id,
                                                            "customer_id":customer_id
                                                        }
                                                        totalloan_paid = totalloan_paid + specificdemandnote_amount_topay
                                                        interest_demandnote_pay = Repay_Loans().pay_interest_demand_note(details)

                                                        #if successful - reduce amount to deduct in the database
                                    
                                                    elif specificdemandnote_type == 'charge':
                                                        details = {
                                                            "demand_note_id":specificdemandnote_id,
                                                            "amount":specificdemandnote_amount_topay,
                                                            "global_id":global_id,
                                                            "customer_id":customer_id
                                                        }
                                                        totalloan_paid = totalloan_paid + specificdemandnote_amount_topay
                                                        charge_demandnote_pay = Repay_Loans().pay_charge_demand_note(details)


                                                    #if successful - reduce amount to deduct in the database
                                                    else:
                                                        message = {"description":"Could not find demand note to be paid!", 
                                                                    "error":"il_r015",
                                                                    "status": 402}
                                                        ErrorLogger().logError(message)   
                                                        return message
                                
                                
                                            elif specificdemandnote_amount_due < payment_amount:
                                                    specificdemandnote_amount_topay = specificdemandnote_amount_due

                                                    if specificdemandnote_type == 'principal':
                                                        
                                                        details = {
                                                            "demand_note_id":specificdemandnote_id,
                                                            "amount":specificdemandnote_amount_topay,
                                                            "global_id":global_id,
                                                            "customer_id":customer_id
                                                        }
                                                        totalloan_paid = totalloan_paid + specificdemandnote_amount_topay
                                                        principal_demandnote_pay = Repay_Loans().pay_principal_demand_note(details)

                                                        
                                                        #if successful - reduce amount to deduct in the database

                                                    elif specificdemandnote_type == 'interest':
                                                        
                                                        details = {
                                                            "demand_note_id":specificdemandnote_id,
                                                            "amount":specificdemandnote_amount_topay,
                                                            "global_id":global_id,
                                                            "customer_id":customer_id
                                                        }
                                                        totalloan_paid = totalloan_paid + specificdemandnote_amount_topay
                                                        interest_demandnote_pay = Repay_Loans().pay_interest_demand_note(details)

                                                        #if successful - reduce amount to deduct in the database

                                                    elif specificdemandnote_type == 'charge':
                                                        details = {
                                                            "demand_note_id":specificdemandnote_id,
                                                            "amount":specificdemandnote_amount_topay,
                                                            "global_id":global_id,
                                                            "customer_id":customer_id
                                                        }
                                                        totalloan_paid = totalloan_paid + specificdemandnote_amount_topay
                                                        charge_demandnote_pay = Repay_Loans().pay_charge_demand_note(details)

                                                        #if successful - reduce amount to deduct in the database

                                                    else:
                                                        message = {"description":"Could not find demand note to be paid!", 
                                                                    "error":"il_r016",
                                                                    "status": 402}
                                                        ErrorLogger().logError(message)   
                                                        return message
                                
                                            else:
                                                specificdemandnote_amount_topay = 0
                                    
                                    else:
                                        pass
        
                        
                        cur.execute("""UPDATE loan_demand_notes SET payment_in_progress = 0 WHERE id = %s""",(demandnote_id))
                        mysql.get_db().commit()
                        
            if totalloan_paid > 0:
                
                #CALL SMS API to notify customer of successful loan payment
                #Get inventory id to use -> get this from loan inventory settings
                cur.execute("""SELECT inventory_id, price_per_item FROM sms_details WHERE status =1 ORDER BY id DESC LIMIT 1 """)
                sms_details = cur.fetchone() 
                if sms_details:
                    cost_per_item = float(sms_details["price_per_item"])
                    inventory_id = sms_details["inventory_id"]
                else:
                    res = {"status":402,
                            "error":"il_r017",
                            "description":"Task was not successful. Price per sms was not found!"}
                    ErrorLogger().logError(res) 
                    return res
                
                try:
                    cur.execute("""SELECT (SUM(d.amount_due)) as amount_due FROM loan_demand_notes As d INNER JOIN loans as l ON l.id = d.loan_id WHERE l.customer_id = %s AND d.amount_due > 0 AND d.status =1 """, [customer_id])
                    total_loans = cur.fetchone()
                    if total_loans:
                        totalloans = float(total_loans["amount_due"])
                except:
                    totalloans = 0
                
                #loan_id
                
                sms_message = f"Dear {first_name}, Ksh {totalloan_paid:,.2f} from your Wallet Account has been used to pay your loan.\n"
                if totalloans > 0:
                    sms_message += f"Loan balance is Ksh {totalloans:,.2f}"
                else:
                    sms_message += "The loan has now been fully paid."

                sms_details = {
                                "entry_id":loan_id, 
                                "date_consumed":date_created, 
                                "global_id":global_id,
                                "msisdn":msisdn,
                                "content":sms_message, 
                                "inventory_id":inventory_id,   
                                "cost_per_item":cost_per_item,                                
                                "type": "loan_repayment"
                                }
                    
                    
                # sms_response = Inventory().sms_inventory_consumed(sms_details)
                        
                demand_notes_paid_api_responses = {"principal_demand_note_payment_status":principal_demandnote_pay, 
                                                   "interest_demand_note_payment_status":interest_demandnote_pay,
                                                   "charge_demand_note_payment_status":charge_demandnote_pay,
                                }
                return demand_notes_paid_api_responses                

            else:
                demand_notes_paid_api_responses = {"principal_demand_note_payment_status":principal_demandnote_pay, 
                                                   "interest_demand_note_payment_status":interest_demandnote_pay,
                                                   "charge_demand_note_payment_status":charge_demandnote_pay}
                
                return demand_notes_paid_api_responses              
            
        except Exception as error:
            message = {"status":501,
                       "error":"il_r018",
                       "description":"Transaction execution failed. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            cur.close() 
         
    def customer_initiated_demand_note_creation(self, selfcreated_demandnotes):
            #Refer to Daemons_module - daemon demand note queue function. They are co-related.
       
        #Get the request data      
        if selfcreated_demandnotes == None:
            message = {"description":"Transaction is missing some details!", 
                       "error":"il_r006",
                       "status": 402}
            ErrorLogger().logError(message)
            return message

        global_id = selfcreated_demandnotes["global_id"]         
        customer_id = selfcreated_demandnotes["customer_id"] 
        loan_type = int(selfcreated_demandnotes["loan_type"])
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "error":"il_r007",
                       "status": 500}
            ErrorLogger().logError(message)
            return message
        
        #Try except block to handle execute task
        principal_demand_note_res = {
                                    "description":"Loan principal demand note was not created!",
                                    "status":201
                                    }

        interest_demand_note_res = {
                                    "description":"Loan interest demand note was not created!",
                                    "status":201
                                    }

        charges_demand_note_res = {
                                    "description":"Loan charge demand note was not created!",
                                    "status":201
                                    }
        demand_note_res = {
                                    "description":"Main demand note was not created!",
                                    "status":201
                                    }
        try:
            #Get customer loan details
            #retrieve funds to use
            cur.execute("""SELECT funds_to_use FROM loan_prepayment_funds WHERE customer_id = %s""", [customer_id]) 
            getfunds_touse_details = cur.fetchone() 
            if getfunds_touse_details:
                funds_to_use = float(getfunds_touse_details["funds_to_use"])

            else:
                funds_to_use = 0
                message = {"description":"There are no funds to generate demands notes!",
                           "error":"il_r008",
                           "status":404}
                ErrorLogger().logError(message)
                return message 
            
            available_funds = funds_to_use
            
        
            if loan_type ==1:
                cur.execute("""SELECT id, outstanding_installments, total_installments, product_class FROM loans WHERE customer_id = %s AND demandnote_cronjob_status = 0 AND (principal_amount_due + interest_amount_due + charge_amount_due) > 0 AND outstanding_installments > 0 ORDER BY product_class ASC""", [customer_id])
                loandetails = cur.fetchall() 
                
            elif loan_type ==2:
                cur.execute("""SELECT id, outstanding_installments, total_installments, product_class FROM loans WHERE customer_id = %s AND demandnote_cronjob_status = 0 AND (principal_amount_due + interest_amount_due + charge_amount_due) > 0 AND outstanding_installments > 0 ORDER BY product_class DESC""", [customer_id])
                loandetails = cur.fetchall() 
                
            else:
                cur.execute("""SELECT id, outstanding_installments, total_installments, product_class FROM loans WHERE customer_id = %s AND demandnote_cronjob_status = 0 AND (principal_amount_due + interest_amount_due + charge_amount_due) > 0 AND outstanding_installments > 0""", [customer_id])
                loandetails = cur.fetchall() 
                
            if loandetails:
                for loandetail in loandetails:
                    
                    loan_id = loandetail["id"]
                    outstanding_installments = int(loandetail["outstanding_installments"])
                    
                    total_installments = int(loandetail["total_installments"])
                    product_class = int(loandetail["product_class"])
                    
                    if available_funds > 0:
                          
                            cur.execute("""SELECT * FROM loans WHERE id = %s""", [loan_id])
                            getloan = cur.fetchone() 

                            customer_id = getloan["customer_id"]
                            product_class = int(getloan["product_class"])
                            defaulted_loan_fines_applied_after = int(getloan["defaulted_loan_fines_applied_after"])
                            demand_note_amount = float(getloan["next_installment_amount"])
                            next_installment_date = getloan["next_installment_date"]
                            outstanding_principal_demandnote_amount = float(getloan["outstanding_principal_demandnote_amount"])
                            outstanding_interest_demandnote_amount = float(getloan["outstanding_interest_demandnote_amount"]) 
                            outstanding_charge_demandnote_amount = float(getloan["outstanding_charge_demandnote_amount"])
                            
                            principal_amount_due = float(getloan["principal_amount_due"])
                            interest_amount_due = float(getloan["interest_amount_due"])
                            charge_amount_due = float(getloan["charge_amount_due"])
                            number_of_installments = int(getloan["total_installments"])
                            
                            principal_amount = float(getloan["principal_amount"])
                            
                            principal_per_installment = (principal_amount / number_of_installments)
                            
                            
                            if (total_installments == outstanding_installments and product_class ==2):
                                demand_note_amount = demand_note_amount
                                
                            elif (total_installments > outstanding_installments and product_class ==2):
                                if outstanding_principal_demandnote_amount > principal_per_installment:
                                    
                                    interest_to_demand = demand_note_amount - principal_per_installment
                                    
                                    demand_note_amount = demand_note_amount - interest_to_demand 
                                else:
                                    demand_note_amount = outstanding_principal_demandnote_amount
                                    
                            elif (total_installments == outstanding_installments and product_class ==1):
                                demand_note_amount = demand_note_amount
                            else:
                                pass
                            
                            
                            interest_id = getloan["interest_id"]
                            loan_repayment_type = int(getloan["loan_repayment_type"])

                            if loan_repayment_type ==1:
                                payment_order = getloan["repayment_merge_details"]
                                payment_order = json.loads(payment_order)
                            
                            elif loan_repayment_type ==2:
                                payment_order = getloan["repayment_split_details"]
                                payment_order = json.loads(payment_order)
                            else:
                                payment_order = ''
                                pass

                            #Get loan asset account
                            cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =5 AND owner_id = %s AND entity_id = %s """, (customer_id, loan_id))
                            get_loan_asset_account = cur.fetchone() 
                            if get_loan_asset_account:
                                loan_asset_account = get_loan_asset_account["number"]
                            else:
                                message = {"status":200,
                                           "description":"Task was not successful. Asset loan account is missing!"}
                                return message
                        
                            #Get Customer Receivable Account - Check if customer receivable account exists for this specific loan product          
                            cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =3 AND owner_id = %s AND entity_id = %s """, [customer_id, loan_id])
                            get_receivable_account = cur.fetchone() 
                            if get_receivable_account:
                                receivable_account = get_receivable_account["number"]                    
                            else:
                                #Get customer details
                                cur.execute("""SELECT first_name, last_name, created_by FROM customer_details WHERE id = %s """, [customer_id])
                                get_customer = cur.fetchone()
                                if get_customer:
                                    first_name = get_customer["first_name"]
                                    last_name = get_customer["last_name"]
                                    created_by = get_customer["created_by"]
                                
                                accountName = first_name + " " + " " + last_name
                                type_Id = 3  # receivable account
                                categoryId = 18
                                sub_category = 0
                                mainaccount = 0
                                openingBalance = 0
                                notes = ''
                                owner_id = customer_id
                                entity_id = loan_id
                                description = ''
                                referenceNumber = ''            
                    
                                account = {
                                        "name": accountName,
                                        "accountType": type_Id,
                                        "accountCategory": categoryId,
                                        "accountSubCategory": sub_category,
                                        "main_account": mainaccount,
                                        "opening_balance": openingBalance,
                                        "owner_id": owner_id,
                                        "entity_id": entity_id,
                                        "notes": notes,
                                        "description": description,
                                        "reference_number": referenceNumber,
                                        "user_id": created_by,
                                        "status":1}                

                                api_response = Account().create_new_account(account)
                                if int(api_response["status"] == 200):
                                    receivable_account = api_response["response"]["account_number"]

                            #Get interest earned income account
                            cur.execute("""SELECT number FROM accounts WHERE status =1 AND sub_category_id=2 AND type =14 AND owner_id = %s """, [interest_id])
                            get_interest_earned_account = cur.fetchone() 
                            if get_interest_earned_account:
                                interest_earned_account = get_interest_earned_account["number"]
                            else:
                                message = {"status":200,
                                           "description":"Task was not successful. Interest income account is missing!"}
                                ErrorLogger().logError(message) 
                                return message
                    
                            if (outstanding_principal_demandnote_amount + outstanding_interest_demandnote_amount + outstanding_charge_demandnote_amount) > 0:
                                #Create demand note
                                demandnote_id = UniqueNumber().demandnoteId()
                                demand_note_details = {
                                    "loan_id":loan_id,
                                    "global_id":global_id,
                                    "customer_id":customer_id,
                                    "demandnote_id":demandnote_id,
                                    "amount":demand_note_amount,
                                    "date_due":next_installment_date            
                                    }
                                
                                demand_note_res = CreateDemandNote().demand_note_creation(demand_note_details)
                                
                                if int(demand_note_res["status"]) == 200:
                                    
                                    if loan_repayment_type ==1 and product_class == 1:#merge repayments for individual loans
                                        #All Individual loans, principal is repaid first.
                                        pass
                                    
                                    elif loan_repayment_type ==2 and product_class == 1:#split repayments for individual loans.
                                    
                                        principal_demandnote_details = {
                                            "loan_asset_account":loan_asset_account,
                                            "receivable_account":receivable_account,
                                            "loan_id":loan_id,
                                            "customer_id":customer_id,
                                            "defaulted_loan_fines_applied_after":defaulted_loan_fines_applied_after,
                                            "global_id":global_id,
                                            "demandnote_id":demandnote_id,                  
                                            "date_due":next_installment_date            
                                            }
                                        
                                        interest_demandnote_details = {
                                            "interest_earned_account":interest_earned_account,
                                            "receivable_account":receivable_account,
                                            "interest_id":interest_id,
                                            "customer_id":customer_id,
                                            "loan_id":loan_id,
                                            "defaulted_loan_fines_applied_after":defaulted_loan_fines_applied_after,
                                            "global_id":global_id,
                                            "demandnote_id":demandnote_id,
                                            "date_due":next_installment_date            
                                            }

                                        charges_demandnote_details = {
                                            "receivable_account":receivable_account,
                                            "loan_id":loan_id,
                                            "customer_id":customer_id,
                                            "defaulted_loan_fines_applied_after":defaulted_loan_fines_applied_after,
                                            "global_id":global_id,
                                            "demandnote_id":demandnote_id,
                                            "date_due":next_installment_date            
                                            }
                                        #Rollover Fee Demand Notes
                                        #Defaulted Loan Fines Demand Notes

                                        principal_demand_note_res = {
                                                "description":"Loan principal was not created!",
                                                "status":201}

                                        interest_demand_note_res = {
                                                "description":"Loan interest was not created!",
                                                "status":201}

                                        charges_demand_note_res = {
                                                "description":"Loan charge was not created!",
                                                "status":201}
                                        
                                        if payment_order["1"] == 'Principal' :
                                            if outstanding_principal_demandnote_amount > 0:
                                                if outstanding_principal_demandnote_amount < demand_note_amount:
                                                    principal_demand_note_amount = outstanding_principal_demandnote_amount
                                                    #Generate principal demand note
                                                    
                                                    principal_demandnote_details["amount"] = principal_demand_note_amount     
                                                    principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId()                    
                                                    principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                                    if int(principal_demand_note_api["status"]) == 200:
                                                        principal_demand_note_res = {"description":"Principal demand note was created successfully!",
                                                                                    "status":200}
                                                        
                                                        #Move to the next payment order
                                                        next_demand_note_amount = demand_note_amount - principal_demand_note_amount
                                                        
                                                        if outstanding_interest_demandnote_amount > 0 and payment_order["2"] == 'Interest' :
                                                            if outstanding_interest_demandnote_amount < next_demand_note_amount:                                    
                                                                interest_demand_note_amount = outstanding_interest_demandnote_amount
                                                                #Generate Interest demand note
                                                                #The demand note will debit receivable account and credit asset loan account

                                                                interest_demandnote_details["amount"] = interest_demand_note_amount
                                                                interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                                if int(interest_demand_note_api["status"]) == 200:
                                                                        interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                                    "status":200}


                                                                next2_demand_note_amount = next_demand_note_amount - interest_demand_note_amount
                                                                #charges_demand_note_amount = next2_demand_note_amount

                                                                if outstanding_charge_demandnote_amount > 0:
                                                                        # print("outstanding_charge_demandnote_amount A")
                                                                        if outstanding_charge_demandnote_amount < next2_demand_note_amount: 
                                                                            charges_demand_note_amount = outstanding_charge_demandnote_amount 
                                                                            #Generate Charges demand note
                                                                            #The demand note will debit receivable account and credit asset loan account
                                                                            charges_demandnote_details["amount"] = charges_demand_note_amount
                                                                            charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                                            if int(charges_demand_note_api["status"]) == 200:
                                                                                charges_demand_note_res = {"description":"Charges demand note was created successfully!",
                                                                                                        "status":200}
                                                                        
                                                                        else:
                                                                            # print("outstanding_charge_demandnote_amount B")
                                                                            charges_demand_note_amount = next2_demand_note_amount 
                                                                            charges_demandnote_details["amount"] = charges_demand_note_amount
                                                                            charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                                            if int(charges_demand_note_api["status"]) == 200:
                                                                                charges_demand_note_res = {"description":"Charges demand note was created successfully!",
                                                                                                        "status":200}
                                                            
                                                            else:
                                                                if next_demand_note_amount > 0:
                                                                    interest_demand_note_amount = next_demand_note_amount
                                                                    #Generate Interest demand note
                                                                    #The demand note will debit receivable account and credit asset loan account

                                                                    interest_demandnote_details["amount"] = interest_demand_note_amount
                                                                    interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                    interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                                    if int(interest_demand_note_api["status"]) == 200:
                                                                        interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                                    "status":200}
                                                                        
                                                        if outstanding_interest_demandnote_amount == 0 and payment_order["2"] == 'Interest' :                                              
                                                            #If interest has been fully paid, then pay charges due
                                                            if outstanding_charge_demandnote_amount > 0:
                                                                    # print("outstanding_charge_demandnote_amount A")
                                                                    if outstanding_charge_demandnote_amount < next_demand_note_amount: 
                                                                        charges_demand_note_amount = outstanding_charge_demandnote_amount 
                                                                        #Generate Charges demand note
                                                                        #The demand note will debit receivable account and credit asset loan account
                                                                        charges_demandnote_details["amount"] = charges_demand_note_amount
                                                                        charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                                        if int(charges_demand_note_api["status"]) == 200:
                                                                            charges_demand_note_res = {"description":"Charges demand note was created successfully!",
                                                                                                    "status":200}
                                                                    
                                                                    else:
                                                                        # print("outstanding_charge_demandnote_amount B")
                                                                        charges_demand_note_amount = next_demand_note_amount 
                                                                        charges_demandnote_details["amount"] = charges_demand_note_amount
                                                                        charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                                        if int(charges_demand_note_api["status"]) == 200:
                                                                            charges_demand_note_res = {"description":"Charges demand note was created successfully!",
                                                                                                    "status":200}
                                                            
                                                        if outstanding_charge_demandnote_amount > 0 and payment_order["2"] == 'Charges' :
                                                            if outstanding_charge_demandnote_amount < next_demand_note_amount:                                    
                                                                charges_demand_note_amount = outstanding_charge_demandnote_amount
                                                                #Generate Charges demand note
                                                                #The demand note will debit receivable account and credit asset loan account

                                                                charges_demandnote_details["amount"] = charges_demand_note_amount
                                                                charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                                if int(charges_demand_note_api["status"]) == 200:
                                                                    charges_demand_note_res = {"description":"Charges demand note was created successfully!",
                                                                                            "status":200}

                                                                next2_demand_note_amount = next_demand_note_amount - charges_demand_note_amount
                                                                #charges_demand_note_amount = next2_demand_note_amount

                                                                if outstanding_interest_demandnote_amount > 0:
                                                                        # print("outstanding_interest_demandnote_amount A")
                                                                        if outstanding_interest_demandnote_amount < next2_demand_note_amount: 
                                                                            interest_demand_note_amount = outstanding_interest_demandnote_amount 
                                                                            #Generate interest demand note
                                                                            #The demand note will debit receivable account and credit asset loan account
                                                                            interest_demandnote_details["amount"] = interest_demand_note_amount
                                                                            interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                            interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                                            if int(interest_demand_note_api["status"]) == 200:
                                                                                interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                                            "status":200}
                                                                        
                                                                        else:
                                                                            interest_demand_note_amount = next2_demand_note_amount 
                                                                            interest_demandnote_details["amount"] = interest_demand_note_amount
                                                                            interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                            interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                                            if int(interest_demand_note_api["status"]) == 200:
                                                                                interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                                            "status":200}
                                                            
                                                            else:
                                                                if next_demand_note_amount > 0:
                                                                    charges_demand_note_amount = next_demand_note_amount
                                                                    #Generate Charges demand note
                                                                    #The demand note will debit receivable account and credit asset loan account

                                                                    charges_demandnote_details["amount"] = charges_demand_note_amount
                                                                    charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                                    if int(charges_demand_note_api["status"]) == 200:
                                                                        interest_demand_note_res = {"description":"Charges demand note was created successfully!",
                                                                                                    "status":200}
                                                                        
                                                        if outstanding_charge_demandnote_amount == 0 and payment_order["2"] == 'Charges' :
                                                            #if charges have been fully paid, move to the next payment due
                                                            if outstanding_interest_demandnote_amount > 0:
                                                                if outstanding_interest_demandnote_amount < next_demand_note_amount: 
                                                                    interest_demand_note_amount = outstanding_interest_demandnote_amount 
                                                                    #Generate interest demand note
                                                                    #The demand note will debit receivable account and credit asset loan account
                                                                    interest_demandnote_details["amount"] = interest_demand_note_amount
                                                                    interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                    interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                                    if int(interest_demand_note_api["status"]) == 200:
                                                                        interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                                    "status":200}
                                                                
                                                                else:
                                                                    interest_demand_note_amount = next_demand_note_amount 
                                                                    interest_demandnote_details["amount"] = interest_demand_note_amount
                                                                    interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                    interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                                    if int(interest_demand_note_api["status"]) == 200:
                                                                        interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                                    "status":200}
                                
                                                else:
                                                    if demand_note_amount > 0:
                                                            principal_demand_note_amount = demand_note_amount
                                                            #Generate principal demand note
                                                            #The demand note will debit receivable account and credit asset loan account

                                                            principal_demandnote_details["amount"] = principal_demand_note_amount   
                                                            principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId()   
                                                            principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                                            if int(principal_demand_note_api["status"]) == 200:
                                                                principal_demand_note_res = {"description":"Principal demand note was created successfully!",
                                                                                            "status":200}
                                            
                                            elif (outstanding_principal_demandnote_amount == 0 and outstanding_interest_demandnote_amount >0):
                                                
                                                if outstanding_interest_demandnote_amount < demand_note_amount:                                    
                                                    interest_demand_note_amount = outstanding_interest_demandnote_amount
                                                    #Generate Interest demand note
                                                    #The demand note will debit receivable account and credit asset loan account

                                                    interest_demandnote_details["amount"] = interest_demand_note_amount
                                                    interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                    interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                    if int(interest_demand_note_api["status"]) == 200:
                                                            interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                        "status":200}


                                                    next2_demand_note_amount = demand_note_amount - interest_demand_note_amount
                                                    #charges_demand_note_amount = next2_demand_note_amount

                                                    if outstanding_charge_demandnote_amount > 0:
                                                        # print("outstanding_charge_demandnote_amount A")
                                                        if outstanding_charge_demandnote_amount < next2_demand_note_amount: 
                                                            charges_demand_note_amount = outstanding_charge_demandnote_amount 
                                                            #Generate Charges demand note
                                                            #The demand note will debit receivable account and credit asset loan account
                                                            charges_demandnote_details["amount"] = charges_demand_note_amount
                                                            charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                            if int(charges_demand_note_api["status"]) == 200:
                                                                charges_demand_note_res = {"description":"Charges demand note was created successfully!",
                                                                                        "status":200}
                                                        
                                                        else:
                                                            # print("outstanding_charge_demandnote_amount B")
                                                            charges_demand_note_amount = next2_demand_note_amount 
                                                            charges_demandnote_details["amount"] = charges_demand_note_amount
                                                            charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                            if int(charges_demand_note_api["status"]) == 200:
                                                                charges_demand_note_res = {"description":"Charges demand note was created successfully!",
                                                                                        "status":200}
                                                            
                                                else:
                                                    if demand_note_amount > 0:
                                                        interest_demand_note_amount = demand_note_amount
                                                        #Generate Interest demand note
                                                        #The demand note will debit receivable account and credit asset loan account

                                                        interest_demandnote_details["amount"] = interest_demand_note_amount
                                                        interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                        interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                        if int(interest_demand_note_api["status"]) == 200:
                                                            interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                        "status":200}
                                            else:
                                                pass   
                                                                
                                        elif payment_order["1"] == 'Interest' :
                                            if outstanding_interest_demandnote_amount > 0:
                                                if outstanding_interest_demandnote_amount < demand_note_amount:
                                                    interest_demand_note_amount = outstanding_interest_demandnote_amount
                                                    #Generate interest demand note
                                                    
                                                    interest_demandnote_details["amount"] = interest_demand_note_amount     
                                                    interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId()   
                                                    interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                    if int(interest_demand_note_api["status"]) == 200:
                                                        interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                    "status":200}

                                                        #Move to the next payment order
                                                        next_demand_note_amount = demand_note_amount - interest_demand_note_amount
                                                        
                                                        if outstanding_principal_demandnote_amount > 0 and payment_order["2"] == 'Principal' :
                                                            if outstanding_principal_demandnote_amount < next_demand_note_amount:                                    
                                                                principal_demand_note_amount = outstanding_principal_demandnote_amount
                                                                #Generate principal demand note
                                                                #The demand note will debit receivable account and credit asset loan account

                                                                principal_demandnote_details["amount"] = principal_demand_note_amount
                                                                principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                
                                                                principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                                                if int(principal_demand_note_api["status"]) == 200:
                                                                    principal_demand_note_res = {"description":"Principal demand note was created successfully!",
                                                                                                "status":200}


                                                                next2_demand_note_amount = next_demand_note_amount - principal_demand_note_amount
                                                                #charges_demand_note_amount = next2_demand_note_amount

                                                                if outstanding_charge_demandnote_amount > 0:
                                                                        if outstanding_charge_demandnote_amount < next2_demand_note_amount: 
                                                                            charges_demand_note_amount = outstanding_charge_demandnote_amount 
                                                                            #Generate Charges demand note
                                                                            #The demand note will debit receivable account and credit asset loan account
                                                                            charges_demandnote_details["amount"] = charges_demand_note_amount
                                                                            
                                                                            charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                                            if int(charges_demand_note_api["status"]) == 200:
                                                                                charges_demand_note_res = {"description":"Charges demand note were created successfully!",
                                                                                                        "status":200}
                                                                        
                                                                        else:
                                                                            charges_demand_note_amount = next2_demand_note_amount 
                                                                            charges_demandnote_details["amount"] = charges_demand_note_amount
                                                                            
                                                                            charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                                            if int(charges_demand_note_api["status"]) == 200:
                                                                                charges_demand_note_res = {"description":"Charges demand note were created successfully!",
                                                                                                        "status":200}
                                                            
                                                            else:
                                                                if next_demand_note_amount > 0:
                                                                    principal_demand_note_amount = next_demand_note_amount
                                                                    #Generate principal demand note
                                                                    #The demand note will debit receivable account and credit asset loan account

                                                                    principal_demandnote_details["amount"] = principal_demand_note_amount
                                                                    principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                    principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                                                    if int(principal_demand_note_api["status"]) == 200:
                                                                        principal_demand_note_res = {"description":"Principal demand note was created successfully!",
                                                                                                    "status":200}
                                                        
                                                        if outstanding_principal_demandnote_amount == 0 and payment_order["2"] == 'Principal' :
                                                            
                                                            if outstanding_charge_demandnote_amount > 0:
                                                                    if outstanding_charge_demandnote_amount < next_demand_note_amount: 
                                                                        charges_demand_note_amount = outstanding_charge_demandnote_amount 
                                                                        #Generate Charges demand note
                                                                        #The demand note will debit receivable account and credit asset loan account
                                                                        charges_demandnote_details["amount"] = charges_demand_note_amount
                                                                        
                                                                        charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                                        if int(charges_demand_note_api["status"]) == 200:
                                                                            charges_demand_note_res = {"description":"Charges demand note were created successfully!",
                                                                                                        "status":200}
                                                                    
                                                                    else:
                                                                        charges_demand_note_amount = next_demand_note_amount 
                                                                        charges_demandnote_details["amount"] = charges_demand_note_amount
                                                                        
                                                                        charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                                        if int(charges_demand_note_api["status"]) == 200:
                                                                            charges_demand_note_res = {"description":"Charges demand note were created successfully!",
                                                                                                        "status":200}
                    
                                                        if outstanding_charge_demandnote_amount > 0 and payment_order["2"] == 'Charges' :
                                                            if outstanding_charge_demandnote_amount < next_demand_note_amount:                                    
                                                                charges_demand_note_amount = outstanding_charge_demandnote_amount
                                                                #Generate charges demand note
                                                                #The demand note will debit receivable account and credit asset loan account

                                                                charges_demandnote_details["amount"] = charges_demand_note_amount                                                     
                                                                charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                                if int(charges_demand_note_api["status"]) == 200:
                                                                    charges_demand_note_res = {"description":"Charges demand note was created successfully!",
                                                                                                "status":200}


                                                                next2_demand_note_amount = next_demand_note_amount - charges_demand_note_amount
                                                                #charges_demand_note_amount = next2_demand_note_amount

                                                                if outstanding_principal_demandnote_amount > 0:
                                                                    if outstanding_principal_demandnote_amount < next2_demand_note_amount: 
                                                                        principal_demand_note_amount = outstanding_principal_demandnote_amount 
                                                                        #Generate Charges demand note
                                                                        #The demand note will debit receivable account and credit asset loan account
                                                                        principal_demandnote_details["amount"] = principal_demand_note_amount   
                                                                        principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                        
                                                                        principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                                                        if int(principal_demand_note_api["status"]) == 200:
                                                                            principal_demand_note_res = {"description":"Principal demand note were created successfully!",
                                                                                                        "status":200}
                                                                    
                                                                    else:
                                                                        principal_demand_note_amount = next2_demand_note_amount 
                                                                        principal_demandnote_details["amount"] = principal_demand_note_amount   
                                                                        principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                        
                                                                        principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                                                        if int(principal_demand_note_api["status"]) == 200:
                                                                            principal_demand_note_res = {"description":"Principal demand note were created successfully!",
                                                                                                        "status":200}
                                                            
                                                            else:
                                                                if next_demand_note_amount > 0:
                                                                    charges_demand_note_amount = next_demand_note_amount
                                                                    #Generate charges demand note
                                                                    #The demand note will debit receivable account and credit asset loan account

                                                                    charges_demandnote_details["amount"] = charges_demand_note_amount
                                                                    charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                                    if int(charges_demand_note_api["status"]) == 200:
                                                                        charges_demand_note_res = {"description":"Charges demand note was created successfully!",
                                                                                                    "status":200}
                                                        
                                                        if outstanding_charge_demandnote_amount == 0 and payment_order["2"] == 'Charges' :
                                                            if outstanding_principal_demandnote_amount > 0:
                                                                if outstanding_principal_demandnote_amount < next_demand_note_amount: 
                                                                    principal_demand_note_amount = outstanding_principal_demandnote_amount 
                                                                    #Generate principal demand note
                                                                    #The demand note will debit receivable account and credit asset loan account
                                                                    principal_demandnote_details["amount"] = principal_demand_note_amount   
                                                                    principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                    
                                                                    principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                                                    if int(principal_demand_note_api["status"]) == 200:
                                                                        principal_demand_note_res = {"description":"Principal demand note were created successfully!",
                                                                                                    "status":200}
                                                                
                                                                else:
                                                                    principal_demand_note_amount = next_demand_note_amount 
                                                                    principal_demandnote_details["amount"] = principal_demand_note_amount   
                                                                    principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                    
                                                                    principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                                                    if int(principal_demand_note_api["status"]) == 200:
                                                                        principal_demand_note_res = {"description":"Principal demand note were created successfully!",
                                                                                                    "status":200}
                                                
                                                
                                                else:
                                                    if demand_note_amount > 0:
                                                            interest_demand_note_amount = demand_note_amount
                                                            #Generate interest demand note
                                                            #The demand note will debit receivable account and credit asset loan account

                                                            interest_demandnote_details["amount"] = interest_demand_note_amount   
                                                            interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId()   
                                                            interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                            if int(interest_demand_note_api["status"]) == 200:
                                                                        interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                                    "status":200}
                            
                                        elif payment_order["1"] == 'Charges' :
                                            if outstanding_charge_demandnote_amount > 0:
                                                if outstanding_charge_demandnote_amount < demand_note_amount:
                                                    charges_demand_note_amount = outstanding_charge_demandnote_amount
                                                    #Generate charges demand note
                                                    
                                                    charges_demandnote_details["amount"] = charges_demand_note_amount                       
                                                    charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                    if int(charges_demand_note_api["status"]) == 200:
                                                        charges_demand_note_res = {"description":"Charges demand note were created successfully!",
                                                                                "status":200}

                                                        #Move to the next payment order
                                                        next_demand_note_amount = demand_note_amount - charges_demand_note_amount
                                                        
                                                        if outstanding_interest_demandnote_amount > 0 and payment_order["2"] == 'Interest' :
                                                            if outstanding_interest_demandnote_amount < next_demand_note_amount:                                    
                                                                interest_demand_note_amount = outstanding_interest_demandnote_amount
                                                                #Generate Interest demand note
                                                                #The demand note will debit receivable account and credit asset loan account

                                                                interest_demandnote_details["amount"] = interest_demand_note_amount
                                                                interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                                if int(interest_demand_note_api["status"]) == 200:
                                                                        interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                                    "status":200}


                                                                next2_demand_note_amount = next_demand_note_amount - interest_demand_note_amount
                                                                #charges_demand_note_amount = next2_demand_note_amount

                                                                if outstanding_principal_demandnote_amount > 0:
                                                                        # print("outstanding_principal_demandnote_amount A")
                                                                        if outstanding_principal_demandnote_amount < next2_demand_note_amount: 
                                                                            principal_demand_note_amount = outstanding_principal_demandnote_amount 
                                                                            #Generate outstanding_principal_demandnote_amount demand note
                                                                            #The demand note will debit receivable account and credit asset loan account
                                                                            principal_demandnote_details["amount"] = principal_demand_note_amount     
                                                                            principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                            principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                                                            if int(principal_demand_note_api["status"]) == 200:
                                                                                principal_demand_note_res = {"description":"Principal demand note was created successfully!",
                                                                                                            "status":200}
                                                                        
                                                                        else:
                                                                            # print("outstanding_principal_demandnote_amount B")
                                                                            principal_demand_note_amount = next2_demand_note_amount 
                                                                            principal_demandnote_details["amount"] = principal_demand_note_amount     
                                                                            principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                            principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                                                            if int(principal_demand_note_api["status"]) == 200:
                                                                                principal_demand_note_res = {"description":"Principal demand note was created successfully!",
                                                                                                            "status":200}
                                                            
                                                            else:
                                                                if next_demand_note_amount > 0:
                                                                    interest_demand_note_amount = next_demand_note_amount
                                                                    #Generate Interest demand note
                                                                    #The demand note will debit receivable account and credit asset loan account

                                                                    interest_demandnote_details["amount"] = interest_demand_note_amount
                                                                    interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                    interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                                    if int(interest_demand_note_api["status"]) == 200:
                                                                        interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                                    "status":200}
                                                        
                                                        if outstanding_interest_demandnote_amount == 0 and payment_order["2"] == 'Interest' :
                                                            #if interest demand note has been paid, move to the next demand note due for payment
                                                            if outstanding_principal_demandnote_amount > 0:
                                                                if outstanding_principal_demandnote_amount < next_demand_note_amount: 
                                                                    principal_demand_note_amount = outstanding_principal_demandnote_amount 
                                                                    #Generate outstanding_principal_demandnote_amount demand note
                                                                    #The demand note will debit receivable account and credit asset loan account
                                                                    principal_demandnote_details["amount"] = principal_demand_note_amount     
                                                                    principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                    principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                                                    if int(principal_demand_note_api["status"]) == 200:
                                                                        principal_demand_note_res = {"description":"Principal demand note was created successfully!",
                                                                                                        "status":200}
                                                                
                                                                else:
                                                                    # print("outstanding_principal_demandnote_amount B")
                                                                    principal_demand_note_amount = next_demand_note_amount 
                                                                    principal_demandnote_details["amount"] = principal_demand_note_amount     
                                                                    principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                    principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                                                    if int(principal_demand_note_api["status"]) == 200:
                                                                        principal_demand_note_res = {"description":"Principal demand note was created successfully!",
                                                                                                        "status":200}
                                    
                                                        if outstanding_principal_demandnote_amount > 0 and payment_order["2"] == 'Principal' :
                                                            if outstanding_principal_demandnote_amount < next_demand_note_amount:                                    
                                                                principal_demand_note_amount = outstanding_principal_demandnote_amount
                                                                #Generate principal demand note
                                                                #The demand note will debit receivable account and credit asset loan account

                                                                principal_demandnote_details["amount"] = principal_demand_note_amount
                                                                principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                                                if int(principal_demand_note_api["status"]) == 200:
                                                                        principal_demand_note_res = {"description":"Principal demand note was created successfully!",
                                                                                                    "status":200}

                                                                next2_demand_note_amount = next_demand_note_amount - principal_demand_note_amount
                                                            
                                                                if outstanding_interest_demandnote_amount > 0:
                                                                    if outstanding_interest_demandnote_amount < next2_demand_note_amount: 
                                                                        interest_demand_note_amount = outstanding_interest_demandnote_amount 
                                                                        #Generate outstanding_interest_demandnote_amount demand note
                                                                        #The demand note will debit receivable account and credit asset loan account
                                                                        interest_demandnote_details["amount"] = interest_demand_note_amount     
                                                                        interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                        interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                                        if int(interest_demand_note_api["status"]) == 200:
                                                                            interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                                        "status":200}
                                                                    
                                                                    else:
                                                                        # print("outstanding_interest_demandnote_amount B")
                                                                        interest_demand_note_amount = next2_demand_note_amount 
                                                                        interest_demandnote_details["amount"] = interest_demand_note_amount     
                                                                        interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                        interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                                        if int(interest_demand_note_api["status"]) == 200:
                                                                            interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                                        "status":200}
                                                            
                                                            else:
                                                                if next_demand_note_amount > 0:
                                                                    principal_demand_note_amount = next_demand_note_amount
                                                                    #Generate principal demand note
                                                                    #The demand note will debit receivable account and credit asset loan account

                                                                    principal_demandnote_details["amount"] = principal_demand_note_amount
                                                                    principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                    principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                                                    if int(principal_demand_note_api["status"]) == 200:
                                                                        principal_demand_note_res = {"description":"Principal demand note was created successfully!",
                                                                                                    "status":200}
                                                        
                                                        if outstanding_principal_demandnote_amount == 0 and payment_order["2"] == 'Principal' :
                                                            #If principal demand note has been paid, move to the next demand note due for payment
                                                            if outstanding_interest_demandnote_amount > 0:
                                                                if outstanding_interest_demandnote_amount < next_demand_note_amount: 
                                                                    interest_demand_note_amount = outstanding_interest_demandnote_amount 
                                                                    #Generate outstanding_interest_demandnote_amount demand note
                                                                    #The demand note will debit receivable account and credit asset loan account
                                                                    interest_demandnote_details["amount"] = interest_demand_note_amount     
                                                                    interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                    interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                                    if int(interest_demand_note_api["status"]) == 200:
                                                                        interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                                    "status":200}
                                                                
                                                                else:
                                                                    # print("outstanding_interest_demandnote_amount B")
                                                                    interest_demand_note_amount = next_demand_note_amount 
                                                                    interest_demandnote_details["amount"] = interest_demand_note_amount     
                                                                    interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                                                    interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                                                    if int(interest_demand_note_api["status"]) == 200:
                                                                        interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                                                    "status":200}
                                                        
                                                else:
                                                    if demand_note_amount > 0:
                                                            charges_demand_note_amount = demand_note_amount
                                                            #Generate charges demand note
                                                            #The demand note will debit receivable account and credit asset loan account

                                                            charges_demandnote_details["amount"] = charges_demand_note_amount   
                                                            charges_demand_note_api = CreateDemandNote().charges_demand_note_creation(charges_demandnote_details)
                                                            if int(charges_demand_note_api["status"]) == 200:
                                                                charges_demand_note_res = {"description":"Charges demand note was created successfully!",
                                                                                            "status":200}
                            
                                        else:
                                            pass
                                        
                                            
                                        available_funds = available_funds - demand_note_amount
                                       
                                    elif loan_repayment_type ==1 and product_class == 2:#merge repayments for group loans
                                        principal_demandnote_details = {
                                            "loan_asset_account":loan_asset_account,
                                            "receivable_account":receivable_account,
                                            "loan_id":loan_id,
                                            "customer_id":customer_id,
                                            "global_id":global_id,
                                            "demandnote_id":demandnote_id,                  
                                            "date_due":next_installment_date            
                                            }
                                        
                                        interest_demandnote_details = {
                                            "interest_earned_account":interest_earned_account,
                                            "receivable_account":receivable_account,
                                            "interest_id":interest_id,
                                            "customer_id":customer_id,
                                            "loan_id":loan_id,
                                            "global_id":global_id,
                                            "demandnote_id":demandnote_id,
                                            "date_due":next_installment_date            
                                            }
                            
                                        principal_demandnote_details["amount"] = principal_per_installment     
                                        principal_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId()                    
                                        principal_demand_note_api = CreateDemandNote().principal_demand_note_creation(principal_demandnote_details)
                                        if int(principal_demand_note_api["status"]) == 200:
                                            principal_demand_note_res = {"description":"Principal demand note was created successfully!",
                                                                         "status":200}
                                            
                                        
                                        if (total_installments == outstanding_installments and product_class ==2): #first installment demand note generation
                                            interest_demand_note_amount = demand_note_amount - principal_per_installment
                                            interest_demandnote_details["amount"] = interest_demand_note_amount
                                            interest_demandnote_details["subdemandnote_id"] = UniqueNumber().subdemandnoteId() 
                                            
                                            interest_demand_note_api = CreateDemandNote().interest_demand_note_creation(interest_demandnote_details)
                                            if int(interest_demand_note_api["status"]) == 200:
                                                interest_demand_note_res = {"description":"Interest demand note was created successfully!",
                                                                            "status":200}
                                            
                                            available_funds = available_funds - demand_note_amount
                                            ##There are no charges demand notes
                        
                                    elif loan_repayment_type ==2 and product_class == 2:#split repayments for group loans
                                        #This function does not exist. Group loans principal and interest is repaid collectively
                                        pass
                                    
                                    else:
                                        pass
                 
                demand_note_message = {"principal_demand_note_res":principal_demand_note_res, 
                                       "interest_demand_note_res":interest_demand_note_res,
                                       "charges_demand_note_res":charges_demand_note_res,
                                       "status":demand_note_res["status"],
                                       "description":demand_note_res["description"]
                                       }

                return demand_note_message
                    
            else:
                
                demand_note_message = {"principal_demand_note_res":principal_demand_note_res, 
                                       "interest_demand_note_res":interest_demand_note_res,
                                       "charges_demand_note_res":charges_demand_note_res,
                                       "status":demand_note_res["status"],
                                       "description":demand_note_res["description"]
                                       }
                ErrorLogger().logError(demand_note_message) 
                return demand_note_message
            
        except Exception as error:
            message = {"principal_demand_note_res":principal_demand_note_res, 
                       "interest_demand_note_res":interest_demand_note_res,
                       "charges_demand_note_res":charges_demand_note_res,
                       "status":501,
                       "error":"il_r010",
                       "description":"Transaction execution failed. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            cur.close() 
        
    def pay_defaulted_loan_fine_demand_note(self, details):
            #Get the request data        
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       "error":"il_r032",
                       "status": 402}
            ErrorLogger().logError(message)
            return message
        
        global_id = details["global_id"]  
        customer_id = details["customer_id"]  
        demand_note_id = details["demand_note_id"]
        amount = float(details["amount"])    
        amount = round(amount, 12) 
        payment_date = Localtime().gettime()

        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "error":"il_r033",
                       "status": 500}
            ErrorLogger().logError(message)
            return message

        #Try except block to handle execute task
        try:
            #Get principal demand note details
            cur.execute("""SELECT loan_id, charge_id FROM loan_defaulted_fines_demand_note_details WHERE id = %s """, [demand_note_id])
            demandnote_details = cur.fetchone() 
            if demandnote_details:
                loan_id = demandnote_details["loan_id"]
                charge_id = demandnote_details["charge_id"]
            else:
                message = {"status":201,
                           "error":"il_r034",
                           "description":"Task was not successful. Demand note was not found!!"}
                ErrorLogger().logError(message) 
                return message
                            
            #Get charge name
            cur.execute("""SELECT defaultedcharge_name FROM product_defaulted_charge_types WHERE id = %s """, [charge_id])
            charge_details = cur.fetchone() 
            if charge_details:
                fee_name = charge_details["defaultedcharge_name"]
            else:
                fee_name = ''
                        
            #Get Customer Receivable Account - Check if customer receivable account exists for this specific loan product             
                
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =3 AND owner_id = %s AND entity_id = %s """, [customer_id, loan_id])
            get_receivable_account = cur.fetchone() 
            if get_receivable_account:
                receivable_account = get_receivable_account["number"]

            #Get customer wallet account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =12 AND owner_id = %s """, [customer_id])
            get_wallet_account = cur.fetchone() 
            if get_wallet_account:
                wallet_account = get_wallet_account["number"]
            else:
                message = {"description":"Task was not successful. Customer wallet account was not found!", 
                           "error":"il_r035",
                           "status": 402}
                ErrorLogger().logError(message)
                return message
            #Get defaulted charge earned income account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND sub_category_id=2 AND type =14 AND owner_id = %s """, [charge_id])
            get_charge_earned_account = cur.fetchone() 
            if get_charge_earned_account:
                defaultedloan_fine_earned_account = get_charge_earned_account["number"]
            else:
                message = {"description":"Task was not successful. Charge income earned account was not found!", 
                           "error":"il_r036",
                           "status": 402}
                ErrorLogger().logError(message)
                return message
            
           

            #Get defaulted charge realized income account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND sub_category_id=1 AND type =14 AND owner_id = %s """, [charge_id])
            get_charge_realized_account = cur.fetchone() 
            
            if get_charge_realized_account:
                defaultedloan_fine_realized_account = get_charge_realized_account["number"]
            else:
                message = {"description":"Task was not successful. Charge income realized account was not found!", 
                           "error":"il_r037",
                           "status": 402}
                ErrorLogger().logError(message)
                return message
            
            

            details = {
                "loan_id":loan_id,
                "wallet_account":wallet_account,
                "receivable_account":receivable_account,
                "defaultedloan_fine_earned_account":defaultedloan_fine_earned_account,
                "defaultedloan_fine_realized_account":defaultedloan_fine_realized_account,
                "loan_id":loan_id,
                "global_id":global_id,
                "amount":amount,
                "payment_date":payment_date,
                "charge_name":fee_name            
                }
            
            demand_message = PayDemandNotes.defaulted_loan_fine_demand_note_payment(self, details)
            if int(demand_message["status"]) == 200:

                #Call API to record tax expense
                details = {"amount":amount,
                           "global_id":global_id,
                           "entry_id":loan_id
                        }
                record_tax_response = TaxExpenseIncurred().record_tax(details)

                if int(record_tax_response["status"]) == 200:
                    #Update principal demand note details.
                    localtime = Localtime().gettime()  
                    now = datetime.strptime(localtime, '%Y-%m-%d %H:%M:%S')
                    now = now.strftime('%Y-%m-%d')
                    cur.execute("""UPDATE loan_defaulted_fines_demand_note_details set payment_in_progress = 0, last_payment_date = %s, amount_due = amount_due - %s, amount_paid = amount_paid + %s WHERE id = %s""", (now, amount, amount, demand_note_id))
                    mysql.get_db().commit()
                    
                    #update 
                    cur.execute("""UPDATE loan_prepayment_funds set funds_to_use = funds_to_use - %s, wallet_balance = wallet_balance - %s, last_transaction_date = %s WHERE customer_id = %s""", (amount, amount, payment_date, customer_id))
                    mysql.get_db().commit()

                    #Update loan item.
                    cur.execute("""UPDATE loans set defaulted_loan_fines_paid = defaulted_loan_fines_paid + %s, defaulted_loan_fines_due = defaulted_loan_fines_due - %s WHERE id = %s""", (amount, amount, loan_id))
                    mysql.get_db().commit()
                
                else:
                    return record_tax_response

                return demand_message
            else:
                return demand_message


        except Exception as error:
            message = {'status':501,
                       "error":"il_r038",
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()

    def pay_rollover_fee_demand_note(self, details):
            #Get the request data        
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       "error":"il_r032",
                       "status": 402}
            ErrorLogger().logError(message)
            return message
        
        global_id = details["global_id"]  
        customer_id = details["customer_id"]  
        loan_id = details["loan_id"] 
        rollover_type = details["rollover_type"] 
        demand_note_id = details["demand_note_id"]
        amount = float(details["amount"])    
        amount = round(amount, 12) 
        payment_date = Localtime().gettime()

        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "error":"il_r033",
                       "status": 500}
            ErrorLogger().logError(message)
            return message

        #Try except block to handle execute task
        try:
            #Get rollover demand note details
            cur.execute("""SELECT rollover_id FROM loans WHERE id = %s """, [loan_id])
            demandnote_details = cur.fetchone() 
            if demandnote_details:
                charge_id = demandnote_details["rollover_id"]
            else:
                message = {"status":201,
                           "error":"il_r034",
                           "description":"Task was not successful. Loan was not found!!"}
                ErrorLogger().logError(message) 
                return message
                    
            #Get Customer Receivable Account - Check if customer receivable account exists for this specific loan product             
                
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =3 AND owner_id = %s AND entity_id = %s """, [customer_id, loan_id])
            get_receivable_account = cur.fetchone() 
            if get_receivable_account:
                receivable_account = get_receivable_account["number"]

            #Get customer wallet account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =12 AND owner_id = %s """, [customer_id])
            get_wallet_account = cur.fetchone() 
            if get_wallet_account:
                wallet_account = get_wallet_account["number"]
            else:
                message = {"description":"Task was not successful. Customer wallet account was not found!", 
                           "error":"il_r035",
                           "status": 402}
                ErrorLogger().logError(message)
                return message

            #Get rollover earned income account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND sub_category_id=2 AND type =14 AND owner_id = %s """, [charge_id])
            get_charge_earned_account = cur.fetchone() 
            if get_charge_earned_account:
                rollover_fee_earned_account = get_charge_earned_account["number"]
            else:
                message = {"description":"Task was not successful. Charge income earned account was not found!", 
                           "error":"il_r036",
                           "status": 402}
                ErrorLogger().logError(message)
                return message

            #Get interest earned income account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND sub_category_id=1 AND type =14 AND owner_id = %s """, [charge_id])
            get_charge_realized_account = cur.fetchone() 
            
            if get_charge_realized_account:
                rollover_fee_realized_account = get_charge_realized_account["number"]
            else:
                message = {"description":"Task was not successful. Rollover fee income realized account was not found!", 
                           "error":"il_r037",
                           "status": 402}
                ErrorLogger().logError(message)
                return message

            details = {
                "loan_id":loan_id,
                "wallet_account":wallet_account,
                "receivable_account":receivable_account,
                "rollover_fee_earned_account":rollover_fee_earned_account,
                "rollover_fee_realized_account":rollover_fee_realized_account,
                "loan_id":loan_id,
                "global_id":global_id,
                "amount":amount,
                "payment_date":payment_date,
                "rollover_type":rollover_type            
                }
            demand_message = PayDemandNotes.rollover_fee_demand_note_payment(self, details)
            if int(demand_message["status"]) == 200:

                #Call API to record tax expense
                details = {"amount":amount,
                           "global_id":global_id,
                           "entry_id":loan_id
                        }
                record_tax_response = TaxExpenseIncurred().record_tax(details)

                if int(record_tax_response["status"]) == 200:
                    #Update principal demand note details.
                    localtime = Localtime().gettime()  
                    now = datetime.strptime(localtime, '%Y-%m-%d %H:%M:%S')
                    now = now.strftime('%Y-%m-%d')
                    cur.execute("""UPDATE loan_rollover_fee_demand_note_details set payment_in_progress = 0, last_payment_date = %s, amount_due = amount_due - %s, amount_paid = amount_paid + %s WHERE id = %s""", (now, amount, amount, demand_note_id))
                    mysql.get_db().commit()
                    
                    #update 
                    cur.execute("""UPDATE loan_prepayment_funds set funds_to_use = funds_to_use - %s, wallet_balance = wallet_balance - %s, last_transaction_date = %s WHERE customer_id = %s""", (amount, amount, payment_date, customer_id))
                    mysql.get_db().commit()

                    #Update loan item.
                    cur.execute("""UPDATE loans set rollover_fee_paid = rollover_fee_paid + %s, rollover_fee_due = rollover_fee_due - %s WHERE id = %s""", (amount, amount, loan_id))
                    mysql.get_db().commit()
                
                else:
                    return record_tax_response

                return demand_message
            else:
                return demand_message


        except Exception as error:
            message = {'status':501,
                       "error":"il_r038",
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()
            
    def pay_principal_demand_note(self, details):
        #Get the request data 
           
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       "error":"il_r019",
                       "status": 402}
            ErrorLogger().logError(message)
            return message

        global_id = details["global_id"]
        customer_id = details["customer_id"]
        demand_note_id = details["demand_note_id"]
        amount = float(details["amount"])     
        amount = round(amount, 12)
        datecreated = Localtime().gettime()

        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "error":"il_r020",
                       "status": 500}
            ErrorLogger().logError(message)
            return message

        #Try except block to handle execute task
        try:
            #Get principal demand note details
            cur.execute("""SELECT loan_id, demandnote_id FROM loan_demand_note_details WHERE id = %s """, [demand_note_id])
            demandnote_details = cur.fetchone() 
            if demandnote_details:
                loan_id = demandnote_details["loan_id"]
                main_demandnote_id = demandnote_details["demandnote_id"]
            else:
                message = {"description":"Task was not successful. Demand note record was not found!", 
                           "error":"il_r021",
                           "status": 402}
                ErrorLogger().logError(message)
                return message
                                    
            #Get Customer Receivable Account - Check if customer receivable account exists for this specific loan product             
                
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =3 AND owner_id = %s AND entity_id = %s """, [customer_id, loan_id])
            get_receivable_account = cur.fetchone() 
            if get_receivable_account:
                receivable_account = get_receivable_account["number"]
            else:
                message = {"description":"Task was not successful. Receivable account was not found!", 
                           "error":"il_r022",
                           "status": 402}
                ErrorLogger().logError(message)
                return message

            #Get customer wallet account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =12 AND owner_id = %s """, [customer_id])
            get_wallet_account = cur.fetchone() 
            
            if get_wallet_account:
                wallet_account = get_wallet_account["number"]
            else:
                message = {"description":"Task was not successful. Wallet account was not found!", 
                           "error":"il_r023",
                           "status": 402}
                ErrorLogger().logError(message)
                return message

            details = {
                "loan_id":loan_id,
                "wallet_account":wallet_account,
                "receivable_account":receivable_account,
                "global_id":global_id,
                "amount":amount,
                "payment_date":datecreated            
                }
            
            
            demand_message = PayDemandNotes().principal_demand_note_payment(details)
            if int(demand_message["status"]) ==200:

                #Update demand notes details table.
                localtime = Localtime().gettime()  
                now = datetime.strptime(localtime, '%Y-%m-%d %H:%M:%S')
                now = now.strftime('%Y-%m-%d')
                cur.execute("""UPDATE loan_demand_note_details set last_payment_date = %s, amount_due = amount_due - %s, amount_paid = amount_paid + %s WHERE id = %s""", (now, amount, amount, demand_note_id))
                mysql.get_db().commit()
                
                #update 
                cur.execute("""UPDATE loan_prepayment_funds set funds_to_use = funds_to_use - %s, wallet_balance = wallet_balance - %s, last_transaction_date = %s WHERE customer_id = %s""", (amount, amount, datecreated, customer_id))
                mysql.get_db().commit()

                #Update demand notes table.
                cur.execute("""UPDATE loan_demand_notes set amount_due = amount_due - %s, amount_paid = amount_paid + %s WHERE id = %s""", (amount, amount, main_demandnote_id))
                mysql.get_db().commit()

                #Update loan item.
                cur.execute("""UPDATE loans set principal_amount_paid = principal_amount_paid + %s, principal_amount_due = principal_amount_due - %s WHERE id = %s""", (amount, amount, loan_id))
                mysql.get_db().commit()
            

                return demand_message
            else:
                return demand_message


        except Exception as error:
            message = {"status":501,
                       "error":"il_r024",
                       "description":"Transaction execution failed. Error description" + format(error)}
            ErrorLogger().logError(message)            
            return message
        finally:
            cur.close() 

    def pay_interest_demand_note(self, details):
        #Get the request data        
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       "error":"il_r025",
                       "status": 402}
            ErrorLogger().logError(message)
            return message
        
        global_id = details["global_id"] 
        customer_id = details["customer_id"] 
        demand_note_id = details["demand_note_id"]
        amount = float(details["amount"])  
        amount = round(amount, 12)   
        payment_date = Localtime().gettime()

        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "error":"il_r026",
                       "status": 500}
            ErrorLogger().logError(message)
            return message

        #Try except block to handle execute task
        try:
            #Get interest demand note details
            cur.execute("""SELECT loan_id, demandnote_id FROM loan_demand_note_details WHERE id = %s """, [demand_note_id])
            demandnote_details = cur.fetchone() 
            if demandnote_details:
                loan_id = demandnote_details["loan_id"]
                main_demandnote_id = demandnote_details["demandnote_id"]
            else:
                message = {"description":"Task was not successful. Demand not was not found!", 
                           "error":"il_r027",
                           "status": 402}
                ErrorLogger().logError(message)
                return message
            
            #Get customer loan details
            cur.execute("""SELECT interest_id FROM loans WHERE id = %s """, [loan_id])
            loandetails = cur.fetchone() 
            if loandetails:
                interest_id = loandetails["interest_id"]
            else:
                message = {"description":"Task was not successful. Loan details were not found!", 
                           "status": 402}
                ErrorLogger().logError(message)
                return message
                        
            #Get Customer Receivable Account - Check if customer receivable account exists for this specific loan product             
                
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =3 AND owner_id = %s AND entity_id = %s """, [customer_id, loan_id])
            get_receivable_account = cur.fetchone() 
            if get_receivable_account:
                receivable_account = get_receivable_account["number"]

            #Get customer wallet account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =12 AND owner_id = %s """, [customer_id])
            get_wallet_account = cur.fetchone() 
            if get_wallet_account:
                wallet_account = get_wallet_account["number"]
            else:
                message = {"description":"Task was not successful. Customer wallet account was not found!", 
                           "error":"il_r028",
                           "status": 402}
                ErrorLogger().logError(message)
                return message

            #Get interest earned income account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND sub_category_id=2 AND type =14 AND owner_id = %s """, [interest_id])
            get_interest_earned_account = cur.fetchone() 
            if get_interest_earned_account:
                interest_earned_account = get_interest_earned_account["number"]
            else:
                message = {"description":"Task was not successful. Interest income earned account was not found!", 
                           "error":"il_r029",
                           "status": 402}
                ErrorLogger().logError(message)
                return message

            #Get interest realized income account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND sub_category_id=1 AND type =14 AND owner_id = %s """, [interest_id])
            get_interest_realized_account = cur.fetchone() 
            
            if get_interest_realized_account:
                interest_realized_account = get_interest_realized_account["number"]
            else:
                message = {"description":"Task was not successful. Interest income realized account was not found!", 
                           "error":"il_r030",
                           "status": 402}
                ErrorLogger().logError(message)
                return message

            details = {
                "loan_id":loan_id,
                "wallet_account":wallet_account,
                "receivable_account":receivable_account,
                "interest_earned_account":interest_earned_account,
                "interest_realized_account":interest_realized_account,
                "loan_id":loan_id,
                "global_id":global_id,
                "amount":amount,
                "payment_date":payment_date            
                }
            demand_message = PayDemandNotes().interest_demand_note_payment(details)
            if int(demand_message["status"]) == 200:

                #Call API to record tax expense
                details = {"amount":amount,
                           "global_id":global_id,
                           "entry_id":loan_id
                       }
                record_tax_response = TaxExpenseIncurred().record_tax(details)
                if int(record_tax_response["status"]) == 200:
                    #Update principal demand note details.
                    localtime = Localtime().gettime()  
                    now = datetime.strptime(localtime, '%Y-%m-%d %H:%M:%S')
                    now = now.strftime('%Y-%m-%d')
                    cur.execute("""UPDATE loan_demand_note_details set last_payment_date = %s, amount_due = amount_due - %s, amount_paid = amount_paid + %s WHERE id = %s""", (now, amount, amount, demand_note_id))
                    mysql.get_db().commit()
                    # cur.execute("""UPDATE loan_demand_note_details set last_payment_date = %s, amount_due = CASE WHEN (amount_due - %s) >= 0 THEN (amount_due - %s) ELSE amount_due END, amount_paid = amount_paid + %s WHERE id = %s""", (now, amount, amount, amount, demand_note_id))
                    # mysql.get_db().commit()
                    
                    #update 
                    cur.execute("""UPDATE loan_prepayment_funds set funds_to_use = funds_to_use - %s, wallet_balance = wallet_balance - %s, last_transaction_date = %s WHERE customer_id = %s""", (amount, amount, payment_date, customer_id))
                    mysql.get_db().commit()

                    #Update demand notes table.
                    cur.execute("""UPDATE loan_demand_notes set amount_due = amount_due - %s, amount_paid = amount_paid + %s WHERE id = %s""", (amount, amount, main_demandnote_id))
                    mysql.get_db().commit()
                    # cur.execute("""UPDATE loan_demand_notes set amount_due = CASE WHEN (amount_due - %s) >= 0 THEN (amount_due - %s) ELSE amount_due END, amount_paid = amount_paid + %s WHERE id = %s""", (amount, amount, amount, main_demandnote_id))
                    # mysql.get_db().commit()

                    #Update loan item.
                    cur.execute("""UPDATE loans set interest_amount_paid = interest_amount_paid + %s, interest_amount_due = interest_amount_due - %s WHERE id = %s""", (amount, amount, loan_id))
                    mysql.get_db().commit()
                
                else:
                    return record_tax_response                
                
                return demand_message
            else:
                return demand_message


        except Exception as error:
            message = {'status':501,
                       "error":"il_r031",
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()

    def pay_charge_demand_note(self, details):
        #Get the request data        
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       "error":"il_r032",
                       "status": 402}
            ErrorLogger().logError(message)
            return message
        
        global_id = details["global_id"]  
        customer_id = details["customer_id"]  
        demand_note_id = details["demand_note_id"]
        amount = float(details["amount"])    
        amount = round(amount, 12) 
        payment_date = Localtime().gettime()

        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "error":"il_r033",
                       "status": 500}
            ErrorLogger().logError(message)
            return message

        #Try except block to handle execute task
        try:
            #Get principal demand note details
            cur.execute("""SELECT loan_id, charge_id, demandnote_id FROM loan_demand_note_details WHERE id = %s """, [demand_note_id])
            demandnote_details = cur.fetchone() 
            if demandnote_details:
                loan_id = demandnote_details["loan_id"]
                main_demandnote_id = demandnote_details["demandnote_id"]
                charge_id = demandnote_details["charge_id"]
            else:
                message = {"status":201,
                           "error":"il_r034",
                           "description":"Task was not successful. Demand note was not found!!"}
                ErrorLogger().logError(message) 
                return message
                            
            #Get charge name
            cur.execute("""SELECT name FROM loan_charge_types WHERE id = %s """, [charge_id])
            charge_details = cur.fetchone() 
            if charge_details:
                fee_name = charge_details["name"]
            else:
                fee_name = ''
                        
            #Get Customer Receivable Account - Check if customer receivable account exists for this specific loan product             
                
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =3 AND owner_id = %s AND entity_id = %s """, [customer_id, loan_id])
            get_receivable_account = cur.fetchone() 
            if get_receivable_account:
                receivable_account = get_receivable_account["number"]

            #Get customer wallet account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =12 AND owner_id = %s """, [customer_id])
            get_wallet_account = cur.fetchone() 
            if get_wallet_account:
                wallet_account = get_wallet_account["number"]
            else:
                message = {"description":"Task was not successful. Customer wallet account was not found!", 
                           "error":"il_r035",
                           "status": 402}
                ErrorLogger().logError(message)
                return message

            #Get charge earned income account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND sub_category_id=2 AND type =14 AND owner_id = %s """, [charge_id])
            get_charge_earned_account = cur.fetchone() 
            if get_charge_earned_account:
                charge_earned_account = get_charge_earned_account["number"]
            else:
                message = {"description":"Task was not successful. Charge income earned account was not found!", 
                           "error":"il_r036",
                           "status": 402}
                ErrorLogger().logError(message)
                return message

            #Get interest earned income account
            cur.execute("""SELECT number FROM accounts WHERE status =1 AND sub_category_id=1 AND type =14 AND owner_id = %s """, [charge_id])
            get_charge_realized_account = cur.fetchone() 
            
            if get_charge_realized_account:
                charge_realized_account = get_charge_realized_account["number"]
            else:
                message = {"description":"Task was not successful. Charge income realized account was not found!", 
                           "error":"il_r037",
                           "status": 402}
                ErrorLogger().logError(message)
                return message

            details = {
                "loan_id":loan_id,
                "wallet_account":wallet_account,
                "receivable_account":receivable_account,
                "charge_earned_account":charge_earned_account,
                "charge_realized_account":charge_realized_account,
                "loan_id":loan_id,
                "global_id":global_id,
                "amount":amount,
                "payment_date":payment_date,
                "charge_name":fee_name            
                }
            demand_message = PayDemandNotes.charge_demand_note_payment(self, details)
            if int(demand_message["status"]) == 200:

                #Call API to record tax expense
                details = {"amount":amount,
                           "global_id":global_id,
                           "entry_id":loan_id
                        }
                record_tax_response = TaxExpenseIncurred().record_tax(details)

                if int(record_tax_response["status"]) == 200:
                    #Update principal demand note details.
                    thisdate = Localtime().gettime()   
                    now = datetime.strptime(thisdate, '%Y-%m-%d %H:%M:%S') 
                    now = now.strftime('%Y-%m-%d')
                    
                    cur.execute("""UPDATE loan_demand_note_details set last_payment_date = %s, amount_due = amount_due - %s, amount_paid = amount_paid + %s WHERE id = %s""", (now, amount, amount, demand_note_id))
                    mysql.get_db().commit()
                    
                    #update 
                    cur.execute("""UPDATE loan_prepayment_funds set funds_to_use = funds_to_use - %s, wallet_balance = wallet_balance - %s, last_transaction_date = %s WHERE customer_id = %s""", (amount, amount, payment_date, customer_id))
                    mysql.get_db().commit()

                    #Update demand notes table.
                    cur.execute("""UPDATE loan_demand_notes set amount_due = amount_due - %s, amount_paid = amount_paid + %s WHERE id = %s""", (amount, amount, main_demandnote_id))
                    mysql.get_db().commit()

                    #Update loan item.
                    cur.execute("""UPDATE loans set charge_amount_paid = charge_amount_paid + %s, charge_amount_due = charge_amount_due - %s WHERE id = %s""", (amount, amount, loan_id))
                    mysql.get_db().commit()
                
                else:
                    return record_tax_response

                return demand_message
            else:
                return demand_message


        except Exception as error:
            message = {'status':501,
                       "error":"il_r038",
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        finally:
            cur.close()
