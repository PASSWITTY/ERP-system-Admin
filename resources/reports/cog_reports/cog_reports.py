from flask import request, Response,jsonify, json
from main import mysql,app
import uuid
from decimal import Decimal
from datetime import datetime

class CogReports():    

    def get_cog_accounts(self, user, details):
           # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)

         #Try except block to handle data extraction
        try:                        
            #Get cog accounts            
            cogtype = 21

            total_cog_accounts = []
            cog_data = []

            status = details['status']

            #Get total asset Balance
            cur.execute("""SELECT sum(balance) totalcog FROM accounts WHERE status = %s AND type = %s ORDER BY id ASC""", [status, cogtype])
            totalcog = cur.fetchone()

            total_cog = float(totalcog['totalcog'])

            cur.execute("""SELECT id, reference_no, number, name, balance FROM accounts WHERE status = %s AND type = %s ORDER BY id ASC""", [status, cogtype])
            cogs = cur.fetchall()

            cog_accounts = []
            for cog in cogs:
                balance = float(cog['balance']) 
                res = {
                     "accountid": cog['id'],
                     "accountref": cog['reference_no'],
                     "accountnumber": cog['number'],
                     "accountname": cog['name'],
                     "balance": balance                    

                }
                cog_accounts.append(res)
                
            total_cog_value = {"totalcog":total_cog}
            total_cog_accounts.append(total_cog_value)

            cog_data.append(cog_accounts)
            cog_data.append(total_cog_accounts)

            
            #The response object
            message = {'status':200,
                       'response':cog_data,
                       'description':'Cog accounts were fetched successfully'}

            return message

        except Exception as error:
            message = {'status':501,
                       'description':'Failed to fetch cog accounts records. {}'.format(error)}
            return message
        finally:
            cur.close()

    