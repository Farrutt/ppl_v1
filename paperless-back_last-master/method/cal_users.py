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

def email_to_business(email):
    tmp_email = email
    tmplist_cardnum = []
    r_data = select_4().select_data_business_v1(tmp_email)
    if r_data['result'] == 'OK':
        tmpdata = r_data['data']
        for i in range(len(tmpdata)):
            tmpbiz_infomation = tmpdata[i]['biz_information']
            if tmpbiz_infomation != None:
                tmpbiz_infomation = eval(tmpbiz_infomation)
                tmpbiz_detail = tmpbiz_infomation['biz_detail']
                for n in range(len(tmpbiz_detail)):
                    tmpgetbiz = tmpbiz_detail[n]['getbiz']
                    tmpid_card_num = tmpgetbiz[0]['id_card_num']
                    if tmpid_card_num not in tmplist_cardnum:
                        tmplist_cardnum.append(tmpid_card_num)
        return (tmplist_cardnum)

def email_data_business_v1(email):
    try:
        tmp_email = email
        tmplist_cardnum = []
        search_email = "%'{}'%".format(email)
        with engine.connect() as connection:
            result = connection.execute(text('SELECT "biz_information" FROM "tb_citizen_Login" WHERE "citizen_data" LIKE :email'),email=search_email)
            connection.close()
        query_result = [dict(row) for row in result]
        if query_result != []:
            for i in range(len(query_result)):
                tmpbiz_infomation = query_result[i]['biz_information']
                if tmpbiz_infomation != None:
                    tmpbiz_infomation = eval(tmpbiz_infomation)
                    tmpbiz_detail = tmpbiz_infomation['biz_detail']
                    for n in range(len(tmpbiz_detail)):
                        tmpgetbiz = tmpbiz_detail[n]['getbiz']
                        tmpid_card_num = tmpgetbiz[0]['id_card_num']
                        if tmpid_card_num not in tmplist_cardnum:
                            tmplist_cardnum.append(tmpid_card_num)
            return ({'result':'OK','data': tmplist_cardnum})
        else:
            return ({'result':'ER','messageER': 'Not found email'})
    except Exception as e:
        print(str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200