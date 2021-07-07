#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from db.db_Class import *
from config.value import *
from method.access import *
from method.hashpy import *
from method.other import *
from config.lib import *
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from method.document import *
from method.cal_step import *
from method.pdfSign import *

# @with_slave
class select_4():
    def select_Signature_v1(self,user_id):
        self.user_id = user_id
        try:
            sql = ''' 
                SELECT
                    p_sign AS "signature"
                FROM
                    "tb_userProfile" 
                WHERE
                    p_userid = :user_id
            '''
            connection = slave.connect()
            result = connection.execute(text(sql),user_id=self.user_id)
            resultQuery = [dict(row) for row in result]
            return [200,resultQuery]
        except Exception as e:
            return [200,str(e)]

    def sleect_template_business_v1(self,tax_id,name,keyword,thai_email):
        self.tax_id = tax_id
        self.name = name
        self.thai_email = thai_email
        self.keyword = keyword
        searchtax = "%{}%".format(self.tax_id)
        searchname = "%{}%".format(self.name)
        stepCode = None
        list_templateCode = []
        count_Template = 0
        try:
            sql = '''
                SELECT
                    tb_step_template."step_Name" AS "step_Name",
                    tb_step_template."step_Code" AS "step_Code",
                    tb_step_template."documentDetails" AS "documentDetails",
                    tb_step_template.condition_temp AS "condition_temp",
                    tb_step_template."step_Data" AS "step_Data",
                    tb_step_template.template_biz AS "template_biz",
                    tb_step_template.username AS "username" 
                FROM
                    tb_step_template 
                WHERE
                    status = 'ACTIVE'                     
                    AND template_biz LIKE :tax_id 
            '''
            if self.name != None:
                sql += ''' AND ( "step_Name" LIKE :stepname OR condition_temp LIKE :stepname )  '''
            if self.keyword != None:
                sql += ''' AND ("step_Code" IN :stepCode) '''
                
            # 1 ขึ้นไป d1dbad8b-3519-43bc-b8a2-982ef8b6ce4f
            if self.keyword == "0":
                stepCode = ['d1dbad8b-3519-43bc-b8a2-982ef8b6ce4f']
                stepCode = tuple(stepCode)            
            if self.keyword == "1":
                stepCode = ['70e8eed3-a994-4f9a-8f61-a909f918c937']
                stepCode = tuple(stepCode)
            if self.keyword == "2":
                stepCode = ['05f87600-9d49-4cf8-b163-4c0186e860c2','fc71ea4c-d465-4db9-a405-b83dbedb7680']
                stepCode = tuple(stepCode)
            if self.keyword == "3":
                stepCode = ['a52ca602-f0f8-4d63-88df-02b3c9adb46b']
                stepCode = tuple(stepCode)
            if self.keyword == "4":
                stepCode = [
                    "723ec4af-9101-4a72-8d7d-334fcd80c6d4",
                    "4c606aed-18e8-4eb4-9b85-3e5f3a29c13a",
                    "88a5483f-82e5-4391-bc04-fe83f29a4012",
                    "f0202b63-3ee5-4bd1-a208-bf634cacacbd"
                ]
                stepCode = tuple(stepCode)
            if self.keyword == "5":
                stepCode = [
                    "f43818c3-2753-4623-98ed-c0bb3512ec22",
                    "cd565136-20b8-4f9b-a1bd-cf845d9bbc60",
                    "49500765-f489-4554-bad8-47e9f86c2e27",
                    "8898817e-787d-4dd4-ac5f-c89e2e96ec53",
                    "55e9c76b-91d8-4e19-b4e7-a1ba4ebe23f0"
                ]
                stepCode = tuple(stepCode)
            print(stepCode)
            sql += ''' 
                ORDER BY
                    tb_step_template."step_Code" ASC  '''
            connection = slave.connect()
            result = connection.execute(text(sql),tax_id=searchtax,stepname=searchname,stepCode=stepCode)
            resultQuery = [dict(row) for row in result]
            for n in range(len(resultQuery)):
                k = resultQuery[n]
                tmpstep_Name = k['step_Name']
                tmpstep_Code = k['step_Code']
                tmpdocumentDetails = k['documentDetails']
                tmpcondition_temp = k['condition_temp']
                step_data = eval(k['step_Data'])
                Temp_activity = False
                tmp_auto_flow = False
                if type(step_data) == tuple:
                    for l in range(len(step_data)):
                        step_detail = step_data[l]['step_detail']
                        activity_code = step_detail[0]['activity_code']
                        for n in range(len(activity_code)):
                            if activity_code[n] == 'A04':
                                Temp_activity = True
                                break
                elif type(step_data) == dict:
                    step_detail = step_data['step_detail']
                    activity_code = step_detail[0]['activity_code']
                    for n in range(len(activity_code)):
                        if activity_code[n] == 'A04':
                            Temp_activity = True
                            break
                if str(k['template_biz']).replace(' ','') != '':
                    if k['template_biz'] != None:
                        list_result_email_step = []
                        list_step_num = []
                        id_card_num = eval(k['template_biz'])
                        id_card_num = id_card_num['id_card_num']
                        if id_card_num == self.tax_id:
                            step_data_info = eval(k['step_Data'])
                            if 'step_num' in step_data_info:
                                list_email = []
                                list_userid = []
                                if 'step_detail' in step_data_info:
                                    for u in range(len(step_data_info['step_detail'])):
                                        json_email = {}
                                        one_email_info = step_data_info['step_detail'][u]['one_email']
                                        if str(one_email_info).replace(' ','').lower() == 'me':
                                            one_email_info = self.thai_email
                                        if '@' not in one_email_info and one_email_info != '':
                                            tmp_auto_flow = True
                                        r = select().select_user_id_from_email_chat_v1(one_email_info)
                                        if 'user_id' in r['messageText']:
                                            user_id_one = r['messageText']['user_id']
                                        list_email.append(one_email_info)
                                        list_userid.append(user_id_one)
                                        if step_data_info['step_num'] not in list_step_num:
                                            list_step_num.append(step_data_info['step_num'])
                                            json_email['step_num'] = step_data_info['step_num']
                                            json_email['one_email'] = list_email
                                            json_email['user_id'] = list_userid
                                            json_email['activity_code'] = step_data_info['step_detail'][u]['activity_code']
                                            if 'rf_step' in step_data_info:
                                                json_email['ref_step'] =  step_data_info['rf_step']
                                            list_acdata = []
                                            for v in range(len(step_data_info['step_detail'][u]['activity_data'])):

                                                if step_data_info['step_detail'][u]['activity_data'][v] == {}:
                                                    continue
                                
                                                else:
                                                    list_acdata.append(step_data_info['step_detail'][u]['activity_data'][v])
                                            json_email['activity_data'] = list_acdata

                                            if 'A04' in step_data_info['step_detail'][u]['activity_code']:
                                                json_email['activity_code_check'] = True
                                            else:
                                                json_email['activity_code_check'] = False
                                            
                                            list_result_email_step.append(json_email)
                            else:
                                for i in range(len(step_data_info)):
                                    list_email = []
                                    list_userid = []
                                    for z in range(len(step_data_info[i]['step_detail'])):
                                        json_email = {}
                                        one_email_info = step_data_info[i]['step_detail'][z]['one_email']
                                        if str(one_email_info).replace(' ','').lower() == 'me':
                                            one_email_info = self.thai_email
                                        if '@' not in one_email_info and one_email_info != '':
                                            tmp_auto_flow = True
                                        # if len(list_step_num) != 0:
                                        r = select().select_user_id_from_email_chat_v1(one_email_info)
                                        if 'user_id' in r['messageText']:
                                            user_id_one = r['messageText']['user_id']
                                        list_email.append(one_email_info)
                                        list_userid.append(user_id_one)
                                        if step_data_info[i]['step_num'] not in list_step_num:
                                            list_step_num.append(step_data_info[i]['step_num'])
                                            json_email['step_num'] = step_data_info[i]['step_num']
                                            json_email['one_email'] = list_email
                                            json_email['user_id'] = list_userid
                                            json_email['activity_code'] = step_data_info[i]['step_detail'][z]['activity_code']
                                            # print(step_data_info[i]['step_detail'][z][''])
                                            if 'rf_step' in step_data_info[i]:
                                                json_email['ref_step'] =  step_data_info[i]['rf_step']
                                            list_acdata = []
                                            if step_data_info[i]['step_detail'][z]['activity_data'] == {}:
                                                json_email['activity_data'] = ''
                                            else:
                                                json_email['activity_data'] = step_data_info[i]['step_detail'][z]['activity_data']

                                            for v in range(len(step_data_info[i]['step_detail'][z]['activity_data'])):

                                                if step_data_info[i]['step_detail'][z]['activity_data'][v] == {}:
                                                    continue
                                
                                                else:
                                                    list_acdata.append(step_data_info[i]['step_detail'][z]['activity_data'][v])
                                            json_email['activity_data'] = list_acdata
                                            if 'A04' in step_data_info[i]['step_detail'][z]['activity_code']:
                                                json_email['activity_code_check'] = True
                                            else:
                                                json_email['activity_code_check'] = False
                                            list_result_email_step.append(json_email)

                            list_templateCode.append({'auto_flow':tmp_auto_flow,'Template_Name':tmpstep_Name,'Template_Code':tmpstep_Code,'Document_Type':tmpdocumentDetails,'Document_Name':tmpstep_Name,'Condition_Template':tmpcondition_temp,'Template_step':list_result_email_step,'Template_Type':'biz','Template_activity':Temp_activity})
                            count_Template = count_Template + 1
                        else:
                            pass
                else:
                    list_result_email_step = []
                    list_step_num = []
                    if k['username'] == self.username:

                        step_data_info = eval(k['step_Data'])
                        if 'step_num' in step_data_info:
                            list_email = []
                            if 'step_detail' in step_data_info:
                                for u in range(len(step_data_info['step_detail'])):
                                    json_email = {}
                                    one_email_info = step_data_info['step_detail'][u]['one_email']
                                    if str(one_email_info).replace(' ','').lower() == 'me':
                                        one_email_info = self.thai_email                                    
                                    if '@' not in one_email_info and one_email_info != '':
                                        tmp_auto_flow = True
                                    list_email.append(one_email_info)
                                    if step_data_info['step_num'] not in list_step_num:
                                        list_step_num.append(step_data_info['step_num'])
                                        json_email['step_num'] = step_data_info['step_num']
                                        json_email['one_email'] = list_email
                                        json_email['activity_code'] = step_data_info['step_detail'][u]['activity_code']
                                        list_acdata = []
                                        for v in range(len(step_data_info['step_detail'][u]['activity_data'])):

                                            if step_data_info['step_detail'][u]['activity_data'][v] == {}:
                                                continue
                            
                                            else:
                                                list_acdata.append(step_data_info['step_detail'][u]['activity_data'][v])
                                        json_email['activity_data'] = list_acdata

                                        if 'A04' in step_data_info['step_detail'][u]['activity_code']:
                                            json_email['activity_code_check'] = True
                                        else:
                                            json_email['activity_code_check'] = False
                                        list_result_email_step.append(json_email)
                        else:
                            for i in range(len(step_data_info)):
                                list_email = []
                                for z in range(len(step_data_info[i]['step_detail'])):
                                    json_email = {}
                                    one_email_info = step_data_info[i]['step_detail'][z]['one_email']
                                    if str(one_email_info).replace(' ','').lower() == 'me':
                                        one_email_info = self.thai_email                                    
                                    if '@' not in one_email_info and one_email_info != '':
                                        tmp_auto_flow = True
                                    # if len(list_step_num) != 0:
                                    list_email.append(one_email_info)
                                    if step_data_info[i]['step_num'] not in list_step_num:
                                        list_step_num.append(step_data_info[i]['step_num'])
                                        json_email['step_num'] = step_data_info[i]['step_num']
                                        json_email['one_email'] = list_email
                                        json_email['activity_code'] = step_data_info[i]['step_detail'][z]['activity_code']
                                        list_acdata = []
                                        if step_data_info[i]['step_detail'][z]['activity_data'] == {}:
                                            json_email['activity_data'] = ''
                                        else:
                                            json_email['activity_data'] = step_data_info[i]['step_detail'][z]['activity_data']

                                        for v in range(len(step_data_info[i]['step_detail'][z]['activity_data'])):

                                            if step_data_info[i]['step_detail'][z]['activity_data'][v] == {}:
                                                continue
                            
                                            else:
                                                list_acdata.append(step_data_info[i]['step_detail'][z]['activity_data'][v])
                                        json_email['activity_data'] = list_acdata
                                        if 'A04' in step_data_info[i]['step_detail'][z]['activity_code']:
                                            json_email['activity_code_check'] = True
                                        else:
                                            json_email['activity_code_check'] = False
                                        list_result_email_step.append(json_email)

                        list_templateCode.append({'auto_flow':tmp_auto_flow,'Template_Name':tmpstep_Name,'Template_Code':tmpstep_Code,'Document_Type':tmpdocumentDetails,'Document_Name':tmpstep_Name,'Condition_Template':tmpcondition_temp,'Template_step':list_result_email_step,'Template_Type':'biz','Template_activity':Temp_activity})
                        count_Template = count_Template + 1
            
            return {'result':'OK','messageText':list_templateCode,'Template_Count':count_Template}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':'notfound data' + str(e)}
        finally:
            connection.close()

    def select_status_business_v1(self,tax_id):
        self.tax_id = tax_id
        try:
            sql = '''select "tb_bizPaperless".status FROM "tb_bizPaperless" where tax_id = :tax_id '''
            connection = slave.connect()
            result = connection.execute(text(sql),tax_id=self.tax_id)
            resultQuery = [dict(row) for row in result]
            if len(resultQuery) != 0:
                data = resultQuery[0]
                return data['status']
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':'notfound data' + str(e)}
        finally:
            connection.close()


    def select_chat_sender_v1(self,sidcode):
        self.sidcode = sidcode
        list_json = []
        list_json2 = []
        arr_step_num = []
        tmplist = []
        tax_id = ''
        json_docuemtn_details = {}
        try:
            sql = '''
                SELECT
                    tb_step_data.sid AS "sid",
                    tb_step_data.data_json AS "data_json",
                    tb_doc_detail.options_page AS "options_page",
                    tb_doc_detail.typefile AS "typefile",
                    tb_doc_detail."documentType" AS "documentType",
                    tb_doc_detail.digit_sign AS "digit_sign",
                    tb_send_detail.send_user AS "send_user",
                    tb_send_detail.send_time AS "send_time",
                    tb_send_detail.sender_name AS "sender_name",
                    tb_send_detail.sender_email AS "sender_email",
                    tb_send_detail.tracking_id AS "tracking_id",
                    tb_send_detail.doc_id AS "document_id",
                    tb_send_detail.template_webhook AS "template_webhook",
                    tb_send_detail.email_center AS "email_center",
                    tb_send_detail.recipient_email AS "recipient_email",
                    tb_send_detail.file_name AS "filename",
                    tb_send_detail.file_id AS "fid",
                    'false' AS "bio_authen" ,
                    "tb_userProfile".p_userid AS "user_id" ,
                    tb_step_data.biz_info AS "biz_info",
                    tb_doc_detail."documentJson" AS "documentJson"
                FROM
                    tb_step_data
                    INNER JOIN tb_doc_detail ON tb_doc_detail.step_id = tb_step_data.sid
                    INNER JOIN tb_send_detail ON tb_send_detail.step_data_sid = tb_step_data.sid
                    INNER JOIN "tb_userProfile" ON "tb_userProfile".p_emailthai = tb_send_detail."sender_email" 
                    OR "tb_userProfile".p_emailthai2 = tb_send_detail."sender_email" 
                    OR "tb_userProfile".p_emailthai3 = tb_send_detail."sender_email" 
                    OR "tb_userProfile".employee_email ILIKE '%'||tb_send_detail."sender_email"||'%' 
                WHERE
                    tb_step_data.sid = :tmpsid
            '''
            connection = slave.connect()
            result = connection.execute(text(sql),tmpsid=self.sidcode)
            resultQuery = [dict(row) for row in result]
            # connection.close()
            if len(resultQuery) > 0:
                tmpdata_json = resultQuery[0]['data_json']
                tmpoptionspage = resultQuery[0]['options_page']
                tmpbiz_info =  resultQuery[0]['biz_info']
                tmpdocumentJson = resultQuery[0]['documentJson']
                tmpdocumentType = resultQuery[0]['documentType']
                try:
                    tmp_json_data_eval = eval(tmpdata_json)
                except Exception as e:
                    raise
                if tmpoptionspage != None:
                    tmpoptionspage = eval(tmpoptionspage)
                    if 'group_detail' in tmpoptionspage:
                        tmp_groupdetail = tmpoptionspage['group_detail']
                        if 'group_status' in tmp_groupdetail:
                            tmp_group_status = tmp_groupdetail['group_status']
                            if tmp_group_status == True:
                                if 'step_num' in tmp_groupdetail:
                                    tmp_step_num_group = tmp_groupdetail['step_num']
                                    for u in range(len(tmp_step_num_group)):
                                        arr_step_num.append(tmp_step_num_group[u])
                if 'step_num' in tmp_json_data_eval:
                    tmplist.append(tmp_json_data_eval)
                    tmp_json_data_eval = tmplist
                for u in range(len(tmp_json_data_eval)):
                    tmp_status_chat = False
                    tmp_status_step_sign = False
                    tmp_json = {}
                    list_email = []
                    list_status = []
                    list_status_ppl = []
                    list_status_Chat = []
                    list_chat_id = []
                    list_chat_id_status =[]
                    list_task_id_status = []
                    list_task_id = []
                    list_state = []
                    tmp_step = tmp_json_data_eval[u]
                    tmp_step_detail = tmp_step['step_detail']
                    tmp_step_num = tmp_step['step_num']
                    tmp_json['step_num'] = tmp_step_num
                    if 'step_sign' in tmp_step:
                        tmp_step_sign = tmp_step['step_sign']
                        tmp_status_step_sign = tmp_step_sign['status']
                        if tmp_status_step_sign == True:
                            print(tmp_status_step_sign)
                    for z in range(len(tmp_step_detail)):
                        tmp_status_chat = False
                        tmp_state = {}
                        tmp_step_details_1 = tmp_step_detail[z]
                        if 'chat_id_status' in tmp_step_details_1:
                            tmp_chat_id_status = bool(tmp_step_details_1['chat_id_status'])
                            list_chat_id_status.append(tmp_chat_id_status)
                        if 'task_id_status' in tmp_step_details_1:
                            tmp_task_id_status = bool(tmp_step_details_1['task_id_status'])
                            list_task_id_status.append(tmp_task_id_status)
                        if 'chat_id' in tmp_step_details_1:
                            tmp_chat_id = tmp_step_details_1['chat_id']
                            list_chat_id.append(tmp_chat_id)
                        if 'task_id' in tmp_step_details_1:
                            tmp_chat_id = tmp_step_details_1['task_id']
                            list_task_id.append(tmp_chat_id)
                        if 'activity_code' in tmp_step_details_1:
                            tmp_activity_code = tmp_step_details_1['activity_code']
                            tmp_activity_status = tmp_step_details_1['activity_status']
                            for u in range(len(tmp_activity_code)):
                                if tmp_activity_code[u] == 'A02':
                                    list_status.append(tmp_activity_status[u])
                                elif tmp_activity_code[u] == 'A03':
                                    list_status_ppl.append(tmp_activity_status[u])
                            if 'A02' in tmp_activity_code:
                                tmp_status_chat = True
                                list_status_Chat.append(tmp_status_chat)
                            else:
                                list_status_Chat.append(tmp_status_chat)
                        tmp_one_email = tmp_step_details_1['one_email']
                        query_Profile = paper_lessuserProfile.query.filter(paper_lessuserProfile.p_emailthai==tmp_one_email).first()
                        if query_Profile != None:
                            if query_Profile.p_taskchat != None:
                                tmp_detail_taskchat = query_Profile.p_taskchat
                                tmp_todo = query_Profile.p_todo
                                tmp_doing = query_Profile.p_doing
                                tmp_done = query_Profile.p_done
                                tmp_state['todo'] = tmp_todo
                                tmp_state['doing'] = tmp_doing
                                tmp_state['done'] = tmp_done
                                list_state.append(tmp_state)
                            else:
                                tmp_state['todo'] = None
                                tmp_state['doing'] = None
                                tmp_state['done'] = None
                                list_state.append(tmp_state)
                        else:
                            tmp_state['todo'] = None
                            tmp_state['doing'] = None
                            tmp_state['done'] = None
                            list_state.append(tmp_state)
                        list_email.append(tmp_one_email)
                    tmp_json['email'] = list_email
                    tmp_json['status_Chat'] = list_status_Chat
                    tmp_json['status'] = list_status
                    tmp_json['status_ppl'] = list_status_ppl
                    tmp_json['chat_id'] = list_chat_id
                    tmp_json['chat_id_status'] = list_chat_id_status
                    tmp_json['chat_state'] = list_state
                    tmp_json['task_id_status'] = list_task_id_status
                    tmp_json['task_id'] = list_task_id
                    tmp_json['status_stepsign'] = tmp_status_step_sign 
                    tmp_json['step_num_group'] = arr_step_num 
                    list_json.append(tmp_json)
                
                document_Name = ''
                document_Type = ''
                document_Remark = ''
                if tmpdocumentJson != None:
                    document_Json = str(tmpdocumentJson)
                    document_Json = eval(document_Json)
                    documentType_data = tmpdocumentType
                    if 'document_remark' in document_Json:
                        document_Name = document_Json['document_name']
                        document_Type = document_Json['document_type']
                        document_Remark = document_Json['document_remark']
                if tmpbiz_info != None and tmpbiz_info!= 'None':
                    biz_data = eval(tmpbiz_info)
                    tax_id = biz_data['id_card_num']
                else:
                    tax_id = ''
                if tax_id != '':
                    sqlchat = '''
                        SELECT
                            tb_document_detail.chat_bot AS "chat_bot" 
                        FROM
                            tb_document_detail 
                        WHERE
                            tb_document_detail."documentType" = :tmpdocumentType 
                            AND tb_document_detail.biz_info IS NOT NULL 
                            AND tb_document_detail.biz_info != ''
                            AND ( tb_document_detail.biz_info LIKE '%%' || :tmptax_id || '%%' ) 
                        '''
                    resultChatBot = connection.execute(text(sqlchat),tmpdocumentType=documentType_data,tmptax_id=tax_id)
                    resultQueryChatBot = [dict(row) for row in resultChatBot]
                    tmpresultQueryChatBot = resultQueryChatBot[0]['chat_bot']
                    try:
                        json_docuemtn_details['chat_bot_details'] = eval(tmpresultQueryChatBot)
                    except Exception as e:
                        json_docuemtn_details['chat_bot_details'] = None
                else:
                    sqlchat = '''
                        SELECT
                            tb_document_detail.chat_bot AS "chat_bot" 
                        FROM
                            tb_document_detail 
                        WHERE
                            tb_document_detail."documentType" = :tmpdocumentType 
                            AND tb_document_detail.biz_info IS  NULL 
                            AND tb_document_detail.biz_info = ''
                        '''
                    resultChatBot = connection.execute(text(sqlchat),tmpdocumentType=documentType_data)
                try:
                    tmprecipient_email = eval(resultQuery[0]['recipient_email'])
                except Exception as e:
                    tmprecipient_email = None
                tmpbody_text = ['เอกสารที่ต้องอนุมัติ','']
                tmpbtn_text = ['Approve','Reject']
                if len(tmpoptionspage) != 0:
                    tmpbody_text = [str(tmpoptionspage['subject_text']),str(tmpoptionspage['body_text'])]
                try:
                    tmpsender_name = eval(resultQuery[0]['sender_name'])
                    tmpsender_name = tmpsender_name['th'] + '\n' + tmpsender_name['eng']
                except Exception as e:
                    print(str(e))
                    tmpsender_name = resultQuery[0]['sender_name']
                    # tmpsender_name_eng = resultQuery[0]['sender_name']
                try:
                    tmpsender_name_eng = eval(resultQuery[0]['sender_name'])
                    tmpsender_name_eng = tmpsender_name_eng['eng']
                except Exception as e:
                    tmpsender_name_eng = resultQuery[0]['sender_name']
                tmp_json = {
                    'user_id':resultQuery[0]['user_id'],
                    'send_user':resultQuery[0]['send_user'],
                    'send_time':resultQuery[0]['send_time'],
                    'sender_name':tmpsender_name,
                    'sender_email':resultQuery[0]['sender_email'],
                    'tracking_id':resultQuery[0]['tracking_id'],
                    'document_id':resultQuery[0]['document_id'],
                    'template_webhook':resultQuery[0]['template_webhook'],
                    'email_center':resultQuery[0]['email_center'],
                    'recipient_email':tmprecipient_email,
                    'typefile':resultQuery[0]['typefile'],
                    'documentType':resultQuery[0]['documentType'],
                    'digit_sign':resultQuery[0]['digit_sign'],
                    'options_page':resultQuery[0]['options_page'],
                    'body_text':tmpbody_text,
                    'button_text':tmpbtn_text,
                    'task_btn_text':['View Detail'],
                    'bio_authen':resultQuery[0]['bio_authen'],
                    'filename':resultQuery[0]['filename'],
                    'fid':resultQuery[0]['fid'],
                    'sender_name_eng':tmpsender_name_eng
                }
                data_json_result = {
                    'documentType_Details':[json_docuemtn_details]
                }
                return {'result':'OK','messageText':list_json,'data':tmp_json,'datachat':data_json_result}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':'notfound data' + str(e)}
        finally:
            connection.close()

    def select_tax_id_for_migrate(self):
        list_data = []
        time_now = int(time.time())
        time_reverse = time_now - int(1296000)
        strf_datetime_end = datetime.datetime.fromtimestamp(time_now).strftime('%Y-%m-%d %H:%M:%S')
        strf_datetime_start = datetime.datetime.fromtimestamp(time_reverse).strftime('%Y-%m-%d')
        start_datetime = str(strf_datetime_start) + 'T00:00:00'
        end_datetime = str(strf_datetime_end)
        try:
            # sql = """ 
            #     SELECT biz_info,step_data_sid
            #     FROM "tb_doc_detail"
            #     INNER JOIN "tb_send_detail_copy" ON "tb_send_detail_copy".step_data_sid = "tb_doc_detail".step_id
            #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_doc_detail".step_id
            #     WHERE "tb_send_detail_copy".tax_id IS NULL 
            #     AND ("tb_send_detail_copy"."send_time" BETWEEN (:start_datetime) AND (:end_datetime))
            # """
            sql = """ 
                SELECT biz_info,step_data_sid
                FROM "tb_doc_detail"
                INNER JOIN "tb_send_detail" ON "tb_send_detail".step_data_sid = "tb_doc_detail".step_id
                INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_doc_detail".step_id
                WHERE "tb_send_detail".tax_id IS NULL 
                
            """
            with engine.connect() as connection:
                result = connection.execute(text(sql),start_datetime=start_datetime,end_datetime=end_datetime)
                connection.close()
            query_result = [dict(row) for row in result] 
            if query_result == []:
                return {'result':'ER','messageText':'no data'}  
            # print ('query_result:',query_result)
            for i in range(len(query_result)):
                biz_info = (query_result[i]['biz_info'])
                if biz_info != None and biz_info != '' and biz_info != 'None':
                    biz_info = eval(query_result[i]['biz_info'])
                    sid = query_result[i]['step_data_sid']
                    tax_id = biz_info['id_card_num']
                    tmp_data = {
                        'sid': sid,
                        'tax_id' : tax_id
                    }
                    list_data.append(tmp_data)
                else:
                    sid = query_result[i]['step_data_sid']
                    tmp_data = {
                        'sid': sid,
                        'tax_id' : None
                    }
            return {'result':'OK','messageText':list_data}  
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def select_sender_for_migrate(self):
        try:
            search_dict = "%{}%".format('eng')
            time_now = int(time.time())
            time_reverse = time_now - int(1296000)
            strf_datetime_end = datetime.datetime.fromtimestamp(time_now).strftime('%Y-%m-%d %H:%M:%S')
            strf_datetime_start = datetime.datetime.fromtimestamp(time_reverse).strftime('%Y-%m-%d')
            start_datetime = str(strf_datetime_start) + 'T00:00:00'
            end_datetime = str(strf_datetime_end)
            # print ('start_datetime:',start_datetime)
            # print ('end_datetime:',end_datetime)

            # with slave.connect() as connection:
            #     result = connection.execute(text(''' SELECT "sender_name","send_user","step_data_sid" 
            #     FROM "tb_send_detail" WHERE "sender_name" NOT LIKE :name 
            #     AND ("tb_send_detail"."send_time" BETWEEN (:start_datetime) AND (:end_datetime)) 
            #     '''),name=search_dict,start_datetime=start_datetime,end_datetime=end_datetime)
            #     connection.close()
            
            # บริษัทนิงฮง
            with slave.connect() as connection:
                result = connection.execute(text(''' SELECT "sender_name","send_user","step_data_sid","tax_id" 
                FROM "tb_send_detail" WHERE "sender_name" NOT LIKE :name
                AND "tax_id" = '0105542064905' 
                '''),name=search_dict)
                connection.close()

            query_result = [dict(row) for row in result]
            # print ('query_result:',query_result)
            if query_result == []:
                return {'result':'ER','messageText':'no data to migrate'}  
            # print ('query_result:',query_result)
            return {'result':'OK','messageText':query_result}
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def select_status_document_v1(self,sid):
        self.sid = sid
        try:
            sql = '''
                SELECT
                    tb_send_detail.document_status,                    
	                tb_doc_detail."documentType" 
                FROM
                    tb_send_detail
                    INNER JOIN tb_doc_detail ON tb_doc_detail.step_id = tb_send_detail.step_data_sid 
                WHERE
                    step_data_sid =:tmpsid 
            '''
            with slave.connect() as connection:
                result = connection.execute(text(sql),tmpsid=self.sid)
            connection.close()
            data = [dict(row) for row in result]
            statusDoc = data[0]['document_status']
            tmpdocumentType = data[0]['documentType']
            return {'result':'OK','messageText':{'status_file_code':statusDoc,'document_type':tmpdocumentType}}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result': 'ER', 'messageText': str(e),'status_Code':200}

    def select_status_nameservice(self,tax_id):
        self.tax_id = tax_id
        try:
            arrtmp = []
            with slave.connect() as connection:
                result = connection.execute(text('''SELECT config FROM "tb_bizPaperless" WHERE "tax_id"=:tax_id'''),tax_id=self.tax_id)
                connection.close()
            query_result = [dict(row) for row in result]
            # print ('query_result:',query_result)
            if query_result != []:
                result_config = eval(query_result[0]['config'])
            else:
                result_config = query_result
            
            return {"result":"OK","data":result_config}  
        except Exception as e:
            print (str(e))
            return {"result":"ER","data":None}  

    def select_docid_v1(self,docid_arr):
        self.docid_arr = docid_arr
        arrtmpsid = []
        try:
            sql = '''
                SELECT "step_data_sid" FROM "public"."tb_send_detail" WHERE "doc_id" IN :tmpdocid
            '''
            with slave.connect() as connection:
                result = connection.execute(text(sql),tmpdocid = self.docid_arr)
            connection.close()
            query_result = [dict(row) for row in result]
            for u in range(len(query_result)):
                arrtmpsid.append(query_result[u]['step_data_sid'])
            return arrtmpsid
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result': 'ER', 'messageText': str(e),'status_Code':200}
        
    def select_group_id(self):
        try:
            sql = '''
                SELECT "id" FROM "public"."tb_group_document"
            '''
            with slave.connect() as connection:
                result = connection.execute(text(sql))
            connection.close()
            query_result = [dict(row) for row in result]
            return query_result
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result': 'ER', 'messageText': str(e),'status_Code':200}

    def select_update_group_status_v1(self,group_id):
        self.group_id = group_id
        try:
            sql = '''
                SELECT "status_group" FROM "public"."tb_group_document" where "id" =:tmpgid
            '''
            with slave.connect() as connection:
                result = connection.execute(text(sql),tmpgid=self.group_id)
            connection.close()
            query_result = [dict(row) for row in result]
            if len(query_result) != 0:
                try:
                    query_result =query_result[0]['status_group']
                    query_result = eval(query_result)
                except Exception as e:
                    return {'result':'ER','data':None}
                r = cal_status_group_v1(query_result)
                tmpstatus = r['messageText']
                update_4().update_status_group_v1(self.group_id,tmpstatus)
                return {"result":"OK","data":query_result}  
            else:
                return {'result':'ER','data':None}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result': 'ER', 'messageText': str(e),'status_Code':200}
    
    def select_get_action_and_status_v2(self,action_name):
        self.action_name = action_name
        try:
            sql = '''
                SELECT
                    tb_action_status.name_action AS "name_action",
                    tb_action_status.status AS "status" 
                FROM
                    tb_action_status 
                WHERE
                    tb_action_status.name_action =:tmpaction_name 
            '''
            with slave.connect() as connection:
                result = connection.execute(text(sql),tmpaction_name=self.action_name)
                connection.close()
            query = [dict(row) for row in result]
            if len(query) > 0:
                return {'result':'OK','messageText':{'status':query[0]['status']}}
            else:
                return {'result':'OK','messageText':{'status':False}}
        except Exception as e:
            return {'result':'ER','messageText':None,'messageER':'notfound data' + str(e)}

    def select_ForWebHook_group_v1(self,group_id):
        self.group_id = group_id
        result_json = {}
        arr_res = []
        infoGroup = {}
        tmpdataGroup = []
        try:
            sql = '''
                SELECT 
                    sid_group,
                    webhook,
                    tracking_group,
                    group_data_json,
                    status_group,
                    maxstep
                FROM "tb_group_document" 
                WHERE id = :tmpgroup_id
            '''
            with slave.connect() as connection:
                result = connection.execute(text(sql),tmpgroup_id=self.group_id)
                connection.close()
            query = [dict(row) for row in result]
            if len(query) != 0:
                res = query[0]
                sid_grp = res['sid_group']
                webhook = res['webhook']
                tracking_group = res['tracking_group']
                group_data_json = res['group_data_json']
                status_group = res['status_group']
                maxstep = res['maxstep']
                try:
                    status_group = eval(status_group)
                except Exception as e:
                    status_group = None
                try:
                    group_data_json = eval(group_data_json)
                    for i in range(len(group_data_json)):
                        tmpdataGroup.append(group_data_json[i][0])
                except Exception as e:
                    group_data_json = None
                try:
                    sid_grp = eval(sid_grp)
                except Exception as e:
                    sid_grp = sid_grp
                infoGroup = {
                    "group_tracking":tracking_group,
                    "group_data":tmpdataGroup,
                    "group_webhook":webhook,
                    "document_count":len(sid_grp),
                    "group_step":status_group,
                    "maxstep":maxstep
                }
                if len(sid_grp) != 0:
                    sid_grp = tuple(sid_grp)
                    sql = ''' 
                        SELECT
                            tsd."template_webhook" AS "webHook",
                            tsd."email_center",
                            tsd."sender_name" AS "userSender",
                            tsd."sender_email" AS "emailSender",
                            tsd."file_name" AS "fileName",
                            tsd."tracking_id" AS "trackingId",
                            tsd."sender_email" AS "sender_email",
                            tsd."send_time" AS "send_time",
                            tdoc."document_id" AS "documentId",
                            tdoc."attempted_folder" AS "attempted_folder",
                            tdoc."data_document" AS "data_document",
                            tbf."pathfolder" AS "pathfolder",
                            tbf."json_data" AS "json_data",
                            tstd."biz_info" AS "biz_info",
                            tdoc."documentJson" AS "documentJson",
                            tdoc."options_page" AS "options_page",
                            tbpdf."string_sign" AS "string_sign",
                            tbpdf."string_pdf" AS "string_pdf" ,
                            tstd."data_json" AS "step_json" ,
                            tsd."stepnow" AS "stepnow" ,
                            tsd."stepmax" AS "stepmax",
                            tsd."status" AS "status"
                        FROM
                            "tb_send_detail" tsd
                            LEFT JOIN tb_doc_detail tdoc ON tdoc.step_id = tsd.step_data_sid
                            LEFT JOIN tb_step_data tstd ON tstd.sid = tsd.step_data_sid
                            LEFT JOIN tb_transactionfile tbf ON tbf.folder_name = tdoc.attempted_folder
                            LEFT JOIN "tb_userProfile" tbpf ON tbpf.p_username = tsd.send_user
                            LEFT JOIN tb_pdf_storage tbpdf ON tbpdf.fid = tdoc.fileid 
                        WHERE
                            step_data_sid IN :tmpsid 
                        '''
                    with slave.connect() as connection:
                        result = connection.execute(text(sql),tmpsid=sid_grp)
                        connection.close()
                    queryDoc = [dict(row) for row in result]
            if len(queryDoc) != 0:
                for n in range(len(queryDoc)):
                    res = queryDoc[n]
                    result_json['webHook'] = res['webHook']
                    try:
                        result_json['email_center'] = eval(res['email_center'])
                    except Exception as e:
                        result_json['email_center'] = None
                    try:
                        userSender = eval(res['userSender'])
                        result_json['userSender'] = userSender['th'] 
                        result_json['userSender_eng'] = userSender['eng'] 
                    except Exception as e:
                        result_json['userSender'] = userSender
                        result_json['userSender_eng'] = userSender
                    result_json['emailSender'] = res['emailSender']
                    result_json['fileName'] = res['fileName']
                    result_json['trackingId'] = res['trackingId']
                    result_json['sender_email'] = res['sender_email']
                    result_json['documentId'] = res['documentId']
                    result_json['datetime'] = str(res['send_time'])
                    result_json['attchfile_path'] = None
                    result_json['attchfile_json'] = None
                    result_json['attempted_folder'] = res['attempted_folder']
                    if res['attempted_folder'] != None:
                        result_json['attchfile_path'] = res['pathfolder']
                        result_json['attchfile_json'] = eval(str(res['json_data']))
                    tmpdata = data_doc(res['data_document'])
                    if tmpdata['result'] == 'OK':
                        tmpdataDoc = tmpdata['messageText']
                    else:
                        tmpdataDoc = None
                    result_json['data_document'] = tmpdataDoc
                    result_json['business'] = res['biz_info']
                    if result_json['business'] != None or result_json['business'] != 'None' or result_json['business'] != '':
                        result_json['business'] = eval(result_json['business'])
                    if result_json['business'] != None:
                        if 'business' in result_json:
                            if 'data_details_biz' in result_json['business']:
                                del result_json['business']['data_details_biz']
                    if res['string_sign'] != None:
                        result_json['PDF_String'] = res['string_sign']
                    else:
                        result_json['PDF_String'] = res['string_pdf']
                    result_json['documentTypeDetail'] = eval(res['documentJson'])
                    try:
                        result_json['body'] = eval(res['options_page'])['body_text']
                    except Exception as e:
                        result_json['body'] = None
                    result_json['data_document_2'] = None
                    try:
                        tmp_service_po = eval(res['options_page'])
                        if 'service_properties' in tmp_service_po:
                            tmp_service_po = tmp_service_po['service_properties']
                            for x in range(len(tmp_service_po)):
                                if tmp_service_po[x]['name_service'] == 'GROUP':
                                    if tmp_service_po[x]['status'] == True:
                                        result_json['data_document_2'] = tmp_service_po[x]['other'][0]['properties']
                    except Exception as e:
                        print(str(e))
                        result_json['data_document_2'] = None
                    result_json['stepnow'] = res['stepnow']
                    result_json['stepmax'] = res['stepmax']
                    result_json['status'] = res['status']
                    r_calstep = cal_dataJson_stepWH_v1(eval(res['step_json']))
                    if r_calstep['result'] == 'OK':
                        result_json['step_json'] = r_calstep['messageText']
                    else:
                        result_json['step_json'] = None
                    arr_res.append(result_json)
            info = {
                "group_detail":infoGroup,
                "document_detail":arr_res
            }
            return {'result': 'OK', 'messageText': info,'status_Code':200}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result': 'ER', 'messageText': str(e),'status_Code':200}

    def select_ForWebHook_v2(self,sidcode):
        self.sidcode = sidcode
        result_json = {}
        try:
            sql = ''' 
                SELECT
                    tsd."template_webhook" AS "webHook",
                    tsd."email_center",
                    tsd."sender_name" AS "userSender",
                    tsd."sender_email" AS "emailSender",
                    tsd."file_name" AS "fileName",
                    tsd."tracking_id" AS "trackingId",
                    tsd."sender_email" AS "sender_email",
                    tsd."send_time" AS "send_time",
                    tdoc."document_id" AS "documentId",
                    tdoc."attempted_folder" AS "attempted_folder",
                    tdoc."data_document" AS "data_document",
                    tbf."pathfolder" AS "pathfolder",
                    tbf."json_data" AS "json_data",
                    tstd."biz_info" AS "biz_info",
                    tdoc."documentJson" AS "documentJson",
                    tdoc."options_page" AS "options_page",
                    tbpdf."string_sign" AS "string_sign",
                    tbpdf."string_pdf" AS "string_pdf" ,
                    tstd."data_json" AS "step_json" ,
                    tsd."stepnow" AS "stepnow" ,
                    tsd."stepmax" AS "stepmax",
                    tsd."status" AS "status"
                FROM
                    "tb_send_detail" tsd
                    LEFT JOIN tb_doc_detail tdoc ON tdoc.step_id = tsd.step_data_sid
                    LEFT JOIN tb_step_data tstd ON tstd.sid = tsd.step_data_sid
                    LEFT JOIN tb_transactionfile tbf ON tbf.folder_name = tdoc.attempted_folder
                    LEFT JOIN "tb_userProfile" tbpf ON tbpf.p_username = tsd.send_user
                    LEFT JOIN tb_pdf_storage tbpdf ON tbpdf.fid = tdoc.fileid 
                WHERE
                    step_data_sid = :tmpsid 
                '''
            with slave.connect() as connection:
                result = connection.execute(text(sql),tmpsid=self.sidcode)
                connection.close()
            query = [dict(row) for row in result]
            if len(query) != 0:
                res = query[0]
                result_json['webHook'] = res['webHook']
                try:
                    result_json['email_center'] = eval(res['email_center'])
                except Exception as e:
                    result_json['email_center'] = None
                
                try:
                    userSender = eval(res['userSender'])
                    result_json['userSender'] = userSender['th'] 
                    result_json['userSender_eng'] = userSender['eng'] 
                except Exception as e:
                    userSender = res['userSender']
                    result_json['userSender'] = userSender
                    result_json['userSender_eng'] = userSender
                result_json['emailSender'] = res['emailSender']
                result_json['fileName'] = res['fileName']
                result_json['trackingId'] = res['trackingId']
                result_json['sender_email'] = res['sender_email']
                result_json['documentId'] = res['documentId']
                result_json['datetime'] = str(res['send_time'])
                result_json['attchfile_path'] = None
                result_json['attchfile_json'] = None
                result_json['attempted_folder'] = res['attempted_folder']
                if res['attempted_folder'] != None:
                    try:
                        result_json['attchfile_path'] = res['pathfolder']
                        result_json['attchfile_json'] = eval(str(res['json_data']))
                        for i in range(len(result_json['attchfile_json'])):
                            result_json['attchfile_json'][i]['url_download'] = myUrl_domain + 'storage/downloadfile/v1/' + res['attempted_folder'] + '/'+ result_json['attchfile_json'][i]['file_name_new']
                    except:
                        result_json['attchfile_path'] = None,
                        result_json['attchfile_json'] = []
                tmpdata = data_doc(res['data_document'])
                if tmpdata['result'] == 'OK':
                    tmpdataDoc = tmpdata['messageText']
                else:
                    tmpdataDoc = None
                result_json['data_document'] = tmpdataDoc
                result_json['business'] = res['biz_info']
                if result_json['business'] != None or result_json['business'] != 'None' or result_json['business'] != '':
                    result_json['business'] = eval(result_json['business'])
                if result_json['business'] != None:
                    if 'business' in result_json:
                        if 'data_details_biz' in result_json['business']:
                            del result_json['business']['data_details_biz']
                if res['string_sign'] != None:
                    result_json['PDF_String'] = res['string_sign']
                else:
                    result_json['PDF_String'] = res['string_pdf']
                result_json['documentTypeDetail'] = eval(res['documentJson'])
                try:
                    result_json['body'] = eval(res['options_page'])['body_text']
                except Exception as e:
                    result_json['body'] = None
                result_json['data_document_2'] = None
                try:
                    tmp_service_po = eval(res['options_page'])
                    if 'service_properties' in tmp_service_po:
                        tmp_service_po = tmp_service_po['service_properties']
                        for x in range(len(tmp_service_po)):
                            if tmp_service_po[x]['name_service'] == 'GROUP':
                                if tmp_service_po[x]['status'] == True:
                                    result_json['data_document_2'] = tmp_service_po[x]['other'][0]['properties']
                except Exception as e:
                    print(str(e))
                    result_json['data_document_2'] = None
                result_json['stepnow'] = res['stepnow']
                result_json['stepmax'] = res['stepmax']
                result_json['status'] = res['status']
                r_calstep = cal_dataJson_stepWH_v1(eval(res['step_json']))
                if r_calstep['result'] == 'OK':
                    result_json['step_json'] = r_calstep['messageText']
                else:
                    result_json['step_json'] = None
            return {'result': 'OK', 'messageText': result_json,'status_Code':200}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result': 'ER', 'messageText': str(e),'status_Code':200}

    def select_RefDocumnet(self,sid):
        self.sid = sid
        try:
            status_refDocument = False
            sql = """ 
                SELECT "ref_document" FROM "public"."tb_send_detail" where "step_data_sid" = '""" + self.sid + """'
            """
            with slave.connect() as connection:
                result = connection.execute(text(sql))
                connection.close()
            query_result = [dict(row) for row in result]
            for x in query_result:
                tmpref_document = x['ref_document']
                if tmpref_document != None:
                    status_refDocument = True
            # print(status_refDocument)
            return {'result':'OK','message':status_refDocument}
        except Exception as e:
            return {'result':'ER','message':str(e)}
        
    
    def select_taxId_Admin(self):
        try:
            arrtmp = []
            sql = """ 
                SELECT a.status as "status",a."transactionMax" as "transactionMax",a."storageMax" as "storageMax",a."update_date" as "update_date",a."transactionNow" as "transactionNow",a."storageNow" as "storageNow",a."config" as "config",
                a.tax_id as "id_card_num",b."bizInfoJson" FROM "tb_bizPaperless" a LEFT JOIN "tb_bizProfile" b on b."bizTax" = a."tax_id"
            """
            with slave.connect() as connection:
                result = connection.execute(text(sql))
                connection.close()
            query_result = [dict(row) for row in result]
            for x in query_result:
                tmpid = None
                tmpid_card_type = None
                tmpfirst_name_th = None
                tmpfirst_name_eng = None
                try:
                    x['bizInfoJson'] = eval(x['bizInfoJson'])
                except Exception as e:
                    x['bizInfoJson'] = None
                try:
                    x['config'] = eval(x['config'])
                except Exception as e:
                    x['config'] = None
                if x['update_date'] != None:
                    x['update_date'] = str(x['update_date']).split('+')[0]
                tmpbizInfoJson = x['bizInfoJson']
                if tmpbizInfoJson != None:
                    tmpid = tmpbizInfoJson['id']
                    tmpid_card_type = tmpbizInfoJson['id_card_type']
                    tmpfirst_name_th = tmpbizInfoJson['first_name_th']
                    tmpfirst_name_eng = tmpbizInfoJson['first_name_eng']
                infojson = {
                    "id":tmpid,
                    "id_card_num":x['id_card_num'],
                    "id_card_type":tmpid_card_type,
                    "first_name_th":tmpfirst_name_th,
                    "first_name_eng":tmpfirst_name_eng,
                    "status":x['status'],
                    "transactionMax":x['transactionMax'],
                    "storageMax":x['storageMax'],
                    "update_date":x['update_date'],
                    "transactionNow":x['transactionNow'],
                    "storageNow":x['storageNow'],
                    "config":x['config']
                }          
                arrtmp.append(infojson)
            list_arr = sorted(arrtmp, key=lambda k: k['id_card_num'], reverse=False)
            print(list_arr)
            return {'result':'OK',"messageText": list_arr,'count':len(list_arr)}
        except Exception as e:
            return {"result":"ER","messageText":"select_taxId_Admin => " + str(e),'count':0}  
        
    def select_taxId_serviceCall(self):
        try:
            arrtmp = []
            sql = """ 
                SELECT tax_id,config FROM "tb_bizPaperless"
            """
            with slave.connect() as connection:
                result = connection.execute(text(sql))
                connection.close()
            query_result = [dict(row) for row in result]
            for x in query_result:
                arrtmp.append(x['tax_id'])
            return {"result":"OK","data":query_result,'tax_id':arrtmp}  
        except Exception as e:
            return {"result":"ER","data":None}  

    def select_pdfbase64(self):
        try:
            sql = """ 
                SELECT fid as file_id,string_pdf as base64file 
                FROM "tb_pdf_storage"
                INNER JOIN "tb_send_detail" ON "tb_send_detail".file_id = "tb_pdf_storage".fid
                WHERE tb_send_detail."filesize" IS NULL ORDER BY "tb_send_detail".send_time DESC LIMIT 1000 
            """
            with slave.connect() as connection:
                result = connection.execute(text(sql))
                connection.close()
            query_result = [dict(row) for row in result]     
            return query_result     
        except Exception as e:
            print(str(e))

    def select_transactionNow_business(self,tmplisttax_id,dtm_start,dtm_end):
        self.tmplisttax_id = tmplisttax_id
        self.dtm_start = dtm_start
        self.dtm_end = dtm_end
        # print(self.dtm_start , self.dtm_end)
        sql_when = ''
        sql_when2 = ''
        sql_when3 = ''
        for i in range(len(self.tmplisttax_id)):
            tmptax_id = self.tmplisttax_id[i]
            sql_when += """WHEN biz_info LIKE '%"""+tmptax_id+"""%' THEN '""" +tmptax_id+ """'"""
            sql_when2 += """WHEN biz_info LIKE '%"""+tmptax_id+"""%' AND tb_send_detail."transaction" IS NULL THEN '1' ELSE '2' """
            sql_when3 += """WHEN biz_info LIKE '%"""+tmptax_id+"""%' AND tb_send_detail."transaction" IS NULL THEN '""" +tmptax_id+ """'"""
        try:
            sql = """ 
                    SELECT
                    MAX(CASE
                        """ + sql_when + """
                        ELSE NULL
                    END) AS tax_id,
                    MAX ( CASE """ +sql_when2+ """ END ) AS "transaction",
                    COUNT("sid"),
                    (SUM(CAST(
                            COALESCE(
                                NULLIF(
                                    regexp_replace(filesize, '[^-0-9.]+', '', 'g'), 
                                    ''),
                                '0')
                        AS numeric))) AS sum_filesize,
                    (SUM(CAST(
                            COALESCE(
                                NULLIF(
                                    regexp_replace(storage, '[^-0-9.]+', '', 'g'), 
                                    ''),
                                '0')
                        AS numeric))) AS sum_filesize_storage
                    FROM
                    "tb_send_detail"
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid
                    LEFT JOIN "tb_transactionfile" ON "tb_transactionfile".folder_name = "tb_doc_detail".attempted_folder
                    WHERE "upload_time" >= '""" + self.dtm_start + """' AND "upload_time" <= '""" + self.dtm_end + """' AND biz_info LIKE '%""" + tmptax_id + """%' 
                    GROUP BY
                    CASE
                        """ + sql_when3 + """
                        ELSE NULL
                    END 
                """
            sql_storage = """ SELECT
                    CASE
                        """ + sql_when + """
                        ELSE NULL
                    END AS tax_id,
                    (SUM(CAST(
                            COALESCE(
                                NULLIF(
                                    regexp_replace(filesize, '[^-0-9.]+', '', 'g'), 
                                    ''),
                                '0')
                        AS numeric))) AS sum_filesize
                    FROM
                    "tb_send_detail"
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid
                    WHERE "upload_time" >= '""" + self.dtm_start + """' AND "upload_time" <= '""" + self.dtm_end + """'
                    GROUP BY
                    CASE
                        """ + sql_when3 + """
                        ELSE NULL
                    END 
                """
            # print(sql)
            with slave.connect() as connection:
                result = connection.execute(text(sql))
                # result_storage = connection.execute(text(sql_storage))
                connection.close()
            query_result = [dict(row) for row in result] 
            # query_result_storage = [dict(row) for row in result_storage]    
            # print(query_result)  
            return query_result     
        except Exception as e:
            print(str(e))

    def select_transactionMax_business(self,tax_id):
        self.tax_id = tax_id
        try:
            if self.tax_id == 'all':
                sql = """ SELECT "tax_id" as tax_id,"status" as status,"transactionMax" as transactionMax,"storageMax" as storageMax FROM "tb_bizPaperless" """
            else:
                sql = """ SELECT "tax_id" as tax_id,"status" as status,"transactionMax" as transactionMax,"storageMax" as storageMax FROM "tb_bizPaperless" WHERE tax_id=:tax_id """
            with engine.connect() as connection:
                result = connection.execute(text(sql),tax_id=self.tax_id)
                connection.close()
            query_result = [dict(row) for row in result]     
            return query_result     
        except Exception as e:
            print(str(e))

    def select_data_Userprofile_v1(self,username):
        self.username = username
        try:
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "p_username" AS "Username","p_updateTime" AS updateUser_Time,"p_webHook" AS webhook,"p_emailthai" AS "email_thai","p_emailthai2" AS "email_thai2","p_emailthai3" AS "email_thai3","p_webHook" AS webhook,"p_sign" AS "signString","p_emailUser" AS emailUser,\
                    "p_options","p_signca","permission_id","pic_profile","employee_email" \
                    FROM "tb_userProfile"  WHERE "p_username" = :username'),username=self.username)
                connection.close()
            query_result = [dict(row) for row in result]
            tmp_statusca = None
            if len(query_result) != 0:
                for i in range(len(query_result)):
                    element = query_result[i]                    
                    if element['p_signca'] == 'Y':
                        tmp_statusca = 'พบข้อมูล CA'
                    else:
                        tmp_statusca = 'ไม่พบข้อมูล CA'
                    element['signCa_status'] = element['p_signca']
                    element['signCA'] = tmp_statusca
                    if element['employee_email'] != None:
                        try:
                            element['employee_email'] = eval(element['employee_email'])
                        except Exception as e:
                            element['employee_email'] = None
                    else:
                        element['employee_email'] = None
                    if element['p_options'] != None:
                        try:
                            element['options'] = eval(element['p_options'])
                        except Exception as e:
                            element['options'] = None
                    else:
                        element['options'] = None
                    element['permission_detail'] = None
                    if element['permission_id'] != None:
                        with slave.connect() as connection:
                            result = connection.execute(text('SELECT "name","role_level","permis_send_approve","permis_create_doc","permis_sign_doc","permis_view_doc","permis_cancel_doc","permis_doc_format","permis_doc_type" \
                                FROM "tb_permission"  WHERE "id"::TEXT = :permission_id'),permission_id=element['permission_id'])
                            connection.close()
                        query_permission = [dict(row) for row in result]
                        if len(query_permission) !=0 :
                            element['permission_detail'] = query_permission[0]
                        else:
                            element['permission_detail'] = None
                    del element['permission_id']
                    del element['p_options']
                    del element['p_signca']
                return ({'result':'OK','data':query_result[0]})
            else:
                return ({'result':'ER','data':None})
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','data':'select_data_Userprofile_v1 fail' + str(e),'messageER':str(e),'status_Code':200}),200

    def select_data_business_v1(self,email):
        self.email = email
        search_email = "%'{}'%".format(self.email)
        try:
            with engine.connect() as connection:
                result = connection.execute(text('SELECT "biz_information" FROM "tb_citizen_Login" WHERE "citizen_data" LIKE :email'),email=search_email)
                connection.close()
            query_result = [dict(row) for row in result]
            if len(query_result) != 0:
                return ({'result':'OK','data':query_result})
            else:
                return ({'result':'ER','data':None})
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_PaperlessToken_v1(self,tokenppl):
        self.tokenppl = tokenppl
        try:
            with engine.connect() as connection:
                result = connection.execute(text('SELECT "service_name","token" FROM "tb_paperless_token" WHERE "token" = :tokenppl'),tokenppl=self.tokenppl)
                connection.close()
            query_result = [dict(row) for row in result]
            if len(query_result) != 0:
                return ({'result':'OK','data':query_result})
            else:
                return ({'result':'ER','data':None})
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_service_id(self,name):
        self.name = name
        search = "%{}%".format(self.name)
        try:
            with engine.connect() as connection:
                result = connection.execute(text('SELECT "code","private" FROM "tb_connex" WHERE "serviceName" LIKE :serviceName'),serviceName=search)
                connection.close()
            query_result = [dict(row) for row in result]
            # print(query_result)
            if len(query_result) != 0:
                return ({'result':'OK','data':query_result})
            else:
                return ({'result':'ER','data':None})
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_pdfstring_v1(self):
        try:
            with engine.connect() as connection:
                result = connection.execute(text('SELECT "fid","string_pdf","hash_pdf","string_sign","hash_sign","path" FROM "tb_pdf_storage" WHERE "path" IS :js_path ORDER BY "fid" ASC LIMIT (100)'),js_path=None)
                connection.close()
            query_result = [dict(row) for row in result]
            if len(query_result) != 0:
                return ({'result':'OK','data':query_result})
            else:
                return ({'result':'ER','data':None})
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_dept_document_type_v1(self,document_type,tax_id):
        self.document_type = document_type
        self.tax_id = tax_id
        self.status = 'ACTIVE'
        try:
            where_sql = ''
            search_tax_id = "'%{}%'".format(self.tax_id)
            if self.tax_id != '':
                where_sql += ' AND "tb_document_detail".biz_info LIKE ' + search_tax_id
            else:
                where_sql += ' AND ("tb_document_detail".biz_info = :biz_info_none OR "tb_document_detail".biz_info = :biz_info)'
            text_sql = text('SELECT "biz_info" FROM "tb_document_detail" WHERE "documentStatus"=:documentStatus AND "documentType"=:document ' + where_sql)
            with engine.connect() as connection:
                    result = connection.execute(text_sql,document=self.document_type,biz_info='',biz_info_none='None',documentStatus='ACTIVE')
                    connection.close()
            query_result = [dict(row) for row in result]
            if len(query_result) != 0:
                return ({'result':'OK','data':query_result})
            else:
                return ({'result':'ER','data':None})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_dataeformfor_rpa_v1(self,sidcode):
        self.sidcode = sidcode
        try:
            with engine.connect() as connection:
                result = connection.execute('''SELECT "data_document" FROM "tb_doc_detail" WHERE "step_id"= %s ''',self.sidcode)
                connection.close()
            query_result = [dict(row) for row in result]
            if len(query_result) != 0:
                return ({'result':'OK','data':query_result})
            else:
                return ({'result':'ER','data':None})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_permission(self,permission_id):
        self.permission_id = permission_id
        try:
            list_arr = []
            with engine.connect() as connection:
                tmp_query = connection.execute('''SELECT * FROM "tb_permission" WHERE "id"= %s ''',self.permission_id)
                for row in tmp_query:
                    list_arr.append({
                        'id' : row['id'],
                        'name' : row['name'],
                        'role_level' : row['role_level'],
                        'permis_send_approve' : row['permis_send_approve'],
                        'permis_create_doc' : row['permis_create_doc'],
                        'permis_sign_doc' : row['permis_sign_doc'],
                        'permis_view_doc' : row['permis_view_doc'],
                        'permis_cancel_doc' : row['permis_cancel_doc'],
                        'permis_doc_format' : row['permis_doc_format'],
                        'permis_doc_type' : row['permis_doc_type'],
                        'update_time' : row['update_time']
                    })
                connection.close()    
            if list_arr != []:
                return {'result':'OK','messageText':list_arr}
            else:
                return {'result':'ER','messageText':'invalid permission_id'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def select_permission_id(self,permis_id):
        try:
            self.permis_id = permis_id
            # query_result = db.session.query(paperless_permission).filter(paperless_permission.name==self.name).all()
            with engine.connect() as connection:
                    result = connection.execute('''SELECT * FROM "tb_permission" WHERE "id"= %s ''',self.permis_id)
                    connection.close()
            query_result = [dict(row) for row in result]
            if query_result == []:
                return {'result':'ER','messageText':'Not have pemission','status_Code':200,'messageER':None}
            else:
                return {'result':'OK','messageText':'have permission','status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_permission_v2(self,name):
        try:
            self.name = name
            # query_result = db.session.query(paperless_permission).filter(paperless_permission.name==self.name).all()
            with engine.connect() as connection:
                    result = connection.execute(text('''SELECT * FROM "tb_permission" WHERE "name"=:name '''),name=self.name)
                    connection.close()
            query_result = [dict(row) for row in result]
            if query_result == []:
                return {'result':'OK','messageText':'Not have name','status_Code':200,'messageER':None}
            else:
                return {'result':'ER','messageText':'This name is already exists','status_Code':200,'messageER':None}

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_permission_detail_v2(self,permission_id):
        self.permission_id = permission_id
        try:
            # tmp_query = paperless_permission.query.filter(paperless_permission.id == self.permission_id).first()
            with engine.connect() as connection:
                result = connection.execute(text('''SELECT * FROM "tb_permission" WHERE "id"=:id '''),id=self.permission_id)
                connection.close()
            query_result = [dict(row) for row in result]
            
            return {'result':'OK','messageText':query_result}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

class insert_4():
    def insert_login_logBiz_userLog(self,account_id,username,access_time,vertify_token,access_token,access_token_time,access_token_begin,one_access_token,citizen_data,hash_data,biz_information,secure_number,ipaddress,getBiz_details,email_list,update_time):
        self.account_id         = account_id
        self.username           = str(username).lower()
        self.access_time        = access_time
        self.access_time        = datetime.datetime.fromtimestamp(self.access_time).strftime('%Y-%m-%d %H:%M:%S')
        self.vertify_token      = vertify_token
        self.access_token       = access_token
        self.access_token_time  = int(access_token_time)
        self.access_token_begin = int(access_token_begin)
        self.one_access_token   = one_access_token
        self.citizen_data       = citizen_data
        self.hash_data          = str(hash_data)
        self.biz_information    = str(biz_information)
        self.secure_number      = secure_number
        self.ipaddress          = ipaddress
        self.JsonBiz            = str(getBiz_details)
        self.email              = email_list[0]
        self.transactionCode    = str(uuid.uuid4())
        self.email_list         = str(email_list)
        self.update_time        = update_time
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            with engine.connect() as connection:
                insert_LoginUser = connection.execute('INSERT INTO "tb_citizen_Login" ("account_id","username","access_time","vertify_token","access_token","access_token_time","access_token_begin","one_access_token" \
                    ,"citizen_data","hash_data","biz_information","secure_number","ipaddress","email_citizen","update_time") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ', self.account_id,self.username,self.access_time,self.vertify_token \
                    ,self.access_token,self.access_token_time,self.access_token_begin,self.one_access_token,self.citizen_data,self.hash_data,self.biz_information,self.secure_number,self.ipaddress,self.email_list,self.update_time)
                insert_bizLogin = connection.execute('INSERT INTO "tb_bizLogin" ("account_id","biz_information","username","update_time") VALUES (%s,%s,%s,%s) ', self.account_id,self.JsonBiz,self.username,str(st))
                insert_transaction_login = connection.execute('INSERT INTO "tb_transactionLogin" ("username","userid","transactionCode","ipaddress","date_time","email") VALUES (%s,%s,%s,%s,%s,%s) ', self.username,self.account_id,self.transactionCode,self.ipaddress,str(st),self.email)
            connection.close()
            return {'result':'OK','messageText':'insertuser ok!'}
        except Exception as ex:
            print(str(ex))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(ex)}
        finally:
            connection.close()

    def insert_paperlessToken_v1(self,name,token):
        try:
            self.name = name
            self.token = token
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            with engine.connect() as connection:
                result_insert = connection.execute('INSERT INTO tb_paperless_token ("service_name", "token", "create_date") VALUES (%s,%s,%s) ', self.name,self.token,str(st))
                tmp_result = [dict(row) for row in result_insert]
                connection.close()
            return ({'result':'OK','messageText':tmp_result,'messageER':None,'status_Code':200})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200})

    def insert_permission_v2(self,name,role_level,permission_doc_type,permission_doc_format,permission_cancel_doc,permission_view_doc,permission_sign_doc,permission_create_doc,permission_send_approve):
        try:
            self.name = name
            self.role_level = role_level
            self.permission_doc_type = permission_doc_type
            self.permission_doc_format = permission_doc_format
            self.permission_cancel_doc = permission_cancel_doc
            self.permission_view_doc = permission_view_doc
            self.permission_sign_doc = permission_sign_doc
            self.permission_create_doc = permission_create_doc
            self.permission_send_approve = permission_send_approve
            tmp_permission = {}
            
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            with engine.connect() as connection:
                result_insert = connection.execute('INSERT INTO tb_permission ("name", "role_level", "permis_send_approve", "permis_create_doc", "permis_sign_doc" ,"permis_view_doc","permis_cancel_doc","permis_doc_format","permis_doc_type","update_time") \
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING "id","name", "role_level", "permis_send_approve", "permis_create_doc", "permis_sign_doc" ,"permis_view_doc","permis_cancel_doc","permis_doc_format","permis_doc_type","update_time"'\
                    ,self.name,self.role_level,self.permission_send_approve,self.permission_create_doc,self.permission_sign_doc,self.permission_view_doc,self.permission_cancel_doc,self.permission_doc_format,self.permission_doc_type,str(st))
                tmp_result = [dict(row) for row in result_insert]
                connection.close()
            return ({'result':'OK','messageText':tmp_result,'messageER':None,'status_Code':200})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200})

    def insert_permission(self,username,permission):
        self.username = username
        self.permission = permission
        try:
            with engine.connect() as connection:
                result = connection.execute('''UPDATE "tb_userProfile" SET "permission_id"=%s WHERE "p_username"=%s RETURNING "p_username" ''',self.permission,self.username)
                tmp_query = [dict(row) for row in result]
                connection.close()
            if not tmp_query:
                return {'result':'ER','messageText':'username not found' }                
            else:
                return {'result':'OK','messageText':None}
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}
    
    def insert_permission_all(self,permission_id):
        self.permission_id = permission_id
        try:
            with engine.connect() as connection:
                result = connection.execute('''UPDATE "tb_userProfile" SET "permission_id"=%s WHERE "permission_id"= %s RETURNING "p_username" ''',self.permission_id,None)
                tmp_query = [dict(row) for row in result]
                connection.close()
            if not tmp_query:
                return {'result':'ER','messageText': 'not have permission_id' }                
            else:
                return {'result':'OK','messageText': 'insert permission susscess'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def insert_permission_all_v2(self,permission_id):
        self.permission_id = permission_id
        try:
            with engine.connect() as connection:
                result = connection.execute('''UPDATE "tb_userProfile" SET "permission_id"=%s WHERE "permission_id"= %s RETURNING "p_username" ''',self.permission_id,None)
                tmp_query = [dict(row) for row in result]
                connection.close()
            if not tmp_query:
                return {'result':'ER','messageText': 'not have permission_id' }                
            else:
                return {'result':'OK','messageText': 'insert permission susscess'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def insert_permission_user(self,id_user,permission):
        self.id = id_user
        self.permission = permission
        try:
            with engine.connect() as connection:
                result = connection.execute(text('''SELECT * FROM "tb_userProfile" WHERE "p_userid"=:p_userid '''),p_userid=self.id)
                connection.close()
            tmp_query = [dict(row) for row in result]
            if tmp_query != []:
                with engine.connect() as connection:
                    result_update = connection.execute('''UPDATE "tb_userProfile" SET "permission_id"=%s WHERE "p_userid"=%s''',self.permission,self.id)
                    connection.close()
                return {'result':'OK','messageText':'OK'}
            else:
                return {'result':'ER','messageText':'username not found' }
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(str(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    # def insert_permission_all(self,permission_id):
    #     self.permission_id = permission_id
    #     try:
    #         tmp_query = paper_lessuserProfile.query.filter(paper_lessuserProfile.permission_id == None).all()
    #         if not tmp_query:
    #             return {'result':'ER','messageText': 'not have none permission_id' }                
    #         else:
    #             for x in range(len(tmp_query)):
    #                 tmp_query[x].permission_id = self.permission_id            
    #             db.session.commit()
    #             return {'result':'OK','messageText': 'insert permission susscess'}
    #     except Exception as e:
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         print(exc_type, fname, exc_tb.tb_lineno)
    #         return {'result':'ER','messageText':str(e)}

    # def insert_permission_all_v2(self,permission_id):
    #     self.permission_id = permission_id
    #     try:
    #         tmp_query = paper_lessuserProfile.query.filter(paper_lessuserProfile.permission_id == None).all()
    #         if not tmp_query:
    #             return {'result':'ER','messageText': 'not have none permission_id' }                
    #         else:
    #             for x in range(len(tmp_query)):
    #                 tmp_query[x].permission_id = self.permission_id            
    #             db.session.commit()
    #             return {'result':'OK','messageText': 'insert permission susscess'}
    #     except Exception as e:
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         print(exc_type, fname, exc_tb.tb_lineno)
    #         return {'result':'ER','messageText':str(e)}

class update_4():
    def update_sender_name_migrate(self,tmp_tuple):
        try:
            self.tmp_tuple = tmp_tuple
            # print ('tmp_tuple:',self.tmp_tuple)
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE "tb_send_detail" SET "sender_name"=%s WHERE "step_data_sid"=%s',self.tmp_tuple)
                connection.close()
            
            # print('result_update:',result_update)
            if result_update != None:
                return {'result':'OK','messageText':'update_success'}
            else:
                return {'result':'ER','messageText':'fail'}

        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_tax_id_migrate(self,tmp_tuple):
        try:
            self.tmp_tuple = tmp_tuple
            # print ('tmp_tuple:',self.tmp_tuple)
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE "tb_send_detail" SET "tax_id"=%s WHERE "step_data_sid"=%s',self.tmp_tuple)
                connection.close()
            
            # print('result_update:',result_update)
            if result_update != None:
                return {'result':'OK','messageText':'update_success'}
            else:
                return {'result':'ER','messageText':'fail'}

        except Exception as e:
            print (str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_pdf_new_v1(self,file_data,data_sign):
        self.file_data = file_data
        self.data_sign = data_sign
        sha512encode = hashlib.sha512(str(self.data_sign).encode('utf-8')).hexdigest()
        tmppath_pdf = None
        try:
            arr_sign = []
            connection = engine.connect()
            result = connection.execute(text('SELECT "tb_pdf_storage"."path","tb_pdf_storage"."path_pdf","tb_pdf_storage"."path_sign","tb_pdf_storage"."string_sign","tb_send_detail"."file_id" FROM "tb_send_detail" INNER JOIN "tb_pdf_storage" ON "fid" = "file_id" \
                WHERE "step_data_sid"=:sidfile AND "status"=:status'),sidfile=self.file_data,status='ACTIVE')
            tmp = [dict(row) for row in result]
            tmp = tmp[0]
            if tmp['string_sign'] == None:
                tmpfile_id = tmp['file_id']
                tmppath_sign = tmp['path_pdf']
                tmppath_data = tmp['path']
                r = updatefile_pdfsign_v1(self.data_sign,sha512encode,tmppath_data)
                if 'path_data' in r:
                    tmppath_pdf = r['path_pdf']
                    tmppath_data = r['path_data']
                    # with engine.connect() as connection:
                    result = connection.execute(text('UPDATE "tb_pdf_storage" SET string_sign=:string_sign,hash_sign=:tmphash_sign,path_sign=:tmppathSign,path=:path WHERE fid=:fileid'),string_sign=self.data_sign,tmphash_sign=sha512encode,tmppathSign=tmppath_pdf,fileid=tmpfile_id,path=tmppath_data)
                    connection.close()
                    if result != None:
                        return {'result':'OK'}
                    else:
                        return {'result':'ER'}
                if r['result'] == 'OK':
                    tmppath_pdf = r['path_pdf']
                # with engine.connect() as connection:
                result = connection.execute(text('UPDATE "tb_pdf_storage" SET string_sign=:string_sign,hash_sign=:tmphash_sign,path_sign=:tmppathSign WHERE fid=:fileid'),string_sign=self.data_sign,tmphash_sign=sha512encode,tmppathSign=tmppath_pdf,fileid=tmpfile_id)
                connection.close()
                if result != None:
                    return {'result':'OK'}
                else:
                    return {'result':'ER'}
            else:
                tmpfile_id = tmp['file_id']
                tmppath_sign = tmp['path_pdf']
                tmppath_data = tmp['path']
                r = updatefile_pdfsign_v1(self.data_sign,sha512encode,tmppath_data)
                if 'path_data' in r:
                    tmppath_pdf = r['path_pdf']
                    tmppath_data = r['path_data']
                    # with engine.connect() as connection:
                    result = connection.execute(text('UPDATE "tb_pdf_storage" SET string_sign=:string_sign,hash_sign=:tmphash_sign,path_sign=:tmppathSign,path=:path WHERE fid=:fileid'),string_sign=self.data_sign,tmphash_sign=sha512encode,tmppathSign=tmppath_pdf,fileid=tmpfile_id,path=tmppath_data)
                    connection.close()
                    if result != None:
                        return {'result':'OK'}
                    else:
                        return {'result':'ER'}
                if r['result'] == 'OK':
                    tmppath_pdf = r['path_pdf']
                # with engine.connect() as connection:
                result = connection.execute(text('UPDATE "tb_pdf_storage" SET string_sign=:string_sign,hash_sign=:tmphash_sign,path_sign=:tmppathSign WHERE fid=:fileid'),string_sign=self.data_sign,tmphash_sign=sha512encode,tmppathSign=tmppath_pdf,fileid=tmpfile_id)
                connection.close()
                if result != None:
                    return {'result':'OK'}
                else:
                    return {'result':'ER'}
        except Exception as ex:
            print(str(ex))
            return {'result':'ER','messageText':str(ex)}
        finally:
            connection.close()

    def sender_status_doc_v1(self,sid):
        self.sid = sid
        connection = engine.connect()
        result_select = select().select_datajson_form_step_data_update_sender_v1(self.sid)
        print(result_select)
        detail_status = str(result_select['messageText']['data_document'])
        document_status = result_select['messageText']['status_document']
        tmp_step_now = str(result_select['messageText']['step_now'])
        tmp_maxstep = str(result_select['messageText']['max_step'])
        sql_update = '''update "tb_send_detail" set "status_details"=:tmpstatus_details,"document_status"=:tmpdocument_status,"stepmax"=:tmpstepmax,"stepnow"=:tmpstepnow WHERE "step_data_sid"=:tmpsid '''
        result = connection.execute(text(sql_update),tmpstatus_details=detail_status,tmpdocument_status=document_status,tmpstepmax=tmp_maxstep,tmpstepnow=tmp_step_now,tmpsid=self.sid)
        connection.close()

    def update_pdf_sign_group(self,group_id,pdf_data,email_thai,sign_base):
        self.group_id = group_id
        self.pdf_data = pdf_data
        self.email_thai = email_thai
        self.sign_base = sign_base
        try:
            sql = '''
                select "step_group_detail" FROM "tb_group_document" where "id"=:tmpid and "status"=:tmpstatus;
            '''
            connection = engine.connect()
            result = connection.execute(text(sql),tmpid=self.group_id,tmpstatus='ACTIVE')
            data = [dict(row) for row in result]
            if len(data) >0:
                for n in range(len(data)):
                    tmpdata = data[n]
                    tmp_step_group_detail = eval(tmpdata['step_group_detail'])
                    for z in range(len(tmp_step_group_detail)):
                        if self.email_thai in tmp_step_group_detail[z]['email_one']:
                            tmp_step_group_detail[z]['sign_base'] = str(self.sign_base)
                            tmp_step_group_detail[z]['email_complete'] = str(self.email_thai)
                    # print(tmp_step_group_detail)
            sql_update = '''update "tb_group_document" set "pdf_sign"=:tmppdf_sign,"step_group_detail"=:tmpstep_group_detail WHERE "id"=:tmpid AND "status"=:tmpstatus;'''
            result = connection.execute(text(sql_update),tmppdf_sign=self.pdf_data,tmpstep_group_detail=str(tmp_step_group_detail),tmpid=self.group_id,tmpstatus='ACTIVE')
            return ['success',200]
        except Exception as e:
            print(str(e))
            return [str(e),400]
        finally:
            connection.close()
            
    def update_step_test(self,sid_data_step,sign_email,activity_code,activity_status,step_num,signlat,signlong,sign_id,data_sign):
        self.sid_data_step = sid_data_step
        self.sign_email = sign_email
        self.activity_code = activity_code
        self.activity_status = activity_status
        self.step_num = step_num
        self.sign_id = sign_id
        # self.data_sign = data_sign
        list_num_step_ref = []
        list_num_step_before = []
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        st_update = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        # sha512encode = hashlib.sha512(str(self.data_sign).encode('utf-8')).hexdigest()
        arr_step = []
        json_step = {}
        tmp_sign_tran = None
        try:
            sql = '''
                SELECT
                    tb_step_data.ID AS "id",
                    tb_step_data.sid AS "sid",
                    tb_step_data.data_json AS "data_step",
                    tb_step_data.update_time AS "update_time",
                    "tb_send_detail"."file_id" ,
                    "tb_pdf_storage"."path",
                    "tb_pdf_storage"."path_pdf",
                    "tb_pdf_storage"."path_sign",
                    "tb_pdf_storage"."string_sign"
                FROM
                    tb_step_data 
                INNER JOIN "tb_send_detail" ON "step_data_sid" = tb_step_data.sid
                INNER JOIN "tb_pdf_storage" ON "fid" = "file_id"
                WHERE
                    tb_step_data.sid = :sidtmp;
            ''' 
            # sql += '''
            #     SELECT
            #         "tb_pdf_storage"."path",
            #         "tb_pdf_storage"."path_pdf",
            #         "tb_pdf_storage"."path_sign",
            #         "tb_pdf_storage"."string_sign",
            #         "tb_send_detail"."file_id" 
            #     FROM
            #         "tb_send_detail"
            #         INNER JOIN "tb_pdf_storage" ON "fid" = "file_id"
            #     WHERE
            #         "step_data_sid" =:sidtmp 
            #         AND "status" =:status
            # '''
            connection = engine.connect()
            result = connection.execute(text(sql),sidtmp=self.sid_data_step,status='ACTIVE')
            data = [dict(row) for row in result]
            for n in range(len(data)):
                tmpdata = data[n]
                tmppath_pdf = None
                tmppath_data = None
                tmpsid = tmpdata['sid']
                tmpdata_step = tmpdata['data_step']
                tmpupdate_time = tmpdata['update_time']
                tmpfile_id = tmpdata['file_id']
                tmppath_sign = tmpdata['path_pdf']
                tmppath_data = tmpdata['path']
                # r = updatefile_pdfsign_v1(self.data_sign,sha512encode,tmppath_data)
                # if 'path_data' in r:
                #     tmppath_pdf = r['path_pdf']
                #     tmppath_data = r['path_data']
                try:
                    json_step = eval(tmpdata_step)
                except Exception as e:
                    return {'result':'ER','messageText':'data json cant eval to json'}
                if 'step_num' in json_step:
                    pass
                else:
                    for u in range(len(json_step)):
                        tmp_step_num = json_step[u]['step_num']
                        if 'rf_step' in json_step[u]:
                            print(json_step[u]['rf_step'])
                            if json_step[u]['rf_step'] != None:
                                if json_step[u]['rf_step'] != "None":
                                    tmp_num_step_ref = str(json_step[u]['rf_step']).split('-')[1]
                                    if tmp_num_step_ref == self.step_num:
                                        list_num_step_ref.append(tmp_num_step_ref)
                                        list_num_step_before.append(tmp_step_num)
                    for u in range(len(json_step)):
                        tmp_step_num_2 = json_step[u]['step_num']
                        if len(list_num_step_ref) != 0:
                            for yy in range(len(list_num_step_ref)):
                                tmp_step_num_ref = list_num_step_ref[yy]
                                tmp_step_before_ref = list_num_step_before[yy]
                                if tmp_step_num_2 == tmp_step_before_ref:
                                    tmp_step_detail = json_step[u]['step_detail']
                                    for z in range(len(tmp_step_detail)):
                                        tmp_step_detail[z]['one_email'] = self.sign_email
                if 'step_detail' in json_step:
                    if str(self.sign_id).replace(' ','') != '':
                        if 'step_sign' in json_step:
                            tmp_step_sign = json_step['step_sign']
                            if tmp_step_sign['status'] == True:
                                tmp_data_sign = tmp_step_sign['data']
                                for yz in range(len(tmp_data_sign)):
                                    tmpdata_signone = tmp_data_sign[yz]
                                    tmp_id = tmpdata_signone['id']
                                    if self.sign_id == tmp_id:
                                        tmpdata_signone['status'] = 'complete'
                                        tmp_sign_tran = tmpdata_signone
                    for o in range(len(json_step['step_detail'])):
                        if 'one_email' in json_step['step_detail'][o] and 'activity_code' in json_step['step_detail'][o] and 'activity_status' in json_step['step_detail'][o]:
                            if self.sign_email == json_step['step_detail'][o]['one_email']:
                                for l in range(len(json_step['step_detail'][o]['activity_code'])):
                                    if json_step['step_detail'][o]['activity_code'][l] == str(self.activity_code):
                                        json_step['step_detail'][o]['activity_status'][l] = self.activity_status
                                        json_step['step_detail'][o]['activity_time'][l] = st_update
                                        if tmp_sign_tran != None:
                                            tmp_sign_tran['status'] = 'complete'
                                            json_step['step_detail'][o]['activity_data'][l] = tmp_sign_tran
                                        else:
                                            json_step['step_detail'][o]['activity_data'][l]['status'] = 'complete'
                                json_step['step_detail'][o]['sign_position']['sign_latitude'] = signlat
                                json_step['step_detail'][o]['sign_position']['sign_longitude'] = signlong
                                json_step['step_detail'][o]['sign_position']['sign_time'] = st_update
                else:
                    for z in range(len(json_step)):
                        arr_step.append(json_step[z]['step_num'])
                    for i in range(len(json_step)):
                        if self.step_num in arr_step:
                            if json_step[i]['step_num'] == self.step_num:
                                if 'step_detail' in json_step[i]:
                                    if 'step_sign' in json_step[i]:
                                        tmp_step_sign = json_step[i]['step_sign']
                                        if tmp_step_sign['status'] == True:
                                            tmp_data_sign = tmp_step_sign['data']
                                            for yz in range(len(tmp_data_sign)):
                                                tmpdata_signone = tmp_data_sign[yz]
                                                tmp_id = tmpdata_signone['id']
                                                if self.sign_id == tmp_id:
                                                    tmpdata_signone['status'] = 'complete'
                                                    tmp_sign_tran = tmpdata_signone
                                    for o in range(len(json_step[i]['step_detail'])):
                                        if 'one_email' in json_step[i]['step_detail'][o] and 'activity_code' in json_step[i]['step_detail'][o] and 'activity_status' in json_step[i]['step_detail'][o]:
                                            if self.sign_email == json_step[i]['step_detail'][o]['one_email']:
                                                for l in range(len(json_step[i]['step_detail'][o]['activity_code'])):
                                                    if json_step[i]['step_detail'][o]['activity_code'][l] == str(self.activity_code):
                                                        json_step[i]['step_detail'][o]['activity_status'][l] = self.activity_status
                                                        json_step[i]['step_detail'][o]['activity_time'][l] = st_update
                                                        if tmp_sign_tran != None:
                                                            tmp_sign_tran['status'] = 'complete'
                                                            json_step[i]['step_detail'][o]['activity_data'][l] = tmp_sign_tran
                                                        else:
                                                            json_step[i]['step_detail'][o]['activity_data'][l]['status'] = 'complete'
                                                json_step[i]['step_detail'][o]['sign_position']['sign_latitude'] = signlat
                                                json_step[i]['step_detail'][o]['sign_position']['sign_longitude'] = signlong
                                                json_step[i]['step_detail'][o]['sign_position']['sign_time'] = st_update                        
                        else:
                            return {'result':'ER','messageText':"step num fail"}
                json_step = json.dumps(json_step)
                json_step_ev = eval(json_step)
                result_select = cal_sender_status_document_v1(json_step_ev)
                detail_status = str(result_select['messageText']['data_document'])
                document_status = result_select['messageText']['status_document']
                tmp_step_now = str(result_select['messageText']['step_now'])
                tmp_maxstep = str(result_select['messageText']['max_step'])
                sql_update = '''
                    UPDATE "tb_step_data" 
                    SET "data_json" =:tmpdatajson,
                    "update_time" =:tmpupdate_time 
                    WHERE
                        "sid" =:tmpsid;
                    UPDATE "tb_send_detail" 
                    SET "status_details" =:tmpstatus_details,
                    "document_status" =:tmpdocument_status,
                    "stepmax" =:tmpstepmax,
                    "stepnow" =:tmpstepnow 
                    WHERE
                        "step_data_sid" =:tmpsid;
                '''
                result = connection.execute(text(sql_update),tmpdatajson=json_step,tmpupdate_time=str(st),tmpsid=self.sid_data_step,tmpstatus_details=detail_status,tmpdocument_status=document_status,tmpstepmax=tmp_maxstep\
                    ,tmpstepnow=tmp_step_now)
            
            connection.close()
            return {'result':'OK','messageText':'update success'}
        except Exception as e:
            print(str(e))
            return [str(e),400]
        finally:
            connection.close()

    def update_step_new_v1(self,sid_data_step,sign_email,activity_code,activity_status,step_num,signlat,signlong,sign_id,data_sign):
        self.sid_data_step = sid_data_step
        self.sign_email = sign_email
        self.activity_code = activity_code
        self.activity_status = activity_status
        self.step_num = step_num
        self.sign_id = sign_id
        self.data_sign = data_sign
        list_num_step_ref = []
        list_num_step_before = []
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        st_update = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        sha512encode = hashlib.sha512(str(self.data_sign).encode('utf-8')).hexdigest()
        arr_step = []
        json_step = {}
        tmp_sign_tran = None
        try:
            sql = '''
                SELECT
                    tb_step_data.ID AS "id",
                    tb_step_data.sid AS "sid",
                    tb_step_data.data_json AS "data_step",
                    tb_step_data.update_time AS "update_time",
                    "tb_send_detail"."file_id" ,
                    "tb_pdf_storage"."path",
                    "tb_pdf_storage"."path_pdf",
                    "tb_pdf_storage"."path_sign",
                    "tb_pdf_storage"."string_sign"
                FROM
                    tb_step_data 
                INNER JOIN "tb_send_detail" ON "step_data_sid" = tb_step_data.sid
                INNER JOIN "tb_pdf_storage" ON "fid" = "file_id"
                WHERE
                    tb_step_data.sid = :sidtmp;
            ''' 
            # sql += '''
            #     SELECT
            #         "tb_pdf_storage"."path",
            #         "tb_pdf_storage"."path_pdf",
            #         "tb_pdf_storage"."path_sign",
            #         "tb_pdf_storage"."string_sign",
            #         "tb_send_detail"."file_id" 
            #     FROM
            #         "tb_send_detail"
            #         INNER JOIN "tb_pdf_storage" ON "fid" = "file_id"
            #     WHERE
            #         "step_data_sid" =:sidtmp 
            #         AND "status" =:status
            # '''
            connection = engine.connect()
            result = connection.execute(text(sql),sidtmp=self.sid_data_step,status='ACTIVE')
            data = [dict(row) for row in result]
            for n in range(len(data)):
                tmpdata = data[n]
                tmppath_pdf = None
                tmppath_data = None
                tmpsid = tmpdata['sid']
                tmpdata_step = tmpdata['data_step']
                tmpupdate_time = tmpdata['update_time']
                tmpfile_id = tmpdata['file_id']
                tmppath_sign = tmpdata['path_pdf']
                tmppath_data = tmpdata['path']
                r = updatefile_pdfsign_v1(self.data_sign,sha512encode,tmppath_data)
                if 'path_data' in r:
                    tmppath_pdf = r['path_pdf']
                    tmppath_data = r['path_data']
                try:
                    json_step = eval(tmpdata_step)
                except Exception as e:
                    return {'result':'ER','messageText':'data json cant eval to json'}
                if 'step_num' in json_step:
                    pass
                else:
                    for u in range(len(json_step)):
                        tmp_step_num = json_step[u]['step_num']
                        if 'rf_step' in json_step[u]:
                            print(json_step[u]['rf_step'])
                            if json_step[u]['rf_step'] != None:
                                if json_step[u]['rf_step'] != "None":
                                    tmp_num_step_ref = str(json_step[u]['rf_step']).split('-')[1]
                                    if tmp_num_step_ref == self.step_num:
                                        list_num_step_ref.append(tmp_num_step_ref)
                                        list_num_step_before.append(tmp_step_num)
                    for u in range(len(json_step)):
                        tmp_step_num_2 = json_step[u]['step_num']
                        if len(list_num_step_ref) != 0:
                            for yy in range(len(list_num_step_ref)):
                                tmp_step_num_ref = list_num_step_ref[yy]
                                tmp_step_before_ref = list_num_step_before[yy]
                                if tmp_step_num_2 == tmp_step_before_ref:
                                    tmp_step_detail = json_step[u]['step_detail']
                                    for z in range(len(tmp_step_detail)):
                                        tmp_step_detail[z]['one_email'] = self.sign_email
                if 'step_detail' in json_step:
                    if str(self.sign_id).replace(' ','') != '':
                        if 'step_sign' in json_step:
                            tmp_step_sign = json_step['step_sign']
                            if tmp_step_sign['status'] == True:
                                tmp_data_sign = tmp_step_sign['data']
                                for yz in range(len(tmp_data_sign)):
                                    tmpdata_signone = tmp_data_sign[yz]
                                    tmp_id = tmpdata_signone['id']
                                    if self.sign_id == tmp_id:
                                        tmpdata_signone['status'] = 'complete'
                                        tmp_sign_tran = tmpdata_signone
                    for o in range(len(json_step['step_detail'])):
                        if 'one_email' in json_step['step_detail'][o] and 'activity_code' in json_step['step_detail'][o] and 'activity_status' in json_step['step_detail'][o]:
                            if self.sign_email == json_step['step_detail'][o]['one_email']:
                                for l in range(len(json_step['step_detail'][o]['activity_code'])):
                                    if json_step['step_detail'][o]['activity_code'][l] == str(self.activity_code):
                                        json_step['step_detail'][o]['activity_status'][l] = self.activity_status
                                        json_step['step_detail'][o]['activity_time'][l] = st_update
                                        if tmp_sign_tran != None:
                                            tmp_sign_tran['status'] = 'complete'
                                            json_step['step_detail'][o]['activity_data'][l] = tmp_sign_tran
                                        else:
                                            json_step['step_detail'][o]['activity_data'][l]['status'] = 'complete'
                                json_step['step_detail'][o]['sign_position']['sign_latitude'] = signlat
                                json_step['step_detail'][o]['sign_position']['sign_longitude'] = signlong
                                json_step['step_detail'][o]['sign_position']['sign_time'] = st_update
                else:
                    for z in range(len(json_step)):
                        arr_step.append(json_step[z]['step_num'])
                    for i in range(len(json_step)):
                        if self.step_num in arr_step:
                            if json_step[i]['step_num'] == self.step_num:
                                if 'step_detail' in json_step[i]:
                                    if 'step_sign' in json_step[i]:
                                        tmp_step_sign = json_step[i]['step_sign']
                                        if tmp_step_sign['status'] == True:
                                            tmp_data_sign = tmp_step_sign['data']
                                            for yz in range(len(tmp_data_sign)):
                                                tmpdata_signone = tmp_data_sign[yz]
                                                tmp_id = tmpdata_signone['id']
                                                if self.sign_id == tmp_id:
                                                    tmpdata_signone['status'] = 'complete'
                                                    tmp_sign_tran = tmpdata_signone
                                    for o in range(len(json_step[i]['step_detail'])):
                                        if 'one_email' in json_step[i]['step_detail'][o] and 'activity_code' in json_step[i]['step_detail'][o] and 'activity_status' in json_step[i]['step_detail'][o]:
                                            if self.sign_email == json_step[i]['step_detail'][o]['one_email']:
                                                for l in range(len(json_step[i]['step_detail'][o]['activity_code'])):
                                                    if json_step[i]['step_detail'][o]['activity_code'][l] == str(self.activity_code):
                                                        json_step[i]['step_detail'][o]['activity_status'][l] = self.activity_status
                                                        json_step[i]['step_detail'][o]['activity_time'][l] = st_update
                                                        if tmp_sign_tran != None:
                                                            tmp_sign_tran['status'] = 'complete'
                                                            json_step[i]['step_detail'][o]['activity_data'][l] = tmp_sign_tran
                                                        else:
                                                            json_step[i]['step_detail'][o]['activity_data'][l]['status'] = 'complete'
                                                json_step[i]['step_detail'][o]['sign_position']['sign_latitude'] = signlat
                                                json_step[i]['step_detail'][o]['sign_position']['sign_longitude'] = signlong
                                                json_step[i]['step_detail'][o]['sign_position']['sign_time'] = st_update                        
                        else:
                            return {'result':'ER','messageText':"step num fail"}
                json_step = json.dumps(json_step)
                json_step_ev = eval(json_step)
                result_select = cal_sender_status_document_v1(json_step_ev)
                detail_status = str(result_select['messageText']['data_document'])
                document_status = result_select['messageText']['status_document']
                tmp_step_now = str(result_select['messageText']['step_now'])
                tmp_maxstep = str(result_select['messageText']['max_step'])
                sql_update = '''
                    UPDATE "tb_pdf_storage" SET string_sign=:string_sign,hash_sign=:tmphash_sign,path_sign=:tmppathSign,path=:path WHERE fid=:fileid;
                    UPDATE "tb_step_data" 
                    SET "data_json" =:tmpdatajson,
                    "update_time" =:tmpupdate_time 
                    WHERE
                        "sid" =:tmpsid;
                    UPDATE "tb_send_detail" 
                    SET "status_details" =:tmpstatus_details,
                    "document_status" =:tmpdocument_status,
                    "stepmax" =:tmpstepmax,
                    "stepnow" =:tmpstepnow 
                    WHERE
                        "step_data_sid" =:tmpsid;
                '''
                result = connection.execute(text(sql_update),tmpdatajson=json_step,tmpupdate_time=str(st),tmpsid=self.sid_data_step,tmpstatus_details=detail_status,tmpdocument_status=document_status,tmpstepmax=tmp_maxstep\
                    ,tmpstepnow=tmp_step_now,string_sign=self.data_sign,tmphash_sign=sha512encode,tmppathSign=tmppath_pdf,fileid=tmpfile_id,path=tmppath_data)
            
            connection.close()
            return {'result':'OK','messageText':'update success'}
            # select_step_data = paper_lessdatastep.query.filter_by(sid=self.sid_data_step)
            # print(select_step_data)
            try:
                json_step = eval(select_step_data.data_json)
            except Exception as e:
                return {'result':'ER','messageText':'data json cant eval to json'}
            
            # print(json_step)
            if 'step_num' in json_step:
                pass
            else:
                for u in range(len(json_step)):
                    tmp_step_num = json_step[u]['step_num']
                    if 'rf_step' in json_step[u]:
                        if json_step[u]['rf_step'] != None:
                            tmp_num_step_ref = str(json_step[u]['rf_step']).split('-')[1]
                            if tmp_num_step_ref == self.step_num:
                                list_num_step_ref.append(tmp_num_step_ref)
                                list_num_step_before.append(tmp_step_num)
                # print(list_num_step_ref,list_num_step_before)
                for u in range(len(json_step)):
                    tmp_step_num_2 = json_step[u]['step_num']
                    if len(list_num_step_ref) != 0:
                        for yy in range(len(list_num_step_ref)):
                            tmp_step_num_ref = list_num_step_ref[yy]
                            tmp_step_before_ref = list_num_step_before[yy]
                            if tmp_step_num_2 == tmp_step_before_ref:
                                tmp_step_detail = json_step[u]['step_detail']
                                for z in range(len(tmp_step_detail)):
                                    tmp_step_detail[z]['one_email'] = self.sign_email
            # print(json_step)
            if 'step_detail' in json_step:
                if str(self.sign_id).replace(' ','') != '':
                    if 'step_sign' in json_step:
                        tmp_step_sign = json_step['step_sign']
                        if tmp_step_sign['status'] == True:
                            tmp_data_sign = tmp_step_sign['data']
                            for yz in range(len(tmp_data_sign)):
                                tmpdata_signone = tmp_data_sign[yz]
                                tmp_id = tmpdata_signone['id']
                                if self.sign_id == tmp_id:
                                    tmpdata_signone['status'] = 'complete'
                                    tmp_sign_tran = tmpdata_signone
                for o in range(len(json_step['step_detail'])):
                    if 'one_email' in json_step['step_detail'][o] and 'activity_code' in json_step['step_detail'][o] and 'activity_status' in json_step['step_detail'][o]:
                        if self.sign_email == json_step['step_detail'][o]['one_email']:
                            for l in range(len(json_step['step_detail'][o]['activity_code'])):
                                if json_step['step_detail'][o]['activity_code'][l] == str(self.activity_code):
                                    json_step['step_detail'][o]['activity_status'][l] = self.activity_status
                                    json_step['step_detail'][o]['activity_time'][l] = st_update
                                    if tmp_sign_tran != None:
                                        tmp_sign_tran['status'] = 'complete'
                                        json_step['step_detail'][o]['activity_data'][l] = tmp_sign_tran
                                    else:
                                        json_step['step_detail'][o]['activity_data'][l]['status'] = 'complete'
                            json_step['step_detail'][o]['sign_position']['sign_latitude'] = signlat
                            json_step['step_detail'][o]['sign_position']['sign_longitude'] = signlong
                            json_step['step_detail'][o]['sign_position']['sign_time'] = st_update
            else:
                for z in range(len(json_step)):
                    arr_step.append(json_step[z]['step_num'])
                for i in range(len(json_step)):
                    # print(self.step_num)
                    if self.step_num in arr_step:
                        if json_step[i]['step_num'] == self.step_num:
                            if 'step_detail' in json_step[i]:
                                if 'step_sign' in json_step[i]:
                                    tmp_step_sign = json_step[i]['step_sign']
                                    if tmp_step_sign['status'] == True:
                                        tmp_data_sign = tmp_step_sign['data']
                                        for yz in range(len(tmp_data_sign)):
                                            tmpdata_signone = tmp_data_sign[yz]
                                            tmp_id = tmpdata_signone['id']
                                            if self.sign_id == tmp_id:
                                                tmpdata_signone['status'] = 'complete'
                                                tmp_sign_tran = tmpdata_signone
                                for o in range(len(json_step[i]['step_detail'])):
                                    if 'one_email' in json_step[i]['step_detail'][o] and 'activity_code' in json_step[i]['step_detail'][o] and 'activity_status' in json_step[i]['step_detail'][o]:
                                        if self.sign_email == json_step[i]['step_detail'][o]['one_email']:
                                            for l in range(len(json_step[i]['step_detail'][o]['activity_code'])):
                                                if json_step[i]['step_detail'][o]['activity_code'][l] == str(self.activity_code):
                                                    json_step[i]['step_detail'][o]['activity_status'][l] = self.activity_status
                                                    json_step[i]['step_detail'][o]['activity_time'][l] = st_update
                                                    if tmp_sign_tran != None:
                                                        tmp_sign_tran['status'] = 'complete'
                                                        json_step[i]['step_detail'][o]['activity_data'][l] = tmp_sign_tran
                                                    else:
                                                        json_step[i]['step_detail'][o]['activity_data'][l]['status'] = 'complete'
                                            json_step[i]['step_detail'][o]['sign_position']['sign_latitude'] = signlat
                                            json_step[i]['step_detail'][o]['sign_position']['sign_longitude'] = signlong
                                            json_step[i]['step_detail'][o]['sign_position']['sign_time'] = st_update
                    else:
                        return {'result':'ER','messageText':"step num fail"}
            json_step = json.dumps(json_step)
            select_step_data.data_json = (json_step)
            select_step_data.update_time = st
            db.session.commit()
            result_select = select().select_datajson_form_step_data_update_sender_v1(self.sid_data_step)
            detail_status = str(result_select['messageText']['data_document'])
            document_status = result_select['messageText']['status_document']
            tmp_step_now = str(result_select['messageText']['step_now'])
            tmp_maxstep = str(result_select['messageText']['max_step'])
            try:
                result_update = paper_lesssender.query.filter(paper_lesssender.step_data_sid==self.sid_data_step).first()
                if result_update != None:
                    result_update.status_details = detail_status
                    result_update.document_status = document_status
                    result_update.stepmax = tmp_maxstep
                    result_update.stepnow = tmp_step_now
                    db.session.commit()
            except Exception as e:
                return {'result':'ER','messageText':str(e)}
            return {'result':'OK','messageText':'update success'}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}
        finally:
            connection.close()

    def update_login_logBiz_userLog(self,account_id,username, access_time, vertify_token,access_token,access_token_time,access_token_begin,one_access_token,citizen_data,hash_data,biz_information,secure_number,ipaddress,getBiz_details,email_list,update_time,update_time_old):
        self.account_id             = account_id
        self.username               = str(username).lower()
        self.access_time            = access_time
        self.access_time            = datetime.datetime.fromtimestamp(self.access_time).strftime('%Y-%m-%d %H:%M:%S')
        self.vertify_token          = vertify_token
        self.access_token           = access_token
        self.access_token_time      = int(access_token_time)
        self.access_token_begin     = int(access_token_begin)
        self.one_access_token       = one_access_token
        self.citizen_data           = citizen_data
        self.hash_data              = str(hash_data)
        self.biz_information        = str(biz_information)
        self.secure_number          = secure_number
        self.ipaddress              = ipaddress
        self.JsonBiz                = str(getBiz_details)
        self.email                  = email_list[0]
        self.transactionCode        = str(uuid.uuid4())
        self.email_list             = str(email_list)
        self.update_time            = update_time
        self.update_time_old        = update_time_old
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')        
        try:
            connection = engine.connect()
            update_LoginUser = connection.execute('UPDATE "tb_citizen_Login" SET "access_time"=%s,"vertify_token"=%s,"access_token"=%s,"access_token_time"=%s,"access_token_begin"=%s,"one_access_token"=%s \
                    ,"citizen_data"=%s,"hash_data"=%s,"biz_information"=%s,"secure_number"=%s,"ipaddress"=%s,"email_citizen"=%s,"update_time"=%s  WHERE id = (SELECT id FROM "tb_citizen_Login" WHERE "account_id"=%s and "username"=%s LIMIT(1))', self.access_time,self.vertify_token \
                    ,self.access_token,self.access_token_time,self.access_token_begin,self.one_access_token,self.citizen_data,self.hash_data,self.biz_information,self.secure_number,self.ipaddress,self.email_list,self.update_time,self.account_id,self.username)
            update_bizLogin = connection.execute('UPDATE "tb_bizLogin" SET "biz_information"=%s,"update_time"=%s  WHERE id = (SELECT id FROM "tb_bizLogin" WHERE "account_id"=%s and "username"=%s LIMIT(1)) ', self.JsonBiz,str(st),self.account_id,self.username)
            insert_transaction_login = connection.execute('INSERT INTO "tb_transactionLogin" ("username","userid","transactionCode","ipaddress","date_time","email") VALUES (%s,%s,%s,%s,%s,%s) ', self.username,self.account_id,self.transactionCode,self.ipaddress,str(st),self.email)
            return {'result': 'OK', 'messageText': 'updateok!','status_Code':200}
            # if self.update_time_old == None:
            #     update_LoginUser = connection.execute('UPDATE "tb_citizen_Login" SET "access_time"=%s,"vertify_token"=%s,"access_token"=%s,"access_token_time"=%s,"access_token_begin"=%s,"one_access_token"=%s \
            #             ,"citizen_data"=%s,"hash_data"=%s,"biz_information"=%s,"secure_number"=%s,"ipaddress"=%s,"email_citizen"=%s,"update_time"=%s  WHERE id = (SELECT id FROM "tb_citizen_Login" WHERE "account_id"=%s and "username"=%s LIMIT(1))', self.access_time,self.vertify_token \
            #             ,self.access_token,self.access_token_time,self.access_token_begin,self.one_access_token,self.citizen_data,self.hash_data,self.biz_information,self.secure_number,self.ipaddress,self.email_list,self.update_time,self.account_id,self.username)
            #     update_bizLogin = connection.execute('UPDATE "tb_bizLogin" SET "biz_information"=%s,"update_time"=%s  WHERE id = (SELECT id FROM "tb_bizLogin" WHERE "account_id"=%s and "username"=%s LIMIT(1)) ', self.JsonBiz,str(st),self.account_id,self.username)
            #     insert_transaction_login = connection.execute('INSERT INTO "tb_transactionLogin" ("username","userid","transactionCode","ipaddress","date_time","email") VALUES (%s,%s,%s,%s,%s,%s) ', self.username,self.account_id,self.transactionCode,self.ipaddress,str(st),self.email)
            #     return {'result': 'OK', 'messageText': 'updateok!','status_Code':200}
            # else:
            #     updatetime_old = update_time_old.strftime('%Y-%m-%d %H:%M:%S')
            # # print(str(self.update_time_old) ==str(self.update_time))
            # if str(self.update_time_old)  == str(self.update_time):
            #     update_LoginUser = connection.execute('UPDATE "tb_citizen_Login" SET "access_time"=%s,"vertify_token"=%s,"access_token"=%s,"access_token_time"=%s,"access_token_begin"=%s,"one_access_token"=%s \
            #         ,"hash_data"=%s,"secure_number"=%s,"ipaddress"=%s  WHERE id = (SELECT id FROM "tb_citizen_Login" WHERE "account_id"=%s and "username"=%s LIMIT(1))', self.access_time,self.vertify_token \
            #         ,self.access_token,self.access_token_time,self.access_token_begin,self.one_access_token,self.hash_data,self.secure_number,self.ipaddress,self.account_id,self.username)     
            # else:
            #     update_LoginUser = connection.execute('UPDATE "tb_citizen_Login" SET "access_time"=%s,"vertify_token"=%s,"access_token"=%s,"access_token_time"=%s,"access_token_begin"=%s,"one_access_token"=%s \
            #             ,"citizen_data"=%s,"hash_data"=%s,"biz_information"=%s,"secure_number"=%s,"ipaddress"=%s,"email_citizen"=%s,"update_time"=%s  WHERE id = (SELECT id FROM "tb_citizen_Login" WHERE "account_id"=%s and "username"=%s LIMIT(1))', self.access_time,self.vertify_token \
            #             ,self.access_token,self.access_token_time,self.access_token_begin,self.one_access_token,self.citizen_data,self.hash_data,self.biz_information,self.secure_number,self.ipaddress,self.email_list,self.update_time,self.account_id,self.username)
            #     update_bizLogin = connection.execute('UPDATE "tb_bizLogin" SET "biz_information"=%s,"update_time"=%s  WHERE id = (SELECT id FROM "tb_bizLogin" WHERE "account_id"=%s and "username"=%s LIMIT(1)) ', self.JsonBiz,str(st),self.account_id,self.username)
            # insert_transaction_login = connection.execute('INSERT INTO "tb_transactionLogin" ("username","userid","transactionCode","ipaddress","date_time","email") VALUES (%s,%s,%s,%s,%s,%s) ', self.username,self.account_id,self.transactionCode,self.ipaddress,str(st),self.email)
            # connection.close()
            # return {'result': 'OK', 'messageText': 'updateok!','status_Code':200}
        except Exception as ex:
            print(str(ex))
            return {'result':'ER','messageText':str(ex)}
        finally:
            connection.close()

    def update_status_group_v1(self,group_id,status):
        self.group_id = group_id
        self.status = status
        try:
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE "tb_group_document" SET "group_status"=%s WHERE "id"=%s',self.status,self.group_id)
            connection.close()
            # print(result_update)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_pdf_step(self,file_data,data_sign):
        try:
            self.file_data = file_data
            self.data_sign = data_sign
            sha512encode = hashlib.sha512(str(self.data_sign).encode('utf-8')).hexdigest()
            tmppath_pdf = None
            arr_sign = []
            with engine.connect() as connection:
                result = connection.execute(text('SELECT "tb_pdf_storage"."path","tb_pdf_storage"."path_pdf","tb_pdf_storage"."path_sign","tb_pdf_storage"."string_sign","tb_send_detail"."file_id" FROM "tb_send_detail" INNER JOIN "tb_pdf_storage" ON "fid" = "file_id" \
                    WHERE "step_data_sid"=:sidfile AND "status"=:status'),sidfile=self.file_data,status='ACTIVE')
                tmp = [dict(row) for row in result]
                tmp = tmp[0]
                connection.close()
            if tmp['string_sign'] == None:
                tmpfile_id = tmp['file_id']
                tmppath_sign = tmp['path_pdf']
                tmppath_data = tmp['path']
                r = updatefile_pdfsign_v1(self.data_sign,sha512encode,tmppath_data)
                if 'path_data' in r:
                    tmppath_pdf = r['path_pdf']
                    tmppath_data = r['path_data']
                    with engine.connect() as connection:
                        result = connection.execute(text('UPDATE "tb_pdf_storage" SET string_sign=:string_sign,hash_sign=:tmphash_sign,path_sign=:tmppathSign,path=:path WHERE fid=:fileid'),string_sign=self.data_sign,tmphash_sign=sha512encode,tmppathSign=tmppath_pdf,fileid=tmpfile_id,path=tmppath_data)
                        connection.close()
                    if result != None:
                        return {'result':'OK'}
                    else:
                        return {'result':'ER'}
                if r['result'] == 'OK':
                    tmppath_pdf = r['path_pdf']
                with engine.connect() as connection:
                    result = connection.execute(text('UPDATE "tb_pdf_storage" SET string_sign=:string_sign,hash_sign=:tmphash_sign,path_sign=:tmppathSign WHERE fid=:fileid'),string_sign=self.data_sign,tmphash_sign=sha512encode,tmppathSign=tmppath_pdf,fileid=tmpfile_id)
                    connection.close()
                if result != None:
                    return {'result':'OK'}
                else:
                    return {'result':'ER'}
            else:
                tmpfile_id = tmp['file_id']
                tmppath_sign = tmp['path_pdf']
                tmppath_data = tmp['path']
                r = updatefile_pdfsign_v1(self.data_sign,sha512encode,tmppath_data)
                if 'path_data' in r:
                    tmppath_pdf = r['path_pdf']
                    tmppath_data = r['path_data']
                    with engine.connect() as connection:
                        result = connection.execute(text('UPDATE "tb_pdf_storage" SET string_sign=:string_sign,hash_sign=:tmphash_sign,path_sign=:tmppathSign,path=:path WHERE fid=:fileid'),string_sign=self.data_sign,tmphash_sign=sha512encode,tmppathSign=tmppath_pdf,fileid=tmpfile_id,path=tmppath_data)
                        connection.close()
                    if result != None:
                        return {'result':'OK'}
                    else:
                        return {'result':'ER'}
                if r['result'] == 'OK':
                    tmppath_pdf = r['path_pdf']
                with engine.connect() as connection:
                    result = connection.execute(text('UPDATE "tb_pdf_storage" SET string_sign=:string_sign,hash_sign=:tmphash_sign,path_sign=:tmppathSign WHERE fid=:fileid'),string_sign=self.data_sign,tmphash_sign=sha512encode,tmppathSign=tmppath_pdf,fileid=tmpfile_id)
                    connection.close()
                if result != None:
                    return {'result':'OK'}
                else:
                    return {'result':'ER'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}
            
    def update_group_v3(self,sidcode,group_id):
        self.sidcode = sidcode
        self.group_id = group_id
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        try:
            for z in range(len(self.sidcode)):
                tmp_list_group_id = []
                tmp_sidcode = self.sidcode[z]
                tmp_list_group_id.append(self.group_id)
                tmp_list_group_id = str(tmp_list_group_id)
                with engine.connect() as connection:
                    result_update = connection.execute('UPDATE "tb_send_detail" SET "group_id"=%s WHERE "step_data_sid"=%s',tmp_list_group_id,tmp_sidcode)
                    result_update_time = connection.execute('UPDATE "tb_step_data" SET "update_time"=%s WHERE "sid"=%s',str(st),tmp_sidcode)
                connection.close()
            return {'result':'OK','messageText':'success'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_status_document_v4(self,username,userEmail,sidcode,type_status):
        self.username= username
        self.userEmail= userEmail
        self.sidcode = sidcode
        self.type_status = str(type_status).upper()
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        try:
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE "tb_send_detail" SET "status"=%s WHERE "send_user"=%s AND "sender_email"=%s AND "step_data_sid"=%s',self.type_status,self.username,self.userEmail,self.sidcode)
                result_update_time = connection.execute('UPDATE "tb_step_data" SET "update_time"=%s WHERE "sid"=%s',str(st),self.sidcode)
            connection.close()
            if result_update != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}
            
    def update_sizeFile_document_v1(self,listdata):
        self.listdata = listdata
        try:
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE "tb_send_detail" SET "filesize"=%s WHERE "file_id"=%s',self.listdata)
                connection.close()
            if result_update != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_status_business(self,listdata):
        self.listdata = listdata
        try:
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE "tb_bizPaperless" SET "status"=%s,"transactionMax"=%s,"storageMax"=%s,"update_date"=%s,"transactionNow"=%s,"storageNow"=%s WHERE "tax_id"=%s',self.listdata)
                connection.close()
            if result_update != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_status_service(self,sid_code,data_status_service):
        self.sid_code = sid_code
        self.data_status_service = data_status_service
        try:
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE tb_send_detail SET "status_service"=%s WHERE "step_data_sid"=%s',self.data_status_service,self.sid_code)
                connection.close()
            if result_update != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_pathPDF_v1(self,json):
        self.json = json
        try:
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE tb_pdf_storage SET "path_pdf"=%s,"path"=%s WHERE "fid"=%s',self.json)
                connection.close()
            if result_update != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_permission_v2(self,id_permis,name,role_level,permission_doc_type,permission_doc_format,permission_cancel_doc,permission_view_doc,permission_sign_doc,permission_create_doc,permission_send_approve):
        try:
            self.id = id_permis
            self.name = name
            self.role_level = role_level
            self.permission_doc_type = permission_doc_type
            self.permission_doc_format = permission_doc_format
            self.permission_cancel_doc = permission_cancel_doc
            self.permission_view_doc = permission_view_doc
            self.permission_sign_doc = permission_sign_doc
            self.permission_create_doc = permission_create_doc
            self.permission_send_approve = permission_send_approve
            tmp_permission = {}
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE tb_permission SET "name"=%s,"role_level"=%s,"permis_send_approve"=%s,"permis_create_doc"=%s,"permis_sign_doc"=%s,"permis_view_doc"=%s,"permis_cancel_doc"=%s,"permis_doc_format"=%s,"permis_doc_type"=%s,"update_time"=%s \
                    WHERE "id"=%s RETURNING "id","name", "role_level", "permis_send_approve", "permis_create_doc", "permis_sign_doc" ,"permis_view_doc","permis_cancel_doc","permis_doc_format","permis_doc_type","update_time"'\
                    ,self.name,self.role_level,self.permission_send_approve,self.permission_create_doc,self.permission_sign_doc,self.permission_view_doc,self.permission_cancel_doc,self.permission_doc_format,self.permission_doc_type,str(st),self.id)
                tmp_result = [dict(row) for row in result_update]
                connection.close()
            return ({'result':'OK','messageText':tmp_result,'messageER':None,'status_Code':200})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

class delete_4():
    def remove_permission(self,permis_id):
        try:
            self.permis_id = permis_id
            # query_result = db.session.query(paperless_permission).filter(paperless_permission.name==self.name).all()
            with engine.connect() as connection:
                result = connection.execute('''SELECT * FROM "tb_permission" WHERE "id"::text= %s ''',self.permis_id)
                connection.close()
            query_result = [dict(row) for row in result]
            if query_result == []:
                return {'result':'ER','messageText':None,'status_Code':200,'messageER':'Not have pemission'}
            else:
                with engine.connect() as connection:
                    # result = connection.execute('''SELECT * FROM "tb_permission" WHERE "id"= %s ''',self.permis_id)
                    result_delete = connection.execute('''DELETE FROM "tb_permission" WHERE "id"= %s''',self.permis_id)
                    connection.close()
                return {'result':'OK','messageText':'delete_success','status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print (e)
            return {'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}

    def set_null_user(self,id_permis):
        try:
            self.permis_id = id_permis
            with engine.connect() as connection:
                result = connection.execute('''SELECT * FROM "tb_userProfile" WHERE "permission_id"::text= %s ''',self.permis_id)
                connection.close()
            query_result = [dict(row) for row in result]
            if query_result == []:
                return {'result':'ER','messageText':None,'status_Code':200,'messageER':'Not have data'}
            else:
                for i in range(len(query_result)):
                    p_id = query_result[i]['p_id']
                    with engine.connect() as connection:
                        result_update = connection.execute('''UPDATE "tb_userProfile" SET "permission_id"=%s WHERE "p_id"=%s''',None,p_id)
                        connection.close()
                return {'result':'OK','messageText':'remove_success','status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}                                                    