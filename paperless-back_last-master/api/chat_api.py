#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.publicqrcode import *
from method.document import *
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
from method.sftp_fucn import *
from method.callwebHook import *
from api.schedule_log import *

if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less




@status_methods.route('/api/chat', methods=['POST','GET'])
def chat_api():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            resCheck = checkToken(str(token_header).split(' ')[1])
            if resCheck['result'] == 'OK':
                pass
            else:
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        list_status_sendmail = []
        for n in range(len(dataJson)):
            if 'email' in dataJson[n] and 'url_sign' in dataJson[n] and 'tracking' in dataJson[n] and 'name_file' in dataJson[n] and len(dataJson[n]) == 4:
                res_search_frd = search_frd(dataJson[n]['email'])
                if res_search_frd['status'] == 'success':
                    print(res_search_frd)
                    res_send_onechat = send_url_sign(res_search_frd['friend']['user_id'],dataJson[n]['name_file'],dataJson[n]['tracking'],dataJson[n]['url_sign'])
                    print(res_send_onechat)
                    if  res_send_onechat['status'] == 'success':
                        list_status_sendmail.append({'result':'OK','messageText':'Send To OneChat OK!','status_Code':200,'status_for_email':dataJson[n]['email']})
                    else:
                        list_status_sendmail.append({'result':'ER','messageText':'Can,t Send To OneChat ER!','status_Code':200,'status_for_email':dataJson[n]['email']})
                else:
                    list_status_sendmail.append({'result':'ER','messageText':'Not Found Friend!!','status_Code':404,'status_for_email':dataJson[n]['email']})
            else:
                list_status_sendmail.append({'result':'ER','messageText':'Parameter Fail!','status_Code':404,'status_for_email':dataJson[n]['email']})
        return jsonify({'detail_sendchat':list_status_sendmail,'result':'OK','status_Code':200}),200
    elif request.method == 'GET':
        try:
            token_header = request.headers['Authorization']
            resCheck = checkToken(str(token_header).split(' ')[1])
            if resCheck['result'] == 'OK':
                pass
            else:
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        if (request.args.get('email')) != None:
            arr_mailre = []
            eval_arr = eval(request.args.get('email'))
            print(len((eval_arr)))
            for n in range(len((eval_arr))):
                print(eval_arr[n])
                json_onechat = {}
                emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", eval_arr[n])
                if emails is None:
                    return jsonify({'result':'ER','messageText':'ข้อมูล email ไม่ตรงตามรูปแบบ','status_Code':200}),200
                else:
                    pass
                try:
                    res_search_frd = search_frd(str(eval_arr[n]).replace(' ',''))
                    if 'result' in res_search_frd:
                        json_onechat['result'] = 'ER'
                        json_onechat['email'] = eval_arr[n]
                    elif 'status' in res_search_frd:
                        json_onechat['result'] = 'OK'
                        json_onechat['email'] = eval_arr[n]
                except KeyError as ex:
                    print(ex)
                arr_mailre.append(json_onechat)
            return jsonify({'result':'OK','messageText':arr_mailre,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/chat/v2', methods=['POST','GET'])
@token_required
def chat_api_v2():
    if request.method == 'POST':
        dataJson = request.json
        list_emailChat_log = []
        status_sendChat = []
        if 'type_service' in dataJson and 'data' in dataJson and 'sid' in dataJson and 'url_sign' in dataJson and 'tracking' in dataJson and 'name_file' in dataJson and len(dataJson) == 6:
            if str(dataJson['type_service']).lower()  == 'first':
                for n in range(len(dataJson['data'])):
                    data_tosender = dataJson['data']
                    if 'email' in data_tosender[n] and 'url_sign' in data_tosender[n] and 'tracking' in data_tosender[n] and 'name_file' in data_tosender[n] and 'message' in data_tosender[n] and 'step_num' in data_tosender[n] and 'sendChat' in data_tosender[n] and len(data_tosender[n]) == 7:
                        status_sendChat.append(data_tosender[n]['sendChat'])
                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                            res_search_frd = search_frd(data_tosender[n]['email'])
                            print(data_tosender[n]['step_num'])
                            if 'status' in res_search_frd:
                                if res_search_frd['status'] == 'success':
                                    res_send = send_url_tochat(res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'])
                                    if 'status' in res_send:
                                        if res_send['status'] == 'success':
                                            update().update_StatusOneChat(dataJson['sid'],data_tosender[n]['email'])
                                            list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat']})
                                        else:
                                           list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat']})
                                else:
                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat']})
                            else:
                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat']})
                        else:
                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat']})

                if True in status_sendChat:
                    result_logChat = selection_email_insert(list_emailChat_log)
                    if result_logChat['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':'Send To OneChat Successfully!','status_Code':200,'messageER':None})
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                else:
                    return jsonify({'result':'OK','messageText':'Not Found Send To OneChat!','status_Code':200,'messageER':None})
            elif str(dataJson['type_service']).lower() =='next':
                data_Url = dataJson['url_sign']
                data_name_file = dataJson['name_file']
                data_tracking = dataJson['tracking']
                resselect_ = select().select_transactionChat(dataJson['sid'])
                resselect_check = check_sendToChat(resselect_)
                result_Array = []
                for i in range(len(resselect_)):
                    if resselect_[i]['statusSign'] == 'Y':
                        resselect_[i]['statusSign'] = 'Complete'
                    else:
                        resselect_[i]['statusSign'] = 'Incomplete'
                    result_Array.append({
                        'emailUser':resselect_[i]['email_User'],
                        'statusSign':resselect_[i]['statusSign'],
                        'stepNum':int(resselect_[i]['stepNum']),
                        'datetime_string':resselect_[i]['datetime_string']
                    })
                if resselect_check['result'] == 'OK':
                    try:
                        arr_tc = select().select_transactionChat_next(resselect_check)
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found DATA!'})
                    for k in arr_tc:
                        res_search_frd = search_frd(k['email_User'])
                        if 'status' in res_search_frd:
                            if res_search_frd['status'] == 'success':
                                result = send_url_tochat_next(res_search_frd['friend']['user_id'],data_name_file,data_tracking,data_Url,k['transactionCode'])
                                if 'status' in result:
                                    if result['status'] == 'success':
                                        update().update_StatusOneChat(dataJson['sid'],k['email_User'])
                                        list_emailChat_log.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                else:
                                    list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                            else:
                                list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                        else:
                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                # print(list_emailChat_log)
                if len(list_emailChat_log) != 0:
                    result_update = update().update_ChatToSend_(list_emailChat_log)
                else:
                    res_select = select().select_ForWebHook(dataJson['sid'])
                    title_toChat = '- PaperlessInformation -'
                    msg_toChat = ''
                    count_res = 0
                    msg_toChat_Paper = ''
                    try:
                        title_toChat  += '\nข้อมูลเอกสาร ' + res_select['messageText']['documentId']
                        documentId = res_select['messageText']['documentId']
                    except Exception as ex:
                        documentId = None
                        print(str(ex))
                        pass
                    # for count in range(len(result_Array)):
                    #     if result_Array[count]['statusSign'] == 'Complete':
                    #         count_res = count + 1
                    #     msg_toChat_Paper = '\n•บุคคลลงชื่อบนเอกสาร ' + str(count_res) +' ใน ' + str(len(result_Array))
                    arr_step = []
                    for count in range(len(result_Array)):
                        count_res = count + 1
                        try:
                            email_User = result_Array[count]['emailUser']
                            statusSign = result_Array[count]['statusSign']
                            datetime_string = result_Array[count]['datetime_string']
                            if result_Array[count]['stepNum'] not in arr_step:
                                arr_step.append(result_Array[count]['stepNum'])
                        except Exception as ex:
                            email_User = ''
                            statusSign = ''

                    for n in arr_step:
                        msg_toChat += '\nลำดับที่ ' + str(n)
                        for count in range(len(result_Array)):
                            try:
                                email_User = result_Array[count]['emailUser']
                                statusSign = result_Array[count]['statusSign']
                                if statusSign == 'Complete':
                                    statusSign = 'เซ็นแล้ว'
                                else:
                                    statusSign = 'ยังไม่เซ็น'
                                datetime_string = result_Array[count]['datetime_string']
                            except Exception as ex:
                                email_User = ''
                                statusSign = ''
                            if result_Array[count]['stepNum'] == n:
                               msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                            # if result_Array[count]['stepNum'] in arr_step:
                            #     msg_toChat += '\nลำดับที่ ' + str(result_Array[count]['stepNum'])
                            # msg_toChat += '\nลำดับที่ ' + str(count_res) + ' ' + email_User +'\nสถานะลงชื่อ ' + statusSign + ''
                                    #  +' สถานะลงชื่อ ' + result_Array[count]['statusSign']
                    if (res_select['result'] == 'OK' and len(res_select['messageText']['webHook']) != 0):
                        webHook_Data = {
                            "result":"OK",
                            "status_Code":200,
                            "url_Sign" :data_Url,
                            "trackingId" :data_tracking,
                            "file_Name" :data_name_file,
                            "messageText":result_Array,
                            "documentId":  documentId
                        }
                        try:
                            response = requests.post(res_select['messageText']['webHook'], json=webHook_Data,headers={'Content-Type': 'application/json'},timeout=10,verify=False)
                        except requests.HTTPError as err:
                            return jsonify({'result': 'ER','status': 'HTTPError','messageText': "HTTP error occurred.",'messageType':'webhook'})
                        except requests.Timeout as err:
                            return jsonify({'result': 'ER','status': 'Timeout','messageText': 'Request timed out','messageType':'webhook'})
                        except requests.ConnectionError as err:
                            return jsonify({'result': 'ER','status': 'ConnectionError','messageText': 'API Connection error occurred.','messageType':'webhook'})
                        except Exception as ex:
                            return jsonify({'result': 'ER','status': 'Exception','messageText': 'An unexpected error: ' + str(ex),'messageType':'webhook'})

                    elif res_select['result'] == 'OK':
                        messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                        result_Email = select().select_GETEmail(dataJson['sid'])
                        res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                        if 'status' in res_search_frd:
                            if res_search_frd['status'] == 'success':
                                result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                                if result_sendChat['status'] == 'success':
                                    return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                                else:
                                    return jsonify({'result':'ER','messageText':'sendChat fail','status_Code':200,'messageER':None,'messageType':'chat'})
                            else:
                                return jsonify({'result':'ER','messageText':'not found friend','status_Code':200,'messageER':None,'messageType':'chat'})
                    result_update = 'Continue'
                return jsonify({'result':'OK','messageText':result_update,'status_Code':200,'messageER':None,'messageType':'webhook'})
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':'No ServiceType!'})
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'Parameter Fail!'})
    elif request.method == 'GET':
        if (request.args.get('email')) != None:
            arr_mailre = []
            eval_arr = eval(request.args.get('email'))
            print(len((eval_arr)))
            for n in range(len((eval_arr))):
                print(eval_arr[n])
                json_onechat = {}
                emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", eval_arr[n])
                if emails is None:
                    return jsonify({'result':'ER','messageText':'ข้อมูล email ไม่ตรงตามรูปแบบ','status_Code':200}),200
                else:
                    pass
                try:
                    res_search_frd = search_frd(str(eval_arr[n]).replace(' ',''))
                    if 'result' in res_search_frd:
                        json_onechat['result'] = 'ER'
                        json_onechat['email'] = eval_arr[n]
                    elif 'status' in res_search_frd:
                        json_onechat['result'] = 'OK'
                        json_onechat['email'] = eval_arr[n]
                except KeyError as ex:
                    print(ex)
                arr_mailre.append(json_onechat)
            return jsonify({'result':'OK','messageText':arr_mailre,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/chat/v3', methods=['POST','GET'])
@token_required
def chat_api_v3():
    if request.method == 'POST':
        dataJson = request.json
        list_emailChat_log = []
        status_sendChat = []
        if 'type_service' in dataJson and 'data' in dataJson and 'sid' in dataJson and 'tracking' in dataJson and 'name_file' in dataJson and len(dataJson) == 5:
            if str(dataJson['type_service']).lower()  == 'first':
                for n in range(len(dataJson['data'])):
                    data_tosender = dataJson['data']
                    if 'email' in data_tosender[n] and 'url_sign' in data_tosender[n] and 'tracking' in data_tosender[n] and 'name_file' in data_tosender[n] and 'message' in data_tosender[n] and 'step_num' in data_tosender[n] and 'sendChat' in data_tosender[n] and len(data_tosender[n]) == 7:
                        status_sendChat.append(data_tosender[n]['sendChat'])
                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                            res_search_frd = search_frd(data_tosender[n]['email'])
                            if 'status' in res_search_frd:
                                if res_search_frd['status'] == 'success':
                                    res_send = send_url_tochat('signning',res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'])
                                    if 'status' in res_send:
                                        if res_send['status'] == 'success':
                                            update().update_StatusOneChat(dataJson['sid'],data_tosender[n]['email'])
                                            list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign']})
                                        else:
                                           list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign']})
                                else:
                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign']})
                            else:
                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign']})
                        else:
                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign']})

                if True in status_sendChat:
                    result_logChat = selection_email_insert(list_emailChat_log)
                    if result_logChat['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':'Send To OneChat Successfully!','status_Code':200,'messageER':None})
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                else:
                    result_logChat = selection_email_insert(list_emailChat_log)
                    return jsonify({'result':'OK','messageText':'Not Found Send To OneChat!','status_Code':200,'messageER':None})
            elif str(dataJson['type_service']).lower() =='next':
                data_name_file = dataJson['name_file']
                data_tracking = dataJson['tracking']
                resselect_ = select().select_transactionChat(dataJson['sid'])
                resselect_check = check_sendToChat(resselect_)
                result_Array = []
                for i in range(len(resselect_)):
                    if resselect_[i]['statusSign'] == 'Y':
                        resselect_[i]['statusSign'] = 'Complete'
                    else:
                        resselect_[i]['statusSign'] = 'Incomplete'
                    result_Array.append({
                        'emailUser':resselect_[i]['email_User'],
                        'statusSign':resselect_[i]['statusSign'],
                        'stepNum':int(resselect_[i]['stepNum']),
                        'datetime_string':resselect_[i]['datetime_string']
                    })
                if resselect_check['result'] == 'OK':
                    try:
                        arr_tc = select().select_transactionChat_next(resselect_check)
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found DATA!'})
                    for k in arr_tc:
                        res_search_frd = search_frd(k['email_User'])
                        if 'status' in res_search_frd:
                            if res_search_frd['status'] == 'success':
                                data_Url = select().select_UrlSign_SidCodeEmailUser(dataJson['sid'],k['email_User'])
                                print(data_Url , 'data_Url')
                                result = send_url_tochat_next('signning',res_search_frd['friend']['user_id'],data_name_file,data_tracking,data_Url,k['transactionCode'],dataJson['sid'])
                                if 'status' in result:
                                    if result['status'] == 'success':
                                        update().update_StatusOneChat(dataJson['sid'],k['email_User'])
                                        list_emailChat_log.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                else:
                                    list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                            else:
                                list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                        else:
                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                if len(list_emailChat_log) != 0:
                    result_update = update().update_ChatToSend_(list_emailChat_log)
                else:
                    res_select = select().select_ForWebHook(dataJson['sid'])
                    title_toChat = '- PaperlessInformation -'
                    msg_toChat = ''
                    count_res = 0
                    msg_toChat_Paper = ''
                    try:
                        title_toChat  += '\nข้อมูลเอกสาร ' + res_select['messageText']['documentId']
                        documentId = res_select['messageText']['documentId']
                    except Exception as ex:
                        documentId = None
                        print(str(ex))
                        pass
                    arr_step = []
                    for count in range(len(result_Array)):
                        count_res = count + 1
                        try:
                            email_User = result_Array[count]['emailUser']
                            statusSign = result_Array[count]['statusSign']
                            datetime_string = result_Array[count]['datetime_string']
                            if result_Array[count]['stepNum'] not in arr_step:
                                arr_step.append(result_Array[count]['stepNum'])
                        except Exception as ex:
                            email_User = ''
                            statusSign = ''

                    for n in arr_step:
                        msg_toChat += '\nลำดับที่ ' + str(n)
                        for count in range(len(result_Array)):
                            try:
                                email_User = result_Array[count]['emailUser']
                                statusSign = result_Array[count]['statusSign']
                                if statusSign == 'Complete':
                                    statusSign = 'เซ็นแล้ว'
                                else:
                                    statusSign = 'ยังไม่เซ็น'
                                datetime_string = result_Array[count]['datetime_string']
                            except Exception as ex:
                                email_User = ''
                                statusSign = ''
                            if result_Array[count]['stepNum'] == n:
                               msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                    if (res_select['result'] == 'OK' and len(res_select['messageText']['webHook']) != 0):
                        webHook_Data = {
                            "result":"OK",
                            "status_Code":200,
                            "url_Sign" :data_Url,
                            "trackingId" :data_tracking,
                            "file_Name" :data_name_file,
                            "messageText":result_Array,
                            "documentId":  documentId
                        }
                        try:
                            response = requests.post(res_select['messageText']['webHook'], json=webHook_Data,headers={'Content-Type': 'application/json'},timeout=10,verify=False)
                        except requests.HTTPError as err:
                            return jsonify({'result': 'ER','status': 'HTTPError','messageText': "HTTP error occurred.",'messageType':'webhook'})
                        except requests.Timeout as err:
                            return jsonify({'result': 'ER','status': 'Timeout','messageText': 'Request timed out','messageType':'webhook'})
                        except requests.ConnectionError as err:
                            return jsonify({'result': 'ER','status': 'ConnectionError','messageText': 'API Connection error occurred.','messageType':'webhook'})
                        except Exception as ex:
                            return jsonify({'result': 'ER','status': 'Exception','messageText': 'An unexpected error: ' + str(ex),'messageType':'webhook'})

                    elif res_select['result'] == 'OK':
                        messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                        result_Email = select().select_GETEmail(dataJson['sid'])
                        res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                        if 'status' in res_search_frd:
                            if res_search_frd['status'] == 'success':
                                result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                                if result_sendChat['status'] == 'success':
                                    return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                                else:
                                    return jsonify({'result':'ER','messageText':'sendChat fail','status_Code':200,'messageER':None,'messageType':'chat'})
                            else:
                                return jsonify({'result':'ER','messageText':'not found friend','status_Code':200,'messageER':None,'messageType':'chat'})
                    print(res_select)
                    result_update = 'Continue'
                return jsonify({'result':'OK','messageText':result_update,'status_Code':200,'messageER':None,'messageType':'webhook'})
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':'No ServiceType!'})
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'Parameter Fail!'})
    elif request.method == 'GET':
        if (request.args.get('email')) != None:
            arr_mailre = []
            eval_arr = eval(request.args.get('email'))
            print(len((eval_arr)))
            for n in range(len((eval_arr))):
                print(eval_arr[n])
                json_onechat = {}
                emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", eval_arr[n])
                if emails is None:
                    return jsonify({'result':'ER','messageText':'ข้อมูล email ไม่ตรงตามรูปแบบ','status_Code':200}),200
                else:
                    pass
                try:
                    res_search_frd = search_frd(str(eval_arr[n]).replace(' ',''))
                    if 'result' in res_search_frd:
                        json_onechat['result'] = 'ER'
                        json_onechat['email'] = eval_arr[n]
                    elif 'status' in res_search_frd:
                        json_onechat['result'] = 'OK'
                        json_onechat['email'] = eval_arr[n]
                except KeyError as ex:
                    print(ex)
                arr_mailre.append(json_onechat)
            return jsonify({'result':'OK','messageText':arr_mailre,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/chat/v4', methods=['POST','GET'])
@token_required
def chat_api_v4():
    if request.method == 'POST':
        dataJson = request.json
        list_emailChat_log = []
        status_sendChat = []
        if 'type_service' in dataJson and 'data' in dataJson and 'sid' in dataJson and 'tracking' in dataJson and 'name_file' in dataJson and len(dataJson) == 5:
            if str(dataJson['type_service']).lower()  == 'first':
                resultURLIMAGE = createImage_formPDF(dataJson['sid'])
                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                print(result_pathUrl)
                for n in range(len(dataJson['data'])):
                    data_tosender = dataJson['data']
                    if 'email' in data_tosender[n] and 'url_sign' in data_tosender[n] and 'tracking' in data_tosender[n] and 'name_file' in data_tosender[n] and 'message' in data_tosender[n] and 'step_num' in data_tosender[n] and 'sendChat' in data_tosender[n] and 'property' in data_tosender[n] and len(data_tosender[n]) == 8:
                        status_sendChat.append(data_tosender[n]['sendChat'])
                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                            res_search_frd = search_frd(data_tosender[n]['email'])
                            if 'status' in res_search_frd:
                                if res_search_frd['status'] == 'success':
                                    userId = res_search_frd['friend']['user_id']
                                    oneId = res_search_frd['friend']['one_id']
                                    resouce_result = select().select_forChat_v1(dataJson['sid'])
                                    if resouce_result['result'] == 'OK':
                                        if str(data_tosender[n]['property']).lower() == 'signning':
                                            res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                        elif str(data_tosender[n]['property']).lower() == 'approve':
                                            res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)

                                        if 'status' in res_send:
                                            if res_send['status'] == 'success':
                                                update().update_StatusOneChat(dataJson['sid'],data_tosender[n]['email'])
                                                # resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                # print(resultgetProject)
                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})

                                            else:
                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                    else:
                                        if str(data_tosender[n]['property']).lower() == 'signning':
                                            res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],None,result_pathUrl)
                                        elif str(data_tosender[n]['property']).lower() == 'approve':
                                            res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],None,result_pathUrl)
                                        if 'status' in res_send:
                                            if res_send['status'] == 'success':
                                                update().update_StatusOneChat(dataJson['sid'],data_tosender[n]['email'])
                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                elif res_search_frd['status'] == 'fail':
                                    arrEmail = []
                                    arrEmail.append(data_tosender[n]['email'])
                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                    if 'status' in resultAddfrd:
                                        if resultAddfrd['status'] == 'success':
                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                res_search_frd = search_frd(data_tosender[n]['email'])
                                                resouce_result = select().select_forChat_v1(dataJson['sid'])
                                                if str(data_tosender[n]['property']).lower() == 'signning':
                                                    res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                elif str(data_tosender[n]['property']).lower() == 'approve':
                                                    res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                if 'status' in res_send:
                                                    if res_send['status'] == 'success':
                                                        update().update_StatusOneChat(dataJson['sid'],data_tosender[n]['email'])
                                                        list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    else:
                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                else:
                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                else:
                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                            elif 'result' in res_search_frd:
                                if res_search_frd['result'] == 'ER':
                                    arrEmail = []
                                    arrEmail.append(data_tosender[n]['email'])
                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                    # print(resultAddfrd,'resultAddfrd')
                                    if 'status' in resultAddfrd:
                                        if resultAddfrd['status'] == 'success':
                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                res_search_frd = search_frd(data_tosender[n]['email'])
                                                resouce_result = select().select_forChat_v1(dataJson['sid'])
                                                if str(data_tosender[n]['property']).lower() == 'signning':
                                                    res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                elif str(data_tosender[n]['property']).lower() == 'approve':
                                                    res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                if 'status' in res_send:
                                                    if res_send['status'] == 'success':
                                                        update().update_StatusOneChat(dataJson['sid'],data_tosender[n]['email'])
                                                        list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    else:
                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                else:
                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                            else:
                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                        else:
                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})

                if True in status_sendChat:
                    result_logChat = selection_email_insert(list_emailChat_log)
                    if result_logChat['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':'send to onechat successfully!','status_Code':200,'messageER':None})
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                else:
                    result_logChat = selection_email_insert(list_emailChat_log)
                    return jsonify({'result':'OK','messageText':'Not Found Send To OneChat!','status_Code':200,'messageER':None})
            elif str(dataJson['type_service']).lower() =='next':
                resultURLIMAGE = createImage_formPDF(dataJson['sid'])
                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                data_name_file = dataJson['name_file']
                data_tracking = dataJson['tracking']
                resselect_ = select().select_transactionChat(dataJson['sid'])
                resselect_check = check_sendToChat(resselect_)
                result_Array = []

                for i in range(len(resselect_)):
                    if resselect_[i]['statusSign'] == 'Y':
                        resselect_[i]['statusSign'] = 'Complete'
                    else:
                        resselect_[i]['statusSign'] = 'Incomplete'

                    result_Array.append({
                        'emailUser':resselect_[i]['email_User'],
                        'statusSign':resselect_[i]['statusSign'],
                        'stepNum':int(resselect_[i]['stepNum']),
                        'datetime_string':resselect_[i]['datetime_string'],
                        'status_propertyChat':resselect_[i]['propertyChat'],
                        'url_Sign':resselect_[i]['url_Sign']
                    })

                if resselect_check['result'] == 'OK':
                    # print(resselect_check)
                    try:
                        arr_tc = select().select_transactionChat_next(resselect_check)
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found DATA!'})
                    for k in arr_tc:
                        res_search_frd = search_frd(k['email_User'])
                        if 'status' in res_search_frd:
                            if res_search_frd['status'] == 'success':
                                data_Url,data_property = select().select_UrlSign_SidCodeEmailUser(dataJson['sid'],k['email_User'])
                                resouce_result = select().select_forChat_v1(dataJson['sid'])
                                if resouce_result['result'] == 'OK':
                                    result = send_url_tochat_next_new_v1(data_property,res_search_frd['friend']['user_id'],data_name_file,data_tracking,data_Url,k['transactionCode'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                    if 'status' in result:
                                        if result['status'] == 'success':
                                            update().update_StatusOneChat(dataJson['sid'],k['email_User'])
                                            list_emailChat_log.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                else:
                                    result = send_url_tochat_next_new_v1(data_property,res_search_frd['friend']['user_id'],data_name_file,data_tracking,data_Url,k['transactionCode'],dataJson['sid'],None,result_pathUrl)
                                    if 'status' in result:
                                        if result['status'] == 'success':
                                            update().update_StatusOneChat(dataJson['sid'],k['email_User'])
                                            list_emailChat_log.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                            else:
                                list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                        elif 'result' in res_search_frd:
                            if res_search_frd['result'] == 'ER':
                                arrEmail = []
                                arrEmail.append(k['email_User'])
                                resultAddfrd = addbot_tofrdAUto(arrEmail)
                                if 'status' in resultAddfrd:
                                    if resultAddfrd['status'] == 'success':
                                        if resultAddfrd['list_friend'][0]['status'] == 'success':
                                            res_search_frd = search_frd(k['email_User'])
                                            data_Url,data_property = select().select_UrlSign_SidCodeEmailUser(dataJson['sid'],k['email_User'])
                                            resouce_result = select().select_forChat_v1(dataJson['sid'])
                                            if resouce_result['result'] == 'OK':
                                                result = send_url_tochat_next_new_v1(data_property,res_search_frd['friend']['user_id'],data_name_file,data_tracking,data_Url,k['transactionCode'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                if 'status' in result:
                                                    if result['status'] == 'success':
                                                        update().update_StatusOneChat(dataJson['sid'],k['email_User'])
                                                        list_emailChat_log.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                                    else:
                                                        list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                                else:
                                                    list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                            else:
                                                result = send_url_tochat_next_new_v1(data_property,res_search_frd['friend']['user_id'],data_name_file,data_tracking,data_Url,k['transactionCode'],dataJson['sid'],None,result_pathUrl)
                                                if 'status' in result:
                                                    if result['status'] == 'success':
                                                        update().update_StatusOneChat(dataJson['sid'],k['email_User'])
                                                        list_emailChat_log.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                                    else:
                                                        list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                                else:
                                                    list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                else:
                                    list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                        else:
                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})

                if len(list_emailChat_log) != 0:
                    result_update = update().update_ChatToSend_(list_emailChat_log)
                    res_select = select().select_ForWebHook(dataJson['sid'])
                    title_toChat = 'แจ้งเตือนระบบ Paperless'
                    msg_toChat = ''
                    count_res = 0
                    msg_toChat_Paper = ''
                    try:
                        title_toChat  += '\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['sender_email'] + '\n'
                        documentId = res_select['messageText']['documentId']
                    except Exception as ex:
                        documentId = None
                        pass
                    arr_step = []

                    for count in range(len(result_Array)):
                        count_res = count + 1
                        try:
                            email_User = result_Array[count]['emailUser']
                            statusSign = result_Array[count]['statusSign']
                            datetime_string = result_Array[count]['datetime_string']
                            arr_step.append(result_Array[count]['stepNum'])
                        except Exception as ex:
                            email_User = ''
                            statusSign = ''
                    for n in arr_step:
                        msg_toChat += '\nลำดับที่ ' + str(n)
                        for count in range(len(result_Array)):
                            try:
                                email_User = result_Array[count]['emailUser']
                                statusSign = result_Array[count]['statusSign']
                                status_propertyChat = result_Array[count]['status_propertyChat']
                                if status_propertyChat == 'signning':
                                    if statusSign == 'Complete':
                                        statusSign = 'เซ็นแล้ว'
                                    else:
                                        statusSign = 'ยังไม่เซ็น'
                                elif status_propertyChat == 'approve':
                                    if statusSign == 'Complete':
                                        statusSign = 'อนุมัติแล้ว'
                                    else:
                                        statusSign = 'ยังไม่อนุมัติ'
                                datetime_string = result_Array[count]['datetime_string']
                            except Exception as ex:
                                email_User = ''
                                statusSign = ''
                            if result_Array[count]['stepNum'] == n:
                                msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                    messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                    result_Email = select().select_GETEmail(dataJson['sid'])
                    res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                    if 'status' in res_search_frd:
                        if res_search_frd['status'] == 'success':
                            result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                            if result_sendChat['status'] == 'success':
                                return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                            else:
                                return jsonify({'result':'ER','messageText':'sendChat fail','status_Code':200,'messageER':None,'messageType':'chat'})
                        else:
                            return jsonify({'result':'ER','messageText':'not found friend','status_Code':200,'messageER':None,'messageType':'chat'})
                else:
                    res_select = select().select_ForWebHook(dataJson['sid'])
                    title_toChat = 'แจ้งเตือนระบบ Paperless'
                    msg_toChat = ''
                    count_res = 0
                    msg_toChat_Paper = ''
                    try:
                        title_toChat  += '\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['sender_email'] + '\n'
                        documentId = res_select['messageText']['documentId']
                    except Exception as ex:
                        documentId = None
                        pass
                    arr_step = []
                    for count in range(len(result_Array)):
                        count_res = count + 1
                        try:
                            email_User = result_Array[count]['emailUser']
                            statusSign = result_Array[count]['statusSign']
                            datetime_string = result_Array[count]['datetime_string']
                            if result_Array[count]['stepNum'] not in arr_step:
                                arr_step.append(result_Array[count]['stepNum'])
                        except Exception as ex:
                            email_User = ''
                            statusSign = ''

                    for n in arr_step:
                        msg_toChat += '\nลำดับที่ ' + str(n)
                        for count in range(len(result_Array)):
                            try:
                                email_User = result_Array[count]['emailUser']
                                statusSign = result_Array[count]['statusSign']
                                status_propertyChat = result_Array[count]['status_propertyChat']
                                if status_propertyChat == 'signning':
                                    if statusSign == 'Complete':
                                        statusSign = 'เซ็นแล้ว'
                                    else:
                                        statusSign = 'ยังไม่เซ็น'
                                elif status_propertyChat == 'approve':
                                    if statusSign == 'Complete':
                                        statusSign = 'อนุมัติแล้ว'
                                    else:
                                        statusSign = 'ยังไม่อนุมัติ'
                                datetime_string = result_Array[count]['datetime_string']
                            except Exception as ex:
                                email_User = ''
                                statusSign = ''
                            if result_Array[count]['stepNum'] == n:
                               msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                    if (res_select['result'] == 'OK' and len(res_select['messageText']['webHook']) != 0):
                        webHook_Data = {
                            "result":"OK",
                            "status_Code":200,
                            "trackingId" :data_tracking,
                            "file_Name" :data_name_file,
                            "messageText":result_Array,
                            "documentId":  documentId
                        }
                        try:
                            response = requests.post(res_select['messageText']['webHook'], json=webHook_Data,headers={'Content-Type': 'application/json'},timeout=10,verify=False)
                        except requests.HTTPError as err:
                            return jsonify({'result': 'ER','status': 'HTTPError','messageText': "HTTP error occurred.",'messageType':'webhook'})
                        except requests.Timeout as err:
                            return jsonify({'result': 'ER','status': 'Timeout','messageText': 'Request timed out','messageType':'webhook'})
                        except requests.ConnectionError as err:
                            return jsonify({'result': 'ER','status': 'ConnectionError','messageText': 'API Connection error occurred.','messageType':'webhook'})
                        except Exception as ex:
                            return jsonify({'result': 'ER','status': 'Exception','messageText': 'An unexpected error: ' + str(ex),'messageType':'webhook'})

                    elif res_select['result'] == 'OK':
                        messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                        result_Email = select().select_GETEmail(dataJson['sid'])
                        res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                        # print(res_search_frd,'res_search_frd')
                        if 'status' in res_search_frd:
                            if res_search_frd['status'] == 'success':
                                result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                                if 'status' in result_sendChat:
                                    if result_sendChat['status'] == 'success':
                                        return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                                    elif result_sendChat['status'] == 'fail':
                                        arrmail = []
                                        arrmail.append(result_Email['messageText']['email_Sender'])
                                        result_AddfrdAuto = addbot_tofrdAUto(arrmail)
                                        res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                                        if res_search_frd['status'] == 'success':
                                            result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                                        return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                                elif 'result' in result_sendChat:
                                    if result_sendChat['result'] == 'ER':
                                        arrmail = []
                                        arrmail.append(result_Email['messageText']['email_Sender'])
                                        result_AddfrdAuto = addbot_tofrdAUto(arrmail)
                                        res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                                        if res_search_frd['status'] == 'success':
                                            result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                                        return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                                    else:
                                        print()
                            else:
                                return jsonify({'result':'ER','messageText':'not found friend','status_Code':200,'messageER':None,'messageType':'chat'})
                        elif 'result' in res_search_frd:
                            arrmail = []
                            arrmail.append(result_Email['messageText']['email_Sender'])
                            result_AddfrdAuto = addbot_tofrdAUto(arrmail)
                            res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                            if res_search_frd['status'] == 'success':
                                result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                            return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                    print(res_select)
                    result_update = 'Continue'
                return jsonify({'result':'OK','messageText':res_select['messageText'],'status_Code':200,'messageER':None,'messageType':'webhook'})
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':'No ServiceType!'})
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'Parameter Fail!'})
    elif request.method == 'GET':
        if (request.args.get('email')) != None:
            arr_mailre = []
            eval_arr = eval(request.args.get('email'))
            print(len((eval_arr)))
            for n in range(len((eval_arr))):
                print(eval_arr[n])
                json_onechat = {}
                emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", eval_arr[n])
                if emails is None:
                    return jsonify({'result':'ER','messageText':'ข้อมูล email ไม่ตรงตามรูปแบบ','status_Code':200}),200
                else:
                    pass
                try:
                    res_search_frd = search_frd(str(eval_arr[n]).replace(' ',''))
                    if 'result' in res_search_frd:
                        json_onechat['result'] = 'ER'
                        json_onechat['email'] = eval_arr[n]
                    elif 'status' in res_search_frd:
                        json_onechat['result'] = 'OK'
                        json_onechat['email'] = eval_arr[n]
                except KeyError as ex:
                    print(ex)
                arr_mailre.append(json_onechat)
            return jsonify({'result':'OK','messageText':arr_mailre,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/chat/v5', methods=['POST','GET'])
@token_required
def chat_api_v5():
    if request.method == 'POST':
        dataJson = request.json
        list_emailChat_log = []
        list_taskChat_log = []
        status_sendChat = []
        if 'type_service' in dataJson and 'data' in dataJson and 'sid' in dataJson and 'tracking' in dataJson and 'name_file' in dataJson and len(dataJson) == 5:
            if str(dataJson['type_service']).lower()  == 'first':
                resultURLIMAGE = createImage_formPDF(dataJson['sid'])
                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                for n in range(len(dataJson['data'])):
                    data_tosender = dataJson['data']
                    if 'email' in data_tosender[n] and 'url_sign' in data_tosender[n] and 'tracking' in data_tosender[n] and 'name_file' in data_tosender[n] and 'message' in data_tosender[n] and 'step_num' in data_tosender[n] and 'sendChat' in data_tosender[n] and 'property' in data_tosender[n] and len(data_tosender[n]) == 8:
                        status_sendChat.append(data_tosender[n]['sendChat'])
                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                            res_search_frd = search_frd(data_tosender[n]['email'])
                            if 'status' in res_search_frd:
                                if res_search_frd['status'] == 'success':
                                    userId = res_search_frd['friend']['user_id']
                                    oneId = res_search_frd['friend']['one_id']
                                    resouce_result = select().select_forChat_v1(dataJson['sid'])
                                    if resouce_result['result'] == 'OK':
                                        if str(data_tosender[n]['property']).lower() == 'signning':
                                            res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                        elif str(data_tosender[n]['property']).lower() == 'approve':
                                            res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)

                                        if 'status' in res_send:
                                            if res_send['status'] == 'success':
                                                update().update_StatusOneChat(dataJson['sid'],data_tosender[n]['email'])
                                                resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                if resultgetProject['result'] == 'OK':
                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                    priority_ = '1'
                                                    titleAndDetails = resouce_result['messageText']
                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                        if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                    resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),dataJson['sid'])
                                                    # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                    if resultSend_CreateTask['result'] == 'OK':
                                                        if 'status' in resultSend_CreateTask['messageText']:
                                                            if resultSend_CreateTask['messageText']['status'] =='success':
                                                                list_taskChat_log.append({'result':'OK','sidCode':dataJson['sid'],'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                    else:
                                                        list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                else:
                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})

                                            else:
                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                    else:
                                        if str(data_tosender[n]['property']).lower() == 'signning':
                                            res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],None,result_pathUrl)
                                        elif str(data_tosender[n]['property']).lower() == 'approve':
                                            res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],None,result_pathUrl)
                                        if 'status' in res_send:
                                            if res_send['status'] == 'success':
                                                update().update_StatusOneChat(dataJson['sid'],data_tosender[n]['email'])
                                                resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                if resultgetProject['result'] == 'OK':
                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                    priority_ = '1'
                                                    titleAndDetails = resouce_result['messageText']
                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                        if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                    resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),dataJson['sid'])
                                                    if resultSend_CreateTask['result'] == 'OK':
                                                        if 'status' in resultSend_CreateTask['messageText']:
                                                            if resultSend_CreateTask['messageText']['status'] =='success':
                                                                list_taskChat_log.append({'result':'OK','sidCode':dataJson['sid'],'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                    else:
                                                        list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                else:
                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                elif res_search_frd['status'] == 'fail':
                                    arrEmail = []
                                    arrEmail.append(data_tosender[n]['email'])
                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                    if 'status' in resultAddfrd:
                                        if resultAddfrd['status'] == 'success':
                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                res_search_frd = search_frd(data_tosender[n]['email'])
                                                resouce_result = select().select_forChat_v1(dataJson['sid'])
                                                userId = res_search_frd['friend']['user_id']
                                                oneId = res_search_frd['friend']['one_id']
                                                if str(data_tosender[n]['property']).lower() == 'signning':
                                                    res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                elif str(data_tosender[n]['property']).lower() == 'approve':
                                                    res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                if 'status' in res_send:
                                                    if res_send['status'] == 'success':
                                                        update().update_StatusOneChat(dataJson['sid'],data_tosender[n]['email'])
                                                        resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                        if resultgetProject['result'] == 'OK':
                                                            projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                            priority_ = '1'
                                                            titleAndDetails = resouce_result['messageText']
                                                            for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                    state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                            resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),dataJson['sid'])
                                                            if resultSend_CreateTask['result'] == 'OK':
                                                                if 'status' in resultSend_CreateTask['messageText']:
                                                                    if resultSend_CreateTask['messageText']['status'] =='success':
                                                                        list_taskChat_log.append({'result':'OK','sidCode':dataJson['sid'],'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                    else:
                                                                        list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                else:
                                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                        list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    else:
                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                else:
                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                else:
                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                            elif 'result' in res_search_frd:
                                if res_search_frd['result'] == 'ER':
                                    arrEmail = []
                                    arrEmail.append(data_tosender[n]['email'])
                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                    # print(resultAddfrd,'resultAddfrd')
                                    if 'status' in resultAddfrd:
                                        if resultAddfrd['status'] == 'success':
                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                res_search_frd = search_frd(data_tosender[n]['email'])
                                                resouce_result = select().select_forChat_v1(dataJson['sid'])
                                                userId = res_search_frd['friend']['user_id']
                                                oneId = res_search_frd['friend']['one_id']
                                                if str(data_tosender[n]['property']).lower() == 'signning':
                                                    res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                elif str(data_tosender[n]['property']).lower() == 'approve':
                                                    res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                if 'status' in res_send:
                                                    if res_send['status'] == 'success':
                                                        update().update_StatusOneChat(dataJson['sid'],data_tosender[n]['email'])
                                                        resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                        if resultgetProject['result'] == 'OK':
                                                            projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                            priority_ = '1'
                                                            titleAndDetails = resouce_result['messageText']
                                                            for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                    state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                            resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),dataJson['sid'])
                                                            if resultSend_CreateTask['result'] == 'OK':
                                                                if 'status' in resultSend_CreateTask['messageText']:
                                                                    if resultSend_CreateTask['messageText']['status'] =='success':
                                                                        list_taskChat_log.append({'result':'OK','sidCode':dataJson['sid'],'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                    else:
                                                                        list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                else:
                                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                        list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    else:
                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                else:
                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                            else:
                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                        else:
                            list_taskChat_log.append({'result':'NO','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})

                if True in status_sendChat:
                    result_logChat = selection_email_insert(list_emailChat_log)
                    if result_logChat['result'] == 'OK':
                        insert().insert_transactionTask(list_taskChat_log)
                        return jsonify({'result':'OK','messageText':'send to onechat successfully!','status_Code':200,'messageER':None})
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                else:
                    result_logChat = selection_email_insert(list_emailChat_log)
                    return jsonify({'result':'OK','messageText':'Not Found Send To OneChat!','status_Code':200,'messageER':None})
            elif str(dataJson['type_service']).lower() =='next':
                resultURLIMAGE = createImage_formPDF(dataJson['sid'])
                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                data_name_file = dataJson['name_file']
                data_tracking = dataJson['tracking']
                resselect_ = select().select_transactionChat(dataJson['sid'])
                resselect_check = check_sendToChat(resselect_)
                result_Array = []

                for i in range(len(resselect_)):
                    if resselect_[i]['statusSign'] == 'Y':
                        resselect_[i]['statusSign'] = 'Complete'
                    elif resselect_[i]['statusSign'] == 'R':
                        resselect_[i]['statusSign'] = 'Reject'
                    else:
                        resselect_[i]['statusSign'] = 'Incomplete'

                    result_Array.append({
                        'emailUser':resselect_[i]['email_User'],
                        'statusSign':resselect_[i]['statusSign'],
                        'stepNum':int(resselect_[i]['stepNum']),
                        'datetime_string':resselect_[i]['datetime_string'],
                        'status_propertyChat':resselect_[i]['propertyChat'],
                        'url_Sign':resselect_[i]['url_Sign']
                    })
                # print(resselect_check , 'resselect_check')

                if resselect_check['result'] == 'OK':
                    if 'statusSign' in resselect_check['msg']:
                        print((resselect_check['msg']))
                        if resselect_check['msg']['statusSign'] == 'R':
                            messageToChat = ''
                            stepnum_ = int(resselect_check['msg']['stepNum']) - 1
                            sid_ = resselect_check['msg']['sid']
                            email_ = resselect_check['msg']['email_User']
                            result_SelectBefore = select().select_transactionChat_before(stepnum_,sid_)
                            if result_SelectBefore['result'] == 'OK':
                                res_select = select().select_ForWebHook(sid_)
                                title_toChat = 'แจ้งเตือนระบบ Paperless'
                                msg_toChat = ''
                                count_res = 0
                                msg_toChat_Paper = ''
                                try:
                                    title_toChat  += '\n- เอกสารถูกปฏิเสธอนุมัติ -\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['sender_email'] + '\n'
                                    documentId = res_select['messageText']['documentId']
                                except Exception as ex:
                                    documentId = None
                                    pass
                                arr_step = []

                                for count in range(len(result_Array)):
                                    count_res = count + 1
                                    try:
                                        email_User = result_Array[count]['emailUser']
                                        statusSign = result_Array[count]['statusSign']
                                        datetime_string = result_Array[count]['datetime_string']
                                        arr_step.append(result_Array[count]['stepNum'])
                                    except Exception as ex:
                                        email_User = ''
                                        statusSign = ''
                                for n in arr_step:
                                    msg_toChat += '\nลำดับที่ ' + str(n)
                                    for count in range(len(result_Array)):
                                        try:
                                            email_User = result_Array[count]['emailUser']
                                            statusSign = result_Array[count]['statusSign']
                                            status_propertyChat = result_Array[count]['status_propertyChat']
                                            if status_propertyChat == 'signning':
                                                if statusSign == 'Complete':
                                                    statusSign = 'เซ็นแล้ว'
                                                elif statusSign == 'Pending':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                elif statusSign == 'Incomplete':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                else:
                                                    statusSign = 'ไม่อนุมัติ'
                                            elif status_propertyChat == 'approve':
                                                if statusSign == 'Complete':
                                                    statusSign = 'อนุมัติแล้ว'
                                                elif statusSign == 'Pending':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                elif statusSign == 'Incomplete':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                else:
                                                    statusSign = 'ไม่อนุมัติ'
                                            datetime_string = result_Array[count]['datetime_string']
                                        except Exception as ex:
                                            email_User = ''
                                            statusSign = ''
                                        if result_Array[count]['stepNum'] == n:
                                            msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                                messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                                for i in range(len(result_SelectBefore['messageText'])):
                                    emailBfore = result_SelectBefore['messageText'][i]['email_User']
                                #     email_ =
                                    res_search_frd = search_frd(emailBfore)
                                    user_id_chat = res_search_frd['friend']['user_id']
                                    result_sendChat = send_messageToChat(messageToChat,user_id_chat)
                                    print(result_sendChat)
                            return jsonify({'result':'OK','messageText':'send chat ok and reject document','status_Code':200,'messageER':None})
                        else:
                            pass
                    try:
                        result_Task = select().select_transactionTaskChat(resselect_check)
                        # print(result_Task, 'result_Task')
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found DATA! transactionTask'})
                    for u in result_Task:
                        res_search_frd = search_frd(u['emailUser'])
                        sid_code = u['sidCode']
                        emailUser = u['emailUser']
                        step_num = u['step_num']
                        task_state_name_new = 'done'
                        userId = res_search_frd['friend']['user_id']
                        oneId = res_search_frd['friend']['one_id']
                        resultgetProject = sendtask_getProject_tochat_v1(oneId)
                        if resultgetProject['result'] == 'OK':
                            for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'done':
                                    state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                        task_id = u['task_id']
                        state_id = state_id_

                        resultChangeState = sendtask_change_stateChat(state_id,task_id)
                        if resultChangeState['result'] == 'OK':
                            update().update_taskchat_state(sid_code,emailUser,step_num,task_state_name_new,state_id)

                    try:
                        arr_tc = select().select_transactionChat_next(resselect_check)
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found DATA!'})
                    # print(arr_tc,'arr_tc')
                    for k in arr_tc:
                        status_Sign = k['statusSign']
                        if status_Sign != 'R':
                            res_search_frd = search_frd(k['email_User'])
                            resouce_result = select().select_forChat_v1(dataJson['sid'])
                            if 'status' in res_search_frd:
                                if res_search_frd['status'] == 'success':
                                    userId = res_search_frd['friend']['user_id']
                                    oneId = res_search_frd['friend']['one_id']
                                    data_Url,data_property = select().select_UrlSign_SidCodeEmailUser(dataJson['sid'],k['email_User'])
                                    if resouce_result['result'] == 'OK':
                                        result = send_url_tochat_next_new_v1(data_property,res_search_frd['friend']['user_id'],data_name_file,data_tracking,data_Url,k['transactionCode'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                        if 'status' in result:
                                            if result['status'] == 'success':
                                                update().update_StatusOneChat(dataJson['sid'],k['email_User'])
                                                resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                if resultgetProject['result'] == 'OK':
                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                    priority_ = '1'
                                                    titleAndDetails = resouce_result['messageText']
                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                        if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                    resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_property).lower(),dataJson['sid'])
                                                    if resultSend_CreateTask['result'] == 'OK':
                                                        if 'status' in resultSend_CreateTask['messageText']:
                                                            if resultSend_CreateTask['messageText']['status'] =='success':
                                                                list_taskChat_log.append({'result':'OK','sidCode':dataJson['sid'],'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'step_num':k['stepNum'],'email':(k['email_User'])})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                    else:
                                                        list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                else:
                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                list_emailChat_log.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                    else:
                                        result = send_url_tochat_next_new_v1(data_property,res_search_frd['friend']['user_id'],data_name_file,data_tracking,data_Url,k['transactionCode'],dataJson['sid'],None,result_pathUrl)
                                        if 'status' in result:
                                            if result['status'] == 'success':
                                                update().update_StatusOneChat(dataJson['sid'],k['email_User'])
                                                list_emailChat_log.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                else:
                                    list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                            elif 'result' in res_search_frd:
                                if res_search_frd['result'] == 'ER':
                                    arrEmail = []
                                    arrEmail.append(k['email_User'])
                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                    if 'status' in resultAddfrd:
                                        if resultAddfrd['status'] == 'success':
                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                res_search_frd = search_frd(k['email_User'])
                                                data_Url,data_property = select().select_UrlSign_SidCodeEmailUser(dataJson['sid'],k['email_User'])
                                                resouce_result = select().select_forChat_v1(dataJson['sid'])
                                                if resouce_result['result'] == 'OK':
                                                    result = send_url_tochat_next_new_v1(data_property,res_search_frd['friend']['user_id'],data_name_file,data_tracking,data_Url,k['transactionCode'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                    if 'status' in result:
                                                        if result['status'] == 'success':
                                                            update().update_StatusOneChat(dataJson['sid'],k['email_User'])
                                                            resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                            if resultgetProject['result'] == 'OK':
                                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                priority_ = '1'
                                                                titleAndDetails = resouce_result['messageText']
                                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_property).lower(),dataJson['sid'])
                                                                if resultSend_CreateTask['result'] == 'OK':
                                                                    if 'status' in resultSend_CreateTask['messageText']:
                                                                        if resultSend_CreateTask['messageText']['status'] =='success':
                                                                            list_taskChat_log.append({'result':'OK','sidCode':dataJson['sid'],'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'step_num':k['stepNum'],'email':(k['email_User'])})
                                                                        else:
                                                                            list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                                    else:
                                                                        list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                                else:
                                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                            list_emailChat_log.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                                        else:
                                                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                                    else:
                                                        list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                                else:
                                                    result = send_url_tochat_next_new_v1(data_property,res_search_frd['friend']['user_id'],data_name_file,data_tracking,data_Url,k['transactionCode'],dataJson['sid'],None,result_pathUrl)
                                                    if 'status' in result:
                                                        if result['status'] == 'success':
                                                            update().update_StatusOneChat(dataJson['sid'],k['email_User'])
                                                            resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                            if resultgetProject['result'] == 'OK':
                                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                priority_ = '1'
                                                                titleAndDetails = resouce_result['messageText']
                                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_property).lower(),dataJson['sid'])
                                                                if resultSend_CreateTask['result'] == 'OK':
                                                                    if 'status' in resultSend_CreateTask['messageText']:
                                                                        if resultSend_CreateTask['messageText']['status'] =='success':
                                                                            list_taskChat_log.append({'result':'OK','sidCode':dataJson['sid'],'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'step_num':k['stepNum'],'email':(k['email_User'])})
                                                                        else:
                                                                            list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                                    else:
                                                                        list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                                else:
                                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                            list_emailChat_log.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                                        else:
                                                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                                    else:
                                                        list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                            else:
                                list_taskChat_log.append({'result':'NO','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                        else:
                            print('----------------------///---------------------------')
                if len(list_emailChat_log) != 0:
                    resultUpdateTask = update().update_taskchat_nextstep(list_taskChat_log)
                    print(resultUpdateTask)
                    result_update = update().update_ChatToSend_(list_emailChat_log)
                    res_select = select().select_ForWebHook(dataJson['sid'])
                    title_toChat = 'แจ้งเตือนระบบ Paperless'
                    msg_toChat = ''
                    count_res = 0
                    msg_toChat_Paper = ''
                    try:
                        title_toChat  += '\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['sender_email'] + '\n'
                        documentId = res_select['messageText']['documentId']
                    except Exception as ex:
                        documentId = None
                        pass
                    arr_step = []

                    for count in range(len(result_Array)):
                        count_res = count + 1
                        try:
                            email_User = result_Array[count]['emailUser']
                            statusSign = result_Array[count]['statusSign']
                            datetime_string = result_Array[count]['datetime_string']
                            arr_step.append(result_Array[count]['stepNum'])
                        except Exception as ex:
                            email_User = ''
                            statusSign = ''
                    for n in arr_step:
                        msg_toChat += '\nลำดับที่ ' + str(n)
                        for count in range(len(result_Array)):
                            try:
                                email_User = result_Array[count]['emailUser']
                                statusSign = result_Array[count]['statusSign']
                                status_propertyChat = result_Array[count]['status_propertyChat']
                                if status_propertyChat == 'signning':
                                    if statusSign == 'Complete':
                                        statusSign = 'เซ็นแล้ว'
                                    elif statusSign == 'Pending':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    elif statusSign == 'Incomplete':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    else:
                                        statusSign = 'ไม่อนุมัติ'
                                elif status_propertyChat == 'approve':
                                    if statusSign == 'Complete':
                                        statusSign = 'อนุมัติแล้ว'
                                    elif statusSign == 'Pending':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    elif statusSign == 'Incomplete':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    else:
                                        statusSign = 'ไม่อนุมัติ'
                                datetime_string = result_Array[count]['datetime_string']
                            except Exception as ex:
                                email_User = ''
                                statusSign = ''
                            if result_Array[count]['stepNum'] == n:
                                msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                    messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                    result_Email = select().select_GETEmail(dataJson['sid'])
                    res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                    if 'status' in res_search_frd:
                        if res_search_frd['status'] == 'success':
                            result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                            if result_sendChat['status'] == 'success':
                                return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                            else:
                                return jsonify({'result':'ER','messageText':'sendChat fail','status_Code':200,'messageER':None,'messageType':'chat'})
                        else:
                            return jsonify({'result':'ER','messageText':'not found friend','status_Code':200,'messageER':None,'messageType':'chat'})
                else:
                    res_select = select().select_ForWebHook(dataJson['sid'])
                    title_toChat = 'แจ้งเตือนระบบ Paperless'
                    msg_toChat = ''
                    count_res = 0
                    msg_toChat_Paper = ''
                    try:
                        title_toChat  += '\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['sender_email'] + '\n'
                        documentId = res_select['messageText']['documentId']
                    except Exception as ex:
                        documentId = None
                        pass
                    arr_step = []
                    for count in range(len(result_Array)):
                        count_res = count + 1
                        try:
                            email_User = result_Array[count]['emailUser']
                            statusSign = result_Array[count]['statusSign']
                            datetime_string = result_Array[count]['datetime_string']
                            if result_Array[count]['stepNum'] not in arr_step:
                                arr_step.append(result_Array[count]['stepNum'])
                        except Exception as ex:
                            email_User = ''
                            statusSign = ''

                    for n in arr_step:
                        msg_toChat += '\nลำดับที่ ' + str(n)
                        for count in range(len(result_Array)):
                            try:
                                email_User = result_Array[count]['emailUser']
                                statusSign = result_Array[count]['statusSign']
                                status_propertyChat = result_Array[count]['status_propertyChat']
                                if status_propertyChat == 'signning':
                                    if statusSign == 'Complete':
                                        statusSign = 'เซ็นแล้ว'
                                    elif statusSign == 'Pending':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    elif statusSign == 'Incomplete':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    else:
                                        statusSign = 'ไม่อนุมัติ'
                                elif status_propertyChat == 'approve':
                                    if statusSign == 'Complete':
                                        statusSign = 'อนุมัติแล้ว'
                                    elif statusSign == 'Pending':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    elif statusSign == 'Incomplete':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    else:
                                        statusSign = 'ไม่อนุมัติ'
                                datetime_string = result_Array[count]['datetime_string']
                            except Exception as ex:
                                email_User = ''
                                statusSign = ''
                            if result_Array[count]['stepNum'] == n:
                               msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                    if (res_select['result'] == 'OK' and len(str(res_select['messageText']['webHook'])) != 0):
                        webHook_Data = {
                            "result":"OK",
                            "status_Code":200,
                            "trackingId" :data_tracking,
                            "file_Name" :data_name_file,
                            "messageText":result_Array,
                            "documentId":  documentId
                        }
                        try:
                            response = requests.post(res_select['messageText']['webHook'], json=webHook_Data,headers={'Content-Type': 'application/json'},timeout=10,verify=False)
                        except requests.HTTPError as err:
                            pass
                            # return jsonify({'result': 'ER','status': 'HTTPError','messageText': "HTTP error occurred.",'messageType':'webhook'})
                        except requests.Timeout as err:
                            pass
                            # return jsonify({'result': 'ER','status': 'Timeout','messageText': 'Request timed out','messageType':'webhook'})
                        except requests.ConnectionError as err:
                            pass
                            # return jsonify({'result': 'ER','status': 'ConnectionError','messageText': 'API Connection error occurred.','messageType':'webhook'})
                        except Exception as ex:
                            pass
                            # return jsonify({'result': 'ER','status': 'Exception','messageText': 'An unexpected error: ' + str(ex),'messageType':'webhook'})

                    elif res_select['result'] == 'OK':
                        messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                        result_Email = select().select_GETEmail(dataJson['sid'])
                        res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                        if 'status' in res_search_frd:
                            if res_search_frd['status'] == 'success':
                                result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                                if 'status' in result_sendChat:
                                    if result_sendChat['status'] == 'success':
                                        return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                                    elif result_sendChat['status'] == 'fail':
                                        arrmail = []
                                        arrmail.append(result_Email['messageText']['email_Sender'])
                                        result_AddfrdAuto = addbot_tofrdAUto(arrmail)
                                        res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                                        if res_search_frd['status'] == 'success':
                                            result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                                        return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                                elif 'result' in result_sendChat:
                                    if result_sendChat['result'] == 'ER':
                                        arrmail = []
                                        arrmail.append(result_Email['messageText']['email_Sender'])
                                        result_AddfrdAuto = addbot_tofrdAUto(arrmail)
                                        res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                                        if res_search_frd['status'] == 'success':
                                            result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                                        return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                                    else:
                                        print()
                            else:
                                return jsonify({'result':'ER','messageText':'not found friend','status_Code':200,'messageER':None,'messageType':'chat'})
                        elif 'result' in res_search_frd:
                            arrmail = []
                            arrmail.append(result_Email['messageText']['email_Sender'])
                            result_AddfrdAuto = addbot_tofrdAUto(arrmail)
                            res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                            if res_search_frd['status'] == 'success':
                                result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                            return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                    print(res_select)
                    result_update = 'Continue'
                return jsonify({'result':'OK','messageText':res_select['messageText'],'status_Code':200,'messageER':None,'messageType':'webhook'})
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':'No ServiceType!'})
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'Parameter Fail!'})
    elif request.method == 'GET':
        if (request.args.get('email')) != None:
            arr_mailre = []
            eval_arr = eval(request.args.get('email'))
            print(len((eval_arr)))
            for n in range(len((eval_arr))):
                print(eval_arr[n])
                json_onechat = {}
                emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", eval_arr[n])
                if emails is None:
                    return jsonify({'result':'ER','messageText':'ข้อมูล email ไม่ตรงตามรูปแบบ','status_Code':200}),200
                else:
                    pass
                try:
                    res_search_frd = search_frd(str(eval_arr[n]).replace(' ',''))
                    if 'result' in res_search_frd:
                        json_onechat['result'] = 'ER'
                        json_onechat['email'] = eval_arr[n]
                    elif 'status' in res_search_frd:
                        json_onechat['result'] = 'OK'
                        json_onechat['email'] = eval_arr[n]
                except KeyError as ex:
                    print(ex)
                arr_mailre.append(json_onechat)
            return jsonify({'result':'OK','messageText':arr_mailre,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/v6/chat_sender', methods=['POST','GET'])
@token_required
def chat_api_v6():
    if request.method == 'POST':
        dataJson = request.json
        list_emailChat_log = []
        list_taskChat_log = []
        status_sendChat = []
        if 'type_service' in dataJson and 'data' in dataJson and 'sid' in dataJson and 'tracking' in dataJson and 'name_file' in dataJson and len(dataJson) == 5:
            if str(dataJson['type_service']).lower()  == 'first':
                resultURLIMAGE = createImage_formPDF(dataJson['sid'])
                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                for n in range(len(dataJson['data'])):
                    data_tosender = dataJson['data']
                    if 'email' in data_tosender[n] and 'url_sign' in data_tosender[n] and 'tracking' in data_tosender[n] and 'name_file' in data_tosender[n] and 'message' in data_tosender[n] and 'step_num' in data_tosender[n] and 'sendChat' in data_tosender[n] and 'property' in data_tosender[n] and len(data_tosender[n]) == 8:
                        status_sendChat.append(data_tosender[n]['sendChat'])
                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                            res_search_frd = search_frd(data_tosender[n]['email'])
                            if 'status' in res_search_frd:
                                if res_search_frd['status'] == 'success':
                                    userId = res_search_frd['friend']['user_id']
                                    oneId = res_search_frd['friend']['one_id']
                                    resouce_result = select().select_forChat_v1(dataJson['sid'])
                                    if resouce_result['result'] == 'OK':
                                        if str(data_tosender[n]['property']).lower() == 'signning':
                                            res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                        elif str(data_tosender[n]['property']).lower() == 'approve':
                                            res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                        # return ''
                                        if 'status' in res_send:
                                            if res_send['status'] == 'success':
                                                id_one_chat_to_msg = res_send['message']['id']
                                                update().update_StatusOneChat(dataJson['sid'],data_tosender[n]['email'])
                                                resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                if resultgetProject['result'] == 'OK':
                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                    priority_ = '1'
                                                    titleAndDetails = resouce_result['messageText']
                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                        if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                    resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),dataJson['sid'],oneId)
                                                    # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                    if resultSend_CreateTask['result'] == 'OK':
                                                        if 'status' in resultSend_CreateTask['messageText']:
                                                            if resultSend_CreateTask['messageText']['status'] =='success':
                                                                list_taskChat_log.append({'result':'OK','sidCode':dataJson['sid'],'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                    else:
                                                        list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                else:
                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})

                                            else:
                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                    else:
                                        if str(data_tosender[n]['property']).lower() == 'signning':
                                            res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],None,result_pathUrl)
                                        elif str(data_tosender[n]['property']).lower() == 'approve':
                                            res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],None,result_pathUrl)
                                        if 'status' in res_send:
                                            if res_send['status'] == 'success':
                                                id_one_chat_to_msg = res_send['message']['id']
                                                update().update_StatusOneChat(dataJson['sid'],data_tosender[n]['email'])
                                                resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                if resultgetProject['result'] == 'OK':
                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                    priority_ = '1'
                                                    titleAndDetails = resouce_result['messageText']
                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                        if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                    resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),dataJson['sid'],oneId)
                                                    if resultSend_CreateTask['result'] == 'OK':
                                                        if 'status' in resultSend_CreateTask['messageText']:
                                                            if resultSend_CreateTask['messageText']['status'] =='success':
                                                                list_taskChat_log.append({'result':'OK','sidCode':dataJson['sid'],'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                    else:
                                                        list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                else:
                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                elif res_search_frd['status'] == 'fail':
                                    arrEmail = []
                                    arrEmail.append(data_tosender[n]['email'])
                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                    if 'status' in resultAddfrd:
                                        if resultAddfrd['status'] == 'success':
                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                res_search_frd = search_frd(data_tosender[n]['email'])
                                                resouce_result = select().select_forChat_v1(dataJson['sid'])
                                                userId = res_search_frd['friend']['user_id']
                                                oneId = res_search_frd['friend']['one_id']
                                                if str(data_tosender[n]['property']).lower() == 'signning':
                                                    res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                elif str(data_tosender[n]['property']).lower() == 'approve':
                                                    res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                if 'status' in res_send:
                                                    if res_send['status'] == 'success':
                                                        id_one_chat_to_msg = res_send['message']['id']
                                                        update().update_StatusOneChat(dataJson['sid'],data_tosender[n]['email'])
                                                        resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                        if resultgetProject['result'] == 'OK':
                                                            projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                            priority_ = '1'
                                                            titleAndDetails = resouce_result['messageText']
                                                            for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                    state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                            resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),dataJson['sid'],oneId)
                                                            if resultSend_CreateTask['result'] == 'OK':
                                                                if 'status' in resultSend_CreateTask['messageText']:
                                                                    if resultSend_CreateTask['messageText']['status'] =='success':
                                                                        list_taskChat_log.append({'result':'OK','sidCode':dataJson['sid'],'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                    else:
                                                                        list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                else:
                                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                        list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    else:
                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                else:
                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                else:
                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                            elif 'result' in res_search_frd:
                                if res_search_frd['result'] == 'ER':
                                    arrEmail = []
                                    arrEmail.append(data_tosender[n]['email'])
                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                    # print(resultAddfrd,'resultAddfrd')
                                    if 'status' in resultAddfrd:
                                        if resultAddfrd['status'] == 'success':
                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                res_search_frd = search_frd(data_tosender[n]['email'])
                                                resouce_result = select().select_forChat_v1(dataJson['sid'])
                                                try:
                                                    userId = res_search_frd['friend']['user_id']
                                                    oneId = res_search_frd['friend']['one_id']
                                                except Exception as ex:
                                                    exc_type, exc_obj, exc_tb = sys.exc_info()
                                                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                                    print(exc_type, fname, exc_tb.tb_lineno)
                                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':str(exc_tb.tb_lineno) + str(exc_type)})

                                                if str(data_tosender[n]['property']).lower() == 'signning':
                                                    res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                elif str(data_tosender[n]['property']).lower() == 'approve':
                                                    res_send = send_url_tochat_new_v2(str(data_tosender[n]['property']).lower(),res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                if 'status' in res_send:
                                                    if res_send['status'] == 'success':
                                                        id_one_chat_to_msg = res_send['message']['id']
                                                        update().update_StatusOneChat(dataJson['sid'],data_tosender[n]['email'])
                                                        resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                        if resultgetProject['result'] == 'OK':
                                                            projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                            priority_ = '1'
                                                            titleAndDetails = resouce_result['messageText']
                                                            for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                    state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                            resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),dataJson['sid'],oneId)
                                                            if resultSend_CreateTask['result'] == 'OK':
                                                                if 'status' in resultSend_CreateTask['messageText']:
                                                                    if resultSend_CreateTask['messageText']['status'] =='success':
                                                                        list_taskChat_log.append({'result':'OK','sidCode':dataJson['sid'],'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                    else:
                                                                        list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                else:
                                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                        list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    else:
                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                else:
                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                            else:
                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                        else:
                            list_taskChat_log.append({'result':'NO','sidCode':dataJson['sid'],'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':dataJson['sid'],'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})

                if True in status_sendChat:
                    result_logChat = selection_email_insert(list_emailChat_log,id_one_chat_to_msg)
                    if result_logChat['result'] == 'OK':
                        insert().insert_transactionTask(list_taskChat_log)
                        return jsonify({'result':'OK','messageText':'send to onechat successfully!','status_Code':200,'messageER':None})
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                else:
                    result_logChat = selection_email_insert(list_emailChat_log,id_one_chat_to_msg)
                    return jsonify({'result':'OK','messageText':'Not Found Send To OneChat!','status_Code':200,'messageER':None})
            elif str(dataJson['type_service']).lower() =='next':
                resultURLIMAGE = createImage_formPDF(dataJson['sid'])
                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                data_name_file = dataJson['name_file']
                data_tracking = dataJson['tracking']
                resselect_ = select().select_transactionChat(dataJson['sid'])
                resselect_check = check_sendToChat(resselect_)
                result_Array = []

                for i in range(len(resselect_)):
                    if resselect_[i]['statusSign'] == 'Y':
                        resselect_[i]['statusSign'] = 'Complete'
                    elif resselect_[i]['statusSign'] == 'R':
                        resselect_[i]['statusSign'] = 'Reject'
                    else:
                        resselect_[i]['statusSign'] = 'Incomplete'

                    result_Array.append({
                        'emailUser':resselect_[i]['email_User'],
                        'statusSign':resselect_[i]['statusSign'],
                        'stepNum':int(resselect_[i]['stepNum']),
                        'datetime_string':resselect_[i]['datetime_string'],
                        'status_propertyChat':resselect_[i]['propertyChat'],
                        'url_Sign':resselect_[i]['url_Sign']
                    })
                # print(resselect_check , 'resselect_check')

                if resselect_check['result'] == 'OK':
                    if 'statusSign' in resselect_check['msg']:
                        print((resselect_check['msg']))
                        result_disble = disble_button_in_oneChat_v1(resselect_check['msg']['id_chat'])
                        if resselect_check['msg']['statusSign'] == 'R':
                            messageToChat = ''
                            stepnum_ = int(resselect_check['msg']['stepNum']) - 1
                            sid_ = resselect_check['msg']['sid']
                            email_ = resselect_check['msg']['email_User']
                            result_SelectBefore = select().select_transactionChat_before(stepnum_,sid_)
                            if result_SelectBefore['result'] == 'OK':
                                res_select = select().select_ForWebHook(sid_)
                                title_toChat = 'แจ้งเตือนระบบ Paperless'
                                msg_toChat = ''
                                count_res = 0
                                msg_toChat_Paper = ''
                                try:
                                    title_toChat  += '\n- เอกสารถูกปฏิเสธอนุมัติ -\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['sender_email'] + '\n'
                                    documentId = res_select['messageText']['documentId']
                                except Exception as ex:
                                    documentId = None
                                    pass
                                arr_step = []

                                for count in range(len(result_Array)):
                                    count_res = count + 1
                                    try:
                                        email_User = result_Array[count]['emailUser']
                                        statusSign = result_Array[count]['statusSign']
                                        datetime_string = result_Array[count]['datetime_string']
                                        arr_step.append(result_Array[count]['stepNum'])
                                    except Exception as ex:
                                        email_User = ''
                                        statusSign = ''
                                for n in arr_step:
                                    msg_toChat += '\nลำดับที่ ' + str(n)
                                    for count in range(len(result_Array)):
                                        try:
                                            email_User = result_Array[count]['emailUser']
                                            statusSign = result_Array[count]['statusSign']
                                            status_propertyChat = result_Array[count]['status_propertyChat']
                                            if status_propertyChat == 'signning':
                                                if statusSign == 'Complete':
                                                    statusSign = 'เซ็นแล้ว'
                                                elif statusSign == 'Pending':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                elif statusSign == 'Incomplete':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                else:
                                                    statusSign = 'ไม่อนุมัติ'
                                            elif status_propertyChat == 'approve':
                                                if statusSign == 'Complete':
                                                    statusSign = 'อนุมัติแล้ว'
                                                elif statusSign == 'Pending':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                elif statusSign == 'Incomplete':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                else:
                                                    statusSign = 'ไม่อนุมัติ'
                                            datetime_string = result_Array[count]['datetime_string']
                                        except Exception as ex:
                                            email_User = ''
                                            statusSign = ''
                                        if result_Array[count]['stepNum'] == n:
                                            msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                                messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                                for i in range(len(result_SelectBefore['messageText'])):
                                    emailBfore = result_SelectBefore['messageText'][i]['email_User']
                                #     email_ =
                                    res_search_frd = search_frd(emailBfore)
                                    user_id_chat = res_search_frd['friend']['user_id']
                                    result_sendChat = send_messageToChat(messageToChat,user_id_chat)
                                    print(result_sendChat)
                            return jsonify({'result':'OK','messageText':'send chat ok and reject document','status_Code':200,'messageER':None})
                        elif resselect_check['msg']['statusSign'] == 'Y':
                            print(result_disble)
                            pass
                        else:
                            pass
                    try:
                        # pass
                        result_Task = select().select_transactionTaskChat(resselect_check)
                        # print(result_Task, 'result_Task')
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found DATA! transactionTask'})
                    # return ''
                    for u in result_Task:
                        res_search_frd = search_frd(u['emailUser'])
                        sid_code = u['sidCode']
                        emailUser = u['emailUser']
                        step_num = u['step_num']
                        task_id = u['task_id']
                        task_state_name_new = 'done'
                        userId = res_search_frd['friend']['user_id']
                        oneId = res_search_frd['friend']['one_id']
                        resultgetProject = sendtask_getProject_tochat_v1(oneId)
                        if resultgetProject['result'] == 'OK':
                            if len(resultgetProject['messageText']['data']) != 0:
                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'done':
                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']

                                state_id = state_id_

                                resultChangeState = sendtask_change_stateChat(state_id,task_id)
                                if resultChangeState['result'] == 'OK':
                                    update().update_taskchat_state(sid_code,emailUser,step_num,task_state_name_new,state_id)

                    try:
                        arr_tc = select().select_transactionChat_next(resselect_check)
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found DATA!'})
                    # print(arr_tc,'arr_tc')
                    for k in arr_tc:
                        status_Sign = k['statusSign']
                        if status_Sign != 'R':
                            res_search_frd = search_frd(k['email_User'])
                            resouce_result = select().select_forChat_v1(dataJson['sid'])
                            if 'status' in res_search_frd:
                                if res_search_frd['status'] == 'success':

                                    userId = res_search_frd['friend']['user_id']
                                    oneId = res_search_frd['friend']['one_id']
                                    data_Url,data_property = select().select_UrlSign_SidCodeEmailUser(dataJson['sid'],k['email_User'])
                                    if resouce_result['result'] == 'OK':
                                        result = send_url_tochat_next_new_v1(data_property,res_search_frd['friend']['user_id'],data_name_file,data_tracking,data_Url,k['transactionCode'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                        if 'status' in result:
                                            if result['status'] == 'success':
                                                id_one_chat_to_msg = result['message']['id']
                                                update().update_StatusOneChat(dataJson['sid'],k['email_User'])
                                                resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                if resultgetProject['result'] == 'OK':
                                                    print(resultgetProject)
                                                    if len(resultgetProject['messageText']['data']) != 0:
                                                        projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                        priority_ = '1'
                                                        titleAndDetails = resouce_result['messageText']
                                                        for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                            if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                        resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_property).lower(),dataJson['sid'],oneId)
                                                        if resultSend_CreateTask['result'] == 'OK':
                                                            if 'status' in resultSend_CreateTask['messageText']:
                                                                if resultSend_CreateTask['messageText']['status'] =='success':
                                                                    list_taskChat_log.append({'result':'OK','sidCode':dataJson['sid'],'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'step_num':k['stepNum'],'email':(k['email_User'])})
                                                                else:
                                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                else:
                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                list_emailChat_log.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                    else:
                                        result = send_url_tochat_next_new_v1(data_property,res_search_frd['friend']['user_id'],data_name_file,data_tracking,data_Url,k['transactionCode'],dataJson['sid'],None,result_pathUrl)
                                        if 'status' in result:
                                            if result['status'] == 'success':
                                                id_one_chat_to_msg = result['message']['id']
                                                update().update_StatusOneChat(dataJson['sid'],k['email_User'])
                                                list_emailChat_log.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                else:
                                    list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                            elif 'result' in res_search_frd:
                                if res_search_frd['result'] == 'ER':
                                    arrEmail = []
                                    arrEmail.append(k['email_User'])
                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                    if 'status' in resultAddfrd:
                                        if resultAddfrd['status'] == 'success':
                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                res_search_frd = search_frd(k['email_User'])
                                                data_Url,data_property = select().select_UrlSign_SidCodeEmailUser(dataJson['sid'],k['email_User'])
                                                resouce_result = select().select_forChat_v1(dataJson['sid'])
                                                if resouce_result['result'] == 'OK':
                                                    result = send_url_tochat_next_new_v1(data_property,res_search_frd['friend']['user_id'],data_name_file,data_tracking,data_Url,k['transactionCode'],dataJson['sid'],resouce_result['messageText'],result_pathUrl)
                                                    if 'status' in result:
                                                        if result['status'] == 'success':
                                                            id_one_chat_to_msg = result['message']['id']
                                                            update().update_StatusOneChat(dataJson['sid'],k['email_User'])
                                                            resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                            if resultgetProject['result'] == 'OK':
                                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                priority_ = '1'
                                                                titleAndDetails = resouce_result['messageText']
                                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_property).lower(),dataJson['sid'],oneId)
                                                                if resultSend_CreateTask['result'] == 'OK':
                                                                    if 'status' in resultSend_CreateTask['messageText']:
                                                                        if resultSend_CreateTask['messageText']['status'] =='success':
                                                                            list_taskChat_log.append({'result':'OK','sidCode':dataJson['sid'],'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'step_num':k['stepNum'],'email':(k['email_User'])})
                                                                        else:
                                                                            list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                                    else:
                                                                        list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                                else:
                                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                            list_emailChat_log.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                                        else:
                                                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                                    else:
                                                        list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                                else:
                                                    result = send_url_tochat_next_new_v1(data_property,res_search_frd['friend']['user_id'],data_name_file,data_tracking,data_Url,k['transactionCode'],dataJson['sid'],None,result_pathUrl)
                                                    if 'status' in result:
                                                        if result['status'] == 'success':
                                                            id_one_chat_to_msg = result['message']['id']
                                                            update().update_StatusOneChat(dataJson['sid'],k['email_User'])
                                                            resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                            if resultgetProject['result'] == 'OK':
                                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                priority_ = '1'
                                                                titleAndDetails = resouce_result['messageText']
                                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_property).lower(),dataJson['sid'],oneId)
                                                                if resultSend_CreateTask['result'] == 'OK':
                                                                    if 'status' in resultSend_CreateTask['messageText']:
                                                                        if resultSend_CreateTask['messageText']['status'] =='success':
                                                                            list_taskChat_log.append({'result':'OK','sidCode':dataJson['sid'],'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'step_num':k['stepNum'],'email':(k['email_User'])})
                                                                        else:
                                                                            list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                                    else:
                                                                        list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                                else:
                                                                    list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                                            list_emailChat_log.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                                        else:
                                                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                                    else:
                                                        list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                            else:
                                                list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                        else:
                                            list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                                    else:
                                        list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                            else:
                                list_taskChat_log.append({'result':'NO','sidCode':dataJson['sid'],'messageText':None,'step_num':k['stepNum'],'email':(k['email_User'])})
                                list_emailChat_log.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                        else:
                            print('----------------------///---------------------------')
                print(list_emailChat_log)
                if len(list_emailChat_log) != 0:
                    resultUpdateTask = update().update_taskchat_nextstep(list_taskChat_log)
                    print(resultUpdateTask)
                    result_update = update().update_ChatToSend_(list_emailChat_log)
                    res_select = select().select_ForWebHook(dataJson['sid'])
                    title_toChat = 'แจ้งเตือนระบบ Paperless'
                    msg_toChat = ''
                    count_res = 0
                    msg_toChat_Paper = ''
                    try:
                        title_toChat  += '\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['sender_email'] + '\n'
                        documentId = res_select['messageText']['documentId']
                    except Exception as ex:
                        documentId = None
                        pass
                    arr_step = []

                    for count in range(len(result_Array)):
                        count_res = count + 1
                        try:
                            email_User = result_Array[count]['emailUser']
                            statusSign = result_Array[count]['statusSign']
                            datetime_string = result_Array[count]['datetime_string']
                            arr_step.append(result_Array[count]['stepNum'])
                        except Exception as ex:
                            email_User = ''
                            statusSign = ''
                    for n in arr_step:
                        msg_toChat += '\nลำดับที่ ' + str(n)
                        for count in range(len(result_Array)):
                            try:
                                email_User = result_Array[count]['emailUser']
                                statusSign = result_Array[count]['statusSign']
                                status_propertyChat = result_Array[count]['status_propertyChat']
                                if status_propertyChat == 'signning':
                                    if statusSign == 'Complete':
                                        statusSign = 'เซ็นแล้ว'
                                    elif statusSign == 'Pending':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    elif statusSign == 'Incomplete':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    else:
                                        statusSign = 'ไม่อนุมัติ'
                                elif status_propertyChat == 'approve':
                                    if statusSign == 'Complete':
                                        statusSign = 'อนุมัติแล้ว'
                                    elif statusSign == 'Pending':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    elif statusSign == 'Incomplete':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    else:
                                        statusSign = 'ไม่อนุมัติ'
                                datetime_string = result_Array[count]['datetime_string']
                            except Exception as ex:
                                email_User = ''
                                statusSign = ''
                            if result_Array[count]['stepNum'] == n:
                                msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                    messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                    result_Email = select().select_GETEmail(dataJson['sid'])
                    res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                    if 'status' in res_search_frd:
                        if res_search_frd['status'] == 'success':
                            result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                            if result_sendChat['status'] == 'success':
                                return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                            else:
                                return jsonify({'result':'ER','messageText':'sendChat fail','status_Code':200,'messageER':None,'messageType':'chat'})
                        else:
                            return jsonify({'result':'ER','messageText':'not found friend','status_Code':200,'messageER':None,'messageType':'chat'})
                else:
                    res_select = select().select_ForWebHook(dataJson['sid'])
                    title_toChat = 'แจ้งเตือนระบบ Paperless'
                    msg_toChat = ''
                    count_res = 0
                    msg_toChat_Paper = ''
                    # res_select['messageText']['PDF_String'] = None
                    # print(res_select['messageText'] , ' res_select 007')
                    try:
                        title_toChat  += '\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['sender_email'] + '\n'
                        documentId = res_select['messageText']['documentId']
                    except Exception as ex:
                        documentId = None
                        pass
                    arr_step = []
                    for count in range(len(result_Array)):
                        count_res = count + 1
                        try:
                            email_User = result_Array[count]['emailUser']
                            statusSign = result_Array[count]['statusSign']
                            datetime_string = result_Array[count]['datetime_string']
                            if result_Array[count]['stepNum'] not in arr_step:
                                arr_step.append(result_Array[count]['stepNum'])
                        except Exception as ex:
                            email_User = ''
                            statusSign = ''

                    for n in arr_step:
                        msg_toChat += '\nลำดับที่ ' + str(n)
                        for count in range(len(result_Array)):
                            try:
                                email_User = result_Array[count]['emailUser']
                                statusSign = result_Array[count]['statusSign']
                                status_propertyChat = result_Array[count]['status_propertyChat']
                                if status_propertyChat == 'signning':
                                    if statusSign == 'Complete':
                                        statusSign = 'เซ็นแล้ว'
                                    elif statusSign == 'Pending':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    elif statusSign == 'Incomplete':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    else:
                                        statusSign = 'ไม่อนุมัติ'
                                elif status_propertyChat == 'approve':
                                    if statusSign == 'Complete':
                                        statusSign = 'อนุมัติแล้ว'
                                    elif statusSign == 'Pending':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    elif statusSign == 'Incomplete':
                                        statusSign = 'ยังไม่อนุมัติ'
                                    else:
                                        statusSign = 'ไม่อนุมัติ'
                                datetime_string = result_Array[count]['datetime_string']
                            except Exception as ex:
                                email_User = ''
                                statusSign = ''
                            if result_Array[count]['stepNum'] == n:
                               msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                    result_select_action = select().select_get_action_and_status('robot')
                    # print(result_select_action , ' result_select_action')
                    if result_select_action['result'] == 'OK':
                        if result_select_action['messageText']['status'] == True:
                            resultselect_ = select().select_attm_file_v1_for_chat_api_to_robot(dataJson['sid'])
                            if resultselect_['result'] == 'OK':
                                doc_id = resultselect_['messageText']['document_Id']
                                pathFolder = resultselect_['messageText']['pathfolder']
                                json_Data_File = resultselect_['messageText']['json_data']
                                username_sender = resultselect_['messageText']['sender_username']
                                document_Type = resultselect_['messageText']['document_Type']
                                if document_Type == 'CS':
                                    sftp_robot().send_file_tosftp_v1(json_Data_File,pathFolder,'/Create',document_Type)
                                elif document_Type == 'CSPOC':
                                    sftp_robot().send_file_tosftp_v1(json_Data_File,pathFolder,'/Create/CSPOC',document_Type)
                                    # mail_to_robot().send_to_robot(pathFolder,json_Data_File,username_sender,doc_id)
                        else:
                            print(result_select_action['messageText']['status'])
                    # print(res_select , 'res_select')
                    # if (res_select['result'] == 'OK' and res_select['messageText']['email_center'] != ''):
                    #     messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                    if (res_select['result'] == 'OK' and res_select['messageText']['webHook'] != None):
                            # webHook_Data = {
                            #     "result":"OK",
                            #     "status_Code":200,
                            #     "trackingId" :data_tracking,
                            #     "file_Name" :data_name_file,
                            #     "messageText":result_Array,
                            #     "documentId":  documentId
                            # }
                        webHook_Data = res_select['messageText']
                        try:
                            response = requests.post(res_select['messageText']['webHook'], json=webHook_Data,headers={'Content-Type': 'application/json'},timeout=10,verify=False)
                        except requests.HTTPError as err:
                            pass
                            # return jsonify({'result': 'ER','status': 'HTTPError','messageText': "HTTP error occurred.",'messageType':'webhook'})
                        except requests.Timeout as err:
                            pass
                            # return jsonify({'result': 'ER','status': 'Timeout','messageText': 'Request timed out','messageType':'webhook'})
                        except requests.ConnectionError as err:
                            pass
                            # return jsonify({'result': 'ER','status': 'ConnectionError','messageText': 'API Connection error occurred.','messageType':'webhook'})
                        except Exception as ex:
                            pass

                            # return jsonify({'result': 'ER','status': 'Exception','messageText': 'An unexpected error: ' + str(ex),'messageType':'webhook'})

                    elif res_select['result'] == 'OK':

                        messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                        result_Email = select().select_GETEmail(dataJson['sid'])
                        res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                        if 'status' in res_search_frd:
                            if res_search_frd['status'] == 'success':
                                result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                                if 'status' in result_sendChat:
                                    if result_sendChat['status'] == 'success':
                                        return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                                    elif result_sendChat['status'] == 'fail':
                                        arrmail = []
                                        arrmail.append(result_Email['messageText']['email_Sender'])
                                        result_AddfrdAuto = addbot_tofrdAUto(arrmail)
                                        res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                                        if res_search_frd['status'] == 'success':
                                            result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                                        return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                                elif 'result' in result_sendChat:
                                    if result_sendChat['result'] == 'ER':
                                        arrmail = []
                                        arrmail.append(result_Email['messageText']['email_Sender'])
                                        result_AddfrdAuto = addbot_tofrdAUto(arrmail)
                                        res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                                        if res_search_frd['status'] == 'success':
                                            result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                                        return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                                    else:
                                        print()
                            else:
                                return jsonify({'result':'ER','messageText':'not found friend','status_Code':200,'messageER':None,'messageType':'chat'})
                        elif 'result' in res_search_frd:
                            arrmail = []
                            arrmail.append(result_Email['messageText']['email_Sender'])
                            result_AddfrdAuto = addbot_tofrdAUto(arrmail)
                            res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                            if res_search_frd['status'] == 'success':
                                result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                            return jsonify({'result':'OK','messageText':'sendChat ok','status_Code':200,'messageER':None,'messageType':'chat'})
                    # print(res_select)
                    result_update = 'Continue'
                return jsonify({'result':'OK','messageText':res_select['messageText'],'status_Code':200,'messageER':None,'messageType':'webhook'})
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':'No ServiceType!'})
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'Parameter Fail!'})
    elif request.method == 'GET':
        if (request.args.get('email')) != None:
            arr_mailre = []
            eval_arr = eval(request.args.get('email'))
            print(len((eval_arr)))
            for n in range(len((eval_arr))):
                print(eval_arr[n])
                json_onechat = {}
                emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", eval_arr[n])
                if emails is None:
                    return jsonify({'result':'ER','messageText':'ข้อมูล email ไม่ตรงตามรูปแบบ','status_Code':200}),200
                else:
                    pass
                try:
                    res_search_frd = search_frd(str(eval_arr[n]).replace(' ',''))
                    if 'result' in res_search_frd:
                        json_onechat['result'] = 'ER'
                        json_onechat['email'] = eval_arr[n]
                    elif 'status' in res_search_frd:
                        json_onechat['result'] = 'OK'
                        json_onechat['email'] = eval_arr[n]
                except KeyError as ex:
                    print(ex)
                arr_mailre.append(json_onechat)
            return jsonify({'result':'OK','messageText':arr_mailre,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/v7/<string:type_chat>/chat_sender', methods=['POST','GET'])
@token_required
def chat_api_v7(type_chat):
    if str(type_chat).lower() == 'first':
        if request.method == 'POST':
            dataJson = request.json
            if 'data' in dataJson and 'sid_code' in dataJson and len(dataJson) == 2:
                sidcode = dataJson['sid_code']
                data_json = dataJson['data']
                resultURLIMAGE = createImage_formPDF2(sidcode)
                if resultURLIMAGE['result'] == 'OK':
                    result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE['data']
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error createImage PDF'}),200
                if len(data_json) != 0:
                    list_taskChat_log = []
                    list_Chat_log = []
                    for n in range(len(data_json)):
                        data_tosender = data_json
                        if 'email' in data_tosender[n] and 'url_sign' in data_tosender[n] and 'tracking' in data_tosender[n] and 'name_file' in data_tosender[n] and 'message' in data_tosender[n] and 'step_num' in data_tosender[n] and 'sendChat' in data_tosender[n] and 'property' in data_tosender[n] and len(data_tosender[n]) == 8:
                            sender_email = data_tosender[n]['email']
                            sender_url_sign_email = data_tosender[n]['url_sign']
                            sender_tracking = data_tosender[n]['tracking']
                            sender_name_file = data_tosender[n]['name_file']
                            sender_message = data_tosender[n]['message']
                            sender_step_num = data_tosender[n]['step_num']
                            sender_sendChat = data_tosender[n]['sendChat']
                            sender_property = data_tosender[n]['property']
                            if sender_step_num == '1' and sender_sendChat == True:
                                res_search_frd = search_frd(sender_email)
                                if 'status' in res_search_frd:
                                    if res_search_frd['status'] == 'success':
                                        user_id_info = res_search_frd['friend']['user_id']
                                        one_id_info = res_search_frd['friend']['one_id']
                                        resouce_result = select().select_forChat_v2(sidcode)
                                        if resouce_result['result'] == 'OK':
                                            res_send = send_url_tochat_new_v3(str(sender_property).lower(),user_id_info,sender_name_file,sender_tracking,sender_url_sign_email,sidcode,resouce_result['messageText'],result_pathUrl)
                                            if 'status' in res_send:
                                                if res_send['status'] == 'success':
                                                    message_from_onechat = res_send['message']
                                                    id_chat = message_from_onechat['id']
                                                    result_update = update().update_StatusOneChat_v2(sidcode,sender_email,sender_step_num)
                                                    resultgetProject = sendtask_getProject_tochat_v2(one_id_info)
                                                    if resultgetProject['result'] == 'OK':
                                                        projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                        priority_ = '1'
                                                        titleAndDetails = resouce_result['messageText']
                                                        for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                            if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                        resultSend_CreateTask = sendtask_creattask_tochat_v2(projectid_,priority_,titleAndDetails,state_id_,str(sender_property).lower(),sidcode,one_id_info)
                                                        if resultSend_CreateTask['result'] == 'OK':
                                                            if 'status' in resultSend_CreateTask['messageText']:
                                                                if resultSend_CreateTask['messageText']['status'] =='success':
                                                                    list_taskChat_log.append({'result':'OK','sidCode':sidcode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                                                else:
                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                                    else:
                                                        list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                                    list_Chat_log.append({'result':'OK','email':sender_email,'sid':sidcode,'step_num':sender_step_num,'sendChat':sender_sendChat,'urlSign':sender_url_sign_email,'property':sender_property,'id_chat':id_chat,'message_chat':message_from_onechat})
                                                else:
                                                    list_Chat_log.append({'result':'NO','email':sender_email,'sid':sidcode,'step_num':sender_step_num,'sendChat':sender_sendChat,'urlSign':sender_url_sign_email,'property':sender_property,'id_chat':None,'message_chat':''})
                                            else:
                                                list_Chat_log.append({'result':'ER','email':sender_email,'sid':sidcode,'step_num':sender_step_num,'sendChat':sender_sendChat,'urlSign':sender_url_sign_email,'property':sender_property,'id_chat':None,'message_chat':''})
                                        else:
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error data not found'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error search frd one chat'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error search frd one chat'}),200
                            else:
                                list_taskChat_log.append({'result':'NO','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                list_Chat_log.append({'result':'NO','email':sender_email,'sid':sidcode,'step_num':sender_step_num,'sendChat':sender_sendChat,'urlSign':sender_url_sign_email,'property':sender_property,'id_chat':None,'message_chat':''})
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect in data'}),404
                    if len(list_Chat_log) != 0:
                        result_logChat = selection_email_insert_v2(list_Chat_log)
                        if result_logChat['result'] == 'OK':
                            result_insert = insert().insert_transactionTask(list_taskChat_log)
                            if result_insert['result'] == 'OK':
                                return jsonify({'result':'OK','messageText':'send to onechat successfully','status_Code':200,'messageER':None}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'cant insert data'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list no information'}),200
                    return jsonify({'result':'OK','messageText':list_Chat_log,'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect in data'}),404
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
    elif str(type_chat).lower() == 'next':
        if request.method == 'POST':
            dataJson = request.json
            if 'sid_code' in dataJson and len(dataJson) == 1:
                sidCode = dataJson['sid_code']
                resultURLIMAGE = createImage_formPDF(sidCode)
                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                resselect_transactionChat = select().select_transactionChat(sidCode)
                resselect_check = check_sendToChat(resselect_transactionChat)
                result_Array = []
                for i in range(len(resselect_transactionChat)):
                    if resselect_transactionChat[i]['statusSign'] == 'Y':
                        resselect_transactionChat[i]['statusSign'] = 'Complete'
                    elif resselect_transactionChat[i]['statusSign'] == 'R':
                        resselect_transactionChat[i]['statusSign'] = 'Reject'
                    else:
                        resselect_transactionChat[i]['statusSign'] = 'Incomplete'

                    result_Array.append({
                        'emailUser':resselect_transactionChat[i]['email_User'],
                        'statusSign':resselect_transactionChat[i]['statusSign'],
                        'stepNum':int(resselect_transactionChat[i]['stepNum']),
                        'datetime_string':resselect_transactionChat[i]['datetime_string'],
                        'status_propertyChat':resselect_transactionChat[i]['propertyChat'],
                        'url_Sign':resselect_transactionChat[i]['url_Sign']
                    })
                print(result_Array)
                if resselect_check['result'] == 'OK':
                    print(resselect_check)
                    if 'statusSign' in resselect_check['msg']:
                        print(resselect_check['msg'])
                        disble_button_in_oneChat_v2(resselect_check['msg']['id_chat'],2,token_header)
                        if resselect_check['msg']['statusSign'] == 'R':
                            stepNum = resselect_check['msg']['stepNum']
                            print(resselect_check)
                            result_SelectBefore = select().select_transactionChat_before(stepNum,sidCode)
                            res_select = select().select_ForWebHook(sidCode)

                            title_toChat = 'แจ้งเตือนระบบ Paperless'
                            msg_toChat = ''
                            count_res = 0
                            msg_toChat_Paper = ''
                            try:
                                title_toChat  += '\n- เอกสารถูกปฏิเสธอนุมัติ -\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['userSender'] + '\n'
                                documentId = res_select['messageText']['documentId']
                            except Exception as ex:
                                documentId = None
                                pass
                            arr_step = []
                            print(documentId)
                            for count in range(len(result_Array)):
                                count_res = count + 1
                                try:
                                    email_User = result_Array[count]['emailUser']
                                    statusSign = result_Array[count]['statusSign']
                                    datetime_string = result_Array[count]['datetime_string']
                                    arr_step.append(result_Array[count]['stepNum'])
                                except Exception as ex:
                                    email_User = ''
                                    statusSign = ''
                            for n in arr_step:
                                msg_toChat += '\nลำดับที่ ' + str(n)
                                for count in range(len(result_Array)):
                                    try:
                                        email_User = result_Array[count]['emailUser']
                                        statusSign = result_Array[count]['statusSign']
                                        status_propertyChat = result_Array[count]['status_propertyChat']
                                        if status_propertyChat == 'signning':
                                            if statusSign == 'Complete':
                                                statusSign = 'อนุมัติแล้ว'
                                            elif statusSign == 'Pending':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            elif statusSign == 'Incomplete':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            else:
                                                statusSign = 'ไม่อนุมัติ'
                                        elif status_propertyChat == 'approve':
                                            if statusSign == 'Complete':
                                                statusSign = 'อนุมัติแล้ว'
                                            elif statusSign == 'Pending':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            elif statusSign == 'Incomplete':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            else:
                                                statusSign = 'ไม่อนุมัติ'
                                        datetime_string = result_Array[count]['datetime_string']
                                    except Exception as ex:
                                        email_User = ''
                                        statusSign = ''
                                    if result_Array[count]['stepNum'] == n:
                                        msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''

                            messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                            print(messageToChat)
                            for i in range(len(result_SelectBefore['messageText'])):
                                email_before = result_SelectBefore['messageText'][i]['email_User']
                                print(email_before)
                            # # #     email_ =
                                res_search_frd = search_frd(email_before)
                                user_id_chat = res_search_frd['friend']['user_id']
                                result_sendChat = send_messageToChat(messageToChat,user_id_chat)
                                print(result_sendChat)
                            return jsonify({'result':'OK','messageText':'send to chat and reject document','status_Code':200,'messageER':None}),200
                    try:
                        result_select_Chat_next = select().select_transactionChat_next(resselect_check)
                    except Exception as ex:
                        print(str(ex))
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found ' + str(ex)}),200
                    print(result_select_Chat_next)
                    list_taskChat_log = []
                    list_sendChat_log = []
                    for k in result_select_Chat_next:
                        status_Sign = k['statusSign']
                        email_user = k['email_User']
                        transactionCode = k['transactionCode']
                        tracking_id = k['tracking_id']
                        file_name = k['file_name']
                        step_num = k['stepNum']
                        print(k)
                        if status_Sign != 'R':
                            res_search_frd = search_frd(email_user)
                            resouce_result = select().select_forChat_v2(sidCode)
                            print(resouce_result)
                            print(res_search_frd)
                            if 'status' in res_search_frd:
                                if res_search_frd['status'] == 'success':
                                    user_id_info = res_search_frd['friend']['user_id']
                                    one_id_info = res_search_frd['friend']['one_id']
                                    data_url,data_property = select().select_UrlSign_SidCodeEmailUser(sidCode,email_user)
                                    if resouce_result['result'] == 'OK':
                                        result_sendChat = send_url_tochat_new_v3(data_property,user_id_info,file_name,tracking_id,data_url,sidCode,resouce_result['messageText'],result_pathUrl)
                                        if 'status' in result_sendChat:
                                            if result_sendChat['status'] == 'success':
                                                message_from_chat = result_sendChat['message']
                                                id_chat = result_sendChat['message']['id']
                                                result_update = update().update_StatusOneChat_v2(sidCode,email_user,step_num)
                                                print(result_update)
                                                print(result_sendChat)
                                                resultgetProject = sendtask_getProject_tochat_v1(one_id_info)
                                                if resultgetProject['result'] == 'OK':
                                                    print(resultgetProject)
                                                    if len(resultgetProject['messageText']['data']) != 0:
                                                        projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                        priority_ = '1'
                                                        titleAndDetails = resouce_result['messageText']
                                                        for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                            if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                        resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_property).lower(),sidCode,one_id_info)
                                                        print(resultSend_CreateTask)
                                                        if resultSend_CreateTask['result'] == 'OK':
                                                            if 'status' in resultSend_CreateTask['messageText']:
                                                                if resultSend_CreateTask['messageText']['status'] =='success':
                                                                    list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'step_num':step_num,'email':email_user})
                                                                else:
                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'step_num':step_num,'email':email_user})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'step_num':step_num,'email':email_user})
                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'step_num':step_num,'email':email_user})
                                                else:
                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'step_num':step_num,'email':email_user})
                                                list_sendChat_log.append({'result':'OK','email':email_user,'sid':sidCode,'transactionCode':transactionCode,'stepNum':step_num,'id_chat':id_chat})
                                            else:
                                                list_sendChat_log.append({'result':'ER','email':email_user,'sid':sidCode,'transactionCode':transactionCode,'stepNum':step_num,'id_chat':None})
                                        else:
                                            list_sendChat_log.append({'result':'ER','email':email_user,'sid':sidCode,'transactionCode':transactionCode,'stepNum':step_num,'id_chat':None})
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error in select UrlSign SidCodeEmailUser'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error search friend one chat'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error search friend one chat'}),200
                    if len(list_sendChat_log) != 0:
                        print(list_sendChat_log)
                        resultUpdateTask = update().update_taskchat_nextstep(list_taskChat_log)
                        result_update = update().update_ChatToSend_v2(list_sendChat_log)
                        result_select = select().select_ForWebHook(sidCode)
                        title_toChat = 'แจ้งเตือนระบบ Paperless'
                        msg_toChat = ''
                        count_res = 0
                        msg_toChat_Paper = ''
                        try:
                            title_toChat  += '\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['sender_email'] + '\n'
                            documentId = res_select['messageText']['documentId']
                        except Exception as ex:
                            documentId = None
                            pass
                        arr_step = []
                        for count in range(len(result_Array)):
                            count_res = count + 1
                            try:
                                email_User = result_Array[count]['emailUser']
                                statusSign = result_Array[count]['statusSign']
                                datetime_string = result_Array[count]['datetime_string']
                                arr_step.append(result_Array[count]['stepNum'])
                            except Exception as ex:
                                email_User = ''
                                statusSign = ''
                        for n in arr_step:
                            msg_toChat += '\nลำดับที่ ' + str(n)
                            for count in range(len(result_Array)):
                                try:
                                    email_User = result_Array[count]['emailUser']
                                    statusSign = result_Array[count]['statusSign']
                                    status_propertyChat = result_Array[count]['status_propertyChat']
                                    if status_propertyChat == 'signning':
                                        if statusSign == 'Complete':
                                            statusSign = 'อนุมัติแล้ว'
                                        elif statusSign == 'Pending':
                                            statusSign = 'ยังไม่อนุมัติ'
                                        elif statusSign == 'Incomplete':
                                            statusSign = 'ยังไม่อนุมัติ'
                                        else:
                                            statusSign = 'ไม่อนุมัติ'
                                    elif status_propertyChat == 'approve':
                                        if statusSign == 'Complete':
                                            statusSign = 'อนุมัติแล้ว'
                                        elif statusSign == 'Pending':
                                            statusSign = 'ยังไม่อนุมัติ'
                                        elif statusSign == 'Incomplete':
                                            statusSign = 'ยังไม่อนุมัติ'
                                        else:
                                            statusSign = 'ไม่อนุมัติ'
                                    datetime_string = result_Array[count]['datetime_string']
                                except Exception as ex:
                                    email_User = ''
                                    statusSign = ''
                                if result_Array[count]['stepNum'] == n:
                                    msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                        messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                        result_Email = select().select_GETEmail(sidCode)
                        if result_Email['result'] == 'OK':
                            res_search_frd = search_frd(result_Email['messageText']['email_Sender'])
                            if 'status' in res_search_frd:
                                if res_search_frd['status'] == 'success':
                                    result_sendChat = send_messageToChat(messageToChat,res_search_frd['friend']['user_id'])
                                    if result_sendChat['status'] == 'success':
                                        return jsonify({'result':'OK','messageText':'send chat success','status_Code':200,'messageER':None,'messageType':'chat'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':'send chat fail','status_Code':200,'messageER':None,'messageType':'chat'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found friend','messageType':'chat'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'service search friend error','messageType':'chat'}),200
                        else:
                            return jsonify({'result':'OK','messageText':'send chat success','status_Code':200,'messageER':None,'messageType':'chat'}),200
                    else:
                        res_select = select().select_ForWebHook(sidCode)
                        title_toChat = 'แจ้งเตือนระบบ Paperless'
                        msg_toChat = ''
                        count_res = 0
                        msg_toChat_Paper = ''
                        print(res_select['messageText'])
                        try:
                            title_toChat  += '\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['sender_email'] + '\n'
                            documentId = res_select['messageText']['documentId']
                        except Exception as ex:
                            documentId = None
                            pass
                        arr_step = []
                        for count in range(len(result_Array)):
                            count_res = count + 1
                            try:
                                email_User = result_Array[count]['emailUser']
                                statusSign = result_Array[count]['statusSign']
                                datetime_string = result_Array[count]['datetime_string']
                                if result_Array[count]['stepNum'] not in arr_step:
                                    arr_step.append(result_Array[count]['stepNum'])
                            except Exception as ex:
                                email_User = ''
                                statusSign = ''

                        for n in arr_step:
                            msg_toChat += '\nลำดับที่ ' + str(n)
                            for count in range(len(result_Array)):
                                try:
                                    email_User = result_Array[count]['emailUser']
                                    statusSign = result_Array[count]['statusSign']
                                    status_propertyChat = result_Array[count]['status_propertyChat']
                                    if status_propertyChat == 'signning':
                                        if statusSign == 'Complete':
                                            statusSign = 'อนุมัติแล้ว'
                                        elif statusSign == 'Pending':
                                            statusSign = 'ยังไม่อนุมัติ'
                                        elif statusSign == 'Incomplete':
                                            statusSign = 'ยังไม่อนุมัติ'
                                        else:
                                            statusSign = 'ไม่อนุมัติ'
                                    elif status_propertyChat == 'approve':
                                        if statusSign == 'Complete':
                                            statusSign = 'อนุมัติแล้ว'
                                        elif statusSign == 'Pending':
                                            statusSign = 'ยังไม่อนุมัติ'
                                        elif statusSign == 'Incomplete':
                                            statusSign = 'ยังไม่อนุมัติ'
                                        else:
                                            statusSign = 'ไม่อนุมัติ'
                                    datetime_string = result_Array[count]['datetime_string']
                                except Exception as ex:
                                    email_User = ''
                                    statusSign = ''
                                if result_Array[count]['stepNum'] == n:
                                    msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                        messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                        result_Email = select().select_GETEmail(sidCode)
                        email_sender_user = result_Email['messageText']['email_Sender']
                        result_search_frd = search_frd(email_sender_user)
                        print(result_search_frd)
                        if 'status' in result_search_frd:
                            if result_search_frd['status'] == 'success':
                                user_id_info = result_search_frd['friend']['user_id']
                                result_send_chat = send_messageToChat(messageToChat,user_id_info)
                                if 'status' in result_send_chat:
                                    if result_send_chat['status'] == 'success':
                                        return jsonify({'result':'OK','messageText':'send chat success','status_Code':200,'messageER':None,'messageType':'chat'})
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'send chat fail','messageType':'chat'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'send chat fail','messageType':'chat'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found friend','messageType':'chat'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'service search friend error','messageType':'chat'}),200

                return jsonify({'result':'OK','messageText':list_sendChat_log,'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'service type incorrect'}),404

@status_methods.route('/api/v8/<string:type_chat>/chat_sender', methods=['POST','GET'])
@token_required
def chat_api_v8(type_chat):
    if str(type_chat).lower() == 'first':
        if request.method == 'POST':
            try:
                token_header = request.headers['Authorization']
                try:
                    token_header = str(token_header).split(' ')[1]
                except Exception as ex:
                    return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
            except KeyError as ex:
                return redirect(url_paperless)
            dataJson = request.json
            if 'data' in dataJson and 'sid_code' in dataJson and len(dataJson) == 2:
                try:
                    sidcode = dataJson['sid_code']
                    data_json = dataJson['data']
                    resultURLIMAGE = createImage_formPDF2(sidcode)
                    if resultURLIMAGE['result'] == 'OK':
                        result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE['data']
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error createImage PDF'}),200
                    if len(data_json) != 0:
                        list_taskChat_log = []
                        list_Chat_log = []
                        for n in range(len(data_json)):
                            data_tosender = data_json
                            if 'email' in data_tosender[n] and 'url_sign' in data_tosender[n] and 'tracking' in data_tosender[n] and 'name_file' in data_tosender[n] and 'message' in data_tosender[n] and 'step_num' in data_tosender[n] and 'sendChat' in data_tosender[n] and 'property' in data_tosender[n] and len(data_tosender[n]) == 8:
                                sender_email = data_tosender[n]['email']
                                sender_url_sign_email = data_tosender[n]['url_sign']
                                sender_tracking = data_tosender[n]['tracking']
                                sender_name_file = data_tosender[n]['name_file']
                                sender_message = data_tosender[n]['message']
                                sender_step_num = data_tosender[n]['step_num']
                                sender_sendChat = data_tosender[n]['sendChat']
                                sender_property = data_tosender[n]['property']
                                if sender_step_num == '1' and sender_sendChat == True:
                                    res_search_frd = search_frd(sender_email,token_header)
                                    if 'status' in res_search_frd:
                                        if res_search_frd['status'] == 'success':
                                            user_id_info = res_search_frd['friend']['user_id']
                                            one_id_info = res_search_frd['friend']['one_id']
                                            resouce_result = select().select_forChat_v2(sidcode)
                                            print(resouce_result)


                                            if resouce_result['result'] == 'OK':
                                                if resouce_result['messageText']['documentType_Details'][0] != None:
                                                    if 'chat_bot_details' in resouce_result['messageText']['documentType_Details'][0]:
                                                        msg_chat_bot = resouce_result['messageText']['documentType_Details'][0]['chat_bot_details']
                                                        if msg_chat_bot != None:
                                                            status_chat_bot = msg_chat_bot['chat_bot_status']
                                                            id_chat_bot = msg_chat_bot['chat_bot_id']
                                                            token_chat_bot = msg_chat_bot['chat_bot_token']
                                                            print(token_chat_bot)
                                                        else:
                                                            id_chat_bot = bot_id
                                                            token_chat_bot = token_service
                                                    else:
                                                        id_chat_bot = bot_id
                                                        token_chat_bot = token_service

                                                res_send = sender_one_chat_templatechat_v1(str(sender_property).lower(),user_id_info,sender_name_file,sender_tracking,sender_url_sign_email,sidcode,resouce_result['messageText'],result_pathUrl,id_chat_bot,token_chat_bot)
                                                print(res_send)
                                                if 'status' in res_send:
                                                    if res_send['status'] == 'success':
                                                        message_from_onechat = res_send['message']
                                                        id_chat = message_from_onechat['id']
                                                        result_update = update().update_StatusOneChat_v2(sidcode,sender_email,sender_step_num)
                                                        resultgetProject = sendtask_getProject_tochat_newversion_v3(one_id_info,id_chat_bot,token_chat_bot,token_header)
                                                        print(resultgetProject)


                                                        if resultgetProject['result'] == 'OK':
                                                            priority_ = '1'
                                                            titleAndDetails = resouce_result['messageText']
                                                            try:
                                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                resultSend_CreateTask = sendtask_creattask_tochat_v3(projectid_,priority_,titleAndDetails,state_id_,str(sender_property).lower(),sidcode,one_id_info,id_chat_bot,token_chat_bot,token_header)

                                                                if resultSend_CreateTask['result'] == 'OK':
                                                                    if 'status' in resultSend_CreateTask['messageText']:
                                                                        if resultSend_CreateTask['messageText']['status'] =='success':
                                                                            list_taskChat_log.append({'result':'OK','sidCode':sidcode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                                                        else:
                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                                                    else:
                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                                                else:
                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                                            except Exception as e:
                                                                print(e)
                                                                list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})

                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})


                                                        list_Chat_log.append({'result':'OK','email':sender_email,'sid':sidcode,'step_num':sender_step_num,'sendChat':sender_sendChat,'urlSign':sender_url_sign_email,'property':sender_property,'id_chat':id_chat,'message_chat':message_from_onechat})
                                                    else:
                                                        list_Chat_log.append({'result':'NO','email':sender_email,'sid':sidcode,'step_num':sender_step_num,'sendChat':sender_sendChat,'urlSign':sender_url_sign_email,'property':sender_property,'id_chat':None,'message_chat':''})
                                                else:
                                                    list_Chat_log.append({'result':'ER','email':sender_email,'sid':sidcode,'step_num':sender_step_num,'sendChat':sender_sendChat,'urlSign':sender_url_sign_email,'property':sender_property,'id_chat':None,'message_chat':''})
                                            else:
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error data not found'}),200
                                        else:
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error search frd one chat'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error search frd one chat'}),200
                                else:
                                    list_taskChat_log.append({'result':'NO','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                    list_Chat_log.append({'result':'NO','email':sender_email,'sid':sidcode,'step_num':sender_step_num,'sendChat':sender_sendChat,'urlSign':sender_url_sign_email,'property':sender_property,'id_chat':None,'message_chat':''})
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect in data'}),404
                        if len(list_Chat_log) != 0:
                            result_logChat = selection_email_insert_v2(list_Chat_log)
                            if result_logChat['result'] == 'OK':
                                print(list_taskChat_log)
                                result_insert = insert().insert_transactionTask(list_taskChat_log)
                                print(result_insert)
                                if result_insert['result'] == 'OK':
                                    return jsonify({'result':'OK','messageText':'send to onechat successfully','status_Code':200,'messageER':None}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'cant insert data'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list no information'}),200
                        return jsonify({'result':'OK','messageText':list_Chat_log,'status_Code':200,'messageER':None}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect in data'}),404

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(str(e))
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
    elif str(type_chat).lower() == 'next':
        if request.method == 'POST':
            try:
                try:
                    token_header = request.headers['Authorization']
                    try:
                        token_header = str(token_header).split(' ')[1]
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
                except KeyError as ex:
                    return redirect(url_paperless)
                dataJson = request.json
                if 'sid_code' in dataJson and len(dataJson) == 1:
                    sidCode = dataJson['sid_code']
                    resultURLIMAGE = createImage_formPDF(sidCode)
                    result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                    resselect_transactionChat = select().select_transactionChat(sidCode)
                    resselect_check = check_sendToChat(resselect_transactionChat)
                    result_Array = []

                    for i in range(len(resselect_transactionChat)):
                        if resselect_transactionChat[i]['statusSign'] == 'Y':
                            resselect_transactionChat[i]['statusSign'] = 'Complete'
                        elif resselect_transactionChat[i]['statusSign'] == 'R':
                            resselect_transactionChat[i]['statusSign'] = 'Reject'
                        else:
                            resselect_transactionChat[i]['statusSign'] = 'Incomplete'

                        result_Array.append({
                            'emailUser':resselect_transactionChat[i]['email_User'],
                            'statusSign':resselect_transactionChat[i]['statusSign'],
                            'stepNum':int(resselect_transactionChat[i]['stepNum']),
                            'datetime_string':resselect_transactionChat[i]['datetime_string'],
                            'status_propertyChat':resselect_transactionChat[i]['propertyChat'],
                            'url_Sign':resselect_transactionChat[i]['url_Sign']
                        })
                    print(result_Array)
                    if resselect_check['result'] == 'OK':
                        print(resselect_check)
                        if 'statusSign' in resselect_check['msg']:
                            print(resselect_check['msg'])
                            disble_button_in_oneChat_v2(resselect_check['msg']['id_chat'],2,token_header)
                            if resselect_check['msg']['statusSign'] == 'R':
                                stepNum = resselect_check['msg']['stepNum']
                                print(resselect_check)
                                result_SelectBefore = select().select_transactionChat_before(stepNum,sidCode)
                                res_select = select().select_ForWebHook(sidCode)
                                resouce_result = select().select_forChat_v2(sidCode)
                                if resouce_result['result'] == 'OK':
                                    if 'chat_bot_details' in resouce_result['messageText']['documentType_Details'][0]:
                                        msg_chat_bot = resouce_result['messageText']['documentType_Details'][0]['chat_bot_details']
                                        if msg_chat_bot != None:
                                            status_chat_bot = msg_chat_bot['chat_bot_status']
                                            id_chat_bot = msg_chat_bot['chat_bot_id']
                                            token_chat_bot = msg_chat_bot['chat_bot_token']
                                            print(token_chat_bot)
                                        else:
                                            id_chat_bot = bot_id
                                            token_chat_bot = token_service
                                    else:
                                        id_chat_bot = bot_id
                                        token_chat_bot = token_service
                                title_toChat = 'แจ้งเตือนระบบ Paperless'
                                msg_toChat = ''
                                count_res = 0
                                msg_toChat_Paper = ''
                                try:
                                    title_toChat  += '\n- เอกสารถูกปฏิเสธอนุมัติ -\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['userSender'] + '\n'
                                    documentId = res_select['messageText']['documentId']
                                except Exception as ex:
                                    documentId = None
                                    pass
                                arr_step = []
                                print(documentId)
                                for count in range(len(result_Array)):
                                    count_res = count + 1
                                    try:
                                        email_User = result_Array[count]['emailUser']
                                        statusSign = result_Array[count]['statusSign']
                                        datetime_string = result_Array[count]['datetime_string']
                                        if result_Array[count]['stepNum'] not in arr_step:
                                            arr_step.append(result_Array[count]['stepNum'])
                                    except Exception as ex:
                                        email_User = ''
                                        statusSign = ''
                                for n in arr_step:
                                    msg_toChat += '\nลำดับที่ ' + str(n)
                                    for count in range(len(result_Array)):
                                        try:
                                            email_User = result_Array[count]['emailUser']
                                            statusSign = result_Array[count]['statusSign']
                                            status_propertyChat = result_Array[count]['status_propertyChat']
                                            if status_propertyChat == 'signning':
                                                if statusSign == 'Complete':
                                                    statusSign = 'อนุมัติแล้ว'
                                                elif statusSign == 'Pending':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                elif statusSign == 'Incomplete':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                else:
                                                    statusSign = 'ไม่อนุมัติ'
                                            elif status_propertyChat == 'approve':
                                                if statusSign == 'Complete':
                                                    statusSign = 'อนุมัติแล้ว'
                                                elif statusSign == 'Pending':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                elif statusSign == 'Incomplete':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                else:
                                                    statusSign = 'ไม่อนุมัติ'
                                            datetime_string = result_Array[count]['datetime_string']
                                        except Exception as ex:
                                            email_User = ''
                                            statusSign = ''
                                        if result_Array[count]['stepNum'] == n:
                                            msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''

                                messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                                print(messageToChat)
                                for i in range(len(result_SelectBefore['messageText'])):
                                    email_before = result_SelectBefore['messageText'][i]['email_User']
                                    print(email_before)
                                # # #     email_ =
                                    res_search_frd = search_frd(email_before,token_header)
                                    user_id_chat = res_search_frd['friend']['user_id']
                                    result_sendChat = send_messageToChat_v3(messageToChat,user_id_chat,token_chat_bot,id_chat_bot,token_header)
                                    print(result_sendChat)
                                return jsonify({'result':'OK','messageText':'send to chat and reject document','status_Code':200,'messageER':None}),200
                        try:
                            result_select_Chat_next = select().select_transactionChat_next(resselect_check)
                        except Exception as ex:
                            print(str(ex))
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found ' + str(ex)}),200
                        print(result_select_Chat_next)
                        print(resselect_check)
                        list_taskChat_log = []
                        list_sendChat_log = []
                        for k in result_select_Chat_next:
                            status_Sign = k['statusSign']
                            email_user = k['email_User']
                            transactionCode = k['transactionCode']
                            tracking_id = k['tracking_id']
                            file_name = k['file_name']
                            step_num = k['stepNum']
                            print(k)
                            if status_Sign != 'R':
                                res_search_frd = search_frd(email_user,token_header)
                                resouce_result = select().select_forChat_v2(sidCode)
                                print(resouce_result)
                                print(res_search_frd)
                                if 'status' in res_search_frd:
                                    if res_search_frd['status'] == 'success':
                                        user_id_info = res_search_frd['friend']['user_id']
                                        one_id_info = res_search_frd['friend']['one_id']
                                        data_url,data_property = select().select_UrlSign_SidCodeEmailUser(sidCode,email_user)
                                        if resouce_result['result'] == 'OK':
                                            if 'chat_bot_details' in resouce_result['messageText']['documentType_Details'][0]:
                                                msg_chat_bot = resouce_result['messageText']['documentType_Details'][0]['chat_bot_details']
                                                if msg_chat_bot != None:
                                                    status_chat_bot = msg_chat_bot['chat_bot_status']
                                                    id_chat_bot = msg_chat_bot['chat_bot_id']
                                                    token_chat_bot = msg_chat_bot['chat_bot_token']
                                                    print(token_chat_bot)
                                                else:
                                                    id_chat_bot = bot_id
                                                    token_chat_bot = token_service
                                            else:
                                                id_chat_bot = bot_id
                                                token_chat_bot = token_service
                                            result_sendChat = sender_one_chat_templatechat_v1(data_property,user_id_info,file_name,tracking_id,data_url,sidCode,resouce_result['messageText'],result_pathUrl,id_chat_bot,token_chat_bot)
                                            if 'status' in result_sendChat:
                                                if result_sendChat['status'] == 'success':
                                                    message_from_chat = result_sendChat['message']
                                                    id_chat = result_sendChat['message']['id']
                                                    result_update = update().update_StatusOneChat_v2(sidCode,email_user,step_num)
                                                    print(result_update)
                                                    print(result_sendChat)
                                                    resultgetProject = sendtask_getProject_tochat_newversion_v3(one_id_info,id_chat_bot,token_chat_bot,token_header)
                                                    if resultgetProject['result'] == 'OK':
                                                        print(resultgetProject)
                                                        if len(resultgetProject['messageText']['data']) != 0:
                                                            projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                            priority_ = '1'
                                                            titleAndDetails = resouce_result['messageText']
                                                            for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                    state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                            resultSend_CreateTask = sendtask_creattask_tochat_v3(projectid_,priority_,titleAndDetails,state_id_,str(data_property).lower(),sidCode,one_id_info,id_chat_bot,token_chat_bot,token_header)
                                                            print(resultSend_CreateTask)
                                                            if resultSend_CreateTask['result'] == 'OK':
                                                                if 'status' in resultSend_CreateTask['messageText']:
                                                                    if resultSend_CreateTask['messageText']['status'] =='success':
                                                                        list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'step_num':step_num,'email':email_user})
                                                                    else:
                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'step_num':step_num,'email':email_user})
                                                                else:
                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'step_num':step_num,'email':email_user})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'step_num':step_num,'email':email_user})
                                                    else:
                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'step_num':step_num,'email':email_user})
                                                    list_sendChat_log.append({'result':'OK','email':email_user,'sid':sidCode,'transactionCode':transactionCode,'stepNum':step_num,'id_chat':id_chat})
                                                else:
                                                    list_sendChat_log.append({'result':'ER','email':email_user,'sid':sidCode,'transactionCode':transactionCode,'stepNum':step_num,'id_chat':None})
                                            else:
                                                list_sendChat_log.append({'result':'ER','email':email_user,'sid':sidCode,'transactionCode':transactionCode,'stepNum':step_num,'id_chat':None})
                                        else:
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error in select UrlSign SidCodeEmailUser'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error search friend one chat'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error search friend one chat'}),200
                        if len(list_sendChat_log) != 0:
                            print(list_sendChat_log)
                            resultUpdateTask = update().update_taskchat_nextstep(list_taskChat_log)
                            result_update = update().update_ChatToSend_v2(list_sendChat_log)
                            result_select = select().select_ForWebHook(sidCode)
                            resouce_result = select().select_forChat_v2(sidCode)
                            if resouce_result['result'] == 'OK':
                                if 'chat_bot_details' in resouce_result['messageText']['documentType_Details'][0]:
                                    msg_chat_bot = resouce_result['messageText']['documentType_Details'][0]['chat_bot_details']
                                    if msg_chat_bot != None:
                                        status_chat_bot = msg_chat_bot['chat_bot_status']
                                        id_chat_bot = msg_chat_bot['chat_bot_id']
                                        token_chat_bot = msg_chat_bot['chat_bot_token']
                                        print(token_chat_bot)
                                    else:
                                        id_chat_bot = bot_id
                                        token_chat_bot = token_service
                                else:
                                    id_chat_bot = bot_id
                                    token_chat_bot = token_service
                            title_toChat = 'แจ้งเตือนระบบ Paperless'
                            msg_toChat = ''
                            count_res = 0
                            msg_toChat_Paper = ''
                            try:
                                title_toChat  += '\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['sender_email'] + '\n'
                                documentId = res_select['messageText']['documentId']
                            except Exception as ex:
                                documentId = None
                                pass
                            arr_step = []
                            for count in range(len(result_Array)):
                                count_res = count + 1
                                try:
                                    email_User = result_Array[count]['emailUser']
                                    statusSign = result_Array[count]['statusSign']
                                    datetime_string = result_Array[count]['datetime_string']
                                    if result_Array[count]['stepNum'] not in arr_step:
                                        arr_step.append(result_Array[count]['stepNum'])
                                except Exception as ex:
                                    email_User = ''
                                    statusSign = ''
                            for n in arr_step:
                                msg_toChat += '\nลำดับที่ ' + str(n)
                                for count in range(len(result_Array)):
                                    try:
                                        email_User = result_Array[count]['emailUser']
                                        statusSign = result_Array[count]['statusSign']
                                        status_propertyChat = result_Array[count]['status_propertyChat']
                                        if status_propertyChat == 'signning':
                                            if statusSign == 'Complete':
                                                statusSign = 'อนุมัติแล้ว'
                                            elif statusSign == 'Pending':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            elif statusSign == 'Incomplete':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            else:
                                                statusSign = 'ไม่อนุมัติ'
                                        elif status_propertyChat == 'approve':
                                            if statusSign == 'Complete':
                                                statusSign = 'อนุมัติแล้ว'
                                            elif statusSign == 'Pending':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            elif statusSign == 'Incomplete':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            else:
                                                statusSign = 'ไม่อนุมัติ'
                                        datetime_string = result_Array[count]['datetime_string']
                                    except Exception as ex:
                                        email_User = ''
                                        statusSign = ''
                                    if result_Array[count]['stepNum'] == n:
                                        msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                            messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                            result_Email = select().select_GETEmail(sidCode)
                            if result_Email['result'] == 'OK':
                                res_search_frd = search_frd(result_Email['messageText']['email_Sender'],token_header)
                                if 'status' in res_search_frd:
                                    if res_search_frd['status'] == 'success':
                                        result_sendChat = send_messageToChat_v3(messageToChat,res_search_frd['friend']['user_id'],token_chat_bot,id_chat_bot,token_header)
                                        if result_sendChat['status'] == 'success':
                                            return jsonify({'result':'OK','messageText':'send chat success','status_Code':200,'messageER':None,'messageType':'chat'}),200
                                        else:
                                            return jsonify({'result':'ER','messageText':'send chat fail','status_Code':200,'messageER':None,'messageType':'chat'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found friend','messageType':'chat'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'service search friend error','messageType':'chat'}),200
                            else:
                                return jsonify({'result':'OK','messageText':'send chat success','status_Code':200,'messageER':None,'messageType':'chat'}),200
                        else:
                            resouce_result = select().select_forChat_v2(sidCode)
                            if resouce_result['result'] == 'OK':
                                if 'chat_bot_details' in resouce_result['messageText']['documentType_Details'][0]:
                                    msg_chat_bot = resouce_result['messageText']['documentType_Details'][0]['chat_bot_details']
                                    if msg_chat_bot != None:
                                        status_chat_bot = msg_chat_bot['chat_bot_status']
                                        id_chat_bot = msg_chat_bot['chat_bot_id']
                                        token_chat_bot = msg_chat_bot['chat_bot_token']
                                        # print(token_chat_bot)
                                    else:
                                        id_chat_bot = bot_id
                                        token_chat_bot = token_service
                                else:
                                    id_chat_bot = bot_id
                                    token_chat_bot = token_service
                            res_select = select().select_ForWebHook(sidCode)
                            title_toChat = 'แจ้งเตือนระบบ Paperless'
                            msg_toChat = ''
                            count_res = 0
                            msg_toChat_Paper = ''
                            # print(res_select['messageText'])
                            try:
                                title_toChat  += '\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['sender_email'] + '\n'
                                documentId = res_select['messageText']['documentId']
                            except Exception as ex:
                                documentId = None
                                pass
                            arr_step = []
                            for count in range(len(result_Array)):
                                count_res = count + 1
                                try:
                                    email_User = result_Array[count]['emailUser']
                                    statusSign = result_Array[count]['statusSign']
                                    datetime_string = result_Array[count]['datetime_string']
                                    if result_Array[count]['stepNum'] not in arr_step:
                                        arr_step.append(result_Array[count]['stepNum'])
                                except Exception as ex:
                                    email_User = ''
                                    statusSign = ''

                            for n in arr_step:
                                msg_toChat += '\nลำดับที่ ' + str(n)
                                for count in range(len(result_Array)):
                                    try:
                                        email_User = result_Array[count]['emailUser']
                                        statusSign = result_Array[count]['statusSign']
                                        status_propertyChat = result_Array[count]['status_propertyChat']
                                        if status_propertyChat == 'signning':
                                            if statusSign == 'Complete':
                                                statusSign = 'อนุมัติแล้ว'
                                            elif statusSign == 'Pending':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            elif statusSign == 'Incomplete':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            else:
                                                statusSign = 'ไม่อนุมัติ'
                                        elif status_propertyChat == 'approve':
                                            if statusSign == 'Complete':
                                                statusSign = 'อนุมัติแล้ว'
                                            elif statusSign == 'Pending':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            elif statusSign == 'Incomplete':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            else:
                                                statusSign = 'ไม่อนุมัติ'
                                        datetime_string = result_Array[count]['datetime_string']
                                    except Exception as ex:
                                        email_User = ''
                                        statusSign = ''
                                    if result_Array[count]['stepNum'] == n:
                                        msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                            messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                            result_Email = select().select_GETEmail(sidCode)
                            email_sender_user = result_Email['messageText']['email_Sender']
                            print(email_sender_user)
                            result_search_frd = search_frd(email_sender_user,token_header)
                            print(result_search_frd)
                            if 'status' in result_search_frd:
                                if result_search_frd['status'] == 'success':
                                    user_id_info = result_search_frd['friend']['user_id']
                                    result_send_chat = send_messageToChat_v3(messageToChat,user_id_info,token_chat_bot,id_chat_bot,token_header)
                                    if 'status' in result_send_chat:
                                        if result_send_chat['status'] == 'success':
                                            return jsonify({'result':'OK','messageText':'send chat success','status_Code':200,'messageER':None,'messageType':'chat'})
                                        else:
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'send chat fail','messageType':'chat'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'send chat fail','messageType':'chat'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found friend','messageType':'chat'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'service search friend error','messageType':'chat'}),200

                    return jsonify({'result':'OK','messageText':list_sendChat_log,'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(exc_obj, exc_tb.tb_lineno)
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                text_webhook = str('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))+ ' ' + str(type(e).__name__) +' '+ str(e) + ' in ' +fname
                status_code = 500
                success = False
                response = {
                    'result': 'ER',
                    'messageText': None,
                    'messageER': str(e),
                    'status_Code':status_code
                }
                # print(text_webhook)
                callWebHook_slack_v1(text_webhook,'','')
                insert().inert_logger_error_v1(text_webhook,'chat v8')
                return jsonify(response), status_code

    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'service type incorrect'}),404

@status_methods.route('/api/v9/<string:type_chat>/chat_sender', methods=['POST','GET'])
@token_required
def chat_api_v9(type_chat):
    if str(type_chat).lower() == 'first':
        if request.method == 'POST':
            dataJson = request.json
            if 'data' in dataJson and 'sid_code' in dataJson and len(dataJson) == 2:
                try:
                    try:
                        token_header = request.headers['Authorization']
                        try:
                            token_header = str(token_header).split(' ')[1]
                        except Exception as ex:
                            return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
                    except KeyError as ex:
                        return redirect(url_paperless)
                    sidcode = dataJson['sid_code']
                    data_json = dataJson['data']
                    resultURLIMAGE = createImage_formPDF2(sidcode)
                    if resultURLIMAGE['result'] == 'OK':
                        result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE['data']
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error createImage PDF'}),200
                    if len(data_json) != 0:
                        list_taskChat_log = []
                        list_Chat_log = []
                        for n in range(len(data_json)):
                            data_tosender = data_json
                            if 'email' in data_tosender[n] and 'url_sign' in data_tosender[n] and 'tracking' in data_tosender[n] and 'name_file' in data_tosender[n] and 'message' in data_tosender[n] and 'step_num' in data_tosender[n] and 'sendChat' in data_tosender[n] and 'property' in data_tosender[n] and len(data_tosender[n]) == 8:
                                sender_email = data_tosender[n]['email']
                                sender_url_sign_email = data_tosender[n]['url_sign']
                                sender_tracking = data_tosender[n]['tracking']
                                sender_name_file = data_tosender[n]['name_file']
                                sender_message = data_tosender[n]['message']
                                sender_step_num = data_tosender[n]['step_num']
                                sender_sendChat = data_tosender[n]['sendChat']
                                sender_property = data_tosender[n]['property']
                                if sender_step_num == '1' and sender_sendChat == True:
                                    res_search_frd = search_frd(sender_email,token_header)
                                    if 'status' in res_search_frd:
                                        if res_search_frd['status'] == 'success':
                                            user_id_info = res_search_frd['friend']['user_id']
                                            one_id_info = res_search_frd['friend']['one_id']
                                            resouce_result = select().select_forChat_v2(sidcode)
                                            print(resouce_result)
                                            if resouce_result['result'] == 'OK':
                                                if resouce_result['messageText']['documentType_Details'][0] != None:
                                                    if 'chat_bot_details' in resouce_result['messageText']['documentType_Details'][0]:
                                                        msg_chat_bot = resouce_result['messageText']['documentType_Details'][0]['chat_bot_details']
                                                        if msg_chat_bot != None:
                                                            status_chat_bot = msg_chat_bot['chat_bot_status']
                                                            id_chat_bot = msg_chat_bot['chat_bot_id']
                                                            token_chat_bot = msg_chat_bot['chat_bot_token']
                                                            print(token_chat_bot)
                                                        else:
                                                            id_chat_bot = bot_id
                                                            token_chat_bot = token_service
                                                    else:
                                                        id_chat_bot = bot_id
                                                        token_chat_bot = token_service
                                                resultgetProject = sendtask_getProject_tochat_newversion_v3(one_id_info,id_chat_bot,token_chat_bot,token_header)
                                                print(resultgetProject)

                                                if resultgetProject['result'] == 'OK':
                                                    result_update = update().update_StatusOneChat_v2(sidcode,sender_email,sender_step_num)
                                                    priority_ = '1'
                                                    titleAndDetails = resouce_result['messageText']
                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                        if str(resultgetProject['messageText']['data'][0]['state'][y]['name']).lower() == 'doing':
                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                    # return ''
                                                    result_sumservice = send_chat_paperless_send_approve_v1(str(sender_property).lower(),one_id_info,sender_name_file,sender_tracking,sender_url_sign_email,sidcode,projectid_,priority_,titleAndDetails,state_id_,resouce_result['messageText'],result_pathUrl,id_chat_bot,token_chat_bot,token_header)
                                                    if result_sumservice['result'] == 'OK':
                                                        tmp_messageText = result_sumservice['messageText']
                                                        tmp_res_off_template = tmp_messageText['res_official_template']
                                                        tmp_res_task = tmp_messageText['res_task']
                                                        if 'status' in tmp_res_off_template:
                                                            message_from_onechat = tmp_res_off_template['message']
                                                            id_chat = tmp_res_off_template['message']['id']
                                                            if tmp_res_off_template['status'] == 'success':
                                                                list_Chat_log.append({'result':'OK','email':sender_email,'sid':sidcode,'step_num':sender_step_num,'sendChat':sender_sendChat,'urlSign':sender_url_sign_email,'property':sender_property,'id_chat':id_chat,'message_chat':message_from_onechat})
                                                            else:
                                                                list_Chat_log.append({'result':'ER','email':sender_email,'sid':sidcode,'step_num':sender_step_num,'sendChat':sender_sendChat,'urlSign':sender_url_sign_email,'property':sender_property,'id_chat':None,'message_chat':''})
                                                        else:
                                                            list_Chat_log.append({'result':'ER','email':sender_email,'sid':sidcode,'step_num':sender_step_num,'sendChat':sender_sendChat,'urlSign':sender_url_sign_email,'property':sender_property,'id_chat':None,'message_chat':''})
                                                        if 'status' in tmp_res_task:
                                                            if tmp_res_task['status'] == 'success':
                                                                list_taskChat_log.append({'result':'OK','sidCode':sidcode,'messageText':{'create_task':tmp_res_task,'get_project':resultgetProject['messageText']},'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                                            else:
                                                                list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                                    else:
                                                        list_Chat_log.append({'result':'ER','email':sender_email,'sid':sidcode,'step_num':sender_step_num,'sendChat':sender_sendChat,'urlSign':sender_url_sign_email,'property':sender_property,'id_chat':None,'message_chat':''})
                                                        list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                                else:
                                                    list_Chat_log.append({'result':'ER','email':sender_email,'sid':sidcode,'step_num':sender_step_num,'sendChat':sender_sendChat,'urlSign':sender_url_sign_email,'property':sender_property,'id_chat':None,'message_chat':''})
                                                    list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                            else:
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error data not found'}),200
                                        else:
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error search frd one chat'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error search frd one chat'}),200
                                else:
                                    list_taskChat_log.append({'result':'NO','sidCode':sidcode,'messageText':None,'sendChat': sender_sendChat,'step_num':sender_step_num,'email':sender_email})
                                    list_Chat_log.append({'result':'NO','email':sender_email,'sid':sidcode,'step_num':sender_step_num,'sendChat':sender_sendChat,'urlSign':sender_url_sign_email,'property':sender_property,'id_chat':None,'message_chat':''})
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect in data'}),404
                        if len(list_Chat_log) != 0:
                            result_logChat = selection_email_insert_v2(list_Chat_log)
                            if result_logChat['result'] == 'OK':
                                result_insert = insert().insert_transactionTask(list_taskChat_log)
                                if result_insert['result'] == 'OK':
                                    return jsonify({'result':'OK','messageText':'send to onechat successfully','status_Code':200,'messageER':None}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'cant insert data'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list no information'}),200
                        return jsonify({'result':'OK','messageText':list_Chat_log,'status_Code':200,'messageER':None}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect in data'}),404

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(str(e))
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
    elif str(type_chat).lower() == 'next':
        if request.method == 'POST':
            try:
                dataJson = request.json
                try:
                    token_header = request.headers['Authorization']
                    try:
                        token_header = str(token_header).split(' ')[1]
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
                except KeyError as ex:
                    return redirect(url_paperless)
                if 'sid_code' in dataJson and len(dataJson) == 1:
                    sidcode = dataJson['sid_code']
                    resultURLIMAGE = createImage_formPDF(sidcode)
                    result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                    resselect_transactionChat = select().select_transactionChat(sidcode)
                    print(resselect_transactionChat)
                    resselect_check = check_sendToChat_v2(resselect_transactionChat)
                    if resselect_check['result'] == 'ER':
                        return jsonify({'result':'OK','messageText':'cant send onechat non data','status_Code':200,'messageER':None,'messageType':'chat','service_Code':'CH01'}),200
                    resouce_result = select().select_forChat_v2(sidcode)
                    # print(resselect_check)
                    result_Array = []
                    for i in range(len(resselect_transactionChat)):
                        if resselect_transactionChat[i]['statusSign'] == 'Y':
                            resselect_transactionChat[i]['statusSign'] = 'Complete'
                        elif resselect_transactionChat[i]['statusSign'] == 'R':
                            resselect_transactionChat[i]['statusSign'] = 'Reject'
                        else:
                            resselect_transactionChat[i]['statusSign'] = 'Incomplete'

                        result_Array.append({
                            'emailUser':resselect_transactionChat[i]['email_User'],
                            'statusSign':resselect_transactionChat[i]['statusSign'],
                            'stepNum':int(resselect_transactionChat[i]['stepNum']),
                            'datetime_string':resselect_transactionChat[i]['datetime_string'],
                            'status_propertyChat':resselect_transactionChat[i]['propertyChat'],
                            'url_Sign':resselect_transactionChat[i]['url_Sign']
                        })
                    if resselect_check['result'] == 'OK':
                        if 'chat_bot_details' in resouce_result['messageText']['documentType_Details'][0]:
                            msg_chat_bot = resouce_result['messageText']['documentType_Details'][0]['chat_bot_details']
                            if msg_chat_bot != None:
                                status_chat_bot = msg_chat_bot['chat_bot_status']
                                id_chat_bot = msg_chat_bot['chat_bot_id']
                                token_chat_bot = msg_chat_bot['chat_bot_token']
                                print(token_chat_bot)
                            else:
                                id_chat_bot = bot_id
                                token_chat_bot = token_service
                        else:
                            id_chat_bot = bot_id
                            token_chat_bot = token_service
                        tmp_list_id_chat = resselect_check['list_id_chat']
                        tmp_data = resselect_check['tmp_data']
                        # email_user = tmp_list_id_chat['email_User']
                        # step_num = tmp_list_id_chat['stepNum']
                        print(tmp_list_id_chat)
                        for u in range(len(tmp_list_id_chat)):
                            disble_button_in_oneChat_v2(tmp_list_id_chat[u],2,token_header)
                        for z in range(len(tmp_data)):
                            # print(tmp_data[z])
                            tmp_email_User = tmp_data[z]['email_User']
                            tmp_stepNum = tmp_data[z]['stepNum']
                            tmp_messageTask = tmp_data[z]['messageTask_Chat']
                            tmp_messageTask_Id = str(tmp_data[z]['messageTask_Id'])
                            if tmp_messageTask != None:
                                tmp_messageTask = eval(str(tmp_messageTask))
                            else:
                                tmp_messageTask = None
                            if tmp_messageTask != None:
                                tmp_create_task = tmp_messageTask['create_task']['data']
                                tmp_id_task = tmp_create_task['task_id']
                                print(tmp_id_task)
                                tmp_get_project = tmp_messageTask['get_project']['data'][0]
                                tmp_state = tmp_get_project['state']
                                for y in range(len(tmp_state)):
                                    tmp_name = tmp_state[y]['name']
                                    if str(tmp_name).lower() == 'done':
                                        tmp_state_id = tmp_state[y]['state_id']
                                        print(tmp_state[y])
                                        resultChangeState = sendtask_change_stateChat_v2(tmp_state_id,tmp_id_task,token_chat_bot,id_chat_bot,token_header)
                                        if resultChangeState['result'] == 'OK':
                                            update().update_taskchat_state(sidcode,tmp_email_User,tmp_stepNum,tmp_name,tmp_state_id)
                    if resselect_check['result'] == 'OK':
                        if 'statusSign' in resselect_check['msg']:
                            if resselect_check['msg']['statusSign'] == 'R':
                                stepNum = resselect_check['msg']['stepNum']
                                print(resselect_check)
                                result_SelectBefore = select().select_transactionChat_before(stepNum,sidcode)
                                res_select = select().select_ForWebHook(sidcode)
                                resouce_result = select().select_forChat_v2(sidcode)
                                if resouce_result['result'] == 'OK':
                                    if 'chat_bot_details' in resouce_result['messageText']['documentType_Details'][0]:
                                        msg_chat_bot = resouce_result['messageText']['documentType_Details'][0]['chat_bot_details']
                                        if msg_chat_bot != None:
                                            status_chat_bot = msg_chat_bot['chat_bot_status']
                                            id_chat_bot = msg_chat_bot['chat_bot_id']
                                            token_chat_bot = msg_chat_bot['chat_bot_token']
                                            print(token_chat_bot)
                                        else:
                                            id_chat_bot = bot_id
                                            token_chat_bot = token_service
                                    else:
                                        id_chat_bot = bot_id
                                        token_chat_bot = token_service
                                title_toChat = 'แจ้งเตือนระบบ Paperless'
                                msg_toChat = ''
                                count_res = 0
                                msg_toChat_Paper = ''
                                try:
                                    title_toChat  += '\n- เอกสารถูกปฏิเสธอนุมัติ -\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['userSender'] + '\n'
                                    documentId = res_select['messageText']['documentId']
                                except Exception as ex:
                                    documentId = None
                                    pass
                                arr_step = []
                                print(documentId)
                                for count in range(len(result_Array)):
                                    count_res = count + 1
                                    try:
                                        email_User = result_Array[count]['emailUser']
                                        statusSign = result_Array[count]['statusSign']
                                        datetime_string = result_Array[count]['datetime_string']
                                        if result_Array[count]['stepNum'] not in arr_step:
                                            arr_step.append(result_Array[count]['stepNum'])
                                    except Exception as ex:
                                        email_User = ''
                                        statusSign = ''
                                for n in arr_step:
                                    msg_toChat += '\nลำดับที่ ' + str(n)
                                    for count in range(len(result_Array)):
                                        try:
                                            email_User = result_Array[count]['emailUser']
                                            statusSign = result_Array[count]['statusSign']
                                            status_propertyChat = result_Array[count]['status_propertyChat']
                                            if status_propertyChat == 'signning':
                                                if statusSign == 'Complete':
                                                    statusSign = 'อนุมัติแล้ว'
                                                elif statusSign == 'Pending':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                elif statusSign == 'Incomplete':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                else:
                                                    statusSign = 'ไม่อนุมัติ'
                                            elif status_propertyChat == 'approve':
                                                if statusSign == 'Complete':
                                                    statusSign = 'อนุมัติแล้ว'
                                                elif statusSign == 'Pending':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                elif statusSign == 'Incomplete':
                                                    statusSign = 'ยังไม่อนุมัติ'
                                                else:
                                                    statusSign = 'ไม่อนุมัติ'
                                            datetime_string = result_Array[count]['datetime_string']
                                        except Exception as ex:
                                            email_User = ''
                                            statusSign = ''
                                        if result_Array[count]['stepNum'] == n:
                                            msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                                messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                                print(messageToChat)
                                for i in range(len(result_SelectBefore['messageText'])):
                                    email_before = result_SelectBefore['messageText'][i]['email_User']
                                    res_search_frd = search_frd(email_before,token_header)
                                    user_id_chat = res_search_frd['friend']['user_id']
                                    result_sendChat = send_messageToChat_v3(messageToChat,user_id_chat,token_chat_bot,id_chat_bot,token_header)
                                    print(result_sendChat)
                                return jsonify({'result':'OK','messageText':'send to chat and reject document','status_Code':200,'messageER':None}),200
                        try:
                            result_select_Chat_next = select().select_transactionChat_next_v2(resselect_check)
                        except Exception as ex:
                            print(str(ex))
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found ' + str(ex)}),200
                        list_taskChat_log = []
                        list_Chat_log = []
                        print(result_select_Chat_next)
                        for k in result_select_Chat_next:
                            status_Sign = k['statusSign']
                            email_user = k['email_User']
                            transactionCode = k['transactionCode']
                            tracking_id = k['tracking_id']
                            file_name = k['file_name']
                            step_num = k['stepNum']
                            print(k)
                            if status_Sign != 'R':
                                res_search_frd = search_frd(email_user,token_header)
                                resouce_result = select().select_forChat_v2(sidcode)
                                print(resouce_result)
                                print(res_search_frd)
                                if 'status' in res_search_frd:
                                    if res_search_frd['status'] == 'success':
                                        user_id_info = res_search_frd['friend']['user_id']
                                        one_id_info = res_search_frd['friend']['one_id']
                                        data_url,data_property = select().select_UrlSign_SidCodeEmailUser(sidcode,email_user,step_num)
                                        if resouce_result['result'] == 'OK':
                                            if 'chat_bot_details' in resouce_result['messageText']['documentType_Details'][0]:
                                                msg_chat_bot = resouce_result['messageText']['documentType_Details'][0]['chat_bot_details']
                                                if msg_chat_bot != None:
                                                    status_chat_bot = msg_chat_bot['chat_bot_status']
                                                    id_chat_bot = msg_chat_bot['chat_bot_id']
                                                    token_chat_bot = msg_chat_bot['chat_bot_token']
                                                    print(token_chat_bot)
                                                else:
                                                    id_chat_bot = bot_id
                                                    token_chat_bot = token_service
                                            else:
                                                id_chat_bot = bot_id
                                                token_chat_bot = token_service
                                            resultgetProject = sendtask_getProject_tochat_newversion_v3(one_id_info,id_chat_bot,token_chat_bot,token_header)
                                            print(resultgetProject)
                                            if resultgetProject['result'] == 'OK':
                                                result_update = update().update_StatusOneChat_v2(sidcode,email_user,step_num)
                                                priority_ = '1'
                                                titleAndDetails = resouce_result['messageText']
                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                    if str(resultgetProject['messageText']['data'][0]['state'][y]['name']).lower() == 'doing':
                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                result_sumservice = send_chat_paperless_send_approve_v1(data_property,one_id_info,file_name,tracking_id,data_url,sidcode,projectid_,priority_,titleAndDetails,state_id_,resouce_result['messageText'],result_pathUrl,id_chat_bot,token_chat_bot,token_header)
                                                if result_sumservice['result'] == 'OK':
                                                    tmp_messageText = result_sumservice['messageText']
                                                    tmp_res_off_template = tmp_messageText['res_official_template']
                                                    tmp_res_task = tmp_messageText['res_task']
                                                    if 'status' in tmp_res_off_template:
                                                        message_from_onechat = tmp_res_off_template['message']
                                                        id_chat = tmp_res_off_template['message']['id']
                                                        if tmp_res_off_template['status'] == 'success':
                                                            list_Chat_log.append({'result':'OK','email':email_user,'sid':sidcode,'transactionCode':transactionCode,'stepNum':step_num,'id_chat':id_chat})
                                                        else:
                                                            list_Chat_log.append({'result':'ER','email':email_user,'sid':sidcode,'transactionCode':transactionCode,'stepNum':step_num,'id_chat':None})
                                                    else:
                                                        list_Chat_log.append({'result':'ER','email':email_user,'sid':sidcode,'transactionCode':transactionCode,'stepNum':step_num,'id_chat':None})
                                                    if 'status' in tmp_res_task:
                                                        if tmp_res_task['status'] == 'success':
                                                            list_taskChat_log.append({'result':'OK','sidCode':sidcode,'messageText':{'create_task':tmp_res_task,'get_project':resultgetProject['messageText']},'step_num':step_num,'email':email_user})
                                                        else:
                                                            list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'step_num':step_num,'email':email_user})
                                                    else:
                                                        list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'step_num':step_num,'email':email_user})
                                                else:
                                                    list_Chat_log.append({'result':'ER','email':email_user,'sid':sidcode,'transactionCode':transactionCode,'stepNum':step_num,'id_chat':None})
                                                    list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'step_num':step_num,'email':email_user})
                                            else:
                                                list_Chat_log.append({'result':'ER','email':email_user,'sid':sidcode,'transactionCode':transactionCode,'stepNum':step_num,'id_chat':None})
                                                list_taskChat_log.append({'result':'ER','sidCode':sidcode,'messageText':None,'step_num':step_num,'email':email_user})
                                        else:
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error in select UrlSign sidcode emailuser'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error search friend one chat'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error search friend one chat'}),200
                        if len(list_Chat_log) != 0:
                            resultUpdateTask = update().update_taskchat_nextstep(list_taskChat_log)
                            result_update = update().update_ChatToSend_v2(list_Chat_log)
                            result_select = select().select_ForWebHook(sidcode)
                            resouce_result = select().select_forChat_v2(sidcode)
                            if resouce_result['result'] == 'OK':
                                if 'chat_bot_details' in resouce_result['messageText']['documentType_Details'][0]:
                                    msg_chat_bot = resouce_result['messageText']['documentType_Details'][0]['chat_bot_details']
                                    if msg_chat_bot != None:
                                        status_chat_bot = msg_chat_bot['chat_bot_status']
                                        id_chat_bot = msg_chat_bot['chat_bot_id']
                                        token_chat_bot = msg_chat_bot['chat_bot_token']
                                    else:
                                        id_chat_bot = bot_id
                                        token_chat_bot = token_service
                                else:
                                    id_chat_bot = bot_id
                                    token_chat_bot = token_service
                            title_toChat = 'แจ้งเตือนระบบ Paperless'
                            msg_toChat = ''
                            count_res = 0
                            msg_toChat_Paper = ''
                            try:
                                title_toChat  += '\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['sender_email'] + '\n'
                                documentId = res_select['messageText']['documentId']
                            except Exception as ex:
                                documentId = None
                                pass
                            arr_step = []
                            for count in range(len(result_Array)):
                                count_res = count + 1
                                try:
                                    email_User = result_Array[count]['emailUser']
                                    statusSign = result_Array[count]['statusSign']
                                    datetime_string = result_Array[count]['datetime_string']
                                    if result_Array[count]['stepNum'] not in arr_step:
                                        arr_step.append(result_Array[count]['stepNum'])
                                except Exception as ex:
                                    email_User = ''
                                    statusSign = ''
                            for n in arr_step:
                                msg_toChat += '\nลำดับที่ ' + str(n)
                                for count in range(len(result_Array)):
                                    try:
                                        email_User = result_Array[count]['emailUser']
                                        statusSign = result_Array[count]['statusSign']
                                        status_propertyChat = result_Array[count]['status_propertyChat']
                                        if status_propertyChat == 'signning':
                                            if statusSign == 'Complete':
                                                statusSign = 'อนุมัติแล้ว'
                                            elif statusSign == 'Pending':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            elif statusSign == 'Incomplete':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            else:
                                                statusSign = 'ไม่อนุมัติ'
                                        elif status_propertyChat == 'approve':
                                            if statusSign == 'Complete':
                                                statusSign = 'อนุมัติแล้ว'
                                            elif statusSign == 'Pending':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            elif statusSign == 'Incomplete':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            else:
                                                statusSign = 'ไม่อนุมัติ'
                                        datetime_string = result_Array[count]['datetime_string']
                                    except Exception as ex:
                                        email_User = ''
                                        statusSign = ''
                                    if result_Array[count]['stepNum'] == n:
                                        msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                            messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                            result_Email = select().select_GETEmail(sidcode)
                            if result_Email['result'] == 'OK':
                                res_search_frd = search_frd(result_Email['messageText']['email_Sender'],token_header)
                                if 'status' in res_search_frd:
                                    if res_search_frd['status'] == 'success':
                                        result_sendChat = send_messageToChat_v3(messageToChat,res_search_frd['friend']['user_id'],token_chat_bot,id_chat_bot,token_header)
                                        if result_sendChat['status'] == 'success':
                                            return jsonify({'result':'OK','messageText':'send chat success','status_Code':200,'messageER':None,'messageType':'chat','service_Code':'CH01'}),200
                                        else:
                                            return jsonify({'result':'ER','messageText':'send chat fail','status_Code':200,'messageER':None,'messageType':'chat'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found friend','messageType':'chat'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'service search friend error','messageType':'chat'}),200
                            else:
                                return jsonify({'result':'OK','messageText':'send chat success','status_Code':200,'messageER':None,'messageType':'chat'}),200
                        else:
                            resouce_result = select().select_forChat_v2(sidcode)
                            if resouce_result['result'] == 'OK':
                                if 'chat_bot_details' in resouce_result['messageText']['documentType_Details'][0]:
                                    msg_chat_bot = resouce_result['messageText']['documentType_Details'][0]['chat_bot_details']
                                    if msg_chat_bot != None:
                                        status_chat_bot = msg_chat_bot['chat_bot_status']
                                        id_chat_bot = msg_chat_bot['chat_bot_id']
                                        token_chat_bot = msg_chat_bot['chat_bot_token']
                                        # print(token_chat_bot)
                                    else:
                                        id_chat_bot = bot_id
                                        token_chat_bot = token_service
                                else:
                                    id_chat_bot = bot_id
                                    token_chat_bot = token_service
                            res_select = select().select_ForWebHook(sidcode)
                            title_toChat = 'แจ้งเตือนระบบ Paperless'
                            msg_toChat = ''
                            count_res = 0
                            msg_toChat_Paper = ''
                            # print(res_select['messageText'])
                            try:
                                title_toChat  += '\n** ข้อมูลเอกสาร **\nเลขที่เอกสาร : ' + res_select['messageText']['documentId'] + '\nชื่อเอกสาร : ' + res_select['messageText']['fileName'] + '\nเลขที่ติดตามสถานะเอกสาร : ' + res_select['messageText']['trackingId'] + '\nชื่อผู้นำเข้าเอกสาร : ' + res_select['messageText']['sender_email'] + '\n'
                                documentId = res_select['messageText']['documentId']
                            except Exception as ex:
                                documentId = None
                                pass
                            arr_step = []
                            for count in range(len(result_Array)):
                                count_res = count + 1
                                try:
                                    email_User = result_Array[count]['emailUser']
                                    statusSign = result_Array[count]['statusSign']
                                    datetime_string = result_Array[count]['datetime_string']
                                    if result_Array[count]['stepNum'] not in arr_step:
                                        arr_step.append(result_Array[count]['stepNum'])
                                except Exception as ex:
                                    email_User = ''
                                    statusSign = ''

                            for n in arr_step:
                                msg_toChat += '\nลำดับที่ ' + str(n)
                                for count in range(len(result_Array)):
                                    try:
                                        email_User = result_Array[count]['emailUser']
                                        statusSign = result_Array[count]['statusSign']
                                        status_propertyChat = result_Array[count]['status_propertyChat']
                                        if status_propertyChat == 'signning':
                                            if statusSign == 'Complete':
                                                statusSign = 'อนุมัติแล้ว'
                                            elif statusSign == 'Pending':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            elif statusSign == 'Incomplete':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            else:
                                                statusSign = 'ไม่อนุมัติ'
                                        elif status_propertyChat == 'approve':
                                            if statusSign == 'Complete':
                                                statusSign = 'อนุมัติแล้ว'
                                            elif statusSign == 'Pending':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            elif statusSign == 'Incomplete':
                                                statusSign = 'ยังไม่อนุมัติ'
                                            else:
                                                statusSign = 'ไม่อนุมัติ'
                                        datetime_string = result_Array[count]['datetime_string']
                                    except Exception as ex:
                                        email_User = ''
                                        statusSign = ''
                                    if result_Array[count]['stepNum'] == n:
                                        msg_toChat += '\n- ' + email_User +'  ' + statusSign + ''
                            messageToChat = title_toChat + "" + msg_toChat_Paper + "" +msg_toChat
                            result_Email = select().select_GETEmail(sidcode)
                            email_sender_user = result_Email['messageText']['email_Sender']
                            print(email_sender_user)
                            result_search_frd = search_frd(email_sender_user,token_header)
                            print(result_search_frd)
                            if 'status' in result_search_frd:
                                if result_search_frd['status'] == 'success':
                                    user_id_info = result_search_frd['friend']['user_id']
                                    result_send_chat = send_messageToChat_v3(messageToChat,user_id_info,token_chat_bot,id_chat_bot,token_header)
                                    if 'status' in result_send_chat:
                                        if result_send_chat['status'] == 'success':
                                            return jsonify({'result':'OK','messageText':'send chat success','status_Code':200,'messageER':None,'messageType':'chat'})
                                        else:
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'send chat fail','messageType':'chat'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'send chat fail','messageType':'chat'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found friend','messageType':'chat'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'service search friend error','messageType':'chat'}),200

                    return jsonify({'result':'OK','messageText':list_Chat_log,'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(exc_obj, exc_tb.tb_lineno)
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                text_webhook = str('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))+ ' ' + str(type(e).__name__) +' '+ str(e) + ' in ' +fname
                status_code = 500
                success = False
                response = {
                    'result': 'ER',
                    'messageText': None,
                    'messageER': str(e),
                    'status_Code':status_code
                }
                # print(text_webhook)
                callWebHook_slack_v1(text_webhook,'','')
                insert().inert_logger_error_v1(text_webhook,'chat v9')
                return jsonify(response), status_code

@status_methods.route('/api/v1/chat/chat_sender', methods=['POST','GET'])
@token_required_v3
def chat_sender_api_v10():
    if request.method == 'POST':
        dataJson = request.json
        if 'sid_code' in dataJson and len(dataJson) == 1:
            try:
                try:
                    token_header = request.headers['Authorization']
                    try:
                        token_header = str(token_header).split(' ')[1]
                    except Exception as ex:
                        abort(401)
                except KeyError as ex:
                    abort(401)
                sidcode = dataJson['sid_code']
                
                result_message = select().select_chat_sender_v1(sidcode)
                # print(result_message)
                # return ''
                result_get = select().select_data_for_chat_v1(sidcode)
                resouce_result = select().select_forChat_v2(sidcode)
                # return jsonify(result_message)
                hash_sid = hashlib.sha512(str(sidcode).encode('utf-8')).hexdigest()
                response_result = []
                id_chat_bot = bot_id
                token_chat_bot = token_service
                tmp_id_chat_one_dis = None
                result_send_to_sender = None
                if result_get['result'] == 'ER':
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':result_get['messageText']}}),200
                if resouce_result['result'] == 'OK':
                    if resouce_result['messageText']['documentType_Details'][0] != None:
                        if 'chat_bot_details' in resouce_result['messageText']['documentType_Details'][0]:
                            msg_chat_bot = resouce_result['messageText']['documentType_Details'][0]['chat_bot_details']
                            if msg_chat_bot != None:
                                status_chat_bot = msg_chat_bot['chat_bot_status']
                                id_chat_bot = msg_chat_bot['chat_bot_id']
                                token_chat_bot = msg_chat_bot['chat_bot_token']
                            else:
                                id_chat_bot = bot_id
                                token_chat_bot = token_service
                        else:
                            id_chat_bot = bot_id
                            token_chat_bot = token_service
                if result_message['result'] == 'OK':
                    tmp_data = result_message['messageText']
                    for u in range(len(tmp_data)):
                        tmp_chat_id = tmp_data[u]['chat_id']
                        tmp_status_chat_id = tmp_data[u]['chat_id']
                        tmp_email = tmp_data[u]['email']
                        tmp_email_before = None
                        tmp_user_id_before = None
                        tmp_statusChat_before = None
                        tmp_status_Chat = tmp_data[u]['status_Chat']
                        tmp_state_task_chat = tmp_data[u]['chat_state'] 
                        tmp_status = tmp_data[u]['status']
                        tmp_status_ppl = tmp_data[u]['status_ppl']
                        tmp_step_num = tmp_data[u]['step_num']
                        tmp_chat_id_status = tmp_data[u]['chat_id_status']
                        tmp_task_id = tmp_data[u]['task_id']
                        tmp_step_num_group = tmp_data[u]['step_num_group']
                        if len(tmp_data) >= 2:
                            if u != 0: 
                                tmp_statusChat_before = tmp_data[u-1]['status_Chat']
                                tmp_email_before = tmp_data[u-1]['email']
                                for n in tmp_email_before:
                                    result_get_userid = select().select_user_id_from_email_chat_v1(n)
                                    if result_get_userid['result'] == 'OK':
                                        tmp_user_id_before = result_get_userid['messageText']['user_id']
                                        if tmp_user_id_before == None:
                                            result_search_frd_before = search_frd_v2(id_chat_bot,n,token_chat_bot,token_header)
                                            if result_search_frd_before['status'] == 'success':
                                                tmp_friend_before = result_search_frd_before['friend']
                                                tmp_user_id_before = tmp_friend_before['one_id']
                        if tmp_statusChat_before != None:
                            for i in range(len(tmp_statusChat_before)):
                                if tmp_statusChat_before[i] == True:
                                    print(tmp_email_before[i])
                        # print(tmp_statusChat_before , 'tmp_status_before')
                        # print(tmp_email_before , ' tmp_email_before')
                        # print(tmp_user_id_before , ' tmp_user_id_before')
                        if 'Reject' in tmp_status_ppl:
                            if True in tmp_chat_id_status:                                
                                # thr = threading.Thread(target=thread_chat_changeStat_DisButton,args=[tmp_state_task_chat,tmp_task_id,tmp_chat_id,token_chat_bot,id_chat_bot,token_header])
                                # thr.daemon = True   
                                # thr.start()
                                for nz in range(len(tmp_task_id)):
                                    one_task_id = tmp_task_id[nz][0]
                                    tmp_json_state_id_done = tmp_state_task_chat[nz]['done']
                                    if tmp_json_state_id_done != None:
                                        sendtask_change_stateChat_v3(tmp_json_state_id_done,one_task_id,token_chat_bot,id_chat_bot,token_header)
                                for z in range(len(tmp_chat_id)):
                                    tmp_id_chat_one_dis = tmp_chat_id[z]
                                    disble_button_in_oneChat_v4(id_chat_bot,token_chat_bot,tmp_id_chat_one_dis,token_header)
                                for j in range(len(tmp_chat_id)):
                                    if tmp_status_Chat[j] == True:
                                        tmp_email_one_2 = tmp_email[j]
                                        tmp_message_chat_id = tmp_chat_id[j]
                                        update().update_onechatId_v1(sidcode,tmp_email_one_2,tmp_step_num,tmp_message_chat_id)
                            for i in range(len(tmp_email)):
                                if tmp_status_Chat[i] == True:
                                    if result_get['result'] == 'OK':
                                        tmp_get_message = result_get['messageText']
                                        tmp_document_id = tmp_get_message['document_id']
                                        tmp_sender_email = tmp_get_message['sender_email']
                                        tmp_sender_name = tmp_get_message['sender_name']
                                        result_message_text = select().select_chat_sender_v1_text(sidcode,tmp_document_id)
                                        result_get_userid_2 = select().select_user_id_from_email_chat_v1(tmp_sender_email)
                                        if result_message_text['result'] == 'OK':
                                            tmp_message_toChat = result_message_text['messageText'] + '\n' + 'สถานะเอกสาร : ปฏิเสธอนุมัติ'
                                        else:
                                            tmp_message_toChat = 'ไม่สามารถเข้าถึงข้อมูลได้'
                                        if result_get_userid_2['result'] == 'OK':
                                            tmp_user_id_2 = result_get_userid_2['messageText']['user_id']
                                            resultStatusChat = select_3().select_profileGetstatus_v1(tmp_user_id_2)
                                            if resultStatusChat['result'] == 'OK':
                                                tmpstatusChat = resultStatusChat['status_chat']
                                                if tmpstatusChat == True:
                                                    result_send_to_sender = send_messageToChat_v4(tmp_message_toChat,tmp_user_id_2,token_chat_bot,id_chat_bot,token_header)
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':[],'message':'fail cant get data','code':'EROC002'}}),200
                                return jsonify({'result':'OK','messageText':{'data':None,'message':'success document reject','code':'SCOC004'},'status_Code':200,'messageER':None}),200
                        elif 'Complete' in tmp_status_ppl or 'Approve' in tmp_status_ppl:
                            response_status_chat_list = []
                            if result_get['result'] == 'OK':
                                tmp_get_message = result_get['messageText']
                                tmp_document_id = tmp_get_message['document_id']
                                tmp_sender_email = tmp_get_message['sender_email']
                                tmp_sender_name = tmp_get_message['sender_name']
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':[],'message':'fail cant get data','code':'EROC002'}}),200
                            # print(tmp_chat_id_status, "tmp_chat_id_status_1")
                            # print(tmp_state_task_chat,tmp_task_id,tmp_chat_id,token_chat_bot,id_chat_bot,token_header)
                            # if True in tmp_chat_id_status:
                            # thr = threading.Thread(target=thread_chat_changeStat_DisButton,args=[tmp_state_task_chat,tmp_task_id,tmp_chat_id,token_chat_bot,id_chat_bot,token_header])
                            # thr.daemon = True   
                            # thr.start()
                            for nz in range(len(tmp_task_id)):
                                one_task_id = tmp_task_id[nz][0]
                                tmp_json_state_id_done = tmp_state_task_chat[nz]['done']
                                if tmp_json_state_id_done != None:
                                    r = sendtask_change_stateChat_v3(tmp_json_state_id_done,one_task_id,token_chat_bot,id_chat_bot,token_header)
                            for z in range(len(tmp_chat_id)):
                                tmp_id_chat_one_dis = tmp_chat_id[z]
                                r = disble_button_in_oneChat_v4(id_chat_bot,token_chat_bot,tmp_id_chat_one_dis,token_header)
                            
                            for j in range(len(tmp_chat_id)):
                                if tmp_status_Chat[j] == True:
                                    tmp_email_one_2 = tmp_email[j]
                                    tmp_message_chat_id = tmp_chat_id[j]
                                    try:
                                        update().update_onechatId_v1(sidcode,tmp_email_one_2,tmp_step_num,tmp_message_chat_id)
                                    except UnboundLocalError as e:
                                        print(str(e),' UnboundLocalError')
                            tmp_u = u + 1
                            if tmp_u == len(tmp_data):
                                chat_id = ''
                                status_chat = 'fail'
                                response_status_chat_json = {}
                                result_message_text = select().select_chat_sender_v1_text(sidcode,tmp_document_id)
                                result_get_userid_2 = select().select_user_id_from_email_chat_v1(tmp_sender_email)
                                if result_message_text['result'] == 'OK':
                                    tmp_message_toChat = result_message_text['messageText'] + '\n' + 'สถานะเอกสาร : เอกสารสมบูรณ์'
                                else:
                                    tmp_message_toChat = 'ไม่สามารถเข้าถึงข้อมูลได้'
                                if result_get_userid_2['result'] == 'OK':
                                    tmp_user_id_2 = result_get_userid_2['messageText']['user_id']
                                    resultStatusChat = select_3().select_profileGetstatus_v1(tmp_user_id_2)
                                    if resultStatusChat['result'] == 'OK':
                                        tmpstatusChat = resultStatusChat['status_chat']
                                        if tmpstatusChat == True:
                                            result_send_to_sender = send_messageToChat_v4(tmp_message_toChat,tmp_user_id_2,token_chat_bot,id_chat_bot,token_header)
                                    # print(result_send_to_sender)
                                    if result_send_to_sender == None:
                                        if 'status' in result_send_to_sender:
                                            if result_send_to_sender['status'] == 'success':
                                                chat_id = result_send_to_sender['message']['id']
                                                status_chat = 'success'
                                                response_status_chat_json['email'] = tmp_sender_email
                                                response_status_chat_json['status_chat'] = status_chat
                                                response_status_chat_json['status_task'] = None
                                                response_status_chat_json['chat_id'] = chat_id
                                                response_status_chat_json['task_id'] = None
                                                response_status_chat_list.append(response_status_chat_json)
                                            else:
                                                response_result.append({'message':{'email':tmp_sender_email,'messageservice':'cant send to chat'},'code':'EROC400'})
                                        else:
                                            response_result.append({'message':{'email':tmp_sender_email,'messageservice':'cant send to chat'},'code':'EROC400'})
                                    else:
                                        response_result.append({'message':{'email':tmp_sender_email,'messageservice':'cant send to chat'},'code':'EROC400'})
                                else:
                                    response_result.append({'message':{'email':tmp_sender_email,'messageservice':result_search_frd['message']},'code':'EROC404'})
                                    
                                return jsonify({'result':'OK','messageText':{'data':response_status_chat_list,'message':'success','code':'SCOC001'},'status_Code':200,'messageER':[]}),200
                                print('ok')
                        else:
                            # print(tmp_step_num , tmp_step_num_group)
                            if int(tmp_step_num) not in tmp_step_num_group:
                                image_data = createImage_formPDF2(sidcode)
                                if image_data['result'] == 'OK':
                                    image_url_path = myUrl_domain + 'public/viewimage/' + image_data['data']
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error createImage pdf','data':None}}),200
                                type_chat = 'signning'
                                response_result = []
                                response_json = {}
                                response_status_chat_list = []
                                count_status_success = 0
                                count_status_fail = 0
                                for uz in range(len(tmp_status_ppl)):
                                    if tmp_status_ppl[uz] == 'Pending':
                                        type_chat = 'approve'
                                if result_get['result'] == 'OK':
                                    tmp_get_message = result_get['messageText']
                                    tmp_document_id = tmp_get_message['document_id']
                                    tmp_sender_email = tmp_get_message['sender_email']
                                    tmp_sender_name = tmp_get_message['sender_name']
                                    tmp_options_page = tmp_get_message['options_page']
                                    tmp_body_text = tmp_get_message['body_text']
                                    tmp_button_text = tmp_get_message['button_text']
                                    tmp_task_btn_text = tmp_get_message['task_btn_text']
                                    tmp_bio_authen = tmp_get_message['bio_authen']
                                    if 'onechat_message' in tmp_options_page:
                                        tmp_onechat_message = tmp_options_page['onechat_message']
                                        if 'enable_config' in tmp_onechat_message:
                                            tmp_enable_config = tmp_onechat_message['enable_config']
                                            if tmp_enable_config == True:
                                                if 'body_text' in tmp_onechat_message:
                                                    tmp_body_text = tmp_onechat_message['body_text']                                                
                                                    tmp_get_message['body_text'] = tmp_body_text
                                                if 'button_text' in tmp_onechat_message:
                                                    tmp_button_text = tmp_onechat_message['button_text']
                                                    tmp_get_message['button_text'] = tmp_button_text
                                                if 'task_btn_text' in tmp_onechat_message:
                                                    tmp_task_btn_text = tmp_onechat_message['task_btn_text']
                                                    tmp_get_message['task_btn_text'] = tmp_task_btn_text
                                                if 'bio_authen' in tmp_onechat_message:
                                                    tmp_bio_authen = tmp_onechat_message['bio_authen']
                                                    tmp_get_message['bio_authen'] = tmp_bio_authen
                                    for zz in range(len(tmp_get_message['body_text'])):
                                        if zz == 0:
                                            if str(tmp_get_message['body_text'][zz]).replace(' ','') == '':
                                                tmp_get_message['body_text'][zz] = tmp_document_id
                                        elif zz == 1:
                                            if str(tmp_get_message['body_text'][zz]).replace(' ','') == '':
                                                tmp_get_message['body_text'][zz] = 'โดย ' + tmp_sender_name
                                    for i in range(len(tmp_email)):
                                        status_task = 'fail'
                                        status_chat = 'fail'
                                        status_get_project = 'fail'
                                        chat_id = ''
                                        task_id = ''
                                        tmp_email_one = tmp_email[i]
                                        response_status_chat_json = {}
                                        resultStatusChat = select_3().select_profileGetstatus_v1(tmp_email_one)
                                        if resultStatusChat['result'] == 'OK':
                                            tmpstatusChat = resultStatusChat['status_chat']
                                            # print(tmpstatusChat,tmp_email_one)
                                            if tmpstatusChat == True:
                                                if len(tmp_status_chat_id) == 0:
                                                    if tmp_status_Chat[i] == True:                                            
                                                        chat_id = None
                                                        tmp_user_id = tmp_email_one
                                                        ##################################### ค้นหาเพื่อน
                                                        # result_get_userid = select().select_user_id_from_email_chat_v1(tmp_email_one)
                                                        # if result_get_userid['result'] == 'OK':
                                                        #     tmp_user_id = result_get_userid['messageText']['user_id']
                                                        #     if tmp_user_id == None:
                                                        #         result_search_frd = search_frd_v2(id_chat_bot,tmp_email_one,token_chat_bot,token_header)
                                                        #         if result_search_frd['status'] == 'success':
                                                        #             tmp_friend = result_search_frd['friend']
                                                        #             tmp_user_id = tmp_friend['one_id']
                                                        #         else:
                                                        #             count_status_fail = count_status_fail + 1
                                                        #             response_result.append({'message':{'email':tmp_email_one,'messageservice':result_search_frd['message']},'code':'EROC404'})
                                                        sendchat_result = send_chat_paperless_send_approve_v2(tmp_bio_authen,tmp_task_btn_text,tmp_body_text,tmp_button_text,tmp_document_id,type_chat,hash_sid,id_chat_bot,token_chat_bot,tmp_email_one,tmp_user_id,image_url_path,token_header)
                                                        
                                                        if sendchat_result['result'] == 'OK':
                                                            tmp_msg = sendchat_result['msg']
                                                            tmp_res_official_template = tmp_msg['res_official_template']
                                                            tmp_res_project = tmp_msg['res_project']
                                                            tmp_res_task = tmp_msg['res_task']
                                                            if tmp_res_official_template['status'] == 'success':
                                                                tmp_message_chat = tmp_res_official_template['message']
                                                                chat_id = tmp_message_chat['id']
                                                                status_chat = 'success'
                                                            if tmp_res_task['status'] == 'success':
                                                                status_task = 'success'
                                                                task_id = tmp_res_task['data']['task_id']
                                                            if tmp_res_project['status'] == 'success':
                                                                status_get_project = 'success'
                                                            count_status_success = count_status_success + 1
                                                            response_status_chat_json['email'] = tmp_email_one
                                                            response_status_chat_json['status_chat'] = status_chat
                                                            response_status_chat_json['status_task'] = status_task
                                                            response_status_chat_json['chat_id'] = chat_id
                                                            response_status_chat_json['task_id'] = task_id
                                                            response_status_chat_list.append(response_status_chat_json)
                                                            result_update = update().update_StatusOneChat_v3(sidcode,tmp_email_one,tmp_step_num,chat_id,task_id,'Complete')
                                                        else:
                                                            count_status_fail = count_status_fail + 1
                                                            response_status_chat_json['email'] = tmp_email_one
                                                            response_status_chat_json['status_chat'] = status_chat
                                                            response_status_chat_json['status_task'] = status_task
                                                            response_status_chat_json['chat_id'] = chat_id
                                                            response_status_chat_json['task_id'] = task_id
                                                            response_status_chat_list.append(response_status_chat_json)
                                                            result_update = update().update_StatusOneChat_v3(sidcode,tmp_email_one,tmp_step_num,chat_id,task_id,'Fail')
                                                    else:
                                                        count_status_fail = count_status_fail + 1
                                                        response_result.append({'message':{'email':tmp_email_one,'messageservice':'dont want send to chat'},'code':'EROC200'})
                                                else:
                                                    if tmp_status_Chat[i] == True:
                                                        chat_id = None
                                                        tmp_user_id = tmp_email_one
                                                        ##################################### ค้นหาเพื่อน
                                                        # result_get_userid = select().select_user_id_from_email_chat_v1(tmp_email_one)
                                                        # if result_get_userid['result'] == 'OK':
                                                        #     tmp_user_id = result_get_userid['messageText']['user_id']
                                                        #     tmp_user_id = None
                                                        #     if tmp_user_id == None:
                                                        #         result_search_frd = search_frd_v2(id_chat_bot,tmp_email_one,token_chat_bot,token_header)
                                                        #         if 'status' in result_search_frd:
                                                        #             if result_search_frd['status'] == 'success':
                                                        #                 tmp_friend = result_search_frd['friend']
                                                        #                 tmp_user_id = tmp_friend['one_id']
                                                        #             else:
                                                        #                 count_status_fail = count_status_fail + 1
                                                        #                 response_result.append({'message':{'email':tmp_email_one,'messageservice':result_search_frd['message']},'code':'EROC404'})
                                                        #         else:
                                                        #             tmp_user_id = tmp_email_one
                                                                    
                                                        # print(tmp_email[i])
                                                        # print(tmp_body_text,tmp_button_text,tmp_document_id,type_chat,hash_sid,id_chat_bot,token_chat_bot,tmp_email_one,tmp_user_id,image_url_path,token_header)
                                                        sendchat_result = sender_one_chat_templatechat_v2(tmp_body_text,tmp_button_text,tmp_document_id,type_chat,hash_sid,id_chat_bot,token_chat_bot,tmp_email_one,tmp_user_id,image_url_path,token_header)
                                                        if sendchat_result['result'] == 'OK':
                                                            tmp_msg = sendchat_result['msg']
                                                            if tmp_msg['status'] == 'success':
                                                                status_chat = 'success'
                                                                chat_id = tmp_msg['message']['id']
                                                                count_status_success = count_status_success + 1
                                                            response_status_chat_json['email'] = tmp_email_one
                                                            response_status_chat_json['status_chat'] = status_chat
                                                            response_status_chat_json['status_task'] = 'success'
                                                            response_status_chat_json['chat_id'] = chat_id
                                                            response_status_chat_json['task_id'] = tmp_task_id[0][0]
                                                            response_status_chat_list.append(response_status_chat_json)
                                                            result_update = update().update_StatusOneChat_v3(sidcode,tmp_email_one,tmp_step_num,chat_id,None,'Complete')
                                                        else:
                                                            count_status_fail = count_status_fail + 1
                                                            response_status_chat_json['email'] = tmp_email_one
                                                            response_status_chat_json['status_chat'] = status_chat
                                                            response_status_chat_json['status_task'] = 'success'
                                                            response_status_chat_json['chat_id'] = chat_id
                                                            response_status_chat_json['task_id'] = tmp_task_id[0][0]
                                                            response_status_chat_list.append(response_status_chat_json)
                                                            result_update = update().update_StatusOneChat_v3(sidcode,tmp_email_one,tmp_step_num,chat_id,None,'Fail')
                                                    else:
                                                        count_status_fail = count_status_fail + 1
                                                        response_result.append({'message':{'email':tmp_email_one,'messageservice':'dont want send to chat'},'code':'EROC200'})
                                        # return jsonify(tmp_data)
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':[],'message':'fail cant get data','code':'EROC002'}}),200
                                result_message_text = select().select_chat_sender_v1_text(sidcode,tmp_document_id)
                                result_get_userid_2 = select().select_user_id_from_email_chat_v1(tmp_sender_email)
                                if result_message_text['result'] == 'OK':
                                    tmp_message_toChat = result_message_text['messageText'] + '\n' + 'สถานะเอกสาร : รอดำเนินการ'
                                else:
                                    tmp_message_toChat = 'ไม่สามารถเข้าถึงข้อมูลได้'
                                if result_get_userid_2['result'] == 'OK':
                                    tmp_user_id_2 = result_get_userid_2['messageText']['user_id']                                    
                                    resultStatusChat = select_3().select_profileGetstatus_v1(tmp_user_id_2)
                                    if resultStatusChat['result'] == 'OK':
                                        tmpstatusChat = resultStatusChat['status_chat']
                                        if tmpstatusChat == True:
                                            result_send_to_sender = send_messageToChat_v4(tmp_message_toChat,tmp_user_id_2,token_chat_bot,id_chat_bot,token_header)
                                    # if result_send_to_sender['status'] == 'success':
                                    #     pass
                                    # else:
                                    #     pass
                                else:
                                    response_result.append({'message':{'email':tmp_email_one,'messageservice':result_search_frd['message']},'code':'EROC404'})
                                if count_status_fail >= 1:
                                    return jsonify({'result':'OK','messageText':{'data':response_status_chat_list,'message':'success','code':'SCOC002'},'status_Code':200,'messageER':response_result}),200
                                # else:
                                return jsonify({'result':'OK','messageText':{'data':response_status_chat_list,'message':'success','code':'SCOC001'},'status_Code':200,'messageER':[]}),200
                            else:
                                return jsonify({'result':'OK','messageText':{'data':'group document','message':'success','code':'SCOC000'},'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':result_message['messageText'],'message':'success','code':'EROC001'}}),200
                                # return jsonify({'result':'OK','messageText':{'data':result_message['messageText'],'message':'success','code':'SCOC002'},'status_Code':200,'messageER':response_result}),200
                # SCOC001 sccuess ทั้งหมด
                # SCOC002 มี fail อยู่บ้างส่วน รายละเอียดที่ messageER
                return jsonify({'result':'OK','messageText':{'data':result_message['messageText'],'message':'success','code':'SCOC001'},'status_Code':200,'messageER':[]}),200
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'exception ' + str(exc_type)}}),200

#new chat
@status_methods.route('/api/v10/chat/chat_sender', methods=['POST','GET'])
@token_required_v3
def chat_sender_api_v1_new():
    if request.method == 'POST':
        dataJson = request.json
        if 'sid_code' in dataJson and len(dataJson) == 1:
            try:
                try:
                    token_header = request.headers['Authorization']
                    try:
                        token_header = str(token_header).split(' ')[1]
                    except Exception as ex:
                        abort(401)
                except KeyError as ex:
                    abort(401)
                sidcode = dataJson['sid_code']
                r = chat_for_service_v1(sidcode,'Bearer ' + token_header)
                return jsonify(r)
                result_message = select_4().select_chat_sender_v1(sidcode)   
                print('result_message',result_message)             
                # result_message = select().select_chat_sender_v1(sidcode)
                # print(result_message)
                # return result_message
                # result_get = select().select_data_for_chat_v1(sidcode)
                # resouce_result = select().select_forChat_v2(sidcode)
                # return jsonify(result_message)
                hash_sid = hashlib.sha512(str(sidcode).encode('utf-8')).hexdigest()
                response_result = []
                id_chat_bot = bot_id
                token_chat_bot = token_service
                tmp_id_chat_one_dis = None
                result_send_to_sender = None
                if result_message['result'] == 'ER':
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':result_message['messageText']}}),200
                if result_message['result'] == 'OK':
                    if result_message['datachat']['documentType_Details'][0] != None:
                        if 'chat_bot_details' in result_message['datachat']['documentType_Details'][0]:
                            msg_chat_bot = result_message['datachat']['documentType_Details'][0]['chat_bot_details']
                            if msg_chat_bot != None:
                                status_chat_bot = msg_chat_bot['chat_bot_status']
                                id_chat_bot = msg_chat_bot['chat_bot_id']
                                token_chat_bot = msg_chat_bot['chat_bot_token']
                            else:
                                id_chat_bot = bot_id
                                token_chat_bot = token_service
                        else:
                            id_chat_bot = bot_id
                            token_chat_bot = token_service 
                print('token_chat_bot',token_chat_bot)   
                if result_message['result'] == 'OK':
                    tmp_data = result_message['messageText']
                    for u in range(len(tmp_data)):
                        tmp_chat_id = tmp_data[u]['chat_id']
                        tmp_status_chat_id = tmp_data[u]['chat_id']
                        tmp_email = tmp_data[u]['email']
                        tmp_email_before = None
                        tmp_user_id_before = None
                        tmp_statusChat_before = None
                        tmp_status_Chat = tmp_data[u]['status_Chat']
                        tmp_state_task_chat = tmp_data[u]['chat_state'] 
                        tmp_status = tmp_data[u]['status']
                        tmp_status_ppl = tmp_data[u]['status_ppl']
                        tmp_step_num = tmp_data[u]['step_num']
                        tmp_chat_id_status = tmp_data[u]['chat_id_status']
                        tmp_task_id = tmp_data[u]['task_id']
                        tmp_step_num_group = tmp_data[u]['step_num_group']
                        if len(tmp_data) >= 2:
                            if u != 0: 
                                tmp_statusChat_before = tmp_data[u-1]['status_Chat']
                                tmp_email_before = tmp_data[u-1]['email']
                                for n in tmp_email_before:
                                    result_get_userid = select().select_user_id_from_email_chat_v1(n)
                                    if result_get_userid['result'] == 'OK':
                                        tmp_user_id_before = result_get_userid['messageText']['user_id']
                                        if tmp_user_id_before == None:
                                            result_search_frd_before = search_frd_v2(id_chat_bot,n,token_chat_bot,token_header)
                                            if result_search_frd_before['status'] == 'success':
                                                tmp_friend_before = result_search_frd_before['friend']
                                                tmp_user_id_before = tmp_friend_before['one_id']
                        if tmp_statusChat_before != None:
                            for i in range(len(tmp_statusChat_before)):
                                if tmp_statusChat_before[i] == True:
                                    print(tmp_email_before[i])
                        # print(tmp_statusChat_before , 'tmp_status_before')
                        # print(tmp_email_before , ' tmp_email_before')
                        # print(tmp_user_id_before , ' tmp_user_id_before')
                        print('tmp_statusChat_before',tmp_statusChat_before)  
                        if 'Reject' in tmp_status_ppl:
                            if True in tmp_chat_id_status:                                
                                # thr = threading.Thread(target=thread_chat_changeStat_DisButton,args=[tmp_state_task_chat,tmp_task_id,tmp_chat_id,token_chat_bot,id_chat_bot,token_header])
                                # thr.daemon = True   
                                # thr.start()
                                # thread_change_state_onechat_v1
                                # thr_changestate = threading.Thread(target=thread_change_state_onechat_v1,args=[tmp_task_id,token_chat_bot,id_chat_bot,token_header])
                                # thr_disble = threading.Thread(target=thread_disble_button_onechat_v1,args=[tmp_chat_id,token_chat_bot,tmp_id_chat_one_dis,id_chat_bot,token_header])
                                # # thr.daemon = True   
                                # thr_changestate.start()
                                # thr_disble.start()
                                # with concurrent.futures.ThreadPoolExecutor() as executor:
                                #     executor.submit(thread_change_state_onechat_v1, tmp_task_id,token_chat_bot,id_chat_bot,token_header)
                                #     executor.submit(thread_disble_button_onechat_v1, tmp_chat_id,token_chat_bot,tmp_id_chat_one_dis,id_chat_bot,token_header)
                                for nz in range(len(tmp_task_id)):
                                    one_task_id = tmp_task_id[nz][0]
                                    # tmp_json_state_id_done = tmp_state_task_chat[nz]['done']
                                    # if tmp_json_state_id_done != None:
                                    r = sendtask_change_stateChat_v4(one_task_id,token_chat_bot,id_chat_bot,token_header)
                                for z in range(len(tmp_chat_id)):
                                    tmp_id_chat_one_dis = tmp_chat_id[z]
                                    disble_button_in_oneChat_v5(id_chat_bot,token_chat_bot,tmp_id_chat_one_dis,token_header)
                                # for nz in range(len(tmp_task_id)):
                                #     one_task_id = tmp_task_id[nz][0]
                                #     tmp_json_state_id_done = tmp_state_task_chat[nz]['done']
                                #     if tmp_json_state_id_done != None:
                                #         sendtask_change_stateChat_v3(tmp_json_state_id_done,one_task_id,token_chat_bot,id_chat_bot,token_header)
                                # for z in range(len(tmp_chat_id)):
                                #     tmp_id_chat_one_dis = tmp_chat_id[z]
                                #     disble_button_in_oneChat_v4(id_chat_bot,token_chat_bot,tmp_id_chat_one_dis,token_header)
                                for j in range(len(tmp_chat_id)):
                                    if tmp_status_Chat[j] == True:
                                        tmp_email_one_2 = tmp_email[j]
                                        tmp_message_chat_id = tmp_chat_id[j]
                                        update().update_onechatId_v1(sidcode,tmp_email_one_2,tmp_step_num,tmp_message_chat_id)
                            for i in range(len(tmp_email)):
                                if tmp_status_Chat[i] == True:
                                    if result_message['result'] == 'OK':
                                        tmp_get_message = result_message['data']
                                        tmp_document_id = tmp_get_message['document_id']
                                        tmp_sender_email = tmp_get_message['sender_email']
                                        tmp_sender_name = tmp_get_message['sender_name']
                                        result_message_text = select().select_chat_sender_v1_text(sidcode,tmp_document_id)
                                        result_get_userid_2 = select().select_user_id_from_email_chat_v1(tmp_sender_email)
                                        if result_message_text['result'] == 'OK':
                                            tmp_message_toChat = result_message_text['messageText'] + '\n' + 'สถานะเอกสาร : ปฏิเสธอนุมัติ'
                                        else:
                                            tmp_message_toChat = 'ไม่สามารถเข้าถึงข้อมูลได้'
                                        if result_get_userid_2['result'] == 'OK':
                                            tmp_user_id_2 = result_get_userid_2['messageText']['user_id']
                                            resultStatusChat = select_3().select_profileGetstatus_v1(tmp_user_id_2)
                                            if resultStatusChat['result'] == 'OK':
                                                tmpstatusChat = resultStatusChat['status_chat']
                                                if tmpstatusChat == True:
                                                    result_send_to_sender = send_messageToChat_v4(tmp_message_toChat,tmp_user_id_2,token_chat_bot,id_chat_bot,token_header)
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':[],'message':'fail cant get data','code':'EROC002'}}),200
                                return jsonify({'result':'OK','messageText':{'data':None,'message':'success document reject','code':'SCOC004'},'status_Code':200,'messageER':None}),200
                        elif 'Complete' in tmp_status_ppl or 'Approve' in tmp_status_ppl:
                            response_status_chat_list = []
                            if result_message['result'] == 'OK':
                                tmp_get_message = result_message['data']
                                tmp_document_id = tmp_get_message['document_id']
                                tmp_sender_email = tmp_get_message['sender_email']
                                tmp_sender_name = tmp_get_message['sender_name']
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':[],'message':'fail cant get data','code':'EROC002'}}),200
                            # print(tmp_chat_id_status, "tmp_chat_id_status_1")
                            # print(tmp_state_task_chat,tmp_task_id,tmp_chat_id,token_chat_bot,id_chat_bot,token_header)
                            # if True in tmp_chat_id_status:
                            # thr_changestate = threading.Thread(target=thread_change_state_onechat_v1,args=[tmp_task_id,token_chat_bot,id_chat_bot,token_header])
                            # thr_disble = threading.Thread(target=thread_disble_button_onechat_v1,args=[tmp_chat_id,token_chat_bot,tmp_id_chat_one_dis,id_chat_bot,token_header])
                            # # # thr.daemon = True   
                            # thr_changestate.start()
                            # thr_disble.start()                            
                            # with concurrent.futures.ThreadPoolExecutor() as executor:
                            #     executor.submit(thread_change_state_onechat_v1, tmp_task_id,token_chat_bot,id_chat_bot,token_header)
                            #     executor.submit(thread_disble_button_onechat_v1, tmp_chat_id,token_chat_bot,tmp_id_chat_one_dis,id_chat_bot,token_header)
                            for nz in range(len(tmp_task_id)):
                                one_task_id = tmp_task_id[nz][0]
                                # tmp_json_state_id_done = tmp_state_task_chat[nz]['done']
                                # if tmp_json_state_id_done != None:
                                r = sendtask_change_stateChat_v4(one_task_id,token_chat_bot,id_chat_bot,token_header)

                            for z in range(len(tmp_chat_id)):
                                tmp_id_chat_one_dis = tmp_chat_id[z]
                                r = disble_button_in_oneChat_v5(id_chat_bot,token_chat_bot,tmp_id_chat_one_dis,token_header)
                            
                            for j in range(len(tmp_chat_id)):
                                if tmp_status_Chat[j] == True:
                                    tmp_email_one_2 = tmp_email[j]
                                    tmp_message_chat_id = tmp_chat_id[j]
                                    # print(tmp_message_chat_id)
                                    try:
                                        update().update_onechatId_v1(sidcode,tmp_email_one_2,tmp_step_num,tmp_message_chat_id)
                                    except UnboundLocalError as e:
                                        print(str(e),' UnboundLocalError')
                            tmp_u = u + 1
                            if tmp_u == len(tmp_data):
                                chat_id = ''
                                status_chat = 'fail'
                                response_status_chat_json = {}
                                result_message_text = select().select_chat_sender_v1_text(sidcode,tmp_document_id)
                                result_get_userid_2 = select().select_user_id_from_email_chat_v1(tmp_sender_email)
                                if result_message_text['result'] == 'OK':
                                    tmp_message_toChat = result_message_text['messageText'] + '\n' + 'สถานะเอกสาร : เอกสารสมบูรณ์'
                                else:
                                    tmp_message_toChat = 'ไม่สามารถเข้าถึงข้อมูลได้'
                                if result_get_userid_2['result'] == 'OK':
                                    tmp_user_id_2 = result_get_userid_2['messageText']['user_id']
                                    resultStatusChat = select_3().select_profileGetstatus_v1(tmp_user_id_2)
                                    if resultStatusChat['result'] == 'OK':
                                        tmpstatusChat = resultStatusChat['status_chat']
                                        if tmpstatusChat == True:
                                            result_send_to_sender = send_messageToChat_v4(tmp_message_toChat,tmp_user_id_2,token_chat_bot,id_chat_bot,token_header)
                                    # print(result_send_to_sender)
                                    if result_send_to_sender == None:
                                        if 'status' in result_send_to_sender:
                                            if result_send_to_sender['status'] == 'success':
                                                chat_id = result_send_to_sender['message']['id']
                                                status_chat = 'success'
                                                response_status_chat_json['email'] = tmp_sender_email
                                                response_status_chat_json['status_chat'] = status_chat
                                                response_status_chat_json['status_task'] = None
                                                response_status_chat_json['chat_id'] = chat_id
                                                response_status_chat_json['task_id'] = None
                                                response_status_chat_list.append(response_status_chat_json)
                                            else:
                                                response_result.append({'message':{'email':tmp_sender_email,'messageservice':'cant send to chat'},'code':'EROC400'})
                                        else:
                                            response_result.append({'message':{'email':tmp_sender_email,'messageservice':'cant send to chat'},'code':'EROC400'})
                                    else:
                                        response_result.append({'message':{'email':tmp_sender_email,'messageservice':'cant send to chat'},'code':'EROC400'})
                                else:
                                    response_result.append({'message':{'email':tmp_sender_email,'messageservice':result_search_frd['message']},'code':'EROC404'})
                                    
                                return jsonify({'result':'OK','messageText':{'data':response_status_chat_list,'message':'success','code':'SCOC001'},'status_Code':200,'messageER':[]}),200
                                print('ok')
                        else:
                            # print(tmp_step_num , tmp_step_num_group)
                            if int(tmp_step_num) not in tmp_step_num_group:
                                image_data = {}
                                image_data['data'] = ''
                                # image_data = createImage_formPDF2(sidcode)
                                # if image_data['result'] == 'OK':
                                image_url_path = myUrl_domain + 'public/viewimage/' + image_data['data']
                                image_url_path = 'https://www.img.in.th/images/83ca9b38ee2d7d129f1826f75ea05e4f.png'
                                # else:
                                #     return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error createImage pdf','data':None}}),200
                                type_chat = 'signning'
                                response_result = []
                                response_json = {}
                                response_status_chat_list = []
                                count_status_success = 0
                                count_status_fail = 0
                                for uz in range(len(tmp_status_ppl)):
                                    if tmp_status_ppl[uz] == 'Pending':
                                        type_chat = 'approve'
                                if result_message['result'] == 'OK':
                                    tmp_get_message = result_message['data']
                                    print(tmp_get_message)
                                    tmp_document_id = tmp_get_message['document_id']
                                    tmp_sender_email = tmp_get_message['sender_email']
                                    tmp_sender_name = tmp_get_message['sender_name']
                                    tmp_options_page = tmp_get_message['options_page']
                                    tmp_body_text = tmp_get_message['body_text']
                                    tmp_button_text = tmp_get_message['button_text']
                                    tmp_task_btn_text = tmp_get_message['task_btn_text']
                                    tmp_bio_authen = tmp_get_message['bio_authen']
                                    if 'onechat_message' in tmp_options_page:
                                        tmp_onechat_message = tmp_options_page['onechat_message']
                                        if 'enable_config' in tmp_onechat_message:
                                            tmp_enable_config = tmp_onechat_message['enable_config']
                                            if tmp_enable_config == True:
                                                if 'body_text' in tmp_onechat_message:
                                                    tmp_body_text = tmp_onechat_message['body_text']                                                
                                                    tmp_get_message['body_text'] = tmp_body_text
                                                if 'button_text' in tmp_onechat_message:
                                                    tmp_button_text = tmp_onechat_message['button_text']
                                                    tmp_get_message['button_text'] = tmp_button_text
                                                if 'task_btn_text' in tmp_onechat_message:
                                                    tmp_task_btn_text = tmp_onechat_message['task_btn_text']
                                                    tmp_get_message['task_btn_text'] = tmp_task_btn_text
                                                if 'bio_authen' in tmp_onechat_message:
                                                    tmp_bio_authen = tmp_onechat_message['bio_authen']
                                                    tmp_get_message['bio_authen'] = tmp_bio_authen
                                    for zz in range(len(tmp_get_message['body_text'])):
                                        if zz == 0:
                                            if str(tmp_get_message['body_text'][zz]).replace(' ','') == '':
                                                tmp_get_message['body_text'][zz] = tmp_document_id
                                        elif zz == 1:
                                            if str(tmp_get_message['body_text'][zz]).replace(' ','') == '':
                                                tmp_get_message['body_text'][zz] = 'โดย ' + tmp_sender_name
                                    print(tmp_email)
                                    for i in range(len(tmp_email)):
                                        status_task = 'fail'
                                        status_chat = 'fail'
                                        status_get_project = 'fail'
                                        chat_id = ''
                                        task_id = ''
                                        tmp_email_one = tmp_email[i]
                                        response_status_chat_json = {}
                                        resultStatusChat = select_3().select_profileGetstatus_v1(tmp_email_one)
                                        chat_message_id = str(uuid.uuid4())
                                        if resultStatusChat['result'] == 'OK':
                                            tmpstatusChat = resultStatusChat['status_chat']
                                            if tmpstatusChat == True:
                                                if len(tmp_status_chat_id) == 0:
                                                    if tmp_status_Chat[i] == True:                                            
                                                        chat_id = None
                                                        tmp_user_id = tmp_email_one
                                                        ##################################### ค้นหาเพื่อน
                                                        # result_get_userid = select().select_user_id_from_email_chat_v1(tmp_email_one)
                                                        # if result_get_userid['result'] == 'OK':
                                                        #     tmp_user_id = result_get_userid['messageText']['user_id']
                                                        #     if tmp_user_id == None:
                                                        #         result_search_frd = search_frd_v2(id_chat_bot,tmp_email_one,token_chat_bot,token_header)
                                                        #         if result_search_frd['status'] == 'success':
                                                        #             tmp_friend = result_search_frd['friend']
                                                        #             tmp_user_id = tmp_friend['one_id']
                                                        #         else:
                                                        #             count_status_fail = count_status_fail + 1
                                                        #             response_result.append({'message':{'email':tmp_email_one,'messageservice':result_search_frd['message']},'code':'EROC404'})
                                                        sendchat_result = send_chat_paperless_send_approve_v3("approve",tmp_bio_authen,tmp_task_btn_text,tmp_body_text,tmp_button_text,tmp_document_id,type_chat,hash_sid,id_chat_bot,token_chat_bot,tmp_email_one,tmp_user_id,image_url_path,token_header,chat_message_id)
                                                        
                                                        result_update = update().update_StatusOneChat_v3(sidcode,tmp_email_one,tmp_step_num,chat_message_id,chat_message_id,'Complete')                                                    
                                                        # if sendchat_result['result'] == 'OK':
                                                        #     tmp_msg = sendchat_result['msg']
                                                        #     tmp_res_official_template = tmp_msg['res_official_template']
                                                        #     tmp_res_project = tmp_msg['res_project']
                                                        #     tmp_res_task = tmp_msg['res_task']
                                                        #     if tmp_res_official_template['status'] == 'success':
                                                        #         tmp_message_chat = tmp_res_official_template['message']
                                                        #         chat_id = tmp_message_chat['id']
                                                        #         status_chat = 'success'
                                                        #     if tmp_res_task['status'] == 'success':
                                                        #         status_task = 'success'
                                                        #         task_id = tmp_res_task['data']['task_id']
                                                        #     if tmp_res_project['status'] == 'success':
                                                        #         status_get_project = 'success'
                                                        #     count_status_success = count_status_success + 1
                                                        #     response_status_chat_json['email'] = tmp_email_one
                                                        #     response_status_chat_json['status_chat'] = status_chat
                                                        #     response_status_chat_json['status_task'] = status_task
                                                        #     response_status_chat_json['chat_id'] = chat_id
                                                        #     response_status_chat_json['task_id'] = task_id
                                                        #     response_status_chat_list.append(response_status_chat_json)
                                                        #     result_update = update().update_StatusOneChat_v3(sidcode,tmp_email_one,tmp_step_num,chat_message_id,chat_message_id,'Complete')
                                                        # else:
                                                        #     count_status_fail = count_status_fail + 1
                                                        #     response_status_chat_json['email'] = tmp_email_one
                                                        #     response_status_chat_json['status_chat'] = status_chat
                                                        #     response_status_chat_json['status_task'] = status_task
                                                        #     response_status_chat_json['chat_id'] = chat_id
                                                        #     response_status_chat_json['task_id'] = task_id
                                                        #     response_status_chat_list.append(response_status_chat_json)
                                                        #     result_update = update().update_StatusOneChat_v3(sidcode,tmp_email_one,tmp_step_num,chat_message_id,chat_message_id,'Fail')
                                                    else:
                                                        count_status_fail = count_status_fail + 1
                                                        response_result.append({'message':{'email':tmp_email_one,'messageservice':'dont want send to chat'},'code':'EROC200'})
                                                else:
                                                    if tmp_status_Chat[i] == True:
                                                        chat_id = None
                                                        tmp_user_id = tmp_email_one
                                                        ##################################### ค้นหาเพื่อน
                                                        # result_get_userid = select().select_user_id_from_email_chat_v1(tmp_email_one)
                                                        # if result_get_userid['result'] == 'OK':
                                                        #     tmp_user_id = result_get_userid['messageText']['user_id']
                                                        #     tmp_user_id = None
                                                        #     if tmp_user_id == None:
                                                        #         result_search_frd = search_frd_v2(id_chat_bot,tmp_email_one,token_chat_bot,token_header)
                                                        #         if 'status' in result_search_frd:
                                                        #             if result_search_frd['status'] == 'success':
                                                        #                 tmp_friend = result_search_frd['friend']
                                                        #                 tmp_user_id = tmp_friend['one_id']
                                                        #             else:
                                                        #                 count_status_fail = count_status_fail + 1
                                                        #                 response_result.append({'message':{'email':tmp_email_one,'messageservice':result_search_frd['message']},'code':'EROC404'})
                                                        #         else:
                                                        #             tmp_user_id = tmp_email_one
                                                                    
                                                        # print(tmp_email[i])
                                                        # print(tmp_body_text,tmp_button_text,tmp_document_id,type_chat,hash_sid,id_chat_bot,token_chat_bot,tmp_email_one,tmp_user_id,image_url_path,token_header)
                                                        sendchat_result = send_chat_paperless_send_approve_v3("approve",tmp_bio_authen,tmp_task_btn_text,tmp_body_text,tmp_button_text,tmp_document_id,type_chat,hash_sid,id_chat_bot,token_chat_bot,tmp_email_one,tmp_user_id,image_url_path,token_header,chat_message_id)
                                                        print(sendchat_result)
                                                        # sendchat_result = send_chat_paperless_send_approve_v3("message",tmp_body_text,tmp_button_text,tmp_document_id,type_chat,hash_sid,id_chat_bot,token_chat_bot,tmp_email_one,tmp_user_id,image_url_path,token_header,chat_message_id)
                                                        result_update = update().update_StatusOneChat_v3(sidcode,tmp_email_one,tmp_step_num,chat_message_id,None,'Complete')
                                                        # if sendchat_result['result'] == 'OK':
                                                        #     tmp_msg = sendchat_result['msg']
                                                        #     if tmp_msg['status'] == 'success':
                                                        #         status_chat = 'success'
                                                        #         chat_id = tmp_msg['message']['id']
                                                        #         count_status_success = count_status_success + 1
                                                        #     response_status_chat_json['email'] = tmp_email_one
                                                        #     response_status_chat_json['status_chat'] = status_chat
                                                        #     response_status_chat_json['status_task'] = 'success'
                                                        #     response_status_chat_json['chat_id'] = chat_id
                                                        #     response_status_chat_json['task_id'] = tmp_task_id[0][0]
                                                        #     response_status_chat_list.append(response_status_chat_json)
                                                        #     result_update = update().update_StatusOneChat_v3(sidcode,tmp_email_one,tmp_step_num,chat_id,None,'Complete')
                                                        # else:
                                                        #     count_status_fail = count_status_fail + 1
                                                        #     response_status_chat_json['email'] = tmp_email_one
                                                        #     response_status_chat_json['status_chat'] = status_chat
                                                        #     response_status_chat_json['status_task'] = 'success'
                                                        #     response_status_chat_json['chat_id'] = chat_id
                                                        #     response_status_chat_json['task_id'] = tmp_task_id[0][0]
                                                        #     response_status_chat_list.append(response_status_chat_json)
                                                        #     result_update = update().update_StatusOneChat_v3(sidcode,tmp_email_one,tmp_step_num,chat_id,None,'Fail')
                                                    else:
                                                        count_status_fail = count_status_fail + 1
                                                        response_result.append({'message':{'email':tmp_email_one,'messageservice':'dont want send to chat'},'code':'EROC200'})
                                        # return jsonify(tmp_data)
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':[],'message':'fail cant get data','code':'EROC002'}}),200
                                result_message_text = select().select_chat_sender_v1_text(sidcode,tmp_document_id)
                                result_get_userid_2 = select().select_user_id_from_email_chat_v1(tmp_sender_email)
                                if result_message_text['result'] == 'OK':
                                    tmp_message_toChat = result_message_text['messageText'] + '\n' + 'สถานะเอกสาร : รอดำเนินการ'
                                else:
                                    tmp_message_toChat = 'ไม่สามารถเข้าถึงข้อมูลได้'
                                if result_get_userid_2['result'] == 'OK':
                                    tmp_user_id_2 = result_get_userid_2['messageText']['user_id']                                    
                                    resultStatusChat = select_3().select_profileGetstatus_v1(tmp_user_id_2)
                                    if resultStatusChat['result'] == 'OK':
                                        tmpstatusChat = resultStatusChat['status_chat']
                                        if tmpstatusChat == True:
                                            result_send_to_sender = send_messageToChat_v4(tmp_message_toChat,tmp_user_id_2,token_chat_bot,id_chat_bot,token_header)
                                    # if result_send_to_sender['status'] == 'success':
                                    #     pass
                                    # else:
                                    #     pass
                                else:
                                    response_result.append({'message':{'email':tmp_email_one,'messageservice':result_search_frd['message']},'code':'EROC404'})
                                if count_status_fail >= 1:
                                    return jsonify({'result':'OK','messageText':{'data':response_status_chat_list,'message':'success','code':'SCOC002'},'status_Code':200,'messageER':response_result}),200
                                # else:
                                return jsonify({'result':'OK','messageText':{'data':response_status_chat_list,'message':'success','code':'SCOC001'},'status_Code':200,'messageER':[]}),200
                            else:
                                return jsonify({'result':'OK','messageText':{'data':'group document','message':'success','code':'SCOC000'},'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':result_message['messageText'],'message':'success','code':'EROC001'}}),200
                                # return jsonify({'result':'OK','messageText':{'data':result_message['messageText'],'message':'success','code':'SCOC002'},'status_Code':200,'messageER':response_result}),200
                # SCOC001 sccuess ทั้งหมด
                # SCOC002 มี fail อยู่บ้างส่วน รายละเอียดที่ messageER
                return jsonify({'result':'OK','messageText':{'data':result_message['messageText'],'message':'success','code':'SCOC001'},'status_Code':200,'messageER':[]}),200
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'exception ' + str(exc_type)}}),200


@status_methods.route('/api/v1/chat/chat_sender_group', methods=['POST'])
def chat_sender_group_api_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'group_id' in dataJson:
            try:
                group_id = dataJson['group_id']
                result_message = select().select_chat_group_v1(group_id)
                if result_message['result'] == 'OK':
                    tmpmessageText = result_message['messageText']
                    tmpsidcode = result_message['sidcode']
                    # print(tmpmessageText)
                    for n in range(len(tmpmessageText)):
                        tmpemailone = tmpmessageText[n]['emailone']
                        tmpstatus = tmpmessageText[n]['status']
                        if 'Incomplete' in tmpstatus:
                            # print(tmpemailone)
                            image_data = createImage_formPDF2(tmpsidcode)
                            if image_data['result'] == 'OK':
                                image_url_path = myUrl_domain + 'public/viewimage/' + image_data['data']
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error createImage pdf','data':None}}),200
                            type_chat = 'group'
                            tmp_task_btn_text = ['อนุมัติเอกสารทั้งหมด','อนุมัติบางเอกสาร']
                            tmp_body_text = ['เอกสาร','ใบปะหน้า']
                            tmp_button_text = ['อนุมัติเอกสารทั้งหมด','อนุมัติบางเอกสาร']
                            tmp_document_id = ''
                            hash_sidcode = hash_512_v2(str(tmpsidcode))
                            hash_groupid = hash_512_v2(str(group_id))
                            id_chat_bot = bot_id
                            token_chat_bot = token_service
                            tmp_email_one = tmpemailone[0]
                            tmp_user_id =''
                            result_get_userid = select().select_user_id_from_email_chat_v1(tmp_email_one)
                            if result_get_userid['result'] == 'OK':
                                tmp_user_id = result_get_userid['messageText']['user_id']
                            sendchat_result = send_chat_paperless_send_approve_v3_group('',tmp_task_btn_text,tmp_body_text,tmp_button_text,tmp_document_id,type_chat,hash_groupid,id_chat_bot,token_chat_bot,tmp_email_one,tmp_user_id,image_url_path,'',hash_sidcode)
                            # print(sendchat_result)
                            return jsonify({'result':'OK','messageText':{'data':'succuess','message':'success','code':'SCOC001'},'status_Code':200,'messageER':[]}),200

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'exception ' + str(exc_type)}}),200

@status_methods.route('/api/v1/chat/close_webview', methods=['POST','GET'])
@token_required
def close_webview_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'user_id' in dataJson and len(dataJson) == 1:
            tmp_user_id = dataJson['user_id']
            result_closewebView = close_webview_v1(tmp_user_id,token_header)
            if result_closewebView['result'] == 'OK':
                return jsonify({'result':'OK','messageText':[result_closewebView['messageText']],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_closewebView['msg']}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404

# @status_methods.route('/api/v9/<string:type_chat>/chat_sender', methods=['POST','GET'])

@status_methods.route('/public/v1/send_messageToChat_test',methods=['POST'])
def send_messageToChat_test():
    token_bot = token_bot_noti
    useridChat = useridChat_warning
    bot_chat_id = bot_chat_id_noti

    # time_sec = "{0:.2f}".format((time.time() - start_time))
    # time_millisec = int((time.time() - start_time)*1000)
    datajson = request.json
    if 'message' in datajson and len(datajson) == 1:
        message = datajson['message']
        try:
            headers = {
                'content-type': 'application/json',
                'Authorization':token_bot
            }
            data_Json = {
                "to": useridChat,
                "bot_id": bot_chat_id,
                "type": "text",
                "message": str(message)
            }
            
            r = requests.post(url_chat,json=data_Json,headers=headers,verify=True, cert=('cert/oneid.cer', 'cert/oneid.key'))
            # print ('RRRRRRRRRRRRRRRRRRr',r.json())
            if r.status_code == 200 or r.status_code == 201:
                return r.json()
            else:
                error_except(r.status_code,str((r.json())['message']),'service oneChat',r.status_code)
                return r.json()
        except requests.Timeout as ex:
            error_except(ex,"Timeout ",'service oneChat',r.status_code)
            return {'result':'ER','msg':'Timeout ' + str(ex)}
        except requests.HTTPError as ex:
            error_except(ex,"HTTPError ",'service oneChat',r.status_code)
            return {'result':'ER','msg':'HTTPError ' + str(ex)}
        except requests.ConnectionError as ex:
            error_except(ex,"ConnectionError ",'service oneChat',r.status_code)
            return {'result':'ER','msg':'ConnectionError ' + str(ex)}
        except requests.RequestException as ex:
            error_except(ex,"RequestException ",'service oneChat',r.status_code)
            return {'result':'ER','msg':'RequestException ' + str(ex)}
        except Exception as ex:
            error_except('ER',str(ex),'service oneChat',r.status_code)
            return {'result':'ER','msg':ex}