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
from db.db_method_4 import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *



if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

@status_methods.route('/api/v1/send_to_mail', methods=['POST'])
def sendmail_to_other():
    if request.method == 'POST':
        dataJson = request.json
        if 'to_email' in dataJson and 'sender_email' in dataJson and 'to_subject' in dataJson and 'to_message' in dataJson and 'sid_code' in dataJson and len(dataJson) == 5:
            to_email = dataJson['to_email']
            sender_email = dataJson['sender_email']
            to_subject = dataJson['to_subject']
            to_message = dataJson['to_message']
            sid_code = dataJson['sid_code']
            result_mail = mail().send_to_email(to_email,sender_email,to_subject,to_message,sid_code)
            if result_mail['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'send email to ' + to_email,'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':result_mail['messageER'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':'parameter incorrct','status_Code':200}),200

@status_methods.route('/api/v2/send_to_mail', methods=['POST'])
def sendmail_to_other_v2():
    if request.method == 'POST':
        dataJson = request.json
        if 'to_email' in dataJson and 'sender_email' in dataJson and 'to_subject' in dataJson and 'to_message' in dataJson and 'sid_code' in dataJson and len(dataJson) == 5:
            to_email = dataJson['to_email']
            sender_email = dataJson['sender_email']
            to_subject = dataJson['to_subject']
            to_message = dataJson['to_message']
            sid_code = dataJson['sid_code']
            arr_result = []
            for x in range(len(to_email)):
                tmpEmail = to_email[x]
                result_mail = mail().send_to_email(tmpEmail,sender_email,to_subject,to_message,sid_code)
                if result_mail['result'] == 'OK':
                    arr_result.append({'email':tmpEmail,'status':'success'})
                else:
                    arr_result.append({'email':tmpEmail,'status':'fail'})
            return jsonify({'result':'OK','messageText':{'message':'success','data':arr_result},'messageER':None,'status_Code':200}),200
        else:
            abort(404)

@status_methods.route('/api/mail/v1',methods=['POST'])
@token_required_v3
def send_Mailv1():
    if request.method == 'POST':
        dataJson = request.json
        result_list = []
        if 'type_service' in dataJson:
            if dataJson['type_service'].lower() == 'first':
                if 'sid' in dataJson and 'tracking' in dataJson and 'name_file' in dataJson and 'data' in dataJson:
                    for i in range(len(dataJson['data'])):
                        if dataJson['data'][i]['step_num'] == "1":
                            # result_Email = mail().check_EmailProfile(dataJson['data'][i]['email'])
                            # if result_Email['result'] == 'OK':
                            #     if 'statusEmail' in result_Email['messageText']:
                            #         if result_Email['messageText']['statusEmail'] == True:
                            #             dataJson['data'][i]['emailUser'] = result_Email['messageText']['emailUser']
                            #             result_mailStatus = mail().send_email(dataJson['data'][i],dataJson['sid'])
                            # else:
                            dataJson['data'][i]['emailUser'] = dataJson['data'][i]['email']
                            result_mailStatus = mail().send_email(dataJson['data'][i],dataJson['sid'])
                            if result_mailStatus['result'] == 'OK':
                                result_list.append({'result':'OK','email':dataJson['data'][i]['email'],'sid':dataJson['sid'],'step_num':dataJson['data'][i]['step_num'],'urlSign':dataJson['data'][i]['url_sign']})
                            else:
                                result_list.append({'result':'ER','email':dataJson['data'][i]['email'],'sid':dataJson['sid'],'step_num':dataJson['data'][i]['step_num'],'urlSign':dataJson['data'][i]['url_sign']})
                        else:
                            result_list.append({'result':'NO','email':dataJson['data'][i]['email'],'sid':dataJson['sid'],'step_num':dataJson['data'][i]['step_num'],'urlSign':dataJson['data'][i]['url_sign']})
                    result_insertMail = mail().insert_logEmail(result_list)
                    if result_insertMail['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':'Send To Email Successfully!','status_Code':200,'messageER':None})
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insertMail['messageText']})
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'param fail'})
            elif dataJson['type_service'].lower() == 'next':
                value_sid = dataJson['sid']
                result_MailTransaction = mail().select_transactionMail(dataJson['sid'])
                result_MailCheck = mail().check_sendToMail(result_MailTransaction)
                result_Array = []
                logmail_list = []
                for i in range(len(result_MailTransaction)):
                    if result_MailTransaction[i]['statusSign'] == 'Y':
                        result_MailTransaction[i]['statusSign'] = 'Complete'
                    else:
                        result_MailTransaction[i]['statusSign'] = 'Incomplete'
                    result_Array.append({
                        'emailUser':result_MailTransaction[i]['email_User'],
                        'statusSign':result_MailTransaction[i]['statusSign'],
                        'stepNum':int(result_MailTransaction[i]['stepNum']),
                        'datetime_string':result_MailTransaction[i]['datetime_string']
                    })
                if result_MailCheck['result'] == 'OK':
                    try:
                        if str(result_MailCheck['msg']).replace(' ','') != '':
                            print(result_MailCheck)
                            arr_tc = select().select_transactioneMail_next(result_MailCheck)
                            print(arr_tc)
                        else:
                            return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':None})
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found DATA!'})
                for k in arr_tc:
                    json_nextEmail = {}
                    result_Email = mail().check_EmailProfile(k['email_User'])
                    print(k)
                    if result_Email['result'] == 'OK':
                        json_nextEmail = {'email':result_Email['messageText']['emailUser'],'url_sign':k['urlSign'],'tracking':dataJson['tracking'],'name_file':dataJson['name_file'],'message':'','step_num':k['stepNum']}
                        result_sendMailAuto = mail().send_email_next(json_nextEmail,value_sid)
                        if result_sendMailAuto['result'] == 'OK':
                            logmail_list.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                        else:
                            logmail_list.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                    else:
                        json_nextEmail = {'email':k['email_User'],'url_sign':k['urlSign'],'tracking':dataJson['tracking'],'name_file':dataJson['name_file'],'message':'','step_num':k['stepNum']}
                        result_sendMailAuto = mail().send_email_next(json_nextEmail,value_sid)
                        if result_sendMailAuto['result'] == 'OK':
                            logmail_list.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                        else:
                            logmail_list.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                # print(logmail_list, ' logmail_list')
                if len(logmail_list) != 0:
                    result_updateEmail = update().update_SendToMail_(logmail_list)
                    print(result_updateEmail)
                else:
                    res_select = select().select_ForWebHook(value_sid)
                    res_select['messageText']['PDF_String'] = None
                    # print(res_select, ' res_select')
                    arr_step = []
                    result_Array = sorted(result_Array, key=lambda k: k['stepNum'], reverse=False)
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
                    msg_toChat = ''
                    print(result_Array)
                    
                    for n in arr_step:
                        msg_toChat += '<br>ลำดับที่ ' + str(n)
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
                               msg_toChat += '<br>- ' + email_User +'  ' + statusSign + ''
                    logger.info(res_select)
                    if res_select['result'] == 'OK':
                        logger.info('email success')
                        logger.info(msg_toChat)
                        # print(res_select['messageText'])
                        try:
                            email_list = eval(res_select['messageText']['email_center'])
                        except Exception as e:
                            email_list = (res_select['messageText']['email_center'])
                        logger.info(email_list)
                        if type(email_list) is list:
                            for zemail in range(len(email_list)):
                                email_center_01 = email_list[zemail]['email']
                                attemp_file = email_list[zemail]['attemp_file']
                                file_pdf = email_list[zemail]['file_pdf']
                                result_email_center = mail().send_emailSend_emailcenter_list(email_center_01,value_sid,msg_toChat,attemp_file,file_pdf)
                        else:
                            print(res_select['messageText']['email_center'])
                            result_email_center = mail().send_emailSend_emailcenter(res_select['messageText']['email_center'],value_sid,msg_toChat)
                            print(result_email_center)
                        # email_center_01 = email_list['email']
                        
                        result_Email = mail().check_EmailProfile(res_select['messageText']['emailSender'])
                        if result_Email['result'] == 'OK':
                            emailsender = result_Email['messageText']['emailUser']
                            resultSenderMail = mail().send_emailSender(emailsender,value_sid,msg_toChat)
                            if resultSenderMail['result'] == 'OK':
                                return jsonify({'result':'OK','messageText':'sender mail ok ' + emailsender,'status_Code':200,'messageER':None})
                            else:
                                return jsonify({'result':'OK','messageText':'sender mail fail ' + emailsender,'status_Code':200,'messageER':None})
                        else:
                            emailsender = res_select['messageText']['emailSender']
                            resultSenderMail = mail().send_emailSender(emailsender,value_sid,msg_toChat)
                            if resultSenderMail['result'] == 'OK':
                                return jsonify({'result':'OK','messageText':'sender mail ok ' + emailsender,'status_Code':200,'messageER':None})
                            else:
                                return jsonify({'result':'OK','messageText':'sender mail fail ' + emailsender,'status_Code':200,'messageER':None})
                return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':None})

@status_methods.route('/api/v2/mail',methods=['POST'])
@token_required_v3
def send_Mailv2():
    if request.method == 'POST':
        dataJson = request.json
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
            result_message = select_4().select_chat_sender_v1(sidcode)
            tmp_u = 0
            tmp_statusEmail = False
            if result_message['result'] == 'OK':
                tmp_messageText = result_message['data']
                tmp_tracking = tmp_messageText['tracking_id']
                tmp_name_file = tmp_messageText['filename']
                tmp_document_id = tmp_messageText['document_id']
                tmp_data = result_message['messageText']
                for u in range(len(tmp_data)):
                    tmp_status_ppl = tmp_data[u]['status_ppl']
                    tmp_email = tmp_data[u]['email']
                    if 'Reject' in tmp_status_ppl:
                        tmp_get_message = result_message['data']
                        tmp_document_id = tmp_get_message['document_id']
                        tmp_sender_email = tmp_get_message['sender_email']
                        tmp_sender_name = tmp_get_message['sender_name']
                        email_sender = mail().check_EmailProfile(tmp_sender_email)
                        tmp_statusEmail = email_sender['messageText']['statusEmail'] 
                        if email_sender['result'] == 'OK':
                            tmp_sender_email = email_sender['messageText']['emailUser']
                        if tmp_statusEmail == True:
                            result_message_text = select().select_mail_sender_v1_text(sidcode,tmp_document_id)
                            tmpmessage = result_message_text['messageText']
                            result_sendemail_sender = mail().send_emailSender(tmp_sender_email,sidcode,tmpmessage)
                        return jsonify({'result':'OK','messageText':{'message':'document reject','data':None},'messageER':None,'status_Code':200}),200
                    elif 'Complete' in tmp_status_ppl or 'Approve' in tmp_status_ppl:
                        tmp_u = u + 1
                        print(tmp_u,len(tmp_data))
                        if tmp_u == len(tmp_data):
                            tmp_statusEmail = False
                            document_type = tmp_document_id.split('-')[0]
                            result_message_text = select().select_mail_sender_v1_text(sidcode,tmp_document_id)
                            tmpmessage = result_message_text['messageText']
                            res_select = select().select_ForWebHook(sidcode)
                            if 'messageText' in res_select:
                                if 'PDF_String' in res_select['messageText']:
                                    res_select['messageText']['PDF_String'] = None
                            try:
                                email_list = eval(res_select['messageText']['email_center'])
                            except Exception as e:
                                email_list = (res_select['messageText']['email_center'])
                            if type(email_list) is list:
                                s_email = []
                                for zemail in range(len(email_list)):
                                    email_center_01 = email_list[zemail]['email']
                                    attemp_file = email_list[zemail]['attemp_file']
                                    file_pdf = email_list[zemail]['file_pdf']
                                    s_email.append(email_center_01)
                                result_email_center = mail().send_emailSend_emailcenter_list_v2([sidcode],email_list,document_type)
                            else:
                                result_email_center = mail().send_emailSend_emailcenter(res_select['messageText']['email_center'],sidcode,tmpmessage)
                                tmp_get_message = result_message['data']
                                tmp_document_id = tmp_get_message['document_id']
                                tmp_sender_email = tmp_get_message['sender_email']
                                tmp_sender_name = tmp_get_message['sender_name']
                                email_sender = mail().check_EmailProfile(tmp_sender_email)
                                tmp_statusEmail = email_sender['messageText']['statusEmail']
                                if email_sender['result'] == 'OK':
                                    tmp_sender_email = email_sender['messageText']['emailUser']
                                if tmp_statusEmail == True:
                                    tmpmessage = result_message_text['messageText']
                                    result_sendemail_sender = mail().send_emailSender(tmp_sender_email,sidcode,tmpmessage)
                        # return jsonify({'result':'OK','messageText':{'message':'document succuess','data':None},'messageER':None,'status_Code':200}),200
                    else:
                        tmp_statusEmail = False
                        tmp_url = None
                        for z in range(len(tmp_email)):
                            result_Url = select().select_geturl(tmp_email[z],sidcode)
                            if result_Url['result'] == 'OK':
                                tmp_url = result_Url['messageText']
                            email_profile = mail().check_EmailProfile(tmp_email[z])
                            tmp_statusEmail = email_profile['messageText']['statusEmail'] 
                            if email_profile['result'] == 'OK':
                                tmp_messageText = email_profile['messageText']
                                tmp_email[z] = tmp_messageText['emailUser']
                            if tmp_statusEmail == True:
                                result_mailStatus = mail().send_email_v2(tmp_email[z],tmp_tracking,tmp_name_file,'',tmp_url, sidcode)
                                if result_mailStatus['result'] == 'OK':
                                    print(result_mailStatus)
                        result_message_text = select().select_mail_sender_v1_text(sidcode,tmp_document_id)
                        tmp_get_message = result_message['data']
                        tmp_document_id = tmp_get_message['document_id']
                        tmp_sender_email = tmp_get_message['sender_email']
                        tmp_sender_name = tmp_get_message['sender_name']
                        email_sender = mail().check_EmailProfile(tmp_sender_email)
                        tmp_statusEmail = email_sender['messageText']['statusEmail'] 
                        if email_sender['result'] == 'OK':
                            tmp_sender_email = email_sender['messageText']['emailUser']
                        if tmp_statusEmail == True:                                
                            result_message_text = select().select_mail_sender_v1_text(sidcode,tmp_document_id)
                            tmpmessage = result_message_text['messageText']
                            result_sendemail_sender = mail().send_emailSender(tmp_sender_email,sidcode,tmpmessage)
                        return jsonify({'result':'OK','messageText':{'message':'send email succuess','data':None},'messageER':None,'status_Code':200}),200                    
            return jsonify({'result':'OK','messageText':{'message':'send email succuess','data':None},'messageER':None,'status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'exception ' + str(exc_type)}}),200
        
