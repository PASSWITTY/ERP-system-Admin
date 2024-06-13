from flask import request, Response,jsonify, json
from main import mysql,app
from decimal import Decimal
from datetime import datetime

class OtherIncomeReports():    

    def get_other_income_accounts(self, user, details):
           # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)

         #Try except block to handle data extraction
        try:                        
            #Get other income accounts            
            other_income = 24

            total_otherincome_accounts = []
            otherincome_data = []

            status = details['status']

            #Get total other_income Balance
            cur.execute("""SELECT sum(balance) totalotherincome FROM accounts WHERE status = %s AND type = %s ORDER BY id ASC""", [status, other_income])
            totalotherincome = cur.fetchone()

            total_otherincome = float(totalotherincome['totalotherincome'])

            cur.execute("""SELECT id, reference_no, number, name, balance FROM accounts WHERE status = %s AND type = %s ORDER BY id ASC""", [status, other_income])
            otherincomes = cur.fetchall()

            otherincome_accounts = []
            for otherincome in otherincomes:
                balance = float(otherincome['balance']) 
                res = {
                     "accountid": otherincome['id'],
                     "accountref": otherincome['reference_no'],
                     "accountnumber": otherincome['number'],
                     "accountname": otherincome['name'],
                     "balance": balance                    

                }
                otherincome_accounts.append(res)
                
            total_otherincome_value = {"totalotherincome":total_otherincome}
            total_otherincome_accounts.append(total_otherincome_value)

            otherincome_data.append(otherincome_accounts)
            otherincome_data.append(total_otherincome_accounts)

            
            #The response object
            message = {'status':200,
                       'response':otherincome_data,
                       'description':'Other income accounts were fetched successfully'}

            return message

        except Exception as error:
            message = {'status':501,
                       'description':'Failed to fetch other income accounts records. {}'.format(error)}
            return message
        finally:
            cur.close()

    