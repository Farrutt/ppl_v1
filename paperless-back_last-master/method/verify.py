# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from config.lib import *
from db.db_method import *

class verify:
    def verify_one_id(self,auth_data_token):
        self.auth_data_token = auth_data_token
        self.url = one_url + '/api/account_and_biz_detail'
        try:
            response = requests.request("GET", url=self.url,headers={'Authorization': self.auth_data_token}, verify=False, stream=True,timeout=10)
            tmp_payload_token = str(self.auth_data_token).split(' ')[1]
            if response.status_code == 200 or response.status_code == 201:
                insert().insert_tran_log_v1(str(response.json()),'OK',str(auth_data_token),self.url,tmp_payload_token)
                return {'result': 'OK','messageText': response}
            else:
                insert().insert_tran_log_v1(str(response.text),'ER',str(auth_data_token),self.url,tmp_payload_token)
                return {'result': 'ER','messageText': response}
        except requests.HTTPError as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(auth_data_token),self.url,tmp_payload_token)
            return {'result': 'ER','messageText': "HTTP error occurred."}
        except requests.Timeout as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(auth_data_token),self.url,tmp_payload_token)
            return {'result': 'ER','messageText': 'Request timed out'}
        except requests.ConnectionError as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(auth_data_token),self.url,tmp_payload_token)
            return {'result': 'ER','messageText': 'API Connection error occurred.'}
        except Exception as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(auth_data_token),self.url,tmp_payload_token)
            return {'result': 'ER','messageText': 'An unexpected error: ' + str(ex)}