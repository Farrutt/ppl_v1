#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config.lib import *

type_product = 'uat'
print(type_product)
if type_product == "uat":
    smtp_server = 'mailtx.inet.co.th'
    null = None
    true = True
    false = False
    # bi
    url_bi = 'http://203.154.135.51:5002'
    url_bi_2 = 'http://203.154.135.51:5001'
    url_biqt = 'http://203.154.135.35:5000'
    # url_bi_cs = 'http://203.154.39.167:5001'
    url_bi_cs = 'http://uatservicereport.one.th:5001'
    url_bi_cs_jv = 'http://uatservicereport.one.th:5007'
    # ai
    url_manageai = 'http://quanta3.manageai.co.th:7777'
    # path file
    path_global_1 = '/home/jirayu.ko/uat_paperless'
    prefix_ppl = '/paper_less_uat'
    #onebox
    url_onebox = 'https://uatbox.one.th'
    url_mainbox = 'https://uatbox.one.th/onebox_uploads'
    # url_mainbox = 'http://127.0.0.1:8903'
    token_onebox = '7de269ee4b15a327d8843a0b2505187dd3fb875c5c39dac06bcbc7e9ff68b5df5fa8d71c56d45fd93aab1be35c57930a56cc70574b2d12c6bb8dba8751685891'
    #dms
    url_dms = "http://172.16.40.100:5000"
    url_req_dms = 'http://172.16.40.100:8080'
    #slack
    url_slack = 'https://hooks.slack.com/services/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'
    # eform
    convert_eform = 'http://10.0.0.32:8800'
    # convert_eform = 'https://uateform.one.th/service'
    url_eform = 'https://eform.one.th/service-eform-uat'
    url_ip_eform = 'https://uateform.one.th/eform_api'
    #
    paperless_tracking = 'https://uatpaperless.one.th/tracking?id='
    login_Page = 'https://uatpaperless.one.th/login?page='
    url_paperless = 'https://uatpaperless.one.th/'
    myUrl = "http://127.0.0.1:8310"
    myUrl_domain = "https://uatpaperless.one.th/paper_less/"
    myUrl_domain2 = 'https://uatpaperless.one.th/login'
    myUrl_toChat = "https://uatpaperless.one.th/onechat/signature"
    myUrl_toTaskChat = "https://uatpaperless.one.th/onechat/task"
    myUrl_toViewPDF_toChat = "https://uatpaperless.one.th/onechat/viewpdf"
    #
    # paperless_tracking = 'https://pocpaperless.one.th/paper_less/tracking?id='
    # login_Page = 'https://pocpaperless.one.th/login?page='
    # url_paperless = 'https://pocpaperless.one.th/'
    # myUrl = "http://127.0.0.1:8310"
    # myUrl_domain = "https://pocpaperless.one.th/paper_less"
    # myUrl_domain2 = 'https://pocpaperless.one.th/login'
    # myUrl_toChat = "https://pocpaperless.one.th/onechat/signature"
    # myUrl_toTaskChat = "https://pocpaperless.one.th/uatpaperless/onechat/task"
    # myUrl_toViewPDF_toChat = "https://pocpaperless.one.th/onechat/viewpdf"
    #
    # OneAuth_UAT
    uat_url_auth = 'https://uat-sign.one.th/OneESign/api/Transport/Etax'
    url_credentials_authorize_v2 = 'https://uat-sign.one.th/webservice/api/v2/credentials/authorize'
    url_credentials_list_v2 = 'https://uat-sign.one.th/webservice/api/v2/credentials/list'
    url_pdfSigning_Sign_v2 = 'https://uat-sign.one.th/webservice/api/v2/signing/pdfSigning'
    url_pdfSigning_Sign_v3 = 'https://uat-sign.one.th/webservice/api/v2/signing/pdfSigning-V3'
    url_createNote_v1 = 'https://uat-sign.one.th/webservice/api/v2/document/createNote'
    url_createNoteAndSign_v1 = 'https://uat-sign.one.th/webservice/api/v2/document/createNoteAndSign'
    url_addHistory_v1 = 'https://uat-sign.one.th/webservice/api/v2/document/addHistory'
    url_oneAuth = 'https://uat-sign.one.th'
    # OneChat_UAT
    token_service = 'Bearer A114be672146a57b690973a5b600f446187e8f9b094e84ae5a955780e477ae54a5cd8f63d965a462a822a7cad1b970374'
    bot_id = 'B0df132b88f9a526691a0576bfdb24196'
    bot_bug_token = 'Bearer A7c724a24bee6546482f4c7b7103fd0051aabbf23020b427dadc2ef6f736b1fb7fa8bdc327089472b837d508c01405d73'
    bot_bug_id = 'Be3e8a16bc612575393012ebd58205420'
    user_bug_id = 'G5ef1c613607a52001afe9391fd5920ffb0075c8f947694440a187e0f'
    token_bot_noti = 'Bearer A7c724a24bee6546482f4c7b7103fd0051aabbf23020b427dadc2ef6f736b1fb7fa8bdc327089472b837d508c01405d73'
    useridChat_warning = 'G5ef1c613607a52001afe9391fd5920ffb0075c8f947694440a187e0f'
    bot_chat_id_noti = 'Bb7f46c3d3d435f39a9822f1e1b57d870'
    url_oneChat = 'https://uatchat-public.one.th:8034'
    url_onechat_1 = 'https://uatchat-manage.one.th:8997'
    url_chat = 'https://uatchat-public.one.th:8034/api/v1/push_message'
    url_frd = 'https://uatchat-manage.one.th:8997/api/v1/searchfriend'
    url_getlist = 'https://uatchat-manage.one.th:8997/api/v1/getlistroom'
    url_addfrdAuto = 'https://uatchat-manage.one.th:8997/api/v1/addfriendmulti'
    url_loginchat = 'https://uatchat-manage.one.th:8997/api/v1/registeronechat'
    url_disble_template = 'https://uatchat-public.one.th:8034/api/v1/bot_disable_template'
    url_close_webview = 'https://uatchat-public.one.th:8034/api/v1/disable_webview'
    token_service_autoAdd = 'Bearer Ad5cf4ee0e11f5ebc836e8176902a664d7e93c2222dca492eaa5f6f788e0fc70efdb1c1042efa4f5491e026603e0c8b3f'
    # taskChat
    url_taskchat = 'https://uatchat-public.one.th:8000'
    Url_Bot_getProject = 'https://uatchat-public.one.th:8000/api/v1/bot_get_project'
    Url_Bot_CreateTask = 'https://uatchat-public.one.th:8000/api/v1/bot_create_task'
    url_change_state = 'https://uatchat-public.one.th:8000/api/v1/bot_change_state'
    # OneChain_UAT
    url_onechain_ForUploadFile = "http://127.0.0.1:8911"
    # url_onechain_ForUploadFile = "https://devinet-etax.one.th/uploadfile"
    # OneId_UAT
    url_checkmail = 'https://testoneid.inet.co.th/api/check_one_mail'
    one_url = "https://testoneid.inet.co.th"
    ref_code  =  "snykbi"
    clientId  =  "147"
    secretKey =  "zgZ45TRqSkoYVZbErn1KCW5FTh5Alin37kZ4vvOk"
    email_admin = ['jirayu.ko@thai.com','sarawut.sint_6340@thai.com']
    mail_address = '@thai.com'
    # Thai dot com payment
    url_thaidotcompayment = 'http://203.150.197.240:4000'
elif type_product == "prod":
    smtp_server = 'mailtx.inet.co.th'
    null = None
    true = True
    false = False
    # bi
    url_bi = 'http://203.154.135.51:5002'
    url_bi_2 = 'http://203.154.135.51:5001'
    url_biqt = 'http://203.154.135.51:5006'
    url_bi_cs = 'http://pplservicereport.one.th:5001'
    url_bi_cs_jv = 'http://pplservicereport.one.th:5004'
    # ail
    url_manageai = 'http://quanta3.manageai.co.th:7777'
    # path file
    path_global_1 = '/home/jirayu.ko/paperless_prod'
    prefix_ppl = '/paper_less'
    #dms
    url_dms = "http://172.16.40.100:5000"
    url_req_dms = 'http://172.16.40.100:8080'
    #onebox
    url_onebox = 'https://box.one.th'
    url_mainbox = 'https://box.one.th/onebox_uploads'
    token_onebox = '7de269ee4b15a327d8843a0b2505187dd3fb875c5c39dac06bcbc7e9ff68b5df5fa8d71c56d45fd93aab1be35c57930a56cc70574b2d12c6bb8dba8751685891'
    #slack
    url_slack = 'https://hooks.slack.com/services/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'
    # eform
    convert_eform = 'https://eform.one.th/service'
    url_eform = 'https://eform.one.th/eform_api'
    url_ip_eform = 'https://eform.one.th/eform_api'
    # prod
    # paperless_tracking = 'https://pocpaperless.one.th/paper_less/tracking?id='
    # login_Page = 'https://pocpaperless.one.th/login?page='
    # url_paperless = 'https://pocpaperless.one.th/'
    # myUrl = "http://127.0.0.1:8310"
    # myUrl_domain = "https://pocpaperless.one.th/paper_less"
    # myUrl_domain2 = 'https://pocpaperless.one.th/login'
    # myUrl_toChat = "https://pocpaperless.one.th/onechat/signature"
    # myUrl_toTaskChat = "https://pocpaperless.one.th/uatpaperless/onechat/task"
    # myUrl_toViewPDF_toChat = "https://pocpaperless.one.th/onechat/viewpdf"
    # 
    myUrl = "http://127.0.0.1:8300"
    #########################################
    # paperless_tracking = 'https://203.154.86.1/tracking?id='
    # login_Page = 'https://203.154.86.1/login?page='
    # url_paperless = 'https://203.154.86.1/'
    # myUrl_domain = "https://203.154.86.1/paper_less/"
    # myUrl_domain2 = "https://203.154.86.1/login"
    # myUrl_toChat = "https://203.154.86.1/onechat/signature"
    # myUrl_toTaskChat = "https://203.154.86.1/onechat/task"
    # myUrl_toViewPDF_toChat = "https://203.154.86.1/onechat/viewpdf"
    paperless_tracking = 'https://paperless.one.th/tracking?id='
    login_Page = 'https://paperless.one.th/login?page='
    url_paperless = 'https://paperless.one.th/'
    myUrl_domain = "https://paperless.one.th/paper_less/"
    myUrl_domain2 = "https://paperless.one.th/login"
    myUrl_toChat = "https://paperless.one.th/onechat/signature"
    myUrl_toTaskChat = "https://paperless.one.th/onechat/task"
    myUrl_toViewPDF_toChat = "https://paperless.one.th/onechat/viewpdf"
    ############################################
    # OneAuth_Prod
    # uat_url_auth = 'https://uat-sign.one.th/OneESign/api/Transport/Etax'
    url_credentials_authorize_v2 = 'https://sign.one.th/webservice/api/v2/credentials/authorize'
    url_credentials_list_v2 = 'https://sign.one.th/webservice/api/v2/credentials/list'
    url_pdfSigning_Sign_v2 = 'https://sign.one.th/webservice/api/v2/signing/pdfSigning'
    url_pdfSigning_Sign_v3 = 'https://sign.one.th/webservice/api/v2/signing/pdfSigning-V3'
    url_createNote_v1 = 'https://sign.one.th/webservice/api/v2/document/createNote'
    url_createNoteAndSign_v1 = 'https://sign.one.th/webservice/api/v2/document/createNoteAndSign'
    url_addHistory_v1 = 'https://sign.one.th/webservice/api/v2/document/addHistory'
    url_oneAuth = 'https://sign.one.th'
    # OneChat_Prod
    token_service = 'Bearer A16185216830056b1946f138905230c3c633dbeec596d4e8d962971c40269af89a5b101b00a02411db4d741312cee67d5'
    bot_id = 'B8bb8493bce765ca99374070aefd167cb'
    bot_bug_token = 'Bearer A0b70e5f65a3b5816b36ccf7435779e47ff8c802cfc414f728808fc7f803cc13c53560af7ab4c4f5aa997cb5fca7a88d2'
    bot_bug_id = 'B8fe9c2cab06956b0a28b0a25e16d43e2'
    user_bug_id = 'G5e44be95e2563f002c0232b4a5b3d209174e553eba02fc3da27e28ac'
    token_bot_noti = 'Bearer A89a857fd25805679a41ad51c3505ae3a6eaf2f84de624a6a8b1689fb1d616973b5f7fff147714ee3b9800cc99b662142'
    useridChat_warning = 'G5e44be95e2563f002c0232b4a5b3d209174e553eba02fc3da27e28ac'
    bot_chat_id_noti = 'Be97d0cbdfc67534abc1c5385fb268a36'
    url_oneChat = 'https://chat-api.one.th/message'
    url_onechat_1 = 'https://chat-api.one.th/manage'
    url_chat = 'https://chat-api.one.th/message/api/v1/push_message'
    url_frd = 'https://chat-api.one.th/manage/api/v1/searchfriend'
    url_getlist = 'https://chat-api.one.th/manage/api/v1/getlistroom'
    url_addfrdAuto = 'https://chat-api.one.th/manage/api/v1/addfriendmulti'
    url_loginchat = 'https://chat-api.one.th/manage/api/v1/registeronechat'
    url_disble_template = 'https://chat-api.one.th/message/api/v1/bot_disable_template'
    url_close_webview = 'https://chat-api.one.th/message/api/v1/disable_webview'
    token_service_autoAdd = 'Bearer A63c3fb9376eb5f399c1833ff8b2f0d5cdb0daf9c145e45eba10c56492dfb136bdc3ecb74e7de4133ad62c4fa900742cf'
    # taskChat
    url_taskchat = 'https://chat-api.one.th/event'
    Url_Bot_getProject = 'https://chat-api.one.th/event/api/v1/bot_get_project'
    Url_Bot_CreateTask = 'https://chat-api.one.th/event/api/v1/bot_create_task'
    url_change_state = 'https://chat-api.one.th/event/api/v1/bot_change_state'
    # OneChain_Prod
    url_onechain_ForUploadFile = "http://127.0.0.1:8911"
    # url_onechain_ForUploadFile = "https://devinet-etax.one.th/uploadfile"
    # OneId_Prod
    url_checkmail = 'https://one.th/api/check_one_mail'
    one_url = "https://one.th"
    ref_code  =  "u8pBiM"
    clientId  =  "136"
    secretKey =  "yiDaGvk4c6jbmXaSdiOtIqgS7Dkn5U1ItNz5hxHU"
    email_admin = ['jirayu.ko@one.th','sarawut.si@one.th']
    mail_address = '@one.th'
    # Thai dot com payment
    url_thaidotcompayment = 'http://203.150.197.240:4000'
elif type_product == 'dev':
    smtp_server = 'mailtx.inet.co.th'
    null = None
    true = True
    false = False
    # bi
    url_bi = 'http://203.154.135.51:5002'
    url_bi_2 = 'http://203.154.135.51:5001'
    # ai
    url_manageai = 'http://quanta3.manageai.co.th:7777'
    # path file
    path_global_1 = '/paperless/dev'
    # path_global_1 = '/home'
    prefix_ppl = '/paper_less_uat'
    #onebox
    url_onebox = 'https://uatbox.one.th'
    url_mainbox = 'https://uatbox.one.th/onebox_uploads'
    # url_mainbox = 'http://127.0.0.1:8903'
    token_onebox = '7de269ee4b15a327d8843a0b2505187dd3fb875c5c39dac06bcbc7e9ff68b5df5fa8d71c56d45fd93aab1be35c57930a56cc70574b2d12c6bb8dba8751685891'
    #dms
    url_dms = "http://172.16.40.100:5000"
    url_req_dms = 'http://172.16.40.100:8080'
    #slack
    url_slack = 'https://hooks.slack.com/services/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'
    # eform
    # convert_eform = 'http://127.0.0.1:8800'
    convert_eform = 'https://eform.one.th/webservice'
    url_eform = 'https://eform.one.th/service-eform-uat'
    url_ip_eform = 'https://uateform.one.th/eform_api'
    #
    paperless_tracking = 'https://ppl.one.th/uatpaperless/tracking?id='
    login_Page = 'https://ppl.one.th/login?page='
    url_paperless = 'https://ppl.one.th/'
    myUrl = "http://127.0.0.1:8310"
    myUrl_domain = "https://ppl.one.th/paper_less/"
    myUrl_domain2 = 'https://ppl.one.th/login'
    myUrl_toChat = "https://ppl.one.th/onechat/signature"
    myUrl_toTaskChat = "https://ppl.one.th/onechat/task"
    myUrl_toViewPDF_toChat = "https://ppl.one.th/onechat/viewpdf"
    #
    # paperless_tracking = 'https://pocpaperless.one.th/paper_less/tracking?id='
    # login_Page = 'https://pocpaperless.one.th/login?page='
    # url_paperless = 'https://pocpaperless.one.th/'
    # myUrl = "http://127.0.0.1:8310"
    # myUrl_domain = "https://pocpaperless.one.th/paper_less"
    # myUrl_domain2 = 'https://pocpaperless.one.th/login'
    # myUrl_toChat = "https://pocpaperless.one.th/onechat/signature"
    # myUrl_toTaskChat = "https://pocpaperless.one.th/uatpaperless/onechat/task"
    # myUrl_toViewPDF_toChat = "https://pocpaperless.one.th/onechat/viewpdf"
    #
    # OneAuth_UAT
    uat_url_auth = 'https://uat-sign.one.th/OneESign/api/Transport/Etax'
    url_credentials_authorize_v2 = 'https://uat-sign.one.th/webservice/api/v2/credentials/authorize'
    url_credentials_list_v2 = 'https://uat-sign.one.th/webservice/api/v2/credentials/list'
    url_pdfSigning_Sign_v2 = 'https://uat-sign.one.th/webservice/api/v2/signing/pdfSigning'
    url_pdfSigning_Sign_v3 = 'https://uat-sign.one.th/webservice/api/v2/signing/pdfSigning-V3'
    url_createNote_v1 = 'https://uat-sign.one.th/webservice/api/v2/document/createNote'
    url_createNoteAndSign_v1 = 'https://uat-sign.one.th/webservice/api/v2/document/createNoteAndSign'
    url_addHistory_v1 = 'https://uat-sign.one.th/webservice/api/v2/document/addHistory'
    url_oneAuth = 'https://uat-sign.one.th'
    # OneChat_UAT
    token_service = 'Bearer A114be672146a57b690973a5b600f446187e8f9b094e84ae5a955780e477ae54a5cd8f63d965a462a822a7cad1b970374'
    bot_id = 'B0df132b88f9a526691a0576bfdb24196'
    bot_bug_token = 'Bearer A7c724a24bee6546482f4c7b7103fd0051aabbf23020b427dadc2ef6f736b1fb7fa8bdc327089472b837d508c01405d73'
    bot_bug_id = 'Be3e8a16bc612575393012ebd58205420'
    user_bug_id = 'G5ef1c613607a52001afe9391fd5920ffb0075c8f947694440a187e0f'
    token_bot_noti = 'Bearer A7c724a24bee6546482f4c7b7103fd0051aabbf23020b427dadc2ef6f736b1fb7fa8bdc327089472b837d508c01405d73'
    useridChat_warning = 'G5ef1c613607a52001afe9391fd5920ffb0075c8f947694440a187e0f'
    bot_chat_id_noti = 'Bb7f46c3d3d435f39a9822f1e1b57d870'
    url_oneChat = 'https://uatchat-public.one.th:8034'
    url_chat = 'https://uatchat-public.one.th:8034/api/v1/push_message'
    url_frd = 'https://uatchat-manage.one.th:8997/api/v1/searchfriend'
    url_getlist = 'https://uatchat-manage.one.th:8997/api/v1/getlistroom'
    url_addfrdAuto = 'https://uatchat-manage.one.th:8997/api/v1/addfriendmulti'
    url_loginchat = 'https://uatchat-manage.one.th:8997/api/v1/registeronechat'
    url_disble_template = 'https://uatchat-public.one.th:8034/api/v1/bot_disable_template'
    url_close_webview = 'https://uatchat-public.one.th:8034/api/v1/disable_webview'
    token_service_autoAdd = 'Bearer Ad5cf4ee0e11f5ebc836e8176902a664d7e93c2222dca492eaa5f6f788e0fc70efdb1c1042efa4f5491e026603e0c8b3f'
    # taskChat
    url_taskchat = 'https://uatchat-public.one.th:8000'
    Url_Bot_getProject = 'https://uatchat-public.one.th:8000/api/v1/bot_get_project'
    Url_Bot_CreateTask = 'https://uatchat-public.one.th:8000/api/v1/bot_create_task'
    url_change_state = 'https://uatchat-public.one.th:8000/api/v1/bot_change_state'
    # OneChain_UAT
    url_onechain_ForUploadFile = "http://127.0.0.1:8911"
    # url_onechain_ForUploadFile = "https://devinet-etax.one.th/uploadfile"
    # OneId_UAT
    url_checkmail = 'https://testoneid.inet.co.th/api/check_one_mail'
    one_url = "https://testoneid.inet.co.th"
    ref_code  =  "snykbi"
    clientId  =  "147"
    secretKey =  "zgZ45TRqSkoYVZbErn1KCW5FTh5Alin37kZ4vvOk"
    email_admin = ['jirayu.ko@thai.com','sarawut.sint_6340@thai.com']
    mail_address = '@thai.com'
elif type_product == 'poc':
    smtp_server = 'mailtx.inet.co.th'
    null = None
    true = True
    false = False
    # bi
    url_bi = 'http://203.154.135.51:5002'
    url_bi_2 = 'http://203.154.135.51:5001'
    url_biqt = 'http://203.154.135.51:5006'
    url_bi_cs = 'http://pplservicereport.one.th:5001'
    url_bi_cs_jv = 'http://pplservicereport.one.th:5004'
    # ail
    url_manageai = 'http://quanta3.manageai.co.th:7777'
    # path file
    path_global_1 = '/root/b_ppl_poc'
    prefix_ppl = '/paper_less'
    #dms
    url_dms = "http://172.16.40.100:5000"
    url_req_dms = 'http://172.16.40.100:8080'
    #onebox
    url_onebox = 'https://box.one.th'
    url_mainbox = 'https://box.one.th/onebox_uploads'
    token_onebox = '7de269ee4b15a327d8843a0b2505187dd3fb875c5c39dac06bcbc7e9ff68b5df5fa8d71c56d45fd93aab1be35c57930a56cc70574b2d12c6bb8dba8751685891'
    #slack
    url_slack = 'https://hooks.slack.com/services/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'
    # eform
    convert_eform = 'https://eform.one.th/service'
    url_eform = 'https://eform.one.th/eform_api'
    url_ip_eform = 'https://eform.one.th/eform_api'
    # prod
    paperless_tracking = 'https://pocpaperless.one.th/tracking?id='
    login_Page = 'https://pocpaperless.one.th/login?page='
    url_paperless = 'https://pocpaperless.one.th/'
    myUrl = "http://127.0.0.1:8310"
    myUrl_domain = "https://pocpaperless.one.th/paper_less"
    myUrl_domain2 = 'https://pocpaperless.one.th/login'
    myUrl_toChat = "https://pocpaperless.one.th/onechat/signature"
    myUrl_toTaskChat = "https://pocpaperless.one.th/uatpaperless/onechat/task"
    myUrl_toViewPDF_toChat = "https://pocpaperless.one.th/onechat/viewpdf"
    # 
    myUrl = "http://127.0.0.1:8300"
    #########################################
    # paperless_tracking = 'https://203.154.86.1/tracking?id='
    # login_Page = 'https://203.154.86.1/login?page='
    # url_paperless = 'https://203.154.86.1/'
    # myUrl_domain = "https://203.154.86.1/paper_less/"
    # myUrl_domain2 = "https://203.154.86.1/login"
    # myUrl_toChat = "https://203.154.86.1/onechat/signature"
    # myUrl_toTaskChat = "https://203.154.86.1/onechat/task"
    # myUrl_toViewPDF_toChat = "https://203.154.86.1/onechat/viewpdf"
    # paperless_tracking = 'https://paperless.one.th/tracking?id='
    # login_Page = 'https://paperless.one.th/login?page='
    # url_paperless = 'https://paperless.one.th/'
    # myUrl_domain = "https://paperless.one.th/paper_less/"
    # myUrl_domain2 = "https://paperless.one.th/login"
    # myUrl_toChat = "https://paperless.one.th/onechat/signature"
    # myUrl_toTaskChat = "https://paperless.one.th/onechat/task"
    # myUrl_toViewPDF_toChat = "https://paperless.one.th/onechat/viewpdf"
    ############################################
    # OneAuth_Prod
    # uat_url_auth = 'https://uat-sign.one.th/OneESign/api/Transport/Etax'
    url_credentials_authorize_v2 = 'https://sign.one.th/webservice/api/v2/credentials/authorize'
    url_credentials_list_v2 = 'https://sign.one.th/webservice/api/v2/credentials/list'
    url_pdfSigning_Sign_v2 = 'https://sign.one.th/webservice/api/v2/signing/pdfSigning'
    url_pdfSigning_Sign_v3 = 'https://sign.one.th/webservice/api/v2/signing/pdfSigning-V3'
    url_createNote_v1 = 'https://sign.one.th/webservice/api/v2/document/createNote'
    url_createNoteAndSign_v1 = 'https://sign.one.th/webservice/api/v2/document/createNoteAndSign'
    url_addHistory_v1 = 'https://sign.one.th/webservice/api/v2/document/addHistory'
    url_oneAuth = 'https://sign.one.th'
    # OneChat_Prod
    token_service = 'Bearer A16185216830056b1946f138905230c3c633dbeec596d4e8d962971c40269af89a5b101b00a02411db4d741312cee67d5'
    bot_id = 'B8bb8493bce765ca99374070aefd167cb'
    bot_bug_token = 'Bearer A0b70e5f65a3b5816b36ccf7435779e47ff8c802cfc414f728808fc7f803cc13c53560af7ab4c4f5aa997cb5fca7a88d2'
    bot_bug_id = 'B8fe9c2cab06956b0a28b0a25e16d43e2'
    user_bug_id = 'G5e44be95e2563f002c0232b4a5b3d209174e553eba02fc3da27e28ac'
    token_bot_noti = 'Bearer A89a857fd25805679a41ad51c3505ae3a6eaf2f84de624a6a8b1689fb1d616973b5f7fff147714ee3b9800cc99b662142'
    useridChat_warning = 'G5e44be95e2563f002c0232b4a5b3d209174e553eba02fc3da27e28ac'
    bot_chat_id_noti = 'Be97d0cbdfc67534abc1c5385fb268a36'
    url_oneChat = 'https://chat-api.one.th/message'
    url_onechat_1 = 'https://chat-api.one.th/manage'
    url_chat = 'https://chat-api.one.th/message/api/v1/push_message'
    url_frd = 'https://chat-api.one.th/manage/api/v1/searchfriend'
    url_getlist = 'https://chat-api.one.th/manage/api/v1/getlistroom'
    url_addfrdAuto = 'https://chat-api.one.th/manage/api/v1/addfriendmulti'
    url_loginchat = 'https://chat-api.one.th/manage/api/v1/registeronechat'
    url_disble_template = 'https://chat-api.one.th/message/api/v1/bot_disable_template'
    url_close_webview = 'https://chat-api.one.th/message/api/v1/disable_webview'
    token_service_autoAdd = 'Bearer A63c3fb9376eb5f399c1833ff8b2f0d5cdb0daf9c145e45eba10c56492dfb136bdc3ecb74e7de4133ad62c4fa900742cf'
    # taskChat
    url_taskchat = 'https://chat-api.one.th/event'
    Url_Bot_getProject = 'https://chat-api.one.th/event/api/v1/bot_get_project'
    Url_Bot_CreateTask = 'https://chat-api.one.th/event/api/v1/bot_create_task'
    url_change_state = 'https://chat-api.one.th/event/api/v1/bot_change_state'
    # OneChain_Prod
    url_onechain_ForUploadFile = "http://127.0.0.1:8911"
    # url_onechain_ForUploadFile = "https://devinet-etax.one.th/uploadfile"
    # OneId_Prod
    url_checkmail = 'https://one.th/api/check_one_mail'
    one_url = "https://one.th"
    ref_code  =  "u8pBiM"
    clientId  =  "136"
    secretKey =  "yiDaGvk4c6jbmXaSdiOtIqgS7Dkn5U1ItNz5hxHU"
    email_admin = ['jirayu.ko@one.th','sarawut.si@one.th']
    mail_address = '@one.th'
    # Thai dot com payment
    url_thaidotcompayment = 'http://203.150.197.240:4000' 