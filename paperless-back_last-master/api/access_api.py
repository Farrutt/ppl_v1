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
from api.schedule_log import *



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

@status_methods.route('/api/security_token_gen', methods=['POST'])
def security_token_gen():
    if request.method == 'POST':
        datajson = request.json
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        try:
            if 'service_name' in datajson and len(datajson) == 1:
                service_name = datajson['service_name']
                service_id = ''.join([random.choice(string.digits) for n in range(13)])
                secretkey = genarate_secretkey((str(service_id)))
                output_file = './storage/public_key/'
                # output_file = path_global_1 + '/storage/public_key/'
                if not os.path.exists(output_file):
                    os.makedirs(output_file)
                file_name = 'public_key_'+ service_name + str(st)
                secretkey = eval(str(secretkey))
                private_key = (secretkey['private'])
                public_key = (secretkey['public'])
                with open(output_file+file_name+'.txt', 'wb') as fh:
                    fh.write(public_key)
                private_key = (private_key).decode('utf8')
                public_key = public_key.decode('utf8')
                result_insert = insert_2().secret_key_bi(service_name,private_key,service_id)
                return jsonify({'result':'OK','messageText':{'private_key':private_key,'public_key':public_key},'status_Code':200,'messageER':None}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/jwt_security', methods=['POST'])
def jwt_security():
    if request.method == 'POST':
        datajson = request.json
        try:
            if 'service_id' in datajson and 'data_encode' in datajson and len(datajson) == 2:
                service_id = datajson['service_id']
                data = datajson['data_encode']
                # result_private_key = select_2().select_private_key(service_id)
                # if result_private_key['result'] == 'OK':
                    # secret_data = result_private_key['messageText']
                    # service_id_code = secret_data['code']
                    # service_name = secret_data['serviceName']
                    # private_key = secret_data['private']
                    # result_secret = encode_secret_key(service_id_code,service_name,private_key,data)
                result_secret = encode_secret_key(service_id,data)
                if result_secret['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'jwt_data':result_secret['messageText']},'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_secret['messageText']}),200
                # else:
                #     return jsonify({'result':'ER','messageText':result_private_key['messageER'],'status_Code':200,'messageER':None}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/decode_jwt_security', methods=['POST'])
def decode_jwt_security():
    if request.method == 'POST':
        datajson = request.json
        try:
            if 'public_key' in datajson and 'jwt_key' in datajson and 'service_id' in datajson:
                public_key = datajson['public_key']
                jwt_key = datajson['jwt_key']
                if 'service_id' in datajson:
                    service_id = datajson['service_id']
                else:
                    if type_product == 'uat':
                        service_id = '6897449463711'
                    elif type_product == 'prod':
                        service_id = '0389183359045'
                result_decode = decode_secret_key(jwt_key,public_key,service_id)
                return jsonify({'result':'OK','messageText':result_decode['messageText'],'status_Code':200,'messageER':None}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/v1/ppl_token_gen', methods=['POST'])
def ppl_token_gen():
    if request.method == 'POST':
        datajson = request.json
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        try:
            if 'service_name' in datajson and len(datajson) == 1:
                tmp_servicename = datajson['service_name']
                tmp_paperlessToken = generate_key(64)
                insert_4().insert_paperlessToken_v1(tmp_servicename,tmp_paperlessToken)
                return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':None}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/v1/deaccess', methods=['GET'])
def deaccess_api():
    if request.method == 'GET':
        try:
            try:
                deaccess = request.headers['Authorization']
                deaccess = deaccess.split(' ')[1]
            except Exception as e:
                abort(401)
            result_decode = dedcode_access(deaccess)
            return jsonify({'result':'OK','messageText':result_decode['messageText'],'status_Code':200,'messageER':None}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200