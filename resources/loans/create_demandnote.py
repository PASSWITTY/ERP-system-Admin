from flask import json, jsonify
from main import mysql
from dateutil.relativedelta import relativedelta    
from datetime import datetime, timedelta
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
from resources.alphanumeric.generate import UniqueNumber
from resources.transactions.transaction import Transaction
from resources.loans.loan_charges import LoanCharges

class CreateDemandNote(): 
    
    #Daemon initiated demand note generation   
    def demand_note_creation(self, details):
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       'error':'cr_d201',
                       "status": 402}
            ErrorLogger().logError(message) 
            return message
        
        loan_id = details["loan_id"]
        global_id = details["global_id"]
        customer_id = details["customer_id"]
        demandnote_id = details["demandnote_id"]
        amount = float(details["amount"])
        amount = round(amount, 12) 
        date_due = details["date_due"]
        start_date = details["start_date"]
        outstanding_installments = int(details["outstanding_installments"])
        total_installments = int(details["total_installments"])
        datecreated = Localtime().gettime()
       
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       'error':'cr_d202',
                       "status": 500}
            ErrorLogger().logError(message) 
            return message

        #Try except block to handle execute task
        try:
            status = 1
            posted = 0
            posting_in_progress = 0
            cur.execute("""INSERT INTO loan_demand_notes (id, global_id, loan_id, customer_id, amount, amount_due, expected_payment_date, start_date, posted, posting_in_progress, date_created, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                              (demandnote_id, global_id, loan_id, customer_id, amount, amount,                  date_due, start_date, posted, posting_in_progress,  datecreated, status))
            mysql.get_db().commit()
          
            if ((total_installments == outstanding_installments) or (total_installments > outstanding_installments)):
                #Update loan item.
                cur.execute("""UPDATE loans set outstanding_installments = outstanding_installments - 1 WHERE id = %s""", (loan_id))
                mysql.get_db().commit()
            
            else:
                pass
            
            message = {"description":"Loan demand note was created successfully",
                       "status":200}
            return message

        except Exception as error:
            message = {"status":501,
                       'error':'cr_d203',
                       "description":"Transaction execution failed. Error description" + format(error)}
            ErrorLogger().logError(message)            
            return message
        finally:
            cur.close() 

    def principal_demand_note_creation(self, details):
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       'error':'cr_d204',
                       "status": 402}
            ErrorLogger().logError(message) 
            return message
       
        loan_id = details["loan_id"]
        customer_id = details["customer_id"]
        global_id = details["global_id"]
        demandnote_id = details["demandnote_id"]
        subdemandnote_id = details["subdemandnote_id"]   
        amount = float(details["amount"])
        amount = round(amount, 12) 
        start_date = details["start_date"]
        date_due = details["date_due"]
        datecreated = Localtime().gettime()
        type ='principal'
        paid = 0

        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       'error':'cr_d205',
                       "status": 500}
            ErrorLogger().logError(message) 
            return message

        #Try except block to handle execute task
        try:
            
            status = 1
            posted = 0
            cur.execute("""INSERT INTO loan_demand_note_details (id, demandnote_id, loan_id, customer_id, global_id, type, amount, amount_paid, amount_due, expected_payment_date, start_date, posted, date_created, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                  (subdemandnote_id, demandnote_id, loan_id, customer_id, global_id, type, amount,        paid,     amount,              date_due, start_date, posted, datecreated, status))
            mysql.get_db().commit()
            
            #Update principal demand notes generated numbers
            cur.execute("""UPDATE loan_demand_notes_generated set principal_demand_notes_pending = principal_demand_notes_pending - 1, principal_demand_notes_processed = principal_demand_notes_processed + 1 WHERE loan_id = %s""", (loan_id))
            mysql.get_db().commit()

            message = {
                    "description":"Loan principal demand note was created successfully",
                    "status":200}
            return message
           
        except Exception as error:
            message = {'status':501,
                       'error':'cr_d207',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 
        finally:
            cur.close()
                        
    def interest_demand_note_creation(self, details):
        if details == None:
            message = {"description":"Transaction is missing some details!", 
                       'error':'cr_d208',
                       "status": 402}
            ErrorLogger().logError(message) 
            return message
     
        loan_id = details["loan_id"]
        customer_id = details["customer_id"]
    
        global_id = details["global_id"]
        demandnote_id = details["demandnote_id"]
        subdemandnote_id = details["subdemandnote_id"]        
        amount = float(details["amount"])
        amount = round(amount, 12) 
        start_date = details["start_date"]
        date_due = details["date_due"]
        datecreated = Localtime().gettime()
        type ='interest'
        paid = 0
        

        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database!", 
                       'error':'cr_d209',
                       "status": 500}
            ErrorLogger().logError(message) 
            return message

        try:
            status = 1     
            posted = 0           
            cur.execute("""INSERT INTO loan_demand_note_details (id, demandnote_id, loan_id, customer_id, global_id, type, amount, amount_paid, amount_due, expected_payment_date, start_date, posted, date_created, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                                  (subdemandnote_id, demandnote_id, loan_id, customer_id, global_id, type, amount,        paid,     amount,              date_due, start_date, posted,  datecreated, status))
            mysql.get_db().commit()
            
            #Update interest demand notes generated numbers
            cur.execute("""UPDATE loan_demand_notes_generated set interest_demand_notes_pending = interest_demand_notes_pending - 1, interest_demand_notes_processed = interest_demand_notes_processed + 1 WHERE loan_id = %s""", (loan_id))
            mysql.get_db().commit()
        
            message = {
                    "description":"Loan interest demand note was created successfully",
                    "status":200}
            return message
            
        except Exception as error:
            message = {'status':501,
                       'error':'cr_d211',
                       'description':'Transaction had an error. Error description ' + format(error)}
            ErrorLogger().logError(message) 
            return message 
        finally:
            cur.close()
            
            
            