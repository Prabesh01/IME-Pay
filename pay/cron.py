from django_cron import CronJobBase, Schedule
import requests
import config
import base64
from .models import Transaction
import json
import datetime
import pytz
tz_NP = pytz.timezone('Asia/Kathmandu')
from django.db.models import Q

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 0.01
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'pay.my_cron_job'

    def do(self):
        mydata=Transaction.objects.filter(Q(ImeTxnStatus=None) | Q(ImeTxnStatus=2)).values()
        for data in mydata:
            r=requests.post('https://stg.imepay.com.np:7979/api/Web/Recheck',auth=(config.Apiuser, config.Password),headers={'Module':base64.b64encode(config.Module.encode('ascii')).decode('ascii')},json={"MerchantCode":config.MerchantCode,"RefId":data['RefId'],"TokenId":data['TokenId']})
            r=r.json()
            if r['ResponseCode']==0 or r['ResponseCode']=='0':
                Transaction.objects.filter(RefId=data['RefId']).update(TransactionId=r['TransactionId'], Msisdn=r['Msisdn'],ImeTxnStatus=r['ResponseCode'],ResponseDate = datetime.datetime.now(tz_NP))
            else:
                if data['ImeTxnStatus']==None:
                    if (datetime.datetime.now(tz_NP)-data['RequestDate']).days<=0:
                        continue
                Transaction.objects.filter(RefId=data['RefId']).delete()