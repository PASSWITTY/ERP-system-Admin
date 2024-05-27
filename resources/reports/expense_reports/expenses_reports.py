from flask import request, Response,jsonify, json
from main import mysql,app
import uuid
from decimal import Decimal
from datetime import datetime

class ExpensesReports():    

    def get_expenses_accounts(self, user, details):
           # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)

         #Try except block to handle data extraction
        try:                        
            #Get expense accounts            
            expensestype = 22 
            taxexpensetype = 25 

            total_expense_accounts = []
            expense_data = []

            status = details['status']

            #Get total asset Balance
            cur.execute("""SELECT sum(balance) totalexpense FROM accounts WHERE status = %s AND (type = %s OR type = %s) ORDER BY id ASC""", [status, expensestype, taxexpensetype])
            totalexpense = cur.fetchone()

            total_expense = float(totalexpense['totalexpense'])

            cur.execute("""SELECT id, reference_no, number, name, balance FROM accounts WHERE status = %s AND (type = %s OR type = %s) ORDER BY id ASC""", [status, expensestype, taxexpensetype])
            expenses = cur.fetchall()

            expense_accounts = []
            for expense in expenses:
                balance = float(expense['balance']) 
                res = {
                     "accountid": expense['id'],
                     "accountref": expense['reference_no'],
                     "accountnumber": expense['number'],
                     "accountname": expense['name'],
                     "balance": balance                 

                }
                expense_accounts.append(res)
                
            total_expense_value = {"totalexpense":total_expense}
            total_expense_accounts.append(total_expense_value)

            expense_data.append(expense_accounts)
            expense_data.append(total_expense_accounts)

            
            #The response object
            message = {'status':200,
                       'response':expense_data,
                       'description':'Expense accounts were fetched successfully'}

            return message

        except Exception as error:
            message = {'status':501,
                       'description':'Failed to fetch expense accounts records. {}'.format(error)}
            return message
        finally:
            cur.close()

    