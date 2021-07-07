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
from method.callwebHook import *
from method.pdf import *
from method.callserver import *



if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

@status_methods.route('/api/v1/step/addemail_sign',methods=['PUT'])
@token_required_v3
def addsign():
    if request.method == 'PUT':
        dataJson = request.json
        if 'sid' in dataJson and 'email' in dataJson and 'step' in dataJson and 'email_step' in dataJson and len(dataJson) == 4 :
            sid = dataJson['sid']
            email = dataJson['email']
            step = dataJson['step']
            email_step = dataJson['email_step']
            result_update = update_2().update_json(sid,email,step,email_step)
            if result_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200
            else :
                return jsonify({'result':'ER','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200           
        else :
            abort(404)


@status_methods.route('/api/step/v2', methods=['PUT','GET'])
@token_required
def update_step_v2():
    if request.method == 'PUT':
        dataJson = request.json
        if 'step_data_sid' in dataJson and 'sign_email' in dataJson and 'activity_code' in dataJson and 'activity_status' in dataJson and 'step_num' in dataJson and 'signlat' in dataJson and 'signlong' in dataJson and len(dataJson) == 7:
            check_update = update().update_step_v2(dataJson['step_data_sid'],dataJson['sign_email'],dataJson['activity_code'],dataJson['activity_status'],dataJson['step_num'],dataJson['signlat'],dataJson['signlong'])
            if check_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Update OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':check_update['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if request.args.get('sid') != None:
            select_get_datastep = select().select_get_stepdata(request.args.get('sid'))
            if select_get_datastep['result'] == 'OK':
                return jsonify(select_get_datastep),200
            else:
                return jsonify({'result':'ER','messageText':select_get_datastep['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/v3/step', methods=['PUT','GET'])
@token_required
def update_step_api_v3():
    if request.method == 'PUT':
        dataJson = request.json
        if 'step_data_sid' in dataJson and 'sign_email' in dataJson and 'activity_code' in dataJson and 'activity_status' in dataJson and 'step_num' in dataJson and 'signlat' in dataJson and 'signlong' in dataJson and len(dataJson) == 7:
            check_update = update().update_step_v3(dataJson['step_data_sid'],dataJson['sign_email'],dataJson['activity_code'],dataJson['activity_status'],dataJson['step_num'],dataJson['signlat'],dataJson['signlong'])
            if check_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'data':None,'message':check_update['messageText']},'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':check_update['messageText']},'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'parameter incorrect'},'status_Code':404}),404
    elif request.method == 'GET':
        if request.args.get('sid') != None:
            select_get_datastep = select().select_get_stepdata(request.args.get('sid'))
            if select_get_datastep['result'] == 'OK':
                return jsonify(select_get_datastep),200
            else:
                return jsonify({'result':'ER','messageText':select_get_datastep['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404


@status_methods.route('/api/v4/step', methods=['PUT','GET'])
@token_required_v3
def update_step_api_v4():
    if request.method == 'PUT':
        try:
            if 'Authorization' not in request.headers:
                abort(401)
            token_header = request.headers['Authorization']
            token_oneid = (str(token_header).split(' ')[1])
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        check_update = {}
        if 'step_data_sid' in dataJson and 'sign_email' in dataJson and 'activity_code' in dataJson and 'activity_status' in dataJson and 'step_num' in dataJson and 'signlat' in dataJson and 'signlong' in dataJson and 'sign_id' in dataJson and len(dataJson) == 8:
            sidCode = dataJson['step_data_sid']
            query_detail_document = select().select_data_for_chat_v1(sidCode)
            if query_detail_document['result'] == 'OK':
                tmp_data_detail = query_detail_document['messageText']
                tmp_document_id = tmp_data_detail['document_id']
                tmp_sender_name = tmp_data_detail['sender_name']
                tmp_email_sender = tmp_data_detail['sender_email']
                tmp_body_text = tmp_data_detail['body_text']
                tmpfid = tmp_data_detail['fid']
            strname_surname = fine_name_surename(dataJson['sign_email'])
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            sidcodehash = hashlib.sha512(str(sidCode).encode('utf-8')).hexdigest()
            url = url_ip_eform + '/api/v1/send_chat_ppl?paperless_id=' +sidcodehash
            tmp_calleformstatus = executor.submit(callGET_v2 ,url  ,token_header)
            check_update = update().update_step_v4(dataJson['step_data_sid'],dataJson['sign_email'],dataJson['activity_code'],dataJson['activity_status'],dataJson['step_num'],dataJson['signlat'],dataJson['signlong'],dataJson['sign_id'])
            if check_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'data':None,'message':check_update['messageText']},'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':check_update['messageText']},'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'parameter incorrect'},'status_Code':404}),404
    elif request.method == 'GET':
        if request.args.get('sid') != None:
            select_get_datastep = select().select_get_stepdata(request.args.get('sid'))
            if select_get_datastep['result'] == 'OK':
                return jsonify(select_get_datastep),200
            else:
                return jsonify({'result':'ER','messageText':select_get_datastep['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404