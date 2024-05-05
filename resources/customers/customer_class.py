from flask import request, Response, json, jsonify
import os
from main import mysql, app
from datetime import datetime
from resources.payload.payload import Localtime
from resources.logs.logger import ErrorLogger


class CustomersClass():
    def individual_credit_taken(self, details):
        if details == None:
            message = {'status':402,
                        'error':'us_s30',
                        'description':'Request data is missing some details!'}

            ErrorLogger().logError(message)
            return message
        
        customer_id = details["customer_id"]
        
        #Establish database connection
        try:
            cur =  mysql.get_db().cursor()

        except mysql.get_db().Error as error:

            message = {'status':500,
                       'error':'us_s31',
                       'description':"Couldn't connect to the Database!" + format(error)}
            ErrorLogger().logError(message)
            return message
        
        try:
    
            try:
                cur.execute("""SELECT (SUM(principal_amount_due)) as principal_amount_due FROM loans WHERE customer_id = %s AND product_class = 1 AND principal_amount_due > 0 AND status =1 """, [customer_id])
                loan_due = cur.fetchone()
                if loan_due:
                    loan_principal_amount_due = float(loan_due["principal_amount_due"])
                else:
                    loan_principal_amount_due = 0
                
                credit_taken = loan_principal_amount_due 
            except:
                credit_taken = 0
                
            
            response = {"credit_taken":credit_taken}
            return response
                
        except Exception as error:
            message = {'status':501,
                       'error':'us_s31',
                       'description':'System error! Error description '+ format(error)}
            ErrorLogger().logError(message)
            return message
        finally:
            cur.close()
    
    def group_credit_taken(self, details):
        if details == None:
            message = {'status':402,
                        'error':'us_s30',
                        'description':'Request data is missing some details!'}

            ErrorLogger().logError(message)
            return message
        
        customer_id = details["customer_id"]
        
        #Establish database connection
        try:
            cur =  mysql.get_db().cursor()

        except mysql.get_db().Error as error:

            message = {'status':500,
                       'error':'us_s31',
                       'description':"Couldn't connect to the Database!" + format(error)}
            ErrorLogger().logError(message)
            return message
        
        try:
    
            try:
                cur.execute("""SELECT (SUM(principal_amount_due)) as principal_amount_due FROM loans WHERE customer_id = %s AND product_class = 2 AND principal_amount_due > 0 AND status =1 """, [customer_id])
                loan_due = cur.fetchone()
                if loan_due:
                    loan_principal_amount_due = float(loan_due["principal_amount_due"])
                else:
                    loan_principal_amount_due = 0
                
                credit_taken = loan_principal_amount_due 
            except:
                credit_taken = 0
                
            
            response = {"credit_taken":credit_taken}
            return response
                
        except Exception as error:
            message = {'status':501,
                       'error':'us_s31',
                       'description':'System error! Error description '+ format(error)}
            ErrorLogger().logError(message)
            return message
        finally:
            cur.close()
            
    def individual_total_loans_due(self, details):
        if details == None:
            message = {'status':402,
                       'error':'us_s17',
                       'description':'Request data is missing some details!'}

            ErrorLogger().logError(message)
            return message
        
        customer_id = details["customer_id"]
        
        #Establish database connection
        try:
            cur =  mysql.get_db().cursor()

        except mysql.get_db().Error as error:

            message = {'status':500,
                       'error':'us_s18',
                       'description':"Couldn't connect to the Database!" + format(error)}
            ErrorLogger().logError(message)
            return message
        
        try:
                        
            try:
                localtime = Localtime().gettime()  
                now = datetime.strptime(localtime, '%Y-%m-%d %H:%M:%S')
                now = now.strftime('%Y-%m-%d')
                
                cur.execute("""SELECT (SUM(amount_due)) as amount_due FROM loan_demand_notes As d INNER JOIN loans As l ON d.loan_id = l.id WHERE l.status = 1 AND d.customer_id = %s AND l.product_class = 1 AND d.amount_due > 0 AND date(d.expected_payment_date) < %s AND d.status =1 """, (customer_id, now))
                sum_overdue_demand_notes = cur.fetchone()
                if sum_overdue_demand_notes:
                    total_overdue_demand_notes = float(sum_overdue_demand_notes["amount_due"])
                else:
                    total_overdue_demand_notes = 0
            except:
                total_overdue_demand_notes = 0
                
            try:
                cur.execute("""SELECT (SUM(amount_due)) as amount_due FROM loan_rollover_fee_demand_note_details As r INNER JOIN loans As l ON r.loan_id = l.id WHERE l.status = 1 AND r.customer_id = %s AND l.product_class = 1 AND r.amount_due > 0 AND r.status =1 """, [customer_id])
                sum_overdue_rollover = cur.fetchone()
                if sum_overdue_rollover:
                    total_overdue_rollover = float(sum_overdue_rollover["amount_due"])
                else:
                    total_overdue_rollover = 0
            except:
                total_overdue_rollover = 0
            
            try:
                cur.execute("""SELECT (SUM(amount_due)) as amount_due FROM loan_defaulted_fines_demand_note_details As d INNER JOIN loan As l ON d.loan_id = l.id WHERE l.status = 1 AND d.customer_id = %s AND l.product_class = 1 AND a.amount_due > 0 AND d.status =1 """, [customer_id])
                sum_overdue_defaultedloan_fines = cur.fetchone()
                if sum_overdue_defaultedloan_fines:
                    total_overdue_defaultedloan_fines = float(sum_overdue_defaultedloan_fines["amount_due"])
                else:
                    total_overdue_defaultedloan_fines = 0
            except:
                total_overdue_defaultedloan_fines = 0
                
            totalloans = total_overdue_demand_notes + total_overdue_rollover + total_overdue_defaultedloan_fines
                        
            response = {"totalloans_due":totalloans}
            return response
                
        except Exception as error:
            message = {'status':501,
                       'description':'System error! Error description '+ format(error)}
            return message
        finally:
            cur.close()
            
    def group_total_loans_due(self, details):
        if details == None:
            message = {'status':402,
                       'error':'us_s17',
                       'description':'Request data is missing some details!'}

            ErrorLogger().logError(message)
            return message
        
        customer_id = details["customer_id"]
        group_id = details["group_id"]
        
        #Establish database connection
        try:
            cur =  mysql.get_db().cursor()

        except mysql.get_db().Error as error:

            message = {'status':500,
                       'error':'us_s18',
                       'description':"Couldn't connect to the Database!" + format(error)}
            ErrorLogger().logError(message)
            return message
        
        try:
                        
            try:
                localtime = Localtime().gettime()  
                now = datetime.strptime(localtime, '%Y-%m-%d %H:%M:%S')
                now = now.strftime('%Y-%m-%d')
                
                cur.execute("""SELECT (SUM(amount_due)) as amount_due FROM loan_demand_notes As d INNER JOIN loans As l ON d.loan_id = l.id WHERE l.status = 1 AND d.customer_id = %s AND l.group_id = %s AND l.product_class = 2 AND d.amount_due > 0 AND date(d.expected_payment_date) < %s AND d.status =1 """, (customer_id, group_id, now))
                sum_overdue_demand_notes = cur.fetchone()
                if sum_overdue_demand_notes:
                    total_overdue_demand_notes = float(sum_overdue_demand_notes["amount_due"])
                else:
                    total_overdue_demand_notes = 0
            except:
                total_overdue_demand_notes = 0
                
            try:
                cur.execute("""SELECT (SUM(amount_due)) as amount_due FROM loan_rollover_fee_demand_note_details As r INNER JOIN loans As l ON r.loan_id = l.id WHERE l.status = 1 AND r.customer_id = %s AND l.group_id = %s AND l.product_class = 2 AND r.amount_due > 0 AND r.status =1 """, [customer_id, group_id])
                sum_overdue_rollover = cur.fetchone()
                if sum_overdue_rollover:
                    total_overdue_rollover = float(sum_overdue_rollover["amount_due"])
                else:
                    total_overdue_rollover = 0
            except:
                total_overdue_rollover = 0
            
            try:
                cur.execute("""SELECT (SUM(amount_due)) as amount_due FROM loan_defaulted_fines_demand_note_details As d INNER JOIN loan As l ON d.loan_id = l.id WHERE l.status = 1 AND d.customer_id = %s AND l.group_id = %s AND l.product_class = 2 AND a.amount_due > 0 AND d.status =1 """, [customer_id, group_id])
                sum_overdue_defaultedloan_fines = cur.fetchone()
                if sum_overdue_defaultedloan_fines:
                    total_overdue_defaultedloan_fines = float(sum_overdue_defaultedloan_fines["amount_due"])
                else:
                    total_overdue_defaultedloan_fines = 0
            except:
                total_overdue_defaultedloan_fines = 0
                
            totalloans = total_overdue_demand_notes + total_overdue_rollover + total_overdue_defaultedloan_fines
                        
            response = {"totalloans_due":totalloans}
            return response
                
        except Exception as error:
            message = {'status':501,
                       'description':'System error! Error description '+ format(error)}
            return message
        finally:
            cur.close()
    
    def immature_individual_loan_amount(self, details):
        if details == None:
            message = {'status':402,
                       'error':'us_s17',
                       'description':'Request data is missing some details!'}

            ErrorLogger().logError(message)
            return message
        
        customer_id = details["customer_id"]
        
        #Establish database connection
        try:
            cur =  mysql.get_db().cursor()

        except mysql.get_db().Error as error:

            message = {'status':500,
                       'error':'us_s18',
                       'description':"Couldn't connect to the Database!" + format(error)}
            ErrorLogger().logError(message)
            return message
        
        try:
            
            try:
                # totalloans_pending_maturity = 0
                cur.execute("""SELECT (SUM(outstanding_principal_demandnote_amount)) as outstanding_principal_demandnote_amount,
                                    (SUM(outstanding_interest_demandnote_amount)) as outstanding_interest_demandnote_amount,
                                    (SUM(outstanding_charge_demandnote_amount)) as outstanding_charge_demandnote_amount
                                    FROM loans WHERE customer_id = %s AND product_class = 1 AND (outstanding_principal_demandnote_amount > 0 OR outstanding_interest_demandnote_amount > 0 OR outstanding_charge_demandnote_amount >0) AND status =1""", [customer_id])
                loan_pending_maturity = cur.fetchone()
                if loan_pending_maturity:
                    pending_maturity_principal_amount_due = float(loan_pending_maturity["outstanding_principal_demandnote_amount"])
                    pending_maturity_interest_amount_due = float(loan_pending_maturity["outstanding_interest_demandnote_amount"])
                    pending_maturity_charge_amount_due = float(loan_pending_maturity["outstanding_charge_demandnote_amount"])
                else:
                    pending_maturity_principal_amount_due = 0
                    pending_maturity_interest_amount_due = 0
                    pending_maturity_charge_amount_due = 0
            
            except:
                pending_maturity_principal_amount_due = 0
                pending_maturity_interest_amount_due = 0
                pending_maturity_charge_amount_due = 0
           
            try:
                localtime = Localtime().gettime()  
                now = datetime.strptime(localtime, '%Y-%m-%d %H:%M:%S')
                now = now.strftime('%Y-%m-%d')
                cur.execute("""SELECT (SUM(amount_due)) as amount_due FROM loan_demand_notes WHERE customer_id = %s AND amount_due > 0 AND status =1 AND date(expected_payment_date) >= %s""", (customer_id, now))
                sum_notoverdue_demand_notes = cur.fetchone()
                if sum_notoverdue_demand_notes:
                    total_notoverdue_demand_notes = float(sum_notoverdue_demand_notes["amount_due"])
                else:
                    total_notoverdue_demand_notes = 0
            except:
                total_notoverdue_demand_notes = 0
         
            
            totalloans_pending_maturity = pending_maturity_principal_amount_due + pending_maturity_interest_amount_due + pending_maturity_charge_amount_due + total_notoverdue_demand_notes
            

            message = {'status':200,
                       "totalloans_pending_maturity":totalloans_pending_maturity,                       
                       'description':"Ongoing loan balance was found"}
            
            return message
                
        except Exception as error:
            message = {'status':501,
                       'description':'System error! Error description '+ format(error)}
            return message
        finally:
            cur.close()
           
    def immature_group_loan_amount(self, details):
        if details == None:
            message = {'status':402,
                       'error':'us_s17',
                       'description':'Request data is missing some details!'}

            ErrorLogger().logError(message)
            return message
        
        customer_id = details["customer_id"]
        
        #Establish database connection
        try:
            cur =  mysql.get_db().cursor()

        except mysql.get_db().Error as error:

            message = {'status':500,
                       'error':'us_s18',
                       'description':"Couldn't connect to the Database!" + format(error)}
            ErrorLogger().logError(message)
            return message
        
        try:
            
            try:
                # totalloans_pending_maturity = 0
                cur.execute("""SELECT (SUM(outstanding_principal_demandnote_amount)) as outstanding_principal_demandnote_amount,
                                    (SUM(outstanding_interest_demandnote_amount)) as outstanding_interest_demandnote_amount,
                                    (SUM(outstanding_charge_demandnote_amount)) as outstanding_charge_demandnote_amount
                                    FROM loans WHERE customer_id = %s AND product_class = 2 AND (outstanding_principal_demandnote_amount > 0 OR outstanding_interest_demandnote_amount > 0 OR outstanding_charge_demandnote_amount >0) AND status =1""", [customer_id])
                loan_pending_maturity = cur.fetchone()
                if loan_pending_maturity:
                    pending_maturity_principal_amount_due = float(loan_pending_maturity["outstanding_principal_demandnote_amount"])
                    pending_maturity_interest_amount_due = float(loan_pending_maturity["outstanding_interest_demandnote_amount"])
                    pending_maturity_charge_amount_due = float(loan_pending_maturity["outstanding_charge_demandnote_amount"])
                else:
                    pending_maturity_principal_amount_due = 0
                    pending_maturity_interest_amount_due = 0
                    pending_maturity_charge_amount_due = 0
            
            except:
                pending_maturity_principal_amount_due = 0
                pending_maturity_interest_amount_due = 0
                pending_maturity_charge_amount_due = 0
           
            try:
                localtime = Localtime().gettime()  
                now = datetime.strptime(localtime, '%Y-%m-%d %H:%M:%S')
                now = now.strftime('%Y-%m-%d')
                cur.execute("""SELECT (SUM(amount_due)) as amount_due FROM loan_demand_notes As d INNER JOIN loans As l ON d.loan_id = l.id WHERE d.customer_id = %s AND d.amount_due > 0 AND d.status =1 AND date(d.expected_payment_date) >= %s AND l.product_class = 2 AND l.status =1""", (customer_id, now))
                sum_notoverdue_demand_notes = cur.fetchone()
                if sum_notoverdue_demand_notes:
                    total_notoverdue_demand_notes = float(sum_notoverdue_demand_notes["amount_due"])
                else:
                    total_notoverdue_demand_notes = 0
            except:
                total_notoverdue_demand_notes = 0
         
            
            totalloans_pending_maturity = pending_maturity_principal_amount_due + pending_maturity_interest_amount_due + pending_maturity_charge_amount_due + total_notoverdue_demand_notes
            

            message = {'status':200,
                       "totalloans_pending_maturity":totalloans_pending_maturity,                       
                       'description':"Ongoing loan balance was found"}
            
            return message
                
        except Exception as error:
            message = {'status':501,
                       'description':'System error! Error description '+ format(error)}
            return message
        finally:
            cur.close()
            
            
    def total_individual_loan_amount(self, details):
        if details == None:
            message = {'status':402,
                       'error':'us_s17',
                       'description':'Request data is missing some details!'}

            ErrorLogger().logError(message)
            return message
        
        customer_id = details["customer_id"]
        
        #Establish database connection
        try:
            cur =  mysql.get_db().cursor()

        except mysql.get_db().Error as error:

            message = {'status':500,
                       'error':'us_s18',
                       'description':"Couldn't connect to the Database!" + format(error)}
            ErrorLogger().logError(message)
            return message
        
        try:
            
            try:
                # total_individual_loans_due
                cur.execute("""SELECT (SUM(principal_amount_due)) as principal_amount_due,
                                          (SUM(interest_amount_due)) as interest_amount_due,
                                          (SUM(charge_amount_due)) as charge_amount_due,
                                          (SUM(rollover_fee_due)) as rollover_fee_due,
                                          (SUM(defaulted_loan_fines_due)) as defaulted_loan_fines_due
                                        FROM loans WHERE customer_id = %s AND product_class = 1 AND (principal_amount_due > 0 OR interest_amount_due > 0 OR charge_amount_due >0 OR rollover_fee_due >0 OR defaulted_loan_fines_due >0) AND status =1""", [customer_id])
                loans_due = cur.fetchone()
                
                if loans_due:
                        individual_principal_amount_due = float(loans_due["principal_amount_due"])
                        individual_interest_amount_due = float(loans_due["interest_amount_due"])
                        individual_charge_amount_due = float(loans_due["charge_amount_due"])
                        individual_rollover_fee_due = float(loans_due["rollover_fee_due"])
                        individual_defaulted_loan_fines_due = float(loans_due["defaulted_loan_fines_due"])
                else:
                        individual_principal_amount_due = 0
                        individual_interest_amount_due = 0
                        individual_charge_amount_due = 0
                        individual_rollover_fee_due = 0
                        individual_defaulted_loan_fines_due = 0
            
            except:
                individual_principal_amount_due = 0
                individual_interest_amount_due = 0
                individual_charge_amount_due = 0
                individual_rollover_fee_due = 0
                individual_defaulted_loan_fines_due = 0
           
            total_individual_loans_due = individual_principal_amount_due + individual_interest_amount_due + individual_charge_amount_due + individual_rollover_fee_due + individual_defaulted_loan_fines_due

            message = {'status':200,
                       "total_individual_loans_due":total_individual_loans_due,                       
                       'description':"Individual total loan balance was found"}
            
            return message
                
        except Exception as error:
            message = {'status':501,
                       'description':'System error! Error description '+ format(error)}
            return message
        finally:
            cur.close()
            
    def total_group_loan_amount(self, details):
        if details == None:
            message = {'status':402,
                       'error':'us_s17',
                       'description':'Request data is missing some details!'}

            ErrorLogger().logError(message)
            return message
        
        customer_id = details["customer_id"]
        
        #Establish database connection
        try:
            cur =  mysql.get_db().cursor()

        except mysql.get_db().Error as error:

            message = {'status':500,
                       'error':'us_s18',
                       'description':"Couldn't connect to the Database!" + format(error)}
            ErrorLogger().logError(message)
            return message
        
        try:
            
            try:
                # total_individual_loans_due
                cur.execute("""SELECT (SUM(principal_amount_due)) as principal_amount_due,
                                          (SUM(interest_amount_due)) as interest_amount_due,
                                          (SUM(charge_amount_due)) as charge_amount_due,
                                          (SUM(rollover_fee_due)) as rollover_fee_due,
                                          (SUM(defaulted_loan_fines_due)) as defaulted_loan_fines_due
                                        FROM loans WHERE customer_id = %s AND product_class = 2 AND (principal_amount_due > 0 OR interest_amount_due > 0 OR charge_amount_due >0 OR rollover_fee_due >0 OR defaulted_loan_fines_due >0) AND status =1""", [customer_id])
                loans_due = cur.fetchone()
                
                if loans_due:
                        group_principal_amount_due = float(loans_due["principal_amount_due"])
                        group_interest_amount_due = float(loans_due["interest_amount_due"])
                        group_charge_amount_due = float(loans_due["charge_amount_due"])
                        group_rollover_fee_due = float(loans_due["rollover_fee_due"])
                        group_defaulted_loan_fines_due = float(loans_due["defaulted_loan_fines_due"])
                else:
                        group_principal_amount_due = 0
                        group_interest_amount_due = 0
                        group_charge_amount_due = 0
                        group_rollover_fee_due = 0
                        group_defaulted_loan_fines_due = 0
            
            except:
                group_principal_amount_due = 0
                group_interest_amount_due = 0
                group_charge_amount_due = 0
                group_rollover_fee_due = 0
                group_defaulted_loan_fines_due = 0
           
            total_group_loans_due = group_principal_amount_due + group_interest_amount_due + group_charge_amount_due + group_rollover_fee_due + group_defaulted_loan_fines_due

            message = {'status':200,
                       "total_group_loans_due":total_group_loans_due,                       
                       'description':"Group total loan balance was found"}
            
            return message
                
        except Exception as error:
            message = {'status':501,
                       'description':'System error! Error description '+ format(error)}
            return message
        finally:
            cur.close()