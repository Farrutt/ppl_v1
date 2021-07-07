#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.qrcode import *
from method.verify import *
from method.callserver import *
from controller.mail_string import *
from controller.validate import *
from db.db_method import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from method.pdf import *
from api.onebox import *
from method.cal_file import *

if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less


def createImage_formPDF(sidCode):
    # path = './storage/pdf/'
    # path_image = './storage/image/'
    path = path_global_1 + '/storage/pdf/'
    path_image = path_global_1 + '/storage/image/'
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path_image):
        os.makedirs(path_image)
    result = select().select_pdfstring_sidCode(sidCode)
    if result['result'] == 'OK':
        base64_pdfFile = result['messageText']['PDF_Base64']
        try:
            unique_filename = str(uuid.uuid4())
            with open(path + unique_filename +".pdf","wb") as f:
                f.write(base64.b64decode((base64_pdfFile)))
        except Exception as e:
            print(str(e))
        namefile = uuid.uuid4().hex
        pathFilePDF = path + unique_filename +".pdf"
        pages = convert_from_path(pathFilePDF, dpi=200,last_page=1, first_page =0,output_folder=path_image,fmt='jpeg',output_file=str(namefile))
        print(pages[0].filename)
        nameforreturn = str(pages[0].filename).split('/')[-1]
        return (nameforreturn)

def createImage_formPDF2(sidCode):
    # path = './storage/pdf/'
    # path_image = './storage/image/'
    path = path_global_1 + '/storage/pdf/'
    path_image = path_global_1 + '/storage/image/'
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path_image):
        os.makedirs(path_image)
    result = select().select_pdfstring_sidCode(sidCode)
    if result['result'] == 'OK':
        base64_pdfFile = result['messageText']['PDF_Base64']
        try:
            unique_filename = str(uuid.uuid4())
            with open(path + unique_filename +".pdf","wb") as f:
                f.write(base64.b64decode((base64_pdfFile)))
        except Exception as e:
            print(str(e))
        namefile = uuid.uuid4().hex
        pathFilePDF = path + unique_filename +".pdf"
        pages = convert_from_path(pathFilePDF, dpi=200,last_page=1, first_page =0,output_folder=path_image,fmt='jpeg',output_file=str(namefile))
        # print(pages[0].filename)
        nameforreturn = str(pages[0].filename).split('/')[-1]
        return {'result':'OK','data':(nameforreturn)}
    else:
        return {'result':'ER'}

def convert_pdf_images_group(foldername,base64_pdfFile):
    # base64_pdfFile = (base64)
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
            f.write(base64.b64decode(base64_pdfFile))
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
                return ({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(ex)})
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
                return ({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(ex)})

@status_methods.route('/api/v2/html_topdf',methods=['POST'])
def html_topdf_api_v2():
    dataJson = request.json
    if 'html_text' in dataJson and 'landscape' in dataJson and len(dataJson) == 2:
        tmp_html_text = dataJson['html_text']
        tmp_landscape = dataJson['landscape']
        unique_foldername = str(uuid.uuid4())
        html_name = str(uuid.uuid4())
        html_name_file = html_name + '.html'
        path = './temp/' + unique_foldername +'/'
        path_indb = '/temp/' + unique_foldername + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        path_save = path  + html_name_file
        path_save_01 = path_indb  + html_name_file
        with open(path_save ,"w",encoding='utf-8') as f:
            f.write(tmp_html_text)
        html_file = open(path_save,"rb")
        # print(path_save)
        files = {
            'file':html_file
        }
        payload = {
            'landscape':tmp_landscape
        }
        # convert_eform = 'https://eform.one.th/webservice'
        response = requests.request("POST", convert_eform+"/api/v4/convert_html_to_pdf", data = payload, files = files, verify = False)
        if response.status_code == 200 or response.status_code == 201:
            tmpjson = response.json()
            if tmpjson['result'] == 'OK':
                if 'message' in tmpjson:
                    tmpmessage = tmpjson['message']
                    tmp_pdfdata = tmpmessage['pdfData']
                    cwd = os.getcwd()
                    # os.remove(cwd + path_save_01)
                    return jsonify({'result':'OK','messageText':{'data':tmp_pdfdata,'message':'success'},'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'fail','code':'ERCV001'},'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'fail','code':'ERCV002'},'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'fail','code':'ERCV999'},'status_Code':200}),200
    else:
        return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'parameter incorrect','code':'ERCV999'},'status_Code':404}),404



@status_methods.route('/download/v1/<string:user_Name>/pdf/<string:sidCode>/<string:key>',methods=['GET'])
def getdownloadpdf_v1(user_Name,sidCode,key):
    try:
        resultSelect = select().select_pdfdownload_v1(sidCode,key)
        if resultSelect['result'] == 'OK':
            unique_filename = str(uuid.uuid4())
            pathwatermark_ = make_watermarker(user_Name)
            resultmerge = mergepdf(1,resultSelect['messageText'],pathwatermark_,user_Name)
            response = make_response(base64.b64decode(resultSelect['messageText']))
            response.headers.set('Content-Type', 'application/pdf')
            response.headers.set(
                'Content-Disposition', 'as_attachment=True', filename='%s.pdf' % unique_filename)
            return response
        else:
            return 'not found pdf'
    except Exception as ex:
        return jsonify({'result':'ER','messageText':str(ex)})

@status_methods.route('/download/base/v1/<string:user_Name>/pdf/<string:sidCode>/<string:key>',methods=['GET'])
@token_required_v3
def getdownloadpdf_v1_base(user_Name,sidCode,key):
    try:
        resultSelect = select().select_pdfdownload_v1(sidCode,key)
        if resultSelect['result'] == 'OK':
            unique_filename = str(uuid.uuid4())
            url_download_file = myUrl_domain + 'api/v1/download/pdf/sign_pdf?sidCode=' + sidCode
            print(url_download_file)
            # pathwatermark_ = make_watermarker(user_Name)
            # try:
            #     resultmerge = mergepdf(1,resultSelect['messageText'],pathwatermark_,user_Name)
            # except Exception as e:
            #     resultmerge = {}
            #     resultmerge['messageText'] = {}
            #     resultmerge['messageText']['responsePdf'] = resultSelect['messageText']
            # response = make_response(base64.b64decode(resultmerge['messageText']['responsePdf']))
            # response.headers.set('Content-Type', 'application/pdf')
            # response.headers.set(
            #     'Content-Disposition', 'as_attachment=True', filename='%s.pdf' % unique_filename)
            # return jsonify({'result':'OK','messageText':{'PDF_Base64_watermake':resultmerge['messageText']['responsePdf'],'PDF_Base64':resultSelect['messageText']},'status_Code':200}),200
            return jsonify({'result':'OK','messageText':{'PDF_Base64_watermake':None,'PDF_Base64':resultSelect['messageText'],'url_download':url_download_file},'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':{'PDF_Base64':None},'status_Code':200}),200
    except Exception as ex:
        return jsonify({'result':'ER','messageText':str(ex),'status_Code':200})

@status_methods.route('/download/v1/<string:user_Name>',methods=['POST'])
def getdownload_v2(user_Name):
    dataJson = request.json
    if 'sidCode' in dataJson:
        tmp_sidCode = dataJson['sidCode']
        tmpkeygen = []
        for x in range(len(tmp_sidCode)):
            sidCodeText = tmp_sidCode[x]
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
            result_data = token_required_func(token_header)
            if result_data['result'] == 'ER':
                abort(401)
            tmp_username = result_data['username']
            tmpemail = result_data['email']
            thai_email = tmpemail
            username = tmp_username
            list_Info = []
            if user_Name == tmp_username:
                resultSelectDownloadLog = select().select_downloadLog_v1(sidCodeText)
                count = 1
                if resultSelectDownloadLog['result'] == 'OK':
                    if 'json_information' in resultSelectDownloadLog['messageText']:
                        try:
                            json_data = eval(str(resultSelectDownloadLog['messageText']['json_information']))
                        except Exception as ex:
                            return jsonify({'result':'ER','messageText':str(ex),'status_Code':200}),200
                        ts = int(time.time())
                        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
                        for i in range(len(json_data)):
                            list_Info.append(json_data[i])
                            count = count + 1
                        jsonInfo = {'userName':tmp_username,'dateDownload':str(st)}
                        list_Info.append(jsonInfo)
                    resultUpdate = update().update_LoadLog(sidCodeText,list_Info,count)
                    if resultUpdate['result'] == 'OK':
                        resultBase64 = select().select_pdfFordownload_v1(sidCodeText)
                        unique_filename = str(uuid.uuid4())
                        tmpkeygen.append(resultSelectDownloadLog['messageText']['keygen'])
                        # return jsonify({'result':'OK','messageText':{'status':'update ok','keygen':resultSelectDownloadLog['messageText']['keygen']},'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':resultUpdate['messageText'],'status_Code':200}),200
                else:
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
                    jsonInformation = [{'userName':tmp_username,'dateDownload':str(st)}]
                    resultInsert = insert().insert_downloadLogFile(sidCodeText,str(jsonInformation))
                    if resultInsert['result'] == 'OK':
                        resultBase64 = select().select_pdfFordownload_v1(sidCodeText)
                        tmpkeygen.append(resultInsert['messageText'])
                        # return jsonify({'result':'OK','messageText':{'status':'insert ok','keygen':resultInsert['messageText']},'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':'insert fail!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
        return jsonify({'result':'OK','messageText':{'status':'update ok','keygen':tmpkeygen},'status_Code':200}),200

@status_methods.route('/download/base/v1/<string:user_Name>/pdf',methods=['POST'])
def getdownloadpdf_v2_base_muti(user_Name):
    dataJson = request.json
    pdfBase64 = []
    urlDownloadfile =[]
    if 'sidCode' in dataJson and 'key' in dataJson:
        tmpsidCode = dataJson['sidCode']
        tmpkey = dataJson['key']
        for x in range(len(tmpsidCode)):
            sidCode = tmpsidCode[x]
            key = tmpkey[x]
            try:
                resultSelect = select().select_pdfdownload_v1(sidCode,key)
                if resultSelect['result'] == 'OK':
                    unique_filename = str(uuid.uuid4())
                    url_download_file = myUrl_domain + 'api/v1/download/pdf/sign_pdf?sidCode=' + sidCode
                    # print(url_download_file)
                    urlDownloadfile.append(url_download_file)
                    pdfBase64.append(resultSelect['messageText'])
                else:
                    return jsonify({'result':'ER','messageText':{'PDF_Base64':None},'status_Code':200}),200
            except Exception as ex:
                return jsonify({'result':'ER','messageText':str(ex),'status_Code':200})
        return jsonify({'result':'OK','messageText':{'PDF_Base64_watermake':None,'PDF_Base64':pdfBase64,'url_download':urlDownloadfile},'status_Code':200}),200

@status_methods.route('/download/v1/<string:user_Name>/<string:sidCode>',methods=['GET'])
def getdownload_v1(user_Name,sidCode):
    try:
        token_header = request.headers['Authorization']
        try:
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
        result_data = token_required_func(token_header)
        if result_data['result'] == 'ER':
            abort(401)
        tmp_username = result_data['username']
        tmpemail = result_data['email']
        # url = one_url + "/api/account_and_biz_detail"
        # headers = {
        #     'Content-Type': "application/json",
        #     'Authorization': "Bearer"+" "+token_header
        # }
        # try:
        #     response = requests.get(url, headers=headers, verify=False)
        #     response = response.json()
        # except requests.Timeout as ex:
        #     return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        # except requests.HTTPError as ex:
        #     return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        # except requests.ConnectionError as ex:
        #     return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        # except requests.RequestException as ex:
        #     return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        # except Exception as ex:
        #     return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        # print(response)
        # if 'result' in response:
        #     if response['result'] == 'Fail':
        #         return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
        # else:
        thai_email = tmpemail
        username = tmp_username
        list_Info = []
        sidCodeText = sidCode
        if user_Name == username:
            resultSelectDownloadLog = select().select_downloadLog_v1(sidCodeText)
            count = 1
            if resultSelectDownloadLog['result'] == 'OK':
                if 'json_information' in resultSelectDownloadLog['messageText']:
                    try:
                        json_data = eval(str(resultSelectDownloadLog['messageText']['json_information']))
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':str(ex),'status_Code':200}),200
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
                    for i in range(len(json_data)):
                        list_Info.append(json_data[i])
                        count = count + 1
                    jsonInfo = {'userName':username,'dateDownload':str(st)}
                    list_Info.append(jsonInfo)
                resultUpdate = update().update_LoadLog(sidCodeText,list_Info,count)
                if resultUpdate['result'] == 'OK':
                    resultBase64 = select().select_pdfFordownload_v1(sidCodeText)
                    unique_filename = str(uuid.uuid4())

                    return jsonify({'result':'OK','messageText':{'status':'update ok','keygen':resultSelectDownloadLog['messageText']['keygen']},'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':resultUpdate['messageText'],'status_Code':200}),200
            else:
                ts = int(time.time())
                st = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
                jsonInformation = [{'userName':username,'dateDownload':str(st)}]
                resultInsert = insert().insert_downloadLogFile(sidCodeText,str(jsonInformation))
                if resultInsert['result'] == 'OK':
                    resultBase64 = select().select_pdfFordownload_v1(sidCodeText)
                    return jsonify({'result':'OK','messageText':{'status':'insert ok','keygen':resultInsert['messageText']},'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':'insert fail!','status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
    except Exception as ex:
        return 'Authorization not found'

@status_methods.route('/download/file/v1',methods=['POST'])
@token_required
def getfile_download_pdf():
    dataJson = request.json
    if 'base_String' in dataJson:
        base64_pdfFile = dataJson['base_String']
        unique_filename = str(uuid.uuid4())
        return send_file(
            io.BytesIO(base64.b64decode(base64_pdfFile)),
            mimetype='application/pdf',
            as_attachment=True,
            attachment_filename='%s.pdf' % unique_filename)

@status_methods.route('/qrcode/v1/<string:user_Name>/qr/<string:sidCode>/<string:key>',methods=['GET'])
def getdownloadpdfqr_v1(user_Name,sidCode,key):
    try:
        resultSelect_base64 = select().select_pdfdownloadqr_v1(sidCode,key)
        if resultSelect_base64['result'] == 'OK':
            unique_filename = str(uuid.uuid4())
            resultSelect = select().select_forqrCodeBase64(sidCode)
            if resultSelect['result'] == 'OK':
                if len(resultSelect['messageText']['qrCode_position']) != 0:
                    resultSelect_Tracking = resultSelect['messageText']['TrackingId']
                    qr_llx = float(resultSelect['messageText']['qrCode_position']['qr_llx'])
                    qr_lly = float(resultSelect['messageText']['qrCode_position']['qr_lly'])
                    qr_urx = float(resultSelect['messageText']['qrCode_position']['qr_urx'])
                    qr_ury = float(resultSelect['messageText']['qrCode_position']['qr_ury'])
                    qr_page = int(resultSelect['messageText']['qrCode_position']['qr_page'])
                    base64PDF = resultSelect_base64['messageText']
                    urlString = url_paperless + 'viewpdf?document=' +resultSelect_Tracking
                    qrcode_base64 = genarateQrcode(urlString)
                    resultpng = genPdf_Topng_qr(qr_urx,qr_ury,qr_llx,qr_lly,qrcode_base64)
                    if resultpng['result'] == 'OK':
                        path_pdf_qr = resultpng['messageText']
                        resultMerge = merge_png_to_pdf_qrCode(qr_page,base64PDF,path_pdf_qr)
                        if resultMerge['result'] == 'OK':
                            pathwatermark_ = make_watermarker(user_Name)
                            resultmerge_ = mergepdf(1,resultMerge['messageText']['responsePdf'],pathwatermark_,user_Name)
                            response = make_response(base64.b64decode(resultmerge_['messageText']['responsePdf']))
                            response.headers.set('Content-Type', 'application/pdf')
                            response.headers.set(
                                'Content-Disposition', 'as_attachment=True', filename='%s.pdf' % unique_filename)
                            return response
                        else:
                            return redirect(url_paperless + "notfound", code=302)
                else:
                    return redirect(url_paperless + "notfound", code=302)
        else:
            return redirect(url_paperless + "notfound", code=302)

    except Exception as ex:
        return jsonify({'result':'ER','messageText':str(ex)})

@status_methods.route('/qrcode/base/v1/<string:user_Name>/qr/<string:sidCode>/<string:key>',methods=['GET'])
def getdownloadpdfqr_v1_base(user_Name,sidCode,key):
    try:
        resultSelect_base64 = select().select_pdfdownloadqr_v1(sidCode,key)
        if resultSelect_base64['result'] == 'OK':
            unique_filename = str(uuid.uuid4())
            resultSelect = select().select_forqrCodeBase64(sidCode)
            if resultSelect['result'] == 'OK':
                if len(resultSelect['messageText']['qrCode_position']) != 0:
                    resultSelect_Tracking = resultSelect['messageText']['TrackingId']
                    qr_llx = float(resultSelect['messageText']['qrCode_position']['qr_llx'])
                    qr_lly = float(resultSelect['messageText']['qrCode_position']['qr_lly'])
                    qr_urx = float(resultSelect['messageText']['qrCode_position']['qr_urx'])
                    qr_ury = float(resultSelect['messageText']['qrCode_position']['qr_ury'])
                    qr_page = int(resultSelect['messageText']['qrCode_position']['qr_page'])
                    base64PDF = resultSelect_base64['messageText']
                    urlString = url_paperless + 'viewpdf?document=' +resultSelect_Tracking
                    qrcode_base64 = genarateQrcode(urlString)
                    resultpng = genPdf_Topng_qr(qr_urx,qr_ury,qr_llx,qr_lly,qrcode_base64)
                    if resultpng['result'] == 'OK':
                        path_pdf_qr = resultpng['messageText']
                        resultMerge = merge_png_to_pdf_qrCode(qr_page,base64PDF,path_pdf_qr)
                        if resultMerge['result'] == 'OK':
                            pathwatermark_ = make_watermarker(user_Name)
                            resultmerge_ = mergepdf(1,resultMerge['messageText']['responsePdf'],pathwatermark_,user_Name)
                            response = make_response(base64.b64decode(resultmerge_['messageText']['responsePdf']))
                            response.headers.set('Content-Type', 'application/pdf')
                            response.headers.set(
                                'Content-Disposition', 'as_attachment=True', filename='%s.pdf' % unique_filename)
                            return jsonify({'result':'OK','messageText':{'PDF_Base64_watermake':resultmerge_['messageText']['responsePdf'],'PDF_Base64':resultMerge['messageText']['responsePdf']},'status_Code':200}),200
                        else:
                            return jsonify({'result':'ER','messageText':{'PDF_Base64':None},'status_Code':200}),200
                else:
                    return redirect(url_paperless + "notfound", code=302)
        else:
            return redirect(url_paperless + "notfound", code=302)

    except Exception as ex:
        return jsonify({'result':'ER','messageText':str(ex)})

@status_methods.route('/qrcode/v1/<string:user_Name>/<string:sidCode>',methods=['GET'])
def getqrCodedownload_v1(user_Name,sidCode):
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
            thai_email = response['thai_email']
            username = response['username']
            list_Info = []
            sidCodeText = sidCode
            if user_Name == username:
                resultSelectDownloadLogQr = select().select_downloadLogQrCode_v1(sidCodeText)
                count = 1
                if resultSelectDownloadLogQr['result'] == 'OK':
                    if 'json_information' in resultSelectDownloadLogQr['messageText']:
                        try:
                            json_data = eval(str(resultSelectDownloadLogQr['messageText']['json_information']))
                        except Exception as ex:
                            return jsonify({'result':'ER','messageText':str(ex),'status_Code':200}),200
                        ts = int(time.time())
                        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
                        for i in range(len(json_data)):
                            list_Info.append(json_data[i])
                            count = count + 1
                        jsonInfo = {'userName':username,'dateDownload':str(st)}
                        list_Info.append(jsonInfo)
                    resultUpdate = update().update_LoadLogQrCode(sidCodeText,list_Info,count)
                    if resultUpdate['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':{'status':'update ok','keygen':resultUpdate['keygen']},'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':{'status':'update err','keygen':None},'status_Code':200}),200
                else:
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
                    jsonInformation = [{'userName':username,'dateDownload':str(st)}]
                    resultInsert = insert().insert_downloadLogQrCodeFile(sidCodeText,str(jsonInformation))
                    if resultInsert['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':{'status':'insert ok','keygen':resultInsert['messageText']},'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
    except Exception as ex:
        print(str(ex))

@status_methods.route('/qrcode/v1/<string:username>',methods=['POST'])
@token_required
def qrCode_onpaper_v1(username):
    if request.method == 'POST':
        dataJson = request.json
        if 'sidCode' in dataJson and len(dataJson) == 1:
            sidCode = dataJson['sidCode']
            resultSelect = select().select_forqrCodeBase64(sidCode)
            if resultSelect['result'] == 'OK':
                resultSelect_Tracking = resultSelect['messageText']['TrackingId']
                qr_llx = float(resultSelect['messageText']['qrCode_position']['qr_llx'])
                qr_lly = float(resultSelect['messageText']['qrCode_position']['qr_lly'])
                qr_urx = float(resultSelect['messageText']['qrCode_position']['qr_urx'])
                qr_ury = float(resultSelect['messageText']['qrCode_position']['qr_ury'])
                qr_page = int(resultSelect['messageText']['qrCode_position']['qr_page'])
                base64PDF = resultSelect['messageText']['base64PDF']
                urlString = url_paperless + 'viewpdf?document=' +resultSelect_Tracking
                qrcode_base64 = genarateQrcode(urlString)
                resultpng = genPdf_Topng_qr(qr_urx,qr_ury,qr_llx,qr_lly,qrcode_base64)
                if resultpng['result'] == 'OK':
                    path_pdf_qr = resultpng['messageText']
                    pathwatermark_ = make_watermarker(resultSelect['messageText'],username)
                    resultMerge = merge_png_to_pdf_qrCode(qr_page,base64PDF,path_pdf_qr)
                    if resultMerge['result'] == 'OK':
                        resultmerge_ = mergepdf(1,resultMerge['messageText']['responsePdf'],pathwatermark_,username)

                        return jsonify({'result':'OK','messageText':resultMerge['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':resultMerge['messageText'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':resultpng['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':resultSelect['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect!'}),404

@status_methods.route('/viewforqr/v1/<string:trackingId>/<string:username_Id>',methods=['GET'])
def viewPdf_qrCode_v1(trackingId,username_Id):
    if request.method == 'GET':
        trackingId = str(trackingId).replace(' ','')
        username_Id = str(username_Id).replace(' ','')
        resultusername = select().select_username(trackingId,username_Id)
        if resultusername == True:
            stringUserName = username_Id
        else:
            stringUserName = 'Anonymous'
        result_Selccttracking = select().select_forqrpdfView_v1(trackingId)
        if result_Selccttracking['result'] == 'OK':
            sidCode = result_Selccttracking['sidCode']
            resultSelect = select().select_forqrCodeBase64(sidCode)
            if resultSelect['result'] == 'OK':
                resultSelect_Tracking = resultSelect['messageText']['TrackingId']
                qr_llx = float(resultSelect['messageText']['qrCode_position']['qr_llx'])
                qr_lly = float(resultSelect['messageText']['qrCode_position']['qr_lly'])
                qr_urx = float(resultSelect['messageText']['qrCode_position']['qr_urx'])
                qr_ury = float(resultSelect['messageText']['qrCode_position']['qr_ury'])
                qr_page = int(resultSelect['messageText']['qrCode_position']['qr_page'])
                base64PDF = resultSelect['messageText']['base64PDF']
                urlString = url_paperless + 'viewpdf?document=' +resultSelect_Tracking
                qrcode_base64 = genarateQrcode(urlString)
                # print(qrcode_base64)
                resultpng = genPdf_Topng_qr(qr_urx,qr_ury,qr_llx,qr_lly,qrcode_base64)
                if resultpng['result'] == 'OK':
                    path_pdf_qr = resultpng['messageText']
                    resultMerge = merge_png_to_pdf_qrCode(qr_page,base64PDF,path_pdf_qr)
                    if resultMerge['result'] == 'OK':
                        pathwatermark_ = make_watermarker(stringUserName)
                        resultmerge_ = mergepdf(1,resultMerge['messageText']['responsePdf'],pathwatermark_,stringUserName)
                        if resultmerge_['result'] == 'OK':
                            return jsonify({'result':'OK','messageText':{'PDFBase64':resultmerge_['messageText']['responsePdf']},'status_Code':200}),200
                        else:
                            return jsonify({'result':'ER','messageText':{'PDFBase64':resultmerge_['messageText']},'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':{'PDFBase64':resultMerge['messageText']},'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':resultpng['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':resultSelect['messageText'],'status_Code':200}),200
            if result_Selccttracking['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'PDFBase64':result_Selccttracking['messageText']},'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':{'PDFBase64':result_Selccttracking['messageText']},'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':result_Selccttracking['messageText'],'status_Code':200}),200

@status_methods.route('/api/v1/storage_filetest',methods=['POST'])
def storage_filetest():
    dataFiles = request.files
    tmplist_file = []
    if 'file[]' in dataFiles:        
        files = request.files.getlist("file[]")
        for file in files:
            file_stringread = (file.read())
            size = str(len(file_stringread))
            # size = convert_bytes_storage(size)
            info = {
                "size_file":str(size)
            }
            tmplist_file.append(info)
    return jsonify(tmplist_file)

@status_methods.route('/storage/<string:type_api>/v1',methods=['POST'])
# @token_required
def keep_storage_v1(type_api):
    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
    size = None
    tmpsum_storage = 0
    if type_api == 'keep':
        if request.method == 'POST':
            dataFiles = request.files
            dataForm = request.form
            unique_foldername = str(uuid.uuid4())
            list_file_name = []
            path = path_global_1 + '/storage/' + unique_foldername + '/'
            path_indb = '/storage/' + unique_foldername +'/'
            # path = './storage/' + unique_foldername +'/'
            # path_indb = '/storage/' + unique_foldername +'/'
            if not os.path.exists(path):
                os.makedirs(path)
            if 'file[]' in dataFiles and 'username' in dataForm:
                files = request.files.getlist("file[]")
                data_userName = dataForm['username']
                for file in files:
                    unique_filename = str(uuid.uuid4())
                    tmpread = file.read()
                    file_string = base64.b64encode(tmpread)                                    
                    file_stringread = tmpread
                    size = str(len(file_stringread))
                    tmpsum_storage += len(file_stringread)
                    typefile = str(file.filename).split('.')[-1]
                    with open(path + unique_filename + "." + typefile, "wb") as fh:
                        fh.write(base64.decodebytes(file_string))
                        list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName,'filesize':size})
                result_Insert = insert().insert_transactionfile(list_file_name,path_indb,unique_foldername,tmpsum_storage)
                if result_Insert['result'] =='OK':
                    return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':unique_foldername,'file_name':list_file_name},'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'cant insert to db','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200})
    elif type_api == 'push':
        if request.method == 'POST':
            dataFiles = request.files
            dataForm = request.form
            unique_foldername = str(uuid.uuid4())
            list_file_name = []
            if 'folder_name' in dataForm and 'username' in dataForm and 'sid' in dataForm:
                folder_name = dataForm['folder_name']
                data_userName = dataForm['username']
                tmp_sid = dataForm['sid']
                if tmp_sid != '':
                    result_select = select().select_folder_name_attm_file_v1(tmp_sid)
                else:
                    if str(folder_name).replace(' ','') != "":
                        if 'file[]' in dataFiles:
                            files = request.files.getlist("file[]")
                            resultSelect = select().select_transactionfile(folder_name)
                            if resultSelect['result'] == 'OK':
                                list_arrfile = resultSelect['messageText']['json_data']
                                pathfolderindb = resultSelect['messageText']['pathfolder']
                                for file in files:
                                    path = path_global_1 + pathfolderindb
                                    path_indb = '/storage/' + unique_foldername +'/'
                                    # path = path_global_1 + '/storage/' + folder_name +'/'
                                    # path_indb = path_global_1 + '/storage/' + folder_name +'/'
                                    unique_filename = str(uuid.uuid4())
                                    tmpread = file.read()
                                    file_string = base64.b64encode(tmpread)                                    
                                    file_stringread = tmpread
                                    size = str(len(file_stringread))
                                    typefile = str(file.filename).split('.')[-1]
                                    try:
                                        with open(path + unique_filename + "." + typefile, "wb") as fh:
                                            fh.write(base64.decodebytes(file_string))
                                            list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName,'filesize':size})
                                    except Exception as ex:
                                        logger.info(ex)
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name'}),200
                                for o in range(len(list_arrfile)):
                                    if 'filesize' in list_arrfile[o]:
                                        tmpsum_storage += int(list_arrfile[o]['filesize'])
                                    list_file_name.append(list_arrfile[o])
                                resUpdate = update().update_transactionfile(list_file_name,folder_name,tmpsum_storage)
                                if resUpdate['result'] == 'OK':
                                    return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'cant update in db'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found in db'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'please input file'}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data form not folder_name value'}),200
                if result_select['result'] == 'OK':
                    tmp_status_attmp = result_select['messageText']
                    if tmp_status_attmp == True:
                        if str(folder_name).replace(' ','') != "":
                            if 'file[]' in dataFiles:
                                files = request.files.getlist("file[]")
                                for file in files:
                                    path = path_global_1 +'/storage/' + folder_name +'/'
                                    path_indb = '/storage/' + folder_name +'/'
                                    # path = './storage/' + folder_name +'/'
                                    # path_indb = '/storage/' + folder_name +'/'
                                    unique_filename = str(uuid.uuid4())
                                    tmpread = file.read()
                                    file_string = base64.b64encode(tmpread)                                    
                                    file_stringread = tmpread
                                    size = str(len(file_stringread))
                                    typefile = str(file.filename).split('.')[-1]
                                    try:
                                        with open(path + unique_filename + "." + typefile, "wb") as fh:
                                            fh.write(base64.decodebytes(file_string))
                                            list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName,'filesize':size})
                                    except Exception as ex:
                                        print(str(ex))
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name'}),200
                                resultSelect = select().select_transactionfile(folder_name)
                                if resultSelect['result'] == 'OK':
                                    list_arrfile = resultSelect['messageText']['json_data']
                                    for o in range(len(list_arrfile)):
                                        print(list_arrfile[o])
                                        if 'filesize' in list_arrfile[o]:
                                            tmpsum_storage += int(list_arrfile[o]['filesize'])
                                        print(tmpsum_storage)
                                        list_file_name.append(list_arrfile[o])
                                    resUpdate = update().update_transactionfile(list_file_name,folder_name,tmpsum_storage)
                                    if resUpdate['result'] == 'OK':
                                        return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'cant update in db'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found in db'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'please input file'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data form not folder_name value'}),200
                    else:    
                        unique_foldername = str(uuid.uuid4())  
                        path =path_global_1 +'/storage/' + unique_foldername +'/'
                        path_indb = '/storage/' + unique_foldername +'/'
                        # path = './storage/' + unique_foldername +'/'
                        # path_indb = '/storage/' + unique_foldername +'/'
                        if not os.path.exists(path):
                            os.makedirs(path)
                        if 'file[]' in dataFiles and 'username' in dataForm:
                            files = request.files.getlist("file[]")
                            data_userName = dataForm['username']
                            for file in files:
                                unique_filename = str(uuid.uuid4())
                                tmpread = file.read()
                                file_string = base64.b64encode(tmpread)                                    
                                file_stringread = tmpread
                                size = str(len(file_stringread))
                                tmpsum_storage += len(file_stringread)
                                typefile = str(file.filename).split('.')[-1]
                                with open(path + unique_filename + "." + typefile, "wb") as fh:
                                    fh.write(base64.decodebytes(file_string))
                                    list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName,'filesize':size})
                            result_Insert = insert().insert_transactionfile(list_file_name,path_indb,unique_foldername,tmpsum_storage)
                            result_update = update().update_attmp_folder_name_for_document_v1(tmp_sid,unique_foldername)
                            if result_Insert['result'] =='OK':
                                return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':unique_foldername,'file_name':list_file_name,'message':'success'},'messageER':None,'status_Code':200}),200
                            else:
                                return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'cant insert to db','status_Code':200}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':404}),404
                else:
                    if str(folder_name).replace(' ','') != "":
                        if 'file[]' in dataFiles:
                            files = request.files.getlist("file[]")
                            for file in files:
                                path = path_global_1 +'/storage/' + folder_name +'/'
                                path_indb = '/storage/' + folder_name +'/'
                                # path = './storage/' + folder_name +'/'
                                # path_indb = '/storage/' + folder_name +'/'
                                unique_filename = str(uuid.uuid4())
                                file_string = base64.b64encode(file.read())
                                typefile = str(file.filename).split('.')[-1]
                                try:
                                    with open(path + unique_filename + "." + typefile, "wb") as fh:
                                        fh.write(base64.decodebytes(file_string))
                                        list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                except Exception as ex:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name'}),200
                            resultSelect = select().select_transactionfile(folder_name)
                            if resultSelect['result'] == 'OK':
                                list_arrfile = resultSelect['messageText']['json_data']
                                for o in range(len(list_arrfile)):
                                    list_file_name.append(list_arrfile[o])
                                resUpdate = update().update_transactionfile(list_file_name,folder_name)
                                if resUpdate['result'] == 'OK':
                                    return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'cant update in db'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found in db'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'please input file'}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data form not folder_name value'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data form not key folder_name'}),200
    elif type_api == 'get':
        if request.method == 'POST':
            dataJson = request.json
            if 'folder_name' in dataJson:
                folder_name = dataJson['folder_name']
                resultSelect = select().select_transactionfile(folder_name)
                if resultSelect['result'] == 'OK':
                    json_data = (resultSelect['messageText']['json_data'])
                    pathfolder = (resultSelect['messageText']['pathfolder'])
                    return jsonify({'result':'OK','messageText':{'file_storage':'paperless','folder_path':pathfolder,'folder_name':folder_name,'file_name':json_data},'messageER':None,'status_Code':200}),200
                else:
                    url = url_ip_eform + '/api/v1/get_attract_file/?folder_name=' + folder_name
                    result_eform = callGET_other(url)
                    if result_eform['result'] == 'OK':
                        tmpmessage = result_eform['messageText'].json()
                        if tmpmessage['result'] == 'OK':
                            tmpdata = tmpmessage['messageText'][0]
                            pathfolder = tmpdata['folder_path']
                            json_data = tmpdata['file_name']
                            folder_name = tmpdata['folder_name']
                            return jsonify({'result':'OK','messageText':{'file_storage':'eform','folder_path':pathfolder,'folder_name':folder_name,'file_name':json_data},'messageER':None,'status_Code':200}),200
                    return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'cant get data','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'parameter incorrect','status_Code':200}),200
    elif type_api == 'remove':
        if request.method == 'POST':
            dataJson = request.json
            if 'folder_name' in dataJson and 'file_name' in dataJson:
                foldername = dataJson['folder_name']
                filename = dataJson['file_name']
                resultSelect = select().select_transactionfile(foldername)
                if resultSelect['result'] == 'OK':
                    arrlisttoCheck = resultSelect['messageText']['json_data']
                    pathfolder = (resultSelect['messageText']['pathfolder'])
                    path_removeFile = pathfolder + filename
                    path_removeFile = path_global_1 + path_removeFile
                    for i in range(len(arrlisttoCheck)):
                        if filename == arrlisttoCheck[i]['file_name_new']:
                            arrlisttoCheck.pop(i)
                            try:
                                os.remove(path_removeFile)
                                break
                            except Exception as ex:
                                return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':None},'messageER':'not found file _1','status_Code':200}),200
                            break
                    for i in range(len(arrlisttoCheck)):
                        if 'filesize' in arrlisttoCheck[i]:
                            tmpsum_storage += int(arrlisttoCheck[i]['filesize'])
                    resUpdate = update().update_transactionfile(arrlisttoCheck,foldername,tmpsum_storage)
                    if resUpdate['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':{'folder_path':None,'folder_name':None,'file_name':arrlisttoCheck},'messageER':None,'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'cant update to db','status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'not found foldername','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'parameter incorrect','status_Code':200}),200
    else:
        return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'type service incorrect','status_Code':200}),200

@status_methods.route('/storage/downloadfile/v1/<string:folder_name>/<string:file_name>',methods=['GET'])
def downloadfile_storage_v1(folder_name,file_name):
    if request.method == 'GET':
        resultSelect = select().select_transactionfile(folder_name)
        if resultSelect['result'] == 'OK':
            json_data = (resultSelect['messageText']['json_data'])
            for i in range(len(json_data)):
                if json_data[i]['file_name_new'] == file_name:
                    original_nameFile = json_data[i]['file_name_original']
            pathfolder = (resultSelect['messageText']['pathfolder'])
            path_downloadFile = pathfolder + file_name
            # path_downloadFile = os.getcwd() + path_downloadFile
            path_folder = os.getcwd() + pathfolder
            # path_downloadFile = pathfolder + file_name
            path_downloadFile = path_global_1 + path_downloadFile
            if os.path.isfile(path_downloadFile):
                try:
                    filename = original_nameFile.encode('latin-1')
                except UnicodeEncodeError:
                    filenames = {
                        'filename': unicodedata.normalize('NFKD', original_nameFile).encode('latin-1', 'ignore'),
                        'filename*': "UTF-8''{}".format(original_nameFile),
                    }
                    filenames['filename'] = filenames['filename'].decode('utf8')
                else:
                    filenames = {'filename': original_nameFile}
                return send_file(os.path.join(path_downloadFile), as_attachment=True, attachment_filename='%s' % filenames['filename'])
            else:
                path_downloadFile = os.getcwd() + path_downloadFile
                try:
                    filename = original_nameFile.encode('latin-1')
                except UnicodeEncodeError:
                    filenames = {
                        'filename': unicodedata.normalize('NFKD', original_nameFile).encode('latin-1', 'ignore'),
                        'filename*': "UTF-8''{}".format(original_nameFile),
                    }
                    filenames['filename'] = filenames['filename'].decode('utf8')
                else:
                    filenames = {'filename': original_nameFile}
                return send_file(os.path.join(path_downloadFile), as_attachment=True, attachment_filename='%s' % filenames['filename'])

@status_methods.route('/storage/viewfile/v1/<string:folder_name>/<string:file_name>',methods=['GET'])
def publicview_storage_v1(folder_name,file_name):
    if request.method == 'GET':
        resultSelect = select().select_transactionfile(folder_name)
        if resultSelect['result'] == 'OK':
            json_data = (resultSelect['messageText']['json_data'])
            for i in range(len(json_data)):
                if json_data[i]['file_name_new'] == file_name:
                    original_nameFile = json_data[i]['file_name_original']
            pathfolder = (resultSelect['messageText']['pathfolder'])
            path_downloadFile = pathfolder + file_name
            path_downloadFile_1 = os.getcwd() + path_downloadFile
            # path_downloadFile = path_downloadFile
            # if path_global_1 not in path_downloadFile:
            #     path_downloadFile = path_global_1 + path_downloadFile
            # path_downloadFile = path_global_1 + path_downloadFile
            if os.path.isfile(path_downloadFile_1):
                with open(path_downloadFile_1, "rb") as pdf_file:
                    encoded_string = base64.b64encode(pdf_file.read())
            else:                
                path_downloadFile_1 = path_global_1 + path_downloadFile
                with open(path_downloadFile_1, "rb") as pdf_file:
                    encoded_string = base64.b64encode(pdf_file.read())
            try:
                filename = original_nameFile.encode('latin-1')
            except UnicodeEncodeError:
                filenames = {
                    'filename': unicodedata.normalize('NFKD', original_nameFile).encode('latin-1', 'ignore'),
                    'filename*': "UTF-8''{}".format(original_nameFile),
                }
                filenames['filename'] = filenames['filename'].decode('utf8')
            else:
                filenames = {'filename': original_nameFile}
            encoded_string = (encoded_string).decode('utf8')
            response = make_response(base64.b64decode(encoded_string))
            if file_name.split('.')[-1] == 'pdf':
                response.headers.set('Content-Type', 'application/pdf')
            elif file_name.split('.')[-1] == 'jpg':
                response.headers.set('Content-Type', 'image/jpeg')
            elif file_name.split('.')[-1] == 'png':
                response.headers.set('Content-Type','image/x-png')
            response.headers.set(
                'Content-Disposition', 'as_attachment=True', filename='%s' % filenames['filename'])
            return response

@status_methods.route('/api/v1/view_sign/image',methods=['GET'])
def view_sign_api_v1():
    if request.method == 'GET':
        if 'email' in request.args:
            if request.args['email'] != None:
                tmp_emailone = request.args['email']
                # print(tmp_emailone)
                result_select = select().select_signning_profile_v1(tmp_emailone)
                if result_select['result'] == 'OK':
                    base64_pdfFile = result_select['messageText']
                    unique_filename = str(uuid.uuid4())
                    return send_file(
                        io.BytesIO(base64.b64decode(base64_pdfFile)),
                        mimetype='image/jpeg',
                        as_attachment=False,
                        attachment_filename='%s.pdf' % unique_filename)

@status_methods.route('/api/v1/download/pdf/sign_pdf',methods=['GET'])
def download_url_pdf_api_v1():
    if request.method == 'GET':
        tmp_sidCode = request.args.get('sidCode')
        if tmp_sidCode != None:
            result_select = select().select_admin_dashboard_pdf_v1(tmp_sidCode)
            if result_select['messageText'][0]['pdf_rejectorcancle'] != None:
                result_select['messageText'][0]['string_sign'] = result_select['messageText'][0]['pdf_rejectorcancle']
            if result_select['messageText'][0]['string_sign'] == None:
                result_select['messageText'][0]['string_sign'] =result_select['messageText'][0]['string_pdf']
            # print(result_select)
            if result_select['result'] == 'OK':
                try:
                    filename = result_select['messageText'][0]['file_name'].encode('latin-1')
                except UnicodeEncodeError:
                    filenames = {
                        'filename': unicodedata.normalize('NFKD', result_select['messageText'][0]['file_name']).encode('latin-1', 'ignore'),
                        'filename*': "UTF-8''{}".format(result_select['messageText'][0]['file_name']),
                    }
                    filenames['filename'] = filenames['filename'].decode('utf8')
                else:
                    filenames = {'filename': result_select['messageText'][0]['file_name']}
                # print(filenames)
                if str(filenames['filename']).replace(' ','') == '.pdf':
                    unique_filename = str(uuid.uuid4())
                    filenames['filename'] = unique_filename + '.pdf'
                    # print(str(filenames['filename*']).split("'")[2])
                return send_file(io.BytesIO(base64.b64decode(str(result_select['messageText'][0]['string_sign']))),mimetype='application/pdf',as_attachment=True,attachment_filename='%s' % str(filenames['filename']))
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}})
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':tmp_sidCode['messageText'],'data':[]}})

@status_methods.route('/storage/v1/pdf/addAttachment', methods=['GET'])
def storage_addAttachment_api_v1():
    if request.method == 'GET':
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            sid = request.args.get('sid')
            unique_filename = str(uuid.uuid4())
            start_dir = os.getcwd()
            temp_folder = './storage'
            list_attachItem = []
            count = 0
            result_select_pdf = select().select_data_for_addAttachment(sid)
            if result_select_pdf['messageText'] != None:
                data_from_view = result_select_pdf['messageText']
                file_name = data_from_view['file_name']
                # print(file_name)
                unique_foldername = str(uuid.uuid4())
                path = path_global_1 + '/storage/temp/' + unique_foldername + '/'
                path_1 = path_global_1 + '/storage/temp/' + unique_foldername + '/'
                # path = './storage/temp/' + unique_foldername + '/'
                # path_1 = '/storage/temp/' + unique_foldername + '/'
                if not os.path.exists(path):
                    os.makedirs(path)
                print(path)
                # return ''
                # VVV -- pdf base64 -- VVV
                str_pdf = data_from_view['string_pdf']
                attemped_folder = data_from_view['attempted_folder']
                if attemped_folder !=None:
                    result_select_json = select().select_foldername_for_addAttachment(attemped_folder)
                    # VVV -- storage_data -- VVV
                    if result_select_json['result'] == 'OK':
                        if result_select_json['messageText'] != None:
                            tmp_data = result_select_json['messageText']
                            tmp_jsondata_file = eval(tmp_data['json_data'])
                            tmp_pathfolder = tmp_data['pathfolder']
                            for n in range(len(tmp_jsondata_file)):
                                namefile_new = tmp_jsondata_file[n]['file_name_new']
                                namefile_original = tmp_jsondata_file[n]['file_name_original']
                                with open(start_dir+tmp_pathfolder+namefile_new, "rb") as f:
                                    encodedZip = base64.b64encode(f.read())
                                    encoded_filein = (encodedZip.decode())
                                count = count + 1
                                tmp_json = {}
                                tmp_json['attachmentName'] = namefile_original
                                tmp_json['attachmentContent'] = encoded_filein
                                tmp_json['attachmentDescription'] = ''
                                list_attachItem.append(tmp_json)
                            result_all = doc_addAttachment_v2(str_pdf,count,list_attachItem,token_header)
                            if result_all['result'] == 'OK':
                                pdffile = result_all['msg']['pdfData']
                                with open(start_dir + path_1 + file_name  , "wb") as fh:
                                    fh.write(base64.b64decode(str(pdffile)))
                                url_download = myUrl_domain + 'storage/v1/pdf/addAttachment/'+unique_foldername+'/'+file_name
                                return jsonify({'result':'OK','messageText':{'url_download':url_download}})
                            else:
                                return jsonify({'result':'ER','messageText': 'Not have data' ,'status_Code':result_all['code'],'messageER':None}),result_all['code']
                        else:
                            return jsonify({'result':'ER','messageText': 'Not have data' ,'status_Code':200,'messageER':None}),200
                    else:
                        return send_file(io.BytesIO(base64.b64decode(str_pdf)),mimetype='application/pdf',as_attachment=True,attachment_filename=file_name)
                else:
                    return send_file(io.BytesIO(base64.b64decode(str_pdf)),mimetype='application/pdf',as_attachment=True,attachment_filename=file_name)
            else:
                return jsonify({'result':'ER','messageText': 'Not have data' ,'status_Code':200,'messageER':None}),200
        except Exception as ex:  
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            db.session.rollback()
            raise
            return jsonify({'result':'ER','messageText': None,'status_Code':200,'messageER':str(ex)}),200

@status_methods.route('/storage/v1/pdf/addAttachment/<string:foldername>/<string:filename>',methods=['GET'])
def storage_addAttachment_api_download_v1(foldername,filename):
    if request.method == 'GET':
        path_1 = '/storage/temp/' + foldername + '/' + filename
        path_downloadFile = os.getcwd() + path_1
        with open(path_downloadFile, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        try:
            filename = filename.encode('latin-1')
        except UnicodeEncodeError:
            filenames = {
                'filename': unicodedata.normalize('NFKD', filename).encode('latin-1', 'ignore'),
                'filename*': "UTF-8''{}".format(filename),
            }
            filenames['filename'] = filenames['filename'].decode('utf8')
        else:
            filenames = {'filename': filename}
        encoded_string = (encoded_string).decode('utf8')
        response = make_response(base64.b64decode(encoded_string))
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set(
            'Content-Disposition', 'as_attachment=True', filename='%s' % filename.decode('utf-8'))
        return response

@status_methods.route('/storage/v2/<string:type_api>',methods=['POST'])
# @token_required
def onebox_save_file_api_v2(type_api):
    try:
        token_header = request.headers['Authorization']
        try:
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
    except KeyError as ex:
        return redirect(url_paperless)
    try:
        token_header = 'Bearer ' + token_header
        result_verify = verify().verify_one_id(token_header)
        if result_verify['result'] != 'OK':
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        result_verify_json = (result_verify['messageText']).json()
        user_id = result_verify_json['biz_detail'][0]['account_id']            
    except Exception as e:
        return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401        
    if type_api == 'keep':
        if request.method == 'POST':
            try:
                dataForm = request.form
                dataFiles = request.files
                if len(dataForm) == 0:
                    return jsonify({'result':'ER','messageText':None,'messageER':'parameter incorrect' ,'status_Code':404}),404
                    
                tax_id_onebox = None
                account_id = None
                list_file_name = []
                list_result = []
                tax_id = dataForm['tax_id']
                sid = dataForm['sid']
                data_userName = dataForm['username']
                # files = request.files.getlist("file[]")
                check = True
                ts = int(time.time())
                st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                st2 = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
                # GET account_id จาก oneid
                try:
                    headers = {
                        'Authorization': token_onebox
                    }
                    data = {
                        'user_id': str(user_id)
                    }
                    result_select_account_id = select_account_id_onebox(data,headers,token_header)
                    # print (result_select_account_id)
                    if result_select_account_id['messageText']['status'] == 'OK':
                        for i in range(len(result_select_account_id['messageText']['result'])):
                            if tax_id != '':
                                if result_select_account_id['messageText']['result'][i]['taxid'] == tax_id:
                                    account_id = result_select_account_id['messageText']['result'][i]['account_id']
                                    tax_id_onebox = result_select_account_id['messageText']['result'][i]['taxid']
                            elif tax_id == '':
                                if result_select_account_id['messageText']['result'][i]['taxid'] == None:
                                    account_id = result_select_account_id['messageText']['result'][i]['account_id']
                                    tax_id_onebox = tax_id

                        if tax_id_onebox != None and account_id != None:
                            # GET folder จาก account_id
                            data_account_id = {
                                'account_id': str(account_id)
                            }
                            result_select_folder = select_folder_onebox(account_id,data_account_id,headers,token_header)
                            if tax_id_onebox != '':
                                result_select_biztax = select().select_BizProfile_for_onebox(tax_id_onebox)
                            
                                if result_select_biztax['result'] == 'OK':
                                    eval_result_select_biztax = eval(result_select_biztax['messageText'][0])
                                    biz_foldername = eval_result_select_biztax['first_name_th']
                                    for j in range(len(result_select_folder['messageText']['result'])):
                                        if result_select_folder['messageText']['result'][j]['folder_name'] == biz_foldername:
                                            folder_id = result_select_folder['messageText']['result'][j]['folder_id']

                                    # Get sub_folder
                                data_folder_id = {
                                    'account_id': str(account_id),
                                    'folder_id' : str(folder_id)
                                }

                                
                                # result_select_sub_folder = select_sub_folder_onebox(data_folder_id,headers,token_header)
                                result_select_sub_folder = get_sub_folder_onebox(data_folder_id,headers,token_header)
                                # print('result_select_sub_folder11111: ',result_select_sub_folder)
                                if result_select_sub_folder['messageText']['status'] == 'OK':

                                    for m in range(len(result_select_sub_folder['messageText']['result'])):

                                        if result_select_sub_folder['messageText']['result'][m]['folder_name'] == 'paperless':
                                            print (result_select_sub_folder['messageText']['result'][m])
                                            print ('Yesssssssss')
                                            check = True
                                            sub_folder_id = result_select_sub_folder['messageText']['result'][m]['folder_id']
                                            break
                                        elif result_select_sub_folder['messageText']['result'][m]['folder_name'] != 'paperless':
                                            print (result_select_sub_folder['messageText']['result'][m])
                                            sub_folder_id = result_select_sub_folder['messageText']['result'][m]['folder_id']
                                            print ('Noooooooo')
                                            check = False

                                    # print ('result_select_sub_folder: ',result_select_sub_folder)
                                    # sub_folder_id = result_select_sub_folder['result'][0]['folder_id']
                                    # print ('sub_folder_id: ',sub_folder_id)

                                    if check == True:
                                        print (check)
                                        # Get sub_folder2
                                        data_folder_id2 = {
                                        'account_id': str(account_id),
                                        'folder_id' : str(sub_folder_id)
                                        }

                                        result_select_sub_folder2 = get_sub_folder_onebox(data_folder_id2,headers,token_header)
                                        if result_select_sub_folder2['messageText']['status'] == 'OK':
                                            print ('result_select_sub_folder2: ',result_select_sub_folder2)
                                            sub_folder_id2 = result_select_sub_folder2['messageText']['result'][0]['folder_id']
                                            print ('sub_folder_id2: ',sub_folder_id2)

                                            result_select_doc_id = select().select_doc_id_onebox(sid)
                                            result_select_doc_id = str(result_select_doc_id).split('\'')[1]
                                            print ('result_select_doc_id: ',result_select_doc_id)
                                            
                                            # Create folder in 'attach_file' folder
                                            data_sub_folder_id = {
                                                'account_id': str(account_id),
                                                'parent_folder_id' : str(sub_folder_id2),
                                                'folder_name' : result_select_doc_id
                                            }
                                            print ('sub_folder_id2: ',sub_folder_id2)
                                            result_create_folder = create_folder_onebox(data_sub_folder_id,headers,token_header)

                                            folder_id_tax = result_create_folder['messageText']['data']['folder_id']
                                            if result_create_folder['messageText']['status'] == 'OK':

                                                print ('dddddddddddddddd')
                                                files = request.files.getlist("file[]")
                                                unique_foldername = str(uuid.uuid4())
                                                path = './storage/temp/' + unique_foldername +'/'
                                                path2 = './storage/temp/'
                                                
                                                for file in files:
                                                    unique_filename = str(uuid.uuid4())
                                                    original_filename = str(file.filename).split('.')[0]
                                                    check_thai = pythainlp.util.isthai(original_filename)
                                                    if check_thai == True:
                                                        original_filename = romanize(original_filename, engine="thai2rom")

                                                    file_string = base64.b64encode(file.read())
                                                    typefile = str(file.filename).split('.')[-1]
                                                    typefile = typefile.split('"')[0]
                                                    with open(path2 + original_filename + "." + typefile, "wb") as fh:
                                                        file_open = fh 
                                                        fh.write(base64.decodebytes(file_string))
                                                        list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                                    file_open = open(path2 + original_filename + "." + typefile, "rb")

                                                    data_save_file = {
                                                        'account_id': str(account_id),
                                                        'folder_id' : str(folder_id_tax), 
                                                    }

                                                    files_save = {
                                                        'file' : file_open
                                                    }    

                                                    result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName),token_header)
                                                    print ('result_save_file: ',result_save_file)
                                                    file_open.close()
                                                    os.remove(path2 + original_filename + "." + typefile)
                                                    list_result.append(result_save_file)

                                                return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200   

                                            elif result_create_folder['messageText']['status'] == 'ER':
                                                return jsonify({'result':'OK','messageText':None,'messageER':list_result ,'status_Code':401}),401  
                                        
                                        elif result_select_sub_folder2['messageText']['status'] == 'ER':

                                            data_tax_sub_folder_id2 = {
                                                    'account_id': str(account_id),
                                                    'parent_folder_id' : str(sub_folder_id),
                                                    'folder_name' : 'attach_folder'
                                                }
                    
                                            result_create_folder_tax2 = create_folder_onebox(data_tax_sub_folder_id2,headers,token_header)
                                            print ('result_create_folderrrrr22222: ',result_create_folder_tax2)

                                            folder_id_tax_folder_sid = result_create_folder_tax2['messageText']['data']['folder_id']

                                            result_select_doc_id = select().select_doc_id_onebox(sid)
                                            result_select_doc_id = str(result_select_doc_id).split('\'')[1]
                                            print ('result_select_doc_id: ',result_select_doc_id)

                                            data_tax_sub_folder_id_sid = {
                                                'account_id': str(account_id),
                                                'parent_folder_id' : str(folder_id_tax_folder_sid),
                                                'folder_name' : result_select_doc_id
                                            }
                                            print ('folder_id_tax_folder2: ',folder_id_tax_folder_sid)
                                            result_create_folder_tax_sid = create_folder_onebox(data_tax_sub_folder_id_sid,headers)
                                            print ('result_create_folderrrrr3333: ',result_create_folder_tax_sid)

                                            folder_id_tax = result_create_folder_tax_sid['messageText']['data']['folder_id']

                                            if result_create_folder_tax_sid['messageText']['status'] == 'OK':

                                                print ('dddddddddddddddd')
                                                files = request.files.getlist("file[]")
                                                unique_foldername = str(uuid.uuid4())
                                                path = './storage/temp/' + unique_foldername +'/'
                                                path2 = './storage/temp/'
                                                
                                                for file in files:
                                                    unique_filename = str(uuid.uuid4())
                                                    original_filename = str(file.filename).split('.')[0]
                                                    check_thai = pythainlp.util.isthai(original_filename)
                                                    if check_thai == True:
                                                        original_filename = romanize(original_filename, engine="thai2rom")

                                                    file_string = base64.b64encode(file.read())
                                                    typefile = str(file.filename).split('.')[-1]
                                                    typefile = typefile.split('"')[0]
                                                    with open(path2 + original_filename + "." + typefile, "wb") as fh:
                                                        file_open = fh 
                                                        fh.write(base64.decodebytes(file_string))
                                                        list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                                    file_open = open(path2 + original_filename + "." + typefile, "rb")

                                                    data_save_file = {
                                                        'account_id': str(account_id),
                                                        'folder_id' : str(folder_id_tax), 
                                                    }

                                                    files_save = {
                                                        'file' : file_open
                                                    }    

                                                    result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName))
                                                    print ('result_save_file: ',result_save_file)
                                                    file_open.close()
                                                    os.remove(path2 + original_filename + "." + typefile)
                                                    list_result.append(result_save_file)

                                                return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200   

                                            elif result_create_folder_tax_sid['messageText']['status'] == 'ER':
                                                return jsonify({'result':'OK','messageText':None,'messageER':list_result ,'status_Code':401}),401  

                                    elif check == False:       
                                            print ('False')                                   
                                            # Create paperless folder in โฟลเดอร์ส่วนตัว
                                            data_tax_sub_folder_id = {
                                                'account_id': str(account_id),
                                                'parent_folder_id' : str(folder_id),
                                                'folder_name' : 'paperless'
                                            }
                        
                                            result_create_folder_tax = create_folder_onebox(data_tax_sub_folder_id,headers,token_header)
                                            print ('result_create_folderrrrrrrrrrrrrrrr: ',result_create_folder_tax)
                                            folder_id_tax_folder2 = result_create_folder_tax['messageText']['data']['folder_id']
                                            print ('folder_id_tax_folder2: ',folder_id_tax_folder2)

                                            
                                            data_tax_sub_folder_id2 = {
                                                'account_id': str(account_id),
                                                'parent_folder_id' : str(folder_id_tax_folder2),
                                                'folder_name' : 'attach_folder'
                                            }

                                            result_create_folder_tax2 = create_folder_onebox(data_tax_sub_folder_id2,headers,token_header)
                                            print ('result_create_folderrrrr22222: ',result_create_folder_tax2)
                                            
                                            if result_create_folder_tax2['messageText']['status'] == 'OK':

                                                result_select_doc_id = select().select_doc_id_onebox(sid)
                                                result_select_doc_id = str(result_select_doc_id).split('\'')[1]
                                                print ('result_select_doc_id: ',result_select_doc_id)

                                                folder_id_tax_folder_sid = result_create_folder_tax2['messageText']['data']['folder_id']
                                                data_tax_sub_folder_id_sid = {
                                                    'account_id': str(account_id),
                                                    'parent_folder_id' : str(folder_id_tax_folder_sid),
                                                    'folder_name' : result_select_doc_id
                                                }
                                                print ('folder_id_tax_folder2: ',folder_id_tax_folder_sid)
                                                result_create_folder_tax_sid = create_folder_onebox(data_tax_sub_folder_id_sid,headers,token_header)
                                                print ('result_create_folderrrrr3333: ',result_create_folder_tax_sid)

                                            
                                            folder_id_save = result_create_folder_tax_sid['messageText']['data']['folder_id']

                                            if result_create_folder_tax_sid['messageText']['status'] == 'OK':

                                                print ('dddddddddddddddd')
                                                files = request.files.getlist("file[]")
                                                unique_foldername = str(uuid.uuid4())
                                                path = './storage/temp/' + unique_foldername +'/'
                                                path2 = './storage/temp/'
                                                
                                                for file in files:
                                                    unique_filename = str(uuid.uuid4())
                                                    original_filename = str(file.filename).split('.')[0]
                                                    check_thai = pythainlp.util.isthai(original_filename)
                                                    if check_thai == True:
                                                        original_filename = romanize(original_filename, engine="thai2rom")

                                                    file_string = base64.b64encode(file.read())
                                                    typefile = str(file.filename).split('.')[-1]
                                                    typefile = typefile.split('"')[0]
                                                    with open(path2 + original_filename + "." + typefile, "wb") as fh:
                                                        file_open = fh 
                                                        fh.write(base64.decodebytes(file_string))
                                                        list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                                    file_open = open(path2 + original_filename + "." + typefile, "rb")

                                                    data_save_file = {
                                                        'account_id': str(account_id),
                                                        'folder_id' : str(folder_id_save), 
                                                    }

                                                    files_save = {
                                                        'file' : file_open
                                                    }    

                                                    result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName),token_header)
                                                    print ('result_save_file: ',result_save_file)
                                                    file_open.close()
                                                    os.remove(path2 + original_filename + "." + typefile)
                                                    list_result.append(result_save_file)

                                                return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200   

                                            elif result_create_folder_tax_sid['messageText']['status'] == 'ER':
                                                return jsonify({'result':'OK','messageText':None,'messageER':list_result ,'status_Code':401}),401


                                elif result_select_sub_folder['messageText']['status'] == 'ER': #ไม่มีโฟลเดอร์ paperless

                                    print ('result_select_sub_folder: ',result_select_sub_folder)                                    
                                    if account_id != None and folder_id != None:
                                        if result_select_sub_folder['messageText']['errorMessage'] == 'Not account exist':

                                            # Create paperless folder in business_id
                                            data_private_sub_folder_id = {
                                                'account_id': str(account_id),
                                                'parent_folder_id' : str(folder_id),
                                                'folder_name' : 'paperless'
                                            }

                                            result_create_folder_tax = create_folder_onebox(data_private_sub_folder_id,headers,token_header)
                                            print ('result_create_folderrrrrrrrrrrrrrrr_tax: ',result_create_folder_tax)

                                            folder_id_tax_ppl = result_create_folder_tax['messageText']['data']['folder_id']

                                            # Create attach folder in business_id
                                            data_private_sub_folder_id = {
                                                'account_id': str(account_id),
                                                'parent_folder_id' : str(folder_id_tax_ppl),
                                                'folder_name' : 'attach_folder'
                                            }

                                            result_create_folder_tax2 = create_folder_onebox(data_private_sub_folder_id,headers,token_header)
                                            print ('result_create_folderrrrrrrrrrrrrrrr_tax: ',result_create_folder_tax2)

                                            folder_id_tax_attach = result_create_folder_tax2['messageText']['data']['folder_id']

                                            # Create doc_id folder in business_id

                                            result_select_doc_id = select().select_doc_id_onebox(sid)
                                            result_select_doc_id = str(result_select_doc_id).split('\'')[1]
                                            print ('result_select_doc_id: ',result_select_doc_id)

                                            data_private_sub_folder_id = {
                                                'account_id': str(account_id),
                                                'parent_folder_id' : str(folder_id_tax_attach),
                                                'folder_name' : result_select_doc_id
                                            }

                                            result_create_folder_tax3 = create_folder_onebox(data_private_sub_folder_id,headers,token_header)
                                            print ('result_create_folderrrrrrrrrrrrrrrr_tax: ',result_create_folder_tax3)

                                            folder_id_tax_docid = result_create_folder_tax3['messageText']['data']['folder_id']

                                            if result_create_folder_tax3['messageText']['status'] == 'OK':

                                                print ('aaaaaaaaaaaaa')
                                                files = request.files.getlist("file[]")
                                                unique_foldername = str(uuid.uuid4())
                                                path = './storage/temp/' + unique_foldername +'/'
                                                path2 = './storage/temp/'
                                                
                                                for file in files:
                                                    unique_filename = str(uuid.uuid4())
                                                    original_filename = str(file.filename).split('.')[0]
                                                    check_thai = pythainlp.util.isthai(original_filename)
                                                    if check_thai == True:
                                                        original_filename = romanize(original_filename, engine="thai2rom")

                                                    file_string = base64.b64encode(file.read())
                                                    typefile = str(file.filename).split('.')[-1]
                                                    typefile = typefile.split('"')[0]
                                                    with open(path2 + original_filename + "." + typefile, "wb") as fh:
                                                        file_open = fh 
                                                        fh.write(base64.decodebytes(file_string))
                                                        list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                                    file_open = open(path2 + original_filename + "." + typefile, "rb")

                                                    data_save_file = {
                                                        'account_id': str(account_id),
                                                        'folder_id' : str(folder_id_tax_docid), 
                                                    }

                                                    files_save = {
                                                        'file' : file_open
                                                    }    

                                                    result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName))
                                                    print ('result_save_file: ',result_save_file)
                                                    file_open.close()
                                                    os.remove(path2 + original_filename + "." + typefile)
                                                    list_result.append(result_save_file)

                                                return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200   

                                            elif result_create_folder_private_sid['messageText']['status'] == 'ER':
                                                return jsonify({'result':'OK','messageText':None,'messageER':list_result ,'status_Code':401}),401

                            elif tax_id_onebox == '':
                                    print ('uuuuuuuuuuuuuuuuuuuuuuuuuuuu: ',result_select_folder['result'])
                                    for k in range(len(result_select_folder['messageText']['result'])):
                                        if (result_select_folder['messageText']['result'][k]['folder_name'] == 'โฟลเดอร์ส่วนตัว'):
                                            folder_id_private_folder = result_select_folder['messageText']['result'][k]['folder_id']
                                            print('folder_id_private_folder: ', folder_id_private_folder)

                                    result_select_doc_id = select().select_doc_id_onebox(sid)
                                    result_select_doc_id = str(result_select_doc_id).split('\'')[1]
                                    print ('result_select_doc_id: ',result_select_doc_id)

                                    data_folder_id = {
                                        'account_id': str(account_id),
                                        'folder_id' : str(folder_id_private_folder)
                                    }
                                    
                                    result_select_sub_folder = select_sub_folder_onebox(data_folder_id,headers)
                                    print ('result_select_sub_folder: ',result_select_sub_folder)

                                    if result_select_sub_folder['messageText']['status'] == 'ER':
                                        if account_id != None and folder_id_private_folder != None:
                                            if result_select_sub_folder['messageText']['errorMessage'] == 'Not account exist':

                                                # Create paperless folder in โฟลเดอร์ส่วนตัว
                                                data_private_sub_folder_id = {
                                                    'account_id': str(account_id),
                                                    'parent_folder_id' : str(folder_id_private_folder),
                                                    'folder_name' : 'paperless'
                                                }

                                                result_create_folder_private = create_folder_onebox(data_private_sub_folder_id,headers,token_header)
                                                print ('result_create_folderrrrrrrrrrrrrrrr: ',result_create_folder_private)
                                                folder_id_private_folder2 = result_create_folder_private['messageText']['data']['folder_id']

                                                data_private_sub_folder_id2 = {
                                                    'account_id': str(account_id),
                                                    'parent_folder_id' : str(folder_id_private_folder2),
                                                    'folder_name' : 'attach_folder'
                                                }

                                                result_create_folder_private2 = create_folder_onebox(data_private_sub_folder_id2,headers,token_header)
                                                folder_id_private_attach2 = result_create_folder_private2['messageText']['data']['folder_id']

                                                result_select_doc_id = select().select_doc_id_onebox(sid)
                                                result_select_doc_id = str(result_select_doc_id).split('\'')[1]

                                                data_private_sub_folder_id_sid = {
                                                    'account_id': str(account_id),
                                                    'parent_folder_id' : str(folder_id_private_attach2),
                                                    'folder_name' : result_select_doc_id
                                                }
                                                result_create_folder_private_sid = create_folder_onebox(data_private_sub_folder_id_sid,headers,token_header)
                                                print ('result_create_folderrrrr3333: ',result_create_folder_private_sid)

                                                foder_id_save2 = result_create_folder_private_sid['messageText']['data']['folder_id']

                                                if result_create_folder_private_sid['messageText']['status'] == 'OK':

                                                    print ('dddddddddddddddd')
                                                    files = request.files.getlist("file[]")
                                                    unique_foldername = str(uuid.uuid4())
                                                    path = './storage/temp/' + unique_foldername +'/'
                                                    path2 = './storage/temp/'
                                                    
                                                    for file in files:
                                                        unique_filename = str(uuid.uuid4())
                                                        original_filename = str(file.filename).split('.')[0]
                                                        check_thai = pythainlp.util.isthai(original_filename)
                                                        if check_thai == True:
                                                            original_filename = romanize(original_filename, engine="thai2rom")

                                                        file_string = base64.b64encode(file.read())
                                                        typefile = str(file.filename).split('.')[-1]
                                                        typefile = typefile.split('"')[0]
                                                        with open(path2 + original_filename + "." + typefile, "wb") as fh:
                                                            file_open = fh 
                                                            fh.write(base64.decodebytes(file_string))
                                                            list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                                        file_open = open(path2 + original_filename + "." + typefile, "rb")

                                                        data_save_file = {
                                                            'account_id': str(account_id),
                                                            'folder_id' : str(foder_id_save2), 
                                                        }

                                                        files_save = {
                                                            'file' : file_open
                                                        }    

                                                        result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName))
                                                        print ('result_save_file: ',result_save_file)
                                                        file_open.close()
                                                        os.remove(path2 + original_filename + "." + typefile)
                                                        list_result.append(result_save_file)

                                                    return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200   

                                                elif result_create_folder_private_sid['messageText']['status'] == 'ER':
                                                    return jsonify({'result':'OK','messageText':None,'messageER':list_result ,'status_Code':401}),401                               

                                    elif result_select_sub_folder['messageText']['status'] == 'OK':
                                        
                                        for l in range(len(result_select_sub_folder['messageText']['result'])):
                                            if result_select_sub_folder['messageText']['result'][l]['folder_name'] == 'paperless':
                                                print (result_select_sub_folder['messageText']['result'][l])
                                                print ('Yesssssssss')
                                                check = True
                                                folder_id_private_folder2 = result_select_sub_folder['messageText']['result'][l]['folder_id']
                                                break
                                            elif result_select_sub_folder['messageText']['result'][l]['folder_name'] != 'paperless':
                                                print (result_select_sub_folder['messageText']['result'][l])
                                                folder_id_private_folder2 = result_select_sub_folder['messageText']['result'][l]['folder_id']
                                                print ('Noooooooo')
                                                check = False

                                        if check == True:
                                            print ('True')
                                            
                                            data_folder_id_attach = {
                                                'account_id': str(account_id),
                                                'folder_id' : str(folder_id_private_folder2)
                                            }

                                            result_select_sub_folder_attach = select_sub_folder_onebox(data_folder_id_attach,headers)
                                            print ('result_select_sub_folder_attach: ',result_select_sub_folder_attach)
                                            if result_select_sub_folder_attach['messageText']['status'] == 'ER':

                                                data_private_sub_folder_id2 = {
                                                    'account_id': str(account_id),
                                                    'parent_folder_id' : str(folder_id_private_folder2),
                                                    'folder_name' : 'attach_folder'
                                                }
                                                print ('folder_id_private_folder2: ',folder_id_private_folder2)
                                                result_create_folder_private2 = create_folder_onebox(data_private_sub_folder_id2,headers,token_header)
                                                print ('result_create_folderrrrr22222: ',result_create_folder_private2)

                                                folder_id_private_folder_sid = result_create_folder_private2['messageText']['data']['folder_id']
                                                data_private_sub_folder_id_sid = {
                                                    'account_id': str(account_id),
                                                    'parent_folder_id' : str(folder_id_private_folder_sid),
                                                    'folder_name' : result_select_doc_id
                                                }
                                                print ('folder_id_private_folder2: ',folder_id_private_folder_sid)
                                                result_create_folder_private_sid = create_folder_onebox(data_private_sub_folder_id_sid,headers,token_header)
                                                print ('result_create_folderrrrr3333: ',result_create_folder_private_sid)

                                            elif result_select_sub_folder_attach['messageText']['status'] == 'OK':
                                                folder_id_private_folder_sid = result_select_sub_folder_attach['messageText']['result'][0]['folder_id']
                                                data_private_sub_folder_id_sid = {
                                                    'account_id': str(account_id),
                                                    'parent_folder_id' : str(folder_id_private_folder_sid),
                                                    'folder_name' : result_select_doc_id
                                                }
                                                print ('folder_id_private_folder2: ',folder_id_private_folder_sid)
                                                result_create_folder_private_sid = create_folder_onebox(data_private_sub_folder_id_sid,headers,token_header)
                                                print ('result_create_folderrrrr3333: ',result_create_folder_private_sid)

                                            foder_id_save2 = result_create_folder_private_sid['messageText']['data']['folder_id']
                                            print ('foder_id_save2: ',foder_id_save2)
                                            if result_create_folder_private_sid['messageText']['status'] == 'OK':

                                                print ('dddddddddddddddd')
                                                files = request.files.getlist("file[]")
                                                unique_foldername = str(uuid.uuid4())
                                                path = './storage/temp/' + unique_foldername +'/'
                                                path2 = './storage/temp/'
                                                
                                                for file in files:
                                                    unique_filename = str(uuid.uuid4())
                                                    original_filename = str(file.filename).split('.')[0]
                                                    check_thai = pythainlp.util.isthai(original_filename)
                                                    if check_thai == True:
                                                        original_filename = romanize(original_filename, engine="thai2rom")

                                                    file_string = base64.b64encode(file.read())
                                                    typefile = str(file.filename).split('.')[-1]
                                                    typefile = typefile.split('"')[0]
                                                    with open(path2 + original_filename + "." + typefile, "wb") as fh:
                                                        file_open = fh 
                                                        fh.write(base64.decodebytes(file_string))
                                                        list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                                    file_open = open(path2 + original_filename + "." + typefile, "rb")

                                                    data_save_file = {
                                                        'account_id': str(account_id),
                                                        'folder_id' : str(foder_id_save2), 
                                                    }

                                                    files_save = {
                                                        'file' : file_open
                                                    }    

                                                    result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName))
                                                    print ('result_save_file: ',result_save_file)
                                                    file_open.close()
                                                    os.remove(path2 + original_filename + "." + typefile)
                                                    list_result.append(result_save_file)

                                                return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200   

                                            elif result_create_folder_private_sid['messageText']['status'] == 'ER':
                                                return jsonify({'result':'OK','messageText':None,'messageER':list_result ,'status_Code':401}),401
                                        
                                        elif check == False:       
                                            print ('False')                                   
                                            # Create paperless folder in โฟลเดอร์ส่วนตัว
                                            data_private_sub_folder_id = {
                                                'account_id': str(account_id),
                                                'parent_folder_id' : str(folder_id_private_folder),
                                                'folder_name' : 'paperless'
                                            }

                                            result_create_folder_private = create_folder_onebox(data_private_sub_folder_id,headers,token_header)
                                            print ('result_create_folderrrrrrrrrrrrrrrr: ',result_create_folder_private)
                                            folder_id_private_folder2 = result_create_folder_private['messageText']['data']['folder_id']
                                            print ('folder_id_private_folder2: ',folder_id_private_folder2)

                                            
                                            data_private_sub_folder_id2 = {
                                                'account_id': str(account_id),
                                                'parent_folder_id' : str(folder_id_private_folder2),
                                                'folder_name' : 'attach_folder'
                                            }

                                            result_create_folder_private2 = create_folder_onebox(data_private_sub_folder_id2,headers,token_header)
                                            print ('result_create_folderrrrr22222: ',result_create_folder_private2)
                                            
                                            if result_create_folder_private2['messageText']['status'] == 'OK':
                                                folder_id_private_folder_sid = result_create_folder_private2['messageText']['data']['folder_id']
                                                data_private_sub_folder_id_sid = {
                                                    'account_id': str(account_id),
                                                    'parent_folder_id' : str(folder_id_private_folder_sid),
                                                    'folder_name' : result_select_doc_id
                                                }
                                                print ('folder_id_private_folder2: ',folder_id_private_folder_sid)
                                                result_create_folder_private_sid = create_folder_onebox(data_private_sub_folder_id_sid,headers)
                                                print ('result_create_folderrrrr3333: ',result_create_folder_private_sid)

                                            
                                            folder_id_save = result_create_folder_private_sid['messageText']['data']['folder_id']
                                            

                                            if result_create_folder_private_sid['messageText']['status'] == 'OK':

                                                print ('dddddddddddddddd')
                                                files = request.files.getlist("file[]")
                                                unique_foldername = str(uuid.uuid4())
                                                path = './storage/temp/' + unique_foldername +'/'
                                                path2 = './storage/temp/'
                                                
                                                for file in files:
                                                    unique_filename = str(uuid.uuid4())
                                                    original_filename = str(file.filename).split('.')[0]
                                                    check_thai = pythainlp.util.isthai(original_filename)
                                                    if check_thai == True:
                                                        original_filename = romanize(original_filename, engine="thai2rom")

                                                    file_string = base64.b64encode(file.read())
                                                    typefile = str(file.filename).split('.')[-1]
                                                    typefile = typefile.split('"')[0]
                                                    with open(path2 + original_filename + "." + typefile, "wb") as fh:
                                                        file_open = fh 
                                                        fh.write(base64.decodebytes(file_string))
                                                        list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                                    file_open = open(path2 + original_filename + "." + typefile, "rb")

                                                    data_save_file = {
                                                        'account_id': str(account_id),
                                                        'folder_id' : str(folder_id_save), 
                                                    }

                                                    files_save = {
                                                        'file' : file_open
                                                    }    

                                                    result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName))
                                                    print ('result_save_file: ',result_save_file)
                                                    file_open.close()
                                                    os.remove(path2 + original_filename + "." + typefile)
                                                    list_result.append(result_save_file)

                                                return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200   

                                            elif result_create_folder_private_sid['messageText']['status'] == 'ER':
                                                return jsonify({'result':'OK','messageText':None,'messageER':list_result ,'status_Code':200}),200
                                           
                        else:
                            return jsonify({'result':'OK','messageText':None,'messageER':'tax_id is not found' ,'status_Code':200}),200        
                    elif result_select_account_id['messageText']['status'] == 'ER':
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        return jsonify({'result':'ER','messageText':None,'messageER':result_select_account_id['messageText']['errorMessage'],'status_Code':200}),200                    
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    return jsonify({'result':'ER','messageText':str(e),'status_Code':200,'service':'oneid'}),200
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':str(e),'data':[]},'status_Code':401}),401        

    if type_api == 'push':
        if request.method == 'POST':
            dataFiles = request.files
            dataForm = request.form
            check = True
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
            st2 = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
            unique_foldername = str(uuid.uuid4())
            list_result = []
            list_file_name = []
            if 'folder_name' in dataForm and 'username' in dataForm and 'tax_id' in dataForm:
                folder_name = dataForm['folder_name']
                data_userName = dataForm['username']
                tax_id = dataForm['tax_id']
                if str(folder_name).replace(' ','') != "":
                    if 'file[]' in dataFiles:
                        files = request.files.getlist("file[]")
                        print ('ggggggggggggggggggggggggg')
                        try:
                            headers = {
                                'Authorization': token_onebox
                            }
                            data = {
                                'user_id': str(user_id)
                            }
                            result_select_account_id = select_account_id_onebox(data,headers)
                            print (result_select_account_id)
                            if result_select_account_id['status'] == 'OK':
                                for i in range(len(result_select_account_id['result'])):
                                    if tax_id != '':
                                        if result_select_account_id['result'][i]['taxid'] == tax_id:
                                            account_id = result_select_account_id['result'][i]['account_id']
                                            tax_id_onebox = result_select_account_id['result'][i]['taxid']
                                            print ('account_id: ',account_id)
                                            print ('tax_id_onebox: ',tax_id_onebox)
                                            print (result_select_account_id['result'][i]['account_name'])
                                    elif tax_id == '':
                                        if result_select_account_id['result'][i]['taxid'] == None:
                                            account_id = result_select_account_id['result'][i]['account_id']
                                            tax_id_onebox = tax_id
                                            print ('account_id: ',account_id)
                                            print ('tax_id_onebox: ',tax_id_onebox)
                                            print (result_select_account_id['result'][i]['account_name'])

                                if tax_id_onebox != None and account_id != None:
                                    # GET folder จาก account_id
                                    data_account_id = {
                                        'account_id': str(account_id)
                                    }
                                    result_select_folder = select_folder_onebox(data_account_id,headers)
                                    print ('result_select_folder: ',result_select_folder)
                                    if tax_id_onebox != '':
                                        result_select_biztax = select_3().select_BizProfile_for_onebox(tax_id_onebox)
                                    
                                        if result_select_biztax['result'] == 'OK':
                                            eval_result_select_biztax = eval(result_select_biztax['messageText'][0])
                                            biz_foldername = eval_result_select_biztax['first_name_th']
                                            print ('biz_foldername: ',biz_foldername)
                                            for j in range(len(result_select_folder['result'])):
                                                if result_select_folder['result'][j]['folder_name'] == biz_foldername:
                                                    folder_id = result_select_folder['result'][j]['folder_id']
                                                    print ('folder_use: ',result_select_folder['result'][j])
                                                    print ('folder_id: ',folder_id)

                                            # Get sub_folder
                                        data_folder_id = {
                                            'account_id': str(account_id),
                                            'folder_id' : str(folder_id)
                                        }

                                        
                                        result_select_sub_folder = select_sub_folder_onebox(data_folder_id,headers)
                                        print('result_select_sub_folder11111: ',result_select_sub_folder)
                                        if result_select_sub_folder['status'] == 'OK':

                                            for m in range(len(result_select_sub_folder['result'])):

                                                if result_select_sub_folder['result'][m]['folder_name'] == 'paperless':
                                                    print (result_select_sub_folder['result'][m])
                                                    print ('Yesssssssss')
                                                    check = True
                                                    sub_folder_id = result_select_sub_folder['result'][m]['folder_id']
                                                    break
                                                elif result_select_sub_folder['result'][m]['folder_name'] != 'paperless':
                                                    print (result_select_sub_folder['result'][m])
                                                    sub_folder_id = result_select_sub_folder['result'][m]['folder_id']
                                                    print ('Noooooooo')
                                                    check = False
                                          
                                            if check == True:
                                                print (check)
                                                # Get sub_folder2
                                                data_folder_id2 = {
                                                'account_id': str(account_id),
                                                'folder_id' : str(sub_folder_id)
                                                }

                                                result_select_sub_folder2 = select_sub_folder_onebox(data_folder_id2,headers)
                                                if result_select_sub_folder2['status'] == 'OK':
                                                    print ('result_select_sub_folder2: ',result_select_sub_folder2)
                                                    sub_folder_id2 = result_select_sub_folder2['result'][0]['folder_id']
                                                    print ('sub_folder_id2: ',sub_folder_id2)
                                                    
                                                    #Get sub folder3
                                                    data_folder_id3 = {
                                                    'account_id': str(account_id),
                                                    'folder_id' : str(sub_folder_id2)
                                                    }

                                                    result_select_sub_folder3 = select_sub_folder_onebox(data_folder_id3,headers)
                                                    if result_select_sub_folder3['status'] == 'OK':
                                                        print ('result_select_sub_folder3: ',result_select_sub_folder3)
                                                       
                                                        for n in range(len(result_select_sub_folder3['result'])):
                                                            print ('folder_name: ',folder_name)
                                                            if result_select_sub_folder3['result'][n]['folder_name'] == folder_name:
                                                                print (result_select_sub_folder3['result'][n])
                                                                print ('Yesssssssss')
                                                                check = True
                                                                sub_folder_id = result_select_sub_folder3['result'][n]['folder_id']
                                                                break
                                                            elif result_select_sub_folder3['result'][n]['folder_name'] != folder_name:
                                                                print (result_select_sub_folder3['result'][n])
                                                                sub_folder_id = result_select_sub_folder3['result'][n]['folder_id']
                                                                print ('Noooooooo')
                                                                check = False

                                                
                                                        if check == True:
                                                            print ('dddddddddddddddd')
                                                            files = request.files.getlist("file[]")
                                                            unique_foldername = str(uuid.uuid4())
                                                            path = './storage/temp/' + unique_foldername +'/'
                                                            path2 = './storage/temp/'
                                                            
                                                            for file in files:
                                                                unique_filename = str(uuid.uuid4())
                                                                original_filename = str(file.filename).split('.')[0]
                                                                check_thai = pythainlp.util.isthai(original_filename)
                                                                if check_thai == True:
                                                                    original_filename = romanize(original_filename, engine="thai2rom")

                                                                file_string = base64.b64encode(file.read())
                                                                typefile = str(file.filename).split('.')[-1]
                                                                typefile = typefile.split('"')[0]
                                                                with open(path2 + original_filename + "." + typefile, "wb") as fh:
                                                                    file_open = fh 
                                                                    fh.write(base64.decodebytes(file_string))
                                                                    list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                                                file_open = open(path2 + original_filename + "." + typefile, "rb")

                                                                data_save_file = {
                                                                    'account_id': str(account_id),
                                                                    'folder_id' : str(sub_folder_id), 
                                                                }

                                                                files_save = {
                                                                    'file' : file_open
                                                                }    

                                                                result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName))
                                                                print ('result_save_file: ',result_save_file)
                                                                file_open.close()
                                                                os.remove(path2 + original_filename + "." + typefile)
                                                                list_result.append(result_save_file)

                                                            return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200   
                                                        
                                                        elif check == False:
                                                            return jsonify({'result':'ER','messageText':None,'messageER':'Not found folder' ,'status_Code':401}),401  

                                                    elif result_select_sub_folder3['status'] == 'ER':
                                                        return jsonify({'result':'ER','messageText':None,'messageER':'Not found folder' ,'status_Code':401}),401  
                                
                                    elif tax_id_onebox == '':
                                        print ('HRYYYYYYYYYYYYYYY: ',result_select_folder['result'])
                                        for k in range(len(result_select_folder['result'])):
                                            if (result_select_folder['result'][k]['folder_name'] == 'โฟลเดอร์ส่วนตัว'):
                                                folder_id_private_folder = result_select_folder['result'][k]['folder_id']
                                                print('folder_id_private_folder: ', folder_id_private_folder)
                                        # GET folder paperless
                                        data_folder_id = {
                                            'account_id': str(account_id),
                                            'folder_id' : str(folder_id_private_folder)
                                        }
                                        
                                        result_select_sub_folder = select_sub_folder_onebox(data_folder_id,headers)
                                        print ('result_select_sub_folder: ',result_select_sub_folder)
                                    
                                        for l in range(len(result_select_sub_folder['result'])):
                                            if result_select_sub_folder['result'][l]['folder_name'] == 'paperless':
                                                print (result_select_sub_folder['result'][l])
                                                print ('Yesssssssss')
                                                check = True
                                                folder_id_private_folder2 = result_select_sub_folder['result'][l]['folder_id']
                                                break
                                            elif result_select_sub_folder['result'][l]['folder_name'] != 'paperless':
                                                print (result_select_sub_folder['result'][l])
                                                folder_id_private_folder2 = result_select_sub_folder['result'][l]['folder_id']
                                                print ('Noooooooo')
                                                check = False
                                                return jsonify({'result':'ER','messageText':None,'messageER':'Not found folder','status_Code':401}),401        

                                        # GET folder attach_folder
                                        data_folder_id2 = {
                                            'account_id': str(account_id),
                                            'folder_id' : str(folder_id_private_folder2)
                                        }
                                        
                                        result_select_sub_folder2 = select_sub_folder_onebox(data_folder_id2,headers)
                                        print ('result_select_sub_folder2: ',result_select_sub_folder2)
                                        if result_select_sub_folder2['status'] == 'OK':
                                            
                                            for m in range(len(result_select_sub_folder2['result'])):
                                                if result_select_sub_folder2['result'][m]['folder_name'] == 'attach_folder':
                                                    print (result_select_sub_folder2['result'][m])
                                                    print ('Yesssssssss')
                                                    check = True
                                                    folder_id_private_folder3 = result_select_sub_folder2['result'][m]['folder_id']
                                                    break
                                                elif result_select_sub_folder2['result'][m]['folder_name'] != 'attach_folder':
                                                    print (result_select_sub_folder2['result'][m])
                                                    folder_id_private_folder3 = result_select_sub_folder2['result'][m]['folder_id']
                                                    print ('Noooooooo')
                                                    check = False
                                                    return jsonify({'result':'ER','messageText':None,'messageER':'Not found folder','status_Code':401}),401

                                        
                                            # GET folder tax
                                            data_folder_id3 = {
                                                'account_id': str(account_id),
                                                'folder_id' : str(folder_id_private_folder3)
                                            }
                                        
                                            result_select_sub_folder3 = select_sub_folder_onebox(data_folder_id3,headers)
                                            print ('result_select_sub_folder3: ',result_select_sub_folder3)
                                            
                                            if result_select_sub_folder3['status'] == 'OK':
                                                for n in range(len(result_select_sub_folder3['result'])):
                                                    if result_select_sub_folder3['result'][n]['folder_name'] == folder_name:
                                                        print (result_select_sub_folder3['result'][n])
                                                        print ('Yesssssssss')
                                                        check = True
                                                        sub_folder_id = result_select_sub_folder3['result'][n]['folder_id']
                                                        break
                                                    elif result_select_sub_folder3['result'][n]['folder_name'] != folder_name:
                                                        print (result_select_sub_folder3['result'][n])
                                                        sub_folder_id = result_select_sub_folder3['result'][n]['folder_id']
                                                        print ('Noooooooo')
                                                        check = False

                                                if check == True:
                                                    print ('dddddddddddddddd')
                                                    files = request.files.getlist("file[]")
                                                    unique_foldername = str(uuid.uuid4())
                                                    path = './storage/temp/' + unique_foldername +'/'
                                                    path2 = './storage/temp/'
                                                    
                                                    for file in files:
                                                        unique_filename = str(uuid.uuid4())
                                                        original_filename = str(file.filename).split('.')[0]
                                                        check_thai = pythainlp.util.isthai(original_filename)
                                                        if check_thai == True:
                                                            original_filename = romanize(original_filename, engine="thai2rom")

                                                        file_string = base64.b64encode(file.read())
                                                        typefile = str(file.filename).split('.')[-1]
                                                        typefile = typefile.split('"')[0]
                                                        with open(path2 + original_filename + "." + typefile, "wb") as fh:
                                                            file_open = fh 
                                                            fh.write(base64.decodebytes(file_string))
                                                            list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                                        file_open = open(path2 + original_filename + "." + typefile, "rb")

                                                        data_save_file = {
                                                            'account_id': str(account_id),
                                                            'folder_id' : str(sub_folder_id), 
                                                        }

                                                        files_save = {
                                                            'file' : file_open
                                                        }    

                                                        result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName))
                                                        print ('result_save_file: ',result_save_file)
                                                        file_open.close()
                                                        os.remove(path2 + original_filename + "." + typefile)
                                                        list_result.append(result_save_file)

                                                    return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200   

                                                elif check == False:
                                                    return jsonify({'result':'ER','messageText':None,'messageER':'Not found folder','status_Code':401}),401        

                                                # elif result_create_folder['status'] == 'ER':
                                                #     return jsonify({'result':'OK','messageText':None,'messageER':list_result ,'status_Code':401}),401  
                                            else:
                                                return jsonify({'result':'ER','messageText':None,'messageER':'Not found folder','status_Code':401}),401        
                                        else:
                                            return jsonify({'result':'ER','messageText':None,'messageER':'Not found folder','status_Code':401}),401        
                
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print(exc_type, fname, exc_tb.tb_lineno)
                            db.session.rollback()
                            raise
                            return jsonify({'result':'ER','messageText':None,'messageER':{'message':str(e),'data':[]},'status_Code':401}),401  

@status_methods.route('/storage/v3/<string:type_api>',methods=['POST'])
# @token_required
def onebox_save_file_api_v3(type_api):
    try:
        token_header = request.headers['Authorization']
        try:
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
    except KeyError as ex:
        return redirect(url_paperless)
    try:
        token_header = 'Bearer ' + token_header
        result_verify = verify().verify_one_id(token_header)
        if result_verify['result'] != 'OK':
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        result_verify_json = (result_verify['messageText']).json()
        user_id = result_verify_json['biz_detail'][0]['account_id']            
    except Exception as e:
        return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401        
    if type_api == 'keep':
        if request.method == 'POST':
            try:
                dataForm = request.form
                dataFiles = request.files
                if len(dataForm) == 0:
                    return jsonify({'result':'ER','messageText':None,'messageER':'parameter incorrect' ,'status_Code':404}),404
                tax_id_onebox = None
                account_id = None
                list_file_name = []
                list_result = []
                tax_id = dataForm['tax_id']
                sid = dataForm['sid']
                data_userName = dataForm['username']
                # files = request.files.getlist("file[]")
                check = True
                ts = int(time.time())
                st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                st2 = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
                # GET account_id จาก oneid
                try:
                    headers = {
                        'Authorization': token_onebox
                    }
                    data = {
                        'user_id': str(user_id)
                    }
                    result_select_account_id = select_account_id_onebox(data,headers,token_header)
                    result_select_doc_id = select_3().select_doc_id_onebox(sid)
                    doc_id = str(result_select_doc_id).split('\'')[1]
                    print(result_select_account_id)
                    if result_select_account_id['messageText']['status'] == 'OK':
                        for i in range(len(result_select_account_id['messageText']['result'])):
                            if tax_id != '':
                                if result_select_account_id['messageText']['result'][i]['taxid'] == tax_id:
                                    account_id = result_select_account_id['messageText']['result'][i]['account_id']
                                    tax_id_onebox = result_select_account_id['messageText']['result'][i]['taxid']
                            elif tax_id == '':
                                if result_select_account_id['messageText']['result'][i]['taxid'] == None:
                                    account_id = result_select_account_id['messageText']['result'][i]['account_id']
                                    tax_id_onebox = tax_id
                        if tax_id_onebox != None and account_id != None:
                            # GET folder จาก account_id
                            data_account_id = {
                                'account_id': str(account_id)
                            }
                            result_select_folder = select_folder_onebox(account_id,data_account_id,headers,token_header)
                            if tax_id_onebox != '':
                                result_select_biztax = select().select_BizProfile_for_onebox(tax_id_onebox)
                                if result_select_biztax['result'] == 'OK':
                                    eval_result_select_biztax = eval(result_select_biztax['messageText'][0])
                                    biz_foldername = eval_result_select_biztax['first_name_th']
                                    for j in range(len(result_select_folder['messageText']['result'])):
                                        if result_select_folder['messageText']['result'][j]['folder_name'] == biz_foldername:
                                            folder_id = result_select_folder['messageText']['result'][j]['folder_id']
                                check_folder = check_file_in_file_attach(folder_id,account_id,headers,doc_id,token_header)
                                if check_folder['result'] == 'OK':
                                    folder_id_docid = check_folder['messageText']
                                    files = request.files.getlist("file[]")
                                    unique_foldername = str(uuid.uuid4())
                                    path = './storage/temp/' + unique_foldername +'/'
                                    path2 = './storage/temp/'
                                    for file in files:
                                        unique_filename = str(uuid.uuid4())
                                        original_filename = str(file.filename).split('.')[0]
                                        file_string = base64.b64encode(file.read())
                                        typefile = str(file.filename).split('.')[-1]
                                        typefile = typefile.split('"')[0]
                                        with open(path2 + original_filename + "." + typefile, "wb") as fh:
                                            file_open = fh 
                                            fh.write(base64.decodebytes(file_string))
                                            list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                        file_open = open(path2 + original_filename + "." + typefile, "rb")
                                        data_save_file = {
                                            'account_id': str(account_id),
                                            'folder_id' : str(folder_id_docid), 
                                        }

                                        files_save = {
                                            'file' : file_open
                                        }    
                                        result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName),token_header)
                                        file_open.close()
                                        # os.remove(path2 + original_filename + "." + typefile)
                                        list_result.append(result_save_file)
                                    return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200   
                                elif check_folder['result'] == 'ER':
                                    return {'result':'ER','messageText':None,'messageER':check_folder['messageText'],'status_Code':200}
                            elif tax_id_onebox == '':
                                    for k in range(len(result_select_folder['messageText']['result'])):
                                        if (result_select_folder['messageText']['result'][k]['folder_name'] == 'โฟลเดอร์ส่วนตัว'):
                                            folder_id_private_folder = result_select_folder['messageText']['result'][k]['folder_id']
                                    check_folder = check_file_in_file_attach(folder_id_private_folder,account_id,headers,doc_id,token_header)
                                    if check_folder['result'] == 'OK':
                                        folder_id_docid = check_folder['messageText']
                                        files = request.files.getlist("file[]")
                                        unique_foldername = str(uuid.uuid4())
                                        path = './storage/temp/' + unique_foldername +'/'
                                        path2 = './storage/temp/'
                                        for file in files:
                                            unique_filename = str(uuid.uuid4())
                                            original_filename = str(file.filename).split('.')[0]
                                            file_string = base64.b64encode(file.read())
                                            typefile = str(file.filename).split('.')[-1]
                                            typefile = typefile.split('"')[0]
                                            with open(path2 + original_filename + "." + typefile, "wb") as fh:
                                                file_open = fh 
                                                fh.write(base64.decodebytes(file_string))
                                                list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                            file_open = open(path2 + original_filename + "." + typefile, "rb")
                                            data_save_file = {
                                                'account_id': str(account_id),
                                                'folder_id' : str(folder_id_docid), 
                                            }
                                            files_save = {
                                                'file' : file_open
                                            }    
                                            result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName),token_header)
                                            file_open.close()
                                            # os.remove(path2 + original_filename + "." + typefile)
                                            list_result.append(result_save_file)
                                        return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200   
                                    elif check_folder['result'] == 'ER':
                                        return {'result':'ER','messageText':None,'messageER':check_folder['messageText'],'status_Code':200}                                       
                        else:
                            return jsonify({'result':'OK','messageText':None,'messageER':'tax_id is not found' ,'status_Code':200}),200        
                    elif result_select_account_id['messageText']['status'] == 'ER':
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        return jsonify({'result':'ER','messageText':None,'messageER':result_select_account_id['messageText']['errorMessage'],'status_Code':200}),200                    
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    return jsonify({'result':'ER','messageText':str(e),'status_Code':200,'service':'oneid'}),200
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':str(e),'data':[]},'status_Code':404}),404        
    if type_api == 'push':
        if request.method == 'POST':
            dataFiles = request.files
            dataForm = request.form
            check = True
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
            st2 = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
            unique_foldername = str(uuid.uuid4())
            list_result = []
            list_file_name = []
            if 'folder_name' in dataForm and 'username' in dataForm and 'tax_id' in dataForm:
                folder_name = dataForm['folder_name']
                data_userName = dataForm['username']
                tax_id = dataForm['tax_id']
                if str(folder_name).replace(' ','') != "":
                    if 'file[]' in dataFiles:
                        files = request.files.getlist("file[]")
                        try:
                            headers = {
                                'Authorization': token_onebox
                            }
                            data = {
                                'user_id': str(user_id)
                            }
                            result_select_account_id = select_account_id_onebox(data,headers,token_header)
                            if result_select_account_id['messageText']['status'] == 'OK':
                                for i in range(len(result_select_account_id['result'])):
                                    if tax_id != '':
                                        if result_select_account_id['messageText']['result'][i]['taxid'] == tax_id:
                                            account_id = result_select_account_id['messageText']['result'][i]['account_id']
                                            tax_id_onebox = result_select_account_id['messageText']['result'][i]['taxid']
                                    elif tax_id == '':
                                        if result_select_account_id['messageText']['result'][i]['taxid'] == None:
                                            account_id = result_select_account_id['messageText']['result'][i]['account_id']
                                            tax_id_onebox = tax_id
                                if tax_id_onebox != None and account_id != None:
                                    # GET folder จาก account_id
                                    data_account_id = {
                                        'account_id': str(account_id)
                                    }
                                    result_select_folder = select_folder_onebox(account_id,data_account_id,headers,token_header)
                                    if tax_id_onebox != '':
                                        result_select_biztax = select().select_BizProfile_for_onebox(tax_id_onebox)
                                        if result_select_biztax['result'] == 'OK':
                                            eval_result_select_biztax = eval(result_select_biztax['messageText'][0])
                                            biz_foldername = eval_result_select_biztax['first_name_th']
                                            for j in range(len(result_select_folder['messageText']['result'])):
                                                if result_select_folder['messageText']['result'][j]['folder_name'] == biz_foldername:
                                                    folder_id = result_select_folder['messageText']['result'][j]['folder_id']
                                        check_folder = check_file_in_file_attach(folder_id,account_id,headers,folder_name,token_header) 
                                        if check_folder['result'] == 'OK':
                                            folder_id_docid = check_folder['messageText']
                                            files = request.files.getlist("file[]")
                                            unique_foldername = str(uuid.uuid4())
                                            path = './storage/temp/' + unique_foldername +'/'
                                            path2 = './storage/temp/'
                                            for file in files:
                                                unique_filename = str(uuid.uuid4())
                                                original_filename = str(file.filename).split('.')[0]
                                                file_string = base64.b64encode(file.read())
                                                typefile = str(file.filename).split('.')[-1]
                                                typefile = typefile.split('"')[0]
                                                with open(path2 + original_filename + "." + typefile, "wb") as fh:
                                                    file_open = fh 
                                                    fh.write(base64.decodebytes(file_string))
                                                    list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                                file_open = open(path2 + original_filename + "." + typefile, "rb")

                                                data_save_file = {
                                                    'account_id': str(account_id),
                                                    'folder_id' : str(folder_id_docid), 
                                                }

                                                files_save = {
                                                    'file' : file_open
                                                }    
                                                result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName),token_header)
                                                file_open.close()
                                                os.remove(path2 + original_filename + "." + typefile)
                                                list_result.append(result_save_file)
                                            return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200   
                                        elif check_folder['result'] == 'ER':
                                            return {'result':'ER','messageText':None,'messageER':check_folder['messageText'],'status_Code':200}
                                    elif tax_id_onebox == '':
                                        for k in range(len(result_select_folder['messageText']['result'])):
                                            if (result_select_folder['messageText']['result'][k]['folder_name'] == 'โฟลเดอร์ส่วนตัว'):
                                                folder_id_private_folder = result_select_folder['messageText']['result'][k]['folder_id']
                                        check_folder = check_file_in_file_attach(folder_id_private_folder,account_id,headers,folder_name,token_header)
                                        if check_folder['result'] == 'OK':
                                            folder_id_docid = check_folder['messageText']
                                            files = request.files.getlist("file[]")
                                            unique_foldername = str(uuid.uuid4())
                                            path = './storage/temp/' + unique_foldername +'/'
                                            path2 = './storage/temp/'
                                            for file in files:
                                                unique_filename = str(uuid.uuid4())
                                                original_filename = str(file.filename).split('.')[0]
                                                file_string = base64.b64encode(file.read())
                                                typefile = str(file.filename).split('.')[-1]
                                                typefile = typefile.split('"')[0]
                                                with open(path2 + original_filename + "." + typefile, "wb") as fh:
                                                    file_open = fh 
                                                    fh.write(base64.decodebytes(file_string))
                                                    list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                                file_open = open(path2 + original_filename + "." + typefile, "rb")
                                                data_save_file = {
                                                    'account_id': str(account_id),
                                                    'folder_id' : str(folder_id_docid), 
                                                }
                                                files_save = {
                                                    'file' : file_open
                                                }    
                                                result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName),token_header)
                                                file_open.close()
                                                os.remove(path2 + original_filename + "." + typefile)
                                                list_result.append(result_save_file)
                                            return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200   
                                        elif check_folder['result'] == 'ER':
                                            return {'result':'ER','messageText':None,'messageER':check_folder['messageText'],'status_Code':200}        
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'messageER':'Not found folder','status_Code':200}),200        
                                else:
                                    return jsonify({'result':'ER','messageText':None,'messageER':'Not found folder','status_Code':200}),200        
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print(exc_type, fname, exc_tb.tb_lineno)
                            return jsonify({'result':'ER','messageText':None,'messageER':{'message':str(e),'data':[]},'status_Code':401}),401  

def html_pdf_to_convert(tmp_html_text,tmp_landscape,tmpid_process,group_id):
    try:
        unique_foldername = str(uuid.uuid4())
        html_name = str(uuid.uuid4())
        html_name_file = html_name + '.html'
        path = path_global_1 + '/temp/' + unique_foldername +'/'
        path_indb = '/temp/' + unique_foldername + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        path_save = path  + html_name_file
        path_save_01 = path_indb  + html_name_file
        with open(path_save ,"w",encoding='utf-8') as f:
            f.write(tmp_html_text)
        html_file = open(path_save,"rb")
        # print(path_save)
        files = {
            'file':html_file
        }
        payload = {
            'landscape':tmp_landscape
        }
        # convert_eform = 'https://eform.one.th/webservice'
        response = requests.request("POST", convert_eform+"/api/v4/convert_html_to_pdf", data = payload, files = files, verify = False)
        if response.status_code == 200 or response.status_code == 201:
            tmpjson = response.json()
            if tmpjson['result'] == 'OK':
                if 'message' in tmpjson:
                    tmpmessage = tmpjson['message']
                    tmp_pdfdata = tmpmessage['pdfData']
                    infojson = {
                        'data':tmp_pdfdata,
                        'message':'success'
                    }
                    print("200")
                    insert().insert_pdf_togroup_v1(group_id,tmp_pdfdata)
                    update_1().update_process_log_status_v2(tmpid_process,'HTMLCON','SUCCESS',str(infojson),None,None)
                    return [tmp_pdfdata,200]
        print("400")
        infojson = {
            'data':None,
            'message':'fail'
        }
        update_1().update_process_log_status_v2(tmpid_process,'HTMLCON','FAIL',str(infojson),None,None)
        return [None,400]
    except Exception as e:
        infojson = {
            'data':None,
            'message':'fail'
        }
        update_1().update_process_log_status_v2(tmpid_process,'HTMLCON','FAIL',str(infojson),None,None)
        return [str(e),400]

def process_coverpage_v1(tmp_html_text,tmp_landscape,group_id,tmpemail_one,token_header,dataJson,sign_string,tmpid_process):
    try:
        sign_position = dataJson['sign_position']
        unique_foldername = str(uuid.uuid4())
        html_name = str(uuid.uuid4())
        html_name_file = html_name + '.html'
        path = path_global_1 + '/temp/' + unique_foldername +'/'
        path_indb = '/temp/' + unique_foldername + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        path_save = path  + html_name_file
        path_save_01 = path_indb  + html_name_file
        with open(path_save ,"w",encoding='utf-8') as f:
            f.write(tmp_html_text)
        html_file = open(path_save,"rb")
        # print(path_save)
        files = {
            'file':html_file
        }
        payload = {
            'landscape':tmp_landscape
        }
        # convert_eform = 'https://eform.one.th/webservice'
        response = requests.request("POST", convert_eform+"/api/v4/convert_html_to_pdf", data = payload, files = files, verify = False)
        if response.status_code == 200 or response.status_code == 201:
            tmpjson = response.json()
            if tmpjson['result'] == 'OK':
                if 'message' in tmpjson:
                    tmpmessage = tmpjson['message']
                    tmp_pdfdata = tmpmessage['pdfData']
                    infojson = {
                        'data':tmp_pdfdata,
                        'message':'onprocess'
                    }
                    print("200")
                    insert().insert_pdf_togroup_v1(group_id,tmp_pdfdata)
                    res_list = credentials_list_v2("","","","","",token_header)
                    credentialId = res_list['msg']['credentials'][0]['credentialId']
                    res_authorize = credentials_authorize_v2(credentialId,"","","","","","","",token_header)
                    if res_authorize['result'] == 'OK':
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
                        res_signPdf = signing_pdfSigning_v3(tmp_pdfdata,sadData,"","","",type_certifyLevel,"","","","","","",token_header,sign_position,sign_string)
                        if res_signPdf['result'] == 'OK':
                            tmpPdfData = res_signPdf['msg']['pdfData']
                            infojson = {
                                'data':tmpPdfData,
                                'message':'success'
                            }
                            update_4().update_pdf_sign_group(group_id,tmpPdfData,tmpemail_one,sign_string)
                            convert_pdf_images_group(group_id,tmpPdfData)
                    update_1().update_process_log_status_v2(tmpid_process,'HTMLCON','SUCCESS',str(infojson),None,None)
                    return [tmp_pdfdata,200]
        print("400")
        infojson = {
            'data':None,
            'message':'fail'
        }
        update_1().update_process_log_status_v2(tmpid_process,'HTMLCON','FAIL',str(infojson),None,None)
        return [None,400]
    except Exception as e:
        print(str(e))
        infojson = {
            'data':None,
            'message':'fail'
        }
        update_1().update_process_log_status_v2(tmpid_process,'HTMLCON','FAIL',str(infojson),None,None)
        return [str(e),400]

@status_methods.route('/api/v1/convertpage_pro',methods=['POST'])
def convert_page_pro_api_v1():
    try:
        token_header = request.headers['Authorization']
    except KeyError as ex:
        return redirect(url_paperless)
    dataJson = request.json
    if 'html_text' in dataJson and 'landscape' in dataJson and 'group_id' in dataJson and 'sign_detail' in dataJson and 'email_one' in dataJson:
        tmphtml_text = dataJson['html_text']
        tmplandscape = dataJson['landscape']
        tmpgroup_id = dataJson['group_id']
        tmpsign_detail = dataJson['sign_detail']
        tmpemail_one = dataJson['email_one']
        tmpid_process = None
        url = "/api/v1/convertpage_pro"
        infojson = {
            'data':None,
            'message':'onprocess'
        }
        result_insert = insert_3().insert_process_request_v1('HTMLCON',str(infojson),url,tmpgroup_id,tmpemail_one)
        if result_insert['result'] == 'OK':
            tmpid_process = result_insert['messageText']['id']
        if 'Step_Num' in tmpsign_detail and 'max_Step' in tmpsign_detail and 'sign_position' in tmpsign_detail and 'sign_string' in tmpsign_detail:
            tmpStep_Num = tmpsign_detail['Step_Num']
            tmpmax_Step = tmpsign_detail['max_Step']
            tmpsign_position = tmpsign_detail['sign_position']
            tmpsign_string = tmpsign_detail['sign_string']
            executor.submit(process_coverpage_v1,tmphtml_text,tmplandscape,tmpgroup_id,tmpemail_one,token_header,tmpsign_detail,tmpsign_string,tmpid_process)
            return jsonify({'result':'OK','messageText':{'message':'on process','data':tmpid_process},'messageER':None,'status_Code':200}),200
    abort(404)

@status_methods.route('/api/v3/html_topdf',methods=['POST'])
def html_topdf_api_v3():
    dataJson = request.json
    if 'html_text' in dataJson and 'landscape' in dataJson and 'group_id' in dataJson:
        tmp_html_text = dataJson['html_text']
        tmp_landscape = dataJson['landscape']
        tmpgroup_id = dataJson['group_id']
        tmpid_process = None
        url = "/api/v1/html_topdf"
        infojson = {
            'data':None,
            'message':'onprocess'
        }
        result_insert = insert_3().insert_process_request_v1('HTMLCON',str(infojson),url,None,None)
        if result_insert['result'] == 'OK':
            tmpid_process = result_insert['messageText']['id']
        executor.submit(html_pdf_to_convert, tmp_html_text,tmp_landscape,tmpid_process,tmpgroup_id)
        return jsonify({'result':'OK','messageText':{'message':'on process','data':tmpid_process},'messageER':None,'status_Code':200}),200

@status_methods.route('/api/v1/html_topdf',methods=['POST'])
def html_topdf_api_v1():
    dataJson = request.json
    if 'html_text' in dataJson and 'landscape' in dataJson and len(dataJson) == 2:
        tmp_html_text = dataJson['html_text']
        tmp_landscape = dataJson['landscape']
        # tmpid_process = None
        # url = "/api/v1/html_topdf"
        # result_insert = insert_3().insert_process_request_v1('HTMLCON',None,url,None,None)
        # if result_insert['result'] == 'OK':
        #     tmpid_process = result_insert['messageText']['id']
        # executor.submit(html_pdf_to_convert, tmp_html_text,tmp_landscape,tmpid_process)
        # return jsonify({'result':'OK','messageText':{'message':'on process','data':tmpid_process},'messageER':None,'status_Code':200}),200
        unique_foldername = str(uuid.uuid4())
        html_name = str(uuid.uuid4())
        html_name_file = html_name + '.html'
        path = './temp/' + unique_foldername +'/'
        path_indb = '/temp/' + unique_foldername + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        path_save = path  + html_name_file
        path_save_01 = path_indb  + html_name_file
        with open(path_save ,"w",encoding='utf-8') as f:
            f.write(tmp_html_text)
        html_file = open(path_save,"rb")
        # print(path_save)
        files = {
            'file':html_file
        }
        payload = {
            'landscape':tmp_landscape
        }
        # convert_eform = 'https://eform.one.th/webservice'
        response = requests.request("POST", convert_eform+"/api/v4/convert_html_to_pdf", data = payload, files = files, verify = False)
        if response.status_code == 200 or response.status_code == 201:
            tmpjson = response.json()
            if tmpjson['result'] == 'OK':
                if 'message' in tmpjson:
                    tmpmessage = tmpjson['message']
                    tmp_pdfdata = tmpmessage['pdfData']
                    # cwd = os.getcwd()
                    # os.remove(cwd + path_save_01)
                    return jsonify({'result':'OK','messageText':{'data':tmp_pdfdata,'message':'success'},'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'fail','code':'ERCV001'},'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'fail','code':'ERCV002'},'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'fail','code':'ERCV999'},'status_Code':200}),200
    else:
        return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'parameter incorrect','code':'ERCV999'},'status_Code':404}),404

@status_methods.route('/storage/v4/<string:type_api>',methods=['POST'])
# @token_required
def onebox_save_file_api_v4(type_api):
    try:
        token_header = request.headers['Authorization']
        try:
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
    except KeyError as ex:
        return redirect(url_paperless)
    try:
        token_header = 'Bearer ' + token_header
        result_verify = verify().verify_one_id(token_header)
        if result_verify['result'] != 'OK':
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        result_verify_json = (result_verify['messageText']).json()
        user_id = result_verify_json['biz_detail'][0]['account_id']            
    except Exception as e:
        return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401        
    if type_api == 'keep':
        if request.method == 'POST':
            try:
                dataForm = request.form
                dataFiles = request.files
                if len(dataForm) == 0:
                    return jsonify({'result':'ER','messageText':None,'messageER':'parameter incorrect' ,'status_Code':404}),404
                tax_id_onebox = None
                account_id = None
                
                list_result = []
                tax_id = dataForm['tax_id']
                sid = dataForm['sid']
                data_userName = dataForm['username']
                # files = request.files.getlist("file[]")
                check = True
                ts = int(time.time())
                st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                st2 = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
                check_return = False
                # GET account_id จาก oneid
                try:
                    headers = {
                        'Authorization': token_onebox
                    }
                    data = {
                        'user_id': str(user_id)
                    }
                    result_select_account_id = select_account_id_onebox(data,headers,token_header)
                    result_select_doc_id = select_3().select_doc_id_onebox_v2(sid)
                    if result_select_doc_id['result'] == 'ER':
                        return jsonify({'result':'OK','messageText':None,'messageER':'invalid sid','status_Code':404}),404
                    result_dept = select_3().select_deptname_onebox(sid)
                    dept_name = result_dept['messageText']
                    # doc_id = str(result_select_doc_id).split('\'')[1]
                    doc_id = str(result_select_doc_id['messageText'])
                    doc_name_type = str(result_select_doc_id['messageText2'])
                    list_name_folder = [dept_name,doc_name_type]
                    Thai_foldername = ['แผนก','ประเภทเอกสาร']
                    if result_select_account_id['messageText']['status'] == 'OK':
                        for i in range(len(result_select_account_id['messageText']['result'])):
                            if tax_id != '':
                                if result_select_account_id['messageText']['result'][i]['taxid'] == tax_id:
                                    account_id = result_select_account_id['messageText']['result'][i]['account_id']
                                    tax_id_onebox = result_select_account_id['messageText']['result'][i]['taxid']
                            elif tax_id == '':
                                if result_select_account_id['messageText']['result'][i]['taxid'] == None:
                                    account_id = result_select_account_id['messageText']['result'][i]['account_id']
                                    tax_id_onebox = tax_id
                        if tax_id_onebox != None and account_id != None:
                            # GET folder จาก account_id
                            data_account_id = {
                                'account_id': str(account_id)
                            }
                            result_select_folder = select_folder_onebox(account_id,data_account_id,headers,token_header)
                            if tax_id_onebox != '':
                                result_select_biztax = select_3().select_BizProfile_for_onebox(tax_id_onebox)
                                if result_select_biztax['result'] == 'OK':
                                    eval_result_select_biztax = eval(result_select_biztax['messageText'][0])
                                    biz_foldername = eval_result_select_biztax['first_name_th']
                                    for j in range(len(result_select_folder['messageText']['result'])):
                                        if result_select_folder['messageText']['result'][j]['folder_name'] == biz_foldername:
                                            folder_id = result_select_folder['messageText']['result'][j]['folder_id']
                                files = request.files.getlist("file[]")
                                list_file_base = []
                                for file in files:
                                    file_string = base64.b64encode(file.read())
                                    list_file_base.append(file_string)
                                for c in range(len(list_name_folder)):
                                    num_count = 0
                                    list_file_name = []
                                    check_folder = check_file_in_file_attach_v2(folder_id,account_id,headers,doc_id,str(Thai_foldername[c]),str(list_name_folder[c]),token_header)
                                # check_folder = check_file_in_file_attach(folder_id,account_id,headers,doc_id,token_header)
                                    if check_folder['result'] == 'OK':
                                        folder_id_docid = check_folder['messageText']
                                        unique_foldername = str(uuid.uuid4())
                                        path = './storage/' + unique_foldername +'/'
                                        path2 = './storage/'
                                        path3 = './storage/' + unique_foldername
                                        if not os.path.exists(path):
                                            os.makedirs(path)
                                        for file in files:
                                            unique_filename = str(uuid.uuid4())
                                            original_filename = str(file.filename).split('.')[0]
                                            # file_string = base64.b64encode(file.read())
                                            typefile = str(file.filename).split('.')[-1]
                                            typefile = typefile.split('"')[0]
                                            with open(path + original_filename + "." + typefile, "wb") as fh:
                                                file_open = fh 
                                                fh.write(base64.decodebytes(list_file_base[num_count]))
                                            save_file_in_com(path,unique_filename,typefile,list_file_base[num_count])
                                                # fh.write(base64.decodebytes(file_string))
                                                # list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                            file_open = open(path + original_filename + "." + typefile, "rb")
                                            data_save_file = {
                                                'account_id': str(account_id),
                                                'folder_id' : str(folder_id_docid), 
                                            }
                                            files_save = {
                                                'file' : file_open
                                            }
                                            result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName),token_header)
                                            file_open.close()
                                            for y in range(len(result_save_file['messageText'])):
                                                list_file_name.append({'file_name_original':original_filename + "." + typefile,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st2),'file_id':result_save_file['messageText'][y]['file_id'],'username':data_userName})
                                            list_result.append(result_save_file['messageText'])
                                            num_count = num_count+1
                                            check_return = True
                                            os.remove(path + original_filename + "." + typefile)
                                        result_insert = insert().insert_transactionfile(list_file_name,path,unique_foldername)
                                        # shutil.rmtree(path3)
                                    elif check_folder['result'] == 'ER':
                                        check_return = False
                                if check_return == True:
                                    return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200 
                                elif check_return == False:
                                    return {'result':'ER','messageText':None,'messageER':check_folder['messageText'],'status_Code':200}
                            elif tax_id_onebox == '':
                                for k in range(len(result_select_folder['messageText']['result'])):
                                    if (result_select_folder['messageText']['result'][k]['folder_name'] == 'โฟลเดอร์ส่วนตัว'):
                                        folder_id_private_folder = result_select_folder['messageText']['result'][k]['folder_id']
                                files = request.files.getlist("file[]")
                                list_file_base = []
                                for file in files:
                                    file_string = base64.b64encode(file.read())
                                    list_file_base.append(file_string)
                                for c in range(len(list_name_folder)):
                                    num_count = 0
                                    list_file_name = []
                                    check_folder = check_file_in_file_attach_v2(folder_id_private_folder,account_id,headers,doc_id,str(Thai_foldername[c]),str(list_name_folder[c]),token_header)
                                # check_folder = check_file_in_file_attach(folder_id_private_folder,account_id,headers,doc_id,token_header)
                                    if check_folder['result'] == 'OK':
                                        folder_id_docid = check_folder['messageText']
                                        unique_foldername = str(uuid.uuid4())
                                        path = './storage/' + unique_foldername +'/'
                                        path2 = './storage/'
                                        path3 = './storage/' + unique_foldername
                                        if not os.path.exists(path):
                                            os.makedirs(path)
                                        for file in files:
                                            unique_filename = str(uuid.uuid4())
                                            original_filename = str(file.filename).split('.')[0]
                                            # file_string = base64.b64encode(file.read())
                                            typefile = str(file.filename).split('.')[-1]
                                            typefile = typefile.split('"')[0]
                                            with open(path + original_filename + "." + typefile, "wb") as fh:
                                                file_open = fh 
                                                # fh.write(base64.decodebytes(file_string))
                                                fh.write(base64.decodebytes(list_file_base[num_count]))
                                                # list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                            save_file_in_com(path,unique_filename,typefile,list_file_base[num_count])
                                            file_open = open(path + original_filename + "." + typefile, "rb")
                                            data_save_file = {
                                                'account_id': str(account_id),
                                                'folder_id' : str(folder_id_docid), 
                                            }
                                            files_save = {
                                                'file' : file_open
                                            }    
                                            result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName),token_header)
                                            file_open.close()
                                            for y in range(len(result_save_file['messageText'])):
                                                list_file_name.append({'file_name_original':original_filename + "." + typefile,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st2),'file_id':result_save_file['messageText'][y]['file_id'],'username':data_userName})
                                            list_result.append(result_save_file['messageText'])
                                            num_count = num_count+1
                                            check_return = True
                                            os.remove(path + original_filename + "." + typefile)
                                        result_insert = insert().insert_transactionfile(list_file_name,path,unique_foldername)
                                        # shutil.rmtree(path3)
                                    elif check_folder['result'] == 'ER':
                                        check_return = False
                                if check_return == True:
                                    return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200 
                                elif check_return == False:
                                    return {'result':'ER','messageText':None,'messageER':check_folder['messageText'],'status_Code':200}
                        else:
                            return jsonify({'result':'OK','messageText':None,'messageER':'tax_id is not found' ,'status_Code':200}),200        
                    elif result_select_account_id['messageText']['status'] == 'ER':
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        return jsonify({'result':'ER','messageText':None,'messageER':result_select_account_id['messageText']['errorMessage'],'status_Code':200}),200                    
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    return jsonify({'result':'ER','messageText':str(e),'status_Code':200,'service':'oneid'}),200
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':str(e),'data':[]},'status_Code':404}),404        
    if type_api == 'push':
        if request.method == 'POST':
            dataFiles = request.files
            dataForm = request.form
            check = True
            check_return = False
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
            st2 = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
            unique_foldername = str(uuid.uuid4())
            list_result = []
            
            if 'sid' in dataForm and 'username' in dataForm and 'tax_id' in dataForm:
                sid = dataForm['sid']
                data_userName = dataForm['username']
                tax_id = dataForm['tax_id']
                result_select_doc_id = select_3().select_doc_id_onebox_v2(sid)
                if result_select_doc_id['result'] == 'ER':
                    return jsonify({'result':'OK','messageText':None,'messageER':'invalid sid','status_Code':404}),404      
                result_dept = select_3().select_deptname_onebox(sid)
                dept_name = result_dept['messageText']
                doc_id = str(result_select_doc_id['messageText'])
                doc_name_type = str(result_select_doc_id['messageText2'])
                list_name_folder = [dept_name,doc_name_type]
                Thai_foldername = ['แผนก','ประเภทเอกสาร']
                if str(sid).replace(' ','') != "":
                    if 'file[]' in dataFiles:
                        files = request.files.getlist("file[]")
                        try:
                            headers = {
                                'Authorization': token_onebox
                            }
                            data = {
                                'user_id': str(user_id)
                            }
                            result_select_account_id = select_account_id_onebox(data,headers,token_header)
                            if result_select_account_id['messageText']['status'] == 'OK':
                                for i in range(len(result_select_account_id['result'])):
                                    if tax_id != '':
                                        if result_select_account_id['messageText']['result'][i]['taxid'] == tax_id:
                                            account_id = result_select_account_id['messageText']['result'][i]['account_id']
                                            tax_id_onebox = result_select_account_id['messageText']['result'][i]['taxid']
                                    elif tax_id == '':
                                        if result_select_account_id['messageText']['result'][i]['taxid'] == None:
                                            account_id = result_select_account_id['messageText']['result'][i]['account_id']
                                            tax_id_onebox = tax_id
                                if tax_id_onebox != None and account_id != None:
                                    # GET folder จาก account_id
                                    data_account_id = {
                                        'account_id': str(account_id)
                                    }
                                    result_select_folder = select_folder_onebox(account_id,data_account_id,headers,token_header)
                                    if tax_id_onebox != '':
                                        result_select_biztax = select_3().select_BizProfile_for_onebox(tax_id_onebox)
                                        if result_select_biztax['result'] == 'OK':
                                            eval_result_select_biztax = eval(result_select_biztax['messageText'][0])
                                            biz_foldername = eval_result_select_biztax['first_name_th']
                                            for j in range(len(result_select_folder['messageText']['result'])):
                                                if result_select_folder['messageText']['result'][j]['folder_name'] == biz_foldername:
                                                    folder_id = result_select_folder['messageText']['result'][j]['folder_id']
                                        files = request.files.getlist("file[]")
                                        list_file_base = []
                                        for file in files:
                                            file_string = base64.b64encode(file.read())
                                            list_file_base.append(file_string)
                                        for c in range(len(list_name_folder)):
                                            print (c)
                                            list_file_name = []
                                            num_count = 0
                                            check_folder = check_file_in_file_attach_v2(folder_id,account_id,headers,doc_id,str(Thai_foldername[c]),str(list_name_folder[c]),token_header)
                                        # check_folder = check_file_in_file_attach(folder_id,account_id,headers,folder_name,token_header) 
                                            if check_folder['result'] == 'OK':
                                                folder_id_docid = check_folder['messageText']
                                                unique_foldername = str(uuid.uuid4())
                                                path = './storage/' + unique_foldername +'/'
                                                path2 = './storage/'
                                                path3 = './storage/' + unique_foldername
                                                if not os.path.exists(path):
                                                    os.makedirs(path)
                                                for file in files:
                                                    unique_filename = str(uuid.uuid4())
                                                    original_filename = str(file.filename).split('.')[0]
                                                    # file_string = base64.b64encode(file.read())
                                                    typefile = str(file.filename).split('.')[-1]
                                                    typefile = typefile.split('"')[0]
                                                    with open(path + original_filename + "." + typefile, "wb") as fh:
                                                        file_open = fh 
                                                        fh.write(base64.decodebytes(list_file_base[num_count]))
                                                    save_file_in_com(path,unique_filename,typefile,list_file_base[num_count])
                                                    file_open = open(path + original_filename + "." + typefile, "rb")

                                                    data_save_file = {
                                                        'account_id': str(account_id),
                                                        'folder_id' : str(folder_id_docid), 
                                                    }

                                                    files_save = {
                                                        'file' : file_open
                                                    }    
                                                    result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName),token_header)
                                                    file_open.close()
                                                    for y in range(len(result_save_file['messageText'])):
                                                        list_file_name.append({'file_name_original':original_filename + "." + typefile,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st2),'file_id':result_save_file['messageText'][y]['file_id'],'username':data_userName})

                                                    list_result.append(result_save_file['messageText'])
                                                    num_count = num_count+1
                                                    check_return = True
                                                    os.remove(path + original_filename + "." + typefile)
                                                result_insert = insert().insert_transactionfile(list_file_name,path,unique_foldername)
                                                # shutil.rmtree(path3)
                                            elif check_folder['result'] == 'ER':
                                                check_return = False
                                        if check_return == True:
                                            return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200 
                                        elif check_return == False:
                                            return {'result':'ER','messageText':None,'messageER':check_folder['messageText'],'status_Code':200}
                                    elif tax_id_onebox == '':
                                        for k in range(len(result_select_folder['messageText']['result'])):
                                            if (result_select_folder['messageText']['result'][k]['folder_name'] == 'โฟลเดอร์ส่วนตัว'):
                                                folder_id_private_folder = result_select_folder['messageText']['result'][k]['folder_id']
                                        files = request.files.getlist("file[]")
                                        list_file_base = []
                                        for file in files:
                                            file_string = base64.b64encode(file.read())
                                            list_file_base.append(file_string)
                                        for c in range(len(list_name_folder)):
                                            print (c)
                                            num_count = 0
                                            list_file_name = []
                                            check_folder = check_file_in_file_attach_v2(folder_id_private_folder,account_id,headers,doc_id,str(Thai_foldername[c]),str(list_name_folder[c]),token_header)
                                        # check_folder = check_file_in_file_attach(folder_id_private_folder,account_id,headers,folder_name,token_header)
                                            if check_folder['result'] == 'OK':
                                                folder_id_docid = check_folder['messageText']
                                                unique_foldername = str(uuid.uuid4())
                                                path = './storage/' + unique_foldername +'/'
                                                path2 = './storage/'
                                                path3 = './storage/' + unique_foldername
                                                if not os.path.exists(path):
                                                    os.makedirs(path)
                                                for file in files:
                                                    unique_filename = str(uuid.uuid4())
                                                    original_filename = str(file.filename).split('.')[0]
                                                    # file_string = base64.b64encode(file.read())
                                                    typefile = str(file.filename).split('.')[-1]
                                                    typefile = typefile.split('"')[0]
                                                    with open(path + original_filename + "." + typefile, "wb") as fh:
                                                        file_open = fh 
                                                        # fh.write(base64.decodebytes(file_string))
                                                        fh.write(base64.decodebytes(list_file_base[num_count]))
                                                        # list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                                    save_file_in_com(path,unique_filename,typefile,list_file_base[num_count])
                                                    file_open = open(path + original_filename + "." + typefile, "rb")
                                                    data_save_file = {
                                                        'account_id': str(account_id),
                                                        'folder_id' : str(folder_id_docid), 
                                                    }
                                                    files_save = {
                                                        'file' : file_open
                                                    }    
                                                    result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,str(data_userName),token_header)
                                                    file_open.close()
                                                    for y in range(len(result_save_file['messageText'])):
                                                        list_file_name.append({'file_name_original':original_filename + "." + typefile,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st2),'file_id':result_save_file['messageText'][y]['file_id'],'username':data_userName})
                                                    list_result.append(result_save_file['messageText'])
                                                    num_count = num_count+1
                                                    check_return = True
                                                    os.remove(path + original_filename + "." + typefile)
                                                result_insert = insert().insert_transactionfile(list_file_name,path,unique_foldername)
                                                # shutil.rmtree(path3)
                                            elif check_folder['result'] == 'ER':
                                                check_return = False
                                        if check_return == True:
                                            return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200 
                                        elif check_return == False:
                                            return {'result':'ER','messageText':None,'messageER':check_folder['messageText'],'status_Code':200}      
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'messageER':'Not found folder','status_Code':200}),200        
                                else:
                                    return jsonify({'result':'ER','messageText':None,'messageER':'Not found folder','status_Code':200}),200        
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print(exc_type, fname, exc_tb.tb_lineno)
                            return jsonify({'result':'ER','messageText':None,'messageER':{'message':str(e),'data':[]},'status_Code':401}),401  

@status_methods.route('/api/v1/refAttach/<string:typestatus>',methods=['POST'])
def ref_AttachFile_api_v1(typestatus):
    try:
        token_header = request.headers['Authorization']
        try:
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            abort(401)
    except KeyError as ex:
        return redirect(url_paperless)
    print(typestatus)

@status_methods.route('/storage/v1/attach_file_onebox/<string:type_api>',methods=['POST'])
# @token_required
def attach_file_to_onebox(type_api): 
    try:
        token_header = request.headers['Authorization']
        try:                
            token_header = str(token_header).split(' ')[1]
            token_required = token_required_func(token_header)
            # username = token_required['username']
            # user_id = token_required['user_id']
        except Exception as ex:
            abort(401)
    except KeyError as ex:
        return redirect(url_paperless)
    try:
        if type_api == 'keep':
            # datajson = request.json
            dataForm = request.form
            if 'sid' in dataForm :
                sid = dataForm['sid']
                result_tax_id = select_2().select_tax_id_onebox_attach_file(sid)
                taxid = result_tax_id['messageText']
                doc_name_type = result_tax_id['messageText2']
                result_dept = select_3().select_deptname_onebox(sid)
                dept_name = result_dept['messageText']
                result_user = select().select_user_first(sid)
                if result_user['result'] == 'OK':
                    username_first = result_user['messageText']['username']
                    userid_first = result_user['messageText']['userid']
                    result_save_attach = get_attach_to_onebox(sid,username_first,userid_first,taxid,dept_name,doc_name_type,token_header) #เพิ่มใหม่
                    
                return jsonify({'result':'OK','messageText':result_save_attach['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
        elif type_api == 'push':
            dataForm = request.form
            dataFiles = request.files
            list_file = []
            list_name_file = []
            files = request.files.getlist("file[]")
            if 'sid' in dataForm :
                sid = dataForm['sid']
                result_tax_id = select_2().select_tax_id_onebox_attach_file(sid)
                taxid = result_tax_id['messageText']
                doc_name_type = result_tax_id['messageText2']
                result_dept = select_3().select_deptname_onebox(sid)
                dept_name = result_dept['messageText']
                result_user = select().select_user_first(sid)
                if result_user['result'] == 'OK':
                    username_first = result_user['messageText']['username']
                    userid_first = result_user['messageText']['userid']
                    for file in files:
                        file_string = (file.read())
                        original_filename = str(file.filename)
                        # print (type(file_string))
                        list_file.append(file_string)
                        list_name_file.append(original_filename)
                        # result_save_attach = get_attach_to_onebox_push(sid,username_first,userid_first,taxid,dept_name,doc_name_type,token_header,file_string,original_filename) #เพิ่มใหม่
                    result_save_attach = get_attach_to_onebox_push(sid,username_first,userid_first,taxid,dept_name,doc_name_type,token_header,list_file,list_name_file) #เพิ่มใหม่
                return jsonify({'result':'OK','messageText':result_save_attach['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
            
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':str(e)}

@status_methods.route('/storage/<string:type_api>/v2_old',methods=['POST'])
# @token_required
def keep_storage_v2_old(type_api):
    try:
        token_header = request.headers['Authorization']
        try:                
            token_header = str(token_header).split(' ')[1]
            token_required = token_required_func(token_header)
            # username = token_required['username']
            # user_id = token_required['user_id']
        except Exception as ex:
            abort(401)
    except KeyError as ex:
        return redirect(url_paperless)
    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
    size = None
    tmpsum_storage = 0
    list_file = []
    list_name_file = []
    if type_api == 'keep':
        if request.method == 'POST':
            dataFiles = request.files
            dataForm = request.form
            unique_foldername = str(uuid.uuid4())
            list_file_name = []
            path = path_global_1 + '/storage/' + unique_foldername + '/'
            path_indb = '/storage/' + unique_foldername +'/'
            # path = './storage/' + unique_foldername +'/'
            # path_indb = '/storage/' + unique_foldername +'/'
            if not os.path.exists(path):
                os.makedirs(path)
            if 'file[]' in dataFiles and 'username' in dataForm and 'sid' in dataForm:
                files = request.files.getlist("file[]")
                data_userName = dataForm['username']
                sid = dataForm['sid']
                for file in files:
                    unique_filename = str(uuid.uuid4())
                    tmpread = file.read()
                    file_string = base64.b64encode(tmpread)                                    
                    file_stringread = tmpread
                    size = str(len(file_stringread))
                    tmpsum_storage += len(file_stringread)
                    typefile = str(file.filename).split('.')[-1]
                    with open(path + unique_filename + "." + typefile, "wb") as fh:
                        files_to_box = base64.decodebytes(file_string)
                        original_filename = str(file.filename)
                        fh.write(base64.decodebytes(file_string))
                        list_file.append(files_to_box)
                        list_name_file.append(original_filename)
                        list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                attach_to_onebox = attach_file_to_onebox_v2(sid,list_file,list_name_file,token_header)
                result_Insert = insert().insert_transactionfile(list_file_name,path_indb,unique_foldername,tmpsum_storage)
                return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':unique_foldername,'file_name':list_file_name},'messageER':None,'status_Code':200}),200
                if result_Insert['result'] =='OK':
                    return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':unique_foldername,'file_name':list_file_name},'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'cant insert to db','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200})
    elif type_api == 'push':
        if request.method == 'POST':
            dataFiles = request.files
            dataForm = request.form
            unique_foldername = str(uuid.uuid4())
            list_file_name = []
            if 'folder_name' in dataForm and 'username' in dataForm and 'sid' in dataForm:
                folder_name = dataForm['folder_name']
                data_userName = dataForm['username']
                tmp_sid = dataForm['sid']
                if tmp_sid != '':
                    result_select = select().select_folder_name_attm_file_v1(tmp_sid)
                else:
                    if str(folder_name).replace(' ','') != "":
                        if 'file[]' in dataFiles:
                            files = request.files.getlist("file[]")
                            resultSelect = select().select_transactionfile(folder_name)
                            if resultSelect['result'] == 'OK':
                                list_arrfile = resultSelect['messageText']['json_data']
                                pathfolderindb = resultSelect['messageText']['pathfolder']
                                for file in files:
                                    path = path_global_1 + pathfolderindb
                                    path_indb = '/storage/' + unique_foldername +'/'
                                    # path = path_global_1 + '/storage/' + folder_name +'/'
                                    # path_indb = path_global_1 + '/storage/' + folder_name +'/'
                                    unique_filename = str(uuid.uuid4())
                                    tmpread = file.read()
                                    file_string = base64.b64encode(tmpread)                                    
                                    file_stringread = tmpread
                                    size = str(len(file_stringread))
                                    typefile = str(file.filename).split('.')[-1]
                                    files_to_box = base64.decodebytes(file_string)
                                    original_filename = str(file.filename)
                                    list_file.append(files_to_box)
                                    list_name_file.append(original_filename)
                                    try:
                                        with open(path + unique_filename + "." + typefile, "wb") as fh:
                                            fh.write(base64.decodebytes(file_string))
                                            list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName,'filesize':size})
                                        attach_to_onebox = attach_file_to_onebox_v2(tmp_sid,list_file,list_name_file,token_header)
                                    except Exception as ex:
                                        logger.info(ex)
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name'}),200
                                for o in range(len(list_arrfile)):
                                    if 'filesize' in list_arrfile[o]:
                                        tmpsum_storage += int(list_arrfile[o]['filesize'])
                                    list_file_name.append(list_arrfile[o])
                                return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                resUpdate = update().update_transactionfile(list_file_name,folder_name,tmpsum_storage)
                                if resUpdate['result'] == 'OK':
                                    return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'cant update in db'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found in db'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'please input file'}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data form not folder_name value'}),200
                if result_select['result'] == 'OK':
                    tmp_status_attmp = result_select['messageText']
                    print ('tmp_status_attmp:',tmp_status_attmp)
                    if tmp_status_attmp == True:
                        if str(folder_name).replace(' ','') != "":
                            if 'file[]' in dataFiles:
                                files = request.files.getlist("file[]")
                                for file in files:
                                    path = path_global_1 +'/storage/' + folder_name +'/'
                                    path_indb = '/storage/' + folder_name +'/'
                                    # path = './storage/' + folder_name +'/'
                                    # path_indb = '/storage/' + folder_name +'/'
                                    unique_filename = str(uuid.uuid4())
                                    tmpread = file.read()
                                    file_string = base64.b64encode(tmpread)                                    
                                    file_stringread = tmpread
                                    size = str(len(file_stringread))
                                    typefile = str(file.filename).split('.')[-1]
                                    files_to_box = base64.decodebytes(file_string)
                                    original_filename = str(file.filename)
                                    list_file.append(files_to_box)
                                    list_name_file.append(original_filename)
                                    try:
                                        with open(path + unique_filename + "." + typefile, "wb") as fh:
                                            fh.write(base64.decodebytes(file_string))
                                            list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName,'filesize':size})
                                    except Exception as ex:
                                        print(str(ex))
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name'}),200
                                attach_to_onebox = attach_file_to_onebox_v2(tmp_sid,list_file,list_name_file,token_header)
                                resultSelect = select().select_transactionfile(folder_name)
                                if resultSelect['result'] == 'OK':
                                    list_arrfile = resultSelect['messageText']['json_data']
                                    for o in range(len(list_arrfile)):
                                        print(list_arrfile[o])
                                        if 'filesize' in list_arrfile[o]:
                                            tmpsum_storage += int(list_arrfile[o]['filesize'])
                                        print(tmpsum_storage)
                                        list_file_name.append(list_arrfile[o])
                                    return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                    resUpdate = update().update_transactionfile(list_file_name,folder_name,tmpsum_storage)
                                    if resUpdate['result'] == 'OK':
                                        return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'cant update in db'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found in db'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'please input file'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data form not folder_name value'}),200
                    else:    
                        unique_foldername = str(uuid.uuid4())  
                        path =path_global_1 +'/storage/' + unique_foldername +'/'
                        path_indb = '/storage/' + unique_foldername +'/'
                        # path = './storage/' + unique_foldername +'/'
                        # path_indb = '/storage/' + unique_foldername +'/'
                        if not os.path.exists(path):
                            os.makedirs(path)
                        if 'file[]' in dataFiles and 'username' in dataForm:
                            files = request.files.getlist("file[]")
                            data_userName = dataForm['username']
                            for file in files:
                                unique_filename = str(uuid.uuid4())
                                tmpread = file.read()
                                file_string = base64.b64encode(tmpread)                                    
                                file_stringread = tmpread
                                size = str(len(file_stringread))
                                tmpsum_storage += len(file_stringread)
                                typefile = str(file.filename).split('.')[-1]
                                files_to_box = base64.decodebytes(file_string)
                                original_filename = str(file.filename)
                                list_file.append(files_to_box)
                                list_name_file.append(original_filename)
                                with open(path + unique_filename + "." + typefile, "wb") as fh:
                                    fh.write(base64.decodebytes(file_string))
                                    list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName,'filesize':size})
                            attach_to_onebox = attach_file_to_onebox_v2(tmp_sid,list_file,list_name_file,token_header)
                            return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':unique_foldername,'file_name':list_file_name,'message':'success'},'messageER':None,'status_Code':200}),200
                            result_Insert = insert().insert_transactionfile(list_file_name,path_indb,unique_foldername,tmpsum_storage)
                            result_update = update().update_attmp_folder_name_for_document_v1(tmp_sid,unique_foldername)
                            if result_Insert['result'] =='OK':
                                return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':unique_foldername,'file_name':list_file_name,'message':'success'},'messageER':None,'status_Code':200}),200
                            else:
                                return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'cant insert to db','status_Code':200}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':404}),404
                else:
                    if str(folder_name).replace(' ','') != "":
                        if 'file[]' in dataFiles:
                            files = request.files.getlist("file[]")
                            for file in files:
                                path = path_global_1 +'/storage/' + folder_name +'/'
                                path_indb = '/storage/' + folder_name +'/'
                                # path = './storage/' + folder_name +'/'
                                # path_indb = '/storage/' + folder_name +'/'
                                unique_filename = str(uuid.uuid4())
                                file_string = base64.b64encode(file.read())
                                typefile = str(file.filename).split('.')[-1]
                                files_to_box = base64.decodebytes(file_string)
                                original_filename = str(file.filename)
                                list_file.append(files_to_box)
                                list_name_file.append(original_filename)
                                try:
                                    with open(path + unique_filename + "." + typefile, "wb") as fh:
                                        fh.write(base64.decodebytes(file_string))
                                        list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                    
                                except Exception as ex:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name'}),200
                            attach_to_onebox = attach_file_to_onebox_v2(tmp_sid,list_file,list_name_file,token_header)
                            resultSelect = select().select_transactionfile(folder_name)
                            if resultSelect['result'] == 'OK':
                                list_arrfile = resultSelect['messageText']['json_data']
                                for o in range(len(list_arrfile)):
                                    list_file_name.append(list_arrfile[o])
                                return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                resUpdate = update().update_transactionfile(list_file_name,folder_name)
                                if resUpdate['result'] == 'OK':
                                    return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'cant update in db'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found in db'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'please input file'}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data form not folder_name value'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data form not key folder_name'}),200
    elif type_api == 'get':
        if request.method == 'POST':
            dataJson = request.json
            if 'folder_name' in dataJson:
                folder_name = dataJson['folder_name']
                resultSelect = select().select_transactionfile(folder_name)
                if resultSelect['result'] == 'OK':
                    json_data = (resultSelect['messageText']['json_data'])
                    pathfolder = (resultSelect['messageText']['pathfolder'])
                    return jsonify({'result':'OK','messageText':{'file_storage':'paperless','folder_path':pathfolder,'folder_name':folder_name,'file_name':json_data},'messageER':None,'status_Code':200}),200
                else:
                    url = url_ip_eform + '/api/v1/get_attract_file/?folder_name=' + folder_name
                    result_eform = callGET_other(url)
                    if result_eform['result'] == 'OK':
                        tmpmessage = result_eform['messageText'].json()
                        if tmpmessage['result'] == 'OK':
                            tmpdata = tmpmessage['messageText'][0]
                            pathfolder = tmpdata['folder_path']
                            json_data = tmpdata['file_name']
                            folder_name = tmpdata['folder_name']
                            return jsonify({'result':'OK','messageText':{'file_storage':'eform','folder_path':pathfolder,'folder_name':folder_name,'file_name':json_data},'messageER':None,'status_Code':200}),200
                    return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'cant get data','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'parameter incorrect','status_Code':200}),200
    elif type_api == 'remove':
        if request.method == 'POST':
            dataJson = request.json
            if 'folder_name' in dataJson and 'file_name' in dataJson:
                foldername = dataJson['folder_name']
                filename = dataJson['file_name']
                resultSelect = select().select_transactionfile(foldername)
                if resultSelect['result'] == 'OK':
                    arrlisttoCheck = resultSelect['messageText']['json_data']
                    pathfolder = (resultSelect['messageText']['pathfolder'])
                    path_removeFile = pathfolder + filename
                    path_removeFile = path_global_1 + path_removeFile
                    for i in range(len(arrlisttoCheck)):
                        if filename == arrlisttoCheck[i]['file_name_new']:
                            arrlisttoCheck.pop(i)
                            try:
                                os.remove(path_removeFile)
                                break
                            except Exception as ex:
                                return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':None},'messageER':'not found file _1','status_Code':200}),200
                            break
                    for i in range(len(arrlisttoCheck)):
                        if 'filesize' in arrlisttoCheck[i]:
                            tmpsum_storage += int(arrlisttoCheck[i]['filesize'])
                    resUpdate = update().update_transactionfile(arrlisttoCheck,foldername,tmpsum_storage)
                    if resUpdate['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':{'folder_path':None,'folder_name':None,'file_name':arrlisttoCheck},'messageER':None,'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'cant update to db','status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'not found foldername','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'parameter incorrect','status_Code':200}),200
    else:
        return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'type service incorrect','status_Code':200}),200

@status_methods.route('/storage/<string:type_api>/v2',methods=['POST'])
# @token_required
def keep_storage_v2(type_api):
    try:
        token_header = request.headers['Authorization']
        try:                
            token_header = str(token_header).split(' ')[1]
            token_required = token_required_func(token_header)
            # username = token_required['username']
            # user_id = token_required['user_id']
        except Exception as ex:
            abort(401)
    except KeyError as ex:
        return redirect(url_paperless)
    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
    size = None
    tmpsum_storage = 0
    tmpsum_storage_new = 0
    list_file = []
    list_name_file = []
    if type_api == 'keep':
        if request.method == 'POST':
            dataFiles = request.files
            dataForm = request.form
            unique_foldername = str(uuid.uuid4())
            list_file_name = []
            path = path_global_1 + '/storage/' + unique_foldername + '/'
            path_indb = '/storage/' + unique_foldername +'/'
            # path = './storage/' + unique_foldername +'/'
            # path_indb = '/storage/' + unique_foldername +'/'
            if not os.path.exists(path):
                os.makedirs(path)
            if 'file[]' in dataFiles and 'username' in dataForm and 'sid' in dataForm:
                files = request.files.getlist("file[]")
                data_userName = dataForm['username']
                sid = dataForm['sid']
                for file in files:
                    unique_filename = str(uuid.uuid4())
                    tmpread = file.read()
                    file_string = base64.b64encode(tmpread)                                    
                    file_stringread = tmpread
                    size = str(len(file_stringread))
                    tmpsum_storage += len(file_stringread)
                    typefile = str(file.filename).split('.')[-1]
                    with open(path + unique_filename + "." + typefile, "wb") as fh:
                        files_to_box = base64.decodebytes(file_string)
                        original_filename = str(file.filename)
                        fh.write(base64.decodebytes(file_string))
                        list_file.append(files_to_box)
                        list_name_file.append(original_filename)
                        list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName,'filesize':size})
                result_update_attemp = update_2().update_attemp_name_doc(unique_foldername,sid)
                attach_to_onebox = attach_file_to_onebox_v2(sid,list_file,list_name_file,token_header)
                result_Insert = insert().insert_transactionfile(list_file_name,path_indb,unique_foldername,tmpsum_storage)
                print ('result_Insert:',result_Insert)
                # return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':unique_foldername,'file_name':list_file_name},'messageER':None,'status_Code':200}),200
                if result_Insert['result'] =='OK':
                    if attach_to_onebox != None:
                        if 'result' in attach_to_onebox:
                            if attach_to_onebox['result'] == 'OK':
                                result_update_onebox = update_2().update_status_save_onebox(unique_foldername)
                            return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':unique_foldername,'file_name':list_file_name},'messageER':None,'status_Code':200}),200
                        else:                        
                            return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':unique_foldername,'file_name':list_file_name},'messageER':None,'status_Code':200}),200
                    else:                        
                        return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':unique_foldername,'file_name':list_file_name},'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'cant insert to db','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200})
    elif type_api == 'push':
        if request.method == 'POST':
            dataFiles = request.files
            dataForm = request.form
            unique_foldername = str(uuid.uuid4())
            list_file_name = []
            if 'folder_name' in dataForm and 'username' in dataForm and 'sid' in dataForm:
                folder_name = dataForm['folder_name']
                data_userName = dataForm['username']
                tmp_sid = dataForm['sid']
                if tmp_sid != '':
                    result_select = select().select_folder_name_attm_file_v1(tmp_sid)
                else:
                    if str(folder_name).replace(' ','') != "":
                        if 'file[]' in dataFiles:
                            files = request.files.getlist("file[]")
                            resultSelect = select().select_transactionfile(folder_name)
                            if resultSelect['result'] == 'OK':
                                list_arrfile = resultSelect['messageText']['json_data']
                                pathfolderindb = resultSelect['messageText']['pathfolder']
                                for file in files:
                                    path = path_global_1 + pathfolderindb
                                    path_indb = '/storage/' + unique_foldername +'/'
                                    # path = path_global_1 + '/storage/' + folder_name +'/'
                                    # path_indb = path_global_1 + '/storage/' + folder_name +'/'
                                    unique_filename = str(uuid.uuid4())
                                    tmpread = file.read()
                                    file_string = base64.b64encode(tmpread)                                    
                                    file_stringread = tmpread
                                    size = str(len(file_stringread))
                                    tmpsum_storage_new += len(file_stringread)
                                    typefile = str(file.filename).split('.')[-1]
                                    files_to_box = base64.decodebytes(file_string)
                                    original_filename = str(file.filename)
                                    list_file.append(files_to_box)
                                    list_name_file.append(original_filename)
                                    try:
                                        with open(path + unique_filename + "." + typefile, "wb") as fh:
                                            fh.write(base64.decodebytes(file_string))
                                            list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName,'filesize':size})
                                        attach_to_onebox = attach_file_to_onebox_v2(tmp_sid,list_file,list_name_file,token_header)
                                    except Exception as ex:
                                        logger.info(ex)
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name'}),200
                                for o in range(len(list_arrfile)):
                                    if 'filesize' in list_arrfile[o]:
                                        tmpsum_storage += int(list_arrfile[o]['filesize'])
                                    list_file_name.append(list_arrfile[o])
                                # return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                print ('tmpsum_storage111:',tmpsum_storage)
                                tmpsum_storage = tmpsum_storage + tmpsum_storage_new
                                resUpdate = update().update_transactionfile(list_file_name,folder_name,tmpsum_storage)
                                if resUpdate['result'] == 'OK':
                                    if attach_to_onebox != None:
                                        if 'result' in attach_to_onebox:
                                            if attach_to_onebox['result'] == 'OK':
                                                result_update_onebox = update_2().update_status_save_onebox(folder_name)
                                    return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'cant update in db'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found in db'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'please input file'}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data form not folder_name value'}),200
                if result_select['result'] == 'OK':
                    tmp_status_attmp = result_select['messageText']
                    print ('tmp_status_attmp:',tmp_status_attmp)
                    if tmp_status_attmp == True:
                        if str(folder_name).replace(' ','') != "":
                            if 'file[]' in dataFiles:
                                files = request.files.getlist("file[]")
                                for file in files:
                                    path = path_global_1 +'/storage/' + folder_name +'/'
                                    path_indb = '/storage/' + folder_name +'/'
                                    # path = './storage/' + folder_name +'/'
                                    # path_indb = '/storage/' + folder_name +'/'
                                    unique_filename = str(uuid.uuid4())
                                    tmpread = file.read()
                                    file_string = base64.b64encode(tmpread)                                    
                                    file_stringread = tmpread
                                    size = str(len(file_stringread))
                                    tmpsum_storage_new += len(file_stringread)
                                    typefile = str(file.filename).split('.')[-1]
                                    files_to_box = base64.decodebytes(file_string)
                                    original_filename = str(file.filename)
                                    list_file.append(files_to_box)
                                    list_name_file.append(original_filename)
                                    try:
                                        with open(path + unique_filename + "." + typefile, "wb") as fh:
                                            fh.write(base64.decodebytes(file_string))
                                            list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName,'filesize':size})
                                    except Exception as ex:
                                        print(str(ex))
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name'}),200
                                attach_to_onebox = attach_file_to_onebox_v2(tmp_sid,list_file,list_name_file,token_header)
                                resultSelect = select().select_transactionfile(folder_name)
                                print ('attach_to_onebox:',attach_to_onebox)
                                print ('resultSelect:',resultSelect)
                                if resultSelect['result'] == 'OK':
                                    list_arrfile = resultSelect['messageText']['json_data']
                                    for o in range(len(list_arrfile)):
                                        print(list_arrfile[o])
                                        if 'filesize' in list_arrfile[o]:
                                            tmpsum_storage += int(list_arrfile[o]['filesize'])
                                        print(tmpsum_storage)
                                        list_file_name.append(list_arrfile[o])
                                    # return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                    print ('tmpsum_storage222:',tmpsum_storage)
                                    print ('tmpsum_storage_new222:',tmpsum_storage_new)
                                    tmpsum_storage = tmpsum_storage + tmpsum_storage_new
                                    print ('tmpsum_storage_ans2222:',tmpsum_storage)
                                    resUpdate = update().update_transactionfile(list_file_name,folder_name,tmpsum_storage)
                                    if resUpdate['result'] == 'OK':
                                        if attach_to_onebox != None:
                                            if 'result' in attach_to_onebox:
                                                if attach_to_onebox['result'] == 'OK':
                                                    result_update_onebox = update_2().update_status_save_onebox(folder_name)
                                        return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'cant update in db'}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found in db'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'please input file'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data form not folder_name value'}),200
                    else:    
                        unique_foldername = str(uuid.uuid4())  
                        path =path_global_1 +'/storage/' + unique_foldername +'/'
                        path_indb = '/storage/' + unique_foldername +'/'
                        # path = './storage/' + unique_foldername +'/'
                        # path_indb = '/storage/' + unique_foldername +'/'
                        if not os.path.exists(path):
                            os.makedirs(path)
                        if 'file[]' in dataFiles and 'username' in dataForm:
                            files = request.files.getlist("file[]")
                            data_userName = dataForm['username']
                            for file in files:
                                unique_filename = str(uuid.uuid4())
                                tmpread = file.read()
                                file_string = base64.b64encode(tmpread)                                    
                                file_stringread = tmpread
                                size = str(len(file_stringread))
                                tmpsum_storage += len(file_stringread)
                                typefile = str(file.filename).split('.')[-1]
                                files_to_box = base64.decodebytes(file_string)
                                original_filename = str(file.filename)
                                list_file.append(files_to_box)
                                list_name_file.append(original_filename)
                                with open(path + unique_filename + "." + typefile, "wb") as fh:
                                    fh.write(base64.decodebytes(file_string))
                                    list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName,'filesize':size})
                            attach_to_onebox = attach_file_to_onebox_v2(tmp_sid,list_file,list_name_file,token_header)
                            # return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':unique_foldername,'file_name':list_file_name,'message':'success'},'messageER':None,'status_Code':200}),200
                            print ('tmpsum_storage333:',tmpsum_storage)
                            result_Insert = insert().insert_transactionfile(list_file_name,path_indb,unique_foldername,tmpsum_storage)
                            result_update = update().update_attmp_folder_name_for_document_v1(tmp_sid,unique_foldername)
                            if result_Insert['result'] =='OK':
                                if attach_to_onebox != None:
                                    if 'result' in attach_to_onebox:
                                        if attach_to_onebox['result'] == 'OK':
                                            result_update_onebox = update_2().update_status_save_onebox(unique_foldername)
                                return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':unique_foldername,'file_name':list_file_name,'message':'success'},'messageER':None,'status_Code':200}),200
                            else:
                                return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'cant insert to db','status_Code':200}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':404}),404
                else:
                    if str(folder_name).replace(' ','') != "":
                        if 'file[]' in dataFiles:
                            files = request.files.getlist("file[]")
                            for file in files:
                                path = path_global_1 +'/storage/' + folder_name +'/'
                                path_indb = '/storage/' + folder_name +'/'
                                # path = './storage/' + folder_name +'/'
                                # path_indb = '/storage/' + folder_name +'/'
                                unique_filename = str(uuid.uuid4())
                                tmpread = file.read()
                                file_string = base64.b64encode(file.read())
                                typefile = str(file.filename).split('.')[-1]
                                files_to_box = base64.decodebytes(file_string)
                                file_stringread = tmpread
                                size = str(len(file_stringread))
                                tmpsum_storage_new += len(file_stringread)
                                original_filename = str(file.filename)
                                list_file.append(files_to_box)
                                list_name_file.append(original_filename)
                                try:
                                    with open(path + unique_filename + "." + typefile, "wb") as fh:
                                        fh.write(base64.decodebytes(file_string))
                                        list_file_name.append({'file_name_original':file.filename,'file_name_new':unique_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                                    
                                except Exception as ex:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name'}),200
                            attach_to_onebox = attach_file_to_onebox_v2(tmp_sid,list_file,list_name_file,token_header)
                            resultSelect = select().select_transactionfile(folder_name)
                            if resultSelect['result'] == 'OK':
                                list_arrfile = resultSelect['messageText']['json_data']
                                for o in range(len(list_arrfile)):
                                    if 'filesize' in list_arrfile[o]:
                                        tmpsum_storage += int(list_arrfile[o]['filesize'])
                                    list_file_name.append(list_arrfile[o])
                                # return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                print ('tmpsum_storage444:',tmpsum_storage)
                                tmpsum_storage = tmpsum_storage + tmpsum_storage_new
                                resUpdate = update().update_transactionfile(list_file_name,folder_name,tmpsum_storage)
                                if resUpdate['result'] == 'OK':
                                    if attach_to_onebox['result'] == 'OK':
                                        result_update_onebox = update_2().update_status_save_onebox(folder_name)
                                    return jsonify({'result':'OK','messageText':{'folder_path':path_indb,'folder_name':folder_name,'file_name':list_file_name},'status_Code':200}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'cant update in db'}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found in db'}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'please input file'}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data form not folder_name value'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data form not key folder_name'}),200
    elif type_api == 'get':
        if request.method == 'POST':
            dataJson = request.json
            if 'folder_name' in dataJson:
                folder_name = dataJson['folder_name']
                resultSelect = select().select_transactionfile(folder_name)
                if resultSelect['result'] == 'OK':
                    json_data = (resultSelect['messageText']['json_data'])
                    pathfolder = (resultSelect['messageText']['pathfolder'])
                    return jsonify({'result':'OK','messageText':{'file_storage':'paperless','folder_path':pathfolder,'folder_name':folder_name,'file_name':json_data},'messageER':None,'status_Code':200}),200
                else:
                    url = url_ip_eform + '/api/v1/get_attract_file/?folder_name=' + folder_name
                    result_eform = callGET_other(url)
                    print(result_eform)
                    if result_eform['result'] == 'OK':
                        tmpmessage = result_eform['messageText'].json()
                        if tmpmessage['result'] == 'OK':
                            tmpdata = tmpmessage['messageText'][0]
                            pathfolder = tmpdata['folder_path']
                            json_data = tmpdata['file_name']
                            folder_name = tmpdata['folder_name']
                            return jsonify({'result':'OK','messageText':{'file_storage':'eform','folder_path':pathfolder,'folder_name':folder_name,'file_name':json_data},'messageER':None,'status_Code':200}),200
                    return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'cant get data','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'parameter incorrect','status_Code':200}),200
    elif type_api == 'remove':
        if request.method == 'POST':
            dataJson = request.json
            if 'folder_name' in dataJson and 'file_name' in dataJson:
                foldername = dataJson['folder_name']
                filename = dataJson['file_name']
                resultSelect = select().select_transactionfile(foldername)
                if resultSelect['result'] == 'OK':
                    arrlisttoCheck = resultSelect['messageText']['json_data']
                    pathfolder = (resultSelect['messageText']['pathfolder'])
                    path_removeFile = pathfolder + filename
                    path_removeFile = path_global_1 + path_removeFile
                    for i in range(len(arrlisttoCheck)):
                        if filename == arrlisttoCheck[i]['file_name_new']:
                            arrlisttoCheck.pop(i)
                            try:
                                os.remove(path_removeFile)
                                break
                            except Exception as ex:
                                return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':None},'messageER':'not found file _1','status_Code':200}),200
                            break
                    for i in range(len(arrlisttoCheck)):
                        if 'filesize' in arrlisttoCheck[i]:
                            tmpsum_storage += int(arrlisttoCheck[i]['filesize'])
                    resUpdate = update().update_transactionfile(arrlisttoCheck,foldername,tmpsum_storage)
                    if resUpdate['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':{'folder_path':None,'folder_name':None,'file_name':arrlisttoCheck},'messageER':None,'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'cant update to db','status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'not found foldername','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'parameter incorrect','status_Code':200}),200
    else:
        return jsonify({'result':'ER','messageText':{'folder_path':None,'folder_name':None,'file_name':[]},'messageER':'type service incorrect','status_Code':200}),200

# def attach_file_to_onebox_v2(sid,list_file,list_name_file,token_header): 
#     try:
#         if sid != None and sid != '':
#             # sid = dataForm['sid']
#             result_tax_id = select_2().select_tax_id_onebox_attach_file(sid)
#             taxid = result_tax_id['messageText']
#             doc_name_type = result_tax_id['messageText2']
#             result_dept = select_3().select_deptname_onebox(sid)
#             dept_name = result_dept['messageText']
#             result_user = select().select_user_first(sid)
#             if result_user['result'] == 'OK':
#                 username_first = result_user['messageText']['username']
#                 userid_first = result_user['messageText']['userid']
#                 result_save_attach = get_attach_to_onebox_push(sid,username_first,userid_first,taxid,dept_name,doc_name_type,token_header,list_file,list_name_file) #เพิ่มใหม่
#             return {'result':'OK','messageText':result_save_attach['messageText'],'status_Code':200}
#         else:
#             return {'result':'ER','messageText':'Parameter Fail!','status_Code':404}
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(exc_type, fname, exc_tb.tb_lineno)
#         return {'result':'ER','messageText':str(e)}

def attach_file_to_onebox_v2(sid,list_file,list_name_file,token_header): 
    try:
        if sid != None and sid != '':
            # sid = dataForm['sid']
            result_tax_id = select_2().select_tax_id_onebox_attach_file(sid)
            taxid = result_tax_id['messageText']
            result_config = select_4().select_status_nameservice(taxid)
            if result_config['result'] == 'OK':
                data_name_service = result_config['data']
                for i in range(len(data_name_service)):
                    if data_name_service[i]['name_service'] == 'ONEBOX' and data_name_service[i]['status'] == True:
                        # print ('yessss')
                        doc_name_type = result_tax_id['messageText2']
                        result_dept = select_3().select_deptname_onebox(sid)
                        dept_name = result_dept['messageText']
                        result_user = select().select_user_first(sid)
                        if result_user['result'] == 'OK':
                            username_first = result_user['messageText']['username']
                            userid_first = result_user['messageText']['userid']
                            result_save_attach = get_attach_to_onebox_push(sid,username_first,userid_first,taxid,dept_name,doc_name_type,token_header,list_file,list_name_file) #เพิ่มใหม่
                        return {'result':'OK','messageText':result_save_attach['messageText'],'status_Code':200}
            else:
                return {'result':'ER','messageText':'data Not found!','status_Code':404}
        else:
            return {'result':'ER','messageText':'Parameter Fail!','status_Code':404}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':str(e)}
        
@status_methods.route('/storage/<string:type_api>/to_eform',methods=['POST'])
# @token_required
def keep_storage_to_eform(type_api):
    try:
        token_header = request.headers['Authorization']
        try:                
            token_header = str(token_header)
            # print (token_header)
            token_required = token_required_func(token_header)
        except Exception as ex:
            abort(401)
    except KeyError as ex:
        return redirect(url_paperless)
    list_file = []
    list_name_file = []
    list_file_name = []
    list_temp_file = []
    if type_api == 'keep':
        if request.method == 'POST':
            dataFiles = request.files
            dataForm = request.form
            unique_foldername = str(uuid.uuid4())
            
            path = path_global_1 + '/storage/' + unique_foldername + '/'
            path_indb = '/storage/' + unique_foldername +'/'
            if not os.path.exists(path):
                os.makedirs(path)
            try:
                if 'file[]' in dataFiles and 'folder_name' in dataForm:
                    files = request.files.getlist("file[]")
                    folder_name = dataForm['folder_name']
                    for file in files:
                        unique_filename = str(uuid.uuid4())
                        tmpread = file.read()
                        file_string = base64.b64encode(tmpread)                                    
                        file_stringread = tmpread
                        size = str(len(file_stringread))
                        file_name = str(file.filename)
                        with open(path + file_name, "wb") as fh:
                            # file_open = fh 
                            fh.write((tmpread))
                        file_open = (file_name,open(path + file_name,'rb'))
                        list_temp_file.append(('file',file_open))
                    file_tmp = list_temp_file
                    headers = {
                        'Authorization': token_header
                    }
                    data = {
                        'folder_name':folder_name,
                        'doc_number':'',
                        'e_id':''
                    }
                    result_call = callPost_eform_attach(data,headers,list_temp_file)
                    if result_call['result'] == 'OK':
                        url = url_ip_eform + '/api/v1/get_attract_file/?folder_name=' + folder_name
                        result_eform = callGET_other(url)
                        if result_eform['result'] == 'OK':
                            tmpmessage = result_eform['messageText'].json()
                            if tmpmessage['result'] == 'OK':
                                tmpdata = tmpmessage['messageText'][0]
                                pathfolder = tmpdata['folder_path']
                                json_data = tmpdata['file_name']
                                folder_name = tmpdata['folder_name']
                                return jsonify({'result':'OK','messageText':{'file_storage':'eform','folder_path':pathfolder,'folder_name':folder_name,'file_name':json_data},'messageER':None,'status_Code':200}),200
                    return jsonify({'result':'OK','messageText':result_call['messageText'],'status_Code':200})
                else:
                    return jsonify({'result':'ER','messageText':'invalid Parameter','status_Code':200})
            except Exception as e:
                print (str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':'Fails!'}),200