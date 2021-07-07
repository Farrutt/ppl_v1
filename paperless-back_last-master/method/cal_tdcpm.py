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

def call_service_pettycash(sid):
    url = url_thaidotcompayment + '/Paperless/PettyCash/insertdata'
    tmp_data = {}
    list_data = []
    try:
        resp_data = select_1().select_info_document(sid)
        if resp_data['result'] == 'OK':
            tmp_query = resp_data['messageText']
            for x in range(len(tmp_query)):
                result = data_doc(tmp_query[x]['data_document'])
                doc_id_ppl = (tmp_query[x]['doc_id'])
                # print ('doc_id_ppl:',doc_id_ppl)
                if result['result'] == 'OK':
                    tmp_sub = result['messageText']['sub']
                    if tmp_sub == 'eformppl':
                        tmp_json = result['messageText']
                        data_json_key = tmp_json['eform_data']
                        # print ('data_json_key:',data_json_key)
                        for i in range(len(data_json_key)):
                            if data_json_key[i]['json_key'] == '11_Bank_Account':
                                Bank_Account = data_json_key[i]['value']
                            if data_json_key[i]['json_key'] == '6_Employee_Code':
                                Employee_Code = data_json_key[i]['value']
                            if data_json_key[i]['json_key'] == '4_Employee_Name':
                                Employee_Name = data_json_key[i]['value']
                            if data_json_key[i]['json_key'] == '5_Surname':
                                Employee_Name = Employee_Name + ' ' +data_json_key[i]['value']
                            if data_json_key[i]['json_key'] == '15_Total_Amount':
                                Total_Amount = data_json_key[i]['value']
                            if data_json_key[i]['json_key'] == '18_Detail':
                                Detail = data_json_key[i]['value']
                            if data_json_key[i]['json_key'] == '10_Email':
                                Email = data_json_key[i]['value']
                            if data_json_key[i]['json_key'] == '9_Tel':
                                Tel = data_json_key[i]['value']
                            if data_json_key[i]['json_key'] == '2_Doc_No':
                                Doc_No = data_json_key[i]['value']
                        tmp_data = {
                            "BankCode":"006",
                            "Bank_Account":Bank_Account,
                            "Employee_Code":Employee_Code,
                            "Employee_Name":Employee_Name,
                            "Total_Amount":Total_Amount,
                            "Detail":Detail,
                            "Email":Email,
                            "Tel":Tel,
                            "Doc_No":Doc_No,
                            "doc_number_paperless":doc_id_ppl
                        }
                        list_data.append(tmp_data)
                        tmp_body = {
                            "count" : 1,
                            "data" : list_data
                        }
                        # print (tmp_json)
                        result_call_serv = callPost_Test(url,tmp_body)
                        print ('result_call_serv:',result_call_serv['messageText'].json())
                        return result_call_serv['messageText'].json()
                        # return tmp_body
                    else:
                        return {'result':'ER','messageText':'Not eformppl'}
                else:
                    return {'result':'ER','messageText':'decode fails'}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':str(e)}
        
def call_service_pettycash_multi(id_group):
    url = url_thaidotcompayment + '/Paperless/PettyCash/insertdata'
    # tmp_data = {}
    list_data = []
    try:
        result_sid = select_2().select_group_sid(id_group)
        list_sid = result_sid['messageText']['sid_group']
        list_sid = eval(list_sid)
        count = 0
        for s in range(len(list_sid)):
            sid = str(list_sid[s])
            resp_data = select_1().select_info_document(sid)
            if resp_data['result'] == 'OK':
                tmp_query = resp_data['messageText']
                for x in range(len(tmp_query)):
                    tmp_data = {}
                    result = data_doc(tmp_query[x]['data_document'])
                    doc_id_ppl = (tmp_query[x]['doc_id'])
                    print ('doc_id_ppl:',doc_id_ppl)
                    if result['result'] == 'OK':
                        tmp_sub = result['messageText']['sub']
                        if tmp_sub == 'eformppl':
                            tmp_json = result['messageText']
                            data_json_key = tmp_json['eform_data']
                            # print ('data_json_key:',data_json_key)
                            for i in range(len(data_json_key)):
                                if data_json_key[i]['json_key'] == '11_Bank_Account':
                                    Bank_Account = data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '6_Employee_Code':
                                    Employee_Code = data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '4_Employee_Name':
                                    Employee_Name = data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '5_Surname':
                                    Employee_Name = Employee_Name + ' ' +data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '15_Total_Amount':
                                    Total_Amount = data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '18_Detail':
                                    Detail = data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '10_Email':
                                    Email = data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '9_Tel':
                                    Tel = data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '2_Doc_No':
                                    Doc_No = data_json_key[i]['value']
                            tmp_data = {
                                "BankCode":"006",
                                "Bank_Account":Bank_Account,
                                "Employee_Code":Employee_Code,
                                "Employee_Name":Employee_Name,
                                "Total_Amount":Total_Amount,
                                "Detail":Detail,
                                "Email":Email,
                                "Tel":Tel,
                                "Doc_No":Doc_No,
                                "doc_number_paperless":doc_id_ppl
                            }
                            list_data.append(tmp_data)
                            count += 1
                        else:
                            return {'result':'ER','messageText':'Not eformppl'}
                    else:
                        return {'result':'ER','messageText':'decode fails'}
            else:
                pass
        tmp_body = {
            "count" : count,
            "data" : list_data
        }
        result_call_serv = callPost_Test(url,tmp_body)
        print ('result_call_serv:',result_call_serv['messageText'].json())
        return result_call_serv['messageText'].json()
        # return tmp_body
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':str(e)}

def call_service_pettycash_v1(sid=None,id_group=None):
    url = url_thaidotcompayment + '/Paperless/PettyCash/insertdata'
    # tmp_data = {}
    list_data = []
    list_sid = []
    count = 0
    try:
        if id_group != None and sid == None:
            result_sid = select_2().select_group_sid(id_group)
            list_sid = result_sid['messageText']['sid_group']
            list_sid = eval(list_sid)
            print ('list_sid_ID:',list_sid)
        elif sid != None and id_group == None:
            list_sid.append(sid)
            print ('list_sid_SID:',list_sid)
        elif sid != None and id_group != None:
            return 'invalid parameter'
        elif sid == None and id_group == None:
            return 'invalid parameter'
        for s in range(len(list_sid)):
            sid = str(list_sid[s])
            resp_data = select_1().select_info_document(sid)
            if resp_data['result'] == 'OK':
                tmp_query = resp_data['messageText']
                for x in range(len(tmp_query)):
                    tmp_data = {}
                    result = data_doc(tmp_query[x]['data_document'])
                    doc_id_ppl = (tmp_query[x]['doc_id'])
                    print ('doc_id_ppl:',doc_id_ppl)
                    if result['result'] == 'OK':
                        tmp_sub = result['messageText']['sub']
                        if tmp_sub == 'eformppl':
                            tmp_json = result['messageText']
                            data_json_key = tmp_json['eform_data']
                            # print ('data_json_key:',data_json_key)
                            for i in range(len(data_json_key)):
                                if data_json_key[i]['json_key'] == '11_Bank_Account':
                                    Bank_Account = data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '6_Employee_Code':
                                    Employee_Code = data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '4_Employee_Name':
                                    Employee_Name = data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '5_Surname':
                                    Employee_Name = Employee_Name + ' ' +data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '15_Total_Amount':
                                    Total_Amount = data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '18_Detail':
                                    Detail = data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '10_Email':
                                    Email = data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '9_Tel':
                                    Tel = data_json_key[i]['value']
                                if data_json_key[i]['json_key'] == '2_Doc_No':
                                    Doc_No = data_json_key[i]['value']
                            tmp_data = {
                                            "BankCode":"006",
                                            "Bank_Account":Bank_Account,
                                            "Employee_Code":Employee_Code,
                                            "Employee_Name":Employee_Name,
                                            "Total_Amount":Total_Amount,
                                            "Detail":Detail,
                                            "Email":Email,
                                            "Tel":Tel,
                                            "Doc_No":Doc_No,
                                            "doc_number_paperless":doc_id_ppl
                                        }
                            list_data.append(tmp_data)
                            count += 1
            else:
                pass
        tmp_body = {
            "count" : count,
            "data" : list_data
        }
        result_call_serv = callPost_Test(url,tmp_body)
        print ('result_call_serv:',result_call_serv['messageText'].json())
        return result_call_serv
        return tmp_body
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':str(e)}