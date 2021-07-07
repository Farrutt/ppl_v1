# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from db.db_method_4 import *
from config.lib import *
from method.hashpy import *
from method.callserver import *
from method.access import *

def cal_taxId_v1(tax_id):
    ts_2 = int(time.time())
    year = datetime.datetime.fromtimestamp(ts_2).strftime('%Y')
    month = datetime.datetime.fromtimestamp(ts_2).strftime('%m')
    year = int(year)
    month = int(month)
    r = calendar.monthrange(year, month)[1]
    year = str(year)
    month = str(month)
    if len(month) == 1:
        month = '0' + month
    endday = str(r)
    if len(endday) == 1:
        endday = '0' + endday
    strday = '01'
    dayfrom = strday
    dayto = endday    
    dtm_from = year + "-" + month + "-" + dayfrom + ' ' + '00:00:00'
    dtm_to = year + "-" + month + "-" + dayto + ' ' + '23:59:59'
    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    tmptax_idarr = []
    tmpresult = []
    tmp_tlast = []
    r1 = select_4().select_transactionMax_business(tax_id)
    for i in range(len(r1)):
        tmpdata = r1[i]
        tmptax_id = tmpdata['tax_id']
        # tmptax_id = tmpdata['tax_id']
        tmptax_idarr.append(tmptax_id)
    lis_r = []
    r = select_4().select_transactionNow_business(tmptax_idarr,dtm_from,dtm_to)
    for m in range(len(r)):
        if r[m]['tax_id'] != None:
            if r[m]['transaction'] == '2':
                r[m]['count'] = (r[m]['count'] * 2)
                r[m-1]['count'] = r[m-1]['count'] + r[m]['count']
                r[m-1]['sum_filesize'] = r[m-1]['sum_filesize'] + r[m]['sum_filesize']
                r[m-1]['sum_filesize_storage'] = r[m-1]['sum_filesize_storage'] + r[m]['sum_filesize_storage']
                r.pop(m)
             
    for n in range(len(r)):
        for i in range(len(r1)):
            if r[n]['tax_id'] == r1[i]['tax_id']:
                r1[i]['count'] = r[n]['count']
                r1[i]['sum_filesize'] = int(r[n]['sum_filesize'])
                r1[i]['sum_filesize_storage'] = int(r[n]['sum_filesize_storage'])
                tmpresult.append(r1[i])
    # return ''
    for j in range(len(tmpresult)):
        tmpresult_totup = []
        tmpdata = tmpresult[j]
        if tmpdata['transactionmax'] == None:
            tmpdata['transactionmax'] = 0        
        if tmpdata['storagemax'] == None:
            tmpdata['storagemax'] = 0
        if tmpdata['count'] >= tmpdata['transactionmax']:
            tmpdata['status'] = False
        else:            
            tmpdata['status'] = True
        if 'sum_filesize' in tmpdata:
            tmpsum_storage =  int(tmpdata['sum_filesize']) + int(tmpdata['sum_filesize_storage'])
        tmpresult_totup.append(tmpdata['status'])
        tmpresult_totup.append(tmpdata['transactionmax'])
        tmpresult_totup.append(tmpdata['storagemax'])
        tmpresult_totup.append(st)     
        tmpresult_totup.append(tmpdata['count'])  
        tmpresult_totup.append(tmpsum_storage)     
        tmpresult_totup.append(tmpdata['tax_id']) 
        tmpresult_totup = tuple(tmpresult_totup)
        tmp_tlast.append(tmpresult_totup) 
    rupdate = update_4().update_status_business(tmp_tlast)
    return rupdate

def cal_Check_tax_id(tax_id):
    tmpstatus = True
    ts_2 = int(time.time())
    year = datetime.datetime.fromtimestamp(ts_2).strftime('%Y')
    month = datetime.datetime.fromtimestamp(ts_2).strftime('%m')
    year = int(year)
    month = int(month)
    r = calendar.monthrange(year, month)[1]
    year = str(year)
    month = str(month)
    if len(month) == 1:
        month = '0' + month
    endday = str(r)
    if len(endday) == 1:
        endday = '0' + endday
    strday = '01'
    dayfrom = strday
    dayto = endday    
    dtm_from = year + "-" + month + "-" + dayfrom + ' ' + '00:00:00'
    dtm_to = year + "-" + month + "-" + dayto + ' ' + '23:59:59'
    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    tmptax_idarr = []
    tmpresult = []
    tmp_tlast = []
    r1 = select_4().select_transactionMax_business(tax_id)
    for i in range(len(r1)):
        tmpdata = r1[i]
        tmptax_id = tmpdata['tax_id']
        # tmptax_id = tmpdata['tax_id']
        tmptax_idarr.append(tmptax_id)
    r = select_4().select_transactionNow_business(tmptax_idarr,dtm_from,dtm_to)
    for n in range(len(r)):
        for i in range(len(r1)):
            if r[n]['tax_id'] == r1[i]['tax_id']:
                r1[i]['count'] = r[n]['count']
                r1[i]['sum_filesize'] = int(r[n]['sum_filesize'])
                r1[i]['sum_filesize_storage'] = int(r[n]['sum_filesize_storage'])
                tmpresult.append(r1[i])
    for j in range(len(tmpresult)):
        tmpresult_totup = []
        tmpdata = tmpresult[j]
        if tmpdata['transactionmax'] == None:
            tmpdata['transactionmax'] = 0        
        if tmpdata['storagemax'] == None:
            tmpdata['storagemax'] = 0
        if tmpdata['count'] >= tmpdata['transactionmax']:
            tmpstatus = False
        else:            
            tmpstatus = True
    return tmpstatus
