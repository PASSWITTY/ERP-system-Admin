from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.alphanumeric.generate import UniqueNumber
from resources.transactions.transaction import Transaction

class WalletWithdraw():
    
    #API to withdraw from wallet account to customer mpesa
    def  customer_wallet_withdraw(self, details):
        if details == None:
            message = {"status":402,
                       'error':'ww_01',
                       "description":"All details are required!"}
            ErrorLogger().logError(message) 
            return message
     
        customer_id = details["customer_id"]
        global_id = details["global_id"]
        amount = details["amount"]
        amount = round(amount, 12) 
        bank_account_number = details["bank_account_number"]
        wallet_account = details["wallet_account"]
        
        date_created = Localtime().gettime()
    
        try:
            #Get customer wallet account
                         
            #Start of transaction posting - Debit Customer Wallet Account with amount to withdraw
            transaction_name = 'Withdraw to Mpesa'
            #if customer langauge is English, get english description 
            description = 'Wallet withdraw of Kes ' + str(amount)
            #if customer langauge is Kiswahili, get swahili description 
            layer4_id = UniqueNumber().transactionsdebitcreditId() 

            transaction_data = {"global_id":global_id, 
                                "entry_id":customer_id, 
                                "sub_entry_id":'',
                                "type":13,
                                "account_number":wallet_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":date_created,
                                "layer4_id":layer4_id
                                }
            
            #Debit customer wallet with amount to withdraw
            debit_trans = Transaction().debit_on_credit_account(transaction_data)
            
            #End of transaction posting

            #Start of transaction posting - Credit B2C Bank Accont with amount to withdraw
            transaction_name = 'Withdraw to Mpesa'
            #if customer langauge is English, get english description 
            description = 'Wallet withdraw of Kes ' + str(amount)
            #if customer langauge is Kiswahili, get swahili description 

            transaction_data = {"global_id":global_id, 
                                "entry_id":customer_id, 
                                "sub_entry_id":'',
                                "type":14,
                                "account_number":bank_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":date_created,
                                "layer4_id":layer4_id
                                }
            
            #Credit B2C Bank Accont with amount to withdraw
            credit_trans = Transaction().credit_on_debit_account(transaction_data)
            #End of transaction posting
            
            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                
              
                message = {
                    "status":200,
                    "customer_wallet_account_status":debit_trans,
                    "bank_account_status":credit_trans}
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
                    'error':'ww_02',
                    "customer_wallet_account_status":debit_trans,
                    "bank_account_status":credit_trans}
                ErrorLogger().logError(message) 
                return message
    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'ww_03',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message
        
    #API to withdraw from wallet account when a customer buys airtime with wallet balance
    def  customer_airtime_purchase_wallet_withdraw(self, details):
        if details == None:
            message = {"status":402,
                       'error':'ww_04',
                       "description":"All details are required!"}
            ErrorLogger().logError(message) 
            return message
     
        customer_id = details["customer_id"]
        global_id = details["global_id"]
        amount = details["amount"]
        amount = round(amount, 12) 
        bank_account_number = details["bank_account_number"]
        wallet_account = details["wallet_account"]
        
        date_created = Localtime().gettime()
    
        try:
            #Get customer wallet account
                         
            #Start of transaction posting - Debit Customer Wallet Account with amount to withdraw
            transaction_name = 'Airtime Purchase'
            #if customer langauge is English, get english description 
            description = 'Wallet withdraw of Kes ' + str(amount)
            #if customer langauge is Kiswahili, get swahili description 
            layer4_id = UniqueNumber().transactionsdebitcreditId() 

            transaction_data = {"global_id":global_id, 
                                "entry_id":customer_id, 
                                "sub_entry_id":'',
                                "type":61,
                                "account_number":wallet_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":date_created,
                                "layer4_id":layer4_id
                                }
            
            #Debit customer wallet with amount to withdraw
            debit_trans = Transaction().debit_on_credit_account(transaction_data)
            
            #End of transaction posting

            #Start of transaction posting - Credit B2C Bank Accont with amount to withdraw
            transaction_name = 'Airtime Purchase'
            #if customer langauge is English, get english description 
            description = 'Wallet withdraw of Kes ' + str(amount)
            #if customer langauge is Kiswahili, get swahili description 

            transaction_data = {"global_id":global_id, 
                                "entry_id":customer_id, 
                                "type":62,
                                "account_number":bank_account_number, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":date_created,
                                "layer4_id":layer4_id
                                }
            
            #Credit B2C Bank Accont with amount to withdraw
            credit_trans = Transaction().credit_on_debit_account(transaction_data)
            #End of transaction posting
            
            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
                
              
                message = {
                    "status":200,
                    "customer_wallet_account_status":debit_trans,
                    "bank_account_status":credit_trans}
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
                    'error':'ww_05',
                    "customer_wallet_account_status":debit_trans,
                    "bank_account_status":credit_trans}
                ErrorLogger().logError(message) 
                return message
    
        #Error handling
        except Exception as error:
            message = {'status':501,
                       'error':'ww_06',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message