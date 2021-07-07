#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.publicqrcode import *
from method.document import *
from method.callserver import *
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

if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

# # api ดูประเภทเอกสาร และ ค้นหาประเภทเอกสาร แบบมี Limit Offset # #

@status_methods.route('/api/v6/documentdetails', methods=['POST','PUT','GET'])
@token_required
def document_detail_v6_():
    if request.method == 'POST':
        dataJson = request.json
        if 'document_json' in dataJson and 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and 'business_json' in dataJson and 'service_permission' in dataJson and 'other_service_permission' in dataJson and 'chat_bot' in dataJson:
            documentJson = dataJson['document_json']
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            service_permission = dataJson['service_permission']
            other_service_permission = dataJson['other_service_permission']
            chat_bot = dataJson['chat_bot']
            ts = int(time.time())
            documentCode = datetime.datetime.fromtimestamp(ts).strftime('%Y%m-%d%H-%M%S-') + str(uuid.uuid4())
            if service_permission != 'paperless':
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'service permission in incorrect','code':'ERDT999'}}),200
            tmp_other_service_permission = dataJson['other_service_permission']
            if len(str(documentType).replace(' ','')) != 0:
                if len(str(documentType).split(' ')) <= 1:
                    documentType_check = re.findall("([A-Z0-9]+)", str(documentType),re.M|re.I)
                    if documentType_check:
                        if documentType_check[0] == documentType:
                            if len(str(documentType)) > 6:
                                #ERDT006 ห้ามตัวอักษรเกิน 4 ตัวอักษร
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'document type length < 4','code':'ERDT006'}}),200
                            print(documentType_check)
                        else:
                            # ERDT001ไม่ให้มีสัญลักษณ์
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'non have symbols','code':'ERDT001'}}),200
                    else:
                        # ERDT002 ควรเป็นภาษาอังกฤษและตัวพิมพ์ใหญ่
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'pattern incorrect','code':'ERDT002'}}),200
                else:
                    # ERDT003 ไม่ควรมีช่องว่าง
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'no space','code':'ERDT003'}}),200
            else:
                # ERDT004 กรุณากรอก Keyword DocType
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'error document type','code':'ERDT004'}}),200
            business_info = dataJson['business_json']
            result_insert = insert().insert_documentDetails_v5(documentJson,documentUser,email,documentType,documentCode,business_info,service_permission,other_service_permission,chat_bot)
            if result_insert['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':{'data':None,'message':'success','code':'SCDT999'},'messageER':None}),200
            else:
                if result_insert['code'] == 'ERDT990':
                    # ERDT990 found document type duplicate in tax id
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'fail found document type duplicate in tax id','code':'ERDT990'}}),200
                if result_insert['code'] == 'ERDT991':
                    # ERDT991 found document type duplicate in username
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'fail found document type duplicate username','code':'ERDT991'}}),200
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'fail ' + result_insert['messageText'],'code':'ERDT999'}}),200
        elif 'document_code' in dataJson and 'service_permission' in dataJson and len(dataJson) == 2:
            documentCode = dataJson['document_code']
            service_permission = dataJson['service_permission']
            if service_permission != 'paperless':
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'service permission in incorrect','code':'ERDT999'}}),200
            resultDetele = update().update_delete_documentTemplate_v2(documentCode)
            if resultDetele['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':{'data':None,'message':'success','code':'SCDT999'},'messageER':None}),200
            else:
                # ERDT005 ไม่สามารถลบข้อมูลได้เนื่องจากมี template ที่ใช้งานประเภทนี่อยู่
                if 'code' in resultDetele:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'fail','code':resultDetele['code']}}),200
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'fail','code':'ERDT990'}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'data':None,'message':'parameter incorrect','code':'ERDT999'}}),404
    
    elif request.method == 'GET':
        try:
            if request.args.get('limit') != None and request.args.get('offset') != None:
                username = request.args.get('username')
                taxid = request.args.get('taxid')
                documentType = request.args.get('documentType')
                status = request.args.get('status')
                service = request.args.get('service')
                limit = request.args.get('limit')
                offset = request.args.get('offset')
                result = select_1().select_documentTemplateDetails_v6(username,taxid,documentType,status,service,limit,offset)
                if result['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'message':'success','data':result['messageText']} ,'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + result['messageER'],'data':None},'status_Code':200})
            else:
                return jsonify({'result':'ER','messageText': 'parameter incorrect','status_Code':200}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200
        
    elif request.method == 'PUT':
        dataJson = request.json
        if 'document_json' in dataJson and 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and 'document_code' in dataJson and 'business_json' in dataJson and \
            'service_permission' in dataJson and 'other_service_permission' in dataJson and 'chat_bot' in dataJson and len(dataJson) == 9:
            documentJson = dataJson['document_json']
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            documentCode = dataJson['document_code']
            business_info = dataJson['business_json']
            service_permission = dataJson['service_permission']
            if service_permission != 'paperless':
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'service permission in incorrect','code':'ERDT999'}}),200
            other_service_permission = dataJson['other_service_permission']
            tmp_chat_bot = dataJson['chat_bot']
            resultUpdate = update().update_documentTemplate_v5(documentJson,documentUser,email,documentType,documentCode,business_info,service_permission,other_service_permission,tmp_chat_bot)
            if resultUpdate['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':{'data':None,'message':'success','code':'SCDT999'},'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'fail ' + resultUpdate['messageER'],'code':'ERDT999'}}),200
                # return jsonify({'result':'ER','messageText':resultUpdate['messageText'],'status_Code':200,'messageER':resultUpdate['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'data':None,'message':'parameter incorrect','code':'ERDT999'}}),404

@status_methods.route('/api/v6/documentdetails_sum', methods=['GET'])
@token_required
def document_details_sum_v6():
    if request.method == 'GET':
        try:
            username = request.args.get('username')
            taxid = request.args.get('taxid')
            documentType = request.args.get('documentType')
            status = request.args.get('status')
            service = request.args.get('service')
            result = select_1().select_documentTemplateDetails_sum_v6(username,taxid,documentType,status,service)
            if result['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':result['messageText']} ,'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + result['messageER'],'data':None},'status_Code':200})
                 
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200
    else:
        return jsonify({'result':'ER','messageText': 'method incorrect','status_Code':200}),200
    
@status_methods.route('/api/v6/documentdetails/search', methods=['GET'])
@token_required
def document_details_search_v6():
    if request.method == 'GET':
        try:
            if request.args.get('limit') != None and request.args.get('offset') != None and request.args.get('keyword') != None:
                username = request.args.get('username')
                taxid = request.args.get('taxid')
                documentType = request.args.get('documentType')
                status = request.args.get('status')
                service = request.args.get('service')
                limit = request.args.get('limit')
                offset = request.args.get('offset')
                keyword = request.args.get('keyword')
                result = select_1().select_documentTemplateDetails_search_v6(username,taxid,documentType,status,service,limit,offset,keyword)
                if result['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'message':'success','data':result['messageText']} ,'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + result['messageER'],'data':None},'status_Code':200})
            else:
                return jsonify({'result':'ER','messageText': 'parameter incorrect','status_Code':200}),200
                 
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200
    else:
        return jsonify({'result':'ER','messageText': 'method incorrect','status_Code':200}),200

@status_methods.route('/api/v6/documentdetails/search_sum', methods=['GET'])
@token_required
def document_details_search_sum_v6():
    if request.method == 'GET':
        try:
            if request.args.get('keyword') != None:
                username = request.args.get('username')
                taxid = request.args.get('taxid')
                documentType = request.args.get('documentType')
                status = request.args.get('status')
                service = request.args.get('service')
                keyword = request.args.get('keyword')
                result = select_1().select_documentTemplateDetails_search_sum_v6(username,taxid,documentType,status,service,keyword)
                if result['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'message':'success','data':result['messageText']} ,'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + result['messageER'],'data':None},'status_Code':200})
            else:
                return jsonify({'result':'ER','messageText': 'parameter incorrect','status_Code':200}),200
                 
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200
    else:
        return jsonify({'result':'ER','messageText': 'method incorrect','status_Code':200}),200

# # api ดูประเภทเอกสาร และ ค้นหาประเภทเอกสาร แบบมี Limit Offset # #

@status_methods.route('/api/document', methods=['POST'])
@token_required
def document_api():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_id' in dataJson and 'type_file' in dataJson and 'file_id' in dataJson and len(dataJson) == 3:
            resinsert_doc = insert().insert_document(dataJson['step_id'],dataJson['type_file'],dataJson['file_id'])
            if resinsert_doc['result'] == 'OK':
                return jsonify({'result':'OK','messageText':resinsert_doc['messageText'],'document_Id':resinsert_doc['document_Id'],'status_Code':200,'ref_Code':resinsert_doc['ref_id']}),200
            else:
                return jsonify({'result':'ER','messageText':resinsert_doc['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/document/v2', methods=['POST'])
@token_required
def document_api_v2():
    # and 'urgent_type' in dataJson
    if request.method == 'POST':
        dataJson = request.json
        if 'step_id' in dataJson and 'type_file' in dataJson and 'file_id' in dataJson and 'document_json' in dataJson and 'document_type' in dataJson and 'urgent_type' in dataJson  and len(dataJson) == 6:
            resinsert_doc = insert().insert_document(dataJson['step_id'],dataJson['type_file'],dataJson['file_id'],dataJson['document_json'],dataJson['document_type'],dataJson['urgent_type'])
            if resinsert_doc['result'] == 'OK':
                return jsonify({'result':'OK','messageText':resinsert_doc['messageText'],'document_Id':resinsert_doc['document_Id'],'status_Code':200,'ref_Code':resinsert_doc['ref_id']}),200
            else:
                return jsonify({'result':'ER','messageText':resinsert_doc['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/document/v3', methods=['POST'])
@token_required
def document_api_v3():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_id' in dataJson and 'type_file' in dataJson and 'file_id' in dataJson and 'document_json' in dataJson and 'document_type' in dataJson and 'urgent_type' in dataJson and 'digit_sign' in dataJson and len(dataJson) == 7:
            resinsert_doc = insert().insert_document(dataJson['step_id'],dataJson['type_file'],dataJson['file_id'],dataJson['document_json'],dataJson['document_type'],dataJson['urgent_type'],dataJson['digit_sign'])
            if resinsert_doc['result'] == 'OK':
                return jsonify({'result':'OK','messageText':resinsert_doc['messageText'],'document_Id':resinsert_doc['document_Id'],'status_Code':200,'ref_Code':resinsert_doc['ref_id']}),200
            else:
                return jsonify({'result':'ER','messageText':resinsert_doc['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/document/v4', methods=['POST'])
@token_required
def document_api_v4():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_id' in dataJson and 'type_file' in dataJson and 'file_id' in dataJson and 'document_json' in dataJson and 'document_type' in dataJson and 'urgent_type' in dataJson and 'digit_sign' in dataJson and 'attempted_name' in dataJson and len(dataJson) == 8:
            result_DocumentID = document_().genarate_document_ID(dataJson['document_type'])
            if result_DocumentID['result'] == 'OK':
                resinsert_doc = insert().insert_document_new_v(dataJson['step_id'],dataJson['type_file'],dataJson['file_id'],dataJson['document_json'],dataJson['document_type'],dataJson['urgent_type'],dataJson['digit_sign'],dataJson['attempted_name'],result_DocumentID['messageText']['documentID'])
                if resinsert_doc['result'] =='OK':
                    return jsonify({'result':'OK','messageText':resinsert_doc['messageText'],'messageER':None,'document_Id':resinsert_doc['document_Id'],'status_Code':200,'ref_Code':resinsert_doc['ref_id']}),200
                else:
                    return jsonify({'result':'ER','messageText':resinsert_doc['messageText'],'messageER':resinsert_doc['messageER'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':result_DocumentID['messageText'],'messageER':result_DocumentID['messageER'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/v5/document', methods=['POST'])
@token_required
def document_api_v5():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_id' in dataJson and 'type_file' in dataJson and 'file_id' in dataJson and 'document_json' in dataJson and 'document_type' in dataJson and 'urgent_type' in dataJson and 'digit_sign' in dataJson and 'attempted_name' in dataJson and 'sign_page_options' in dataJson and len(dataJson) == 9:
            result_DocumentID = document_().genarate_document_ID(dataJson['document_type'])
            if result_DocumentID['result'] == 'OK':
                resinsert_doc = insert().insert_document_new_v(dataJson['step_id'],dataJson['type_file'],dataJson['file_id'],dataJson['document_json'],dataJson['document_type'],dataJson['urgent_type'],dataJson['digit_sign'],dataJson['attempted_name'],result_DocumentID['messageText']['documentID'],dataJson['sign_page_options'],None)
                if resinsert_doc['result'] =='OK':
                    return jsonify({'result':'OK','messageText':resinsert_doc['messageText'],'messageER':None,'document_Id':resinsert_doc['document_Id'],'status_Code':200,'ref_Code':resinsert_doc['ref_id']}),200
                else:
                    return jsonify({'result':'ER','messageText':resinsert_doc['messageText'],'messageER':resinsert_doc['messageER'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':result_DocumentID['messageText'],'messageER':result_DocumentID['messageER'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/v6/document', methods=['POST'])
@token_required
def document_api_v6():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_id' in dataJson and 'type_file' in dataJson and 'file_id' in dataJson and 'document_json' in dataJson and 'document_type' in dataJson and 'urgent_type' in dataJson and 'digit_sign' in dataJson and 'attempted_name' in dataJson and 'sign_page_options' in dataJson and 'options_page' in dataJson and len(dataJson) == 10:
            result_DocumentID = document_().genarate_document_ID(dataJson['document_type'])
            if result_DocumentID['result'] == 'OK':
                resinsert_doc = insert().insert_document_new_v(dataJson['step_id'],dataJson['type_file'],dataJson['file_id'],dataJson['document_json'],dataJson['document_type'],dataJson['urgent_type'],dataJson['digit_sign'],dataJson['attempted_name'],result_DocumentID['messageText']['documentID'],dataJson['sign_page_options'],dataJson['options_page'])
                if resinsert_doc['result'] =='OK':
                    return jsonify({'result':'OK','messageText':resinsert_doc['messageText'],'messageER':None,'document_Id':resinsert_doc['document_Id'],'status_Code':200,'ref_Code':resinsert_doc['ref_id']}),200
                else:
                    return jsonify({'result':'ER','messageText':resinsert_doc['messageText'],'messageER':resinsert_doc['messageER'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':result_DocumentID['messageText'],'messageER':result_DocumentID['messageER'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/documentdetails/v1', methods=['POST','PUT','GET'])
@token_required
def document_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'document_json' in dataJson and 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and len(dataJson) == 4:
            documentJson = dataJson['document_json']
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            ts = int(time.time())
            documentCode = datetime.datetime.fromtimestamp(ts).strftime('%Y%m-%d%H-%M%S-') + str(uuid.uuid4())
            result_insert = insert().insert_documentDetails(documentJson,documentUser,email,documentType,documentCode)
            if result_insert['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':result_insert['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
        elif 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and len(dataJson) == 3:
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            resultDetele = update().update_delete_documentTemplate_v1(email,documentUser,documentType)
            if resultDetele['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':resultDetele['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':resultDetele['messageText'],'status_Code':200,'messageER':resultDetele['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('documentType')) == None and (request.args.get('status')) == None:
            select_get = select().select_documentTemplateDetails_v1(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('documentType')) != None and (request.args.get('status')) == None:
            select_get = select().select_documentTemplateDetailsAndDocumentType_v1(str(request.args.get('username')).replace(' ',''),str(request.args.get('documentType')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) != None:
            select_get = select().select_documentTemplateDetails_v1_status(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        return jsonify({'result':'OK','status_Code':200,'messageText':None}),200
    elif request.method == 'PUT':
        dataJson = request.json
        if 'document_json' in dataJson and 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and 'document_code' in dataJson and len(dataJson) == 5:
            documentJson = dataJson['document_json']
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            documentCode = dataJson['document_code']
            resultUpdate = update().update_documentTemplate_v1(documentJson,documentUser,email,documentType,documentCode)
            if resultUpdate['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':resultUpdate['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':resultUpdate['messageText'],'status_Code':200,'messageER':resultUpdate['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect','status_Code':404}),404

@status_methods.route('/api/v2/documentdetails', methods=['POST','PUT','GET'])
@token_required
def document_details_v2():
    if request.method == 'POST':
        dataJson = request.json
        if 'document_json' in dataJson and 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and 'business_json' in dataJson and len(dataJson) == 5:
            documentJson = dataJson['document_json']
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            if len(str(documentType).replace(' ','')) != 0:
                if len(str(documentType).split(' ')) <= 1:
                    documentType_check = re.findall("([A-Z0-9]+)", str(documentType),re.M|re.I)
                    if documentType_check:
                        if documentType_check[0] == documentType:
                            print(documentType_check)
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error document type  msg: no have symbols'}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error document type  msg: pattern incorrect'}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error document type  msg: no space'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error document type'}),200
            business_info = dataJson['business_json']
            ts = int(time.time())
            documentCode = datetime.datetime.fromtimestamp(ts).strftime('%Y%m-%d%H-%M%S-') + str(uuid.uuid4())
            result_insert = insert().insert_documentDetails_v2(documentJson,documentUser,email,documentType,documentCode,business_info)
            if result_insert['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':result_insert['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
        elif 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and len(dataJson) == 3:
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            resultDetele = update().update_delete_documentTemplate_v1(email,documentUser,documentType)
            if resultDetele['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':resultDetele['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':resultDetele['messageText'],'status_Code':200,'messageER':resultDetele['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('documentType')) == None and (request.args.get('status')) == None:
            select_get = select().select_documentTemplateDetails_v1(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('documentType')) == None and (request.args.get('status')) == None and (request.args.get('taxid')) != None:
            select_get = select().select_documentTemplateDetails_v2_tax(str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('documentType')) != None and (request.args.get('status')) == None:
            select_get = select().select_documentTemplateDetailsAndDocumentType_v1(str(request.args.get('username')).replace(' ',''),str(request.args.get('documentType')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) != None:
            select_get = select().select_documentTemplateDetails_v1_status(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        return jsonify({'result':'OK','status_Code':200,'messageText':None}),200
    elif request.method == 'PUT':
        dataJson = request.json
        if 'document_json' in dataJson and 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and 'document_code' in dataJson and 'business_json' in dataJson and len(dataJson) == 6:
            documentJson = dataJson['document_json']
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            documentCode = dataJson['document_code']
            business_info = dataJson['business_json']
            resultUpdate = update().update_documentTemplate_v2(documentJson,documentUser,email,documentType,documentCode,business_info)
            if resultUpdate['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':resultUpdate['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':resultUpdate['messageText'],'status_Code':200,'messageER':resultUpdate['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect','status_Code':404}),404

@status_methods.route('/api/v3/documentdetails', methods=['POST','PUT','GET'])
@token_required
def document_details_v3():
    if request.method == 'POST':
        dataJson = request.json
        if 'document_json' in dataJson and 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and 'business_json' in dataJson and 'service_permission' in dataJson and len(dataJson) == 6:
            documentJson = dataJson['document_json']
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            service_permission = dataJson['service_permission']
            if len(str(documentType).replace(' ','')) != 0:
                if len(str(documentType).split(' ')) <= 1:
                    documentType_check = re.findall("([A-Z0-9]+)", str(documentType),re.M|re.I)
                    if documentType_check:
                        if documentType_check[0] == documentType:
                            print(documentType_check)
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error document type  msg: no have symbols'}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error document type  msg: pattern incorrect'}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error document type  msg: no space'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error document type'}),200
            business_info = dataJson['business_json']
            ts = int(time.time())
            documentCode = datetime.datetime.fromtimestamp(ts).strftime('%Y%m-%d%H-%M%S-') + str(uuid.uuid4())
            result_insert = insert().insert_documentDetails_v2(documentJson,documentUser,email,documentType,documentCode,business_info,service_permission)
            if result_insert['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':result_insert['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
        elif 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and len(dataJson) == 3:
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            resultDetele = update().update_delete_documentTemplate_v1(email,documentUser,documentType)
            if resultDetele['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':resultDetele['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':resultDetele['messageText'],'status_Code':200,'messageER':resultDetele['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('documentType')) == None and (request.args.get('status')) == None:
            select_get = select().select_documentTemplateDetails_v1(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('documentType')) == None and (request.args.get('status')) == None and (request.args.get('taxid')) != None and (request.args.get('service')) == None:
            select_get = select().select_documentTemplateDetails_v2_tax(str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('documentType')) != None and (request.args.get('status')) == None:
            select_get = select().select_documentTemplateDetailsAndDocumentType_v1(str(request.args.get('username')).replace(' ',''),str(request.args.get('documentType')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) != None:
            select_get = select().select_documentTemplateDetails_v1_status(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) == None and (request.args.get('service')) != None and (request.args.get('taxid')) == None:
            select_get = select().select_documentTemplateDetails_list_service_v1(str(request.args.get('username')).replace(' ',''),str(request.args.get('service')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('status')) == None and (request.args.get('service')) != None and (request.args.get('taxid')) != None:
            select_get = select().select_documentTemplateDetails_list_service_v1_tax(str(request.args.get('taxid')).replace(' ',''),str(request.args.get('service')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        return jsonify({'result':'OK','status_Code':200,'messageText':None}),200
    elif request.method == 'PUT':
        dataJson = request.json
        if 'document_json' in dataJson and 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and 'document_code' in dataJson and 'business_json' in dataJson and 'service_permission' in dataJson and len(dataJson) == 7:
            documentJson = dataJson['document_json']
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            documentCode = dataJson['document_code']
            business_info = dataJson['business_json']
            service_permission = dataJson['service_permission']
            resultUpdate = update().update_documentTemplate_v2(documentJson,documentUser,email,documentType,documentCode,business_info,service_permission)
            if resultUpdate['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':resultUpdate['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':resultUpdate['messageText'],'status_Code':200,'messageER':resultUpdate['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect','status_Code':404}),404

@status_methods.route('/api/v4/documentdetails', methods=['POST','PUT','GET'])
@token_required_v3
def document_details_v4():
    if request.method == 'POST':
        dataJson = request.json
        if 'document_json' in dataJson and 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and 'business_json' in dataJson and 'service_permission' in dataJson and len(dataJson) == 6:
            documentJson = dataJson['document_json']
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            service_permission = dataJson['service_permission']
            if len(str(documentType).replace(' ','')) != 0:
                if len(str(documentType).split(' ')) <= 1:
                    documentType_check = re.findall("([A-Z0-9]+)", str(documentType),re.M|re.I)
                    if documentType_check:
                        if documentType_check[0] == documentType:
                            print(documentType_check)
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error document type  msg: no have symbols'}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error document type  msg: pattern incorrect'}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error document type  msg: no space'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error document type'}),200
            business_info = dataJson['business_json']
            ts = int(time.time())
            documentCode = datetime.datetime.fromtimestamp(ts).strftime('%Y%m-%d%H-%M%S-') + str(uuid.uuid4())
            result_insert = insert().insert_documentDetails_v2(documentJson,documentUser,email,documentType,documentCode,business_info,service_permission)
            if result_insert['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':result_insert['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
        elif 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and len(dataJson) == 3:
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            resultDetele = update().update_delete_documentTemplate_v1(email,documentUser,documentType)
            if resultDetele['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':resultDetele['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':resultDetele['messageText'],'status_Code':200,'messageER':resultDetele['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('documentType')) == None and (request.args.get('status')) == None:
            select_get = select().select_documentTemplateDetails_v1(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('documentType')) == None and (request.args.get('status')) == None and (request.args.get('taxid')) != None and (request.args.get('service')) == None:
            select_get = select().select_documentTemplateDetails_v2_tax(str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('documentType')) != None and (request.args.get('status')) == None:
            select_get = select().select_documentTemplateDetailsAndDocumentType_v1(str(request.args.get('username')).replace(' ',''),str(request.args.get('documentType')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) != None:
            select_get = select().select_documentTemplateDetails_v1_status(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) == None and (request.args.get('service')) != None and (request.args.get('taxid')) == None:
            select_get = select().select_documentTemplateDetails_list_service_v1(str(request.args.get('username')).replace(' ',''),str(request.args.get('service')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('status')) == None and (request.args.get('service')) != None and (request.args.get('taxid')) != None:
            select_get = select().select_documentTemplateDetails_list_service_v1_tax(str(request.args.get('taxid')).replace(' ',''),str(request.args.get('service')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        return jsonify({'result':'OK','status_Code':200,'messageText':None}),200
    elif request.method == 'PUT':
        dataJson = request.json
        if 'document_json' in dataJson and 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and 'document_code' in dataJson and 'business_json' in dataJson and 'service_permission' in dataJson and len(dataJson) == 7:
            documentJson = dataJson['document_json']
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            documentCode = dataJson['document_code']
            business_info = dataJson['business_json']
            service_permission = dataJson['service_permission']
            resultUpdate = update().update_documentTemplate_v2(documentJson,documentUser,email,documentType,documentCode,business_info,service_permission)
            if resultUpdate['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':resultUpdate['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':resultUpdate['messageText'],'status_Code':200,'messageER':resultUpdate['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect','status_Code':404}),404

@status_methods.route('/api/v5/documentdetails', methods=['POST','PUT','GET'])
@token_required_v3
def document_details_v5():
    if request.method == 'POST':
        dataJson = request.json
        if 'document_json' in dataJson and 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and 'business_json' in dataJson and 'service_permission' in dataJson and 'other_service_permission' in dataJson and 'chat_bot' in dataJson:
            documentJson = dataJson['document_json']
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            service_permission = dataJson['service_permission']
            other_service_permission = dataJson['other_service_permission']
            chat_bot = dataJson['chat_bot']
            ts = int(time.time())
            documentCode = datetime.datetime.fromtimestamp(ts).strftime('%Y%m-%d%H-%M%S-') + str(uuid.uuid4())
            if service_permission != 'paperless':
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'service permission in incorrect','code':'ERDT999'}}),200
            tmp_other_service_permission = dataJson['other_service_permission']
            if len(str(documentType).replace(' ','')) != 0:
                if len(str(documentType).split(' ')) <= 1:
                    documentType_check = re.findall("([A-Z0-9]+)", str(documentType),re.M|re.I)
                    if documentType_check:
                        if documentType_check[0] == documentType:
                            if len(str(documentType)) > 6:
                                #ERDT006 ห้ามตัวอักษรเกิน 4 ตัวอักษร
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'document type length < 4','code':'ERDT006'}}),200
                            print(documentType_check)
                        else:
                            # ERDT001ไม่ให้มีสัญลักษณ์
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'non have symbols','code':'ERDT001'}}),200
                    else:
                        # ERDT002 ควรเป็นภาษาอังกฤษและตัวพิมพ์ใหญ่
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'pattern incorrect','code':'ERDT002'}}),200
                else:
                    # ERDT003 ไม่ควรมีช่องว่าง
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'no space','code':'ERDT003'}}),200
            else:
                # ERDT004 กรุณากรอก Keyword DocType
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'error document type','code':'ERDT004'}}),200
            business_info = dataJson['business_json']
            result_insert = insert().insert_documentDetails_v5(documentJson,documentUser,email,documentType,documentCode,business_info,service_permission,other_service_permission,chat_bot)
            if result_insert['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':{'data':None,'message':'success','code':'SCDT999'},'messageER':None}),200
            else:
                if result_insert['code'] == 'ERDT990':
                    # ERDT990 found document type duplicate in tax id
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'fail found document type duplicate in tax id','code':'ERDT990'}}),200
                if result_insert['code'] == 'ERDT991':
                    # ERDT991 found document type duplicate in username
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'fail found document type duplicate username','code':'ERDT991'}}),200
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'fail ' + result_insert['messageText'],'code':'ERDT999'}}),200
        elif 'document_code' in dataJson and 'service_permission' in dataJson and len(dataJson) == 2:
            documentCode = dataJson['document_code']
            service_permission = dataJson['service_permission']
            if service_permission != 'paperless':
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'service permission in incorrect','code':'ERDT999'}}),200
            resultDetele = update().update_delete_documentTemplate_v2(documentCode)
            if resultDetele['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':{'data':None,'message':'success','code':'SCDT999'},'messageER':None}),200
            else:
                # ERDT005 ไม่สามารถลบข้อมูลได้เนื่องจากมี template ที่ใช้งานประเภทนี่อยู่
                if 'code' in resultDetele:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'fail','code':resultDetele['code']}}),200
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'fail','code':'ERDT990'}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'data':None,'message':'parameter incorrect','code':'ERDT999'}}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('documentType')) == None and (request.args.get('status')) == None:
            select_get = select().select_documentTemplateDetails_v5(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('documentType')) == None and (request.args.get('status')) == None and (request.args.get('taxid')) != None and (request.args.get('service')) == None:
            select_get = select().select_documentTemplateDetails_v5_tax(str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('documentType')) != None and (request.args.get('status')) == None:
            select_get = select().select_documentTemplateDetailsAndDocumentType_v1(str(request.args.get('username')).replace(' ',''),str(request.args.get('documentType')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) != None:
            select_get = select().select_documentTemplateDetails_v1_status(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) == None and (request.args.get('service')) != None and (request.args.get('taxid')) == None:
            select_get = select().select_documentTemplateDetails_list_service_v1(str(request.args.get('username')).replace(' ',''),str(request.args.get('service')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('status')) == None and (request.args.get('service')) != None and (request.args.get('taxid')) != None:
            select_get = select().select_documentTemplateDetails_list_service_v1_tax(str(request.args.get('taxid')).replace(' ',''),str(request.args.get('service')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':select_get['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        return jsonify({'result':'OK','status_Code':200,'messageText':None}),200
    elif request.method == 'PUT':
        dataJson = request.json
        if 'document_json' in dataJson and 'document_user' in dataJson and 'email' in dataJson and 'document_type' in dataJson and 'document_code' in dataJson and 'business_json' in dataJson and \
            'service_permission' in dataJson and 'other_service_permission' in dataJson and 'chat_bot' in dataJson and len(dataJson) == 9:
            documentJson = dataJson['document_json']
            documentUser = dataJson['document_user']
            email = dataJson['email']
            documentType = dataJson['document_type']
            documentCode = dataJson['document_code']
            business_info = dataJson['business_json']
            service_permission = dataJson['service_permission']
            if service_permission != 'paperless':
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'service permission in incorrect','code':'ERDT999'}}),200
            other_service_permission = dataJson['other_service_permission']
            tmp_chat_bot = dataJson['chat_bot']
            resultUpdate = update().update_documentTemplate_v5(documentJson,documentUser,email,documentType,documentCode,business_info,service_permission,other_service_permission,tmp_chat_bot)
            if resultUpdate['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':{'data':None,'message':'success','code':'SCDT999'},'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'fail ' + resultUpdate['messageER'],'code':'ERDT999'}}),200
                # return jsonify({'result':'ER','messageText':resultUpdate['messageText'],'status_Code':200,'messageER':resultUpdate['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'data':None,'message':'parameter incorrect','code':'ERDT999'}}),404