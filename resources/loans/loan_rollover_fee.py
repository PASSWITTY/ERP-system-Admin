from flask import json, jsonify
from main import mysql
from dateutil.relativedelta import relativedelta    
from datetime import datetime, timedelta
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.alphanumeric.generate import UniqueNumber
from resources.transactions.transaction import Transaction

class RolloverFee():  
    def rollover_fee_creation(self, rollover_details):
        if rollover_details == None:
            message = {"description":"Transaction is missing some details!", 
                       "status": 402}
            return message
        
        receivable_account = rollover_details["receivable_account"]
        rollover_fee_earned_account = rollover_details["rollover_fee_earned_account"]     
        rollover_id = rollover_details["rollover_id"] 
        loan_id = rollover_details["loan_id"]
        customer_id = rollover_details["customer_id"]
        global_id = rollover_details["global_id"]
        subdemandnote_id = rollover_details["subdemandnote_id"]   
        amount = rollover_details["amount"]
        type = rollover_details["type"]
        amount = round(amount, 12) 
        datecreated = Localtime().gettime()
        date_due = Localtime().gettime() #Rollover is due immediately        
        amount_paid = 0

        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       "status": 500}
            return message

        #Try except block to handle execute task
        try:
            
            #Start of transaction posting - Debit Customer Receivable Account with roll over fee amount

            transaction_name = type + ' Rollover Fee'
            #if customer langauge is English, get english description 
            description = 'Loan rollover fee of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 
            layer4_id = UniqueNumber().transactionsdebitcreditId() 

            transaction_data = {"global_id":global_id, 
                                "entry_id":subdemandnote_id, 
                                "sub_entry_id":loan_id, 
                                "type":39,
                                "account_number":receivable_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":datecreated,
                                "layer4_id":layer4_id
                                }
            
            #Debit Customer Receivable Account with Principal roll over fee amount
            debit_trans = Transaction().debit_on_debit_account(transaction_data)
            #End of transaction posting

            #Start of transaction posting - Credit Loan Asset Account with roll over fee

            transaction_name = type + ' Rollover Fee'
            #if customer langauge is English, get english description 
            description = 'Loan rollover fee of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 

            transaction_data = {"global_id":global_id, 
                                "entry_id":subdemandnote_id, 
                                "sub_entry_id":loan_id, 
                                "type":40,
                                "account_number":rollover_fee_earned_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":datecreated,
                                "layer4_id":layer4_id
                                }
            
            #Credit Roll Over Account with Principal roll over fee amount
            credit_trans = Transaction().credit_on_credit_account(transaction_data)
            #End of transaction posting

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):

                status = 1
                id = UniqueNumber().rolloverfeeentryId()
                
                cur.execute("""INSERT INTO loan_rollover_fee_demand_note_details (id, subdemandnote_id, loan_id, rollover_id, customer_id, global_id, type, amount, amount_paid, amount_due, expected_payment_date, date_created, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                                                 (id, subdemandnote_id, loan_id, rollover_id, customer_id, global_id, type, amount, amount_paid, amount, date_due, datecreated, status))
                mysql.get_db().commit()
                
                #Update loan item.
                
                cur.execute("""SELECT loan_product_id, duration_cycle FROM loans WHERE id = %s""", (loan_id))
                prod = cur.fetchone() 
                if prod:
                    product_id = prod["loan_product_id"]
                    duration_cycle = prod["duration_cycle"]
                    
                    cur.execute("""SELECT next_rollover_after FROM loan_product_periods WHERE product_id = %s AND duration_id = %s""", (product_id, duration_cycle))
                    rollover_date = cur.fetchone() 
                    if rollover_date:
                        next_rollover_after = int(rollover_date["next_rollover_after"])
                    
                else: 
                    product_id = ''
                    next_rollover_after = 0
                
                thisdate = Localtime().gettime()   
                now = datetime.strptime(thisdate, '%Y-%m-%d %H:%M:%S')
                
            
                rollover_expected_date = now + timedelta(days=next_rollover_after)
                next_rollover_date = rollover_expected_date.strftime('%Y-%m-%d')
            
                cur.execute("""UPDATE loans set rollover_fee_amount = rollover_fee_amount + %s, rollover_fee_due = rollover_fee_due + %s, rollover_expected_date = %s WHERE id = %s""", (amount, amount, next_rollover_date, loan_id))
                mysql.get_db().commit()
                
                cur.execute("""UPDATE loan_demand_note_details set rollovers_generated = rollovers_generated + 1 WHERE id = %s""", (subdemandnote_id))
                mysql.get_db().commit()

                message = {
                        "receivable_account_status":debit_trans,
                        "rollover_fee_account_status":credit_trans,
                        "description":"Loan principal rollover fee was created successfully",
                        "status":200}
                return message
            
            else:
                #Reverse the failed transaction
                if int(debit_trans["status"]) == 200 and int(credit_trans["status"]) != 200:
                    #Rollback this debit transaction
                    data = debit_trans["data"]
                    trans_id = debit_trans["data"]["trans_id"]
                    amount = float(debit_trans["data"]["amount"])
                    if amount >0 and trans_id is not None:
                        #Delete this specific debit transaction
                        rollback_debit_trans = Transaction().debit_on_debit_account_rollback(data)
                    else:
                        pass
                
                if int(credit_trans["status"]) == 200 and int(debit_trans["status"]) != 200:
                    #Rollback this credit transaction

                    data = credit_trans["data"]
                    trans_id = credit_trans["data"]["trans_id"]
                    amount = float(credit_trans["data"]["amount"])
                    if amount >0 and trans_id is not None:
                        #Delete this specific credit transaction
                        rollback_credit_trans = Transaction().credit_on_credit_account_rollback(data)
                    else:
                        pass
                            

                message = {
                    "status":201,
                    "receivable_account_status":debit_trans,
                    "rollover_fee_account_status":credit_trans}
                return message


        except Exception as error:
            message = {'status':501,
                       'description':'Transaction had an error. Error description ' + format(error)}
            return message 
        finally:
            cur.close()  
   
