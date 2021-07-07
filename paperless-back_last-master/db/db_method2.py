#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from db.db_Class import *
from config.value import *
from method.access import *
from method.hashpy import *
from method.other import *
from config.lib import *

def select_status_file_forSign(sid):
    try:
        query_status = paper_lesssender.query.filter(paper_lesssender.step_data_sid==sid).first()
        if query_status != None:
            tmpjson = query_status.__dict__
            return {'result':'OK','messageText':tmpjson}
        else:
            return {'result':'ER','messageText':{}}
    except Exception as e:
        return {'result':'ER','messageText':{}}

def select_data_pdf_beer(sid, usermail):
    # self.sid = sid
    try:
        sql = '''
            SELECT
                tb_send_detail.file_id,
                tb_step_data.data_json,
                tb_pdf_storage.hash_pdf,
                tb_pdf_storage.hash_sign,
                tb_pdf_storage."path",
                tb_pdf_storage.path_pdf,
                tb_pdf_storage.path_sign,
                tb_pdf_storage.path_rejectorcancle,
                tb_pdf_storage.pdf_rejectorcancle,
                tb_pdf_storage.string_pdf,
                tb_pdf_storage.string_sign
            FROM
                "tb_send_detail"
                INNER JOIN tb_step_data ON tb_step_data.sid = "tb_send_detail".step_data_sid
                INNER JOIN tb_pdf_storage ON tb_pdf_storage.fid = tb_send_detail.file_id 
            WHERE
                "tb_send_detail".step_data_sid =:tmpsid; '''
        with slave.connect() as connection:
            result = connection.execute(text(sql),tmpsid=sid)
            data = [dict(row) for row in result]
        connection.close()
        tmpdata = data[0]
        data_json = data[0]['data_json']
        data_json = data[0]['data_json'].replace("'", '"')
        tmpfile_id = data[0]['file_id']
        # data_json = 
        # query_sid = paper_lessdatastep.query.filter(paper_lessdatastep.sid == sid).first() #.filter(view_document.step_data_sid == self.sid).
        # data_step = query_sid.__dict__ #data_json find position
        # data_json = data_step['data_json']
        # data_json = data_step['data_json'].replace("'", '"')
        arr_tmp = []
        data_step_dict = eval(data_json)
        if 'step_num' in data_step_dict:
            arr_tmp.append(data_step_dict)
            data_step_dict = arr_tmp
        dict_position = {}
        for data in data_step_dict:
            # print(data)
            for d in data['step_detail']:
                if d['one_email'] == usermail:
                    for d_position in d['activity_data']:
                        if d_position != {}:
                            dict_position = d_position
                    break
        # print(dict_position)
        if 'max_page' not in dict_position:
            dict_position['max_page'] = '1'
        dict_position['file_id'] = tmpfile_id
        dict_position['hash_pdf'] = tmpdata['hash_pdf']
        dict_position['hash_sign'] = tmpdata['hash_sign']
        dict_position['path_pdf'] = tmpdata['path_pdf']
        dict_position['path_sign'] = tmpdata['path_sign']
        dict_position['path_rejectorcancle'] = tmpdata['path_rejectorcancle']
        dict_position['string_pdf'] = tmpdata['string_pdf']
        dict_position['string_sign'] = tmpdata['string_sign']
        dict_position['pdf_rejectorcancle'] = tmpdata['pdf_rejectorcancle']
        dict_position['path'] = tmpdata['path']
        # return dict_position
        # query_send_detail = paper_lesssender.query.filter(paper_lesssender.step_data_sid == sid).first()
        # sender = query_send_detail.__dict__
        # dict_position['file_id'] = sender['file_id']
        # query_pdf = paper_lesspdf.query.filter(paper_lesspdf.fid == dict_position['file_id']).first()
        # base64_pdf = query_pdf.__dict__ #pdf base64
        # for key,value in base64_pdf.items():
        #     dict_position[key] = value
            # print(value)
            # with io.BytesIO(base64.b64decode(value)) as open_pdf_file:
            #     read_pdf = PdfFileReader(open_pdf_file)
            #     num_pages = read_pdf.getNumPages()
        # print(dict_position)
        # if 'string_sign' in dict_position:
        #     if dict_position['string_sign'] != None:
        #         with io.BytesIO(base64.b64decode(dict_position['string_sign'])) as open_pdf_file:
        #             read_pdf = PdfFileReader(open_pdf_file)
        #             num_pages = read_pdf.getNumPages()
        #             dict_position['max_page'] = str(num_pages)
                # print(dict_position)
        return {'result':'OK','messageText':dict_position}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        db.session.rollback()
        raise
        return {'result':'ER','messageText':str(ex)}
    finally:
        db.session.close()


# r = select_data_pdf_beer('b1b903d6-be24-4d92-8d0e-d7c22b19138b','warud.mi@thai.com')
# print(r['messageText'].keys())