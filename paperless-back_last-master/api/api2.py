#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.callserver import *
from method.convert import *
from method.access import *
from method.publicqrcode import *
from method.document import *
from method.cal_taxId import *
from method.verify import *
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
from api.profile import *
from api.api import *
from method.callwebHook import *
from method.cal_pdf import *

if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less
# myUrl = 'https://devinet-etax.one.th/paper_less_uat'


def callAPI(token,method,path,payload):
    try:
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer"+" "+token
        }
        if method == "POST":
            response = requests.request("POST", url=path, headers=headers, json=payload, verify=False)
        if method == "GET":
            response = requests.get(path, headers=headers, verify=False)
        # print(response,method,path)
        return response
    except Exception as ex:
        return  jsonify({'result':'ER','messageText':ex})

def callAPI_OneChain(method,path,payload):
    try:
        headers = {
            'Content-Type': "application/json"
        }
        if method == "POST":
            response = requests.request("POST", url=path, headers=headers, json=payload, verify=False)
        if method == "GET":
            response = requests.get(path, headers=headers, verify=False)
        # print(response,method,path)
        return response
    except Exception as ex:
        return  jsonify({'result':'ER','messageText':ex})

def convert_pdf_image_v1(foldername,base64pdf):
    # dataJson = request.json
    resul_res = {}
    list_file_name = []
    base64_pdfFile = base64pdf
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
        # print(base64_pdfFile)
        unique_filename = str(uuid.uuid4())
        with open(path +'/'+ unique_filename +".pdf","wb") as f:
            f.write(base64.b64decode((base64_pdfFile)))
    except Exception as e:
        print(str(e))
        print(str(e))
    # print(path +'/'+ unique_filename)
    address_file = path + '/' + unique_filename + '.pdf'
    # print(address_file)
    countpages = 0
    images = convert_from_bytes(open(address_file,'rb').read())
    for i, image in enumerate(images):
        countpages = countpages + 1
    # print(countpages)
    try:
        maxPages = pdf2image._page_count(address_file)
    except Exception as e:
        maxPages = countpages
    print(maxPages)
    #  min(page+10-1,maxPages)
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

def ReadfileLog():
    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    path = path_global_1 +'/storage/log_cal/' + str(st) + '/'
    st_filename = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S-')
    if not os.path.exists(path):
        os.makedirs(path)
    unique_filename = str(uuid.uuid4())
    filename = 'report_paperless' + st_filename + unique_filename
    # workbook = xlsxwriter.Workbook(path + filename + '.xlsx')
    # print(path + filename + '.xlsx')
    with open('C:\\Users\\Jirayu\\Desktop\\sign\\log_request_2020-12-01.log',encoding="utf-8") as fin:
        for line in fin:
            logid = ''
            path = ''
            parameter = ''
            time_ms = ''
            try:
                ts = line.split(' ')[0].replace('[','').replace(']','')
                logid = line.split(' ')[2]
                path = line.split(' ')[3].split('?')[0]
                # print(len(line.split(' ')[3].split('?')))
                if len(line.split(' ')[3].split('?')) > 1:
                    parameter = line.split(' ')[3].split('?')[1]
                time_ms = line.split(' ')[-2]
                info = {
                    "datetime":ts,
                    "id":logid,
                    "path":path,
                    "parameter":parameter,
                    "time":int(time_ms)
                }
                print(info)
            except Exception as e:
                # print(str(e))
                pass
            
    # fo = open("C:\\Users\\Jirayu\\Desktop\\sign\\log_request_2020-12-01.log", "r+")
    # line = fo.readline()
    # print(line)
    # fo.close()

# ReadfileLog()

def getExcel_CS():
    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    sql = ''' 
        SELECT
            "tb_step_data"."update_time",
            "tb_send_detail"."send_time",
            "tb_send_detail"."status",
            "tb_send_detail"."sender_name",
            "tb_send_detail"."sender_email",
            "tb_send_detail"."file_name",
            "tb_send_detail"."doc_id" AS "document_id",
            "tb_send_detail"."document_status",
            "tb_send_detail"."status_details",
            "tb_send_detail"."status_service"
        FROM
            "tb_send_detail"
            LEFT JOIN "tb_doc_detail" ON tb_send_detail.step_data_sid = tb_doc_detail.step_id
            LEFT JOIN "tb_step_data" ON tb_send_detail.step_data_sid = tb_step_data.sid -- WHERE tb_step_data.data_json like '%wanchai.vach@one.th%'
            LEFT JOIN "tb_userProfile" ON "tb_userProfile".p_username = tb_send_detail.send_user 
        WHERE
            biz_info LIKE '%0107544000094%' 
            AND "tb_doc_detail"."documentType" = 'CS'
            
            AND tb_send_detail.send_time >= '2020-12-01 00:00:00' 
            AND tb_send_detail.send_time <= '2020-12-30 23:59:59' 
            ORDER BY-- 	"tb_step_data".update_time DESC
            tb_send_detail.send_time ASC -- 	LIMIT 100
    '''
    connection = engine.connect()
    result = connection.execute(text(sql))
    query_result = [dict(row) for row in result]
    path = path_global_1 +'/storage/excel_report/' + str(st) + '/'
    st_filename = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S-')
    if not os.path.exists(path):
        os.makedirs(path)
    unique_filename = str(uuid.uuid4())
    filename = 'report_paperless' + st_filename + unique_filename
    workbook = xlsxwriter.Workbook(path + filename + '.xlsx')
    print(path + filename + '.xlsx')
    worksheet = workbook.add_worksheet()
    format1 = workbook.add_format()
    format2 = workbook.add_format()
    format2.set_align('center')
    format2.set_align('vcenter')
    format2.font_size = 10
    format2.set_text_wrap()
    cell_format = workbook.add_format({'bold': True})
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    cell_format.set_text_wrap()
    cell_format.font_size = 11
    count = len(query_result)
    worksheet.write('A1', 'ลำดับ',cell_format)
    worksheet.write('B1', 'เลขที่เอกสาร',cell_format)
    worksheet.write('C1', 'สถานะ',cell_format)
    worksheet.write('D1', 'ชื่อผู้รออนุมัติ',cell_format)
    worksheet.write('E1', 'ชื่อผู้ส่ง',cell_format)
    worksheet.write('F1', 'เวลาส่งเอกสารเข้าระบบ ppl',cell_format)
    worksheet.write('G1', 'สถานะการส่ง BOT',cell_format)
    worksheet.set_column(0,0,6)
    worksheet.set_column(1,1,22)
    worksheet.set_column(2,3,18)
    worksheet.set_column(4,4,23)
    worksheet.set_column(5,6,20)
    worksheet.set_column(7,12,25)
    row = 1
    for num in range (0, count):
        statusRPA = False
        line = query_result[num]
        # print(line)
        worksheet.write(row, 0, (num+1), format2)
        worksheet.write(row, 1, line['document_id'],format2)
        if line['status'] == "REJECT":
            line['document_status'] = "ถูกยกเลิก"
        if line['document_status'] == "Y":
            line['document_status'] = "อนุมัติแล้ว"
        elif line['document_status'] == "N":
            line['document_status'] = "กำลังดำเนินการ"
        elif line['document_status'] == "R":
            line['document_status'] = "ปฏิเสธอนุมัติ"
        worksheet.write(row, 2, line['document_status'],format2)
        str_email = ''
        if line['document_status'] == "กำลังดำเนินการ":
            try:
                line['status_details'] =eval(line['status_details'])
                for i in range(len( line['status_details'])):
                    step_status_code =  line['status_details'][i]['step_status_code']
                    if step_status_code == 'W':
                        email = line['status_details'][i]['email']
                        for e in range(len(email)):
                            str_email += email[e]
            except Exception as e:
                line['status_details'] =  line['status_details']
        worksheet.write(row, 3, str_email,format2)
        try:
            line['sender_name'] = eval(line['sender_name'])['th']
        except Exception as e:
            line['sender_name'] = line['sender_name']
        worksheet.write(row, 4, line['sender_name'],format2)
        worksheet.write(row, 5, str(line['send_time']),format2)
        if line['status_service'] == '{}':
            line['status_service'] = ""
        elif line['status_service'] == '[]':
            line['status_service'] = ""
        else:
            try:
                line['status_service'] = eval(line['status_service'])
                for n in range(len(line['status_service'])):
                    if line['status_service'][n]['service'] == 'RPA':
                        if line['status_service'][n]['status'] == True:
                            statusRPA = True
            except Exception as e:
                line['status_service'] = line['status_service']
        if statusRPA:
            line['status_service'] = 'ส่งสำเร็จ'
        else:
            line['status_service'] = 'ส่งไม่สำเร็จ'
            if line['document_status'] == "กำลังดำเนินการ":
                line['status_service'] = 'ยังไม่ได้นำส่ง'
        worksheet.write(row, 6, line['status_service'],format2)

        row += 1
    workbook.close()

# getExcel_CS()

@status_methods.route('/api/checkonemail',methods=['POST'])
@token_required
def service_checkmail():
    try:
        data = request.json
        arr_data = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
            res = ex.map(func_call_check_mail, data)
            arr_status = (list(res))

        return jsonify({'result':'OK','messageText':arr_status,'status_Code':200}),200 
    except Exception as ex:
        return jsonify({'result':'ER','messageText':str(ex)}),500

@status_methods.route('/api/service',methods=['POST'])
def service_total():
    try:
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
            token_header_decode = check_Ref_Token(token_header)
        except KeyError as ex:
            return redirect(url_paperless)

        result_arraylist = []
        result_detail_service = {}
        dataForm = request.form
        dataFile = request.files
        if 'inputFile' in dataFile and 'username' in dataForm and 'templateCode'in dataForm and 'oneEmail' in dataForm and len(dataForm) == 3:           
            result_detail_service['result_detail_service'] = {}
            input_file      = dataFile['inputFile']
            username        = dataForm['username']
            oneEmail        = dataForm['oneEmail']
            template_code   = dataForm['templateCode']
            base64_filedata = (base64.b64encode(input_file.read())).decode('utf-8')
            
            data_url = myUrl+"/api/template?string=true&username="+username+"&"+"template="+template_code
            getTemplate = callAPI(token_header,'GET',data_url,'')
            getTemplate = getTemplate.json()
            if getTemplate['result'] == "OK":
                result_detail_service['result_detail_service']['result_getTemplate_service'] = getTemplate 
                fileName = input_file.filename
                totalStep = str(getTemplate['messageText'][0]['step_Max'])
                stepJson = str(getTemplate['messageText'][0]['data_step'])
                try:
                    getmail_string  = { 
                        "string_Json": stepJson,
                        "step_Max" : int(totalStep)
                    }
                    data_url_getmail = myUrl+"/api/mail_string/v2"
                    getStepMail = callAPI(token_header,'POST',data_url_getmail,getmail_string)
                    getStepMail = getStepMail.json()
                    if getStepMail['result'] == 'OK':                        
                        stepArray = getStepMail['messageText']
                        for item in range(len(stepArray)):
                            if stepArray[item]['email_result'] == []:
                                return jsonify({'result':'ER','messageText':'template has no receiver','status_Code':200})
                except Exception as ex:
                    return jsonify({'result':'ER','messageText':str(ex)})
                upload_string  = {
                    "template":    "",
                    "step":        totalStep,
                    "step_data":   stepJson,
                    "name_file":   fileName,
                    "convert_id":  None,
                    "file_string": base64_filedata,
                }
                data_url_upload = myUrl+"/api/upload"
                getUpload = callAPI(token_header,'POST',data_url_upload,upload_string)
                getUpload = getUpload.json()
                if getUpload['result'] == "OK":
                    result_detail_service['result_detail_service']['result_Upload'] = getUpload 
                    stepSid = getUpload['step_data_sid']
                    fileID  = getUpload['file_id']
                    fileType = input_file.content_type
                    trackingID = getUpload['tracking_code']
                    document_string  = { 
                        "step_id":   stepSid,
                        "type_file": fileType,
                        "file_id":   fileID
                    }
                    data_url_document = myUrl+"/api/document"
                    getDocument = callAPI(token_header,'POST',data_url_document,document_string)
                    getDocument = getDocument.json()
                    if getDocument['result'] == "OK":
                        result_detail_service['result_detail_service']['result_Document'] = getDocument 
                        documentID = getDocument['document_Id']
                        sender_string  = { 
                            "send_user":        username,
                            "status":           "ACTIVE",
                            "sender_name":      username,
                            "sender_email":     oneEmail,
                            "sender_position":  "owner",
                            "file_id":          fileID,
                            "file_name":        fileName,
                            "tracking_id":      trackingID,
                            "step_data_sid":    stepSid,
                            "step_code":        template_code,
                            "doc_id":           documentID,
                        }
                        data_url_sender = myUrl+"/api/sender"
                        print(sender_string)
                        getSender = callAPI(token_header,'POST',data_url_sender,sender_string)
                        getSender = getSender.json()
                        if getSender['result'] == "OK":
                            # sum result by knot
                            result_detail_service['result_detail_service']['result_Sender_Detail'] = getSender

                            chatUrl = getSender['messageText']['url_Chat']
                            sign_string  = { 
                                "sid":      stepSid,
                                "sign_json":stepJson,
                                "file_id":  fileID,
                            }
                            data_url_sign = myUrl+"/api/sign"
                            getSign = callAPI(token_header,'POST',data_url_sign,sign_string)
                            getSign = getSign.json()
                            if getSign['result'] == "OK":
                                result_detail_service['result_detail_service']['result_GetSignning'] = getSign
                                chatData = []
                                for item in range(len(stepArray)):                                    
                                    stepMail = stepArray[item]['email_result']
                                    stepNum_Mail = stepArray[item]['step_num']
                                    for item_mail in range(len(stepMail)):
                                        chatData.append({"email":stepMail[item_mail]['email'],"url_sign":chatUrl,"tracking":trackingID,"name_file":fileName,"message":"","step_num":stepNum_Mail,"sendChat":stepMail[item_mail]['status_chat']})
                                chatRequestData = {
                                    "type_service" : 'first',
                                    "sid": stepSid,
                                    "url_sign" : chatUrl,
                                    "tracking" : trackingID,
                                    "name_file" : fileName,
                                    "data": chatData
                                }
                                print(chatRequestData)
                                if len(chatData) > 0:
                                    url_chat = myUrl+"/api/chat/v2"
                                    sendChat = callAPI(token_header,'POST',url_chat,chatRequestData)
                                    sendChat = sendChat.json()
                                    if sendChat['result'] == "OK":
                                        return jsonify({'result':'OK','messageText':'Upload Complete, SendChat Success','status_Code':200})
                                    else:
                                        return jsonify({'result':'ER','messageText':'Upload Complete, SendChat Failed','status_Code':200})
                                else:
                                    return jsonify({'result':'OK','messageText':'Upload Complete, SendChat Not found','status_Code':200})
                            else:
                                return jsonify(getSign)
                        else:
                            return jsonify(getSender)
                    else:
                        return jsonify(getDocument)
                else:
                    return jsonify(getUpload)
            else:
                if getTemplate['messageText'] == "ไม่พบข้อมูล":
                    getTemplate['messageText'] = None
                    getTemplate['errorMessage'] = "ไม่พบรูปแบบที่ต้องการ"
                return jsonify(getTemplate)
        else:
            return jsonify({'result':'ER','messageText':'parameter error'})
    except KeyError as ex:
        return jsonify({'result':'ER','messageText':str(ex)})

@status_methods.route('/api/service/v2',methods=['POST'])
def service_total_v2():
    try:
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
            token_header_decode = check_Ref_Token(token_header)
        except KeyError as ex:
            return redirect(url_paperless)
        result_arraylist = []
        result_detail_service = {}
        dataForm = request.form
        dataFile = request.files
        if 'inputFile' in dataFile and 'username' in dataForm and 'templateCode'in dataForm and 'oneEmail' in dataForm and len(dataForm) == 3:           
            result_detail_service['result_detail_service'] = {}
            input_file      = dataFile['inputFile']
            username        = dataForm['username']
            oneEmail        = dataForm['oneEmail']
            template_code   = dataForm['templateCode']
            base64_filedata = (base64.b64encode(input_file.read())).decode('utf-8')
            
            data_url = myUrl+"/api/template/v2?string=true&username="+username+"&"+"template="+template_code
            getTemplate = callAPI(token_header,'GET',data_url,'')
            getTemplate = getTemplate.json()
            if getTemplate['result'] == "OK":
                result_detail_service['result_detail_service']['result_getTemplate_service'] = getTemplate 
                fileName = input_file.filename
                totalStep = str(getTemplate['messageText'][0]['step_Max'])
                stepJson = str(getTemplate['messageText'][0]['data_step'])
                stepUpload = str(getTemplate['messageText'][0]['step_Upload'])
                try:
                    getmail_string  = { 
                        "string_Json": stepJson,
                        "step_Max" : int(totalStep)
                    }
                    data_url_getmail = myUrl+"/api/mail_string/v2"
                    getStepMail = callAPI(token_header,'POST',data_url_getmail,getmail_string)
                    getStepMail = getStepMail.json()
                    if getStepMail['result'] == 'OK':
                        stepArray = getStepMail['messageText']
                        for item in range(len(stepArray)):
                            if stepArray[item]['email_result'] == []:
                                return jsonify({'result':'ER','messageText':'template has no receiver','status_Code':200})
                except Exception as ex:
                    return jsonify({'result':'ER','messageText':str(ex)})
                upload_string  = {
                    "template":    "",
                    "step":        totalStep,
                    "step_data":   stepJson,
                    "name_file":   fileName,
                    "convert_id":  None,
                    "file_string": base64_filedata,
                    "step_data_Upload": stepUpload
                }
                data_url_upload = myUrl+"/upload/v2_1"
                getUpload = callAPI(token_header,'POST',data_url_upload,upload_string)
                getUpload = getUpload.json()
                if getUpload['result'] == "OK":
                    result_detail_service['result_detail_service']['result_Upload'] = getUpload 
                    stepSid = getUpload['step_data_sid']
                    fileID  = getUpload['file_id']
                    fileType = input_file.content_type
                    trackingID = getUpload['tracking_code']
                    document_string  = { 
                        "step_id":   stepSid,
                        "type_file": fileType,
                        "file_id":   fileID
                    }
                    data_url_document = myUrl+"/api/document"
                    getDocument = callAPI(token_header,'POST',data_url_document,document_string)
                    getDocument = getDocument.json()
                    if getDocument['result'] == "OK":
                        result_detail_service['result_detail_service']['result_Document'] = getDocument 
                        documentID = getDocument['document_Id']
                        sender_string  = { 
                            "send_user":        username,
                            "status":           "ACTIVE",
                            "sender_name":      username,
                            "sender_email":     oneEmail,
                            "sender_position":  "owner",
                            "file_id":          fileID,
                            "file_name":        fileName,
                            "tracking_id":      trackingID,
                            "step_data_sid":    stepSid,
                            "step_code":        template_code,
                            "doc_id":           documentID,
                        }
                        data_url_sender = myUrl+"/api/sender"
                        print(sender_string)
                        getSender = callAPI(token_header,'POST',data_url_sender,sender_string)
                        getSender = getSender.json()
                        if getSender['result'] == "OK":
                            # sum result by knot
                            result_detail_service['result_detail_service']['result_Sender_Detail'] = getSender

                            chatUrl = getSender['messageText']['url_Chat']
                            sign_string  = { 
                                "sid":      stepSid,
                                "sign_json":stepJson,
                                "file_id":  fileID,
                            }
                            data_url_sign = myUrl+"/api/sign"
                            getSign = callAPI(token_header,'POST',data_url_sign,sign_string)
                            getSign = getSign.json()
                            if getSign['result'] == "OK":
                                result_detail_service['result_detail_service']['result_GetSignning'] = getSign
                                chatData = []
                                for item in range(len(stepArray)):                                    
                                    stepMail = stepArray[item]['email_result']
                                    stepNum_Mail = stepArray[item]['step_num']
                                    for item_mail in range(len(stepMail)):
                                        chatData.append({"email":stepMail[item_mail]['email'],"url_sign":chatUrl,"tracking":trackingID,"name_file":fileName,"message":"","step_num":stepNum_Mail,"sendChat":stepMail[item_mail]['status_chat']})
                                chatRequestData = {
                                    "type_service" : 'first',
                                    "sid": stepSid,
                                    "url_sign" : chatUrl,
                                    "tracking" : trackingID,
                                    "name_file" : fileName,
                                    "data": chatData
                                }
                                if len(chatData) > 0:
                                    url_chat = myUrl+"/api/chat/v2"
                                    sendChat = callAPI(token_header,'POST',url_chat,chatRequestData)
                                    sendChat = sendChat.json()
                                    if sendChat['result'] == "OK":
                                        return jsonify({'result':'OK','messageText':'Upload Complete, SendChat Success','status_Code':200,'messageDetailService':result_detail_service})
                                    else:
                                        return jsonify({'result':'ER','messageText':'Upload Complete, SendChat Failed','status_Code':200})
                                else:
                                    return jsonify({'result':'OK','messageText':'Upload Complete, SendChat Not found','status_Code':200})
                            else:
                                return jsonify(getSign)
                        else:
                            return jsonify(getSender)
                    else:
                        return jsonify(getDocument)
                else:
                    return jsonify(getUpload)
            else:
                if getTemplate['messageText'] == "ไม่พบข้อมูล":
                    getTemplate['messageText'] = None
                    getTemplate['errorMessage'] = "ไม่พบรูปแบบที่ต้องการ"
                return jsonify(getTemplate)
        else:
            return jsonify({'result':'ER','messageText':'parameter error'})
    except KeyError as ex:
        return jsonify({'result':'ER','messageText':str(ex)})

@status_methods.route('/api/service/v3',methods=['POST'])
def service_total_v3():
    '''upload doc and onechain'''
    try:
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
            token_header_decode = check_Ref_Token(token_header)
        except KeyError as ex:
            return redirect(url_paperless)
        result_arraylist = []
        result_detail_service = {}
        dataForm = request.form
        dataFile = request.files
        if 'inputFile' in dataFile and 'username' in dataForm and 'templateCode'in dataForm and 'oneEmail' in dataForm and len(dataForm) == 3:           
            result_detail_service['result_detail_service'] = {}
            input_file      = dataFile['inputFile']
            username        = dataForm['username']
            oneEmail        = dataForm['oneEmail']
            template_code   = dataForm['templateCode']
            base64_filedata = (base64.b64encode(input_file.read())).decode('utf-8')
            
            data_url = myUrl+"/api/template/v2?string=true&username="+username+"&"+"template="+template_code
            getTemplate = callAPI(token_header,'GET',data_url,'')
            getTemplate = getTemplate.json()
            if getTemplate['result'] == "OK":
                result_detail_service['result_detail_service']['result_getTemplate_service'] = getTemplate 
                fileName = input_file.filename
                totalStep = str(getTemplate['messageText'][0]['step_Max'])
                stepJson = str(getTemplate['messageText'][0]['data_step'])
                stepUpload = str(getTemplate['messageText'][0]['step_Upload'])
                try:
                    getmail_string  = { 
                        "string_Json": stepJson,
                        "step_Max" : int(totalStep)
                    }
                    data_url_getmail = myUrl+"/api/mail_string/v2"
                    getStepMail = callAPI(token_header,'POST',data_url_getmail,getmail_string)
                    getStepMail = getStepMail.json()
                    if getStepMail['result'] == 'OK':
                        Json_userAccount = {}
                        mail_Array = []
                        stepArray = getStepMail['messageText']
                        for item in range(len(stepArray)):
                            if stepArray[item]['email_result'] == []:
                                return jsonify({'result':'ER','messageText':'template has no receiver','status_Code':200})
                            for itemMail in range(len(stepArray[item]['email_result'])):
                                mail_Array.append(stepArray[item]['email_result'][itemMail]['email'])
                        Json_userAccount['username'] = username
                        Json_userAccount['email_thai'] = mail_Array
                except Exception as ex:
                    return jsonify({'result':'ER','messageText':str(ex)})
                upload_string  = {
                    "template":    "",
                    "step":        totalStep,
                    "step_data":   stepJson,
                    "name_file":   fileName,
                    "convert_id":  None,
                    "file_string": base64_filedata,
                    "step_data_Upload": stepUpload,
                    "biz_detail": None
                }
                
                data_url_upload = myUrl+"/upload/v2_1"
                getUpload = callAPI(token_header,'POST',data_url_upload,upload_string)
                getUpload = getUpload.json()
                if getUpload['result'] == "OK":
                    result_detail_service['result_detail_service']['result_Upload'] = getUpload
                    login_OneChain = {
                        "username": "onebilling",
                        "orgName": "OneChain"
                    }
                    data_url_LoginOnechain = url_onechain_ForUploadFile + "/api/v1/login"
                    getLogin_OneChain = callAPI_OneChain('POST',data_url_LoginOnechain,login_OneChain)
                    getLogin_OneChain = getLogin_OneChain.json()
                    if getLogin_OneChain['result'] == "OK":
                        result_detail_service['result_detail_service']['result_LoginOneChain'] = getLogin_OneChain 
                        token_OneChain = getLogin_OneChain['messageText']['token']
                        upload_string_OneChain  = {
                            "user_id":    "123456789",
                            "file_string":    base64_filedata,
                            "file_extension": "pdf"
                        }
                        data_url_uploadOnechain = url_onechain_ForUploadFile + "/api/v2/upload"
                        getUpload_OneChain = callAPI(token_OneChain,'POST',data_url_uploadOnechain,upload_string_OneChain)
                        getUpload_OneChain = getUpload_OneChain.json()
                        if getUpload_OneChain['result'] == "OK":
                            stepSid = getUpload['step_data_sid']
                            fileID  = getUpload['file_id']
                            fileType = input_file.content_type
                            trackingID = getUpload['tracking_code']
                            result_detail_service['result_detail_service']['result_UploadOneChain'] = getUpload_OneChain
                            timestamp = getUpload_OneChain['messageText']['response_from_endorser']['metadate']['timestamp']
                            transactionId = getUpload_OneChain['messageText']['response_from_endorser']['metadate']['transactionId']
                            file_id = getUpload_OneChain['messageText']['response_from_endorser']['metadate']['file_id']
                            metadate_String = {}
                            metadate_String['metadata'] = (getUpload_OneChain['messageText']['response_from_endorser']['metadate'])
                            putOneChain_paperless  = { 
                                "sid":              stepSid,
                                "file_id":          file_id,
                                "transactionId":    transactionId,
                                "timestamp":        timestamp,
                                "metadate":         str(metadate_String),
                                "account":          str(Json_userAccount)
                            }
                            data_urlOneChainAndPaperLess = myUrl+"/api/onechain"
                            getResponse_OnePaperless = callAPI(token_header,'POST',data_urlOneChainAndPaperLess,putOneChain_paperless)
                            getResponse_OnePaperless = getResponse_OnePaperless.json()
                            if getResponse_OnePaperless['result'] == "OK":          
                                document_string  = { 
                                    "step_id":   stepSid,
                                    "type_file": fileType,
                                    "file_id":   fileID
                                }
                                data_url_document = myUrl+"/api/document"
                                getDocument = callAPI(token_header,'POST',data_url_document,document_string)
                                getDocument = getDocument.json()
                                if getDocument['result'] == "OK":
                                    result_detail_service['result_detail_service']['result_Document'] = getDocument 
                                    documentID = getDocument['document_Id']
                                    sender_string  = { 
                                        "send_user":        username,
                                        "status":           "ACTIVE",
                                        "sender_name":      username,
                                        "sender_email":     oneEmail,
                                        "sender_position":  "owner",
                                        "file_id":          fileID,
                                        "file_name":        fileName,
                                        "tracking_id":      trackingID,
                                        "step_data_sid":    stepSid,
                                        "step_code":        template_code,
                                        "doc_id":           documentID,
                                    }
                                    data_url_sender = myUrl+"/api/sender/v2"
                                    getSender = callAPI(token_header,'POST',data_url_sender,sender_string)
                                    getSender = getSender.json()
                                    if getSender['result'] == "OK":
                                        # sum result by knot
                                        result_detail_service['result_detail_service']['result_Sender_Detail'] = getSender

                                        chatUrl = getSender['messageText']['url_Chat']
                                        sign_string  = { 
                                            "sid":      stepSid,
                                            "sign_json":stepJson,
                                            "file_id":  fileID,
                                        }
                                        data_url_sign = myUrl+"/api/sign"
                                        getSign = callAPI(token_header,'POST',data_url_sign,sign_string)
                                        getSign = getSign.json()
                                        if getSign['result'] == "OK":
                                            result_detail_service['result_detail_service']['result_GetSignning'] = getSign
                                            chatData = []
                                            for item in range(len(stepArray)):                                    
                                                stepMail = stepArray[item]['email_result']
                                                stepNum_Mail = stepArray[item]['step_num']
                                                for item_mail in range(len(stepMail)):
                                                    chatData.append({"email":stepMail[item_mail]['email'],"url_sign":chatUrl,"tracking":trackingID,"name_file":fileName,"message":"","step_num":stepNum_Mail,"sendChat":stepMail[item_mail]['status_chat']})
                                            chatRequestData = {
                                                "type_service" : 'first',
                                                "sid": stepSid,
                                                "url_sign" : chatUrl,
                                                "tracking" : trackingID,
                                                "name_file" : fileName,
                                                "data": chatData
                                            }
                                            if len(chatData) > 0:
                                                url_chat = myUrl+"/api/chat/v2"
                                                sendChat = callAPI(token_header,'POST',url_chat,chatRequestData)
                                                sendChat = sendChat.json()
                                                if sendChat['result'] == "OK":
                                                    result = {}
                                                    result['document_Id'] = result_detail_service['result_detail_service']['result_Document']['document_Id']
                                                    result['ref_Code'] = result_detail_service['result_detail_service']['result_Document']['ref_Code']
                                                    result['urlforSign'] = result_detail_service['result_detail_service']['result_Sender_Detail']['messageText']['url_Chat']
                                                    result['file_name'] =  result_detail_service['result_detail_service']['result_Upload']['file_name']
                                                    result['tracking_Code'] =  result_detail_service['result_detail_service']['result_Upload']['tracking_code']
                                                    return jsonify({'result':'OK','messageText':{'messageStatus':'Upload Complete, SendChat Success','messageDetail':result},'status_Code':200,'messageER':None})
                                                else:
                                                    return jsonify({'result':'ER','messageText':'Upload Complete','status_Code':200,'messageER':'SendChat Failed!'})
                                            else:
                                                return jsonify({'result':'OK','messageText':'Upload Complete, SendChat Not found','status_Code':200,'messageER':None})
                                        else:
                                            return jsonify(getSign)
                                    else:
                                        return jsonify(getSender)
                                else:
                                    return jsonify(getDocument)
                            else:
                                return jsonify(getResponse_OnePaperless)
                        else:
                            return jsonify(getUpload_OneChain)
                    else:
                        return jsonify(getLogin_OneChain)
                else:
                    return jsonify(getUpload)
            else:
                if getTemplate['messageText'] == "ไม่พบข้อมูล":
                    getTemplate['messageText'] = None
                    getTemplate['messageER'] = "ไม่พบรูปแบบที่ต้องการ"
                return jsonify(getTemplate)
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':'parameter error','status_Code':404}),404
    except KeyError as ex:
        return jsonify({'result':'ER','messageText':None,'messageER':str(ex),'status_Code':200}),200

@status_methods.route('/api/service/v4',methods=['POST'])
def service_total_v4():
    '''upload doc and onechain'''
    try:
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
            url = one_url + "/api/account_and_biz_detail"
            headers = {
                'Content-Type': "application/json",
                'Authorization': "Bearer"+" "+token_header
            }
            try:
                response = requests.get(url, headers=headers, verify=False)
                response = response.json()
            except requests.Timeout as ex:
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
            except requests.HTTPError as ex:
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
            except requests.ConnectionError as ex:
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
            except requests.RequestException as ex:
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
            except Exception as ex:
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
            if 'result' in response:
                if response['result'] == 'Fail':
                    return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
            else:
                thai_email = response['thai_email']
                username = response['username']
                result_arraylist = []
                result_detail_service = {}
                dataForm = request.form
                dataFile = request.files
                if 'inputFile' in dataFile and 'username' in dataForm and 'templateCode'in dataForm and 'oneEmail' in dataForm and len(dataForm) == 3:
                    if username == dataForm['username'] and thai_email == dataForm['oneEmail']:
                        result_detail_service['result_detail_service'] = {}
                        input_file      = dataFile['inputFile']
                        username        = dataForm['username']
                        oneEmail        = dataForm['oneEmail']
                        template_code   = dataForm['templateCode']
                        base64_filedata = (base64.b64encode(input_file.read())).decode('utf-8')
                        
                        data_url = myUrl+"/api/template/v2?string=true&username="+username+"&"+"template="+template_code
                        getTemplate = callAPI(token_header,'GET',data_url,'')
                        getTemplate = getTemplate.json()
                        if getTemplate['result'] == "OK":
                            result_detail_service['result_detail_service']['result_getTemplate_service'] = getTemplate 
                            fileName = input_file.filename
                            totalStep = str(getTemplate['messageText'][0]['step_Max'])
                            stepJson = str(getTemplate['messageText'][0]['data_step'])
                            stepUpload = str(getTemplate['messageText'][0]['step_Upload'])
                            try:
                                getmail_string  = { 
                                    "string_Json": stepJson,
                                    "step_Max" : int(totalStep)
                                }
                                data_url_getmail = myUrl+"/api/mail_string/v2"
                                getStepMail = callAPI(token_header,'POST',data_url_getmail,getmail_string)
                                getStepMail = getStepMail.json()
                                if getStepMail['result'] == 'OK':
                                    Json_userAccount = {}
                                    mail_Array = []
                                    stepArray = getStepMail['messageText']
                                    for item in range(len(stepArray)):
                                        if stepArray[item]['email_result'] == []:
                                            return jsonify({'result':'ER','messageText':'template has no receiver','status_Code':200})
                                        for itemMail in range(len(stepArray[item]['email_result'])):
                                            mail_Array.append(stepArray[item]['email_result'][itemMail]['email'])
                                    Json_userAccount['username'] = username
                                    Json_userAccount['email_thai'] = mail_Array
                            except Exception as ex:
                                return jsonify({'result':'ER','messageText':str(ex)})
                            upload_string  = {
                                "template":    "",
                                "step":        totalStep,
                                "step_data":   stepJson,
                                "name_file":   fileName,
                                "convert_id":  None,
                                "file_string": base64_filedata,
                                "step_data_Upload": stepUpload,
                                "biz_detail": None
                            }
                            
                            data_url_upload = myUrl+"/upload/v2_1"
                            getUpload = callAPI(token_header,'POST',data_url_upload,upload_string)
                            getUpload = getUpload.json()
                            if getUpload['result'] == "OK":
                                result_detail_service['result_detail_service']['result_Upload'] = getUpload
                                login_OneChain = {
                                    "username": "onebilling",
                                    "orgName": "OneChain"
                                }
                                data_url_LoginOnechain = url_onechain_ForUploadFile + "/api/v1/login"
                                getLogin_OneChain = callAPI_OneChain('POST',data_url_LoginOnechain,login_OneChain)
                                getLogin_OneChain = getLogin_OneChain.json()
                                if getLogin_OneChain['result'] == "OK":
                                    result_detail_service['result_detail_service']['result_LoginOneChain'] = getLogin_OneChain 
                                    token_OneChain = getLogin_OneChain['messageText']['token']
                                    upload_string_OneChain  = {
                                        "user_id":    "123456789",
                                        "file_string":    base64_filedata,
                                        "file_extension": "pdf"
                                    }
                                    data_url_uploadOnechain = url_onechain_ForUploadFile + "/api/v2/upload"
                                    getUpload_OneChain = callAPI(token_OneChain,'POST',data_url_uploadOnechain,upload_string_OneChain)
                                    getUpload_OneChain = getUpload_OneChain.json()
                                    if getUpload_OneChain['result'] == "OK":
                                        stepSid = getUpload['step_data_sid']
                                        fileID  = getUpload['file_id']
                                        fileType = input_file.content_type
                                        trackingID = getUpload['tracking_code']
                                        result_detail_service['result_detail_service']['result_UploadOneChain'] = getUpload_OneChain
                                        timestamp = getUpload_OneChain['messageText']['response_from_endorser']['metadate']['timestamp']
                                        transactionId = getUpload_OneChain['messageText']['response_from_endorser']['metadate']['transactionId']
                                        file_id = getUpload_OneChain['messageText']['response_from_endorser']['metadate']['file_id']
                                        metadate_String = {}
                                        metadate_String['metadata'] = (getUpload_OneChain['messageText']['response_from_endorser']['metadate'])
                                        putOneChain_paperless  = { 
                                            "sid":              stepSid,
                                            "file_id":          file_id,
                                            "transactionId":    transactionId,
                                            "timestamp":        timestamp,
                                            "metadate":         str(metadate_String),
                                            "account":          str(Json_userAccount)
                                        }
                                        data_urlOneChainAndPaperLess = myUrl+"/api/onechain"
                                        getResponse_OnePaperless = callAPI(token_header,'POST',data_urlOneChainAndPaperLess,putOneChain_paperless)
                                        getResponse_OnePaperless = getResponse_OnePaperless.json()
                                        if getResponse_OnePaperless['result'] == "OK":          
                                            document_string  = { 
                                                "step_id":   stepSid,
                                                "type_file": fileType,
                                                "file_id":   fileID
                                            }
                                            data_url_document = myUrl+"/api/document"
                                            getDocument = callAPI(token_header,'POST',data_url_document,document_string)
                                            getDocument = getDocument.json()
                                            if getDocument['result'] == "OK":
                                                result_detail_service['result_detail_service']['result_Document'] = getDocument 
                                                documentID = getDocument['document_Id']
                                                sender_string  = { 
                                                    "send_user":        username,
                                                    "status":           "ACTIVE",
                                                    "sender_name":      username,
                                                    "sender_email":     oneEmail,
                                                    "sender_position":  "owner",
                                                    "file_id":          fileID,
                                                    "file_name":        fileName,
                                                    "tracking_id":      trackingID,
                                                    "step_data_sid":    stepSid,
                                                    "step_code":        template_code,
                                                    "doc_id":           documentID,
                                                }
                                                data_url_sender = myUrl+"/api/sender/v2"
                                                getSender = callAPI(token_header,'POST',data_url_sender,sender_string)
                                                getSender = getSender.json()
                                                if getSender['result'] == "OK":
                                                    # sum result by knot
                                                    result_detail_service['result_detail_service']['result_Sender_Detail'] = getSender

                                                    sign_string  = { 
                                                        "sid":      stepSid,
                                                        "sign_json":stepJson,
                                                        "file_id":  fileID,
                                                    }
                                                    data_url_sign = myUrl+"/api/sign"
                                                    getSign = callAPI(token_header,'POST',data_url_sign,sign_string)
                                                    getSign = getSign.json()
                                                    if getSign['result'] == "OK":
                                                        result_detail_service['result_detail_service']['result_GetSignning'] = getSign
                                                        chatData = []
                                                        Email_arr = []
                                                        arr_emailReponse = ''
                                                        for item in range(len(stepArray)):                                    
                                                            stepMail = stepArray[item]['email_result']
                                                            stepNum_Mail = stepArray[item]['step_num']
                                                            for item_mail in range(len(stepMail)):
                                                                Email_arr.append(stepMail[item_mail]['email'])
                                                                chatData.append({"email":stepMail[item_mail]['email'],"url_sign":None,"tracking":trackingID,"name_file":fileName,"message":"","step_num":stepNum_Mail,"sendChat":stepMail[item_mail]['status_chat']})
                                                        emailGetUrlSign = {
                                                            "email" : Email_arr,
                                                            "sidCode" : stepSid
                                                        }
                                                        url_getUrl = myUrl + "/api/geturl/v1"
                                                        getUrlSign = callAPI(token_header,'POST',url_getUrl,emailGetUrlSign)
                                                        getUrlSign = getUrlSign.json()
                                                        if getUrlSign['result'] == 'OK':
                                                            result_detail_service['result_detail_service']['result_getUrl'] = getUrlSign
                                                            arr_emailReponse = getUrlSign['messageText']
                                                        for arr_item in range(len(arr_emailReponse)):
                                                            if chatData[arr_item]['email'] == arr_emailReponse[arr_item]['email']:
                                                                chatData[arr_item]['url_sign'] = arr_emailReponse[arr_item]['urlSign']
                                                        chatRequestData = {
                                                            "type_service" : 'first',
                                                            "sid": stepSid,
                                                            "tracking" : trackingID,
                                                            "name_file" : fileName,
                                                            "data": chatData
                                                        }

                                                        if len(chatData) > 0:
                                                            url_chat = myUrl+"/api/chat/v3"
                                                            sendChat = callAPI(token_header,'POST',url_chat,chatRequestData)
                                                            sendChat = sendChat.json()
                                                            if sendChat['result'] == "OK":
                                                                result = {}
                                                                result['document_Id'] = result_detail_service['result_detail_service']['result_Document']['document_Id']
                                                                result['ref_Code'] = result_detail_service['result_detail_service']['result_Document']['ref_Code']
                                                                result['urlforSign'] = result_detail_service['result_detail_service']['result_getUrl']['messageText']
                                                                result['file_name'] =  result_detail_service['result_detail_service']['result_Upload']['file_name']
                                                                result['tracking_Code'] =  result_detail_service['result_detail_service']['result_Upload']['tracking_code']
                                                                return jsonify({'result':'OK','messageText':{'messageStatus':'Upload Complete, SendChat Success','messageDetail':result},'status_Code':200,'messageER':None})
                                                            else:
                                                                return jsonify({'result':'ER','messageText':'Upload Complete','status_Code':200,'messageER':'SendChat Failed!'})
                                                        else:
                                                            return jsonify({'result':'OK','messageText':'Upload Complete, SendChat Not found','status_Code':200,'messageER':None})
                                                    else:
                                                        return jsonify(getSign)
                                                else:
                                                    return jsonify(getSender)
                                            else:
                                                return jsonify(getDocument)
                                        else:
                                            return jsonify(getResponse_OnePaperless)
                                    else:
                                        return jsonify(getUpload_OneChain)
                                else:
                                    return jsonify(getLogin_OneChain)
                            else:
                                return jsonify(getUpload)
                        else:
                            if getTemplate['messageText'] == "ไม่พบข้อมูล":
                                getTemplate['messageText'] = None
                                getTemplate['messageER'] = "ไม่พบรูปแบบที่ต้องการ"
                            return jsonify(getTemplate)
                    else:
                        return jsonify({'result':'ER','messageText':None,'messageER':'Authorization Username Or Password Wrong!','status_Code':404}),404
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':'parameter error','status_Code':404}),404

        except KeyError as ex:
            return redirect(url_paperless)
        
    except KeyError as ex:
        return jsonify({'result':'ER','messageText':None,'messageER':str(ex),'status_Code':200}),200

@status_methods.route('/api/v1/template_for_service',methods=['POST'])
def template_service_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!' + str(e)})
        if result_verify['result'] == 'OK':
            messageText_result = result_verify['messageText'].json()
            if 'result' not in messageText_result:
                username = messageText_result['username']
                thai_email = messageText_result['thai_email']
                dataJson = request.json
                if 'tax_Id' in dataJson and 'username' in dataJson and len(dataJson) == 2:
                    _username = dataJson['username']
                    _taxId = dataJson['tax_Id']
                    result_Select  =select().select_get_template_for_eform_v1(_username,_taxId,thai_email)
                    result_Select_Dod = select().select_get_document_type_for_eform_v1(_username,_taxId)
                    return jsonify({'result':'OK','template':result_Select,'document_type':result_Select_Dod})
                else:
                    return jsonify({'result':'ER','messageText':'parameter incorrect!','status_Code':404}),404

@status_methods.route('/api/v1/get_template_service',methods=['GET'])
def get_template_service():
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
        # result_verify = token_required_func(token_header)
        # print(result_verify)
        result_verify = verify().verify_one_id(token_header)
        if result_verify['result'] != 'OK':
            abort(401)
    except Exception as e:
        abort(401)
    if result_verify['result'] == 'OK':
        messageText_result = result_verify['messageText'].json()
        if 'result' not in messageText_result:
            username = messageText_result['username']
            thai_email = messageText_result['thai_email']
            tmptax_id = request.args.get('taxid')
            name = request.args.get('name')
            keyword = request.args.get('keyword')
            if tmptax_id != None:
                return_template = select_4().sleect_template_business_v1(tmptax_id,name,keyword,thai_email)
                return jsonify({'result':'OK','template':return_template,'document_type':None})
        else:
            abort(404)
    else:
        abort(404)


@status_methods.route('/api/v1/get_signature',methods=['GET'])
def get_signature():
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
        # result_verify = token_required_func(token_header)
        # print(result_verify)
        result_verify = verify().verify_one_id(token_header)
        if result_verify['result'] != 'OK':
            abort(401)
    except Exception as e:
        abort(401)
    if result_verify['result'] == 'OK':
        messageText_result = result_verify['messageText'].json()
        if 'result' not in messageText_result:
            user_id = messageText_result['id']
            username = messageText_result['username']
            thai_email = messageText_result['email']
            r = select_4().select_Signature_v1(user_id)
            if r[0] == 200:
                return jsonify({'result':'OK','data':r[1]})
            else:
                return jsonify({'result':'ER','data':None})
        else:
            abort(404)
    else:
        abort(404)


@status_methods.route('/api/v1/template_for_eform',methods=['POST','GET'])
def template_eform_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!' + str(e)})
        if result_verify['result'] == 'OK':
            messageText_result = result_verify['messageText'].json()
            if 'result' not in messageText_result:
                username = messageText_result['username']
                thai_email = messageText_result['thai_email']
                dataJson = request.json
                if 'tax_Id' in dataJson and 'username' in dataJson and len(dataJson) == 2:
                    _username = dataJson['username']
                    _taxId = dataJson['tax_Id']
                    result_Select  =select().select_get_template_for_eform_v1(_username,_taxId,thai_email)
                    result_Select_Dod = select().select_get_document_type_for_eform_v1(_username,_taxId)
                    return jsonify({'result':'OK','template':result_Select,'document_type':result_Select_Dod})
                else:
                    return jsonify({'result':'ER','messageText':'parameter incorrect!','status_Code':404}),404
    elif request.method == 'GET':
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
        if result_verify['result'] == 'OK':
            messageText_result = result_verify['messageText'].json()
            if 'result' not in messageText_result:
                username = messageText_result['username']
                thai_email = messageText_result['thai_email']
                tmptax_id = request.args.get('taxid')
                tmpusername = request.args.get('username')
                if tmptax_id != None and tmpusername != None:
                    # r_template = select().select_get_template_for_eform_v1(tmpusername,tmptax_id,thai_email)
                    # r_doctype = select().select_get_document_type_for_eform_v1(tmpusername,tmptax_id)
                    # with concurrent.futures.ThreadPoolExecutor() as executor:
                    #     future = executor.submit(select().select_get_template_for_eform_v1, tmpusername,tmptax_id,thai_email)
                    #     return_value = future.result()
                        # print(return_value)
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        resulttemplate = executor.submit(select().select_get_template_for_eform_v1,tmpusername,tmptax_id,thai_email)
                        resultdoctype = executor.submit(select().select_get_document_type_for_eform_v1,tmpusername,tmptax_id)
                        return_template = resulttemplate.result()
                        return_doctype = resultdoctype.result()
                    return jsonify({'result':'OK','template':return_template,'document_type':return_doctype})
        abort(404)

@status_methods.route('/api/v2/template_for_eform',methods=['GET'])
def template_eform_api_v2():
    if request.method == 'GET':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!' + str(e)})
        if result_verify['result'] == 'OK':
            messageText_result = result_verify['messageText'].json()
            if 'result' not in messageText_result:
                username = request.args.get('username')
                thai_email = request.args.get('thai_email')
                if username != None and thai_email != None:
                    # with concurrent.futures.ThreadPoolExecutor() as executor:
                    #     resulttemplate = executor.submit(select().select_get_template_for_eform_v1,_username,_taxId,thai_email)
                    #     return_template = resulttemplate.result()
                    # print(return_template)
                    result_Select  =select().select_get_template_for_eform_v1(_username,_taxId,thai_email)
                    result_Select_Dod = select().select_get_document_type_for_eform_v1(_username,_taxId)
                    return jsonify({'result':'OK','template':result_Select,'document_type':result_Select_Dod})
                else:
                    abort(404)

@status_methods.route('/api/v5/service',methods=['POST'])
def service_totle_v5():
    try:
        token_header = request.headers['Authorization']
        try:
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
        url = one_url + "/api/account_and_biz_detail"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer"+" "+token_header
        }
        try:
            response = requests.get(url, headers=headers, verify=False)
            response = response.json()
        except requests.Timeout as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.HTTPError as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.ConnectionError as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.RequestException as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except Exception as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        if 'result' in response:
            if response['result'] == 'Fail':
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
        else:
            biz_info = []
            thai_email = response['thai_email']
            username = response['username']
            if 'biz_detail' in response:
                getbiz = response['biz_detail']
                for i in range(len(getbiz)):
                    jsonData = {
                        'id':getbiz[i]['getbiz'][0]['id'],
                        'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                        'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                        'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                        'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                        'role_level':getbiz[i]['getrole'][0]['role_level'],
                        'role_name':getbiz[i]['getrole'][0]['role_name']
                    }
                    biz_info.append(jsonData)
            result_arraylist = []
            result_detail_service = {}
            dataForm = request.form
            dataFile = request.files
            result_CheckTaxId = []
            biz_json = ''
            chatData = []
            list_emailChat_log = []
            chatRequestData = {}
            status_sendChat = []
            result_list = []
            arr_result_Email = []
            list_taskChat_log = []
            MailData = {}
            if 'inputFile' in dataFile and 'username' in dataForm and 'templateCode'in dataForm and 'oneEmail' in dataForm and 'taxId' in dataForm and 'DocumentType' in dataForm and len(dataForm) == 5:
                if username == dataForm['username'] and thai_email == dataForm['oneEmail']:
                    input_file      = dataFile['inputFile']
                    username        = dataForm['username']
                    oneEmail        = dataForm['oneEmail']
                    template_code   = dataForm['templateCode']
                    tax_Id          = dataForm['taxId']  
                    Document_type   = dataForm['DocumentType']  
                    fileName        = input_file.filename
                    base64_filedata = (base64.b64encode(input_file.read())).decode('utf-8')
                    if str(tax_Id).replace(' ','') is not '':
                        if len(biz_info) != 0:
                            for i in range(len(biz_info)):
                                if tax_Id == biz_info[i]['id_card_num']:
                                    result_CheckTaxId.append('Y')
                                    biz_json = biz_info[i]
                            if 'Y' in result_CheckTaxId:
                                pass
                            else:
                                return jsonify({'result':'ER','messageText':'taxId not found','status_Code':200}),200
                    else:
                        biz_json = None
                    tax_Id = str(tax_Id).replace(' ','')
                    if tax_Id != '':
                        get_Template = select().select_get_string_templateAndusername_tax_new(str(template_code).replace(' ',''),str(tax_Id).replace(' ',''))
                        if get_Template['result'] == 'OK':
                            document_details = str(get_Template['messageText'][0]['document_details_string'])
                            document_type = get_Template['messageText'][0]['document_details']['document_type']
                            string_json = eval(get_Template['messageText'][0]['data_step'])
                            string_json_NoneEval = str(get_Template['messageText'][0]['data_step'])
                            step_Max = get_Template['messageText'][0]['step_Max']
                            result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                            string_json_NoneEval = str(result_SelectEmailMe['messageText'])                     
                            string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                            qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                            getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                            getEmail_list = []
                            if getEmail['result'] == 'OK':
                                for o in range(len(getEmail['messageText'])):
                                    if 'email_result' in getEmail['messageText'][o]:
                                        for i in getEmail['messageText'][o]['email_result']:
                                            getStepNumber = getEmail['messageText'][o]['step_num']
                                            getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                            sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                            res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                            if res_insert_pdf['result'] == 'OK':
                                getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                                if getTracking['result'] == 'OK':                                    
                                    ts = int(time.time())
                                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                    result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    if result_insert['result'] == 'OK':                                        
                                        sidCode = getTracking['step_data_sid']
                                        typeFile = str(fileName).split('.')[-1]
                                        FileId = res_insert_pdf['messageText']
                                        trackingId = getTracking['messageText']
                                        result_DocumentID = document_().genarate_document_ID(document_type)
                                        getDocument = insert().insert_document_new_v(sidCode,typeFile,FileId,document_details,document_type,'M',documentID=result_DocumentID['messageText']['documentID'])
                                        if getDocument['result'] == 'OK':
                                            document_Id = getDocument['document_Id']
                                            ts = int(time.time())
                                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                            getSender = insert().insert_paper_sender(username,st,'ACTIVE',username,oneEmail,'owner',FileId,fileName,trackingId,sidCode,template_code,document_Id)
                                            if getSender['result'] == 'OK':
                                                arr_result = []
                                                getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                                chatstatus_forservice(string_json)
                                                if getSign['result'] == 'OK':
                                                    for i in getEmail_list:
                                                        emailUser = i['email']
                                                        getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                                        if getUrl_Sign['result'] == 'OK':
                                                            arr_result.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num'],
                                                                'sendChat': i['status_chat'],
                                                                'property' : i['property']
                                                            })
                                                            arr_result_Email.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num']                                                                
                                                            })
                                                    chatRequestData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result
                                                    }
                                                    MailData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result_Email
                                                    }
                                                    data_tosender = chatRequestData['data']                                  
                                                    for n in range(len(data_tosender)):
                                                        status_sendChat.append(data_tosender[n]['sendChat'])
                                                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                                                            res_search_frd = search_frd(data_tosender[n]['email'])
                                                            # print(res_search_frd,' res_search_frd')
                                                            if 'status' in res_search_frd:
                                                                if res_search_frd['status'] == 'success':
                                                                    resultURLIMAGE = createImage_formPDF(sidCode)
                                                                    result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                    print(result_pathUrl)
                                                                    resouce_result = select().select_forChat_v1(sidCode)
                                                                    if resouce_result['result'] == 'OK':                
                                                                        res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl)
                                                                        if 'status' in res_send:
                                                                            if res_send['status'] == 'success':
                                                                                update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                else:
                                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            elif 'result' in res_search_frd:
                                                                if res_search_frd['result'] == 'ER':                            
                                                                    arrEmail = []
                                                                    arrEmail.append(data_tosender[n]['email'])
                                                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                                                    if 'status' in resultAddfrd:
                                                                        if resultAddfrd['status'] == 'success':
                                                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                                                resultURLIMAGE = createImage_formPDF(sidCode)
                                                                                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                                print(result_pathUrl)
                                                                                resouce_result = select().select_forChat_v1(sidCode)
                                                                                if resouce_result['result'] == 'OK':                
                                                                                    res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl)
                                                                                    if 'status' in res_send:
                                                                                        if res_send['status'] == 'success':
                                                                                            update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                            list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                                        else:
                                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                                    else:
                                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                    else:
                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            else:
                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                        else:
                                                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    if True in status_sendChat:
                                                        result_logChat = selection_email_insert(list_emailChat_log)
                                                        if result_logChat['result'] == 'OK':
                                                            data_Mail = MailData['data']
                                                            for i in range(len(data_Mail)):
                                                                if data_Mail[i]['step_num'] == "1":
                                                                    result_Email = mail().check_EmailProfile(data_Mail[i]['email'])
                                                                    if result_Email['result'] == 'OK':
                                                                        data_Mail[i]['emailUser'] = result_Email['messageText']['emailUser']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                    else:
                                                                        data_Mail[i]['emailUser'] = data_Mail[i]['email']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                        # print(result_mailStatus, ' result_mailStatus')
                                                                    if result_mailStatus['result'] == 'OK':
                                                                        result_list.append({'result':'OK','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':None})
                                                                    else:
                                                                        result_list.append({'result':'ER','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':result_mailStatus['messageText']})
                                                                else:
                                                                    result_list.append({'result':'NO','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign']})
                                                            # print(result_list , ' result_list')
                                                            result_insertMail = mail().insert_logEmail(result_list)
                                                            if result_insertMail['result'] == 'OK':
                                                                return jsonify({'result':'OK','messageText':{'result_Mail_service':result_list,'result_Chat_service':list_emailChat_log},'status_Code':200}),200
                                                            else:
                                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insertMail['messageText']})
                                                        else:
                                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                                                    else:
                                                        result_logChat = selection_email_insert(list_emailChat_log)
                                                        return jsonify({'result':'OK','messageText':'Not Found Send To OneChat!','status_Code':200,'messageER':None})
                                                    
                                            return jsonify({'result':'OK','messageText':'Success!','tracking_code':getTracking['messageText'],'step_data_sid':getTracking['step_data_sid'],'convert_id':getTracking['convert_id'],'file_id':res_insert_pdf['messageText'],'file_name':fileName,'status_Code':200}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                        else:        
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template not found in taxId'}),200
                            return ''
                    else:
                        get_Template = select().select_get_string_templateAndusername(str(username).replace(' ',''),str(template_code).replace(' ',''))
                        # print(get_Template)
                        if get_Template['result'] == 'OK':
                            document_details = str(get_Template['messageText'][0]['document_details_string'])
                            document_type = get_Template['messageText'][0]['document_details']['document_type']
                            string_json = eval(get_Template['messageText'][0]['data_step'])
                            string_json_NoneEval = str(get_Template['messageText'][0]['data_step'])
                            step_Max = get_Template['messageText'][0]['step_Max']
                            result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                            print(result_SelectEmailMe)
                            string_json_NoneEval = str(result_SelectEmailMe['messageText'])                            
                            string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                            qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                            getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                            getEmail_list = []
                            if getEmail['result'] == 'OK':
                                for o in range(len(getEmail['messageText'])):
                                    if 'email_result' in getEmail['messageText'][o]:
                                        for i in getEmail['messageText'][o]['email_result']:
                                            getStepNumber = getEmail['messageText'][o]['step_num']
                                            getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                            # print(getEmail_list,'getEmail_list')
                            sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                            res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                            if res_insert_pdf['result'] == 'OK':
                                getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                                if getTracking['result'] == 'OK':
                                    ts = int(time.time())
                                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                    # print(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    if result_insert['result'] == 'OK':                                        
                                        sidCode = getTracking['step_data_sid']
                                        typeFile = str(fileName).split('.')[-1]
                                        FileId = res_insert_pdf['messageText']
                                        trackingId = getTracking['messageText']
                                        result_DocumentID = document_().genarate_document_ID(document_type)
                                        # print(result_DocumentID, ' result_DocumentID')
                                        getDocument = insert().insert_document_new_v(sidCode,typeFile,FileId,document_details,document_type,'M',documentID=result_DocumentID['messageText']['documentID'])
                                        if getDocument['result'] == 'OK':
                                            document_Id = getDocument['document_Id']
                                            ts = int(time.time())
                                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                            getSender = insert().insert_paper_sender(username,st,'ACTIVE',username,oneEmail,'owner',FileId,fileName,trackingId,sidCode,template_code,document_Id)
                                            if getSender['result'] == 'OK':
                                                arr_result = []
                                                getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                                chatstatus_forservice(string_json)
                                                if getSign['result'] == 'OK':
                                                    for i in getEmail_list:
                                                        emailUser = i['email']
                                                        getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                                        if getUrl_Sign['result'] == 'OK':
                                                            arr_result.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num'],
                                                                'sendChat': i['status_chat'],
                                                                'property' : i['property']
                                                            })
                                                            print(arr_result)
                                                            arr_result_Email.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num']                                                                
                                                            })
                                                    chatRequestData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result
                                                    }
                                                    MailData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result_Email
                                                    }
                                                    data_tosender = chatRequestData['data']                                  
                                                    for n in range(len(data_tosender)):
                                                        status_sendChat.append(data_tosender[n]['sendChat'])
                                                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                                                            res_search_frd = search_frd(data_tosender[n]['email'])
                                                            oneId = res_search_frd['friend']['one_id']
                                                            if 'status' in res_search_frd:
                                                                if res_search_frd['status'] == 'success':
                                                                    resultURLIMAGE = createImage_formPDF(sidCode)
                                                                    result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                    print(result_pathUrl)
                                                                    resouce_result = select().select_forChat_v1(sidCode)
                                                                    if resouce_result['result'] == 'OK':                
                                                                        res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl)
                                                                        if 'status' in res_send:
                                                                            if res_send['status'] == 'success':
                                                                                update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                                                print(resultgetProject)
                                                                                
                                                                                if resultgetProject['result'] == 'OK':
                                                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                    priority_ = '1'
                                                                                    titleAndDetails = resouce_result['messageText']
                                                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                        if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                    resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode)
                                                                                    # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                    if resultSend_CreateTask['result'] == 'OK':
                                                                                        if 'status' in resultSend_CreateTask['messageText']:
                                                                                            if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                        else:
                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                    else:
                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                else:
                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                else:
                                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            elif 'result' in res_search_frd:
                                                                if res_search_frd['result'] == 'ER':                            
                                                                    arrEmail = []
                                                                    arrEmail.append(data_tosender[n]['email'])
                                                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                                                    if 'status' in resultAddfrd:
                                                                        if resultAddfrd['status'] == 'success':
                                                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                                                resultURLIMAGE = createImage_formPDF(sidCode)
                                                                                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                                print(result_pathUrl)
                                                                                resouce_result = select().select_forChat_v1(sidCode)
                                                                                if resouce_result['result'] == 'OK':                
                                                                                    res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl)
                                                                                    if 'status' in res_send:
                                                                                        if res_send['status'] == 'success':
                                                                                            update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                            resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                                                            if resultgetProject['result'] == 'OK':
                                                                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                                priority_ = '1'
                                                                                                titleAndDetails = resouce_result['messageText']
                                                                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                                resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode)
                                                                                                print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                                if resultSend_CreateTask['result'] == 'OK':
                                                                                                    if 'status' in resultSend_CreateTask['messageText']:
                                                                                                        if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                            list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                        else:
                                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                    else:
                                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                else:
                                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                                        else:
                                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                                    else:
                                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                    else:
                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            else:
                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                        else:
                                                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    if True in status_sendChat:
                                                        result_logChat = selection_email_insert(list_emailChat_log)
                                                        if result_logChat['result'] == 'OK':
                                                            insert().insert_transactionTask(list_taskChat_log)
                                                            data_Mail = MailData['data']
                                                            for i in range(len(data_Mail)):
                                                                if data_Mail[i]['step_num'] == "1":
                                                                    result_Email = mail().check_EmailProfile(data_Mail[i]['email'])
                                                                    if result_Email['result'] == 'OK':
                                                                        data_Mail[i]['emailUser'] = result_Email['messageText']['emailUser']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                    else:
                                                                        data_Mail[i]['emailUser'] = data_Mail[i]['email']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                        # print(result_mailStatus, ' result_mailStatus')
                                                                    if result_mailStatus['result'] == 'OK':
                                                                        result_list.append({'result':'OK','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':None})
                                                                    else:
                                                                        result_list.append({'result':'ER','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':result_mailStatus['messageText']})
                                                                else:
                                                                    result_list.append({'result':'NO','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign']})
                                                            # print(result_list , ' result_list')
                                                            result_insertMail = mail().insert_logEmail(result_list)
                                                            if result_insertMail['result'] == 'OK':
                                                                return jsonify({'result':'OK','messageText':{'result_Mail_service':result_list,'result_Chat_service':list_emailChat_log},'status_Code':200}),200
                                                            else:
                                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insertMail['messageText']})
                                                        else:
                                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                                                    else:
                                                        
                                                        result_logChat = selection_email_insert(list_emailChat_log)
                                                        return jsonify({'result':'OK','messageText':'Not Found Send To OneChat!','status_Code':200,'messageER':None})
                                                    
                                            return jsonify({'result':'OK','messageText':'Success!','tracking_code':getTracking['messageText'],'step_data_sid':getTracking['step_data_sid'],'convert_id':getTracking['convert_id'],'file_id':res_insert_pdf['messageText'],'file_name':fileName,'status_Code':200}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                        else:        
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template or document type not found'}),200
                            return jsonify(get_Template)
            else:
                return jsonify({'result':'ER','messageText':'parameter incorrect!','status_Code':404}),404

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','messageText':str(ex),'status_Code':200}),200
    
@status_methods.route('/api/v1/service_for_eform',methods=['POST'])
def service_for_eform_v1():
    try:        
        try:
            token_header = request.headers['Authorization']
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'Bearer Token Error!'}),401
        url = one_url + "/api/account_and_biz_detail"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer"+" "+token_header
        }
        try:
            response = requests.get(url, headers=headers, verify=False)
            response = response.json()
        except requests.Timeout as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.HTTPError as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.ConnectionError as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.RequestException as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except Exception as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        if 'result' in response:
            if response['result'] == 'Fail':
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
        else:
            biz_info = []
            thai_email = response['thai_email']
            username = response['username']
            sender_name = response['first_name_th'] + ' ' + response['last_name_th']
            if 'biz_detail' in response:
                getbiz = response['biz_detail']
                for i in range(len(getbiz)):
                    jsonData = {
                        'id':getbiz[i]['getbiz'][0]['id'],
                        'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                        'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                        'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                        'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                        'role_level':getbiz[i]['getrole'][0]['role_level'],
                        'role_name':getbiz[i]['getrole'][0]['role_name']
                    }
                    biz_info.append(jsonData)
            result_arraylist = []
            result_detail_service = {}
            dataJson = request.json
            result_CheckTaxId = []
            biz_json = ''
            chatData = []
            list_emailChat_log = []
            chatRequestData = {}
            status_sendChat = []
            result_list = []
            arr_result_Email = []
            list_taskChat_log = []
            MailData = {}
            if 'File_PDF' in dataJson and 'username' in dataJson and 'templateCode'in dataJson and 'oneEmail' in dataJson and 'taxId' in dataJson and 'DocumentType' in dataJson and len(dataJson) == 6:
                if username == dataJson['username'] and thai_email == dataJson['oneEmail']:
                    input_file      = dataJson['File_PDF']
                    username        = dataJson['username']
                    oneEmail        = dataJson['oneEmail']
                    template_code   = dataJson['templateCode']
                    tax_Id          = dataJson['taxId']  
                    Document_type   = dataJson['DocumentType']
                    fileName        = 'e-form_' + str(datetime.datetime.now()).split('.')[0].split(' ')[0] + 'T' +str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[0] + '-' + str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[1] + '-'+str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[2]
                    fileName        = str(fileName).replace(' ','') + ".pdf"
                    base64_filedata = input_file
                    if str(tax_Id).replace(' ','') is not '':
                        if len(biz_info) != 0:
                            for i in range(len(biz_info)):
                                if tax_Id == biz_info[i]['id_card_num']:
                                    result_CheckTaxId.append('Y')
                                    biz_json = biz_info[i]
                            if 'Y' in result_CheckTaxId:
                                pass
                            else:
                                return jsonify({'result':'ER','messageText':'taxId not found','status_Code':200}),200
                    else:
                        biz_json = None
                    tax_Id = str(tax_Id).replace(' ','')
                    if tax_Id != '':
                        get_Template = select().select_get_string_templateAndusername_tax_new(str(template_code).replace(' ',''),str(tax_Id).replace(' ',''))
                        if get_Template['result'] == 'OK':
                            document_details = str(get_Template['messageText'][0]['document_details_string'])
                            document_type = get_Template['messageText'][0]['document_details']['document_type']
                            string_json = eval(get_Template['messageText'][0]['data_step'])
                            string_json_NoneEval = str(get_Template['messageText'][0]['data_step'])
                            step_Max = get_Template['messageText'][0]['step_Max']
                            result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                            string_json_NoneEval = str(result_SelectEmailMe['messageText'])                     
                            string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                            qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                            getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                            getEmail_list = []
                            if getEmail['result'] == 'OK':
                                for o in range(len(getEmail['messageText'])):
                                    if 'email_result' in getEmail['messageText'][o]:
                                        for i in getEmail['messageText'][o]['email_result']:
                                            getStepNumber = getEmail['messageText'][o]['step_num']
                                            getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                            sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                            res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                            if res_insert_pdf['result'] == 'OK':
                                getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                                if getTracking['result'] == 'OK':                                    
                                    ts = int(time.time())
                                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                    result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    if result_insert['result'] == 'OK':                                        
                                        sidCode = getTracking['step_data_sid']
                                        typeFile = str(fileName).split('.')[-1]
                                        FileId = res_insert_pdf['messageText']
                                        trackingId = getTracking['messageText']
                                        result_DocumentID = document_().genarate_document_ID(document_type)
                                        getDocument = insert().insert_document_new_v(sidCode,typeFile,FileId,document_details,document_type,'M',documentID=result_DocumentID['messageText']['documentID'])
                                        if getDocument['result'] == 'OK':
                                            document_Id = getDocument['document_Id']
                                            ts = int(time.time())
                                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                            getSender = insert().insert_paper_sender_v2(username,st,'ACTIVE',sender_name,oneEmail,'owner',FileId,fileName,trackingId,sidCode,template_code,document_Id,'','')
                                            if getSender['result'] == 'OK':
                                                arr_result = []
                                                getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                                chatstatus_forservice(string_json)
                                                if getSign['result'] == 'OK':
                                                    for i in getEmail_list:
                                                        emailUser = i['email']
                                                        getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                                        if getUrl_Sign['result'] == 'OK':
                                                            arr_result.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num'],
                                                                'sendChat': i['status_chat'],
                                                                'property' : i['property']
                                                            })
                                                            arr_result_Email.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num']                                                                
                                                            })
                                                    chatRequestData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result
                                                    }
                                                    MailData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result_Email
                                                    }
                                                    data_tosender = chatRequestData['data']                                  
                                                    for n in range(len(data_tosender)):
                                                        status_sendChat.append(data_tosender[n]['sendChat'])
                                                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                                                            res_search_frd = search_frd(data_tosender[n]['email'])
                                                            
                                                            if 'status' in res_search_frd:
                                                                if res_search_frd['status'] == 'success':
                                                                    oneId = res_search_frd['friend']['one_id']
                                                                    userid_info = res_search_frd['friend']['user_id']
                                                                    resultURLIMAGE = createImage_formPDF(sidCode)
                                                                    result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                    print(result_pathUrl)
                                                                    resouce_result = select().select_forChat_v1(sidCode)
                                                                    userIdOne = res_search_frd['friend']['user_id']
                                                                    if resouce_result['result'] == 'OK':                
                                                                        res_send = send_url_tochat_new_v3(data_tosender[n]['property'],userid_info,data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl)
                                                                        print(res_send)
                                                                        if 'status' in res_send:
                                                                            if res_send['status'] == 'success':
                                                                                
                                                                                id_one_chat_to_msg = res_send['message']['id']
                                                                                update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                                                print(resultgetProject)
                                                                                
                                                                                if resultgetProject['result'] == 'OK':
                                                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                    priority_ = '1'
                                                                                    titleAndDetails = resouce_result['messageText']
                                                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                        if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                    resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId)
                                                                                    # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                    if resultSend_CreateTask['result'] == 'OK':
                                                                                        if 'status' in resultSend_CreateTask['messageText']:
                                                                                            if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                        else:
                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                    else:
                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                else:
                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                else:
                                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            elif 'result' in res_search_frd:
                                                                if res_search_frd['result'] == 'ER':                            
                                                                    arrEmail = []
                                                                    arrEmail.append(data_tosender[n]['email'])
                                                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                                                    if 'status' in resultAddfrd:
                                                                        if resultAddfrd['status'] == 'success':
                                                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                                                resultURLIMAGE = createImage_formPDF(sidCode)
                                                                                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                                print(result_pathUrl)
                                                                                resouce_result = select().select_forChat_v1(sidCode)
                                                                                if resouce_result['result'] == 'OK':                
                                                                                    res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl)
                                                                                    print(res_send)
                                                                                    if 'status' in res_send:
                                                                                        if res_send['status'] == 'success':
                                                                                            id_one_chat_to_msg = res_send['message']['id']
                                                                                            update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                            resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                                                            if resultgetProject['result'] == 'OK':
                                                                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                                priority_ = '1'
                                                                                                titleAndDetails = resouce_result['messageText']
                                                                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                                resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId)
                                                                                                # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                                if resultSend_CreateTask['result'] == 'OK':
                                                                                                    if 'status' in resultSend_CreateTask['messageText']:
                                                                                                        if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                            list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                        else:
                                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                    else:
                                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                else:
                                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                                        else:
                                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                                    else:
                                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                    else:
                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            else:
                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                        else:
                                                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    if True in status_sendChat:
                                                        result_logChat = selection_email_insert(list_emailChat_log,id_one_chat_to_msg)
                                                        if result_logChat['result'] == 'OK':
                                                            insert().insert_transactionTask(list_taskChat_log)
                                                            data_Mail = MailData['data']
                                                            for i in range(len(data_Mail)):
                                                                if data_Mail[i]['step_num'] == "1":
                                                                    result_Email = mail().check_EmailProfile(data_Mail[i]['email'])
                                                                    if result_Email['result'] == 'OK':
                                                                        data_Mail[i]['emailUser'] = result_Email['messageText']['emailUser']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                    else:
                                                                        data_Mail[i]['emailUser'] = data_Mail[i]['email']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                        # print(result_mailStatus, ' result_mailStatus')
                                                                    if result_mailStatus['result'] == 'OK':
                                                                        result_list.append({'result':'OK','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':None})
                                                                    else:
                                                                        result_list.append({'result':'ER','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':result_mailStatus['messageText']})
                                                                else:
                                                                    result_list.append({'result':'NO','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign']})
                                                            # print(result_list , ' result_list')
                                                            result_insertMail = mail().insert_logEmail(result_list)
                                                            sid_code = getTracking['step_data_sid']
                                                            sid_code_sha512 = hashlib.sha512(str(sid_code).encode('utf-8')).hexdigest()
                                                            if result_insertMail['result'] == 'OK':
                                                                return jsonify({'result':'OK','messageText':{'result_mail_service':result_list,'result_chat_service':list_emailChat_log,'id_transaction_paperless':sid_code_sha512},'status_Code':200}),200
                                                            else:
                                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insertMail['messageText']})
                                                        else:
                                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                                                    else:                                                        
                                                        result_logChat = selection_email_insert(list_emailChat_log,None)
                                                        return jsonify({'result':'OK','messageText':'Not Found Send To OneChat!','status_Code':200,'messageER':None})
                                            else:
                                                delete().delete_all_table_for_service(sidCode)  
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'upload file fail'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                        else:        
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template not found in taxId'}),200
                            return ''
                    else:
                        get_Template = select().select_get_string_templateAndusername(str(username).replace(' ',''),str(template_code).replace(' ',''))
                        # print(get_Template)
                        if get_Template['result'] == 'OK':
                            document_details = str(get_Template['messageText'][0]['document_details_string'])
                            document_type = get_Template['messageText'][0]['document_details']['document_type']
                            string_json = eval(get_Template['messageText'][0]['data_step'])
                            string_json_NoneEval = str(get_Template['messageText'][0]['data_step'])
                            step_Max = get_Template['messageText'][0]['step_Max']
                            result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                            print(result_SelectEmailMe)
                            string_json_NoneEval = str(result_SelectEmailMe['messageText'])                            
                            string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                            qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                            getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                            getEmail_list = []
                            if getEmail['result'] == 'OK':
                                for o in range(len(getEmail['messageText'])):
                                    if 'email_result' in getEmail['messageText'][o]:
                                        for i in getEmail['messageText'][o]['email_result']:
                                            getStepNumber = getEmail['messageText'][o]['step_num']
                                            getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                            # print(getEmail_list,'getEmail_list')
                            sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                            res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                            if res_insert_pdf['result'] == 'OK':
                                getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                                if getTracking['result'] == 'OK':
                                    ts = int(time.time())
                                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                    # print(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    if result_insert['result'] == 'OK':                                        
                                        sidCode = getTracking['step_data_sid']
                                        typeFile = str(fileName).split('.')[-1]
                                        FileId = res_insert_pdf['messageText']
                                        trackingId = getTracking['messageText']
                                        result_DocumentID = document_().genarate_document_ID(document_type)
                                        # print(result_DocumentID, ' result_DocumentID')
                                        getDocument = insert().insert_document_new_v(sidCode,typeFile,FileId,document_details,document_type,'M',documentID=result_DocumentID['messageText']['documentID'])
                                        
                                        if getDocument['result'] == 'OK':
                                            document_Id = getDocument['document_Id']
                                            ts = int(time.time())
                                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                            
                                            getSender = insert().insert_paper_sender_v2(username,st,'ACTIVE',sender_name,oneEmail,'owner',FileId,fileName,trackingId,sidCode,template_code,document_Id,'','')
                                            # print(getSender,'getSender')
                                            if getSender['result'] == 'OK':
                                                arr_result = []
                                                getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                                chatstatus_forservice(string_json)
                                                if getSign['result'] == 'OK':
                                                    for i in getEmail_list:
                                                        emailUser = i['email']
                                                        getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                                        if getUrl_Sign['result'] == 'OK':
                                                            arr_result.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num'],
                                                                'sendChat': i['status_chat'],
                                                                'property' : i['property']
                                                            })
                                                            print(arr_result)
                                                            arr_result_Email.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num']                                                                
                                                            })
                                                    chatRequestData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result
                                                    }
                                                    MailData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result_Email
                                                    }
                                                    data_tosender = chatRequestData['data']                                  
                                                    for n in range(len(data_tosender)):
                                                        status_sendChat.append(data_tosender[n]['sendChat'])
                                                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                                                            res_search_frd = search_frd(data_tosender[n]['email'])
                                                            oneId = res_search_frd['friend']['one_id']
                                                            if 'status' in res_search_frd:
                                                                if res_search_frd['status'] == 'success':
                                                                    resultURLIMAGE = createImage_formPDF(sidCode)
                                                                    result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                    print(result_pathUrl)
                                                                    resouce_result = select().select_forChat_v1(sidCode)
                                                                    userIdOne = res_search_frd['friend']['user_id']
                                                                    if resouce_result['result'] == 'OK':                
                                                                        res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl)
                                                                        if 'status' in res_send:
                                                                            if res_send['status'] == 'success':
                                                                                id_one_chat_to_msg = res_send['message']['id']
                                                                                update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                                                print(resultgetProject)
                                                                                
                                                                                if resultgetProject['result'] == 'OK':
                                                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                    priority_ = '1'
                                                                                    titleAndDetails = resouce_result['messageText']
                                                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                        if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                    resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId)
                                                                                    # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                    if resultSend_CreateTask['result'] == 'OK':
                                                                                        if 'status' in resultSend_CreateTask['messageText']:
                                                                                            if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                        else:
                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                    else:
                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                else:
                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                else:
                                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            elif 'result' in res_search_frd:
                                                                if res_search_frd['result'] == 'ER':                            
                                                                    arrEmail = []
                                                                    arrEmail.append(data_tosender[n]['email'])
                                                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                                                    if 'status' in resultAddfrd:
                                                                        if resultAddfrd['status'] == 'success':
                                                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                                                resultURLIMAGE = createImage_formPDF(sidCode)
                                                                                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                                print(result_pathUrl)
                                                                                resouce_result = select().select_forChat_v1(sidCode)
                                                                                if resouce_result['result'] == 'OK':                
                                                                                    res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl)
                                                                                    if 'status' in res_send:
                                                                                        if res_send['status'] == 'success':
                                                                                            id_one_chat_to_msg = res_send['message']['id']
                                                                                            update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                            resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                                                            if resultgetProject['result'] == 'OK':
                                                                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                                priority_ = '1'
                                                                                                titleAndDetails = resouce_result['messageText']
                                                                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                                resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId)
                                                                                                # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                                if resultSend_CreateTask['result'] == 'OK':
                                                                                                    if 'status' in resultSend_CreateTask['messageText']:
                                                                                                        if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                            list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                        else:
                                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                    else:
                                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                else:
                                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                                        else:
                                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                                    else:
                                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                    else:
                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            else:
                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                        else:
                                                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    if True in status_sendChat:
                                                        result_logChat = selection_email_insert(list_emailChat_log,id_one_chat_to_msg)
                                                        if result_logChat['result'] == 'OK':
                                                            insert().insert_transactionTask(list_taskChat_log)
                                                            data_Mail = MailData['data']
                                                            for i in range(len(data_Mail)):
                                                                if data_Mail[i]['step_num'] == "1":
                                                                    result_Email = mail().check_EmailProfile(data_Mail[i]['email'])
                                                                    if result_Email['result'] == 'OK':
                                                                        data_Mail[i]['emailUser'] = result_Email['messageText']['emailUser']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                    else:
                                                                        data_Mail[i]['emailUser'] = data_Mail[i]['email']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                        # print(result_mailStatus, ' result_mailStatus')
                                                                    if result_mailStatus['result'] == 'OK':
                                                                        result_list.append({'result':'OK','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':None})
                                                                    else:
                                                                        result_list.append({'result':'ER','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':result_mailStatus['messageText']})
                                                                else:
                                                                    result_list.append({'result':'NO','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign']})
                                                            # print(result_list , ' result_list')
                                                            result_insertMail = mail().insert_logEmail(result_list)
                                                            sid_code = getTracking['step_data_sid']
                                                            sid_code_sha512 = hashlib.sha512(str(sid_code).encode('utf-8')).hexdigest()
                                                            if result_insertMail['result'] == 'OK':
                                                                return jsonify({'result':'OK','messageText':{'result_mail_service':result_list,'result_chat_service':list_emailChat_log,'id_transaction_paperless':sid_code_sha512},'status_Code':200}),200
                                                            else:
                                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insertMail['messageText']})
                                                        else:
                                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                                                    else:                                                        
                                                        result_logChat = selection_email_insert(list_emailChat_log,id_one_chat_to_msg)
                                                        return jsonify({'result':'OK','messageText':'Not Found Send To OneChat!','status_Code':200,'messageER':None})
                                            else:
                                                delete().delete_all_table_for_service(sidCode)   
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'upload file fail'}),200
                                    else:
                                        
                                        return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                        else:        
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template or document type not found'}),200
                            return jsonify(get_Template)
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','messageText':str(ex),'status_Code':200}),200

@status_methods.route('/api/v2/service_for_eform',methods=['POST'])
def service_for_eform_v2():
    try:        
        try:
            token_header = request.headers['Authorization']
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'Bearer Token Error!'}),401
        url = one_url + "/api/account_and_biz_detail"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer"+" "+token_header
        }
        try:
            response = requests.get(url, headers=headers, verify=False)
            response = response.json()
        except requests.Timeout as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.HTTPError as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.ConnectionError as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.RequestException as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except Exception as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        if 'result' in response:
            if response['result'] == 'Fail':
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
        else:
            biz_info = []
            thai_email = response['thai_email']
            username = response['username']
            sender_name = response['first_name_th'] + ' ' + response['last_name_th']
            if 'biz_detail' in response:
                getbiz = response['biz_detail']
                for i in range(len(getbiz)):
                    jsonData = {
                        'id':getbiz[i]['getbiz'][0]['id'],
                        'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                        'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                        'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                        'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                        'role_level':getbiz[i]['getrole'][0]['role_level'],
                        'role_name':getbiz[i]['getrole'][0]['role_name']
                    }
                    biz_info.append(jsonData)
            result_arraylist = []
            result_detail_service = {}
            dataJson = request.json
            result_CheckTaxId = []
            biz_json = ''
            chatData = []
            list_emailChat_log = []
            chatRequestData = {}
            status_sendChat = []
            result_list = []
            arr_result_Email = []
            list_taskChat_log = []
            MailData = {}
            id_one_chat_to_msg = None
            if 'File_PDF' in dataJson and 'username' in dataJson and 'templateCode'in dataJson and 'oneEmail' in dataJson and 'taxId' in dataJson and 'DocumentType' in dataJson and 'Folder_Attachment_Name' in dataJson and len(dataJson) == 7:
                if username == dataJson['username'] and thai_email == dataJson['oneEmail']:
                    input_file      = dataJson['File_PDF']
                    username        = dataJson['username']
                    oneEmail        = dataJson['oneEmail']
                    template_code   = dataJson['templateCode']
                    tax_Id          = dataJson['taxId']  
                    Document_type   = dataJson['DocumentType']
                    Folder_Attachment_Name   = dataJson['Folder_Attachment_Name']
                    if str(Folder_Attachment_Name).replace(' ','') != '':
                        pass
                    else:
                        Folder_Attachment_Name = None
                    fileName        = 'e-form_' + str(datetime.datetime.now()).split('.')[0].split(' ')[0] + 'T' +str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[0] + '-' + str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[1] + '-'+str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[2]
                    fileName        = str(fileName).replace(' ','') + ".pdf"
                    base64_filedata = input_file
                    if str(tax_Id).replace(' ','') is not '':
                        if len(biz_info) != 0:
                            for i in range(len(biz_info)):
                                if tax_Id == biz_info[i]['id_card_num']:
                                    result_CheckTaxId.append('Y')
                                    biz_json = biz_info[i]
                            if 'Y' in result_CheckTaxId:
                                pass
                            else:
                                return jsonify({'result':'ER','messageText':'taxId not found','status_Code':200}),200
                    else:
                        biz_json = None
                    tax_Id = str(tax_Id).replace(' ','')
                    if tax_Id != '':
                        get_Template = select().select_get_string_templateAndusername_tax_new(str(template_code).replace(' ',''),str(tax_Id).replace(' ',''))
                        if get_Template['result'] == 'OK':
                            document_details = str(get_Template['messageText'][0]['document_details_string'])
                            document_type = get_Template['messageText'][0]['document_details']['document_type']
                            string_json = eval(get_Template['messageText'][0]['data_step'])
                            string_json_NoneEval = str(get_Template['messageText'][0]['data_step'])
                            step_Max = get_Template['messageText'][0]['step_Max']
                            result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                            string_json_NoneEval = str(result_SelectEmailMe['messageText'])                     
                            string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                            qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                            getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                            getEmail_list = []
                            if getEmail['result'] == 'OK':
                                for o in range(len(getEmail['messageText'])):
                                    if 'email_result' in getEmail['messageText'][o]:
                                        for i in getEmail['messageText'][o]['email_result']:
                                            getStepNumber = getEmail['messageText'][o]['step_num']
                                            getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                            sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                            res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                            if res_insert_pdf['result'] == 'OK':
                                getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                                if getTracking['result'] == 'OK':                                    
                                    ts = int(time.time())
                                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                    result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    if result_insert['result'] == 'OK':                                        
                                        sidCode = getTracking['step_data_sid']
                                        typeFile = str(fileName).split('.')[-1]
                                        FileId = res_insert_pdf['messageText']
                                        trackingId = getTracking['messageText']
                                        result_DocumentID = document_().genarate_document_ID(document_type)
                                        getDocument = insert().insert_document_new_v(sidCode,typeFile,FileId,document_details,document_type,'M',attempted_name=Folder_Attachment_Name,documentID=result_DocumentID['messageText']['documentID'])
                                        if getDocument['result'] == 'OK':
                                            document_Id = getDocument['document_Id']
                                            ts = int(time.time())
                                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                            getSender = insert().insert_paper_sender_v2(username,st,'ACTIVE',sender_name,oneEmail,'owner',FileId,fileName,trackingId,sidCode,template_code,document_Id,'','')
                                            if getSender['result'] == 'OK':
                                                arr_result = []
                                                getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                                chatstatus_forservice(string_json)
                                                if getSign['result'] == 'OK':
                                                    for i in getEmail_list:
                                                        emailUser = i['email']
                                                        getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                                        if getUrl_Sign['result'] == 'OK':
                                                            arr_result.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num'],
                                                                'sendChat': i['status_chat'],
                                                                'property' : i['property']
                                                            })
                                                            arr_result_Email.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num']                                                                
                                                            })
                                                    chatRequestData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result
                                                    }
                                                    MailData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result_Email
                                                    }
                                                    data_tosender = chatRequestData['data']                                  
                                                    for n in range(len(data_tosender)):
                                                        status_sendChat.append(data_tosender[n]['sendChat'])
                                                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                                                            res_search_frd = search_frd(data_tosender[n]['email'])
                                                            
                                                            if 'status' in res_search_frd:
                                                                if res_search_frd['status'] == 'success':
                                                                    oneId = res_search_frd['friend']['one_id']
                                                                    userid_info = res_search_frd['friend']['user_id']
                                                                    resultURLIMAGE = createImage_formPDF(sidCode)
                                                                    result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                    print(result_pathUrl)
                                                                    resouce_result = select().select_forChat_v1(sidCode)
                                                                    userIdOne = res_search_frd['friend']['user_id']
                                                                    if resouce_result['result'] == 'OK':                
                                                                        res_send = send_url_tochat_new_v3(data_tosender[n]['property'],userid_info,data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl)
                                                                        print(res_send)
                                                                        if 'status' in res_send:
                                                                            if res_send['status'] == 'success':
                                                                                
                                                                                id_one_chat_to_msg = res_send['message']['id']
                                                                                update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                                                print(resultgetProject)
                                                                                
                                                                                if resultgetProject['result'] == 'OK':
                                                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                    priority_ = '1'
                                                                                    titleAndDetails = resouce_result['messageText']
                                                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                        if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                    resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId)
                                                                                    # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                    if resultSend_CreateTask['result'] == 'OK':
                                                                                        if 'status' in resultSend_CreateTask['messageText']:
                                                                                            if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                        else:
                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                    else:
                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                else:
                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                else:
                                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            elif 'result' in res_search_frd:
                                                                if res_search_frd['result'] == 'ER':                            
                                                                    arrEmail = []
                                                                    arrEmail.append(data_tosender[n]['email'])
                                                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                                                    if 'status' in resultAddfrd:
                                                                        if resultAddfrd['status'] == 'success':
                                                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                                                resultURLIMAGE = createImage_formPDF(sidCode)
                                                                                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                                print(result_pathUrl)
                                                                                resouce_result = select().select_forChat_v1(sidCode)
                                                                                if resouce_result['result'] == 'OK':                
                                                                                    res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl)
                                                                                    print(res_send)
                                                                                    if 'status' in res_send:
                                                                                        if res_send['status'] == 'success':
                                                                                            id_one_chat_to_msg = res_send['message']['id']
                                                                                            update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                            resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                                                            if resultgetProject['result'] == 'OK':
                                                                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                                priority_ = '1'
                                                                                                titleAndDetails = resouce_result['messageText']
                                                                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                                resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId)
                                                                                                # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                                if resultSend_CreateTask['result'] == 'OK':
                                                                                                    if 'status' in resultSend_CreateTask['messageText']:
                                                                                                        if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                            list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                        else:
                                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                    else:
                                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                else:
                                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                                        else:
                                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                                    else:
                                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                    else:
                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            else:
                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                        else:
                                                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    if True in status_sendChat:
                                                        result_logChat = selection_email_insert(list_emailChat_log,id_one_chat_to_msg)
                                                        if result_logChat['result'] == 'OK':
                                                            insert().insert_transactionTask(list_taskChat_log)
                                                            data_Mail = MailData['data']
                                                            for i in range(len(data_Mail)):
                                                                if data_Mail[i]['step_num'] == "1":
                                                                    result_Email = mail().check_EmailProfile(data_Mail[i]['email'])
                                                                    if result_Email['result'] == 'OK':
                                                                        data_Mail[i]['emailUser'] = result_Email['messageText']['emailUser']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                    else:
                                                                        data_Mail[i]['emailUser'] = data_Mail[i]['email']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                        # print(result_mailStatus, ' result_mailStatus')
                                                                    if result_mailStatus['result'] == 'OK':
                                                                        result_list.append({'result':'OK','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':None})
                                                                    else:
                                                                        result_list.append({'result':'ER','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':result_mailStatus['messageText']})
                                                                else:
                                                                    result_list.append({'result':'NO','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign']})
                                                            # print(result_list , ' result_list')
                                                            result_insertMail = mail().insert_logEmail(result_list)
                                                            sid_code = getTracking['step_data_sid']
                                                            sid_code_sha512 = hashlib.sha512(str(sid_code).encode('utf-8')).hexdigest()
                                                            if result_insertMail['result'] == 'OK':
                                                                return jsonify({'result':'OK','messageText':{'result_mail_service':result_list,'result_chat_service':list_emailChat_log,'id_transaction_paperless':sid_code_sha512},'status_Code':200}),200
                                                            else:
                                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insertMail['messageText']})
                                                        else:
                                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                                                    else:                                                        
                                                        result_logChat = selection_email_insert(list_emailChat_log,None)
                                                        return jsonify({'result':'OK','messageText':'Not Found Send To OneChat!','status_Code':200,'messageER':None})
                                            else:
                                                delete().delete_all_table_for_service(sidCode)  
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'upload file fail'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                        else:        
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template not found in taxId'}),200
                            return ''
                    else:
                        get_Template = select().select_get_string_templateAndusername(str(username).replace(' ',''),str(template_code).replace(' ',''))
                        # print(get_Template)
                        if get_Template['result'] == 'OK':
                            document_details = str(get_Template['messageText'][0]['document_details_string'])
                            document_type = get_Template['messageText'][0]['document_details']['document_type']
                            string_json = eval(get_Template['messageText'][0]['data_step'])
                            string_json_NoneEval = str(get_Template['messageText'][0]['data_step'])
                            step_Max = get_Template['messageText'][0]['step_Max']
                            result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                            print(result_SelectEmailMe)
                            string_json_NoneEval = str(result_SelectEmailMe['messageText'])                            
                            string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                            qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                            getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                            getEmail_list = []
                            if getEmail['result'] == 'OK':
                                for o in range(len(getEmail['messageText'])):
                                    if 'email_result' in getEmail['messageText'][o]:
                                        for i in getEmail['messageText'][o]['email_result']:
                                            getStepNumber = getEmail['messageText'][o]['step_num']
                                            getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                            # print(getEmail_list,'getEmail_list')
                            sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                            res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                            if res_insert_pdf['result'] == 'OK':
                                getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                                if getTracking['result'] == 'OK':
                                    ts = int(time.time())
                                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                    # print(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    if result_insert['result'] == 'OK':                                        
                                        sidCode = getTracking['step_data_sid']
                                        typeFile = str(fileName).split('.')[-1]
                                        FileId = res_insert_pdf['messageText']
                                        trackingId = getTracking['messageText']
                                        result_DocumentID = document_().genarate_document_ID(document_type)
                                        # print(result_DocumentID, ' result_DocumentID')
                                        getDocument = insert().insert_document_new_v(sidCode,typeFile,FileId,document_details,document_type,'M',attempted_name=Folder_Attachment_Name,documentID=result_DocumentID['messageText']['documentID'])
                                        
                                        if getDocument['result'] == 'OK':
                                            document_Id = getDocument['document_Id']
                                            ts = int(time.time())
                                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                            
                                            getSender = insert().insert_paper_sender_v2(username,st,'ACTIVE',sender_name,oneEmail,'owner',FileId,fileName,trackingId,sidCode,template_code,document_Id,'','')
                                            # print(getSender,'getSender')
                                            if getSender['result'] == 'OK':
                                                arr_result = []
                                                getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                                chatstatus_forservice(string_json)
                                                if getSign['result'] == 'OK':
                                                    for i in getEmail_list:
                                                        emailUser = i['email']
                                                        getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                                        if getUrl_Sign['result'] == 'OK':
                                                            arr_result.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num'],
                                                                'sendChat': i['status_chat'],
                                                                'property' : i['property']
                                                            })
                                                            print(arr_result)
                                                            arr_result_Email.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num']                                                                
                                                            })
                                                    chatRequestData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result
                                                    }
                                                    MailData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result_Email
                                                    }
                                                    data_tosender = chatRequestData['data']                                  
                                                    for n in range(len(data_tosender)):
                                                        status_sendChat.append(data_tosender[n]['sendChat'])
                                                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                                                            res_search_frd = search_frd(data_tosender[n]['email'])
                                                            oneId = res_search_frd['friend']['one_id']
                                                            if 'status' in res_search_frd:
                                                                if res_search_frd['status'] == 'success':
                                                                    resultURLIMAGE = createImage_formPDF(sidCode)
                                                                    result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                    print(result_pathUrl)
                                                                    resouce_result = select().select_forChat_v1(sidCode)
                                                                    userIdOne = res_search_frd['friend']['user_id']
                                                                    if resouce_result['result'] == 'OK':                
                                                                        res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl)
                                                                        if 'status' in res_send:
                                                                            if res_send['status'] == 'success':
                                                                                id_one_chat_to_msg = res_send['message']['id']
                                                                                update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                                                print(resultgetProject)
                                                                                
                                                                                if resultgetProject['result'] == 'OK':
                                                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                    priority_ = '1'
                                                                                    titleAndDetails = resouce_result['messageText']
                                                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                        if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                    resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId)
                                                                                    # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                    if resultSend_CreateTask['result'] == 'OK':
                                                                                        if 'status' in resultSend_CreateTask['messageText']:
                                                                                            if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                        else:
                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                    else:
                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                else:
                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                else:
                                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            elif 'result' in res_search_frd:
                                                                if res_search_frd['result'] == 'ER':                            
                                                                    arrEmail = []
                                                                    arrEmail.append(data_tosender[n]['email'])
                                                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                                                    if 'status' in resultAddfrd:
                                                                        if resultAddfrd['status'] == 'success':
                                                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                                                resultURLIMAGE = createImage_formPDF(sidCode)
                                                                                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                                print(result_pathUrl)
                                                                                resouce_result = select().select_forChat_v1(sidCode)
                                                                                if resouce_result['result'] == 'OK':                
                                                                                    res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl)
                                                                                    if 'status' in res_send:
                                                                                        if res_send['status'] == 'success':
                                                                                            id_one_chat_to_msg = res_send['message']['id']
                                                                                            update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                            resultgetProject = sendtask_getProject_tochat_v1(oneId)
                                                                                            if resultgetProject['result'] == 'OK':
                                                                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                                priority_ = '1'
                                                                                                titleAndDetails = resouce_result['messageText']
                                                                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                                resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId)
                                                                                                # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                                if resultSend_CreateTask['result'] == 'OK':
                                                                                                    if 'status' in resultSend_CreateTask['messageText']:
                                                                                                        if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                            list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                        else:
                                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                    else:
                                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                else:
                                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                                        else:
                                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                                    else:
                                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                    else:
                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            else:
                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                        else:
                                                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    if True in status_sendChat:
                                                        result_logChat = selection_email_insert(list_emailChat_log,id_one_chat_to_msg)
                                                        if result_logChat['result'] == 'OK':
                                                            insert().insert_transactionTask(list_taskChat_log)
                                                            data_Mail = MailData['data']
                                                            for i in range(len(data_Mail)):
                                                                if data_Mail[i]['step_num'] == "1":
                                                                    result_Email = mail().check_EmailProfile(data_Mail[i]['email'])
                                                                    if result_Email['result'] == 'OK':
                                                                        data_Mail[i]['emailUser'] = result_Email['messageText']['emailUser']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                    else:
                                                                        data_Mail[i]['emailUser'] = data_Mail[i]['email']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                        # print(result_mailStatus, ' result_mailStatus')
                                                                    if result_mailStatus['result'] == 'OK':
                                                                        result_list.append({'result':'OK','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':None})
                                                                    else:
                                                                        result_list.append({'result':'ER','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':result_mailStatus['messageText']})
                                                                else:
                                                                    result_list.append({'result':'NO','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign']})
                                                            # print(result_list , ' result_list')
                                                            result_insertMail = mail().insert_logEmail(result_list)
                                                            sid_code = getTracking['step_data_sid']
                                                            sid_code_sha512 = hashlib.sha512(str(sid_code).encode('utf-8')).hexdigest()
                                                            if result_insertMail['result'] == 'OK':
                                                                return jsonify({'result':'OK','messageText':{'result_mail_service':result_list,'result_chat_service':list_emailChat_log,'id_transaction_paperless':sid_code_sha512},'status_Code':200}),200
                                                            else:
                                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insertMail['messageText']})
                                                        else:
                                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                                                    else:                                                        
                                                        result_logChat = selection_email_insert(list_emailChat_log,id_one_chat_to_msg)
                                                        return jsonify({'result':'OK','messageText':'Not Found Send To OneChat!','status_Code':200,'messageER':None})
                                            else:
                                                delete().delete_all_table_for_service(sidCode)   
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'upload file fail'}),200
                                    else:
                                        
                                        return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                        else:        
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template or document type not found'}),200
                            return jsonify(get_Template)
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','messageText':str(ex),'status_Code':200}),200

@status_methods.route('/api/v3/service_for_eform',methods=['POST'])
def service_for_eform_v3():
    try:        
        try:
            token_header = request.headers['Authorization']
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'Bearer Token Error!'}),401
        url = one_url + "/api/account_and_biz_detail"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer"+" "+token_header
        }
        try:
            response = requests.get(url, headers=headers, verify=False)
            response = response.json()
        except requests.Timeout as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.HTTPError as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.ConnectionError as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.RequestException as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except Exception as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        if 'result' in response:
            if response['result'] == 'Fail':
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
        else:
            biz_info = []
            thai_email = response['thai_email']
            username = response['username']
            sender_name = response['first_name_th'] + ' ' + response['last_name_th']
            if 'biz_detail' in response:
                getbiz = response['biz_detail']
                for i in range(len(getbiz)):
                    jsonData = {
                        'id':getbiz[i]['getbiz'][0]['id'],
                        'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                        'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                        'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                        'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                        'role_level':getbiz[i]['getrole'][0]['role_level'],
                        'role_name':getbiz[i]['getrole'][0]['role_name']
                    }
                    biz_info.append(jsonData)
            result_arraylist = []
            result_detail_service = {}
            dataJson = request.json
            result_CheckTaxId = []
            biz_json = ''
            chatData = []
            list_emailChat_log = []
            chatRequestData = {}
            status_sendChat = []
            result_list = []
            arr_result_Email = []
            list_taskChat_log = []
            MailData = {}
            id_one_chat_to_msg = None
            if 'File_PDF' in dataJson and 'username' in dataJson and 'templateDetails'in dataJson and 'oneEmail' in dataJson and 'taxId' in dataJson and 'DocumentType' in dataJson and 'Folder_Attachment_Name' in dataJson and len(dataJson) == 7:
                if username == dataJson['username'] and thai_email == dataJson['oneEmail']:
                    input_file      = dataJson['File_PDF']
                    username        = dataJson['username']
                    oneEmail        = dataJson['oneEmail']
                    template_detils = dataJson['templateDetails']
                    try:
                        null = None
                        template_detils_eval = eval(template_detils)
                        template_code = template_detils_eval['Template_Code']
                        template_step = template_detils_eval['Template_step']
                        # print(template_code)
                    except Exception as e:
                        print(str(e))
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template details error'}),200
                    # print(template_detils_eval)
                    # template_code   = dataJson['templateDetails']
                    tax_Id          = dataJson['taxId']  
                    Document_type   = dataJson['DocumentType']
                    Folder_Attachment_Name   = dataJson['Folder_Attachment_Name']
                    if str(Folder_Attachment_Name).replace(' ','') != '':
                        pass
                    else:
                        Folder_Attachment_Name = None
                    fileName        = 'e-form_' + str(datetime.datetime.now()).split('.')[0].split(' ')[0] + 'T' +str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[0] + '-' + str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[1] + '-'+str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[2]
                    fileName        = str(fileName).replace(' ','') + ".pdf"
                    base64_filedata = input_file
                    if str(tax_Id).replace(' ','') is not '':
                        if len(biz_info) != 0:
                            for i in range(len(biz_info)):
                                if tax_Id == biz_info[i]['id_card_num']:
                                    result_CheckTaxId.append('Y')
                                    biz_json = biz_info[i]
                            if 'Y' in result_CheckTaxId:
                                pass
                            else:
                                return jsonify({'result':'ER','messageText':'taxId not found','status_Code':200}),200
                    else:
                        biz_json = None
                    tax_Id = str(tax_Id).replace(' ','')
                    list_eval = []
                    list_tmp_step_num = []
                    if tax_Id != '':
                        get_Template = select().select_get_string_templateAndusername_tax_new(str(template_code).replace(' ',''),str(tax_Id).replace(' ',''))
                        # return jsonify({'messageText':get_Template})
                        # return ''
                        if get_Template['result'] == 'OK':
                            # print(template_step)
                            # return ''
                            for zzi in range(len(template_step)):
                                one_email_info = template_step[zzi]['one_email']
                                for uzi in range(len(one_email_info)):
                                    if str(one_email_info[uzi]).replace(' ','') == '':
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found :email in list'}),200
                                    else:
                                        emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", str(one_email_info[uzi]).replace(' ',''))
                                        if emails is None:
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'email in list error'}),200
                                        else:
                                            pass
                                    
                                    eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                    if 'step_num' in eval_data_step:
                                        print((eval_data_step))
                                        step_num_in_db = eval_data_step['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                        eval_data_step = (eval_data_step)
                                        string_json = eval_data_step
                                    else:
                                        step_num_in_db = eval_data_step[zzi]['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            if step_num_in_db not in list_tmp_step_num:
                                                list_tmp_step_num.append(step_num_in_db)
                                                for uugg in range(len(template_step[zzi]['one_email'])):
                                                    eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                list_eval.append(eval_data_step[zzi])
                                        string_json = (list_eval)
                            string_json_NoneEval = str(string_json)
                            document_details = str(get_Template['messageText'][0]['document_details_string'])
                            document_type = get_Template['messageText'][0]['document_details']['document_type']
                            # string_json = eval(get_Template['messageText'][0]['data_step'])
                            # string_json_NoneEval = str(get_Template['messageText'][0]['data_step'])
                            step_Max = get_Template['messageText'][0]['step_Max']
                            result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                            return jsonify({'messageText':result_SelectEmailMe})
                            string_json_NoneEval = str(result_SelectEmailMe['messageText'])                     
                            string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                            qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                            tmp_digit_sign = get_Template['messageText'][0]['digit_sign']
                            getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                            getEmail_list = []
                            if getEmail['result'] == 'OK':
                                for o in range(len(getEmail['messageText'])):
                                    if 'email_result' in getEmail['messageText'][o]:
                                        for i in getEmail['messageText'][o]['email_result']:
                                            getStepNumber = getEmail['messageText'][o]['step_num']
                                            getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                            sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                            res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                            
                            if res_insert_pdf['result'] == 'OK':
                                getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                                if getTracking['result'] == 'OK':                                    
                                    ts = int(time.time())
                                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                    result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    if result_insert['result'] == 'OK':                                        
                                        sidCode = getTracking['step_data_sid']
                                        typeFile = str(fileName).split('.')[-1]
                                        FileId = res_insert_pdf['messageText']
                                        trackingId = getTracking['messageText']
                                        result_DocumentID = document_().genarate_document_ID(document_type)
                                        options_page_string = {'subject_text': '<ไม่มีหัวเรื่อง>', 'body_text': fileName}
                                        getDocument = insert().insert_document_new_v(sidCode,typeFile,FileId,document_details,document_type,'M',digit_sign=tmp_digit_sign,attempted_name=Folder_Attachment_Name,documentID=result_DocumentID['messageText']['documentID'],options_page=options_page_string)
                                        if getDocument['result'] == 'OK':
                                            document_Id = getDocument['document_Id']
                                            ts = int(time.time())
                                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                            getSender = insert().insert_paper_sender_v2(username,st,'ACTIVE',sender_name,oneEmail,'owner',FileId,fileName,trackingId,sidCode,template_code,document_Id,'','')
                                            if getSender['result'] == 'OK':
                                                arr_result = []
                                                getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                                chatstatus_forservice(string_json)
                                                
                                                if getSign['result'] == 'OK':
                                                    print(getEmail_list)
                                                    for i in getEmail_list:
                                                        emailUser = i['email']
                                                        getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                                        
                                                        if getUrl_Sign['result'] == 'OK':
                                                            arr_result.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num'],
                                                                'sendChat': i['status_chat'],
                                                                'property' : i['property']
                                                            })
                                                            arr_result_Email.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num']                                                                
                                                            })
                                                    chatRequestData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result
                                                    }
                                                    MailData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result_Email
                                                    }
                                                    data_tosender = chatRequestData['data']                                  
                                                    for n in range(len(data_tosender)):
                                                        status_sendChat.append(data_tosender[n]['sendChat'])
                                                        print(data_tosender[n])
                                                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                                                            res_search_frd = search_frd(data_tosender[n]['email'],token_header)
                                                            
                                                            if 'status' in res_search_frd:
                                                                if res_search_frd['status'] == 'success':
                                                                    oneId = res_search_frd['friend']['one_id']
                                                                    userid_info = res_search_frd['friend']['user_id']
                                                                    resultURLIMAGE = createImage_formPDF(sidCode)
                                                                    result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                    print(result_pathUrl)
                                                                    resouce_result = select().select_forChat_v1(sidCode)
                                                                    userIdOne = res_search_frd['friend']['user_id']
                                                                    if resouce_result['result'] == 'OK':                
                                                                        res_send = send_url_tochat_new_v3(data_tosender[n]['property'],userid_info,data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl,token_header)
                                                                        print(res_send)
                                                                        if 'status' in res_send:
                                                                            if res_send['status'] == 'success':
                                                                                
                                                                                id_one_chat_to_msg = res_send['message']['id']
                                                                                update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                resultgetProject = sendtask_getProject_tochat_v1(oneId,token_header)
                                                                                print(resultgetProject)
                                                                                
                                                                                if resultgetProject['result'] == 'OK':
                                                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                    priority_ = '1'
                                                                                    titleAndDetails = resouce_result['messageText']
                                                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                        if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                    resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId,token_header)
                                                                                    # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                    if resultSend_CreateTask['result'] == 'OK':
                                                                                        if 'status' in resultSend_CreateTask['messageText']:
                                                                                            if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                        else:
                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                    else:
                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                else:
                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                else:
                                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            elif 'result' in res_search_frd:
                                                                if res_search_frd['result'] == 'ER':                            
                                                                    arrEmail = []
                                                                    arrEmail.append(data_tosender[n]['email'])
                                                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                                                    if 'status' in resultAddfrd:
                                                                        if resultAddfrd['status'] == 'success':
                                                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                                                resultURLIMAGE = createImage_formPDF(sidCode)
                                                                                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                                print(result_pathUrl)
                                                                                resouce_result = select().select_forChat_v1(sidCode)
                                                                                if resouce_result['result'] == 'OK':                
                                                                                    res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl,token_header)
                                                                                    print(res_send)
                                                                                    if 'status' in res_send:
                                                                                        if res_send['status'] == 'success':
                                                                                            id_one_chat_to_msg = res_send['message']['id']
                                                                                            update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                            resultgetProject = sendtask_getProject_tochat_v1(oneId,token_header)
                                                                                            if resultgetProject['result'] == 'OK':
                                                                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                                priority_ = '1'
                                                                                                titleAndDetails = resouce_result['messageText']
                                                                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                                resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId,token_header)
                                                                                                # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                                if resultSend_CreateTask['result'] == 'OK':
                                                                                                    if 'status' in resultSend_CreateTask['messageText']:
                                                                                                        if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                            list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                        else:
                                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                    else:
                                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                else:
                                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                                        else:
                                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                                    else:
                                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                    else:
                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            else:
                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                        else:
                                                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    print(list_emailChat_log)
                                                    if True in status_sendChat:
                                                        result_logChat = selection_email_insert(list_emailChat_log,id_one_chat_to_msg)
                                                        if result_logChat['result'] == 'OK':
                                                            insert().insert_transactionTask(list_taskChat_log)
                                                            data_Mail = MailData['data']
                                                            for i in range(len(data_Mail)):
                                                                if data_Mail[i]['step_num'] == "1":
                                                                    result_Email = mail().check_EmailProfile(data_Mail[i]['email'])
                                                                    if result_Email['result'] == 'OK':
                                                                        data_Mail[i]['emailUser'] = result_Email['messageText']['emailUser']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                    else:
                                                                        data_Mail[i]['emailUser'] = data_Mail[i]['email']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                        # print(result_mailStatus, ' result_mailStatus')
                                                                    if result_mailStatus['result'] == 'OK':
                                                                        result_list.append({'result':'OK','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':None})
                                                                    else:
                                                                        result_list.append({'result':'ER','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':result_mailStatus['messageText']})
                                                                else:
                                                                    result_list.append({'result':'NO','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign']})
                                                            # print(result_list , ' result_list')
                                                            result_insertMail = mail().insert_logEmail(result_list)
                                                            sid_code = getTracking['step_data_sid']
                                                            sid_code_sha512 = hashlib.sha512(str(sid_code).encode('utf-8')).hexdigest()
                                                            if result_insertMail['result'] == 'OK':
                                                                return jsonify({'result':'OK','messageText':{'result_mail_service':result_list,'result_chat_service':list_emailChat_log,'id_transaction_paperless':sid_code_sha512,'url_tracking':'https://paperless.one.th/tracking?id=' + trackingId},'status_Code':200}),200
                                                            else:
                                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insertMail['messageText']})
                                                        else:
                                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                                                    else:                                                        
                                                        sid_code = getTracking['step_data_sid']
                                                        sid_code_sha512 = hashlib.sha512(str(sid_code).encode('utf-8')).hexdigest()                                                      
                                                        result_logChat = selection_email_insert(list_emailChat_log,None)
                                                        return jsonify({'result':'OK','messageText':{'msg':'Not Found Send To OneChat!','id_transaction_paperless':sid_code_sha512,'url_tracking':'https://paperless.one.th/tracking?id=' + trackingId},'status_Code':200,'messageER':None})
                                            else:
                                                delete().delete_all_table_for_service(sidCode)  
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'upload file fail'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                        else:        
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template not found in taxId'}),200
                            return ''
                    else:
                        get_Template = select().select_get_string_templateAndusername(str(username).replace(' ',''),str(template_code).replace(' ',''))
                        # print(get_Template)
                        # return ''
                        if get_Template['result'] == 'OK':
                            for zzi in range(len(template_step)):
                                one_email_info = template_step[zzi]['one_email']
                                for uzi in range(len(one_email_info)):
                                    if str(one_email_info[uzi]).replace(' ','') == '':
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found :email in list'}),200
                                    else:
                                        emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", str(one_email_info[uzi]).replace(' ',''))
                                        if emails is None:
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'email in list error'}),200
                                        else:
                                            pass
                                    
                                    eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                    if 'step_num' in eval_data_step:
                                        print((eval_data_step))
                                        step_num_in_db = eval_data_step['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                        eval_data_step = (eval_data_step)
                                        string_json = eval_data_step
                                    else:
                                        step_num_in_db = eval_data_step[zzi]['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                        list_eval.append(eval_data_step[zzi])
                                        string_json = (list_eval)
                            string_json_NoneEval = str(string_json)
                            document_details = str(get_Template['messageText'][0]['document_details_string'])
                            document_type = get_Template['messageText'][0]['document_details']['document_type']
                            # string_json = eval(get_Template['messageText'][0]['data_step'])
                            # string_json_NoneEval = str(get_Template['messageText'][0]['data_step'])
                            step_Max = get_Template['messageText'][0]['step_Max']                            
                            tmp_digit_sign = get_Template['messageText'][0]['digit_sign']
                            result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                            print(result_SelectEmailMe)
                            string_json_NoneEval = str(result_SelectEmailMe['messageText'])                            
                            string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                            qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                            getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                            getEmail_list = []
                            if getEmail['result'] == 'OK':
                                for o in range(len(getEmail['messageText'])):
                                    if 'email_result' in getEmail['messageText'][o]:
                                        for i in getEmail['messageText'][o]['email_result']:
                                            getStepNumber = getEmail['messageText'][o]['step_num']
                                            getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                            # print(getEmail_list,'getEmail_list')
                            sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                            res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                            if res_insert_pdf['result'] == 'OK':
                                getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                                if getTracking['result'] == 'OK':
                                    ts = int(time.time())
                                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                    # print(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    if result_insert['result'] == 'OK':                                        
                                        sidCode = getTracking['step_data_sid']
                                        typeFile = str(fileName).split('.')[-1]
                                        FileId = res_insert_pdf['messageText']
                                        trackingId = getTracking['messageText']
                                        result_DocumentID = document_().genarate_document_ID(document_type)
                                        # print(result_DocumentID, ' result_DocumentID')
                                        options_page_string = {'subject_text': '<ไม่มีหัวเรื่อง>', 'body_text': fileName}
                                        getDocument = insert().insert_document_new_v(sidCode,typeFile,FileId,document_details,document_type,'M',digit_sign=tmp_digit_sign,attempted_name=Folder_Attachment_Name,documentID=result_DocumentID['messageText']['documentID'],options_page=options_page_string)
                                        if getDocument['result'] == 'OK':
                                            document_Id = getDocument['document_Id']
                                            ts = int(time.time())
                                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                            
                                            getSender = insert().insert_paper_sender_v2(username,st,'ACTIVE',sender_name,oneEmail,'owner',FileId,fileName,trackingId,sidCode,template_code,document_Id,'','')
                                            # print(getSender,'getSender')
                                            if getSender['result'] == 'OK':
                                                arr_result = []
                                                getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                                return ''
                                                chatstatus_forservice(string_json)
                                                if getSign['result'] == 'OK':
                                                    for i in getEmail_list:
                                                        emailUser = i['email']
                                                        getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                                        if getUrl_Sign['result'] == 'OK':
                                                            arr_result.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num'],
                                                                'sendChat': i['status_chat'],
                                                                'property' : i['property']
                                                            })
                                                            print(arr_result)
                                                            arr_result_Email.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num']                                                                
                                                            })
                                                    chatRequestData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result
                                                    }
                                                    MailData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result_Email
                                                    }
                                                    data_tosender = chatRequestData['data']                                  
                                                    for n in range(len(data_tosender)):
                                                        status_sendChat.append(data_tosender[n]['sendChat'])
                                                        
                                                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                                                            res_search_frd = search_frd(data_tosender[n]['email'],token_header)
                                                            oneId = res_search_frd['friend']['one_id']
                                                            if 'status' in res_search_frd:
                                                                if res_search_frd['status'] == 'success':
                                                                    resultURLIMAGE = createImage_formPDF(sidCode)
                                                                    result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                    print(result_pathUrl)
                                                                    resouce_result = select().select_forChat_v1(sidCode)
                                                                    userIdOne = res_search_frd['friend']['user_id']
                                                                    if resouce_result['result'] == 'OK':                
                                                                        res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl,token_header)
                                                                        if 'status' in res_send:
                                                                            if res_send['status'] == 'success':
                                                                                id_one_chat_to_msg = res_send['message']['id']
                                                                                update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                resultgetProject = sendtask_getProject_tochat_v1(oneId,token_header)
                                                                                print(resultgetProject)
                                                                                
                                                                                if resultgetProject['result'] == 'OK':
                                                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                    priority_ = '1'
                                                                                    titleAndDetails = resouce_result['messageText']
                                                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                        if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                    resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId,token_header)
                                                                                    # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                    if resultSend_CreateTask['result'] == 'OK':
                                                                                        if 'status' in resultSend_CreateTask['messageText']:
                                                                                            if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                        else:
                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                    else:
                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                else:
                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                else:
                                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            elif 'result' in res_search_frd:
                                                                if res_search_frd['result'] == 'ER':                            
                                                                    arrEmail = []
                                                                    arrEmail.append(data_tosender[n]['email'])
                                                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                                                    if 'status' in resultAddfrd:
                                                                        if resultAddfrd['status'] == 'success':
                                                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                                                resultURLIMAGE = createImage_formPDF(sidCode)
                                                                                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                                print(result_pathUrl)
                                                                                resouce_result = select().select_forChat_v1(sidCode)
                                                                                if resouce_result['result'] == 'OK':                
                                                                                    res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl)
                                                                                    if 'status' in res_send:
                                                                                        if res_send['status'] == 'success':
                                                                                            id_one_chat_to_msg = res_send['message']['id']
                                                                                            update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                            resultgetProject = sendtask_getProject_tochat_v1(oneId,token_header)
                                                                                            if resultgetProject['result'] == 'OK':
                                                                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                                priority_ = '1'
                                                                                                titleAndDetails = resouce_result['messageText']
                                                                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                                resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId,token_header)
                                                                                                # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                                if resultSend_CreateTask['result'] == 'OK':
                                                                                                    if 'status' in resultSend_CreateTask['messageText']:
                                                                                                        if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                            list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                        else:
                                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                    else:
                                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                else:
                                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                                        else:
                                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                                    else:
                                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                    else:
                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            else:
                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                        else:
                                                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    if True in status_sendChat:
                                                        result_logChat = selection_email_insert(list_emailChat_log,id_one_chat_to_msg)
                                                        if result_logChat['result'] == 'OK':
                                                            insert().insert_transactionTask(list_taskChat_log)
                                                            data_Mail = MailData['data']
                                                            for i in range(len(data_Mail)):
                                                                if data_Mail[i]['step_num'] == "1":
                                                                    result_Email = mail().check_EmailProfile(data_Mail[i]['email'])
                                                                    if result_Email['result'] == 'OK':
                                                                        data_Mail[i]['emailUser'] = result_Email['messageText']['emailUser']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                    else:
                                                                        data_Mail[i]['emailUser'] = data_Mail[i]['email']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                        # print(result_mailStatus, ' result_mailStatus')
                                                                    if result_mailStatus['result'] == 'OK':
                                                                        result_list.append({'result':'OK','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':None})
                                                                    else:
                                                                        result_list.append({'result':'ER','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':result_mailStatus['messageText']})
                                                                else:
                                                                    result_list.append({'result':'NO','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign']})
                                                            # print(result_list , ' result_list')
                                                            result_insertMail = mail().insert_logEmail(result_list)
                                                            sid_code = getTracking['step_data_sid']
                                                            sid_code_sha512 = hashlib.sha512(str(sid_code).encode('utf-8')).hexdigest()
                                                            if result_insertMail['result'] == 'OK':
                                                                return jsonify({'result':'OK','messageText':{'result_mail_service':result_list,'result_chat_service':list_emailChat_log,'id_transaction_paperless':sid_code_sha512,'url_tracking':'https://paperless.one.th/tracking?id=' + trackingId},'status_Code':200}),200
                                                            else:
                                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insertMail['messageText']})
                                                        else:
                                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                                                    else:  
                                                        sid_code = getTracking['step_data_sid']
                                                        sid_code_sha512 = hashlib.sha512(str(sid_code).encode('utf-8')).hexdigest()                                                      
                                                        result_logChat = selection_email_insert(list_emailChat_log,id_one_chat_to_msg)
                                                        return jsonify({'result':'OK','messageText':{'msg':'Not Found Send To OneChat!','id_transaction_paperless':sid_code_sha512,'url_tracking':'https://paperless.one.th/tracking?id=' + trackingId},'status_Code':200,'messageER':None})
                                            else:
                                                delete().delete_all_table_for_service(sidCode)   
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'upload file fail'}),200
                                    else:
                                        
                                        return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                        else:        
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template or document type not found'}),200
                            return jsonify(get_Template)
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'cant get username and email'}),401
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','messageText':str(ex),'status_Code':200}),200

@status_methods.route('/api/v4/service_for_eform',methods=['POST'])
def service_for_eform_v4():
    try:        
        try:
            token_header = request.headers['Authorization']
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'unauthorized'}),401
        url = one_url + "/api/account_and_biz_detail"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer"+" "+token_header
        }
        try:
            response = requests.get(url, headers=headers, verify=False)
            response = response.json()
        except requests.Timeout as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'unauthorized'}),401
        except requests.HTTPError as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'unauthorized'}),401
        except requests.ConnectionError as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'unauthorized'}),401
        except requests.RequestException as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'unauthorized'}),401
        except Exception as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'unauthorized'}),401
        if 'result' in response:
            if response['result'] == 'Fail':
                abort(401)
        else:
            
            biz_info = []
            thai_email = response['thai_email']
            username = response['username']
            sender_name = response['first_name_th'] + ' ' + response['last_name_th']
            if 'biz_detail' in response:
                getbiz = response['biz_detail']
                for i in range(len(getbiz)):
                    jsonData = {
                        'id':getbiz[i]['getbiz'][0]['id'],
                        'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                        'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                        'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                        'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                        'role_level':getbiz[i]['getrole'][0]['role_level'],
                        'role_name':getbiz[i]['getrole'][0]['role_name']
                    }
                    biz_info.append(jsonData)
            result_arraylist = []
            result_detail_service = {}
            dataJson = request.json
            result_CheckTaxId = []
            biz_json = ''
            chatData = []
            list_emailChat_log = []
            chatRequestData = {}
            status_sendChat = []
            result_list = []
            arr_result_Email = []
            list_taskChat_log = []
            MailData = {}
            id_one_chat_to_msg = None
            if 'File_PDF' in dataJson and 'username' in dataJson and 'templateDetails'in dataJson and 'oneEmail' in dataJson and 'taxId' in dataJson\
            and 'DocumentType' in dataJson and 'Folder_Attachment_Name' in dataJson and 'subject_text' in dataJson and 'body_text' in dataJson and len(dataJson) == 9:
                if username == dataJson['username'] and thai_email == dataJson['oneEmail']:
                    input_file      = dataJson['File_PDF']
                    username        = dataJson['username']
                    oneEmail        = dataJson['oneEmail']
                    template_detils = dataJson['templateDetails']
                    options_page_string = {
                        'subject_text': dataJson['subject_text'], 
                        'body_text': dataJson['body_text']
                    }
                    try:
                        null = None
                        template_detils_eval = eval(template_detils)
                        template_code = template_detils_eval['Template_Code']
                        template_step = template_detils_eval['Template_step']
                        # print(template_code)
                    except Exception as e:
                        print(str(e))
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template details error'}),200
                    # print(template_detils_eval)
                    # template_code   = dataJson['templateDetails']
                    tax_Id          = dataJson['taxId']  
                    Document_type   = dataJson['DocumentType']
                    Folder_Attachment_Name   = dataJson['Folder_Attachment_Name']
                    if str(Folder_Attachment_Name).replace(' ','') != '':
                        tmp_attemp_status = True
                    else:
                        tmp_attemp_status = False
                        Folder_Attachment_Name = None
                    fileName        = 'e-form_' + str(datetime.datetime.now()).split('.')[0].split(' ')[0] + 'T' +str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[0] + '-' + str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[1] + '-'+str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[2]
                    fileName        = str(fileName).replace(' ','') + ".pdf"
                    base64_filedata = input_file
                    if str(tax_Id).replace(' ','') is not '':
                        if len(biz_info) != 0:
                            for i in range(len(biz_info)):
                                if tax_Id == biz_info[i]['id_card_num']:
                                    result_CheckTaxId.append('Y')
                                    biz_json = biz_info[i]
                            if 'Y' in result_CheckTaxId:
                                pass
                            else:
                                return jsonify({'result':'ER','messageText':'taxId not found','status_Code':200}),200
                    else:
                        biz_json = None
                    tax_Id = str(tax_Id).replace(' ','')
                    list_eval = []
                    list_tmp_step_num = []
                    if tax_Id != '':
                        get_Template = select().select_get_string_templateAndusername_tax_new(str(template_code).replace(' ',''),str(tax_Id).replace(' ',''))
                        if get_Template['result'] == 'OK':
                            for zzi in range(len(template_step)):
                                one_email_info = template_step[zzi]['one_email']
                                # print(one_email_info)
                                # return ''
                                if len(one_email_info) != 0:
                                    for uzi in range(len(one_email_info)):
                                        if str(one_email_info[uzi]).replace(' ','') == '':
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found :email in list'}),200
                                        else:
                                            emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", str(one_email_info[uzi]).replace(' ',''))
                                            if emails is None:
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'email in list error'}),200
                                            else:
                                                pass
                                        
                                        eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                        
                                        if 'step_num' in eval_data_step:
                                            # print((eval_data_step))
                                            step_num_in_db = eval_data_step['step_num']
                                            if template_step[zzi]['step_num'] == step_num_in_db:
                                                for uugg in range(len(template_step[zzi]['one_email'])):
                                                    eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                    list_eval.append(eval_data_step)
                                            eval_data_step = (eval_data_step)
                                            string_json = eval_data_step
                                        
                                        else:
                                            # # print(eval_data_step)
                                            # print(template_step[zzi]['one_email'])
                                            step_num_in_db = eval_data_step[zzi]['step_num']
                                            if template_step[zzi]['step_num'] == step_num_in_db:
                                                if step_num_in_db not in list_tmp_step_num:
                                                    list_tmp_step_num.append(step_num_in_db)
                                                    # print(template_step[zzi]['one_email'])
                                                    if len(template_step[zzi]['one_email']) != 0:
                                                        for uugg in range(len(template_step[zzi]['one_email'])):
                                                            eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                    else:
                                                        eval_data_step[zzi]['step_detail'][uugg]['one_email'] = ""
                                                        # print(eval_data_step[zzi])
                                                    list_eval.append(eval_data_step[zzi])
                                            string_json = (list_eval)
                                else:
                                    # if str(one_email_info).replace(' ','') == '':
                                    #     return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found :email in list'}),200
                                    # else:
                                    #     emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", str(one_email_info).replace(' ',''))
                                    #     if emails is None:
                                    #         return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'email in list error'}),200
                                    #     else:
                                    #         pass
                                    
                                    eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                    
                                    if 'step_num' in eval_data_step:
                                        # print((eval_data_step))
                                        step_num_in_db = eval_data_step['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                list_eval.append(eval_data_step)
                                        eval_data_step = (eval_data_step)
                                        string_json = eval_data_step
                                    
                                    else:
                                        # # print(eval_data_step)
                                        # print(template_step[zzi]['one_email'])
                                        step_num_in_db = eval_data_step[zzi]['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            if step_num_in_db not in list_tmp_step_num:
                                                list_tmp_step_num.append(step_num_in_db)
                                                # print(template_step[zzi]['one_email'])
                                                # if len(template_step[zzi]['one_email']) != 0:
                                                for uugg in range(len(template_step[zzi]['one_email'])):
                                                    #     eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                # else:
                                                    eval_data_step[zzi]['step_detail'][uugg]['one_email'] = ""
                                                    # print(eval_data_step[zzi])
                                                list_eval.append(eval_data_step[zzi])
                                            string_json = (list_eval)
                            # print(string_json)
                            # return '' 
                            string_json_NoneEval = str(string_json)
                            document_details = str(get_Template['messageText'][0]['document_details_string'])
                            document_type = get_Template['messageText'][0]['document_details']['document_type']
                            # string_json = eval(get_Template['messageText'][0]['data_step'])
                            # string_json_NoneEval = str(get_Template['messageText'][0]['data_step'])
                            email_center = str(get_Template['messageText'][0]['email_center'])
                            step_Max = get_Template['messageText'][0]['step_Max']
                            result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                            string_json_NoneEval = str(result_SelectEmailMe['messageText'])                     
                            string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                            qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                            tmp_digit_sign = get_Template['messageText'][0]['digit_sign']
                            getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                            getEmail_list = []
                            if getEmail['result'] == 'OK':
                                for o in range(len(getEmail['messageText'])):
                                    if 'email_result' in getEmail['messageText'][o]:
                                        for i in getEmail['messageText'][o]['email_result']:
                                            getStepNumber = getEmail['messageText'][o]['step_num']
                                            getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                            sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                            res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                            
                            if res_insert_pdf['result'] == 'OK':
                                getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                                if getTracking['result'] == 'OK':                                    
                                    ts = int(time.time())
                                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                    result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    if result_insert['result'] == 'OK':                                        
                                        sidCode = getTracking['step_data_sid']
                                        typeFile = str(fileName).split('.')[-1]
                                        FileId = res_insert_pdf['messageText']
                                        trackingId = getTracking['messageText']
                                        result_DocumentID = document_().genarate_document_ID(document_type)
                                        # options_page_string = {'subject_text': '<ไม่มีหัวเรื่อง>', 'body_text': fileName}
                                        getDocument = insert().insert_document_new_v(sidCode,typeFile,FileId,document_details,document_type,'M',digit_sign=tmp_digit_sign,attempted_name=Folder_Attachment_Name,documentID=result_DocumentID['messageText']['documentID'],options_page=options_page_string)
                                        if getDocument['result'] == 'OK':
                                            document_Id = getDocument['document_Id']
                                            ts = int(time.time())
                                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                            getSender = insert().insert_paper_sender_v2(username,st,'ACTIVE',sender_name,oneEmail,'owner',FileId,fileName,trackingId,sidCode,template_code,document_Id,'',email_center)
                                            if getSender['result'] == 'OK':
                                                arr_result = []
                                                getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                                chatstatus_forservice(string_json)
                                                
                                                if getSign['result'] == 'OK':
                                                    print(getEmail_list)
                                                    for i in getEmail_list:
                                                        emailUser = i['email']
                                                        getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                                        
                                                        if getUrl_Sign['result'] == 'OK':
                                                            arr_result.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num'],
                                                                'sendChat': i['status_chat'],
                                                                'property' : i['property']
                                                            })
                                                            arr_result_Email.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num']                                                                
                                                            })
                                                    chatRequestData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result
                                                    }
                                                    MailData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result_Email
                                                    }
                                                    data_tosender = chatRequestData['data']                                  
                                                    for n in range(len(data_tosender)):
                                                        status_sendChat.append(data_tosender[n]['sendChat'])
                                                        print(data_tosender[n])
                                                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                                                            res_search_frd = search_frd(data_tosender[n]['email'],token_header)
                                                            
                                                            if 'status' in res_search_frd:
                                                                if res_search_frd['status'] == 'success':
                                                                    oneId = res_search_frd['friend']['one_id']
                                                                    userid_info = res_search_frd['friend']['user_id']
                                                                    resultURLIMAGE = createImage_formPDF(sidCode)
                                                                    result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                    print(result_pathUrl)
                                                                    resouce_result = select().select_forChat_v1(sidCode)
                                                                    userIdOne = res_search_frd['friend']['user_id']
                                                                    if resouce_result['result'] == 'OK':                
                                                                        res_send = send_url_tochat_new_v3(data_tosender[n]['property'],userid_info,data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl,token_header)
                                                                        print(res_send)
                                                                        if 'status' in res_send:
                                                                            if res_send['status'] == 'success':
                                                                                
                                                                                id_one_chat_to_msg = res_send['message']['id']
                                                                                update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                resultgetProject = sendtask_getProject_tochat_v1(oneId,token_header)
                                                                                print(resultgetProject)
                                                                                
                                                                                if resultgetProject['result'] == 'OK':
                                                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                    priority_ = '1'
                                                                                    titleAndDetails = resouce_result['messageText']
                                                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                        if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                    resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId,token_header)
                                                                                    # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                    if resultSend_CreateTask['result'] == 'OK':
                                                                                        if 'status' in resultSend_CreateTask['messageText']:
                                                                                            if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                        else:
                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                    else:
                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                else:
                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                else:
                                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            elif 'result' in res_search_frd:
                                                                if res_search_frd['result'] == 'ER':                            
                                                                    arrEmail = []
                                                                    arrEmail.append(data_tosender[n]['email'])
                                                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                                                    if 'status' in resultAddfrd:
                                                                        if resultAddfrd['status'] == 'success':
                                                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                                                resultURLIMAGE = createImage_formPDF(sidCode)
                                                                                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                                print(result_pathUrl)
                                                                                resouce_result = select().select_forChat_v1(sidCode)
                                                                                if resouce_result['result'] == 'OK':                
                                                                                    res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl,token_header)
                                                                                    print(res_send)
                                                                                    if 'status' in res_send:
                                                                                        if res_send['status'] == 'success':
                                                                                            id_one_chat_to_msg = res_send['message']['id']
                                                                                            update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                            resultgetProject = sendtask_getProject_tochat_v1(oneId,token_header)
                                                                                            if resultgetProject['result'] == 'OK':
                                                                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                                priority_ = '1'
                                                                                                titleAndDetails = resouce_result['messageText']
                                                                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                                resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId,token_header)
                                                                                                # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                                if resultSend_CreateTask['result'] == 'OK':
                                                                                                    if 'status' in resultSend_CreateTask['messageText']:
                                                                                                        if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                            list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                        else:
                                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                    else:
                                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                else:
                                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                                        else:
                                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                                    else:
                                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                    else:
                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            else:
                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                        else:
                                                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    print(list_emailChat_log)
                                                    if True in status_sendChat:
                                                        result_logChat = selection_email_insert(list_emailChat_log,id_one_chat_to_msg)
                                                        if result_logChat['result'] == 'OK':
                                                            insert().insert_transactionTask(list_taskChat_log)
                                                            data_Mail = MailData['data']
                                                            for i in range(len(data_Mail)):
                                                                if data_Mail[i]['step_num'] == "1":
                                                                    result_Email = mail().check_EmailProfile(data_Mail[i]['email'])
                                                                    if result_Email['result'] == 'OK':
                                                                        data_Mail[i]['emailUser'] = result_Email['messageText']['emailUser']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                    else:
                                                                        data_Mail[i]['emailUser'] = data_Mail[i]['email']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                        # print(result_mailStatus, ' result_mailStatus')
                                                                    if result_mailStatus['result'] == 'OK':
                                                                        result_list.append({'result':'OK','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':None})
                                                                    else:
                                                                        result_list.append({'result':'ER','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':result_mailStatus['messageText']})
                                                                else:
                                                                    result_list.append({'result':'NO','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign']})
                                                            # print(result_list , ' result_list')
                                                            result_insertMail = mail().insert_logEmail(result_list)
                                                            sid_code = getTracking['step_data_sid']
                                                            sid_code_sha512 = hashlib.sha512(str(sid_code).encode('utf-8')).hexdigest()
                                                            if result_insertMail['result'] == 'OK':
                                                                return jsonify({'result':'OK','messageText':{'result_mail_service':result_list,'result_chat_service':list_emailChat_log,'id_transaction_paperless':sid_code_sha512,'url_tracking':'https://paperless.one.th/tracking?id=' + trackingId,'tracking_id':trackingId,'attemp_status':tmp_attemp_status},'status_Code':200}),200
                                                            else:
                                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insertMail['messageText']})
                                                        else:
                                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                                                    else:                                                        
                                                        sid_code = getTracking['step_data_sid']
                                                        sid_code_sha512 = hashlib.sha512(str(sid_code).encode('utf-8')).hexdigest()                                                      
                                                        result_logChat = selection_email_insert(list_emailChat_log,None)
                                                        return jsonify({'result':'OK','messageText':{'msg':'Not Found Send To OneChat!','id_transaction_paperless':sid_code_sha512,'url_tracking':'https://paperless.one.th/tracking?id=' + trackingId,'tracking_id':trackingId,'attemp_status':tmp_attemp_status},'status_Code':200,'messageER':None})
                                            else:
                                                delete().delete_all_table_for_service(sidCode)  
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'upload file fail'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                        else:        
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template not found in taxId'}),200
                            return ''
                    else:
                        get_Template = select().select_get_string_templateAndusername(str(username).replace(' ',''),str(template_code).replace(' ',''))
                        # print(get_Template)
                        # return ''
                        if get_Template['result'] == 'OK':
                            for zzi in range(len(template_step)):
                                one_email_info = template_step[zzi]['one_email']
                                # print(one_email_info)
                                # return ''
                                if len(one_email_info) != 0:
                                    for uzi in range(len(one_email_info)):
                                        if str(one_email_info[uzi]).replace(' ','') == '':
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found :email in list'}),200
                                        else:
                                            emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", str(one_email_info[uzi]).replace(' ',''))
                                            if emails is None:
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'email in list error'}),200
                                            else:
                                                pass
                                        
                                        eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                        
                                        if 'step_num' in eval_data_step:
                                            # print((eval_data_step))
                                            step_num_in_db = eval_data_step['step_num']
                                            if template_step[zzi]['step_num'] == step_num_in_db:
                                                for uugg in range(len(template_step[zzi]['one_email'])):
                                                    eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                    list_eval.append(eval_data_step)
                                            eval_data_step = (eval_data_step)
                                            string_json = eval_data_step
                                        
                                        else:
                                            # # print(eval_data_step)
                                            # print(template_step[zzi]['one_email'])
                                            step_num_in_db = eval_data_step[zzi]['step_num']
                                            if template_step[zzi]['step_num'] == step_num_in_db:
                                                if step_num_in_db not in list_tmp_step_num:
                                                    list_tmp_step_num.append(step_num_in_db)
                                                    # print(template_step[zzi]['one_email'])
                                                    if len(template_step[zzi]['one_email']) != 0:
                                                        for uugg in range(len(template_step[zzi]['one_email'])):
                                                            eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                    else:
                                                        eval_data_step[zzi]['step_detail'][uugg]['one_email'] = ""
                                                        # print(eval_data_step[zzi])
                                                    list_eval.append(eval_data_step[zzi])
                                            string_json = (list_eval)
                                else:
                                    # if str(one_email_info).replace(' ','') == '':
                                    #     return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found :email in list'}),200
                                    # else:
                                    #     emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", str(one_email_info).replace(' ',''))
                                    #     if emails is None:
                                    #         return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'email in list error'}),200
                                    #     else:
                                    #         pass
                                    
                                    eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                    
                                    if 'step_num' in eval_data_step:
                                        # print((eval_data_step))
                                        step_num_in_db = eval_data_step['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                list_eval.append(eval_data_step)
                                        eval_data_step = (eval_data_step)
                                        string_json = eval_data_step
                                    
                                    else:
                                        # # print(eval_data_step)
                                        # print(template_step[zzi]['one_email'])
                                        step_num_in_db = eval_data_step[zzi]['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            if step_num_in_db not in list_tmp_step_num:
                                                list_tmp_step_num.append(step_num_in_db)
                                                # print(template_step[zzi]['one_email'])
                                                # if len(template_step[zzi]['one_email']) != 0:
                                                for uugg in range(len(template_step[zzi]['one_email'])):
                                                    #     eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                # else:
                                                    eval_data_step[zzi]['step_detail'][uugg]['one_email'] = ""
                                                    # print(eval_data_step[zzi])
                                                list_eval.append(eval_data_step[zzi])
                                            string_json = (list_eval)
                            # print(string_json)
                            # return '' 
                            string_json_NoneEval = str(string_json)
                            document_details = str(get_Template['messageText'][0]['document_details_string'])
                            document_type = get_Template['messageText'][0]['document_details']['document_type']
                            # string_json = eval(get_Template['messageText'][0]['data_step'])
                            # string_json_NoneEval = str(get_Template['messageText'][0]['data_step'])
                            email_center = str(get_Template['messageText'][0]['email_center'])
                            step_Max = get_Template['messageText'][0]['step_Max']                            
                            tmp_digit_sign = get_Template['messageText'][0]['digit_sign']
                            result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                            print(result_SelectEmailMe)
                            string_json_NoneEval = str(result_SelectEmailMe['messageText'])                            
                            string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                            qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                            getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                            getEmail_list = []
                            if getEmail['result'] == 'OK':
                                for o in range(len(getEmail['messageText'])):
                                    if 'email_result' in getEmail['messageText'][o]:
                                        for i in getEmail['messageText'][o]['email_result']:
                                            getStepNumber = getEmail['messageText'][o]['step_num']
                                            getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                            # print(getEmail_list,'getEmail_list')
                            sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                            res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                            if res_insert_pdf['result'] == 'OK':
                                getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                                if getTracking['result'] == 'OK':
                                    ts = int(time.time())
                                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                    # print(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    if result_insert['result'] == 'OK':                                        
                                        sidCode = getTracking['step_data_sid']
                                        typeFile = str(fileName).split('.')[-1]
                                        FileId = res_insert_pdf['messageText']
                                        trackingId = getTracking['messageText']
                                        result_DocumentID = document_().genarate_document_ID(document_type)
                                        # print(result_DocumentID, ' result_DocumentID')
                                        # options_page_string = {'subject_text': '<ไม่มีหัวเรื่อง>', 'body_text': fileName}
                                        getDocument = insert().insert_document_new_v(sidCode,typeFile,FileId,document_details,document_type,'M',digit_sign=tmp_digit_sign,attempted_name=Folder_Attachment_Name,documentID=result_DocumentID['messageText']['documentID'],options_page=options_page_string)
                                        if getDocument['result'] == 'OK':
                                            document_Id = getDocument['document_Id']
                                            ts = int(time.time())
                                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                            
                                            getSender = insert().insert_paper_sender_v2(username,st,'ACTIVE',sender_name,oneEmail,'owner',FileId,fileName,trackingId,sidCode,template_code,document_Id,'',email_center)
                                            # print(getSender,'getSender')
                                            if getSender['result'] == 'OK':
                                                arr_result = []
                                                getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                                # return ''
                                                chatstatus_forservice(string_json)
                                                if getSign['result'] == 'OK':
                                                    for i in getEmail_list:
                                                        emailUser = i['email']
                                                        getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                                        if getUrl_Sign['result'] == 'OK':
                                                            arr_result.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num'],
                                                                'sendChat': i['status_chat'],
                                                                'property' : i['property']
                                                            })
                                                            print(arr_result)
                                                            arr_result_Email.append({
                                                                'email':emailUser,
                                                                'url_sign':getUrl_Sign['messageText'],
                                                                'tracking':trackingId,
                                                                'name_file':fileName,
                                                                'message':'',
                                                                'step_num': i['step_num']                                                                
                                                            })
                                                    chatRequestData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result
                                                    }
                                                    MailData = {
                                                        "sid": sidCode,
                                                        "tracking" : trackingId,
                                                        "name_file" : fileName,
                                                        "data": arr_result_Email
                                                    }
                                                    data_tosender = chatRequestData['data']                                  
                                                    for n in range(len(data_tosender)):
                                                        status_sendChat.append(data_tosender[n]['sendChat'])
                                                        
                                                        if data_tosender[n]['step_num'] == '1' and data_tosender[n]['sendChat'] == True:
                                                            res_search_frd = search_frd(data_tosender[n]['email'],token_header)
                                                            oneId = res_search_frd['friend']['one_id']
                                                            if 'status' in res_search_frd:
                                                                if res_search_frd['status'] == 'success':
                                                                    resultURLIMAGE = createImage_formPDF(sidCode)
                                                                    result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                    print(result_pathUrl)
                                                                    resouce_result = select().select_forChat_v1(sidCode)
                                                                    userIdOne = res_search_frd['friend']['user_id']
                                                                    if resouce_result['result'] == 'OK':                
                                                                        res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl,token_header)
                                                                        if 'status' in res_send:
                                                                            if res_send['status'] == 'success':
                                                                                id_one_chat_to_msg = res_send['message']['id']
                                                                                update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                resultgetProject = sendtask_getProject_tochat_v1(oneId,token_header)
                                                                                print(resultgetProject)
                                                                                
                                                                                if resultgetProject['result'] == 'OK':
                                                                                    projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                    priority_ = '1'
                                                                                    titleAndDetails = resouce_result['messageText']
                                                                                    for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                        if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                            state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                    resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId,token_header)
                                                                                    # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                    if resultSend_CreateTask['result'] == 'OK':
                                                                                        if 'status' in resultSend_CreateTask['messageText']:
                                                                                            if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                        else:
                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                    else:
                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                else:
                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                else:
                                                                    list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            elif 'result' in res_search_frd:
                                                                if res_search_frd['result'] == 'ER':                            
                                                                    arrEmail = []
                                                                    arrEmail.append(data_tosender[n]['email'])
                                                                    resultAddfrd = addbot_tofrdAUto(arrEmail)
                                                                    if 'status' in resultAddfrd:
                                                                        if resultAddfrd['status'] == 'success':
                                                                            if resultAddfrd['list_friend'][0]['status'] == 'success':
                                                                                resultURLIMAGE = createImage_formPDF(sidCode)
                                                                                result_pathUrl = myUrl_domain + 'public/viewimage/' + resultURLIMAGE
                                                                                print(result_pathUrl)
                                                                                resouce_result = select().select_forChat_v1(sidCode)
                                                                                if resouce_result['result'] == 'OK':                
                                                                                    res_send = send_url_tochat_new_v2(data_tosender[n]['property'],res_search_frd['friend']['user_id'],data_tosender[n]['name_file'],data_tosender[n]['tracking'],data_tosender[n]['url_sign'],sidCode,resouce_result['messageText'],result_pathUrl)
                                                                                    if 'status' in res_send:
                                                                                        if res_send['status'] == 'success':
                                                                                            id_one_chat_to_msg = res_send['message']['id']
                                                                                            update().update_StatusOneChat(sidCode,data_tosender[n]['email'])
                                                                                            resultgetProject = sendtask_getProject_tochat_v1(oneId,token_header)
                                                                                            if resultgetProject['result'] == 'OK':
                                                                                                projectid_ = resultgetProject['messageText']['data'][0]['project_id']
                                                                                                priority_ = '1'
                                                                                                titleAndDetails = resouce_result['messageText']
                                                                                                for y in range(len(resultgetProject['messageText']['data'][0]['state'])):
                                                                                                    if resultgetProject['messageText']['data'][0]['state'][y]['name'] == 'doing':
                                                                                                        state_id_ =  resultgetProject['messageText']['data'][0]['state'][y]['state_id']
                                                                                                resultSend_CreateTask = sendtask_creattask_tochat_v1(projectid_,priority_,titleAndDetails,state_id_,str(data_tosender[n]['property']).lower(),sidCode,oneId,token_header)
                                                                                                # print(resultSend_CreateTask , 'resultSend_CreateTask')
                                                                                                if resultSend_CreateTask['result'] == 'OK':
                                                                                                    if 'status' in resultSend_CreateTask['messageText']:
                                                                                                        if resultSend_CreateTask['messageText']['status'] =='success':
                                                                                                            list_taskChat_log.append({'result':'OK','sidCode':sidCode,'messageText':{'create_task':resultSend_CreateTask['messageText'],'get_project':resultgetProject['messageText']},'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                        else:
                                                                                                            list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                    else:
                                                                                                        list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                                else:
                                                                                                    list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            else:
                                                                                                list_taskChat_log.append({'result':'ER','sidCode':sidCode,'messageText':None,'sendChat': data_tosender[n]['sendChat'],'step_num':data_tosender[n]['step_num'],'email':data_tosender[n]['email']})
                                                                                            list_emailChat_log.append({'result':'OK','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                                        else:
                                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                                    else:
                                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                            else:
                                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                                        else:
                                                                            list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                                    else:
                                                                        list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']}) 
                                                            else:
                                                                list_emailChat_log.append({'result':'ER','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                        else:
                                                            list_emailChat_log.append({'result':'NO','email':data_tosender[n]['email'],'sid':sidCode,'step_num':data_tosender[n]['step_num'],'sendChat':data_tosender[n]['sendChat'],'urlSign':data_tosender[n]['url_sign'],'property':data_tosender[n]['property']})
                                                    if True in status_sendChat:
                                                        result_logChat = selection_email_insert(list_emailChat_log,id_one_chat_to_msg)
                                                        if result_logChat['result'] == 'OK':
                                                            insert().insert_transactionTask(list_taskChat_log)
                                                            data_Mail = MailData['data']
                                                            for i in range(len(data_Mail)):
                                                                if data_Mail[i]['step_num'] == "1":
                                                                    result_Email = mail().check_EmailProfile(data_Mail[i]['email'])
                                                                    if result_Email['result'] == 'OK':
                                                                        data_Mail[i]['emailUser'] = result_Email['messageText']['emailUser']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                    else:
                                                                        data_Mail[i]['emailUser'] = data_Mail[i]['email']
                                                                        result_mailStatus = mail().send_email(data_Mail[i],sidCode)
                                                                        # print(result_mailStatus, ' result_mailStatus')
                                                                    if result_mailStatus['result'] == 'OK':
                                                                        result_list.append({'result':'OK','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':None})
                                                                    else:
                                                                        result_list.append({'result':'ER','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign'],'messageER':result_mailStatus['messageText']})
                                                                else:
                                                                    result_list.append({'result':'NO','email':data_Mail[i]['email'],'sid':sidCode,'step_num':data_Mail[i]['step_num'],'urlSign':data_Mail[i]['url_sign']})
                                                            # print(result_list , ' result_list')
                                                            result_insertMail = mail().insert_logEmail(result_list)
                                                            sid_code = getTracking['step_data_sid']
                                                            sid_code_sha512 = hashlib.sha512(str(sid_code).encode('utf-8')).hexdigest()
                                                            if result_insertMail['result'] == 'OK':
                                                                return jsonify({'result':'OK','messageText':{'result_mail_service':result_list,'result_chat_service':list_emailChat_log,'id_transaction_paperless':sid_code_sha512,'url_tracking':'https://paperless.one.th/tracking?id=' + trackingId,'tracking_id':trackingId,'attemp_status':tmp_attemp_status},'status_Code':200}),200
                                                            else:
                                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insertMail['messageText']})
                                                        else:
                                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_logChat['messageText']})
                                                    else:  
                                                        sid_code = getTracking['step_data_sid']
                                                        sid_code_sha512 = hashlib.sha512(str(sid_code).encode('utf-8')).hexdigest()                                                      
                                                        result_logChat = selection_email_insert(list_emailChat_log,id_one_chat_to_msg)
                                                        return jsonify({'result':'OK','messageText':{'msg':'Not Found Send To OneChat!','id_transaction_paperless':sid_code_sha512,'url_tracking':'https://paperless.one.th/tracking?id=' + trackingId,'tracking_id':trackingId,'attemp_status':tmp_attemp_status},'status_Code':200,'messageER':None})
                                            else:
                                                delete().delete_all_table_for_service(sidCode)   
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'upload file fail'}),200
                                    else:
                                        
                                        return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                        else:        
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template or document type not found'}),200
                            return jsonify(get_Template)
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'cant get username and email'}),401
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','messageText':str(ex),'status_Code':200}),200

@status_methods.route('/public/v1/upload_ppl_service',methods=['POST'])
def public_upload_ppl_service():    
    try:
        token_header = request.headers['Authorization']
        token_header = str(token_header).split(' ')[1]
    except Exception as ex:
        return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'unauthorized'}),401
    url = one_url + "/api/account_and_biz_detail"
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer"+" "+token_header
    }
    try:
        response = requests.get(url, headers=headers, verify=False,timeout=10)
        response = response.json()
        # print(response)
        # return ''
    except requests.Timeout as ex:
        abort(401)
    except requests.HTTPError as ex:
        abort(401)
    except requests.ConnectionError as ex:
        abort(401)
    except requests.RequestException as ex:
        abort(401)
    except Exception as ex:
        abort(401)
    if 'result' in response:
        if response['result'] == 'Fail':
            abort(401)
    dep_id_list = []
    tmp_role_id_list = []
    dept_name_list = []
    position_list = []
    list_role_level = []
    low_role_id = []
    low_role_name = []
    dep_data = None       
    biz_info = []
    tmpdept_id = []
    tmpdept_name_list = []
    tmpposition_list = []
    tmpuser_id = response['id']
    thai_email = response['thai_email']
    username = response['username']
    sender_name = response['first_name_th'] + ' ' + response['last_name_th']
    # print(result_GetMydetp)
    if 'biz_detail' in response:
        getbiz = response['biz_detail']
        for i in range(len(getbiz)):
            data_get_my_dep = {
                "tax_id":getbiz[i]['getbiz'][0]['id_card_num']
            } 
            text_one_access = "Bearer" + " " + token_header
            result_GetMydetp = callAuth_post_v2(one_url+'/api/get_my_department_role',data_get_my_dep,text_one_access)
            if result_GetMydetp['result'] == 'OK':
                res_json = result_GetMydetp['messageText'].json()
                if res_json['data'] != None:
                    data_res = res_json['data']                                            
                    if data_res != '':
                        for y in range(len(data_res)):
                            dep_id = (data_res[y]['dept_id'])
                            tmp_role_id = (data_res[y]['role_id'])
                            tmp_role_detail = data_res[y]['role'][0]
                            tmp_role_level = tmp_role_detail['role_level']
                            tmp_role_name = tmp_role_detail['role_name']
                            if dep_id != '' and dep_id != None:
                                dep_id_list.append(dep_id)
                                dep_data = data_res[y]['department']
                                for iy in range(len(dep_data)):
                                    dept_name_list.append(dep_data[iy]['dept_name'])
                                    try:
                                        position_list.append(dep_data[iy]['dept_position'])
                                    except Exception as e:
                                        position_list.append('')
                            if tmp_role_id != '' and tmp_role_id != None:
                                tmp_role_id_list.append(tmp_role_id)
                                low_role_id.append(tmp_role_level)
                                low_role_name.append(tmp_role_name)
            if len(dep_id_list) != 0:
                tmpdept_id = dep_id_list[0]
            if len(dept_name_list) != 0:
                tmpdept_name_list = dept_name_list[0]
            if len(position_list) != 0:
                tmpposition_list = position_list[0]
            jsonData = {
                'id':getbiz[i]['getbiz'][0]['id'],
                'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                'role_level':getbiz[i]['getrole'][0]['role_level'],
                'role_name':getbiz[i]['getrole'][0]['role_name'],
                'dept_id':tmpdept_id,
                'dept_name':tmpdept_name_list,
                'dept_position':tmpposition_list,
            }
            biz_info.append(jsonData)
    profile_func_v1(tmpuser_id,username,thai_email,token_header)
    result_arraylist = []
    result_detail_service = {}
    dataJson = request.json
    result_CheckTaxId = []
    biz_json = ''
    chatData = []
    list_emailChat_log = []
    chatRequestData = {}
    status_sendChat = []
    result_list = []
    arr_result_Email = []
    list_taskChat_log = []
    MailData = {}
    id_one_chat_to_msg = None
    # try:
    if 'File_PDF' in dataJson and 'username' in dataJson and 'templateDetails'in dataJson and 'oneEmail' in dataJson and 'taxId' in dataJson\
    and 'DocumentType' in dataJson and 'Folder_Attachment_Name' in dataJson and 'subject_text' in dataJson and 'body_text' in dataJson and 'data_document' in dataJson and len(dataJson) == 10:
        if username == dataJson['username'] and thai_email == dataJson['oneEmail']:
            input_file      = dataJson['File_PDF']
            username        = dataJson['username']
            oneEmail        = dataJson['oneEmail']
            template_detils = dataJson['templateDetails']
            data_document = dataJson['data_document']
            options_page_string = {
                'subject_text': dataJson['subject_text'], 
                'body_text': dataJson['body_text']
            }
            try:
                null = None
                template_detils_eval = eval(template_detils)
                template_code = template_detils_eval['Template_Code']
                template_step = template_detils_eval['Template_step']
            except Exception as e:
                return jsonify({'status':'fail','message':'template details error','code':200,'data':[]}),200
            tax_Id          = dataJson['taxId']  
            Document_type   = dataJson['DocumentType']
            Folder_Attachment_Name   = dataJson['Folder_Attachment_Name']
            if str(Folder_Attachment_Name).replace(' ','') != '':
                tmp_attemp_status = True
            else:
                tmp_attemp_status = False
                Folder_Attachment_Name = None
            fileName        = 'e-form_' + str(datetime.datetime.now()).split('.')[0].split(' ')[0] + 'T' +str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[0] + '-' + str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[1] + '-'+str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[2]
            fileName        = str(fileName).replace(' ','') + ".pdf"
            base64_filedata = input_file
            # return ''
            if str(tax_Id).replace(' ','') is not '':
                if len(biz_info) != 0:
                    for i in range(len(biz_info)):
                        if tax_Id == biz_info[i]['id_card_num']:
                            result_CheckTaxId.append('Y')
                            biz_json = biz_info[i]
                    if 'Y' in result_CheckTaxId:
                        pass
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'taxId not found'}),200
            else:
                biz_json = None
            tax_Id = str(tax_Id).replace(' ','')
            list_eval = []
            list_tmp_step_num = []
            if tax_Id != '':
                get_Template = select().select_get_string_templateAndusername_tax_new(str(template_code).replace(' ',''),str(tax_Id).replace(' ',''))
                if get_Template['result'] == 'OK':
                    for zzi in range(len(template_step)):
                        one_email_info = template_step[zzi]['one_email']
                        # print(one_email_info)
                        # return ''
                        if len(one_email_info) != 0:
                            for uzi in range(len(one_email_info)):
                                eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                
                                if 'step_num' in eval_data_step:
                                    # print((eval_data_step))
                                    step_num_in_db = eval_data_step['step_num']
                                    if template_step[zzi]['step_num'] == step_num_in_db:
                                        for uugg in range(len(template_step[zzi]['one_email'])):
                                            eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                            list_eval.append(eval_data_step)
                                    eval_data_step = (eval_data_step)
                                    string_json = eval_data_step
                                
                                else:
                                    # # print(eval_data_step)
                                    # print(template_step[zzi]['one_email'])
                                    step_num_in_db = eval_data_step[zzi]['step_num']
                                    if template_step[zzi]['step_num'] == step_num_in_db:
                                        if step_num_in_db not in list_tmp_step_num:
                                            list_tmp_step_num.append(step_num_in_db)
                                            # print(template_step[zzi]['one_email'])
                                            if len(template_step[zzi]['one_email']) != 0:
                                                for uugg in range(len(template_step[zzi]['one_email'])):
                                                    eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                            else:
                                                eval_data_step[zzi]['step_detail'][uugg]['one_email'] = ""
                                                # print(eval_data_step[zzi])
                                            list_eval.append(eval_data_step[zzi])
                                    string_json = (list_eval)
                        else:
                            eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                            
                            if 'step_num' in eval_data_step:
                                # print((eval_data_step))
                                step_num_in_db = eval_data_step['step_num']
                                if template_step[zzi]['step_num'] == step_num_in_db:
                                    for uugg in range(len(template_step[zzi]['one_email'])):
                                        eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                        list_eval.append(eval_data_step)
                                eval_data_step = (eval_data_step)
                                string_json = eval_data_step
                            
                            else:
                                # # print(eval_data_step)
                                # print(template_step[zzi]['one_email'])
                                step_num_in_db = eval_data_step[zzi]['step_num']
                                if template_step[zzi]['step_num'] == step_num_in_db:
                                    if step_num_in_db not in list_tmp_step_num:
                                        list_tmp_step_num.append(step_num_in_db)
                                        # print(template_step[zzi]['one_email'])
                                        # if len(template_step[zzi]['one_email']) != 0:
                                        for uugg in range(len(template_step[zzi]['one_email'])):
                                            #     eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                        # else:
                                            eval_data_step[zzi]['step_detail'][uugg]['one_email'] = ""
                                            # print(eval_data_step[zzi])
                                        list_eval.append(eval_data_step[zzi])
                                    string_json = (list_eval)
                    # print(string_json)
                    # return '' 
                    string_json_NoneEval = str(string_json)
                    document_details = str(get_Template['messageText'][0]['document_details_string'])
                    document_type = get_Template['messageText'][0]['document_details']['document_type']
                    tmp_options_page = get_Template['messageText'][0]['options_page']
                    if tmp_options_page != None:
                        tmp_options_page = eval(tmp_options_page)
                    result_datadoc = data_doc(data_document)
                    result_documentType = select_1().select_document_type_forservice_v1(None,tax_Id,Document_type)
                    if result_documentType['result'] == 'OK' and result_datadoc['result'] == 'OK':
                        tmpmessage = result_documentType['messageText']
                        
                        for tzq in range(len(tmpmessage)):
                            if 'name_service' in tmpmessage[tzq]:
                                if tmpmessage[tzq]['name_service'] == 'GROUP':
                                    if 'other' in tmpmessage[tzq]:
                                        for xx in range(len(tmpmessage[tzq]['other'])):
                                            for uu in range(len(tmpmessage[tzq]['other'])):
                                                if 'properties' in tmpmessage[tzq]['other'][uu]:
                                                    for op in range(len(tmpmessage[tzq]['other'][uu]['properties'])):
                                                        if 'name' in tmpmessage[tzq]['other'][uu]['properties'][op]:
                                                            tmpnamekey = tmpmessage[tzq]['other'][uu]['properties'][op]['name']
                                                            if 'formdata_eform' in  result_datadoc['messageText']:
                                                                tmp_formdata_eform = result_datadoc['messageText']['eform_data']
                                                                if len(tmp_formdata_eform) != 0:
                                                                    for yy in range(len(tmp_formdata_eform)):
                                                                        tmpjson_key = tmp_formdata_eform[yy]['json_key']
                                                                        tmp_value = tmp_formdata_eform[yy]['value']
                                                                        if str(tmpjson_key).replace(' ','').lower() == str(tmpnamekey).replace(' ','').lower():
                                                                            tmpmessage[tzq]['other'][uu]['properties'][op]['value'] = tmp_value
                        options_page_string['service_properties'] = tmpmessage
                        if len(tmp_options_page) != 0:
                            tmp_options_page.update(options_page_string)
                        options_page_string = tmp_options_page
                        if len(options_page_string) == 0:
                            options_page_string = {
                                'subject_text': dataJson['subject_text'], 
                                'body_text': dataJson['body_text']
                            }
                    # return ''
                    #  = str(get_Template['messageText'][0]['email_center'])
                    email_center = str(get_Template['messageText'][0]['email_center'])
                    webhook = str(get_Template['messageText'][0]['webhook'])
                    step_Max = get_Template['messageText'][0]['step_Max']
                    result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                    string_json_NoneEval = str(result_SelectEmailMe['messageText'])                     
                    string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                    qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                    tmp_digit_sign = get_Template['messageText'][0]['digit_sign']
                    getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                    getEmail_list = []
                    if getEmail['result'] == 'OK':
                        for o in range(len(getEmail['messageText'])):
                            if 'email_result' in getEmail['messageText'][o]:
                                for i in getEmail['messageText'][o]['email_result']:
                                    getStepNumber = getEmail['messageText'][o]['step_num']
                                    getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                    sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                    res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                    
                    if res_insert_pdf['result'] == 'OK':
                        getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                        if getTracking['result'] == 'OK':                                    
                            ts = int(time.time())
                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                            result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                            
                            if result_insert['result'] == 'OK':                                        
                                sidCode = getTracking['step_data_sid']
                                typeFile = str(fileName).split('.')[-1]
                                FileId = res_insert_pdf['messageText']
                                trackingId = getTracking['messageText']
                                convert_pdf_image_v1(sidCode,str(base64_filedata))
                                result_DocumentID = document_().genarate_document_ID(document_type)
                                # options_page_string = {'subject_text': '<ไม่มีหัวเรื่อง>', 'body_text': fileName}
                                getDocument = insert().insert_document_new_v2(sidCode,typeFile,FileId,document_details,document_type,'M',digit_sign=tmp_digit_sign,attempted_name=Folder_Attachment_Name,documentID=result_DocumentID['messageText']['documentID'],options_page=options_page_string,data_document = data_document)
                                
                                if getDocument['result'] == 'OK':
                                    document_Id = getDocument['document_Id']
                                    ts = int(time.time())
                                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                    getSender = insert().insert_paper_sender_v2(username,st,'ACTIVE',sender_name,oneEmail,'owner',FileId,fileName,trackingId,sidCode,template_code,document_Id,webhook,email_center)
                                    # print(getSender)
                                    # return ''
                                    if getSender['result'] == 'OK':
                                        arr_result = []
                                        data_dict = {}
                                        data_list = []

                                        getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                        sid_code_sha512 = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
                                        chat_service = chat_for_service_v1(sidCode,'Bearer ' + token_header)
                                        # print ('list_eval: ',list_eval)
                                        for i in getEmail_list:
                                            emailUser = i['email']
                                            getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                            if getUrl_Sign['result'] == 'OK':
                                                data_list.append({
                                                    'email':emailUser,
                                                    'url_sign':getUrl_Sign['messageText'],
                                                    'tracking':trackingId,
                                                    'name_file':fileName,
                                                    'message':'',
                                                    'step_num': i['step_num']                                                                
                                                })

                                        type_service = 'first'
                                        send_mail = send_Mail_for_service_v1(type_service,sidCode,trackingId,str(fileName),data_list)
                                        print(chat_service)
                                        return jsonify({'result':'OK','messageText':{'id_transaction_paperless':sid_code_sha512,'url_tracking':paperless_tracking + trackingId,'tracking_id':trackingId,'attemp_status':tmp_attemp_status,'chat_service': chat_service[0]['messageText']['data']},'status_Code':200}),200

                                    else:
                                        delete().delete_all_table_for_service(sidCode)  
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'upload file fail'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':getDocument['messageText'],'status_Code':200}),200
                            else:
                                return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                        else:
                            return jsonify({'result':'ER','messageText':getTracking['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':res_insert_pdf['messageText'],'status_Code':200}),200
                else:        
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template not found in taxId'}),200
                    return ''
            else:
                get_Template = select().select_get_string_templateAndusername(str(username).replace(' ',''),str(template_code).replace(' ',''))
                # data_doc(data_document)
                # return ''
                if get_Template['result'] == 'OK':
                    for zzi in range(len(template_step)):
                        one_email_info = template_step[zzi]['one_email']
                        for uzi in range(len(one_email_info)):
                            if len(one_email_info) != 0:
                                for uzi in range(len(one_email_info)):
                                    if str(one_email_info[uzi]).replace(' ','') == '':
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found :email in list'}),200
                                    else:
                                        emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", str(one_email_info[uzi]).replace(' ',''))
                                        if emails is None:
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'email in list error'}),200
                                        else:
                                            pass
                                    
                                    eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                    
                                    if 'step_num' in eval_data_step:
                                        step_num_in_db = eval_data_step['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                list_eval.append(eval_data_step)
                                        eval_data_step = (eval_data_step)
                                        string_json = eval_data_step
                                    
                                    else:
                                        # # print(eval_data_step)
                                        # print(template_step[zzi]['one_email'])
                                        step_num_in_db = eval_data_step[zzi]['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            if step_num_in_db not in list_tmp_step_num:
                                                list_tmp_step_num.append(step_num_in_db)
                                                # print(template_step[zzi]['one_email'])
                                                if len(template_step[zzi]['one_email']) != 0:
                                                    for uugg in range(len(template_step[zzi]['one_email'])):
                                                        eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                else:
                                                    eval_data_step[zzi]['step_detail'][uugg]['one_email'] = ""
                                                    # print(eval_data_step[zzi])
                                                list_eval.append(eval_data_step[zzi])
                                        string_json = (list_eval)
                            else:
                                # if str(one_email_info).replace(' ','') == '':
                                #     return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found :email in list'}),200
                                # else:
                                #     emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", str(one_email_info).replace(' ',''))
                                #     if emails is None:
                                #         return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'email in list error'}),200
                                #     else:
                                #         pass
                                
                                eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                
                                if 'step_num' in eval_data_step:
                                    # print((eval_data_step))
                                    step_num_in_db = eval_data_step['step_num']
                                    if template_step[zzi]['step_num'] == step_num_in_db:
                                        for uugg in range(len(template_step[zzi]['one_email'])):
                                            eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                            list_eval.append(eval_data_step)
                                    eval_data_step = (eval_data_step)
                                    string_json = eval_data_step
                                
                                else:
                                    # # print(eval_data_step)
                                    # print(template_step[zzi]['one_email'])
                                    step_num_in_db = eval_data_step[zzi]['step_num']
                                    if template_step[zzi]['step_num'] == step_num_in_db:
                                        if step_num_in_db not in list_tmp_step_num:
                                            list_tmp_step_num.append(step_num_in_db)
                                            # print(template_step[zzi]['one_email'])
                                            # if len(template_step[zzi]['one_email']) != 0:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                #     eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                            # else:
                                                eval_data_step[zzi]['step_detail'][uugg]['one_email'] = ""
                                                # print(eval_data_step[zzi])
                                            list_eval.append(eval_data_step[zzi])
                                        string_json = (list_eval)
                    string_json_NoneEval = str(string_json)
                    document_details = str(get_Template['messageText'][0]['document_details_string'])
                    document_type = get_Template['messageText'][0]['document_details']['document_type']
                    tmp_options_page = get_Template['messageText'][0]['options_page']
                    if tmp_options_page != None:
                        tmp_options_page = eval(tmp_options_page)
                    result_datadoc = data_doc(data_document)
                    result_documentType = select_1().select_document_type_forservice_v1(None,tax_Id,Document_type)
                    if result_documentType['result'] == 'OK' and result_datadoc['result'] == 'OK':
                        tmpmessage = result_documentType['messageText']
                        for tzq in range(len(tmpmessage)):
                            if 'name_service' in tmpmessage[tzq]:
                                if tmpmessage[tzq]['name_service'] == 'GROUP':
                                    if 'other' in tmpmessage[tzq]:
                                        for xx in range(len(tmpmessage[tzq]['other'])):
                                            for uu in range(len(tmpmessage[tzq]['other'])):
                                                if 'properties' in tmpmessage[tzq]['other'][uu]:
                                                    for op in range(len(tmpmessage[tzq]['other'][uu]['properties'])):
                                                        if 'name' in tmpmessage[tzq]['other'][uu]['properties'][op]:
                                                            tmpnamekey = tmpmessage[tzq]['other'][uu]['properties'][op]['name']
                                                            if 'formdata_eform' in  result_datadoc['messageText']:
                                                                tmp_formdata_eform = result_datadoc['messageText']['eform_data']
                                                                if len(tmp_formdata_eform) != 0:
                                                                    for yy in range(len(tmp_formdata_eform)):
                                                                        tmpjson_key = tmp_formdata_eform[yy]['json_key']
                                                                        tmp_value = tmp_formdata_eform[yy]['value']
                                                                        if str(tmpjson_key).replace(' ','').lower() == str(tmpnamekey).replace(' ','').lower():
                                                                            tmpmessage[tzq]['other'][uu]['properties'][op]['value'] = tmp_value
                        options_page_string['service_properties'] = tmpmessage
                        if len(tmp_options_page) != 0:
                            tmp_options_page.update(options_page_string)
                        options_page_string = tmp_options_page
                        if len(options_page_string) == 0:
                            options_page_string = {
                                'subject_text': dataJson['subject_text'], 
                                'body_text': dataJson['body_text']
                            }
                    email_center = str(get_Template['messageText'][0]['email_center'])
                    webhook = str(get_Template['messageText'][0]['webhook'])
                    step_Max = get_Template['messageText'][0]['step_Max']                            
                    tmp_digit_sign = get_Template['messageText'][0]['digit_sign']
                    result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                    print(result_SelectEmailMe)
                    string_json_NoneEval = str(result_SelectEmailMe['messageText'])                            
                    string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                    qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                    getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                    getEmail_list = []
                    if getEmail['result'] == 'OK':
                        for o in range(len(getEmail['messageText'])):
                            if 'email_result' in getEmail['messageText'][o]:
                                for i in getEmail['messageText'][o]['email_result']:
                                    getStepNumber = getEmail['messageText'][o]['step_num']
                                    getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                    # print(getEmail_list,'getEmail_list')
                    sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                    res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                    if res_insert_pdf['result'] == 'OK':
                        getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                        if getTracking['result'] == 'OK':
                            ts = int(time.time())
                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                            # print(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                            result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                            if result_insert['result'] == 'OK':                                        
                                sidCode = getTracking['step_data_sid']
                                typeFile = str(fileName).split('.')[-1]
                                FileId = res_insert_pdf['messageText']
                                trackingId = getTracking['messageText']
                                convert_pdf_image_v1(sidCode,str(base64_filedata))
                                result_DocumentID = document_().genarate_document_ID(document_type)
                                # print(result_DocumentID, ' result_DocumentID')
                                # options_page_string = {'subject_text': '<ไม่มีหัวเรื่อง>', 'body_text': fileName}
                                getDocument = insert().insert_document_new_v2(sidCode,typeFile,FileId,document_details,document_type,'M',digit_sign=tmp_digit_sign,attempted_name=Folder_Attachment_Name,documentID=result_DocumentID['messageText']['documentID'],options_page=options_page_string)
                                if getDocument['result'] == 'OK':
                                    document_Id = getDocument['document_Id']
                                    ts = int(time.time())
                                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                    
                                    getSender = insert().insert_paper_sender_v2(username,st,'ACTIVE',sender_name,oneEmail,'owner',FileId,fileName,trackingId,sidCode,template_code,document_Id,webhook,email_center)
                                    # print(getSender,'getSender')
                                    if getSender['result'] == 'OK':
                                        arr_result = []
                                        data_list = []
                                        data_dict = {}
                                        
                                        getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                        sid_code_sha512 = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
                                        chat_service = chat_for_service_v1(sidCode,'Bearer ' + token_header)
                                        
                                        for i in getEmail_list:
                                            emailUser = i['email']
                                            getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                            if getUrl_Sign['result'] == 'OK':
                                                data_list.append({
                                                    'email':emailUser,
                                                    'url_sign':getUrl_Sign['messageText'],
                                                    'tracking':trackingId,
                                                    'name_file':fileName,
                                                    'message':'',
                                                    'step_num': i['step_num']                                                                
                                                })

                                        
                                        type_service = 'first'
                                        send_mail = send_Mail_for_service_v1(type_service,sidCode,trackingId,str(fileName),data_list)
                                        
                                        return jsonify({'result':'OK','messageText':{'id_transaction_paperless':sid_code_sha512,'url_tracking':paperless_tracking + trackingId,'tracking_id':trackingId,'attemp_status':tmp_attemp_status,'chat_service': chat_service[0]['messageText']['data']},'status_Code':200}),200

                                    else:
                                        delete().delete_all_table_for_service(sidCode)   
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'upload file fail'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':getDocument['messageText']}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insert['messageText']}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':getTracking['messageText']}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':res_insert_pdf['messageText']}),200
                else:        
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template or document type not found'}),200
                    return jsonify(get_Template)
        else:
            abort(401)
    else:
        abort(404)
    # except Exception as ex:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     print(exc_type, fname, exc_tb.tb_lineno)
    #     return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':str(ex)}),200

@status_methods.route('/api/v1/old_upload_ppl_service',methods=['POST'])
def upload_service_ppl_v1():    
    try:
        token_header = request.headers['Authorization']
        token_header = str(token_header).split(' ')[1]
    except Exception as ex:
        return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'unauthorized'}),401
    url = one_url + "/api/account_and_biz_detail"
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer"+" "+token_header
    }
    try:
        response = requests.get(url, headers=headers, verify=False,timeout=10)
        response = response.json()
        # print(response)
        # return ''
    except requests.Timeout as ex:
        abort(401)
    except requests.HTTPError as ex:
        abort(401)
    except requests.ConnectionError as ex:
        abort(401)
    except requests.RequestException as ex:
        abort(401)
    except Exception as ex:
        abort(401)
    if 'result' in response:
        if response['result'] == 'Fail':
            abort(401)
    try:   
        arrtax_id = []
        tmp_role_id_list = []
        list_role_level = []
        low_role_id = []
        low_role_name = []
        dep_data = None
        biz_info = []
        tmpuser_id = response['id']
        thai_email = response['thai_email']
        username = response['username']
        sender_name = str(response['first_name_th']) + ' ' + str(response['last_name_th'])
        if 'biz_detail' in response:
            getbiz = response['biz_detail']
            for i in range(len(getbiz)):
                if getbiz[i]['getbiz'][0]['id_card_num'] not in arrtax_id:
                    arrtax_id.append(getbiz[i]['getbiz'][0]['id_card_num'])
                    data_get_my_dep = {
                        "tax_id":getbiz[i]['getbiz'][0]['id_card_num']
                    } 
                    text_one_access = "Bearer" + " " + token_header
                    result_GetMydetp = callAuth_post_v2(one_url+'/api/get_my_department_role',data_get_my_dep,text_one_access)
                    if result_GetMydetp['result'] == 'OK':
                        res_json = result_GetMydetp['messageText'].json()
                        # print(res_json)
                        if res_json['data'] != None:
                            data_res = res_json['data']                                          
                            if data_res != '':
                                for y in range(len(data_res)):
                                    dep_id_list = []
                                    dept_name_list = []
                                    position_list = []
                                    tmpdept_id = []
                                    tmpdept_name_list = []
                                    tmpposition_list = []
                                    dep_id = (data_res[y]['dept_id'])
                                    tmp_role_id = (data_res[y]['role_id'])
                                    tmp_role_detail = data_res[y]['role'][0]
                                    tmp_role_level = tmp_role_detail['role_level']
                                    tmp_role_name = tmp_role_detail['role_name']
                                    if dep_id != '' and dep_id != None:
                                        dep_id_list.append(dep_id)
                                        dep_data = data_res[y]['department']
                                        for iy in range(len(dep_data)):
                                            dept_name_list.append(dep_data[iy]['dept_name'])
                                            try:
                                                position_list.append(dep_data[iy]['dept_position'])
                                            except Exception as e:
                                                position_list.append('')
                                    if tmp_role_id != '' and tmp_role_id != None:
                                        tmp_role_id_list.append(tmp_role_id)
                                        low_role_id.append(tmp_role_level)
                                        low_role_name.append(tmp_role_name)
                    if len(dep_id_list) != 0:
                        tmpdept_id = [dep_id_list[0]]
                    if len(dept_name_list) != 0:
                        tmpdept_name_list = [dept_name_list[0]]
                    if len(position_list) != 0:
                        tmpposition_list = [position_list[0]]
                    jsonData = {
                        'id':getbiz[i]['getbiz'][0]['id'],
                        'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                        'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                        'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                        'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                        'role_level':getbiz[i]['getrole'][0]['role_level'],
                        'role_name':getbiz[i]['getrole'][0]['role_name'],
                        'dept_id':tmpdept_id,
                        'dept_name':tmpdept_name_list,
                        'dept_position':tmpposition_list,
                    }
                    biz_info.append(jsonData)
        profile_func_v1(tmpuser_id,username,thai_email,token_header)
        result_arraylist = []
        result_detail_service = {}
        dataJson = request.json
        result_CheckTaxId = []
        biz_json = ''
        chatData = []
        list_emailChat_log = []
        chatRequestData = {}
        status_sendChat = []
        result_list = []
        arr_result_Email = []
        list_taskChat_log = []
        MailData = {}
        id_one_chat_to_msg = None
        if 'File_PDF' in dataJson and 'username' in dataJson and 'templateDetails'in dataJson and 'oneEmail' in dataJson and 'taxId' in dataJson\
        and 'DocumentType' in dataJson and 'Folder_Attachment_Name' in dataJson and 'subject_text' in dataJson and 'body_text' in dataJson and 'data_document' in dataJson:
            if username == dataJson['username'] and thai_email == dataJson['oneEmail']:
                tmpref_document = None
                fileName = None
                tmptype = "owner"
                if 'ref_document' in dataJson:
                    tmpref_document = str(dataJson['ref_document'])
                if 'filename' in dataJson:
                    fileName = str(dataJson['filename'])
                if 'type' in dataJson:
                    tmptype = dataJson['type']
                if 'tracking_id' in dataJson:
                    tmptracking = dataJson['tracking']
                input_file      = dataJson['File_PDF']
                username        = dataJson['username']
                oneEmail        = dataJson['oneEmail']
                template_detils = dataJson['templateDetails']
                data_document = dataJson['data_document']
                options_page_string = {
                    'subject_text': dataJson['subject_text'], 
                    'body_text': dataJson['body_text']
                }
                try:
                    null = None
                    template_detils_eval = eval(template_detils)
                    template_code = template_detils_eval['Template_Code']
                    template_step = template_detils_eval['Template_step']
                    # print(template_code)
                except Exception as e:
                    print(str(e))
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template details error'}),200
                # print(template_detils_eval)
                # template_code   = dataJson['templateDetails']
                tax_Id          = dataJson['taxId']  
                Document_type   = dataJson['DocumentType']
                Folder_Attachment_Name   = dataJson['Folder_Attachment_Name']
                if str(Folder_Attachment_Name).replace(' ','') != '':
                    tmp_attemp_status = True
                else:
                    tmp_attemp_status = False
                    Folder_Attachment_Name = None
                if fileName == None:
                    fileName        = 'e-form_' + str(datetime.datetime.now()).split('.')[0].split(' ')[0] + 'T' +str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[0] + '-' + str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[1] + '-'+str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[2]
                    fileName        = str(fileName).replace(' ','') + ".pdf"
                base64_filedata = input_file
                rdept = select_4().select_dept_document_type_v1(Document_type,tax_Id)
                datadeptName = None
                if rdept['result'] == 'OK':
                    if len(rdept['data']) != 0:
                        messagedata_rdept = rdept['data'][0]
                        if 'dept_name' in  eval(messagedata_rdept['biz_info']):
                            datadeptName = eval(messagedata_rdept['biz_info'])['dept_name']
                # return jsonify(datadeptName)
                if str(tax_Id).replace(' ','') is not '':
                    if len(biz_info) != 0:
                        for i in range(len(biz_info)):
                            if tax_Id == biz_info[i]['id_card_num']:
                                result_CheckTaxId.append('Y')
                                biz_json = biz_info[i]
                                if datadeptName != None:
                                    biz_json['dept_name'] = datadeptName
                        if 'Y' in result_CheckTaxId:
                            pass
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'tax_id not found'}),200
                else:
                    biz_json = None
                tax_Id = str(tax_Id).replace(' ','')
                list_eval = []
                list_tmp_step_num = []
                tmp_sign_page_options = 'OFF'
                if tax_Id != '':
                    get_Template = select().select_get_string_templateAndusername_tax_new(str(template_code).replace(' ',''),str(tax_Id).replace(' ',''))
                    if get_Template['result'] == 'OK':
                        for zzi in range(len(template_step)):
                            one_email_info = template_step[zzi]['one_email']
                            # print(one_email_info)
                            # return ''
                            if len(one_email_info) != 0:
                                for uzi in range(len(one_email_info)):
                                    eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                    if 'step_num' in eval_data_step:
                                        # print((eval_data_step))
                                        step_num_in_db = eval_data_step['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                list_eval.append(eval_data_step)
                                        eval_data_step = (eval_data_step)
                                        string_json = eval_data_step
                                    
                                    else:
                                        # # print(eval_data_step)
                                        # print(template_step[zzi]['one_email'])
                                        step_num_in_db = eval_data_step[zzi]['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            if step_num_in_db not in list_tmp_step_num:
                                                list_tmp_step_num.append(step_num_in_db)
                                                # print(template_step[zzi]['one_email'])
                                                if len(template_step[zzi]['one_email']) != 0:
                                                    for uugg in range(len(template_step[zzi]['one_email'])):
                                                        eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                else:
                                                    eval_data_step[zzi]['step_detail'][uugg]['one_email'] = ""
                                                    # print(eval_data_step[zzi])
                                                list_eval.append(eval_data_step[zzi])
                                        string_json = (list_eval)
                            else:
                                eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                
                                if 'step_num' in eval_data_step:
                                    step_num_in_db = eval_data_step['step_num']
                                    if template_step[zzi]['step_num'] == step_num_in_db:
                                        for uugg in range(len(template_step[zzi]['one_email'])):
                                            eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                            list_eval.append(eval_data_step)
                                    eval_data_step = (eval_data_step)
                                    string_json = eval_data_step
                                
                                else:
                                    # # print(eval_data_step)
                                    # print(template_step[zzi]['one_email'])
                                    step_num_in_db = eval_data_step[zzi]['step_num']
                                    if template_step[zzi]['step_num'] == step_num_in_db:
                                        if step_num_in_db not in list_tmp_step_num:
                                            list_tmp_step_num.append(step_num_in_db)
                                            # print(template_step[zzi]['one_email'])
                                            # if len(template_step[zzi]['one_email']) != 0:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                #     eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                            # else:
                                                eval_data_step[zzi]['step_detail'][uugg]['one_email'] = ""
                                                # print(eval_data_step[zzi])
                                            list_eval.append(eval_data_step[zzi])
                                        string_json = (list_eval)
                        # print(string_json)
                        # return '' 
                        string_json_NoneEval = str(string_json)
                        document_details = str(get_Template['messageText'][0]['document_details_string'])
                        document_type = get_Template['messageText'][0]['document_details']['document_type']
                        tmp_options_page = get_Template['messageText'][0]['options_page']
                        if tmp_options_page != None:
                            tmp_options_page = eval(tmp_options_page)
                        result_datadoc = data_doc(data_document)
                        result_documentType = select_1().select_document_type_forservice_v1(None,tax_Id,Document_type)
                        if result_documentType['result'] == 'OK' and result_datadoc['result'] == 'OK':
                            tmpmessage = result_documentType['messageText']
                            
                            for tzq in range(len(tmpmessage)):
                                if 'name_service' in tmpmessage[tzq]:
                                    if tmpmessage[tzq]['name_service'] == 'GROUP':
                                        if 'other' in tmpmessage[tzq]:
                                            for xx in range(len(tmpmessage[tzq]['other'])):
                                                for uu in range(len(tmpmessage[tzq]['other'])):
                                                    if 'properties' in tmpmessage[tzq]['other'][uu]:
                                                        for op in range(len(tmpmessage[tzq]['other'][uu]['properties'])):
                                                            if 'name' in tmpmessage[tzq]['other'][uu]['properties'][op]:
                                                                tmpnamekey = tmpmessage[tzq]['other'][uu]['properties'][op]['name']
                                                                if 'formdata_eform' in  result_datadoc['messageText']:
                                                                    tmp_formdata_eform = result_datadoc['messageText']['eform_data']
                                                                    if len(tmp_formdata_eform) != 0:
                                                                        for yy in range(len(tmp_formdata_eform)):
                                                                            tmpjson_key = tmp_formdata_eform[yy]['json_key']
                                                                            tmp_value = tmp_formdata_eform[yy]['value']
                                                                            if str(tmpjson_key).replace(' ','').lower() == str(tmpnamekey).replace(' ','').lower():
                                                                                tmpmessage[tzq]['other'][uu]['properties'][op]['value'] = tmp_value
                                    if tmpmessage[tzq]['name_service'] == 'GROUP2':
                                        if 'other' in tmpmessage[tzq]:
                                            for xx in range(len(tmpmessage[tzq]['other'])):
                                                for uu in range(len(tmpmessage[tzq]['other'])):
                                                    if 'properties' in tmpmessage[tzq]['other'][uu]:
                                                        for op in range(len(tmpmessage[tzq]['other'][uu]['properties'])):
                                                            if 'name' in tmpmessage[tzq]['other'][uu]['properties'][op]:
                                                                tmpnamekey = tmpmessage[tzq]['other'][uu]['properties'][op]['name']
                                                                if 'formdata_eform' in  result_datadoc['messageText']:
                                                                    tmp_formdata_eform = result_datadoc['messageText']['eform_data']
                                                                    if len(tmp_formdata_eform) != 0:
                                                                        for yy in range(len(tmp_formdata_eform)):
                                                                            tmpjson_key = tmp_formdata_eform[yy]['json_key']
                                                                            tmp_value = tmp_formdata_eform[yy]['value']
                                                                            if str(tmpjson_key).replace(' ','').lower() == str(tmpnamekey).replace(' ','').lower():
                                                                                tmpmessage[tzq]['other'][uu]['properties'][op]['value'] = tmp_value
                            options_page_string['service_properties'] = tmpmessage
                            if len(tmp_options_page) != 0:
                                tmp_options_page.update(options_page_string)
                            options_page_string = tmp_options_page
                            if len(options_page_string) == 0:
                                options_page_string = {
                                    'subject_text': dataJson['subject_text'], 
                                    'body_text': dataJson['body_text']
                                }
                        # return ''
                        #  = str(get_Template['messageText'][0]['email_center'])
                        email_center = str(get_Template['messageText'][0]['email_center'])
                        webhook = str(get_Template['messageText'][0]['webhook'])
                        step_Max = get_Template['messageText'][0]['step_Max']
                        result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                        string_json_NoneEval = str(result_SelectEmailMe['messageText'])                     
                        string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                        qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                        tmp_digit_sign = get_Template['messageText'][0]['digit_sign']
                        tmp_sign_page_options = get_Template['messageText'][0]['sign_page_options']
                        getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                        getEmail_list = []
                        if getEmail['result'] == 'OK':
                            for o in range(len(getEmail['messageText'])):
                                if 'email_result' in getEmail['messageText'][o]:
                                    for i in getEmail['messageText'][o]['email_result']:
                                        getStepNumber = getEmail['messageText'][o]['step_num']
                                        getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                        sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                        res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                        
                        if res_insert_pdf['result'] == 'OK':
                            getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                            if getTracking['result'] == 'OK':                                    
                                ts = int(time.time())
                                st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                
                                if result_insert['result'] == 'OK':                                        
                                    sidCode = getTracking['step_data_sid']
                                    typeFile = str(fileName).split('.')[-1]
                                    FileId = res_insert_pdf['messageText']
                                    trackingId = getTracking['messageText']
                                    print(sidCode)
                                    convert_pdf_image_v1(sidCode,str(base64_filedata))
                                    result_DocumentID = document_().genarate_document_ID(document_type)
                                    # options_page_string = {'subject_text': '<ไม่มีหัวเรื่อง>', 'body_text': fileName}
                                    getDocument = insert().insert_document_new_v2(sidCode,typeFile,FileId,document_details,document_type,'M',digit_sign=tmp_digit_sign,attempted_name=Folder_Attachment_Name,documentID=result_DocumentID['messageText']['documentID'],options_page=options_page_string,data_document = data_document,sign_page_options=tmp_sign_page_options)
                                    
                                    if getDocument['result'] == 'OK':
                                        document_Id = getDocument['document_Id']
                                        ts = int(time.time())
                                        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                        getSender = insert().insert_paper_sender_v2(username,st,'ACTIVE',sender_name,oneEmail,tmptype,FileId,fileName,trackingId,sidCode,template_code,document_Id,webhook,email_center,ref_document=tmpref_document)
                                        # print(getSender)
                                        # return ''
                                        if getSender['result'] == 'OK':
                                            arr_result = []
                                            data_dict = {}
                                            data_list = []

                                            getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                            sid_code_sha512 = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
                                            chat_service = chat_for_service_v1(sidCode,'Bearer ' + token_header)
                                            # print ('list_eval: ',list_eval)
                                            for i in getEmail_list:
                                                emailUser = i['email']
                                                getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                                if getUrl_Sign['result'] == 'OK':
                                                    data_list.append({
                                                        'email':emailUser,
                                                        'url_sign':getUrl_Sign['messageText'],
                                                        'tracking':trackingId,
                                                        'name_file':fileName,
                                                        'message':'',
                                                        'step_num': i['step_num']                                                                
                                                    })

                                            type_service = 'first'
                                            send_mail = send_Mail_for_service_v2(sidCode)
                                            # send_mail = send_Mail_for_service_v2(type_service,sidCode,trackingId,str(fileName),data_list)
                                            print(chat_service)
                                            executor.submit(call_webhookService,sidCode)
                                            return jsonify({'result':'OK','messageText':{'id_transaction_paperless':sid_code_sha512,'url_tracking':paperless_tracking + trackingId,'tracking_id':trackingId,'attemp_status':tmp_attemp_status,'chat_service': chat_service[0]['messageText']['data']},'status_Code':200}),200

                                        else:
                                            delete().delete_all_table_for_service(sidCode)  
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'upload file fail'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':getDocument['messageText'],'status_Code':200}),200
                                else:
                                    return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                            else:
                                return jsonify({'result':'ER','messageText':getTracking['messageText'],'status_Code':200}),200
                        else:
                            return jsonify({'result':'ER','messageText':res_insert_pdf['messageText'],'status_Code':200}),200
                    else:        
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template not found in taxId'}),200
                        return ''
                else:
                    get_Template = select().select_get_string_templateAndusername(str(username).replace(' ',''),str(template_code).replace(' ',''))
                    # data_doc(data_document)
                    # return ''
                    if get_Template['result'] == 'OK':
                        for zzi in range(len(template_step)):
                            one_email_info = template_step[zzi]['one_email']
                            for uzi in range(len(one_email_info)):
                                if len(one_email_info) != 0:
                                    for uzi in range(len(one_email_info)):
                                        if str(one_email_info[uzi]).replace(' ','') == '':
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found :email in list'}),200
                                        else:
                                            emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", str(one_email_info[uzi]).replace(' ',''))
                                            if emails is None:
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'email in list error'}),200
                                            else:
                                                pass
                                        
                                        eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                        
                                        if 'step_num' in eval_data_step:
                                            step_num_in_db = eval_data_step['step_num']
                                            if template_step[zzi]['step_num'] == step_num_in_db:
                                                for uugg in range(len(template_step[zzi]['one_email'])):
                                                    eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                    list_eval.append(eval_data_step)
                                            eval_data_step = (eval_data_step)
                                            string_json = eval_data_step
                                        
                                        else:
                                            # # print(eval_data_step)
                                            # print(template_step[zzi]['one_email'])
                                            step_num_in_db = eval_data_step[zzi]['step_num']
                                            if template_step[zzi]['step_num'] == step_num_in_db:
                                                if step_num_in_db not in list_tmp_step_num:
                                                    list_tmp_step_num.append(step_num_in_db)
                                                    # print(template_step[zzi]['one_email'])
                                                    if len(template_step[zzi]['one_email']) != 0:
                                                        for uugg in range(len(template_step[zzi]['one_email'])):
                                                            eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                    else:
                                                        eval_data_step[zzi]['step_detail'][uugg]['one_email'] = ""
                                                        # print(eval_data_step[zzi])
                                                    list_eval.append(eval_data_step[zzi])
                                            string_json = (list_eval)
                                else:
                                    # if str(one_email_info).replace(' ','') == '':
                                    #     return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found :email in list'}),200
                                    # else:
                                    #     emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", str(one_email_info).replace(' ',''))
                                    #     if emails is None:
                                    #         return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'email in list error'}),200
                                    #     else:
                                    #         pass
                                    
                                    eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                    
                                    if 'step_num' in eval_data_step:
                                        # print((eval_data_step))
                                        step_num_in_db = eval_data_step['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                list_eval.append(eval_data_step)
                                        eval_data_step = (eval_data_step)
                                        string_json = eval_data_step
                                    
                                    else:
                                        # # print(eval_data_step)
                                        # print(template_step[zzi]['one_email'])
                                        step_num_in_db = eval_data_step[zzi]['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            if step_num_in_db not in list_tmp_step_num:
                                                list_tmp_step_num.append(step_num_in_db)
                                                # print(template_step[zzi]['one_email'])
                                                # if len(template_step[zzi]['one_email']) != 0:
                                                for uugg in range(len(template_step[zzi]['one_email'])):
                                                    #     eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                # else:
                                                    eval_data_step[zzi]['step_detail'][uugg]['one_email'] = ""
                                                    # print(eval_data_step[zzi])
                                                list_eval.append(eval_data_step[zzi])
                                            string_json = (list_eval)
                        string_json_NoneEval = str(string_json)
                        document_details = str(get_Template['messageText'][0]['document_details_string'])
                        document_type = get_Template['messageText'][0]['document_details']['document_type']
                        tmp_options_page = get_Template['messageText'][0]['options_page']
                        if tmp_options_page != None:
                            tmp_options_page = eval(tmp_options_page)
                        result_datadoc = data_doc(data_document)
                        result_documentType = select_1().select_document_type_forservice_v1(None,tax_Id,Document_type)
                        if result_documentType['result'] == 'OK' and result_datadoc['result'] == 'OK':
                            tmpmessage = result_documentType['messageText']
                            for tzq in range(len(tmpmessage)):
                                if 'name_service' in tmpmessage[tzq]:
                                    if tmpmessage[tzq]['name_service'] == 'GROUP':
                                        if 'other' in tmpmessage[tzq]:
                                            for xx in range(len(tmpmessage[tzq]['other'])):
                                                for uu in range(len(tmpmessage[tzq]['other'])):
                                                    if 'properties' in tmpmessage[tzq]['other'][uu]:
                                                        for op in range(len(tmpmessage[tzq]['other'][uu]['properties'])):
                                                            if 'name' in tmpmessage[tzq]['other'][uu]['properties'][op]:
                                                                tmpnamekey = tmpmessage[tzq]['other'][uu]['properties'][op]['name']
                                                                if 'formdata_eform' in  result_datadoc['messageText']:
                                                                    tmp_formdata_eform = result_datadoc['messageText']['eform_data']
                                                                    if len(tmp_formdata_eform) != 0:
                                                                        for yy in range(len(tmp_formdata_eform)):
                                                                            tmpjson_key = tmp_formdata_eform[yy]['json_key']
                                                                            tmp_value = tmp_formdata_eform[yy]['value']
                                                                            if str(tmpjson_key).replace(' ','').lower() == str(tmpnamekey).replace(' ','').lower():
                                                                                tmpmessage[tzq]['other'][uu]['properties'][op]['value'] = tmp_value
                            options_page_string['service_properties'] = tmpmessage
                            if len(tmp_options_page) != 0:
                                tmp_options_page.update(options_page_string)
                            options_page_string = tmp_options_page
                            if len(options_page_string) == 0:
                                options_page_string = {
                                    'subject_text': dataJson['subject_text'], 
                                    'body_text': dataJson['body_text']
                                }
                        email_center = str(get_Template['messageText'][0]['email_center'])
                        webhook = str(get_Template['messageText'][0]['webhook'])
                        step_Max = get_Template['messageText'][0]['step_Max']                            
                        tmp_digit_sign = get_Template['messageText'][0]['digit_sign']
                        result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                        print(result_SelectEmailMe)
                        string_json_NoneEval = str(result_SelectEmailMe['messageText'])                            
                        string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                        qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                        tmp_sign_page_options = get_Template['messageText'][0]['sign_page_options']
                        getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                        getEmail_list = []
                        if getEmail['result'] == 'OK':
                            for o in range(len(getEmail['messageText'])):
                                if 'email_result' in getEmail['messageText'][o]:
                                    for i in getEmail['messageText'][o]['email_result']:
                                        getStepNumber = getEmail['messageText'][o]['step_num']
                                        getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                        # print(getEmail_list,'getEmail_list')
                        sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                        res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                        if res_insert_pdf['result'] == 'OK':
                            getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                            if getTracking['result'] == 'OK':
                                ts = int(time.time())
                                st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                # print(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                if result_insert['result'] == 'OK':                                        
                                    sidCode = getTracking['step_data_sid']
                                    typeFile = str(fileName).split('.')[-1]
                                    FileId = res_insert_pdf['messageText']
                                    trackingId = getTracking['messageText']
                                    convert_pdf_image_v1(sidCode,str(base64_filedata))
                                    result_DocumentID = document_().genarate_document_ID(document_type)
                                    # print(result_DocumentID, ' result_DocumentID')
                                    # options_page_string = {'subject_text': '<ไม่มีหัวเรื่อง>', 'body_text': fileName}
                                    getDocument = insert().insert_document_new_v2(sidCode,typeFile,FileId,document_details,document_type,'M',digit_sign=tmp_digit_sign,attempted_name=Folder_Attachment_Name,documentID=result_DocumentID['messageText']['documentID'],options_page=options_page_string,sign_page_options=tmp_sign_page_options)
                                    if getDocument['result'] == 'OK':
                                        document_Id = getDocument['document_Id']
                                        ts = int(time.time())
                                        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                        
                                        getSender = insert().insert_paper_sender_v2(username,st,'ACTIVE',sender_name,oneEmail,tmptype,FileId,fileName,trackingId,sidCode,template_code,document_Id,webhook,email_center,ref_document=tmpref_document)
                                        # print(getSender,'getSender')
                                        if getSender['result'] == 'OK':
                                            arr_result = []
                                            data_list = []
                                            data_dict = {}
                                            
                                            getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                            sid_code_sha512 = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
                                            chat_service = chat_for_service_v1(sidCode,'Bearer ' + token_header)
                                            
                                            for i in getEmail_list:
                                                emailUser = i['email']
                                                getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                                if getUrl_Sign['result'] == 'OK':
                                                    data_list.append({
                                                        'email':emailUser,
                                                        'url_sign':getUrl_Sign['messageText'],
                                                        'tracking':trackingId,
                                                        'name_file':fileName,
                                                        'message':'',
                                                        'step_num': i['step_num']                                                                
                                                    })

                                            
                                            type_service = 'first'
                                            send_mail = send_Mail_for_service_v1(type_service,sidCode,trackingId,str(fileName),data_list)
                                            
                                            return jsonify({'result':'OK','messageText':{'id_transaction_paperless':sid_code_sha512,'url_tracking':paperless_tracking + trackingId,'tracking_id':trackingId,'attemp_status':tmp_attemp_status,'chat_service': chat_service[0]['messageText']['data']},'status_Code':200}),200

                                        else:
                                            delete().delete_all_table_for_service(sidCode)   
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'upload file fail'}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':getDocument['messageText']}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insert['messageText']}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':getTracking['messageText']}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':res_insert_pdf['messageText']}),200
                    else:        
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template or document type not found'}),200
                        return jsonify(get_Template)
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'cant get username and email'}),401
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':str(ex)}),200

@status_methods.route('/api/v2/upload_ppl_service',methods=['POST'])
def upload_service_ppl_v2():
    try:        
        try:
            token_header = request.headers['Authorization']
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'unauthorized'}),401
        url = one_url + "/api/account_and_biz_detail"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer"+" "+token_header
        }
        try:
            response = requests.get(url, headers=headers, verify=False)
            response = response.json()
        except requests.Timeout as ex:
            abort(401)
        except requests.HTTPError as ex:
            abort(401)
        except requests.ConnectionError as ex:
            abort(401)
        except requests.RequestException as ex:
            abort(401)
        except Exception as ex:
            abort(401)
        if 'result' in response:
            if response['result'] == 'Fail':
                abort(401)
        else:
            
            biz_info = []
            thai_email = response['thai_email']
            username = response['username']
            sender_name = response['first_name_th'] + ' ' + response['last_name_th']
            if 'biz_detail' in response:
                getbiz = response['biz_detail']
                for i in range(len(getbiz)):
                    jsonData = {
                        'id':getbiz[i]['getbiz'][0]['id'],
                        'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                        'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                        'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                        'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                        'role_level':getbiz[i]['getrole'][0]['role_level'],
                        'role_name':getbiz[i]['getrole'][0]['role_name']
                    }
                    biz_info.append(jsonData)
            result_arraylist = []
            result_detail_service = {}
            dataJson = request.json
            result_CheckTaxId = []
            biz_json = ''
            chatData = []
            list_emailChat_log = []
            chatRequestData = {}
            status_sendChat = []
            result_list = []
            arr_result_Email = []
            list_taskChat_log = []
            MailData = {}
            id_one_chat_to_msg = None
            if 'File_PDF' in dataJson and 'username' in dataJson and 'templateDetails'in dataJson and 'oneEmail' in dataJson and 'taxId' in dataJson\
            and 'DocumentType' in dataJson and 'Folder_Attachment_Name' in dataJson and 'subject_text' in dataJson and 'body_text' in dataJson and 'data_document' in dataJson\
            and 'email_center' in dataJson and len(dataJson) == 11:
                if username == dataJson['username'] and thai_email == dataJson['oneEmail']:
                    input_file      = dataJson['File_PDF']
                    username        = dataJson['username']
                    oneEmail        = dataJson['oneEmail']
                    template_detils = dataJson['templateDetails']
                    data_document = dataJson['data_document']
                    tmp_emailcenter = dataJson['email_center']
                    options_page_string = {
                        'subject_text': dataJson['subject_text'], 
                        'body_text': dataJson['body_text']
                    }
                    try:
                        null = None
                        template_detils_eval = eval(template_detils)
                        template_code = template_detils_eval['Template_Code']
                        template_step = template_detils_eval['Template_step']
                        # print(template_code)
                    except Exception as e:
                        print(str(e))
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template details error'}),200
                    # print(template_detils_eval)
                    # template_code   = dataJson['templateDetails']
                    tax_Id          = dataJson['taxId']  
                    Document_type   = dataJson['DocumentType']
                    Folder_Attachment_Name   = dataJson['Folder_Attachment_Name']
                    if str(Folder_Attachment_Name).replace(' ','') != '':
                        tmp_attemp_status = True
                    else:
                        tmp_attemp_status = False
                        Folder_Attachment_Name = None
                    fileName        = 'e-form_' + str(datetime.datetime.now()).split('.')[0].split(' ')[0] + 'T' +str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[0] + '-' + str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[1] + '-'+str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[2]
                    fileName        = str(fileName).replace(' ','') + ".pdf"
                    base64_filedata = input_file
                    if str(tax_Id).replace(' ','') is not '':
                        if len(biz_info) != 0:
                            for i in range(len(biz_info)):
                                if tax_Id == biz_info[i]['id_card_num']:
                                    result_CheckTaxId.append('Y')
                                    biz_json = biz_info[i]
                            if 'Y' in result_CheckTaxId:
                                pass
                            else:
                                return jsonify({'result':'ER','messageText':'taxId not found','status_Code':200}),200
                    else:
                        biz_json = None
                    tax_Id = str(tax_Id).replace(' ','')
                    list_eval = []
                    list_tmp_step_num = []
                    if tax_Id != '':
                        get_Template = select().select_get_string_templateAndusername_tax_new(str(template_code).replace(' ',''),str(tax_Id).replace(' ',''))
                        # print(get_Template)
                        # return ''
                        if get_Template['result'] == 'OK':
                            for zzi in range(len(template_step)):
                                one_email_info = template_step[zzi]['one_email']
                                for uzi in range(len(one_email_info)):
                                    if str(one_email_info[uzi]).replace(' ','') == '':
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found :email in list'}),200
                                    else:
                                        emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", str(one_email_info[uzi]).replace(' ',''))
                                        if emails is None:
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'email in list error'}),200
                                        else:
                                            pass
                                    
                                    eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                    
                                    if 'step_num' in eval_data_step:
                                        print((eval_data_step))
                                        step_num_in_db = eval_data_step['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                list_eval.append(eval_data_step)
                                        eval_data_step = (eval_data_step)
                                        string_json = eval_data_step
                                    
                                    else:
                                        print(eval_data_step)
                                        step_num_in_db = eval_data_step[zzi]['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            if step_num_in_db not in list_tmp_step_num:
                                                list_tmp_step_num.append(step_num_in_db)
                                                for uugg in range(len(template_step[zzi]['one_email'])):
                                                    eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                    print(eval_data_step[zzi])
                                                list_eval.append(eval_data_step[zzi])
                                        string_json = (list_eval) 
                            string_json_NoneEval = str(string_json)
                            document_details = str(get_Template['messageText'][0]['document_details_string'])
                            document_type = get_Template['messageText'][0]['document_details']['document_type']
                            # string_json = eval(get_Template['messageText'][0]['data_step'])
                            # string_json_NoneEval = str(get_Template['messageText'][0]['data_step'])
                            email_center = str(get_Template['messageText'][0]['email_center'])
                            step_Max = get_Template['messageText'][0]['step_Max']
                            result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                            string_json_NoneEval = str(result_SelectEmailMe['messageText'])                     
                            string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                            qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                            tmp_digit_sign = get_Template['messageText'][0]['digit_sign']
                            getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                            getEmail_list = []
                            if getEmail['result'] == 'OK':
                                for o in range(len(getEmail['messageText'])):
                                    if 'email_result' in getEmail['messageText'][o]:
                                        for i in getEmail['messageText'][o]['email_result']:
                                            getStepNumber = getEmail['messageText'][o]['step_num']
                                            getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                            sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                            res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                            
                            if res_insert_pdf['result'] == 'OK':
                                getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                                if getTracking['result'] == 'OK':                                    
                                    ts = int(time.time())
                                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                    result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    if result_insert['result'] == 'OK':                                        
                                        sidCode = getTracking['step_data_sid']
                                        typeFile = str(fileName).split('.')[-1]
                                        FileId = res_insert_pdf['messageText']
                                        trackingId = getTracking['messageText']
                                        convert_pdf_image_v1(sidCode,str(base64_filedata))
                                        result_DocumentID = document_().genarate_document_ID(document_type)
                                        # options_page_string = {'subject_text': '<ไม่มีหัวเรื่อง>', 'body_text': fileName}
                                        getDocument = insert().insert_document_new_v2(sidCode,typeFile,FileId,document_details,document_type,'M',digit_sign=tmp_digit_sign,attempted_name=Folder_Attachment_Name,documentID=result_DocumentID['messageText']['documentID'],options_page=options_page_string,data_document = data_document)
                                        if getDocument['result'] == 'OK':
                                            document_Id = getDocument['document_Id']
                                            ts = int(time.time())
                                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                            if tmp_emailcenter != '':
                                                email_center = []
                                                for x in range(len(tmp_emailcenter)):
                                                    email_center.append({"email":tmp_emailcenter[x],"file_pdf":"true","attemp_file":"true"})
                                                email_center = str(email_center)
                                            getSender = insert().insert_paper_sender_v2(username,st,'ACTIVE',sender_name,oneEmail,'owner',FileId,fileName,trackingId,sidCode,template_code,document_Id,'',email_center)
                                            if getSender['result'] == 'OK':
                                                arr_result = []
                                                data_dict = {}
                                                data_list = []

                                                getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                                sid_code_sha512 = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
                                                chat_service = chat_for_service_v1(sidCode,'Bearer ' + token_header)
                                                # print ('list_eval: ',list_eval)
                                                for i in getEmail_list:
                                                    emailUser = i['email']
                                                    getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                                    if getUrl_Sign['result'] == 'OK':
                                                        data_list.append({
                                                            'email':emailUser,
                                                            'url_sign':getUrl_Sign['messageText'],
                                                            'tracking':trackingId,
                                                            'name_file':fileName,
                                                            'message':'',
                                                            'step_num': i['step_num']                                                                
                                                        })

                                                type_service = 'first'
                                                send_mail = send_Mail_for_service_v1(type_service,sidCode,trackingId,str(fileName),data_list)
                                                
                                                return jsonify({'result':'OK','messageText':{'id_transaction_paperless':sid_code_sha512,'url_tracking':paperless_tracking + trackingId,'tracking_id':trackingId,'attemp_status':tmp_attemp_status,'chat_service': chat_service[0]['messageText']['data']},'status_Code':200}),200

                                            else:
                                                delete().delete_all_table_for_service(sidCode)  
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'upload file fail'}),200
                                        else:
                                            return jsonify({'result':'ER','messageText':getDocument['messageText'],'status_Code':200}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                                else:
                                    return jsonify({'result':'ER','messageText':getTracking['messageText'],'status_Code':200}),200
                            else:
                                return jsonify({'result':'ER','messageText':res_insert_pdf['messageText'],'status_Code':200}),200
                        else:        
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template not found in taxId'}),200
                            return ''
                    else:
                        get_Template = select().select_get_string_templateAndusername(str(username).replace(' ',''),str(template_code).replace(' ',''))
                        
                        if get_Template['result'] == 'OK':
                            for zzi in range(len(template_step)):
                                one_email_info = template_step[zzi]['one_email']
                                for uzi in range(len(one_email_info)):
                                    if str(one_email_info[uzi]).replace(' ','') == '':
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data not found :email in list'}),200
                                    else:
                                        emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", str(one_email_info[uzi]).replace(' ',''))
                                        if emails is None:
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'email in list error'}),200
                                        else:
                                            pass
                                    
                                    eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                    if 'step_num' in eval_data_step:
                                        print((eval_data_step))
                                        step_num_in_db = eval_data_step['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                list_eval.append(eval_data_step)
                                        eval_data_step = (eval_data_step)
                                        string_json = eval_data_step
                                    else:
                                        step_num_in_db = eval_data_step[zzi]['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                        list_eval.append(eval_data_step[zzi])
                                        string_json = (list_eval)
                            string_json_NoneEval = str(string_json)
                            document_details = str(get_Template['messageText'][0]['document_details_string'])
                            document_type = get_Template['messageText'][0]['document_details']['document_type']
                            # string_json = eval(get_Template['messageText'][0]['data_step'])
                            # string_json_NoneEval = str(get_Template['messageText'][0]['data_step'])
                            email_center = str(get_Template['messageText'][0]['email_center'])
                            step_Max = get_Template['messageText'][0]['step_Max']                            
                            tmp_digit_sign = get_Template['messageText'][0]['digit_sign']
                            result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                            print(result_SelectEmailMe)
                            string_json_NoneEval = str(result_SelectEmailMe['messageText'])                            
                            string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                            qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                            getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                            getEmail_list = []
                            if getEmail['result'] == 'OK':
                                for o in range(len(getEmail['messageText'])):
                                    if 'email_result' in getEmail['messageText'][o]:
                                        for i in getEmail['messageText'][o]['email_result']:
                                            getStepNumber = getEmail['messageText'][o]['step_num']
                                            getEmail_list.append({'email':i['email'],'status_chat':i['status_chat'],'step_num':getStepNumber,'property':i['property']})
                            # print(getEmail_list,'getEmail_list')
                            sha512encode = hashlib.sha512(str(base64_filedata).encode('utf-8')).hexdigest()            
                            res_insert_pdf = insert().insert_paper_pdf(str(base64_filedata),sha512encode)
                            if res_insert_pdf['result'] == 'OK':
                                getTracking = insert().insert_paper_tracking(None,res_insert_pdf['messageText'],template_code,step_Max)
                                if getTracking['result'] == 'OK':
                                    ts = int(time.time())
                                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                    # print(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    result_insert = insert().insert_paper_datastepv2_1(getTracking['step_data_sid'],string_json_NoneEval,st,string_Upload,step_Max,biz_json,qrCode_position)
                                    if result_insert['result'] == 'OK':                                        
                                        sidCode = getTracking['step_data_sid']
                                        typeFile = str(fileName).split('.')[-1]
                                        FileId = res_insert_pdf['messageText']
                                        trackingId = getTracking['messageText']
                                        convert_pdf_image_v1(sidCode,str(base64_filedata))
                                        result_DocumentID = document_().genarate_document_ID(document_type)
                                        # print(result_DocumentID, ' result_DocumentID')
                                        # options_page_string = {'subject_text': '<ไม่มีหัวเรื่อง>', 'body_text': fileName}
                                        getDocument = insert().insert_document_new_v2(sidCode,typeFile,FileId,document_details,document_type,'M',digit_sign=tmp_digit_sign,attempted_name=Folder_Attachment_Name,documentID=result_DocumentID['messageText']['documentID'],options_page=options_page_string)
                                        if getDocument['result'] == 'OK':
                                            document_Id = getDocument['document_Id']
                                            ts = int(time.time())
                                            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
                                            if tmp_emailcenter != '':
                                                email_center = []
                                                for x in range(len(tmp_emailcenter)):
                                                    email_center.append({"email":tmp_emailcenter[x],"file_pdf":"true","attemp_file":"true"})
                                                email_center = str(email_center)
                                            getSender = insert().insert_paper_sender_v2(username,st,'ACTIVE',sender_name,oneEmail,'owner',FileId,fileName,trackingId,sidCode,template_code,document_Id,'',email_center)
                                            # print(getSender,'getSender')
                                            if getSender['result'] == 'OK':
                                                arr_result = []
                                                data_list = []
                                                data_dict = {}
                                               
                                                getSign = insert().insert_sign_data(sidCode,string_json_NoneEval,FileId)
                                                sid_code_sha512 = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
                                                chat_service = chat_for_service_v1(sidCode,'Bearer ' + token_header)
                                                
                                                for i in getEmail_list:
                                                    emailUser = i['email']
                                                    getUrl_Sign = select().select_geturl(emailUser,sidCode)
                                                    if getUrl_Sign['result'] == 'OK':
                                                        data_list.append({
                                                            'email':emailUser,
                                                            'url_sign':getUrl_Sign['messageText'],
                                                            'tracking':trackingId,
                                                            'name_file':fileName,
                                                            'message':'',
                                                            'step_num': i['step_num']                                                                
                                                        })

                                                
                                                type_service = 'first'
                                                send_mail = send_Mail_for_service_v1(type_service,sidCode,trackingId,str(fileName),data_list)
                                                
                                                return jsonify({'result':'OK','messageText':{'id_transaction_paperless':sid_code_sha512,'url_tracking':paperless_tracking + trackingId,'tracking_id':trackingId,'attemp_status':tmp_attemp_status,'chat_service': chat_service[0]['messageText']['data']},'status_Code':200}),200

                                            else:
                                                delete().delete_all_table_for_service(sidCode)   
                                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'upload file fail'}),200
                                        else:
                                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':getDocument['messageText']}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insert['messageText']}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':getTracking['messageText']}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':res_insert_pdf['messageText']}),200
                        else:        
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'template or document type not found'}),200
                            return jsonify(get_Template)
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'cant get username and email'}),401
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':str(ex)}),200

@status_methods.route('/api/v1/get_status',methods=['GET'])
def get_status_eform_v1():
    if request.method == 'GET':
        tracking = request.args.get('tracking')
        if tracking != None:
            tracking_eform = str(tracking).replace(' ','')
            return select().select_track_eform(tracking_eform)

@status_methods.route('/api/v1/get_status_document',methods=['POST'])
def get_status_document_eform_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                abort(401)
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header_bearer = 'Bearer ' + token_header
            result_verify = token_required_func(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!' + str(e)})
        if result_verify['result'] == 'OK':
            username = result_verify['username']
            thai_email = result_verify['email']
            dataJson = request.json
            if 'ppl_code' in dataJson and len(dataJson) == 1:
                paperlessCode = dataJson['ppl_code']
                result_select = select().select_status_for_eform_v2(paperlessCode,thai_email)
                if result_select['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_select['messageER']}),200
            else:
                abort(404)
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':'token has expired','status_Code':401}),401

@status_methods.route('/api/v1/get_profile_sign',methods=['POST'])
def get_profile_sign_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!' + str(e)})
        if result_verify['result'] == 'OK':
            messageText_result = result_verify['messageText'].json()
            print(messageText_result)
            if 'result' not in messageText_result:
                email_thai = messageText_result['thai_email']
                username = messageText_result['username']
                dataJson = request.json
                if 'email_User' in dataJson and 'username' in dataJson and len(dataJson) == 2:
                    tmp_emailUser = dataJson['email_User']
                    tmp_username = dataJson['username']
                    if tmp_emailUser == email_thai and tmp_username == username:
                        result_select = select().select_profile_For_eform_v1(tmp_emailUser,tmp_username)
                        if result_select['result'] == 'OK':
                            return jsonify({'result':'OK','messageText':[result_select['messageText']],'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':[],'status_Code':400,'messageER':result_select['messageText']}),400
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'email or username non match'}),401
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':None}),401
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':None}),401

@status_methods.route('/api/v1/update_template',methods=['POST'])
@token_required
def update_temp():
    try:
        dataJson = request.json
        if 'step_num' in dataJson and 'template_code' in dataJson and 'step_data' in dataJson:
            step_num = dataJson['step_num']
            step_code = dataJson['template_code']
            step_data = dataJson['step_data']
            result_update = update().update_template_v1(step_num,step_code,step_data)
            if result_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_update['messageText'],'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':result_update['messageText'],'status_Code':200}),200
    except Exception as e:
        return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':500}),500

@status_methods.route('/api/v1/push_data_flow',methods=['POST'])
def push_data_flow_v1():
    if 'Authorization' not in request.headers:
        abort(401)
    token_header = request.headers['Authorization']
    try:                
        token_header = str(token_header).split(' ')[1]
    except Exception as ex:
        abort(401)
    dataJson = request.json
    if 'fileData' not in dataJson and 'documentData' not in dataJson:
        abort(404)
    tmpfileData = dataJson['fileData']
    tmpdocumentData = dataJson['documentData']
    tmpdecodedata  = data_doc(tmpdocumentData)
    try:
        if 'messageText' in tmpdecodedata:
            tmp_datamessage = tmpdecodedata['messageText']
            if 'flow_eform' in tmp_datamessage:
                tmpdata_flow_eform = eval(str(tmp_datamessage['flow_eform']))
                formdata_eform = eval(str(tmp_datamessage['formdata_eform']))
                data_json_key = eval(str(formdata_eform['data_json_key']))
                filename = data_json_key[0]['document_name'] + '.pdf'
                sender_email = data_json_key[0]['email_user']
                sender_name = data_json_key[0]['sender_name']
                type_file =  'application/pdf'
                biz_detail = data_json_key[0]['permission_form']
                send_user = data_json_key[0]['create_by']
                document_type = tmp_datamessage['document_type']
                attempted_name = data_json_key[0]['attempted_name']
                last_digitsign = 'true'
                if 'last_digitsign' in data_json_key[0]:
                    last_digitsign = data_json_key[0]['last_digitsign']
                document_json = paper_lessdocument_detail.query.filter(paper_lessdocument_detail.documentUser==send_user)\
                .filter(paper_lessdocument_detail.documentType==document_type).all()
                if len(document_json) == 0:
                    document_json = "{'document_type': None, 'document_name': None, 'document_remark': None}"
                sign_page_options = 'OFF'
                step_max = data_json_key[0]['step_max']
                options_page =  data_json_key[0]['options_page']
                sender_position =  data_json_key[0]['sender_position']
                step_upload_01 = {
                    'step_num':'0',
                    'step_description': 'upload document',
                    'step_answer': '',
                    'step_detail': [{
                        'one_email': send_user,
                        'activity_code': ['A01'],
                        'activity_description': ['PAPERLESS_UPLOAD'],
                        'activity_status': ['OK'],
                        'activity_time':[{}]
                    }]
                }
                urgent_type = 'M'
                digit_sign = data_json_key[0]['digit_sign']
                status = 'ACTIVE'
                step_code = ''
                sender_webhook= data_json_key[0]['sender_webhook']
                email_center = data_json_key[0]['email_center']
                time_expire = data_json_key[0]['time_expire']
                importance = data_json_key[0]['importance']
                convert_id = None
                template = data_json_key[0]['template_code']
                qrCode_position = "{'qr_llx':'-2.544','qr_lly':'1.248','qr_page':1,'qr_urx':'0.000','qr_ury':'0.000'}"
                eform_id = data_json_key[0]['eform_id']
                result_upload = insert_1().insert_upload_ppl(template,step_max,str(tmpdata_flow_eform),filename,convert_id,\
                tmpfileData,str(step_upload_01),biz_detail,qrCode_position,document_type,type_file,document_json,\
                urgent_type,digit_sign,attempted_name,sign_page_options,options_page,\
                send_user,status,sender_name,sender_email,sender_position,step_code,sender_webhook,email_center\
                ,time_expire,str(importance),eform_id,last_digitsign)
                if result_upload['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':result_upload['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':result_upload['messageText'],'status_Code':200}),200
        return jsonify({'result':'OK','messageText':{'data':tmpdecodedata,'message':'success'},'messageER':None,'status_Code':200}),200
    except Exception as ex:
        return jsonify({'result':'ER','messageText':None,'messageER':str(ex),'status_Code':200}),200

@status_methods.route('/api/v1/upload_ppl_service',methods=['POST'])
def ppl_service_api_v1():
    try:
        token_header = request.headers['Authorization']
        token_header = str(token_header).split(' ')[1]
    except Exception as ex:
        abort(401)
    url = one_url + "/api/account_and_biz_detail"
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer"+" "+token_header
    }
    try:
        response = requests.get(url, headers=headers, verify=False,timeout=10)
        response = response.json()
    except Exception as ex:
        abort(401)
    if 'result' in response:
        if response['result'] == 'Fail':
            abort(401)
    dep_id_list = []
    tmp_role_id_list = []
    dept_name_list = []
    position_list = []
    list_role_level = []
    low_role_id = []
    low_role_name = []
    dep_data = None       
    biz_info = []
    tmpdept_id = []
    tmpdept_name_list = []
    tmpposition_list = []
    tmpuser_id = response['id']
    thai_email = response['thai_email']
    username = response['username']
    sender_name = response['first_name_th'] + ' ' + response['last_name_th']
    sender_name_eng = response['first_name_eng'] + ' ' + response['last_name_eng']
    if 'biz_detail' in response:
        getbiz = response['biz_detail']
        for i in range(len(getbiz)):
            data_get_my_dep = {
                "tax_id":getbiz[i]['getbiz'][0]['id_card_num']
            } 
            text_one_access = "Bearer" + " " + token_header
            result_GetMydetp = callAuth_post_v2(one_url+'/api/get_my_department_role',data_get_my_dep,text_one_access)
            if result_GetMydetp['result'] == 'OK':
                res_json = result_GetMydetp['messageText'].json()
                if res_json['data'] != None:
                    data_res = res_json['data']                                            
                    if data_res != '':
                        for y in range(len(data_res)):
                            dep_id = (data_res[y]['dept_id'])
                            tmp_role_id = (data_res[y]['role_id'])
                            tmp_role_detail = data_res[y]['role'][0]
                            tmp_role_level = tmp_role_detail['role_level']
                            tmp_role_name = tmp_role_detail['role_name']
                            if dep_id != '' and dep_id != None:
                                dep_id_list.append(dep_id)
                                dep_data = data_res[y]['department']
                                for iy in range(len(dep_data)):
                                    dept_name_list.append(dep_data[iy]['dept_name'])
                                    try:
                                        position_list.append(dep_data[iy]['dept_position'])
                                    except Exception as e:
                                        position_list.append('')
                            if tmp_role_id != '' and tmp_role_id != None:
                                tmp_role_id_list.append(tmp_role_id)
                                low_role_id.append(tmp_role_level)
                                low_role_name.append(tmp_role_name)
            if len(dep_id_list) != 0:
                tmpdept_id = dep_id_list[0]
            if len(dept_name_list) != 0:
                tmpdept_name_list = dept_name_list[0]
            if len(position_list) != 0:
                tmpposition_list = position_list[0]
            jsonData = {
                'id':getbiz[i]['getbiz'][0]['id'],
                'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                'role_level':getbiz[i]['getrole'][0]['role_level'],
                'role_name':getbiz[i]['getrole'][0]['role_name'],
                'dept_id':tmpdept_id,
                'dept_name':tmpdept_name_list,
                'dept_position':tmpposition_list,
            }
            biz_info.append(jsonData)
    executor.submit(profile_func_v1(tmpuser_id,username,thai_email,token_header))
    result_arraylist = []
    result_detail_service = {}
    dataJson = request.json
    result_CheckTaxId = []
    biz_json = ''
    chatData = []
    list_emailChat_log = []
    chatRequestData = {}
    status_sendChat = []
    result_list = []
    arr_result_Email = []
    list_taskChat_log = []
    MailData = {}
    id_one_chat_to_msg = None
    null = None
    if 'File_PDF' in dataJson and 'username' in dataJson and 'templateDetails'in dataJson and 'oneEmail' in dataJson and 'taxId' in dataJson\
    and 'DocumentType' in dataJson and 'Folder_Attachment_Name' in dataJson and 'subject_text' in dataJson and 'body_text' in dataJson and 'data_document' in dataJson:
        if username == dataJson['username'] and thai_email == dataJson['oneEmail']:
            input_file      = dataJson['File_PDF']
            username        = dataJson['username']
            oneEmail        = dataJson['oneEmail']
            template_detils = dataJson['templateDetails']
            data_document = dataJson['data_document']
            tax_Id          = dataJson['taxId']  
            Document_type   = dataJson['DocumentType']
            Folder_Attachment_Name   = dataJson['Folder_Attachment_Name']
            tmpref_document = None
            fileName = None
            tmpdocument_id = None
            tmptype_file = "application/pdf"
            tmptype = "owner"
            if 'ref_document' in dataJson:
                tmpref_document = str(dataJson['ref_document'])
            if 'filename' in dataJson:
                fileName = str(dataJson['filename'])
            if 'type' in dataJson:
                tmptype = dataJson['type']
            if 'tracking_id' in dataJson:
                tmptracking = dataJson['tracking']
            if 'document_id' in dataJson:
                tmpdocument_id = dataJson['document_id']
            if str(Folder_Attachment_Name).replace(' ','') != '':
                tmp_attemp_status = True
            else:
                tmp_attemp_status = False
                Folder_Attachment_Name = None
            options_page_string = {
                'subject_text': dataJson['subject_text'], 
                'body_text': dataJson['body_text']
            }
            try:
                template_detils_eval = eval(template_detils)
                template_code = template_detils_eval['Template_Code']
                template_step = template_detils_eval['Template_step']
            except Exception as e:
                return jsonify({'status':'fail','message':'template details error','code':200,'data':[]}),400
            if fileName == None:
                fileName        = 'e-form_' + str(datetime.datetime.now()).split('.')[0].split(' ')[0] + 'T' +str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[0] + '-' + str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[1] + '-'+str(datetime.datetime.now()).split('.')[0].split(' ')[1].split(':')[2]
                fileName        = str(fileName).replace(' ','') + ".pdf"
            base64_filedata = input_file
            rdept = select_4().select_dept_document_type_v1(Document_type,tax_Id)
            datadeptName = None
            if rdept['result'] == 'OK':
                if len(rdept['data']) != 0:
                    messagedata_rdept = rdept['data'][0]
                    if 'dept_name' in  eval(messagedata_rdept['biz_info']):
                        datadeptName = eval(messagedata_rdept['biz_info'])['dept_name']
            # return jsonify(datadeptName)
            if str(tax_Id).replace(' ','') is not '':
                if len(biz_info) != 0:
                    for i in range(len(biz_info)):
                        if tax_Id == biz_info[i]['id_card_num']:
                            result_CheckTaxId.append('Y')
                            biz_json = biz_info[i]
                            if datadeptName != None:
                                biz_json['dept_name'] = datadeptName
                    if 'Y' in result_CheckTaxId:
                        pass
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'tax_id not found'}),200
            else:
                biz_json = None
            tax_Id = str(tax_Id).replace(' ','')
            recheck = cal_Check_tax_id(tax_Id)
            if recheck == True:
                rGetMaxpage = get_maxpages_pdf(input_file)    
                if rGetMaxpage[0] == 200:
                    maxPages = rGetMaxpage[1]
                    message = rGetMaxpage[2]
                list_eval = []
                list_tmp_step_num = []
                tmp_sign_page_options = 'OFF'
                if tax_Id != '':
                    get_Template = select().select_get_string_templateAndusername_tax_new(str(template_code).replace(' ',''),str(tax_Id).replace(' ',''))
                    # return get_Template
                    if get_Template['result'] == 'OK':
                        for zzi in range(len(template_step)):
                            one_email_info = template_step[zzi]['one_email']
                            if len(one_email_info) != 0:
                                for uzi in range(len(one_email_info)):
                                    eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                    if 'step_num' in eval_data_step:
                                        # print((eval_data_step))
                                        step_num_in_db = eval_data_step['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                list_eval.append(eval_data_step)
                                        eval_data_step = (eval_data_step)
                                        string_json = eval_data_step
                                    
                                    else:
                                        # # print(eval_data_step)
                                        # print(template_step[zzi]['one_email'])
                                        step_num_in_db = eval_data_step[zzi]['step_num']
                                        if template_step[zzi]['step_num'] == step_num_in_db:
                                            if step_num_in_db not in list_tmp_step_num:
                                                list_tmp_step_num.append(step_num_in_db)
                                                # print(template_step[zzi]['one_email'])
                                                if len(template_step[zzi]['one_email']) != 0:
                                                    for uugg in range(len(template_step[zzi]['one_email'])):
                                                        eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                                else:
                                                    eval_data_step[zzi]['step_detail'][uugg]['one_email'] = ""
                                                    # print(eval_data_step[zzi])
                                                list_eval.append(eval_data_step[zzi])
                                        string_json = (list_eval)
                            else:
                                eval_data_step = eval(get_Template['messageText'][0]['data_step'])
                                
                                if 'step_num' in eval_data_step:
                                    step_num_in_db = eval_data_step['step_num']
                                    if template_step[zzi]['step_num'] == step_num_in_db:
                                        for uugg in range(len(template_step[zzi]['one_email'])):
                                            eval_data_step['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                            list_eval.append(eval_data_step)
                                    eval_data_step = (eval_data_step)
                                    string_json = eval_data_step
                                
                                else:
                                    # # print(eval_data_step)
                                    # print(template_step[zzi]['one_email'])
                                    step_num_in_db = eval_data_step[zzi]['step_num']
                                    if template_step[zzi]['step_num'] == step_num_in_db:
                                        if step_num_in_db not in list_tmp_step_num:
                                            list_tmp_step_num.append(step_num_in_db)
                                            # print(template_step[zzi]['one_email'])
                                            # if len(template_step[zzi]['one_email']) != 0:
                                            for uugg in range(len(template_step[zzi]['one_email'])):
                                                #     eval_data_step[zzi]['step_detail'][uugg]['one_email'] = template_step[zzi]['one_email'][uugg]
                                            # else:
                                                eval_data_step[zzi]['step_detail'][uugg]['one_email'] = ""
                                                # print(eval_data_step[zzi])
                                            list_eval.append(eval_data_step[zzi])
                                        string_json = (list_eval)
                        string_json_NoneEval = str(string_json)
                        document_details = str(get_Template['messageText'][0]['document_details_string'])
                        document_type = get_Template['messageText'][0]['document_details']['document_type']
                        tmp_options_page = get_Template['messageText'][0]['options_page']
                        if tmp_options_page != None:
                            tmp_options_page = eval(tmp_options_page)
                        result_datadoc = data_doc(data_document)
                        result_documentType = select_1().select_document_type_forservice_v1(None,tax_Id,Document_type)
                        if result_documentType['result'] == 'OK' and result_datadoc['result'] == 'OK':
                            tmpmessage = result_documentType['messageText']
                            for tzq in range(len(tmpmessage)):
                                if 'name_service' in tmpmessage[tzq]:
                                    if tmpmessage[tzq]['name_service'] == 'GROUP':
                                        if 'other' in tmpmessage[tzq]:
                                            for xx in range(len(tmpmessage[tzq]['other'])):
                                                for uu in range(len(tmpmessage[tzq]['other'])):
                                                    if 'properties' in tmpmessage[tzq]['other'][uu]:
                                                        for op in range(len(tmpmessage[tzq]['other'][uu]['properties'])):
                                                            if 'name' in tmpmessage[tzq]['other'][uu]['properties'][op]:
                                                                tmpnamekey = tmpmessage[tzq]['other'][uu]['properties'][op]['name']
                                                                if 'formdata_eform' in  result_datadoc['messageText']:
                                                                    tmp_formdata_eform = result_datadoc['messageText']['eform_data']
                                                                    if len(tmp_formdata_eform) != 0:
                                                                        for yy in range(len(tmp_formdata_eform)):
                                                                            tmpjson_key = tmp_formdata_eform[yy]['json_key']
                                                                            tmp_value = tmp_formdata_eform[yy]['value']
                                                                            if str(tmpjson_key).replace(' ','').lower() == str(tmpnamekey).replace(' ','').lower():
                                                                                tmpmessage[tzq]['other'][uu]['properties'][op]['value'] = tmp_value
                                    if tmpmessage[tzq]['name_service'] == 'GROUP2':
                                        if 'other' in tmpmessage[tzq]:
                                            for xx in range(len(tmpmessage[tzq]['other'])):
                                                for uu in range(len(tmpmessage[tzq]['other'])):
                                                    if 'properties' in tmpmessage[tzq]['other'][uu]:
                                                        for op in range(len(tmpmessage[tzq]['other'][uu]['properties'])):
                                                            if 'name' in tmpmessage[tzq]['other'][uu]['properties'][op]:
                                                                tmpnamekey = tmpmessage[tzq]['other'][uu]['properties'][op]['name']
                                                                if 'formdata_eform' in  result_datadoc['messageText']:
                                                                    tmp_formdata_eform = result_datadoc['messageText']['eform_data']
                                                                    if len(tmp_formdata_eform) != 0:
                                                                        for yy in range(len(tmp_formdata_eform)):
                                                                            tmpjson_key = tmp_formdata_eform[yy]['json_key']
                                                                            tmp_value = tmp_formdata_eform[yy]['value']
                                                                            if str(tmpjson_key).replace(' ','').lower() == str(tmpnamekey).replace(' ','').lower():
                                                                                tmpmessage[tzq]['other'][uu]['properties'][op]['value'] = tmp_value
                            options_page_string['service_properties'] = tmpmessage
                            if len(tmp_options_page) != 0:
                                tmp_options_page.update(options_page_string)
                            options_page_string = tmp_options_page
                            if len(options_page_string) == 0:
                                options_page_string = {
                                    'subject_text': dataJson['subject_text'], 
                                    'body_text': dataJson['body_text']
                                }
                        email_center = str(get_Template['messageText'][0]['email_center'])
                        webhook = str(get_Template['messageText'][0]['webhook'])
                        step_Max = get_Template['messageText'][0]['step_Max']
                        result_SelectEmailMe = selection_email_JsonData(string_json,step_Max,oneEmail)
                        string_json_NoneEval = str(result_SelectEmailMe['messageText'])                     
                        string_Upload = str(get_Template['messageText'][0]['step_Upload'])
                        qrCode_position = str(get_Template['messageText'][0]['qrCode_position'])
                        tmp_digit_sign = get_Template['messageText'][0]['digit_sign']
                        tmp_sign_page_options = get_Template['messageText'][0]['sign_page_options']
                        tmp_urgent_code = get_Template['messageText'][0]['urgent_code']
                        tmp_time_expire = get_Template['messageText'][0]['time_expire']
                        tmp_importance = get_Template['messageText'][0]['importance_doc']
                        tmp_last_digitsign = get_Template['messageText'][0]['last_digit_sign']
                        tmp_status_ref = get_Template['messageText'][0]['status_ref']
                        # tmp_sign_page_options = get_Template['messageText'][0]['sign_page_options']
                        # tmp_sign_page_options = get_Template['messageText'][0]['sign_page_options']
                        # tmp_sign_page_options = get_Template['messageText'][0]['sign_page_options']
                        getEmail = selection_email_v2(string_json,step_Max,oneEmail)
                        tmpconvert_id = None
                        eform_id = None  
                        tmptax_id = None    
                        tmpnamesender = '{"th":"'+str(sender_name)+'","eng":"'+str(sender_name_eng)+'"}'  
                        if 'id_card_num' in biz_json:
                            tmptax_id = biz_json['id_card_num']
                            executor.submit(cal_taxId_v1,tax_Id)
                        result_upload = insert_1().insert_upload_ppl_v2(template_code,int(step_Max),string_json_NoneEval,fileName,tmpconvert_id,base64_filedata,string_Upload,biz_json,qrCode_position,Document_type,tmptype_file,document_details,\
                        tmp_urgent_code,tmp_digit_sign,Folder_Attachment_Name,tmp_sign_page_options,tmp_options_page,\
                        username,"ACTIVE",tmpnamesender,oneEmail,tmptype,template_code,webhook,email_center\
                        ,tmp_time_expire,tmp_importance,eform_id,tmp_last_digitsign,tmp_status_ref,tmpref_document,tax_Id,data_document,tmpdocument_id,messagePages=message)
                        if result_upload['result'] == 'OK':
                            sidCode = result_upload['messageText'][0]['step_data_sid']
                            trackingId = result_upload['messageText'][0]['tracking_code']
                            convert_pdf_image_v1(sidCode,str(base64_filedata))
                            sid_code_sha512 = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
                            chat_service = chat_for_service_v1(sidCode,'Bearer ' + token_header)
                            send_mail = send_Mail_for_service_v2(sidCode)
                            executor.submit(call_webhookService,sidCode)
                            if chat_service['result'] == 'OK':
                                tmpmessagechat_service = chat_service['messageText']
                            else:
                                tmpmessagechat_service = chat_service['messageER']
                            return jsonify({'result':'OK','messageText':{'id_transaction_paperless':sid_code_sha512,'url_tracking':paperless_tracking + trackingId,'tracking_id':trackingId,'attemp_status':tmp_attemp_status,'chat_service': tmpmessagechat_service['data']},'status_Code':200}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'messageER':'upload service fail'}),400
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':400,'messageER':'transaction full'}),400
        else:
            abort(401)
    abort(404)