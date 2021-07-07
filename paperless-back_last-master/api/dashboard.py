#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.cal_users import *
from method.publicqrcode import *
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


if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less


@status_methods.route('/dashboard/<string:type_dashboard>/v1', methods=['POST'])
@token_required
def dashboard_v1(type_dashboard):
    if type_dashboard == 'sender':
        if request.method == 'POST':
            dataJson = request.json
            if 'username' in dataJson and 'secret_key' in dataJson and len(dataJson) == 2:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    user_Name = str(dataJson['username']).lower()
                    result_select = select().select_dashboard_sender(user_Name)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and len(dataJson) == 2:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select().select_dashboard_recipient(emailUser)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'type incorrect (string - sender or recipient)'}),200

@status_methods.route('/dashboard/v2/<string:type_dashboard>', methods=['POST'])
@token_required
def dashboard_v2(type_dashboard):
    if type_dashboard == 'sender':
        if request.method == 'POST':
            dataJson = request.json
            if 'username' in dataJson and 'secret_key' in dataJson and len(dataJson) == 2:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    user_Name = str(dataJson['username']).lower()
                    result_select = select().select_dashboard_sender(user_Name)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and len(dataJson) == 2:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select().select_dashboard_recipient_v2(emailUser)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'type incorrect (string - sender or recipient)'}),200

@status_methods.route('/dashboard/v3/<string:type_dashboard>', methods=['POST'])
def dashboard_v3(type_dashboard):
    if type_dashboard == 'sender':
        if request.method == 'POST':
            dataJson = request.json
            if 'username' in dataJson and 'emailUser' in dataJson and 'secret_key' in dataJson and len(dataJson) == 3:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    user_Name = str(dataJson['username']).lower()
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select().select_dashboard_sender_v3(user_Name,emailUser)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and len(dataJson) == 2:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select().select_dashboard_recipient_v3(emailUser)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'type incorrect (string - sender or recipient)'}),200

@status_methods.route('/api/v1/document/<string:type_dashboard>', methods=['GET'])
@token_required_v3
def document_api_v1(type_dashboard):
    if type_dashboard == 'recipient_external':
        if request.method == 'GET':
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            sort_key = request.args.get('sort_key')
            group_status = request.args.get('group_status')
            datetime_tmp = request.args.get('datetime')
            timeapprove = bool(request.args.get('timeapprove'))
            if email == None or secret_key == None  or limit == None or offset == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            if timeapprove == '':
                timeapprove = None
            email = str(email).lower()
            r_listtax_id = email_to_business(email)
            result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,None,None,None,r_listtax_id,sort_key,group_status,datetime_tmp,tmptimeapprove=timeapprove)
            if result_select['result'] == 'OK':
                if result_select['messageText']['document'] != []:
                    max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_last'])['update_last']
                    max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
                else:
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'sum_recipient_external':
        if request.method == 'GET':
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            document_type = request.args.get('document_type')
            group_status = request.args.get('group_status')
            datetime_tmp = request.args.get('datetime')
            if email == None or secret_key == None or document_type == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            email = str(email).lower()
            r_listtax_id = email_to_business(email)
            result_select = select_3().select_recp_count_v1(type_dashboard,email,document_type,r_listtax_id,'',group_status,pick_datetime=datetime_tmp)
            if result_select['result'] == 'OK':
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'recipient_external_search':
        if request.method == 'GET':
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            document_type = request.args.get('document_type')
            keyword = request.args.get('keyword')
            sort_key = request.args.get('sort_key')
            datetime_tmp = request.args.get('datetime')
            timeapprove = bool(request.args.get('timeapprove'))
            if email == None or secret_key == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            if timeapprove == '':
                timeapprove = None
            email = str(email).lower()
            r_listtax_id = email_to_business(email)
            result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,document_type,keyword,'',r_listtax_id,sort_key,pick_datetime=datetime_tmp,tmptimeapprove=timeapprove)
            if result_select['result'] == 'OK':
                if result_select['messageText']['document'] != []:
                    max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_last'])['update_last']
                    max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
                else:
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'filter_recipient_external':
        if request.method == 'GET':
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            document_type = request.args.get('document_type')
            status = request.args.get('status')
            sort_key = request.args.get('sort_key')
            group_status = request.args.get('group_status')
            datetime_tmp = request.args.get('datetime')
            timeapprove = bool(request.args.get('timeapprove'))
            if email == None or secret_key == None or limit == None or offset == None or document_type == None or status == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            if timeapprove == '':
                timeapprove = None
            email = str(email).lower()
            r_listtax_id = email_to_business(email)
            result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,document_type,'',status,r_listtax_id,sort_key,group_status,pick_datetime=datetime_tmp,tmptimeapprove=timeapprove)
            if result_select['result'] == 'OK':
                if result_select['messageText']['document'] != []:
                    max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_last'])['update_last']
                    max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
                else:
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'sum_filter_recipient_external':
        if request.method == 'GET':
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            document_type = request.args.get('document_type')
            group_status = request.args.get('group_status')
            datetime_tmp = request.args.get('datetime')
            if email == None or secret_key == None or document_type == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            email = str(email).lower()
            r_listtax_id = email_to_business(email)
            result_select = select_3().select_recp_count_v1(type_dashboard,email,document_type,r_listtax_id,'',group_status,pick_datetime=datetime_tmp)
            if result_select['result'] == 'OK':
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'sum_search_recipient_external':
        if request.method == 'GET':
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            document_type = request.args.get('document_type')
            keyword = request.args.get('keyword')
            datetime_tmp = request.args.get('datetime')
            if email == None or secret_key == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            email = str(email).lower()
            r_listtax_id = email_to_business(email)
            result_select = select_3().select_recp_count_v1(type_dashboard,email,document_type,r_listtax_id,keyword,pick_datetime=datetime_tmp)
            if result_select['result'] == 'OK':
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'sum_filter':
        if request.method == 'GET':
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            document_type = request.args.get('document_type')
            tax_id = request.args.get('tax_id')
            group_status = request.args.get('group_status')
            datetime_tmp = request.args.get('datetime')
            if email == None or secret_key == None or document_type == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            email = str(email).lower()
            result_select = select_3().select_recp_count_v1(type_dashboard,email,document_type,tax_id,'',group_status,pick_datetime=datetime_tmp)
            if result_select['result'] == 'OK':
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'sum':
        if request.method == 'GET':
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            tax_id = request.args.get('tax_id')
            group_status = request.args.get('group_status')
            datetime_tmp = request.args.get('datetime')
            if email == None or secret_key == None or tax_id == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            email = str(email).lower()
            result_select = select_3().select_recp_count_v1(type_dashboard,email,'',tax_id,'',group_status,pick_datetime=datetime_tmp)
            if result_select['result'] == 'OK':
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'sum_recipient_search':
        if request.method == 'GET':
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            tax_id = request.args.get('tax_id')
            document_type = request.args.get('document_type')
            keyword = request.args.get('keyword')
            datetime_tmp = request.args.get('datetime')
            if email == None or secret_key == None or tax_id == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            email = str(email).lower()
            result_select = select_3().select_recp_count_v1(type_dashboard,email,document_type,tax_id,keyword,pick_datetime=datetime_tmp)
            if result_select['result'] == 'OK':
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'recipient':
        if request.method == 'GET':
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            tax_id = request.args.get('tax_id')
            sort_key = request.args.get('sort_key')
            group_status = request.args.get('group_status')
            datetime_tmp = request.args.get('datetime')
            timeapprove = bool(request.args.get('timeapprove'))
            if email == None or secret_key == None or limit == None or offset == None or tax_id == None :
                abort(404)    
            if datetime_tmp == '':
                datetime_tmp = None
            if timeapprove == '':
                timeapprove = None
            email = str(email).lower()
            result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,None,None,None,tax_id,sort_key,group_status,datetime_tmp,tmptimeapprove=timeapprove)
            
            # print ('max_update_time:',max_update_time)
            # print ('max_update_time_ts:',max_update_time_ts)
            if result_select['result'] == 'OK':
                if result_select['messageText']['document'] != []:
                    max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_last'])['update_last']
                    max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
                else:
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'recipient_update':
        if request.method == 'GET':
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            tax_id = request.args.get('tax_id')
            sort_key = request.args.get('sort_key')
            group_status = request.args.get('group_status')
            datetime_tmp = request.args.get('datetime')
            timestamp = request.args.get('timestamp')
            timeapprove = bool(request.args.get('timeapprove'))
            if email == None or secret_key == None or limit == None or offset == None or tax_id == None or timestamp == None:
                abort(404)    
            if datetime_tmp == '':
                datetime_tmp = None
            if timeapprove == '':
                timeapprove = None
            email = str(email).lower()
            result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,None,None,None,tax_id,sort_key,group_status,datetime_tmp,timestamp,tmptimeapprove=timeapprove)
            # max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_time'])['update_time']
            # max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
            if result_select['result'] == 'OK':
                if result_select['messageText']['document'] != []:
                    max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_last'])['update_last']
                    max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
                else:
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'recipient_search':
        if request.method == 'GET':
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            document_type = request.args.get('document_type')
            keyword = request.args.get('keyword')
            tax_id = request.args.get('tax_id')
            sort_key = request.args.get('sort_key')
            datetime_tmp = request.args.get('datetime')
            timeapprove = bool(request.args.get('timeapprove'))
            if email == None or secret_key == None or limit == None or offset == None or document_type == None or keyword == None or tax_id == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            if timeapprove == '':
                timeapprove = None
            email = str(email).lower()
            result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,document_type,keyword,'',tax_id,sort_key,pick_datetime=datetime_tmp,tmptimeapprove=timeapprove)
            if result_select['result'] == 'OK':
                if result_select['messageText']['document'] != []:
                    max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_last'])['update_last']
                    max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
                else:
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'recipient_filter':
        if request.method == 'GET':
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            document_type = request.args.get('document_type')
            status = request.args.get('status')
            tax_id = request.args.get('tax_id')
            sort_key = request.args.get('sort_key')
            group_status = request.args.get('group_status')
            datetime_tmp = request.args.get('datetime')
            timeapprove = bool(request.args.get('timeapprove'))
            if email == None or secret_key == None or limit == None or offset == None or document_type == None or status == None or tax_id == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            if timeapprove == '':
                timeapprove = None
            email = str(email).lower()
            result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,document_type,'',status,tax_id,sort_key,group_status,datetime_tmp,tmptimeapprove=timeapprove)
            if result_select['result'] == 'OK':
                if result_select['messageText']['document'] != []:
                    max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_last'])['update_last']
                    max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
                else:
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'recipient_filter_update':
        if request.method == 'GET':
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            document_type = request.args.get('document_type')
            status = request.args.get('status')
            tax_id = request.args.get('tax_id')
            sort_key = request.args.get('sort_key')
            group_status = request.args.get('group_status')
            datetime_tmp = request.args.get('datetime')
            timestamp = request.args.get('timestamp')
            timeapprove = bool(request.args.get('timeapprove'))
            if email == None or secret_key == None or limit == None or offset == None or document_type == None or status == None or tax_id == None or timestamp == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            if timeapprove == '':
                timeapprove = None
            email = str(email).lower()
            result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,document_type,'',status,tax_id,sort_key,group_status,datetime_tmp,timestamp,tmptimeapprove=timeapprove)
            if result_select['result'] == 'OK':
                if result_select['messageText']['document'] != []:
                    max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_last'])['update_last']
                    max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
                else:
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'sender_sum':
        if request.method == 'GET':
            username = request.args.get('username')
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            tax_id = request.args.get('tax_id')
            group_status = request.args.get('group_status')
            datetime_tmp = request.args.get('datetime')
            if username == None or email == None or secret_key == None or tax_id == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            email = str(email).lower()
            result_select = select_3().select_document_sender_count_v1(type_dashboard,username,email,'',tax_id,'',group_status,pick_datetime=datetime_tmp)
            if result_select['result'] == 'OK':
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'sender_sum_filter':
        if request.method == 'GET':
            username = request.args.get('username')
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            document_type = request.args.get('document_type')
            tax_id = request.args.get('tax_id')
            group_status = request.args.get('group_status')
            datetime_tmp = request.args.get('datetime')
            if username == None or email == None or secret_key == None or document_type == None or tax_id == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            email = str(email).lower()
            result_select = select_3().select_document_sender_count_v1(type_dashboard,username,email,document_type,tax_id,'',group_status,pick_datetime=datetime_tmp)
            if result_select['result'] == 'OK':
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'sender_sum_search':
        if request.method == 'GET':
            username = request.args.get('username')
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            document_type = request.args.get('document_type')
            tax_id = request.args.get('tax_id')
            keyword = request.args.get('keyword')
            datetime_tmp = request.args.get('datetime')
            if username == None or email == None or secret_key == None or document_type == None or tax_id == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None
            email = str(email).lower()
            result_select = select_3().select_document_sender_count_v1(type_dashboard,username,email,document_type,tax_id,keyword,pick_datetime=datetime_tmp)
            if result_select['result'] == 'OK':
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'sender':
        if request.method == 'GET':
            username = request.args.get('username')
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            tax_id = request.args.get('tax_id')
            sort_key = request.args.get('sort_key')
            group_status = request.args.get('group_status')
            datetime_tmp = request.args.get('datetime')
            timeapprove = bool(request.args.get('timeapprove'))
            if email == None or username == None or secret_key == None or limit == None or offset == None or tax_id == None:
                abort(404)      
            if datetime_tmp == '':
                datetime_tmp = None
            if timeapprove == '':
                timeapprove = None
            email = str(email).lower()
            result_select = select_3().select_document_sender_v1(type_dashboard,username,email,limit,offset,'','','',tax_id,sort_key,group_status,pick_datetime=datetime_tmp,tmptimeapprove=timeapprove)
            if result_select['result'] == 'OK':
                if result_select['messageText']['document'] != []:
                    max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_last'])['update_last']
                    max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
                else:
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'sender_filter':
        if request.method == 'GET':
            username = request.args.get('username')
            email = request.args.get('email')
            secret_key = request.args.get('secret_key')
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            document_type = request.args.get('document_type')
            status = request.args.get('status')
            tax_id = request.args.get('tax_id')
            sort_key = request.args.get('sort_key')
            group_status = request.args.get('group_status')
            datetime_tmp = request.args.get('datetime')
            timeapprove = bool(request.args.get('timeapprove'))
            if email == None or username == None or secret_key == None or limit == None or offset == None or tax_id == None or status == None or document_type == None:
                abort(404)  
            if datetime_tmp == '':
                datetime_tmp = None 
            if timeapprove == '':
                timeapprove = None   
            email = str(email).lower()
            result_select = select_3().select_document_sender_v1(type_dashboard,username,email,limit,offset,document_type,'',status,tax_id,sort_key,group_status,pick_datetime=datetime_tmp,tmptimeapprove=timeapprove)
            if result_select['result'] == 'OK':
                if result_select['messageText']['document'] != []:
                    max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_last'])['update_last']
                    max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
                else:
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    elif type_dashboard == 'sender_search':
        if request.method == 'GET':
            email = request.args.get('email')
            username = request.args.get('username')
            secret_key = request.args.get('secret_key')
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            document_type = request.args.get('document_type')
            keyword = request.args.get('keyword')
            tax_id = request.args.get('tax_id')
            sort_key = request.args.get('sort_key')
            datetime_tmp = request.args.get('datetime')
            timeapprove = bool(request.args.get('timeapprove'))
            if email == None or secret_key == None or limit == None or offset == None or document_type == None or keyword == None or tax_id == None:
                abort(404)
            if datetime_tmp == '':
                datetime_tmp = None  
            if timeapprove == '':
                timeapprove = None  
            email = str(email).lower()
            result_select = select_3().select_document_sender_v1(type_dashboard,username,email,limit,offset,document_type,keyword,'',tax_id,sort_key,pick_datetime=datetime_tmp,tmptimeapprove=timeapprove)
            if result_select['result'] == 'OK':
                if result_select['messageText']['document'] != []:
                    max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_last'])['update_last']
                    max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
                else:
                    return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
                return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
            else:
                return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
    else:
        return jsonify({'status':'fail','message':'type incorrect (string - sender or recipient)','data':None,'code':200}),200


# @status_methods.route('/api/v1/document/<string:type_dashboard>', methods=['GET'])
# @token_required_v3
# def document_api_v1(type_dashboard):
#     if type_dashboard == 'recipient_external':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             limit = request.args.get('limit')
#             offset = request.args.get('offset')
#             sort_key = request.args.get('sort_key')
#             group_status = request.args.get('group_status')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or secret_key == None  or limit == None or offset == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             r_listtax_id = email_to_business(email)
#             result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,None,None,None,r_listtax_id,sort_key,group_status,datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'sum_recipient_external':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             document_type = request.args.get('document_type')
#             group_status = request.args.get('group_status')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or secret_key == None or document_type == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             r_listtax_id = email_to_business(email)
#             result_select = select_3().select_recp_count_v1(type_dashboard,email,document_type,r_listtax_id,'',group_status,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'recipient_external_search':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             limit = request.args.get('limit')
#             offset = request.args.get('offset')
#             document_type = request.args.get('document_type')
#             keyword = request.args.get('keyword')
#             sort_key = request.args.get('sort_key')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or secret_key == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             r_listtax_id = email_to_business(email)
#             result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,document_type,keyword,'',r_listtax_id,sort_key,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'filter_recipient_external':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             limit = request.args.get('limit')
#             offset = request.args.get('offset')
#             document_type = request.args.get('document_type')
#             status = request.args.get('status')
#             sort_key = request.args.get('sort_key')
#             group_status = request.args.get('group_status')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or secret_key == None or limit == None or offset == None or document_type == None or status == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             r_listtax_id = email_to_business(email)
#             result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,document_type,'',status,r_listtax_id,sort_key,group_status,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'sum_filter_recipient_external':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             document_type = request.args.get('document_type')
#             group_status = request.args.get('group_status')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or secret_key == None or document_type == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             r_listtax_id = email_to_business(email)
#             result_select = select_3().select_recp_count_v1(type_dashboard,email,document_type,r_listtax_id,'',group_status,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'sum_search_recipient_external':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             document_type = request.args.get('document_type')
#             keyword = request.args.get('keyword')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or secret_key == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             r_listtax_id = email_to_business(email)
#             result_select = select_3().select_recp_count_v1(type_dashboard,email,document_type,r_listtax_id,keyword,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'sum_filter':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             document_type = request.args.get('document_type')
#             tax_id = request.args.get('tax_id')
#             group_status = request.args.get('group_status')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or secret_key == None or document_type == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             result_select = select_3().select_recp_count_v1(type_dashboard,email,document_type,tax_id,'',group_status,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'sum':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             tax_id = request.args.get('tax_id')
#             group_status = request.args.get('group_status')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or secret_key == None or tax_id == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             result_select = select_3().select_recp_count_v1(type_dashboard,email,'',tax_id,'',group_status,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'sum_recipient_search':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             tax_id = request.args.get('tax_id')
#             document_type = request.args.get('document_type')
#             keyword = request.args.get('keyword')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or secret_key == None or tax_id == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             result_select = select_3().select_recp_count_v1(type_dashboard,email,document_type,tax_id,keyword,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'recipient':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             limit = request.args.get('limit')
#             offset = request.args.get('offset')
#             tax_id = request.args.get('tax_id')
#             sort_key = request.args.get('sort_key')
#             group_status = request.args.get('group_status')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or secret_key == None or limit == None or offset == None or tax_id == None :
#                 abort(404)    
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,None,None,None,tax_id,sort_key,group_status,datetime_tmp)
            
#             # print ('max_update_time:',max_update_time)
#             # print ('max_update_time_ts:',max_update_time_ts)
#             if result_select['result'] == 'OK':
#                 if result_select['messageText']['document'] != []:
#                     max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_time'])['update_time']
#                     max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
#                     return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
#                 else:
#                     return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'recipient_update':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             limit = request.args.get('limit')
#             offset = request.args.get('offset')
#             tax_id = request.args.get('tax_id')
#             sort_key = request.args.get('sort_key')
#             group_status = request.args.get('group_status')
#             datetime_tmp = request.args.get('datetime')
#             timestamp = request.args.get('timestamp')
#             if email == None or secret_key == None or limit == None or offset == None or tax_id == None or timestamp == None:
#                 abort(404)    
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,None,None,None,tax_id,sort_key,group_status,datetime_tmp,timestamp)
#             # max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_time'])['update_time']
#             # max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
#             if result_select['result'] == 'OK':
#                 if result_select['messageText']['document'] != []:
#                     max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_time'])['update_time']
#                     max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
#                     return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
#                 else:
#                     return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'recipient_search':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             limit = request.args.get('limit')
#             offset = request.args.get('offset')
#             document_type = request.args.get('document_type')
#             keyword = request.args.get('keyword')
#             tax_id = request.args.get('tax_id')
#             sort_key = request.args.get('sort_key')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or secret_key == None or limit == None or offset == None or document_type == None or keyword == None or tax_id == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,document_type,keyword,'',tax_id,sort_key,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'recipient_filter':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             limit = request.args.get('limit')
#             offset = request.args.get('offset')
#             document_type = request.args.get('document_type')
#             status = request.args.get('status')
#             tax_id = request.args.get('tax_id')
#             sort_key = request.args.get('sort_key')
#             group_status = request.args.get('group_status')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or secret_key == None or limit == None or offset == None or document_type == None or status == None or tax_id == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,document_type,'',status,tax_id,sort_key,group_status,datetime_tmp)
#             if result_select['result'] == 'OK':
#                 if result_select['messageText']['document'] != []:
#                     max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_time'])['update_time']
#                     max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
#                     return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
#                 else:
#                     return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'recipient_filter_update':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             limit = request.args.get('limit')
#             offset = request.args.get('offset')
#             document_type = request.args.get('document_type')
#             status = request.args.get('status')
#             tax_id = request.args.get('tax_id')
#             sort_key = request.args.get('sort_key')
#             group_status = request.args.get('group_status')
#             datetime_tmp = request.args.get('datetime')
#             timestamp = request.args.get('timestamp')
#             if email == None or secret_key == None or limit == None or offset == None or document_type == None or status == None or tax_id == None or timestamp == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             result_select = select_3().select_recp_new_v1(type_dashboard,email,limit,offset,document_type,'',status,tax_id,sort_key,group_status,datetime_tmp,timestamp)
#             if result_select['result'] == 'OK':
#                 if result_select['messageText']['document'] != []:
#                     max_update_time = max(result_select['messageText']['document'],key=lambda item:item['update_time'])['update_time']
#                     max_update_time_ts = int(datetime.datetime.timestamp(max_update_time))
#                     return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'timestamp':max_update_time_ts,'code':200}),200
#                 else:
#                     return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'sender_sum':
#         if request.method == 'GET':
#             username = request.args.get('username')
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             tax_id = request.args.get('tax_id')
#             group_status = request.args.get('group_status')
#             datetime_tmp = request.args.get('datetime')
#             if username == None or email == None or secret_key == None or tax_id == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             result_select = select_3().select_document_sender_count_v1(type_dashboard,username,email,'',tax_id,'',group_status,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'sender_sum_filter':
#         if request.method == 'GET':
#             username = request.args.get('username')
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             document_type = request.args.get('document_type')
#             tax_id = request.args.get('tax_id')
#             group_status = request.args.get('group_status')
#             datetime_tmp = request.args.get('datetime')
#             if username == None or email == None or secret_key == None or document_type == None or tax_id == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             result_select = select_3().select_document_sender_count_v1(type_dashboard,username,email,document_type,tax_id,'',group_status,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'sender_sum_search':
#         if request.method == 'GET':
#             username = request.args.get('username')
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             document_type = request.args.get('document_type')
#             tax_id = request.args.get('tax_id')
#             keyword = request.args.get('keyword')
#             datetime_tmp = request.args.get('datetime')
#             if username == None or email == None or secret_key == None or document_type == None or tax_id == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             result_select = select_3().select_document_sender_count_v1(type_dashboard,username,email,document_type,tax_id,keyword,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'sender':
#         if request.method == 'GET':
#             username = request.args.get('username')
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             limit = request.args.get('limit')
#             offset = request.args.get('offset')
#             tax_id = request.args.get('tax_id')
#             sort_key = request.args.get('sort_key')
#             group_status = request.args.get('group_status')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or username == None or secret_key == None or limit == None or offset == None or tax_id == None:
#                 abort(404)      
#             if datetime_tmp == '':
#                 datetime_tmp = None
#             email = str(email).lower()
#             result_select = select_3().select_document_sender_v1(type_dashboard,username,email,limit,offset,'','','',tax_id,sort_key,group_status,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'sender_filter':
#         if request.method == 'GET':
#             username = request.args.get('username')
#             email = request.args.get('email')
#             secret_key = request.args.get('secret_key')
#             limit = request.args.get('limit')
#             offset = request.args.get('offset')
#             document_type = request.args.get('document_type')
#             status = request.args.get('status')
#             tax_id = request.args.get('tax_id')
#             sort_key = request.args.get('sort_key')
#             group_status = request.args.get('group_status')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or username == None or secret_key == None or limit == None or offset == None or tax_id == None or status == None or document_type == None:
#                 abort(404)  
#             if datetime_tmp == '':
#                 datetime_tmp = None    
#             email = str(email).lower()
#             result_select = select_3().select_document_sender_v1(type_dashboard,username,email,limit,offset,document_type,'',status,tax_id,sort_key,group_status,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     elif type_dashboard == 'sender_search':
#         if request.method == 'GET':
#             email = request.args.get('email')
#             username = request.args.get('username')
#             secret_key = request.args.get('secret_key')
#             limit = request.args.get('limit')
#             offset = request.args.get('offset')
#             document_type = request.args.get('document_type')
#             keyword = request.args.get('keyword')
#             tax_id = request.args.get('tax_id')
#             sort_key = request.args.get('sort_key')
#             datetime_tmp = request.args.get('datetime')
#             if email == None or secret_key == None or limit == None or offset == None or document_type == None or keyword == None or tax_id == None:
#                 abort(404)
#             if datetime_tmp == '':
#                 datetime_tmp = None  
#             email = str(email).lower()
#             result_select = select_3().select_document_sender_v1(type_dashboard,username,email,limit,offset,document_type,keyword,'',tax_id,sort_key,pick_datetime=datetime_tmp)
#             if result_select['result'] == 'OK':
#                 return jsonify({'status':'success','message':'Get Data Success','data':result_select['messageText'],'code':200}),200
#             else:
#                 return jsonify({'status':'fail','message':'Get Data Fail','data':None,'code':200}),200
#     else:
#         return jsonify({'status':'fail','message':'type incorrect (string - sender or recipient)','data':None,'code':200}),200


@status_methods.route('/dashboard/v5/<string:type_dashboard>', methods=['POST'])
# @token_required
def dashboard_v5(type_dashboard):
    if type_dashboard == 'sender':
        if request.method == 'POST':
            dataJson = request.json
            if 'username' in dataJson and 'emailUser' in dataJson and 'secret_key' in dataJson:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    tmptimeapprove = None
                    if 'timeapprove' in dataJson:
                        tmptimeapprove = dataJson['timeapprove']
                    user_Name = str(dataJson['username']).lower()
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select().select_dashboard_sender_v4(user_Name,emailUser,tmptimeapprove)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    tmptimeapprove = None
                    if 'timeapprove' in dataJson:
                        tmptimeapprove = dataJson['timeapprove']
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select_1().select_dashboard_recipient_v6_list_update_time(emailUser,tmptimeapprove)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'timestamp':int(time.time()),'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                abort(404)
    elif type_dashboard == 'sum':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson:
                tmpgroupstatus = None
                if 'group_status' in dataJson:
                    tmpgroupstatus = dataJson['group_status']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select_1().select_dashboard_recipient_v5_sum(emailUser,tmpgroupstatus)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'sum_filter':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and 'document_type' in dataJson and len(dataJson) == 3:
                tmp_document_type = dataJson['document_type']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select_1().select_dashboard_recipient_v5_sum_filter(emailUser,tmp_document_type)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient_update':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and 'datetime_start' in dataJson and 'datetime_end' in dataJson:
                datetime_start =  dataJson['datetime_start']
                datetime_end = dataJson['datetime_end']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    tmptimeapprove = None
                    if 'timeapprove' in dataJson:
                        tmptimeapprove = dataJson['timeapprove']
                    if 'timestamp' in dataJson:
                        timestamp = dataJson['timestamp']
                        if timestamp == '':
                            timestamp = None
                    emailUser = str(dataJson['emailUser']).lower()
                    # result_select = select_1().select_dashboard_recipient_v6_list(emailUser,datetime_start,datetime_end,tmptimeapprove,timestamp)
                    result_select = select_1().select_dashboard_recipient_updateV2(emailUser,datetime_start,datetime_end,tmptimeapprove,timestamp)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'timestamp':int(time.time()),'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient_new':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and 'limit' in dataJson and 'offset' in dataJson:
                tmp_limit =  dataJson['limit']
                tmp_offset = dataJson['offset']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    tmpgroup = None
                    tmptimeapprove = None
                    if 'group_status' in dataJson:
                        tmpgroup = dataJson['group_status']
                    if 'timeapprove' in dataJson:
                        tmptimeapprove = dataJson['timeapprove']
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select_1().select_dashboard_recipient_v6_new_limitoffset(emailUser,tmp_limit,tmp_offset,tmpgroup,tmptimeapprove)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'timestamp':result_select['timestamp'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                abort(404)
    elif type_dashboard == 'recipient_search':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and 'limit' in dataJson and 'offset' in dataJson and 'document_type' in dataJson and 'keyword' in dataJson:
                tmp_document_type =  dataJson['document_type']
                tmp_keyword = dataJson['keyword']
                tmp_limit =  dataJson['limit']
                tmp_offset = dataJson['offset']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    tmptimeapprove = None
                    if 'timeapprove' in dataJson:
                        tmptimeapprove = dataJson['timeapprove']
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select_1().select_dashboard_recipient_v6_new_limitoffset_search(emailUser,tmp_limit,tmp_offset,tmp_document_type,tmp_keyword,tmptimeapprove)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'timestamp':int(time.time()),'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient_filter':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and 'limit' in dataJson and 'offset' in dataJson and 'document_type' in dataJson and 'status' in dataJson:
                tmp_document_type =  dataJson['document_type']
                tmp_status = dataJson['status']
                tmp_limit =  dataJson['limit']
                tmp_offset = dataJson['offset']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    tmpgroup = None
                    tmptimeapprove = None
                    if 'group_status' in dataJson:
                        tmpgroup = dataJson['group_status']
                    if 'timeapprove' in dataJson:
                        tmptimeapprove = dataJson['timeapprove']
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select_1().select_dashboard_recipient_v6_new_limitoffset_filter(emailUser,tmp_limit,tmp_offset,tmp_status,tmp_document_type,tmpgroup,tmptimeapprove)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'timestamp':int(time.time()),'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'type incorrect (string - sender or recipient)'}),200

@status_methods.route('/api/v1/dashboard/recipient/<string:type_dashboard>', methods=['POST'])
def recipient_dashboard_api_v1(type_dashboard):
    if 'Authorization' in request.headers:
        token_header = request.headers['Authorization']
        try:                
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            abort(401)
    else:
        return redirect(url_paperless)
    result_data = token_required_func(token_header)
    if result_data['result'] != 'OK':
        abort(401)
    tmp_email = result_data['email']
    if type_dashboard == 'sum':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and len(dataJson) == 2:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    if tmp_email not in email_admin:
                        if emailUser != tmp_email:
                            abort(401)
                    result_select = select_1().select_dashboard_recipient_v5_sum(emailUser)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'sum_filter':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and 'document_type' in dataJson and len(dataJson) == 3:
                tmp_document_type = dataJson['document_type']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    if tmp_email not in email_admin:
                        if emailUser != tmp_email:
                            abort(401)
                    result_select = select_1().select_dashboard_recipient_v5_sum_filter(emailUser,tmp_document_type)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient_update':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and 'datetime_start' in dataJson and 'datetime_end' in dataJson and len(dataJson) == 4:
                datetime_start =  dataJson['datetime_start']
                datetime_end = dataJson['datetime_end']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    if tmp_email not in email_admin:
                        if emailUser != tmp_email:
                            abort(401)
                    result_select = select_1().select_dashboard_recipient_v6_list(emailUser,datetime_start,datetime_end)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'timestamp':int(time.time()),'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient_new':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and 'limit' in dataJson and 'offset' in dataJson and len(dataJson) == 4:
                tmp_limit =  dataJson['limit']
                tmp_offset = dataJson['offset']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    if tmp_email not in email_admin:
                        if emailUser != tmp_email:
                            abort(401)
                    result_select = select_1().select_dashboard_recipient_v5_new_limitoffset(emailUser,tmp_limit,tmp_offset)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'timestamp':int(time.time()),'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient_search':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and 'limit' in dataJson and 'offset' in dataJson and 'document_type' in dataJson and 'keyword' in dataJson and len(dataJson) == 6:
                tmp_document_type =  dataJson['document_type']
                tmp_keyword = dataJson['keyword']
                tmp_limit =  dataJson['limit']
                tmp_offset = dataJson['offset']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    if tmp_email not in email_admin:
                        if emailUser != tmp_email:
                            abort(401)
                    result_select = select_1().select_dashboard_recipient_v5_new_limitoffset_search(emailUser,tmp_limit,tmp_offset,tmp_document_type,tmp_keyword)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'timestamp':int(time.time()),'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient_filter':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and 'limit' in dataJson and 'offset' in dataJson and 'document_type' in dataJson and 'status' in dataJson and len(dataJson) == 6:
                tmp_document_type =  dataJson['document_type']
                tmp_status = dataJson['status']
                tmp_limit =  dataJson['limit']
                tmp_offset = dataJson['offset']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    if tmp_email not in email_admin:
                        if emailUser != tmp_email:
                            abort(401)
                    result_select = select_1().select_dashboard_recipient_v5_new_limitoffset_filter(emailUser,tmp_limit,tmp_offset,tmp_status,tmp_document_type)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'timestamp':int(time.time()),'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    else:
        abort(404)

@status_methods.route('/api/v1/dashboard/sender/<string:type_dashboard>', methods=['POST'])
def sender_dashboard_api_v1(type_dashboard):
    if 'Authorization' in request.headers:
        token_header = request.headers['Authorization']
        try:                
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            abort(401)
    else:
        return redirect(url_paperless)
    result_data = token_required_func(token_header)
    if result_data['result'] != 'OK':
        abort(401)
    tmp_email = result_data['email']
    tmp_username = result_data['username']
    if type_dashboard == 'sum':
        if request.method == 'POST':
            dataJson = request.json
            if 'username' in dataJson and 'emailUser' in dataJson and 'secret_key' in dataJson and len(dataJson) == 3:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    user_Name = str(dataJson['username']).lower()
                    emailUser = str(dataJson['emailUser']).lower()
                    if tmp_email not in email_admin:
                        if emailUser != tmp_email and user_Name != tmp_username:
                            abort(401)
                    result_select = select_1().select_dashboard_sender_v3_sum(user_Name,emailUser)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                abort(404)
    elif type_dashboard == 'sum_filter':
        if request.method == 'POST':
            dataJson = request.json
            if 'username' in dataJson and 'emailUser' in dataJson and 'secret_key' in dataJson and 'document_type' in dataJson and len(dataJson) == 4:
                tmp_document_type = dataJson['document_type']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    user_Name = str(dataJson['username']).lower()
                    emailUser = str(dataJson['emailUser']).lower()
                    if tmp_email not in email_admin:
                        if emailUser != tmp_email and user_Name != tmp_username:
                            abort(401)
                    result_select = select_1().select_dashboard_sender_v3_sum_filter(user_Name,emailUser,tmp_document_type)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                abort(404)
    elif type_dashboard == 'sender_new':
        if request.method == 'POST':
            dataJson = request.json
            if 'username' in dataJson and 'emailUser' in dataJson and 'secret_key' in dataJson and 'limit' in dataJson and 'offset' in dataJson:
                tmp_limit =  dataJson['limit']
                tmp_offset = dataJson['offset']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    user_Name = str(dataJson['username']).lower()
                    emailUser = str(dataJson['emailUser']).lower()
                    tmpgroup = None
                    if 'group_status' in dataJson:
                        tmpgroup = dataJson['group_status']
                    if tmp_email not in email_admin:
                        if emailUser != tmp_email and user_Name != tmp_username:
                            abort(401)
                    result_select = select_1().select_dashboard_sender_v3_new_limitoffset(user_Name,emailUser,tmp_limit,tmp_offset,tmpgroup)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'timestamp':int(time.time()),'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                abort(404)
    elif type_dashboard == 'sender_search':
        if request.method == 'POST':
            dataJson = request.json
            if 'username' in dataJson and 'emailUser' in dataJson and 'secret_key' in dataJson and 'limit' in dataJson and 'offset' in dataJson and 'document_type' in dataJson and 'keyword' in dataJson and len(dataJson) == 7:
                tmp_document_type =  dataJson['document_type']
                tmp_keyword = dataJson['keyword']
                tmp_limit =  dataJson['limit']
                tmp_offset = dataJson['offset']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    user_Name = str(dataJson['username']).lower()
                    emailUser = str(dataJson['emailUser']).lower()
                    if tmp_email not in email_admin:
                        if emailUser != tmp_email and user_Name != tmp_username:
                            abort(401)
                    result_select = select_1().select_dashboard_sender_v3_new_limitoffset_search(user_Name,emailUser,tmp_limit,tmp_offset,tmp_document_type,tmp_keyword)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'timestamp':int(time.time()),'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                abort(404)
    elif type_dashboard == 'sender_filter':
        if request.method == 'POST':
            dataJson = request.json
            if 'username' in dataJson and 'emailUser' in dataJson and 'secret_key' in dataJson and 'limit' in dataJson and 'offset' in dataJson and 'document_type' in dataJson and 'status' in dataJson:
                tmp_document_type =  dataJson['document_type']
                tmp_status = dataJson['status']
                tmp_limit =  dataJson['limit']
                tmp_offset = dataJson['offset']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    user_Name = str(dataJson['username']).lower()
                    emailUser = str(dataJson['emailUser']).lower()
                    tmpgroup = None
                    if 'group_status' in dataJson:
                        tmpgroup = dataJson['group_status']
                    if tmp_email not in email_admin:
                        if emailUser != tmp_email and user_Name != tmp_username:
                            abort(401)
                    result_select = select_1().select_dashboard_sender_v3_new_limitoffset_filter(user_Name,emailUser,tmp_limit,tmp_offset,tmp_status,tmp_document_type,tmpgroup)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'timestamp':int(time.time()),'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                abort(404)
    else:
        abort(404)

@status_methods.route('/dashboard/v5/thread/<string:type_dashboard>', methods=['POST'])
# @token_required
def dashboard_v5_api_thread(type_dashboard):
    if type_dashboard == 'sender':
        if request.method == 'POST':
            dataJson = request.json
            if 'username' in dataJson and 'emailUser' in dataJson and 'secret_key' in dataJson and len(dataJson) == 3:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    user_Name = str(dataJson['username']).lower()
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select().select_dashboard_sender_v3(user_Name,emailUser)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and len(dataJson) == 2:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select_1().select_dashboard_recipient_v5_list_thread(emailUser)
                    if result_select['result'] == 'OK':
                        # data_as_str = json.dumps(result_select['messageText'])
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'sum':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and len(dataJson) == 2:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select_1().select_dashboard_recipient_v5_sum(emailUser)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient_update':
        if request.method == 'POST':
            if 'emailUser' in dataJson and 'secret_key' in dataJson and 'datetime_start' in dataJson and 'datetime_end' in dataJson and len(dataJson) == 4:
                datetime_start =  dataJson['datetime_start']
                datetime_end = dataJson['datetime_end']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select_1().select_dashboard_recipient_v6_list(emailUser,datetime_start,datetime_end)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'type incorrect (string - sender or recipient)'}),200

@status_methods.route('/dashboard/v6/<string:type_dashboard>', methods=['POST'])
# @token_required
def dashboard_v6(type_dashboard):
    if type_dashboard == 'sender':
        if request.method == 'POST':
            dataJson = request.json
            if 'username' in dataJson and 'emailUser' in dataJson and 'secret_key' in dataJson and len(dataJson) == 3:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    user_Name = str(dataJson['username']).lower()
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select().select_dashboard_sender_v3(user_Name,emailUser)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and 'datetime_start' in dataJson and 'datetime_end' in dataJson and len(dataJson) == 4:
                datetime_start =  dataJson['datetime_start']
                datetime_end = dataJson['datetime_end']
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select_1().select_dashboard_recipient_v6_list(emailUser,datetime_start,datetime_end)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'type incorrect (string - sender or recipient)'}),200


@status_methods.route('/dashboard/v4/<string:type_dashboard>', methods=['POST'])
@token_required
def dashboard_v4(type_dashboard):
    if type_dashboard == 'sender':
        if request.method == 'POST':
            dataJson = request.json
            if 'username' in dataJson and 'emailUser' in dataJson and 'secret_key' in dataJson and len(dataJson) == 3:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    user_Name = str(dataJson['username']).lower()
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select().select_dashboard_sender_v4(user_Name,emailUser)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and len(dataJson) == 2:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    result_select = select().select_dashboard_recipient_v3_v2(emailUser)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'type incorrect (string - sender or recipient)'}),200

@status_methods.route('/api/sender/dashboard/v1', methods=['GET'])
@token_required_v2
def dashboard_sender_api_v1(username,email_thai,token_header):
    if (request.args.get('senderuser')) != None and not (request.args.get('textsid')):
        select_getsender = select().select_get_sender_OneChain(str(request.args.get('senderuser')).replace(' ','').lower())
        if select_getsender['result'] == 'OK':
            return jsonify(select_getsender),200
        else:
            return jsonify({'result':'ER','messageText':select_getsender['messageText'],'status_Code':200}),200
    elif (request.args.get('senderuser')) != None and (request.args.get('textsid')) != None:
        select_getsender = select_1().select_sender_db_v3(str(request.args.get('senderuser')).replace(' ','').lower(),str(request.args.get('textsid')).replace(' ',''),email_thai)
        if select_getsender['result'] == 'OK':
            return jsonify(select_getsender),200
        else:
            return jsonify({'result':'ER','messageText':select_getsender['messageText'],'status_Code':200}),200
    else:
        return jsonify({'result':'ER','messageText':'parameter incorrect','status_Code':404}),404

@status_methods.route('/api/recipient/dashboard/v1', methods=['GET'])
@token_required
def dashboard_recipient_api_v1():
    if (request.args.get('email')) != None and not request.args.get('sid'):
        emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", request.args.get('email'))
        if emails is None:
            return jsonify({'result':'ER','messageText':'ข้อมูล email ไม่ตรงตามรูปแบบ','status_Code':200}),200
        else:
            pass
        res_select_recipient = select().select_get_recipient_OneChain(str(request.args.get('email')).replace(' ','').lower())
        if res_select_recipient['result'] == 'OK':
            return jsonify(res_select_recipient),200
        else:
            return jsonify({'result':'ER','messageText':res_select_recipient['messageText'],'status_Code':200}),200
    elif (request.args.get('email')) != None and (request.args.get('sid')) != None:
        emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", request.args.get('email'))
        if emails is None:
            return jsonify({'result':'ER','messageText':'ข้อมูล email ไม่ตรงตามรูปแบบ','status_Code':200}),200
        else:
            pass
        res_select_recipient_sid = select().select_recpin_db_v3(str(request.args.get('email')).replace(' ','').lower(),str(request.args.get('sid')).replace(' ',''))
        if res_select_recipient_sid['result'] == 'OK':
            return jsonify(res_select_recipient_sid),200
        else:
            return jsonify({'result':'ER','messageText':res_select_recipient_sid['messageText'],'messageER':res_select_recipient_sid['messageER'],'status_Code':200}),200
    else:
        return jsonify({'result':'ER','messageText':'parameter incorrect','status_Code':404}),404


@status_methods.route('/api/v2/sender/dashboard', methods=['GET'])
@token_required_v2
def dashboard_sender_apiv2(username,email_thai,token_header):
    if request.method == 'GET':
        if (request.args.get('senderuser')) != None and not (request.args.get('textsid')):
            select_getsender = select().select_get_sender_OneChain(str(request.args.get('senderuser')).replace(' ','').lower())
            if select_getsender['result'] == 'OK':
                return jsonify(select_getsender),200
            else:
                return jsonify({'result':'ER','messageText':select_getsender['messageText'],'status_Code':200}),200
        elif (request.args.get('senderuser')) != None and (request.args.get('textsid')) != None:
            select_getsender = select().select_sender_one_v3_last(str(request.args.get('senderuser')).replace(' ','').lower(),str(request.args.get('textsid')).replace(' ',''),email_thai)
            if select_getsender['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'data':select_getsender['messageText'],'message':'success'},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':[],'message':'fail ' + select_getsender['messageText']}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'data':None,'message':'parameter incorrect','code':'ERDO999'}}),404

@status_methods.route('/api/v2/recipient/dashboard', methods=['GET'])
@token_required_v3
def dashboard_recipient_apiv2():
    if request.method == 'GET':
        if (request.args.get('email')) != None and not request.args.get('sid'):
            emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", request.args.get('email'))
            if emails is None:
                return jsonify({'result':'ER','messageText':'ข้อมูล email ไม่ตรงตามรูปแบบ','status_Code':200}),200
            else:
                pass
            res_select_recipient = select().select_get_recipient_OneChain(str(request.args.get('email')).replace(' ','').lower())
            if res_select_recipient['result'] == 'OK':
                return jsonify(res_select_recipient),200
            else:
                return jsonify({'result':'ER','messageText':res_select_recipient['messageText'],'status_Code':200}),200
        elif (request.args.get('email')) != None and (request.args.get('sid')) != None:
            emails = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", request.args.get('email'))
            if emails is None:
                return jsonify({'result':'ER','messageText':'ข้อมูล email ไม่ตรงตามรูปแบบ','status_Code':200}),200
            else:
                pass
            res_select_recipient_sid = select_1().select_recipient_one_v3_last(str(request.args.get('email')).replace(' ','').lower(),str(request.args.get('sid')).replace(' ',''))
            if res_select_recipient_sid['result'] == 'OK':
                return jsonify(res_select_recipient_sid),200
            else:
                return jsonify({'result':'ER','messageText':res_select_recipient_sid['messageText'],'messageER':res_select_recipient_sid['messageER'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/dashboard/v3/day/<string:type_dashboard>', methods=['POST'])
@token_required
def dashboard_v3_every_month(type_dashboard):
    if type_dashboard == 'sender':
        if request.method == 'POST':
            dataJson = request.json
            if 'username' in dataJson and 'emailUser' in dataJson and 'secret_key' in dataJson and 'day' in dataJson and len(dataJson) == 4:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    user_Name = str(dataJson['username']).lower()
                    emailUser = str(dataJson['emailUser']).lower()
                    tmp_day = (dataJson['day'])
                    result_select = select().select_dashboard_sender_v5(user_Name,emailUser,tmp_day)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    elif type_dashboard == 'recipient':
        if request.method == 'POST':
            dataJson = request.json
            if 'emailUser' in dataJson and 'secret_key' in dataJson and 'day' in dataJson and len(dataJson) == 3:
                if dataJson['secret_key'] == '4DnsTP8Nz2':
                    emailUser = str(dataJson['emailUser']).lower()
                    tmp_day = (dataJson['day'])
                    result_select = select().select_dashboard_recipient_v5(emailUser,tmp_day)
                    if result_select['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'type incorrect (string - sender or recipient)'}),200

@status_methods.route('/dashboard/v1/document/collect',methods=['POST'])
@token_required
def document_collect_api_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'email_one' in dataJson:
            tmp_emailone = dataJson['email_one']
            result_select = select().select_email_collect_v1(tmp_emailone)
            if result_select['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_select['messageText'],'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':result_select['messageER'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'data':None,'message':'parameter incorrect','code':'ERDO999'}}),404
        # pass

@status_methods.route('/dashboard/v1/viewpaper', methods=['POST'])
@token_required_v3
def viewpaper_count():
    if request.method == 'POST':
        dataJson = request.json
        if 'email' in dataJson:
            email = dataJson['email']
            list_result = []
            tmp_json = {}
            with concurrent.futures.ThreadPoolExecutor() as executor:
                week_sender = executor.submit(select().select_countpaperWeek_senderemail,email)
                week_recp = executor.submit(select().select_countpaperWeek_recpemail,email)
                day_sender = executor.submit(select().selct_count_paperDay_senderemail,email)
                day_recp = executor.submit(select().selct_count_paperDay_recpemail,email)
                hour_sender = executor.submit(select().selct_count_paperHour_sendermail,email)
                hour_recp = executor.submit(select().selct_count_paperHour_recpmail,email)
                return_weekSender = week_sender.result()
                return_weekRecp = week_recp.result()
                return_daySender = day_sender.result()
                return_dayRecp = day_recp.result()
                return_hourSender = hour_sender.result()
                return_hourRecp = hour_recp.result()
            list_result = []
            tmp_2 = {}
            tmp_2['message'] = return_weekSender['messageText']
            tmp_2['status'] = return_weekSender['result']
            tmp_json['sender_week'] = tmp_2
            tmp_2 = {}

            tmp_2 = {}
            tmp_2['message'] = return_weekRecp['messageText']
            tmp_2['status'] = return_weekRecp['result']
            tmp_json['recp_week'] = tmp_2
            tmp_2 = {}

            tmp_2 = {}
            tmp_2['message'] = return_daySender['messageText']
            tmp_2['status'] = return_daySender['result']
            tmp_json['sender_day'] = tmp_2
            tmp_2 = {}

            tmp_2 = {}
            tmp_2['message'] = return_dayRecp['messageText']
            tmp_2['status'] = return_dayRecp['result']
            tmp_json['recp_day'] = tmp_2
            tmp_2 = {}

            tmp_2 = {}
            tmp_2['message'] = return_hourSender['messageText']
            tmp_2['status'] = return_hourSender['result']
            tmp_json['sender_hour'] = tmp_2
            tmp_2 = {}

            tmp_2 = {}
            tmp_2['message'] = return_hourRecp['messageText']
            tmp_2['status'] = return_hourRecp['result']
            tmp_json['recp_hour'] = tmp_2
            tmp_2 = {}
            list_result.append(tmp_json)
            if return_weekSender['result'] == 'OK' and  return_weekRecp['result'] == 'OK' and return_daySender['result'] == 'OK' and return_dayRecp['result'] == 'OK' and return_hourSender['result'] == 'OK' and return_hourRecp['result'] == 'OK':
                return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':None}),200
            else :
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':list_result}),200

        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

@status_methods.route('/dashboard/v2/viewpaper', methods=['POST'])
@token_required
def viewpaper_count_v2():
    if request.method == 'POST':
        dataJson = request.json
        if 'email' in dataJson and 'document_type' in dataJson and 'tax_id' in dataJson:
            email = dataJson['email']
            document_type = dataJson['document_type']
            tax_id = dataJson['tax_id']
            list_result = []
            tmp_json = {}
            with concurrent.futures.ThreadPoolExecutor() as executor:
                week_sender = executor.submit(select().select_countpaperWeek_senderemail_v2,email,document_type,tax_id)
                week_recp = executor.submit(select().select_countpaperWeek_recpemail_v2,email,document_type,tax_id)
                day_sender = executor.submit(select().selct_count_paperDay_senderemail_v2,email,document_type,tax_id)
                day_recp = executor.submit(select().selct_count_paperDay_recpemail_v2,email,document_type,tax_id)
                hour_sender = executor.submit(select().selct_count_paperHour_sendermail_v2,email,document_type,tax_id)
                hour_recp = executor.submit(select().selct_count_paperHour_recpmail_v2,email,document_type,tax_id)
                all_recp = executor.submit(select().select_count_paper_all_recp,email,document_type,tax_id)
                all_sender = executor.submit(select().select_count_paper_all_sender,email,document_type,tax_id)
                return_weekSender = week_sender.result()
                return_weekRecp = week_recp.result()
                return_daySender = day_sender.result()
                return_dayRecp = day_recp.result()
                return_hourSender = hour_sender.result()
                return_hourRecp = hour_recp.result()
                return_all_recp = all_recp.result()
                return_all_sender = all_sender.result()
            list_result = []
            tmp_2 = {}
            tmp_2['message'] = return_weekSender['messageText']
            tmp_2['status'] = return_weekSender['result']
            tmp_json['sender_week'] = tmp_2
            tmp_2 = {}

            tmp_2 = {}
            tmp_2['message'] = return_weekRecp['messageText']
            tmp_2['status'] = return_weekRecp['result']
            tmp_json['recp_week'] = tmp_2
            tmp_2 = {}

            tmp_2 = {}
            tmp_2['message'] = return_daySender['messageText']
            tmp_2['status'] = return_daySender['result']
            tmp_json['sender_day'] = tmp_2
            tmp_2 = {}

            tmp_2 = {}
            tmp_2['message'] = return_dayRecp['messageText']
            tmp_2['status'] = return_dayRecp['result']
            tmp_json['recp_day'] = tmp_2
            tmp_2 = {}

            tmp_2 = {}
            tmp_2['message'] = return_hourSender['messageText']
            tmp_2['status'] = return_hourSender['result']
            tmp_json['sender_hour'] = tmp_2
            tmp_2 = {}

            tmp_2 = {}
            tmp_2['message'] = return_hourRecp['messageText']
            tmp_2['status'] = return_hourRecp['result']
            tmp_json['recp_hour'] = tmp_2
            tmp_2 = {}

            tmp_2 = {}
            tmp_2['message'] = return_all_recp['messageText']
            tmp_2['status'] = return_all_recp['result']
            tmp_json['recp_all'] = tmp_2
            tmp_2 = {}

            tmp_2 = {}
            tmp_2['message'] = return_all_sender['messageText']
            tmp_2['status'] = return_all_sender['result']
            tmp_json['sender_all'] = tmp_2
            tmp_2 = {}
            
            list_result.append(tmp_json)
            if return_weekSender['result'] == 'OK' and  return_weekRecp['result'] == 'OK' and return_daySender['result'] == 'OK' and return_dayRecp['result'] == 'OK' and return_hourSender['result'] == 'OK' and return_hourRecp['result'] == 'OK':
                return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':None}),200
            else :
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':list_result}),200

        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

@status_methods.route('/api/v1/reference_doc', methods=['GET'])
@token_required_v3
def dashboard_reference_doc():
    if request.method == 'GET':
        if (request.args.get('sid')) != None:
            res_select_reference_doc_sid = select_1().select_reference_doc(str(request.args.get('sid')).replace(' ',''))
            if res_select_reference_doc_sid['result'] == 'OK':
                return jsonify(res_select_reference_doc_sid),200
            else:
                return jsonify({'result':'ER','messageText':res_select_reference_doc_sid['messageText'],'messageER':res_select_reference_doc_sid['messageER'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
