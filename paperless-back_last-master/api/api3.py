# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from config.lib import *
from api.api import *
from api.api2 import *
from api.api3 import *
from api.login import *
from api.apiBiz import *
from api.file import *
from api.dashboard import *
from api.template_api import *
from api.sendmail_api import *
from api.document_api import *
from api.chat_api import *
from api.image_api import *
from api.department_api import *
from api.mail_api import *
from api.auth_api import *
from api.dashboard_admin import *
from api.other_api import *
from api.sio import *
from api.register import *
from api.excel_report import *
from api.profile import *
from api.step_api import *
from api.onebox import *
from api.mail import *
# from api.onebox_api import *
from api.schedule_log import *
from api.group_api import *
from db.db_method2 import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from db.db_method_4 import *
from method.cal_BI import *
from method.cal_tdcpm import *
from method.callwebHook import *
from method.callserver import *

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

def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

def updatePDF_for_groupV2(datajson,sid):
    # เดี๊ยวแก้ต่อ
    # print('ok')
    res_select_check = select().select_pdf_check_forupdate(sid)
    # print(res_select_check)
    if res_select_check['result'] == 'OK':
        res_updatepdf = update().update_pdf(sid,datajson['string_sign'])
        # 
        result_01 = update_1().update_pdf_groupv2(sid,datajson['string_sign'])
        # print('result_01',result_01)
        if res_updatepdf['result'] == 'OK':
            return res_updatepdf
    else:
        res_updatepdf = update().update_pdf(sid,datajson['string_sign'])
        # 
        result_01 = update_1().update_pdf_groupv2(sid,datajson['string_sign'])
        # print('result_01',result_01)
        if res_updatepdf['result'] == 'OK':
            return res_updatepdf

def updatepdf_image_backgroud(base64_pdfFile,foldername):
    # base64_pdfFile = dataJson['base64_PDF']
    path = path_global_1 + '/storage/pdf/' + foldername
    # path = './storage/pdf/' + foldername
    if not os.path.exists(path):
        os.makedirs(path)
    list_file_name = []
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
    # path_image = './storage/image/' + foldername
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
                return ({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200
    except Exception as e:
        return ({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(e)}),200

    try:
        unique_filename = str(uuid.uuid4())
        with open(path +'/'+ unique_filename +".pdf","wb") as f:
            f.write(base64.b64decode((base64_pdfFile)))
    except Exception as e:
        print(str(e))
        # print(str(e))
    address_file = path + '/' + unique_filename + '.pdf'
    countpages = 0
    images = convert_from_bytes(open(address_file,'rb').read())
    for i, image in enumerate(images):
        countpages = countpages + 1
    # print(countpages)
    try:
        maxPages = pdf2image._page_count(address_file)
    except Exception as e:
        maxPages = countpages
    # print(maxPages)
    #  min(page+10-1,maxPages)
    if maxPages != 1:
        # for page in range(1,maxPages,1):
            # print(page)
        pages = convert_from_path(address_file, dpi=200, fmt='jpeg',output_folder=path_image)
        for u in range(len(pages)):
            # print(pages[u].filename)
            filename_only = str(pages[u].filename).split('/')[-1]
            try:
                url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                with open(pages[u].filename, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    encoded_string = (encoded_string).decode('utf8')
                # list_file_name.append({'image_Base64': str(encoded_string), 'image_Url': url_view_image})
                list_file_name.append({'image_Url': url_view_image})
            except Exception as ex:
                return ({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(ex)}),200
        return ({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200
    else:
        pages = convert_from_path(address_file, dpi=200, first_page=0,fmt='jpeg', last_page = 1,output_folder=path_image)
        for u in range(len(pages)):
            # print(pages[u].filename)
            filename_only = str(pages[u].filename).split('/')[-1]
            try:
                url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                with open(pages[u].filename, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    encoded_string = (encoded_string).decode('utf8')
                # list_file_name.append({'image_Base64': str(encoded_string), 'image_Url': url_view_image})
                list_file_name.append({'image_Url': url_view_image})
            except Exception as ex:
                return ({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(ex)}),200
        return ({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200

def updatepdf_image(base64_pdfFile,foldername):
    # base64_pdfFile = dataJson['base64_PDF']
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
    # path_image = './storage/image/' + foldername
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
        # print(str(e))
    address_file = path + '/' + unique_filename + '.pdf'
    countpages = 0
    images = convert_from_bytes(open(address_file,'rb').read())
    for i, image in enumerate(images):
        countpages = countpages + 1
    # print(countpages)
    try:
        maxPages = pdf2image._page_count(address_file)
    except Exception as e:
        maxPages = countpages
    # print(maxPages)
    #  min(page+10-1,maxPages)
    if maxPages != 1:
        # for page in range(1,maxPages,1):
            # print(page)
        pages = convert_from_path(address_file, dpi=200, fmt='jpeg',output_folder=path_image)
        for u in range(len(pages)):
            # print(pages[u].filename)
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
            # print(pages[u].filename)
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

def other_service_cost(sidCode,token_header):
    try:
        if 'result' in token_header:
            if token_header['result'] == 'OK':
                token_header = request.headers['Authorization']
        try:                
            token_header = str(token_header).split(' ')[1]
            token_required = token_required_func(token_header)
            username = token_required['username']
            user_id = token_required['user_id']
        except Exception as ex:
            abort(401)
    except KeyError as ex:
        return redirect(url_paperless)
    try:
        print('sidCode')
        tmptax_idDoc = None
        status_service = []
        now = datetime.datetime.now()
        sid_code = sidCode
        tmpdataTaxid = None
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        json_data = [
            {"name_service":"RPA","status":True,"other":[{"path_folder":"/Create/CSPOC","url_path":""}]},
            {"name_service":"DMS","status":False,"other":[{"path_folder":"","url_path":""}]},
            {"name_service":"WEBHOOK","status":False,"other":[{"path_folder":"","url_path":"https://google.co.th"}]},
            {"name_service":"ONEBOX","status":False,"other":[{"path_folder":"","url_path":""}]}
        ]
        tax_id = ['0107544000094','5513213355654','7200767062847','5201285728555','3897235192540','0105538109282','5292833186265','0105538109282','0105544049695','1941028239092','5464337215261','1829875326489','5284976278602']
        r_DataTaxid = select_4().select_taxId_serviceCall()
        if r_DataTaxid['result'] == 'OK':
            tax_id = r_DataTaxid['tax_id']
        tmpdataTaxid = r_DataTaxid['data']
        result_documenttype = select().select_document_type_forOthers_v1(sid_code,tax_id)
        result_select = select_4().select_status_document_v1(sid_code)
        tmp_list_service = []
        if result_documenttype['result'] == 'OK':
            tmp_message = result_documenttype['messageText']
            if tmp_message != None:
                # print(result_documenttype, ' result_documenttype')
                tmp_TaxtId = result_documenttype['tax_id']
                for yu in tmpdataTaxid:
                    if yu['tax_id'] == tmp_TaxtId:
                        tmptax_idDoc = yu['tax_id']
                        json_data = eval(yu['config'])
                tmp_documentType = result_select['messageText']['document_type']
                tmp_relativePath = tmp_documentType + '/' + str(now.year) + '/' + str('{:02d}'.format(now.month))
                tmp_message = eval(tmp_message)
                for y in range(len(json_data)):
                    tmp_data = json_data[y]
                    for t in range(len(tmp_message)):
                        tmp_message_data = tmp_message[t]
                        if tmp_data['name_service'] == tmp_message_data['name_service']:
                            tmp_data = tmp_message_data
                            tmp_list_service.append(tmp_data)
        else:
            return ({'result':'ER','messageText':None,'messageER':{'message':'non business','data':None},'status_Code':200})
        if len(tmp_list_service) != 0:                                 
            json_data =  tmp_list_service
        else:
            json_data = json_data
        if result_select['result'] == 'OK':
            get_status_file = result_select['messageText']['status_file_code']
            get_documentType = result_select['messageText']['document_type']
            # get_status_file = 'Y'
            if get_status_file == 'Y':
                result_select_data = select_4().select_ForWebHook_v2(sid_code)
                if tmp_TaxtId == '0107544000094' or tmp_TaxtId == '5513213355654':
                    srt_service_Bi = 'BI_' + get_documentType
                    srt_service_thaidotcom = 'TDC_' + get_documentType
                    if str(get_documentType).lower() == 'qts':
                        info_r = {"service":srt_service_Bi,"status":False,"message":None}
                        r = call_service_QT_BI(sid_code)
                        # print(r)
                        if r['result'] == 'OK':
                            info_r = {"service":srt_service_Bi,"status":True,"message":None}  
                        status_service.append(info_r) 
                    elif str(get_documentType).lower() == 'tm':
                        info_r = {"service":srt_service_Bi,"status":False,"message":None}
                        r = call_service_terminate_BI(sid_code)
                        if r['result'] == 'OK':
                            info_r = {"service":srt_service_Bi,"status":True,"message":None}  
                        status_service.append(info_r)
                    elif str(get_documentType).lower() == 'tms':
                        info_r = {"service":srt_service_Bi,"status":False,"message":None}
                        r = call_service_terminate_BI(sid_code)
                        if r['result'] == 'OK':
                            info_r = {"service":srt_service_Bi,"status":True,"message":None}  
                        status_service.append(info_r) 
                    elif str(get_documentType).lower() == 'tsfn':
                        info_r = {"service":srt_service_thaidotcom,"status":False,"message":None}
                        r = call_service_pettycash_v1(sid_code,None)
                        if r['result'] == 'OK':
                            info_r = {"service":srt_service_thaidotcom,"status":True,"message":None}  
                        status_service.append(info_r) 
                    elif str(get_documentType).lower() == 'sfn':
                        info_r = {"service":srt_service_thaidotcom,"status":False,"message":None}
                        r = call_service_pettycash_v1(sid_code,None)
                        if r['result'] == 'OK':
                            info_r = {"service":srt_service_thaidotcom,"status":True,"message":None}  
                        status_service.append(info_r) 
                    # elif str(get_documentType).lower() == 'cs' or str(get_documentType).lower() == 'scs':
                    #     info_r = {"service":srt_service_Bi,"status":False,"message":None}
                    #     r = call_service_BI(tmpgroup_id,'','','','','','')
                    #     if r['result'] == 'OK':
                    #         info_r = {"service":srt_service_Bi,"status":True,"message":None}  
                    #     status_service.append(info_r)                 
                list_documentType = ['cspoc','cs','scs','tm','scst','po','cerhr','spo','tms','poc','pcm','chman','csact','csnib','csttm','cstdc','csims','csman','csinb','spr','qtnw','qt','qts','cspa']
                for u in range(len(json_data)):
                    data = json_data[u]
                    if data['name_service'] == 'RPA':
                        info_r = {"service":data['name_service'],"status":False,"message":None}
                        if data['status'] == True:
                            print('RPA')
                            result_select_action = select_4().select_get_action_and_status_v2('robot')
                            if result_select_action['result'] == 'OK':
                                if result_select_action['messageText']['status'] == True:
                                    resultselect_attm_file = select().select_attm_file_v1_for_chat_api_to_robot(sid_code)
                                    if resultselect_attm_file['result'] == 'OK':
                                        doc_id = resultselect_attm_file['messageText']['document_Id']
                                        keyword = str(doc_id).split('-')[0].lower()
                                        pathFolder = resultselect_attm_file['messageText']['pathfolder']
                                        json_Data_File = resultselect_attm_file['messageText']['json_data']
                                        username_sender = resultselect_attm_file['messageText']['sender_username']
                                        document_Type = resultselect_attm_file['messageText']['document_Type']
                                        if keyword in list_documentType:
                                            document_Type = keyword
                                        if document_Type in list_documentType or 'cs' in document_Type:
                                            result_file_last_pdf  = select().select_file_sign_last_to_email(sid_code)
                                            if result_file_last_pdf['result'] == 'OK':
                                                pdf_base64_sign = result_file_last_pdf['messageText']
                                                file_name_sign_pdf = result_file_last_pdf['file_name']    
                                                print(tmptax_idDoc)                                            
                                                # print(json_Data_File,pathFolder,'',document_Type,doc_id,pdf_base64_sign,file_name_sign_pdf,sid_code)
                                                r_robot = sftp_robot().send_file_tosftp_new_v2(json_Data_File,pathFolder,'',document_Type,doc_id,pdf_base64_sign,file_name_sign_pdf,sid_code,tax_id=tmptax_idDoc)
                                                if 'result' in r_robot:
                                                    if r_robot['result'] == 'OK':
                                                        info_r = {"service":data['name_service'],"status":True,"message":"success"}                                                        
                                                        insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'upload sftp complete',token_header)
                                                    else:
                                                        info_r = {"service":data['name_service'],"status":False,"message":r_robot['messageER']}
                                                        insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,str(r_robot['messageER']),token_header)
                                            else:
                                                info_r = {"service":data['name_service'],"status":False,"message":"data not found file"}
                                                insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'data not found file',token_header)
                                    else:
                                        doc_id = resultselect_attm_file['messageText']['document_Id']
                                        keyword = str(doc_id).split('-')[0].lower()
                                        username_sender = resultselect_attm_file['messageText']['sender_username']
                                        document_Type = resultselect_attm_file['messageText']['document_Type']
                                        folder_name = resultselect_attm_file['messageText']['folder_name']
                                        pathtemp_eform = ""
                                        json_data_details = ""
                                        pathnonperfix = ""
                                        check_filename = []
                                        if keyword in list_documentType:
                                            document_Type = keyword
                                        if folder_name != None:
                                            url = url_ip_eform + '/api/v1/get_attract_file/?folder_name=' + folder_name
                                            result_eform = callGET_other(url)
                                            folder_name = str(uuid.uuid4())
                                            pathtemp_eform = path_global_1 +'/storage/temp/' + folder_name +'/'
                                            pathnonperfix = '/storage/temp/' + folder_name +'/'
                                            if not os.path.exists(pathtemp_eform):
                                                os.makedirs(pathtemp_eform)
                                            if result_eform['result'] == 'OK':
                                                tmpmessage = result_eform['messageText'].json()
                                                if tmpmessage['result'] == 'OK':
                                                    tmpdata = tmpmessage['messageText'][0]
                                                    pathfolder = tmpdata['folder_path']
                                                    json_data_details = tmpdata['file_name']
                                                    folder_name = tmpdata['folder_name']
                                                    print(json_data_details)
                                                    for nz in range(len(json_data_details)):
                                                        tmpfile_name_original = json_data_details[nz]['file_name_original']
                                                        if tmpfile_name_original not in check_filename:
                                                            check_filename.append(tmpfile_name_original)
                                                        else:
                                                            tmpfile_name_original = str(nz) + '-' + tmpfile_name_original
                                                        tmpurl_download = json_data_details[nz]['url_download']
                                                        r = requests.get(tmpurl_download,verify=False)
                                                        with open(pathtemp_eform + tmpfile_name_original,'wb') as f: 
                                                            f.write(r.content)
                                                        print(pathtemp_eform + tmpfile_name_original)
                                        # return ''
                                        print(document_Type , keyword)
                                        if document_Type in list_documentType or keyword in list_documentType:
                                            result_file_last_pdf  =select().select_file_sign_last_to_email(sid_code)
                                            if result_file_last_pdf['result'] == 'OK':
                                                pdf_base64_sign = result_file_last_pdf['messageText']
                                                file_name_sign_pdf = result_file_last_pdf['file_name']   
                                                print(tmptax_idDoc)                                             
                                                r_robot = sftp_robot().send_file_tosftp_new_v2(json_data_details,pathnonperfix,'',document_Type,doc_id,pdf_base64_sign,file_name_sign_pdf,sid_code,tax_id=tmptax_idDoc)
                                                if 'result' in r_robot:
                                                    if r_robot['result'] == 'OK':
                                                        info_r = {"service":data['name_service'],"status":True,"message":"success"}                                                        
                                                        insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'upload sftp complete',token_header)
                                                    else:
                                                        info_r = {"service":data['name_service'],"status":False,"message":r_robot['messageER']}
                                                        insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,str(r_robot['messageER']),token_header)
                                            else:
                                                info_r = {"service":data['name_service'],"status":False,"message":"data not found file"}
                                                insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'data not found file',token_header)
                                        # insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'data not found attachment')]
                        status_service.append(info_r)
                    elif data['name_service'] == 'WEBHOOK':
                        info_r = {"service":data['name_service'],"status":False,"message":None}
                        if data['status'] == True:
                            print('WEBHOOK')
                            # r = call_webhookService(sid_code)
                            result_select = select().select_ForWebHook(sid_code)
                            if result_select['result'] == 'OK' and str(result_select['messageText']['webHook']).replace(' ','') != '':
                                del(result_select['messageText']['email_center'])
                                webhook_Data = result_select['messageText']
                                url = result_select['messageText']['webHook']
                                parsed = urlparse.urlparse(url)
                                if 'cid' in parse_qs(parsed.query):                                    
                                    r_OTHERs = call_serviceOTHERs(sid_code)
                                    if 'data' in r_OTHERs:
                                        for o in range(len(r_OTHERs['data'])):
                                            tmpr_Others = r_OTHERs['data'][o]
                                            tmpUrl = tmpr_Others['url']
                                            tmp_Data = tmpr_Others['data']
                                            try:
                                                response = requests.post(tmpUrl, json=tmpr_Others,headers={'Content-Type': 'application/json'},timeout=10,verify=False)
                                                insert().insert_tran_log_v1(str(response.text),'OK',str(tmpr_Others),tmpUrl,"")
                                                info_r = {"service":data['name_service'] + '_PDF_Service_' + str(st),"status":True,"message":'success ' + str(response.text)}
                                            except requests.HTTPError as err:
                                                pass
                                                info_r = {"service":data['name_service'] + '_PDF_Service_' + str(st),"status":False,"message":str(err)}
                                                insert().insert_tran_log_v1(str(response.text),'OK',str(tmpr_Others),tmpUrl,"")
                                            except requests.Timeout as err:
                                                pass
                                                info_r = {"service":data['name_service'] + '_PDF_Service_' + str(st),"status":False,"message":str(err)}
                                                insert().insert_tran_log_v1(str(response.text),'OK',str(tmpr_Others),tmpUrl,"")
                                            except requests.ConnectionError as err:
                                                pass
                                                info_r = {"service":data['name_service'] + '_PDF_Service_' + str(st),"status":False,"message":str(err)}
                                                insert().insert_tran_log_v1(str(response.text),'OK',str(tmpr_Others),tmpUrl,"")
                                            except Exception as err:
                                                pass
                                                info_r = {"service":data['name_service'] + '_PDF_Service_' + str(st),"status":False,"message":str(err)}
                                                insert().insert_tran_log_v1(str(response.text),'OK',str(tmpr_Others),tmpUrl,"")
                                            status_service.append(info_r)
                                else:
                                    multiple_files = []
                                    files_muti = {}
                                    tmpattempted_folder = webhook_Data['attempted_folder']
                                    if 'attchfile_json' in webhook_Data:
                                        tmpattchfile_json = webhook_Data['attchfile_json']
                                        if tmpattchfile_json != None:
                                            tmpattchfile_path = webhook_Data['attchfile_path']
                                            for zu in range(len(tmpattchfile_json)):
                                                path_fileattch = path_global_1 + tmpattchfile_path + tmpattchfile_json[zu]['file_name_new']
                                                tmpfilename = tmpattchfile_json[zu]['file_name_original']  
                                                # print(path_fileattch)       
                                                multiple_files.append(('files',(tmpfilename,open(path_fileattch, 'rb'))))
                                        else:
                                            if tmpattempted_folder != None:
                                                url = url_ip_eform + '/api/v1/get_attract_file/?folder_name=' + tmpattempted_folder
                                                result_eform = callGET_other(url)
                                                folder_name = str(uuid.uuid4())
                                                path = path_global_1 +'/storage/temp/' + folder_name +'/'
                                                if not os.path.exists(path):
                                                    os.makedirs(path)
                                                if result_eform['result'] == 'OK':
                                                    tmpmessage = result_eform['messageText'].json()
                                                    if tmpmessage['result'] == 'OK':
                                                        tmpdata = tmpmessage['messageText'][0]
                                                        pathfolder = tmpdata['folder_path']
                                                        json_data_details = tmpdata['file_name']
                                                        folder_name = tmpdata['folder_name']
                                                        for nz in range(len(json_data_details)):
                                                            tmpfile_name_original = json_data_details[nz]['file_name_original']
                                                            tmpurl_download = json_data_details[nz]['url_download']
                                                            r = requests.get(tmpurl_download,verify=False)
                                                            with open(path + tmpfile_name_original,'wb') as f: 
                                                                f.write(r.content)
                                                            # print(path + tmpfile_name_original)             
                                                            multiple_files.append(('files',(tmpfile_name_original, open(path + tmpfile_name_original, 'rb'))))
                                        tmpjsonrequest = {
                                            'data':str(webhook_Data)
                                        }
                                        headers = {}
                                        try:
                                            response = requests.request("POST", result_select['messageText']['webHook'], files=multiple_files,data=tmpjsonrequest,headers=headers,verify=False,timeout=10)
                                            info_r = {"service":data['name_service'] + '_PDF_Attachment',"status":True,"message":'success ' + str(response.text)}                                  
                                        except requests.HTTPError as err:
                                            pass
                                            info_r = {"service":data['name_service'] + '_PDF_Attachment',"status":False,"message":str(err)}
                                        except requests.Timeout as err:
                                            pass
                                            info_r = {"service":data['name_service'] + '_PDF_Attachment',"status":False,"message":str(err)}
                                        except requests.ConnectionError as err:
                                            pass
                                            info_r = {"service":data['name_service'] + '_PDF_Attachment',"status":False,"message":str(err)}
                                        except Exception as err:
                                            pass
                                            info_r = {"service":data['name_service'] + '_PDF_Attachment',"status":False,"message":str(err)}
                                        status_service.append(info_r)
                                        try:
                                            response = requests.post(result_select['messageText']['webHook'], json=webhook_Data,headers={'Content-Type': 'application/json'},timeout=10,verify=False)
                                            info_r = {"service":data['name_service'] + '_PDF',"status":True,"message":'success ' + str(response.text)}
                                        except requests.HTTPError as err:
                                            pass
                                            info_r = {"service":data['name_service'] + '_PDF',"status":False,"message":str(err)}
                                        except requests.Timeout as err:
                                            pass
                                            info_r = {"service":data['name_service'] + '_PDF',"status":False,"message":str(err)}
                                        except requests.ConnectionError as err:
                                            pass
                                            info_r = {"service":data['name_service'] + '_PDF',"status":False,"message":str(err)}
                                        except Exception as err:
                                            pass
                                            info_r = {"service":data['name_service'] + '_PDF',"status":False,"message":str(err)}
                                        status_service.append(info_r)
                    elif data['name_service'] == 'DMS':
                        info_r = {"service":data['name_service'],"status":False,"message":None}
                        if data['status'] == True:
                            print('DMS')
                            datajson_properties = {}
                            data_properties_to_dms = {}
                            tmp_file_name = result_select_data['messageText']['fileName']
                            result_select_action = select().select_get_action_and_status('dms')
                            if result_select_action['result'] == 'OK':
                                if result_select_action['messageText']['status'] == True:                                        
                                    result_docuemnt_data = select().select_pty_file_pdf_v1(sid_code)
                                    if result_docuemnt_data['result'] == 'OK':
                                        msg_data = result_docuemnt_data['msg']['options_page']
                                        if 'service_properties' in msg_data:
                                            tmp_service_properties = msg_data['service_properties']
                                            for z in range(len(tmp_service_properties)):
                                                tmp_name_service = tmp_service_properties[z]['name_service']
                                                tmp_other = tmp_service_properties[z]['other']
                                                for iu in range(len(tmp_other)):
                                                    if 'properties' in tmp_other[iu]:
                                                        tmp_properties = tmp_other[iu]['properties']
                                                        for zyu in range(len(tmp_properties)):
                                                            tmp_name_data = tmp_properties[zyu]['name'] 
                                                            tmp_value_data =tmp_properties[zyu]['value'] 
                                                            if str(tmp_name_data).replace(' ','') != '':
                                                                datajson_properties['Doc:'+tmp_name_data] = tmp_value_data
                                            if datajson_properties != {}:
                                                result_login = step_1_login_dms_v1(token_header)
                                                if result_login['result'] == 'OK':
                                                    insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'login ok ' + str(result_login['msg']),token_header)
                                                    result_attm_file = select().select_attm_file_v1_for_chat_api_to_robot(sid_code)
                                                    if result_attm_file['result'] == 'OK':
                                                        doc_id = result_attm_file['messageText']['document_Id']
                                                        pathFolder = result_attm_file['messageText']['pathfolder']
                                                        json_Data_File = result_attm_file['messageText']['json_data']
                                                        username_sender = result_attm_file['messageText']['sender_username']
                                                        document_Type = result_attm_file['messageText']['document_Type']                                                        
                                                        
                                                        result_file_last_pdf  =select().select_file_sign_last_to_email(sid_code)
                                                        if result_file_last_pdf['result'] == 'OK':
                                                            path = './storage/pdf/' + doc_id
                                                            if not os.path.exists(path):
                                                                os.makedirs(path) 
                                                            pdf_base64_sign = result_file_last_pdf['messageText']
                                                            file_name_sign_pdf = result_file_last_pdf['file_name']
                                                            with open(path + '/' + file_name_sign_pdf, "wb") as fh:
                                                                fh.write(base64.b64decode(pdf_base64_sign))
                                                            path_pdf = path + '/' + file_name_sign_pdf
                                                            token_dms = result_login['msg']['entry']['id']
                                                            for x in range(len(json_Data_File)): 
                                                                path_pdf_attm = '.' + pathFolder  + json_Data_File[x]['file_name_new']
                                                                # print(datajson_properties)
                                                                datajson_properties['name'] = json_Data_File[x]['file_name_original']
                                                                datajson_properties['relativePath'] = tmp_relativePath
                                                                data_properties_to_dms = {
                                                                    "properties":[datajson_properties]
                                                                }
                                                                # print(datajson_properties)
                                                                data_properties_to_dms = str(data_properties_to_dms) 
                                                                step_2_upload_dms_v1(token_dms,'',path_pdf_attm,json_Data_File[x]['file_name_original'],'','',data_properties_to_dms,token_header)
                                                            datajson_properties['name'] = tmp_file_name
                                                            datajson_properties['relativePath'] = tmp_relativePath
                                                            data_properties_to_dms = {
                                                                "properties":[datajson_properties]
                                                            }
                                                            data_properties_to_dms = str(data_properties_to_dms) 
                                                            step_2_upload_dms_v1(token_dms,'',path_pdf,file_name_sign_pdf,'','',data_properties_to_dms,token_header)
                                                            info_r = {"service":data['name_service'],"status":True,"message":'success'}
                                                            insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'have attm file ' + str(result_attm_file['messageText']),token_header)
                                                        else:
                                                            info_r = {"service":data['name_service'],"status":False,"message":'cant upload pdf sign file'}
                                                            insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'cant upload pdf sign file' + str(result_file_last_pdf['messageText']),token_header) 
                                                    else:
                                                        doc_id = result_attm_file['messageText']['document_Id']
                                                        username_sender = result_attm_file['messageText']['sender_username']
                                                        document_Type = result_attm_file['messageText']['document_Type']  
                                                        result_file_last_pdf  =select().select_file_sign_last_to_email(sid_code)                                                     
                                                        if result_file_last_pdf['result'] == 'OK':
                                                            path = './storage/pdf/' + doc_id
                                                            if not os.path.exists(path):
                                                                os.makedirs(path) 
                                                            pdf_base64_sign = result_file_last_pdf['messageText']
                                                            file_name_sign_pdf = result_file_last_pdf['file_name']
                                                            with open(path + '/' + file_name_sign_pdf, "wb") as fh:
                                                                fh.write(base64.b64decode(pdf_base64_sign))
                                                            path_pdf = path + '/' + file_name_sign_pdf
                                                            token_dms = result_login['msg']['entry']['id']
                                                            datajson_properties['name'] = tmp_file_name
                                                            datajson_properties['relativePath'] = tmp_relativePath
                                                            data_properties_to_dms = {
                                                                "properties":[datajson_properties]
                                                            }
                                                            data_properties_to_dms = str(data_properties_to_dms)
                                                            step_2_upload_dms_v1(token_dms,'',path_pdf,file_name_sign_pdf,'','',data_properties_to_dms,token_header)
                                                            info_r = {"service":data['name_service'],"status":True,"message":'success'}
                                                            insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'dont have attm file' + str(result_attm_file['messageText']),token_header)
                                                        else:
                                                            info_r = {"service":data['name_service'],"status":False,"message":'cant upload pdf sign file'}
                                                            insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'cant upload pdf sign file' + str(result_file_last_pdf['messageText']),token_header)
                        status_service.append(info_r)
                    elif data['name_service'] == 'ONEBOX':
                        info_r = {"service":data['name_service'],"status":False,"message":None}
                        if data['status'] == True:
                            print('ONEBOX')
                            result_tax_id = select_3().select_tax_id_to_onebox_v2(sid_code,tax_id)
                            doc_name_type = result_tax_id['messageText2']
                            result_dept = select_3().select_deptname_onebox(sid_code)
                            dept_name = result_dept['messageText']
                            taxid = result_tax_id['messageText']
                            result_user = select().select_user_first(sid_code)
                            if result_user['result'] == 'OK':
                                username_first = result_user['messageText']['username']
                                userid_first = result_user['messageText']['userid']
                                result_save_onebox = get_pdf_to_onebox_v2(sid_code,username_first,userid_first,taxid,dept_name,doc_name_type,token_header)
                                # print(result_save_onebox)
                                if result_save_onebox['result'] == 'OK': 
                                    info_r = {"service":data['name_service'],"status":True,"message":'success'}  
                        status_service.append(info_r)
            elif get_status_file == 'R':
                list_documentType = ['cerhr']
                result_select_data = select_4().select_ForWebHook_v2(sid_code)
                for u in range(len(json_data)):
                    data = json_data[u]
                    if data['name_service'] == 'RPA':
                        info_r = {"service":data['name_service'],"status":False,"message":None}
                        if data['status'] == True:
                            print('RPA')
                            result_select_action = select_4().select_get_action_and_status_v2('robot')
                            # print(result_select_action)
                            if result_select_action['result'] == 'OK':
                                if result_select_action['messageText']['status'] == True:
                                    resultselect_attm_file = select().select_attm_file_v1_for_chat_api_to_robot(sid_code)
                                    # print(resultselect_attm_file , 'resultselect_attm_file')
                                    if resultselect_attm_file['result'] == 'OK':
                                        doc_id = resultselect_attm_file['messageText']['document_Id']
                                        pathFolder = resultselect_attm_file['messageText']['pathfolder']
                                        json_Data_File = resultselect_attm_file['messageText']['json_data']
                                        username_sender = resultselect_attm_file['messageText']['sender_username']
                                        document_Type = resultselect_attm_file['messageText']['document_Type']
                                        if document_Type in list_documentType:
                                            result_file_last_pdf  = select().select_file_sign_last_to_email(sid_code)
                                            if result_file_last_pdf['result'] == 'OK':
                                                pdf_base64_sign = result_file_last_pdf['messageText']
                                                file_name_sign_pdf = result_file_last_pdf['file_name']                                                
                                                r_robot = sftp_robot().send_file_tosftp_new_v2(json_Data_File,pathFolder,'',document_Type,doc_id,pdf_base64_sign,file_name_sign_pdf,sid_code,get_status_file)
                                                if 'result' in r_robot:
                                                    if r_robot['result'] == 'OK':
                                                        info_r = {"service":data['name_service'],"status":True,"message":"success"}                                                        
                                                        insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'upload sftp complete',token_header)
                                                    else:
                                                        info_r = {"service":data['name_service'],"status":False,"message":r_robot['messageER']}
                                                        insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,str(r_robot['messageER']),token_header)
                                            else:
                                                info_r = {"service":data['name_service'],"status":False,"message":"data not found file"}
                                                insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'data not found file',token_header)
                                    else:
                                        doc_id = resultselect_attm_file['messageText']['document_Id']
                                        username_sender = resultselect_attm_file['messageText']['sender_username']
                                        document_Type = resultselect_attm_file['messageText']['document_Type']
                                        folder_name = resultselect_attm_file['messageText']['folder_name']
                                        pathtemp_eform = ""
                                        json_data_details = ""
                                        pathnonperfix = ""
                                        if folder_name != None:
                                            url = url_ip_eform + '/api/v1/get_attract_file/?folder_name=' + folder_name
                                            result_eform = callGET_other(url)
                                            folder_name = str(uuid.uuid4())
                                            pathtemp_eform = path_global_1 +'/storage/temp/' + folder_name +'/'
                                            pathnonperfix = '/storage/temp/' + folder_name +'/'
                                            if not os.path.exists(pathtemp_eform):
                                                os.makedirs(pathtemp_eform)
                                            if result_eform['result'] == 'OK':
                                                tmpmessage = result_eform['messageText'].json()
                                                if tmpmessage['result'] == 'OK':
                                                    tmpdata = tmpmessage['messageText'][0]
                                                    pathfolder = tmpdata['folder_path']
                                                    json_data_details = tmpdata['file_name']
                                                    folder_name = tmpdata['folder_name']
                                                    for nz in range(len(json_data_details)):
                                                        tmpfile_name_original = json_data_details[nz]['file_name_original']
                                                        tmpurl_download = json_data_details[nz]['url_download']
                                                        r = requests.get(tmpurl_download,verify=False)
                                                        with open(pathtemp_eform + tmpfile_name_original,'wb') as f: 
                                                            f.write(r.content)
                                                        print(pathtemp_eform + tmpfile_name_original)
                                        if document_Type in list_documentType:
                                            result_file_last_pdf  =select().select_file_sign_last_to_email(sid_code)
                                            if result_file_last_pdf['result'] == 'OK':
                                                pdf_base64_sign = result_file_last_pdf['messageText']
                                                file_name_sign_pdf = result_file_last_pdf['file_name']                                                
                                                r_robot = sftp_robot().send_file_tosftp_new_v2(json_data_details,pathnonperfix,'',document_Type,doc_id,pdf_base64_sign,file_name_sign_pdf,sid_code,get_status_file)
                                                if 'result' in r_robot:
                                                    if r_robot['result'] == 'OK':
                                                        info_r = {"service":data['name_service'],"status":True,"message":"success"}                                                        
                                                        insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'upload sftp complete',token_header)
                                                    else:
                                                        info_r = {"service":data['name_service'],"status":False,"message":r_robot['messageER']}
                                                        insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,str(r_robot['messageER']),token_header)
                                            else:
                                                info_r = {"service":data['name_service'],"status":False,"message":"data not found file"}
                                                insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'data not found file',token_header)
                                        # insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'data not found attachment')]
                        status_service.append(info_r) 
                call_webhookService(sidCode)  
            else:
                call_webhookService(sidCode)
        # print(sid_code,status_service)
        r_update = update_4().update_status_service(sid_code,str(status_service))
        return get_status_file
    except Exception as e:
        print(str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        # return redirect(url_paperless)

def updatePDF(datajson,sid):
    # เดี๊ยวแก้ต่อ
    res_select_check = select().select_pdf_check_forupdate(sid)
    # print(res_select_check)
    if res_select_check['result'] == 'OK':
        res_updatepdf = update().update_pdf_v2(sid,datajson['string_sign'])
        if res_updatepdf['result'] == 'OK':
            return res_updatepdf
    else:
        res_updatepdf = update().update_pdf_v2(sid,datajson['string_sign'])
        if res_updatepdf['result'] == 'OK':
            return res_updatepdf

def process_signning_group_v1(dataJson,token_header,tmpid_process,group_id,email):
    try:
        list_sign_cert = []
        arr_list_result_document = []
        arr_status = []
        arr_sid = []
        tmpstatus = 'ONPROCESS'
        for sid in dataJson['list_sid']:
            data_test = select_data_pdf_beer(sid, dataJson['email'])
            sign_position = data_test['messageText']
            sign_string = dataJson['sign_string']
            email = dataJson['email']
            tmprange = len(dataJson['list_sid'])
            if 'sign_llx' in sign_position and 'sign_lly' in sign_position and 'sign_urx' in sign_position and 'sign_ury' in sign_position and 'sign_page' in sign_position and 'max_page' in sign_position:
                if sign_position['sign_llx'] != '0' and sign_position['sign_lly'] != '0' and sign_position['sign_urx'] != '0' and sign_position['sign_ury'] != '0':
                    res_arraylist = []
                    if sign_position['string_sign'] != None:
                        base64_pdf_String = sign_position['string_sign']
                    else:
                        base64_pdf_String = sign_position['string_pdf']
                    res_list = credentials_list_v2("","","","","",token_header)
                    if res_list['result'] == 'ER' and 'code' in res_list:
                        tmpstatus = 'FAIL'
                        if sid not in arr_sid:
                            arr_sid.append(sid)
                            arr_status.append(tmpstatus)
                            update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,res_list['msg'],'ERSIGN001')
                            arr_list_result_document.append({'sid':sid,'email':email,'status_document':'Fail','errorMessage':'401','step_num':dataJson['Step_Num'],'errorCode':'ERSIGN001'})
                    if res_list['result'] == 'OK':
                        data_msg = res_list['msg']
                        try:
                            totalResult_oneAuth = data_msg['totalResult']
                            if totalResult_oneAuth == 0:
                                tmpstatus = 'FAIL'
                                if sid not in arr_sid:
                                    arr_sid.append(sid)
                                    arr_status.append(tmpstatus)
                                    update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,res_list['msg'],'ERSIGN001')
                                    arr_list_result_document.append({'sid':sid,'email':email,'status_document':'Fail','errorMessage':'sign profile not found' ,'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN001'})
                        except Exception as e:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + str(e)}),200
                    else:
                        tmpstatus = 'FAIL'
                        if sid not in arr_sid:
                            arr_sid.append(sid)
                            arr_status.append(tmpstatus)
                            update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,res_list['msg'],'ERSIGN001')
                            # print({'sid':sid,'email':email,'status_document':'Fail','errorMessage':'List Service Fail' ,'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN001'})
                            arr_list_result_document.append({'sid':sid,'email':email,'status_document':'Fail','errorMessage':'List Service Fail ' + str(res_list['code']) ,'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN001'})
                    
                    type_certifyLevel = ''
                    try:
                        if res_list['result'] == 'OK':
                            res_arraylist.append({'result_listService':res_list})
                            credentialId = res_list['msg']['credentials'][0]['credentialId']
                            res_authorize = credentials_authorize_v2(credentialId,"","","","","","","",token_header)
                            if res_authorize['result'] == 'OK':
                                res_arraylist.append({'result_authorizeService':res_authorize})
                                sadData = res_authorize['msg']['sad']
                                if int(sign_position['sign_page']) == int(sign_position['max_page']):
                                    if int(dataJson['Step_Num']) == int(dataJson['max_Step']):
                                        type_certifyLevel = 'CERTIFY'
                                    else:
                                        type_certifyLevel = 'NON-CERTIFY'
                                else:
                                    if int(dataJson['Step_Num']) == int(dataJson['max_Step']):
                                        type_certifyLevel = 'CERTIFY'
                                    else:
                                        type_certifyLevel = 'NON-CERTIFY'
                                # print(sign_position)
                                # return ''
                                res_signPdf = signing_pdfSigning_v3(base64_pdf_String,sadData,"","","",type_certifyLevel,"","","","","","",token_header,sign_position,sign_string)
                                if res_signPdf['result'] == 'OK':
                                    res_arraylist.append({'result_signPdfService':res_signPdf})
                                    tmppdfSign = res_signPdf['msg']['pdfData']
                                    # print(res_signPdf)
                                    # print('success')
                                    # return ''
                                    result_update_pdf = updatePDF({'sid_id_file': sign_position['file_id'], 'string_sign': tmppdfSign},sid)
                                    updatepdf_image(tmppdfSign,sid)
                                    check_update = update().update_step_v4(sid,dataJson['email'],'A03','Complete',str(dataJson['Step_Num']),0.0,0.0,'')
                                    result_function = other_service_cost(sid,token_header)
                                    list_sign_cert.append({'result':'OK','messageText':res_arraylist,'status_Code':200,'messageER':None,'messageService':type_certifyLevel, 'result_update_pdf': result_update_pdf})
                                    tmpstatus = 'SUCCESS'
                                    if sid not in arr_sid:
                                        arr_sid.append(sid)
                                        arr_status.append(tmpstatus)
                                        update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,None,None)
                                        arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Complete','errorMessage':None,'step_num':dataJson['Step_Num'],'errorCode':None})
                                else:
                                    tmpstatus = 'FAIL'
                                    if sid not in arr_sid:
                                        arr_sid.append(sid)
                                        arr_status.append(tmpstatus)
                                        update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,res_signPdf['msg'],'ERSIGN001')
                                        arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'signPdf Service ' + res_signPdf['msg'],'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN001'})
                            else:
                                tmpstatus = 'FAIL'
                                if sid not in arr_sid:
                                    arr_sid.append(sid)
                                    arr_status.append(tmpstatus)
                                    update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,res_authorize['msg'],'ERSIGN002')
                                    arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'Authorize Service ' + res_authorize['msg'],'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN002'})
                        else:
                            tmpstatus = 'FAIL'
                            if sid not in arr_sid:
                                arr_sid.append(sid)
                                arr_status.append(tmpstatus)
                                update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,res_list['msg'],'ERSIGN003')
                                arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'list Service ' + res_list['msg'],'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN003'})
                    except Exception as ex:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        tmpstatus = 'FAIL'
                        if sid not in arr_sid:
                            arr_sid.append(sid)
                            arr_status.append(tmpstatus)
                            update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,'Exception ' + str(ex) +str(exc_type) + str(fname) + str(exc_tb.tb_lineno),'ERSIGN999')
                            arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'Exception ' + str(ex) +str(exc_type) + str(fname) + str(exc_tb.tb_lineno),'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN999'})
                    
                else:
                    check_update = update().update_step_v4(sid,dataJson['email'],'A03','Approve',str(dataJson['Step_Num']),0.0,0.0,'')
                    result_function = other_service_cost(sid,token_header)
                    tmpstatus = 'SUCCESS'
                    if sid not in arr_sid:
                        arr_sid.append(sid)
                        arr_status.append(tmpstatus)
                        update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,None,None)
                        arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Complete','errorMessage':None,'step_num':dataJson['Step_Num'],'errorCode':None})

            else:
                tmpstatus = 'FAIL'
                if sid not in arr_sid:
                    arr_sid.append(sid)
                    arr_status.append(tmpstatus)
                    update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,'Parameter incorrect','ERSIGN404')
                    arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'Parameter incorrect','step_num':dataJson['Step_Num'],'errorCode':'ERSIGN404'})
            
        # thread = threading.Thread(target=do_work, kwargs={'dataJson': dataJson, 'token_header': token_header})
        # thread.start()
        resultUpdate = update_3().update_process_id_log_status_v1(tmpid_process,'SIGN',tmpstatus,str(arr_list_result_document),group_id,email)
        # tb_group_document
        # tmprange = 0
        if tmprange == len(arr_list_result_document):
            update_2().update_status_ingroup_v1(dataJson['group_id'],email)
            result_checkstatus = select_3().select_querystatus_group_v1(dataJson['group_id'])
            # print(result_checkstatus)
            if result_checkstatus['result'] == 'OK':
                tmpmessage = result_checkstatus['messageText']
                tmp_email_middle = result_checkstatus['email_middle']
                # print(tmp_email_middle)
                tmp_document_type = result_checkstatus['document_type']
                if tmpmessage == 'N':
                    if arr_status.count('SUCCESS') == len(dataJson['list_sid']):
                        unique_folderFilename = dataJson['group_id']
                        chat_sender_group_v1(dataJson['group_id'],None)
                        if tmp_document_type == 'SCS' or tmp_document_type == 'SCST' or tmp_document_type == 'CS':
                            call_service_BI(dataJson['group_id'],'','','','','','')
                else:
                    if arr_status.count('SUCCESS') == len(dataJson['list_sid']):
                        result_select_email = select().select_datajson_toemail(dataJson['list_sid'])
                        if tmp_email_middle != None:
                            mail().sendEmail_center_group(dataJson['list_sid'],tmp_email_middle,tmp_document_type)
                        chat_sender_group_v1(dataJson['group_id'],None)
                        if tmp_document_type == 'SCS' or tmp_document_type == 'SCST' or tmp_document_type == 'CS':
                            call_service_BI(dataJson['group_id'],'','','','Approve','','')
                        if tmp_document_type == 'TSFN' or tmp_document_type == 'SFN':
                            call_service_pettycash_v1(None,dataJson['group_id'])
            print('success')
        else:
            tmpstatus = 'FAIL'
            # update_3().update_process_onprocess_status_v1(tmpid_process,email,"",tmpstatus,'Process Fail','PGS01')
            resultUpdate = update_3().update_process_id_log_status_v1(tmpid_process,'SIGN',tmpstatus,str(arr_list_result_document),group_id,email)
        return jsonify({'result':'OK','messageText':dataJson['list_sid'],'status_Code':200,'messageER':None}),200
    except Exception as ex:        
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        tmpstatus = 'FAIL'
        if sid not in arr_sid:
            arr_sid.append(sid)
            arr_status.append(tmpstatus)
            update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,'Exception ' + str(ex) +str(exc_type) + str(fname) + str(exc_tb.tb_lineno),'ERSIGN999')
            arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'Exception ' + str(ex) +str(exc_type) + str(fname) + str(exc_tb.tb_lineno),'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN999'})

# no_document
def process_signning_group_version2(dataJson,token_header,tmpid_process,group_id,email):
    try:
        list_sign_cert = []
        arr_list_result_document = []
        arr_status = []
        arr_sid = []
        arrSidSuccess = []
        tmpstatus = 'ONPROCESS'
        for idx, sid in enumerate(dataJson['list_sid']):
            data_test = select_data_pdf_beer(sid, dataJson['email'])
            sign_position = data_test['messageText']
            sign_string = dataJson['sign_string']
            email = dataJson['email']
            tmpstep_num = dataJson['Step_Num'][idx]
            tmpmax_Step = dataJson['max_Step'][idx]
            if int(tmpstep_num) == int(tmpmax_Step):
                arrSidSuccess.append(sid)
            if 'sign_llx' in sign_position and 'sign_lly' in sign_position and 'sign_urx' in sign_position and 'sign_ury' in sign_position and 'sign_page' in sign_position and 'max_page' in sign_position:
                if sign_position['sign_llx'] != '0' and sign_position['sign_lly'] != '0' and sign_position['sign_urx'] != '0' and sign_position['sign_ury'] != '0':
                    res_arraylist = []
                    if sign_position['string_sign'] != None:
                        base64_pdf_String = sign_position['string_sign']
                    else:
                        base64_pdf_String = sign_position['string_pdf']
                    res_list = credentials_list_v2("","","","","",token_header)
                    if res_list['result'] == 'ER' and 'code' in res_list:
                        tmpstatus = 'FAIL'
                        if sid not in arr_sid:
                            arr_sid.append(sid)
                            arr_status.append(tmpstatus)
                            update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,res_list['msg'],'ERSIGN001')
                            arr_list_result_document.append({'sid':sid,'email':email,'status_document':'Fail','errorMessage':'401','step_num':tmpstep_num,'errorCode':'ERSIGN001'})
                    if res_list['result'] == 'OK':
                        data_msg = res_list['msg']
                        try:
                            totalResult_oneAuth = data_msg['totalResult']
                            if totalResult_oneAuth == 0:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'sign profile not found'}),200
                            else:
                                pass
                        except Exception as e:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + str(e)}),200
                    else:
                        tmpstatus = 'FAIL'
                        if sid not in arr_sid:
                            arr_sid.append(sid)
                            arr_status.append(tmpstatus)
                            update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,res_list['msg'],'ERSIGN001')
                            # print({'sid':sid,'email':email,'status_document':'Fail','errorMessage':'List Service Fail' ,'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN001'})
                            arr_list_result_document.append({'sid':sid,'email':email,'status_document':'Fail','errorMessage':'List Service Fail ' + str(res_list['code']) ,'step_num':tmpstep_num,'errorCode':'ERSIGN001'})
                    
                    type_certifyLevel = ''
                    try:
                        if res_list['result'] == 'OK':
                            res_arraylist.append({'result_listService':res_list})
                            credentialId = res_list['msg']['credentials'][0]['credentialId']
                            res_authorize = credentials_authorize_v2(credentialId,"","","","","","","",token_header)
                            if res_authorize['result'] == 'OK':
                                res_arraylist.append({'result_authorizeService':res_authorize})
                                sadData = res_authorize['msg']['sad']
                                if int(sign_position['sign_page']) == int(sign_position['max_page']):
                                    if int(tmpstep_num) == int(tmpmax_Step):
                                        type_certifyLevel = 'CERTIFY'
                                    else:
                                        type_certifyLevel = 'NON-CERTIFY'
                                else:
                                    if int(tmpstep_num) == int(tmpmax_Step):
                                        type_certifyLevel = 'CERTIFY'
                                    else:
                                        type_certifyLevel = 'NON-CERTIFY'
                                # print(sign_position)
                                # return ''
                                res_signPdf = signing_pdfSigning_v3(base64_pdf_String,sadData,"","","",type_certifyLevel,"","","","","","",token_header,sign_position,sign_string)
                                if res_signPdf['result'] == 'OK':
                                    res_arraylist.append({'result_signPdfService':res_signPdf})
                                    tmppdfSign = res_signPdf['msg']['pdfData']
                                    # print(res_signPdf)
                                    # print('success')
                                    # return ''
                                    result_update_pdf = updatePDF_for_groupV2({'sid_id_file': sign_position['file_id'], 'string_sign': tmppdfSign},sid)
                                    updatepdf_image(tmppdfSign,sid)
                                    # print('tmpstep_num ' , tmpstep_num, ' tmpmax_Step' , tmpmax_Step)
                                    # print(sid,dataJson['email'],'A03','Complete',tmpstep_num,0.0,0.0,'')
                                    check_update = update().update_step_v4(sid,dataJson['email'],'A03','Complete',str(tmpstep_num),0.0,0.0,'')
                                    # print(check_update)
                                    # result_function = other_service_cost(sid,token_header)
                                    list_sign_cert.append({'result':'OK','messageText':res_arraylist,'status_Code':200,'messageER':None,'messageService':type_certifyLevel, 'result_update_pdf': result_update_pdf})
                                    tmpstatus = 'SUCCESS'
                                    if sid not in arr_sid:
                                        arr_sid.append(sid)
                                        arr_status.append(tmpstatus)
                                        update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,None,None)
                                        arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Complete','errorMessage':None,'step_num':tmpstep_num,'errorCode':None})
                                else:
                                    tmpstatus = 'FAIL'
                                    if sid not in arr_sid:
                                        arr_sid.append(sid)
                                        arr_status.append(tmpstatus)
                                        update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,res_signPdf['msg'],'ERSIGN001')
                                        arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'signPdf Service ' + res_signPdf['msg'],'step_num':tmpstep_num,'errorCode':'ERSIGN001'})
                            else:
                                tmpstatus = 'FAIL'
                                if sid not in arr_sid:
                                    arr_sid.append(sid)
                                    arr_status.append(tmpstatus)
                                    update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,res_authorize['msg'],'ERSIGN002')
                                    arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'Authorize Service ' + res_authorize['msg'],'step_num':tmpstep_num,'errorCode':'ERSIGN002'})
                        else:
                            tmpstatus = 'FAIL'
                            if sid not in arr_sid:
                                arr_sid.append(sid)
                                arr_status.append(tmpstatus)
                                update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,res_list['msg'],'ERSIGN003')
                                arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'list Service ' + res_list['msg'],'step_num':tmpstep_num,'errorCode':'ERSIGN003'})
                    except Exception as ex:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        tmpstatus = 'FAIL'
                        if sid not in arr_sid:
                            arr_sid.append(sid)
                            arr_status.append(tmpstatus)
                            update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,'Exception ' + str(ex) +str(exc_type) + str(fname) + str(exc_tb.tb_lineno),'ERSIGN999')
                            arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'Exception ' + str(ex) +str(exc_type) + str(fname) + str(exc_tb.tb_lineno),'step_num':tmpstep_num,'errorCode':'ERSIGN999'})
                    
                else:
                    check_update = update().update_step_v4(sid,dataJson['email'],'A03','Approve',str(tmpstep_num),0.0,0.0,'')
                    result_function = other_service_cost(sid,token_header)
                    tmpstatus = 'SUCCESS'
                    if sid not in arr_sid:
                        arr_sid.append(sid)
                        arr_status.append(tmpstatus)
                        update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,None,None)
                        arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Complete','errorMessage':None,'step_num':tmpstep_num,'errorCode':None})

            else:
                tmpstatus = 'FAIL'
                if sid not in arr_sid:
                    arr_sid.append(sid)
                    arr_status.append(tmpstatus)
                    update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,'Parameter incorrect','ERSIGN404')
                    arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'Parameter incorrect','step_num':tmpstep_num,'errorCode':'ERSIGN404'})
        # 
        
        # for k in range(len(arrSidSuccess)):
        #     tmp_sidcode = arrSidSuccess[k]
        #     indexdoc = sid_group.index(tmp_sidcode)
        #     if email_middle[indexdoc]['email_middle'] != '':
        #         email_middle[indexdoc]['email_middle'] = eval(email_middle[indexdoc]['email_middle'])
        #         result=mail().sendMailCenter_group_v2(([sid_group[indexdoc]]),(email_middle[indexdoc]['email_middle']))
        # 
        # thread = threading.Thread(target=do_work, kwargs={'dataJson': dataJson, 'token_header': token_header})
        # thread.start()
        resultUpdate = update_3().update_process_id_log_status_v2(tmpid_process,'SIGN',tmpstatus,str(arr_list_result_document),group_id,email)
        # tb_group_document
        update_2().update_status_ingroup_v2(dataJson['group_id'],email)

        result_checkstatus = select_3().select_querystatus_group_version2(dataJson['group_id'])
        result = select_2().select_infoGroup_v2(group_id)
        result = result[0]
        # print('result',(result))
        sid_group = result['sid_group']
        email_middle = result['email_middle']
        doctype_group = result['doctype_group']
        bizinfo_group = result['bizinfo_group']
        arr_filterDoctype = []
        for p in range(len(arrSidSuccess)):
            tmp_sidcode = arrSidSuccess[p]
            indexdoc = sid_group.index(tmp_sidcode)
            idx_doctype = doctype_group[indexdoc]
            idx_bizinfo = bizinfo_group[indexdoc]
            idx_key = idx_doctype['document_type'] + idx_bizinfo['tax_id']
            idx_emailmiddle = email_middle[indexdoc]
            if (idx_key) in str(arr_filterDoctype):
                for u in range(len(arr_filterDoctype)):
                    # print('idx_doctype',idx_doctype)
                    if idx_doctype['document_type'] == arr_filterDoctype[u]['document_type'] and idx_bizinfo['tax_id'] == arr_filterDoctype[u]['bizinfo_group']:
                        arr_filterDoctype[u]['sidfilter'].append(tmp_sidcode)
            else:
                temp = {
                    'document_type' : idx_doctype['document_type'] ,
                    'sidfilter' : [tmp_sidcode],
                    'email_middle' : idx_emailmiddle,
                    'bizinfo_group' : idx_bizinfo['tax_id'],
                    'key': idx_key
                }
                arr_filterDoctype.append(temp)
        for ii in range(len(arr_filterDoctype)):
            if arr_filterDoctype[ii]['email_middle'] != '':
                arr_filterDoctype[ii]['email_middle']['email_middle'] = eval(arr_filterDoctype[ii]['email_middle']['email_middle'])
                result=mail().sendMailCenter_group_v2(arr_filterDoctype[ii]['sidfilter'],arr_filterDoctype[ii]['email_middle']['email_middle'])
        chat_sender_group_v2(str(dataJson['group_id']),None)

        if result_checkstatus['result'] == 'OK':
            tmpmessage = result_checkstatus['messageText']
            tmp_email_middle = result_checkstatus['email_middle']
            # tmp_document_type = result_checkstatus['document_type']
            if tmpmessage == 'N':
                if arr_status.count('SUCCESS') == len(dataJson['list_sid']):
                    unique_folderFilename = dataJson['group_id']
                    # chat_sender_group_v1(dataJson['group_id'],None)
                    # if tmp_document_type == 'SCS' or tmp_document_type == 'SCST' or tmp_document_type == 'CS':
                    #     call_service_BI(dataJson['group_id'],'','','','','','')
            else:
                if arr_status.count('SUCCESS') == len(dataJson['list_sid']):
                    result_select_email = select().select_datajson_toemail(dataJson['list_sid'])
                    # if tmp_email_middle != None:
                    #     mail().sendEmail_center_group(dataJson['list_sid'],tmp_email_middle,tmp_document_type)
                    # chat_sender_group_v1(dataJson['group_id'],None)
                    # if tmp_document_type == 'SCS' or tmp_document_type == 'SCST':
                    #     call_service_BI(dataJson['group_id'],'','','','Approve','','')
        return jsonify({'result':'OK','messageText':dataJson['list_sid'],'status_Code':200,'messageER':None}),200
    except Exception as ex:      
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        tmpstatus = 'FAIL'
        if sid not in arr_sid:
            arr_sid.append(sid)
            arr_status.append(tmpstatus)
            update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,'Exception ' + str(ex) +str(exc_type) + str(fname) + str(exc_tb.tb_lineno),'ERSIGN999')
            arr_list_result_document.append({'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'Exception ' + str(ex) +str(exc_type) + str(fname) + str(exc_tb.tb_lineno),'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN999'})

def process_update_group_v1(group_id,email,step_num,sign_base):
    try:
        sql = '''SELECT * FROM "public"."tb_group_document" WHERE "id" = :tmpgroup_id '''        
        connection = engine.connect()
        result = connection.execute(text(sql),tmpgroup_id=group_id)
        data = [dict(row) for row in result]
        tmpdata = data[0]
        # print(tmpdata.keys())
        tmpsid = eval(tmpdata['sid_group'])
        for n in tmpsid:
            sql_update = '''
            SELECT
                tb_pdf_storage.string_sign 
            FROM
                tb_send_detail
                INNER JOIN tb_pdf_storage ON tb_pdf_storage.fid = tb_send_detail.file_id 
            WHERE
                tb_send_detail.step_data_sid = :tmpsid
            '''  
            result_PDF = connection.execute(text(sql_update),tmpsid=n)
            data_PDF = [dict(row) for row in result_PDF]
            tmpdata_PDF = data_PDF[0]
            tmppdfSign = tmpdata_PDF['string_sign']
            # check_update = update_4().update_step_new_v1(n,email,'A03','Complete',str(step_num),0.0,0.0,'',tmppdfSign)
            url = 'https://paperless.one.th/paper_less/api/convert2/pdf_image/' + n
            info = {
                "base64_PDF":tmppdfSign
            }
            callPost(url,info)
            # updatepdf_image_backgroud(tmppdfSign,n)
    except Exception as e:
        return {'result':'OK','messageText':str(e)}
    finally:
        connection.close()

@status_methods.route("/update_group",methods=['POST'])
def update_group_api_v1():
    dataJson = request.json
    if 'group_id' in dataJson:
        r = process_update_group_v1(dataJson['group_id'],dataJson['email'],dataJson['step_num'],dataJson['sign_base'])
    return jsonify(r)

def process_signning_group_v2(dataJson):
    try:
        list_sign_cert = []
        sid = dataJson['sid']
        data_test = select_data_pdf_beer(sid, dataJson['email'])
        sign_position = data_test['messageText']
        sign_string = dataJson['sign_string']
        email = dataJson['email']
        token_header = dataJson['token_header']
        tmpid_process = dataJson['tmpid_process']
        group_id = dataJson['group_id']
        tmprange = len(dataJson)
        if 'sign_llx' in sign_position and 'sign_lly' in sign_position and 'sign_urx' in sign_position and 'sign_ury' in sign_position and 'sign_page' in sign_position and 'max_page' in sign_position:
            if sign_position['sign_llx'] != '0' and sign_position['sign_lly'] != '0' and sign_position['sign_urx'] != '0' and sign_position['sign_ury'] != '0':
                res_arraylist = []
                if sign_position['string_sign'] != None:
                    base64_pdf_String = sign_position['string_sign']
                else:
                    base64_pdf_String = sign_position['string_pdf']
                res_list = credentials_list_v2("","","","","",token_header)
                if res_list['result'] == 'ER' and 'code' in res_list:
                    return {'sid':sid,'email':email,'status_document':'Fail','errorMessage':'401','step_num':dataJson['Step_Num'],'errorCode':'ERSIGN001'}
                if res_list['result'] == 'OK':
                    data_msg = res_list['msg']
                    try:
                        totalResult_oneAuth = data_msg['totalResult']
                        if totalResult_oneAuth == 0:
                            tmpstatus = 'FAIL'
                            return {'sid':sid,'email':email,'status_document':'Fail','errorMessage':'sign profile not found' ,'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN001'}
                    except Exception as e:
                        return {'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + str(e)}
                else:
                    tmpstatus = 'FAIL'
                    return {'sid':sid,'email':email,'status_document':'Fail','errorMessage':'List Service Fail ' + str(res_list['code']) ,'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN001'}
                
                type_certifyLevel = ''
                try:
                    if res_list['result'] == 'OK':
                        res_arraylist.append({'result_listService':res_list})
                        credentialId = res_list['msg']['credentials'][0]['credentialId']
                        if dataJson['email'] == 'morragot.ku@one.th':
                            credentialId = res_list['msg']['credentials'][1]['credentialId']
                        res_authorize = credentials_authorize_v2(credentialId,"","","","","","","",token_header)
                        if res_authorize['result'] == 'OK':
                            res_arraylist.append({'result_authorizeService':res_authorize})
                            sadData = res_authorize['msg']['sad']
                            if int(sign_position['sign_page']) == int(sign_position['max_page']):
                                if int(dataJson['Step_Num']) == int(dataJson['max_Step']):
                                    type_certifyLevel = 'CERTIFY'
                                else:
                                    type_certifyLevel = 'NON-CERTIFY'
                            else:
                                if int(dataJson['Step_Num']) == int(dataJson['max_Step']):
                                    type_certifyLevel = 'CERTIFY'
                                else:
                                    type_certifyLevel = 'NON-CERTIFY'
                            res_signPdf = signing_pdfSigning_v3(base64_pdf_String,sadData,"","","",type_certifyLevel,"","","","","","",token_header,sign_position,sign_string)
                            if res_signPdf['result'] == 'OK':
                                res_arraylist.append({'result_signPdfService':res_signPdf})
                                tmppdfSign = res_signPdf['msg']['pdfData']
                                # result_update_pdf = updatePDF({'sid_id_file': sign_position['file_id'], 'string_sign': tmppdfSign},sid)
                                check_update = update_4().update_step_new_v1(sid,dataJson['email'],'A03','Complete',str(dataJson['Step_Num']),0.0,0.0,'',tmppdfSign)
                                updatepdf_image_backgroud(tmppdfSign,sid)
                                other_service_cost(sid,token_header)
                                # list_sign_cert.append({'result':'OK','messageText':res_arraylist,'status_Code':200,'messageER':None,'messageService':type_certifyLevel, 'result_update_pdf': result_update_pdf})
                                tmpstatus = 'SUCCESS'
                                return {'sid':sid,'email':dataJson['email'],'status_document':'Complete','errorMessage':None,'step_num':dataJson['Step_Num'],'errorCode':None}
                            else:
                                tmpstatus = 'FAIL'
                                return {'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'signPdf Service ' + res_signPdf['msg'],'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN001'}
                        else:
                            tmpstatus = 'FAIL'
                            return {'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'Authorize Service ' + res_authorize['msg'],'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN002'}
                    else:
                        tmpstatus = 'FAIL'
                        return {'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'list Service ' + res_list['msg'],'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN003'}
                except Exception as ex:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    tmpstatus = 'FAIL'
                    return {'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'Exception ' + str(ex) +str(exc_type) + str(fname) + str(exc_tb.tb_lineno),'step_num':dataJson['Step_Num'],'errorCode':'ERSIGN999'}
            else:
                check_update = update().update_step_v4(sid,dataJson['email'],'A03','Approve',str(dataJson['Step_Num']),0.0,0.0,'')
                result_function = other_service_cost(sid,token_header)
                tmpstatus = 'SUCCESS'
                return {'sid':sid,'email':dataJson['email'],'status_document':'Complete','errorMessage':None,'step_num':dataJson['Step_Num'],'errorCode':None}
        else:
            tmpstatus = 'FAIL'
            return {'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':'Parameter incorrect','step_num':dataJson['Step_Num'],'errorCode':'ERSIGN404'}
        # return jsonify({'result':'OK','messageText':dataJson['list_sid'],'status_Code':200,'messageER':None}),200
    except Exception as e:
        return {'sid':sid,'email':dataJson['email'],'status_document':'Fail','errorMessage':str(e),'step_num':dataJson['Step_Num'],'errorCode':None}
    # return arr_tmp['sid']

def start_thread_processSign_v1(dataJson,tmpid_process,group_id,email,count_doc,doc_tmp):
    try:
        status_fail = False
        arr_status = []
        arr_sum_status = []
        arr_sum_sid = []
        # print(dataJson[0]['token_header'])
        token_header = dataJson[0]['token_header']
        # print(time.time())
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
            res = ex.map(process_signning_group_v2, dataJson)
            arr_status = (list(res))

        if count_doc == len(arr_status):
            for n in range(len(arr_status)):
                tmpsid = arr_status[n]['sid']
                if 'status_document' in arr_status[n]:
                    statustmp = arr_status[n]['status_document']
                    arr_sum_status.append(statustmp)
                    if statustmp == 'Fail':
                        status_fail = True
                    # else:
                    #     if tmpsid not in arr_sum_sid:
                    #         arr_sum_sid.append(tmpsid)
                    #         result_function = other_service_cost(tmpsid,token_header)
            # print(status_fail)
            resultUpdate = update_3().update_process_id_log_status_v1(tmpid_process,'SIGN','SUCCESS',str(arr_status),group_id,email)
            if status_fail==True:
                resultUpdate = update_3().update_process_id_log_status_v1(tmpid_process,'SIGN','FAIL',str(arr_status),group_id,email)
            else:
                update_2().update_status_ingroup_v1(group_id,email)            
            result_checkstatus = select_3().select_querystatus_group_v1(group_id)
            if result_checkstatus['result'] == 'OK':
                tmpmessage = result_checkstatus['messageText']
                tmp_email_middle = result_checkstatus['email_middle']
                tmp_document_type = result_checkstatus['document_type']
                if tmpmessage == 'N':
                    if statustmp.count('Complete') == count_doc:
                        unique_folderFilename = group_id
                        chat_sender_group_v1(group_id,None)
                        if tmp_document_type == 'SCS' or tmp_document_type == 'SCST' or tmp_document_type == 'CS':
                            call_service_BI(group_id,'','','','','','')
                else:
                    result_select_email = select().select_datajson_toemail(doc_tmp)
                    if tmp_email_middle != None:
                        mail().sendEmail_center_group(doc_tmp,tmp_email_middle,tmp_document_type)
                    chat_sender_group_v1(group_id,None)
                    if tmp_document_type == 'SCS' or tmp_document_type == 'SCST' or tmp_document_type == 'CS':
                        call_service_BI(group_id,'','','','Approve','','')
                    if tmp_document_type == 'TSFN' or tmp_document_type == 'SFN':
                        call_service_pettycash_v1(None,group_id)    
            call_webhookService_group(group_id)
            resultUpdate = update_3().update_process_id_log_status_v1(tmpid_process,'SIGN','SUCCESS',str(arr_status),group_id,email)
            print('success')
        else:
            tmpstatus = 'FAIL'
            resultUpdate = update_3().update_process_id_log_status_v1(tmpid_process,'SIGN',tmpstatus,str(arr_status),group_id,email)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(str(e))

# no_document
@status_methods.route('/api/sign_auth/group_v2',methods=['POST'])
# @token_required_v3
def signning_groupversion2():
    if request.method == 'POST':
        arr_list_result_document = []
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'list_sid' in dataJson and 'email' in dataJson and 'userName' in dataJson and 'sign_string' in dataJson and 'max_Step' in dataJson and 'Step_Num' in dataJson and 'group_id' in dataJson and  len(dataJson) == 7:
            tmpemailuser = dataJson['email']
            url = '/api/sign_auth/group_v2'
            for j in range(len(dataJson['list_sid'])):
                arr_list_result_document.append({'sid':dataJson['list_sid'][j],'email':tmpemailuser,'status_document':'ONPROCESS','errorMessage':None,'step_num':dataJson['Step_Num'],'errorCode':None})
            result_insert = insert_3().insert_process_request_v1('SIGN',str(arr_list_result_document),url,dataJson['group_id'],tmpemailuser)
            tmpid_process = None
            if result_insert['result'] == 'OK':
                tmpid_process = result_insert['messageText']['id']
            result_singnning = executor.submit(process_signning_group_version2, dataJson,token_header,tmpid_process,dataJson['group_id'],dataJson['email'])
            
            # print(result_singnning.result())
            return jsonify({'result':'OK','messageText':{'message':'on process','data':tmpid_process},'messageER':None,'status_Code':200}),200


@status_methods.route('/api/v2/sign_auth/group_sum',methods=['POST'])
# @token_required_v3
def sign_authv2_beer1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'list_sid' in dataJson and 'email' in dataJson and 'userName' in dataJson and 'sign_string' in dataJson and 'max_Step' in dataJson and 'Step_Num' in dataJson and 'group_id' in dataJson and  len(dataJson) == 7:
            # def do_work(dataJson, token_header):
            list_sign_cert = []
            result_process_success = []
            result_process_fail = []
            for sid in dataJson['list_sid']:
                result_status = select_status_file_forSign(sid)
                if result_status['result'] == 'OK':
                    tmpdatadoc = result_status['messageText']
                    if 'document_status' in tmpdatadoc:
                        tmpstatus_doc = tmpdatadoc['document_status']
                        if tmpstatus_doc == 'N':
                            data_test = select_data_pdf_beer(sid, dataJson['email'])
                            sign_position = data_test['messageText']
                            sign_string = dataJson['sign_string']
                            if 'sign_llx' in sign_position and 'sign_lly' in sign_position and 'sign_urx' in sign_position and 'sign_ury' in sign_position and 'sign_page' in sign_position and 'max_page' in sign_position:
                                if sign_position['sign_llx'] != '0' and sign_position['sign_lly'] != '0' and sign_position['sign_urx'] != '0' and sign_position['sign_ury'] != '0':
                                    res_arraylist = []
                                    if sign_position['string_sign'] != None:
                                        base64_pdf_String = sign_position['string_sign']
                                    else:
                                        base64_pdf_String = sign_position['string_pdf']
                                    res_list = credentials_list_v2("","","","","",token_header)
                                    if res_list['result'] == 'ER' and 'code' in res_list:
                                        abort(401)
                                    if res_list['result'] == 'OK':
                                        data_msg = res_list['msg']
                                        try:
                                            totalResult_oneAuth = data_msg['totalResult']
                                            if totalResult_oneAuth == 0:
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'sign profile not found'}),200
                                            else:
                                                pass
                                        except Exception as e:
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + str(e)}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! 007'}),200
                                    type_certifyLevel = ''
                                    try:
                                        if res_list['result'] == 'OK':
                                            res_arraylist.append({'result_listService':res_list})
                                            credentialId = res_list['msg']['credentials'][0]['credentialId']
                                            res_authorize = credentials_authorize_v2(credentialId,"","","","","","","",token_header)
                                            if res_authorize['result'] == 'OK':
                                                res_arraylist.append({'result_authorizeService':res_authorize})
                                                sadData = res_authorize['msg']['sad']
                                                if int(sign_position['sign_page']) == int(sign_position['max_page']):
                                                    if int(dataJson['Step_Num']) == int(dataJson['max_Step']):
                                                        type_certifyLevel = 'CERTIFY'
                                                    else:
                                                        type_certifyLevel = 'NON-CERTIFY'
                                                else:
                                                    if int(dataJson['Step_Num']) == int(dataJson['max_Step']):
                                                        type_certifyLevel = 'NON-CERTIFY'
                                                    else:
                                                        type_certifyLevel = 'NON-CERTIFY'
                                                # print(sign_position)
                                                # return ''
                                                res_signPdf = signing_pdfSigning_v3(base64_pdf_String,sadData,"","","",type_certifyLevel,"","","","","","",token_header,sign_position,sign_string)

                                                if res_signPdf['result'] == 'OK':
                                                    res_arraylist.append({'result_signPdfService':res_signPdf})
                                                    tmppdfSign = res_signPdf['msg']['pdfData']
                                                    # print(res_signPdf)
                                                    # print('success')
                                                    # return ''
                                                    result_update_pdf = updatePDF({'sid_id_file': sign_position['file_id'], 'string_sign': tmppdfSign},sid)
                                                    updatepdf_image(tmppdfSign,sid)
                                                    check_update = update().update_step_v4(sid,dataJson['email'],'A03','Complete',str(dataJson['Step_Num']),0.0,0.0,'')
                                                    
                                                    result_function = other_service_cost(sid,token_header)
                                                    result_process_success.append({'sid':sid,'message':'success'})
                                                    list_sign_cert.append({'result':'OK','messageText':res_arraylist,'status_Code':200,'messageER':None,'messageService':type_certifyLevel, 'result_update_pdf': result_update_pdf})
                                                else:
                                                    result_process_fail.append({'sid':sid,'message':'fail signPdf Service Error!'})
                                                    # return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'signPdf Service Error!'}),200
                                            else:
                                                result_process_fail.append({'sid':sid,'message':'fail Authorize Service Error!' + res_authorize['msg']})
                                                # return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Authorize Service Error!' + res_authorize['msg']}),200
                                        else:
                                            result_process_fail.append({'sid':sid,'message':'fail list Service Error!' + res_list['msg']})
                                            # return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + res_list['msg']}),200
                                    except Exception as ex:
                                        exc_type, exc_obj, exc_tb = sys.exc_info()
                                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                        print(exc_type, fname, exc_tb.tb_lineno)
                                        result_process_fail.append({'sid':sid,'message':'fail ' + str(ex)})
                                else:
                                    check_update = update().update_step_v4(sid,dataJson['email'],'A03','Approve',str(dataJson['Step_Num']),0.0,0.0,'')
                                    result_function = other_service_cost(sid,token_header)
                            else:
                                result_process_fail.append({'sid':sid,'message':'parameter incorrect'})
                                # return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
                        else:
                            result_process_fail.append({'sid':sid,'message':'document success'})
            # thread = threading.Thread(target=do_work, kwargs={'dataJson': dataJson, 'token_header': token_header})
            # thread.start()
            unique_folderFilename = dataJson['group_id']
            result_select_email = select().select_datajson_toemail(dataJson['list_sid'])
            path = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
            path_indb = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
            if not os.path.exists(path):
                os.makedirs(path)
            if result_select_email['result'] == 'OK':
                resultTracking = select_3().select_trackinggroup_v1(dataJson['group_id'])
                dataBi = result_select_email['data_bi']
                # info = {
                #     "group_tracking":resultTracking['tracking_group'],
                #     "group_color":resultTracking['group_color'],
                #     "group_detail":dataBi
                # }
                # if type_product == 'prod':
                #     url_BI_logic = url_bi_2 + '/calculate'
                # else:
                #     url_BI_logic = url_bi_2 + '/calculateTest'
                # resultDataBI = callPost_v3(url_BI_logic,info)
                # if resultDataBI['result'] == 'OK':
                #     tmpmessage = resultDataBI['messageText'].json()
                #     if tmpmessage['message'] == 'Success':
                #         tmpdata = tmpmessage['data']
                #         if 'Warning_Detail' in tmpdata:
                #             pathfile = path + unique_folderFilename + '.html'
                #             try:
                #                 with open(pathfile, 'a') as the_file:
                #                     the_file.write(tmpdata['Warning_Detail'])
                #                 update_3().update_HtmlData_Bi_v1(dataJson['group_id'],tmpdata['Warning_Detail'])
                #             except Exception as e:
                #                 pass
            r_chat = chat_sender_group_v1(dataJson['group_id'],None)
            print(r_chat)
            return jsonify({'result':'OK','messageText':{'success':result_process_success,'fail':result_process_fail},'status_Code':200,'messageER':None}),200
        # else:
        #     return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404

@status_methods.route('/api/v4/sign_auth/group_sum',methods=['POST'])
# @token_required_v3
def signning_group_api_v1():
    if request.method == 'POST':
        arr_list_result_document = []
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'list_sid' in dataJson and 'email' in dataJson and 'userName' in dataJson and 'sign_string' in dataJson and 'max_Step' in dataJson and 'Step_Num' in dataJson and 'group_id' in dataJson and  len(dataJson) == 7:
            tmpemailuser = dataJson['email']
            url = '/api/v3/sign_auth/group_sum'
            for j in range(len(dataJson['list_sid'])):
                arr_list_result_document.append({'sid':dataJson['list_sid'][j],'email':tmpemailuser,'status_document':'ONPROCESS','errorMessage':None,'step_num':dataJson['Step_Num'],'errorCode':None})
            result_insert = insert_3().insert_process_request_v1('SIGN',str(arr_list_result_document),url,dataJson['group_id'],tmpemailuser)
            tmpid_process = None
            if result_insert['result'] == 'OK':
                tmpid_process = result_insert['messageText']['id']
            result_singnning = executor.submit(process_signning_group_v1, dataJson,token_header,tmpid_process,dataJson['group_id'],dataJson['email'])
            
            # print(result_singnning.result())
            return jsonify({'result':'OK','messageText':{'message':'on process','data':tmpid_process},'messageER':None,'status_Code':200}),200

@status_methods.route('/api/v3/sign_auth/group_sum',methods=['POST'])
# @token_required_v3
def signning_group_api_v2():
    if request.method == 'POST':
        arr_list_result_document = []
        arr_data = []
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'list_sid' in dataJson and 'email' in dataJson and 'userName' in dataJson and 'sign_string' in dataJson and 'max_Step' in dataJson and 'Step_Num' in dataJson and 'group_id' in dataJson and  len(dataJson) == 7:
            tmpemailuser = dataJson['email']
            url = '/api/v3/sign_auth/group_sum'
            count_doc = len(dataJson['list_sid'])
            doc_tmp = dataJson['list_sid']
            for j in range(len(dataJson['list_sid'])):
                arr_list_result_document.append({'sid':dataJson['list_sid'][j],'email':tmpemailuser,'status_document':'ONPROCESS','errorMessage':None,'step_num':dataJson['Step_Num'],'errorCode':None})
            tmpid_process = None
            result_insert = insert_3().insert_process_request_v1('SIGN',str(arr_list_result_document),url,dataJson['group_id'],tmpemailuser)
            if result_insert['result'] == 'OK':
                tmpid_process = result_insert['messageText']['id']
            for n in range(len(dataJson['list_sid'])):
                info = {
                    'sid':dataJson['list_sid'][n],
                    'email':dataJson['email'],
                    'userName':dataJson['userName'],
                    'sign_string':dataJson['sign_string'],
                    'group_id':dataJson['group_id'],
                    'Step_Num':dataJson['Step_Num'],
                    'max_Step':dataJson['max_Step'],
                    'token_header':token_header,
                    'tmpid_process':tmpid_process
                }
                arr_data.append(info)
            result_singnning = executor.submit(start_thread_processSign_v1, arr_data,tmpid_process,dataJson['group_id'],dataJson['email'],count_doc,doc_tmp)
            return jsonify({'result':'OK','messageText':{'message':'on process','data':tmpid_process},'messageER':None,'status_Code':200}),200

@status_methods.route('/api/v1/sign_auth/group_sum/display',methods=['GET'])
def group_sum_display_api_v1():
    if request.method == 'GET':
        tmpprocessId = request.args.get('processid')
        if tmpprocessId != None:
            result_query = select_3().select_data_processlog_v1(tmpprocessId)
            if result_query['result'] == 'OK':
                jsonresult = {}
                tmparr_sid = []
                tmparr_result = []
                tmpmesage = result_query['messageText'][0]
                tmpstatus = tmpmesage['status']
                jsonresult['process_status'] = tmpstatus 
                tmpdocument_status = eval(tmpmesage['document'])
                # tmpstatus_document = eval(tmpmesage['document'])
                for x in range(len(tmpdocument_status)):
                    if tmpdocument_status[x] != None:
                        if 'sid' in tmpdocument_status[x]:
                            tmparr_json = {}
                            tmparr_json['sid'] = tmpdocument_status[x]['sid']
                            tmparr_json['status_document'] = tmpdocument_status[x]['status_document']
                            tmparr_result.append(tmparr_json)
                jsonresult['process_document_detail'] = tmparr_result
                return jsonify({'result':'OK','messageText':{'message':'success','data':jsonresult},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail','data':None},'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail','data':None},'status_Code':200}),200

@status_methods.route('/api/sign_auth/v2/beer',methods=['POST'])
def sign_authv2_beer():
    if request.method == 'POST':
        param_json = request.json
        list_string_pdf_merge = []
        if 'list_sid' in param_json and 'email' in param_json and 'userName' in param_json and 'sign_string' in param_json  and  len(param_json) == 4:
            for sid in param_json['list_sid']:
                data_test = select_data_pdf_beer(sid, param_json['email'])
                data_set = data_test['messageText']
                page = int(data_set['sign_page'])
                llx = float(data_set['sign_llx'])
                lly = float(data_set['sign_lly'])
                urx = float(data_set['sign_urx'])
                ury = float(data_set['sign_ury'])
                userName = param_json['userName']
                stringPicture = param_json['sign_string']
                stringPdf = data_set['string_pdf']
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
                        list_string_pdf_merge.append(string_pdf_merge['messageText'])
                    else:
                        return jsonify({'result': 'ER', 'messageText':None, 'status_Code': 200,'messageER':string_pdf_merge['messageText']}), 200
                else:
                    return jsonify({'result': 'ER', 'messageText':None, 'status_Code': 200,'messageER':string_Path['messageText']}), 200
            return jsonify({'result': 'OK', 'messageText':list_string_pdf_merge, 'status_Code': 200,'messageER':None}), 200

@status_methods.route('/api/sign_auth/v2/beer111',methods=['POST'])
def sign_authv2_beer111():
    def do_work(value):
        time.sleep(value)
        print('sdffsdfdsfdsfsf')
    thread = threading.Thread(target=do_work, kwargs={'value': 20})
    thread.start()
    return 'started'

@status_methods.route('/api/v1/other_service', methods=['POST'])
def other_service_call_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
                print(token_required)
                username = token_required['username']
                user_id = token_required['user_id']
                tmpemail = token_required['user_id']
            except Exception as ex:
                abort(401)
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'sidCode' in dataJson and len(dataJson) == 1:
            tmpsidcode = dataJson['sidCode']
            # result_insert = insert_3().insert_process_request_v1('SIGN',str(arr_list_result_document),url,None,tmpemailuser)
            # tmpid_process = None
            # if result_insert['result'] == 'OK':
            #     tmpid_process = result_insert['messageText']['id']
            get_status_file = other_service_cost(tmpsidcode,token_required)
            print(get_status_file)
            if 'result' in get_status_file:
                if get_status_file['result'] =='ER':
                    return jsonify({'result':'ER','messageText':None,'messageER':get_status_file['messageER'],'status_Code':200}),200
            return jsonify({'result':'OK','messageText':[{'messageCode':get_status_file}],'messageER':None,'status_Code':200}),200

@status_methods.route('/api/v1/other_arr',methods=['POST'])
def other_arr_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
                username = token_required['username']
                user_id = token_required['user_id']
            except Exception as ex:
                abort(401)
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'sidCode' in dataJson and len(dataJson) == 1:
            tmparrstatus = []
            tmpsidcode = dataJson['sidCode']
            for n in tmpsidcode:
                get_status_file = other_service_cost(n,token_required)
                tmparrstatus.append({'status':get_status_file,'sidcode':n})
                # print(get_status_file)
            if 'result' in get_status_file:
                if get_status_file['result'] =='ER':
                    return jsonify({'result':'ER','messageText':None,'messageER':get_status_file['messageER'],'status_Code':200}),200
            return jsonify({'result':'OK','messageText':tmparrstatus,'messageER':None,'status_Code':200}),200

@status_methods.route('/api/v1/sidothers',methods=['POST'])
def serviceothers_fuc():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            # try:                
            #     token_header = str(token_header).split(' ')[1]
            #     # token_required = token_required_func(token_header)
            #     # username = token_required['username']
            #     # user_id = token_required['user_id']
            # except Exception as ex:
            #     abort(401)
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        tmparr = []
        if 'sidCode' in dataJson and len(dataJson) == 1:
            tmpsidcode = dataJson['sidCode']
            try:
                for n in tmpsidcode:
                    print(n)
                    info = {
                        "sidCode":n
                    }
                    url = 'https://paperless.one.th/paper_less/api/v1/other_service'
                    r = callAuth_post(url,info,token_header)
                    # print(r)
                    # print(n,r['messageText'].text)
                    tmparr.append({'status':str(r['messageText'].text),'sidcode':n})
                    # print(r)
                return jsonify(tmparr)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return jsonify({'result':'ER','message':str(e)})

@status_methods.route('/api/v1/process/display',methods=['GET'])
def process_display_api_v1():
    if request.method == 'GET':
        tmpprocessId = request.args.get('processid')
        if tmpprocessId != None:
            result_query = select_3().select_data_processlog_v1(tmpprocessId)
            if result_query['result'] == 'OK':
                jsonresult = {}
                tmparr_sid = []
                tmparr_result = []
                tmpmesage = result_query['messageText'][0]
                tmpstatus = tmpmesage['status']
                jsonresult['process_status'] = tmpstatus 
                tmpdocument_status = eval(tmpmesage['document'])
                # tmpstatus_document = eval(tmpmesage['document'])
                jsonresult['process_document_detail'] = tmpdocument_status
                return jsonify({'result':'OK','messageText':{'message':'success','data':jsonresult},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail','data':None},'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail','data':None},'status_Code':200}),200