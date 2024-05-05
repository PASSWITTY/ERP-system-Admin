from flask import json, jsonify
from main import mysql
from dateutil.relativedelta import relativedelta    
from datetime import datetime, timedelta
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.alphanumeric.generate import UniqueNumber
from resources.transactions.transaction import Transaction
from accounts_module.accounts_model import Account


class CreateDefaultedFineDemandNote():    
    
    def defaultedloanfine_demand_note_creation(self, details):
        if details == None:
            message = {"status":402,
                       'error':'LDF_01',
                       "description":"All details are required!"}
            ErrorLogger().logError(message) 
            return message
                
        loan_id = details["loan_id"]
        global_id = details["global_id"]
        defaultedfine_lists = details["defaultedfine_lists"]
        amount = details["amount"]
        amount = round(amount, 12) 
        customer_id = details["customer_id"]
        date_created = Localtime().gettime()
    
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database", 
                       'error':'LDF_02',
                       "status":500}
            return message

        try:
            total_fees = 0
            #Create customer receivable account for this loan
            
            for charge_list in defaultedfine_lists:           
                charge_rate = charge_list["fee_rate"] 
                charge_amount = charge_list["fee_amount"]
                fee_name = charge_list["fee_name"]                
                charge_id = charge_list["fee_id"]
              
                if charge_rate != "":
                    charge_rate = float(charge_rate)
                    charge_rate = round(charge_rate, 12) 
                else:
                    charge_rate = 0
                
                if charge_amount != "":
                    charge_amount = float(charge_amount)
                    charge_amount = round(charge_amount, 12) 
                else:
                    charge_amount = 0

                if charge_rate > 0:
                    fee_amount = (charge_rate * amount ) / 100
                    fee_amount = round(fee_amount, 12) 
                else:
                    fee_amount = charge_amount
               
                #Get customer receivable account
                cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =3 AND entity_id = %s AND owner_id = %s """, (loan_id, customer_id))
                get_loan_receivable_account = cur.fetchone() 
                if get_loan_receivable_account:
                    customer_receivable_account_number = get_loan_receivable_account["number"]
                    
                else:
                    #Get customer details
                    cur.execute("""SELECT first_name, last_name, created_by FROM customer_details WHERE id = %s """, [customer_id])
                    get_customer = cur.fetchone()
                    if get_customer:
                        first_name = get_customer["first_name"]
                        last_name = get_customer["last_name"]
                        user_id = get_customer["created_by"]

                    else:                
                        message = {"description":"Customer details were not found! Transaction canceled!", 
                                    "status":402}
                        ErrorLogger().logError(message)                
                        return message
                                    
                    accountName = first_name + " " + " " + last_name + " " + "Receivable Account"
                    type_Id = 3  # Receivable account type 3
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
                            "user_id": user_id,
                            "status":1}                

                    api_response = Account().create_new_account(account)
                    if int(api_response["status"] == 200):
                        customer_receivable_account_number = api_response["response"]["account_number"]
                
                cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =14 AND sub_category_id =2 AND owner_id = %s """, [charge_id])
                get_charge_account = cur.fetchone() 
                
                if get_charge_account:
                    charge_account = get_charge_account["number"]

                    #Start of transaction posting - Debit Customer wallet account with charge amount

                    transaction_name = str(fee_name) + ' for Defaulted loan'
                    #if customer langauge is English, get english description 
                    description = str(fee_name) + ' for Defaulted loan of Kes ' + str(fee_amount) + ". Loan reference number is " + loan_id
                    #if customer langauge is Kiswahili, get swahili description 
                    layer4_id = UniqueNumber().transactionsdebitcreditId()                     

                    transaction_data = {"global_id":global_id,
                                        "entry_id":loan_id, 
                                        "sub_entry_id":'',
                                        "type":41,
                                        "account_number":customer_receivable_account_number, 
                                        "amount":fee_amount, 
                                        "transaction_name":transaction_name,
                                        "description":description, 
                                        "settlement_date":date_created,
                                        "layer4_id":layer4_id                                        
                                        }
                
                    #Debit Customer Wallet account with charge amount
                    debit_trans = Transaction().debit_on_debit_account(transaction_data)
                    #End of transaction posting
                
                    #Start of transaction posting - Credit Realized Income Charge account with charge fee amount

                    transaction_name = str(fee_name) + ' for Defaulted loan'
                    #if customer langauge is English, get english description 
                    description = str(fee_name) + ' for Defaulted loan of Kes ' + str(fee_amount) + ". Loan reference number is " + loan_id
                    #if customer langauge is Kiswahili, get swahili description 

                    transaction_data = {"global_id":global_id, 
                                        "entry_id":loan_id, 
                                        "sub_entry_id":'',
                                        "type":42,
                                        "account_number":charge_account, 
                                        "amount":fee_amount, 
                                        "transaction_name":transaction_name,
                                        "description":description, 
                                        "settlement_date":date_created,
                                        "layer4_id":layer4_id
                                        }
                    
                    #Credit earned income account with charge amount
                    credit_trans = Transaction().credit_on_credit_account(transaction_data)
                    #End of transaction posting

                    if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):   
                        pass                   

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
            
                total_fees = total_fees + fee_amount
                
            if total_fees > 0:
                amount_paid = 0
                status = 1
                payment_in_progress = 0
                demandnote_id = UniqueNumber().defaultedloanfinesentryId()
                cur.execute("""INSERT INTO loan_defaulted_fines_demand_note_details (id, loan_id, customer_id, charge_id, payment_in_progress, global_id, amount, amount_paid, amount_due, date_created, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",                             
                                                                         (demandnote_id, loan_id, customer_id, charge_id, payment_in_progress, global_id, total_fees, amount_paid, total_fees, date_created, status))
                mysql.get_db().commit()

                #Update loan item.
                cur.execute("""UPDATE loans set defaulted_loan_fines_generated = 1, defaulted_loan_fines_due = defaulted_loan_fines_due + %s, defaulted_loan_fines_paid = 0, defaulted_loan_fines_amount = defaulted_loan_fines_amount + %s WHERE id = %s""", (total_fees, total_fees, loan_id))
                mysql.get_db().commit()

                message = {
                        "description":"Defaulted Loan fines were posted successfully",
                        "status":200,
                        "total_fees":total_fees}
                return message

            else:
                message = {
                        "description":"Transaction canceled!. Defaulted loan fines were not posted successfully!",
                        'error':'LDF_03',
                        "status":201}
                ErrorLogger().logError(message) 
                return message

            
        except Exception as error:
            message = {'status':501,
                       'error':'LDF_04',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 
        finally:
            cur.close()
            
            
