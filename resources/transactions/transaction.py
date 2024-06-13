from flask import Response, jsonify
from main import mysql, app
from datetime import datetime
from resources.alphanumeric.generate import UniqueNumber
from resources.logs.logger import ErrorLogger
from resources.payload.payload import Localtime
import uuid

class Transaction():
    def debit_on_debit_account(self, transaction_data):
        
        if transaction_data == None:
            message = {"status":402,     
                       "error":"t_r001",             
                       "description":"Request data is missing some details!"}
            ErrorLogger().logError(message)
            return message

        #Open a connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database", 
                       "error":"t_r002",
                       "status":500}
            ErrorLogger().logError(message)
            return message 
            
        try:  
            #process data        
            global_id = transaction_data["global_id"]
            entry_id = transaction_data["entry_id"]
            sub_entry_id = transaction_data["sub_entry_id"]
            transaction_type = transaction_data["type"]
            dr_ac_number = transaction_data["account_number"]
            amount = transaction_data["amount"] 
            amount = round(amount, 12)
            dr_trans_name = transaction_data["transaction_name"]
            description = transaction_data["description"]
            settlementDate = transaction_data["settlement_date"]        
            layer1_id = transaction_data["layer1_id"]

            
            trans_uuid_ = str(uuid.uuid4())
            trans_uuid = trans_uuid_.replace("-", "" )
            trans_uuid = str(trans_uuid)
            trans_id = 'tt' + str(trans_uuid[-12:])
            
            created_date = Localtime().gettime()   
            #Update debit account balance, increase the balance.
            cur.execute("""UPDATE accounts set last_transaction_id = %s, last_amount = %s, balance = balance + %s WHERE number = %s""", ([trans_id],[amount],[amount],[dr_ac_number]))
            
        except Exception as error:
            message = {"description": f"Account balance update failed. Transaction id {trans_id} Amount {amount} Account {dr_ac_number} Error description" + format(error),
                       "error":"t_r003",
                       "status":500}
            ErrorLogger().logError(message)
            
            return message 

        try: 
            cur.execute("""SELECT amount, balance_before, balance_after, account_number FROM accounts_balances_log WHERE last_transaction_id = %s """, [trans_id])
            get_log = cur.fetchone() 
            if get_log:
                amount = float(get_log["amount"])
                amount = round(amount, 12)
                balance_before = float(get_log["balance_before"])
                balance_before = round(balance_before, 12)
                balance_after = float(get_log["balance_after"])
                balance_after = round(balance_after, 12)
                account_number = get_log["account_number"]

            #Record a debit transaction on a debit account
            status = 1
           
            sql = "INSERT INTO transactions (id, global_id, layer1_id, entry_id, sub_entry_id, transaction_type, account_number, debit_amount, balance_before, balance_after, transaction_name, description, settlement_date, created_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
            values = (trans_id, global_id, layer1_id, entry_id, sub_entry_id, transaction_type, account_number, amount, balance_before, balance_after, dr_trans_name, description, settlementDate, created_date, status)
            cur.execute(sql, values)             
             
            data = {"trans_id":trans_id,"amount":amount, "dr_ac_number":dr_ac_number}
            message = {"description":"Transaction was successful", 
                       "data":data,
                       "status":200}
            return message 
        
        except Exception as error:
            mysql.get_db().rollback() 
            mysql.get_db().rollback() 
            message = {"status":501,
                       "error":"t_r004",
                       "description": f"Transaction execution failed. Transaction id {trans_id} Amount {amount} Account {dr_ac_number} Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close() 

    def debit_on_debit_account_rollback(self, data):
        if data == None:
            message = {"status":402,
                       "error":"t_r005",
                       "description":"Request data is missing some details!"}
            ErrorLogger().logError(message)
            return message
        
    
        #Open a connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database", 
                       "error":"t_r006",
                       "status":500}
            ErrorLogger().logError(message)
            
            return message

        try:  
            trans_id = data["trans_id"]
            amount = float(data["amount"])
            amount = round(amount, 12)
            dr_ac_number = data["dr_ac_number"]

            cur.execute("""UPDATE transactions set status =0 WHERE id = %s""", (trans_id))
            mysql.get_db().commit()

            #Update debit account balance, reverse previous increment of the amount.
            cur.execute("""UPDATE accounts set last_transaction_id = %s, last_amount = %s, balance = balance - %s WHERE number = %s""", ([trans_id],[amount],[amount],[dr_ac_number]))
            mysql.get_db().commit() 
             
           
        except Exception as error:
            message = {"status":501,
                       "error":"t_r007",
                       "description":f"Transaction Debit on debit rollback failed. Transaction id {trans_id} Amount {amount} Account {dr_ac_number}   Error description " + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            cur.close()

    def credit_on_debit_account(self, transaction_data):
        
        if transaction_data == None:
            message = {"status":402,
                       "error":"t_r008",
                       "description":"Request data is missing some details!"}
            ErrorLogger().logError(message)
            return message

        #Open a connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database", 
                       "error":"t_r009",
                       "status":500}
            ErrorLogger().logError(message)
            
            return message

        try:
            #process data        
            global_id = transaction_data["global_id"]
            entry_id = transaction_data["entry_id"]
            sub_entry_id = transaction_data["sub_entry_id"]
            transaction_type = transaction_data["type"]
            cr_ac_number = transaction_data["account_number"]
            amount = transaction_data["amount"]
            amount = round(amount, 12)
            cr_trans_name = transaction_data["transaction_name"]
            description = transaction_data["description"]
            settlementDate = transaction_data["settlement_date"]        
            layer1_id = transaction_data["layer1_id"]

            
            trans_uuid_ = str(uuid.uuid4())
            trans_uuid = trans_uuid_.replace("-", "" )
            trans_uuid = str(trans_uuid)
            trans_id = 'tt' + str(trans_uuid[-12:])
            
            created_date = Localtime().gettime()
            #Record a credit transaction on a debit account
            cur.execute("""UPDATE accounts set last_transaction_id = %s, last_amount = %s, balance= balance - %s WHERE number = %s""", ([trans_id],[amount],[amount],[cr_ac_number]))
        
        except Exception as error:
            message = {"description": f"Account balance update failed. Transaction id {trans_id} Amount {amount} Account {cr_ac_number} Error description" + format(error),
                       "error":"t_r010",
                       "status":500}
            ErrorLogger().logError(message)
            
            return message 

        try: 
            cur.execute("""SELECT amount, balance_before, balance_after, account_number FROM accounts_balances_log WHERE last_transaction_id = %s """, [trans_id])
            get_log = cur.fetchone() 
            if get_log:
                amount = float(get_log["amount"])
                amount = round(amount, 12)
                balance_before = float(get_log["balance_before"])
                balance_before = round(balance_before, 12)
                balance_after = float(get_log["balance_after"])
                balance_after = round(balance_after, 12)
                account_number = get_log["account_number"]

            status = 1
            
            sql = "INSERT INTO transactions (id, global_id, layer1_id, entry_id, sub_entry_id, transaction_type, account_number, credit_amount, balance_before, balance_after, transaction_name, description, settlement_date, created_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (trans_id, global_id, layer1_id, entry_id, sub_entry_id, transaction_type, account_number, amount, balance_before, balance_after, cr_trans_name, description, settlementDate, created_date, status)
            cur.execute(sql, values)
            
            data = {"trans_id":trans_id,"amount":amount, "cr_ac_number":cr_ac_number}
            message = {"description":"Transaction was successful", 
                       "data":data,
                       "status":200}
            return message   

        except Exception as error:
            mysql.get_db().rollback()
            mysql.get_db().rollback() 
            message = {"status":501,
                        "error":"t_r011",
                       "description": f"Transaction execution failed. Transaction id {trans_id} Amount {amount} Account {cr_ac_number}   Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit() 
            cur.close() 

    def credit_on_debit_account_rollback(self, data):
        if data == None:
            message = {"status":402,
                       "error":"t_r012",
                       "description":"Request data is missing some details!"}
            ErrorLogger().logError(message)
            return message
        
        #Open a connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database", 
                       "error":"t_r013",
                       "status":500}
            ErrorLogger().logError(message)
            
            return message

        try:  
            trans_id = data["trans_id"]
            amount = data["amount"]
            amount = round(amount, 12)
            cr_ac_number = data["cr_ac_number"]

            cur.execute("""UPDATE transactions set status =0 WHERE id = %s""", (trans_id))
            mysql.get_db().commit()

            #Update credt account balance, reverse previous increase of the amount.
            cur.execute("""UPDATE accounts set last_transaction_id = %s, last_amount = %s, balance = balance + %s WHERE number = %s""", ([trans_id],[amount],[amount],[cr_ac_number]))
            mysql.get_db().commit()  
        
        except Exception as error:
            message = {"status":501,
                       "error":"t_r014",
                       "description": f"Transaction Credit on debit rollback failed. Transaction id {trans_id} Amount {amount} Account {cr_ac_number}  Error description " + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            cur.close()

    def debit_on_credit_account(self, transaction_data):
        
        if transaction_data == None:
            message = {"status":402,
                       "error":"t_r015",
                       "description":"Request data is missing some details!"}
            ErrorLogger().logError(message)
            return message

        #Open a connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database", 
                       "error":"t_r016",
                       "status":500}
            ErrorLogger().logError(message)
            
            return message

        try:
            #process data
            global_id = transaction_data["global_id"]
            entry_id = transaction_data["entry_id"]
            sub_entry_id = transaction_data["sub_entry_id"]
            transaction_type = transaction_data["type"]
            dr_ac_number = transaction_data["account_number"]
            amount = transaction_data["amount"]
            amount = round(amount, 12)
            dr_trans_name = transaction_data["transaction_name"]
            description = transaction_data["description"]
            settlementDate = transaction_data["settlement_date"]        
            layer1_id = transaction_data["layer1_id"]

            
            trans_uuid_ = str(uuid.uuid4())
            trans_uuid = trans_uuid_.replace("-", "" )
            trans_uuid = str(trans_uuid)
            trans_id = 'tt' + str(trans_uuid[-12:])
            
            created_date = Localtime().gettime()
            #Update debit account balance, decrease the balance.
            cur.execute("""UPDATE accounts set last_transaction_id = %s, last_amount = %s, balance= balance - %s WHERE number = %s""", ([trans_id], [amount], [amount], [dr_ac_number]))
        except Exception as error:
            message = {"description": f"Account balance update failed. Transaction id {trans_id} Amount {amount} Account {dr_ac_number} Error description" + format(error),
                       "error":"t_r017",
                       "status":500}
            ErrorLogger().logError(message)
            
            return message 

        try:
            cur.execute("""SELECT amount, balance_before, balance_after, account_number FROM accounts_balances_log WHERE last_transaction_id = %s """, [trans_id])
            get_log = cur.fetchone() 
            if get_log:
                amount = float(get_log["amount"])
                amount = round(amount, 12)
                balance_before = float(get_log["balance_before"])
                balance_before = round(balance_before, 12)
                balance_after = float(get_log["balance_after"])
                balance_after = round(balance_after, 12)
                account_number = get_log["account_number"]
                

            #Record a credit transaction on a debit account
            status = 1
            sql = "INSERT INTO transactions (id, global_id, layer1_id, entry_id, sub_entry_id, transaction_type, account_number, debit_amount, balance_before, balance_after, transaction_name, description, settlement_date, created_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (trans_id, global_id, layer1_id, entry_id, sub_entry_id, transaction_type, account_number, amount, balance_before, balance_after, dr_trans_name, description, settlementDate, created_date, status)
            cur.execute(sql, values) 
            
            data = {"trans_id":trans_id,"amount":amount, "dr_ac_number":dr_ac_number}
            message = {"description":"Transaction was successful", 
                       "data":data,
                       "status":200}
            return message  

        except Exception as error:
            mysql.get_db().rollback()
            mysql.get_db().rollback() 
            message = {"status":501,
                       "error":"t_r018",
                       "description":f"Transaction execution failed. Transaction id {trans_id} Amount {amount} Account {dr_ac_number}  Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close() 

    def debit_on_credit_account_rollback(self, data):
        if data == None:
            message = {"status":402,
                       "error":"t_r019",
                       "description":"Request data is missing some details!"}
            ErrorLogger().logError(message)
            return message
        
        #Open a connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database", 
                       "error":"t_r020",
                       "status":500}
            ErrorLogger().logError(message)
            
            return message

        try:   
            trans_id = data["trans_id"]
            amount = data["amount"]
            amount = round(amount, 12)
            dr_ac_number = data["dr_ac_number"]

            cur.execute("""UPDATE transactions set status =0 WHERE id = %s""", (trans_id))
            mysql.get_db().commit()
        
            #Update debit account balance, reverse previous increment of the amount.
            cur.execute("""UPDATE accounts set last_transaction_id = %s, last_amount = %s, balance = balance + %s WHERE number = %s""", ([trans_id],[amount],[amount],[dr_ac_number]))
            mysql.get_db().commit()  
        
        except Exception as error:
            message = {"status":501,
                       "error":"t_r021",
                       "description":f"Transaction Debit on credit rollback failed. Transaction id {trans_id} Amount {amount} Account {dr_ac_number}  Error description " + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            cur.close()

    def credit_on_credit_account(self, transaction_data):
        
        if transaction_data == None:
            message = {"status":402,
                       "error":"t_r022",
                       "description":"Request data is missing some details!"}
            ErrorLogger().logError(message)
            return message
        
        #Open a connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database", 
                       "error":"t_r023",
                       "status":500}
            ErrorLogger().logError(message)
            
            return message

        try:
            #process data            
            global_id = transaction_data["global_id"]
            entry_id = transaction_data["entry_id"]
            sub_entry_id = transaction_data["sub_entry_id"]
            transaction_type = transaction_data["type"]
            cr_ac_number = transaction_data["account_number"]
            amount = transaction_data["amount"]
            amount = round(amount, 12)
            cr_trans_name = transaction_data["transaction_name"]
            description = transaction_data["description"]
            settlementDate = transaction_data["settlement_date"]            
            layer1_id = transaction_data["layer1_id"]

            trans_uuid_ = str(uuid.uuid4())
            trans_uuid = trans_uuid_.replace("-", "" )
            trans_uuid = str(trans_uuid)
            trans_id = 'tt' + str(trans_uuid[-12:])
            
            created_date = Localtime().gettime()
            #Update credit account balance, increase the balance.
            cur.execute("""UPDATE accounts set last_transaction_id = %s, last_amount = %s, balance= balance + %s WHERE number = %s""", ([trans_id],[amount],[amount],[cr_ac_number]))
        
        except Exception as error:
            message = {"description": f"Account balance update failed. Transaction id {trans_id} Amount {amount} Account {cr_ac_number} Error description" + format(error),
                       "error":"t_r024",
                       "status":500}
            ErrorLogger().logError(message)
            
            return message 
        
        try: 
            cur.execute("""SELECT amount, balance_before, balance_after, account_number FROM accounts_balances_log WHERE last_transaction_id = %s """, [trans_id])
            get_log = cur.fetchone() 
            if get_log:
                amount = float(get_log["amount"])
                amount = round(amount, 12)
                balance_before = float(get_log["balance_before"])
                balance_before = round(balance_before, 12)
                balance_after = float(get_log["balance_after"])
                balance_after = round(balance_after, 12)
                account_number = get_log["account_number"]

            #Record a debit transaction on a debit account
            status = 1
            sql = "INSERT INTO transactions (id, global_id, layer1_id, entry_id, sub_entry_id, transaction_type, account_number, credit_amount, balance_before, balance_after, transaction_name, description, settlement_date, created_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (trans_id, global_id, layer1_id, entry_id, sub_entry_id, transaction_type, account_number, amount, balance_before, balance_after, cr_trans_name, description, settlementDate, created_date, status)
            cur.execute(sql, values)
            
            data = {"trans_id":trans_id,"amount":amount, "cr_ac_number":cr_ac_number}
            message = {"description":"Transaction was successful", 
                       "data":data,
                       "status":200}
            return message 

        except Exception as error:
            mysql.get_db().rollback()
            mysql.get_db().rollback() 
            message = {"status":501,
                       "error":"t_r025",
                       "description": f"Transaction execution failed. Transaction id {trans_id} Amount {amount} Account {cr_ac_number}  Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def credit_on_credit_account_rollback(self, data):
        if data == None:
            message = {"status":402,
                       "error":"t_r026",
                       "description":"Request data is missing some details!"}
            ErrorLogger().logError(message)
            return message
        
        #Open a connection to the database
        try:
            cur =  mysql.get_db().cursor()
        except:
            message = {"description":"Couldn't connect to the Database", 
                       "error":"t_r027",
                       "status":500}
            ErrorLogger().logError(message)
            
            return message

        try:     
            trans_id = data["trans_id"]
            amount = data["amount"]
            amount = round(amount, 12)
            cr_ac_number = data["cr_ac_number"]

            cur.execute("""UPDATE transactions set status =0 WHERE id = %s""", (trans_id))
            mysql.get_db().commit() 
              
            #Update credt account balance, reverse previous increase of the amount.
            cur.execute("""UPDATE accounts set last_transaction_id = %s, last_amount = %s, balance = balance - %s WHERE number = %s""", ([trans_id],[amount],[amount],[cr_ac_number]))
            mysql.get_db().commit() 

        except Exception as error:
            message = {"status":501,
                       "error":"t_r028",
                        "description": f"Transaction Credit on credit rollback failed. Transaction {trans_id} Amount {amount} Account {cr_ac_number} Error description " + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            cur.close()
        
