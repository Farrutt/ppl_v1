#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *

url_convertpdf = 'https://etaxgateway.one.th/convert'
class convert:
    def api_convert(self,data_file):
        self.data_file = data_file
        self.file = self.data_file['file']
        try:
            multipart_data = MultipartEncoder(
                fields={
                    "nameFile":(self.file.filename),
                    "file":(self.file.filename, self.file.read(),"multipart/form-data")
                }
            )
            headers = {
                'Content-Type': multipart_data.content_type
            }
            self.multipart_data = multipart_data
            response = requests.request("POST", url_convertpdf, data=multipart_data, headers=headers, verify=False)
        except Exception as ex:
            print(ex)
            return {'result':'ER','messageText':str(ex)}
        finally:
            try:
                # print(response , "convert")
                if response.json()['status'] == 'Success':
                    return {'result':'OK','messageText':response.json()}
            except Exception as ex:
                return {'result':'ER','messageText':str(ex)}
            
        
        
