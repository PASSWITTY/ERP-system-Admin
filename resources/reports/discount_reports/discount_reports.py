from flask import request, Response,jsonify, json
from main import mysql,app
import uuid
from decimal import Decimal
from datetime import datetime

class DiscountReports():    

    def get_discount_accounts(self, user, details):
           # Open A connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {'status':500,
                       'description':"Couldn't connect to the Database!"}
            return jsonify(message)

         #Try except block to handle data extraction
        try:                        
            #Get discount accounts            
            discount = 19

            total_discount_accounts = []
            discount_data = []

            status = details['status']

            #Get total discount Balance
            cur.execute("""SELECT sum(balance) totaldiscount FROM accounts WHERE status = %s AND type = %s ORDER BY id ASC""", [status, discount])
            totaldiscount = cur.fetchone()

            total_discount = float(totaldiscount['totaldiscount'])

            cur.execute("""SELECT id, reference_no, number, name, balance FROM accounts WHERE status = %s AND type = %s ORDER BY id ASC""", [status, discount])
            discounts = cur.fetchall()

            discount_accounts = []
            for discount in discounts:
                balance = float(discount['balance']) 
                res = {
                     "accountid": discount['id'],
                     "accountref": discount['reference_no'],
                     "accountnumber": discount['number'],
                     "accountname": discount['name'],
                     "balance": balance                                 

                }
                discount_accounts.append(res)
                
            total_discount_value = {"totaldiscount":total_discount}
            total_discount_accounts.append(total_discount_value)

            discount_data.append(discount_accounts)
            discount_data.append(total_discount_accounts)

            
            #The response object
            message = {'status':200,
                       'response':discount_data,
                       'description':'Discount accounts were fetched successfully'}

            return message

        except Exception as error:
            message = {'status':501,
                       'description':'Failed to fetch discount accounts records. {}'.format(error)}
            return message
        finally:
            cur.close()

    