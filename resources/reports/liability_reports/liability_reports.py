from flask import request, Response,jsonify, json
from main import mysql

class LiabilityReports():  

    def get_liability_accounts(self, user, details):
               
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)

         #Try except block to handle data extraction
        try:            
            
            #Get liability accounts         
            payable_accs = 9
            shortterm_loan_accs = 11
            longterm_loan_accs = 12
            accrued_expenses = 13
            customer_prepayments = 14
            other_longterm_liabilities = 15
            

            total_liability_accounts = []
            liability_data = []

            status = details['status']

            #Get total income Balance
            cur.execute("""SELECT sum(balance) totalliabilities FROM accounts WHERE status = %s AND balance > 0 AND (type = %s OR type = %s OR type = %s OR type = %s OR type = %s OR type = %s) ORDER BY id ASC""", (status, payable_accs, accrued_expenses, longterm_loan_accs, shortterm_loan_accs, customer_prepayments, other_longterm_liabilities))
            totalliability = cur.fetchone()

            total_liabilities = float(totalliability['totalliabilities'])


            cur.execute("""SELECT id, reference_no, number, name, balance FROM accounts WHERE status = %s AND balance > 0 AND (type = %s OR type = %s OR type = %s OR type = %s OR type = %s OR type = %s) ORDER BY id ASC""", (status, payable_accs, accrued_expenses, longterm_loan_accs, shortterm_loan_accs, customer_prepayments, other_longterm_liabilities))
            liabilities = cur.fetchall()

            liabilities_accounts = []
            for liability in liabilities:
                balance = float(liability['balance']) 
                # balance = round(balance, 2)
                res = {
                    "accountid": liability['id'],
                    "accountref": liability['reference_no'],
                    "accountnumber": liability['number'],
                    "accountname": liability['name'],
                    "balance": balance                    

                }
                liabilities_accounts.append(res)
            
            total_liability_value = {"totalLiability":total_liabilities}

            total_liability_accounts.append(total_liability_value)

            liability_data.append(liabilities_accounts)
            liability_data.append(total_liability_accounts)
            
            #The response object
            message = {'status':200,
                       'response':liability_data,
                       'description':'Liability accounts report details was fetched successfully'}

            return message


        except Exception as error:
            message = {'status':501,
                       'response':[],
                       'description':'Failed to fetch liability accounts records. {}'.format(error)}
            return message
        finally:
            cur.close()