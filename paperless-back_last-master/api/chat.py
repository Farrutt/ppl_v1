#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

def thread_change_state_onechat_v1(tmp_task_id,token_chat_bot,id_chat_bot,token_header):
    for nz in range(len(tmp_task_id)):
        one_task_id = tmp_task_id[nz][0]
        r = sendtask_change_stateChat_v4(one_task_id,token_chat_bot,id_chat_bot,token_header)

def thread_disble_button_onechat_v1(tmp_chat_id,token_chat_bot,tmp_id_chat_one_dis,id_chat_bot,token_header):
    for z in range(len(tmp_chat_id)):
        tmp_id_chat_one_dis = tmp_chat_id[z]
        r = disble_button_in_oneChat_v5(id_chat_bot,token_chat_bot,tmp_id_chat_one_dis,token_header)


def chat_sender_group_v2(group_id,email):
    try:
        group_id = group_id
        result_message = select_1().select_chat_group_v2(group_id)
        if result_message['result'] == 'OK':
            tmpmessageText = result_message['messageText']
            tmpsidcode = result_message['sidcode']
            for n in range(len(tmpmessageText)):
                tmpemailone = tmpmessageText[n]['emailone']
                tmpstatus = tmpmessageText[n]['status']
                if 'Incomplete' in tmpstatus:                    
                    image_url_path = 'https://www.img.in.th/images/83ca9b38ee2d7d129f1826f75ea05e4f.png'
                    # image_data = createImage_formPDF2(tmpsidcode)
                    # if image_data['result'] == 'OK':
                    #     image_url_path = myUrl_domain + 'public/viewimage/' + image_data['data']
                    # else:
                    #     return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error createImage pdf','data':None}}),200
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
                    if email != None:
                        tmp_email_one = email
                    else:
                        tmp_email_one = tmpemailone[0]
                    if type(tmp_email_one) is list:
                        for z in range(len(tmp_email_one)):
                            oneemail = tmp_email_one[z]
                            tmp_user_id =''
                            result_get_userid = select().select_user_id_from_email_chat_v1(oneemail)
                            if result_get_userid['result'] == 'OK':
                                tmp_user_id = result_get_userid['messageText']['user_id']
                            if tmp_user_id == None:
                                tmp_user_id = oneemail
                            tmp_email_one = (tmp_user_id)
                            sendchat_result = send_chat_paperless_send_approve_v3_group('',tmp_task_btn_text,tmp_body_text,tmp_button_text,tmp_document_id,type_chat,hash_groupid,id_chat_bot,token_chat_bot,tmp_email_one,tmp_user_id,image_url_path,'',hash_sidcode)
                    else:
                        tmp_user_id =''
                        result_get_userid = select().select_user_id_from_email_chat_v1(tmp_email_one)
                        if result_get_userid['result'] == 'OK':
                            tmp_user_id = result_get_userid['messageText']['user_id']
                        if tmp_user_id == None:
                            tmp_user_id = tmp_email_one
                        tmp_email_one = (tmp_user_id)
                        sendchat_result = send_chat_paperless_send_approve_v3_group('',tmp_task_btn_text,tmp_body_text,tmp_button_text,tmp_document_id,type_chat,hash_groupid,id_chat_bot,token_chat_bot,tmp_email_one,tmp_user_id,image_url_path,'',hash_sidcode)

                    return jsonify({'result':'OK','messageText':{'data':'succuess','message':'success','code':'SCOC001'},'status_Code':200,'messageER':[]}),200

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'exception ' + str(exc_type)}}),200

def search_frd(key_search,token_header):
    try:
        url = url_frd
        payload = "{\n    \"bot_id\": \"" + bot_id + "\",\n    \"key_search\": \"" + key_search +"\"\n}"
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_service
        }

        response = requests.request("POST", url_frd, data=payload, headers=headers,verify=False)
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url_frd,token_header)
            return response.json()
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url_frd,token_header)
            return response.json()
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_frd,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_frd,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_frd,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_frd,token_header)
        return {'result':'ER','msg':ex}

def search_frd_v2(bot_id,key_search,token_service,token_header):
    try:
        url = url_frd
        payload = {
            "bot_id": bot_id,
            "key_search": key_search
        }
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_service
        }

        response = requests.request("POST", url_frd, json=payload, headers=headers,verify=False,timeout=5)
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url_frd,token_header)
            return response.json()
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url_frd,token_header)
            return response.json()
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_frd,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_frd,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_frd,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_frd,token_header)
        return {'result':'ER','msg':ex}

def send_url_sign(data_To,nameFile,Treacking_num,url_link):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        r = requests.post(url_chat,json={
                "to": data_To,
                "bot_id": bot_id,
                "type": "template",
                "elements" : [
                {
                    "image" : "https://lh3.googleusercontent.com/W1Jwfw3dKIo8BsQFaLc0y4UflpgSUlDKiWn4LgjKXFW1Uxj1t8qfwYu987CnBDWdsENT",
                    "title" : "Plase Sign",
                    "detail" : "ชื่อไฟล์ " + nameFile + " \n" + "หมายเลข Tracking " + Treacking_num ,
                    "choice" : [
                                    {
                                        "label" : "ลงลายเซ็น",
                                        "type" : "link",
                                        "url" : url_link
                                    }
                                ]
                }
            ]
        },headers=headers,verify=False)
        # "upload_to_box":{"service":"e-tax","type":"bot_file"} for file to onebox
        r.raise_for_status()
        return r.json()
    except requests.Timeout as ex:
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        return {'result':'ER','msg':ex}

def send_url_tochat(typeChat,data_To,nameFile,Treacking_num,url_link,sidCode,resouce_result=None):
    try:
        if typeChat == 'signning':
            title_Chat = 'please sign'
            type_label = 'ลงนามอนุมัติ'
        elif typeChat == 'approve':
            title_Chat = 'please approve'
            type_label = 'ลงนามอนุมัติ'
        elif typeChat == None:
            title_Chat = 'please sign'
            type_label = 'ลงนามอนุมัติ'
        hash_sid = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
        if resouce_result != None:
            title_Chat = resouce_result['documentName']
            sender_name = resouce_result['name_sender']
        else:
            title_Chat = ''
            sender_name = ''
        details_message = 'โดย ' + sender_name
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        url_topaperless = myUrl_domain2 + '?type=' + typeChat +'&sumpage=' + hash_sid +'&page='
        r = requests.post(url_chat,json={
                "to": data_To,
                "bot_id": bot_id,
                "type": "template",
                "elements" : [
                {
                    "image" : "",
                    "title" : title_Chat,
                    "detail" : details_message + '\n' + 'แผนก ' ,
                    "choice" : [
                                    {
                                        "label" : type_label,
                                        "type" : "link",
                                        "url" : url_topaperless,
                                        "sign":"true"
                                    }
                                ]
                }
            ]
        },headers=headers,verify=False)
        # "upload_to_box":{"service":"e-tax","type":"bot_file"} for file to onebox
        r.raise_for_status()
        return r.json()
    except requests.Timeout as ex:
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        return {'result':'ER','msg':ex}

def send_url_tochat_next(typeChat,data_To,nameFile,Treacking_num,url_link,transactionCode,sidCode):

    try:
        if typeChat == 'signning':
            title_Chat = 'please sign'
            type_label = 'ลงนามอนุมัติ'
        elif typeChat == 'approve':
            title_Chat = 'please approve'
            type_label = 'ลงนามอนุมัติ'
        hash_sid = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        url_topaperless = myUrl_domain2 + '?type=' + typeChat +'&sumpage=' + hash_sid +'&page='
        r = requests.post(url_chat,json={
                "to": data_To,
                "bot_id": bot_id,
                "type": "template",
                "elements" : [
                {
                    "image" : "",
                    "title" : title_Chat,
                    "detail" : "" + nameFile + "\n" + "เลขที่ติดตามสถานะเอกสาร " + Treacking_num ,
                    "choice" : [
                                    {
                                        "label" : type_label,
                                        "type" : "link",
                                        "url" : url_topaperless,
                                        "sign":"true"
                                    }
                                ]
                }
            ]
        },headers=headers,verify=False)
        # "upload_to_box":{"service":"e-tax","type":"bot_file"} for file to onebox
        r.raise_for_status()
        return r.json()
    except requests.Timeout as ex:
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        return {'result':'ER','msg':ex}

def send_url_tochat_next_new_v1(typeChat,data_To,nameFile,Treacking_num,url_link,transactionCode,sidCode,resouce_result=None,imgURL=None):

    try:
        if typeChat == 'signning':
            title_Chat = 'please sign'
            type_label = 'ลงนามอนุมัติ'
        elif typeChat == 'approve':
            title_Chat = 'please approve'
            type_label = 'ลงนามอนุมัติ'
        hash_sid = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
        if resouce_result != None:
            title_Chat = ''
            if resouce_result['documentName'] != None:
                title_Chat = resouce_result['documentName']
            if resouce_result['name_sender'] != None:
                sender_name = resouce_result['name_sender']
        else:
            title_Chat = ''
            sender_name = ''
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        details_message = 'โดย ' + sender_name
        url_topaperless = myUrl_domain2 + '?type=' + typeChat +'&sumpage=' + hash_sid +'&page='
        url_topaperless_approve = myUrl_toChat + '?type=' + typeChat +'&action=approve&sumpage=' + hash_sid +'&page='
        url_topaperless_reject = myUrl_toChat + '?type=' + typeChat +'&action=reject&sumpage=' + hash_sid +'&page='
        url_viewPdf =  myUrl_toViewPDF_toChat + '?sumpage=' + hash_sid
        r = requests.post(url_chat,json={
                "to": data_To,
                "bot_id": bot_id,
                "type": "official_template",
                "detail": details_message,
                "title":title_Chat,
                "image": imgURL,
                "onclick_img": {
                    "type": "link",
                    "size":"full",
                    "url": url_viewPdf
                },
                "choice": [
                    {
                        "label": "ลงนามอนุมัติ",
                        "type": "webview",
                        "url": url_topaperless_approve,
                        "size" : "compact",
                        "color": "#ffffff",
                        "background": "#4268fb",
                        "sign": "true"
                    },
                    {
                        "label": "ปฏิเสธการลงนาม",
                        "type": "webview",
                        "size" : "full",
                        "url": url_topaperless_reject,
                        "color": "#dd6262",
                        "background": "",
                        "sign": "true"
                    }
                ]
        },headers=headers,verify=False)
        # "upload_to_box":{"service":"e-tax","type":"bot_file"} for file to onebox
        r.raise_for_status()

        return r.json()
    except requests.Timeout as ex:
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        return {'result':'ER','msg':ex}

def send_messageToChat(message,useridChat):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        data_Json = {
            "to": useridChat,
            "bot_id": bot_id,
            "type": "text",
            "message": message
        }
        r = requests.post(url_chat,json=data_Json,headers=headers,verify=False)
        print(r.json())
        r.raise_for_status()
        return r.json()
    except requests.Timeout as ex:
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        return {'result':'ER','msg':ex}

def send_message_Onechat(token_service,useridChat,bot_id,message,custom_notification):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        data_Json = {
            "to": useridChat,
            "bot_id": bot_id,
            "type": "text",
            "message": message,
            "custom_notification" : custom_notification
        }
        r = requests.post(url_chat,json=data_Json,headers=headers,verify=False)
        print(r.json())
        r.raise_for_status()
        return r.json()
    except requests.Timeout as ex:
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        return {'result':'ER','msg':ex}

def send_messageToChat_v3(message,useridChat,token_bot,bot_chat_id,token_header):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_bot
        }
        data_Json = {
            "to": useridChat,
            "bot_id": bot_chat_id,
            "type": "text",
            "message": message
        }
        r = requests.post(url_chat,json=data_Json,headers=headers,verify=False)
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(data_Json),url_chat,token_header)
            return r.json()
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(data_Json),url_chat,token_header)
            return r.json()
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header)
        return {'result':'ER','msg':ex}

def send_messageToChat_v4(message,useridChat,token_bot,bot_chat_id,token_header):
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
        time_duration = ''
        r = requests.post(url_chat,json=data_Json,headers=headers,verify=False,timeout=10)
        time_duration = str(int(r.elapsed.total_seconds() * 1000))
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(data_Json),url_chat,token_header,time_duration)
            return r.json()
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(data_Json),url_chat,token_header,time_duration)
            return r.json()
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header,time_duration)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header,time_duration)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header,time_duration)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header,time_duration)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header,time_duration)
        return {'result':'ER','msg':ex}

def send_messageToChat_v5(message,useridChat,token_bot,bot_chat_id,token_header):
    try:
        list_assign_tmp = []
        list_assign_tmp.append(useridChat)
        task_btn_text = ['View Detail']
        type_chat = 'approve'
        label_button_1 = 'More detail..'
        bio_authen = 'false'
        str_body = 'เอกสารค้างอนุมัติ'
        priority_ = "1"
        ts_start = int(time.time())
        ts_end = int(time.time()) + 259200
        st_time_start = datetime.datetime.fromtimestamp(ts_start).strftime('%Y-%m-%d %H:%M:%S')
        st_time_end = datetime.datetime.fromtimestamp(ts_end).strftime('%Y-%m-%d %H:%M:%S')
   
        # url_topaperless = myUrl_domain2 + '?type=' + type_chat +'&sumpage=' + hash_sid +'&page='
        url_topaperless_approve = myUrl_toChat + '?type=' + type_chat +'&action=approve&sumpage='
        # url_topaperless_reject = myUrl_toChat + '?type=' + type_chat +'&action=reject&sumpage=' + hash_sid +'&page='
        # url_viewPdf =  myUrl_toViewPDF_toChat + '?sumpage=' + hash_sid
        url_topaperless_approve_task = myUrl_toTaskChat + '?type=' + type_chat +'&action=approve&sumpage=' 
        url_more_details_w = myUrl_domain2 + '?filter_type=W&page='
        headers = {
            'content-type': 'application/json',
            'Authorization':token_bot
        }
        data_Json = {
            "bot_id": bot_chat_id,
            "to": useridChat,
            "custom_notification":"เอกสารค้างรออนุมัติ", 
            # "ref":[],
            "official_template_info": {
                "type": "official_template",
                "detail": message,
                "title": 'แจ้งเตือน',
                "image": '',
                "onclick_img": {
                    "sign": "true",
                    "type": "webview",
                    "size": "full",
                    "url": url_topaperless_approve_task
                },
                "choice": [
                    {
                        "label": label_button_1,
                        "bio_authen":bio_authen,
                        "type": "webview",
                        "url": url_more_details_w,
                        "size": "full",
                        "color": "#000000",
                        # "background": "#4268fb",
                        "sign": "true"
                    }
            ]
        },
            "task_info": {
                "priority": priority_,
                "title": '',
                "task_message":"0",
                "detail": str_body,
                "time_start": st_time_start,
                "time_end": st_time_end,
                "assign": list_assign_tmp,
                "sign_info": {
                    "type": "webview",
                    "size": "full",
                    "label": task_btn_text[0],
                    "url": url_topaperless_approve_task,
                    "sign": "true"
                }
            }
        }
        url = url_oneChat + '/api/v1/paperless_send_approve'    
        time_duration = ''
        r = requests.post(url,json=data_Json,headers=headers,verify=False,timeout=10)
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(data_Json),url_chat,token_header)
            return r.json()
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(data_Json),url_chat,token_header)
            return r.json()
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url_chat,token_header)
        return {'result':'ER','msg':ex}

def addbot_tofrdAUto(email):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service_autoAdd
        }
        data_Json = {
            "email_one": email,
            "bot_id": bot_id
        }
        url = url_onechat_1 + '/api/v2/addfriendmulti'
        r = requests.post(url,json=data_Json,headers=headers,verify=False,timeout=10)
        # logger.info(url_addfrdAuto)
        logger.info(r)
        logger.info(r.text)
        # if r.status_code == 200 or r.status_code == 201:
        #     insert().insert_tran_log_v1(str(r.json()),'OK',str(dataJson),url,token_header)
        #     return {'result':'OK','messageText':r.json()}
        # else:
        #     insert().insert_tran_log_v1(str(r.text),'ER',str(dataJson),url,token_header)
        #     return {'result':'ER','msg':'message ' + str(r.text)}
        return r.json()
    except requests.Timeout as ex:
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        return {'result':'ER','msg':ex}

def disble_button_in_oneChat_v1(msg_id_chatid):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        # print(msg_id_chatid,bot_id)
        r = requests.post(url_disble_template,json={
            "message_id":msg_id_chatid,
            "target_index":"0",
            "bot_id":bot_id
        },headers=headers,verify=False)
        # "upload_to_box":{"service":"e-tax","type":"bot_file"} for file to onebox
        r = r.json()
        return {'result':'OK','messageText':r}
    except requests.Timeout as ex:
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        return {'result':'ER','msg':ex}

def disble_button_in_oneChat_v2(msg_id_chatid,count_button,token_header):
    for i in range(count_button):
        try:
            headers = {
                'content-type': 'application/json',
                'Authorization':token_service
            }
            # print(msg_id_chatid,bot_id)
            datajson = {
                "message_id":msg_id_chatid,
                "target_index":str(i),
                "bot_id":bot_id
            }
            r = requests.post(url_disble_template,json=datajson,headers=headers,verify=False)
            # "upload_to_box":{"service":"e-tax","type":"bot_file"} for file to onebox
            # print(r.json())
            # r = r.json()
            # return {'result':'OK','messageText':r}
            insert().insert_tran_log_v1(str(r.json()),'OK',str(datajson),url_disble_template,token_header)
        except requests.Timeout as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_disble_template,token_header)
            return {'result':'ER','msg':'Timeout ' + str(ex)}
        except requests.HTTPError as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_disble_template,token_header)
            return {'result':'ER','msg':'HTTPError ' + str(ex)}
        except requests.ConnectionError as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_disble_template,token_header)
            return {'result':'ER','msg':'ConnectionError ' + str(ex)}
        except requests.RequestException as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_disble_template,token_header)
            return {'result':'ER','msg':'RequestException ' + str(ex)}
        except Exception as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_disble_template,token_header)
            return {'result':'ER','msg':ex}

def disble_button_in_oneChat_v3(bot_id,token_service,msg_id_chatid,token_header):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        # print(msg_id_chatid,bot_id)
        datajson = {
            "message_id":msg_id_chatid,
            "target_index":["0","1"],
            "bot_id":bot_id
        }
        url = url_oneChat + '/api/v2/bot_disable_template'
        r = requests.post(url,json=datajson,headers=headers,verify=False,timeout=10)
        insert().insert_tran_log_v1(str(r.json()),'OK',str(datajson),url,token_header)
        print(r.text)
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':ex}

def disble_button_in_oneChat_v4(bot_id,token_service,msg_id_chatid,token_header):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        # print(msg_id_chatid,bot_id)
        datajson = {
            "bot_id":bot_id,
            "list_message_id":msg_id_chatid
        }
        url = url_oneChat + '/api/v3/bot_disable_template'
        r = requests.post(url,json=datajson,headers=headers,verify=False,timeout=10)
        insert().insert_tran_log_v1(str(r.json()),'OK',str(datajson),url,token_header)
        # print(r.text)
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':ex}

def disble_button_in_oneChat_v5(bot_id,token_service,list_official_id,token_header):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        # print(msg_id_chatid,bot_id)
        datajson = {
            "bot_id":bot_id,
            "list_official_id":list_official_id
        }

        # datajson = {
        #     "bot_id":bot_id,
        #     "list_message_id":msg_id_chatid
        # }
        time_duration = ''
        url = url_oneChat + '/api/v4/bot_disable_template'
        r = requests.post(url,json=datajson,headers=headers,verify=False,timeout=10)
        time_duration = str(int(r.elapsed.total_seconds() * 1000))
        insert().insert_tran_log_v1(str(r.json()),'OK',str(datajson),url,token_header,time_duration)
        # print(r.text)
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header,time_duration)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header,time_duration)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header,time_duration)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header,time_duration)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header,time_duration)
        return {'result':'ER','msg':ex}

def send_url_tochat_new_v2(typeChat,data_To,nameFile,Treacking_num,url_link,sidCode,resouce_result=None,imageURL=None,token_header=None):
    try:
        if typeChat == 'signning':
            title_Chat = 'please sign'
            type_label = 'ลงนามอนุมัติ'
        elif typeChat == 'approve':
            title_Chat = 'please approve'
            type_label = 'ลงนามอนุมัติ'
        elif typeChat == None:
            title_Chat = 'please sign'
            type_label = 'ลงนามอนุมัติ'
        hash_sid = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
        if resouce_result != None:
            title_Chat = ''
            if resouce_result['documentName'] != None:
                title_Chat = resouce_result['documentName']
            if resouce_result['name_sender'] != None:
                sender_name = resouce_result['name_sender']
        else:
            title_Chat = ''
            sender_name = ''
        details_message = 'โดย ' + sender_name
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        url_topaperless = myUrl_domain2 + '?type=' + typeChat +'&sumpage=' + hash_sid +'&page='
        url_topaperless_approve = myUrl_toChat + '?type=' + typeChat +'&action=approve&sumpage=' + hash_sid +'&page='
        url_topaperless_reject = myUrl_toChat + '?type=' + typeChat +'&action=reject&sumpage=' + hash_sid +'&page='
        url_viewPdf =  myUrl_toViewPDF_toChat + '?sumpage=' + hash_sid
        dataJson = {
                "to": data_To,
                "bot_id": bot_id,
                "type": "official_template",
                "detail": details_message,
                "title":title_Chat,
                "image": imageURL,
                "onclick_img": {
                    "type": "webview",
                    "size" : "full",
                    "url":url_viewPdf
                },
                "choice": [
                    {
                        "label": "ลงนามอนุมัติ",
                        "type": "webview",
                        "url": url_topaperless_approve,
                        "size" : "compact",
                        "color": "#ffffff",
                        "background": "#4268fb",
                        "sign": "true"
                    },
                    {
                        "label": "ปฏิเสธการลงนาม",
                        "type": "webview",
                        "size" : "full",
                        "url": url_topaperless_reject,
                        "color": "#dd6262",
                        "background": "",
                        "sign": "true"
                    }
                ]
        }
        r = requests.post(url_chat,json=dataJson,headers=headers,verify=False)
        # "upload_to_box":{"service":"e-tax","type":"bot_file"} for file to onebox
        insert().insert_tran_log_v1(str(r.json()),'OK',str(dataJson),url_chat,token_header)
        # insert().insert_tran_log_v1(str(r.json()),'OK',str(datajson),url_chat)
        r.raise_for_status()
        return r.json()
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url_chat,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url_chat,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url_chat,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url_chat,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url_chat,token_header)
        return {'result':'ER','msg':ex}

def send_url_tochat_new_v3(typeChat,data_To,nameFile,Treacking_num,url_link,sidCode,resouce_result=None,imageURL=None,token_header=None):
    try:
        time_duration = ''
        if typeChat == 'signning':
            title_Chat = 'please sign'
            type_label = 'ลงนามอนุมัติ'
        elif typeChat == 'approve':
            title_Chat = 'please approve'
            type_label = 'ลงนามอนุมัติ'
        elif typeChat == None:
            title_Chat = 'please sign'
            type_label = 'ลงนามอนุมัติ'
        hash_sid = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
        if resouce_result != None:
            title_Chat = ''
            if resouce_result['documentName'] != None:
                title_Chat = resouce_result['documentName']
            if resouce_result['name_sender'] != None:
                sender_name = resouce_result['name_sender']
        else:
            title_Chat = ''
            sender_name = ''
        details_message = 'โดย ' + sender_name
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        url_topaperless = myUrl_domain2 + '?type=' + typeChat +'&sumpage=' + hash_sid +'&page='
        url_topaperless_approve = myUrl_toChat + '?type=' + typeChat +'&action=approve&sumpage=' + hash_sid +'&page='
        url_topaperless_reject = myUrl_toChat + '?type=' + typeChat +'&action=reject&sumpage=' + hash_sid +'&page='
        url_viewPdf =  myUrl_toViewPDF_toChat + '?sumpage=' + hash_sid
        datajson = {
                "to": data_To,
                "bot_id": bot_id,
                "type": "official_template",
                "detail": details_message,
                "title":title_Chat,
                "image": imageURL,
                "onclick_img": {
                    "type": "webview",
                    "size" : "full",
                    "url":url_viewPdf
                },
                "choice": [
                    {
                        "label": "ลงนามอนุมัติ",
                        "type": "webview",
                        "url": url_topaperless_approve,
                        "size" : "compact",
                        "color": "#ffffff",
                        "background": "#4268fb",
                        "sign": "true"
                    },
                    {
                        "label": "ปฏิเสธการลงนาม",
                        "type": "webview",
                        "size" : "compact",
                        "url": url_topaperless_reject,
                        "color": "#dd6262",
                        "background": "",
                        "sign": "true"
                    }
                ]
        }
        r = requests.post(url_chat,json=datajson,headers=headers,verify=False,timeout=10)
        time_duration = str(int(r.elapsed.total_seconds() * 1000))
        # "upload_to_box":{"service":"e-tax","type":"bot_file"} for file to onebox
        # print(r.json())
        insert().insert_tran_log_v1(str(r.json()),'OK',str(datajson),url_chat,token_header,time_duration)
        r.raise_for_status()
        return r.json()
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_chat,token_header,time_duration)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_chat,token_header,time_duration)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_chat,token_header,time_duration)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_chat,token_header,time_duration)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_chat,token_header,time_duration)
        return {'result':'ER','msg':ex}

def chatstatus_forservice(data_Json):
    listdata = []
    jsondata = {}
    if 'step_num' in data_Json:
        value_stepDetails = data_Json['step_detail']
        for n in range(len(value_stepDetails)):
            print(value_stepDetails[n]['one_email'])
    else:
        print(data_Json)

def sendtask_getProject_tochat_v1(oneid_result,token_header):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        dataJson = {
            "bot_id": bot_id,
            "one_id": oneid_result
        }
        r = requests.post(Url_Bot_getProject,json=dataJson,headers=headers,verify=False)
        # "upload_to_box":{"service":"e-tax","type":"bot_file"} for file to onebox
        insert().insert_tran_log_v1(str(r.json()),'OK',str(dataJson),Url_Bot_getProject,token_header)
        r = r.json()
        return {'result':'OK','messageText':r}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),Url_Bot_getProject,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),Url_Bot_getProject,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),Url_Bot_getProject,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),Url_Bot_getProject,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),Url_Bot_getProject,token_header)
        return {'result':'ER','msg':ex}

def sendtask_getProject_tochat_v2(oneid_result):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        r = requests.post(Url_Bot_getProject,json={
            "bot_id": bot_id,
            "one_id": oneid_result
        },headers=headers,verify=False,timeout=10)
        r = r.json()
        return {'result':'OK','messageText':r}
    except requests.Timeout as ex:
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        return {'result':'ER','msg':ex}

def sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,typeChat,sidCode,user_id_one,token_header):
    try:
        user_id_one = str(user_id_one)
        ts_start = int(time.time())
        ts_end = int(time.time()) + 259200
        st_time_start = datetime.datetime.fromtimestamp(ts_start).strftime('%Y-%m-%d %H:%M:%S')
        st_time_end = datetime.datetime.fromtimestamp(ts_end).strftime('%Y-%m-%d %H:%M:%S')
        if titleAndDetails != None:
            title_Chat = ''
            if titleAndDetails['documentName'] != None:
                title_Chat = titleAndDetails['documentName']
            if titleAndDetails['name_sender'] != None:
                sender_name = titleAndDetails['name_sender']
        else:
            title_Chat = ''
            sender_name = ''
        details_message = 'โดย ' + sender_name
        hash_sid = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
        url_topaperless_approve = myUrl_toChat + '?type=' + typeChat +'&action=approve&sumpage=' + hash_sid +'&page='
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        data_json = {
            "bot_id":bot_id,
            "project_id":projectid_,
            "priority":priority_,
            "title":title_Chat,
            "detail":details_message,
            "state_id":state_id_,
            "time_start":st_time_start,
            "time_end":st_time_end,
            "assign":[user_id_one],
            "sign_info":{
                		"type":"webview",
                		"size":"compact",
                		"label":"ลงนามอนุมัติ",
                		"url":url_topaperless_approve,
                		"sign":"true"
        	       }


        }
        r = requests.post(Url_Bot_CreateTask,json=data_json,headers=headers,verify=False)
        print(data_json)
        insert().insert_tran_log_v1(str(r.json()),'OK',str(data_json),Url_Bot_CreateTask,token_header)
        # "upload_to_box":{"service":"e-tax","type":"bot_file"} for file to onebox
        r = r.json()
        return {'result':'OK','messageText':r}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_json),Url_Bot_CreateTask,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_json),Url_Bot_CreateTask,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_json),Url_Bot_CreateTask,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_json),Url_Bot_CreateTask,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_json),Url_Bot_CreateTask,token_header)
        return {'result':'ER','msg':ex}

def sendtask_creattask_tochat_v2(projectid_,priority_,titleAndDetails,state_id_,typeChat,sidCode,user_id_one):
    try:
        user_id_one = str(user_id_one)
        ts_start = int(time.time())
        ts_end = int(time.time()) + 259200
        st_time_start = datetime.datetime.fromtimestamp(ts_start).strftime('%Y-%m-%d %H:%M:%S')
        st_time_end = datetime.datetime.fromtimestamp(ts_end).strftime('%Y-%m-%d %H:%M:%S')
        if titleAndDetails != None:
            title_Chat = ''
            if titleAndDetails['documentName'] != None:
                title_Chat = titleAndDetails['documentName']
            if titleAndDetails['name_sender'] != None:
                sender_name = titleAndDetails['name_sender']
        else:
            title_Chat = ''
            sender_name = ''
        details_message = 'โดย ' + sender_name
        hash_sid = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
        url_topaperless_approve = myUrl_toChat + '?type=' + typeChat +'&action=approve&sumpage=' + hash_sid +'&page='
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        data_json = {
            "bot_id":bot_id,
            "project_id":projectid_,
            "priority":priority_,
            "title":title_Chat,
            "detail":details_message,
            "state_id":state_id_,
            "time_start":st_time_start,
            "time_end":st_time_end,
            "assign":[user_id_one],
            "sign_info":{
                		"type":"webview",
                		"size":"compact",
                		"label":"ลงนามอนุมัติ",
                		"url":url_topaperless_approve,
                		"sign":"true"
        	       }


        }
        r = requests.post(Url_Bot_CreateTask,json=data_json,headers=headers,verify=False)
        print(data_json)
        # "upload_to_box":{"service":"e-tax","type":"bot_file"} for file to onebox
        r = r.json()
        return {'result':'OK','messageText':r}
    except requests.Timeout as ex:
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        return {'result':'ER','msg':ex}

def sendtask_creattask_tochat_v3(projectid_,priority_,titleAndDetails,state_id_,typeChat,sidCode,user_id_one,id_bot_chat,token_bot_chat,token_header):
    try:
        user_id_one = str(user_id_one)
        ts_start = int(time.time())
        ts_end = int(time.time()) + 259200
        st_time_start = datetime.datetime.fromtimestamp(ts_start).strftime('%Y-%m-%d %H:%M:%S')
        st_time_end = datetime.datetime.fromtimestamp(ts_end).strftime('%Y-%m-%d %H:%M:%S')
        if titleAndDetails != None:
            title_Chat = ''
            if titleAndDetails['documentName'] != None:
                title_Chat = titleAndDetails['documentName']
            if titleAndDetails['name_sender'] != None:
                sender_name = titleAndDetails['name_sender']
        else:
            title_Chat = ''
            sender_name = ''
        details_message = 'โดย ' + sender_name
        hash_sid = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
        url_topaperless_approve = myUrl_toChat + '?type=' + typeChat +'&action=approve&sumpage=' + hash_sid +'&page='
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        data_json = {
            "bot_id":bot_id,
            "project_id":projectid_,
            "priority":priority_,
            "title":title_Chat,
            "detail":details_message,
            "state_id":state_id_,
            "time_start":st_time_start,
            "time_end":st_time_end,
            "assign":[user_id_one],
            "sign_info":{
                		"type":"webview",
                		"size":"compact",
                		"label":"ลงนามอนุมัติ",
                		"url":url_topaperless_approve,
                		"sign":"true"
        	       }


        }
        r = requests.post(Url_Bot_CreateTask,json=data_json,headers=headers,verify=False,timeout=10)
        print(data_json)
        insert().insert_tran_log_v1(str(r.json()),'OK',str(data_json),Url_Bot_CreateTask,token_header)
        # "upload_to_box":{"service":"e-tax","type":"bot_file"} for file to onebox
        r = r.json()
        return {'result':'OK','messageText':r}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_json),Url_Bot_CreateTask,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_json),Url_Bot_CreateTask,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_json),Url_Bot_CreateTask,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_json),Url_Bot_CreateTask,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_json),Url_Bot_CreateTask,token_header)
        return {'result':'ER','msg':ex}

def send_chat_paperless_send_approve_v1(typeChat,user_id_one,nameFile,Treacking_num,url_link,sidCode,projectid_,priority_,titleAndDetails,state_id_,resouce_result=None,imageURL=None,id_bot_chat=None,token_bot_chat=None,token_header=None):
    dataJson = {}
    url = ''
    try:
        list_assign_tmp = []
        list_assign_tmp.append(user_id_one)
        ts_start = int(time.time())
        ts_end = int(time.time()) + 259200
        st_time_start = datetime.datetime.fromtimestamp(ts_start).strftime('%Y-%m-%d %H:%M:%S')
        st_time_end = datetime.datetime.fromtimestamp(ts_end).strftime('%Y-%m-%d %H:%M:%S')
        if typeChat == 'signning':
            title_Chat = 'please sign'
            type_label = 'ลงนามอนุมัติ'
        elif typeChat == 'approve':
            title_Chat = 'please approve'
            type_label = 'ลงนามอนุมัติ'
        elif typeChat == None:
            title_Chat = 'please sign'
            type_label = 'ลงนามอนุมัติ'
        hash_sid = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
        if resouce_result != None:
            title_Chat = ''
            if resouce_result['documentName'] != None:
                title_Chat = resouce_result['documentName']
            if resouce_result['name_sender'] != None:
                sender_name = resouce_result['name_sender']
            document_Id = resouce_result['document_Id']
        else:
            title_Chat = ''
            sender_name = ''
            document_Id = ''
        details_message = 'โดย ' + sender_name
        headers = {
            'content-type': 'application/json',
            'Authorization':token_bot_chat
        }
        url_topaperless = myUrl_domain2 + '?type=' + typeChat +'&sumpage=' + hash_sid +'&page='
        url_topaperless_approve = myUrl_toChat + '?type=' + typeChat +'&action=approve&sumpage=' + hash_sid +'&page='
        url_topaperless_reject = myUrl_toChat + '?type=' + typeChat +'&action=reject&sumpage=' + hash_sid +'&page='
        url_viewPdf =  myUrl_toViewPDF_toChat + '?sumpage=' + hash_sid
        url_topaperless_approve_task = myUrl_toTaskChat + '?type=' + typeChat +'&action=approve&sumpage=' + hash_sid +'&page='
        headers = {
            'content-type': 'application/json',
            'Authorization':token_bot_chat
        }
        dataJson = {
            "bot_id": id_bot_chat,
            "to": user_id_one,
            # "ref":[],
            "official_template_info": {
                "type": "official_template",
                "detail": document_Id + '\n' + details_message,
                "title": title_Chat,
                "image": imageURL,
                "onclick_img": {
                    "type": "webview",
                    "size": "full",
                    "url": url_viewPdf
                },
                "choice": [
                    {
                        "label": "Approve",
                        "type": "webview",
                        "url": url_topaperless_approve,
                        "size": "compact",
                        "color": "#ffffff",
                        "background": "#4268fb",
                        "sign": "true"
                    },
                    {
                        "label": "Reject",
                        "type": "webview",
                        "size": "compact",
                        "url": url_topaperless_reject,
                        "color": "#dd6262",
                        "background": "",
                        "sign": "true"
                    }
                ]
            },
            "task_info": {
                "priority": priority_,
                "title": title_Chat,
                "detail": document_Id + '\n' +details_message,
                "time_start": st_time_start,
                "time_end": st_time_end,
                "assign": list_assign_tmp,
                "sign_info": {
                    "type": "webview",
                    "size": "full",
                    "label": "View Detail",
                    "url": url_topaperless_approve_task,
                    "sign": "true"
                }
            }
        }
        url = url_oneChat + '/api/v1/paperless_send_approve'
        r = requests.post(url_oneChat + '/api/v1/paperless_send_approve',json=dataJson,headers=headers,verify=False,timeout=10)
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(dataJson),url,token_header)
            return {'result':'OK','messageText':r.json()}
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(dataJson),url,token_header)
            return {'result':'ER','msg':'message ' + str(r.text)}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header)
        return {'result':'ER','msg':ex}
#
def send_chat_paperless_send_approve_v2(bio_authen,task_btn_text,body_text,button_text,document_id,type_chat,hash_sid,id_bot_chat,token_bot_chat,email_to,user_id_one,image_url_path,token_header):
    list_assign_tmp = []
    list_assign_tmp.append(user_id_one)
    ts_start = int(time.time())
    ts_end = int(time.time()) + 259200
    st_time_start = datetime.datetime.fromtimestamp(ts_start).strftime('%Y-%m-%d %H:%M:%S')
    st_time_end = datetime.datetime.fromtimestamp(ts_end).strftime('%Y-%m-%d %H:%M:%S')
    priority_ = "1"
    str_body = ''
    for u in range(len(body_text)):
        str_body += body_text[u] + '\n'
    label_button_1 = str(button_text[0])
    label_button_2 = str(button_text[1])
    headers = {
        'content-type': 'application/json',
        'Authorization':token_bot_chat
    }
    url_topaperless = myUrl_domain2 + '?type=' + type_chat +'&sumpage=' + hash_sid +'&page='
    url_topaperless_approve = myUrl_toChat + '?type=' + type_chat +'&action=approve&sumpage=' + hash_sid +'&page='
    url_topaperless_reject = myUrl_toChat + '?type=' + type_chat +'&action=reject&sumpage=' + hash_sid +'&page='
    url_viewPdf =  myUrl_toViewPDF_toChat + '?sumpage=' + hash_sid
    url_topaperless_approve_task = myUrl_toTaskChat + '?type=' + type_chat +'&action=approve&sumpage=' + hash_sid +'&page='
    headers = {
        'content-type': 'application/json',
        'Authorization':token_bot_chat
    }
    dataJson = {
        "bot_id": id_bot_chat,
        "to": email_to,
        "custom_notification":"send a document",
        # "ref":[],
        "official_template_info": {
            "type": "official_template",
            "detail": str_body,
            "title": document_id,
            "image": image_url_path,
            "onclick_img": {
                "sign": "true",
                "type": "webview",
                "size": "full",
                "url": url_topaperless_approve_task
            },
            "choice": [
                {
                    "label": label_button_1,
                    "bio_authen":bio_authen,
                    "type": "webview",
                    "url": url_topaperless_approve,
                    "size": "compact",
                    "color": "#ffffff",
                    "background": "#4268fb",
                    "sign": "true"
                },
                {
                    "label": label_button_2,
                    "bio_authen":bio_authen,
                    "type": "webview",
                    "size": "compact",
                    "url": url_topaperless_reject,
                    "color": "#dd6262",
                    "background": "",
                    "sign": "true"
                }
            ]
        },
        "task_info": {
            "priority": priority_,
            "title": body_text[0],
            "task_message":"0",
            "detail": str_body,
            "time_start": st_time_start,
            "time_end": st_time_end,
            "assign": list_assign_tmp,
            "sign_info": {
                "type": "webview",
                "size": "full",
                "label": task_btn_text[0],
                "url": url_topaperless_approve_task,
                "sign": "true"
            }
        }
    }
    url = url_oneChat + '/api/v1/paperless_send_approve'    
    time_duration = ''
    try:
        r = requests.post(url,json=dataJson,headers=headers,verify=False,timeout=10)
        time_duration = str(int(r.elapsed.total_seconds() * 1000))
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(dataJson),url,token_header,time_duration)
            return {'result':'OK','msg':r.json()}
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(dataJson),url,token_header,time_duration)
            return {'result':'ER','msg':r.json()}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':str(ex)}

def send_chat_paperless_send_approve_v3(type_message,bio_authen,task_btn_text,body_text,button_text,document_id,type_chat,hash_sid,id_bot_chat,token_bot_chat,email_to,user_id_one,image_url_path,token_header,uuid):
    list_assign_tmp = []
    list_assign_tmp.append(user_id_one)
    ts_start = int(time.time())
    ts_end = int(time.time()) + 259200
    st_time_start = datetime.datetime.fromtimestamp(ts_start).strftime('%Y-%m-%d %H:%M:%S')
    st_time_end = datetime.datetime.fromtimestamp(ts_end).strftime('%Y-%m-%d %H:%M:%S')
    priority_ = "1"
    str_body = ''
    for u in range(len(body_text)):
        str_body += body_text[u] + '\n'
    label_button_1 = str(button_text[0])
    label_button_2 = str(button_text[1])
    headers = {
        'content-type': 'application/json',
        'Authorization':token_bot_chat
    }
    url_topaperless = myUrl_domain2 + '?type=' + type_chat +'&sumpage=' + hash_sid +'&page='
    url_topaperless_approve = myUrl_toChat + '?type=' + type_chat +'&action=approve&sumpage=' + hash_sid +'&email='+email_to+'&page='
    url_topaperless_reject = myUrl_toChat + '?type=' + type_chat +'&action=reject&sumpage=' + hash_sid +'&email='+email_to+'&page='
    url_viewPdf =  myUrl_toViewPDF_toChat + '?sumpage=' + hash_sid
    url_topaperless_approve_task = myUrl_toTaskChat + '?type=' + type_chat +'&action=approve&sumpage=' + hash_sid +'&email='+email_to+'&page='
    tmptask_info = ""
    if type_message == "approve":
        tmptask_info = {
            "priority": priority_,
            "title": body_text[0],
            "task_message":"0",
            "detail": str_body,
            "time_start": st_time_start,
            "time_end": st_time_end,
            "assign": list_assign_tmp,
            "sign_info": {
                "type": "webview",
                "size": "full",
                "label": task_btn_text[0],
                "url": url_topaperless_approve_task,
                "sign": "true"
            }
        }
    headers = {
        'content-type': 'application/json',
        'Authorization':token_bot_chat
    }
    dataJson = {
        "official_id":uuid,
        "bot_id": id_bot_chat,
        "to": email_to,
        "custom_notification":"send a document",
        # "ref":[],
        "official_template_info": {
            "type": "official_template",
            "detail": str_body,
            "title": document_id,
            "image": image_url_path,
            "onclick_img": {
                "sign": "true",
                "type": "webview",
                "size": "full",
                "url": url_topaperless_approve_task
            },
            "choice": [
                {
                    "label": label_button_1,
                    "bio_authen":bio_authen,
                    "type": "webview",
                    "url": url_topaperless_approve,
                    "size": "compact",
                    "color": "#ffffff",
                    "background": "#4268fb",
                    "sign": "true"
                },
                {
                    "label": label_button_2,
                    "bio_authen":bio_authen,
                    "type": "webview",
                    "size": "compact",
                    "url": url_topaperless_reject,
                    "color": "#dd6262",
                    "background": "",
                    "sign": "true"
                }
            ]
        },
        "task_info": tmptask_info
    }
    # print(dataJson)
    url = url_oneChat + '/api/v1/paperless_send_approve'    
    time_duration = ''
    try:
        r = requests.post(url,json=dataJson,headers=headers,verify=False,timeout=10)
        time_duration = str(int(r.elapsed.total_seconds() * 1000))
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(dataJson),url,token_header,time_duration)
            return {'result':'OK','msg':r.json()}
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(dataJson),url,token_header,time_duration)
            return {'result':'ER','msg':r.json()}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':str(ex)}

def send_chat_paperless_send_approve_v3_group(bio_authen,task_btn_text,body_text,button_text,document_id,type_chat,hash_groupid,id_bot_chat,token_bot_chat,email_to,user_id_one,image_url_path,token_header,hashsid):
    try:
        time_duration = ''
        list_assign_tmp = []
        list_assign_tmp.append(user_id_one)
        ts_start = int(time.time())
        ts_end = int(time.time()) + 259200
        st_time_start = datetime.datetime.fromtimestamp(ts_start).strftime('%Y-%m-%d %H:%M:%S')
        st_time_end = datetime.datetime.fromtimestamp(ts_end).strftime('%Y-%m-%d %H:%M:%S')
        priority_ = "1"
        str_body = ''
        for u in range(len(body_text)):
            str_body += body_text[u] + '\n'
        label_button_1 = str(button_text[0])
        label_button_2 = str(button_text[1])
        headers = {
            'content-type': 'application/json',
            'Authorization':token_bot_chat
        }
        url_topaperless = myUrl_domain2 + '/login?type=' + type_chat +'&document=' + hash_groupid +'&page='
        url_topaperless_approve = myUrl_toChat + '/login?type=' + type_chat +'&action=approve&document=' + hash_groupid +'&page='
        url_topaperless_some_approve = myUrl_toChat + '/login?type=' + type_chat +'&action=somapprove&document=' + hash_groupid +'&page='
        url_viewPdf =  myUrl_toViewPDF_toChat + '/login?sumpage=' + hashsid
        url_topaperless_approve_task = myUrl_toTaskChat + '/login?type=' + type_chat +'&action=approve&document=' + hash_groupid +'&page='
        headers = {
            'content-type': 'application/json',
            'Authorization':token_bot_chat
        }
        dataJson = {
            "bot_id": id_bot_chat,
            "to": email_to,
            "custom_notification":"send a document",
            # "ref":[],
            "official_template_info": {
                "type": "official_template",
                "detail": str_body,
                "title": document_id,
                "image": image_url_path,
                "onclick_img": {
                    "sign": "true",
                    "type": "webview",
                    "size": "full",
                    "url": url_topaperless_approve_task
                },
                "choice": [
                    {
                        "label": label_button_1,
                        "bio_authen":bio_authen,
                        "type": "webview",
                        "url": url_topaperless_approve,
                        "size": "compact",
                        "color": "#ffffff",
                        "background": "#4268fb",
                        "sign": "true"
                    },
                    {
                        "label": label_button_2,
                        "bio_authen":bio_authen,
                        "type": "webview",
                        "size": "compact",
                        "url": url_topaperless_some_approve,
                        "color": "#ffffff",
                        "background": "#4268fb",
                        "sign": "true"
                    }
                ]
            },
            "task_info": {
                "priority": priority_,
                "title": body_text[0],
                "task_message":"0",
                "detail": str_body,
                "time_start": st_time_start,
                "time_end": st_time_end,
                "assign": list_assign_tmp,
                "sign_info": {
                    "type": "webview",
                    "size": "full",
                    "label": task_btn_text[0],
                    "url": url_topaperless_approve_task,
                    "sign": "true"
                }
            }
        }
        url = url_oneChat + '/api/v1/paperless_send_approve'
        r = requests.post(url_oneChat + '/api/v1/paperless_send_approve',json=dataJson,headers=headers,verify=False,timeout=10)
        time_duration = str(int(r.elapsed.total_seconds() * 1000))
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(dataJson),url,token_header,time_duration)
            return {'result':'OK','msg':r.json()}
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(dataJson),url,token_header,time_duration)
            return {'result':'ER','msg':r.text}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        current_app.logger.info(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),url,token_header,time_duration)
        return {'result':'ER','msg':ex}

def sendtask_getProject_tochat_newversion_v3(oneid_result,id_bot_chat=None,token_bot_chat=None,token_header=None):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_bot_chat
        }
        dataJson = {
            "bot_id": id_bot_chat,
            "one_id": oneid_result
        }
        r = requests.post(Url_Bot_getProject,json=dataJson,headers=headers,verify=False,timeout=10)
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(dataJson),Url_Bot_getProject,token_header)
            return {'result':'OK','messageText':r.json()}
        else:
            insert().insert_tran_log_v1(str(t.text),'ER',str(dataJson),Url_Bot_getProject,token_header)
            return {'result':'ER','msg':'message ' + str(t.text)}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),Url_Bot_getProject,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),Url_Bot_getProject,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),Url_Bot_getProject,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),Url_Bot_getProject,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(dataJson),Url_Bot_getProject,token_header)
        return {'result':'ER','msg':ex}

def sender_one_chat_templatechat_v2(body_text,button_text,document_id,type_chat,hash_sid,id_bot_chat,token_bot_chat,email_to,user_id_one,image_url_path,token_header):
    # print(body_text,button_text,document_id,type_chat,hash_sid,id_bot_chat,token_bot_chat,email_to,user_id_one,image_url_path,token_header)
    try:
        str_body = ''
        for u in range(len(body_text)):
            str_body += body_text[u] + '\n'
        label_button_1 = str(button_text[0])
        label_button_2 = str(button_text[1])
        headers = {
            'content-type': 'application/json',
            'Authorization':token_bot_chat
        }
        url_topaperless = myUrl_domain2 + '?type=' + type_chat +'&sumpage=' + hash_sid +'&page='
        url_topaperless_approve = myUrl_toChat + '?type=' + type_chat +'&action=approve&sumpage=' + hash_sid +'&page='
        url_topaperless_reject = myUrl_toChat + '?type=' + type_chat +'&action=reject&sumpage=' + hash_sid +'&page='
        url_viewPdf =  myUrl_toViewPDF_toChat + '?sumpage=' + hash_sid
        datajson = {
                "to": user_id_one,
                "bot_id": id_bot_chat,
                "type": "official_template",
                "detail": str_body,
                "title":document_id,
                "image": image_url_path,
                "onclick_img": {
                    "type": "webview",
                    "size" : "full",
                    "url":url_viewPdf
                },
                "choice": [
                    {
                        "label": label_button_1,
                        "type": "webview",
                        "url": url_topaperless_approve,
                        "size": "compact",
                        "color": "#ffffff",
                        "background": "#4268fb",
                        "sign": "true"
                    },
                    {
                        "label": label_button_2,
                        "type": "webview",
                        "size" : "compact",
                        "url": url_topaperless_reject,
                        "color": "#dd6262",
                        "background": "",
                        "sign": "true"
                    }
                ]
        }
        url = url_oneChat + '/api/v1/push_message'
        # print(datajson)
        r = requests.post(url,json=datajson,headers=headers,verify=False,timeout=10)
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(datajson),url,token_header)
            return {'result':'OK','msg':r.json()}
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(datajson),url,token_header)
            return {'result':'ER','msg':r.json()}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        print(str(ex))
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':ex}

def sender_one_chat_templatechat_v3(body_text,button_text,document_id,type_chat,hash_sid,id_bot_chat,token_bot_chat,email_to,user_id_one,image_url_path,token_header):
    # print(body_text,button_text,document_id,type_chat,hash_sid,id_bot_chat,token_bot_chat,email_to,user_id_one,image_url_path,token_header)
    try:
        str_body = ''
        for u in range(len(body_text)):
            str_body += body_text[u] + '\n'
        label_button_1 = str(button_text[0])
        label_button_2 = str(button_text[1])
        headers = {
            'content-type': 'application/json',
            'Authorization':token_bot_chat
        }
        url_topaperless = myUrl_domain2 + '?type=' + type_chat +'&sumpage=' + hash_sid +'&page='
        url_topaperless_approve = myUrl_toChat + '?type=' + type_chat +'&action=approve&sumpage=' + hash_sid +'&page='
        url_topaperless_reject = myUrl_toChat + '?type=' + type_chat +'&action=reject&sumpage=' + hash_sid +'&page='
        url_viewPdf =  myUrl_toViewPDF_toChat + '?sumpage=' + hash_sid
        datajson = {
                "to": user_id_one,
                "bot_id": id_bot_chat,
                "type": "official_template",
                "detail": str_body,
                "title":document_id,
                "image": image_url_path,
                "onclick_img": {
                    "type": "webview",
                    "size" : "full",
                    "url":url_viewPdf
                },
                "choice": [
                    {
                        "label": label_button_1,
                        "type": "webview",
                        "url": url_topaperless_approve,
                        "size": "compact",
                        "color": "#ffffff",
                        "background": "#4268fb",
                        "sign": "true"
                    },
                    {
                        "label": label_button_2,
                        "type": "webview",
                        "size" : "compact",
                        "url": url_topaperless_reject,
                        "color": "#dd6262",
                        "background": "",
                        "sign": "true"
                    }
                ]
        }
        url = url_oneChat + '/api/v1/push_message'
        # print(datajson)
        r = requests.post(url,json=datajson,headers=headers,verify=False,timeout=10)
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(datajson),url,token_header)
            return {'result':'OK','msg':r.json()}
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(datajson),url,token_header)
            return {'result':'ER','msg':r.json()}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        print(str(ex))
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':ex}

def sender_one_chat_templatechat_v1(typeChat,data_To,nameFile,Treacking_num,url_link,sidCode,resouce_result=None,imageURL=None,id_bot_chat=None,token_bot_chat=None,token_header=None):
    try:
        if typeChat == 'signning':
            title_Chat = 'please sign'
            type_label = 'ลงนามอนุมัติ'
        elif typeChat == 'approve':
            title_Chat = 'please approve'
            type_label = 'ลงนามอนุมัติ'
        elif typeChat == None:
            title_Chat = 'please sign'
            type_label = 'ลงนามอนุมัติ'
        hash_sid = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
        if resouce_result != None:
            title_Chat = ''
            if resouce_result['documentName'] != None:
                title_Chat = resouce_result['documentName']
            if resouce_result['name_sender'] != None:
                sender_name = resouce_result['name_sender']
        else:
            title_Chat = ''
            sender_name = ''
        details_message = 'โดย ' + sender_name
        headers = {
            'content-type': 'application/json',
            'Authorization':token_bot_chat
        }
        url_topaperless = myUrl_domain2 + '?type=' + typeChat +'&sumpage=' + hash_sid +'&page='
        url_topaperless_approve = myUrl_toChat + '?type=' + typeChat +'&action=approve&sumpage=' + hash_sid +'&page='
        url_topaperless_reject = myUrl_toChat + '?type=' + typeChat +'&action=reject&sumpage=' + hash_sid +'&page='
        url_viewPdf =  myUrl_toViewPDF_toChat + '?sumpage=' + hash_sid
        datajson = {
                "to": data_To,
                "bot_id": id_bot_chat,
                "type": "official_template",
                "detail": details_message,
                "title":title_Chat,
                "image": imageURL,
                "onclick_img": {
                    "type": "webview",
                    "size" : "full",
                    "url":url_viewPdf
                },
                "choice": [
                    {
                        "label": "ลงนามอนุมัติ",
                        "type": "webview",
                        "url": url_topaperless_approve,
                        "size" : "compact",
                        "color": "#ffffff",
                        "background": "#4268fb",
                        "sign": "true"
                    },
                    {
                        "label": "ปฏิเสธการลงนาม",
                        "type": "webview",
                        "size" : "full",
                        "url": url_topaperless_reject,
                        "color": "#dd6262",
                        "background": "",
                        "sign": "true"
                    }
                ]
        }
        print(datajson)
        r = requests.post(url_chat,json=datajson,headers=headers,verify=False,timeout=10)
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(datajson),url_chat,token_header)
            return r.json()
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(datajson),url_chat,token_header)
            return r.json()
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_chat,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_chat,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_chat,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_chat,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_chat,token_header)
        return {'result':'ER','msg':ex}

def sendtask_change_stateChat(state_id_,task_id_):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service
        }
        r = requests.post(url_change_state,json={
            "bot_id": bot_id,
            "state_id": state_id_,
            "task_id": task_id_
        }
        ,headers=headers,verify=False,timeout=10)
        # "upload_to_box":{"service":"e-tax","type":"bot_file"} for file to onebox
        r = r.json()
        return {'result':'OK','messageText':r}
    except requests.Timeout as ex:
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        return {'result':'ER','msg':ex}

def sendtask_change_stateChat_v2(state_id_,task_id_,token_chat_bot,chat_bot_id,token_header):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_chat_bot
        }
        datajson = {
            "bot_id": chat_bot_id,
            "state_id": state_id_,
            "task_id": task_id_
        }
        r = requests.post(url_change_state,json=datajson
        ,headers=headers,verify=False,timeout=10)
        # "upload_to_box":{"service":"e-tax","type":"bot_file"} for file to onebox

        r = r.json()
        print(r)
        insert().insert_tran_log_v1(str(r),'OK',str(datajson),url_change_state,token_header)
        return {'result':'OK','messageText':r}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_change_state,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_change_state,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_change_state,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_change_state,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_change_state,token_header)
        return {'result':'ER','msg':ex}

def sendtask_change_stateChat_v3(state_id,task_id,token_chat_bot,chat_bot_id,token_header):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_chat_bot
        }
        datajson = {
            "bot_id": chat_bot_id,
            "state_id": state_id,
            "task_id": task_id
        }
        url = url_taskchat + '/api/v1/bot_change_state'
        r = requests.post(url,json=datajson
        ,headers=headers,verify=False,timeout=10)
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(datajson),url,token_header)
            return {'result':'OK','msg':r.json()}
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(datajson),url,token_header)
            return {'result':'ER','msg':r.json()}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header)
        return {'result':'ER','msg':ex}

def sendtask_change_stateChat_v4(official_id,token_chat_bot,chat_bot_id,token_header):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_chat_bot
        }
        datajson = {
            "bot_id":chat_bot_id,
            "official_id":official_id
        }
        url = url_taskchat + '/api/v3/bot_change_state'
        time_duration = ''
        r = requests.post(url,json=datajson
        ,headers=headers,verify=False,timeout=10)
        time_duration = str(int(r.elapsed.total_seconds() * 1000))
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(datajson),url,token_header,time_duration)
            return {'result':'OK','msg':r.json()}
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(datajson),url,token_header,time_duration)
            return {'result':'ER','msg':r.json()}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header,time_duration)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header,time_duration)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header,time_duration)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header,time_duration)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,token_header,time_duration)
        return {'result':'ER','msg':ex}

def login_OneChat(user_id,token_access):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service_autoAdd
        }
        datajson = {
            "one_id": user_id
        }
        r = requests.post(url_loginchat,json=datajson,headers=headers,verify=False,timeout=3)
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(datajson),url_loginchat,token_access)
            return {'result':'OK','messageText':r.json()}
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(datajson),url_loginchat,token_access)
            return {'result':'ER','msg':'message ' + str(r.text)}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_loginchat,token_access)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_loginchat,token_access)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_loginchat,token_access)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_loginchat,token_access)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_loginchat,token_access)
        return {'result':'ER','msg':ex}

def close_webview_v1(user_id,hash_token):
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_service_autoAdd
        }
        datajson = {
            "user_id":user_id
        }
        r = requests.post(url_close_webview,json=datajson
        ,headers=headers,verify=False)
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(datajson),url_close_webview,hash_token)
            return {'result':'OK','messageText':r.json()}
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(datajson),url_close_webview,hash_token)
            return {'result':'ER','msg':'messgae ' + str(r.text)}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_close_webview,hash_token)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_close_webview,hash_token)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_close_webview,hash_token)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_close_webview,hash_token)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url_close_webview,hash_token)
        return {'result':'ER','msg':ex}

def chat_for_service_v1(sidcode,token_header):
    dataJson = {
        'sid_code' : sidcode
    }
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
            tmplanguage = 'th'
            id_chat_bot = bot_id
            token_chat_bot = token_service
            tmp_id_chat_one_dis = None
            result_send_to_sender = None
            if result_message['result'] == 'ER':
                return ({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':result_message['messageText']}})
            if result_message['result'] == 'OK':
                if result_message['datachat']['documentType_Details'][0] != None:
                    if 'chat_bot_details' in result_message['datachat']['documentType_Details'][0]:
                        msg_chat_bot = result_message['datachat']['documentType_Details'][0]['chat_bot_details']
                        if msg_chat_bot != None:
                            # status_chat_bot = msg_chat_bot['a']
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
                    tmp_get_message = result_message['data']
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
                    try:                                    
                        tmp_options_page = eval(tmp_get_message['options_page'])
                    except Exception as e:
                        tmp_options_page = tmp_get_message['options_page']
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
                                if 'language' in tmp_onechat_message:
                                    tmplanguage = tmp_onechat_message['language']
                                    if tmplanguage == 'EN':
                                        tmplanguage = 'eng'
                                    elif tmplanguage == 'TH':
                                        tmplanguage = 'th'
                                    tmp_get_message['language'] = tmplanguage
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
                                    result_message_text = select().select_chat_sender_v1_text(sidcode,tmp_document_id,tmplanguage)
                                    result_get_userid_2 = select().select_user_id_from_email_chat_v1(tmp_sender_email)
                                    if result_message_text['result'] == 'OK':
                                        if tmplanguage == 'th':
                                            tmp_message_toChat = result_message_text['messageText'] + '\n' + 'สถานะเอกสาร : ปฏิเสธอนุมัติ'
                                        elif tmplanguage == 'eng':
                                            tmp_message_toChat = result_message_text['messageText'] + '\n' + 'Document Status : Reject approval'
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
                                    return ({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':[],'message':'fail cant get data','code':'EROC002'}})
                            return ({'result':'OK','messageText':{'data':None,'message':'success document reject','code':'SCOC004'},'status_Code':200,'messageER':None})
                    elif 'Complete' in tmp_status_ppl or 'Approve' in tmp_status_ppl:
                        response_status_chat_list = []
                        if result_message['result'] == 'OK':
                            tmp_get_message = result_message['data']
                            tmp_document_id = tmp_get_message['document_id']
                            tmp_sender_email = tmp_get_message['sender_email']
                            tmp_sender_name = tmp_get_message['sender_name']
                            tmp_sender_name_eng = tmp_get_message['sender_name_eng']
                            try:                                    
                                tmp_options_page = eval(tmp_get_message['options_page'])
                            except Exception as e:
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
                                        if 'language' in tmp_onechat_message:
                                            tmplanguage = tmp_onechat_message['language']
                                            if tmplanguage == 'EN':
                                                tmplanguage = 'eng'
                                            elif tmplanguage == 'TH':
                                                tmplanguage = 'th'
                                            tmp_get_message['language'] = tmplanguage
                        else:
                            return ({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':[],'message':'fail cant get data','code':'EROC002'}})
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
                            result_message_text = select().select_chat_sender_v1_text(sidcode,tmp_document_id,tmplanguage)
                            result_get_userid_2 = select().select_user_id_from_email_chat_v1(tmp_sender_email)
                            if result_message_text['result'] == 'OK':
                                if tmplanguage == 'th':
                                    tmp_message_toChat = result_message_text['messageText'] + '\n' + 'สถานะเอกสาร : เอกสารสมบูรณ์'
                                elif tmplanguage == 'eng':
                                    tmp_message_toChat = result_message_text['messageText'] + '\n' + 'Document Status : Complete document'
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
                                
                            return ({'result':'OK','messageText':{'data':response_status_chat_list,'message':'success','code':'SCOC001'},'status_Code':200,'messageER':[]})
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
                                tmp_document_id = tmp_get_message['document_id']
                                tmp_sender_email = tmp_get_message['sender_email']
                                tmp_sender_name = tmp_get_message['sender_name']
                                tmp_sender_name_eng = tmp_get_message['sender_name_eng']
                                try:                                    
                                    tmp_options_page = eval(tmp_get_message['options_page'])
                                except Exception as e:
                                    tmp_options_page = tmp_get_message['options_page']
                                tmp_body_text = tmp_get_message['body_text']
                                tmp_button_text = tmp_get_message['button_text']
                                tmp_task_btn_text = tmp_get_message['task_btn_text']
                                tmp_bio_authen = tmp_get_message['bio_authen']
                                if 'onechat_message' in tmp_options_page:
                                    tmp_onechat_message = tmp_options_page['onechat_message']
                                    print('tmp_onechat_message ',tmp_onechat_message)
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
                                            if 'language' in tmp_onechat_message:
                                                tmplanguage = tmp_onechat_message['language']
                                                if tmplanguage == 'EN':
                                                    tmplanguage = 'eng'
                                                elif tmplanguage == 'TH':
                                                    tmplanguage = 'th'
                                                tmp_get_message['language'] = tmplanguage
                                for zz in range(len(tmp_get_message['body_text'])):
                                    if zz == 0:
                                        if str(tmp_get_message['body_text'][zz]).replace(' ','') == '':
                                            tmp_get_message['body_text'][zz] = tmp_document_id
                                    elif zz == 1:
                                        if str(tmp_get_message['body_text'][zz]).replace(' ','') == '':
                                            if tmplanguage == 'th':
                                                tmp_get_message['body_text'][zz] = 'โดย ' + tmp_sender_name
                                            elif tmplanguage == 'eng':
                                                tmp_get_message['body_text'][zz] = 'By ' + tmp_sender_name_eng
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
                                return ({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':[],'message':'fail cant get data','code':'EROC002'}})
                            result_message_text = select().select_chat_sender_v1_text(sidcode,tmp_document_id,tmplanguage)
                            print(result_message_text)
                            result_get_userid_2 = select().select_user_id_from_email_chat_v1(tmp_sender_email)
                            if result_message_text['result'] == 'OK':
                                if tmplanguage == 'th':                                    
                                    tmp_message_toChat = result_message_text['messageText'] + '\n' + 'สถานะเอกสาร : รอดำเนินการ'
                                elif tmplanguage == 'eng':
                                    tmp_message_toChat = result_message_text['messageText'] + '\n' + 'Document Status : Pending'
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
                                return ({'result':'OK','messageText':{'data':response_status_chat_list,'message':'success','code':'SCOC002'},'status_Code':200,'messageER':response_result})
                            # else:
                            return ({'result':'OK','messageText':{'data':response_status_chat_list,'message':'success','code':'SCOC001'},'status_Code':200,'messageER':[]})
                        else:
                            return ({'result':'OK','messageText':{'data':'group document','message':'success','code':'SCOC000'},'status_Code':200,'messageER':None})
            else:
                return ({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':result_message['messageText'],'message':'success','code':'EROC001'}})
                            # return jsonify({'result':'OK','messageText':{'data':result_message['messageText'],'message':'success','code':'SCOC002'},'status_Code':200,'messageER':response_result}),200
            # SCOC001 sccuess ทั้งหมด
            # SCOC002 มี fail อยู่บ้างส่วน รายละเอียดที่ messageER
            return ({'result':'OK','messageText':{'data':result_message['messageText'],'message':'success','code':'SCOC001'},'status_Code':200,'messageER':[]})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'exception ' + str(exc_type)}})

def chat_sender_group_v1(group_id,email):
    try:
        group_id = group_id
        result_message = select().select_chat_group_v1(group_id)
        if result_message['result'] == 'OK':
            tmpmessageText = result_message['messageText']
            tmpsidcode = result_message['sidcode']
            for n in range(len(tmpmessageText)):
                tmpemailone = tmpmessageText[n]['emailone']
                tmpstatus = tmpmessageText[n]['status']
                if 'Incomplete' in tmpstatus:
                    image_url_path = 'https://www.img.in.th/images/83ca9b38ee2d7d129f1826f75ea05e4f.png'
                    # image_data = createImage_formPDF2(tmpsidcode)
                    # if image_data['result'] == 'OK':
                    #     image_url_path = myUrl_domain + 'public/viewimage/' + image_data['data']
                    # else:
                    #     return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error createImage pdf','data':None}}),200
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
                    if email != None:
                        tmp_email_one = email
                    else:
                        tmp_email_one = tmpemailone[0]
                    if type(tmp_email_one) is list:
                        for z in range(len(tmp_email_one)):
                            oneemail = tmp_email_one[z]
                            tmp_user_id =''
                            result_get_userid = select().select_user_id_from_email_chat_v1(oneemail)
                            if result_get_userid['result'] == 'OK':
                                tmp_user_id = result_get_userid['messageText']['user_id']
                            if tmp_user_id == None:
                                tmp_user_id = oneemail
                            tmp_email_one = (tmp_user_id)
                            sendchat_result = send_chat_paperless_send_approve_v3_group('',tmp_task_btn_text,tmp_body_text,tmp_button_text,tmp_document_id,type_chat,hash_groupid,id_chat_bot,token_chat_bot,tmp_email_one,tmp_user_id,image_url_path,'',hash_sidcode)
                    else:
                        tmp_user_id =''
                        result_get_userid = select().select_user_id_from_email_chat_v1(tmp_email_one)
                        if result_get_userid['result'] == 'OK':
                            tmp_user_id = result_get_userid['messageText']['user_id']
                        if tmp_user_id == None:
                            tmp_user_id = tmp_email_one
                        tmp_email_one = (tmp_user_id)
                        sendchat_result = send_chat_paperless_send_approve_v3_group('',tmp_task_btn_text,tmp_body_text,tmp_button_text,tmp_document_id,type_chat,hash_groupid,id_chat_bot,token_chat_bot,tmp_email_one,tmp_user_id,image_url_path,'',hash_sidcode)

                    return ({'result':'OK','messageText':{'data':'succuess','message':'success','code':'SCOC001'},'status_Code':200,'messageER':[]})

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'exception ' + str(exc_type)}}),200

def quickreply_onechat_v1(message,useridChat,token_bot,bot_chat_id,token_header):
    try:
        url_more_details_w = url_paperless + '?filter_type=W&stoken='
        url_welcome = url_paperless + '?stoken='
        headers = {
            'content-type': 'application/json',
            'Authorization':token_bot
        }
        data_Json = {
            "to": useridChat,
            "bot_id": bot_chat_id,
            "type": "text",
            "message": message,
            "quick_reply":[{
                        "label": "เข้าสู่หน้าเว็บไซต์",
                        "type": "link",
                        "url": url_welcome,
                        "sign":"true"
                    },{
                        "label": "เอกสารที่รออนุมัติ",
                        "type": "link",
                        "url": url_more_details_w,
                        "sign":"true"
                    },{
                        "label": "ติดตามสถานะเอกสาร",
                        "type": "link",
                        "url": paperless_tracking
                    }]
        }
        url = url_oneChat + '/api/v1/push_quickreply'
        r = requests.post(url,json=data_Json,headers=headers,verify=False,timeout=10)
        print(r.text)
        if r.status_code == 200 or r.status_code == 201:
            insert().insert_tran_log_v1(str(r.json()),'OK',str(data_Json),url,token_header)
            return r.json()
        else:
            insert().insert_tran_log_v1(str(r.text),'ER',str(data_Json),url,token_header)
            return r.json()
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_Json),url,token_header)
        return {'result':'ER','msg':ex}
