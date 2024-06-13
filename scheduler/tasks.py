from flask import request, Response, json, jsonify
from celery import Celery
from daemons_module.daemons_model import Daemons

celery = Celery('tasks', 
             broker='amqp://admin:SecuredPassword@localhost:5672', 
             backend='redis://')


class CronTasks():
    # define the celery task
    
    #Generate all demand notes when a loan has been created
    @celery.task(name='cronjob_queue_demandnote')
    def cronjob_queue_demandnote():
        cron_queue_demandnote = Daemons().daemon_queue_demand_notes()
        
        if int(cron_queue_demandnote["status"]) == 200:
            message = 'status : 200, description : Success - Loan demand notes have been queued!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Loan demand notes were not queued!'       
            print(message) 
        return message
    
    
    @celery.task(name='cronjob_process_demandnote')
    def cronjob_process_demandnote():
        cron_process_demandnote = Daemons().daemon_process_demand_note_queue()
        
        if int(cron_process_demandnote["status"]) == 200:
            message = 'status : 200, description : Success - Loan demand note was generated successfully!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Loan demand note was not generated!'       
            print(message) 
        return message
    

    @celery.task(name='cronjob_post_demandnote')
    def cronjob_post_demandnote():
        cron_post_demandnote = Daemons().daemon_post_demand_note_queue()
        
        if int(cron_post_demandnote["status"]) == 200:
            message = 'status : 200, description : Success - Loan demand note was posted successfully!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Loan demand note was not posted!'       
            print(message) 
        return message
    
    
    @celery.task(name='cronjob_queue_loan_rollover_fee')
    def cronjob_queue_loan_rollover_fee():
        cron_queue_rollover_fee = Daemons().daemon_create_rollover_fee_demandnotes_queue()
        
        if int(cron_queue_rollover_fee["status"]) == 200:
            message = 'status : 200, description : Success - Loans have been queued for rollover fee generation!'
            print(message)

        else:
            message = 'status : 201, description : Failed - No loan was queued for rollover fee generation!'       
            print(message) 
        return message
    
    
    @celery.task(name='cronjob_process_rollover_fee')
    def cronjob_process_rollover_fee():
        cron_process_rollover_fee = Daemons().daemon_process_rollover_fee_demandnotes_queue()
        
        if int(cron_process_rollover_fee["status"]) == 200:
            message = 'status : 200, description : Success - Loan rollover fee was applied successfully!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Loan rollover fee was not applied!'       
            print(message) 
        return message
    
    
    @celery.task(name='cronjob_queue_defaulted_loan_fines')
    def cronjob_queue_defaulted_loan_fines():
        cron_queue_defaulted_loan_fines = Daemons().daemon_create_defaulted_loan_fines_demandnotes_queue()
        
        if int(cron_queue_defaulted_loan_fines["status"]) == 200:
            message = 'status : 200, description : Success - Defaulted loan fines were queued successfully!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Defaulted loan fines were not queued!'       
            print(message) 
        return message
    
    
    @celery.task(name='cronjob_process_defaulted_loan_fines')
    def cronjob_process_defaulted_loan_fines():
        cron_process_defaulted_loan_fines = Daemons().daemon_process_defaulted_loan_fines_demandnotes_queue()
        
        if int(cron_process_defaulted_loan_fines["status"]) == 200:
            message = 'status : 200, description : Success - Defaulted loan fines demand note was generated successfully!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Defaulted loan fines demand note was not generated!'       
            print(message) 
        return message
    
        
    #Get Mpesa Balance
    @celery.task(name='cronjob_process_get_mpesa_b2c_balance')
    def cronjob_process_get_mpesa_b2c_balance():
        cron_process_get_mpesa_b2c_balance = Daemons().get_mpesa_b2c_balance()

        if int(cron_process_get_mpesa_b2c_balance["status"]) == 200:
            message = 'status : 200, description : Success - Mpesa B2C balance was fetched successfully!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Mpesa B2C balance fetch failed!'       
            print(message) 
        message = 'status : 201, description : Failed - Mpesa B2C balance fetch failed!' 
        return message
    
    
    #Get Airtime Balance
    @celery.task(name='cronjob_process_get_airtime_Wallet_balance')
    def cronjob_process_get_airtime_Wallet_balance():
        cron_process_get_airtime_Wallet_balance = Daemons().get_airtime_wallet_balance()

        if int(cron_process_get_airtime_Wallet_balance["status"]) == 200:
            message = 'status : 200, description : Success - Airtime wallet balance was fetched successfully!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Airtime Wallet balance fetch failed!'       
            print(message) 
        message = 'status : 201, description : Failed - Airtime Wallet balance fetch failed!' 
        return message
    
    
    #Send SMS Remainder
    @celery.task(name='cronjob_process_loan_payment_remainder_sms')
    def cronjob_process_loan_payment_remainder_sms():
        cron_process_loan_payment_remainder_sms = Daemons().generate_loan_payment_remainder_sms()

        if int(cron_process_loan_payment_remainder_sms["status"]) == 200:
            message = 'status : 200, description : Success - Loan payment remainder sms was generated successfully!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Loan payment remainder sms not generated!'       
            print(message) 
        message = 'status : 201, description : Failed - No loan payment remainder sms was generated!' 
        return message
    
    #Send SMS for Loan Repayment Remainder
    @celery.task(name='cronjob_process_send_loan_payment_remainder_sms')
    def cronjob_process_send_loan_payment_remainder_sms():
        cron_process_send_loan_payment_remainder_sms = Daemons().send_loan_payment_remainder_sms()

        if int(cron_process_send_loan_payment_remainder_sms["status"]) == 200:
            message = 'status : 200, description : Success - loan payment remainder sms was send successfully!'
            print(message)

        else:
            message = 'status : 201, description : Failed - loan payment remainder sms was not send!'       
            print(message) 
        message = 'status : 201, description : Failed - No loan payment remainder sms was not send!' 
        return message
    
    #Send SMS for Loan Repayment Remainder
    @celery.task(name='cronjob_process_send_reducing_balance_loan_payment_remainder_sms')
    def cronjob_process_send_reducing_balance_loan_payment_remainder_sms():
        cron_process_send_reducing_balance_loan_payment_remainder_sms = Daemons().send_reducing_balance_loan_payment_remainder_sms()

        if int(cron_process_send_reducing_balance_loan_payment_remainder_sms["status"]) == 200:
            message = 'status : 200, description : Success - group loan payment remainder sms was send successfully!'
            print(message)

        else:
            message = 'status : 201, description : Failed - loan payment remainder sms was not send!'       
            print(message) 
        message = 'status : 201, description : Failed - No loan payment remainder sms was not send!' 
        return message
    
    #Send SMS for Loan Repayment Remainder
    @celery.task(name='cronjob_process_loan_payment_remainder_eveduedate_sms')
    def cronjob_process_loan_payment_remainder_eveduedate_sms():
        cron_process_loan_payment_remainder_eveduedate_sms = Daemons().generate_loan_payment_remainder_eveduedate_sms()

        if int(cron_process_loan_payment_remainder_eveduedate_sms["status"]) == 200:
            message = 'status : 200, description : Success - Loan payment remainder on duedate eve sms was generated successfully!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Loan payment remainder sms on duedate eve not generated!'       
            print(message) 
        message = 'status : 201, description : Failed - No loan payment remainder sms on duedate eve was generated!' 
        return message

    #Create Okoa Airtime Loan
    @celery.task(name='cronjob_process_create_okoa_airtime_loan')
    def cronjob_process_create_okoa_airtime_loan():
        cron_process_create_okoa_airtime_loan = Daemons().create_okoa_airtime_loan()

        if int(cron_process_create_okoa_airtime_loan["status"]) == 200:
            message = 'status : 200, description : Success - Okoa Airtime loan was generated successfully!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Okoa Airtime loan was not generated!'       
            print(message) 
        message = 'status : 201, description : Failed - No Okoa Airtime loan was generated!' 
        return message
    
    #Pay defaulted fines using wallet
    @celery.task(name='cronjob_process_loan_defaulted_fines_repayment_using_wallet_balance')
    def cronjob_process_loan_defaulted_fines_repayment_using_wallet_balance():
        cron_process_loan_defaulted_fines_repayment_using_wallet_balance = Daemons().loan_defaulted_fines_repayment_using_wallet_balance()

        if int(cron_process_loan_defaulted_fines_repayment_using_wallet_balance["status"]) == 200:
            message = 'status : 200, description : Success - Loan defaulted fine was repaid successfully using wallet balance!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Loan defaulted fine repayment using wallet balance failed!'       
            print(message) 
        message = 'status : 201, description : Failed - No Loan defaulted fine was repaid using wallet balance!' 
        return message
    
    #Pay rollover fines using wallet
    @celery.task(name='cronjob_process_loan_rollover_fee_repayment_using_wallet_balance')
    def cronjob_process_loan_rollover_fee_repayment_using_wallet_balance():
        cron_process_loan_rollover_fee_repayment_using_wallet_balance = Daemons().loan_rollover_fee_repayment_using_wallet_balance()

        if int(cron_process_loan_rollover_fee_repayment_using_wallet_balance["status"]) == 200:
            message = 'status : 200, description : Success - Loan rollover fee was repaid successfully using wallet balance!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Loan rollover fee repayment using wallet balance failed!'       
            print(message) 
        message = 'status : 201, description : Failed - No Loan rollover fee was repaid using wallet balance!' 
        return message
    
    #Pay demand notes using wallet
    @celery.task(name='cronjob_process_loan_demandnote_repayment_using_wallet_balance')
    def cronjob_process_loan_demandnote_repayment_using_wallet_balance():
        cron_process_loan_demandnote_repayment_using_wallet_balance = Daemons().loan_demand_note_repayment_using_wallet_balance()

        if int(cron_process_loan_demandnote_repayment_using_wallet_balance["status"]) == 200:
            message = 'status : 200, description : Success - Loan demand note was repaid successfully using wallet balance!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Loan demand note repayment using wallet balance failed!'       
            print(message) 
        message = 'status : 201, description : Failed - No Loan demand note was repaid using wallet balance!' 
        return message
    
    #Pay loans using wallet
    @celery.task(name='cronjob_process_loan_repayment_using_wallet_balance')
    def cronjob_process_loan_repayment_using_wallet_balance():
        cron_process_loan_repayment_using_wallet_balance = Daemons().loan_repayment_using_wallet_balance()

        if int(cron_process_loan_repayment_using_wallet_balance["status"]) == 200:
            message = 'status : 200, description : Success - Group Loan repayment using wallet balance was processed successfully!'
            print(message)

        else:
            message = 'status : 201, description : Failed - Group Loan repayment using wallet balance failed!'       
            print(message) 
        message = 'status : 201, description : Failed - No Group Loan repayment was processed!' 
        return message