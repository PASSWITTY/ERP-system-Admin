from flask import request, Response, json, jsonify
from resources.password.crypt_password import hash_password, unhash_password
from main import mysql, app
from resources.payload.payload import Localtime
from resources.middleware.tokens.jwt import sign_token, refresh_token, sign_permissions 
from resources.logs.logger import ErrorLogger
from resources.reports.assets_reports.assets_reports import AssetsReports
from resources.reports.liability_reports.liability_reports import LiabilityReports 
from resources.reports.equity_reports.equity_reports import EquityReports
from resources.reports.income_statements.income_statement_total import IncomeStatement

class FinanceReports():
            
    def get_assets_accounts(self, user):  
        
        details = request.get_json()

        if details == None:
            message = {'status':402,
                       'description':'Request data is missing some details!'}
            return jsonify(message)

         #Try except block to handle data extraction
        try:                        
            #Get assets accounts            
            assets_data = AssetsReports.get_assets_accounts(self, user, details)
            
            if int(assets_data['status']) == 200:
                asset_accounts = assets_data['response'][0]
                total_asset_accounts_balance = assets_data['response'][1]
                message = {'status':200,
                           'response':[asset_accounts,total_asset_accounts_balance],
                           'description':'Report details was fetched successfully'}

                return jsonify(message)
            
            else:
                message = {'status':assets_data['status'],
                           'response':[],
                           'description':'Report was not found'}

                return jsonify(message)


        except Exception as error:
            message = {'status':501,
                       'response':[],
                       'description':'Failed to fetch asset accounts records one. {}'.format(error)}
            return jsonify(message)
        
    def get_liability_accounts(self, user):  
                
        details = request.get_json()

        if details == None:
            message = {'status':402,
                       'description':'Request data is missing some details!'}
            return jsonify(message)
               
         #Try except block to handle data extraction
        try:            
            
            #Get liability accounts         
            liability_data = LiabilityReports.get_liability_accounts(self, user, details)
            
            if int(liability_data['status']) == 200:
                liability_accounts = liability_data['response'][0]                
                total_liability_accounts_balance = liability_data['response'][1]
               
                message = {'status':200,
                           'response':[liability_accounts,total_liability_accounts_balance],
                           'description':'Liability accounts details were fetched successfully'}

                return jsonify(message)
            
            else:
                message = {'status':liability_data['status'],
                           'response':[],
                           'description':'Liability accounts details were not found'}

            return jsonify(message)


        except Exception as error:
            message = {'status':501,
                       'response':[],
                       'description':'Failed to fetch liability accounts records one. {}'.format(error)}
            return jsonify(message)
        
    def get_equity_accounts(self, user):  
        
        details = request.get_json()

        if details == None:
            message = {'status':402,
                       'description':'Request data is missing some details!'}
            return jsonify(message)

         #Try except block to handle data extraction
        try:         
            equity_data = EquityReports.get_equity_accounts(self, user, details)
            
            if int(equity_data['status']) == 200:
                equity_accounts = equity_data['response'][0]                
                total_equity_accounts_balance = equity_data['response'][1]
               
                message = {'status':200,
                           'response':[equity_accounts, total_equity_accounts_balance],
                           'description':'Equity accounts details were fetched successfully'}

                return jsonify(message)
            
            else:
                message = {'status':equity_data['status'],
                           'response':[],
                           'description':'Equity accounts details were not found'}

            return jsonify(message)


        except Exception as error:
            message = {'status':501,
                       'response':[],
                       'description':'Failed to fetch equity accounts records one. {}'.format(error)}
            return jsonify(message)
        

    def get_profit_loss(self, user):     
        details = request.get_json()

        if details == None:
            message = {'status':402,
                       'description':'Request data is missing some details!'}
            return jsonify(message)
                
         #Try except block to handle data extraction
        try:           
            
            income_statement_data = IncomeStatement.get_profit_loss_balance(self, user, details)
            
            if int(income_statement_data['status']) == 200:
                print(income_statement_data)
                income_statement = income_statement_data['response']              
            #     total_equity_accounts_balance = income_statement_data['response'][1]
               
                message = {'status':200,
                           'response':income_statement,
                           'description':'Income statement balance was fetched successfully'}

                return jsonify(message)
            
            else:
                message = {'status':income_statement_data['status'],
                           'response':[],
                           'description':'Income statement balance was not found'}

            return jsonify(message)


        except Exception as error:
            message = {'status':501,
                       'response':[],
                       'description':'Failed to fetch equity accounts records one. {}'.format(error)}
            return jsonify(message)
        
        
    def get_shareholder_equity(self, user):
        details = request.get_json()

        if details == None:
            message = {'status':402,
                       'description':'Request data is missing some details!'}
            return jsonify(message)
        
         #Try except block to handle data extraction
        try:            

            equity_data = EquityReports.get_equity_accounts(self, user, details)
            if int(equity_data['status']) == 200:
                equity_accounts = equity_data['response'][0]                
                total_equity_accounts_balance = float(equity_data['response'][1][0]['totalEquity'])
                
            else:
                total_equity_accounts_balance = 0
            
            income_statement_data = IncomeStatement.get_profit_loss_balance(self, user, details)            
            if int(income_statement_data['status']) == 200:                
                income_statement_balance = float(income_statement_data['response']['net_income']) 
                
            else:
                income_statement_balance = 0        

            shareholderequity =  (total_equity_accounts_balance + income_statement_balance)   

            message = {'status':200,
                       'response':shareholderequity,
                       'description':'Share holder equity was computed successfully'}

            return jsonify(message)            


        except Exception as error:
            message = {'status':501,
                       'response': 0,
                       'description':'Failed to compute share holder equity amount. {}'.format(error)}
            return message
        
        
    def get_shareholder_funds(self, user):
        details = request.get_json()

        if details == None:
            message = {'status':402,
                       'description':'Request data is missing some details!'}
            return jsonify(message)
        
         #Try except block to handle data extraction
        try:            

            assets_accounts_response = AssetsReports().get_assets_accounts(user, details)
            if int(assets_accounts_response['status']) == 200:
                get_total_assets = assets_accounts_response["response"][1][0]
                totalassets = float(get_total_assets["totalAssets"])
            
            else:
                totalassets = 0

            
            liability_accounts_response = LiabilityReports().get_liability_accounts(user, details)
            if int(liability_accounts_response['status']) == 200:
                get_total_liability = liability_accounts_response["response"][1][0]
                totalliabilities = get_total_liability['totalLiability']
            
            else:
                totalliabilities = 0

            shareholderfunds =  (totalassets - totalliabilities)   

            message = {'status':200,
                       'response':shareholderfunds,
                       'description':'Share holder funds were computed successfully'}

            return jsonify(message)            


        except Exception as error:
            message = {'status':501,
                       'response': 0,
                       'description':'Failed to fetch share holder accounts records. {}'.format(error)}
            return message