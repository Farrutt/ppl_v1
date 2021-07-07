#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db.db_Class import *
from config.value import *
from method.access import *
from method.hashpy import *
from method.other import *
from config.lib import *
from db.db_method_1 import *
from method.cal_users import *
from method.callserver import *

def find_name_surename_by_username_TH_EN_list(username):
    try:
        search_dict = "%{}%".format(username)
        # query_name = paper_lesslogin.query.filter(paper_lesslogin.biz_information.contains(username[i])).first()
        with slave.connect() as connection:
            result = connection.execute(text(''' SELECT "biz_information" FROM "tb_citizen_Login" WHERE "username" =:name'''),name=username)
            connection.close()
        query_name = [dict(row) for row in result][0]
        # print ('query_name',query_name)
        # print (query_name)
        name_surename_en = ''
        name_surename_th = ''
        if query_name != None :
            biz_information = query_name['biz_information']
            biz_information_eval = eval(str(biz_information))
            name_en = biz_information_eval['first_name_eng']
            name_th = biz_information_eval['first_name_th']
            if name_en != None:
                name_surename_en += name_en
                surename_en = biz_information_eval['last_name_eng']
                name_surename_en += ' ' + surename_en
            else:
                name_surename_en = email
            if name_th != None:
                name_surename_th += name_th
                surename_th = biz_information_eval['last_name_th']
                name_surename_th += ' ' + surename_th
            else:
                name_surename_th = email
            tmp_dict = {
                'th':name_surename_th,
                'eng':name_surename_en
                }
            
        else:
            tmp_dict = {
                'th':email,
                'eng':email
                }
            
        return {'result':'OK','messageText':tmp_dict}
    except Exception as e:
        print (str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':str(e)}

def migrate_sender_name(tmp_dict):
    try:
        # print ('tmp_dict:',tmp_dict)
        tuple_list = []
        for j in range(len(tmp_dict)):
            sid = tmp_dict[j]['sid']
            send_user = tmp_dict[j]['send_user']
            result_name = find_name_surename_by_username_TH_EN_list(send_user)
            new_sender_name = result_name['messageText']
            # print ('new_sender_name:',new_sender_name)
            tmp_dict[j].update({'sender_name':new_sender_name})
            # print ('new_sender_name:',new_sender_name)
            tuple_tmp = (str(new_sender_name),sid)
            tuple_list.append(tuple_tmp)
        # print ('tuple_list:',tuple_list)
        result_update = update_4().update_sender_name_migrate(tuple_list)
        return {'result':'OK','messageText':result_update['messageText']}

    except Exception as e:
        print (str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':str(e)}

def migrate_tax_id(tmp_dict):
    try:
        # print ('tmp_dict:',tmp_dict)
        tuple_list = []
        for j in range(len(tmp_dict)):
            sid = tmp_dict[j]['sid']
            tax_id = tmp_dict[j]['tax_id']
            if tax_id == '5513213355654': 
                tuple_tmp = (str(tax_id),sid)
                tuple_list.append(tuple_tmp)
            else:
                pass
        # print ('tuple_list:',tuple_list)
        result_update = update_4().update_tax_id_migrate(tuple_list)
        return {'result':'OK','messageText':result_update['messageText']}
        # return {'result':'OK','messageText':'SUCCESS'}
    except Exception as e:
        print (str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':str(e)}
