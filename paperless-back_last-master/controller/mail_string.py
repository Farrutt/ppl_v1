#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config.lib import *
from db.db_method import *

def selection_email(json):
    try:
        arr_email = []
        for n in range(len(json)):
            if 'step_detail' in json[n]:
                arr_email_step = {}
                arr_email_step['step_num'] = (json[n]['step_num'])
                arr_email_step['email_result'] = []                
                for k in range(len(json[n]['step_detail'])):
                    if json[n]['step_detail'][k]['one_email'] != "":
                        if "A02" in json[n]['step_detail'][k]['activity_code']:
                            arr_email_step['email_result'].append({'email':json[n]['step_detail'][k]['one_email'],'status_chat':True})
                        else:
                            arr_email_step['email_result'].append({'email':json[n]['step_detail'][k]['one_email'],'status_chat':False})
            arr_email.append(arr_email_step) 
        return {'result':'OK','messageText':arr_email,'status_Code':200}
    except Exception as ex:
        return {'result':'ER','messageText':str(ex),'status_Code':200}

def selection_email_v2(json,maxStep,email):
    try:
        
        arr_email = []
        arr_email_step = {}
        if maxStep == 1:
            if 'step_detail' in json:
                print(json,maxStep,email)
                arr_email_step = {}
                arr_email_step['step_num'] = (json['step_num'])
                arr_email_step['email_result'] = []                
                for k in range(len(json['step_detail'])):
                    if str(json['step_detail'][k]['one_email']).lower() == 'me':
                        json['step_detail'][k]['one_email'] = email
                    print(json['step_detail'][k]['one_email'])          
                    if json['step_detail'][k]['one_email'] != "":
                        for n in range(len(json['step_detail'][k]['activity_code'])):
                            print(json['step_detail'][k]['activity_code'][n])
                            if 'A03' == json['step_detail'][k]['activity_code'][n]:
                                if json['step_detail'][k]['activity_status'][n] == 'Incomplete':
                                    status_property = 'signning'
                                elif json['step_detail'][k]['activity_status'][n] == 'Pending':
                                    status_property = 'approve'
                            print("A02" == json['step_detail'][k]['activity_code'][n])                        
                            if "A02" == json['step_detail'][k]['activity_code'][n]:                                                                                                            
                                arr_email_step['email_result'].append({'email':json['step_detail'][k]['one_email'],'status_chat':True,'property':status_property})
                            # else:
                            #     arr_email_step['email_result'].append({'email':json['step_detail'][k]['one_email'],'status_chat':False,'property':status_property})
            
            arr_email.append(arr_email_step)
        else:
            for n in range(len(json)):
                if 'step_detail' in json[n]:
                    arr_email_step = {}
                    arr_email_step['step_num'] = (json[n]['step_num'])
                    arr_email_step['email_result'] = []                
                    for k in range(len(json[n]['step_detail'])):
                        if str(json[n]['step_detail'][k]['one_email']).lower() == 'me':
                            json['step_detail'][k]['one_email'] = email   
                        if json[n]['step_detail'][k]['one_email'] != "":
                            for j in range(len(json[n]['step_detail'][k]['activity_code'])):
                                print(json[n]['step_detail'][k]['activity_code'][j])
                                if 'A03' == json[n]['step_detail'][k]['activity_code'][j]:
                                    if json[n]['step_detail'][k]['activity_status'][j] == 'Incomplete':
                                        status_property = 'signning'
                                    elif json[n]['step_detail'][k]['activity_status'][j] == 'Pending':
                                        status_property = 'approve'
                                print("A02" == json[n]['step_detail'][k]['activity_code'][j])                        
                                if "A02" == json[n]['step_detail'][k]['activity_code'][j]:                                                                                                            
                                    arr_email_step['email_result'].append({'email':json[n]['step_detail'][k]['one_email'],'status_chat':True,'property':status_property})
                            # if "A02" in json[n]['step_detail'][k]['activity_code']:
                            #     if json['step_detail'][k]['activity_status'][n] == 'Incomplete':
                            #         status_property = 'signning'
                            #     elif json['step_detail'][k]['activity_status'][n] == 'Pending':
                            #         status_property = 'approve'
                            #     arr_email_step['email_result'].append({'email':json[n]['step_detail'][k]['one_email'],'status_chat':True,'property':status_property})
                            # else:
                            #     if json['step_detail'][k]['activity_status'][n] == 'Incomplete':
                            #         status_property = 'signning'
                            #     elif json['step_detail'][k]['activity_status'][n] == 'Pending':
                            #         status_property = 'approve'
                            #     arr_email_step['email_result'].append({'email':json['step_detail'][k]['one_email'],'status_chat':False,'property':status_property})
                arr_email.append(arr_email_step) 
        return {'result':'OK','messageText':arr_email,'status_Code':200}
    except Exception as ex:
        return {'result':'ER','messageText':str(ex),'status_Code':200,'service':'_email_v2'}

def selection_email_JsonData(json_String_Data,maxStep,email):
    try:
        print(json_String_Data,maxStep,email)
        arr_email = []
        if maxStep == 1:
            if 'step_detail' in json_String_Data:
                arr_email_step = {}
                arr_email_step['step_num'] = (json_String_Data['step_num'])
                arr_email_step['email_result'] = []                
                for k in range(len(json_String_Data['step_detail'])):
                    # print(str(json_String_Data['step_detail'][k]['one_email']).lower())
                    if str(json_String_Data['step_detail'][k]['one_email']).lower() == 'me':
                        json_String_Data['step_detail'][k]['one_email'] = email
        else:
            for n in range(len(json_String_Data)):
                if 'step_detail' in json_String_Data[n]:
                    arr_email_step = {}
                    arr_email_step['step_num'] = (json_String_Data[n]['step_num'])
                    arr_email_step['email_result'] = []                
                    for k in range(len(json_String_Data[n]['step_detail'])):
                        # print(str(json_String_Data['step_detail'][k]['one_email']).lower())
                        if str(json_String_Data[n]['step_detail'][k]['one_email']).lower() == 'me':
                            json_String_Data[n]['step_detail'][k]['one_email'] = email
        # print('')
        # print(json_String_Data)
        return {'result':'OK','messageText':json_String_Data,'status_Code':200}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':str(e),'status_Code':200,'service':'_selection_email_JsonData_'}

def selection_email_insert(list_data,id_one_chat_to_msg):
    i = 0
    arr_result=[]
    try:
        for n in list_data:
            if n['result'] == 'OK':
                statusId = 'Y'
            if n['result'] == 'ER':
                statusId = 'ER'
            if n['result'] == 'NO':
                statusId = 'N'
            sendChat = n['sendChat']
            email_one = n['email']
            sidCode = n['sid']
            statusSign = 'N'
            step_num = n['step_num']
            urlsign = n['urlSign']
            try:
                propertyChat = str(n['property']).lower()
            except Exception as ex:
                propertyChat = None
            i = i + 1
            if i == 1:
                res_in = insert().insert_transactionChat(sidCode,statusId,str(i),email_one,statusSign,step_num,sendChat,urlsign,propertyChat,id_one_chat_to_msg)
            else:
                res_in = insert().insert_transactionChat(sidCode,statusId,str(i),email_one,statusSign,step_num,sendChat,urlsign,propertyChat,id_one_chat_to_msg)
            arr_result.append(res_in)
        return {'result':'OK','messageText':arr_result,'status_Code':200}
    except Exception as ex:
        return {'result':'ER','messageText':str(ex),'status_Code':200}

def selection_email_insert_v2(list_data):
    i = 0
    arr_result=[]
    print(len(list_data))
    try:
        for n in list_data:
            print(n)
            if n['result'] == 'OK':
                statusId = 'Y'
            if n['result'] == 'ER':
                statusId = 'ER'
            if n['result'] == 'NO':
                statusId = 'N'
            sendChat = n['sendChat']
            email_one = n['email']
            sidCode = n['sid']
            statusSign = 'N'
            step_num = n['step_num']
            urlsign = n['urlSign']
            id_one_chat_to_msg = n['id_chat']
            try:
                message_chat = n['message_chat']
            except Exception as e:
                message_chat = ''
            try:
                propertyChat = str(n['property']).lower()
            except Exception as e:
                propertyChat = None
            i = i + 1
            if i == 1:
                res_in = insert().insert_transactionChat(sidCode,statusId,str(i),email_one,statusSign,step_num,sendChat,urlsign,propertyChat,id_one_chat_to_msg)
            else:
                res_in = insert().insert_transactionChat(sidCode,statusId,str(i),email_one,statusSign,step_num,sendChat,urlsign,propertyChat,id_one_chat_to_msg)
            arr_result.append(res_in)
        return {'result':'OK','messageText':arr_result,'status_Code':200}
    except Exception as ex:
        return {'result':'ER','messageText':str(ex),'status_Code':200}
    
def check_sendToChat(list_data):
    k = 1
    i = 0
    listarr_check_statusSign = []
    listarr_check_stepNum = []
    listarr_check_transactionCode = []
    listarr_check_sidCode = []
    listarr_check_email_User = []
    listarr_check_idChat = []
    temp = ''
    tmp_list = []
    tmp_list_id_chat = []
    for n in list_data:
        if int(n['stepNum']) >= k:
            i = i + 1
            listarr_check_statusSign.append(n['statusSign'])
            listarr_check_email_User.append(n['email_User'])
            listarr_check_stepNum.append(n['stepNum'])
            listarr_check_transactionCode.append(str(n['transactionCode']))
            listarr_check_sidCode.append(n['sidCode'])
            listarr_check_idChat.append(n['id_chat'])
    for o in range(len(listarr_check_statusSign)):
        if listarr_check_statusSign[o] == 'Y':
            temp = {'statusSign':listarr_check_statusSign[o],'email_User':listarr_check_email_User[o],'stepNum':listarr_check_stepNum[o],'transactionCode':str(listarr_check_transactionCode[o]),'sid':str(listarr_check_sidCode[o]),'id_chat':str(listarr_check_idChat[o])}
            tmp_list.append(temp)
        elif listarr_check_statusSign[o] == 'R':
            temp = {'statusSign':listarr_check_statusSign[o],'email_User':listarr_check_email_User[o],'stepNum':listarr_check_stepNum[o],'transactionCode':str(listarr_check_transactionCode[o]),'sid':str(listarr_check_sidCode[o]),'id_chat':str(listarr_check_idChat[o])}
            tmp_list.append(temp)
        
    return {'result':'OK','msg':temp,'list_id_chat':tmp_list_id_chat}

def check_sendToChat_v2(list_data):
    try:
        k = 1
        i = 0
        listarr_check_statusSign = []
        listarr_check_stepNum = []
        listarr_check_transactionCode = []
        listarr_check_sidCode = []
        listarr_check_email_User = []
        listarr_check_idChat = []
        listarr_check_messageTaskChat = []
        listarr_check_messageTaskId = []
        temp = ''
        temp_1 = ''
        tmp_list = []
        tmp_list_id_chat = []
        tmp_list_data = []
        for n in list_data:
            if int(n['stepNum']) >= k:
                i = i + 1
                listarr_check_statusSign.append(n['statusSign'])
                listarr_check_email_User.append(n['email_User'])
                listarr_check_stepNum.append(n['stepNum'])
                listarr_check_transactionCode.append(str(n['transactionCode']))
                listarr_check_sidCode.append(n['sidCode'])
                listarr_check_idChat.append(n['id_chat'])
                listarr_check_messageTaskChat.append(n['messageTask_Chat'])
                listarr_check_messageTaskId.append(n['messageTask_Id'])
        for o in range(len(listarr_check_statusSign)):
            if listarr_check_statusSign[o] == 'Y':
                temp = {'statusSign':listarr_check_statusSign[o],'email_User':listarr_check_email_User[o],'stepNum':listarr_check_stepNum[o],'transactionCode':str(listarr_check_transactionCode[o]),'sid':str(listarr_check_sidCode[o]),'id_chat':str(listarr_check_idChat[o]),'messageTask_Chat':listarr_check_messageTaskChat[o],'messageTask_Id':listarr_check_messageTaskId[o]}
                tmp_list.append(temp)
            elif listarr_check_statusSign[o] == 'R':
                temp = {'statusSign':listarr_check_statusSign[o],'email_User':listarr_check_email_User[o],'stepNum':listarr_check_stepNum[o],'transactionCode':str(listarr_check_transactionCode[o]),'sid':str(listarr_check_sidCode[o]),'id_chat':str(listarr_check_idChat[o]),'messageTask_Chat':listarr_check_messageTaskChat[o],'messageTask_Id':listarr_check_messageTaskId[o]}
                tmp_list.append(temp)            
            elif listarr_check_statusSign[o] == 'N':
                temp_1 = {'statusSign':listarr_check_statusSign[o],'email_User':listarr_check_email_User[o],'stepNum':listarr_check_stepNum[o],'transactionCode':str(listarr_check_transactionCode[o]),'sid':str(listarr_check_sidCode[o]),'id_chat':str(listarr_check_idChat[o]),'messageTask_Chat':listarr_check_messageTaskChat[o],'messageTask_Id':listarr_check_messageTaskId[o]}
                tmp_list.append(temp_1)
        tmp_step_num_temp = int(temp['stepNum'])
        for u in range(len(tmp_list)):
            tmp_step_num = int(tmp_list[u]['stepNum'])
            if tmp_step_num == tmp_step_num_temp:
                tmp_id_chat = tmp_list[u]['id_chat']
                if tmp_id_chat not in tmp_list_id_chat:
                    tmp_list_id_chat.append(tmp_id_chat)
                tmp_list_data.append(tmp_list[u])
        return {'result':'OK','msg':temp,'list_id_chat':tmp_list_id_chat,'tmp_data':tmp_list_data}
    except Exception as e:
        insert().insert_tran_log_v1(str(e),'ER',"",'check_sendToChat_v2',"")
        return {'result':'ER','msg':[],'list_id_chat':[],'tmp_data':[]}
    