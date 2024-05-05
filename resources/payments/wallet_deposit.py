from flask import json, jsonify
from main import mysql
from dateutil.relativedelta import relativedelta    
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.alphanumeric.generate import UniqueNumber
from resources.transactions.transaction import Transaction

class WalletDeposit():

    #API to deposit from mpesa to customer wallet 
    def customer_wallet_deposit(self, details):
        if details == None:
            message = {'status':402,
                       'description':'Request data is missing some details!'}
            return message
     
        wallet_account = details["wallet_account"]
        global_id = details["global_id"]
        amount = details["amount"]
        amount = round(amount, 12) 
        bank_account_number = details["bank_account_number"]
        date_created = Localtime().gettime()
        entry_id = details["trans_ref"]
        
        try:         

            #Start of transaction posting - Debit C2B Bank Accont with deposit amount
            transaction_name = 'Mpesa Deposit'
            #if customer langauge is English, get english description 
            description = 'Customer Deposit of Kes ' + str(amount) + '. Mpesa reference ' + entry_id
            #if customer langauge is Kiswahili, get swahili description 
            layer4_id = UniqueNumber().transactionsdebitcreditId() 

            transaction_data = {"global_id":global_id, 
                                "entry_id":entry_id, 
                                "sub_entry_id":'',
                                "type":19,
                                "account_number":bank_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":date_created,
                                "layer4_id":layer4_id
                                }
            
            #Debit C2B Account with deposit amount
            debit_trans = Transaction().debit_on_debit_account(transaction_data)
            #End of transaction posting
                        
            #Start of transaction posting - Credit Customer Wallet Accont with amount deposited
            transaction_name = 'Mpesa Deposit'
            #if customer langauge is English, get english description 
            description = 'Mpesa Deposit of Kes ' + str(amount) + '. Mpesa reference ' + entry_id
            #if customer langauge is Kiswahili, get swahili description 

            transaction_data = {"global_id":global_id, 
                                "entry_id":entry_id, 
                                "sub_entry_id":'',
                                "type":20,
                                "account_number":wallet_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":date_created,
                                "layer4_id":layer4_id
                                }
            
            #Credit Wallet Accont with deposit amount
            credit_trans = Transaction().credit_on_credit_account(transaction_data)
            #End of transaction posting

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):

                message = {"c2b_paybill_account_status":debit_trans,
                           "wallet_account_status":credit_trans,
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
                    "description":"Transaction failed and was rolledback",
                    "c2b_paybill_account_status":debit_trans,
                    "wallet_account_status":credit_trans}
                return message

        #Error handling
        except Exception as error:
            message = {'status':501,
                       'description':'Transaction had an error. Error description ' + format(error)}
            return message 
        
        
    #API to deposit from bank cheque to customer wallet 
    def customer_wallet_cheque_deposit(self, details):
        if details == None:
            message = {'status':402,
                       'description':'Request data is missing some details!'}
            return message
     
        wallet_account = details["wallet_account"]
        global_id = details["global_id"]
        amount = details["amount"]
        amount = round(amount, 12) 
        bank_account_number = details["bank_account_number"]
        date_created = Localtime().gettime()
        entry_id = details["trans_ref"]
        
        try:         

            #Start of transaction posting - Debit C2B Bank Accont with deposit amount
            transaction_name = 'Cheque Deposit'
            #if customer langauge is English, get english description 
            description = 'Cheque Deposit of Kes ' + str(amount) + '. Cheque number ' + entry_id
            #if customer langauge is Kiswahili, get swahili description 
            layer4_id = UniqueNumber().transactionsdebitcreditId() 

            transaction_data = {"global_id":global_id, 
                                "entry_id":entry_id, 
                                "sub_entry_id":'',
                                "type":90,
                                "account_number":bank_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":date_created,
                                "layer4_id":layer4_id
                                }
            
            #Debit C2B Account with deposit amount
            debit_trans = Transaction().debit_on_debit_account(transaction_data)
            #End of transaction posting
                        
            #Start of transaction posting - Credit Customer Wallet Accont with amount deposited
            transaction_name = 'Cheque Deposit'
            #if customer langauge is English, get english description 
            description = 'Cheque Deposit of Kes ' + str(amount) + '. Cheque number ' + entry_id
            #if customer langauge is Kiswahili, get swahili description 

            transaction_data = {"global_id":global_id, 
                                "entry_id":entry_id, 
                                "sub_entry_id":'',
                                "type":91,
                                "account_number":wallet_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":date_created,
                                "layer4_id":layer4_id
                                }
            
            #Credit Wallet Accont with deposit amount
            credit_trans = Transaction().credit_on_credit_account(transaction_data)
            #End of transaction posting

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):

                message = {"bank_account_status":debit_trans,
                           "wallet_account_status":credit_trans,
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
                    "description":"Transaction failed and was rolledback",
                    "bank_account_status":debit_trans,
                    "wallet_account_status":credit_trans}
                return message

        #Error handling
        except Exception as error:
            message = {'status':501,
                       'description':'Transaction had an error. Error description ' + format(error)}
            return message 