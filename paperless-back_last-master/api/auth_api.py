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
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *
from method.sftp_fucn import *
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

@status_methods.route('/api/v1/OneAuth/Sign',methods=['POST'])
def oneAuth_API_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'base64_string' in dataJson and 'max_Step' in dataJson and 'Step_Num' in dataJson and 'sign_position' in dataJson and 'sign_string' in dataJson and 'credentialId' in dataJson and len(dataJson) == 6:
            sign_position = dataJson['sign_position']
            sign_string = dataJson['sign_string']
            if 'sign_llx' in sign_position and 'sign_lly' in sign_position and 'sign_urx' in sign_position and 'sign_ury' in sign_position and 'sign_page' in sign_position and 'max_page' in sign_position and len(sign_position) == 6:
                res_arraylist = []
                base64_pdf_String = dataJson['base64_string']
                credentialId = dataJson['credentialId']
                type_certifyLevel = ''
                try:
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
                        # print(type_certifyLevel)
                        res_signPdf = signing_pdfSigning_v3(base64_pdf_String,sadData,"","","",type_certifyLevel,"","","","","","",token_header,sign_position,sign_string)
                        # print(res_signPdf)
                        if res_signPdf['result'] == 'OK':
                            res_arraylist.append({'result_signPdfService':res_signPdf})
                            return jsonify({'result':'OK','messageText':res_arraylist,'status_Code':200,'messageER':None,'messageService':type_certifyLevel}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'sign pdf service error ' + res_signPdf['msg']}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'authorize service error ' + res_authorize['msg']}),200
                except Exception as ex:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list service error ' + str(ex)}),200
            else:
                abort(404)
        else:
            abort(404)


@status_methods.route('/api/v4/OneAuth/Sign',methods=['POST'])
def oneAuth_API_v4():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'base64_string' in dataJson and 'max_Step' in dataJson and 'Step_Num' in dataJson and 'sign_position' in dataJson and 'sign_string' in dataJson:
            tmplast_digitsign = None
            credentialId = None
            stamp_all = None
            if 'last_digitsign' in dataJson:
                tmplast_digitsign = dataJson['last_digitsign']
            if 'credentialId' in dataJson:
                credentialId = dataJson['credentialId']
            if 'stamp_all' in dataJson:
                stamp_all = dataJson['stamp_all']
            sign_position = dataJson['sign_position']
            sign_string = dataJson['sign_string']
            if 'sign_llx' in sign_position and 'sign_lly' in sign_position and 'sign_urx' in sign_position and 'sign_ury' in sign_position and 'sign_page' in sign_position and 'max_page' in sign_position and len(sign_position) == 6:
                res_arraylist = []
                base64_pdf_String = dataJson['base64_string']
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
                        if credentialId == None:
                            credentialId = res_list['msg']['credentials'][0]['credentialId']
                        res_authorize = credentials_authorize_v2(credentialId,"","","","","","","",token_header)
                        if res_authorize['result'] == 'OK':
                            res_arraylist.append({'result_authorizeService':res_authorize})
                            sadData = res_authorize['msg']['sad']
                            if tmplast_digitsign == None or tmplast_digitsign == False:
                                if stamp_all == None or stamp_all == False:
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
                                elif stamp_all == True:                                    
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
                            elif tmplast_digitsign == True:
                                if int(sign_position['sign_page']) == int(sign_position['max_page']):
                                    if int(dataJson['Step_Num']) == int(dataJson['max_Step']):
                                        type_certifyLevel = 'NON-CERTIFY'
                                    else:
                                        type_certifyLevel = 'NON-CERTIFY'
                                else:
                                    if int(dataJson['Step_Num']) == int(dataJson['max_Step']):
                                        type_certifyLevel = 'NON-CERTIFY'
                                    else:
                                        type_certifyLevel = 'NON-CERTIFY'
                            res_signPdf = signing_pdfSigning_v3(base64_pdf_String,sadData,"","","",type_certifyLevel,"","","","","","",token_header,sign_position,sign_string)
                            # print(res_signPdf)
                            if res_signPdf['result'] == 'OK':
                                res_arraylist.append({'result_signPdfService':res_signPdf})
                                return jsonify({'result':'OK','messageText':res_arraylist,'status_Code':200,'messageER':None,'messageService':type_certifyLevel}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'signPdf Service Error!'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Authorize Service Error!' + res_authorize['msg']}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + res_list['msg']}),200
                except Exception as ex:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + str(ex)}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404

@status_methods.route('/api/v5/OneAuth/Sign',methods=['POST'])
def oneAuth_API_v5():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'base64_string' in dataJson and 'max_Step' in dataJson and 'Step_Num' in dataJson and 'sign_position' in dataJson and 'sign_string' in dataJson and len(dataJson) == 5:
            sign_position = dataJson['sign_position']
            sign_string = dataJson['sign_string']
            if 'sign_llx' in sign_position and 'sign_lly' in sign_position and 'sign_urx' in sign_position and 'sign_ury' in sign_position and 'sign_page' in sign_position and 'max_page' in sign_position and len(sign_position) == 6:
                res_arraylist = []
                base64_pdf_String = dataJson['base64_string']
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
                                    type_certifyLevel = 'CERTIFY'
                                else:
                                    type_certifyLevel = 'NON-CERTIFY'
                            # print(type_certifyLevel)
                            res_signPdf = signing_pdfSigning_v3(base64_pdf_String,sadData,"","","",type_certifyLevel,"","","","","","",token_header,sign_position,sign_string)
                            # print(res_signPdf)
                            if res_signPdf['result'] == 'OK':
                                res_arraylist.append({'result_signPdfService':res_signPdf})
                                return jsonify({'result':'OK','messageText':res_arraylist,'status_Code':200,'messageER':None,'messageService':type_certifyLevel}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'signPdf Service Error!'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'Authorize Service Error!' + res_authorize['msg']}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + res_list['msg']}),200
                except Exception as ex:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + str(ex)}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404

@status_methods.route('/api/v1/OneAuth/createNote', methods=['POST'])
def createNote_oneauth_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'pdfData' in dataJson and 'noteDisplayPage' in dataJson and 'noteDisplayRectangle' in dataJson and 'noteDisplayImage' in dataJson and 'noteTitle' in dataJson and 'noteText' in dataJson and len(dataJson) == 6:
            pdfData = dataJson['pdfData']
            noteDisplayPage = dataJson['noteDisplayPage']
            noteDisplayRectangle = dataJson['noteDisplayRectangle']
            noteDisplayImage = dataJson['noteDisplayImage']
            noteTitle = dataJson['noteTitle']
            noteText = dataJson['noteText']
            namefile = str(uuid.uuid4())
            # try:
            #     output_file = './temp/' + namefile + '.pdf'
            #     with io.BytesIO(base64.b64decode(pdfData)) as open_pdf_file:
            #         # pdf_reader = get_pdf_reader(open_pdf_file, file_arg)
            #         read_pdf = PdfFileReader(open_pdf_file)
            #         num_pages = read_pdf.getNumPages()
            #         pdf_writer = PdfFileWriter()
            #         for i in range(num_pages):
            #             pdf_writer.addPage(read_pdf.getPage(i))
            #         with open(output_file, 'wb') as fh:
            #             pdf_writer.write(fh)
            #     with open(output_file, "rb") as f:
            #         encodedZip = base64.b64encode(f.read())
            #         basefiledata = (encodedZip.decode())
            #     os.remove(output_file)
            # except Exception as e:
            #     basefiledata = pdfData
            result_oneAuth_createNote = createNote_pdf_v1(pdfData,noteDisplayPage,noteDisplayRectangle,noteDisplayImage,noteTitle,noteText,token_header)
            # print(result_oneAuth_createNote)
            if result_oneAuth_createNote['result'] == 'OK':
                if 'responseCode' in result_oneAuth_createNote['msg']:
                    if result_oneAuth_createNote['msg']['responseCode'] == 401:
                        abort(401)
                    if result_oneAuth_createNote['msg']['responseCode'] == 500:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':[result_oneAuth_createNote['msg']]}),200
                return jsonify({'result':'OK','messageText':[result_oneAuth_createNote['msg']],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':[result_oneAuth_createNote['msg']]}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200

@status_methods.route('/api/v1/OneAuth/createNoteAndSign', methods=['POST'])
def createNoteAndSign_oneauth_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'page' in dataJson and 'llx' in dataJson and 'lly' in dataJson and 'urx' in dataJson and 'ury' in dataJson and 'userName' in dataJson and 'stringPicture' in dataJson and 'stringPdf' in dataJson and  len(dataJson) == 8:
            page = dataJson['page']
            llx = dataJson['llx']
            lly = dataJson['lly']
            urx = dataJson['urx']
            ury = dataJson['ury']
            tmp_sign_position = {
                "sign_llx":llx,
                "sign_lly":lly,
                "sign_urx":urx,
                "sign_ury":ury,
                "sign_page":page
            }
            userName = dataJson['userName']
            stringPicture = dataJson['stringPicture']
            stringPdf = dataJson['stringPdf']
            res_arraylist = []
            res_list = credentials_list_v2("","","","","",token_header)
            if res_list['result'] == 'OK':
                data_msg = res_list['msg']
                try:
                    totalResult_oneAuth = data_msg['totalResult']
                    if totalResult_oneAuth == 0:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'sign profile not found'}),200
                    else:
                        pass
                except Exception as e:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list service error ' + str(e)}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list service error'}),200
            if res_list['result'] == 'OK':
                res_arraylist.append({'result_listService':res_list})
                credentialId = res_list['msg']['credentials'][0]['credentialId']
                res_authorize = credentials_authorize_v2(credentialId,"","","","","","","",token_header)
                if res_authorize['result'] == 'OK':
                    res_arraylist.append({'result_authorizeService':res_authorize})
                    sadData = res_authorize['msg']['sad']
                    result_Sign_Note = createNote_andSign_pdf_v1(stringPdf,sadData,"","","","","","","","","","",token_header,tmp_sign_position,stringPicture)
                    print(result_Sign_Note)
            return ''
            # result_oneAuth_createNote = createNote_andSign_pdf_v1(pdfData,noteDisplayPage,noteDisplayRectangle,noteDisplayImage,noteTitle,noteText,token_header)
            # if result_oneAuth_createNote['result'] == 'OK':
            #     return jsonify({'result':'OK','messageText':[result_oneAuth_createNote['msg']],'status_Code':200,'messageER':None}),200
            # else:
            #     return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':[result_oneAuth_createNote['msg']]}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200

@status_methods.route('/api/v1/OneAuth/addHistory', methods=['POST'])
def addHistory_oneAuth_v1():
    try:
        token_header = request.headers['Authorization']
    except KeyError as ex:
        return redirect(url_paperless)
    dataJson = request.json
    if 'pdfData' in dataJson and 'historyData' in dataJson and len(dataJson) == 2:
        pdfData = dataJson['pdfData']
        historyData = dataJson['historyData']
        if len(historyData) != 0:
            result_addHistory = addHistory_pdf_v1(pdfData,historyData,token_header)
            if result_addHistory['result'] == 'OK':
                return jsonify({'result':'OK','messageText':[result_addHistory['msg']],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':[result_addHistory['msg']]}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'historyData incorrect'}),200
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404

@status_methods.route('/api/v1/OneAuth/checkSign', methods=['GET'])
def OneAuth_checkSign_v1():
    try:
        token_header = request.headers['Authorization']
    except KeyError as ex:
        return redirect(url_paperless)
    res_list = credentials_list_v3("","","","","",token_header)
    if res_list['result'] == 'OK':
        data_msg = res_list['msg']
        try:
            totalResult_oneAuth = data_msg['totalResult']
            if totalResult_oneAuth == 0:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'sign profile not found','err_Code':'ER200'}),200
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':None}),200
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list service error! ' + str(e)}),200
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list service error!','err_Code':'ER500'}),200

@status_methods.route('/api/v1/OneAuth/pdf/validateDocument', methods=['POST'])
def read_pdf_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{"data":None,"message":ex}}),200
        dataJson = request.json
        if 'pdfData' in dataJson and len(dataJson) == 1:
            pdfData = dataJson['pdfData']
            result_pdfData = get_pdfData_v1(pdfData,token_header)
            if result_pdfData['result'] == 'OK':
                return jsonify({'result':'OK','massageText':{"data":result_pdfData['msg'],"message":"success"},"status_Code":200,"messageER":None})
            else:
                return jsonify({'result':'ER','massageText':None,"status_Code":200,"messageER":{"data":None,"message":"fail " + result_pdfData['msg']}})
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'data':None,'message':'parameter incorrect','code':'EROA999'}}),404

@status_methods.route('/api/v1/OneAuth/pdf/addAttachment', methods=['POST'])
def addAttachment_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{"data":None,"message":ex}}),200
        try:
            dataForm = request.form
            dataFile = request.files
            if 'pdfData' in dataForm and 'description' in dataForm:
                pdfData = dataForm['pdfData']
                description = dataForm['description']
                files = request.files.getlist("file[]")
                count = 0
                one_access_token = None
                eval_description = eval(str(description))
                len_eval_description = len(eval_description)

                if (len_eval_description) == len(files):
                    list_attachItem = []
                    
                    for file in files:
                        file_string = (base64.b64encode(file.read())).decode()                    
                        result_description = eval_description[count]["description"]
                        count = count + 1
                        tmp_json = {}
                        tmp_json['attachmentName'] = file.filename
                        tmp_json['attachmentContent'] = file_string
                        tmp_json['attachmentDescription'] = result_description
                        list_attachItem.append(tmp_json)
                    result = doc_addAttachment_v1(pdfData,count,list_attachItem,token_header)
                    if result['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':{'data':result['msg'],'mesage':'success'},'status_Code':200,'messageER':None}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'mesage':'fail ' + result['msg']}}),200
                else:
                    return jsonify({'result':'ER','messageText': None,'status_Code':200,'messageER':{'data':None,'message': 'fail description != files'}}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'data':None,'message':'parameter incorrect','code':'EROA999'}}),404
        except Exception as ex:
            return jsonify({'result':'ER','messageText': None,'status_Code':200,'messageER':{'data':None,'message': str(ex)}}),200

@status_methods.route('/api/v1/OneAuth/pdf/signatureJson', methods=['POST'])
def signatureJson_api_v1():
    try:
        try:
            res_arraylist = []
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{"data":None,"message":ex}}),200
        dataJson = request.json
        if 'sidcode' in dataJson and 'max_Step' in dataJson and 'Step_Num' in dataJson and 'base64_string' in dataJson and 'sign_string' in dataJson and 'sign_position' in dataJson and len(dataJson) == 6:
            sign_position = dataJson['sign_position']
            if 'sign_llx' in sign_position and 'sign_lly' in sign_position and 'sign_page' in sign_position and 'sign_urx' in sign_position and 'sign_ury' in sign_position and 'max_page' in sign_position and len(sign_position) == 6:
                tmp_sidcode = dataJson['sidcode']
                tmp_max_Step = dataJson['max_Step']
                tmp_Step_Num = dataJson['Step_Num']
                tmp_base64_string = dataJson['base64_string']
                tmp_sign_string = dataJson['sign_string']
                tmp_sign_position = dataJson['sign_position']
                return jsonify(tmp_sign_position)
    except Exception as e:
        pass

@status_methods.route('/api/v1/OneAuth/signaturejson', methods=['POST'])
def signaturejson_api_v1():

    # info = {
    #     'document_id':'POS-63000000002',
    #     'tracking':'XFC6665638VQA',
    #     'webhook': myUrl_domain+'webhook/v1?id=',
    #     'jws':'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZG9jdW1lbnRfdHlwZSI6IlBPUyIsImRvY3VtZW50aWQiOiJQT1MtNjMwMDAwMDAwMDIiLCJ0cmFja2luZyI6IlhGQzY2NjU2MzhWUUEiLCJpYXQiOjE1MTYyMzkwMjJ9.NkQjKhdohdWo4T0Rt5RcaOHZIVvKdCMlrFM6BLdSF7kbughGWV1XbTbFJFPhysN4xcWyAw2niI9nCXNa37VXt4yMD96gl_TvUpvc_FpB2RlbyqJWTW_Et6lR06l-IC1ePrCnvUdyBw7H_htIQW43yt7BgObiOSJmG-MiEq_0vPeJm2o3jbQvUUUw6EoWeixY9Uv51GZ1ggiqZGruC-Tvr-xvSqeQoszrS3e1NriKv9CeOpOa_COuC4usD4o-4Nvrx1cqcLpF6UGxvlL9VdFzVqOeY4S-CaQGQLa4h6MnYQec8KFdUPd0qSIM3SzUjs5bocoLsDqgxbFPXm6iFArCFw',
    #     "visibleSignaturePage": 1,
    #     "visibleSignatureRectangle": "",
    #     "visibleSignatureImagePath": ""
    # }
    try:
        res_arraylist = []
        token_header = request.headers['Authorization']
    except KeyError as ex:
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{"data":None,"message":ex}}),200
    res_list = credentials_list_v2("","","","","",token_header)
    if res_list['result'] == 'OK':
        res_arraylist.append({'result_listService':res_list})
        credentialId = res_list['msg']['credentials'][0]['credentialId']
        res_authorize = credentials_authorize_v2(credentialId,"","","","","","","",token_header)
        if res_authorize['result'] == 'OK':
            tmp_sad = res_authorize['msg']['sad']
    info = {
        "sadData": tmp_sad,
        "cadData": "",
        "documentId": "POS-63000000002",
        "bcResponseURL": myUrl_domain+'webhook/v1?id=',
        "signatureContent": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZG9jdW1lbnRfdHlwZSI6IlBPUyIsImRvY3VtZW50aWQiOiJQT1MtNjMwMDAwMDAwMDIiLCJ0cmFja2luZyI6IlhGQzY2NjU2MzhWUUEiLCJpYXQiOjE1MTYyMzkwMjJ9.NkQjKhdohdWo4T0Rt5RcaOHZIVvKdCMlrFM6BLdSF7kbughGWV1XbTbFJFPhysN4xcWyAw2niI9nCXNa37VXt4yMD96gl_TvUpvc_FpB2RlbyqJWTW_Et6lR06l-IC1ePrCnvUdyBw7H_htIQW43yt7BgObiOSJmG-MiEq_0vPeJm2o3jbQvUUUw6EoWeixY9Uv51GZ1ggiqZGruC-Tvr-xvSqeQoszrS3e1NriKv9CeOpOa_COuC4usD4o-4Nvrx1cqcLpF6UGxvlL9VdFzVqOeY4S-CaQGQLa4h6MnYQec8KFdUPd0qSIM3SzUjs5bocoLsDqgxbFPXm6iFArCFw",
        "signatureAppearance": {
            "reason": "",
            "location": "",
            "certifyLevel": "",
            "hashAlgorithm": "",
            "overwriteOriginal": True,
            "visibleSignature": "",
            "visibleSignaturePage": 1,
            "visibleSignatureRectangle": '' + '0.037' + ',' + '0.032' + ',' +'0.12' + ',' + '0.06' + '',
            "visibleSignatureImagePath": "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"
        }
    }
    signatureJson_api_auth_v1(info,token_header)
    # print(info)
    return jsonify(res_arraylist)

@status_methods.route('/api/v1/OneAuth/jsonPdfSigning', methods=['POST'])
def jsonPdfSigning_api_v1():
    dataJson = request.json
    if 'pdfData' in dataJson:
        tmppdfData = dataJson['pdfData']
    try:
        res_arraylist = []
        token_header = request.headers['Authorization']
    except KeyError as ex:
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{"data":None,"message":ex}}),200
    res_list = credentials_list_v2("","","","","",token_header)
    if res_list['result'] == 'OK':
        res_arraylist.append({'result_listService':res_list})
        credentialId = res_list['msg']['credentials'][0]['credentialId']
        res_authorize = credentials_authorize_v2(credentialId,"","","","","","","",token_header)
        if res_authorize['result'] == 'OK':
            tmp_sad = res_authorize['msg']['sad']
    info = {
        "sadData": tmp_sad,
        "cadData": "",
        "documentId": "POS-63000000002",
        "bcResponseURL": myUrl_domain+'webhook/v1?id=',
        "signatureContent": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZG9jdW1lbnRfdHlwZSI6IlBPUyIsImRvY3VtZW50aWQiOiJQT1MtNjMwMDAwMDAwMDIiLCJ0cmFja2luZyI6IlhGQzY2NjU2MzhWUUEiLCJpYXQiOjE1MTYyMzkwMjJ9.NkQjKhdohdWo4T0Rt5RcaOHZIVvKdCMlrFM6BLdSF7kbughGWV1XbTbFJFPhysN4xcWyAw2niI9nCXNa37VXt4yMD96gl_TvUpvc_FpB2RlbyqJWTW_Et6lR06l-IC1ePrCnvUdyBw7H_htIQW43yt7BgObiOSJmG-MiEq_0vPeJm2o3jbQvUUUw6EoWeixY9Uv51GZ1ggiqZGruC-Tvr-xvSqeQoszrS3e1NriKv9CeOpOa_COuC4usD4o-4Nvrx1cqcLpF6UGxvlL9VdFzVqOeY4S-CaQGQLa4h6MnYQec8KFdUPd0qSIM3SzUjs5bocoLsDqgxbFPXm6iFArCFw",
        "signatureAppearance": {
            "reason": "",
            "location": "",
            "certifyLevel": "",
            "hashAlgorithm": "",
            "overwriteOriginal": True,
            "visibleSignature": "",
            "visibleSignaturePage": 1,
            "visibleSignatureRectangle": '' + '0.179' + ',' + '0.754' + ',' +'0.13' + ',' + '0.06' + '',
            "visibleSignatureImagePath": "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"
        },
        "signatureList": [],
        "pdfData": tmppdfData
    }
    result = signaturePDFJson_api_auth_v1(info,token_header)
    return jsonify(result)

@status_methods.route('/api/v1/OneAuth/checkDocumentStatus', methods=['POST'])
def checkDocumentStatus_api_v1():
    dataJson = request.json
    if 'pdfData' in dataJson and 'documentId' in dataJson and len(dataJson) == 2:
        tmppdfData = dataJson['pdfData']
        tmpdocumentId = dataJson['documentId']
        res_arraylist = []
        maxPages = 0
        message = "nonnoti"
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            abort(401)
        result_data = token_required_func(token_header)
        if result_data == 'ER':
            abort(401)
        info = {
            "documentId": tmpdocumentId,
            "pdfData": tmppdfData
        }
        rGetMaxpage = get_maxpages_pdf(tmppdfData)    
        if rGetMaxpage[0] == 200:
            maxPages = rGetMaxpage[1]
            message = rGetMaxpage[2]
        resultcall_api = checkDocumentStatus_v1(info,token_header)
        if resultcall_api['result'] == 'OK':
            if 'msg' in resultcall_api:
                if 'responseCode' in resultcall_api['msg']:
                    if resultcall_api['msg']['responseCode'] == 200:
                        return jsonify({'result':'OK','messageText':{'message':'success','data':resultcall_api['msg'],'pages':maxPages,'pages_message':message},'messageER':None,'status_Code':200}),200
        return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail','data':resultcall_api['msg'],'pages':maxPages,'pages_message':message},'status_Code':200}),200

@status_methods.route('/api/v1/OneAuth/listsign', methods=['GET'])
def listsign_api_v1():
    tmpemail = request.args.get('email')
    if tmpemail == None:
        abort(404)
    try:
        token_header = request.headers['Authorization']
        token_header = str(token_header).split(' ')[1]
    except KeyError as ex:
        abort(401)
    result_data = token_required_func(token_header)
    if result_data['result'] == 'ER':
        abort(401)
    if result_data['email'] != tmpemail:
        abort(401)
    tmptoken = 'Bearer ' + result_data['token']
    try:
        res_list = credentials_list_v2("","","","","",tmptoken)
        if res_list['result'] == 'OK':
            tmpmessageData = res_list['msg']
            return jsonify({'status':'success','message':'get data success','data':tmpmessageData}),200
    except Exception as e:
        return jsonify({'status':'fail','message':'/api/v1/OneAuth/listsign => ' + str(e),'data':None}),200

@status_methods.route('/api/v1/set/sign_auth', methods=['POST'])
def set_sign_from_oneauth_v1():
    if request.method == 'POST':
        type_sign ="set"
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return redirect(url_paperless)
        type_sign = str(type_sign).lower().replace(' ','')
        res_list = credentials_list_v2("","","","","",token_header)
        if res_list['result'] == 'OK':
            data_msg = res_list['msg']
            try:
                totalResult_oneAuth = data_msg['totalResult']
                if totalResult_oneAuth == 0:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'sign profile not found'}),200
                else:
                    credentialId = res_list['msg']['credentials'][0]['credentialId']
            except Exception as e:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + str(e)}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error'}),200
        dataJson = request.json
        if 'sign_imgData' in dataJson and len(dataJson) == 1:
            sign_imgData_base64 = dataJson['sign_imgData']
            result_oneAuth_get_sign = oneAuth_get_set_sign_v2(token_header,type_sign,credentialId,sign_imgData_base64)
            if result_oneAuth_get_sign['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'upload img to ca succuess','status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'set_sign service error'}),200
        elif 'sign_imgData' in dataJson and 'credenId' in dataJson and len(dataJson) == 2:
            sign_imgData_base64 = dataJson['sign_imgData']
            tmpcredentialId = dataJson['credenId']
            result_oneAuth_get_sign = oneAuth_get_set_sign_v2(token_header,type_sign,tmpcredentialId,sign_imgData_base64)
            if result_oneAuth_get_sign['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'upload img to CA succuess','status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'set_sign service error'}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200

@status_methods.route('/api/v1/get/sign_auth', methods=['GET'])
def get_sign_from_oneauth_v1():
    tmparr_resp = []
    try:
        token_header = request.headers['Authorization']
    except KeyError as ex:
        return redirect(url_paperless)
    tmpcredenId = request.args.get('credenId')
    if tmpcredenId == None:        
        res_list = credentials_list_v2("","","","","",token_header)
        if res_list['result'] == 'OK':
            data_msg = res_list['msg']
            try:
                totalResult_oneAuth = data_msg['totalResult']
                if totalResult_oneAuth == 0:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'sign profile not found'}),200
                else:
                    credentialId = res_list['msg']['credentials'][0]['credentialId']
                    pass
            except Exception as e:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + str(e)}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list service fail !'}),200
        result_oneAuth_get_sign = oneAuth_get_set_sign_v2(token_header,"get",credentialId,"")
        if result_oneAuth_get_sign['result'] == 'OK':
            responseMessage_msg = result_oneAuth_get_sign['msg']
            if responseMessage_msg['responseMessage'] == 'success':
                imageData_oneauth = responseMessage_msg['imageData']
                return jsonify({'result':'OK','messageText':[{'imageData':imageData_oneauth}],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'sign not found'}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'service get sign err'}),200
    else:
        tmpcredenId = str(tmpcredenId)
        try:
            tmpcredenId = eval(tmpcredenId)
        except Exception as e:
            tmpcredenId = str(tmpcredenId)
        if type(tmpcredenId) is str or type(tmpcredenId) is int:
            result_oneAuth_get_sign = oneAuth_get_set_sign_v2(token_header,"get",tmpcredenId,"")
            if result_oneAuth_get_sign['result'] == 'OK':
                responseMessage_msg = result_oneAuth_get_sign['msg']
                if responseMessage_msg['responseMessage'] == 'success':
                    imageData_oneauth = responseMessage_msg['imageData']
                    info = {
                        'imageData':imageData_oneauth,
                        'credentialId':str(tmpcredenId)
                    }
                    tmparr_resp.append(info)
                    return jsonify({'result':'OK','messageText':tmparr_resp,'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'sign not found'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'service get sign err'}),200
        elif type(tmpcredenId) is list:
            for z in tmpcredenId:
                result_oneAuth_get_sign = oneAuth_get_set_sign_v2(token_header,"get",z,"")
                if result_oneAuth_get_sign['result'] == 'OK':
                    responseMessage_msg = result_oneAuth_get_sign['msg']
                    if responseMessage_msg['responseMessage'] == 'success':
                        imageData_oneauth = responseMessage_msg['imageData']
                        info = {
                            'imageData':imageData_oneauth,
                            'credentialId':z
                        }
                        tmparr_resp.append(info)
                    else:
                        info = {
                            'imageData':None,
                            'credentialId':z
                        }
                        tmparr_resp.append(info)
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'service get sign err'}),200
            return jsonify({'result':'OK','messageText':tmparr_resp,'status_Code':200,'messageER':None}),200


