from flask import request, Response,jsonify, json
from main import mysql,app
import uuid
from decimal import Decimal
from datetime import datetime

class RevenueReports():    

    def get_revenue_accounts(self, user, details):
           # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)

         #Try except block to handle data extraction
        try:                        
            #Get revenue accounts            
            income = 14

            total_revenue_accounts = []
            revenue_data = []

            status = details['status']

            #Get total asset Balance
            cur.execute("""SELECT sum(balance) totalrevenue FROM accounts WHERE status = %s AND type = %s ORDER BY id ASC""", [status, income])
            totalrevenue = cur.fetchone()

            total_revenue = float(totalrevenue['totalrevenue'])

            cur.execute("""SELECT id, reference_no, number, name, balance FROM accounts WHERE status = %s AND type = %s ORDER BY id ASC""", [status, income])
            revenues = cur.fetchall()

            revenue_accounts = []
            for revenue in revenues:
                balance = float(revenue['balance']) 
                res = {
                     "accountid": revenue['id'],
                     "accountref": revenue['reference_no'],
                     "accountnumber": revenue['number'],
                     "accountname": revenue['name'],
                     "balance": balance                                 

                }
                revenue_accounts.append(res)
                
            total_revenue_value = {"totalrevenue":total_revenue}
            total_revenue_accounts.append(total_revenue_value)

            revenue_data.append(revenue_accounts)
            revenue_data.append(total_revenue_accounts)

            
            #The response object
            message = {'status':200,
                       'response':revenue_data,
                       'description':'Revenue accounts were fetched successfully'}

            return message

        except Exception as error:
            message = {'status':501,
                       'description':'Failed to fetch revenue accounts records. {}'.format(error)}
            return message
        finally:
            cur.close()

    