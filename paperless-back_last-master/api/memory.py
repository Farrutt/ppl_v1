from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.hashpy import *
from method.verify import *
from db.db_method import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.login import *
import os
from datetime import date
import datetime

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less



class memory_check:
    global check
    check = None
    
    def get_check(self):
        # check = None
        try:
            print ('123456',check)
        except Exception as e:
            print(str(e))
        return check

    def set_check(self,ch):
        self.ch = ch
        check = self.ch


# @status_methods.route('/memory_log',methods=['POST'])
def memory_log(message,status_code,request,url_request,methods,hash_token=None):
# def memory_log():
    try:
        
        current_time = time.strftime('%Y-%m')
        date_file = time.strftime('%d-%m-%Y')
        path = '/paperless/log_file/'+ current_time + '/'
        filename = 'test_save_log3'
        
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        id_log = str(uuid.uuid4())
        # print ('hash_token: ',hash_token)

        
        if request != None:
            if 'password' in request:
                
                password = request['password']
                for x in range(len(password)-4):
                    password = password.replace(password[x],'X')
                # print (password)
                request['password'] = password
            
        
        if hash_token != None:
            hash_token = hashlib.sha512(str(hash_token).encode('utf-8')).hexdigest()
        else:
            hash_token = None

        dict_text = {
            'id' : id_log,
            'message' : message,
            'status_code': status_code,
            'datetime': str(st),
            'request' : request,
            'url_request': url_request,
            'methods': methods,
            'hash_token': hash_token
        }

        if not os.path.exists(path):
            os.makedirs(path)
        
        json_dump = json.dumps(dict_text, indent=4)
        
        with open(path + 'request_log_'+ date_file + '.log', "a") as f:
            with open(path + 'request_log_'+ date_file + '.log', "r+") as ff:
                if len(ff.read()) == 0:
                    ff.write(json_dump)
                else:
                    ff.write(',\n' + json_dump)
        
        f.close()
       
        return {'result':'OK','messageText':'save file success','text_id':dict_text['id']}
        

    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print('error',str(e))
            return {'result':'ER','messageText':str(e)}