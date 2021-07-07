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
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *
from method.sftp_fucn import *
from method.callwebHook import *
import urllib.request
import certifi
import ssl
from db.db_Class import *

@status_methods.route('/api/v1/qr_code',methods=['POST'])
def qr_code():
    dataJson = request.json
    try:
        if 'email_user' in dataJson and 'password' in dataJson:
            len_user = len(dataJson['email_user'])
            for i in range(len_user):
                email_user = dataJson['email_user'][i]['user']
                pass_word = dataJson['password'][i]['pass']
                token_qr = hash_512_v2(str(uuid.uuid4()))
                pwd_id = str(uuid.uuid4())
                data_pwd = {
                    'pwdss':token_qr+pass_word+token_qr
                }
                hash_pwd = encode_p(data_pwd)
                url_qrcode = myUrl_domain + 'view_qr_code?code=' + token_qr
                data_url = {
                    'email_user':email_user,
                    'pwd':pwd_id
                }
                value = encode_url(data_url)
                value_spilt = value.split('.')
                hash_value = value_spilt[0]+'.'+value_spilt[1]
                token_url = value_spilt[2]
                result_qrcode = save_qrcode(email_user,token_url)
                if result_qrcode['result'] == 'OK':
                    path_qrcode = result_qrcode['messageText']
                    url_login_qrcode = result_qrcode['url']
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':'qrcode error','status_Code':200}),200
                if result_qrcode['result'] == 'OK':
                    result_insert = insert_qr().insert_user_qrcode(email_user,url_qrcode,path_qrcode,token_url,token_qr,hash_value,url_login_qrcode)
                    result_pwd = insert_qr().insert_pwd(pwd_id,hash_pwd)
                    if result_insert['result'] == 'OK' and result_pwd['result'] == 'OK':
                        continue
                    else:
                        return jsonify({'result':'ER','messageText':None,'messageER':result_insert['messageER'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':'incorrect','status_Code':200}),200
            return jsonify({'result':'OK','messageText':'sucess','messageER':None,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':'parameter incorrect','status_Code':200}),200
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageER': str(err)}

@status_methods.route('/api/v1/login_paperless_qrcode',methods=['POST'])
def login_paperless_qrcode():
    if request.method == 'POST':
        data = request.json
        if 'value' in data and len(data) == 1:
            token_url = data['value']
            result_data = select_qr().select_email_user_v3(token_url)
            if result_data['result'] == 'OK':
                data_value = result_data['data']
                username = data_value['email_user']
                pwd_id   = data_value['pwd']
                result_id = select_qr().select_pwd(pwd_id)
                if result_id['result'] == 'OK':
                    data_hash = result_id['data']
                    pwd = data_hash['pwdss']
                    pwd_1 = pwd[:-128]
                    password = pwd_1[128:]
            # username = data['username']
            # password = data['password']
            ipaddress = ''
            biz_info = []
            check_biz_id = []
            tmp_json = {
                "grant_type":  "password",
                "username":     username,
                "password":     password,
                "client_id":    clientId,
                "client_secret":secretKey
            }
            response = callPost_v2(one_url+"/api/oauth/getpwd",tmp_json)
            
            if response['result'] == 'OK':
                tmp_messageText = response['messageText'].json()
                if tmp_messageText['result'] == 'Success':
                    try:
                        username = tmp_messageText['username']
                        user_id = tmp_messageText['account_id']
                    except Exception as ex:
                        abort(401)
                    token_one = tmp_messageText['token_type'] + ' '+ tmp_messageText['access_token']
                    access_token_one = tmp_messageText['access_token']
                    result_selectdb = select_3().select_citizen_login_v1(username)
                    getBuz = callGET_v2(one_url+"/api/account_and_biz_detail",token_one)
                    ts = time.time()
                    try:
                        info = {
                            'accesstoken':access_token_one
                        }
                        executor.submit(login_OneChat,user_id,access_token_one)
                        executor.submit(get_account_byuserid,info,access_token_one)
                    except Exception as e:
                        print(str(e))
                    print(result_selectdb)
                    if result_selectdb['result'] == 'OK':
                        if getBuz['result'] == 'OK':
                            tmp_account_biz = getBuz['messageText'].json()
                            ts = time.time()
                            user_id         = tmp_account_biz['id']
                            user_email      = tmp_account_biz['thai_email']
                            user_type       = tmp_account_biz['account_category']
                            one_accesstoken = str(tmp_messageText['access_token'])
                            access_time     = ts
                            refresh_token   = tmp_messageText['refresh_token']
                            access_token_time   = ts + tmp_messageText['expires_in']
                            access_token_begin  = ts
                            hash_data       = hash_512_v2(password)
                            citizen_data    = str(tmp_account_biz)
                            getBiz_details  =  tmp_account_biz['biz_detail']
                            generate_seCode =   'P7Rw2h5GUVE2LpbVNRBO'
                            result_refToken = generate_tokenPaperless(username,user_email)
                            executor.submit(update_datalogin,user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress,getBiz_details)
                            try:
                                citizen_data = eval(citizen_data)
                            except Exception as ex:
                                abort(401)
                            return jsonify({'result':'OK','username':username,'one_access_token':one_accesstoken,'paperless_access_token':result_refToken,'one_result_data':citizen_data})
                        else:                       
                            abort(401)
                    else:
                        if getBuz['result'] == 'OK':
                            tmp_account_biz = getBuz['messageText'].json()
                            ts = time.time()
                            user_id         = tmp_account_biz['id']
                            user_email      = tmp_account_biz['thai_email']
                            user_type       = tmp_account_biz['account_category']
                            one_accesstoken = str(tmp_messageText['access_token'])
                            access_time     = ts
                            refresh_token   = tmp_messageText['refresh_token']
                            access_token_time   = ts + tmp_messageText['expires_in']
                            access_token_begin  = ts
                            hash_data       = hash_512_v2(password)
                            citizen_data    = str(tmp_account_biz)
                            getBiz_details  =  tmp_account_biz['biz_detail']
                            generate_seCode = 'P7Rw2h5GUVE2LpbVNRBO'
                            result_refToken = generate_tokenPaperless(username,user_email)
                            result_insert = insert().insert_login(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress)
                            result_BizLoing = insert().insert_LogBizLogin(username,user_id,getBiz_details)
                        else:
                            abort(401)
                try:
                    citizen_data = eval(citizen_data)
                except Exception as ex:
                    abort(401)
                    
                return jsonify({'result':'OK','username':username,'one_access_token':one_accesstoken,'paperless_access_token':result_refToken,'one_result_data':citizen_data})
            else:
                abort(401)
        else:
            abort(404)

@status_methods.route('/api/v2/qr_code',methods=['POST'])
def qr_code_v2():
    dataJson = request.json
    try:
        if 'email_user' in dataJson and 'password' in dataJson:
            len_user = len(dataJson['email_user'])
            for i in range(len_user):
                email_user = dataJson['email_user'][i]['user']
                pass_word = dataJson['password'][i]['pass']
                token_qr = hash_512_v2(str(uuid.uuid4()))
                pwd_id = str(uuid.uuid4())
                data_pwd = {
                    'pwdss':token_qr+pass_word+token_qr
                }
                hash_pwd = encode_p(data_pwd)
                url_qrcode = myUrl_domain + 'view_qr_code?code=' + token_qr
                data_url = {
                    'email_user':email_user,
                    'pwd':pwd_id
                }
                token_url_filter = (''.join(random_generator_secret()))
                value = encode_url(data_url)
                value_spilt = value.split('.')
                hash_value = value_spilt[0]+'.'+value_spilt[1]
                token_url = value_spilt[2]
                result_qrcode = save_qrcode(email_user,token_url_filter)
                if result_qrcode['result'] == 'OK':
                    path_qrcode = result_qrcode['messageText']
                    url_login_qrcode = result_qrcode['url']
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':'qrcode error','status_Code':200}),200
                if result_qrcode['result'] == 'OK':
                    result_insert = insert_qr().insert_user_qrcode(email_user,url_qrcode,path_qrcode,token_url,token_qr,hash_value,url_login_qrcode,token_url_filter)
                    if result_insert['result'] == 'ER':
                        # return jsonify({'result':'ER','messageText':None,'messageER':result_insert['messageER'],'status_Code':200}),200
                        continue
                    else:
                        result_pwd = insert_qr().insert_pwd(pwd_id,hash_pwd)
                    if result_insert['result'] == 'OK' and result_pwd['result'] == 'OK':
                        continue
                    else:
                        return jsonify({'result':'ER','messageText':None,'messageER':result_insert['messageER'],'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':'incorrect','status_Code':200}),200
            return jsonify({'result':'OK','messageText':'success','messageER':None,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':'parameter incorrect','status_Code':200}),200
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageER': str(err)}

@status_methods.route('/view_qr_code', methods=['GET'])
def view_qr_code():
    try:
        if (request.args.get('code')) != None:
            token = str(request.args.get('code')).replace(' ','')
            result_select = paperless_user_qrcode.query.filter(paperless_user_qrcode.token_qr == token).first()
            if result_select != None:
                path_image = eval(result_select.path_qrcode)
                qr_code_path = path_image['path_img'] + path_image['img_name']
                with open(qr_code_path, "rb") as qr_code:
                    encoded_string = base64.b64encode(qr_code.read())
                return send_file(io.BytesIO(base64.b64decode(encoded_string)),mimetype='image/jpeg',as_attachment=False)
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'Not foun data'},'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':'parameter incorrect','status_Code':200}),200
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':'not found ' + str(e)})

@status_methods.route('/api/v1/login_qrcode',methods=['POST'])
def login_qrcode():
    data = request.json
    try:
        token_url = data['value']
        result_data = select_qr().select_email_user(token_url)
        if result_data['result'] == 'OK':
            data_value = result_data['data']
            username = data_value['email_user']
            pwd_id   = data_value['pwd']
            result_id = select_qr().select_pwd(pwd_id)
            if result_id['result'] == 'OK':
                data_hash = result_id['data']
                pwd = data_hash['pwdss']
                pwd_1 = pwd[:-128]
                password = pwd_1[128:]
                tmp_json = {
                    "grant_type":  "password",
                    "username":     username,
                    "password":     password,
                    "client_id":    clientId,
                    "client_secret":secretKey
                }
                ipaddress = ''
                response = callPost_v2(one_url+"/api/oauth/getpwd",tmp_json)
                if response['result'] == 'OK':
                    tmp_messageText = response['messageText'].json()
                    print(tmp_messageText)
                    if tmp_messageText['result'] == 'Success':
                        try:
                            username = tmp_messageText['username']
                        except Exception as ex:
                            return jsonify({'result':'Fail','responseCode':401,'data':None,'errorMessage':'login fail! username not found'}),401
                        token_one = tmp_messageText['token_type'] + ' '+ tmp_messageText['access_token']
                        access_token_one = tmp_messageText['access_token']
                        getBuz = callGET_v2(one_url+"/api/account_and_biz_detail",token_one)
                        if getBuz['result'] == 'OK':
                            tmp_account_biz = getBuz['messageText'].json()
                            ts = time.time()
                            user_id         = tmp_account_biz['id']
                            user_email      = tmp_account_biz['thai_email']
                            user_type       = tmp_account_biz['account_category']
                            one_accesstoken = str(tmp_messageText['access_token'])
                            access_time     = ts
                            refresh_token   = tmp_messageText['refresh_token']
                            access_token_time   = ts + tmp_messageText['expires_in']
                            access_token_begin  = ts
                            hash_data       = hash_512_v2(password)
                            citizen_data    = str(tmp_account_biz)
                            getBiz_details  =  tmp_account_biz['biz_detail']
                            result_select   = select().select_LoginUser(username,user_id,user_email)
                            try:
                                # print(result_select)
                                if result_select['result'] == 'OK':
                                    generate_seCode =   'P7Rw2h5GUVE2LpbVNRBO'
                                    result_refToken = generate_tokenPaperless(username,user_email)
                                    result_update = update().update_LoginUser(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress)
                                    resultUpdateLog = update().update_LogLoingBiz(username,user_id,getBiz_details)
                                else:
                                    result_insert = {}
                                    result_insert['result'] = 'OK'
                                    generate_seCode = 'P7Rw2h5GUVE2LpbVNRBO'
                                    result_refToken = generate_tokenPaperless(username,user_email)
                                    result_insert = insert().insert_login(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress)
                                    result_BizLoing = insert().insert_LogBizLogin(username,user_id,getBiz_details)
                                    if result_insert['result'] =='OK':
                                        print(result_insert)
                                    else:
                                        print(result_insert)
                                insert().insert_UserLog(username,user_id,ipaddress,user_email)
                            except Exception as ex:
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                print(exc_type, fname, exc_tb.tb_lineno)
                                # insert().insert_transaction_log(str(response.json()),'OK',str(payload),url)
                                # insert().insert_transaction_log(str(exc_type + ' ' + fname +  ' ' + exc_tb.tb_lineno),'ER',"","/api/v3/login_citizen")
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'connection db fail ' + str(ex)})
                            try:
                                citizen_data = eval(citizen_data)
                            except Exception as ex:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'ไม่สามารถแปลง data เป็น Json ได้'})
                            biz_info = []
                            check_biz_id = []
                            if 'biz_detail' in tmp_account_biz:                        
                                for i in range(len(tmp_account_biz['biz_detail'])):
                                    result_Select_Check_biz = select().select_checkBizPaperless(tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'])
                                    if result_Select_Check_biz['result'] == 'OK':
                                        
                                        if tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'] not in check_biz_id:
                                            # print(getBuz['biz_detail'][i]['getbiz'][0]['id_card_num'],'idcard')
                                            check_biz_id.append(tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'])
                                            data_get_my_dep = {
                                                "tax_id": tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num']
                                            }
                                            text_one_access = 'Bearer ' + one_accesstoken
                                            resultCallAuth_get_dep = callGET_v2(one_url+'/api/v1/service/business/account/'+user_id+'/department_role?tax_id=' + tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'],text_one_access)
                                            # print(resultCallAuth_get_dep)
                                            dep_id_list = []
                                            dept_name_list = []
                                            position_list = []
                                            jsonData = {}
                                            if resultCallAuth_get_dep['result'] == 'OK':
                                                res_json = resultCallAuth_get_dep['messageText'].json()
                                                print(res_json)
                                                if res_json['data'] != None:
                                                    
                                                    data_res = res_json['data']
                                                    if data_res != '':
                                                        for y in range(len(data_res)):
                                                            dep_id = (data_res[y]['dept_id'])
                                                            if dep_id != '' and dep_id != None:
                                                                dep_id_list.append(dep_id)
                                                                dep_data = data_res[y]['department']
                                                                for iy in range(len(dep_data)):
                                                                    dept_name_list.append(dep_data[iy]['dept_name'])
                                                                    try:
                                                                        position_list.append(dep_data[iy]['dept_position'])
                                                                    except Exception as e:
                                                                        position_list.append('')
                                                            elif dep_id != None:
                                                                dep_id_list.append(dep_id)
                                                                dep_data = data_res[y]['department']
                                                                for iy in range(len(dep_data)):
                                                                    dept_name_list.append(dep_data[iy]['dept_name'])
                                                                    try:
                                                                        position_list.append(dep_data[iy]['dept_position'])
                                                                    except Exception as e:
                                                                        position_list.append('')
                                                            else:
                                                                dep_id_list = []
                                                                dep_data = []
                                                                dept_name_list = []
                                                                position_list = []
                                                    else:
                                                        dep_id_list = []
                                                        dep_data = []
                                                        dept_name_list = []
                                                        position_list = []
                                                else:
                                                    jsonData ={}
                                                    dep_id_list = []
                                                    dep_data = []
                                                    dept_name_list = []
                                                    position_list = []
                                                # print(getBuz['biz_detail'][i]['getbiz'])
                                                jsonData = {
                                                    'id':tmp_account_biz['biz_detail'][i]['getbiz'][0]['id'],
                                                    'first_name_th':tmp_account_biz['biz_detail'][i]['getbiz'][0]['first_name_th'],
                                                    'first_name_eng':tmp_account_biz['biz_detail'][i]['getbiz'][0]['first_name_eng'],
                                                    'id_card_type':tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_type'],
                                                    'id_card_num':tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'],
                                                    'role_level':tmp_account_biz['biz_detail'][i]['getrole'][0]['role_level'],
                                                    'role_id':tmp_account_biz['biz_detail'][i]['getrole'][0]['id'],
                                                    'role_name':tmp_account_biz['biz_detail'][i]['getrole'][0]['role_name'],
                                                    'dept_id':dep_id_list,
                                                    'dept_name':dept_name_list,
                                                    'dept_position':position_list
                                                }
                                                # print(jsonData)
                                                biz_info.append(jsonData)
                            else:
                                biz_info = []
                            return jsonify({'result':'OK','username':username,'one_access_token':one_accesstoken,'paperless_access_token':result_refToken,'one_result_data':citizen_data,'one_biz_detail':biz_info})
                        else:
                            result_LoginOffline = LoginOffline(username,password,ipaddress)
                            return jsonify(result_LoginOffline),200
                    else:
                        return jsonify(tmp_messageText)
                else:
                    if response['status_Code'] == 401:
                        return jsonify({'result':'Fail','responseCode':401,'data':None,'errorMessage':'login fail! username not found'}),401
                    else:
                        result_LoginOffline = LoginOffline(username,password,ipaddress)
                        return jsonify(result_LoginOffline),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':result_id['messageER'],'status_Code':200}),200
        else:
            abort(401)
    except Exception as e:
        print(str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'Fail','responseCode':500,'data':None,'errorMessage':str(e)})

def random_generator_secret():
    random_list = []
    for i in range(40):
        random_list.append(random.choice(string.ascii_uppercase + string.digits))
    return random_list

def update_datalogin(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress,getBiz_details):
    result_update = update().update_LoginUser(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress)
    resultUpdateLog = update().update_LogLoingBiz(username,user_id,getBiz_details)
    print(result_update)

def save_qrcode(email_user,token):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=8
        )
        # url = 'https://eform.one.th/login_qr?qr_token='+token
        url = myUrl_domain2 + '_qr?qr_token='+token
        qr.add_data(url)
        qr.make()
        img = qr.make_image(fill_color="black", back_color="white")
        email_user = str(email_user).split('@')[0] + '.jpg'
        # img_name = str(uuid.uuid4()) + '.jpg'
        cwd = os.getcwd()
        image_path = path_global_1 + "/storage/image_qr/"
        # image_path = cwd + "/storage/image_qr/"
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        img.save(image_path+email_user)
        data = {"img_name":email_user,"path_img":image_path}
        return {'result':'OK','messageText':data,'url':url,'messageER': None,'status_Code':200}
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageER': str(err)}

def encode_p(data):
    randoms = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
    secret_key = "f1fedb3d175929f4ef714c8198187944"
    encodes = jwt.encode(data,secret_key,algorithm='HS256')
    encodes = encodes.decode('utf8').split('.')
    encodes[1] = randoms + encodes[1] + randoms
    encodes[2] = randoms + encodes[2]
    encodes = encodes[2] +'.'+encodes[0]+'.'+encodes[1]
    return encodes

def encode_url(data):
    randoms = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
    randoms_2  = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(216)])
    secret_key = "f1fedb3d175929f4ef714c8198187944"
    encodes = jwt.encode(data,secret_key,algorithm='HS256')
    encodes = encodes.decode('utf8').split('.')
    encodes[1] = encodes[1]+randoms_2
    encodes[2] = randoms + encodes[2]
    encodes = encodes[2] +'.'+encodes[0]+'.'+encodes[1]
    return encodes

def decode_url(data):
    decodes = data
    decodes = decodes.split('.')
    decodes[2] = decodes[2][:-216] ##[:-32] ลบข้อมูลนับจากหลังไป 32 ตัวอักษร
    decodes[0] = decodes[0][16:]
    decodes = decodes[1]+'.'+decodes[2]+'.'+decodes[0]
    secret_key = "f1fedb3d175929f4ef714c8198187944"
    decodes = jwt.decode(decodes,secret_key,algorithms='HS256')
    return decodes

def decode_p(data):
    decodes = data
    decodes = decodes.split('.')
    decodes[2] = decodes[2][:-16] ##[:-32] ลบข้อมูลนับจากหลังไป 32 ตัวอักษร
    decodes[2] = decodes[2][16:]
    decodes[0] = decodes[0][16:]
    decodes = decodes[1]+'.'+decodes[2]+'.'+decodes[0]
    secret_key = "f1fedb3d175929f4ef714c8198187944"
    decodes = jwt.decode(decodes,secret_key,algorithms='HS256')
    return decodes

class insert_qr:
    def insert_user_qrcode(self,email_user,url_qrcode,path_qrcode,token_url,token_qr,hash_value,url_login_qrcode,token_url_filter):
        self.email_user         = email_user
        self.url_qrcode         = url_qrcode
        self.path_qrcode        = str(path_qrcode)
        self.token_url          = token_url 
        self.token_qr           = token_qr
        self.hash_value         = hash_value
        self.url_login_qrcode   = url_login_qrcode
        self.token_url_filter   = token_url_filter
        try:
            query_result = db.session.query(paperless_user_qrcode.email_user).filter(paperless_user_qrcode.email_user == self.email_user).all()
            print (query_result)
            if query_result == []:
                table_to_insert = paperless_user_qrcode(
                email_user         =self.email_user,
                url_qrcode         =self.url_qrcode,
                path_qrcode        =self.path_qrcode,
                token_url          =self.token_url,
                token_qr           =self.token_qr,
                hash_value         =self.hash_value,
                url_login_qrcode   =self.url_login_qrcode,
                token_url_filter   =self.token_url_filter,
                url_login_qrcode_new =None
                )
                db.session.add(table_to_insert)
                db.session.flush()
                db.session.commit()
                return {'result':'OK','messageText':'insert success','messageER':None}
            else:
                return {'result':'ER','messageText':None,'messageER':'email_user is already exists'}

        except exc.SQLAlchemyError as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageER':str(ex)}
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageER': str(err)}

    # def insert_user_qrcode(self,email_user,url_qrcode,path_qrcode,token_url,token_qr,hash_value,url_login_qrcode):
    #     self.email_user         = email_user
    #     self.url_qrcode         = url_qrcode
    #     self.path_qrcode        = str(path_qrcode)
    #     self.token_url          = token_url 
    #     self.token_qr           = token_qr
    #     self.hash_value         = hash_value
    #     self.url_login_qrcode   = url_login_qrcode
    #     try:
    #         table_to_insert = paperless_user_qrcode(
    #         email_user         =self.email_user,
    #         url_qrcode         =self.url_qrcode,
    #         path_qrcode        =self.path_qrcode,
    #         token_url          =self.token_url,
    #         token_qr           =self.token_qr,
    #         hash_value         =self.hash_value,
    #         url_login_qrcode   =self.url_login_qrcode
    #         )
    #         db.session.add(table_to_insert)
    #         db.session.flush()
    #         db.session.commit()
    #         return {'result':'OK','messageText':'insert success','messageER':None}
    #     except exc.SQLAlchemyError as ex:
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         print(exc_type, fname, exc_tb.tb_lineno)
    #         return {'result':'ER','messageER':str(ex)}
    #     except Exception as err:
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         print(exc_type, fname, exc_tb.tb_lineno)
    #         return {'result':'ER','messageER': str(err)}

    def insert_pwd(self,pwd_id,hash_pwd):
        self.pwd_id = pwd_id
        self.hash_pwd = hash_pwd
        try:
            table_to_insert = paperless_pwd(
                pwd_id  = self.pwd_id,
                hash_pwd = self.hash_pwd
            )
            db.session.add(table_to_insert)
            db.session.flush()
            db.session.commit()
            return {'result':'OK','messageText':'insert success','messageER':None}
        except exc.SQLAlchemyError as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageER':str(ex)}
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageER': str(err)}

class select_qr:
    def select_email_user_v2(self,token_url):
        self.token_url = token_url
        query_email = db.session.query(
            paperless_user_qrcode.token_url,
            paperless_user_qrcode.hash_value,
            paperless_user_qrcode.token_url_filter
            ).filter_by(token_url_filter=self.token_url).first()
        if query_email != None:
            token_url = query_email.token_url
            hash_value = query_email.hash_value
            hash_data = hash_value+'.'+token_url
            data_value = decode_url(hash_data)
            return {'result':'OK','data':data_value}
        else:
            return {'result':'ER','status_Code':200,'messageText':None,'messageER':'not found user'} 

    def select_email_user_v3(self,token_url):
        self.token_url = token_url
        query_email = db.session.query(
            paperless_user_qrcode.token_url,
            paperless_user_qrcode.hash_value,
            paperless_user_qrcode.token_url_filter
            ).filter_by(token_url_filter=self.token_url).first()
        if query_email != None:
            token_url = query_email.token_url
            hash_value = query_email.hash_value
            hash_data = hash_value+'.'+token_url
            data_value = decode_url(hash_data)
            return {'result':'OK','data':data_value}
        elif query_email == None:
            query_token = db.session.query(
            paperless_user_qrcode.token_url,
            paperless_user_qrcode.hash_value,
            paperless_user_qrcode.token_url_filter
            ).filter_by(url_login_qrcode_new=self.token_url).first()
            if query_token != None:
                token_url = query_token.token_url
                hash_value = query_token.hash_value
                hash_data = hash_value+'.'+token_url
                data_value = decode_url(hash_data)
                return {'result':'OK','data':data_value}
            else:
                return {'result':'ER','status_Code':200,'messageText':None,'messageER':'not found user'} 

    def select_email_user(self,token_url):
        self.token_url = token_url
        query_email = db.session.query(
            paperless_user_qrcode.token_url,
            paperless_user_qrcode.hash_value
            ).filter_by(token_url=self.token_url).first()
        if query_email != None:
            token_url = query_email.token_url
            hash_value = query_email.hash_value
            hash_data = hash_value+'.'+token_url
            data_value = decode_url(hash_data)
            return {'result':'OK','data':data_value}
        else:
            return {'result':'ER','status_Code':200,'messageText':None,'messageER':'not found user'} 

    def select_pwd(self,pwd_id):
        self.pwd_id = pwd_id
        query_id = db.session.query(
            paperless_pwd.hash_pwd
            ).filter_by(pwd_id=self.pwd_id).first()
        if query_id != None:
            hash_value = query_id.hash_pwd
            data_value = decode_p(hash_value)
            return {'result':'OK','data':data_value}
        else:
            return {'result':'ER','status_Code':200,'messageText':None,'messageER':'not found user'}
