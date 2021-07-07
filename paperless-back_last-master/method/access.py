# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from db.db_method import *
from db.db_method_1 import *
from config.lib import *
from method.hashpy import *

class model_access:
    def __init__(self, ref_token):
        self.ref_token = ref_token
    
    def get_ref_token(self):
        return self.ref_token
    
    def set_ref_token(self, ref_token):
        self.ref_token = ref_token

def genarate_secretkey(serviceName):
    try:
        keyPair = RSA.generate(3072)

        pubKey = keyPair.publickey()
        # print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
        pubKeyPEM = pubKey.exportKey()
        # print(pubKeyPEM.decode('ascii'))

        # print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")
        privKeyPEM = keyPair.exportKey()
        # print(privKeyPEM.decode('ascii'))
        msg = (serviceName).encode()
        key = RSA.importKey(pubKeyPEM)
        encryptor = PKCS1_OAEP.new(key)
        encrypted = encryptor.encrypt(msg)
        # print("Encrypted:", binascii.hexlify(encrypted))

        # decryptor = PKCS1_OAEP.new(keyPair)
        # decrypted = decryptor.decrypt(encrypted)
        # print('Decrypted:', decrypted)
        # decryptor = PKCS1_OAEP.new(keyPair)
        # decrypted = decryptor.decrypt(encrypted)
        # print('Decrypted:', decrypted)
        return {'result':'OK','public':pubKeyPEM,'private':privKeyPEM,'key':binascii.hexlify(encrypted),'key_process':encrypted}
    except Exception as e:
        print(str(e))
        return {'result':'ER','message':str(e)}

def get_access(token_header):
    ts = time.time() + 86400
    item_ = model_access(token_header) 
    item_.set_refToken(token_header)
    JsonData = decode(item_.get_refToken())
    JsonData['exp'] = str(ts).split('.')[0]
    JsonData['apitype'] = 'Paperless'
    jwt_newSet = encode(JsonData)
    return jwt_newSet

def get_access_v2(token_header):
    ts = time.time() + 86400
    item_ = model_access(token_header) 
    item_.set_refToken(token_header)
    JsonData = decode(item_.get_refToken())
    if 'type' in JsonData:
        if JsonData['type'] == 'paperless':
            JsonData['exp'] = str(ts).split('.')[0]
            JsonData['apitype'] = 'Paperless'
            jwt_newSet = encode(JsonData)
            return {'result':'OK' , 'token':jwt_newSet, 'messageText':None}
        else:
            return {'result':'ER' , 'token':None, 'messageText':'type Fail!'}
    else:
        return {'result':'ER' , 'token':None, 'messageText':'null type!'}

def generate_token_paperless(username, user_email, typeToken = 'paperless'):
    iat_time = time.time()
    exp_time = time.time() + 3600
    jsonData = {
        "iat":      int(iat_time), 
        "username": username, 
        "type":     typeToken, 
        "email":    user_email, 
        "exp":      int(exp_time)
    }
    jwtencode = encode(jsonData)
    return jwtencode

def check_token(token):
    decodes = token
    decodes = decodes.split('.')
    decodes[2] = decodes[2][:-32] ##[:-32] ลบข้อมูลนับจากหลังไป 32 ตัวอักษร
    decodes = decodes[1]+'.'+decodes[2]+'.'+decodes[0]
    try:
        decodes = jwt.decode(decodes, 'bill', algorithms = 'HS256')
        if 'apitype' in decodes:
            if decodes['apitype'] == 'Paperless':
                return {'result':'OK'}
            else:
                return {'result':'ER'}
        else:
            print('decodes not have apitype!')
            return {'result':'ER'}
    except jwt.ExpiredSignatureError:
        print('ExpiredSignatureError!')
        return {'result':'ER'}
    except jwt.InvalidTokenError:
        print('InvalidTokenError!')
        return {'result':'ER'}

def check_ref_token_v1(token):
    decodes = token
    decodes = decodes.split('.')
    decodes[2] = decodes[2][:-32] ##[:-32] ลบข้อมูลนับจากหลังไป 32 ตัวอักษร
    decodes = decodes[1]+'.'+decodes[2]+'.'+decodes[0]
    try:
        decodes = jwt.decode(decodes, 'bill', algorithms = 'HS256')
        return {'result':'OK', 'messageText':decodes}
    except jwt.ExpiredSignatureError:
        print('ExpiredSignatureError!')
        return {'result':'ER'}
    except jwt.InvalidTokenError:
        print('InvalidTokenError!')
        return {'result':'ER'}

def check_Ref_Token(token):
    decodes = token
    decodes = decodes.split('.')
    decodes[2] = decodes[2][:-32] ##[:-32] ลบข้อมูลนับจากหลังไป 32 ตัวอักษร
    decodes = decodes[1]+'.'+decodes[2]+'.'+decodes[0]
    try:
        decodes = jwt.decode(decodes, 'bill', algorithms = 'HS256')
        return {'result':'OK', 'messageText':decodes}
    except jwt.ExpiredSignatureError:
        print('ExpiredSignatureError!')
        return {'result':'ER'}
    except jwt.InvalidTokenError:
        print('InvalidTokenError!')
        return {'result':'ER'}

def token_requiredv1(f):
    """Determines if the access token is valid
    """
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        if len(auth_headers) != 2:
            return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401}), 401

        try:
            decodes = auth_headers[1]
            decodes = decodes.split('.')
            decodes[2] = decodes[2][:-32] ##[:-32] ลบข้อมูลนับจากหลังไป 32 ตัวอักษร
            decodes = decodes[1]+'.'+decodes[2]+'.'+decodes[0]
            decodes = jwt.decode(decodes, 'bill', algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            print('ExpiredSignatureError!')
            return jsonify({'result':'ER', 'messageText':'ExpiredSignatureError!', 'status_Code':401}), 401
        except jwt.InvalidTokenError:
            print('InvalidTokenError!')
            return jsonify({'result':'ER', 'messageText':'InvalidTokenError!', 'status_Code':401}), 401
        except Exception as e:
            print(e)
            return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401}), 401
        return f(*args, **kwargs)
    return _verify

def data_doc(data_document):
    try:
        decodes = jwt.decode(data_document, 'yiDaGvk4c6jbmXaSdiOtIqgS7Dkn5U1ItNz5hxHU', algorithms = 'HS256')
        # print('decodes',decodes)
        return {'result':'OK', 'messageText':decodes}
    except jwt.ExpiredSignatureError:
        print('ExpiredSignatureError!')
        return {'result':'ER'}
    except jwt.InvalidTokenError:
        print('InvalidTokenError!')
        return {'result':'ER'}

def generate_tokenPaperless(username,user_email,typeToken='paperless'):
    username = username
    user_email = user_email
    typeToken = typeToken
    iat_time = time.time()
    exp_time = time.time() + 86400
    jsonData = {
        "iat":      int(iat_time),
        "username": username,
        "type":     typeToken,
        "email":    user_email,
        "exp":      int(exp_time)
    }
    jwtencode = encode(jsonData)
    return jwtencode

def token_required_func(token_Code):
    str_time = time.time()
    resultcheck_shraed_token = check_and_decode_tokenoneid(token_Code)
    end_time = time.time()
    print(resultcheck_shraed_token)
    if resultcheck_shraed_token['result'] == 'ER':
        result_token = check_and_decode_tokenoneid_v2(token_Code)
        # print(result_token)
        if result_token['result'] == 'ER':
            return {'result':'ER'}
        else:
            result_countRowToken = select().select_token_required_v1(token_Code)
            tmpdata = result_token['messageText']
            if result_countRowToken['result'] == 'OK':
                if 'sub' in tmpdata:
                    tmp_userid = tmpdata['sub']
                    result_email = select_1().select_query_email_v1(tmp_userid,token_Code)
                    if result_email['result'] == 'OK':
                        username = result_email['username']
                        email_thai = result_email['emailuser']
                        token_header = result_email['token']
                        tmp_citizen_data = result_email['citizen_data']
                        tmp_biz_info = result_email['biz_info']
                        resulttoeknPaperless = generate_tokenPaperless(username, email_thai)
                        insert().insert_token_requiredOneId(token_header, resulttoeknPaperless,username,email_thai)
                    else:
                        return {'result':'ER'}
                return {'result':'OK','email':email_thai,'username':username,'token':token_header,'user_id':tmp_userid,'citizen_data':tmp_citizen_data,'biz_info':tmp_biz_info}
            else:
                tmpdata = result_token['messageText']
                if 'sub' in tmpdata:
                    tmp_userid = tmpdata['sub']
                    result_email = select_1().select_query_email_v1(tmp_userid,token_Code)
                    if result_email['result'] == 'OK':
                        username = result_email['username']
                        email_thai = result_email['emailuser']
                        token_header = result_email['token']
                        tmp_citizen_data = result_email['citizen_data']
                        tmp_biz_info = result_email['biz_info']
                        resulttoeknPaperless = generate_tokenPaperless(username, email_thai)
                        insert().insert_token_requiredOneId(token_header, resulttoeknPaperless,username,email_thai)
                    else:
                        return {'result':'ER'}
                time_Stemp_expire = result_countRowToken['messageText']['time_expire']
                time_Stemp_base = result_countRowToken['messageText']['time_update']
                if int(time_Stemp_expire) <= int(time_Stemp_base):
                    return {'result':'ER'}
                else:
                    res_checkToken = check_ref_token_v_new(result_countRowToken['messageText']['access'])
                    # print(res_checkToken)
                    if res_checkToken['result'] == 'OK':
                        resulttoeknPaperless = generate_tokenPaperless(username, res_checkToken['messageText']['email'])
                        resultUpdate = update().updateTokenPaperlessSystem(token_Code, resulttoeknPaperless)
                        if resultUpdate['result'] != 'OK':
                            return {'result':'ER'}
                    else:
                        return {'result':'ER'}
                return {'result':'OK','email':email_thai,'username':username,'token':token_header,'user_id':tmp_userid,'citizen_data':tmp_citizen_data,'biz_info':tmp_biz_info}   
    else:
        result_countRowToken = select().select_token_required_v1(token_Code)
        print(result_countRowToken)
        tmpdata = resultcheck_shraed_token['messageText']
        if result_countRowToken['result'] == 'OK':
            if 'sub' in tmpdata:
                tmp_userid = tmpdata['sub']
                result_email = select_1().select_query_email_v1(tmp_userid,token_Code)
                if result_email['result'] == 'OK':
                    username = result_email['username']
                    email_thai = result_email['emailuser']
                    token_header = result_email['token']
                    tmp_citizen_data = result_email['citizen_data']
                    tmp_biz_info = result_email['biz_info']
                    resulttoeknPaperless = generate_tokenPaperless(username, email_thai)
                    insert().insert_token_requiredOneId(token_header, resulttoeknPaperless,username,email_thai)
                else:
                    return {'result':'ER'}
            return {'result':'OK','email':email_thai,'username':username,'token':token_header,'user_id':tmp_userid,'citizen_data':tmp_citizen_data,'biz_info':tmp_biz_info} 
        else:
            time_Stemp_expire = result_countRowToken['messageText']['time_expire']
            time_Stemp_base = result_countRowToken['messageText']['time_update']
            tmpdata = resultcheck_shraed_token['messageText']
            if int(time_Stemp_expire) <= int(time_Stemp_base):
                return {'result':'ER'}
            else:
                if 'sub' in tmpdata:
                    tmp_userid = tmpdata['sub']
                    result_email = select_1().select_query_email_v1(tmp_userid,token_Code)
                    if result_email['result'] == 'OK':
                        username = result_email['username']
                        email_thai = result_email['emailuser']
                        token_header = result_email['token']
                        tmp_citizen_data = result_email['citizen_data']
                        tmp_biz_info = result_email['biz_info']
                        resulttoeknPaperless = generate_tokenPaperless(username, email_thai)
                        insert().insert_token_requiredOneId(token_header, resulttoeknPaperless,username,email_thai)
                    else:
                        return {'result':'ER'}
                res_checkToken = check_ref_token_v_new(result_countRowToken['messageText']['access'])
                if res_checkToken['result'] == 'OK':
                    resulttoeknPaperless = generate_tokenPaperless(username, res_checkToken['messageText']['email'])
                    resultUpdate = update().updateTokenPaperlessSystem(token_Code, resulttoeknPaperless)
                    if resultUpdate['result'] != 'OK':
                        return {'result':'ER'}
                else:
                    return {'result':'ER'}
            return {'result':'OK','email':email_thai,'username':username,'token':token_header,'user_id':tmp_userid,'citizen_data':tmp_citizen_data,'biz_info':tmp_biz_info} 

def token_required_v3(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        if len(auth_headers) != 2:
            abort(401)
        token_Code = auth_headers[1]        
        str_time = time.time()
        resultcheck_shraed_token = check_and_decode_tokenoneid(token_Code)
        end_time = time.time()
        # print(end_time-str_time)
        if resultcheck_shraed_token['result'] == 'ER':
            result_token = check_and_decode_tokenoneid_v2(token_Code)
            # print(result_token)
            if result_token['result'] == 'ER':
                abort(401)
            else:
                result_countRowToken = select().select_token_required_v1(token_Code)
                tmpdata = result_token['messageText']
                if result_countRowToken['result'] == 'OK':
                    if 'sub' in tmpdata:
                        tmp_userid = tmpdata['sub']
                        result_email = select_1().select_query_email_v1(tmp_userid,token_Code)
                        if result_email['result'] == 'OK':
                            username = result_email['username']
                            email_thai = result_email['emailuser']
                            token_header = result_email['token']
                            resulttoeknPaperless = generate_tokenPaperless(username, email_thai)
                            insert().insert_token_requiredOneId(token_header, resulttoeknPaperless,username,email_thai)
                        else:
                            abort(401)
                    return f(*args, **kwargs)
                else:
                    time_Stemp_expire = result_countRowToken['messageText']['time_expire']
                    time_Stemp_base = result_countRowToken['messageText']['time_update']
                    tmpdata = result_token['messageText']
                    if int(time_Stemp_expire) <= int(time_Stemp_base):
                        abort(401)
                    else:
                        res_checkToken = check_ref_token_v_new(result_countRowToken['messageText']['access'])
                        if res_checkToken['result'] == 'OK':
                            resulttoeknPaperless = generate_tokenPaperless(None, res_checkToken['messageText']['email'])
                            # resultUpdate = update().updateTokenPaperlessSystem(token_Code, resulttoeknPaperless)
                            # if resultUpdate['result'] != 'OK':
                            #     abort(401)
                        else:
                            abort(401)
                    return f(*args, **kwargs)            
        else:
            result_countRowToken = select().select_token_required_v1(token_Code)
            tmpdata = resultcheck_shraed_token['messageText']
            if result_countRowToken['result'] == 'OK':
                if 'sub' in tmpdata:
                    tmp_userid = tmpdata['sub']
                    result_email = select_1().select_query_email_v1(tmp_userid,token_Code)
                    if result_email['result'] == 'OK':
                        username = result_email['username']
                        email_thai = result_email['emailuser']
                        token_header = result_email['token']
                        resulttoeknPaperless = generate_tokenPaperless(username, email_thai)
                        insert().insert_token_requiredOneId(token_header, resulttoeknPaperless,username,email_thai)
                    else:
                        abort(401)
                return f(*args, **kwargs)
            else:
                time_Stemp_expire = result_countRowToken['messageText']['time_expire']
                time_Stemp_base = result_countRowToken['messageText']['time_update']
                tmpdata = resultcheck_shraed_token['messageText']
                if int(time_Stemp_expire) <= int(time_Stemp_base):
                    abort(401)
                else:
                    res_checkToken = check_ref_token_v_new(result_countRowToken['messageText']['access'])
                    if res_checkToken['result'] == 'OK':
                        resulttoeknPaperless = generate_tokenPaperless(None, res_checkToken['messageText']['email'])
                        # resultUpdate = update().updateTokenPaperlessSystem(token_Code, resulttoeknPaperless)
                        # if resultUpdate['result'] != 'OK':
                        #     abort(401)
                    else:
                        abort(401)
                return f(*args, **kwargs)
    return _verify

def token_required(f):
    """Determines if the access token is valid
    """
    @wraps(f)
    def _verify(*args, **kwargs):
        # print(f.__name__ + " was called")
        auth_headers = request.headers.get('Authorization', '').split()
        if len(auth_headers) != 2:
            return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401, 'Service':'OneId'}), 401
        token_Code = auth_headers[1]
        result_countRowToken = select().select_token_required_v1(token_Code)
        print(result_countRowToken)
        if result_countRowToken['result'] == 'OK':
            try:
                url = one_url + "/api/account_and_biz_detail"
                headers = {
                    'Content-Type': "application/json", 
                    'Authorization': auth_headers[0] + " " + auth_headers[1]
                }

                response = requests.request("GET", url,  headers = headers, verify = False,timeout=10)
                response = response.json()
                email_thai = response['thai_email']
                username = response['username']
                if 'result' in response:
                    if response['result'] == 'Fail':
                        return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401, 'Service':'OneId'}), 401
            except requests.Timeout as ex:
                return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401, 'Service':'OneId'}), 401
            except requests.HTTPError as ex:
                return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401, 'Service':'OneId'}), 401
            except requests.ConnectionError as ex:
                return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401, 'Service':'OneId'}), 401
            except requests.RequestException as ex:
                return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401, 'Service':'OneId'}), 401
            except Exception as ex:
                return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401, 'Service':'OneId'}), 401
            resulttoeknPaperless = generate_tokenPaperless(username, email_thai)
            insert().insert_token_requiredOneId(token_Code, resulttoeknPaperless,username,email_thai)
            return f(*args, **kwargs)
        else:
            username = 'username'
            time_Stemp_expire = result_countRowToken['messageText']['time_expire']
            time_Stemp_base = result_countRowToken['messageText']['time_update']
            # 1hr  
            # print(int(time_Stemp_expire) , int(time_Stemp_base))
            if int(time_Stemp_expire) <= int(time_Stemp_base):
                return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401, 'Service':'OneId'}), 401
            else:
                res_checkToken = check_ref_token_v_new(result_countRowToken['messageText']['access'])
                if res_checkToken['result'] == 'OK':
                    resulttoeknPaperless = generate_tokenPaperless(None, res_checkToken['messageText']['email'])
                    resultUpdate = update().updateTokenPaperlessSystem(token_Code, resulttoeknPaperless)
                    if resultUpdate['result'] != 'OK':
                        # return redirect(url_paperless)
                        return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401, 'Service':'OneId'}), 401
                else:
                    # return redirect(url_paperless)
                    return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401, 'Service':'OneId'}), 401
                return f(*args, **kwargs)
    return _verify

def token_required_v2(f):
    """Determines if the access token is valid
    """
    @wraps(f)
    def _verify(*args, **kwargs):
        # print(f.__name__ + " was called")
        auth_headers = request.headers.get('Authorization', '').split()
        if len(auth_headers) != 2:
            abort(401)
            return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401, 'Service':'OneId'}), 401
        token_Code = auth_headers[1]
        result_countRowToken = select().select_token_required_v1(token_Code)
        
        if result_countRowToken['result'] == 'OK':
            try:
                url = one_url + "/api/account_and_biz_detail"
                headers = {
                    'Content-Type': "application/json", 
                    'Authorization': auth_headers[0] + " " + auth_headers[1]
                }

                response = requests.request("GET", url,  headers = headers, verify = False)
                # if response.status_code != 200 or response.status_code != 201:
                #     abort(401)
                # else:
                # print(response)
                response = response.json()
                email_thai = response['thai_email']
                username = response['username']
                if 'result' in response:
                    if response['result'] == 'Fail':
                        abort(401)
            except requests.Timeout as ex:
                abort(401)
            except requests.HTTPError as ex:
                abort(401)
            except requests.ConnectionError as ex:
                abort(401)
            except requests.RequestException as ex:
                abort(401)
            except Exception as ex:
                abort(401)
            resulttoeknPaperless = generate_tokenPaperless(username, email_thai)
            insert().insert_token_requiredOneId(token_Code, resulttoeknPaperless,username,email_thai)
            return f(username,email_thai,token_Code)
            return f(*args, **kwargs)
        else:
            try:
                time_Stemp_expire = result_countRowToken['messageText']['time_expire']
                time_Stemp_base = result_countRowToken['messageText']['time_update']
            except Exception as e:
                abort(401)
            
            # 1hr  
            # print(int(time_Stemp_expire) , int(time_Stemp_base))
            if int(time_Stemp_expire) <= int(time_Stemp_base):
                abort(401)
                return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401, 'Service':'OneId'}), 401
            else:
                try:
                    tmp_access = result_countRowToken['messageText']['access']
                except Exception as e:
                    abort(401)
                res_checkToken = check_ref_token_v_new(tmp_access)
                # print(res_checkToken)
                if res_checkToken['result'] == 'OK':
                    username = res_checkToken['messageText']['username']
                    email_thai = res_checkToken['messageText']['email']
                    if res_checkToken['result'] == 'OK':
                        resulttoeknPaperless = generate_tokenPaperless(username, email_thai)
                        resultUpdate = update().updateTokenPaperlessSystem(token_Code, resulttoeknPaperless)
                        if resultUpdate['result'] != 'OK':
                            # return redirect(url_paperless)
                            abort(401)
                            return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401, 'Service':'OneId'}), 401
                    # else:
                    #     # return redirect(url_paperless)
                    #     abort(401)
                    #     return jsonify({'result':'ER', 'messageText':'Authorization Fail!', 'status_Code':401, 'Service':'OneId'}), 401
                else:
                    abort(401)
                
                return f(username,email_thai,token_Code)
                return f(*args, **kwargs)
    return _verify

def check_ref_token_v_new(token):
    decodes = token
    decodes = decodes.split('.')
    decodes[2] = decodes[2][:-32] ##[:-32] ลบข้อมูลนับจากหลังไป 32 ตัวอักษร
    decodes = decodes[1]+'.'+decodes[2]+'.'+decodes[0]
    try:
        decodes = jwt.decode(decodes, 'bill', algorithms = 'HS256')
        return {'result':'OK', 'messageText':decodes}
    except jwt.ExpiredSignatureError:
        print('ExpiredSignatureError!')
        return {'result':'ER'}
    except jwt.InvalidTokenError:
        print('InvalidTokenError!')
        return {'result':'ER'}

def one_access_res_token(req_header):
    
    print(req_header)
    
def check_and_decode_tokenfrom_chat(access):
    try:
        decoded_jwt = jwt.decode(access, 'asdfghjkl1', algorithms = ['HS256'])
        decoded_jwt = decoded_jwt['access_token']   
        decoded_jwt = decoded_jwt
        return {'result':'OK', 'messageText':decoded_jwt}
    except jwt.ExpiredSignatureError:
        print('ExpiredSignatureError!')
        return {'result':'ER'}
    except jwt.InvalidTokenError:
        print('InvalidTokenError!')
        return {'result':'ER'}

def check_and_decode_tokenoneid(access):
    try:
        public_key = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4qyXOIqcyF0zBOyZTOIt\nbVhUQ+frwlpkUW2+mfH+7d0WxaW9lGIWTHKkMM+sCdCpQ6Y0eHECj+1iadZR/8LZ\n'\
        'bH8r8zwfAEhXwGBVtXN0XcGKYwBjmH0iGhGZPMALetCuyRaXpOTbJUps4P6QQkr/\nxONJWtQP7n9vXCBCRIlgUie3vh2nOBl/OLg3xgNdEdCrMJlxcUa3J/EyXyde6Oug\nqgvs//qefdQCkM0txRmRzk81811d/ucORgYlk/0+MksxElP5gHAdOfqtsG4bDgSr\n'\
        'KBlpAJH4mp3Y2BTsaIHGw0gGdgMRgZosqkIOaKMOOTHV4cL7pm5opX9vhUUwhw5i\ndQIDAQAB\n'\
        '-----END PUBLIC KEY-----'
        publicKey = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4qyXOIqcyF0zBOyZTOItbVhUQ+frwlpkUW2+mfH+7d0WxaW9lGIWTHKkMM+sCdCpQ6Y0eHECj+1iadZR/8LZbH8r8zwfAEhXwGBVtXN0XcGKYwBjmH0iGhGZPMALetCuyRaXpOTbJUps4P6QQkr/xONJWtQP7n9vXCBCRIlgUie3vh2nOBl/OLg3xgNdEdCrMJlxcUa3J/EyXyde6Ougqgvs//qefdQCkM0txRmRzk81811d/ucORgYlk/0+MksxElP5gHAdOfqtsG4bDgSrKBlpAJH4mp3Y2BTsaIHGw0gGdgMRgZosqkIOaKMOOTHV4cL7pm5opX9vhUUwhw5idQIDAQAB\n-----END PUBLIC KEY-----'

        # print(publicKey)
        decoded_jwt = jwt.decode(access , publicKey,audience=clientId, algorithms ='RS256')
        # decoded_jwt = decoded_jwt['access_token']
        # decoded_jwt = decoded_jwt
        return {'result':'OK', 'messageText':decoded_jwt}
    except jwt.ExpiredSignatureError:
        print('ExpiredSignatureError!')
        return {'result':'ER'}
    except jwt.InvalidTokenError:
        print('InvalidTokenError!')
        return {'result':'ER'}
    except jwt.exceptions.InvalidAudienceError:
        return {'result':'ER'}

def check_and_decode_tokenoneid_v2(access):
    try:
        decoded_jwt = jwt.decode(access , algorithms ='RS256',verify=False)
        # print(decoded_jwt)
        tmp_time = int(time.time())
        tmp_exp = int(decoded_jwt['exp'])
        if tmp_exp <= tmp_time:
            print('ExpiredSignatureError!')
            return {'result':'ER'}
        # decoded_jwt = decoded_jwt
        return {'result':'OK', 'messageText':decoded_jwt}
    except jwt.ExpiredSignatureError:
        print('ExpiredSignatureError!')
        return {'result':'ER'}
    except jwt.InvalidTokenError:
        print('InvalidTokenError!')
        return {'result':'ER'}

def encode_secret_key(service_id,data_secret):
    data = {}
    jti = str(uuid.uuid4())
    datetime_now = datetime.datetime.now()
    datetime_tstamp = int(datetime.datetime.timestamp(datetime_now))+604800
    result_private_key = select_2().select_private_key(service_id)
    if result_private_key['result'] == 'OK':
        secret_data = result_private_key['messageText']
        # service_id_code = secret_data['code']
        service_name = secret_data['serviceName']
        private_key = secret_data['private']
        try:
            data = {
                "iss": "paperless",
                "aud": service_id,
                "servicename": service_name,
                "jti" : jti,
                "exp": datetime_tstamp,
                "data_decode" :data_secret
            }
            encodes = jwt.encode(data,private_key,algorithm='RS256')
            encodes = encodes.decode('utf8').split('.')
            encodes[1] = encodes[1]
            encodes = encodes[2] +'.'+encodes[0]+'.'+encodes[1]
            # print (encodes)
            return {'result':'OK', 'messageText':encodes}

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

def decode_secret_key(jwt_key,public_key,service_id):
    try:
        decodes = jwt_key.split('.')
        decodes[2] = decodes[2] 
        decodes = decodes[1]+'.'+decodes[2]+'.'+decodes[0]
        decodes = jwt.decode(decodes,public_key,audience=service_id,algorithms='RS256')
        return {'result':'OK', 'messageText':decodes}

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':str(e)}

def generate_key(length):
    return (''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))).upper()

def endcode_access(one_access):
    try:
        data = {
            "iss": "paperless",
            "aud": None,
            "token_data" :one_access
        }
        encodes = jwt.encode(data, 'q2TCgLKSwawLCtVFJnShihR16YqYcNUO', algorithm='HS256')
        # encodes = jwt.encode(data,b'dawdwad',algorithm='RS256')
        encodes = encodes.decode('utf8').split('.')
        encodes[1] = encodes[1]
        encodes = encodes[2] +'.'+encodes[0]+'.'+encodes[1]
        # print (encodes)
        return encodes
    except Exception as e:
        print(str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return None

def dedcode_access(one_access):
    try:
        decodes = one_access.split('.')
        decodes[2] = decodes[2] 
        decodes = decodes[1]+'.'+decodes[2]+'.'+decodes[0]
        decodes = jwt.decode(decodes,'q2TCgLKSwawLCtVFJnShihR16YqYcNUO',algorithms='HS256',verify=False)
        print(decodes)
        return {'result':'OK', 'messageText':decodes}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':str(e)}

# def check_and_decode_tokenoneid_new(access):
#     try:
#         from jwcrypto import jwt, jwk
        
#         ET = jwt.JWT(jwt=access,algs=["HS256"])
#         print(ET.claims)
#         # ST = jwt.JWT(jwt=ET.claims)
#         # print(ST.claims)
#         decoded_jwt = ''
#         # decoded_jwt = decoded_jwt['access_token']
#         # decoded_jwt = decoded_jwt
#         return {'result':'OK', 'messageText':decoded_jwt}
#     except jwt.JWTExpired:
#         print('ExpiredSignatureError!')
#         return {'result':'ER'}
#     except jwt.JWException:
#         print('InvalidTokenError!')
#         return {'result':'ER'}
