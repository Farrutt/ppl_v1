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
from db.db_method_4 import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *
from api.memory import *
from api.ocr_api import *
from method.sftp_fucn import *
from method.callwebHook import *
from method.pdfSign import *
from method.cal_file import *
from api.schedule_log import *
from method.cal_BI import *
from method.cal_taxId import *
from method.cal_tdcpm import *
from method.cal_step import *
from method.migrate import *
from api.schedule_rpa import *
from api.schedule_mail import *
from api.schedule_chat import *
from method.cal_pdf import *



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


# def service():
# # #     doc_tmp = ['c7553fc0-46a0-46c7-8c7b-0e5d10e5fbfc']
# # #     group_id = '871bacdf-9415-412d-b26e-8cb82a30e03c'
# # #     result_checkstatus = select_3().select_querystatus_group_v1(group_id)
# # #     if result_checkstatus['result'] == 'OK':
# # #         tmpmessage = result_checkstatus['messageText']
# # #         tmp_email_middle = result_checkstatus['email_middle']
# # #         tmp_document_type = result_checkstatus['document_type']
# # #         if tmpmessage == 'N':
# # #             if arr_status.count('SUCCESS') == count_doc:
# # #                 unique_folderFilename = group_id
# # #                 chat_sender_group_v1(group_id,None)
# # #                 if tmp_document_type == 'SCS' or tmp_document_type == 'SCST' or tmp_document_type == 'CS':
# # #                     call_service_BI(group_id,'','','','','','')
# # #         else:
# # #             result_select_email = select().select_datajson_toemail(doc_tmp)
# # #             if tmp_email_middle != None:
# # #                 mail().sendEmail_center_group(doc_tmp,tmp_email_middle,tmp_document_type)
# # #             chat_sender_group_v1(group_id,None)
# # #             if tmp_document_type == 'SCS' or tmp_document_type == 'SCST' or tmp_document_type == 'CS':
# # #                 r = call_service_BI(group_id,'','','','Approve','','')
# # #                 print(r)
# # #             if tmp_document_type == 'TSFN' or tmp_document_type == 'SFN':
# # #                 call_service_pettycash_v1(None,group_id)

# call_service_BI('46e7b19d-2846-436d-bf25-2fc8b25da074','','','','','','')
# def service():
# # # #     #     documentType = 'csngs'
# # # # #     listDoc = ['cspoc','cs','scs','tm','scst','po','cerhr','spo','tms','poc','pcm','chman','csact','csnib','csttm','cstdc','csims','csman','csinb']
# # # # #     print(documentType in listDoc or 'cs' in documentType)
#     sid = [
#         '29a5dfad-c67c-4a45-b41b-620e1fec5c2f'
# ]
#     for n in sid:
#         print(n)
#         update_4().sender_status_doc_v1(n)
# service()
#     tax_id = '0107538000321'
#     sql = '''
#         SELECT
#             "tb_step_data"."biz_info" AS "business",
#             "tb_step_data"."update_time",
#             "tb_step_data".data_json,
#             "tb_send_detail".sender_position,
#             "tb_send_detail"."send_time",
#             "tb_send_detail"."status",
#             "tb_send_detail"."sender_name",
#             "tb_send_detail"."sender_email",
#             "tb_send_detail"."file_id",
#             "tb_send_detail"."file_name",
#             "tb_send_detail"."tracking_id",
#             "tb_send_detail"."step_data_sid" AS "sid",
#             "tb_send_detail"."doc_id" AS "document_id",
#             "tb_send_detail"."document_status",
#             "tb_send_detail"."status_details",
#             "tb_send_detail"."status_service",
#             "tb_send_detail"."filesize",
#             "tb_send_detail".template_webhook,
#             "tb_doc_detail"."documentType",
#             "tb_doc_detail".options_page 
#         FROM
#             "tb_send_detail"
#             LEFT JOIN "tb_doc_detail" ON tb_send_detail.step_data_sid = tb_doc_detail.step_id
#             LEFT JOIN "tb_step_data" ON tb_send_detail.step_data_sid = tb_step_data.sid -- WHERE tb_step_data.data_json like '%wanchai.vach@one.th%'
            
#         WHERE
#             "tb_step_data"."biz_info" LIKE '%''' + tax_id + '''%' 
#             AND "tb_step_data".update_time >= '2020-10-26 00:00:00' AND "tb_step_data".update_time <= '2020-10-27 13:00:00'
#         ORDER BY
# 	        "tb_step_data".update_time DESC
#     '''
# #     sid =['ef1c54ab-e6f1-49ce-a052-9293d0194dbd', '880f6e36-e59e-48d0-8398-aa597fa5f97f', 'b398fed8-bd20-4144-a728-8e64282c81dd', '85ab935c-8b00-4790-a571-86b64588f9be', 'd93165b3-5227-4a1d-ad71-1d3dd744ee45', '6af62c5a-a28a-4eb0-84aa-b8b0cfc8badf', '182c1672-e247-40a0-ac0d-4059ec52368c']
# def check_group_approve():
#     sql = ''' 
#         SELECT
#             "tb_step_data"."biz_info" AS "business",
#             "tb_step_data"."update_time",
#             "tb_step_data".data_json,
#             "tb_send_detail".send_user,
#             "tb_send_detail".sender_position,
#             "tb_send_detail"."send_time",
#             "tb_send_detail"."status",
#             "tb_send_detail"."sender_name",
#             "tb_send_detail"."sender_email",
#             "tb_send_detail"."file_id",
#             "tb_send_detail"."file_name",
#             "tb_send_detail"."tracking_id",
#             "tb_send_detail"."step_data_sid" AS "sid",
#             "tb_send_detail"."doc_id" AS "document_id",
#             "tb_send_detail"."document_status",
#             "tb_send_detail"."status_details",
#             "tb_send_detail"."status_service",
#             "tb_send_detail"."filesize",
#             "tb_send_detail".template_webhook,
#             "tb_send_detail".email_center,
#             "tb_send_detail".recipient_email,
#             tb_doc_detail.digit_sign,
#             "tb_doc_detail"."documentType",
#             "tb_doc_detail".options_page ,
#             "tb_doc_detail".data_document ,
#             "tb_doc_detail".attempted_folder ,
#             "tb_userProfile".p_userid,
#             tb_pdf_storage.string_sign
#         FROM
#             "tb_send_detail"
#             LEFT JOIN "tb_doc_detail" ON tb_send_detail.step_data_sid = tb_doc_detail.step_id
#             LEFT JOIN "tb_step_data" ON tb_send_detail.step_data_sid = tb_step_data.sid 
#             LEFT JOIN "tb_userProfile" ON "tb_userProfile".p_username = tb_send_detail.send_user
#             LEFT JOIN tb_pdf_storage ON "tb_pdf_storage".fid = tb_send_detail.file_id
#         WHERE
#         "tb_send_detail"."step_data_sid" IN (
#   '6d40f08a-fce8-4844-a287-609f8ee94e51', '26fb4a0d-4c78-49ee-876e-8ff6eca4cb52', '01eac742-69e1-4edc-96b4-15b0a1572de3', '56167f65-a128-49cf-941a-88fa8d21e0e1', 'da1290ef-05b4-4b39-a778-c2468dd78bb2', '76094c88-780c-4735-8f61-06c73f2bf971', '0eababf4-548e-4aeb-bed1-823649747d81', '11683ce5-9752-4f56-ac71-f71d62b8fb7e', 'd7d640ed-1374-4151-9370-f4eb21cddd18', 'b6574d04-8e4c-4170-ad81-b2b304bf570c', 'c4994067-d698-42aa-af0a-0591fe4f2073', '3075f3db-0c74-4ca2-a4cf-f9ad2be7af3d', 'ee5768c0-fc5b-4212-923e-e19af15eecea', '168f46fd-a70f-4fed-ac8d-0e352f0ca3a8', '4ac93455-e3b1-46c8-8712-435caf0dc99f', '2df062b0-eec6-408e-af15-20ad36e38422', '7b104924-d569-4615-83d2-47fe8f4d0e7e', '0e6e5593-0853-4ada-aab0-33724a0ff54f', '029fa6da-bef1-4336-820f-36b44f310e42', 'd8a161b2-5d5a-4c20-aec6-cac3dd52f57d', 'bd051123-5169-4594-a58f-212b6af6d47f', 'b523aff5-71b9-42b6-9ae7-4ad5e4e60615', '59f1402f-f6c9-4c0b-a56c-bffe321efe34', '84cf9d03-933a-472a-8eed-74e9c2ef9d0c'
# )
#             ORDER BY
#             "tb_step_data".update_time DESC 
#             LIMIT 50
#     '''
#     connection = engine.connect()
#     result = connection.execute(text(sql))
#     query_result = [dict(row) for row in result]
#     for n in query_result:
#         print(n['sid'])
#         tmppdfSign = n['string_sign']
#         url = 'https://paperless.one.th/paper_less/api/convert2/pdf_image/' + n['sid']
#         info = {
#             "base64_PDF":tmppdfSign
#         }
#         callPost(url,info)

# check_group_approve()
#         n['data_json'] = eval(n['data_json'])
#         result_select = cal_sender_status_document_v1(n['data_json'])
#         print(n['sid'])
#         detail_status = str(result_select['messageText']['data_document'])
#         document_status = result_select['messageText']['status_document']
#         tmp_step_now = str(result_select['messageText']['step_now'])
#         tmp_maxstep = str(result_select['messageText']['max_step'])
#         sql_update = '''update "tb_send_detail" set "status_details"=:tmpstatus_details,"document_status"=:tmpdocument_status,"stepmax"=:tmpstepmax,"stepnow"=:tmpstepnow WHERE "step_data_sid"=:tmpsid '''
#         result = connection.execute(text(sql_update),tmpstatus_details=detail_status,tmpdocument_status=document_status,tmpstepmax=tmp_maxstep,tmpstepnow=tmp_step_now,tmpsid=n['sid'])
#     connection.close()
#     for i in query_result:
#         print(str(i['id']))
#         group_id = str(i['id'])
#         result_checkstatus = select_3().select_querystatus_group_v1(group_id)
#         if result_checkstatus['result'] == 'OK':
#             tmpmessage = result_checkstatus['messageText']
#             tmp_email_middle = result_checkstatus['email_middle']
#             tmp_document_type = result_checkstatus['document_type']
#             if tmpmessage == 'N':
#                 if arr_status.count('SUCCESS') == count_doc:
#                     unique_folderFilename = group_id
#                     chat_sender_group_v1(group_id,None)
#                     if tmp_document_type == 'SCS' or tmp_document_type == 'SCST' or tmp_document_type == 'CS':
#                         call_service_BI(group_id,'','','','','','')
#             else:
#                 # result_select_email = select().select_datajson_toemail(doc_tmp)
#                 # if tmp_email_middle != None:
#                 #     mail().sendEmail_center_group(doc_tmp,tmp_email_middle,tmp_document_type)
#                 # chat_sender_group_v1(group_id,None)
#                 if tmp_document_type == 'SCS' or tmp_document_type == 'SCST' or tmp_document_type == 'CS':
#                     call_service_BI(group_id,'','','','Approve','','')
#                 if tmp_document_type == 'TSFN' or tmp_document_type == 'SFN':
#                     call_service_pettycash_v1(None,group_id)

# check_group_approve()

# select().select_filter_sidcode_to_group_v2(['ce0bcc2f-1ddc-47d8-86d5-83cf11ca8df4'],'suwanan.ch@thai.com')
# call_service_BI('0efe9003-434c-48ee-980f-b2ea557ac621','','','','','','')
# call_service_BI('6a655728-52cb-4e26-9b8a-5dad947e5d62','','','','Approve','','')
# call_service_BI('','0389183359045','','','','','3328950b-baaa-4447-affe-96a3fcb67178')
# select_4().select_taxId_Admin()
# v4 ตัด document_type ออก
# call_serviceOTHERs('3dd2364b-b5de-4ece-843c-6f8e1ec285a8')
# call_service_QT_BI("8a86202e-1a08-4777-85e0-8a68f9f2317e")
# r = select_3().select_trackinggroup_v1('026bb79c-980b-4c6c-990b-9e687df96fd6')
# print(r)
# def service_email():
#     r = cal_status_group_v1([{'email_one': ['jirayu.ko@thai.com'], 'name_one': ['จิรายุ กรพิทักษ์'], 'status': 'Complete'}, {'email_one': ['warud.mi@thai.com'], 'name_one': ['วรุจน์ มินสุวรรณ'], 'status': 'Complete'}, {'email_one': ['farrutt.th@thai.com'], 'name_one': ['ฟารุตต์ ธีระรังสิกุล'], 'status': 'Complete'}])
#     print(r)
#     tmpid_process = '839c0fd8-fcaa-419f-9c80-b7d975384754'
#     email = 'jirayu.ko@thai.com'
#     group_id = 'c2add259-177a-4216-a6bd-e8cbad80b740'
#     arr_status = [{'sid': '6ca4dd36-7c0b-4807-919e-cbdb29e9bc7a', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': 'cdf38fb4-1722-4a5f-bb9b-d8e7cc59b80f', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': 'f24dcd5c-3c80-4485-9100-b4bde913bf52', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '9fe7878a-78c9-4b4f-bc8f-6437b2571a62', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '4b6616c6-9ae2-447f-95eb-8e706011884b', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '30853e24-a81b-4862-86ef-763d0df5b228', 'email': 'jirayu.ko@thai.com', 'status_document': 'Fail', 'errorMessage': "Authorize Service Timeout HTTPSConnectionPool(host='uat-sign.one.th', port=443): Read timed out. (read timeout=5)", 'step_num': 1, 'errorCode': 'ERSIGN002'}, {'sid': '50d31dc6-629c-4dd2-819d-783202632d96', 'email': 'jirayu.ko@thai.com', 'status_document': 'Fail', 'errorMessage': "Authorize Service Timeout HTTPSConnectionPool(host='uat-sign.one.th', port=443): Read timed out. (read timeout=5)", 'step_num': 1, 'errorCode': 'ERSIGN002'}, {'sid': '9c723249-a80f-40cb-95d8-97e4afb86275', 'email': 'jirayu.ko@thai.com', 'status_document': 'Fail', 'errorMessage': "Authorize Service Timeout HTTPSConnectionPool(host='uat-sign.one.th', port=443): Read timed out. (read timeout=5)", 'step_num': 1, 'errorCode': 'ERSIGN002'}, {'sid': 'e07e37e9-9a6d-450d-89cd-0be281ae76ef', 'email': 'jirayu.ko@thai.com', 'status_document': 'Fail', 'errorMessage': "Authorize Service Timeout HTTPSConnectionPool(host='uat-sign.one.th', port=443): Read timed out. (read timeout=5)", 'step_num': 1, 'errorCode': 'ERSIGN002'}, {'sid': 'a62b28a7-5888-40a3-ae04-1a88b4064567', 'email': 'jirayu.ko@thai.com', 'status_document': 'Fail', 'errorMessage': "Authorize Service Timeout HTTPSConnectionPool(host='uat-sign.one.th', port=443): Read timed out. (read timeout=5)", 'step_num': 1, 'errorCode': 'ERSIGN002'}, {'sid': 'f21e797e-d5b2-413e-900c-485bf387d01c', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '0a5e5dac-1bc1-4ce1-959f-9266cdd77f06', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '4d517bf4-a9e2-4d38-9cd6-00adaeda552d', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '1099a1d4-1217-4117-9ed1-b0238d20d407', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': 'a6ad8c7f-e071-4fec-ab46-2428282288cf', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': 'ababa943-b5a2-4452-8d31-c07291b649c2', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '3dc61ecc-1538-4a13-831a-070192ea6871', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': 'afaa0d9e-97c3-4825-ab08-8bbae9ce6a64', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '355f1e94-3d6f-40b1-9b8e-c489e4ee8b92', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': 'a986eddc-8cfa-4b72-a2ee-9f51c3ae60e2', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '88b2c070-9455-4dfc-b51e-26c1f6d891fb', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': 'ab462585-8d28-4fab-b3fd-a8298fc1c64b', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '6894b651-7b28-4157-b270-01265acc0dcd', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '1882cb88-946f-4d38-8dbe-267e0a66d0ef', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '50c80c89-0b9c-48f8-837f-d9d13c658fa9', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '3fcea922-cc25-4b33-9216-e16b017ed727', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '0472871a-4259-41a8-aa3a-58fed571a55d', 'email': 'jirayu.ko@thai.com', 'status_document': 'Fail', 'errorMessage': "Authorize Service Timeout HTTPSConnectionPool(host='uat-sign.one.th', port=443): Read timed out. (read timeout=5)", 'step_num': 1, 'errorCode': 'ERSIGN002'}, {'sid': '1402567a-c517-4986-a9a6-c2c532c40fbd', 'email': 'jirayu.ko@thai.com', 'status_document': 'Fail', 'errorMessage': "Authorize Service Timeout HTTPSConnectionPool(host='uat-sign.one.th', port=443): Read timed out. (read timeout=5)", 'step_num': 1, 'errorCode': 'ERSIGN002'}, {'sid': '5a98369f-f6e8-4656-83f6-70401e050f81', 'email': 'jirayu.ko@thai.com', 'status_document': 'Fail', 'errorMessage': "Authorize Service Timeout HTTPSConnectionPool(host='uat-sign.one.th', port=443): Read timed out. (read timeout=5)", 'step_num': 1, 'errorCode': 'ERSIGN002'}, {'sid': '16cce664-9578-43f1-b2bd-03ccca764a0d', 'email': 'jirayu.ko@thai.com', 'status_document': 'Fail', 'errorMessage': "Authorize Service Timeout HTTPSConnectionPool(host='uat-sign.one.th', port=443): Read timed out. (read timeout=5)", 'step_num': 1, 'errorCode': 'ERSIGN002'}, {'sid': '274456c1-f514-4686-b1a6-2c13baef591a', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': 'e97b35f6-a762-4463-867e-3135496dd880', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': 'ae546658-93e8-4a80-b83a-f8e8c9944d22', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '6dae3b46-af1c-493f-8f9f-777a3adb80df', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '460c8f2e-2b3c-435a-8c98-c1802c796f67', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '068a52d2-aa2b-4a9c-a087-9d74b32240dd', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': '255de2e4-1785-4591-b7a1-93f2e1ff9eec', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': 'd4b74dfe-24f7-4757-9a5a-e816fc7a8af3', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}, {'sid': 'e3721d96-940e-4210-b24c-e90eac71185b', 'email': 'jirayu.ko@thai.com', 'status_document': 'Complete', 'errorMessage': None, 'step_num': 1, 'errorCode': None}]
#     for n in range(len(arr_status)):
#         tmpsid = arr_status[n]['sid']
#         if 'status_document' in arr_status[n]:
#             statustmp = arr_status[n]['status_document']
#             print(statustmp)
#             if statustmp == 'Fail':
#                 status_fail = True
#             else:
#                 print('other')
#                 # result_function = other_service_cost(tmpsid,token_header)
#     # print(status_fail)
#     if status_fail==True:
#         print('update')
#         resultUpdate = update_3().update_process_id_log_status_v1(tmpid_process,'SIGN','FAIL',str(arr_status),group_id,email)
#     else:
#         print('update group')
#         update_2().update_status_ingroup_v1(group_id,email)
# sid = ['67b84ab3-bd03-4e6d-a945-a26426be1d47']
# for n in sid:
#     print(n)
#     r= update_4().update_step_test(n,'wanchai.vach@one.th','A03','Complete','7',0.00,0.00,'','')
#     print(r)
# r = select().select_transactionfile('53f77fa9-3237-4bc4-b52b-14784b934244')
# print(r)
@status_methods.route("/email_send",methods=['GET'])
def email_send():
    if request.method == 'GET':
        token_header = request.headers['Authorization']
        listsid = [
            "9143de0c-89d4-4e32-ad76-b0c056cef6a7",

            "f8f87101-e37a-45ad-8123-920feb9e70e2",

            "67cea844-5da9-475c-8186-e567a0a8d74d",

            "5d112002-42ad-45c5-88a0-58f3bba79c3e",

            "6b8dde05-4097-4f0e-926a-8ff571605367",

            "ce4c0b90-63db-4404-a441-d23620aed07f",

            "dc5f9648-aea5-4884-8d6b-2363aa4a2568",

            "5a44b385-4583-4b11-90da-74065d182bfd",

            "4f2d606d-5bbf-4084-807a-0f0f851c26c5",

            "ec4e7c11-5017-47d7-997a-61a6561fa9c9",

            "5944401b-1828-4dd7-8e09-e28778421461",

            "a675c455-1692-468c-937e-c57638776ba9",

            "f7a056c1-1058-4f8e-a447-ebd8ee2bd7ac",

            "cdeeb589-340c-4638-9f75-b028add42809",

            "ccd00c9c-5221-470c-8594-a90a435a81be",

            "f4f17866-2bed-450e-ab92-e1af6eae05ce",

            "f76b4e3c-4e7d-41ce-b044-3b5d1281c78e",

            "299dd762-63f6-4484-8bbb-10eb77f2754c",

            "b380ec75-c63f-44d2-b1ff-f06752fbdcc2",

            "20e7cdae-9797-4ada-b3a0-037f6c53ffc6",

            "2094f99a-e375-444a-a708-5eaee39347af",

            "597ea99a-5f27-4e06-900f-ab5dbe31f38f",

            "cfe7bbf3-af55-4a9a-84a5-63eca8fe8a84",


            "67f3ffbb-d308-4024-ba24-3abe05a5bcb5",

            "4d694087-d393-421c-9085-5ba4d0e6ec2f",

            "ed4eeb73-8596-4b19-b5a6-4374a06071d5",

            "3270901a-8454-4880-8c41-e7e5f99b67d8",

            "928193fe-c37b-4545-9520-1f49ed0f9739",

            "7ca94887-4154-482b-ae42-e5d921e8cb2f",

            "e1b1dfbd-d8f3-4411-b5aa-e37a06cce680",

            "c9290601-c903-4da8-8145-f38f2c0876f7",

            "41985afb-72f4-4ea9-9b93-96006a57f491",

            "f344a8ef-fbc9-4d80-bbf5-f0a04be5cabe",

            "27160230-ab6f-489e-b784-43877492319b",

            "1878104b-ccee-46ce-ac58-c30bae17698c",

            "05445840-e464-45de-878e-8a99012d4dc0",

            "591c7f42-5982-46fd-8b78-c24394eaaecb",

            "87b2244b-734c-4fcb-b9ee-80a4a9e14258",

            "17630f37-ad13-4d4d-80b4-5c4226158112",

            "1f729b7b-70db-4f6e-94ac-ffabaf31e8aa",

            "cfef4fb5-6f0d-4b3d-b0ad-df07056248fa",

            "e30b24b0-a04c-487a-b1bb-2b7b2d2f6a49",

            "34b6fb3a-dd51-4560-8dac-5eb0f661f5a9",

            "548cc8b3-9fe9-4c81-bed6-4403abf45b06",


            "9c08d521-e0b5-4367-b82f-e8cbd627397c",

            "b2d57931-5ff3-4bbd-af57-b9f53a6447c8",
            "caa44e23-6fc8-4960-94ae-cbf306660bfe",

            "a0a9caea-2b53-4c17-8852-3ddbf244acec",

            "220b0964-0ff8-4898-b957-a2bc280b92ed",

            "99570c3d-7f4c-4404-bd7b-f136654d0960",

            "4d35e219-ea56-4ad4-8fc0-f8e4cf355707",

            "834c856a-efe0-495f-930e-a1434dc6ed59",

            "79910537-f037-478c-9131-56ecd40516e9",

            "8cd6ff42-219c-422b-91b4-9c546d21bff8",

            "b110b6ef-3c78-4b7c-8e41-e6f95c0dcdae",

            "ec0678a5-5eba-4107-b855-2ad0de81736f",

            "2f510c82-8300-4223-af44-7fbbc21cf3ac",

            "bf906f5e-ab03-491d-9e2a-f74f74e3e528",

            "1dbbacd6-428d-4dcc-b5b9-292ffa25768e",

            "5e575123-19d6-4133-9e85-59777bfaaceb",

            "a8c2686e-0333-4e2d-8f56-caeef5f09c52",

            "d1d433ce-10a1-45bb-bc73-474ac51b0f86",

            "b7e5bfc0-a06e-4f40-926f-b59ca8f7ec4a",


            "e5fb0ac9-d5a0-491f-ad4c-82fa8c565f39",

            "9ab003f2-dde2-4588-bd20-571f82759e50",

            "4e684ab6-da17-4382-adc1-ec8ae66c7091",


            "7e514c4d-a2a4-4625-aaf0-aa93fc11f85e",

            "05997ead-0988-4b3c-be9b-de30a8ea7ae4",

            "a1cd7977-751e-4678-afa1-769371e5bb67",

            "ff4df98f-b872-49f9-abf6-89e181bb575a",

            "34340322-2bde-4a2a-a61d-a99c4862451a",

            "d351671f-97b7-4c01-85ea-a6ae5b065408",

            "8087556e-ff17-43de-b428-976fe34e529b",

            "f999546c-b682-4cbb-9603-00a2692649ba",

            "e5c4839f-dd16-4943-b089-da439bc64a23",

            "551a2577-9e02-4c21-a663-29cc491922d8",

            "38c94574-18ab-447a-b2da-b39071caf0b2",

            "38e6e23a-09f4-40af-ab74-1d320fa2e70f",

            "6952bea4-079e-4146-8b3d-1cae4c1c70d7",

            "d2731f89-b374-47f6-a10b-15050db7b4a3",

            "16f53a40-1eac-44a8-8226-6e24410735a6",

            "45d4245e-a7e3-4b00-ba0b-3cd89e1b43ca",

            "766feb90-fc99-42f9-9134-2b54cfe8f08b",

            "738fadb8-dcff-4b22-8bd8-8a98b2e99530",

            "5c81c848-97fc-43f3-b88d-5bd00106527b",

            "7ae0e1f7-80bc-4bc8-a56b-ed99699bdc09",

            "9b3b35d6-ad7f-4436-83b8-7e257eb5aa57",


            "3df19506-ba98-4933-b607-4691bef054f3",

            "3757725d-a208-47b0-b639-9f0086d1fa60",

            "fa407d3c-763c-4550-b1c7-4f8b87c87861",
            "7239e9da-48d7-42dc-861d-83c68c9adf4b",

            "d12ce599-66e5-4739-9566-cf62663ae97c",

            "39dc2e09-79af-4a98-bad5-dcbce8cabbf7",

            "a4380a09-c03a-4ba6-b6e9-22a3e247ba5a",

            "93fbdded-5a80-4389-ba0e-97c37986a393",

            "3e52bf25-4cd8-40bb-9461-0247f3b112a4",

            "24730136-2205-44c5-baeb-c77d2530d0f7",
            

            "c60e6f4b-7a60-4bc2-8556-a626680ce780",

            "9dbe173d-2908-40b3-940c-1c92209332be",

            "3c5e6d84-d3d1-4136-af01-da1927459109",

            "87de2a6f-ad3b-4144-b94c-f9cb032f78ca",

            "da88aabe-298c-42df-a208-dc1489d696cf",

            "a1944126-ef08-4f96-ab88-aa5c730e6eb2",

            "5226aa7d-c348-4409-812f-0615ba3b7608",

            "c4c58b23-835b-4168-bd35-79d882761875",

            "ba5a5fd9-4163-42d0-ac8a-60457d344e24",

            "8e0b60b3-3adb-4e37-af8f-7750c98a2ce7",

            "1da9eef1-129d-423a-b057-4fcbbe73d7d5",

            "aae72692-de69-4a9a-82ad-8fdb4ad69ff2",

            "a7135c70-1caf-4f17-a77f-f6b5cb77cd53",
            "5f2fe2b9-f868-4e42-a520-e56648d555ba",

            "e8b6373c-c12d-4374-893b-fd036f94dc40",

            "d528c98a-32db-4a4e-944d-c1a9c335acd3",

            "a68e2ac2-ce5a-4f39-97b2-0a04a779a242",

            "2cc5d2b2-9aa0-4aa7-b683-38f160e310ae",

            "cbc7418d-a641-4907-beaa-df7d35b3a644",

            "3f1822f0-6281-47f2-836e-e3fba0c7b862",

            "e83c18d0-50df-43dc-a1fa-7646550f263a",

            "be812a36-e8b1-4652-96eb-3f33edd9f868",

            "fb44f7d4-dc91-4b64-ae29-c7a798576a51",

            "538b464a-ee2d-4a1d-95b6-ee67d9bd1a21",

            "e740b670-e99a-4e08-95dd-7d015d306693",

            "2ab1d680-8ea9-4d72-9c47-98c76cf43e5f",

            "3e9e4f66-ad2e-4260-8d3b-09877087a0e4",

            "92f5feb6-1530-4574-a922-3b39506fa0b8",

            "d9b08c10-5c94-411b-b5fb-29034f3be46a",

            "7f08e77d-5eb1-4df0-9e14-477492edc96a",

            "a1cf0a51-6261-4948-8cec-d7786c77a9e1",

            "dcf848f2-0848-44ed-804c-b88e86d1c8e4",

            "480e3bfa-f238-41e0-9d05-4175f5b8a0cb",

            "653875fc-489d-454b-95b8-c2d2b0d6d2e4",

            "2738c86e-8f9a-4a97-bf5c-9446fcb9d865",

            "357e3d02-3846-4b38-9592-48defa0a5f6e",

            "aa730500-be15-4fd1-8ac9-5698d2156046",

            "c1e75fed-8159-4a20-b98e-2c4fef422c49",

            "0d952c1a-af90-40f6-bd1a-cb48116d7f35",

            "c99fff3f-74f5-4917-806d-80731af0fac1",

            "15cab44e-0ca6-4fd5-98d7-b873355bea3c",

            "5d9eec61-2a98-4fed-a49e-bd9e84c07625",

            "0882e90a-5085-414b-9afc-74414b9c8448",

            "42928baf-7851-42a6-91ba-b484fea1990c",

            "701652f8-5698-4203-b35a-3ba1b472a228",
            "a169ab01-d42a-4fe7-90cb-fa1a8f097d25",

            "db6f9046-0151-4939-a758-80e4f97815d0",

            "d462181d-3288-4ed6-80ab-f65a494f5cf2",

            "5f93543f-9c7b-4b1d-93e9-e1168135ddc1",

            "90ee9a7f-11c5-44bd-b5b4-137911ddffe1",

            "f337c84a-2278-4636-915e-369a55347dee",

            "9bbc0bd2-d586-4ce9-99c1-11f4226f3b9c",

            "9f74b2e9-f987-42c0-89ea-23a96957b70d",

            "b6aea6c7-eb39-48d0-a4e0-8b5aa4155d94",

            "750fc1f1-f120-4ae3-9cea-c8b9e2a6c4d4",

            "a743a97b-c6f5-41d2-856d-6c3a70cf09a6",

            "88aa5146-0a0c-4230-8c74-d81ee564a735",

            "7037b2c1-dd04-43ff-97d4-081ed9fdbb24",

            "b79d0e2d-c2d9-4fb9-9a58-3f223af38745",

            "29022fee-964b-4224-b8b5-f8a3ab6e3a8f",


            "c7ee8d71-e84a-4207-8066-d4408f9463fe",

            "9f675e35-6c3b-4c45-893b-d79b1b60ab3d",

            "16f80847-c8da-4bc1-af7f-0f35d9bac08c",

            "2e079d83-1394-403a-80dd-fb85b98f51be",

            "0b451dde-475c-4f3a-9e3e-b9d72a11307c",

            "0111aa3e-7046-4aad-8780-09a1db1cf4f3",

            "021ac849-c0db-4017-8562-6fe2e4b65b9b",

            "fd4df0b9-6d19-4386-856a-514ead1ee771",

            "5870b2bd-1aa6-4467-b1af-fa874c67b67b",

            "78b5bc43-7704-48cc-bb51-712e06dcd8a4",

            "5eaf361f-c7d9-4c0f-ab29-49f1f595ded6",

            "135f372c-4ee7-491d-adef-be60f608cb82",

            "4342f2a5-7dd2-471c-9dda-4179233b4ec8",

            "85befa96-d35c-43c3-81cf-75dc9da15b54",

            "d725891f-f137-44ba-b129-9e06040582a0",

            "061eb4c1-a4bb-4409-8a31-707b37a1bd97",

            "9e45c9d3-558a-473b-9483-6d92af75b230",

            "9ad7f3f0-0780-482f-8ad1-a637e914359f",

            "0fc223f5-3b7e-4aba-87aa-b74cb0e32be8",

            "f6cb0f27-f35b-4aa2-868a-fba32339cf8b",

            "d8df848b-0de7-446c-ba32-bc9758759a5b",

            "45141969-cde0-4881-9a73-a180ac89be33",

            "3ace49b7-3296-410a-921f-42392e2d7826",

            "862bc8da-e4ff-42a2-92e4-d2b62fe3e8c1",

            "a1ed887a-c1ef-4699-a7e1-7cb13b5d4fe8",

            "466795c8-bc8a-4add-bd39-e5862c6415c4",

            "e3f87c48-77e1-40c3-9b97-9f69ab8a138b",

            "1bc7eb17-559c-4762-8e33-61ecaf5c7ea7",

            "c836ac94-6628-4483-9361-8b9b6e55b86d",

            "8da4c92a-5d67-4cb6-8623-2840b7c84b28",

            "058ed0b6-973c-4b5d-a627-09ee96c5125e",

            "9d6b45e9-907d-4f88-afee-93e0b9d4bae0",

            "9266b6bd-cd0c-45a0-9e23-2707f7ae169f",

            "051c8f14-b370-4af9-a200-b94ab13d1bdb",

            "041ef73e-914b-42a0-9f5f-ab28317c00f5",

            "30eb5cc1-a8ed-4a45-9fa6-ee49af7b80da",

            "168ceead-a29c-42c4-85de-be61511442da",

            "eb901eb1-e1c0-48e5-ac18-e805b0697214",

            "44c769f5-5d42-4119-9bae-790a9c9b1cb6",

            "896d61d4-858d-4885-919b-8d8307185f8c",

            "9e4c3dcc-c1b3-46d0-a6c4-c4ef21674087",

            "d757a22a-6c1e-4e97-8800-e01007d47319",

            "11b27097-f14f-406c-a482-c177cb25c566",

            "efffed3c-4ba1-49b6-af45-412e09037eac",

            "ed8ada34-748a-46aa-93ef-4cc8f58394f1",

            "103210ac-8a2c-468b-87ab-47aa12caf87e",

            "07a93be5-ac37-4cd3-9058-e2122440ea11",

            "29a39862-136c-4e66-a0d1-cc714df33e3b",

            "b2d33309-6901-4dd3-b811-c3f73c64bb03",

            "c4e69e64-fa7c-44a3-9d52-eab09f1eff4a",

            "ae3c5a09-cd3e-4f82-ae09-f26970f10ec8",

            "d12b4ce0-43d1-412e-a52b-de9c1b82b8cc",

            "48aca040-1002-4f7a-aeb1-280f7893b430",

            "0b15aa67-e978-4307-8bae-f1f8d57c7e52",

            "eab73355-8f06-4c92-80bf-936eb325f5e5",

            "ec82d7cf-da07-4069-b1d1-87d8efb2e2a5",

            "cb96f7ee-dba1-4597-ad1a-d86fd2825535",

            "bc7e8028-2f04-446e-8501-2e01fd9d7cc8",

            "37283f1d-1f33-498d-bdaa-4be9b940621f",

            "ed2ca9fd-0b10-46c6-a5fa-bcdd373b1391",

            "58207e43-4e52-4b3c-b016-03e90304cf13",

            "db8c0405-9622-4048-a7d8-7befbeebe146",

            "b6ce627b-dd29-401f-991f-1d56d27cce10",

            "0b493536-591b-4d3d-bfc9-3c1cce844eea",

            "88a7a850-a6e7-4319-8dad-07909f2d4df7",

            "6bd38afa-3ae3-42e0-9100-b04c8377ecbb",

            "05f2ef44-47a9-4bff-a351-8c160b46df8a",

            "8fe4cfa2-c357-4d11-a94a-8f84d32e36c8",

            "ac5af1ef-ee19-4bd3-b5a4-701d096016f2",

            "7f39239f-790e-449a-8270-abb6cd014590",

            "7c08be1d-c7d2-4f52-a01e-72a4b08009d7",

            "9c397df0-d6bc-4f6d-b895-c19e5d26e83e",

            "c55ecae9-b35e-4666-9c53-e2a5f8a4fc97",

            "2f20fa40-261a-4bf4-a276-8ea27f52de62",
            "a59b85ee-856c-4806-b553-3a4cfb3f50e9",

            "7792d337-303c-47ed-a2f4-bdec600da0e7",

            "4f734f62-9fc5-4740-893e-8b7b914cbec5",

            "504b3902-47c7-4087-bdbb-161e3fa9fbe1",

            "82ec0093-66de-4bb0-9088-19e8a3f0c98f",

            "501a45a1-bfa3-48fa-8e7c-73c9604875fe",

            "9b8462a2-cbde-44e5-b48a-29c936470ce4",

            "df39ca11-0eaa-4117-9577-34214c6a54c4",

            "6f2a7d33-42a1-49af-9174-4c287816b637",

            "1796a888-421f-4b07-91ed-c967251573ef",

            "e0ca0896-3f34-45b4-bf02-7cfabe3e581f",

            "8cc1c093-da84-4e5f-acef-8091a47cbd4f",

            "a99b9417-2ef9-4a6f-94be-916cec71afca",

            "6f9e52a6-3400-4e56-b0ed-01b789b9e7b8",

            "db09e677-5415-45c5-8449-ad98427e1d6f",

            "305dcbc4-c446-471c-949c-5549468cfd5e",

            "5e23c520-b4bf-4c8e-9d8a-ff7655fa4a2f",

            "a5660386-fef0-4f0e-95a8-cc98d81d51db",

            "317994ed-c8d9-4fb2-b432-59e519cb99f7",

            "a85dab52-9a12-4d91-aa01-811dc66c51b0",

            "54d3793f-60c8-4195-99ba-fa49dfcec0a2",

            "d1954681-ce81-4722-8bf6-6ff8afa1be7f",

            "aa01c61d-06e0-41c5-bf06-0598a2f32edb",

            "3b410c00-2370-48f3-9608-4c3f6d448804",
            "e417ebdb-16ea-45cb-aa36-ab07a6b5411c",
            "818be9bc-e3dc-47b5-bb2e-a5c07f647382",

            "15c6f7e8-13d3-4ccb-8814-ca70132af3c1",

            "eed2bcb3-5853-4376-87ec-5822cd949943",

            "f738e26e-ef79-4229-8322-8ddadf61019c",

            "28ad2471-67e9-45bc-9558-62e3a1a1c99b",

            "8fb7a8dd-9aa0-4185-8299-7611e28ba7f0",

            "0a9f309d-5e48-4885-9459-44e6ffe998cd",

            "abba9609-0f76-4880-a1fa-7476899c7b07",

            "f604d9d2-7d3c-4e2f-ae12-a554cee426bb",

            "1e4c03e3-ebba-4152-8961-6846649b6377",

            "e5ba1ad0-594d-4dac-a0e7-4496c73874f9",

            "0c4d02bd-d9fc-45f5-863d-22441f95f454",

            "5f4f1742-e44b-47b5-9249-2cf9d056cfd7",

            "a1bbd473-d954-4082-a6df-c7ea9b9c453f",

            "d34fe200-e1cf-4fce-a9f2-20bc60fd4ce9",

            "4991927b-ed69-4fb2-89df-02ac23a4494e",

            "5592a7bc-cc90-427a-93ed-dbdea109ac23",

            "1fade25f-b00c-4608-ba74-4c74809c177b",

            "64aa15ba-bf19-4b58-b122-c112eaa38ecf",

            "0e877f39-f9bf-40b6-b810-61add78df904",

            "7d3c5746-923a-45eb-bf79-ae122efbfd94",

            "91675fc1-146d-4786-bf47-b0b713b22308",

            "6ca11a66-adb9-4d54-941c-deb010d5bf8d",

            "ca822f6d-ea59-4430-859d-2267b528cfec",

            "f6c9a10f-8496-4f73-a4e6-19c0438c4ecd",

            "3f8aadfb-7622-4b28-b383-dbfe88f3101a",

            "ac4e902d-2428-468f-80b8-8d6313f7c9a4",

            "7f0ea6c6-95eb-4561-8273-f90f98b2c124",

            "9d828923-b572-4623-90b2-cdae2dd2f3fd",

            "00a3a1bb-e215-4e38-b198-70733557738c",

            "93912eb4-2f86-44ec-8fc4-17248ccd4b68",

            "27cc54e2-d213-46da-9528-fd0f968ef141",
            "f33825a1-02b1-461b-a6e6-6fe3ec1bdc8a",
            "f8ba4ea2-08d9-41f6-9fa2-5e1605062f79",

            "0909f9c6-f172-4f2f-bec8-709a6d7f4dd1",

            "98eb66f8-bdfc-45cd-9679-9ea775814098",

            "3e92ecdb-607c-4786-83d1-29746f0d04be",

            "ed549beb-b931-4f46-96eb-38533d8eabba",

            "ea4b803e-88d9-4c10-9785-3f2904e5fa7a",


            "1498991f-000e-482a-b175-aa06d057844d",

            "6ecbf84b-9bef-4717-a391-d2bf1f8c465e",

            "e36a19e3-fc46-4b97-a612-da35d38e3cf6",

            "25a618a8-fbc5-4cb1-9050-f481e622f686",

            "ea77b4db-5ce4-43ca-afe2-a224bb36a7e7",

            "e358855e-3d4b-45ec-926a-03cf89dc616b",

            "1dc15cdd-1a58-4b85-86e4-30f9630a4899",

            "a6e5c786-ae3a-41ce-bd57-ab5f22bed564",

            "87cb3969-0da9-4ff5-8ba1-554a84a2c9fb",

            "c8b92907-0d1c-4e2c-bf1a-c85c1d50da52",

            "41d14339-c262-48dc-a9d5-79e0fadc3e72",

            "46e5b80a-ba86-4e2e-97c2-ad9bf1c4b49c",

            "4ab53112-ecd1-47a2-93c9-fc47656ad9d4",


            "791cc9fc-e072-49e6-8c52-d8f38fa3424e",

            "9bd378ac-06ce-49f0-bf6f-1b139453ec8c",

            "cd0e7965-ed0a-422f-b78e-4cf218a23aab",

            "a2317d02-e2ca-44cf-85ba-552035b5eecb",

            "ac101388-d3ac-47b1-b349-d167c341fa2c",

            "175fd837-6d97-4abe-b3aa-7e1a15af57f9",

            "eaf15e37-3181-443b-974b-8812cfeba23f",

            "fb905e94-3d40-4104-a1a7-eca0a5c1efe4",

            "79e93955-3449-47cb-b64b-ec54fbe337e5",

            "85184b6c-97f7-40b3-90f5-c1e0bb1319b1",

            "be807e92-2525-40dd-89e8-64d8fcc879a0",

            "e6741689-da96-47b8-b939-9ab0bc2cd643",

            "0839c67e-c595-4310-86cd-f225f92f43d8",

            "d2d96fb3-eae0-4531-99e7-6f243ca4341d",

            "5370fad3-2f7d-4b8c-a47d-8832d868235a",

            "1e845433-ebdd-4c63-a27e-7fa1e2465c8a",

            "520104a5-eb3c-401c-b1d0-b89401da2ce2",

            "6d85ce4e-29ca-4bbf-84da-537400c3b08e",

            "18c6cfb8-17e2-45cc-b9dc-68d311b5fad1",

            "abddf065-f7ed-4023-87b1-df9c695e07fa",

            "38cb4f14-f053-40bd-890f-9d12ca8304a8",

            "e19710a5-2ef6-4a3d-8c6b-1413ecac9a38",

            "981d8e4f-608d-49c5-8dbe-0ecf7e599f00",

            "79f9d305-ffa9-4c3f-b750-dbc96657df81",

            "e0bd9059-5244-4cef-8159-957e3e0018bd",

            "1b008577-a794-4fbe-95af-8bfc9087630c",

            "a8b2144e-dafa-4552-8247-a60d4a8d42ad",

            "c871e8b7-7106-4a92-a52d-73a489f12450",

            "3a3e29c9-d9eb-4480-a343-058e46584eee",

            "d49ec390-6b5d-4f42-9be9-940653ef3484",

            "db9214b8-183f-416c-9fb2-420a80d37bc6",

            "d30a1414-29c8-4221-810d-931aa7e1d6bf",

            "d27e4685-c8a1-48ec-9f5a-24a673c3e3ff",

            "84d301e5-5d78-49b6-a0c5-ff869d1a6789",

            "775f2664-daad-4955-89d4-2ff4db987b23",

            "a4721607-27d1-4b48-82cd-da474e5699fa",

            "d9e65329-6e4c-480a-adf7-51fde3999a36",

            "35c49988-658a-4565-8111-1ed975cc6b7e",

            "88baa767-0b1c-4507-a8f6-6638e46e65a9",

            "524f49b5-d091-42d6-b95e-bfa409f2878d",

            "65e914ae-378d-47aa-8e16-65988ca91ad9",

            "f01ada8a-b84c-43c0-8f98-13becd472d3b",


            "b504b271-9a69-4ee8-b614-19c46dd9f9e9",

            "6ffe5021-6a97-4f4c-8e18-a64f71c3357b",

            "cca544d9-d560-4ae2-87d3-9cec9726b7bc",

            "1b92d4a6-5213-4fd3-8e76-f903ba08b44c",

            "407b92e1-3925-4c2b-85e9-299ea8f86a70",

            "15af244b-3fc3-4056-baf7-e31b8664362e",

            "74c5cf33-a101-4cbe-8b91-3d3740cbb443",

            "2f7d995c-7016-4651-9301-a9749d533bdb",

            "7f5d8609-9ac4-45dc-9215-98169fee3d84",

            "bd3e6c4f-6e7f-4094-bdba-52c28eb8cc8e",

            "3958bc87-afde-4627-ab25-aeee57ce8458",

            "84779036-2952-4aa3-a534-bf16ac6039f0",

            "6a7280f7-b9a1-4737-8cd8-6dfc3520f3a4",

            "f7cf737b-0e8b-49c2-a664-f6786b8a46bc",

            "62f2957c-ca8c-4abb-b039-0e1ac2da8525",

            "a038bf26-1857-4885-8bde-1af4e316aa27",

            "f2fa542c-adca-4177-8dc1-c51ad08f92a7",

            "7ce79f3a-59c6-4953-8b51-4d05cee3993a",

            "99b40001-1794-418e-b9cc-0670a8481154",

            "fd5806d2-1146-4acf-988a-1ea9714a414f",

            "4bb0441a-0e6d-4a67-a4f3-5df179e8558b",

            "425d1ab5-3093-4931-b99c-ccb11ac8712e",

            "b3c58747-c224-4734-8656-428cb414add8",

            "ed36f125-b155-495d-8e5a-0bfdaeb7cc61",

            "0fada2a2-a9a3-4758-965d-d51de3dbe84b",

            "76d835d4-dc99-4f1d-8c56-8445e653189e",

            "3c402773-8651-463f-868a-cb6afb84eb6d",

            "04054be9-f2ba-436e-8c0d-872aad528560",

            "376c3219-6195-4bd2-9dc4-9bf885cf1bb7",

            "14e64a06-46af-4424-9e29-a773342cddd9",

            "659ce1af-db88-4f8f-86d4-da7826e7f85c",

            "cb0316fa-9363-43af-948d-002c52561208",

            "119d3065-877e-4c96-81aa-5bd4e2ed56d8",

            "44390fb9-b559-4bbe-b392-7bb388494772",

            "1608c440-8841-4f35-a2e3-a9790d6321c2",

            "5a17aa8e-9c67-4ecd-afc4-7cd95e03bca6",

            "1c1b2cc5-10ab-4520-ac61-501072f72bd1",

            "56744d83-550d-4cce-8f8a-451108cfc148",

            "fa46441c-8b3a-4aa3-92ca-f07c52e73233",

            "84a78540-f3b8-41b2-be13-5224695a808e",

            "08244919-e09f-4864-8d48-87444fdfd743",

            "a81c8711-ae5d-4bbc-85f1-37df04c6c182",

            "b3b1d704-f671-4308-8bab-cf0692305b88",

            "d7b80749-47e0-4381-84cb-c729702116bb",

            "88c7d507-e764-4226-aa35-224f0b943e18",

            "06f55972-f7cb-4562-a7b8-120f13719f07",

            "03f00151-f802-4842-b7f0-7f7fc89622e1",

            "4f422816-0006-477c-a46e-496b5218f9c7",

            "ab73173f-a6c3-47b7-bccd-dea17c6ed1ad",

            "90a674e5-1b35-4287-9af2-9e7eb3447b1b",

            "00d3de8e-a860-414d-8b8d-bdfbbee6665b",

            "6614a6bd-eeea-4f65-ba2d-905e92e6671e",

            "9767a6fa-9035-4931-b039-81919c78e418",

            "c5287274-cab6-408b-8a2d-ca65f32b6993",

            "183bb24a-366a-4ace-b163-58b20bd7dcd1",

            "dbd77488-e7c2-4153-8d85-1faf3f315faf",


            "2a993f63-de9a-48a5-929c-ea7b657c130c",

            "8b983921-4f66-4c07-ae22-c8053aba5402",

            "22c61ce1-2227-4ecd-b59b-e15485569190",

            "a4a3b22a-4bc2-4373-ab08-60dcdfb09729",
            "2ad82862-d4e5-4332-ad1f-4dfcde4c5cb9",

            "c14d3888-41a5-4fcc-b830-7278b13fb01d",

            "9cb4d731-c1d6-4f49-80eb-ccba3e87122f",

            "93cb38a5-2595-41af-952f-f1712ae79d2a",

            "9bcc1527-361c-4cae-876e-0a9195bc09f1",

            "3f03e25c-960a-44e0-ae7f-39e749b4e18c",

            "595c1d94-b18e-4e62-aa49-03d2dbdaa9e6",

            "b638d065-3434-48f6-981b-3076e04e0f99",

            "4c92e9bf-954c-4306-a868-091547baa13f",

            "9203507f-b34e-4659-95b3-4b278331b4ba",

            "9c86ab49-b53a-45fc-837a-853c9ea703fa",

            "27065aa4-6ce8-4b2f-8a8b-0c732979794b",

            "91aad7cb-0e43-4fb4-a8a7-915b27aa706f",

            "ed967d3d-33bc-4c58-a80a-8acbefd32168",

            "be26481c-b1c1-408c-bf30-bb4fc8b9691f",

            "f14e07d9-5495-4da9-96be-a13f5f64abeb",

            "df3c1c84-4c7d-4e89-a734-bb4602ae83b5",

            "63edb895-280c-4b74-be15-b696cc37619b",

            "46ead4d7-7456-40e9-a8e1-a002323a1218",

            "45e9895a-971a-4bb4-a317-1b35bd13fd02",

            "6061bd38-aa8e-411c-b7ad-c24ff04e8147",

            "928dea2d-52c0-4651-8b47-10ea8fecdf44",

            "7f2f14e2-67a7-47d2-91d1-9740e5eb6026",

            "e0556ec7-8228-4fde-8e9a-1ddf4c798bd7",

            "9c59540a-f962-4486-b92f-6834b1bf114e",

            "4e793659-ac5c-424e-be57-ca2460586e9d",

            "2f7949eb-456b-42ff-b195-adb23a07fb31",

            "f944fcb2-b0f4-4f7f-b80d-d3748808ece1",

            "bd13ac9d-3ac5-4089-8256-4df9ba7efea5",

            "d8d1cbc2-572c-4b50-a2a3-24fe26429ed6",

            "ecd5e974-9218-42eb-8ce4-7c28357ed0b8",

            "53bd24d1-3ea3-4d32-9d55-5a009a71a687",

            "bfe53cd5-bbac-4500-8abd-48e202203d0b",

            "7d5a31ac-a49c-488f-af87-a8f138b755d0",

            "9525aa66-3c8c-4d4c-bec5-ea501dc8e7e0",

            "1d04e2ad-1a7f-471e-acad-3b2a000e6e8f",

            "a2fd6b96-9284-41b9-881e-d1b8ad1e3731",

            "de0818ff-ea34-4047-9a8f-fdd7d65e7a2c",

            "2645b378-c147-4b3d-b9c4-48e8f1b5955d",
            "03efecb1-ef8b-4a0e-801c-fd7660a36521",

            "a48b4923-2106-4cd6-8744-cc8ec327a7eb",

            "7790dee2-3a3f-4e1d-a54b-d94e47025d4c",

            "05e2dbb6-2aae-4cea-89eb-0e63bc3f40b2",

            "11fdf796-5ece-4a11-8666-f813e901f214",

            "ff9dbf4d-5506-4151-9f6b-78ae36601704",

            "7ac96bc5-b3ff-4c1e-9fc1-a831ae6f3498",
            "b583a8cf-d547-4854-be27-a653b74a1422",

            "474c59e4-d8b1-47a4-8f8e-015f05685608",

            "91f9679b-30c8-43ae-a583-5099cf540a1c",

            "3badd957-7f15-4a9a-aaac-3bb5de01c21a",

            "e432694f-3166-4d47-bcbc-7a7b78d8f6e6",

            "871f948d-8eac-4dd8-b657-3d121f8739bf",

            "85cb15f1-3a65-46db-b3c8-63c6ffb98f0a",

            "701a0bc2-e9e5-4ce5-b266-3fa4be51d193",

            "aa3c5081-b566-4a16-80bf-5288d4ea71fc",

            "fb7cf61a-b95b-431c-8bd7-03e661b8c359",

            "b014df9e-4f72-46e7-bff0-d978e27b800e",

            "ca9f9465-a2ce-4899-a82a-e9ff3a9623ab",

            "ec4d12af-55d8-4f25-8137-c2b494660a83",

            "c0d9696d-167d-4b7a-8724-cb5c6fefb0e2",

            "efce92fb-4509-4b54-a2ac-f1927bb66714",

            "65843b9b-fb49-4227-b36e-8838e5ded608",

            "6e3671dd-3425-4d21-9683-a180c9efe247",

            "4adccddf-dcc3-40b9-b206-63ad02078dbf",

            "39cd1f04-b4ce-4c9a-9545-2dc4f72a9869",

            "3a38947f-4601-4713-a178-0dfe44ee546c",

            "48d9dc50-9a8b-4719-8336-9431c1cac97d",

            "6b66b246-085f-4267-8c75-058b09788506",

            "f033792e-802e-46df-8433-f2d6f8a7a93a",

            "925e9dae-7b48-4e5e-af67-5993dd28cc27",

            "949c2d0d-5b20-44e8-b220-1c6b606aa518",

            "ded66dcd-5721-4df4-8afe-48b18f95469e",

            "ef2d9d89-f90e-4c99-af0c-2361d3782e33",

            "24d7077c-7853-4c50-9f3b-e64532e61bb4",

            "e0fc45c7-4d6d-473c-a563-0479fc1ed3ed",

            "3b7f5e7a-20f2-45fe-a9c6-2c54c50d46f4",

            "7d6befad-4da1-46ae-9aed-689dc652cdaa",

            "a7268714-8565-44cb-82f5-5aeae335f88d",

            "ea68a09c-fe88-44db-bc57-473c0a434b81",

            "d51a4ca9-82f5-4d50-afd3-fb46d518e0b9",

            "c0fea00c-ec77-43fd-8f3a-76e20ff2dcdd",

            "f815746f-f48e-4bbd-b75d-484d2423fda0",

            "c3057596-b31b-4c80-81b2-9734c6d9c2d7",

            "18bacc3b-a9a9-4c10-8300-56342b88d4f9",

            "9a272c9f-0e3c-43b7-bd7a-9cbf6a965212",

            "b22efa56-d255-4121-a143-2aa58ae3e7a2",

            "99cd025d-5103-4e01-b313-adb65cfd42c1",

            "f5eaa90b-3095-421a-a522-831cbe6bb8fe",

            "ac5a6c16-0410-4e0c-89d9-89e77fd9c689",

            "1fa67364-bd70-4ea9-8759-140c9b1a6d29",

            "743d1ce8-0e27-49dd-8649-705076053184",
            "1605bb93-4a0b-4022-8539-d308d6496e51",

            "7ac318a6-866c-4441-b5a3-4153809c588b",

            "0ee7cc54-83d1-4d2a-bcaa-2ad0c93c1fc4",

            "6064b3c3-618a-4e7d-8ef9-1e7cc925b9ca",

            "6978978a-e11d-4676-890f-7b2d375fa6a4",

            "5b901b09-324f-4884-b8d7-897be5b6f002",

            "9a9b1711-d3e2-49ca-9d1c-e44869a626f8",

            "a4b7e8ad-fb9f-4229-83fc-10231adc6229",

            "87f95187-5b41-4cb6-878d-1ba502a2ad93",

            "30514cca-7213-421d-8ef0-f3f9cabad517",

            "dae992da-f8b6-436f-98b0-a5a2cd31e258",

            "049b58ad-1ef8-4558-83b2-cf3cef5fd8f2",

            "741826d4-87ef-4905-9d2e-c780f838be8b",

            "47cab729-0be1-4e66-9205-5738e615fc1c",

            "f5e7a39a-78de-4569-a73b-10baf65633d9",

            "8ff3c357-5159-44b1-bb83-3b70cba28203",

            "27339394-dd53-4d8a-86a2-613f351cfaa4",

            "d7786dd6-cd34-4b1b-b0a3-03c365a69a48",

            "372a92dd-e0c8-40d8-a88e-cc9df39cce5f",

            "5b35832d-e7a4-44f1-b249-a3040d98e44c",

            "a5e2ff20-f6ee-4ea3-a2a0-d36e9994dfb3",

            "9380ff61-9f8a-4635-b242-165c361870e2",

            "d82dde48-98cb-403c-b2e3-1c7ad380b161",

            "a9f99381-68fd-465e-addc-a815be4403a4",

            "58675c97-68de-456c-bacd-534cac670c21",

            "3b76efcf-48aa-4c79-84b8-5551cffc6d05",

            "979e439f-d3c2-49dc-83f7-7d1a495f7819",

            "c97cd40e-52b6-4445-bfbf-4679df39b1ba",


            "d9bc95dc-4804-423a-8220-94e8033fe81b",

            "cdd0530e-5728-44cc-8749-e7234239e799",

            "0005a424-86b2-4c95-92b0-3cdb0d26b541",

            "94f1801a-3316-4452-bb4b-12e9a5cb11c5",

            "62615652-38a1-4c5e-acc7-f3c0ad34e36c",

            "6554f4da-e628-473b-ab84-248194f98108",

            "01a19fdc-b03b-42da-ba1d-00d272071843",

            "b07e1876-b20f-4857-b59a-8c78b527ab37",
            "7dbc6c68-f03e-43b1-bcc1-97db82bed077",

            "4075b98b-b7b4-497e-b33c-10f560c3ceab",

            "9be1525d-031e-4622-b941-011e58c774a6",

            "fd6f2d1e-c6dd-412f-9bb9-a45497b48458",

            "33490d67-233f-4f1b-ac6b-857c63889d4a",

            "446aa039-e41a-4a7c-9aa2-445a60ec6ff4",

            "cae9d77f-ffe1-455a-abfc-1c889385ca7d"

            ]
        for i in range(len(listsid)):
            url = 'https://paperless.one.th/paper_less/api/v2/mail'
            info = {"sid_code":listsid[i]}
            print(listsid[i])
            r = callAuth_post(url,info,token_header)
            print(r)

@status_methods.route("/schedule_rpa",methods=['GET'])
def schedule_rpa():
    if request.method == 'GET':
        dt_start = request.args.get('dt_start')
        dt_end  = request.args.get('dt_end')
        doc_type  = request.args.get('doc_type')
        r = schedule_check_servicedoc(dt_start,dt_end,doc_type)
        print(r)
        return "OK"

@status_methods.route("/schedule_emailcenter",methods=['GET'])
def schedule_emailcenter():
    if request.method == 'GET':
        dt_start = request.args.get('dt_start')
        dt_end  = request.args.get('dt_end')
        doc_type  = request.args.get('doc_type')
        r = schedule_check_email_center(dt_start,dt_end,doc_type)
        print(r)
        return "OK"

@status_methods.route("/schedule_bconechat",methods=['GET'])
def schedule_bconechat():
    if request.method == 'GET':
        r = get_taxid_bc_msg()
        print(r)
        return "OK"

@status_methods.route("/Version",methods=['GET','PUT'])
def get_version():
    if request.method == 'GET':
        version = null 
        try:           
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                f = open(path_global_1+"/storage/-v.txt", "r")
                version = (f.read())
            except Exception as e:
                version = null
            return version
        except Exception as e:
            return version
        version = null
    elif request.method == 'PUT':
        dataJson = request.json
        version_ = dataJson['version_']
        name_owner = dataJson['name_owner']
        keys = dataJson['keys']
        if name_owner == 'name_owner':
            if keys == "41n5FWmE07HsIidGCpQBYbVvuRZSxa3e8jXztk296KqrJTNohlPfUyDAwOLcMg":
                f = open(path_global_1+"/storage/-v.txt", "w")
                f.write(version_)
                f.close()
                return "OK"
        return "Worry"


@status_methods.route("/testfuc",methods=['GET'])
def testfuc_api_v1():
    r = select_1().select_query_templategroup_v1('dd0ae8a0-43b6-490c-b67c-b350524f79c2')
    return jsonify(r)

# service_email()
@status_methods.route("/api/v1/backupdata",methods=['POST'])
def backupdata_api_v1():
    dataJson = request.json
    if 'data' in dataJson:
        try:            
            tmpdata = dataJson['data']
            connection = engine.connect()
            for n in range(len(tmpdata)):
                tmpid_paperless = tmpdata[n]['id_paperless']
                tmpdataendcode = tmpdata[n]['data']
                sql = '''update tb_doc_detail SET data_document =:tmpdatadoc WHERE step_id = (select tb_track_paper.step_data_sid FROM tb_track_paper where tb_track_paper.hash_sid_code = :tmpid_paperless  )'''
                result_update = connection.execute(text(sql),tmpdatadoc=str(tmpdataendcode),tmpid_paperless=tmpid_paperless)
                print(tmpid_paperless)
            return jsonify({'result':'OK'})
        except Exception as e:
            print(str(e))
        finally:
            connection.close()

@status_methods.route("/T_200")
def T_200():
    return jsonify({'result':'OK'}),200

@status_methods.route("/T_404")
def T_404():
    abort(404)

@status_methods.route("/convert_JSON",methods=['POST'])
def convert_JSON_api():
    dataJson = request.json
    if 'data' in dataJson:
        tmpjson = eval(dataJson['data'])
        return jsonify(tmpjson)

@status_methods.route("/formdata",methods=['POST'])
def formdata_api():
    dataJson = request.json
    print(dataJson['url'])
    # select_result = select_1().select_step()
    # result_documentType = select_1().select_document_type_forservice_v1(None,"0107544000094","SPO")
    # result_datadoc = data_doc("")
    return jsonify(dataJson)

@status_methods.route("/api/v1/cs_onlybi",methods=['POST'])
def cs_onlybi_api_v1():
    dataJson = request.json
    if 'group_id' in dataJson:
        group_id = dataJson['group_id']
        n,req = call_service_BI(group_id,'','','','','','')
        return jsonify(n,req)
    abort(404)

@status_methods.route("/api/v1/cs_dashboard_onlybi",methods=['POST'])
def cs_dashboard_onlybi_api_v1():
    dataJson = request.json
    arr_result = []
    if 'doc_id' in dataJson:
        tmpdocid = dataJson['doc_id']
        tmpdocid = tuple(tmpdocid)
        sql = '''
            select step_data_sid AS "sid" from tb_send_detail where doc_id in :doctuple 
        '''
        with slave.connect() as connection:
            result = connection.execute(text(sql),doctuple=tmpdocid)
            connection.close()
        query_result = [dict(row) for row in result]
        for n in query_result:
            r = call_webhookService(n['sid'])
            arr_result.append(r)
            print(n['sid'])
        return jsonify(arr_result)
    if 'sid' in dataJson:
        tmpsid = dataJson['sid']        
        for n in tmpsid:
            r = call_webhookService(n)
            arr_result.append(r)
            print(n)
        # n = call_service_BI(group_id,'','','','','','')
        # return "success"
        return jsonify(arr_result)
    abort(404)

@status_methods.route("/api/v1/testWebhook",methods=['POST'])
def testWebhook_api_v1():
    dataJson = request.json
    if 'sid' in dataJson:
        tmpsid = dataJson['sid']
        n = call_serviceOTHERs(tmpsid)
    return jsonify(n)

@status_methods.route("/api/v1/testWebhook_Group",methods=['POST'])
def testWebhook_Group_api_v1():
    dataJson = request.json
    if 'group_id' in dataJson:
        tmpgroup_id = dataJson['group_id']
        n = call_webhookService_group(tmpgroup_id)
        # n = call_serviceOTHERs_Group(tmpgroup_id)
    return jsonify(n)

@status_methods.route("/webhook",methods=['POST'])
def webhook_api():
    dataJson = request.json
    print(dataJson)
    # return 0
    # dataJson = tuple(dataJson)
    # print(dataJson)
    # n = select_4().select_docid_v1(dataJson)
    # n = call_service_BI('28762c8b-1386-49d5-a891-efcb6dab610d','','','','','','')
    # n = call_webhookService('61d8b0d8-2b8a-4316-b3dc-ddbb63011a5c')
    # r = select_4().select_group_id()
    # for x in range(len(r)):
    #     tmpid = r[x]['id']
    #     print(tmpid)
    #     n = select_4().select_update_group_status_v1(tmpid)
    # r = cal_status_group_v1('96b858ac-844d-46e4-bbaf-f65972af895d')
    # n = call_serviceOTHERs('61d8b0d8-2b8a-4316-b3dc-ddbb63011a5c')    
    # r = select().select_ForWebHook("14f047d4-d1e1-4930-b8d8-d6d5912ab041")
    # cur = con.cursor()
    # cur.execute("SELECT 1;")
    # rows = cur.fetchall()  
    # db = MyDatabase()
    # cur = (db.query("SELECT 1;"))
    # db.close()  
    # con.close()
    return jsonify({'result':'OK'})
	# return render_template("index.html",template_folder='template')
# call_service_terminate_BI('a4047957-6d5a-45a2-9b98-27ea667e6503')

@status_methods.route('/api/v4/template/template_group_sum',methods=['GET'])
@token_required_v3
def template_group_sum_v4():    
    try:
        if request.method == 'GET':
            username = request.args.get('username')
            tax_id = request.args.get('tax_id')
            id_data = request.args.get('id')
            # document_type = request.args.get('document_type')
            result_group_template = select_2().select_list_template_group_sum_v5(username,tax_id,id_data)
            if result_group_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':result_group_template['messageText']} ,'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + result_group_template['messageER'],'data':None},'status_Code':200})
        else:
            return jsonify({'result':'ER','messageText': 'method incorrect','status_Code':404}),404            
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200

@status_methods.route('/api/v1/convert_base64',methods=['POST'])
def convert_base64_v1():
    if request.method == 'POST':
        if 'file' in request.files:
            image = request.files['file']  
            image_string = base64.b64encode(image.read())
            return jsonify({'result':'OK','message':'success','data':image_string})

# v4 ตัด document_type ออก
@status_methods.route('/api/v4/template/template_group',methods=['PUT','POST','GET'])
@token_required_v3
def template_group_v4():
    if request.method == 'POST':
        token_header = request.headers['Authorization']
        resCheck = (str(token_header).split(' ')[1])       
        token_required = token_required_func(resCheck)
        username = token_required['username']
        thai_email = token_required['email']
        dataJson = request.json
        '''------ INSERT ------'''
        if 'group_name' in dataJson and 'group_code' in dataJson and 'template' in dataJson and 'group_title' in dataJson and 'step_group' in dataJson and 'group_data' in dataJson and 'business_info' in dataJson and 'use_status' in dataJson and 'cover_page' in dataJson and 'group_color' in dataJson\
            and 'email_step' in dataJson and 'status_doing_auto' in dataJson:
            group_name = dataJson['group_name']
            group_code = dataJson['group_code']
            template = dataJson['template']
            group_title = dataJson['group_title']
            step_group = dataJson['step_group']
            group_data = dataJson['group_data']
            business_info = dataJson['business_info']
            use_status = dataJson['use_status']
            cover_page = dataJson['cover_page']
            group_color = dataJson['group_color']
            email_step = dataJson['email_step']
            status_doing_auto = dataJson['status_doing_auto']
            tmp_email_middle = None
            tmp_timegroup = None
            tmp_daygroup = None
            if 'email_middle' in dataJson:
                tmp_email_middle = dataJson['email_middle']
            if 'timegroup' in dataJson:
                tmp_timegroup = dataJson['timegroup']
            if 'daygroup' in dataJson:
                tmp_daygroup = dataJson['daygroup']
            insert_result = insert_2().insert_template_group_v4(group_name,group_code,template,group_title,step_group,group_data,business_info,thai_email,thai_email,use_status,cover_page,group_color,tmp_email_middle,tmp_timegroup,tmp_daygroup,email_step,status_doing_auto)
            if insert_result['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':insert_result['messageText'],'data':None},'status_Code':200}),200
        # ------ DELETE ------
        elif 'id' in dataJson and len(dataJson) == 1:
            id_data = dataJson['id']
            delete_result = update_2().delete_template_group_v3(id_data,username)
            if delete_result['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'OK','messageText':None,'messageER':{'message':'data not found','data':None},'status_Code':200}),200
        else:
            abort(404)
    elif request.method == 'PUT':
         # ------ UPDATE ------
        try:
            token_header = request.headers['Authorization']
            resCheck = (str(token_header).split(' ')[1])       
            token_required = token_required_func(resCheck)
            # print ('token_required: ',token_required)
            username = token_required['username']
            thai_email = token_required['email']
            dataJson = request.json
            if 'id' in dataJson and 'group_name' in dataJson and 'group_code' in dataJson and 'template' in dataJson and 'group_title' in dataJson and 'step_group' in dataJson and 'group_data' in dataJson and 'business_info' in dataJson and 'use_status' in dataJson and 'cover_page' in dataJson and 'group_color' in dataJson\
                and 'email_step' in dataJson and 'status_doing_auto' in dataJson:
                id_data = dataJson['id']
                group_name = dataJson['group_name']
                group_code = dataJson['group_code']
                template = dataJson['template']
                group_title = dataJson['group_title']
                step_group = dataJson['step_group']
                group_data = dataJson['group_data']
                business_info = dataJson['business_info']
                use_status = dataJson['use_status']
                cover_page = dataJson['cover_page']
                group_color = dataJson['group_color']
                email_step = dataJson['email_step']
                status_doing_auto = dataJson['status_doing_auto']
                tmp_email_middle = None
                tmp_timegroup = None
                tmp_daygroup = None
                if 'email_middle' in dataJson:
                    tmp_email_middle = dataJson['email_middle']
                if 'timegroup' in dataJson:
                    tmp_timegroup = dataJson['timegroup']
                if 'daygroup' in dataJson:
                    tmp_daygroup = dataJson['daygroup']
                update_result = update_2().update_template_group_v7(id_data,group_name,group_code,template,group_title,step_group,group_data,business_info,thai_email,use_status,cover_page,group_color,tmp_email_middle,tmp_timegroup,tmp_daygroup,email_step,status_doing_auto)
                # print(update_result)
                if update_result['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + update_result['messageText'],'data':None},'status_Code':200}),200
            #------ UPDATE USE_STATUS ------
            elif 'id' in dataJson and 'use_status' in dataJson and len(dataJson) == 2:
                id_data = dataJson['id']
                use_status = dataJson['use_status']
                use_status_result = update_2().use_status_template_group_v3(id_data,use_status,username)
                if use_status_result['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':'success','messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':'invalid id','status_Code':200}),200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'Fail','responseCode':500,'data':None,'errorMessage':str(e)})

    # ----- GET_LIST -----
    elif request.method == 'GET':
        try:
            if request.args.get('limit') != None and request.args.get('offset') != None:
                username = request.args.get('username')
                tax_id = request.args.get('tax_id')
                id_data = request.args.get('id')
                # document_type = request.args.get('document_type')
                limit = request.args.get('limit')
                offset = request.args.get('offset')
                result_group_template = select_2().select_list_template_group_v5(username,tax_id,id_data,limit,offset)
                if result_group_template['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'message':'success','data':result_group_template['messageText']} ,'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + result_group_template['messageER'],'data':None},'status_Code':200})
            else:
                return jsonify({'result':'ER','messageText': 'parameter incorrect','status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200

@status_methods.route('/api/convertbtyebase',methods=['GET'])
def convertbtyebase_v1():
    r = convert_base_bytes()
    return jsonify(r)

@status_methods.route('/api/v1/throws/document', methods=['POST'])
def document_throws_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'data' in dataJson:
            data = dataJson['data']
            for x in range(len(data)):
                sid = data[x]
                result = select_1().select_info_document_qts(sid)
            if result['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':{'data':result,'message':'success'},'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'Fail because '+ result['messageText']}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'data':None,'message': 'parameter incorrect'}}),404

@status_methods.route('/api/v2/template/template_group',methods=['PUT','POST','GET'])
@token_required_v3
def template_group_v2():
    if request.method == 'POST':
        token_header = request.headers['Authorization']
        resCheck = (str(token_header).split(' ')[1])       
        token_required = token_required_func(resCheck)
        username = token_required['username']
        thai_email = token_required['email']
        dataJson = request.json
        '''------ INSERT ------'''
        if 'group_name' in dataJson and 'group_code' in dataJson and 'template' in dataJson and 'document_type' in dataJson and 'group_title' in dataJson and 'step_group' in dataJson and 'group_data' in dataJson and 'business_info' in dataJson and 'use_status' in dataJson and 'cover_page' in dataJson and 'group_color' in dataJson:
            group_name = dataJson['group_name']
            group_code = dataJson['group_code']
            template = dataJson['template']
            document_type = dataJson['document_type']
            group_title = dataJson['group_title']
            step_group = dataJson['step_group']
            group_data = dataJson['group_data']
            business_info = dataJson['business_info']
            use_status = dataJson['use_status']
            cover_page = dataJson['cover_page']
            group_color = dataJson['group_color']
            tmp_email_middle = None
            tmp_timegroup = None
            tmp_daygroup = None
            if 'email_middle' in dataJson:
                tmp_email_middle = dataJson['email_middle']
            if 'timegroup' in dataJson:
                tmp_timegroup = dataJson['timegroup']
            if 'daygroup' in dataJson:
                tmp_daygroup = dataJson['daygroup']
            insert_result = insert_2().insert_template_group_v3(group_name,group_code,template,document_type,group_title,step_group,group_data,business_info,thai_email,thai_email,use_status,cover_page,group_color,tmp_email_middle,tmp_timegroup,tmp_daygroup)
            if insert_result['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':insert_result['messageText'],'data':None},'status_Code':200}),200
        # ------ DELETE ------
        elif 'id' in dataJson and len(dataJson) == 1:
            id_data = dataJson['id']
            delete_result = update_2().delete_template_group_v2(id_data,username)
            if delete_result['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'OK','messageText':None,'messageER':{'message':'data not found','data':None},'status_Code':200}),200
        else:
            abort(404)
    elif request.method == 'PUT':
         # ------ UPDATE ------
        try:
            token_header = request.headers['Authorization']
            resCheck = (str(token_header).split(' ')[1])       
            token_required = token_required_func(resCheck)
            # print ('token_required: ',token_required)
            username = token_required['username']
            thai_email = token_required['email']
            dataJson = request.json
            if 'id' in dataJson and 'group_name' in dataJson and 'group_code' in dataJson and 'template' in dataJson and 'document_type' in dataJson and 'group_title' in dataJson and 'step_group' in dataJson and 'group_data' in dataJson and 'business_info' in dataJson and 'use_status' in dataJson and 'cover_page' in dataJson and 'group_color' in dataJson:
                id_data = dataJson['id']
                group_name = dataJson['group_name']
                group_code = dataJson['group_code']
                template = dataJson['template']
                document_type = dataJson['document_type']
                group_title = dataJson['group_title']
                step_group = dataJson['step_group']
                group_data = dataJson['group_data']
                business_info = dataJson['business_info']
                use_status = dataJson['use_status']
                cover_page = dataJson['cover_page']
                group_color = dataJson['group_color']
                tmp_email_middle = None
                tmp_timegroup = None
                tmp_daygroup = None
                if 'email_middle' in dataJson:
                    tmp_email_middle = dataJson['email_middle']
                if 'timegroup' in dataJson:
                    tmp_timegroup = dataJson['timegroup']
                if 'daygroup' in dataJson:
                    tmp_daygroup = dataJson['daygroup']
                update_result = update_2().update_template_group_v6(id_data,group_name,group_code,template,document_type,group_title,step_group,group_data,business_info,thai_email,use_status,cover_page,group_color,tmp_email_middle,tmp_timegroup,tmp_daygroup)
                # print(update_result)
                if update_result['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + update_result['messageText'],'data':None},'status_Code':200}),200
            #------ UPDATE USE_STATUS ------
            elif 'id' in dataJson and 'use_status' in dataJson and len(dataJson) == 2:
                id_data = dataJson['id']
                use_status = dataJson['use_status']
                use_status_result = update_2().use_status_template_group_v2(id_data,use_status,username)

                if use_status_result['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':'success','messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':'invalid id','status_Code':200}),200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'Fail','responseCode':500,'data':None,'errorMessage':str(e)})

    # ----- GET_LIST -----
    elif request.method == 'GET':
        try:
            if request.args.get('limit') != None and request.args.get('offset') != None:
                username = request.args.get('username')
                tax_id = request.args.get('tax_id')
                id_data = request.args.get('id')
                document_type = request.args.get('document_type')
                limit = request.args.get('limit')
                offset = request.args.get('offset')
                result_group_template = select_2().select_list_template_group_v4(username,tax_id,id_data,document_type,limit,offset)
                if result_group_template['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'message':'success','data':result_group_template['messageText']} ,'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + result_group_template['messageER'],'data':None},'status_Code':200})
            else:
                return jsonify({'result':'ER','messageText': 'parameter incorrect','status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200

@status_methods.route('/api/v2/template/template_group_sum',methods=['GET'])
@token_required_v3
def template_group_sum_v2():    
    try:
        if request.method == 'GET':
            username = request.args.get('username')
            tax_id = request.args.get('tax_id')
            id_data = request.args.get('id')
            document_type = request.args.get('document_type')
            result_group_template = select_2().select_list_template_group_sum_v4(username,tax_id,id_data,document_type)
            if result_group_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':result_group_template['messageText']} ,'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + result_group_template['messageER'],'data':None},'status_Code':200})
        else:
            return jsonify({'result':'ER','messageText': 'method incorrect','status_Code':200}),200            
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200

@status_methods.route('/api/v2/template/template_group/search',methods=['GET'])
@token_required_v3
def template_group_search_v2():
    if request.method == 'GET':
        try:
            if request.args.get('limit') != None and request.args.get('offset') != None and request.args.get('keyword') != None:
                username = request.args.get('username')
                tax_id = request.args.get('tax_id')
                document_type = request.args.get('document_type')
                limit = request.args.get('limit')
                offset = request.args.get('offset')
                keyword = request.args.get('keyword')
                result_group_template = select_2().select_list_template_group_search_v4(username,tax_id,document_type,limit,offset,keyword)
                if result_group_template['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'message':'success','data':result_group_template['messageText']} ,'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + result_group_template['messageER'],'data':None},'status_Code':200})
            else:
                return jsonify({'result':'ER','messageText': 'parameter incorrect','status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200

@status_methods.route('/api/v2/template/template_group/search_sum',methods=['GET'])
@token_required_v3
def template_group_search_sum_v2():
    if request.method == 'GET':
        try:
            if request.args.get('keyword') != None:
                username = request.args.get('username')
                tax_id = request.args.get('tax_id')
                document_type = request.args.get('document_type')
                keyword = request.args.get('keyword')
                result_group_template = select_2().select_list_template_group_search_sum_v4(username,tax_id,document_type,keyword)
                if result_group_template['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'message':'success','data':result_group_template['messageText']} ,'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + result_group_template['messageER'],'data':None},'status_Code':200})
            else:
                return jsonify({'result':'ER','messageText': 'parameter incorrect','status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200
    else:
        return jsonify({'result':'ER','messageText': 'method incorrect','status_Code':200}),200

@status_methods.route('/api/v1/testsql', methods=['POST'])
def testsql():
    email_thai = 'suwanan.ch@thai.com'
    time = '2020-05-14 15:42:25'
    # result = update_3().update_process_onprocess_status_v1('64854345-22fd-4bb6-b44a-1cea8ee5bbfc','','','','','')
    return {'OK':'OK','result':result}

@status_methods.route('/api/v1/throws/document', methods=['POST'])
def document_throws():
    if request.method == 'POST':
        dataJson = request.json
        if 'sid' in dataJson :
            sid = dataJson['sid']
            result = select_1().select_info_document(sid)
            if result['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':{'data':result,'message':'success'},'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'Fail because '+ result['messageText']}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'data':None,'message': 'parameter incorrect'}}),404

@status_methods.route('/api/v1/activity/search',methods=['GET'])
def select_activity_search():
    if request.method == 'GET':
        if request.args.get('email_user') != None and request.args.get('offset') != None and request.args.get('limit') != None and request.args.get('keyword') != None:
            if request.args.get('email_user') != "" and request.args.get('offset') != "" and request.args.get('limit') != "":
                email_user = request.args.get('email_user')
                offsets = request.args.get('offset')
                limits = request.args.get('limit')
                keyword = request.args.get('keyword')
                result_log = select_1().select_activity_search(email_user,offsets,limits,keyword)
                if result_log['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter value null'}),404
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'method incorrect'}),404

@status_methods.route('/api/v1/activity/search_count',methods=['GET'])
def select_activity_search_count():
    if request.method == 'GET':
        if request.args.get('email_user') != None:
            email_user = request.args.get('email_user')
            keyword = request.args.get('keyword')
            result_log = select_1().select_activity_search_count(email_user,keyword)
            if result_log['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter email null'}),404
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'method incorrect'}),404

@status_methods.route('/api/v1/tash',methods=['POST'])
@token_required_v3
def tash():
    if request.method == 'POST':
        dataJson = request.json
        if 'email' in dataJson and 'sid' in dataJson:
            email = dataJson['email']
            sid = dataJson['sid']
            result_update = update_1().update_tash(email,sid)
            return jsonify({'result':'OK','messageText':'success','status_Code':200,'messageER':None}),200
        # else:
        #     return jsonify({'result':'OK','messageText':'','status_Code':200,'messageER':None}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

            # if result_log['result'] == 'OK':
            #     return jsonify({'result':'OK','messageText':'success','status_Code':200,'messageER':None}),200
            # else:
            #     return jsonify({'result':'OK','messageText':'error','status_Code':200,'messageER':result_log['messageER']}),200

# def thread_callback():
#     print(time.time())
#     print("Hello inside Thread")

# def thread_callback_1():
#     print(time.time())
#     print("Hello inside Thread")

# thr = threading.Thread(target=thread_callback)
# thr_1 = threading.Thread(target=thread_callback_1)
# thr.start()
# thr_1.start()
# r = fine_name_surename('jirayu.ko@one.th')
# print(r)
# r = select_3().select_BizProfile_for_onebox('0105548134654')
# print(r)
# print(select_3().select_profileGetstatus_v1('jirayuknot55@gmail.com'))
@status_methods.route('/api/v1/pdf_step', methods=['PUT'])
@token_required_v3
def pdf_step_api_v1():
    if request.method == 'PUT':
        try:
            if 'Authorization' not in request.headers:
                abort(401)
            token_header = request.headers['Authorization']
            token_oneid = (str(token_header).split(' ')[1])
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'string_sign' in dataJson and 'step_data_sid' in dataJson and 'sign_email' in dataJson and 'activity_code' in dataJson and 'activity_status' in dataJson and 'step_num' in dataJson and 'signlat' in dataJson and 'signlong' in dataJson and 'sign_id' in dataJson:
            arr_result = []
            sidCode = dataJson['step_data_sid']
            tmp_string_sign = dataJson['string_sign']
            tmpsign_email = dataJson['sign_email']
            tmpactivity_code = dataJson['activity_code']
            tmpactivity_status = dataJson['activity_status']
            tmpstep_num = dataJson['step_num']
            tmpsignlat = dataJson['signlat']
            tmpsignlong = dataJson['signlong']
            tmpsign_id = dataJson['sign_id']
            # thr_updatepdf = threading.Thread(target=update_4().update_step_new_v1,args=[sidCode, tmp_string_sign])
            # thr_updatestep = threading.Thread(target=update_4().update_pdf_new_v1,args=[sidCode,tmpsign_email,tmpactivity_code,tmpactivity_status,tmpstep_num,tmpsignlat,tmpsignlong,tmpsign_id])
            # thr_updatepdf.start()
            # thr_updatestep.start()
            query_detail_document = select().select_data_for_chat_v1(sidCode)
            if query_detail_document['result'] == 'OK':
                tmp_data_detail = query_detail_document['messageText']
                tmp_document_id = tmp_data_detail['document_id']
                tmp_sender_name = tmp_data_detail['sender_name']
                tmp_email_sender = tmp_data_detail['sender_email']
                tmp_body_text = tmp_data_detail['body_text']
                tmpfid = tmp_data_detail['fid']
            # strname_surname = fine_name_surename(dataJson['sign_email'])
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            sidcodehash = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
            # tmpcheck_update =  executor.submit(update_4().update_step_new_v1,sidCode,tmpsign_email,tmpactivity_code,tmpactivity_status,tmpstep_num,tmpsignlat,tmpsignlong,tmpsign_id,tmp_string_sign)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # tmpres_updatepdf =  executor.submit(update_4().update_pdf_new_v1,sidCode,tmp_string_sign)
                tmpcheck_update =  executor.submit(update_4().update_step_new_v1,sidCode,tmpsign_email,tmpactivity_code,tmpactivity_status,tmpstep_num,tmpsignlat,tmpsignlong,tmpsign_id,tmp_string_sign)
                check_update = tmpcheck_update.result()
                # res_updatepdf = tmpres_updatepdf.result()                
                url = url_ip_eform + '/api/v1/send_chat_ppl?paperless_id=' +sidcodehash
                tmp_calleformstatus = executor.submit(callGET_v2 ,url  ,token_header)

            # if res_updatepdf['result'] == 'OK':
            #     arr_result.append({'message_step':'update pdf success'})
            # else:
            #     arr_result.append({'message_step':'update pdf fail'})
            
            # if check_update['result'] == 'OK':
            #     arr_result.append({'message_pdf':check_update['messageText']})
            # else:
            #     arr_result.append({'message_pdf':check_update['messageText']})
            return jsonify({'result':'OK','messageText':'update step pdf success','status_Code':200}),200
        else:
            abort(404)

@status_methods.route('/', methods=['GET'])
def main_website():
    return 'paperless document (v1) Internet Thailand Public Company Limited.'

@status_methods.route('/upload', methods=['GET', 'POST'])
def api_main():
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
        dataForm = request.form
        dataFile = request.files
        if 'file' in dataFile:
            if 'template' in dataForm and 'step' in dataForm and 'step_data' in dataForm and len(dataForm) == 3:
                try:
                    eval(dataForm['step_data'])
                except Exception as ex:
                    return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_data ให้เป็น Json ได้','status_Code':200}),200
                res_convert = convert().api_convert(dataFile)
                if res_convert['result'] == 'OK':
                    sha512encode = hashlib.sha512(str(res_convert['messageText']['file']).encode('utf-8')).hexdigest()
                    res_insert_pdf = insert().insert_paper_pdf(str(res_convert['messageText']['file']),sha512encode)
                    if res_insert_pdf['result'] == 'OK':
                        res_track = insert().insert_paper_tracking(res_convert['messageText']['id'],res_insert_pdf['messageText'],dataForm['template'],dataForm['step'])
                        if res_track['result'] == 'OK':
                            ts = int(time.time())
                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                            insert().insert_paper_datastep(res_track['step_data_sid'],dataForm['step_data'],st)
                            return jsonify({'result':'OK','messageText':'Success!','tracking_code':res_track['messageText'],'step_data_sid':res_track['step_data_sid'],'convert_id':res_track['convert_id'],'file_id':res_insert_pdf['messageText'],'file_name':res_convert['messageText']['filename'],'status_Code':200}),200
                        else:
                            return jsonify({'result':'ER','messageText':res_track['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':res_insert_pdf['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':res_convert['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
        else:
            return jsonify({'result':'ER','messageText':'Not Found Fail!','status_Code':404}),404
    elif request.method == 'GET':
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

@status_methods.route('/upload/v2', methods=['GET', 'POST'])
def upload_apiv2():
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
        datajson = request.json
        if 'template' in datajson and 'step' in datajson and 'step_data' in datajson and 'name_file' in datajson and 'convert_id' in datajson and 'file_string' in datajson and len(datajson) == 6:
            try:
                eval(datajson['step_data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_data ให้เป็น Json ได้','status_Code':400}),400
            sha512encode = hashlib.sha512(str(datajson['file_string']).encode('utf-8')).hexdigest()
            res_insert_pdf = insert().insert_paper_pdf(str(datajson['file_string']),sha512encode)
            if res_insert_pdf['result'] == 'OK':
                res_track = insert().insert_paper_tracking(datajson['convert_id'],res_insert_pdf['messageText'],datajson['template'],datajson['step'])
                if res_track['result'] == 'OK':
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                    insert().insert_paper_datastep(res_track['step_data_sid'],datajson['step_data'],st)
                    return jsonify({'result':'OK','messageText':'Success!','tracking_code':res_track['messageText'],'step_data_sid':res_track['step_data_sid'],'convert_id':res_track['convert_id'],'file_id':res_insert_pdf['messageText'],'file_name':datajson['name_file'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':res_track['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_pdf['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

@status_methods.route('/upload/v2_1', methods=['GET', 'POST'])
@token_required
def upload_apiv2_1():
    if request.method == 'POST':
        datajson = request.json
        if 'template' in datajson and 'step' in datajson and 'step_data' in datajson and 'name_file' in datajson and 'convert_id' in datajson and 'file_string' in datajson and 'step_data_Upload' in datajson and 'biz_detail' in datajson and 'qrCode_position' in datajson and len(datajson) == 9:
            try:
                eval(datajson['step_data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_data ให้เป็น Json ได้','status_Code':400}),400

            sha512encode = hashlib.sha512(str(datajson['file_string']).encode('utf-8')).hexdigest()
            tmp_filestringbase64 = str(datajson['file_string'])
            
            res_insert_pdf = insert().insert_paper_pdf(str(datajson['file_string']),sha512encode)
            if res_insert_pdf['result'] == 'OK':
                res_track = insert().insert_paper_tracking(datajson['convert_id'],res_insert_pdf['messageText'],datajson['template'],datajson['step'])
                if res_track['result'] == 'OK':
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                    if  datajson['biz_detail'] != None:
                        if 'id_card_num' in datajson['biz_detail']:
                            tmptax_id = datajson['biz_detail']['id_card_num']
                            executor.submit(cal_taxId_v1,tmptax_id)
                    result_insert = insert().insert_paper_datastepv2_1(res_track['step_data_sid'],datajson['step_data'],st,datajson['step_data_Upload'],datajson['step'],datajson['biz_detail'],datajson['qrCode_position'])
                    if result_insert['result'] == 'OK':
                        convert_pdf_image_v1(res_track['step_data_sid'],tmp_filestringbase64)                        
                        info = {
                            "input_file": str(datajson['file_string'])
                        }
                        # manageai_document_tesseract_v1(res_track['step_data_sid'],info)
                        # tmp_callocr = executor.submit(manageai_document_tesseract_v1,res_track['step_data_sid']  ,info)
                        return jsonify({'result':'OK','messageText':'Success!','tracking_code':res_track['messageText'],'step_data_sid':res_track['step_data_sid'],'convert_id':res_track['convert_id'],'file_id':res_insert_pdf['messageText'],'file_name':datajson['name_file'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':res_track['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_pdf['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

@status_methods.route('/upload/v2_2', methods=['GET', 'POST'])
@token_required
def upload_apiv2_2():
    if request.method == 'POST':
        datajson = request.json
        if 'template' in datajson and 'step' in datajson and 'step_data' in datajson and 'name_file' in datajson and 'convert_id' in datajson and 'file_string' in datajson and 'step_data_Upload' in datajson and 'biz_detail' in datajson and 'qrCode_position' in datajson and len(datajson) == 9:
            try:
                eval(datajson['step_data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_data ให้เป็น Json ได้','status_Code':400}),400
            sha512encode = hashlib.sha512(str(datajson['file_string']).encode('utf-8')).hexdigest()
            res_insert_pdf = insert().insert_paper_pdf(str(datajson['file_string']),sha512encode)
            if res_insert_pdf['result'] == 'OK':
                res_track = insert().insert_paper_tracking(datajson['convert_id'],res_insert_pdf['messageText'],datajson['template'],datajson['step'])
                if res_track['result'] == 'OK':
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                    result_insert = insert().insert_paper_datastepv2_1(res_track['step_data_sid'],datajson['step_data'],st,datajson['step_data_Upload'],datajson['step'],datajson['biz_detail'],datajson['qrCode_position'])
                    if result_insert['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':'Success!','tracking_code':res_track['messageText'],'step_data_sid':res_track['step_data_sid'],'convert_id':res_track['convert_id'],'file_id':res_insert_pdf['messageText'],'file_name':datajson['name_file'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':res_track['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_pdf['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

@status_methods.route('/api/v3/upload_ppl', methods=['GET', 'POST'])
@token_required_v3
def upload_apiv3():
    if request.method == 'POST':
        datajson = request.json
        list_status_api = []
        if 'template' in datajson and 'step' in datajson and 'step_data' in datajson and 'name_file' in datajson and 'convert_id' in datajson and 'file_string' in datajson and 'step_data_Upload' in datajson and 'biz_detail' in datajson and 'qrCode_position' in datajson and 'document_type' in datajson \
        and 'type_file' in datajson and 'document_json' in datajson and 'urgent_type' in datajson and 'digit_sign' in datajson and 'attempted_name' in datajson and 'sign_page_options' in datajson and 'options_page' in datajson \
        and 'send_user' in datajson and 'status' in datajson and 'sender_name' in datajson and 'sender_email' in datajson \
        and 'sender_position' in datajson and 'step_code' in datajson and 'sender_webhook' in datajson and 'email_center' in datajson and 'time_expire' in datajson and 'importance' in datajson \
        and 'last_digitsign' in datajson and len(datajson) == 28:
            eform_id = None
            size = convert_base64Tosize(datajson['file_string'])            
            if 'id_card_num' in datajson['biz_detail']:
                tmptax_id = datajson['biz_detail']['id_card_num']
                executor.submit(cal_taxId_v1,tmptax_id)
            result_upload = insert_1().insert_upload_ppl(datajson['template'],datajson['step'],datajson['step_data'],datajson['name_file'],datajson['convert_id'],datajson['file_string'],datajson['step_data_Upload'],datajson['biz_detail'],datajson['qrCode_position'],datajson['document_type'],datajson['type_file'],datajson['document_json'],\
            datajson['urgent_type'],datajson['digit_sign'],datajson['attempted_name'],datajson['sign_page_options'],datajson['options_page'],\
            datajson['send_user'],datajson['status'],datajson['sender_name'],datajson['sender_email'],datajson['sender_position'],datajson['step_code'],datajson['sender_webhook'],datajson['email_center']\
            ,datajson['time_expire'],datajson['importance'],eform_id,datajson['last_digitsign'])
            if result_upload['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_upload['messageText'],'status_Code':200}),200
            else :
                return jsonify({'result':'ER','messageText':result_upload['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

# recheck = cal_taxId_v1('5513213355654')
# print(recheck)
@status_methods.route('/api/v4/upload_ppl', methods=['GET', 'POST'])
@token_required_v3
def upload_apiv4():
    if request.method == 'POST':
        datajson = request.json
        list_status_api = []
        # print('len',len(datajson))
        if 'template' in datajson and 'step' in datajson and 'step_data' in datajson and 'name_file' in datajson and 'convert_id' in datajson and 'file_string' in datajson and 'step_data_Upload' in datajson and 'biz_detail' in datajson and 'qrCode_position' in datajson and 'document_type' in datajson \
        and 'type_file' in datajson and 'document_json' in datajson and 'urgent_type' in datajson and 'digit_sign' in datajson and 'attempted_name' in datajson and 'sign_page_options' in datajson and 'options_page' in datajson \
        and 'send_user' in datajson and 'status' in datajson and 'sender_name' in datajson and 'sender_email' in datajson \
        and 'sender_position' in datajson and 'step_code' in datajson and 'sender_webhook' in datajson and 'email_center' in datajson and 'time_expire' in datajson and 'importance' in datajson \
        and 'last_digitsign' in datajson and 'status_ref' in datajson and 'list_ref' in datajson:
            rGetMaxpage = get_maxpages_pdf(datajson['file_string'])    
            if rGetMaxpage[0] == 200:
                maxPages = rGetMaxpage[1]
                message = rGetMaxpage[2]
            tmpsender_name_eng = None
            if 'sender_name_eng' in datajson:
                tmpsender_name_eng = datajson['sender_name_eng']
            eform_id = None  
            tmptax_id = None    
            tmpnamesender = datajson['sender_name']
            if tmpsender_name_eng != None:
                tmpnamesender = '{"th":"'+str(datajson['sender_name'])+'","eng":"'+str(tmpsender_name_eng)+'"}'    
            if datajson['biz_detail'] != None:  
                if 'id_card_num' in datajson['biz_detail']:
                    tmptax_id = datajson['biz_detail']['id_card_num']
            recheck = cal_Check_tax_id(tmptax_id)
            if recheck == True:
                result_upload = insert_1().insert_upload_ppl_v2(datajson['template'],datajson['step'],datajson['step_data'],datajson['name_file'],datajson['convert_id'],datajson['file_string'],datajson['step_data_Upload'],datajson['biz_detail'],datajson['qrCode_position'],datajson['document_type'],datajson['type_file'],datajson['document_json'],\
                datajson['urgent_type'],datajson['digit_sign'],datajson['attempted_name'],datajson['sign_page_options'],datajson['options_page'],\
                datajson['send_user'],datajson['status'],tmpnamesender,datajson['sender_email'],datajson['sender_position'],datajson['step_code'],datajson['sender_webhook'],datajson['email_center']\
                ,datajson['time_expire'],datajson['importance'],eform_id,datajson['last_digitsign'],datajson['status_ref'],datajson['list_ref'],tmptax_id,messagePages=message)
                if result_upload['result'] == 'OK':
                    if datajson['biz_detail'] != None:  
                        if 'id_card_num' in datajson['biz_detail']:
                            tmptax_id = datajson['biz_detail']['id_card_num']
                            executor.submit(cal_taxId_v1,tmptax_id)
                    if 'step_data_sid' in result_upload['messageText'][0]:
                        executor.submit(call_webhookService,result_upload['messageText'][0]['step_data_sid'])
                    return jsonify({'result':'OK','messageText':result_upload['messageText'],'status_Code':200}),200
                else :
                    return jsonify({'result':'ER','messageText':result_upload['messageText'],'status_Code':200}),200
            else:
                    return jsonify({'result':'ER','messageText':'Transaction Full','status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

@status_methods.route('/api/v1/get_list_send_detail', methods=['GET'])
def get_list_send_detail():
    if request.method == 'GET':
        try:
            doc_type = request.args.get('doc_type')
            if doc_type == None :
                abort(404)
            result_select = select_2().select_list_ref_v2(doc_type)
            if result_select['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':result_select['messageER'],'status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/v2/get_list_send_detail', methods=['GET'])
def get_list_send_detail_v2():
    if request.method == 'GET':
        try:
            doc_type = request.args.get('doc_type')
            email = request.args.get('email')
            if doc_type == None :
                abort(404)
            result_select = select_2().select_list_ref_v2(doc_type,email)
            if result_select['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':result_select['messageER'],'status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/v1/testjuu', methods=['GET', 'POST'])
def testv1():
    r = createfile_pdfsign_v1('pdfstring','pdfhash')
    return jsonify(r)

@status_methods.route('/upload/v201', methods=['GET', 'POST'])
def upload_apiv201():
    if request.method == 'POST':
        datajson = request.json
        if 'template' in datajson and 'step' in datajson and 'step_data' in datajson and 'name_file' in datajson and 'convert_id' in datajson and 'file_string' in datajson and len(datajson) == 6:
            try:
                eval(datajson['step_data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_data ให้เป็น Json ได้','status_Code':400}),400
            sha512encode = hashlib.sha512(str(datajson['file_string']).encode('utf-8')).hexdigest()
            res_insert_pdf = insert().insert_paper_pdf(str(datajson['file_string']),sha512encode)
            if res_insert_pdf['result'] == 'OK':
                res_track = insert().insert_paper_tracking(datajson['convert_id'],res_insert_pdf['messageText'],datajson['template'],datajson['step'])
                if res_track['result'] == 'OK':
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                    insert().insert_paper_datastep(res_track['step_data_sid'],datajson['step_data'],st)
                    return jsonify({'result':'OK','messageText':'Success!','tracking_code':res_track['messageText'],'step_data_sid':res_track['step_data_sid'],'convert_id':res_track['convert_id'],'file_id':res_insert_pdf['messageText'],'file_name':datajson['name_file'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':res_track['messageText'],'status_Code':400}),400
            else:
                return jsonify({'result':'ER','messageText':res_insert_pdf['messageText'],'status_Code':400}),400
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

@status_methods.route('/api/upload', methods=['GET', 'POST'])
def upload_apinew():
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
        datajson = request.json
        if 'template' in datajson and 'step' in datajson and 'step_data' in datajson and 'name_file' in datajson and 'convert_id' in datajson and 'file_string' in datajson and len(datajson) == 6:
            try:
                eval(datajson['step_data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_data ให้เป็น Json ได้','status_Code':400}),400
            sha512encode = hashlib.sha512(str(datajson['file_string']).encode('utf-8')).hexdigest()
            res_insert_pdf = insert().insert_paper_pdf(str(datajson['file_string']),sha512encode)
            if res_insert_pdf['result'] == 'OK':
                res_track = insert().insert_paper_tracking(datajson['convert_id'],res_insert_pdf['messageText'],datajson['template'],datajson['step'])
                if res_track['result'] == 'OK':
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                    insert().insert_paper_datastep(res_track['step_data_sid'],datajson['step_data'],st)
                    return jsonify({'result':'OK','messageText':'Success!','tracking_code':res_track['messageText'],'step_data_sid':res_track['step_data_sid'],'convert_id':res_track['convert_id'],'file_id':res_insert_pdf['messageText'],'file_name':datajson['name_file'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':res_track['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_pdf['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

@status_methods.route('/api/test', methods=['POST'])
@token_required
def testapi():
    return 'o'

@status_methods.route('/api/onechain', methods=['GET', 'POST'])
@token_required
def insert_onechain():
    if request.method == 'POST':
        dataJson = request.json
        if 'sid' in dataJson and 'file_id' in dataJson and 'transactionId' in dataJson and 'timestamp' in dataJson and 'metadate' in dataJson and 'account' in dataJson and len(dataJson) == 6:
            try:
                eval(dataJson['metadate'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล metadate ให้เป็น Json ได้'}),200
            try:
                eval(dataJson['account'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล account ให้เป็น Json ได้'}), 200
            result = insert().insert_transactionChain(dataJson['sid'],dataJson['file_id'],dataJson['transactionId'],dataJson['timestamp'],dataJson['metadate'],dataJson['account'])
            if result['result'] =='OK':
                return jsonify(result),200
            else:
                return jsonify(result),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/step', methods=['PUT','GET'])
def update_step():
    if request.method == 'PUT':
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
        if 'step_data_sid' in dataJson and 'sign_email' in dataJson and 'activity_code' in dataJson and 'activity_status' in dataJson and 'step_num' in dataJson and 'signlat' in dataJson and 'signlong' in dataJson and len(dataJson) == 7:

            check_update = update().update_step(dataJson['step_data_sid'],dataJson['sign_email'],dataJson['activity_code'],dataJson['activity_status'],dataJson['step_num'],dataJson['signlat'],dataJson['signlong'])
            if check_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Update OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':check_update['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
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
        if request.args.get('sid') != None:
            select_get_datastep = select().select_get_stepdata(request.args.get('sid'))
            if select_get_datastep['result'] == 'OK':
                return jsonify(select_get_datastep),200
            else:
                return jsonify({'result':'ER','messageText':select_get_datastep['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/inet_track', methods=['POST'])
def get_step():
    if request.method == 'POST':
        dataJson = request.json
        if 'tracking_Code' in dataJson:
            return select().select_track(dataJson['tracking_Code'])


# r = select().select_BizProfile('0107544000094')
# print(r)
# resultchecktemplate = select_1().select_check_template_stepforgroup_v1(['0c2eddc7-c57d-4b6a-aca6-115dbc466822'])
# print(resultchecktemplate)
# r= select().select_token_required_v1('eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImVkYzZmODliMGU2Njk1MTA2MDYwYTY3NjA3YTE0ZGZjYjMyMDkxNDBlZDY2ZmIzYTRiN2Q2NzFiNTU5OTg5NjNjMDA1YTcyY2MyMmNmYjIwIn0.eyJhdWQiOiIxMzYiLCJqdGkiOiJlZGM2Zjg5YjBlNjY5NTEwNjA2MGE2NzYwN2ExNGRmY2IzMjA5MTQwZWQ2NmZiM2E0YjdkNjcxYjU1OTk4OTYzYzAwNWE3MmNjMjJjZmIyMCIsImlhdCI6MTYwMTk2MjE5OSwibmJmIjoxNjAxOTYyMTk5LCJleHAiOjE2MDIwNDg1OTksInN1YiI6Ijc4NjUzOTAxMjYwOCIsInNjb3BlcyI6WyJwaWMiXX0.AWHHKRqefEaSOuhBQ7D5gcFTpUfoPZuXItto8gi0Sl1uvdJH-IBrbBlLc9buxXR67mCVYnUIEMv5ob5rFpaGwiED21JcFCqitUz4lLlwa_2szKpRlH0xVTN0tMTe3ROZLVrGsdH2v_VhziBpTxwXkQlTqNz9D8DZVirEt0dqL-G5FohT0K1zhYw4mD33jgYSQ4IOKR_1BUwCYp6iQe46g-E8VTPRvb9JrZipHFqV_bD4avGebAuVGX8HOliebAGql3rNKIuA9ey5rn3a3ItrZhPV7jizuntbBsM-OcwXQdMfkVoQuUpzSAy2oUJOSptEnwsoTRJUOyFjKGw5ThLaO57UiMT9JEFOZvYNTVfFXncDx36hgfusZa415bfFJ6XQXp79OEgsGBb2H5qsiEZIMSPc7tcdl1iLdoSFV_rTyp9MgWYKxU7v322znX2jdRf3aZBYnEdrUEtySxhswHlbf4FbLdmk1WW9Y7sZALNFyPRIbqoP8XGxUmBbwyE98O8kOqj8DheAZP1JqR7xY30dA-zx6OBivliaR5mVONziHuHtsfVOXztgeAJ0JfBoRM32wcR0xl94F9x5lIpyHHJnKAI78mjLT_jk9_bAK8eMYRDZRnHVAt7o6xO5slSHuM_p_KRHR276AgaI3pduDLwIdRmOF_GjvCkDfZWLz9ZMaHM')


@status_methods.route('/api/v2/tracking_paperless', methods=['POST'])
def tracking_paperless_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'tracking_Code' in dataJson:
            return select().select_track_v2(dataJson['tracking_Code'])

@status_methods.route('/api/template', methods=['POST','PUT','GET'])
def template():
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
        if 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Name' in dataJson and len(dataJson) == 6:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            res_insert_template = insert().insert_paper_template(dataJson['step_Code'],dataJson['step_Data'],dataJson['step_Max'],dataJson['username'],dataJson['email'],st,dataJson['step_Name'])
            if res_insert_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Insert OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_template['messageText'],'status_Code':200}),200
        elif 'username' in dataJson and 'template_code' in dataJson and len(dataJson) == 2:
            res_delete = delete().delete_template(dataJson['username'],dataJson['template_code'])
            if res_delete['result'] == 'OK':
                return jsonify(res_delete),200
            else:
                return jsonify({'result':'ER','messageText':res_delete['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
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
        if 'step_Name' in dataJson and 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and len(dataJson) == 6:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            res_step_update = update().update_step_table(
                dataJson['step_Code'], dataJson['step_Data'], dataJson['step_Max'], dataJson['username'], dataJson['email'], dataJson['step_Name'])
            if res_step_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Update OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Can,t to Update!','status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
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
        if (request.args.get('username')) != None and (request.args.get('template')) == None:
            select_get = select().select_get_template(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('template')) != None and not (request.args.get('string')):
            select_get = select().select_get_templateandusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('string')) != None and (request.args.get('username')) != None and (request.args.get('template')) != None:
            '''get template string'''
            if str(request.args.get('string')).replace(' ','') == 'true':
                pass
            else:
                return jsonify({'result':'ER','messageText':'string to bool (true or false)','status_Code':200}),200
            if str(request.args.get('string')).replace(' ','') == 'true':
                select_get = select().select_get_string_templateAndusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
            else:
                select_get = select().select_get_templateandusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/recipient_chat', methods=['GET'])
@token_required
def recipient_chat_api():
    if request.args.get('email') != None and request.args.get('string') != None:
        res_select = select().select_recep_chat(str(request.args.get('email')).replace(' ',''),str(request.args.get('string')).replace(' ',''))
        if res_select['result'] == 'OK':
            return jsonify(res_select),200
        else:
            return jsonify({'result':'ER','messageText':res_select['messageText']}),200

@status_methods.route('/api/recipient_chat_v2', methods=['GET'])
@token_required
def recipient_chat_api_v2():
    if request.args.get('email') != None and request.args.get('string') != None:
        result_tmpsidcode = select().select_hash_tosid(request.args.get('string'))
        if result_tmpsidcode['result'] == 'OK':
            tmpdata = result_tmpsidcode['message']
            res_select_recipient_sid = select().select_recipient_chat_v3_one(str(request.args.get('email')).replace(' ','').lower(),tmpdata)
            if res_select_recipient_sid['result'] == 'OK':
                return jsonify(res_select_recipient_sid),200
            else:
                return jsonify({'result':'ER','messageText':res_select_recipient_sid['messageText'],'messageER':res_select_recipient_sid['messageER'],'status_Code':200}),200

@status_methods.route('/api/v3/recipient_chat', methods=['GET'])
@token_required_v3
def recipient_chat_api_v3():
    if request.args.get('email') != None and request.args.get('string') != None:
        result_tmpsidcode = select().select_hash_tosid(request.args.get('string'))
        if result_tmpsidcode['result'] == 'OK':
            tmpdata = result_tmpsidcode['message']
            res_select_recipient_sid = select().select_recipient_chat_v3_one(str(request.args.get('email')).replace(' ','').lower(),tmpdata)
            if res_select_recipient_sid['result'] == 'OK':
                return jsonify(res_select_recipient_sid),200
            else:
                return jsonify({'result':'ER','messageText':res_select_recipient_sid['messageText'],'messageER':res_select_recipient_sid['messageER'],'status_Code':200}),200
        # res_select = select().select_recep_chat_v3(str(request.args.get('email')).replace(' ',''),str(request.args.get('string')).replace(' ',''))
        # if res_select['result'] == 'OK':
        #     return jsonify(res_select),200
        # else:
        #     return jsonify({'result':'ER','messageText':res_select['messageText']}),200

@status_methods.route('/api/v1/generate_key',methods=['GET'])
def generate_key_api_v1():
    count_key = (request.args.get('num'))
    if count_key == None:
        return jsonify({'result':'ER','message':[]})
    else:
        try:
            count_key = int(count_key)
        except Exception as e:
            return jsonify({'result':'ER','message':[]})
        if type(count_key) is int:
            arr_key = []
            for u in range(count_key):
                key_ = str(uuid.uuid4())
                arr_key.append(key_)
            return jsonify({'result':'OK','message':arr_key})
        else:
            return jsonify({'result':'ER','message':[]})

@status_methods.route('/api/recipient_publicsign/v1/<string:emailuser>/<string:fid>', methods=['GET'])
# @token_required
def recipient_publicsign_v1(emailuser,fid):
    result_Select = select().select_recep_publicsign(str(emailuser).replace(' ',''),str(fid).replace(' ',''))
    if result_Select['result'] == 'OK':
        return jsonify(result_Select),200
    else:
        return jsonify({'result':'ER','messageText':result_Select['messageText'],'status_Code':200}),200

@status_methods.route('/api/sender', methods=['POST','PUT','GET'])
@token_required
def sender_api():
    if request.method == 'POST':
        dataJson = request.json
        if 'send_user' in dataJson and 'status' in dataJson and 'sender_name' in dataJson and 'sender_email' in dataJson and 'sender_position' in dataJson and 'file_id' in dataJson and 'file_name' in dataJson and 'tracking_id' in dataJson and 'step_data_sid' in dataJson and 'step_code' in dataJson and 'doc_id' in dataJson and len(dataJson) == 11:
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            sha512encode = hashlib.sha512(str(dataJson['step_data_sid']).encode('utf-8')).hexdigest()
            url_sendtochat = login_Page + sha512encode
            res_insert_sender = insert().insert_paper_sender(dataJson['send_user'],st,dataJson['status'],dataJson['sender_name'],dataJson['sender_email'],dataJson['sender_position'],dataJson['file_id'],dataJson['file_name'],dataJson['tracking_id'],dataJson['step_data_sid'],dataJson['step_code'],dataJson['doc_id'])
            if res_insert_sender['result'] == 'OK':
                res = {'result':'OK','messageText':{'messageText':res_insert_sender['messageText'],'url_Chat':url_sendtochat},'status_Code':200}
                return jsonify(res),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_sender['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('senderuser')) != None:
            select_getsender = select().select_get_sender(str(request.args.get('senderuser')).replace(' ',''))
            if select_getsender['result'] == 'OK':
                return jsonify(select_getsender),200
            else:
                return jsonify({'result':'ER','messageText':select_getsender['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'sid' in dataJson and 'status' in dataJson and len(dataJson) == 2:
            res_update_send_detail = update().update_send_detail(dataJson['sid'], dataJson['status'])
            if res_update_send_detail['result'] == 'OK':
                return jsonify({'result': 'OK', 'messageText': res_update_send_detail['messageText'], 'status_Code': 200}), 200
            else:
                return jsonify({'result': 'ER', 'messageText': res_update_send_detail['messageText'], 'status_Code': 200}), 200
    else:
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

@status_methods.route('/api/sender/v2', methods=['POST','PUT','GET'])
@token_required
def sender_apiv2():
    if request.method == 'POST':
        dataJson = request.json
        if 'send_user' in dataJson and 'status' in dataJson and 'sender_name' in dataJson and 'sender_email' in dataJson and 'sender_position' in dataJson and 'file_id' in dataJson and 'file_name' in dataJson and 'tracking_id' in dataJson and 'step_data_sid' in dataJson and 'step_code' in dataJson and 'doc_id' in dataJson and len(dataJson) == 11:
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            res_insert_sender = insert().insert_paper_sender(dataJson['send_user'],st,dataJson['status'],dataJson['sender_name'],dataJson['sender_email'],dataJson['sender_position'],dataJson['file_id'],dataJson['file_name'],dataJson['tracking_id'],dataJson['step_data_sid'],dataJson['step_code'],dataJson['doc_id'])
            if res_insert_sender['result'] == 'OK':
                res = {'result':'OK','messageText':{'messageText':res_insert_sender['messageText']},'status_Code':200}
                return jsonify(res),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_sender['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('senderuser')) != None and not (request.args.get('textsid')):
            select_getsender = select().select_get_sender_OneChain(str(request.args.get('senderuser')).replace(' ',''))
            if select_getsender['result'] == 'OK':
                return jsonify(select_getsender),200
            else:
                return jsonify({'result':'ER','messageText':select_getsender['messageText'],'status_Code':200}),200
        elif (request.args.get('senderuser')) != None and (request.args.get('textsid')) != None:
            select_getsender = select().select_get_sender_sid_v2(str(request.args.get('senderuser')).replace(' ',''),str(request.args.get('textsid')).replace(' ',''))
            if select_getsender['result'] == 'OK':
                return jsonify(select_getsender),200
            else:
                return jsonify({'result':'ER','messageText':select_getsender['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'sid' in dataJson and 'status' in dataJson and len(dataJson) == 2:
            res_update_send_detail = update().update_send_detail(dataJson['sid'], dataJson['status'])
            if res_update_send_detail['result'] == 'OK':
                return jsonify({'result': 'OK', 'messageText': res_update_send_detail['messageText'], 'status_Code': 200}), 200
            else:
                return jsonify({'result': 'ER', 'messageText': res_update_send_detail['messageText'], 'status_Code': 200}), 200
    else:
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

@status_methods.route('/api/v3/sender_details', methods=['POST','PUT','GET'])
@token_required
def sender_apiv3():
    if request.method == 'POST':
        dataJson = request.json
        if 'send_user' in dataJson and 'status' in dataJson and 'sender_name' in dataJson and 'sender_email' in dataJson and 'sender_position' in dataJson and 'file_id' in dataJson and 'file_name' in dataJson and 'tracking_id' in dataJson and 'step_data_sid' in dataJson and 'step_code' in dataJson and 'doc_id' in dataJson and 'sender_webhook' in dataJson and 'email_center' in dataJson and len(dataJson) == 13:
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            res_insert_sender = insert().insert_paper_sender_v2(dataJson['send_user'],st,dataJson['status'],dataJson['sender_name'],dataJson['sender_email'],dataJson['sender_position'],dataJson['file_id'],dataJson['file_name'],dataJson['tracking_id'],dataJson['step_data_sid'],dataJson['step_code'],dataJson['doc_id'],dataJson['sender_webhook'],dataJson['email_center'])
            if res_insert_sender['result'] == 'OK':
                res = {'result':'OK','messageText':{'messageText':res_insert_sender['messageText']},'status_Code':200}
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'status_Code':200,'messageER':None}),200
                return jsonify(res),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_sender['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('senderuser')) != None and not (request.args.get('textsid')):
            select_getsender = select().select_get_sender_OneChain(str(request.args.get('senderuser')).replace(' ',''))
            if select_getsender['result'] == 'OK':
                return jsonify(select_getsender),200
            else:
                return jsonify({'result':'ER','messageText':select_getsender['messageText'],'status_Code':200}),200
        elif (request.args.get('senderuser')) != None and (request.args.get('textsid')) != None:
            select_getsender = select().select_get_sender_sid_v2(str(request.args.get('senderuser')).replace(' ',''),str(request.args.get('textsid')).replace(' ',''))
            if select_getsender['result'] == 'OK':
                return jsonify(select_getsender),200
            else:
                return jsonify({'result':'ER','messageText':select_getsender['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'sid' in dataJson and 'status' in dataJson and len(dataJson) == 2:
            res_update_send_detail = update().update_send_detail(dataJson['sid'], dataJson['status'])
            if res_update_send_detail['result'] == 'OK':
                return jsonify({'result': 'OK', 'messageText': res_update_send_detail['messageText'], 'status_Code': 200}), 200
            else:
                return jsonify({'result': 'ER', 'messageText': res_update_send_detail['messageText'], 'status_Code': 200}), 200
    else:
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

# select_4().select_RefDocumnet('6dfb92ef-a64a-4ee9-9e47-2c736369d037')

@status_methods.route('/api/v4/sender_details', methods=['POST','PUT','GET'])
# @token_required
def sender_api_v4():
    if request.method == 'POST':
        dataJson = request.json
        if 'send_user' in dataJson and 'status' in dataJson and 'sender_name' in dataJson and 'sender_email' in dataJson and 'sender_position' in dataJson and 'file_id' in dataJson and 'file_name' in dataJson and 'tracking_id' in dataJson and 'step_data_sid' in dataJson and 'step_code' in dataJson and 'doc_id' in dataJson and 'sender_webhook' in dataJson and 'email_center' in dataJson and len(dataJson) == 13:
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            tmp_send_user = dataJson['send_user']
            tmp_status = dataJson['status']
            tmp_sender_name = dataJson['sender_name']
            tmp_sender_email = dataJson['sender_email']
            tmp_sender_position = dataJson['sender_position']
            tmp_file_id = dataJson['file_id']
            tmp_file_name = dataJson['file_name']
            tmp_tracking_id = dataJson['tracking_id']
            tmp_sidcode = dataJson['step_data_sid']
            tmp_step_code = dataJson['step_code']
            tmp_doc_id = dataJson['doc_id']
            tmp_sender_webhook = dataJson['sender_webhook']
            tmp_email_center = dataJson['email_center']
            
            res_insert_sender = insert().insert_paper_sender_v2(tmp_send_user,st,tmp_status,tmp_sender_name,tmp_sender_email,tmp_sender_position,tmp_file_id,tmp_file_name,tmp_tracking_id,tmp_sidcode,tmp_step_code,tmp_doc_id,tmp_sender_webhook,tmp_email_center)
            if res_insert_sender['result'] == 'OK':
                # res = {'result':'OK','messageText':{'messageText':res_insert_sender['messageText']},'status_Code':200}
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'status_Code':200,'messageER':None}),200
                return jsonify(res),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_sender['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('senderuser')) != None and not (request.args.get('textsid')):
            select_getsender = select().select_get_sender_OneChain(str(request.args.get('senderuser')).replace(' ',''))
            if select_getsender['result'] == 'OK':
                return jsonify(select_getsender),200
            else:
                return jsonify({'result':'ER','messageText':select_getsender['messageText'],'status_Code':200}),200
        elif (request.args.get('senderuser')) != None and (request.args.get('textsid')) != None:
            select_getsender = select().select_get_sender_sid_v2(str(request.args.get('senderuser')).replace(' ',''),str(request.args.get('textsid')).replace(' ',''))
            if select_getsender['result'] == 'OK':
                return jsonify(select_getsender),200
            else:
                return jsonify({'result':'ER','messageText':select_getsender['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'sid' in dataJson and 'status' in dataJson and len(dataJson) == 2:
            res_update_send_detail = update().update_send_detail(dataJson['sid'], dataJson['status'])
            if res_update_send_detail['result'] == 'OK':
                return jsonify({'result': 'OK', 'messageText': res_update_send_detail['messageText'], 'status_Code': 200}), 200
            else:
                return jsonify({'result': 'ER', 'messageText': res_update_send_detail['messageText'], 'status_Code': 200}), 200
    else:
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

@status_methods.route('/api/recipient', methods=['POST','PUT','GET'])
@token_required
def recipient_api():
    if request.method == 'GET':
        emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", request.args.get('email'))
        if emails is None:
            return jsonify({'result':'ER','messageText':'ข้อมูล email ไม่ตรงตามรูปแบบ','status_Code':200}),200
        else:
            pass
        if (request.args.get('email')) != None and not request.args.get('sid'):
            res_select_recipient = select().select_get_recipient(str(request.args.get('email')).replace(' ',''))
            if res_select_recipient['result'] == 'OK':
                return jsonify(res_select_recipient),200
            else:
                return jsonify({'result':'ER','messageText':res_select_recipient['messageText'],'status_Code':200}),200
        elif (request.args.get('email')) != None and (request.args.get('sid')) != None:
            res_select_recipient_sid = select().select_get_recipient_sid(str(request.args.get('email')).replace(' ',''),str(request.args.get('sid')).replace(' ',''))
            return jsonify(res_select_recipient_sid),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    else:
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

@status_methods.route('/api/recipient/v2', methods=['POST','PUT','GET'])
@token_required
def recipient_apiv2():
    if request.method == 'GET':
        emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", request.args.get('email'))
        if emails is None:
            return jsonify({'result':'ER','messageText':'ข้อมูล email ไม่ตรงตามรูปแบบ','status_Code':200}),200
        else:
            pass
        if (request.args.get('email')) != None and not request.args.get('sid'):
            res_select_recipient = select().select_get_recipient_OneChain(str(request.args.get('email')).replace(' ',''))
            if res_select_recipient['result'] == 'OK':
                return jsonify(res_select_recipient),200
            else:
                return jsonify({'result':'ER','messageText':res_select_recipient['messageText'],'status_Code':200}),200
        elif (request.args.get('email')) != None and (request.args.get('sid')) != None:
            res_select_recipient_sid = select().select_get_recipient_sid_OneChain(str(request.args.get('email')).replace(' ',''),str(request.args.get('sid')).replace(' ',''))
            if res_select_recipient_sid['result'] == 'OK':
                return jsonify(res_select_recipient_sid),200
            else:
                return jsonify({'result':'ER','messageText':res_select_recipient_sid['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    else:
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

@status_methods.route('/api/pdf', methods=['GET','PUT','POST'])
@token_required
def pdf_api():
    if request.method == 'GET':
        if (request.args.get('data')) != None:
            res_select_pdf = select().select_get_pdf(str(request.args.get('data')).replace(' ',''))
            return jsonify(res_select_pdf),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'Parameter Fail!'}),404
    elif request.method == 'PUT':
        datajson = request.json
        if 'sid_id_file' in datajson and 'string_sign' in datajson:
            res_select_check = select().select_pdf_check_forupdate(datajson['sid_id_file'])
            if res_select_check['result'] == 'OK':
                res_updatepdf = update().update_pdf(datajson['sid_id_file'],datajson['string_sign'])
                if res_updatepdf['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':res_updatepdf['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':res_updatepdf['messageText'],'status_Code':200}),200
            else:
                res_updatepdf = update().update_pdf(datajson['sid_id_file'],datajson['string_sign'])
                if res_updatepdf['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':res_updatepdf['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':res_updatepdf['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'Parameter Fail!'}),404
    elif request.method == 'POST':
        datajson = request.json
        if 'OneChain' in datajson and 'sidCode' in datajson and len(datajson) == 2:
            if isinstance(datajson['OneChain'],bool):
                if datajson['OneChain'] == True:
                    res_select_pdf = select().select_get_pdf_v2(str(datajson['sidCode']).replace(' ',''))
                    if res_select_pdf['result'] == 'OK':
                        res_LoginOnechain = Login_OneChain()
                        if res_LoginOnechain['result'] == "OK":
                            getTokenOneChain = res_LoginOnechain['messageText']['token']
                            userId = res_select_pdf['messageText']['file_OneChain']['metadata']['user_id']
                            fileId = res_select_pdf['messageText']['file_OneChain']['metadata']['file_id']
                            result_queryFileOneChain = QueryFile_OneChain(getTokenOneChain,userId,fileId)
                            if result_queryFileOneChain['result'] == 'OK':
                                res_select_pdf['messageText']['file_OneChain'] = {}
                                buffer_file = result_queryFileOneChain['messageText']['buffer_file']['data']
                                res_Base64 = Convert_ArrBuffer_To_Base64(buffer_file)
                                if res_Base64['result'] == 'OK':
                                    st = datetime.datetime.fromtimestamp(result_queryFileOneChain['messageText']['metadata']['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                                    res_select_pdf['messageText']['file_OneChain']['file_base'] = res_Base64['messageText']['base_string']
                                    res_select_pdf['messageText']['file_OneChain']['datetime'] = None
                                    res_select_pdf['messageText']['file_OneChain']['datetime_string'] = st
                                    res_select_pdf['messageText']['file_OneChain']['datetime_upload']= None
                                    res_select_pdf['messageText']['file_OneChain']['datetime_upload_string']= st
                                    return jsonify({'result':'OK','messageText':res_select_pdf['messageText'],'status_Code':200,'messageER':None}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found PDF!'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found PDF!'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found PDF!'}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found PDF!'}),200
                else:
                    res_select_pdf = select().select_get_pdf(str(datajson['sidCode']).replace(' ',''))
                    result_SelectPdf = {}
                    if res_select_pdf['result'] == 'OK':
                        result_SelectPdf['file_OneChain'] = {}
                        result_SelectPdf['file_OneChain']['datetime'] = None
                        result_SelectPdf['file_OneChain']['datetime_string'] = None
                        result_SelectPdf['file_OneChain']['datetime_upload'] = None
                        result_SelectPdf['file_OneChain']['datetime_upload_string'] = None
                        result_SelectPdf['file_OneChain']['file_base'] = None
                        result_SelectPdf['file_Paperless'] = {}
                        result_SelectPdf['file_Paperless'] = res_select_pdf['messageText']
                        return jsonify({'result':'OK','messageText':result_SelectPdf,'status_Code':200,'messageER':None}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found PDF!'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'OneChain Bool Only!'}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'Parameter Fail!'}),404

@status_methods.route('/api/pdf/v2', methods=['GET','PUT','POST'])
@token_required_v3
def pdf_api_v2():
    if request.method == 'GET':
        if (request.args.get('data')) != None:
            res_select_pdf = select().select_get_pdf(str(request.args.get('data')).replace(' ',''))
            return jsonify(res_select_pdf),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'Parameter Fail!'}),404
    elif request.method == 'PUT':
        datajson = request.json
        if 'sid_id_file' in datajson and 'string_sign' in datajson:
            res_select_check = select().select_pdf_check_forupdate(datajson['sid_id_file'])
            if res_select_check['result'] == 'OK':
                res_updatepdf = update().update_pdf_v2(datajson['sid_id_file'],datajson['string_sign'])
                if res_updatepdf['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'message':'update success','data':None},'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':res_updatepdf['messageText'],'status_Code':200}),200
            else:
                res_updatepdf = update().update_pdf_v2(datajson['sid_id_file'],datajson['string_sign'])
                if res_updatepdf['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'message':'update success','data':None},'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':res_updatepdf['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'Parameter Fail!'}),404
    elif request.method == 'POST':
        datajson = request.json
        if 'OneChain' in datajson and 'sidCode' in datajson and len(datajson) == 2:
            if isinstance(datajson['OneChain'],bool):
                if datajson['OneChain'] == True:
                    res_select_pdf = select().select_get_pdf_v2(str(datajson['sidCode']).replace(' ',''))
                    if res_select_pdf['result'] == 'OK':
                        res_LoginOnechain = Login_OneChain()
                        if res_LoginOnechain['result'] == "OK":
                            getTokenOneChain = res_LoginOnechain['messageText']['token']
                            userId = res_select_pdf['messageText']['file_OneChain']['metadata']['user_id']
                            fileId = res_select_pdf['messageText']['file_OneChain']['metadata']['file_id']
                            result_queryFileOneChain = QueryFile_OneChain(getTokenOneChain,userId,fileId)
                            if result_queryFileOneChain['result'] == 'OK':
                                res_select_pdf['messageText']['file_OneChain'] = {}
                                buffer_file = result_queryFileOneChain['messageText']['buffer_file']['data']
                                res_Base64 = Convert_ArrBuffer_To_Base64(buffer_file)
                                if res_Base64['result'] == 'OK':
                                    st = datetime.datetime.fromtimestamp(result_queryFileOneChain['messageText']['metadata']['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                                    res_select_pdf['messageText']['file_OneChain']['file_base'] = res_Base64['messageText']['base_string']
                                    res_select_pdf['messageText']['file_OneChain']['datetime'] = None
                                    res_select_pdf['messageText']['file_OneChain']['datetime_string'] = st
                                    res_select_pdf['messageText']['file_OneChain']['datetime_upload']= None
                                    res_select_pdf['messageText']['file_OneChain']['datetime_upload_string']= st
                                    return jsonify({'result':'OK','messageText':res_select_pdf['messageText'],'status_Code':200,'messageER':None}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found PDF!'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found PDF!'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found PDF!'}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found PDF!'}),200
                else:
                    res_select_pdf = select().select_get_pdf(str(datajson['sidCode']).replace(' ',''))
                    result_SelectPdf = {}
                    if res_select_pdf['result'] == 'OK':
                        result_SelectPdf['file_OneChain'] = {}
                        result_SelectPdf['file_OneChain']['datetime'] = None
                        result_SelectPdf['file_OneChain']['datetime_string'] = None
                        result_SelectPdf['file_OneChain']['datetime_upload'] = None
                        result_SelectPdf['file_OneChain']['datetime_upload_string'] = None
                        result_SelectPdf['file_OneChain']['file_base'] = None
                        result_SelectPdf['file_Paperless'] = {}
                        result_SelectPdf['file_Paperless'] = res_select_pdf['messageText']
                        return jsonify({'result':'OK','messageText':result_SelectPdf,'status_Code':200,'messageER':None}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found PDF!'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'OneChain Bool Only!'}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'Parameter Fail!'}),404

@status_methods.route('/api/views/v1', methods=['POST'])
def view_Detailsv1():
    if request.method == 'POST':
        datajson = request.json
        if 'email' in datajson and 'sidCode' in datajson and len(datajson) == 2:
            result_selectViews = select().select_getViewDetails(datajson['sidCode'],datajson['email'])
            if result_selectViews['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_selectViews['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_selectViews['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404

@status_methods.route('/api/sign', methods=['POST','GET'])
@token_required
def sign_api():
    if request.method == 'POST':
        datajson = request.json
        if 'sid' in datajson and 'sign_json' in datajson and 'file_id' in datajson and len(datajson) == 3:
            try:
                eval(datajson['sign_json'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล sign_json ให้เป็น Json ได้ '}),200
            res_insert_sign = insert().insert_sign_data(datajson['sid'],datajson['sign_json'],datajson['file_id'])
            if res_insert_sign['result'] == 'OK':
                return jsonify({'result':'OK','messageText':res_insert_sign['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_sign['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
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
        if (request.args.get('signsid')) != None and (request.args.get('email')) != None:
            res_select_sign = select().select_sign(str(request.args.get('signsid')).replace(' ',''),str(request.args.get('email')).replace(' ',''))
            if res_select_sign['result'] == 'OK':
                return jsonify(res_select_sign),200
            else:
                return jsonify(res_select_sign),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/sign/v2', methods=['POST','GET'])
@token_required
def sign_api_v2():
    if request.method == 'POST':
        datajson = request.json
        if 'sid' in datajson and 'sign_json' in datajson and 'file_id' in datajson and len(datajson) == 3:
            try:
                eval(datajson['sign_json'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล sign_json ให้เป็น Json ได้ '}),200
            res_insert_sign = insert().insert_sign_data(datajson['sid'],datajson['sign_json'],datajson['file_id'])
            if res_insert_sign['result'] == 'OK':
                return jsonify({'result':'OK','messageText':res_insert_sign['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_sign['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('signsid')) != None and (request.args.get('email')) != None:
            res_select_sign = select().select_sign_v2(str(request.args.get('signsid')).replace(' ',''),str(request.args.get('email')).replace(' ',''))
            if res_select_sign['result'] == 'OK':
                return jsonify(res_select_sign),200
            else:
                return jsonify(res_select_sign),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/v3/sign', methods=['POST','GET'])
@token_required_v3
def sign_api_v3():
    if request.method == 'POST':
        datajson = request.json
        if 'sid' in datajson and 'sign_json' in datajson and 'file_id' in datajson and len(datajson) == 3:
            try:
                eval(datajson['sign_json'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล sign_json ให้เป็น Json ได้ '}),200
            res_insert_sign = insert().insert_sign_data(datajson['sid'],datajson['sign_json'],datajson['file_id'])
            if res_insert_sign['result'] == 'OK':
                return jsonify({'result':'OK','messageText':res_insert_sign['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_sign['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('signsid')) != None and (request.args.get('email')) != None:
            res_select_sign = select().select_sign_v3(str(request.args.get('signsid')).replace(' ',''),str(request.args.get('email')).replace(' ',''))
            if res_select_sign['result'] == 'OK':
                return jsonify(res_select_sign),200
            else:
                return jsonify(res_select_sign),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/pdfSign/v1',methods=['GET'])
@token_required_v3
def pdfSign_api():
    if request.method == 'GET':
        try:
            token_header = request.headers['Authorization']
            # token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            abort(401)
        if (request.args.get('data')) != None and (request.args.get('stepnum')) != None:
            result_select = select().select_CheckPdf(str(request.args.get('data')).replace(' ',''),str(request.args.get('stepnum')).replace(' ',''))
            tmp_shared_token = None
            url = one_url + '/api/v2/service/shared-token'
            resultToken = callAuth_get(url,token_header)
            if 'status' in resultToken:
                if resultToken['status'] == 'success':
                    tmpjson_token = resultToken['response']
                    tmpjson_token = tmpjson_token.json()
                    if tmpjson_token['result'] == 'Success':
                        tmpdata = tmpjson_token['data']
                        tmp_shared_token = tmpdata['shared_token']
                    # print(tmpjson_token.json())
            result_select['shared_token'] = tmp_shared_token
            return jsonify(result_select)
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/pdfSign/v2',methods=['GET'])
@token_required_v3
def pdfSign_api_v2():
    if request.method == 'GET':
        try:
            token_header = request.headers['Authorization']
            # token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            abort(401)
        if (request.args.get('data')) != None and (request.args.get('stepnum')) != None:
            # result_select = select().select_CheckPdf(str(request.args.get('data')).replace(' ',''),str(request.args.get('stepnum')).replace(' ',''))
            # tmp_shared_token = None
            url = one_url + '/api/v2/service/shared-token'
            data = str(request.args.get('data')).replace(' ','')
            stepnum = str(request.args.get('stepnum')).replace(' ','')
            with concurrent.futures.ThreadPoolExecutor() as executor:
                select01 = executor.submit(select().select_CheckPdf,data,stepnum)
                callAuth_get01 = executor.submit(callAuth_get,url,token_header)
                result_select = select01.result()
                resultToken = callAuth_get01.result()
            if 'status' in resultToken:
                if resultToken['status'] == 'success':
                    tmpjson_token = resultToken['response']
                    tmpjson_token = tmpjson_token.json()
                    if tmpjson_token['result'] == 'Success':
                        tmpdata = tmpjson_token['data']
                        tmp_shared_token = tmpdata['shared_token']
                    # print(tmpjson_token.json())
            result_select['shared_token'] = tmp_shared_token
            return jsonify(result_select)
        abort(404)

@status_methods.route('/api/mail', methods=['POST'])
def mail_api():
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
        setEmail_json = request.json
        result_mail = []
        for n in range(len(setEmail_json)):
            if 'sid' in setEmail_json[n] and 'subject' in setEmail_json[n] and 'to' in setEmail_json[n] and 'url_file' in setEmail_json[n] and 'qr_code' in setEmail_json[n] and 'description' in setEmail_json[n] and len(setEmail_json[n]) == 6:
                HOST = "mailtx.inet.co.th"
                SUBJECT = setEmail_json[n]['subject']
                TO = setEmail_json[n]['to']
                Url_file = setEmail_json[n]['url_file']

                FROM = "Signning Document"
                msg = MIMEMultipart('alternative')
                msg['Subject'] = SUBJECT
                msg['From'] = FROM
                msg['To'] = TO
                string_qrCode = qr_Code.gen_qrcode(setEmail_json[n]['qr_code'])
                hash_string_qrCode = hashlib.sha256(str(string_qrCode).encode('utf8')).hexdigest()
                sid = setEmail_json[n]['sid']
                url_sendEmail = 'https://devinet-etax.one.th/status_methods/api/qrcode/' + str(hash_string_qrCode)  +'.jpg'
                html = "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"></head><body><p><b>" + SUBJECT +"</b></p><p>ลิงค์เข้าระบบลงลายเซ็น :<b>" + Url_file +"</b></p></br><p>" + setEmail_json[n]['description'] + "</p><br><img src=" + url_sendEmail + " width=\"250\" height=\"250\"><br><br><i>ขอบคุณที่ใช้บริการ</i><br>" \
                "<p><i>© Copyright 2020, Internet Thailand Public Company Limited.</i><br><br>กรุณาอย่าตอบกลับอีเมลนี้</p></body></html>"
                part2 = MIMEText(html, 'html',"utf-8")
                msg.attach(part2)
                try:
                    s = smtplib.SMTP(HOST)
                    s.sendmail(FROM, TO, msg.as_string())
                    s.quit()
                    res_insert = insert().insert_sendEmail(sid,'OK',TO,FROM,string_qrCode,setEmail_json[n]['qr_code'])
                    result_mail.append(res_insert)
                except Exception as ex:
                    res_insert = insert().insert_sendEmail(sid, str(ex), TO, FROM,string_qrCode, setEmail_json[n]['qr_code'])
                    result_mail.append({'status': 'ER', 'messageText': str(ex)})
            else:
                result_mail.append({'result':'ER','messageText':'Parameter Fail!','status_Code':404})
        return jsonify({'detail_sendmail': result_mail, 'result': 'OK', 'status_Code': 200}), 200

@status_methods.route('/api/mail_string', methods=['POST'])
def mail_string_api():
    if request.method == 'POST':
        json_string = request.json
        if 'string_Json' in json_string and len(json_string) == 1:
            try:
                json_string['string_Json'] = eval(json_string['string_Json'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล string_Json ให้เป็น Json ได้ '}),200
            res_selectEmail = selection_email(json_string['string_Json'])
            if res_selectEmail['result'] == 'OK':
                return jsonify(res_selectEmail),200
            else:
                return jsonify(res_selectEmail),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/mail_string/v2', methods=['POST'])
def mail_string_api_v2():
    if request.method == 'POST':
        json_string = request.json
        if 'string_Json' in json_string and 'step_Max' in json_string and len(json_string) == 2:
            try:
                json_string['string_Json'] = eval(json_string['string_Json'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล string_Json ให้เป็น Json ได้ '}),200
            res_selectEmail = selection_email_v2(json_string['string_Json'],json_string['step_Max'])
            if res_selectEmail['result'] == 'OK':
                return jsonify(res_selectEmail),200
            else:
                return jsonify(res_selectEmail),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/qrcode/<string:qr_namefile>.jpg', methods=['GET'])
def qrCode(qr_namefile):
    res_base_qrCode = select().select_qrCodeImage(qr_namefile)
    letters = string.ascii_letters
    string_ = ''.join(random.choice(letters) for i in range(20))
    imgdata = base64.b64decode(res_base_qrCode['qrcode_string'])
    response = make_response(imgdata)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'as_attachment=False', filename='%s.jpg' % string_)
    return response

@status_methods.route('/file/pdf/<string:pdf_namefile>.pdf', methods=['GET'])
def getPdf_NameFile(pdf_namefile=None):
    if pdf_namefile is not None:
        with open("./templateFile/" + pdf_namefile +".pdf", "rb") as pdf_file:
            encoded_string = pdf_file.read()
        print(encoded_string)
        response = make_response(encoded_string)
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set(
            'Content-Disposition', 'as_attachment=False', filename='%s.pdf' % pdf_namefile)
        return response

@status_methods.route('/api/ref', methods=['POST','PUT'])
def ref_Doc():
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
        json_Set = request.json
        if 'sid' in json_Set:
            print(select().select_refCode(json_Set['sid']))
            return jsonify({'result': 'OK', 'status_Code': 200}), 200
    elif request.method == 'PUT':
        try:
            token_header = request.headers['Authorization']
            resCheck = checkToken(str(token_header).split(' ')[1])
            if resCheck['result'] == 'OK':
                pass
            else:
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        json_Set = request.json
        try:
            eval(json_Set['ref_Details'])
        except Exception as ex:
            return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล sign_json ให้เป็น Json ได้ '}),200
        if 'sid' in json_Set and 'ref_Code' in json_Set and 'ref_Details' in json_Set and len(json_Set) == 3:
            update().update_refCode(json_Set['sid'],json_Set['ref_Code'],json_Set['ref_Details'])
            return jsonify({'result': 'OK', 'messageText':'update OK!', 'status_Code': 200}), 200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/sign_auth',methods=['POST'])
@token_required
def sign_auth():
    if request.method == 'POST':
        json_Set = request.json
        if 'page' in json_Set and 'llx' in json_Set and 'lly' in json_Set and 'urx' in json_Set and 'ury' in json_Set and 'userName' in json_Set and 'stringPicture' in json_Set and 'stringPdf' in json_Set and  len(json_Set) == 8:
            page = json_Set['page']
            llx = json_Set['llx']
            lly = json_Set['lly']
            urx = json_Set['urx']
            ury = json_Set['ury']
            userName = json_Set['userName']
            stringPicture = json_Set['stringPicture']
            stringPdf = json_Set['stringPdf']
            try:
                token_header = request.headers['Authorization']
            except KeyError as ex:
                return jsonify({'result':'ER','messageText':'Not Found Authorization!','status_Code':401 }),401
            res_send_sign = send_tosign(page,llx,lly,urx,ury,userName,stringPicture,stringPdf,token_header)
            if res_send_sign['result'] == 'OK':
                return jsonify({'result': 'OK', 'messageText':res_send_sign['msg'], 'status_Code': 200}), 200
            else:
                return jsonify({'result': 'ER', 'messageText':res_send_sign['msg'], 'status_Code': 200}), 200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/sign_auth/v2',methods=['POST'])
# @token_required
def sign_authv2():
    if request.method == 'POST':
        json_Set = request.json
        if 'page' in json_Set and 'llx' in json_Set and 'lly' in json_Set and 'urx' in json_Set and 'ury' in json_Set and 'userName' in json_Set and 'stringPicture' in json_Set and 'stringPdf' in json_Set and  len(json_Set) == 8:
            page = int(json_Set['page'])
            llx = float(json_Set['llx'])
            lly = float(json_Set['lly'])
            urx = float(json_Set['urx'])
            ury = float(json_Set['ury'])
            userName = json_Set['userName']
            stringPicture = json_Set['stringPicture']
            stringPdf = json_Set['stringPdf']
            with io.BytesIO(base64.b64decode(stringPdf)) as open_pdf_file:
                read_pdf = PdfFileReader(open_pdf_file)
                num_pages = read_pdf.getNumPages()
                pHeight = read_pdf.getPage(0).mediaBox.getUpperRight_y() / 2
                pWidth = read_pdf.getPage(0).mediaBox.getUpperRight_x() / 2
                pHeight = int(pHeight)
                pWidth = int(pWidth)
            string_Path = pdf_class().genPdf_Topng_v2(urx,ury,llx,lly,stringPicture,pWidth,pHeight)
            if string_Path['result'] == 'OK':
                string_pdf_merge = pdf_class().merge_png_to_pdf(page,stringPdf,string_Path['messageText'],userName)
                if string_pdf_merge['result'] == 'OK':
                    return jsonify({'result': 'OK', 'messageText':string_pdf_merge['messageText'], 'status_Code': 200,'messageER':None}), 200
                else:
                    return jsonify({'result': 'ER', 'messageText':None, 'status_Code': 200,'messageER':string_pdf_merge['messageText']}), 200
            else:
                return jsonify({'result': 'ER', 'messageText':None, 'status_Code': 200,'messageER':{'string_Path':['messageText'],'code':'ERSA001'}}), 200

@status_methods.route('/api/v3/signning',methods=['POST'])
# @token_required
def sign_auth_api_v3():
    if request.method == 'POST':
        json_Set = request.json
        if 'page' in json_Set and 'llx' in json_Set and 'lly' in json_Set and 'urx' in json_Set and 'ury' in json_Set and 'userName' in json_Set and 'stringPicture' in json_Set and 'stringPdf' in json_Set and 'landscape' in json_Set and  len(json_Set) == 9:
            page = int(json_Set['page'])
            llx = float(json_Set['llx'])
            lly = float(json_Set['lly'])
            urx = float(json_Set['urx'])
            ury = float(json_Set['ury'])
            userName = json_Set['userName']
            stringPicture = json_Set['stringPicture']
            stringPdf = json_Set['stringPdf']
            orientation = json_Set['landscape']
            string_Path = pdf_class().genPdf_Topng_v2(urx,ury,llx,lly,stringPicture,orientation)
            if string_Path['result'] == 'OK':
                string_pdf_merge = pdf_class().merge_png_to_pdf(page,stringPdf,string_Path['messageText'],userName)
                if string_pdf_merge['result'] == 'OK':
                    return jsonify({'result': 'OK', 'messageText':string_pdf_merge['messageText'], 'status_Code': 200,'messageER':None}), 200
                else:
                    return jsonify({'result': 'ER', 'messageText':None, 'status_Code': 200,'messageER':string_pdf_merge['messageText']}), 200
            else:
                return jsonify({'result': 'ER', 'messageText':None, 'status_Code': 200,'messageER':string_Path['messageText']}), 200
        else:
            return jsonify({'result': 'ER', 'messageText':None, 'status_Code': 404,'messageER':'parameter incorrect'}), 404

@status_methods.route('/api/access',methods=['GET'])
def access():
    if request.method == 'GET':
        try:
            token_header = request.headers['Authorization']
            try:
                res_newToken = get_access(str(token_header).split(' ')[1])
            except Exception as ex:
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':200}),200
        except KeyError as ex:
            return jsonify({'result':'ER','messageText':'Not Found Authorization!','status_Code':401}),401
        return jsonify({'result':'OK','token':res_newToken})

@status_methods.route('/api/access/v2',methods=['GET'])
def access_v2():
    if request.method == 'GET':
        try:
            token_header = request.headers['Authorization']
            try:
                res_newToken = get_access_v2(str(token_header).split(' ')[1])
                if res_newToken['result'] == 'OK':
                    return jsonify({'result':'OK','token':res_newToken['token'],'messageText':None})
                else:
                    return jsonify({'result':'ER','token':None,'messageText':res_newToken['messageText']})
            except Exception as ex:
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':200}),200
        except KeyError as ex:
            return jsonify({'result':'ER','messageText':'Not Found Authorization!','status_Code':401}),401

@status_methods.route('/api/OneAuth/Sign/v2',methods=['POST'])
def oneAuth_API_v2():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'base64_string' in dataJson and 'max_Step' in dataJson and 'Step_Num' in dataJson and len(dataJson) == 3:
            res_arraylist = []
            base64_pdf_String = dataJson['base64_string']
            res_list = credentials_list_v2("","","","","",token_header)
            type_certifyLevel = ''
            try:
                if res_list['result'] == 'OK':
                    res_arraylist.append({'result_listService':res_list})
                    credentialId = res_list['msg']['credentials'][0]['credentialId']
                    res_authorize = credentials_authorize_v2(credentialId,"","","","","","","",token_header)
                    if res_authorize['result'] == 'OK':
                        res_arraylist.append({'result_authorizeService':res_authorize})
                        sadData = res_authorize['msg']['sad']
                        if dataJson['Step_Num'] == dataJson['max_Step']:
                            type_certifyLevel = 'CERTIFY'
                        else:
                            type_certifyLevel = 'NON-CERTIFY'
                        res_signPdf = signing_pdfSigning_v2(base64_pdf_String,sadData,"","","",type_certifyLevel,"","","","","","",token_header)
                        print(res_signPdf)
                        if res_signPdf['result'] == 'OK':
                            res_arraylist.append({'result_signPdfService':res_signPdf})
                            return jsonify({'result':'OK','messageText':res_arraylist,'status_Code':200,'messageER':None,'messageService':type_certifyLevel}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'signPdf Service Error!'}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Authorize Service Error!'}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error!'}),200
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error!'}),200

@status_methods.route('/api/OneAuth/Sign/v3',methods=['POST'])
def oneAuth_API_v3():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'base64_string' in dataJson and 'max_Step' in dataJson and 'Step_Num' in dataJson and 'sign_position' in dataJson and 'sign_string' in dataJson and len(dataJson) == 5:
            sign_position = dataJson['sign_position']
            sign_string = dataJson['sign_string']
            if 'sign_llx' in sign_position and 'sign_lly' in sign_position and 'sign_urx' in sign_position and 'sign_ury' in sign_position and 'sign_page' in sign_position and len(sign_position) == 5:
                res_arraylist = []
                base64_pdf_String = dataJson['base64_string']
                res_list = credentials_list_v2("","","","","",token_header)
                type_certifyLevel = ''
                try:
                    if res_list['result'] == 'OK':
                        res_arraylist.append({'result_listService':res_list})
                        credentialId = res_list['msg']['credentials'][0]['credentialId']
                        res_authorize = credentials_authorize_v2(credentialId,"","","","","","","",token_header)
                        if res_authorize['result'] == 'OK':
                            res_arraylist.append({'result_authorizeService':res_authorize})
                            sadData = res_authorize['msg']['sad']
                            if int(dataJson['Step_Num']) == int(dataJson['max_Step']):
                                type_certifyLevel = 'CERTIFY'
                            else:
                                type_certifyLevel = 'NON-CERTIFY'
                            res_signPdf = signing_pdfSigning_v3(base64_pdf_String,sadData,"","","",type_certifyLevel,"","","","","","",token_header,sign_position,sign_string)
                            print(res_signPdf)
                            if res_signPdf['result'] == 'OK':
                                res_arraylist.append({'result_signPdfService':res_signPdf})
                                return jsonify({'result':'OK','messageText':res_arraylist,'status_Code':200,'messageER':None,'messageService':type_certifyLevel}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'signPdf Service Error!'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Authorize Service Error!'}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + res_list['msg']}),200
                except Exception as ex:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + str(ex)}),200

@status_methods.route('/api/getsign/v1',methods=['POST'])
@token_required
def getSign_api():
    if request.method == 'POST':
        dataJson = request.json
        if 'username' in dataJson and 'userid' in dataJson and len(dataJson) == 2:
            username = dataJson['username']
            userId = dataJson['userid']
            resultSignString = select().select_signString(username,userId)
            if resultSignString['result'] == 'OK':
                return jsonify({'result':'OK','messageText':resultSignString['messageText']['signString'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':resultSignString['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404

@status_methods.route('/api/comment/v1',methods=['POST'])
# @token_required
def getCommentv1():
    if request.method == 'POST':
        dataJson = request.json
        if 'typeService' in dataJson:
            if dataJson['typeService'].lower() == 'insert':
                if 'sidCode' in dataJson and 'json_Comment' in dataJson:
                    try:
                        eval(dataJson['json_Comment'])
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'json_Comment No Json'}),200
                    res_insertComment = insert().insert_messageComment(dataJson['sidCode'],dataJson['json_Comment'])
                    if res_insertComment['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':'insert success','status_Code':200,'messageER':None}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'insert fail ' + res_insertComment['messageText']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404
            elif dataJson['typeService'].lower() == 'select':
                if 'sidCode' in dataJson:
                    result_getComment = select().select_getComment(dataJson['sidCode'])
                    if result_getComment['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_getComment['messageText'],'status_Code':200,'messageER':None}),200
                    else:
                        return jsonify({'result':'OK','messageText':[],'status_Code':200,'messageER':result_getComment['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404
            elif dataJson['typeService'].lower() == 'update':
                if 'sidCode' in dataJson and 'email' in dataJson and 'messageComment' in dataJson:
                    result_update = update().update_messageComment(dataJson['sidCode'],dataJson['email'],dataJson['messageComment'])
                    if result_update['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_update['messageText']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404

@status_methods.route('/api/v2/comment',methods=['POST','GET','PUT'])
@token_required_v3
def getCommentv2():
    if request.method == 'POST':
        dataJson = request.json
        if 'sidCode' in dataJson and 'email' in dataJson and 'id' in dataJson and 'comment' in dataJson and 'step' in dataJson and len(dataJson) == 5:
            sidCode = dataJson['sidCode']
            email = dataJson['email']
            tmp_id = dataJson['id']
            comment = dataJson['comment']
            step = dataJson['step']
            result = insert().insert_messageComment_v2(sidCode,email,tmp_id,comment,step)
            if result['result'] == 'OK':
                if result['dict_comment'] != None:
                    list_onemail = []
                    list_resultOnechat = []
                    dict_comment = result['dict_comment']
                    msg_general = dict_comment['msg_general']
                    msg_sender = dict_comment['msg_sender']
                    list_onemail = dict_comment['list_onemail']
                    st1 = datetime.datetime.now()
                    for x in range(len(list_onemail)):
                        get_idBot = search_frd(list_onemail[x],'')
                        if get_idBot != None:
                            # get_idBot_eval = eval(str(get_idBot))
                            # fri = eval(str(get_idBot_eval['friend']))
                            # id_onechat = fri['user_id']
                            if email == list_onemail[x]:
                                result_onechat = send_messageToChat(msg_sender,list_onemail[x])
                            else :
                                result_onechat = send_messageToChat(msg_general,list_onemail[x])
                    return jsonify({'result':'OK','messageText':result['messageText'],'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result['messageText']}),200                
                return jsonify({'result':'OK','messageText':result['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result['messageText']}),200
        elif 'sidCode' in dataJson and 'email' in dataJson and 'id' in dataJson and len(dataJson) == 3:
            sidCode = dataJson['sidCode']
            email = dataJson['email']
            tmp_id = dataJson['id']
            result = delete().delete_status_comment(sidCode,email,tmp_id)
            if result['result'] == 'OK':
                if result['dict_comment'] != None:
                    list_onemail = []
                    list_resultOnechat = []
                    dict_comment = result['dict_comment']
                    msg_general = dict_comment['msg_general']
                    msg_sender = dict_comment['msg_sender']
                    list_onemail = dict_comment['list_onemail']
                    st1 = datetime.datetime.now()
                    for x in range(len(list_onemail)):
                        get_idBot = search_frd(list_onemail[x],'')
                        if get_idBot != None:
                            # get_idBot_eval = eval(str(get_idBot))
                            # fri = eval(str(get_idBot_eval['friend']))
                            # id_onechat = fri['user_id']
                            if email == list_onemail[x]:
                                result_onechat = send_messageToChat(msg_sender,list_onemail[x])
                            else :
                                result_onechat = send_messageToChat(msg_general,list_onemail[x])
                return jsonify({'result':'OK','messageText':result['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'OK','messageText':[],'status_Code':200,'messageER':result['messageText']}),200
        elif 'comment' in dataJson and len(dataJson) == 1:
            comment01 = dataJson['comment']
            # print(sidCode)
            List_result = []
            for x in range(len(comment01)):
                sidCode = comment01[x]['ppl_id']
                email = comment01[x]['email']
                tmp_id = comment01[x]['id']
                comment = comment01[x]['comment']
                modified_date = comment01[x]['modified_date']
                step = ''
                result_status = {}
                result = insert().insert_messageComment_for_Eform(sidCode,email,tmp_id,comment,step,modified_date)
                if result['result'] == 'OK':
                    if result['dict_comment'] != None:
                        list_onemail = []
                        list_resultOnechat = []
                        dict_comment = result['dict_comment']
                        msg_general = dict_comment['msg_general']
                        msg_sender = dict_comment['msg_sender']
                        list_onemail = dict_comment['list_onemail']
                        st1 = datetime.datetime.now()
                        for x in range(len(list_onemail)):
                            get_idBot = search_frd(list_onemail[x],'')
                            if get_idBot != None:
                                # get_idBot_eval = eval(str(get_idBot))
                                # fri = eval(str(get_idBot_eval['friend']))
                                # id_onechat = fri['user_id']
                                if email == list_onemail[x]:
                                    result_onechat = send_messageToChat(msg_sender,list_onemail[x])
                                else :
                                    result_onechat = send_messageToChat(msg_general,list_onemail[x])
                        # return jsonify({'result':'OK','messageText':result['messageText'],'status_Code':200,'messageER':None}),200
                        result_status = {
                            'status_insert': 'OK',
                            'status_send_chat': 'OK',
                            'ppl_id': sidCode,
                            'comment': comment
                        }
                        List_result.append(result_status)
                    else:
                        pass
                        result_status = {
                            'status_insert': 'OK',
                            'status_send_chat': 'ER',
                            'ppl_id': sidCode,
                            'comment': comment
                        }
                        List_result.append(result_status)
                        # return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result['messageText']}),200                
                    # return jsonify({'result':'OK','messageText':result['messageText'],'status_Code':200,'messageER':None}),200
                else:
                    pass
                    result_status = {
                        'status_insert': 'ER',
                        'status_send_chat': 'ER',
                        'ppl_id': sidCode,
                        'comment': comment[x]
                    }
                    List_result.append(result_status)
                    # return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result['messageText']}),200
            return jsonify({'result':'OK','messageText':List_result,'status_Code':200,'messageER':None}),200

        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404
    elif request.method == 'GET':
        result_getComment = select().select_getComment(request.args.get('sidCode'))
        if result_getComment['result'] == 'OK':
            return jsonify({'result':'OK','messageText':result_getComment['messageText'],'status_Code':200,'messageER':None}),200
        else:
            return jsonify({'result':'OK','messageText':[],'status_Code':200,'messageER':result_getComment['messageText']}),200
    elif request.method == 'PUT':
        dataJson = request.json
        if 'sidCode' in dataJson and 'email' in dataJson and 'id' in dataJson and 'comment' in dataJson and 'step' in dataJson:
            sidCode = dataJson['sidCode']
            email = dataJson['email']
            tmp_id = dataJson['id']
            comment = dataJson['comment']
            step = dataJson['step']
            result = update().update_messageComment_v2(sidCode,email,tmp_id,comment,step)

            if result['result'] == 'OK':
                if result['dict_comment'] != None:
                    list_onemail = []
                    list_resultOnechat = []
                    dict_comment = result['dict_comment']
                    msg_general = dict_comment['msg_general']
                    msg_sender = dict_comment['msg_sender']
                    list_onemail = dict_comment['list_onemail']
                    st1 = datetime.datetime.now()
                    for x in range(len(list_onemail)):
                        get_idBot = search_frd(list_onemail[x],'')
                        if get_idBot != None:
                            # get_idBot_eval = eval(str(get_idBot))
                            # fri = eval(str(get_idBot_eval['friend']))
                            # id_onechat = fri['user_id']
                            if email == list_onemail[x]:
                                result_onechat = send_messageToChat(msg_sender,list_onemail[x])
                            else :
                                result_onechat = send_messageToChat(msg_general,list_onemail[x])
                    return jsonify({'result':'OK','messageText':result['messageText'],'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result['messageText']}),200

                return jsonify({'result':'OK','messageText':result['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404

@status_methods.route('/webhook/v1',methods=['POST'])
def webHook_v1():
    tmp_id = request.args.get('id')
    logger.info(tmp_id)
    dataJson = request.json
    print(dataJson)
    # print(documentid)
    return jsonify({'result':'OK'})

@status_methods.route('/getcookie/v1',methods=['GET'])
def getcookie():
    head_referer = request.headers.get("Host")
    ts = time.time()
    ts = str(ts).split('.')[0]
    lettersAndDigits = string.ascii_letters + string.digits
    string_random = ''.join(random.choice(lettersAndDigits) for i in range(36)) + ts
    return string_random

# r = select_5().insert_userprofile_v1('jirayuknot55@thai.com')
# print(r)
@status_methods.route('/api/addfriendmulti/v1',methods=['POST'])
@token_required
def addbottofrd_chat():
    if request.method == 'POST':
        dataJson = request.json
        arr_result = []
        if 'email' in dataJson and len(dataJson) == 1:
            email = dataJson['email']
            resultAddBot = addbot_tofrdAUto(email)
            if 'status' in resultAddBot:
                if resultAddBot['status'] == 'success':
                    return jsonify({'result':'OK','messageText':resultAddBot,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':resultAddBot,'status_Code':200}),200
            elif 'result' in resultAddBot:
                if resultAddBot['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':resultAddBot,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':resultAddBot,'status_Code':200}),200

@status_methods.route('/api/geturl/v1',methods=['POST'])
@token_required
def getUrl_api():
    if request.method == 'POST':
        dataJson = request.json
        arr_result = []
        if 'email' in dataJson and 'sidCode' in dataJson and len(dataJson) == 2:
            for i in dataJson['email']:
                emailUser = dataJson['email']
                result_Url = select().select_geturl(i,dataJson['sidCode'])
                if result_Url['result'] == 'OK':
                    arr_result.append({'email':i,'urlSign':result_Url['messageText']})
                else:
                    if result_Url['messageText'] == "sid Not Found!":
                        return jsonify({'result':'ER','messageText':'sid Not Found!','status_Code':200}),200
                    else:
                        arr_result.append({'email':i,'urlSign':result_Url['messageText']})
            return jsonify({'result':'OK','messageText':arr_result,'status_Code':200}),200

@status_methods.route('/api/rejectdoc/v1',methods=['POST'])
# @token_required
def delete_Document_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'username' in dataJson and 'emailUser' in dataJson and 'sid' in dataJson and 'type' in dataJson and len(dataJson) == 4:
            username = dataJson['username']
            email_User = dataJson['emailUser']
            sidCode = dataJson['sid']
            type_status = str(dataJson['type']).lower()
            if type_status == 'reject':
                resupdate = update().update_statusDoc(username,email_User,sidCode,type_status)
                if resupdate['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':resupdate['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':resupdate['messageText'],'status_Code':200}),200
            elif type_status == 'active':
                resupdate = update().update_statusDoc(username,email_User,sidCode,type_status)
                if resupdate['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':resupdate['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':resupdate['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'type incorrect!','status_Code':404}),404
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect!','status_Code':404}),404

@status_methods.route('/api/v1/document/trash',methods=['GET'])
@token_required_v3
def trash():
    limit = ''
    offset = ''
    type_ = 'view'
    key = None
    if request.method == 'GET':
        if request.args.get('email_user') != None and request.args.get('limit') != None and request.args.get('offset') != None:
            email_user = request.args.get('email_user')
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            result_log = select_1().select_trash_recipient(email_user,limit,offset,type_,key)
            if result_log['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200
        elif request.args.get('email_user') != None and request.args.get('limit') == None and request.args.get('offset') == None:
            email_user = request.args.get('email_user')
            result_log = select_1().select_trash_recipient(email_user,limit,offset,type_,key)
            if result_log['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200

@status_methods.route('/api/v1/document/trash/count',methods=['GET'])
@token_required_v3
def trash_count():
    if request.method == 'GET':
        if request.args.get('email_user') != None:
            email_user = request.args.get('email_user')
            result_log = select_1().select_trash_log_count(email_user)
            if result_log['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'=ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200

@status_methods.route('/api/v1/search/doctype/trash',methods=['GET'])
@token_required_v3
def search_trash():
    limit = ''
    offset = ''
    doc_type = ''
    type_ = 'search_doctype'
    if request.method == 'GET':
        if request.args.get('email_user') != None and request.args.get('limit') != None and request.args.get('offset') != None and \
            request.args.get('doc_type') != None:
            email_user = request.args.get('email_user')
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            doc_type =  request.args.get('doc_type')
            result_log = select_1().select_trash_recipient(email_user,limit,offset,type_,doc_type)
            if result_log['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200
        elif request.args.get('email_user') != None and request.args.get('limit') == None and request.args.get('offset') == None and \
            request.args.get('doc_type') != None:
            email_user = request.args.get('email_user')
            doc_type =  request.args.get('doc_type')
            result_log = select_1().select_trash_recipient(email_user,limit,offset,type_,doc_type)
            if result_log['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200

@status_methods.route('/api/v1/search/doctype/trash/count',methods=['GET'])
@token_required_v3
def search_trash_count():
    limit = ''
    offset = ''
    doc_type = ''
    type_ = 'search_doctype'
    if request.method == 'GET':
        if request.args.get('email_user') != None and request.args.get('doc_type') != None:
            email_user = request.args.get('email_user')
            doc_type =  request.args.get('doc_type')
            result_log = select_1().select_trash_recipient_count(email_user,limit,offset,type_,doc_type)
            if result_log['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200

@status_methods.route('/api/v1/search/document/trash',methods=['GET'])
@token_required_v3
def search_trash_doc():
    limit = ''
    offset = ''
    keyword = ''
    type_ = 'search_document'
    if request.method == 'GET':
        if request.args.get('email_user') != None and request.args.get('limit') != None and request.args.get('offset') != None and \
            request.args.get('keyword') != None:
            email_user = request.args.get('email_user')
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            keyword =  request.args.get('keyword')
            result_log = select_1().select_trash_recipient(email_user,limit,offset,type_,keyword)
            if result_log['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200
        elif request.args.get('email_user') != None and request.args.get('limit') == None and request.args.get('offset') == None and \
            request.args.get('keyword') != None:
            email_user = request.args.get('email_user')
            keyword =  request.args.get('keyword')
            result_log = select_1().select_trash_recipient(email_user,limit,offset,type_,keyword)
            if result_log['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200

@status_methods.route('/api/v1/search/document/trash/count',methods=['GET'])
@token_required_v3
def search_trash_count_document():
    limit = ''
    offset = ''
    doc_type = ''
    type_ = 'search_document'
    if request.method == 'GET':
        if request.args.get('email_user') != None and request.args.get('doc_type') != None:
            email_user = request.args.get('email_user')
            doc_type =  request.args.get('doc_type')
            result_log = select_1().select_trash_recipient_count(email_user,limit,offset,type_,doc_type)
            if result_log['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200

@status_methods.route('/api/v1/document_type/trash',methods=['GET'])
@token_required_v3
def search_trash_doctype():
    limit = ''
    offset = ''
    doc_type = ''
    type_ = 'select_documentType'
    if request.method == 'GET':
        if request.args.get('email_user') != None:
            email_user = request.args.get('email_user')
            result_log = select_1().select_docType(email_user)
            if result_log['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200

@status_methods.route('/api/v1/activity/log',methods=['GET'])
def select_activity_log_api_v1():
    if request.method == 'GET':
        if request.args.get('email_user') != None and request.args.get('offset') != None and request.args.get('limit') != None:
            if request.args.get('email_user') != "" and request.args.get('offset') != "" and request.args.get('limit') != "":
                email_user = request.args.get('email_user')
                offsets = request.args.get('offset')
                limits = request.args.get('limit')
                result_log = select_1().select_activity_v2(email_user,offsets,limits)
                if result_log['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(404)

@status_methods.route('/api/v1/activity/log/one',methods=['GET'])
def select_activity_one_api_v1():
    if request.method == 'GET':
        if request.args.get('email_user') != None and request.args.get('log_id') != None:
            if request.args.get('email_user') != "" and request.args.get('log_id') != "":
                email_user = request.args.get('email_user')
                log_id = request.args.get('log_id')
                result_log = select_1().select_activity_one(email_user,log_id)
                if result_log['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(404)

@status_methods.route('/api/v1/activity/count',methods=['GET'])
@token_required_v3
def select_activity_count():
    if request.method == 'GET':
        if request.args.get('email_user') != None:
            email_user = request.args.get('email_user')
            result_log = select_1().select_activity_count(email_user)
            if result_log['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter email null'}),404
    else:
        abort(404)

@status_methods.route('/api/v2/rejectdoc',methods=['POST'])
# @token_required
def reject_document_api_v2():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                abort(401)
        except KeyError as ex:
            abort(401)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                abort(401)
        except Exception as e:
            abort(401)
        dataJson = request.json
        if 'username' in dataJson and 'emailUser' in dataJson and 'sid' in dataJson and 'type' in dataJson and len(dataJson) == 4:
            tmplanguage = 'th'
            username = dataJson['username']
            email_User = dataJson['emailUser']
            sidCode = dataJson['sid']
            type_status = str(dataJson['type']).lower()
            token_chat_bot = token_service
            id_chat_bot = bot_id
            if type_status == 'reject':
                query_group_id = select_1().select_querygroup_id_document_v1(sidCode)
                if query_group_id['result'] == 'OK':
                    if 'group_id' in query_group_id['messageText']:
                        delete_1().del_group_from_document_v1(sidCode,query_group_id['messageText']['group_id'],email_User)
                result_message = select_4().select_chat_sender_v1(sidCode)
                query_detail_document = select().select_data_for_chat_v1(sidCode)
                if result_message['result'] == 'OK':
                    tmp_data = result_message['messageText']
                    tmp_get_message = result_message['data']
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
                if query_detail_document['result'] == 'OK':
                    tmp_data_detail = query_detail_document['messageText']
                    print(tmp_data_detail)
                    tmp_document_id = tmp_data_detail['document_id']
                    tmp_sender_name = tmp_data_detail['sender_name']
                    tmp_sender_name_eng = tmp_data_detail['sender_name_eng']
                    tmp_email_sender = tmp_data_detail['sender_email']
                    tmp_body_text = tmp_data_detail['body_text']
                    tmpfid = tmp_data_detail['fid']
                    for zz in range(len(tmp_body_text)):
                        if zz == 0:
                            if str(tmp_body_text[zz]).replace(' ','') == '':
                                tmp_body_text[zz] = tmp_document_id
                        elif zz == 1:
                            if str(tmp_body_text[zz]).replace(' ','') == '':
                                if tmplanguage == 'th':
                                    tmp_body_text[zz] = 'โดย ' + tmp_sender_name
                                elif tmplanguage == 'eng':
                                    tmp_body_text[zz] = 'By ' + tmp_sender_name_eng
                if tmplanguage == 'th':
                    text_body_tochat = 'แจ้งเตือน Paperless' + '\n'
                elif tmplanguage == 'eng':
                    text_body_tochat = 'Notification Paperless' + '\n'
                for u in tmp_body_text:
                    if tmplanguage == 'th':
                        text_body_tochat += 'เลขที่เอกสาร ' + u + '\n'
                    elif tmplanguage == 'eng':
                        text_body_tochat += 'Document No. ' + u + '\n'
                if tmplanguage == 'th':
                    text_body_tochat += '\n' + 'สถานะเอกสาร : ยกเลิกเอกสาร'
                elif tmplanguage == 'eng':                    
                    text_body_tochat += '\n' + 'Document Status : Cancel documents'
                # if query_select['result'] == 'OK':
                #     tmp_data_sendchat = query_select['messageText']
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
                        
                        tmp_status_chat = tmp_data[u]['status_Chat']
                        tmp_chat_id = tmp_data[u]['chat_id']
                        tmp_emailone = tmp_data[u]['email']
                        tmp_step_num = tmp_data[u]['step_num']
                        if True in tmp_status_chat:
                            for t in range(len(tmp_chat_id)):
                                if len(tmp_chat_id[t]) != 0:
                                    thai_email = tmp_emailone[t]
                                    chat_id = tmp_chat_id[t]
                                    disble_button_in_oneChat_v5(id_chat_bot,token_chat_bot,chat_id,token_header)
                                    try:                                        
                                        executor.submit(update().update_onechatId_v1,sidCode,thai_email,tmp_step_num,chat_id)
                                        executor.submit(call_webhookService,sidCode)
                                        result_get_userid_2 = select().select_user_id_from_email_chat_v1(thai_email)
                                        tmp_user_id_2 = result_get_userid_2['messageText']['user_id']
                                        result_send_to_sender = send_messageToChat_v4(text_body_tochat,tmp_user_id_2,token_chat_bot,id_chat_bot,token_header)
                                    except Exception as e:
                                        pass
                try:
                    result_get_userid_2 = select().select_user_id_from_email_chat_v1(tmp_email_sender)
                    tmp_user_id_2 = result_get_userid_2['messageText']['user_id']
                    result_send_to_sender = send_messageToChat_v4(text_body_tochat,tmp_user_id_2,token_chat_bot,id_chat_bot,token_header)
                except Exception as e:
                    pass   
                # executor.submit(watermark_cancel_v1(email_User,sidCode,username,tmpfid))
                resupdate = update_4().update_status_document_v4(username,email_User,sidCode,type_status)
                if resupdate['result'] == 'OK':
                    executor.submit(select_2().rejectdoc_to_eform,sidCode,token_header)
                    return jsonify({'result':'OK','messageText':resupdate['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':resupdate['messageText'],'status_Code':200}),200
            elif type_status == 'active':
                resupdate = update().update_status_document_v2(username,email_User,sidCode,type_status)
                if resupdate['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':resupdate['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':resupdate['messageText'],'status_Code':200}),200
            elif type_status == 'delete':
                token_chat_bot = token_service
                id_chat_bot = bot_id
                resupdate = delete_1().delete_tash(username,email_User,sidCode)
                if resupdate['result'] == 'OK':
                    result_message = select().select_chat_sender_v1(sidCode)
                    list_onemail =  resupdate['messageText'][0]['list_onemail']
                    msg = resupdate['messageText'][0]['msg']
                    tmp_data = result_message['messageText']
                    for u in range(len(tmp_data)):
                        tmp_chat_id = tmp_data[u]['chat_id']
                        tmp_status_ppl = tmp_data[u]['status_ppl']
                        for z in range(len(tmp_chat_id)):
                            tmp_id_chat_one_dis = tmp_chat_id[z]
                            executor.submit(disble_button_in_oneChat_v4,id_chat_bot,token_chat_bot,tmp_id_chat_one_dis,token_header)

                    for x in range(len(list_onemail)):
                        result_onechat = send_messageToChat(msg,list_onemail[x])
                    tmp_data = result_message['messageText']
                    
                    return jsonify({'result':'OK','messageText':resupdate['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':resupdate['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'type incorrect!','status_Code':404}),404
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect!','status_Code':404}),404


@status_methods.route('/api/statusdoc/v1',methods=['POST'])
def status_Document_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'sid' in dataJson and 'type' in dataJson and len(dataJson) == 2:
            sidCode = dataJson['sid']
            type_status = str(dataJson['type']).lower()
            if type_status == 'reject':
                resultUpdate = update().update_statusDoc_v1(sidCode,type_status)
                if resultUpdate['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':resultUpdate['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':resultUpdate['messageText'],'status_Code':200}),200
            elif type_status == 'active':
                resultUpdate = update().update_statusDoc_v1(sidCode,type_status)
                if resultUpdate['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':resultUpdate['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':resultUpdate['messageText'],'status_Code':200}),200
            elif type_status == 'cancel':
                resultUpdate = update().update_statusDoc_v1(sidCode,type_status)
                if resultUpdate['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':resultUpdate['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':resultUpdate['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'type incorrect!','status_Code':404}),404
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect!','status_Code':404}),404

@status_methods.route('/api/v1/test/watermark',methods=['POST'])
# @token_required
def create_watermark():
    if request.method == 'POST':
        try:
            path = './storage/watermark/data/'
            if not os.path.exists(path):
                os.makedirs(path)
            pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf')) # ดึงไฟล์ THSarabunNew.ttf มาลงทะเบียนฟอนต์ในโค้ด
            c = canvas.Canvas(path + "simple_demo.pdf") # ไฟล์ที่จะเขียน
            c.setFont("THSarabunNew", 30) # กำหนดฟอนต์ที่ใช้ และขนาดคือ 30
            username = 'เอกสารถูกยกเลิกโดย ' + 'jirayuknot55'
            c.setFillColor('red',0.35)
            c.saveState()
            c.translate(500,100)
            c.rotate(45)
            c.drawCentredString(0,0,username)
            c.drawCentredString(50,450,username)
            c.drawCentredString(50,150,username)
            c.drawCentredString(0,300,username)
            c.drawCentredString(0,600,username)
            c.restoreState()
            c.save()
            return 'Success'
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/genqrcode_transfer/v1',methods=['POST'])
@token_required
def genqrcode_transfer_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'sidCode' in dataJson and 'string_pdf' in dataJson and len(dataJson) == 2:
            sidCode_data = dataJson['sidCode']
            string_PDF = dataJson['string_pdf']
            resultSelect  = select().select_forqrCodeSign_public_v1(sidCode_data)
            if resultSelect['result'] == 'OK':
                sha512encode = hashlib.sha512(str(resultSelect['emailUser']).encode('utf-8')).hexdigest()
                sha512encode_sidCode = hashlib.sha512(str(sidCode_data).encode('utf-8')).hexdigest()
                url_qrCodePublicSign = url_paperless + 'pdfsignpublic?emailuser=' + sha512encode + '&fid=' + sha512encode_sidCode
                sign_Position = eval(str(resultSelect['sign_Position']))
                qr_llx = float(sign_Position['qr_llx'])
                qr_lly = float(sign_Position['qr_lly'])
                qr_urx = float(sign_Position['qr_urx'])
                qr_ury = float(sign_Position['qr_ury'])
                qr_page = int(sign_Position['qr_page'])
                stringQrCode = genarateQrcode_public(url_qrCodePublicSign)
                pathPDF_QrCode = genPdf_Topng_qr_pulic(qr_urx,qr_ury,qr_llx,qr_lly,stringQrCode)
                if pathPDF_QrCode['result'] == 'OK':
                    resultMerge = merge_png_to_pdf_qrCode_public(qr_page,string_PDF,pathPDF_QrCode['messageText'])
                    if resultMerge['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':resultMerge['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':resultMerge['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':pathPDF_QrCode['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'sidCode not found','status_Code':200}),200

@status_methods.route('/api/textgenpng/v1',methods=['POST'])
def genpng_imagesformtext():
    if request.method == 'POST':
        dataJson = request.json
        if 'pdf_string' in dataJson and 'text_string' in dataJson and len(dataJson) == 2:
            gentext_topng()
            return jsonify({})

@status_methods.route('/api/status/v1/<string:username>/<string:emailUser>',methods=['GET'])
@token_required
def statusReader_v1(username,emailUser):
    try:
        resultSelectView = select().select_statusView_v1(username,emailUser)
        if resultSelectView['result'] == 'OK':
            return jsonify({'result':'OK','messageText':resultSelectView['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':resultSelectView['messageText'],'status_Code':200}),200
    except Exception as ex:
        return jsonify({'result':'ER','messageText':None,'status_Code':200}),200

@status_methods.route('/public/view/pdf/v1',methods=['POST'])
def public_PDF_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'pdf_sidCode' in dataJson:
            sidCode_hash = dataJson['pdf_sidCode']
            result_base64 = select().select_public_pdfview_v1(sidCode_hash)
            if result_base64['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_base64['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_base64['messageER']}),200

@status_methods.route('/public/v2/view/pdf',methods=['POST'])
def public_view_pdf_v2():
    if request.method == 'POST':
        dataJson = request.json
        if 'pdf_sidCode' in dataJson:
            sidCode_hash = dataJson['pdf_sidCode']
            result_base64 = select().select_public_pdfview_v2(sidCode_hash)
            if result_base64['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_base64['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_base64['messageER']}),200

@status_methods.route('/public/viewimage/<string:image_nameFile>',methods=['GET'])
def public_viewimage_jpg(image_nameFile):
    path_image = path_global_1 + '/storage/image/' + image_nameFile
    if os.path.isfile(path_image):
        return send_file(path_image, mimetype='image/jpeg')
    else:
        path_image = './storage/image/' + image_nameFile
        # path_image = os.getcwd() + './storage/image/' + image_nameFile
        return send_file(path_image, mimetype='image/jpeg')

@status_methods.route('/api/view2/pdf_image/<string:foldername>/<string:filename>',methods=['GET'])
def public_viewimage_jpg_v1(foldername,filename):
    path_image = path_global_1 + '/storage/image/' + foldername + '/' + filename
    if os.path.exists(path_image):
        return send_file(path_image, mimetype='image/jpeg')
    else:
        path_image = os.getcwd() + '/storage/image/' + foldername + '/' + filename
        return send_file(path_image, mimetype='image/jpeg')
    # return send_file(path_image, mimetype='image/jpeg')

def convert_pdf_image_v1(foldername,base64pdf):
    # dataJson = request.json
    resul_res = {}
    list_file_name = []
    base64_pdfFile = base64pdf
    path = path_global_1 + '/storage/pdf/' + foldername
    # path = './storage/pdf/' + foldername
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        for the_file in os.listdir(path):
            file_path = os.path.join(path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200
    except Exception as e:
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200
    path_image = path_global_1 + '/storage/image/' + foldername
    if not os.path.exists(path_image):
        os.makedirs(path_image)
    try:
        for the_file in os.listdir(path_image):
            file_path = os.path.join(path_image, the_file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    # os.unlink(file_path)
            except Exception as e:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200
    except Exception as e:
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200

    try:
        unique_filename = str(uuid.uuid4())
        with open(path +'/'+ unique_filename +".pdf","wb") as f:
            f.write(base64.b64decode((base64_pdfFile)))
    except Exception as e:
        print(str(e))
    address_file = path + '/' + unique_filename + '.pdf'
    countpages = 0
    images = convert_from_bytes(open(address_file,'rb').read())
    for i, image in enumerate(images):
        countpages = countpages + 1
    try:
        maxPages = pdf2image._page_count(address_file)
    except Exception as e:
        maxPages = countpages
    print(maxPages)
    if maxPages != 1:
        # for page in range(1,maxPages,1):
            # print(page)
        pages = convert_from_path(address_file, dpi=200, fmt='jpeg',output_folder=path_image)
        for u in range(len(pages)):
            print(pages[u].filename)
            filename_only = str(pages[u].filename).split('/')[-1]
            try:
                url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                with open(pages[u].filename, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    encoded_string = (encoded_string).decode('utf8')
                # list_file_name.append({'image_Base64': str(encoded_string), 'image_Url': url_view_image})
                list_file_name.append({'image_Url': url_view_image})
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(ex)}),200
        return jsonify({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200
    else:
        pages = convert_from_path(address_file, dpi=200, first_page=0,fmt='jpeg', last_page = 1,output_folder=path_image)
        for u in range(len(pages)):
            print(pages[u].filename)
            filename_only = str(pages[u].filename).split('/')[-1]
            try:
                url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                with open(pages[u].filename, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    encoded_string = (encoded_string).decode('utf8')
                # list_file_name.append({'image_Base64': str(encoded_string), 'image_Url': url_view_image})
                list_file_name.append({'image_Url': url_view_image})
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(ex)}),200
        return jsonify({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200

@status_methods.route('/api/v1/delsign',methods=['PUT'])
def delsign_api_v1():
    if request.method == 'PUT':
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        dataJson = request.json
        if 'sid' in dataJson and 'email' in dataJson and 'step' in dataJson and 'email_step' in dataJson and len(dataJson) == 4 :
            sid = dataJson['sid']
            email = dataJson['email']
            step = dataJson['step']
            email_step = dataJson['email_step']
            token_chat_bot = token_service
            id_chat_bot = bot_id
            result_message = select().select_chat_sender_v1(sid)
            result_update = update_1().update_deljson(sid,email,step,email_step)
            if result_update['result'] == 'OK':
                chat_service = chat_for_service_v1(sid,'Bearer ' + token_header)
                # print('chat_service',chat_service)
                print('result_message',result_message)
              
                if result_message['result'] == 'OK':
                    tmp_data = result_message['messageText']
                    for u in range(len(tmp_data)):
                        tmp_chat_id = tmp_data[u]['chat_id']
                        tmp_status_ppl = tmp_data[u]['status_ppl']
                        for z in range(len(tmp_chat_id)):
                            tmp_id_chat_one_dis = tmp_chat_id[z]
                            disble_button_in_oneChat_v4(id_chat_bot,token_chat_bot,tmp_id_chat_one_dis,token_header)

                return jsonify({'result':'OK','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200
            else :
                return jsonify({'result':'ER','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200

            # print('1234')
           
        else :
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

@status_methods.route('/api/v1/addsign',methods=['PUT'])
def addsign_api_v():
    if request.method == 'PUT':
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        dataJson = request.json
        if 'sid' in dataJson and 'email' in dataJson and 'step' in dataJson and 'email_step' in dataJson and len(dataJson) == 4 :
            sid = dataJson['sid']
            email = dataJson['email']
            step = dataJson['step']
            email_step = dataJson['email_step']
            result_update = update_1().update_json(sid,email,step,email_step)
            if result_update['result'] == 'OK':
                chat_service = chat_for_service_v1(sid,'Bearer ' + token_header)
                print('chat_service',chat_service)
                return jsonify({'result':'OK','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200
            else :
                return jsonify({'result':'ER','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200

            # print('1234')
           
        else :
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

@status_methods.route('/api/v1/log/tranfer',methods=['GET'])
@token_required_v3
def tranferlog():
    if request.method == 'GET':
        if request.args.get('sid') != None:
            sid = request.args.get('sid')
            result_log = select_1().select_tranferlog(sid)
            if result_log['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'OK','messageText':result_log['messageText'],'status_Code':200,'messageER':result_log['messageER']}),200

@status_methods.route('/api/v1/tranfersign',methods=['PUT'])
@token_required_v3
def tranfersign_api_v():
    if request.method == 'PUT':
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                abort(401)
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                abort(401)
        except Exception as e:
                abort(401)
        dataJson = request.json
        if 'sid' in dataJson and 'email' in dataJson and 'step' in dataJson and 'email_to' in dataJson and len(dataJson) == 4 :
            sid = dataJson['sid']
            email = dataJson['email']
            step = dataJson['step']
            email_to = dataJson['email_to']
            token_chat_bot = token_service
            id_chat_bot = bot_id
            result_message = select().select_chat_sender_v1(sid)
            result_update = update_1().update_tranfer_sign(sid,email,step,email_to)
            if result_update['result'] == 'OK':
                chat_service = chat_for_service_v1(sid,'Bearer ' + token_header)
                # print('chat_service',chat_service)
                if result_message['result'] == 'OK':
                    tmp_data = result_message['messageText']
                    for u in range(len(tmp_data)):
                        tmp_chat_id = tmp_data[u]['chat_id']
                        tmp_status_ppl = tmp_data[u]['status_ppl']
                        for z in range(len(tmp_chat_id)):
                            tmp_id_chat_one_dis = tmp_chat_id[z]
                            disble_button_in_oneChat_v4(id_chat_bot,token_chat_bot,tmp_id_chat_one_dis,token_header)

                return jsonify({'result':'OK','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200
            else :
                return jsonify({'result':'ER','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200
        else :
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

@status_methods.route('/api/v1/convert/pdftopdf',methods=['POST'])
def pdftopdf_api_v1():
    dataJson = request.json
    namefile = str(uuid.uuid4())
    if 'pdfData' in dataJson:
        pdfData = dataJson['pdfData']
        try:
            output_file = path_global_1 + '/temp/' + namefile + '.pdf'
            with io.BytesIO(base64.b64decode(pdfData)) as open_pdf_file:
                read_pdf = PdfFileReader(open_pdf_file)
                num_pages = read_pdf.getNumPages()
                pdf_writer = PdfFileWriter()
                for i in range(num_pages):
                    pdf_writer.addPage(read_pdf.getPage(i))
                with open(output_file, 'wb') as fh:
                    pdf_writer.write(fh)
            with open(output_file, "rb") as f:
                encodedZip = base64.b64encode(f.read())
                basefiledata = (encodedZip.decode())
            os.remove(output_file)
        except Exception as e:
            print(str(e))
            basefiledata = pdfData
            return jsonify({'status':'fail','message':'cont covert pdf','data':None}),200
        return jsonify({'status':'success','message':'covert success','data':basefiledata}),200

@status_methods.route('/api/convert2/pdf_image/<string:foldername>',methods=['POST','GET'])
def api_convert_v1(foldername):
    if request.method == 'POST':
        dataJson = request.json
        resul_res = {}
        list_file_name = []
        if 'base64_PDF' in dataJson:
            base64_pdfFile = dataJson['base64_PDF']
            path = path_global_1+'/storage/pdf/' + foldername
            if not os.path.exists(path):
                os.makedirs(path)
            try:
                for the_file in os.listdir(path):
                    file_path = os.path.join(path, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200
            except Exception as e:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200
            path_image = path_global_1 + '/storage/image/' + foldername
            if not os.path.exists(path_image):
                os.makedirs(path_image)
            try:
                for the_file in os.listdir(path_image):
                    file_path = os.path.join(path_image, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            # os.unlink(file_path)
                    except Exception as e:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200
            except Exception as e:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200

            try:
                unique_filename = str(uuid.uuid4())
                with open(path +'/'+ unique_filename +".pdf","wb") as f:
                    f.write(base64.b64decode((base64_pdfFile)))
            except Exception as e:
                print(str(e))
            address_file = path + '/' + unique_filename + '.pdf'
            countpages = 0
            pages = convert_from_path(address_file, dpi=200, fmt='jpeg',output_folder=path_image,thread_count=1)
            for u in range(len(pages)):
                print(pages[u].filename)
                filename_only = str(pages[u].filename).split('/')[-1]
                try:
                    url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                    with open(pages[u].filename, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                        encoded_string = (encoded_string).decode('utf8')
                    # list_file_name.append({'image_Base64': str(encoded_string), 'image_Url': url_view_image})
                    list_file_name.append({'image_Url': url_view_image})
                except Exception as ex:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(ex)}),200
            return jsonify({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200

            if maxPages != 1:
                # for page in range(1,maxPages,1):
                    # print(page)
                pages = convert_from_path(address_file, dpi=200, fmt='jpeg',output_folder=path_image,thread_count=1)
                for u in range(len(pages)):
                    print(pages[u].filename)
                    filename_only = str(pages[u].filename).split('/')[-1]
                    try:
                        url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                        with open(pages[u].filename, "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read())
                            encoded_string = (encoded_string).decode('utf8')
                        # list_file_name.append({'image_Base64': str(encoded_string), 'image_Url': url_view_image})
                        list_file_name.append({'image_Url': url_view_image})
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(ex)}),200
                return jsonify({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200
            else:
                pages = convert_from_path(address_file, dpi=200, first_page=0,fmt='jpeg', last_page = 1,output_folder=path_image,thread_count=1)
                for u in range(len(pages)):
                    print(pages[u].filename)
                    filename_only = str(pages[u].filename).split('/')[-1]
                    try:
                        url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                        with open(pages[u].filename, "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read())
                            encoded_string = (encoded_string).decode('utf8')
                        # list_file_name.append({'image_Base64': str(encoded_string), 'image_Url': url_view_image})
                        list_file_name.append({'image_Url': url_view_image})
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(ex)}),200
                return jsonify({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200
    elif request.method == 'GET':
        list_file_name = []
        # path_image = os.getcwd() + '/storage/image/' + foldername
        path_image = path_global_1 + '/storage/image/' + foldername
        try:
            for the_file in sorted(os.listdir(path_image)):
                file_path = os.path.join(path_image, the_file)
                # print(file_path)
                filename_only = str(file_path).split('/')[-1]
                url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                list_file_name.append({'image_Url': url_view_image})
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200
        return jsonify({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200

@status_methods.route('/api/v1/convert/pdf_image/<string:foldername>',methods=['POST','GET'])
def convert_pdf_images_api_v1(foldername):
    if request.method == 'POST':
        dataJson = request.json
        resul_res = {}
        list_file_name = []
        if 'base64_PDF' in dataJson:
            base64_pdfFile = dataJson['base64_PDF']
            list_dataresult = []
            url = '/api/v1/convert/pdf_image/'
            list_dataresult = []
            result_insert = insert_3().insert_process_request_v1('CONVERT',str(list_dataresult),url,None,None)
            tmpid_process = None
            if result_insert['result'] == 'OK':
                tmpid_process = result_insert['messageText']['id']
            # print(tmpid_process)
            executor.submit(convert_pdf_images,foldername,base64_pdfFile,tmpid_process)
            return jsonify({'result':'OK','messageText':{'message':'on process','data':tmpid_process},'messageER':None,'status_Code':200}),200
            
    elif request.method == 'GET':
        list_file_name = []
        # path_image = os.getcwd() + '/storage/image/' + foldername
        path_image = path_global_1 + '/storage/image/' + foldername
        try:
            for the_file in os.listdir(path_image):
                file_path = os.path.join(path_image, the_file)
                print(file_path)
                filename_only = str(file_path).split('/')[-1]
                url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                list_file_name.append({'image_Url': url_view_image})
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200
        return jsonify({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200


@status_methods.route('/api/v1/group/pdf_image/<string:foldername>',methods=['POST','GET'])
def pdf_image_group_api_v1(foldername):
    if request.method == 'POST':
        dataJson = request.json
        resul_res = {}
        list_file_name = []
        if 'base64_PDF' in dataJson:
            base64_pdfFile = dataJson['base64_PDF']
            path = path_global_1 + '/storage/pdf/' + foldername
            if not os.path.exists(path):
                os.makedirs(path)
            try:
                for the_file in os.listdir(path):
                    file_path = os.path.join(path, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200
            except Exception as e:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200
            path_image = path_global_1 + '/storage/image/' + foldername
            if not os.path.exists(path_image):
                os.makedirs(path_image)
            try:
                for the_file in os.listdir(path_image):
                    file_path = os.path.join(path_image, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            # os.unlink(file_path)
                    except Exception as e:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200
            except Exception as e:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200

            try:
                unique_filename = str(uuid.uuid4())
                with open(path +'/'+ unique_filename +".pdf","wb") as f:
                    f.write(base64.b64decode((base64_pdfFile)))
            except Exception as e:
                print(str(e))
            address_file = path + '/' + unique_filename + '.pdf'
            countpages = 0
            images = convert_from_bytes(open(address_file,'rb').read())
            for i, image in enumerate(images):
                countpages = countpages + 1
            try:
                maxPages = pdf2image._page_count(address_file)
            except Exception as e:
                maxPages = countpages
            print(maxPages)
            if maxPages != 1:
                # for page in range(1,maxPages,1):
                    # print(page)
                pages = convert_from_path(address_file, dpi=200, fmt='jpeg',output_folder=path_image)
                for u in range(len(pages)):
                    print(pages[u].filename)
                    filename_only = str(pages[u].filename).split('/')[-1]
                    try:
                        url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                        with open(pages[u].filename, "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read())
                            encoded_string = (encoded_string).decode('utf8')
                        # list_file_name.append({'image_Base64': str(encoded_string), 'image_Url': url_view_image})
                        list_file_name.append({'image_Url': url_view_image})
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(ex)}),200
                return jsonify({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200
            else:
                pages = convert_from_path(address_file, dpi=200, first_page=0,fmt='jpeg', last_page = 1,output_folder=path_image)
                for u in range(len(pages)):
                    print(pages[u].filename)
                    filename_only = str(pages[u].filename).split('/')[-1]
                    try:
                        url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                        with open(pages[u].filename, "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read())
                            encoded_string = (encoded_string).decode('utf8')
                        # list_file_name.append({'image_Base64': str(encoded_string), 'image_Url': url_view_image})
                        list_file_name.append({'image_Url': url_view_image})
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(ex)}),200
                return jsonify({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200
    elif request.method == 'GET':
        list_file_name = []
        # path_image = os.getcwd() + '/storage/image/' + foldername
        path_image = path_global_1 + '/storage/image/' + foldername
        try:
            for the_file in os.listdir(path_image):
                file_path = os.path.join(path_image, the_file)
                print(file_path)
                filename_only = str(file_path).split('/')[-1]
                url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                list_file_name.append({'image_Url': url_view_image})
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200
        return jsonify({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200

@status_methods.route('/api/v1/get_logo/<string:tax_id>/<string:file_name>',methods=['POST','GET'])
# @token_required
def get_logo_v1(tax_id,file_name):
    if request.method == 'GET':
        list_file_name = []
        # path_image = os.getcwd() + '/logo_biz/' + tax_id
        try:
            path_image = os.getcwd() + '/logo_biz/' + tax_id +'/' + file_name
            send_file(path_image, mimetype='image/png')
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200

@status_methods.route('/convert2/pdf_image/<string:foldername>',methods=['POST'])
def convert_v1(foldername):
    maxPages = pdf2image._page_count('./gre_research_validity_data.pdf')
    for page in range(1,maxPages,10):
        pages = convert_from_path('./gre_research_validity_data.pdf', dpi=200, first_page=page,fmt='jpeg', last_page = min(page+10-1,maxPages),output_folder='./')
    for u in range(len(pages)):
        print(pages[u].filename)
    return jsonify({'result':'OK','messageText':{'url_image':None,'name_image':None},'status_Code':200,'messageER':None}),200

@status_methods.route('/ftps/v1',methods=['POST'])
def ftps_fucname_v1():
    SERVER = '203.150.197.76'
    USER = 'ftp_user'
    PASS = 'F9wxw,jwfhovo'
    PORT = 22
    pdf_path = 'SiamPiwat_Cloud 1 vm วันสยาม.pdf'
    try:
        import pysftp
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(SERVER, username=USER, password=PASS,cnopts=cnopts) as sftp:
            with sftp.cd('/Create'):
                print(sftp.put('./SiamPiwat_Cloud 1 vm วันสยาม.pdf'))
        # client = SftpClient(SERVER,PORT,USER,PASS)
        # client.upload(pdf_path,'/Create')
        return ''
    except Exception as e:
        print(e)

@status_methods.route('/api/v1/jpg_png',methods=['POST'])
def jpg_png_v1():
    import base64
    from PIL import Image
    from io import BytesIO
    dataJson = request.json
    if 'jpgData' in dataJson:
        data = dataJson['jpgData']
        folder_name = str(uuid.uuid4())
        file_name = str(uuid.uuid4())
        path = './temp/' + folder_name  
        if not os.path.exists(path):
            os.makedirs(path)
        path_file = path + '/' + file_name + '.png'
        im = Image.open(BytesIO(base64.b64decode(data)))
        im.save(path_file, 'PNG')
        with open(path_file, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        encoded_string = encoded_string.decode('utf-8')
        os.remove(path_file)
        return jsonify({'result':'OK','messageText':{'data':encoded_string,'message':'succuess'},'status_Code':200,'messageER':None})

@status_methods.route('/api/v1/get_pdf_page',methods=['POST'])
def get_pdf_page_v1():
    pdf_string = './[Admin Manaual] คู่มือการจัดการ Group และ Users.pdf'
    datajson = request.json
    try:
        from PyPDF2 import PdfFileReader
        with io.BytesIO(base64.b64decode(datajson['base64'])) as open_pdf_file:
            read_pdf = PdfFileReader(open_pdf_file)
            num_pages = read_pdf.getNumPages()
            print(num_pages)
        # pdf = PdfFileReader((io.BytesIO(base64.b64decode(datajson['base64'])),'rb'))

        # print(pdf.getNumPages())
        return ''
    except Exception as e:
        print(e)

@status_methods.route('/api/v1/xls_file',methods=['POST'])
def xls_file_v1():
    import xlsxwriter
    row = 1
    col = 0
    tempeiei_ = 1
    # Create a workbook and add a worksheet.
    result_select = select().select_to_report_sum('','','QT')
    # print(result_select)
    workbook = xlsxwriter.Workbook('Expenses01.xlsx')
    worksheet = workbook.add_worksheet()
    if result_select['result'] == 'OK':
        for i in range(len(result_select['messageText'])):
            print(result_select['messageText'][i])
        # for i in range(len(result_select['messageText'])):
        #     if tempeiei_ == 40:
        #         tempeiei_ = 0
        #         merge_format = workbook.add_format({
        #             'bold': 1,
        #             'align': 'center',
        #         })

        #         worksheet.merge_range('A'+str(row) +':O'+str(row), 'รายงานสรุป QT', merge_format)
        #         row += 1
        #         # tmp_i = i
        #     else:
        #         document_id = result_select['messageText'][row]['document_id']
        #         indexid = result_select['messageText'][row]['count_index']
        #         worksheet.write(row, col,     indexid)
        #         worksheet.write(row, col+1,     document_id)
        #         row += 1
        #         tempeiei_ += 1


    # for item, cost in (expenses):
    #     worksheet.write(row, col,     item)
    #     worksheet.write(row, col + 1, cost)
    #     row += 1
    merge_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
    })
    worksheet.merge_range('A1:O1', 'รายงานสรุป QT', merge_format)
    # expenses = (
    #     ['Rent', 1000],
    #     ['Gas',   100],
    #     ['Food',  300],
    #     ['Gym',    50],
    # )

    # # Start from the first cell. Rows and columns are zero indexed.
    # row = 0
    # col = 0

    # # Iterate over the data and write it out row by row.
    # for item, cost in (expenses):
    #     worksheet.write(row, col,     item)
    #     worksheet.write(row, col + 1, cost)
    #     row += 1

    # # Write a total using a formula.
    # worksheet.write(row, 0, 'Total')
    # worksheet.write(row, 1, '=SUM(B1:B4)')

    workbook.close()
    return ''

@status_methods.route('/api/v1/sid_hash_tb_track',methods=['POST'])
def change_to_recp_v1():
    select().select_hash_sid_512()
    return ''

@status_methods.route('/api/v1/change_email_intemplate',methods=['POST'])
def change_email_intemplate_v1():
    select().select_template_and_update_v1()
    return ''

@status_methods.route('/api/v1/add_subject_text',methods=['POST'])
def add_subject_text_v1():
    select().select_file_name_to_subject_v1()
    return ''

@status_methods.route('/api/v1/get_status_recp',methods=['POST'])
def get_status_recp_v1():
    select().select_get_recp_to_insert_v1()
    return ''

@status_methods.route('/api/v1/keeplogginerr',methods=['POST'])
def keeplogginerr_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'method' in dataJson and 'text_body' in dataJson and 'url_request' in dataJson and 'status_code' in dataJson and len(dataJson) == 4:
            text_body = dataJson['text_body']
            methods_req = dataJson['method']
            status_as_string = dataJson['status_code']
            url_tmp = dataJson['url_request']
            callWebHook_slack_v1('Methods : ' + methods_req + ' HTTP Status Code : ' + str(status_as_string) + '\n' + text_body,text_body,url_tmp)
            return {'result':'OK','messageText':{'message':'succuess','data':None},'messageER':None,'status_Code':200}

@status_methods.route('/api/v1/jj')
def jj_api_v1():
    r = select().select_ForWebHook('8b884cdf-324d-4594-8740-c0253d6b47e8')
    # r = select_3().select_onebiz_transaction_v1('5513213355654')
    # r = select_3().select_deptname_onebox('d6b5cb40-831e-424d-80c8-c3b3e68bdd33')
    # sid = [
    #     "a5a58f86-39ea-49b0-aa55-978ebc0d74ab",
    #     "a5b87b7c-4603-4466-84d4-4a74680a83ae"
    # ]
    # resJson = select().select_datajson_toemail(sid)
    return jsonify(r)

@status_methods.route('/api/v1/update/pdf', methods=['PUT'])
def update_pdf_api_v1():
    if request.method == 'PUT':
        dataJson = request.json
        if 'paperless_id' in dataJson and 'File_PDF' in dataJson and 'data_document' in dataJson and len(dataJson) == 3:
            paperless_id = dataJson['paperless_id']
            File_PDF = dataJson['File_PDF']
            data_document = dataJson['data_document']
            result_update = update().update_stringpdf(paperless_id,File_PDF,data_document)
            if result_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':result_update['messageText'],'status_Code':200,'messageER':'update error'}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

@status_methods.route('/api/v2/update/pdf', methods=['PUT'])
def update_pdf_api_v2():
    if request.method == 'PUT':
        dataJson = request.json
        if 'paperless_id' in dataJson and 'File_PDF' in dataJson and 'data_document' in dataJson \
        and len(dataJson) == 3:
            paperless_id = dataJson['paperless_id']
            File_PDF = dataJson['File_PDF']
            data_jwt = dataJson['data_document']
            data_document  = data_doc(dataJson['data_document'])
            result_update = update().update_stringpdf_v2(paperless_id,File_PDF,data_document,data_jwt)
            if result_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':result_update['messageText'],'status_Code':200,'messageER':'update error'}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

@status_methods.route('/api/v1/html', methods=['GET'])
def view_html_v1():
    if request.method == 'GET':
        group_id = request.args.get('group_id')
        name_id = request.args.get('name_id')
        if group_id != None and name_id == None:
            path = path_global_1 + '/storage/html/' + group_id +'/' + group_id + '.html'
            # path = '/storage/html/' + group_id +'/' + group_id + '.html'
            with open(path,'r') as f:
                output = f.read()
            return output
        elif group_id != None and name_id != None:
            path = path_global_1 + '/storage/html/' + group_id +'/' + name_id + '.html'
            # path = './storage/html/' + group_id +'/' + name_id + '.html'
            with open(path,'r') as f:
                output = f.read()
            return output
        else:
            abort(404)

@status_methods.route("/fast")
def fast():
    return "42"

@status_methods.route('/api/v1/test',methods=['POST'])
def get_test_007():
    r = select().select_datajson_toemail(['71670f2d-8daf-47e4-90d6-c7847fb4a98e','3413c4cd-a94d-411e-9638-168be2e34aec'])
    # result_select = select().select_datajson_form_step_data_update_sender_v1('d9870311-ff5e-4fe8-ab8a-80d45e924108')
    # result_select = select().select_datajson_form_step_data_update_sender_v1('a44c9435-4c2b-4ea3-a926-4f162d822413')
    # result_select = select().select_datajson_form_step_data_update_sender_v1('2087139c-f700-4149-b435-ef6f34fc7703')
    # result_select = select().select_datajson_form_step_data_update_sender_v1('0c3c9f9e-5f32-490a-9e77-85c599a74c29')
    # result_select = select().select_datajson_form_step_data_update_sender_v1('18473548-5fb1-44ad-a04d-bb0e4fbae632')
    # result_select = select().select_datajson_form_step_data_update_sender_v1('e1017d03-f849-45d0-b4e9-8cc1634a3f64')
    # result_select = select().select_datajson_form_step_data_update_sender_v1('1ec39104-57c2-449c-82b4-66ebb303b6d9')
    # result_select = select().select_datajson_form_step_data_update_sender_v1('7dd5698a-f82d-4b78-92b1-505ce8e4e6c1')
    return jsonify(r)

@status_methods.route('/api/v2/test',methods=['POST'])
def get_test_007_v2():
    result = select_1().sleect_sid_datetimeupdate()
    return jsonify(result)

@status_methods.route('/api/v1/testtoken',methods=['POST'])
@token_required_v3
def get_testtoken_007_v2():
    # result = select_1().select_all_sid_v1()
    return ''
    # select().select_UrlSign_SidCodeEmailUser('1b027f35-e4dd-4fe4-9569-53d88e1a2315','jirayu.ko@one.th',3)
    # tmp_token = request.headers['Authorization']
    # tmp_token_01 = str(tmp_token).split(' ')[1]
    # check_and_decode_tokenoneid(tmp_token_01)
    # return ''

@status_methods.route('/api/v1/testretrun',methods=['POST'])
def testretrun():
    return {'result':'OK'}

@status_methods.route('/api/v1/testsql',methods=['POST'])
def testretrun_2():
    result = select_1().select_testsql()
    return {'result':'OK','messageText':result}

@status_methods.route('/api/v1/checkSIgnProfile',methods=['POST'])
def checkSIgnProfile():
    result = select().select_signProfile()
    return jsonify(result)

@status_methods.route('/api/v1/test_email_1',methods=['POST'])
def test_email_1():
    mail().send_email_test()
    return jsonify({'result':'OK'})

@status_methods.route('/api/v1/test_transfer',methods=['POST'])
def test_transfer_api_v1():
    # dataJson = request.json
    g_arr_list = []
    g = []
    list_tmp = []
    r = select_4().select_pdfstring_v1()
    if r['result'] == 'OK':
        r = r['data']
    for n in range(len(r)):
        g_arr = []
        fbase = createfile_pdfsign_v1(r[n]['string_pdf'],r[n]['hash_pdf'])
        del fbase['result']
        del fbase['path_pdfhash']
        del fbase['path_pdfsign']
        fbase['fid'] = r[n]['fid']
        fbase['path'] = fbase['path_data']
        del fbase['path_data']
        # fbase['path'] = r[n]['path_data']
        # g.append(fbase)
        g_arr.append(fbase['path_pdf'])   
        g_arr.append(fbase['path'])         
        g_arr.append(fbase['fid'])  
        list_tmp.append(fbase['fid'])                 
        g_tple = tuple(g_arr)
        g_arr_list.append(g_tple)
    # print(g_arr_list)
    r = update_4().update_pathPDF_v1(g_arr_list)
    return jsonify(list_tmp)
    # return jsonify({'status':'success'})

@status_methods.route('/api/v1/clear_document',methods=['POST'])
def clear_document_api_v1():
    select_1().select_stepdata_v1('0105530066223')
    return ''

@status_methods.route('/api/v1/remove',methods=['POST'])
def remove_api_v1():
    arr_tmp = []
    tmp_arr_v1 = [0,1,2,3,4]
    tmp_arr_v2 = [0,1]
    for i in range(len(tmp_arr_v1)):
        for j in range(len(tmp_arr_v2)):
            if tmp_arr_v1[i] != tmp_arr_v2[j]:
                if tmp_arr_v2[j] not in arr_tmp:
                    arr_tmp.append(tmp_arr_v2[j])
            
    print(arr_tmp)

@status_methods.route('/api/v1/sftp_rpa',methods=['POST'])
def sftp_rpa_v1():
    SERVER = '203.150.197.76'  
    USER = 'ftp_user'  
    PASS = 'F9wxw,jwfhovo'
    PORT = 22
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    try:
        with pysftp.Connection(SERVER, username=USER, password=PASS,cnopts=cnopts) as sftp:
            print('connect success')
    except Exception as e:
        print('connect fail')
    return ''
    # import openpyxl
    # file = request.files['file']
    # file_excel = openpyxl.load_workbook(file)
    # excel_active = file_excel.active
    # arr_docid = []
    # for n in range(2,131,1):
    #     # print(n)
    #     cell_obj = excel_active.cell(row=n,column=3) 
    #     # print(cell_obj.value)
    #     arr_docid.append(cell_obj.value)
    # # sidcode = select_1().select_data_groupform()
    # # result = select_1().select_filter_template(sidcode)
    # # ff = select_1().edit_group_detail(result)
    # # arr_docid = []
    # # arr_docid = ['SCS-63000000102','SCS-63000000267','SCS-63000000225','SCS-63000000177','SCS-63000000307','SCS-63000000138','SCS-63000000131']
    # result = select().select_docid_tosidcode_v1(arr_docid)
    # sidcode = result['messageText']
    # # sidcode = ['e997aa3f-1d85-42bf-a4c8-60288c866abe']
    # select_1().select_data_edit_v2(sidcode)
    # return jsonify(result) 

@status_methods.route('/api/v1/tranfer_people',methods=['GET'])
def tranfer_people_api_v1():
    if request.method == 'POST':
        return ''

@status_methods.before_request
def before_request():
    methods_req = request.method
    # print(request.environ.get('HTTP_X_FORWARDED_FOR'))
    url_req = request.url
    body_req = request.get_json()
    uuid_log = str(uuid.uuid4())
    session["uuid_log"] = uuid_log
    start = time.time()
    session["time_start"] = start
    try:
        tmp_token = request.headers['Authorization']
        tmp_token_01 = str(tmp_token).split(' ')[1]
    except Exception as e:
        tmp_token_01 = None    
    if '/public/v1/log' not in url_req:
        pass

@status_methods.after_request
def do_something_whenever_a_request_has_been_handled(response):
    text_id = session.get("id")
    time_start = session.get("time_start")
    end_time = (time.time() - time_start)*1000
    end_time = ("{:.2f}".format(end_time))
    end_time_str = str(end_time)+' ms'
    str_status = str(response.status).split(' ')[1]
    status_as_string = str(response.status_code)
    status_code = response.status_code
    methods_req = request.method
    url_req = request.url
    # uuid_log = str(uuid.uuid4())
    try:
        # uuid_log = session["uuid_log"]
        todays = (datetime.date.today())
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        date_today = datetime.datetime.strptime(str(todays),"%Y-%m-%d").strftime("%d-%m-%Y")
        day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
        uuid_log = request.environ.get("FLASK_REQUEST_ID")
        try:
            mesg = json.loads(response.get_data())
            
            # print ('UUIDDDDD:',uuid_log)
            if 'result' in mesg:
                if mesg['result'] == 'OK':
                    pass
                    # update().update_req_v1(text_id,mesg,status_as_string)
                    status_log = status_as_string + 'OK'
                else:
                    callWebHook_slack_v1(str(mesg),'',url_req)
                    status_log = status_as_string + ' ER'
                    # update().update_req_v1(text_id,mesg,'ER')
            else:
                # print(mesg)
                callWebHook_slack_v1(str(mesg),'',url_req)
                status_log = status_as_string + ' ER'
                # update().update_req_v1(text_id,mesg,'ER')
            # url_req = request.environ.get("REQUEST_URI")
            parsed = urlparse.urlparse(url_req)
            if str(parsed.query) != '':
                url_req = str(parsed.path)+'?'+str(parsed.query)
            else:
                url_req = str(parsed.path)
            text_to_log = day_n_time+' '+' '+uuid_log+' '+url_req+' '+status_log+' '+end_time_str
            save_log3(text_to_log,'request_')
        except Exception as e:
            if methods_req == 'GET':
                if status_code == 200 or status_code == 201:
                    # update().update_req_v1(text_id,None,status_as_string)
                    pass
                else:
                    callWebHook_slack_v1('Methods : ' + methods_req + ' HTTP Status Code : ' + str(status_as_string),'',url_req)
                    # update().update_req_v1(text_id,None,status_as_string)
            else:
                if status_code == 200 or status_code == 201:
                    pass
                    # update().update_req_v1(text_id,None,status_as_string)
                else:
                    callWebHook_slack_v1('Methods : ' + methods_req + ' HTTP Status Code : ' + str(status_as_string),'',url_req)
                    # update().update_req_v1(text_id,None,status_as_string)
            # url_req = request.environ.get("REQUEST_URI")
            parsed = urlparse.urlparse(url_req)
            if str(parsed.query) != '':
                url_req = str(parsed.path)+'?'+str(parsed.query)
            else:
                url_req = str(parsed.path)
            print ('url_req22:',url_req)
            text_to_log = day_n_time+' '+' '+uuid_log+' '+url_req+' '+status_as_string + ' ' + str_status+' '+end_time_str
            save_log3(text_to_log,'request_')
            
        # logging.warning("status as string %s" % status_as_string)
        return response
    except Exception as e:
        logger.info(e)
        return response

@status_methods.route('/test_ran')
def hello_world():
    if request.args.get('res') != None:
        test = request.args.get('res')
    re_id = request.environ.get("FLASK_REQUEST_ID")
    print ('re_id:',re_id)
    print ('EEEEE:',request.environ.get("REQUEST_URI"))
    
    return test
    # return jsonify({'result':'OK','status_Code':200,'messageText':test,'messageER':None}),200


@status_methods.route('/api/count_storage_file', methods=['POST'])
def count_storage_file():
    if request.method == 'POST':
        try:
            result_select = select_2().count_file_storage_v2()
            return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/fid_path_to_base64', methods=['POST'])
def fid_path_to_base64():
    if request.method == 'POST':
        datajson = request.json
        try:
            if 'fid' in datajson and len(datajson) == 1:
                fid = datajson['fid']
                result_select = select_2().path_to_base64_v2(fid)
                if result_select['result'] == 'OK':
                    path_base64_all = result_select['messageText']
                    return jsonify({'result':'OK','messageText':path_base64_all,'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found'}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/v1/document_other_business',methods=['GET'])
# @token_required_v3
def document_business_v1():
    if request.method == 'GET':
        try:
            if request.args.get('email') != None:
                email = request.args.get('email')
                dataDocument = select_2().select_data_document_other_business(email)       
                if dataDocument['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'message':'success','data': dataDocument['data'] },'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':{'message': dataDocument['messageER'],'data':None},'status_Code':200})
            else:
                return jsonify({'result':'ER','messageText': 'parameter incorrect','status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200
    else:
        return jsonify({'result':'ER','messageText': 'method incorrect','status_Code':200}),200

@status_methods.route('/api/v1/get_filesize_biz',methods=['POST'])
# @token_required_v3
def get_filesize_biz_v1():
    try:
        if request.method == 'POST':
            # folder_name IN ('3a3d375b-7972-49ea-8d83-7e213c5d11aa','4a65158c-9cde-423b-b9e2-cdd4cbfdfff3','6e13c42c-773d-4d00-949a-a1649e360434','9471eecb-a264-4314-aea1-e1ab2f9021d1','9e78ee79-b2ad-4925-bafc-9a399586c9ea','b8762888-6fde-415d-9e29-0a6883ab73be','c747a2fb-c450-4a5c-a3d1-7d0d980adf6c','c9e58a01-bb32-43bb-b297-ffea359a229a','da6c8363-9711-40e3-9cae-762824d83b9d','fd4405a9-466d-4344-a75a-ea5b738cb4e0','c95edab0-0e12-4fe3-9ab2-384d27b2248e')
            total_size = 0
            # path = 'D:/iNet_storage/test_file_json/'
            # path = 'D:/iNet_storage/file_test/'
            path = path_global_1 + '/storage/'
            list_err = []
            select_all = select_2().select_json_file_attach_all()
            # print(select_all)
            if select_all['result'] == 'OK':
                tmp_query = select_all['messageText']
            else:
                return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':select_all['messageText']}),200
            for y in range(len(tmp_query)):
                foldername_qry = (tmp_query[y]['folder_name'])
                path2 = path + str(foldername_qry)
                for dirpath, dirnames, filenames in os.walk(path2):
                    list_file = []
                    for i in filenames:
                        dict_file = {}
                        f = os.path.join(dirpath, i)
                        folder_name = dirpath.split('/')[5]
                        dict_file = {
                            "file_name" : i,
                            "folder_name" : str(folder_name),
                            "file_size" : (os.path.getsize(f))
                        }
                        list_file.append(dict_file)
                        total_size += os.path.getsize(f)
                    for x in range(len(list_file)):
                        print (x)
                        # print ('list_file:',list_file)
                        # print ('folder_name:',list_file[x]['folder_name'])
                        folder_name_db = list_file[x]['folder_name']
                        # result_select = select_2().select_json_file_attach_v2(folder_name_db,list_file,total_size)
                        result_select = update_2().update_json_file_attach_v1(folder_name_db,list_file,total_size,tmp_query)
                        if result_select['result'] == 'OK':
                            break
                        else:
                            list_err.append(folder_name_db)
                    total_size = 0
        return jsonify({'result':'OK','messageText': {'status_update':'update_success','folder_name_err':list_err}}),200
    except Exception as e:
        print (str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','status_Code':200,'messageText':'update_fail','messageER':{'data':None,'message':str(e)}}),200

@status_methods.route('/api/v1/migrate_sender_name',methods=['POST'])
def api_migrate_sender_name():
    try:
        list_tuple = []
        result_select = select_4().select_sender_for_migrate()
        if result_select['result'] == 'OK':
            for i in range(len(result_select['messageText'])):
                result_tmp = result_select['messageText'][i]
                sid = result_tmp['step_data_sid']
                send_user = result_tmp['send_user']
                tmp_dict = {
                    'sid' : sid,
                    'send_user': send_user
                }
                list_tuple.append(tmp_dict)
            result_migrate = migrate_sender_name(list_tuple)
            return jsonify({'result':'OK','status_Code':200,'messageText':result_migrate['messageText'],'messageER':None}),200
        else:
            return jsonify({'result':'ER','status_Code':200,'messageText':result_select['messageText'],'messageER':None}),200
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200

# print (select_4().select_tax_id_for_migrate())

@status_methods.route('/api/v1/migrate_tax_id',methods=['POST'])
def api_migrate_tax_id():
    try:
        list_tuple = []
        result_select = select_4().select_tax_id_for_migrate()
        if result_select['result'] == 'OK':
            for i in range(len(result_select['messageText'])):
                result_tmp = result_select['messageText'][i]
                sid = result_tmp['sid']
                tax_id = result_tmp['tax_id']
                tmp_dict = {
                    'sid' : sid,
                    'tax_id': tax_id
                }
                list_tuple.append(tmp_dict)
                # print ('list_tuple:',list_tuple)
            if list_tuple == []:
                return jsonify({'result':'ER','status_Code':200,'messageText':'no data to migrate','messageER':None}),200
            else:
                result_migrate = migrate_tax_id(list_tuple)
                return jsonify({'result':'OK','status_Code':200,'messageText':result_migrate['messageText'],'messageER':None}),200
        else:
            return jsonify({'result':'ER','status_Code':200,'messageText':result_select['messageText'],'messageER':None}),200
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200

@status_methods.route('/api/v1/nodejs_replace_qoute',methods=['POST'])
def nodejs_replace_qoute():
    try:
        if request.method == 'POST':
            dataJson = request.json
            if 'string' in dataJson and len(dataJson) == 1:
                string = dataJson['string']
                print (string)
                str_eval = eval(str(string))
                print (str_eval)
            return jsonify({'result':'OK','status_Code':200,'messageText':str_eval,'messageER':None}),200

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200

# @event.listens_for(Engine, "before_cursor_execute")
# def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#     context._query_start_time = time.time()
#     # current_app.logger.debug("Start Query:\n%s" % statement)
#     print("Start Query:\n%s" % statement)
#     # Modification for StackOverflow answer:
#     # Show parameters, which might be too verbose, depending on usage..
#     # current_app.logger.debug("Parameters:\n%r" % (parameters,))
#     # print(("Parameters:\n%r" % (parameters,)))


# @event.listens_for(Engine, "after_cursor_execute")
# def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#     total = time.time() - context._query_start_time
#     # current_app.logger.debug("Query Complete!")
#     print(("Query Complete!"))
#     # Modification for StackOverflow: times in milliseconds
#     # current_app.logger.debug("Total Time: %.02fms" % (total*1000))
#     print(("Total Time: %.02fms" % (total*1000)))

# def selectdb_test():
#     while True:
#         try:
#             with engine.connect() as connection:
#                 result_select = connection.execute(text('''SELECT 1'''))
#                 print(result_select)
#                 connection.close()          
#             with slave.connect() as connection:
#                 result_select = connection.execute(text('''SELECT 1'''))
#                 print(result_select)
#                 connection.close()  
#             time.sleep(10)
#         except Exception as e:
#             pass
# x = threading.Thread(target=selectdb_test)
# x.start()