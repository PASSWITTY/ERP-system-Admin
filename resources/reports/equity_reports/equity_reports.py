from flask import request, Response,jsonify, json
from main import mysql,app
import uuid
from decimal import Decimal
from datetime import datetime

class EquityReports(): 


    def get_equity_accounts(self, user, details):
        # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)

         #Try except block to handle data extraction
        try:         
            
            #Get accounts         
            equity = 16
            retained_earnings = 16
            total_equity_accounts = []
            equity_data = []
            status = details['status']

            #Get total equity Balance
            cur.execute("""SELECT sum(balance) totalequity FROM accounts WHERE status = %s AND (type = %s OR type = %s) ORDER BY id ASC""", [status, equity, retained_earnings])
            totalequity = cur.fetchone()

            total_equity = float(totalequity['totalequity'])

            cur.execute("""SELECT id, reference_no, number, name, balance FROM accounts WHERE status = %s AND (type = %s OR type = %s) ORDER BY id ASC""", [status, equity, retained_earnings])
            equities = cur.fetchall()

            equity_accounts = []
            for equity in equities:
                balance = float(equity['balance']) 
                res = {
                     "accountid": equity['id'],
                     "accountref": equity['reference_no'],
                     "accountnumber": equity['number'],
                     "accountname": equity['name'],
                     "balance": balance              

                }
                equity_accounts.append(res)
            
            total_equity_value = {"totalEquity":total_equity}

            total_equity_accounts.append(total_equity_value)
            equity_data.append(equity_accounts)
            equity_data.append(total_equity_accounts)
            
            message = {'status':200,
                       'response':equity_data,
                       'description':'Equity accounts details were fetched successfully'}

            return message

        except Exception as error:
            message = {'status':501,
                       'description':'Failed to fetch equity accounts records. {}'.format(error)}
            return message
        finally:
            cur.close()