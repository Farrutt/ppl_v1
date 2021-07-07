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
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *
from method.sftp_fucn import *



if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less



@status_methods.route('/api/insert_draft_document', methods=['POST'])
# @token_required
def insert_draft_document():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
                email = token_required['email']
                # email = 'farrutt.th@thai.com'
                print ('email: ',email)
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        datajson = request.json
        try:
            if 'sid' in datajson and len(datajson) == 1:
                sid = datajson['sid']
                result_step_data = select_2().select_step_data_draft(sid)
                step_data = result_step_data['messageText']
                result_pdf_detail = select_2().select_pdf_detail(sid)
                pdf_detail = result_pdf_detail['messageText']
                # print (step_data , pdf_detail)
                result_insert = insert_2().insert_draft(step_data,pdf_detail)
                # print (result_insert)
            return jsonify({'result':'OK','messageText':result_insert['messageText'],'messageER':None,'status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

# @status_methods.route('/api/insert_draft_document_v2', methods=['POST'])
# # @token_required
# def insert_draft_document_v2():
#     if request.method == 'POST':
#         try:
#             token_header = request.headers['Authorization']
#             try:                
#                 token_header = str(token_header).split(' ')[1]
#                 token_required = token_required_func(token_header)
#                 email = token_required['email']
#                 # email = 'farrutt.th@thai.com'
#                 print ('email: ',email)
#             except Exception as ex:
#                 return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
#         except KeyError as ex:
#             return redirect(url_paperless)
#         datajson = request.json
#         try:
#             if 'step_data' in datajson and 'step_data_Upload' in datajson and 'biz_info' in datajson and 'qrCode_position' in datajson \
#             and 'recipient_email' in datajson and 'file_string' in datajson and 'document_json' in datajson and 'options_page' in datajson\
#             and 'document_type' in datajson and 'sender_email' in datajson and 'template' in datajson and 'type_file' in datajson \
#             and 'folder_name' in datajson and 'email_center' in datajson and 'step_code' in datajson and 'attempted_name' in datajson \
#             and 'attach_data' in datajson and 'importance' in datajson and 'last_digitsign' in datajson and 'time_expire' in datajson\
#             and len(datajson) == 20:
#                 data_json = datajson['step_data']
#                 data_json_Upload = datajson['step_data_Upload']
#                 biz_info = datajson['biz_info']
#                 qrCode_position = datajson['qrCode_position']
#                 recipient_email = datajson['recipient_email']
#                 string_pdf = datajson['file_string']
#                 documentJson = datajson['document_json']
#                 options_page = datajson['options_page']
#                 documentType = datajson['document_type']
#                 sender_email = datajson['sender_email']
#                 template = datajson['template']
#                 type_file = datajson['type_file']
#                 folder_name = datajson['folder_name']
#                 email_center = datajson['email_center']
#                 step_code = datajson['step_code']
#                 attempted_name = datajson['attempted_name']
#                 attach_data = datajson['attach_data']
#                 importance = datajson['importance']
#                 last_digitsign = datajson['last_digitsign']
#                 time_expire = datajson['time_expire']
#                 result_insert = insert_2().insert_draft_v3_sql(data_json,data_json_Upload,biz_info,qrCode_position,recipient_email,string_pdf,documentJson,options_page,documentType,sender_email,template,type_file,folder_name,email_center,step_code,attempted_name,attach_data,importance,last_digitsign,time_expire)
#                 # print (result_insert)
#                 return jsonify({'result':'OK','messageText':result_insert['messageText'],'messageER':None,'status_Code':200}),200
#             else:
#                 return jsonify({'result':'ER','messageText':None,'messageER':'missing key','status_Code':200}),200
#         except Exception as e:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_type, fname, exc_tb.tb_lineno)
#             return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/insert_draft_document_v2', methods=['POST'])
# @token_required
def insert_draft_document_v2():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
                email = token_required['email']
                # email = 'farrutt.th@thai.com'
                print ('email: ',email)
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        datajson = request.json
        try:
            if 'step_data' in datajson and 'step_data_Upload' in datajson and 'biz_info' in datajson and 'qrCode_position' in datajson \
            and 'recipient_email' in datajson and 'file_string' in datajson and 'document_json' in datajson and 'options_page' in datajson\
            and 'document_type' in datajson and 'sender_email' in datajson and 'template' in datajson and 'type_file' in datajson \
            and 'folder_name' in datajson and 'email_center' in datajson and 'step_code' in datajson and 'attempted_name' in datajson \
            and 'attach_data' in datajson and 'importance' in datajson and 'last_digitsign' in datajson and 'time_expire' in datajson\
            and 'status_ref' in datajson and 'list_ref' in datajson and len(datajson) == 22:
                data_json = datajson['step_data']
                data_json_Upload = datajson['step_data_Upload']
                biz_info = datajson['biz_info']
                qrCode_position = datajson['qrCode_position']
                recipient_email = datajson['recipient_email']
                string_pdf = datajson['file_string']
                documentJson = datajson['document_json']
                options_page = datajson['options_page']
                documentType = datajson['document_type']
                sender_email = datajson['sender_email']
                template = datajson['template']
                type_file = datajson['type_file']
                folder_name = datajson['folder_name']
                email_center = datajson['email_center']
                step_code = datajson['step_code']
                attempted_name = datajson['attempted_name']
                attach_data = datajson['attach_data']
                importance = datajson['importance']
                last_digitsign = datajson['last_digitsign']
                time_expire = datajson['time_expire']
                status_ref = datajson['status_ref']
                list_ref = datajson['list_ref']
                result_insert = insert_2().insert_draft_v3_sql(data_json,data_json_Upload,biz_info,qrCode_position,recipient_email,string_pdf,documentJson,options_page,documentType,sender_email,template,type_file,folder_name,email_center,step_code,attempted_name,attach_data,importance,last_digitsign,time_expire,status_ref,list_ref)
                # print (result_insert)
                return jsonify({'result':'OK','messageText':result_insert['messageText'],'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':'missing key','status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

# @status_methods.route('/api/update_draft_document', methods=['POST'])
# # @token_required
# def update_draft_document():
#     if request.method == 'POST':
#         try:
#             token_header = request.headers['Authorization']
#             try:                
#                 token_header = str(token_header).split(' ')[1]
#                 token_required = token_required_func(token_header)
#                 email = token_required['email']
#                 # email = 'farrutt.th@thai.com'
#                 print ('email: ',email)
#             except Exception as ex:
#                 return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
#         except KeyError as ex:
#             return redirect(url_paperless)
#         datajson = request.json
#         try:
#             if 'tid' in datajson and 'step_data' in datajson and 'step_data_Upload' in datajson\
#                 and 'biz_info' in datajson and 'qrCode_position' in datajson and 'recipient_email' in datajson \
#                 and 'file_string' in datajson and 'document_json' in datajson and 'options_page' in datajson \
#                 and 'document_type' in datajson and 'template' in datajson and 'type_file' in datajson \
#                 and 'folder_name' in datajson and 'email_center' in datajson and 'step_code' in datajson\
#                 and 'attempted_name' in datajson and 'attach_data' in datajson and 'importance' in datajson \
#                 and 'last_digitsign' in datajson and 'time_expire' in datajson and len(datajson) == 20:
#                 id_data = datajson['tid']
#                 data_json = datajson['step_data']
#                 data_json_Upload = datajson['step_data_Upload']
#                 biz_info = datajson['biz_info']
#                 qrCode_position = datajson['qrCode_position']
#                 recipient_email = datajson['recipient_email']
#                 string_pdf = datajson['file_string']
#                 documentJson = datajson['document_json']
#                 options_page = datajson['options_page']
#                 documentType = datajson['document_type']
#                 template = datajson['template']
#                 type_file = datajson['type_file']
#                 folder_name = datajson['folder_name']
#                 email_center = datajson['email_center']
#                 step_code = datajson['step_code']
#                 attempted_name = datajson['attempted_name']
#                 attach_data = datajson['attach_data']
#                 importance = datajson['importance']
#                 last_digitsign = datajson['last_digitsign']
#                 time_expire = datajson['time_expire']
#                 result_update = update_2().update_draft_document_v2_sql(id_data,data_json,data_json_Upload,biz_info,qrCode_position,recipient_email,string_pdf,documentJson,options_page,documentType,template,type_file,folder_name,email_center,step_code,attempted_name,attach_data,importance,last_digitsign,time_expire)
#                 return jsonify({'result':'OK','messageText':result_update['messageText'],'messageER':None,'status_Code':200}),200
#             else:
#                 return jsonify({'result':'ER','messageText':None,'messageER':'missing key','status_Code':200}),200

#         except Exception as e:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_type, fname, exc_tb.tb_lineno)
#             return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/update_draft_document', methods=['POST'])
# @token_required
def update_draft_document():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
                email = token_required['email']
                # email = 'farrutt.th@thai.com'
                print ('email: ',email)
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        datajson = request.json
        try:
            if 'tid' in datajson and 'step_data' in datajson and 'step_data_Upload' in datajson\
                and 'biz_info' in datajson and 'qrCode_position' in datajson and 'recipient_email' in datajson \
                and 'file_string' in datajson and 'document_json' in datajson and 'options_page' in datajson \
                and 'document_type' in datajson and 'template' in datajson and 'type_file' in datajson \
                and 'folder_name' in datajson and 'email_center' in datajson and 'step_code' in datajson\
                and 'attempted_name' in datajson and 'attach_data' in datajson and 'importance' in datajson \
                and 'last_digitsign' in datajson and 'time_expire' in datajson and 'status_ref' in datajson \
                and 'list_ref' in datajson and len(datajson) == 22:
                id_data = datajson['tid']
                data_json = datajson['step_data']
                data_json_Upload = datajson['step_data_Upload']
                biz_info = datajson['biz_info']
                qrCode_position = datajson['qrCode_position']
                recipient_email = datajson['recipient_email']
                string_pdf = datajson['file_string']
                documentJson = datajson['document_json']
                options_page = datajson['options_page']
                documentType = datajson['document_type']
                template = datajson['template']
                type_file = datajson['type_file']
                folder_name = datajson['folder_name']
                email_center = datajson['email_center']
                step_code = datajson['step_code']
                attempted_name = datajson['attempted_name']
                attach_data = datajson['attach_data']
                importance = datajson['importance']
                last_digitsign = datajson['last_digitsign']
                time_expire = datajson['time_expire']
                status_ref = datajson['status_ref']
                list_ref = datajson['list_ref']
                result_update = update_2().update_draft_document_v2_sql(id_data,data_json,data_json_Upload,biz_info,qrCode_position,recipient_email,string_pdf,documentJson,options_page,documentType,template,type_file,folder_name,email_center,step_code,attempted_name,attach_data,importance,last_digitsign,time_expire,status_ref,list_ref)
                return jsonify({'result':'OK','messageText':result_update['messageText'],'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':'missing key','status_Code':200}),200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/count_get_draft_document', methods=['GET'])
# @token_required
def count_get_draft_document():
    if request.method == 'GET':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
                email = token_required['email']
                # email = 'farrutt.th@thai.com'
                print ('email: ',email)
            except Exception as ex:
                abort(404)
        except KeyError as ex:
            return redirect(url_paperless)
        email = request.args.get('email')
        try:
            result_select = select_2().count_select_draft_document_v2_sql(email)
            return jsonify({'result':'OK','messageText':result_select['messageText'],'messageER':None,'status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

# @status_methods.route('/api/get_draft_document', methods=['POST'])
# # @token_required
# def get_draft_document():
#     if request.method == 'POST':
#         try:
#             token_header = request.headers['Authorization']
#             try:                
#                 token_header = str(token_header).split(' ')[1]
#                 token_required = token_required_func(token_header)
#             except Exception as ex:
#                 return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
#         except KeyError as ex:
#             return redirect(url_paperless)
#         datajson = request.json
#         try:
#             if 'email' in datajson and 'limit' in datajson and 'offset' in datajson and len(datajson) == 3:
#                 email = datajson['email']
#                 limit = datajson['limit']
#                 offset = datajson['offset']
#                 result_select = select_2().select_draft_document_v2_sql(email,limit,offset)
#                 return jsonify({'result':'OK','messageText':result_select['messageText'],'messageER':None,'status_Code':200}),200
#         except Exception as e:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_type, fname, exc_tb.tb_lineno)
#             return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/get_draft_document', methods=['POST'])
# @token_required
def get_draft_document():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        datajson = request.json
        try:
            if 'email' in datajson and 'limit' in datajson and 'offset' in datajson and len(datajson) == 3:
                email = datajson['email']
                limit = datajson['limit']
                offset = datajson['offset']
                result_select = select_2().select_draft_document_v2_sql(email,limit,offset)
                return jsonify({'result':'OK','messageText':result_select['messageText'],'messageER':None,'status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/get_draft_document_id', methods=['GET'])
# @token_required
def get_draft_document_id():
    if request.method == 'GET':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
                email = token_required['email']
                # email = 'farrutt.th@thai.com'
                print ('email: ',email)
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        tid = request.args.get('tid')
        try:
            result_select = select_2().select_draft_document_by_id_v2_sql(tid)
            return jsonify({'result':'OK','messageText':result_select['messageText'],'messageER':None,'status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200


@status_methods.route('/api/delete_draft_document', methods=['PUT'])
# @token_required
def delete_draft_document():
    if request.method == 'PUT':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
                email = token_required['email']
                # email = 'farrutt.th@thai.com'
                print ('email: ',email)
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            datajson = request.json
            if 'tid' in datajson and len(datajson) == 1:
                tid = datajson['tid']
                result_delete = update_2().delete_draft_document_v2_sql(tid)
                return jsonify({'result':'OK','messageText':result_delete['messageText'],'messageER':None,'status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200


@status_methods.route('/api/search_draft_document', methods=['POST'])
# @token_required
def search_draft_document():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        datajson = request.json
        try:
            if 'key' in datajson and 'limit' in datajson and 'offset' in datajson and 'email' in datajson and len(datajson) == 4:
                key = datajson['key']
                email = datajson['email']
                limit = datajson['limit']
                offset = datajson['offset']
                result_select = select_2().search_draft_document_v2_sql(key,limit,offset,email)
                return jsonify({'result':'OK','messageText':result_select['messageText'],'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'OK','messageText':'missing key','messageER':None,'status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200


@status_methods.route('/api/count_draft_search', methods=['POST'])
# @token_required
def count_draft_search():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        datajson = request.json
        try:
            if 'key' in datajson and 'email' in datajson and len(datajson) == 2:
                key = datajson['key']
                email = datajson['email']
                result_select = select_2().count_all_draft(key,email)
                return jsonify({'result':'OK','messageText':result_select['messageText'],'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'OK','messageText':'missing key','messageER':None,'status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/get_file_attach', methods=['POST'])
@token_required_v3
def updaget_file_attachte_pdf_v2():
    try: 
        if request.method == 'POST':
            dataFiles = request.files
            list_data =[]
            files = request.files.getlist("file[]")
            unique_foldername = str(uuid.uuid4())
            path = './storage/' + unique_foldername +'/'
            path2 = './storage/' + unique_foldername
            if not os.path.exists(path):
                os.makedirs(path)
            for file in files:
                file_string = base64.b64encode(file.read())
                original_filename = str(file.filename).split('.')[0]
                print(original_filename)
                typefile = str(file.filename).split('.')[-1]
                data = str(file)
                with open(path + original_filename + "." + typefile, "wb") as fh:
                    fh.write(base64.decodebytes(file_string))
                size = os.stat(path + original_filename + "." + typefile).st_size
                content_type = (file.content_type)
                dict_file = {
                    "name" : original_filename +'.'+ typefile,
                    "type" : content_type,
                    "size" : size
                }
                list_data.append(dict_file)
            shutil.rmtree(path)
            return jsonify({'result':'OK','messageText':list_data,'status_Code':200,'messageER':None}),200
    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200