from flask import request, Response, json, jsonify
import os
from main import mysql, app
from datetime import datetime
from resources.payload.payload import Localtime
from resources.logs.logger import ErrorLogger



class PaymentsTransactionsCosts():
    def mpesa_b2c_charges(self, withdraw_amount):
        
            # Open A connection to the database
            try:
                cur =  mysql.get_db().cursor()            
            except:
                message = {"status":500,
                        "data":0,
                        "description":"Couldn't connect to the Database!"}
                return message

            try:
                cur.execute("""SELECT charges_amount, markup_fee FROM mpesa_transactions_charges WHERE status =1 AND start_amount <=%s AND end_amount >=%s """, [withdraw_amount, withdraw_amount])
                get_b2c_charges= cur.fetchone()                 
                if get_b2c_charges:
                    b2c_charge_amount = float(get_b2c_charges["charges_amount"]) 
                    b2c_markup_fee = float(get_b2c_charges["markup_fee"]) 
                    data = {
                             "b2c_charge_amount":b2c_charge_amount, 
                             "b2c_markup_fee":b2c_markup_fee
                             }

                    message = {"description":"B2C transaction cost was found!", 
                               "data":data,
                               "status":200
                                }

                    return message
                else:
                    message = {
                            "description":"B2C transaction cost was not found!", 
                            "status":201
                            }
                    return message
                
            except Exception as error:
                message = {"status":501,
                        "description":"Transaction failed! Error description " + format(error)}
                return message
            finally:
                cur.close()