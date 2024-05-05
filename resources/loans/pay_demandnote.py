from resources.logs.logger import ErrorLogger
from resources.transactions.transaction import Transaction
from resources.alphanumeric.generate import UniqueNumber

class PayDemandNotes():
    def rollover_fee_demand_note_payment(self, details):
        if details == None:
            message = {"status":402,
                       'error':'pd_m04',
                        "description":"Request data is missing some details!"}
            ErrorLogger().logError(message)
            return message

        loan_id = details["loan_id"] 
        global_id = details["global_id"]
        amount = details["amount"]
        amount = round(amount, 12) 
        wallet_account = details["wallet_account"]
        receivable_account = details["receivable_account"]
        rollover_fee_earned_account = details["rollover_fee_earned_account"] 
        rollover_fee_realized_account = details["rollover_fee_realized_account"]        
        payment_date = details["payment_date"]
        rollover_type = details["rollover_type"]

        #Try except block to handle execute task
        try:
            #Start of transaction posting - Debit Wallet Account with demand note amount paid
            transaction_name = rollover_type + ' rollover fee payment'
            #if customer langauge is English, get english description 
            description = 'Loan rollover fee payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 
            layer4_id = UniqueNumber().transactionsdebitcreditId()
            transaction_data = {"global_id":global_id, 
                                "entry_id":loan_id, 
                                "sub_entry_id":'',
                                "type":47,
                                "account_number":wallet_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":payment_date,
                                "layer4_id":layer4_id

                                }
            
            #Debit wallet account with demand note amount paid
            debit_trans = Transaction().debit_on_credit_account(transaction_data)
            #End of transaction posting

            #Start of transaction posting - Credit Customer Receivable Account with demand note amount paid

            transaction_name = rollover_type + ' rollover fee payment'
            #if customer langauge is English, get english description 
            description = 'Loan rollover fee payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 

            transaction_data = {"global_id":global_id, 
                                "entry_id":loan_id, 
                                "sub_entry_id":'',
                                "type":48,
                                "account_number":receivable_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":payment_date,
                                "layer4_id":layer4_id
                                }
            
            #Credit Customer Receivable Account with rollover fee demand note amount paid
            credit_trans = Transaction().credit_on_debit_account(transaction_data)
            #End of transaction posting

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):

                #Start of transaction posting - Debit rollover fee Income Earned Account with rollover fee demand note amount paid

                transaction_name = rollover_type + ' rollover fee payment'
                #if customer langauge is English, get english description 
                description = 'Loan rollover fee payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
                #if customer langauge is Kiswahili, get swahili description 

                layer4_id = UniqueNumber().transactionsdebitcreditId()
                transaction_data = {"global_id":global_id, 
                                    "entry_id":loan_id, 
                                    "sub_entry_id":'',
                                    "type":49,
                                    "account_number":rollover_fee_earned_account, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":payment_date,
                                    "layer4_id":layer4_id
                                    }
                
                #Debit rollover fee income earned account with demand note amount paid
                debit_income_trans = Transaction().debit_on_credit_account(transaction_data)
                #End of transaction posting

                #Start of transaction posting - Credit Customer Receivable Account with rollover fee demand note amount paid

                transaction_name = rollover_type + ' rollover fee payment'
                #if customer langauge is English, get english description 
                description = 'Loan rollover fee payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
                #if customer langauge is Kiswahili, get swahili description 

                transaction_data = {"global_id":global_id, 
                                    "entry_id":loan_id, 
                                    "sub_entry_id":'',
                                    "type":50,
                                    "account_number":rollover_fee_realized_account, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":payment_date,
                                    "layer4_id":layer4_id
                                    }
                
                #Credit Customer Receivable Account with rollover fee demand note amount paid
                credit_income_trans = Transaction().credit_on_credit_account(transaction_data)
                #End of transaction posting

                if ((int(debit_income_trans["status"]) == 200) and (int(credit_income_trans["status"]) == 200)):
        
                    message = {
                            "wallet_account_status":debit_trans,
                            "receivable_account_status":credit_trans,
                            "income_earned_account_status":debit_income_trans,
                            "income_realized_account_status":credit_income_trans,
                            "description":"Rollover fee payment was received successfully",
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
                            rollback_debit_income_trans = Transaction().debit_on_credit_account_rollback(data)
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
                                "wallet_account_status":debit_trans,
                                "receivable_account_status":credit_trans,
                                "income_earned_account_status":debit_income_trans,
                                "income_realized_account_status":credit_income_trans,
                                "description":"Transaction failed!. Rollover fee payment was not successful",
                                'error':'pd_m05',
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
                    'error':'pd_m06',
                    "wallet_account":debit_trans,
                    "receivable_account":credit_trans}
                ErrorLogger().logError(message)
                return message

        except Exception as error:
            message = {'status':501,
                       'error':'pd_m07',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 

    def defaulted_loan_fine_demand_note_payment(self, details):
        if details == None:
            message = {"status":402,
                       'error':'pd_m04',
                        "description":"Request data is missing some details!"}
            ErrorLogger().logError(message)
            return message

        loan_id = details["loan_id"] 
        global_id = details["global_id"]
        amount = details["amount"]
        amount = round(amount, 12) 
        wallet_account = details["wallet_account"]
        receivable_account = details["receivable_account"]
        defaultedloan_fine_earned_account = details["defaultedloan_fine_earned_account"] 
        defaultedloan_fine_realized_account = details["defaultedloan_fine_realized_account"]        
        payment_date = details["payment_date"]
        charge_name = details["charge_name"]

        #Try except block to handle execute task
        try:
            #Start of transaction posting - Debit Wallet Account with demand note amount paid
            transaction_name = charge_name + ' payment'
            #if customer langauge is English, get english description 
            description = 'Defaulted loan fine payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 
            layer4_id = UniqueNumber().transactionsdebitcreditId()
            transaction_data = {"global_id":global_id, 
                                "entry_id":loan_id, 
                                "sub_entry_id":'',
                                "type":51,
                                "account_number":wallet_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":payment_date,
                                "layer4_id":layer4_id

                                }
            
            #Debit wallet account with demand note amount paid
            debit_trans = Transaction().debit_on_credit_account(transaction_data)
            #End of transaction posting

            #Start of transaction posting - Credit Customer Receivable Account with demand note amount paid

            transaction_name = charge_name + ' payment'
            #if customer langauge is English, get english description 
            description = 'Defaulted loan fine payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 

            transaction_data = {"global_id":global_id, 
                                "entry_id":loan_id, 
                                "sub_entry_id":'',
                                "type":52,
                                "account_number":receivable_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":payment_date,
                                "layer4_id":layer4_id
                                }
            
            #Credit Customer Receivable Account with defaulted loan fine demand note amount paid
            credit_trans = Transaction().credit_on_debit_account(transaction_data)
            #End of transaction posting

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):

                #Start of transaction posting - Debit defaulted loan fine Income Earned Account with defaulted loan fine demand note amount paid

                transaction_name = charge_name +' payment'
                #if customer langauge is English, get english description 
                description = 'Defaulted loan fine payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
                #if customer langauge is Kiswahili, get swahili description 

                layer4_id = UniqueNumber().transactionsdebitcreditId()
                transaction_data = {"global_id":global_id, 
                                    "entry_id":loan_id, 
                                    "sub_entry_id":'',
                                    "type":53,
                                    "account_number":defaultedloan_fine_earned_account, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":payment_date,
                                    "layer4_id":layer4_id
                                    }
                
                #Debit defaulted loan fine income earned account with demand note amount paid
                debit_income_trans = Transaction().debit_on_credit_account(transaction_data)
                #End of transaction posting

                #Start of transaction posting - Credit Customer Receivable Account with defaulted loan fine demand note amount paid

                transaction_name = charge_name +' payment'
                #if customer langauge is English, get english description 
                description = 'Defaulted loan fine payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
                #if customer langauge is Kiswahili, get swahili description 

                transaction_data = {"global_id":global_id, 
                                    "entry_id":loan_id, 
                                    "sub_entry_id":'',
                                    "type":54,
                                    "account_number":defaultedloan_fine_realized_account, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":payment_date,
                                    "layer4_id":layer4_id
                                    }
                
                #Credit Customer Receivable Account with defaulted loan fine demand note amount paid
                credit_income_trans = Transaction().credit_on_credit_account(transaction_data)
                #End of transaction posting

                if ((int(debit_income_trans["status"]) == 200) and (int(credit_income_trans["status"]) == 200)):
        
                    message = {
                            "wallet_account_status":debit_trans,
                            "receivable_account_status":credit_trans,
                            "income_earned_account_status":debit_income_trans,
                            "income_realized_account_status":credit_income_trans,
                            "description":"Defaulted loan fine payment was received successfully",
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
                            rollback_debit_income_trans = Transaction().debit_on_credit_account_rollback(data)
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
                                "wallet_account_status":debit_trans,
                                "receivable_account_status":credit_trans,
                                "income_earned_account_status":debit_income_trans,
                                "income_realized_account_status":credit_income_trans,
                                "description":"Transaction failed!. Defaulted loan fine payment was not successful",
                                'error':'pd_m05',
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
                    'error':'pd_m06',
                    "wallet_account":debit_trans,
                    "receivable_account":credit_trans}
                ErrorLogger().logError(message)
                return message

        except Exception as error:
            message = {'status':501,
                       'error':'pd_m07',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
         
    def principal_demand_note_payment(self, details):
        if details == None:
            message = {"status":402,
                       'error':'pd_m01',
                       "description":"Request data is missing some details!"}
            ErrorLogger().logError(message)
            return message

        loan_id = details["loan_id"]
        wallet_account = details["wallet_account"]
        receivable_account = details["receivable_account"]
        global_id = details["global_id"]
        amount = details["amount"]
        amount = round(amount, 12) 
        payment_date = details["payment_date"]

        #Try except block to handle execute task
        try:
            #Start of transaction posting - Debit Wallet Account with demand note amount paid

            transaction_name = 'Principal payment'
            #if customer langauge is English, get english description 
            description = 'Loan principal payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 
            
            layer4_id = UniqueNumber.transactionsdebitcreditId(self) 

            transaction_data = {"global_id":global_id, 
                                "entry_id":loan_id, 
                                "sub_entry_id":'',
                                "type":21,
                                "account_number":wallet_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":payment_date,
                                "layer4_id":layer4_id
                                }
            
            #Debit wallet account with demand note amount paid
            debit_trans = Transaction().debit_on_credit_account(transaction_data)
            #End of transaction posting

            #Start of transaction posting - Credit Customer Receivable Account with demand note amount paid

            transaction_name = 'Principal payment'
            #if customer langauge is English, get english description 
            description = 'Loan principal payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 

            transaction_data = {"global_id":global_id, 
                                "entry_id":loan_id, 
                                "sub_entry_id":'',
                                "type":22,
                                "account_number":receivable_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":payment_date,
                                "layer4_id":layer4_id
                                }
            
            #Credit Customer Receivable Account with demand note amount paid
            credit_trans = Transaction().credit_on_debit_account(transaction_data)
            #End of transaction posting

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):
        
                message = {
                        "wallet_account_status":debit_trans,
                        "receivable_account_status":credit_trans,
                        "description":"Loan principal payment was received successfully",
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
                        "wallet_account_status":debit_trans,
                        "receivable_account_status":credit_trans,
                        "status":201,
                        'error':'pd_m02'}
                ErrorLogger().logError(message)
                return message

        except Exception as error:
            message = {'status':501,
                       'error':'pd_m03',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        
    def interest_demand_note_payment(self, details):
        if details == None:
            message = {"status":402,
                       'error':'pd_m04',
                        "description":"Request data is missing some details!"}
            ErrorLogger().logError(message)
            return message

        loan_id = details["loan_id"] 
        global_id = details["global_id"]
        amount = details["amount"]
        amount = round(amount, 12) 
        wallet_account = details["wallet_account"]
        receivable_account = details["receivable_account"]
        interest_earned_account = details["interest_earned_account"] 
        interest_realized_account = details["interest_realized_account"]        
        payment_date = details["payment_date"]

        #Try except block to handle execute task
        try:
            #Start of transaction posting - Debit Wallet Account with interest demand note amount paid
            transaction_name = 'Interest payment'
            #if customer langauge is English, get english description 
            description = 'Loan interest payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 
            layer4_id = UniqueNumber().transactionsdebitcreditId()
            transaction_data = {"global_id":global_id, 
                                "entry_id":loan_id, 
                                "sub_entry_id":'',
                                "type":23,
                                "account_number":wallet_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":payment_date,
                                "layer4_id":layer4_id

                                }
            
            #Debit wallet account with demand note amount paid
            debit_trans = Transaction().debit_on_credit_account(transaction_data)
            #End of transaction posting

            #Start of transaction posting - Credit Customer Receivable Account with interest demand note amount paid

            transaction_name = 'Interest payment'
            #if customer langauge is English, get english description 
            description = 'Loan interest payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 

            transaction_data = {"global_id":global_id, 
                                "entry_id":loan_id, 
                                "sub_entry_id":'',
                                "type":24,
                                "account_number":receivable_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":payment_date,
                                "layer4_id":layer4_id
                                }
            
            #Credit Customer Receivable Account with interest demand note amount paid
            credit_trans = Transaction().credit_on_debit_account(transaction_data)
            #End of transaction posting

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):

                #Start of transaction posting - Debit Interest Income Earned Account with interest demand note amount paid

                transaction_name = 'Interest payment'
                #if customer langauge is English, get english description 
                description = 'Loan interest payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
                #if customer langauge is Kiswahili, get swahili description 

                layer4_id = UniqueNumber().transactionsdebitcreditId()
                transaction_data = {"global_id":global_id, 
                                    "entry_id":loan_id, 
                                    "sub_entry_id":'',
                                    "type":25,
                                    "account_number":interest_earned_account, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":payment_date,
                                    "layer4_id":layer4_id
                                    }
                
                #Debit interest income earned account with demand note amount paid
                debit_income_trans = Transaction().debit_on_credit_account(transaction_data)
                #End of transaction posting

                #Start of transaction posting - Credit Customer Receivable Account with interest demand note amount paid

                transaction_name = 'Interest payment'
                #if customer langauge is English, get english description 
                description = 'Loan interest payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
                #if customer langauge is Kiswahili, get swahili description 

                transaction_data = {"global_id":global_id, 
                                    "entry_id":loan_id, 
                                    "sub_entry_id":'',
                                    "type":26,
                                    "account_number":interest_realized_account, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":payment_date,
                                    "layer4_id":layer4_id
                                    }
                
                #Credit Customer Receivable Account with interest demand note amount paid
                credit_income_trans = Transaction().credit_on_credit_account(transaction_data)
                #End of transaction posting

                if ((int(debit_income_trans["status"]) == 200) and (int(credit_income_trans["status"]) == 200)):
        
                    message = {
                            "wallet_account_status":debit_trans,
                            "receivable_account_status":credit_trans,
                            "income_earned_account_status":debit_income_trans,
                            "income_realized_account_status":credit_income_trans,
                            "description":"Loan interest payment was received successfully",
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
                            rollback_debit_income_trans = Transaction().debit_on_credit_account_rollback(data)
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
                                "wallet_account_status":debit_trans,
                                "receivable_account_status":credit_trans,
                                "income_earned_account_status":debit_income_trans,
                                "income_realized_account_status":credit_income_trans,
                                "description":"Transaction failed!. Loan interest payment was not successful",
                                'error':'pd_m05',
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
                    'error':'pd_m06',
                    "wallet_account":debit_trans,
                    "receivable_account":credit_trans}
                ErrorLogger().logError(message)
                return message

        except Exception as error:
            message = {'status':501,
                       'error':'pd_m07',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message 
        
    def charge_demand_note_payment(self, details):
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       'error':'pd_m08', 
                       "status": 402}
            ErrorLogger().logError(message)
            return message

        loan_id = details["loan_id"] 
        charge_name = details["charge_name"] 
        global_id = details["global_id"]
        amount = details["amount"]
        amount = round(amount, 12) 
        wallet_account = details["wallet_account"]
        receivable_account = details["receivable_account"]
        charge_earned_account = details["charge_earned_account"] 
        charge_realized_account = details["charge_realized_account"]        
        payment_date = details["payment_date"]

        #Try except block to handle execute task
        try:
            #Start of transaction posting - Debit Wallet Account with Charge demand note amount paid
            transaction_name = 'Charge payment'
            #if customer langauge is English, get english description 
            description = str(charge_name) + ' loan charge payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 
            layer4_id = UniqueNumber().transactionsdebitcreditId()
            transaction_data = {"global_id":global_id, 
                                "entry_id":loan_id, 
                                "sub_entry_id":'',
                                "type":55,
                                "account_number":wallet_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":payment_date,
                                "layer4_id":layer4_id

                                }
            
            #Debit wallet account with demand note amount paid
            debit_trans = Transaction().debit_on_credit_account(transaction_data)
            #End of transaction posting

            #Start of transaction posting - Credit Customer Receivable Account with Charge demand note amount paid

            transaction_name = 'Charge payment'
            #if customer langauge is English, get english description 
            description = str(charge_name) + ' loan charge payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
            #if customer langauge is Kiswahili, get swahili description 

            transaction_data = {"global_id":global_id, 
                                "entry_id":loan_id, 
                                "sub_entry_id":'',
                                "type":56,
                                "account_number":receivable_account, 
                                "amount":amount, 
                                "transaction_name":transaction_name,
                                "description":description, 
                                "settlement_date":payment_date,
                                "layer4_id":layer4_id
                                }
            
            #Credit Customer Receivable Account with Charge demand note amount paid
            credit_trans = Transaction().credit_on_debit_account(transaction_data)
            #End of transaction posting

            if ((int(debit_trans["status"]) == 200) and (int(credit_trans["status"]) == 200)):

                #Start of transaction posting - Debit Charge Income Earned Account with Charge demand note amount paid

                transaction_name = 'Charge payment'
                #if customer langauge is English, get english description 
                description = str(charge_name) + ' loan charge payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
                #if customer langauge is Kiswahili, get swahili description 

                layer4_id = UniqueNumber().transactionsdebitcreditId()
                transaction_data = {"global_id":global_id, 
                                    "entry_id":loan_id, 
                                    "sub_entry_id":'',
                                    "type":57,
                                    "account_number":charge_earned_account, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":payment_date,
                                    "layer4_id":layer4_id
                                    }
                
                #Debit Charge income earned account with demand note amount paid
                debit_income_trans = Transaction().debit_on_credit_account(transaction_data)
                #End of transaction posting

                #Start of transaction posting - Credit Customer Receivable Account with Charge demand note amount paid

                transaction_name = 'Charge payment'
                #if customer langauge is English, get english description 
                description = str(charge_name) + ' loan charge payment of Kes ' + str(amount) + ". Loan reference number is " + loan_id
                #if customer langauge is Kiswahili, get swahili description 

                transaction_data = {"global_id":global_id, 
                                    "entry_id":loan_id, 
                                    "sub_entry_id":'',
                                    "type":58,
                                    "account_number":charge_realized_account, 
                                    "amount":amount, 
                                    "transaction_name":transaction_name,
                                    "description":description, 
                                    "settlement_date":payment_date,
                                    "layer4_id":layer4_id
                                    }
                
                #Credit Customer Receivable Account with Charge demand note amount paid
                credit_income_trans = Transaction().credit_on_credit_account(transaction_data)
                #End of transaction posting

                if ((int(debit_income_trans["status"]) == 200) and (int(credit_income_trans["status"]) == 200)):
            
                    message = {
                            "wallet_account_status":debit_trans,
                            "receivable_account_status":credit_trans,
                            "income_earned_account_status":debit_income_trans,
                            "income_realized_account_status":credit_income_trans,
                            "description":"Loan charge payment was received successfully",
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
                            rollback_debit_income_trans = Transaction().debit_on_credit_account_rollback(data)
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
                                "wallet_account_status":debit_trans,
                                "receivable_account_status":credit_trans,
                                "income_earned_account_status":debit_income_trans,
                                "income_realized_account_status":credit_income_trans,
                                'error':'pd_m09',
                                "description":"Transaction failed!. Loan charge payment was not successful",
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
                    'error':'pd_m10',
                    "wallet_account":debit_trans,
                    "receivable_account":credit_trans}
                ErrorLogger().logError(message)
                return message


        except Exception as error:
            message = {'status':501,
                       'error':'pd_m11',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message)
            return message