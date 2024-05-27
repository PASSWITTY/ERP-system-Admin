from flask import request, Response,jsonify, json
from main import mysql,app

class OtherExpensesReports():    

    def get_other_expenses_accounts(self, user, details):
           # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)

         #Try except block to handle data extraction
        try:                        
            #Get other expense accounts            
            other_expense = 18

            total_otherexpense_accounts = []
            otherexpense_data = []

            status = details['status']

            #Get total other_expense Balance
            cur.execute("""SELECT sum(balance) totalotherexpense FROM accounts WHERE status = %s AND type = %s ORDER BY id ASC""", [status, other_expense])
            totalotherexpense = cur.fetchone()

            total_otherexpense = float(totalotherexpense['totalotherexpense'])

            cur.execute("""SELECT id, reference_no, number, name, balance FROM accounts WHERE status = %s AND type = %s ORDER BY id ASC""", [status, other_expense])
            otherexpenses = cur.fetchall()

            otherexpense_accounts = []
            for otherexpense in otherexpenses:
                balance = float(otherexpense['balance']) 
                res = {
                     "accountid": otherexpense['id'],
                     "accountref": otherexpense['reference_no'],
                     "accountnumber": otherexpense['number'],
                     "accountname": otherexpense['name'],
                     "balance": balance                   

                }
                otherexpense_accounts.append(res)
                
            total_otherexpense_value = {"totalotherexpense":total_otherexpense}
            total_otherexpense_accounts.append(total_otherexpense_value)

            otherexpense_data.append(otherexpense_accounts)
            otherexpense_data.append(total_otherexpense_accounts)

            
            #The response object
            message = {'status':200,
                       'response':otherexpense_data,
                       'description':'Other expense accounts were fetched successfully'}

            return message

        except Exception as error:
            message = {'status':501,
                       'description':'Failed to fetch other expense accounts records. {}'.format(error)}
            return message
        finally:
            cur.close()

    