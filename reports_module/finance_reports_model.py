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
from resources.reports.revenue_reports.revenue_reports import RevenueReports
from resources.reports.discount_reports.discount_reports import DiscountReports 
from resources.reports.cog_reports.cog_reports import CogReports
from resources.reports.expense_reports.expenses_reports import ExpensesReports
from resources.reports.other_income_reports.other_income_reports import OtherIncomeReports
from resources.reports.other_expense_reports.other_expenses_reports import OtherExpensesReports


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
                income_statement = income_statement_data['response']              
               
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
                       'description':'Failed to fetch liability accounts records. {}'.format(error)}
            return message
        
    def get_revenue_accounts(self, user):
        details = request.get_json()

        if details == None:
            message = {'status':401,
                       'description':'Request data is missing some details!'}
            return jsonify(message)

         #Try except block to handle data extraction
        try:                        
            #Get assets accounts            
            revenue_data = RevenueReports.get_revenue_accounts(self, user, details)
            # print(revenue_data['response'][0])
            if int(revenue_data['status']) == 200:
                revenue_accounts = revenue_data['response'][0]
                total_revenue_accounts_balance = revenue_data['response'][1]
                message = {'status':200,
                           'response':[revenue_accounts,total_revenue_accounts_balance],
                           'description':'Report details was fetched successfully'}

                return jsonify(message)
            
            else:
                message = {'status':revenue_data['status'],
                           'response':[],
                           'description':'Report was not found'}

                return jsonify(message)


        except Exception as error:
            message = {'status':501,
                       'response':[],
                       'description':'Failed to fetch revenue accounts records. {}'.format(error)}
            return jsonify(message)
        
        
    def get_discount_accounts(self, user):
        details = request.get_json()

        if details == None:
            message = {'status':401,
                       'description':'Request data is missing some details!'}
            return jsonify(message)

         #Try except block to handle data extraction
        try:                        
            #Get assets accounts            
            discount_data = DiscountReports.get_discount_accounts(self, user, details)
            # print(discount_data['response'][0])
            if int(discount_data['status']) == 200:
                discount_accounts = discount_data['response'][0]
                total_discount_accounts_balance = discount_data['response'][1]
                message = {'status':200,
                           'response':[discount_accounts,total_discount_accounts_balance],
                           'description':'Report details was fetched successfully'}

                return jsonify(message)
            
            else:
                message = {'status':discount_data['status'],
                           'response':[],
                           'description':'Report was not found'}

                return jsonify(message)


        except Exception as error:
            message = {'status':501,
                       'response':[],
                       'description':'Failed to fetch discount accounts records. {}'.format(error)}
            return jsonify(message)
        
    def get_cog_accounts(self, user):
        details = request.get_json()

        if details == None:
            message = {'status':401,
                       'description':'Request data is missing some details!'}
            return jsonify(message)

         #Try except block to handle data extraction
        try:                        
            #Get cog accounts            
            cog_data = CogReports.get_cog_accounts(self, user, details)
            # print(cog_data['response'][0])
            if int(cog_data['status']) == 200:
                cog_accounts = cog_data['response'][0]
                total_cog_accounts_balance = cog_data['response'][1]
                message = {'status':200,
                           'response':[cog_accounts, total_cog_accounts_balance],
                           'description':'Report details was fetched successfully'}

                return jsonify(message)
            
            else:
                message = {'status':cog_data['status'],
                           'description':'Report was not found'}

                return jsonify(message)


        except Exception as error:
            message = {'status':501,
                       'description':'Failed to fetch cog accounts records one. {}'.format(error)}
            return jsonify(message)
        
    def get_expenses_accounts(self, user):
        details = request.get_json()

        if details == None:
            message = {'status':401,
                       'description':'Request data is missing some details!'}
            return jsonify(message)

         #Try except block to handle data extraction
        try:                        
            #Get expenses accounts            
            expenses_data = ExpensesReports.get_expenses_accounts(self, user, details)
            if int(expenses_data['status']) == 200:
                expenses_accounts = expenses_data['response'][0]
                total_expenses_accounts_balance = expenses_data['response'][1]
                message = {'status':200,
                           'response':[expenses_accounts, total_expenses_accounts_balance],
                           'description':'Report details was fetched successfully'}

                return jsonify(message)
            
            else:
                message = {'status':expenses_data['status'],
                           'description':'Report was not found'}

                return jsonify(message)


        except Exception as error:
            message = {'status':501,
                       'description':'Failed to fetch expenses accounts records one. {}'.format(error)}
            return jsonify(message)

    def get_other_income_accounts(self, user):
        details = request.get_json()

        if details == None:
            message = {'status':401,
                       'description':'Request data is missing some details!'}
            return jsonify(message)

         #Try except block to handle data extraction
        try:                        
            #Get other income accounts            
            otherincome_data = OtherIncomeReports.get_other_income_accounts(self, user, details)
            if int(otherincome_data['status']) == 200:
                otherincome_accounts = otherincome_data['response'][0]
                total_otherincome_accounts_balance = otherincome_data['response'][1]
                message = {'status':200,
                           'response':[otherincome_accounts, total_otherincome_accounts_balance],
                           'description':'Report details was fetched successfully'}

                return jsonify(message)
            
            else:
                message = {'status':otherincome_data['status'],
                           'description':'Report was not found'}

                return jsonify(message)


        except Exception as error:
            message = {'status':501,
                       'description':'Failed to fetch other income accounts records one. {}'.format(error)}
            return jsonify(message)
        
        
    def get_other_expenses_accounts(self, user):
        details = request.get_json()

        if details == None:
            message = {'status':401,
                       'description':'Request data is missing some details!'}
            return jsonify(message)

         #Try except block to handle data extraction
        try:                        
            #Get other expenses accounts            
            otherexpenses_data = OtherExpensesReports.get_other_expenses_accounts(self, user, details)
            if int(otherexpenses_data['status']) == 200:
                otherexpenses_accounts = otherexpenses_data['response'][0]
                total_otherexpenses_accounts_balance = otherexpenses_data['response'][1]
                message = {'status':200,
                           'response':[otherexpenses_accounts, total_otherexpenses_accounts_balance],
                           'description':'Report details was fetched successfully'}

                return jsonify(message)
            
            else:
                message = {'status':otherexpenses_data['status'],
                           'description':'Report was not found'}

                return jsonify(message)

        except Exception as error:
            message = {'status':501,
                       'description':'Failed to fetch other expenses accounts records one. {}'.format(error)}
            return jsonify(message)