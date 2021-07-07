# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from db.db_method import *
from db.db_method_1 import *
# from db.db_method_3 import *
from config.lib import *
from method.hashpy import *
from method.pdf import *

def convert_base64Tosize(strdata):
    return (len(strdata) * 3) / 4 - strdata.count('=', -2)

def base64Tobytes(txt):
    n = float(len(txt))
    if txt.endswith("==") : p = 2
    elif txt.endswith("="): p = 1
    else : p = 0
    byte = (n / 4) * 3 - p
    kb = byte * 0.000977
    return byte

def convert_base_bytes():    
    tmplistdata = []
    r = (select_4().select_pdfbase64())
    for i in range(len(r)):
        listdata = []
        FileSize = base64Tobytes(r[i]['base64file'])
        fileid = (r[i]['file_id'])
        listdata.append(FileSize)
        listdata.append(fileid)
        tmptuple = tuple(listdata)
        tmplistdata.append(tmptuple)
    r = update_4().update_sizeFile_document_v1(tmplistdata)
    return (r)

def convert_bytes_storage(tmp_bytes):
    tmp_bytes = float(tmp_bytes)    
    tmpkb = (tmp_bytes / 1024)  
    tmpmb = (tmp_bytes / 1048576)  
    tmpgb = (tmp_bytes / 1073741824)
    info = {
        "Kilobyte":tmpkb,
        "Megabyte":tmpmb,
        "Gigabyte":tmpgb
    }
    return (info)

def watermark_cancel_v1(email_User,sidCode,username,tmpfid):
    strname_surname = fine_name_surename(email_User)
    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    tmp_pathwatermark = make_watermarker_reject_cancel('เอกสารนี้ถูกยกเลิกโดย ' + strname_surname,'วันที่/เวลา ' + st)
    resultpdf = select().select_get_pdf_v2(sidCode)
    if resultpdf['result'] == 'OK':
        tmpdatapdf = resultpdf['messageText']
        tmppdforg = tmpdatapdf['file_Paperless']['file_base']
    with io.BytesIO(base64.b64decode(tmppdforg)) as open_pdf_file:
        read_pdf = PdfFileReader(open_pdf_file)
        num_pages = read_pdf.getNumPages()
    result_mergepdf = mergepdf_reject_cancel(num_pages,tmppdforg,tmp_pathwatermark,username)
    if result_mergepdf['result'] == 'OK':
        tmpPDF_ = result_mergepdf['messageText']['responsePdf']
    r = update_3().update_pdf_rejectordelete_v1(tmpfid,tmpPDF_)
    print(r)
                
def check_special_str_filename(string):
    try:
        # string = "Geeks$For$Geeks"
        string = str(string)
        print ('string:',string)
        regex = re.compile('[@!#$%^&*()<>?/\|}{~:\']') 
        # regex = re.compile('[@!#$%^&*<>?/\|}{~:]') 
        regex = re.compile('[<>:"/\|?*\']')
        check = False
            
        if(regex.search(string) == None): 
            check = False
            text = "This String not have special str"
            # print(text) 
                
        else:
            check = True
            text = "This String have special str"
            # print(text) 
        return {'result':'OK','messageText':{'status':check,'messageText':text},'status_Code':200}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def replace_symbol_filename(filename):
    try:
        # filename = "how ดู อิส โส for the maple syrup? $20.99? That's ridiculous!!!"
        invalid = '<>:"/\|?*\''
        for char in invalid:
            filename = filename.replace(char, '_')
        return filename

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return filename
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def convert_pdf_images(foldername,base64_pdfFile,tmpid_process):
    try:
        list_file_name = []
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
        # countpages = 0
        # images = convert_from_bytes(open(address_file,'rb').read())
        # for i, image in enumerate(images):
        #     countpages = countpages + 1
        # try:
        #     maxPages = pdf2image._page_count(address_file)
        # except Exception as e:
        #     maxPages = countpages
        # print(maxPages)
        pages = convert_from_path(address_file, dpi=200, fmt='jpeg',output_folder=path_image)
        for u in range(len(pages)):
            print(u)
            filename_only = str(pages[u].filename).split('/')[-1]
            try:
                url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                with open(pages[u].filename, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    encoded_string = (encoded_string).decode('utf8')
                # list_file_name.append({'image_Base64': str(encoded_string), 'image_Url': url_view_image})
                list_file_name.append({'image_Url': url_view_image})
                tmpstatus = 'ONPROCESS'
                # print(tmpstatus)
                list_dataresult = list_file_name
                resultUpdate = update_1().update_process_log_status_v2(tmpid_process,'CONVERT',tmpstatus,str(list_dataresult),None,None)
            except Exception as ex:
                print(str(ex))
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(ex)}),200
        # if (u+1) == maxPages:
        tmpstatus = 'SUCCESS'
        resultUpdate = update_1().update_process_log_status_v2(tmpid_process,'CONVERT',tmpstatus,str(list_dataresult),None,None)
        return jsonify({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200
        if maxPages != 1:
            # for page in range(1,maxPages,1):
                # print(page)
            pages = convert_from_path(address_file, dpi=200, fmt='jpeg',output_folder=path_image)
            for u in range(len(pages)):
                print(u)
                filename_only = str(pages[u].filename).split('/')[-1]
                try:
                    url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                    with open(pages[u].filename, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                        encoded_string = (encoded_string).decode('utf8')
                    # list_file_name.append({'image_Base64': str(encoded_string), 'image_Url': url_view_image})
                    list_file_name.append({'image_Url': url_view_image})
                    tmpstatus = 'ONPROCESS'
                    # print(tmpstatus)
                    list_dataresult = list_file_name
                    resultUpdate = update_1().update_process_log_status_v2(tmpid_process,'CONVERT',tmpstatus,str(list_dataresult),None,None)
                except Exception as ex:
                    print(str(ex))
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(ex)}),200
            if (u+1) == maxPages:
                tmpstatus = 'SUCCESS'
                resultUpdate = update_1().update_process_log_status_v2(tmpid_process,'CONVERT',tmpstatus,str(list_dataresult),None,None)
            return jsonify({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200
        else:
            pages = convert_from_path(address_file, dpi=200, first_page=0,fmt='jpeg', last_page = 1,output_folder=path_image)
            for u in range(len(pages)):
                print(u)
                filename_only = str(pages[u].filename).split('/')[-1]
                try:
                    url_view_image = myUrl_domain + 'api/view2/pdf_image/' + foldername +'/' + filename_only
                    with open(pages[u].filename, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                        encoded_string = (encoded_string).decode('utf8')
                    # list_file_name.append({'image_Base64': str(encoded_string), 'image_Url': url_view_image})
                    list_file_name.append({'image_Url': url_view_image})
                    tmpstatus = 'ONPROCESS'
                    # print(tmpstatus)
                    list_dataresult = list_file_name
                    resultUpdate = update_1().update_process_log_status_v2(tmpid_process,'CONVERT',tmpstatus,str(list_dataresult),None,None)
                    # update_3().update_process_onprocess_status_v1(tmpid_process,email,sid,tmpstatus,res_list['msg'],'ERSIGN001')
                except Exception as ex:
                    print(str(ex))
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'not found folder name ' + str(ex)}),200            
            if (u+1) == maxPages:
                tmpstatus = 'SUCCESS'
                resultUpdate = update_1().update_process_log_status_v2(tmpid_process,'CONVERT',tmpstatus,str(list_dataresult),None,None)
            return jsonify({'result': 'OK', 'messageText': list_file_name, 'status_Code': 200}), 200
    except Exception as e:
        print(str(e))