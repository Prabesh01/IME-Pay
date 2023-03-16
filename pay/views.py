from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
import requests
import config
import uuid
import base64
from .models import Transaction
import json
import datetime
import pytz
tz_NP = pytz.timezone('Asia/Kathmandu')

def home(req):
    if req.GET:
        try:
            reply=base64.b64decode(req.GET.get('data')).decode('utf-8').split('|')
            if len(reply)!=7:
                return redirect('home')          
        except:
            return redirect('home') 
        # strictly check if a user resends past data. dont precess if ResponseCode already in db
        dupcheck=Transaction.objects.filter(RefId=reply[4],TokenId=reply[6],TranAmount=reply[5])
        if len(dupcheck)<=0:
            messages.add_message(req, messages.WARNING, "This payment doesn't exist")
            return redirect('home')          
        if dupcheck.values()[0]['ImeTxnStatus']!=None:
            messages.add_message(req, messages.WARNING, 'This payment was already proceed')
            return redirect('home')          
        if reply[0]==0 or reply[0]=='0':
            dupcheck.update(TransactionId=reply[3], Msisdn=reply[2],ImeTxnStatus='5',ResponseDate = datetime.datetime.now(tz_NP))
            r=requests.post('https://stg.imepay.com.np:7979/api/Web/Confirm',auth=(config.Apiuser, config.Password),headers={'Module':base64.b64encode(config.Module.encode('ascii')).decode('ascii')},json={"MerchantCode":config.MerchantCode,"RefId":reply[4],"TokenId":reply[6],"TransactionId":reply[3],"Msisdn":reply[2]})
            r=r.json()
            if r['ResponseCode']==0 or r['ResponseCode']=='0':
                dupcheck.update(ImeTxnStatus=r['ResponseCode'],ResponseDate = datetime.datetime.now(tz_NP))            
                messages.add_message(req, messages.SUCCESS, 'Payment Sucess!')
            else:
                messages.add_message(req, messages.INFO, r['ResponseDescription'])
            return redirect('home')
        if reply[0]==2 or reply[0]=='2':
            try:
                dupcheck.update(TransactionId=reply[3], Msisdn=reply[2],ImeTxnStatus=reply[0],ResponseDate = datetime.datetime.now(tz_NP))
            except:
                pass
            r=requests.post('https://stg.imepay.com.np:7979/api/Web/Recheck',auth=(config.Apiuser, config.Password),headers={'Module':base64.b64encode(config.Module.encode('ascii')).decode('ascii')},json={"MerchantCode":config.MerchantCode,"RefId":reply[4],"TokenId":reply[6]})
            r=r.json()
            if r['ResponseCode']==0 or r['ResponseCode']=='0':
                dupcheck.update(TransactionId=r['TransactionId'], Msisdn=r['Msisdn'],ImeTxnStatus=r['ResponseCode'],ResponseDate = datetime.datetime.now(tz_NP))
                messages.add_message(req, messages.SUCCESS, 'Payment Sucess!')
            else:
                messages.add_message(req, messages.ERROR, reply[1])
            return redirect('home')
        else:
            dupcheck.delete()
            messages.add_message(req, messages.ERROR, reply[1])
            return redirect('home')
    else:
        r=requests.post('https://stg.imepay.com.np:7979/api/Web/GetToken',auth=(config.Apiuser, config.Password),headers={'Module':base64.b64encode(config.Module.encode('ascii')).decode('ascii')},json={"MerchantCode":config.MerchantCode,"Amount":"15","RefId":str(uuid.uuid1())})
        try:
            r=r.json()
            Transaction(TranAmount=r['Amount'], RefId=r['RefId'],TokenId=r['TokenId'],RequestDate = datetime.datetime.now(tz_NP)).save()
        except:
            messages.add_message(req, messages.ERROR, 'Sth went wrong. Please try again!')
            return HttpResponse("Something went wrong! Report this issue to owner. Or visit some time later.")
        messages.add_message(req, messages.INFO, 'NRs. 15')
        data=f"{r['TokenId']}|{config.MerchantCode}|{r['RefId']}|{r['Amount']}|GET|{req.build_absolute_uri()}|{req.build_absolute_uri()}"
        return render(req, 'home.html',{'url': 'https://stg.imepay.com.np:7979/WebCheckout/Checkout?data='+base64.b64encode(data.encode('ascii')).decode('ascii')})