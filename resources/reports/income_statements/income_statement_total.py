from flask import request, Response,jsonify, json
from main import mysql,app
import uuid
from decimal import Decimal
from datetime import datetime

class IncomeStatement(): 

    def get_profit_loss_balance(self, user, details):        
         # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)

         #Try except block to handle data extraction
        try:            
            
            #Get income and expenses accounts         
            income = 14
            cog = 15

            expenses = 16
            other_income = 17
            other_expenses = 18

            total_income = 0
            total_expenses = 0
            
            total_income = float(total_income)          

            total_expenses = float(total_expenses)
            status = details['status']

            
            #Get total income Balance
            cur.execute("""SELECT sum(balance) totalincome FROM accounts WHERE status = %s AND type = %s or type = %s ORDER BY id ASC""", ([status, income, other_income]))
            totalincome = cur.fetchone()
            if totalincome:
               total_income = float(totalincome['totalincome'])
            else:
                total_income = 0

            #Get total expenses Balance
            cur.execute("""SELECT sum(balance) totalexpenses FROM accounts WHERE status = %s AND type = %s or type = %s or type = %s ORDER BY id ASC""", ([status, cog, expenses, other_expenses]))
            totalexpenses = cur.fetchone()
            if totalexpenses:            
               total_expenses = float(totalexpenses['totalexpenses'])
            else:
                total_expenses = 0
            
            net_income = total_income - total_expenses

            res = {"net_income": net_income}
            
            #The response object
            message = {'status':200,
                       'response':res,
                       'description':'Income statement balance was found!'}

            return message

        except Exception as error:
            message = {'status':501,
                       'description':'Failed to fetch income statement balance. {}'.format(error)}
            return message
        finally:
            cur.close()