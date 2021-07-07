#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.qrcode import *
from controller.mail_string import *
from controller.validate import *
from db.db_method import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from method.pdf import *

if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

@status_methods.route('/api/v1/resize_image',methods=['POST'])
def resize_image_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'image_sign_string' in dataJson:
            image_sign = dataJson['image_sign_string']
            path = './temp/sign_image/'
            path_for_use = '/temp/sign_image/'
            if not os.path.exists(path):
                os.makedirs(path)
            unique_filename = str(uuid.uuid4())
            with open(path + unique_filename + '.png', "wb") as fh:
                fh.write(base64.b64decode((image_sign)))
            path_file_image_sign = os.getcwd() + path_for_use + unique_filename + '.png'
            with open(path_file_image_sign, 'r+b') as f:
                with Image.open(f) as image:
                    cover = resizeimage.resize_width(image, 300)
                    cover.save(path_file_image_sign, image.format)
            with open(path_file_image_sign, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read())
            os.remove(path_file_image_sign)
            return jsonify({'result':'OK','messageText':encoded_string.decode('utf8')})
