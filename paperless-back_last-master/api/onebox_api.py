#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.qrcode import *
from controller.mail_string import *
from controller.validate import *
from db.db_method import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from method.pdf import *
from method.verify import *
from api.onebox import *
import os
import pythainlp
from pythainlp.transliterate import romanize
from pythainlp.transliterate import transliterate
from pythainlp.corpus import wordnet
from pythainlp.soundex import udom83
from pythainlp.soundex import lk82
from pythainlp.soundex import metasound
import pythainlp.util


if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

@status_methods.route('/api/onebox/save_file_onebox',methods=['POST'])
# @token_required
def onebox_save_file():
    
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
        result_verify_json = (result_verify['messageText']).json()
            
    except Exception as e:
        return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401        

    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    st2 = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')   
    user_id = result_verify_json['biz_detail'][0]['account_id']
    if request.method == 'POST':
        try:
            # GET account_id จาก oneid
            headers = {
                'Authorization': "7de269ee4b15a327d8843a0b2505187dd3fb875c5c39dac06bcbc7e9ff68b5df5fa8d71c56d45fd93aab1be35c57930a56cc70574b2d12c6bb8dba8751685891"
            }
            data = {
                'user_id': str(user_id)
            }
            result_select_account_id = select_account_id_onebox(data,headers)         
             # GET folder จาก account_id
            account_id = result_select_account_id['result'][0]['account_id']
            data_account_id = {
                'account_id': str(account_id)
            }
            result_select_folder = select_folder_onebox(account_id,data_account_id,headers)
            folder_id = result_select_folder['result'][0]['folder_id']
            data_save_file = {
                'account_id': str(account_id),
                'folder_id' : str(folder_id), 
            }
            dataFiles = request.files
            dataForm = request.form
            unique_foldername = str(uuid.uuid4())
            list_file_name = []
            list_response = []
            path = path_global_1 + '/storage/temp/' + unique_foldername +'/'
            path_indb = path_global_1 + '/storage/temp/' + unique_foldername +'/'
            path_folder = path_global_1 + '/storage/temp/'
            # path = './storage/temp/' + unique_foldername +'/'
            # path_indb = '/storage/temp/' + unique_foldername +'/'
            # path_folder = '/storage/temp/'
            if not os.path.exists(path):
                os.makedirs(path)
            if 'file[]' in dataFiles and 'username' in dataForm:
                files = request.files.getlist("file[]")
                data_userName = dataForm['username']
                for file in files:
                    unique_filename = str(uuid.uuid4())
                    original_filename = str(file.filename).split('.')[0]
                    check_thai = pythainlp.util.isthai(original_filename)
                    if check_thai == True:
                        original_filename = romanize(original_filename, engine="thai2rom")
                    # try:
                    #     original_filename = original_filename2.encode('latin-1')
                    #     print ('1111')
                    # except UnicodeEncodeError:
                    #     print ('22222')
                    #     filenames = {
                    #         'filename': unicodedata.normalize('NFKD', original_filename2).encode('latin-1', 'ignore'),
                    #         'filename*': "UTF-8''{}".format(original_filename2),
                    #     }
                    #     original_filename = filenames['filename'].decode('utf8')

                    file_string = base64.b64encode(file.read())
                    typefile = str(file.filename).split('.')[-1]
                    typefile = typefile.split('"')[0]
                    # print ('original_filename: ',original_filename)
                    with open(path + original_filename + "." + typefile, "wb") as fh:
                        file_open = fh 
                        fh.write(base64.decodebytes(file_string))
                        list_file_name.append({'file_name_original':file.filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                    file_open = open(path + original_filename + "." + typefile, "rb")
                    files_save = {
                        'file' : file_open
                    }    
                    # print ('list_file_name: ', file_open)

                    result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,data_userName)
                    list_response.append(result_save_file)
                    file_open.close()
                result_insert = insert().insert_transactionfile_copy1(list_response,path_indb,unique_foldername)
                return jsonify({'result':'OK','messageText':list_response,'messageER':None,'status_Code':200}),200
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            db.session.rollback()
            raise
            return jsonify({'result':'ER','messageText':'Fail!','status_Code':401,'service':'oneid'}),401
        finally:
            path_removeFile = os.getcwd() + path_indb 
            print (path_removeFile)
            shutil.rmtree(path_removeFile)

@status_methods.route('/api/onebox/transactionfile_copy1',methods=['GET'])
def onebox_transactionfile_copy1():
    if request.method == 'GET':
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
            result_verify_json = (result_verify['messageText']).json()
                
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401        

        try: 
            dataJson = request.json
            if 'attempted_id' in dataJson and len(dataJson) == 1:
                attempted_id = dataJson['attempted_id']
                result_select = select().select_transactionfile_copy1(attempted_id)
                return jsonify({'result':'OK','messageText':result_select['messageText'],'messageER':None,'status_Code':200}),200        

        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':str(e),'data':[]},'status_Code':401}),401        

@status_methods.route('/api/onebox/download_file',methods=['GET'])
def onebox_download_file():
    if request.method == 'GET':
        try:
            tmp_file_id = request.args.get('file_id')
            unique_foldername = str(uuid.uuid4())
            path = '/storage/temp/'
            path_download = os.getcwd() + path 
            ts = int(time.time())
            st = str(datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y'))
            result_download_file = None

            print ('NAME: ', path_download + st)

            if tmp_file_id != None:
                # user_id = result_verify_json['biz_detail'][0]['account_id']
                headers = {
                    'Authorization': "7de269ee4b15a327d8843a0b2505187dd3fb875c5c39dac06bcbc7e9ff68b5df5fa8d71c56d45fd93aab1be35c57930a56cc70574b2d12c6bb8dba8751685891"
                }
                data = {
                    'file_id' : str(tmp_file_id),
                    # 'user_id': ''
                }
                
                result_download_file_onebox = download_file_onebox(data,headers)
                return (result_download_file_onebox)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            db.session.rollback()
            raise
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':str(e),'data':[]},'status_Code':401}),401        

