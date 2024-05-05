from flask import json, jsonify
from main import mysql
from resources.logs.logger import ErrorLogger
from resources.transactions.transaction import Transaction
from resources.alphanumeric.generate import UniqueNumber


class Loans():
    
     #API to create customer loan
    def customer_loan_creation(self, details):
        if details == None:
            message = {"status":402,
                       "description":"All details are required!"}
            ErrorLogger().logError(message) 
            return message
        
        interest_charge_rate = details["interest_charge_rate"]  
        interest_charge_rate = round(interest_charge_rate, 12)
        interest_rate_per_cycle = details["interest_rate_per_cycle"]
        interest_rate_per_cycle = round(interest_rate_per_cycle, 12) 
        interest_id = details["interest_id"]  
        repayments_per_duration_cycle = details["repayments_per_duration_cycle"]    
        frequency_id = details["frequency_id"]        
        duration_cycle_name = details["duration_cycle_name"]        
        loan_repayment_type = details["loan_repayment_type"]
        if loan_repayment_type ==1:
            repayment_merge_details = json.dumps(details["repayment_merge_details"])
        else:
            repayment_merge_details = ''

        if loan_repayment_type ==2:
            repayment_split_details = json.dumps(details["repayment_split_details"])
        else:
            repayment_split_details = ''

        maximum_rollovers = details["maximum_rollovers"]
        rollover_required = details["rollover_required"]
        
        rollover_id = details["rollover_id"]
        rollover_fee_rate = details["rollover_fee_rate"]
        rollover_fee_rate = round(rollover_fee_rate, 12) 
        
        rollover_rate_per_cycle = details["rollover_rate_per_cycle"]
        rollover_rate_per_cycle = round(rollover_rate_per_cycle, 12) 
        
        rollover_principal = int(details["rollover_principal"])
        rollover_interest = int(details["rollover_interest"])
        rollover_charges = int(details["rollover_charges"])
        
        defaulted_loan_fines_required = details["defaulted_loan_fines_required"]
        defaulted_loan_fines_details = details["defaulted_loan_fines_details"]
        defaulted_fine_principal = int(details["defaulted_fine_principal"])
        defaulted_fine_interest = int(details["defaulted_fine_interest"])
        defaulted_fine_charges = int(details["defaulted_fine_charges"])
        defaulted_loan_fines_applied_after = int(details["defaulted_loan_fines_applied_after"])
        defaulted_loan_fines_date = details["defaulted_loan_fines_date"]

        disbursement_mode = details["disbursement_mode"]
        loan_asset_account = details["loan_asset_account"]        
        wallet_account = details["wallet_account"]     
        chargelists = details["chargelists"]   
        total_fees = details["total_fees"]
        total_fees = round(total_fees, 12)         
        
        loan_id = details["loan_id"]
        total_interest_amount = details["total_interest_amount"]
        total_interest_amount = round(total_interest_amount, 12)
        customer_id = details["customer_id"]
        product_id = details["product_id"]
        principal_amount = details["principal_amount"]
        principal_amount = round(principal_amount, 12)
        loan_amount = details["loan_amount"]
        loan_amount = round(loan_amount, 12)
        duration_period = int(details["duration_period"])
        number_of_installments = details["number_of_installments"]
        loan_status = details["loan_status"]
        global_id = details["global_id"] 
        group_id = details["group_id"] 
        session_id = details["session_id"]         
        product_type = int(details["product_type"]) 
        product_class = int(details["product_class"])      
        date_created = details["date_created"]       
        
        rollover_expected_date = details["rollover_expected_date"]
        next_installment_date = details["next_installment_date"]
        # next_installment_amount = details["next_installment_amount"]
        # next_installment_amount = round(next_installment_amount, 12) 
        start_date = details["start_date"]
        end_date = details["end_date"]
        amount_paid = 0 
        
        print("Start from here 2")
        
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message) 
            return message

        try:   
            if principal_amount > 0:               
                
                cur.execute("""SELECT a.balance FROM accounts AS a INNER JOIN default_accounts AS d ON a.number = d.account_number WHERE d.default_type_number = 5 AND d.default_status =1""")
                b2c_details = cur.fetchone() 
                if b2c_details:
                    b2c_balance = float(b2c_details["balance"])
                    
                    if principal_amount <= b2c_balance:   
                                   
                        cron_state =0 
                        cur.execute("""INSERT INTO loans (id, global_id, customer_id, loan_product_id, group_id, product_class, loan_amount, principal_amount, principal_amount_paid, principal_amount_due,        interest_amount, interest_amount_paid,   interest_amount_due, charge_amount, charge_amount_paid, charge_amount_due, charges_details, interest_id, maximum_rollovers, rollover_required, rollover_id,       rollover_fee_rate, rollover_principal, rollover_interest, rollover_charges, rollover_expected_date, defaulted_loan_fines_required, defaulted_loan_fines_details, defaulted_fine_principal, defaulted_fine_interest, defaulted_fine_charges, defaulted_loan_fines_applied_after, defaulted_loan_fines_date, monthly_interest_rate, interest_rate_per_cycle, duration_length, duration_cycle, duration_cycle_name, repayments_per_duration_cycle,     total_installments, outstanding_installments, outstanding_interest_installments,         sms_remainders, outstanding_principal_demandnote_amount, outstanding_interest_demandnote_amount, outstanding_charge_demandnote_amount, next_installment_date, next_interest_installment_date, loan_repayment_type, repayment_merge_details, repayment_split_details, disbursement_mode, start_date, end_date, date_created,      status, demandnote_cronjob_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                    (loan_id, global_id, customer_id,      product_id, group_id, product_class, loan_amount, principal_amount,           amount_paid,      principal_amount, total_interest_amount,          amount_paid, total_interest_amount,    total_fees,        amount_paid,        total_fees,     chargelists, interest_id, maximum_rollovers, rollover_required, rollover_id, rollover_rate_per_cycle, rollover_principal, rollover_interest, rollover_charges, rollover_expected_date, defaulted_loan_fines_required, defaulted_loan_fines_details, defaulted_fine_principal, defaulted_fine_interest, defaulted_fine_charges, defaulted_loan_fines_applied_after, defaulted_loan_fines_date,  interest_charge_rate, interest_rate_per_cycle, duration_period,   frequency_id, duration_cycle_name, repayments_per_duration_cycle, number_of_installments,   number_of_installments,            number_of_installments, number_of_installments,                        principal_amount,                  total_interest_amount,                           total_fees, next_installment_date,          next_installment_date, loan_repayment_type, repayment_merge_details, repayment_split_details, disbursement_mode, start_date, end_date, date_created, loan_status,                cron_state))
                        mysql.get_db().commit()
                        
                        #####Insert demand note generating table
                        
                        status = 1
                        zero = 0
                        
                        cur.execute("""INSERT INTO loan_demand_notes_generated (loan_id, principal_amount, date_created, status,     total_demand_notes,   pending_demand_notes, principal_demand_notes_pending, principal_demand_notes_processed, interest_demand_notes_pending, interest_demand_notes_processed, demandnote_cronjob_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                                               (loan_id, principal_amount, date_created, status, number_of_installments, number_of_installments,         number_of_installments,                             zero,        number_of_installments,                            zero,                      zero))
                        mysql.get_db().commit() 
                         
                        #Start of transaction posting - Debit Loan Asset Account with Principal amount
                    
                        transaction_name = 'Loan'
                        #if customer langauge is English, get english description 
                        description = 'Loan disbursemnt of Kes ' + str(principal_amount) + ". Loan reference number is " + loan_id
                        #if customer langauge is Kiswahili, get swahili description 

                        layer4_id = UniqueNumber().transactionsdebitcreditId() 
                        transaction_data = {"global_id":global_id, 
                                            "entry_id":loan_id, 
                                            "sub_entry_id":'',
                                            "type":11,
                                            "account_number":loan_asset_account, 
                                            "amount":principal_amount, 
                                            "transaction_name":transaction_name,
                                            "description":description, 
                                            "settlement_date":date_created,
                                            "layer4_id":layer4_id
                                            }
                    
                        #Debit Loan Asset Account with Principal amount
                        debit_trans = Transaction().debit_on_debit_account(transaction_data)
                        #End of transaction posting
                        #Start of transaction posting - Credit Customer Wallet with Principal amount

                        transaction_name = 'Loan disbursement'
                        #if customer langauge is English, get english description 
                        description = 'Loan disbursement of Kes ' + str(principal_amount) + ". Loan reference number is " + loan_id
                        #if customer langauge is Kiswahili, get swahili description 

                        transaction_data = {"global_id":global_id,
                                            "entry_id":loan_id, 
                                            "sub_entry_id":'',
                                            "type":12,
                                            "account_number":wallet_account, 
                                            "amount":principal_amount, 
                                            "transaction_name":transaction_name,
                                            "description":description, 
                                            "settlement_date":date_created,
                                            "layer4_id":layer4_id
                                            }
                    
                        #Credit Customer Wallet with Principal amount
                        credit_trans = Transaction().credit_on_credit_account(transaction_data)
                        #End of transaction posting
                        
                        if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):   
                            
                            #session_id    
                            if product_type == 2:
                                #update okoa airtime to show a loan was created successfully
                                cur.execute("""UPDATE loan_requests_okoa_airtime SET loan_created_status = 1 WHERE id = %s""",(session_id))
                                mysql.get_db().commit() 
                            else:
                                pass          

                            message = {
                                'status': 200,
                                "description":"Customer loan was created successfully", 
                                "loan_id":loan_id,
                                "principal_amount":principal_amount,                                           
                                "loan_asset_account_status":debit_trans,
                                "customer_wallet_account_status":credit_trans,
                                }
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
                                'status': 201,                 
                                "loan_asset_account_status":debit_trans,
                                "customer_wallet_account_status":credit_trans,
                                }
                            return message
                        
                    else:
                        message = {
                                "status": 201,                 
                                "description":"Transaction failed. Insufficient B2C Balance",
                                }
                        return message
                            
            else:
                message = {
                            "status": 201,                 
                            "description":"Transaction failed. Loan amount is not correct!",
                            }
                return message
        
        # Error handling
        except Exception as error:
            message = {'status':501,
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 
        finally:
            cur.close()