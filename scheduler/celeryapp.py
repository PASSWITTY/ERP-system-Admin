try:
    from flask import Flask
    from celery import Celery
    from celery.schedules import crontab
    from datetime import timedelta
except Exception as e:
    print("Error : {} ".format(e))


def make_celery(app):
    celery = Celery('scheduler' ,
                    include=['scheduler.tasks'],
                    backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    
    app.config.timezone = 'EAT'

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    app.config['CELERYBEAT_SCHEDULE'] = {
    
        'cronjob_queue_demandnote': {
            'task': 'cronjob_queue_demandnote',
            'schedule': timedelta(seconds=120)
            },
        
        'cronjob_process_demandnote': {
            'task': 'cronjob_process_demandnote',
            'schedule': timedelta(seconds=120)
            },
        
        'cronjob_post_demandnote': {
            'task': 'cronjob_post_demandnote',
            'schedule': timedelta(seconds=120)
            },
                
        'cronjob_queue_loan_rollover_fee': {
            'task': 'cronjob_queue_loan_rollover_fee',
            'schedule': timedelta(seconds=120)
            },
        
        'cronjob_process_rollover_fee': {
            'task': 'cronjob_process_rollover_fee',
            'schedule': timedelta(seconds=120)
            },
        
        'cronjob_queue_defaulted_loan_fines': {
            'task': 'cronjob_queue_defaulted_loan_fines',
            'schedule': timedelta(seconds=120)
            },
        
        'cronjob_process_defaulted_loan_fines': {
            'task': 'cronjob_process_defaulted_loan_fines',
            'schedule': timedelta(seconds=120)
            },
                                
        'cronjob_process_get_mpesa_b2c_balance': {
            'task': 'cronjob_process_get_mpesa_b2c_balance',
            'schedule': timedelta(seconds=120)
            },
        
        'cronjob_process_loan_payment_remainder_sms': {
            'task': 'cronjob_process_loan_payment_remainder_sms',
            'schedule': timedelta(seconds=120)
            },
        
        'cronjob_process_send_loan_payment_remainder_sms': {
            'task': 'cronjob_process_send_loan_payment_remainder_sms',            
            'schedule': timedelta(seconds=120)
            
            },
        
        'cronjob_process_send_reducing_balance_loan_payment_remainder_sms': {
            'task': 'cronjob_process_send_reducing_balance_loan_payment_remainder_sms',            
            'schedule': timedelta(seconds=120)
            
            },
        
        'cronjob_process_loan_payment_remainder_eveduedate_sms': {
            'task': 'cronjob_process_loan_payment_remainder_eveduedate_sms',
            'schedule': timedelta(seconds=120)
            },
        
        'cronjob_process_create_okoa_airtime_loan': {
            'task': 'cronjob_process_create_okoa_airtime_loan',
            'schedule': timedelta(seconds=300)
            },
        
        'cronjob_process_loan_defaulted_fines_repayment_using_wallet_balance': {
            'task': 'cronjob_process_loan_defaulted_fines_repayment_using_wallet_balance',
            'schedule': timedelta(seconds=120)
            },
        
        'cronjob_process_loan_rollover_fee_repayment_using_wallet_balance': {
            'task': 'cronjob_process_loan_rollover_fee_repayment_using_wallet_balance',
            'schedule': timedelta(seconds=120)
            },
        
        'cronjob_process_loan_demandnote_repayment_using_wallet_balance': {
            'task': 'cronjob_process_loan_demandnote_repayment_using_wallet_balance',
            'schedule': timedelta(seconds=120)
            },
        
        'cronjob_process_loan_repayment_using_wallet_balance': {
            'task': 'cronjob_process_loan_repayment_using_wallet_balance',
            'schedule': timedelta(seconds=120)
            },
        
        

        # 'Every-15-seconds': {
        #     'task': 'return_that_thing',
        #     'schedule': timedelta(seconds=15)
        #     },

    }

    
    celery.conf.update(app.config)
    return celery