#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.publicqrcode import *
from method.document import *
from method.verify import *
from method.callserver import *
from controller.mail_string import *
from controller.validate import *
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *
from api.memory import *
from method.sftp_fucn import *
from method.callwebHook import *



if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less
elif type_product =='poc':
    status_methods = paper_less


@status_methods.route('/api/v1/schedule_approvedocument', methods=['GET'])
def test_approve_check_api_v1():
    arremail_one = []
    tmparr_insertdata = []
    arremail_one_1 = []
    tmparr_updatedata = []
    tmparr_updatedata_sendchat = []
    list_email = []
    list_email_db = []
    list_email_send = []
    result_2 = []
    result_data = select_3().select_status_document_v1()
    # return {'d':result_data}
    # for z in range(len(result_data)):
    #     print(len(result_data[z]['sid']),result_data[z]['email'])
    # return {'result':result_data}
    for x in range(len(result_data)):
        list_email.append(result_data[x]['email'])
    if len(result_data) != 0:        
        status_chat = 'FAIL'
        ts_2 = int(time.time())
        st_2 = datetime.datetime.fromtimestamp(ts_2).strftime('%d/%b/%Y %H:%M:%S')
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        result_select = select_3().select_data_alert_v1(st_2)
        if result_select['result'] == 'OK':
            for y in range(len(result_select['messageText'])) :
                list_email_db.append(result_select['messageText'][y]['email'])
            for i in range(len(list_email)):
                if list_email[i] not in list_email_db :
                    arr_insertdata = []
                    tmpemail_one = result_data[i]['email']
                    tmpdoc_id = result_data[i]['doc_id']
                    tmpsid = str(result_data[i]['sid'])
                    tmpnoti_document_hour = result_data[i]['noti_document_hour']
                    tmpnoti_time_timestamp = (result_data[i]['noti_time_timestamp'] + 60 * 60 * tmpnoti_document_hour)
                    tmpnoti_time_timestamp_string = datetime.datetime.fromtimestamp(tmpnoti_time_timestamp).strftime('%d/%b/%Y %H:%M:%S')
                    tmpnoti_time_timestamp = result_data[i]['noti_time_timestamp']
                    tmpstr = 'เอกสารค้างที่รอคุณอนุมัติ' + '\n'
                    tmp_doc_id =  result_data[i]['doc_id']
                    tmpstr += 'จำนวนเอกสารทั้งหมด ' + str(len(tmp_doc_id))
                    # for u in range(len(tmp_doc_id)):
                    #     tmpstr += str(u+1) + '. ' + tmp_doc_id[u] + '\n'
                    token_bot = token_service
                    botchat_id = bot_id
                    status_chat = 'ACTIVE'
                    result_chat = send_messageToChat_v5(tmpstr,tmpemail_one,token_bot,botchat_id,"")
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                    ts_1 = int(time.time()) + 86400
                    st_1 = datetime.datetime.fromtimestamp(ts_1).strftime('%d/%b/%Y %H:%M:%S')
                    arr_insertdata.append(tmpemail_one)
                    arr_insertdata.append(st)
                    arr_insertdata.append(tmpsid)
                    arr_insertdata.append(status_chat)
                    arr_insertdata.append(st)
                    arr_insertdata.append(tmpnoti_time_timestamp_string)
                    tuple_arr_insertdata = tuple(arr_insertdata)
                    tmparr_insertdata.append(tuple_arr_insertdata)
            if len(tmparr_insertdata) != 0:
                insert_3().insert_data_alert_documentlog_v2(tmparr_insertdata)
        if result_select['result'] == 'OK':
            tmp_message = result_select['messageText']
            tmparr_insertdata = []
            for v in range(len(tmp_message)):
                tmpemail_one_01 = tmp_message[v]['email']
                for i in range(len(result_data)):
                    tmpemail_one_02 = result_data[i]['email']
                    tmpdoc_id = result_data[i]['doc_id']
                    tmpsid = str(result_data[i]['sid'])
                    tmpnoti_document_hour = result_data[i]['noti_document_hour']
                    tmpnoti_time_timestamp = (result_data[i]['noti_time_timestamp'] + 60 * 60 * tmpnoti_document_hour)
                    tmpnoti_time_timestamp_string = datetime.datetime.fromtimestamp(tmpnoti_time_timestamp).strftime('%d/%b/%Y %H:%M:%S')
                    tmpstr = 'เอกสารค้างที่รอคุณอนุมัติ' + '\n'
                    tmp_doc_id =  result_data[i]['doc_id']
                    tmpstr += 'จำนวนเอกสารทั้งหมด ' + str(len(tmp_doc_id))
                    # for u in range(len(tmp_doc_id)):
                    #     tmpstr += str(u+1) + '. ' + tmp_doc_id[u] + '\n'
                    token_bot = token_service
                    botchat_id = bot_id
                    if tmpemail_one_02 == tmpemail_one_01:
                        arr_update_chat = []
                        result_chat = send_messageToChat_v5(tmpstr,tmpemail_one_02,token_bot,botchat_id,"")
                        status_chat = 'ACTIVE'
                        ts = int(time.time())
                        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                        ts_1 = int(time.time()) + 86400
                        st_1 = datetime.datetime.fromtimestamp(ts_1).strftime('%d/%b/%Y %H:%M:%S')
                        arr_update_chat.append(st)
                        arr_update_chat.append(tmpnoti_time_timestamp_string)
                        arr_update_chat.append(st)
                        arr_update_chat.append(tmpemail_one_02)
                        tuple_arr_updatedatachat = tuple(arr_update_chat)
                        tmparr_updatedata_sendchat.append(tuple_arr_updatedatachat)
                    else:
                        arremail_one_1.append(tmpemail_one_02)
            if len(tmparr_updatedata_sendchat) != 0:
                update_3().update_data_alert_documentlog_sendchat_v1(tmparr_updatedata_sendchat)
            if len(arremail_one_1) != 0:
                for i in range(len(result_data)):
                    arr_updatedata = []
                    tmpemail_one = result_data[i]['email']
                    tmpdoc_id = result_data[i]['doc_id']
                    tmpsid = str(result_data[i]['sid'])
                    tmpnoti_document_hour = result_data[i]['noti_document_hour']
                    tmpnoti_time_timestamp = (result_data[i]['noti_time_timestamp'] + 60 * 60 * tmpnoti_document_hour)
                    tmpnoti_time_timestamp_string = datetime.datetime.fromtimestamp(tmpnoti_time_timestamp).strftime('%d/%b/%Y %H:%M:%S')
                    tmpstr = 'เอกสารค้างที่รอคุณอนุมัติ' + '\n'
                    tmp_doc_id =  result_data[i]['doc_id']
                    tmpstr += 'จำนวนเอกสารทั้งหมด ' + str(len(tmp_doc_id))
                    # for u in range(len(tmp_doc_id)):
                    #     tmpstr += str(u+1) + '. ' + tmp_doc_id[u] + '\n'
                    token_bot = token_service
                    botchat_id = bot_id
                    status_chat = 'ACTIVE'
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                    ts_1 = int(time.time()) + 86400
                    st_1 = datetime.datetime.fromtimestamp(ts_1).strftime('%d/%b/%Y %H:%M:%S')
                    arr_updatedata.append(tmpsid)
                    arr_updatedata.append(st)
                    arr_updatedata.append(tmpnoti_time_timestamp_string)
                    arr_updatedata.append(tmpemail_one)
                    tuple_arr_updatedata = tuple(arr_updatedata)
                    tmparr_updatedata.append(tuple_arr_updatedata)   
            update_3().update_data_alert_documentlog_v2(tmparr_updatedata)            
        else:            
            for i in range(len(result_data)):
                tmpemail_one = result_data[i]['email']
                tmpdoc_id = result_data[i]['doc_id']
                tmpsid = str(result_data[i]['sid'])
                tmpstr = 'เอกสารค้างที่รอคุณอนุมัติ' + '\n'
                tmp_doc_id =  result_data[i]['doc_id']
                tmpstr += 'จำนวนเอกสารทั้งหมด ' + str(len(tmp_doc_id))
                # for u in range(len(tmp_doc_id)):
                #     tmpstr += str(u+1) + '. ' + tmp_doc_id[u] + '\n'
                token_bot = token_service
                botchat_id = bot_id
                arremail_one.append(tmpemail_one)
            Tuple_arrmail = tuple(arremail_one)
            result_select = select_3().select_data_alert_documentlog_v1(Tuple_arrmail,st)
            if result_select['result'] == 'OK':
                tmpmessage = result_select['messageText']
                for x in range(len(tmpmessage)):
                    tmpemailone = tmpmessage[x]['email']
                    arremail_one_1.append(tmpemailone)
                for i in range(len(result_data)):
                    tmpemail_one = result_data[i]['email']
                    if tmpemail_one not in arremail_one_1:
                        arr_insertdata = []
                        tmpemail_one = result_data[i]['email']
                        tmpdoc_id = result_data[i]['doc_id']
                        tmpsid = str(result_data[i]['sid'])
                        tmpnoti_document_hour = result_data[i]['noti_document_hour']
                        tmpnoti_time_timestamp = (result_data[i]['noti_time_timestamp'] + 60 * 60 * tmpnoti_document_hour)
                        tmpnoti_time_timestamp_string = datetime.datetime.fromtimestamp(tmpnoti_time_timestamp).strftime('%d/%b/%Y %H:%M:%S')
                        tmpnoti_time_timestamp = result_data[i]['noti_time_timestamp']
                        tmpstr = 'รายการเอกสารค้างที่รอคุณอนุมัติ' + '\n'
                        tmp_doc_id =  result_data[i]['doc_id']
                        tmpstr += 'จำนวนเอกสารทั้งหมด ' + str(len(tmp_doc_id)) +'\n\n'
                        for u in range(len(tmp_doc_id)):
                            tmpstr += str(u+1) + '. ' + tmp_doc_id[u] + '\n'
                        token_bot = token_service
                        botchat_id = bot_id
                        status_chat = 'ACTIVE'
                        result_chat = send_messageToChat_v5(tmpstr,tmpemail_one,token_bot,botchat_id,"")
                        ts = int(time.time())
                        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                        ts_1 = int(time.time()) + 86400
                        st_1 = datetime.datetime.fromtimestamp(ts_1).strftime('%d/%b/%Y %H:%M:%S')
                        arr_insertdata.append(tmpemail_one)
                        arr_insertdata.append(st)
                        arr_insertdata.append(tmpsid)
                        arr_insertdata.append(status_chat)
                        arr_insertdata.append(st)
                        arr_insertdata.append(tmpnoti_time_timestamp_string)
                        tuple_arr_insertdata = tuple(arr_insertdata)
                        tmparr_insertdata.append(tuple_arr_insertdata)
                    else:
                        arr_updatedata = []
                        tmpemail_one = result_data[i]['email']
                        tmpdoc_id = result_data[i]['doc_id']
                        tmpsid = str(result_data[i]['sid'])
                        tmpnoti_document_hour = result_data[i]['noti_document_hour']
                        tmpnoti_time_timestamp = (result_data[i]['noti_time_timestamp'] + 60 * 60 * tmpnoti_document_hour)
                        tmpnoti_time_timestamp_string = datetime.datetime.fromtimestamp(tmpnoti_time_timestamp).strftime('%d/%b/%Y %H:%M:%S')
                        tmpstr = 'เอกสารค้างที่รอคุณอนุมัติ' + '\n'
                        tmp_doc_id =  result_data[i]['doc_id']
                        tmpstr += 'จำนวนเอกสารทั้งหมด ' + str(len(tmp_doc_id))
                        for u in range(len(tmp_doc_id)):
                            tmpstr += str(u+1) + '. ' + tmp_doc_id[u] + '\n'
                        token_bot = token_service
                        botchat_id = bot_id
                        status_chat = 'ACTIVE'
                        ts = int(time.time())
                        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                        ts_1 = int(time.time()) + 86400
                        st_1 = datetime.datetime.fromtimestamp(ts_1).strftime('%d/%b/%Y %H:%M:%S')
                        arr_updatedata.append(tmpsid)
                        arr_updatedata.append(st)       
                        arr_updatedata.append(tmpnoti_time_timestamp_string)
                        arr_updatedata.append(tmpemail_one)                 
                        tuple_arr_updatedata = tuple(arr_updatedata)
                        tmparr_updatedata.append(tuple_arr_updatedata)
                if len(tmparr_insertdata) != 0:
                    insert_3().insert_data_alert_documentlog_v2(tmparr_insertdata)
                if len(tmparr_updatedata) != 0:
                    update_3().update_data_alert_documentlog_v2(tmparr_updatedata)
            else:
                for i in range(len(result_data)):
                    arr_insertdata = []
                    tmpemail_one = result_data[i]['email']
                    tmpdoc_id = result_data[i]['doc_id']
                    tmpsid = str(result_data[i]['sid'])
                    tmpnoti_document_hour = result_data[i]['noti_document_hour']
                    tmpnoti_time_timestamp = (result_data[i]['noti_time_timestamp'] + 60 * 60 * tmpnoti_document_hour)
                    tmpnoti_time_timestamp_string = datetime.datetime.fromtimestamp(tmpnoti_time_timestamp).strftime('%d/%b/%Y %H:%M:%S')
                    tmpstr = 'เอกสารค้างที่รอคุณอนุมัติ' + '\n'
                    tmp_doc_id =  result_data[i]['doc_id']
                    tmpstr += 'จำนวนเอกสารทั้งหมด ' + str(len(tmp_doc_id))
                    token_bot = token_service
                    botchat_id = bot_id
                    result_chat = send_messageToChat_v5(tmpstr,tmpemail_one,token_bot,botchat_id,"")
                    status_chat = 'ACTIVE'
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                    ts_1 = int(time.time()) + 86400
                    st_1 = datetime.datetime.fromtimestamp(ts_1).strftime('%d/%b/%Y %H:%M:%S')
                    arr_insertdata.append(tmpemail_one)
                    arr_insertdata.append(st)
                    arr_insertdata.append(tmpsid)
                    arr_insertdata.append(status_chat)
                    arr_insertdata.append(st)
                    arr_insertdata.append(tmpnoti_time_timestamp_string)
                    # print(arr_insertdata)
                    tuple_arr_insertdata = tuple(arr_insertdata)
                    tmparr_insertdata.append(tuple_arr_insertdata)
                insert_3().insert_data_alert_documentlog_v2(tmparr_insertdata)
    return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200


