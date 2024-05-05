from flask import Response, json, jsonify
from main import mysql
from datetime import datetime
from resources.transactions.transaction import Transaction
from resources.payload.payload import Localtime
from resources.alphanumeric.generate import UniqueNumber
from accounts_module.accounts_model import Account
from resources.logs.logger import ErrorLogger


from decimal import Decimal

class Agent():

     #API to approve a agents cashout    
    def approve_agent_cashout_expense(self, details):
        if details == None:
            message = {'status':402,
                       'error':'ap_a16',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]
        approved_by = details["user_id"]
        expense_account_number = details["expense_account_number"]
        payable_account_number = details["payable_account_number"]
        amount = float(details["amount"])
        settlement_date = details["settlement_date"]
        
        date_approved = Localtime().gettime()

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'ap_a17',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
       
        try: 
            
            #Start of transaction - Increase Agent Expense Account Balance
            global_id = UniqueNumber().globalIdentifier()
            
            transaction_name = 'Agent Payout Expense Incurred'
            description = 'Agent cashout expense incurred of Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            layer4_id = UniqueNumber.transactionsdebitcreditId(self)
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":74,
                                "account_number":expense_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id

                                }
                            
            #Debit Agent expense account with interest payout amount  
            debit_trans = Transaction.debit_on_debit_account(self, transaction_data)
            #End of transaction - Increase expense account
            
            #Start of transaction - Increase Agent Payable Account Balance
                       
            transaction_name = 'Agent Payout Expense Incurred'
            description = 'Agent cashout expense incurred of Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":75,
                                "account_number":payable_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id
                                }
                            
            #Credit Agent Payable account with interest payout amount
            credit_trans = Transaction.credit_on_credit_account(self, transaction_data)
            #End of transaction - Increase payable account

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                
                #update account status
                cur.execute("""UPDATE sacco_payout_expenses set status=1, date_approved = %s, approved_by =%s WHERE id = %s""", ([date_approved, approved_by, id]))
                mysql.get_db().commit()

                message = {'status':200,
                           "agent_expense_transaction_status":debit_trans,
                           "agent_payable_transaction_status":credit_trans,
                           'description':'Sacco payout expense was approved successfully'}
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
                           "error":"ap_a37",
                           "status":201,
                           "description":"Agent payout expense approval was not successful!",
                           "agent_expense_transaction_status":debit_trans,
                           "agent_payable_transaction_status":credit_trans}
                
                ErrorLogger().logError(message)
                return message
            
            
        #Error handling
        except Exception as error:         
            message = {'status':501,
                       'error':'ap_a18',
                       'description':'Failed to approve agent payout expense record. Error description ' + format(error)}            
            ErrorLogger().logError(message)
            return message
        finally:
                cur.close()
                
        
    #API to approve a agents cashout    
    def approve_agent_cashout_payment(self, details):
        if details == None:
            message = {'status':402,
                       'error':'ap_a32',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]
        approved_by = details["user_id"]
        bank_account_number = details["bank_account_number"]
        payable_account_number = details["payable_account_number"]
        amount = float(details["amount"])
        settlement_date = details["settlement_date"]
        
        date_approved = Localtime().gettime()

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'ap_a33',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
       
        try: 
            
            #Start of transaction - Decrease Agent Payable Account Balance
            global_id = UniqueNumber().globalIdentifier()
            
            transaction_name = 'Agent Payout Expense Paid'
            description = 'Agent cashout expense payment of Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            layer4_id = UniqueNumber.transactionsdebitcreditId(self)
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":76,
                                "account_number":payable_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id

                                }
                            
            #Debit Agent payable account with interest amount paid
            debit_trans = Transaction.debit_on_credit_account(self, transaction_data)
            #End of transaction - Decrease payable account
            
            #Start of transaction - Decrease Bank Account Balance
                       
            transaction_name = 'Agent Payout Expense Paid'
            description = 'Agent cashout expense payment of Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":'',
                                "type":77,
                                "account_number":bank_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id
                                }
                            
            #Credit Bank account with interest payout amount
            credit_trans = Transaction.credit_on_debit_account(self, transaction_data)
            #End of transaction - Decrease Bank account

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                
                #update account status
                cur.execute("""UPDATE sacco_payout_payment set status=1, date_approved = %s, approved_by =%s WHERE id = %s""", ([date_approved, approved_by, id]))
                mysql.get_db().commit()

                message = {'status':200,
                           "agent_payable_transaction_status":debit_trans,
                           "bank_transaction_status":credit_trans,
                           'description':'Sacco payout payment was approved successfully'}
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
                           "error":"ap_a34",
                           "status":201,
                           "description":"Agent payout payment approval was not successful!",
                           "agent_payable_transaction_status":debit_trans,
                           "bank_transaction_status":credit_trans}
                
                ErrorLogger().logError(message)
                return message
            
            
        #Error handling
        except Exception as error:         
            message = {'status':501,
                       'error':'ap_a35',
                       'description':'Failed to agent payout payment record. Error description ' + format(error)}            
            ErrorLogger().logError(message)
            return message
        finally:
                cur.close()


    #API to approve a cashout loan settlemtn    
    def approve_cashout_loan_settlement(self, details):
        if details == None:
            message = {'status':402,
                       'error':'ap_a36',
                       'description':'Request data is missing some details!'}
            ErrorLogger().logError(message)
            return message

        id = details["id"]
        approved_by = details["user_id"]
        wallet_account_number = details["wallet_account_number"]
        payable_account_number = details["payable_account_number"]
        amount = float(details["amount"])
        settlement_date = details["settlement_date"]
        customer_id = details["customer_id"]
        loan_id = details["loan_id"]
        
        date_approved = Localtime().gettime()

        try:
            cur = mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'error':'ap_a37',
                       'description':"Couldn't connect to the Database!"}
            ErrorLogger().logError(message)
            return message
       
        try: 
            
            #Start of transaction - Decrease Agent Payable Account Balance
            global_id = UniqueNumber().globalIdentifier()
            
            transaction_name = 'Settle defaulted Loan'
            description = 'Agent cashout loan settlement of Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            layer4_id = UniqueNumber.transactionsdebitcreditId(self)
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":loan_id,
                                "type":92,
                                "account_number":payable_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id

                                }
                            
            #Debit Agent payable account with loan amount paid
            debit_trans = Transaction.debit_on_credit_account(self, transaction_data)
            #End of transaction - Decrease payable account
            
            #Start of transaction - Increase customer wallet account balance
                       
            transaction_name = 'Settle defaulted Loan'
            description = 'Agent cashout loan settlement of Kes' + str(amount)
            settlement_date = Localtime().gettime() 
            transaction_data = {
                                "global_id":global_id, 
                                "entry_id":id, 
                                "sub_entry_id":loan_id,
                                "type":93,
                                "account_number":wallet_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":settlement_date,
                                "layer4_id":layer4_id
                                }
                            
            #Credit wallet account with loan amount paid
            credit_trans = Transaction.credit_on_credit_account(self, transaction_data)
            #End of transaction - Decrease Bank account

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                
                #update account status
                cur.execute("""UPDATE cashout_loan_settlement set status=1, date_approved = %s, approved_by =%s WHERE id = %s""", ([date_approved, approved_by, id]))
                mysql.get_db().commit()

                message = {'status':200,
                           "agent_payable_transaction_status":debit_trans,
                           "customer_wallet_transaction_status":credit_trans,
                           'description':'Agent cashout loan settlement was approved successfully'}
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
                        rollback_credit_trans = Transaction().credit_on_credit_account_rollback(data)
                    else:
                        pass                            

                message = {
                           "error":"ap_a38",
                           "status":201,
                           "description":"Agent cashout loan settlement approval was not successful!",
                           "agent_payable_transaction_status":debit_trans,
                           "bank_transaction_status":credit_trans}
                
                ErrorLogger().logError(message)
                return message
            
            
        #Error handling
        except Exception as error:         
            message = {'status':501,
                       'error':'ap_a39',
                       'description':'Failed to agent payout payment record. Error description ' + format(error)}            
            ErrorLogger().logError(message)
            return message
        finally:
                cur.close()