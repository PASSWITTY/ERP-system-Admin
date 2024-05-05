from flask import request, Response, json, jsonify
import os
from main import mysql, app
from datetime import datetime
from resources.payload.payload import Localtime
from resources.logs.logger import ErrorLogger
import math


class UniqueNumber():
    def globalIdentifier(self):  #0 
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_global_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = '0' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().globalIdentifier()
            message = {"status":501,
                       "description": f"Error generating global id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close() 
  
    def accountId(self):  #A
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_account_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'A' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().accountId()
            message = {"status":501,
                       "description": f"Error generating account id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def bankDepositId(self):  #BD
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_bank_deposit_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'BD' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().bankDepositId()
            message = {"status":501,
                       "description": f"Error generating bank deposit Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
              
    def demandnoteId(self):  #F
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_demandnote_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'F' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().demandnoteId()
            message = {"status":501,
                       "description": f"Error generating demand note id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close() 

    def subdemandnoteId(self):  #FF
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_subdemandnote_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'FF' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().subdemandnoteId()
            message = {"status":501,
                       "description": f"Error generating sub demand notes id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def rolloverfeeentryId(self):  #R
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_rollover_fee_entry_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'R' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().rolloverfeeentryId()
            message = {"status":501,
                       "description": f"Error generating rollover fee id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def rolloverfeeReverseId(self):  #RR
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_reversed_rollover_fee_entry_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'RR' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().rolloverfeeReverseId()
            message = {"status":501,
                       "description": f"Error generating reverse rollover fee id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def defaultedloanfinesentryId(self):  #LF
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_loan_default_fines_entry_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'LF' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().defaultedloanfinesentryId()
            message = {"status":501,
                       "description": f"Error generating default fines entry id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def leadId(self):  #E    
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_lead_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'E' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().leadId()
            message = {"status":501,
                       "description": f"Error generating lead id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def staffId(self):  #S
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_staff_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'S' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().staffId()
            message = {"status":501,
                       "description": f"Error generating staff id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def userId(self):  #U
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_user_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'U' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().userId()
            message = {"status":501,
                       "description": f"Error generating user id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def customerId(self):  #C  
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_customer_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber().accountSyntax(int_var)            
            alpha_var = 'C' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().customerId()
            message = {"status":501,
                       "description": f"Error generating customer id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
            
    def customer_ussd_login_item_id(self):  #CU
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_ussd_login_item_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber().accountSyntax(int_var)            
            alpha_var = 'CU' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().customer_ussd_login_item_id()
            message = {"status":501,
                       "description": f"Error generating ussd logins id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def customer_mobileapp_login_id(self):  #CA
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_mobileapp_login_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber().accountSyntax(int_var)            
            alpha_var = 'CA' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().customer_mobileapp_login_id()
            message = {"status":501,
                       "description": f"Error generating mobile app login id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def spoofReportId(self):  #CR
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_spoofreport_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber().accountSyntax(int_var)            
            alpha_var = 'CR' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().spoofReportId()
            message = {"status":501,
                       "description": f"Error generating spoof report id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
            
    def groupId(self):  #G
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_group_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber().accountSyntax(int_var)            
            alpha_var = 'G' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().groupId()
            message = {"status":501,
                       "description": f"Error generating group id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def groupCustomerId(self):  #GC
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_group_customer_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber().accountSyntax(int_var)            
            alpha_var = 'GC' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().groupCustomerId()
            message = {"status":501,
                       "description": f"Error generating group customer id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def loanproductId(self):  #P
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_product_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'P' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().loanproductId()
            message = {"status":501,
                       "description": f"Error generating product id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
            
    def productPeriodId(self):  #J
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_product_period_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'J' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().productPeriodId()
            message = {"status":501,
                       "description": f"Error generating product period id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def loansId(self):  #L
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_loans_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'L' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().loansId()
            message = {"status":501,
                       "description": f"Error generating loan id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def loanChargeId(self):  #LC
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_loancharge_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'LC' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().loanChargeId()
            message = {"status":501,
                       "description": f"Error generating loan charge id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def defaultChargesId(self):  #LK
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_defaultcharge_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'LK' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().defaultChargesId()
            message = {"status":501,
                       "description": f"Error generating default charge id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def loanRepaymentFundsId(self):  #LP
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_loanrepayment_funds_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'LP' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().loanRepaymentFundsId()
            message = {"status":501,
                       "description": f"Error generating loan repayment funds id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def defaultLoanChargeId(self):  #LD
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_defaulted_loancharge_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'LD' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().defaultLoanChargeId()
            message = {"status":501,
                       "description": f"Error generating loan charge id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def productAdHocChargeId(self):  #LH
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_product_adhoc_charge_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'LH' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().productAdHocChargeId()
            message = {"status":501,
                       "description": f"Error generating loan adhoc charge id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def loanInterestId(self):  #LI
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_loaninterest_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'LI' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().loanInterestId()
            message = {"status":501,
                       "description": f"Error generating loan interest charge id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
            
    def loanTaxId(self):  #LT
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_loantax_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'LT' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().loanTaxId()
            message = {"status":501,
                       "description": f"Error generating loan tax id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def loanRolloverId(self):  #LR
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_loanrollover_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'LR' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().loanRolloverId()
            message = {"status":501,
                       "description": f"Error generating loans charge id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def loanCronJobDemandnoteGenerateId(self):  #LG
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_cronjob_createdemandnote_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'LG' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().loanCronJobDemandnoteGenerateId()
            message = {"status":501,
                       "description": f"Error generating cronjob id for demand note. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def rolloverfeeCronJobDemandnoteGenerateId(self):  #LJ
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_rolloverfee_cronjob_createdemandnote_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'LJ' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().rolloverfeeCronJobDemandnoteGenerateId()
            message = {"status":501,
                       "description": f"Error generating cronjob id for rollover fee cron job queue. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
            
    def defaultedloanfinesCronJobDemandnoteGenerateId(self):  #LH
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_defaultedloanfines_cronjob_createdemandnote_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'LH' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().defaultedloanfinesCronJobDemandnoteGenerateId()
            message = {"status":501,
                       "description": f"Error generating cronjob id for defaulted loan fines demand note. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
            
    def defaultedOkoaAirtimeRequestId(self):  #LA
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_okoa_airtime_requests_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'LA' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().defaultedOkoaAirtimeRequestId()
            message = {"status":501,
                       "description": f"Error generating okoa airtime loan request id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
            
    def transactionsId(self):  #T
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_transactions_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'T' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().transactionsId()
            message = {"status":501,
                       "description": f"Error generating transaction Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
   
    def transactionsdebitcreditId(self):  #TT
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_transactiondebitcredit_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'TT' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().transactionsdebitcreditId()
            message = {"status":501,
                       "description": f"Error generating debit credit transaction Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
  
    def supplierId(self):  #Z
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_supplier_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'Z' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().supplierId()
            message = {"status":501,
                       "description": f"Error generating supplier Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def inventoryItemId(self):  #I
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_inventoryitem_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'I' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().inventoryItemId()
            message = {"status":501,
                       "description": f"Error generating inventory item Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def smsReferenceId(self):  #IS
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_sms_reference_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'IS' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().smsReferenceId()
            message = {"status":501,
                       "description": f"Error generating sms Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
            
    def airtimeStockId(self):  #IA
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_airtime_stock_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'IA' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().airtimeStockId()
            message = {"status":501,
                       "description": f"Error generating sms Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def mpesaB2CRequestId(self):  #MR
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_mpesab2c_request_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'MR' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().mpesaB2CRequestId()
            message = {"status":501,
                       "description": f"Error generating sms Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def mpesaC2BRequestId(self):  #MC
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_mpesac2b_request_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'MC' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().mpesaC2BRequestId()
            message = {"status":501,
                       "description": f"Error generating mpesa c2b Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
            
    def mpesaC2BTillRequestId(self):  #ME
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_mpesac2b_till_request_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'ME' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().mpesaC2BRequestId()
            message = {"status":501,
                       "description": f"Error generating mpesa c2b Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def mpesaC2BPaybillRequestId(self):  #MB
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_mpesac2b_paybill_request_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'MB' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().mpesaC2BPaybillRequestId()
            message = {"status":501,
                       "description": f"Error generating mpesa c2b paybill Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def mpesaSTKRequestId(self):  #MS
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_mpesastk_request_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'MS' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().mpesaSTKRequestId()
            message = {"status":501,
                       "description": f"Error generating mpesa stk request Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def mpesaSTKPaybillRequestId(self):  #MG
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_mpesastk_paybill_request_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'MG' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().mpesaSTKPaybillRequestId()
            message = {"status":501,
                       "description": f"Error generating mpesa stk paybill request Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
            
    def mpesaAirtimeSTKRequestId(self):  #MT
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_mpesaairtime_stk_request_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'MT' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().mpesaSTKRequestId()
            message = {"status":501,
                       "description": f"Error generating mpesa stk request Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def mpesaTransactionQueryId(self):  #MQ
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_mpesa_transaction_query_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'MQ' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().mpesaTransactionQueryId()
            message = {"status":501,
                       "description": f"Error generating mpesa transaction query Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def MpesaDisbursementRequestId(self):  #MD
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_mpesa_disbursement_request_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'MD' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().MpesaDisbursementRequestId()
            message = {"status":501,
                       "description": f"Error generating mpesa disbursement request Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def MpesaDisbursementResponseId(self):  #MF
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_mpesa_disbursement_response_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'MF' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().MpesaDisbursementResponseId()
            message = {"status":501,
                       "description": f"Error generating mpesa disbursement response Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def MpesadepositRequestId(self):  #MP
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_mpesa_deposit_request_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'MP' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().MpesadepositRequestId()
            message = {"status":501,
                       "description": f"Error generating mpesa deposit request Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    
    def saccoId(self):  #V
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_sacco_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'V' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().saccoId()
            message = {"status":501,
                       "description": f"Error generating sacco Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
    def saccoPayoutExpenseID(self):  #VE
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_sacco_payout_expense_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'VE' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().saccoPayoutExpenseID()
            message = {"status":501,
                       "description": f"Error generating sacco payout expense Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
            
    def saccoPayoutPaymentID(self):  #VP
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_sacco_payout_payment_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'VP' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().saccoPayoutPaymentID()
            message = {"status":501,
                       "description": f"Error generating sacco payout payment Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()
            
    def cashoutLoanSettlementID(self):  #VC
        try:
            cur = mysql.get_db().cursor()
        except:
            return Response({"Couldn't connect to the Database"}, status=500)
    
        try:   
            date_created = Localtime().gettime()
            cur.execute("""INSERT INTO generate_cashout_loan_settlement_id (date_created) VALUES (%s)""",(date_created))
            mysql.get_db().commit() 
            
            int_var = cur.lastrowid

            generatedid = UniqueNumber.accountSyntax(self, int_var)            
            alpha_var = 'VP' + str(generatedid)
                    
            return alpha_var
        except Exception as error:
            mysql.get_db().rollback() 
            UniqueNumber().cashoutLoanSettlementID()
            message = {"status":501,
                       "description": f"Error generating cashout loan settlement Id. Error description" + format(error)}
            ErrorLogger().logError(message)
            
            return message
        finally:
            mysql.get_db().commit()
            cur.close()

    def accountSyntax(self, var):

        # list of all allowed alphanumeric
        alphanumeric = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        # def generate_id():
        number = var
        remainders = []
        while number > 0:
            remainder = number % 36
            whole = math.floor(number / 36)
            number = whole
            remainders.append(remainder)

        if (len(remainders) > 12):
            raise Exception("Maximum digits are 12")

        #   return remainders

        # def format_to_id(remainders):  
        generated_id = ""
        for remainder in remainders:
            generated_id = alphanumeric[remainder] + generated_id

        formatted = "00000000000" + generated_id

        var = formatted[-12:]

        return var

