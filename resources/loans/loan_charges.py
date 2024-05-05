from main import mysql 
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.alphanumeric.generate import UniqueNumber
from resources.transactions.transaction import Transaction
from accounts_module.accounts_model import Account
from datetime import datetime, timedelta


class LoanCharges():
    
    #API to create loan charges
    def loan_charges_creation(self, charges_details):
        if charges_details == None:
            message = {"status":402,
                       'error':'L_01',
                       "description":"All details are required!"}
            ErrorLogger().logError(message) 
            return message
                
        loan_id = charges_details["id"]
        global_id = charges_details["global_id"]
        charge_lists = charges_details["charge_lists"]
        amount = charges_details["amount"]
        amount = round(amount, 12) 
        date_created = Localtime().gettime()
        
        user_id = charges_details["user_id"]
        first_name = charges_details["first_name"]
        last_name = charges_details["last_name"]
        customer_id = charges_details["customer_id"]
        wallet_account = charges_details["wallet_account"]
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database", 
                       'error':'L_02',
                       "status":500}
            return message

        try:
            total_fees = 0
            #Create customer receivable account for this loan
            
            for charge_list in charge_lists:           
                charge_rate = charge_list["fee_rate"] 
                charge_amount = charge_list["fee_amount"]
                fee_name = charge_list["fee_name"]                
                charge_id = charge_list["fee_id"]
                payment_type = int(charge_list["paymenttype"])
              
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
                
                if payment_type ==2:
                    charge_paid = 0
                    cur.execute("""INSERT INTO loan_charge_pending (loan_id, global_id, charge_id, charge_amount_due, charge_amount_paid) VALUES (%s, %s, %s, %s, %s)""", (loan_id, global_id, charge_id, fee_amount, charge_paid))
                    mysql.get_db().commit()
                
                if payment_type ==1: #pre-paid charge e.g insurance fee
                    
                    #Get customer receivable account
                    cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =3 AND entity_id = %s AND owner_id = %s """, (loan_id, customer_id))
                    get_loan_receivable_account = cur.fetchone() 
                    if get_loan_receivable_account:
                        customer_receivable_account_number = get_loan_receivable_account["number"]
                        
                    else:
                                        
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
                    
                
                    cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =14 AND sub_category_id =1 AND owner_id = %s """, [charge_id])
                    get_charge_account = cur.fetchone() 
                    
                    if get_charge_account:
                        charge_realized_income_account = get_charge_account["number"]

                        #Start of transaction posting - Debit Customer receivable account with charge amount

                        transaction_name = str(fee_name) + ' Loan Charge'
                        #if customer langauge is English, get english description 
                        description = str(fee_name) + ' Loan charge of Kes ' + str(fee_amount) + ". Loan reference number is " + loan_id
                        #if customer langauge is Kiswahili, get swahili description 
                        layer4_id = UniqueNumber().transactionsdebitcreditId()                     

                        transaction_data = {"global_id":global_id,
                                            "entry_id":loan_id, 
                                            "sub_entry_id":'',
                                            "type":15,
                                            "account_number":customer_receivable_account_number, 
                                            "amount":fee_amount, 
                                            "transaction_name":transaction_name,
                                            "description":description, 
                                            "settlement_date":date_created,
                                            "layer4_id":layer4_id                                        
                                            }
                    
                        #Debit Customer receivable account with charge amount
                        debit_trans = Transaction().debit_on_debit_account(transaction_data)
                        #End of transaction posting
                    
                        #Start of transaction posting - Credit Realized Income Charge account with charge fee amount

                        transaction_name = str(fee_name) + ' Loan Charge'
                        #if customer langauge is English, get english description 
                        description = str(fee_name) + ' Loan charge fee of Kes ' + str(fee_amount) + ". Loan reference number is " + loan_id
                        #if customer langauge is Kiswahili, get swahili description 

                        transaction_data = {"global_id":global_id, 
                                            "entry_id":loan_id, 
                                            "sub_entry_id":'',
                                            "type":16,
                                            "account_number":charge_realized_income_account, 
                                            "amount":fee_amount, 
                                            "transaction_name":transaction_name,
                                            "description":description, 
                                            "settlement_date":date_created,
                                            "layer4_id":layer4_id
                                            }
                        
                        #Credit earned income account with charge amount
                        credit_trans = Transaction().credit_on_credit_account(transaction_data)
                        #End of transaction posting
                        
                        #Start transaction to pay pre-paid charges. 
                        #Debit customer wallet with charge amount to be paid
                        if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):   
                            transaction_name = str(fee_name) + ' Loan Charge Payment'
                            #if customer langauge is English, get english description 
                            description = str(fee_name) +' payment of Kes ' + str(fee_amount) + ". Loan reference number is " + loan_id
                            #if customer langauge is Kiswahili, get swahili description 

                            layer4_id = UniqueNumber().transactionsdebitcreditId()
                            transaction_data = {"global_id":global_id, 
                                                "entry_id":loan_id, 
                                                "sub_entry_id":'',
                                                "type":59,
                                                "account_number":wallet_account, 
                                                "amount":fee_amount, 
                                                "transaction_name":transaction_name,
                                                "description":description, 
                                                "settlement_date":date_created,
                                                "layer4_id":layer4_id
                                                }
                            
                            #Credit customer receivable account with amount paid
                            debit_income_trans = Transaction().debit_on_credit_account(transaction_data)
                            #End of transaction posting

                            #Start of transaction posting - Credit Customer Receivable Account with mpesa charge amount paid

                            transaction_name = str(fee_name) + ' Loan Charge Payment'
                            #if customer langauge is English, get english description 
                            description = str(fee_name) +' payment of Kes ' + str(fee_amount) + ". Loan reference number is " + loan_id
                            #if customer langauge is Kiswahili, get swahili description 

                            transaction_data = {"global_id":global_id, 
                                                "entry_id":loan_id, 
                                                "sub_entry_id":'',
                                                "type":60,
                                                "account_number":customer_receivable_account_number, 
                                                "amount":fee_amount, 
                                                "transaction_name":transaction_name,
                                                "description":description, 
                                                "settlement_date":date_created,
                                                "layer4_id":layer4_id
                                                }
                            
                            credit_income_trans = Transaction().credit_on_debit_account(transaction_data)
                            #End of transaction posting
                            
                            if ((int(debit_income_trans["status"]) == 200) and (int(credit_income_trans["status"]) == 200)):
                        
                                message = {
                                        "customer_receivable_account_status":debit_trans,
                                        "charge_income_realized_account_status":credit_trans,
                                        "wallet_account_status":debit_income_trans,
                                        "customer_receivable_account_status":credit_income_trans,
                                        "description":"Prepaid charges were deducted successfully",
                                        "status":200}
                                return message
                            
                            else:
                                #Reverse the failed transaction

                                if int(debit_trans["status"]) == 200:
                                    #Rollback this debit transaction
                                    data = debit_trans["data"]
                                    trans_id = debit_trans["data"]["trans_id"]
                                    amount = float(debit_trans["data"]["amount"])
                                    if amount >0 and trans_id is not None:
                                        #Delete this specific debit transaction
                                        rollback_debit_trans = Transaction().debit_on_credit_account_rollback(data)
                                    else:
                                        pass
                                
                                if int(credit_trans["status"]) == 200:
                                    #Rollback this credit transaction
                                    data = credit_trans["data"]
                                    trans_id = credit_trans["data"]["trans_id"]
                                    amount = float(credit_trans["data"]["amount"])
                                    if amount >0 and trans_id is not None:
                                        #Delete this specific credit transaction
                                        rollback_credit_trans = Transaction().credit_on_debit_account_rollback(data)
                                    else:
                                        pass

                                if int(debit_income_trans["status"]) == 200 and int(credit_income_trans["status"]) != 200:
                                    #Rollback this debit transaction
                                    data = debit_income_trans["data"]
                                    trans_id = debit_income_trans["data"]["trans_id"]
                                    amount = float(debit_income_trans["data"]["amount"])
                                    if amount >0 and trans_id is not None:
                                        #Delete this specific debit transaction
                                        rollback_debit_income_trans = Transaction().debit_on_debit_account_rollback(data)
                                    else:
                                        pass
                                
                                if int(credit_income_trans["status"]) == 200 and int(debit_income_trans["status"]) != 200:
                                    #Rollback this credit transaction

                                    data = credit_income_trans["data"]
                                    trans_id = credit_income_trans["data"]["trans_id"]
                                    amount = float(credit_income_trans["data"]["amount"])
                                    if amount >0 and trans_id is not None:
                                        #Delete this specific credit transaction
                                        rollback_credit_income_trans = Transaction().credit_on_debit_account_rollback(data)
                                    else:
                                        pass
                                            
                                message = {
                                        "customer_receivable_account_status":debit_trans,
                                        "charge_income_realized_account_status":credit_trans,
                                        "wallet_account_status":debit_income_trans,
                                        "customer_receivable_account_status":credit_income_trans,
                                        "description":"Prepaid charges were deducted successfully",
                                        "error":"pd_m05",
                                        "status":201
                                            }
                                ErrorLogger().logError(message)
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
                
                    total_fees = total_fees + fee_amount
                    
            if total_fees > 0:
                cur.execute("""INSERT INTO loan_charges_log (loan_id, global_id, amount, date_created) VALUES (%s, %s, %s, %s)""", (loan_id, global_id, total_fees, date_created))
                mysql.get_db().commit()

                # #Update loan item.
                cur.execute("""UPDATE loans set charge_amount_due = charge_amount_due - %s, outstanding_charge_demandnote_amount = outstanding_charge_demandnote_amount - %s, charge_amount_paid = charge_amount_paid + %s WHERE id = %s""", (total_fees, total_fees, total_fees, loan_id))
                mysql.get_db().commit()

                message = {
                        "description":"Loan charges were posted successfully",
                        "status":200,
                        "total_fees":total_fees}
                return message

            else:
               
                message = {
                        "description":"There was no pre-paid Loan charges",
                        "status":200,
                        "total_fees":total_fees}
                return message

            
        except Exception as error:
            message = {'status':501,
                       'error':'L_04',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 
        finally:
            cur.close()
            
    #API to calculate total charges per loan
    def total_loan_charges(self, chargesfee_details):
        if chargesfee_details == None:
            message = {"description":"Transaction is missing some details!", 
                       'error':'L_05',
                       "status": 402}
            ErrorLogger().logError(message) 
            return message
        
        charge_lists = chargesfee_details["charge_lists"]
        amount = float(chargesfee_details["amount"])
        amount = round(amount, 12) 

        total_fees = 0 
        prepaid_fee = 0
        postpaid_fee = 0

        for charge_list in charge_lists:                
            charge_rate = charge_list["fee_rate"]
            charge_amount = charge_list["fee_amount"]
            charge_paymenttype = int(charge_list["paymenttype"])

            if charge_paymenttype ==1: #Prepaid fee            
                if charge_rate:
                    charge_rate = float(charge_rate)
                else:
                    charge_rate = 0
                
                if charge_amount:
                    charge_amount = float(charge_amount)
                else:
                    charge_amount = 0

                if charge_rate > 0:
                    fee_amount = (charge_rate * amount ) / 100
                else:
                    fee_amount = charge_amount
                
                prepaid_fee = prepaid_fee + fee_amount
            
            if charge_paymenttype ==2: #postpaid fee            
                if charge_rate:
                    charge_rate = float(charge_rate)
                else:
                    charge_rate = 0
                
                if charge_amount:
                    charge_amount = float(charge_amount)
                else:
                    charge_amount = 0

                if charge_rate > 0:
                    fee_amount = (charge_rate * amount ) / 100
                else:
                    fee_amount = charge_amount
                
                postpaid_fee = postpaid_fee + fee_amount

        total_fees = prepaid_fee + postpaid_fee
            
        
        charges_fees = {"total_fees":float(total_fees), "prepaid_fee":float(prepaid_fee), "postpaid_fee":float(postpaid_fee)}

        return charges_fees
    
    def reducing_balance(self, details):
        if details == None:
            message = {'status':402,
                       'error':'us_s30',
                       'description':'Request data is missing some details!'}

            ErrorLogger().logError(message)
            return message
        
        principal = float(details["principal"])
        monthly_interest_rate = details["monthly_interest_rate"]
        loan_period = int(details["loan_period"])
        
        try:    
            if loan_period > 0:
                
                p = loan_period
                a = 0
                total_interest = 0
                
                month_principal = principal
                while (a:=a+1) <= p:
                    interest = (month_principal * monthly_interest_rate / 100)
                    opening_balance = month_principal + interest
                    principal_to_pay = (principal / loan_period)
                    monthly_repayment = principal_to_pay + interest
                    closing_balance = opening_balance - monthly_repayment
                    month_principal = closing_balance                    
                    total_interest = total_interest + interest                   
                
                response = {"total_interest":total_interest}
                return response
                
        except Exception as error:
            message = {'status':501,
                       'error':'us_s31',
                       'description':'System error! Error description '+ format(error)}
            ErrorLogger().logError(message)
            return message

    def reducing_balance_next_installment(self, details):
        if details == None:
            message = {'status':402,
                       'error':'us_s30',
                       'description':'Request data is missing some details!'}

            ErrorLogger().logError(message)
            return message
        
        principal_disbursed = float(details["principal_disbursed"])
        principal_due = float(details["principal_due"])
        monthly_interest_rate = float(details["monthly_interest_rate"])
        loan_period = int(details["loan_period"])
        outstanding_interest_installments = int(details["outstanding_interest_installments"])
        
        try:    
            if outstanding_interest_installments > 0:
                
                interest_to_pay = (principal_due * monthly_interest_rate / 100)            
                principal_to_pay = (principal_due / outstanding_interest_installments)
                installment_amount = interest_to_pay + principal_to_pay
                
                response = {"next_installment_amount":installment_amount, "interest_to_pay":interest_to_pay}
                return response
                
        except Exception as error:
            message = {'status':501,
                       'error':'us_s31',
                       'description':'System error! Error description '+ format(error)}
            ErrorLogger().logError(message)
            return message
        
    def reducing_balance_sms(self, details):
        if details == None:
            message = {'status':402,
                       'error':'us_s30',
                       'description':'Request data is missing some details!'}

            ErrorLogger().logError(message)
            return message
        
        principal_due = float(details["principal_due"])
        loan_period = int(details["outstanding_installments"])
        monthly_interest_rate = float(details["monthly_interest_rate"])
  
        frequency_id = int(details["frequency_id"])
        number_of_installments = int(details["number_of_installments"])
        # start_date = datetime.strptime(details["start_date"], "%Y-%m-%d %H:%M:%S") 
        start_date = details["start_date"].strftime('%Y-%m-%d %H:%M:%S')
        
        if principal_due > 0:
            
            if frequency_id ==1:
                days = 1
                days_added = (days / number_of_installments)
            
            elif frequency_id ==2:
                days = 3
                days_added = (days / number_of_installments)
            
            elif frequency_id ==3:
                days = 7
                days_added = (days / number_of_installments)
            
            elif frequency_id ==4:
                days = 14
                days_added = (days / number_of_installments)
            
            elif frequency_id ==5:
                days = 30
                days_added = (days / number_of_installments)
            
            elif frequency_id ==7: #three months
                days = 90
                days_added = (days / number_of_installments)
            
            elif frequency_id ==8: #six months
                days = 180
                days_added = (days / number_of_installments)
            else:
                days = 0
                days_added = 0
        
        try:    
            if loan_period > 0:
                
                p = loan_period
                a = 0
                total_interest = 0
                
                month_principal = principal_due
                next_installment_date = start_date
                messagebody = "hello"
                while (a:=a+1) <= p:
                    interest = (month_principal * monthly_interest_rate / 100)
                    opening_balance = month_principal + interest
                    principal_to_pay = (principal_due / loan_period)
                    monthly_repayment = principal_to_pay + interest
                    closing_balance = opening_balance - monthly_repayment
                    month_principal = closing_balance                    
                    total_interest = total_interest + interest 
                    
                    
                    next_installment_date = next_installment_date + timedelta(days=days_added)
                    next_installment_date = next_installment_date.strftime('%Y-%m-%d')   
                    
                    message_body = f" {str(next_installment_date)} repayment is Ksh {monthly_repayment:,.2f}" 
                    messagebody += f"{message_body}"
                    
                             
                
                response = {"message_body":str(messagebody)}
                return response
                
        except Exception as error:
            message = {'status':501,
                       'error':'us_s31',
                       'description':'System error! Error description '+ format(error)}
            ErrorLogger().logError(message)
            return message
    #This function is not being used. Should be deleted
    # def incur_payment_charges_expense(self, details):
    
    #     if details == None:
    #         message = {"description":"Transaction is missing some details!", 
    #                    'error':'L_05',
    #                    "status": 402}
    #         ErrorLogger().logError(message) 
    #         return message

    #     customer_id = details["customer_id"]
    #     global_id = details["global_id"]
    #     amount = details["amount"]
        
    #     entry_id = details["entry_id"]      
    #     first_name = details["first_name"]
    #     last_name = details["last_name"]
    #     user_id = details["user_id"]
        
    #     amount = round(amount, 12)
    #     date_created = Localtime().gettime()

    #     # Open A connection to the database
    #     try:
    #         cur = mysql.get_db().cursor()
    #     except:
    #         message = {'status':500,
    #                    'error':'L_07',
    #                    'description':"Couldn't connect to the Database!"}
    #         ErrorLogger().logError(message) 
    #         return message
        
    #     try:  
    #          #check b2c charges amount
    #         cur.execute("""SELECT charges_amount FROM mpesa_transactions_charges WHERE status =1 AND start_amount <=%s AND end_amount >=%s """, [amount, amount])
    #         get_b2c_charges= cur.fetchone()                 
    #         if get_b2c_charges:
    #             b2c_charge_amount = float(get_b2c_charges["charges_amount"])  
 
    #         else:                
    #             message = {'status':404,
    #                        'error':'L_08',
    #                        'description':"B2C charges were not defined!"}
    #             ErrorLogger().logError(message) 
    #             return message
            
    #         #Get customer receivable account
    #         cur.execute("""SELECT number FROM accounts WHERE status =1 AND type =3 AND entity_id = %s AND owner_id = %s """, (entry_id, customer_id))
    #         get_loan_receivable_account = cur.fetchone() 
    #         if get_loan_receivable_account:
    #             customer_receivable_account_number = get_loan_receivable_account["number"]
                
    #         else:
                                
    #             accountName = first_name + " " + " " + last_name + " " + "Receivable Account"
    #             type_Id = 3  # Receivable account type 3
    #             categoryId = 18
    #             sub_category = 0
    #             mainaccount = 0
    #             openingBalance = 0
    #             notes = ''
    #             owner_id = customer_id
    #             entity_id = entry_id
    #             description = ''
    #             referenceNumber = ''            
    
    #             account = {
    #                     "name": accountName,
    #                     "accountType": type_Id,
    #                     "accountCategory": categoryId,
    #                     "accountSubCategory": sub_category,
    #                     "main_account": mainaccount,
    #                     "opening_balance": openingBalance,
    #                     "owner_id": owner_id,
    #                     "entity_id": entity_id,
    #                     "notes": notes,
    #                     "description": description,
    #                     "reference_number": referenceNumber,
    #                     "user_id": user_id,
    #                     "status":1}                

    #             api_response = Account().create_new_account(account)
    #             if int(api_response["status"] == 200):
    #                 customer_receivable_account_number = api_response["response"]["account_number"]
            
    #         #get b2c charges realized income account
    #         cur.execute("""SELECT account_number FROM default_accounts WHERE default_status =1 AND default_type_number=6""")
    #         b2c_realizedincome_acc = cur.fetchone()                        
    #         if b2c_realizedincome_acc:
    #             b2c_realizedincome_account = b2c_realizedincome_acc["account_number"]
    #         else:
    #             message = {'status':404,
    #                        'error':'L_09',
    #                        'description':"Default B2C expense account has not been setup!"}
    #             ErrorLogger().logError(message) 
    #             return message
        

    #         # Start of transaction posting - Debit charges expense Account with charge amount incurred
    #         transaction_name = 'Mpesa charges'
    #         # if customer langauge is English, get english description
    #         description = 'Mpesa charges of Ksh. ' + str(b2c_charge_amount)
    #         # if customer langauge is Kiswahili, get swahili description
    #         layer4_id = UniqueNumber().transactionsdebitcreditId()

    #         transaction_data = {"global_id": global_id,
    #                             "entry_id": entry_id,
    #                             "sub_entry_id":'',
    #                             "type":17,
    #                             "account_number": customer_receivable_account_number,
    #                             "amount": b2c_charge_amount,
    #                             "transaction_name": transaction_name,
    #                             "description": description,
    #                             "settlement_date": date_created,
    #                             "layer4_id": layer4_id
    #                             }

    #         # Debit momo payments charges expense account
    #         debit_trans = Transaction().debit_on_debit_account(transaction_data)
    #         # End of transaction posting

    #         # Start of transaction posting - Credit B2C payable account with charges amount
    #         transaction_name = 'Mpesa charges'
    #         # if customer langauge is English, get english description
    #         description = 'Mpesa charges of Ksh. ' + str(b2c_charge_amount)
    #         # if customer langauge is Kiswahili, get swahili description

    #         transaction_data = {"global_id": global_id,
    #                             "entry_id": entry_id,
    #                             "sub_entry_id":'',
    #                             "type":18,
    #                             "account_number": b2c_realizedincome_account,
    #                             "amount": b2c_charge_amount,
    #                             "transaction_name": transaction_name,
    #                             "description": description,
    #                             "settlement_date": date_created,
    #                             "layer4_id": layer4_id
    #                             }

    #         # Credit B2C partner payable account with amount charged
    #         credit_trans = Transaction().credit_on_credit_account(transaction_data)
    #         # End of transaction posting

    #         if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
    #             message = {
    #                 "status":200,
    #                 "data":b2c_charge_amount,
    #                 "b2c_expense_account_status":debit_trans,
    #                 "b2c_payable_account_status":credit_trans}
    #             return message
            
    #         else:
    #             #Reverse the failed transaction
    #             if int(debit_trans["status"]) == 200 and int(credit_trans["status"]) != 200:
    #                 #Rollback this debit transaction
    #                 data = debit_trans["data"]
    #                 trans_id = debit_trans["data"]["trans_id"]
    #                 amount = float(debit_trans["data"]["amount"])
    #                 if amount >0 and trans_id is not None:
    #                     #Delete this specific debit transaction
    #                     rollback_debit_trans = Transaction().debit_on_debit_account_rollback(data)
    #                 else:
    #                     pass
                
    #             if int(credit_trans["status"]) == 200 and int(debit_trans["status"]) != 200:
    #                 #Rollback this credit transaction

    #                 data = credit_trans["data"]
    #                 trans_id = credit_trans["data"]["trans_id"]
    #                 amount = float(credit_trans["data"]["amount"])
    #                 if amount >0 and trans_id is not None:
    #                     #Delete this specific credit transaction
    #                     rollback_credit_trans = Transaction().credit_on_credit_account_rollback(data)
    #                 else:
    #                     pass
                               
    #             message = {
    #                 "status":201,
    #                 'error':'L_11',
    #                 "b2c_expense_account_status":debit_trans,
    #                 "b2c_payable_account_status":credit_trans}
    #             ErrorLogger().logError(message) 
    #             return message


    #     # Error handling
    #     except Exception as error:
    #         message = {'status':501,
    #                    'error':'L_12',
    #                    'description':'Transaction had an error. Error description ' + format(error)}
    #         ErrorLogger().logError(message) 
    #         return message 
        
    def offset_payment_charges(self, details):
        
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       'error':'L_13',
                       "status": 402}
            ErrorLogger().logError(message) 
            return message

        customer_id = details["customer_id"]
        wallet_account = details["wallet_account"]
        global_id = details["global_id"]        
        b2c_charge_amount = float(details["amount"])    
        b2c_markup_fee = float(details["b2c_markup_fee"])  
        b2c_utility_account = details["b2c_utility_account"]     
        b2c_income_acc = details["b2c_income_acc"]     
        date_created = Localtime().gettime()

        # Open A connection to the database
        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'L_14',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message) 
            return message

        try:  
             # Start of transaction posting - Debit customer wallet Account with charge amount incurred
            transaction_name = 'Mpesa charges'
            # if customer langauge is English, get english description
            description = 'Mpesa charges of Ksh. ' + str(b2c_charge_amount)
            # if customer langauge is Kiswahili, get swahili description
            layer4_id = UniqueNumber().transactionsdebitcreditId()

            transaction_data = {"global_id": global_id,
                                "entry_id": customer_id,
                                "sub_entry_id":'',
                                "type":17,
                                "account_number": wallet_account,
                                "amount": b2c_charge_amount,
                                "transaction_name": transaction_name,
                                "description": description,
                                "settlement_date": date_created,
                                "layer4_id": layer4_id
                                }

            # Debit momo payments charges wallet account
            debit_trans = Transaction().debit_on_credit_account(transaction_data)
            # End of transaction posting

            # Start of transaction posting - Credit B2C Utility account with charges amount
            transaction_name = 'Mpesa charges'
            # if customer langauge is English, get english description
            description = 'Mpesa charges of Ksh. ' + str(b2c_charge_amount)
            # if customer langauge is Kiswahili, get swahili description

            transaction_data = {"global_id": global_id,
                                "entry_id": customer_id,
                                "sub_entry_id":'',
                                "type":18,
                                "account_number": b2c_utility_account,
                                "amount": b2c_charge_amount,
                                "transaction_name": transaction_name,
                                "description": description,
                                "settlement_date": date_created,
                                "layer4_id": layer4_id
                                }

            # Credit B2C utility account with amount charged
            credit_trans = Transaction().credit_on_debit_account(transaction_data)
            # End of transaction posting

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                
                #Start of transaction posting - Debit rollover fee Income Earned Account with rollover fee demand note amount paid

                transaction_name = "Mpesa charges income"
                #if customer langauge is English, get english description 
                description = 'Mpesa charges markup ' + str(b2c_markup_fee)
                #if customer langauge is Kiswahili, get swahili description 

                layer4_id = UniqueNumber().transactionsdebitcreditId()
                transaction_data = {"global_id":global_id, 
                                    "entry_id":customer_id, 
                                    "sub_entry_id":'',
                                    "type":67,
                                    "account_number":b2c_utility_account, 
                                    "amount":b2c_markup_fee, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":date_created,
                                    "layer4_id":layer4_id
                                    }
                
                #Debit b2c utility Account with mpesa markup amount paid
                debit_income_trans = Transaction().debit_on_debit_account(transaction_data)
                #End of transaction posting

                #Start of transaction posting - Credit Customer Receivable Account with rollover fee demand note amount paid

                transaction_name = "Mpesa charges income"
                #if customer langauge is English, get english description 
                description = 'Mpesa charges markup ' + str(b2c_markup_fee)
                #if customer langauge is Kiswahili, get swahili description 

                transaction_data = {"global_id":global_id, 
                                    "entry_id":customer_id, 
                                    "sub_entry_id":'',
                                    "type":68,
                                    "account_number":b2c_income_acc, 
                                    "amount":b2c_markup_fee, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":date_created,
                                    "layer4_id":layer4_id
                                    }
                
                #Credit income Account with mpesa markup amount paid
                credit_income_trans = Transaction().credit_on_credit_account(transaction_data)
                #End of transaction posting
                
                if ((int(debit_income_trans["status"]) == 200) and (int(credit_income_trans["status"]) == 200)):
            
                    message = {
                            "wallet_account_status":debit_trans,
                            "b2c_utiltiy_account_status":credit_trans,
                            "b2c_utility_acc_status":debit_income_trans,
                            "b2c_income_acc_status":credit_income_trans,
                            "description":"Mpesa markup fee payment was successful",
                            "status":200}
                    return message
                
                else:
                    #Reverse the failed transaction
                    
                    if int(debit_trans["status"]) == 200:   
                        #Rollback this debit transaction                     
                        data = debit_trans["data"]
                        trans_id = debit_trans["data"]["trans_id"]                        
                        amount = float(debit_trans["data"]["amount"])
                        if amount >0 and trans_id is not None:
                            #Delete this specific debit transaction
                            rollback_debit_trans = Transaction().debit_on_credit_account_rollback(data)
                        else:
                            pass
                    
                    if int(credit_trans["status"]) == 200:
                        #Rollback this credit transaction

                        data = credit_trans["data"]
                        trans_id = credit_trans["data"]["trans_id"]
                        amount = float(credit_trans["data"]["amount"])
                        if amount >0 and trans_id is not None:
                            #Delete this specific credit transaction
                            rollback_credit_trans = Transaction().credit_on_debit_account_rollback(data)
                        else:
                            pass
                    
                    if int(debit_income_trans["status"]) == 200 and int(credit_income_trans["status"]) != 200:
                        #Rollback this debit transaction
                        data = debit_income_trans["data"]
                        trans_id = debit_income_trans["data"]["trans_id"]
                        amount = float(debit_income_trans["data"]["amount"])
                        if amount >0 and trans_id is not None:
                            #Delete this specific debit transaction
                            rollback_debit_income_trans = Transaction().debit_on_debit_account_rollback(data)
                        else:
                            pass
                    
                    if int(credit_income_trans["status"]) == 200 and int(debit_income_trans["status"]) != 200:
                        #Rollback this credit transaction

                        data = credit_income_trans["data"]
                        trans_id = credit_income_trans["data"]["trans_id"]
                        amount = float(credit_income_trans["data"]["amount"])
                        if amount >0 and trans_id is not None:
                            #Delete this specific credit transaction
                            rollback_credit_income_trans = Transaction().credit_on_credit_account_rollback(data)
                        else:
                            pass
                                
                    message = {
                        "status":201,
                        'error':'L_11',
                        "description":"Transaction failed!. Mpesa markup fee payment was not successful",
                        "customer_wallet_account_status":debit_trans,
                        "b2c_utiltiy_account_status":credit_trans,
                        "b2c_utility_acc_status":debit_income_trans,
                        "b2c_income_acc_status":credit_income_trans,
                        }
                    ErrorLogger().logError(message) 
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
                        rollback_debit_trans = Transaction().debit_on_credit_account_rollback(data)
                    else:
                        pass
                
                if int(credit_trans["status"]) == 200 and int(debit_trans["status"]) != 200:
                    #Rollback this credit transaction

                    data = credit_trans["data"]
                    trans_id = credit_trans["data"]["trans_id"]
                    amount = float(credit_trans["data"]["amount"])
                    if amount >0 and trans_id is not None:
                        #Delete this specific credit transaction
                        rollback_credit_trans = Transaction().credit_on_debit_account_rollback(data)
                    else:
                        pass                            

                message = {
                        "status":201,
                        'error':'L_11',
                        "description":"Transaction failed!. Mpesa transaction fee payment was not successful",
                        "Wallet_account_status":debit_trans,
                        "b2c_utiltiy_account_status":credit_trans,
                        }
                ErrorLogger().logError(message)
                return message
        # Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'L_18',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 