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
from controller.mail_string import *
from controller.validate import *
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from db.db_method_4 import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *
from method.sftp_fucn import *
from method.callwebHook import *
from method.cal_tracking import *

@status_methods.route('/api/v3/tracking_paperless',methods=['GET','POST'])
def public_tracking_v1():    
    if request.method == 'GET':
        tmp_id = request.args.get('id')
        tmp_id = str(tmp_id).replace(' ','')
        checktracking = check_digit_tracking(tmp_id)
        # if checktracking:
        if len(tmp_id) > 0:
            r = select_3().select_track_v3(tmp_id)
            return jsonify(r['messageText'])
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':'data not found'})
        # abort(404)
    if request.method == 'POST':
        dataJson = request.json
        if 'tracking_Code' in dataJson:
            tmptrackingcode = dataJson['tracking_Code']
            if len(tmptrackingcode) > 0:
                r = select_3().select_track_v3(tmptrackingcode)
                return jsonify(r['messageText'])            
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':'data not found'})