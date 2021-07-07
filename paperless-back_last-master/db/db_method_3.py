#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from db.db_Class import *
from config.value import *
from method.access import *
from method.hashpy import *
from method.other import *
from config.lib import *
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *


def convert_datetime_TH_2(timestamp_string):
    now1 = datetime.datetime.fromtimestamp(timestamp_string)
    month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[now1.month]
    thai_year = now1.year + 543
    time_str = now1.strftime('%H:%M:%S')
    return "%d %s %d"%(now1.day, month_name, thai_year) # 30 ตุลาคม 2560 20:45:30

def convert_datetime_TH_2_display_sendTime(timestamp_string):
    now1 = datetime.datetime.fromtimestamp(timestamp_string)
    month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[now1.month]
    thai_year = now1.year + 543
    time_str = now1.strftime('%H:%M:%S')
    return "%d %s %d %s"%(now1.day, month_name, thai_year,time_str) # 30 ตุลาคม 2560 20:45:30

def convert_datetime_TH_2_display(timestamp_string):
    now1 = datetime.datetime.fromtimestamp(timestamp_string)
    month_name = 'x ม.ค ก.พ มี.ค เม.ย พ.ค มิ.ย ก.ค ส.ค ก.ย ต.ค พ.ย ธ.ค'.split()[now1.month]
    thai_year = now1.year + 543
    time_str = now1.strftime('%H:%M:%S')
    return "%d %s"%(now1.day, month_name) # 30 ตุลาคม 2560 20:45:30

def timestring_to_timestamp(datetime):
    return int(datetime.timestamp())

def timestamp_to_strtime(datetime_timestamp):
    return datetime.datetime.fromtimestamp(datetime_timestamp).strftime('%Y-%m-%d %H:%M:%S')

def timestamp_to_strtime_justtime(datetime_timestamp):
    return datetime.datetime.fromtimestamp(datetime_timestamp).strftime('%H:%M')

def hr_min_totimestamp(datetime_timestamp):
    return int(time.mktime(datetime.datetime.strptime(datetime_timestamp, "%H:%M").timetuple()))

def convert_datetime_totimestamp(datetime_timestamp):
    return int(time.mktime(datetime.datetime.strptime(datetime_timestamp, '%Y-%m-%d %H:%M:%S').timetuple()))

def filter_calculate_email_user_v1(json_query,json_query_profile):
    tmp_time_now = int(time.time())
    arr_email_one = []
    tmparr_email = []
    tmparr_jsonresult = []
    tmparr_result = []
    for i in range(len(json_query)):
        tmpjsonquery_1 = json_query[i]
        tmp_emailnoti = tmpjsonquery_1['email_noti']
        tmp_sid = tmpjsonquery_1['step_data_sid']
        tmp_doc_id = tmpjsonquery_1['doc_id']
        tmp_noti_timed = tmpjsonquery_1['expire_time']
        tmp_oneday_plus_2= tmpjsonquery_1['oneday_plus_2']
        if tmp_emailnoti != None:
            for j in range(len(tmp_emailnoti)):
                tmpjsonresult = {}
                tmpjsonresult['sid'] = []         
                tmpjsonresult['doc_id'] = []    
                tmpjsonresult['expire_time'] = []
                tmpjsonresult['expire_time_timestamp'] = []
                if (tmp_emailnoti[j]) != '':
                    if tmp_emailnoti[j] not in tmparr_email:  
                        tmpjsonresult['email'] = tmp_emailnoti[j]
                        arr_email_one.append(tmp_emailnoti[j])
                        tmparr_jsonresult.append(tmpjsonresult)
                        tmparr_email.append(tmp_emailnoti[j])
    for z in range(len(tmparr_jsonresult)):
        if 'email' in tmparr_jsonresult[z]:
            tmp_email = tmparr_jsonresult[z]['email']
            for g in range(len(json_query)):
                tmpjsonquery_1 = json_query[g]
                tmp_emailnoti = tmpjsonquery_1['email_noti']
                tmp_doc_id = tmpjsonquery_1['doc_id']
                tmp_noti_time = tmpjsonquery_1['expire_time']
                tmp_sid = tmpjsonquery_1['step_data_sid']
                tmp_oneday_plus_2= tmpjsonquery_1['oneday_plus_2']
                if (tmp_emailnoti) != None:
                    if tmp_email in tmp_emailnoti:
                        tmparr_jsonresult[z]['sid'].append(tmp_sid)
                        tmparr_jsonresult[z]['doc_id'].append(tmp_doc_id)
                        tmparr_jsonresult[z]['expire_time'].append(tmp_noti_time)
                        tmparr_jsonresult[z]['expire_time_timestamp'].append(tmp_oneday_plus_2)
    for n in range(len(tmparr_jsonresult)):
        if 'email' in tmparr_jsonresult[n]:
            tmparr_jsonresult[n]['status_noti'] = False
            tmpemailone = tmparr_jsonresult[n]['email']
            tmp_timeexpire_time = tmparr_jsonresult[n]['expire_time_timestamp']
            tmparr_jsonresult[n]['expire_time_timestamp_update'] = []
            tmparr_jsonresult[n]['expire_time'] = []
            for tt in range(len(json_query_profile)):
                if 'p_emailthai' in json_query_profile[tt]:
                    tmp_emailprofile = json_query_profile[tt]['p_emailthai']
                    tmp_options = json_query_profile[tt]['p_options']
                    if tmp_options != None:
                        if str(tmp_options).replace(' ','').lower() != '':
                            tmp_options = eval(tmp_options)
                            if 'notification_status' in tmp_options:
                                tmpnotification_status = tmp_options['notification_status']
                                if 'notificationOneChat' in tmpnotification_status:
                                    tmpnotificationOneChat = tmpnotification_status['notificationOneChat']
                                    if 'status' in tmpnotificationOneChat:
                                        tmpstatus = tmpnotificationOneChat['status']
                                        if tmpstatus == True:
                                            tmp_config = tmpnotificationOneChat['config']
                                            if tmp_config == []:
                                                tmp_config = 1
                                            if tmp_config == '':
                                                tmp_config = 1
                                            for y in range(len(tmp_timeexpire_time)):
                                                if tmp_emailprofile == tmpemailone:
                                                    tmptime_rang = tmpnotificationOneChat['time_rang']
                                                    if 'start_time' in tmptime_rang and 'end_time' in tmptime_rang:
                                                        tmp_starttimenoti = tmptime_rang['start_time']
                                                        tmp_stoptimenoti = tmptime_rang['end_time']
                                                        if tmp_starttimenoti == None:
                                                            tmp_starttimenoti = '08:00'
                                                        if tmp_stoptimenoti == None:
                                                            tmp_stoptimenoti = '17:00'
                                                        tmphr_min_now = (timestamp_to_strtime_justtime(tmp_time_now))
                                                        tmpdatetime_start = timestamp_to_strtime(tmp_time_now)
                                                        tmpdatetime_start = convert_datetime_totimestamp(tmpdatetime_start.split(' ')[0] + ' ' + tmp_starttimenoti.split(':')[0] + ':' + tmp_starttimenoti.split(':')[1] + ':' + '00')
                                                        tmpdatetime_stop = (timestamp_to_strtime(tmp_time_now))
                                                        # tmpspiltdatetime = tmpdatetime_stop.split(' ')
                                                        # print(tmp_stoptimenoti)
                                                        # tmpspilttimenoti = tmp_stoptimenoti.split(":")
                                                        # print(tmpspiltdatetime[0] + ' ' + tmpspilttimenoti[0])
                                                        tmpdatetime_stop = convert_datetime_totimestamp(tmpdatetime_stop.split(' ')[0] + ' ' + tmp_stoptimenoti.split(':')[0] + ':' + tmp_stoptimenoti.split(':')[1] + ':' + '00')
                                                    if type(tmp_config) is not int:
                                                        tmp_config = int(tmp_config)
                                                    if type(tmp_config) is int:
                                                        converttime = 60 * 60 * tmp_config
                                                        expireupdate = tmp_timeexpire_time[y] + converttime
                                                        tmparr_jsonresult[n]['expire_time_timestamp_update'].append(expireupdate)
                                                        tmparr_jsonresult[n]['expire_time'].append(timestamp_to_strtime(expireupdate))
                                                        tmparr_jsonresult[n]['noti_document_hour'] = tmp_config
                                                        if tmp_time_now >= expireupdate and tmp_time_now >= tmpdatetime_start and tmp_time_now <= tmpdatetime_stop:
                                                            tmparr_jsonresult[n]['status_noti'] = True
    for g in range(len(tmparr_jsonresult)):
        arr_index = []
        if 'email' in tmparr_jsonresult[g]:
            tmpdata = tmparr_jsonresult[g]
            if 'expire_time_timestamp_update' in tmpdata:
                tmpstatus_noti = tmpdata['status_noti']
                tmpexpire_time_timestamp = tmpdata['expire_time_timestamp_update']
                tmpemail = tmpdata['email']
                if tmpstatus_noti == True:
                    jsoniresult = {}
                    jsoniresult['email'] = tmpemail
                    for z in range(len(tmpexpire_time_timestamp)):
                        if tmp_time_now >= tmpexpire_time_timestamp[z]:
                            pass
                        else:
                            arr_index.append(z)
                    for jd in arr_index:
                        try:
                            tmpdata['sid'].pop(jd)
                            tmpdata['doc_id'].pop(jd)
                            tmpdata['expire_time_timestamp'].pop(jd)
                        except Exception as e:
                            pass
                    jsoniresult['sid'] = tmpdata['sid']
                    jsoniresult['doc_id'] = tmpdata['doc_id']
                    jsoniresult['expire_time_timestamp'] = tmpdata['expire_time_timestamp']
                    jsoniresult['noti_time_timestamp'] = min(tmpdata['expire_time_timestamp'])
                    jsoniresult['expire_time'] = []
                    jsoniresult['noti_document_hour'] = tmpdata['noti_document_hour']
                    for yy in range(len(jsoniresult['expire_time_timestamp'])):
                        jsoniresult['expire_time'].append(timestamp_to_strtime(jsoniresult['expire_time_timestamp'][yy]))
                    tmparr_result.append(jsoniresult)
                    # print(len(jsoniresult['sid']),len(jsoniresult['doc_id']),len(jsoniresult['expire_time_timestamp']),len(jsoniresult['expire_time']))
    return (tmparr_result)

def recursive_select_recp_new_v1(emailUser,limit,offset,status,list_sum,sum_row_tooffset,document_type,tax_id,group_status,pick_datetime,sort_key,tmptimeapprove=None):    
    emailUser = emailUser
    status = status
    document_type = document_type
    group_status = group_status
    tmptimeapprove = tmptimeapprove
    if tmptimeapprove != None:
        tmptimeapprove = tmptimeapprove
    if limit != '':
        limit = int(limit)
    else:
        limit = ''
    if offset != '':
        offset = int(offset)
    else:
        offset = ''
    status = status
    list_sum = list_sum
    status_ACTIVE = 'ACTIVE'
    search = "%'{}'%".format(emailUser)
    search_tax_id = "'%''{}''%'".format(tax_id)
    wheresql = ''    
    before_datetime = None
    after_datetime = None
    if pick_datetime != None:
        if pick_datetime != "":
            pick_datetime = int(pick_datetime)
            search_datetime = datetime.datetime.fromtimestamp(pick_datetime).strftime('%Y-%m-%d')
            before_datetime = str(search_datetime) + 'T00:00:00'
            after_datetime = str(search_datetime) + 'T23:59:59'
    if tmptimeapprove == True:
        if sort_key == None:
            ORDER_sql = ' ORDER BY "tb_step_data".update_time DESC LIMIT :limit OFFSET :offset '
        else:
            if sort_key == 'desc':
                ORDER_sql = ' ORDER BY "tb_step_data".update_time DESC LIMIT :limit OFFSET :offset '
            else:
                ORDER_sql = ' ORDER BY "tb_step_data".update_time ASC LIMIT :limit OFFSET :offset '
    else:
        if sort_key == None:
            ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
        else:
            if sort_key == 'desc':
                ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
            else:
                ORDER_sql = ' ORDER BY "tb_send_detail".send_time ASC LIMIT :limit OFFSET :offset '
    where_sql = 'WHERE status=:status AND "recipient_email" LIKE :recipient_email '
    if tax_id != '':
        if type(tax_id) is str:
            where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id
        elif type(tax_id) is list:
            for n in tax_id:
                tmp_taxid = "'%''" + n + "''%'"
                where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + '))'
            where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null)'
    else:
        where_sql += ''
    if status != '':
        where_sql += ' AND "tb_send_detail"."document_status" = :document_status '
    if document_type != '':
        where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
    if group_status == "true":
        where_sql += ' AND ("tb_send_detail"."group_id"=:group_idtmp OR "tb_send_detail"."group_id" IS NULL) '
    if pick_datetime !=  None:
        where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
    where_sql += ORDER_sql
    # print(where_sql)
    text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
                "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
                "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
                "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
                "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
                "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
            FROM "tb_send_detail" \
            INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
            INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    with slave.connect() as connection:
        result = connection.execute(text_sql\
            ,status=status_ACTIVE,recipient_email=search,limit=limit,offset=offset,documentType=document_type,document_status='N',biz_info='',biz_info_none='None',group_idtmp='[]',group_idNone=None,before_datetime=before_datetime,after_datetime=after_datetime)
        connection.close()
    query = [dict(row) for row in result]
    # if self.tax_id != '':
    #     if type(self.tax_id) is str:
    #         where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id
    #     elif type(self.tax_id) is list:
    #         for n in self.tax_id:
    #             tmp_taxid = "'%''" + n + "''%'"
    #             where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + '))'
    #         where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null)'
    # if document_type != '':
    #     if tax_id != '':
    #         query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
    #             .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
    #             .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
    #             .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
    #             .filter(paper_lesssender.document_status=='N')\
    #             .filter(paper_lessdocument.documentType==document_type)\
    #             .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
    #             .order_by(desc(paper_lesssender.send_time))\
    #             .limit(limit)\
    #             .offset(offset)\
    #             .all()
    #         if group_status == "true":
    #             query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
    #                 .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
    #                 .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
    #                 .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
    #                 .filter(paper_lesssender.document_status=='N')\
    #                 .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id=='[]'))\
    #                 .filter(paper_lessdocument.documentType==document_type)\
    #                 .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
    #                 .order_by(desc(paper_lesssender.send_time))\
    #                 .limit(limit)\
    #                 .offset(offset)\
    #                 .all()
    #     else:
    #         query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
    #             .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
    #             .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
    #             .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
    #             .filter(paper_lesssender.document_status=='N')\
    #             .filter(paper_lessdocument.documentType==document_type)\
    #             .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
    #             .order_by(desc(paper_lesssender.send_time))\
    #             .limit(limit)\
    #             .offset(offset)\
    #             .all()
    #         if group_status == "true":
    #             query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
    #                 .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
    #                 .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
    #                 .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
    #                 .filter(paper_lesssender.document_status=='N')\
    #                 .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id=='[]'))\
    #                 .filter(paper_lessdocument.documentType==document_type)\
    #                 .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
    #                 .order_by(desc(paper_lesssender.send_time))\
    #                 .limit(limit)\
    #                 .offset(offset)\
    #                 .all()
    # else:
    #     if tax_id != '':                       
    #         query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
    #             .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
    #             .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
    #             .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
    #             .filter(paper_lesssender.document_status=='N')\
    #             .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
    #             .order_by(desc(paper_lesssender.send_time))\
    #             .limit(limit)\
    #             .offset(offset)\
    #             .all()    
    #         if group_status == "true":  
    #             query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
    #                 .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
    #                 .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
    #                 .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
    #                 .filter(paper_lesssender.document_status=='N')\
    #                 .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id=='[]'))\
    #                 .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
    #                 .order_by(desc(paper_lesssender.send_time))\
    #                 .limit(limit)\
    #                 .offset(offset)\
    #                 .all()                    # .filter(~paper_lessdatastep.biz_info.contains(in_(["'%''5513213355654''%'"])))\
    #     else:
    #         query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
    #             .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
    #             .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
    #             .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
    #             .filter(paper_lesssender.document_status=='N')\
    #             .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
    #             .order_by(desc(paper_lesssender.send_time))\
    #             .limit(limit)\
    #             .offset(offset)\
    #             .all()
    #         if group_status == "true": 
    #             query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
    #                 .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
    #                 .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
    #                 .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
    #                 .filter(paper_lesssender.document_status=='N')\
    #                 .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id=='[]'))\
    #                 .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
    #                 .order_by(desc(paper_lesssender.send_time))\
    #                 .limit(limit)\
    #                 .offset(offset)\
    #                 .all()
    # for u in range(len(query_temp)):
    #     arr_email_document = []
    #     tmp_req_email = []
    #     email_step_sum_w = []
    #     for z in range(len(query_temp[u])):
    #         if z == 0:
    #             tmp_dict_json = query_temp[u][z].__dict__
    #             if '_sa_instance_state' in tmp_dict_json:
    #                 tmp_dict_json['_sa_instance_state'] = str(tmp_dict_json['_sa_instance_state']) 
    #             tmp_sicode = tmp_dict_json['step_data_sid']
    #             # tmp_sid_code_list.append(tmp_sicode)
    #             tmp_send_time = tmp_dict_json['send_time']
    #             tmp_document_id = tmp_dict_json['doc_id']
    #             tmp_tracking_id = tmp_dict_json['tracking_id']
    #             tmp_sender_name = tmp_dict_json['sender_name']
    #             tmp_sender_email = tmp_dict_json['sender_email']
    #             tmp_file_name = tmp_dict_json['file_name']
    #             tmp_groupid = tmp_dict_json['group_id']
    #             email_step_sum = tmp_dict_json['recipient_email']
    #             if email_step_sum != None:
    #                 email_step_sum = eval(email_step_sum)
    #             # print(email_step_sum)
    #             tmpstatus_detail = tmp_dict_json['status_details']
    #             tmpdocument_status = tmp_dict_json['document_status']
    #             tmpstepnow = tmp_dict_json['stepnow']
    #             status_groupid = False
    #             if tmp_groupid != None:
    #                 tmp_groupid = eval(tmp_groupid)
    #                 if len(tmp_groupid) != 0:
    #                     status_groupid = True
    #             if tmpstepnow != None:
    #                 tmpstepnow = int(tmpstepnow)
    #             tmpstepmax = tmp_dict_json['stepmax']
    #             if tmpstepmax != None:
    #                 tmpstepmax = int(tmpstepmax)
    #             if tmpstatus_detail != None:
    #                 tmpstatus_detail = eval(tmpstatus_detail)                            
    #                 for z in range(len(tmpstatus_detail)):
    #                     email_step_sum_w.append(tmpstatus_detail[z]['email'])

    #                 if tmpdocument_status == 'N':
    #                     for x in range(len(tmpstatus_detail)):
    #                         if emailUser not in arr_email_document:
    #                             if emailUser in tmpstatus_detail[x]['email']:
    #                                 if tmpstatus_detail[x]['step_status_code'] == 'W':
    #                                     arr_email_document.append(emailUser)
    #                                     tmpdocument_status = tmpstatus_detail[x]['step_status_code']
    #                                     break
    #                                 else:
    #                                     tmpdocument_status = tmpstatus_detail[x]['step_status_code']
    #             if tmpdocument_status == 'Z':
    #                 res_status_file_string = 'อยู่ในช่วงดำเนินการ'
    #             elif tmpdocument_status == 'W':
    #                 res_status_file_string = 'รอคุณอนุมัติ'
    #             elif tmpdocument_status == 'N':
    #                 res_status_file_string = 'กำลังดำเนินการ'
    #             elif tmpdocument_status == 'R':
    #                 res_status_file_string = 'เอกสารที่ส่งคืนแก้ไข'
    #             else:
    #                 res_status_file_string = ''
    #         if z == 1:
    #             tmp_document_type = None
    #             tmp_dict_json = query_temp[u][z].__dict__
    #             if '_sa_instance_state' in tmp_dict_json:
    #                 tmp_dict_json['_sa_instance_state'] = str(tmp_dict_json['_sa_instance_state'])
    #             tmp_sign_page_options = tmp_dict_json['sign_page_options']
    #             tmp_document_type = tmp_dict_json['documentType']
    #             tmp_options_page = []
    #             if tmp_dict_json['options_page'] != None:
    #                 if tmp_dict_json['options_page'] != '':
    #                 # print(tmp_dict_json['options_page'],tmp_document_id)
    #                     tmp_options_page = [eval(tmp_dict_json['options_page'])]
    #             else:
    #                 tmp_options_page = []
    #             if len(tmp_options_page) != 0:
    #                 # print(tmp_options_page[0]['group_detail'])
    #                 tmp_status_group = False
    #                 if status_groupid == True:
    #                     if len(tmp_options_page) != 0:
    #                         if 'group_detail' in tmp_options_page[0]:
    #                             tmp_group_detail = tmp_options_page[0]['group_detail']
    #                             if 'group_status' in tmp_group_detail:
    #                                 if tmp_group_detail['group_status'] == True:
    #                                     tmp_status_group = True
    #                                     tmpstepnum = tmp_group_detail['step_num']
    #             if tmp_dict_json['documentJson'] != None:
    #                 documentJson_result = eval(tmp_dict_json['documentJson'])
    #                 documentName = documentJson_result['document_name']
    #                 documentType = documentJson_result['document_type']
    #             else:
    #                 documentName = None
    #                 documentType = None
    #             if tmp_dict_json['urgent_type'] != None:
    #                 documentUrgentType = tmp_dict_json['urgent_type']
    #                 if documentUrgentType == 'I':
    #                     documentUrgentString = 'ด่วนมาก'
    #                 elif documentUrgentType == 'U':
    #                     documentUrgentString = 'ด่วน'
    #                 elif documentUrgentType == 'M':
    #                     documentUrgentString = 'ปกติ'
    #         tmp_biz_info = None
    #         tmpdept_name = None
    #         tmprolename = None
    #         tmprole_level = None
    #         if z == 2:
    #             if query_temp[u][z] != None:
    #                 if query_temp[u][z] != 'None':
                        
    #                     eval_biz_info = json.dumps(query_temp[u][z])
    #                     eval_biz_info = json.loads(eval_biz_info)
    #                     eval_biz_info = eval(eval_biz_info)
    #                     # eval_biz_info
    #                     # print(eval_biz_info)
    #                     if 'role_name' in eval_biz_info:
    #                         tmprolename = None
    #                     if 'dept_name' in eval_biz_info:
    #                         tmpdept_name = None
    #                     if 'role_level' in eval_biz_info:
    #                         tmprole_level = None
    #                     if 'dept_name' in eval_biz_info:            
    #                         tmp_biz_info = {
    #                             'tax_id':eval_biz_info['id_card_num'],
    #                             'role_name' : tmprolename,
    #                             'dept_name' : tmpdept_name,
    #                             'role_level' :tmprole_level             
    #                         }                                
    #                     elif 'dept_name' not in eval_biz_info:
    #                         tmp_biz_info = {
    #                             'tax_id':eval_biz_info['id_card_num'],
    #                             'role_name' : eval_biz_info['role_name'],
    #                             'dept_name' : [],
    #                             'role_level' : eval_biz_info['role_level']               
    #                         }
                
    #         dateTime_String = tmp_send_time
    #         th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
    #         ts = int(time.time())
    #         date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    #         year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
    #         datetime_display = int(dateTime_String.timestamp())
    #         date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
    #         yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
    #         time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
    #         old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
    #         if date_time_today == date_time_db:
    #             date_display_show = time_show_db
    #         else:
    #             if year_today == yar_db:
    #                 date_display_show = convert_datetime_TH_2_display(datetime_display)
    #             else:
    #                 date_display_show = old_year
    #     if tmp_status_group == True:
    #         for ui in range(len(tmpstepnum)):
    #             intstepnum = tmpstepnum[ui] - 1
    #             try:
    #                 for w in range(len(email_step_sum_w[intstepnum])):
    #                     tmp_req_email.append(email_step_sum_w[intstepnum][w])
    #             except Exception as e:
    #                 tmp_req_email = []    
    for x in range(len(query)):
        arr_email_document = []
        tmp_req_email = []
        email_step_sum_w = []
        tmpdata = query[x]
        tmp_sicode = tmpdata['step_data_sid']
        # tmp_sid_code_list.append(tmp_sicode)
        tmp_send_time = tmpdata['send_time']
        tmp_document_id = tmpdata['doc_id']
        tmp_tracking_id = tmpdata['tracking_id']
        tmp_sender_name = tmpdata['sender_name']
        tmp_sender_email = tmpdata['sender_email']
        tmp_file_name = tmpdata['file_name']
        tmp_groupid = tmpdata['group_id']
        email_step_sum = tmpdata['recipient_email']
        if email_step_sum != None:
            email_step_sum = eval(email_step_sum)
        tmpstatus_detail = tmpdata['status_details']
        tmpdocument_status = tmpdata['document_status']
        tmpstepnow = tmpdata['stepnow']
        update_time = tmpdata['update_time']
        sender_name_eng = find_name_surename_by_username(tmp_sender_email)
        tmptime_update = update_time
        tmptime_update_timestamp = int(tmptime_update.timestamp())
        tmptime_update_string = str(update_time).split('+')[0]
        th_dateTime_2_last = convert_datetime_TH_2(tmptime_update_timestamp)
        ts = int(time.time())
        date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
        datetime_display_update = int(tmptime_update.timestamp())
        date_time_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%Y-%m-%d')
        yar_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%Y')
        time_show_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%H:%M')
        old_year = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%d/%m/%Y')
        if date_time_today == date_time_db:
            date_last_display_show = time_show_db
        else:
            if year_today == yar_db:
                date_last_display_show = convert_datetime_TH_2_display(datetime_display_update)
            else:
                date_last_display_show = old_year

        status_groupid = False
        if tmp_groupid != None:
            if tmp_groupid != '':
                tmp_groupid = eval(tmp_groupid)
                if len(tmp_groupid) != 0:
                    status_groupid = True
        if tmpstepnow != None:
            tmpstepnow = int(tmpstepnow)
        tmpstepmax = tmpdata['stepmax']
        if tmpstepmax != None:
            tmpstepmax = int(tmpstepmax)
        if tmpstatus_detail != None:
            tmpstatus_detail = eval(tmpstatus_detail)                            
            for z in range(len(tmpstatus_detail)):
                email_step_sum_w.append(tmpstatus_detail[z]['email'])

            if tmpdocument_status == 'N':
                for x in range(len(tmpstatus_detail)):
                    # print(tmp_sicode)
                    # print(tmpstatus_detail[x])
                    # email_step_sum_w.append(tmpstatus_detail[x]['email'])
                    if emailUser not in arr_email_document:
                        if emailUser in tmpstatus_detail[x]['email']:
                            if tmpstatus_detail[x]['step_status_code'] == 'W':
                                arr_email_document.append(emailUser)
                                tmpdocument_status = tmpstatus_detail[x]['step_status_code']
                                break
                            else:
                                tmpdocument_status = tmpstatus_detail[x]['step_status_code']
        if tmpdocument_status == 'Z':
            res_status_file_string = 'อยู่ในช่วงดำเนินการ'
        elif tmpdocument_status == 'W':
            res_status_file_string = 'รอคุณอนุมัติ'
        elif tmpdocument_status == 'N':
            res_status_file_string = 'กำลังดำเนินการ'
        elif tmpdocument_status == 'R':
            res_status_file_string = 'เอกสารที่ส่งคืนแก้ไข'
        else:
            res_status_file_string = 'เอกสารสมบูรณ์'
        tmp_sign_page_options = tmpdata['sign_page_options']
        tmp_document_type = tmpdata['documentType']
        tmp_options_page = []
        if tmpdata['options_page'] != None:
            if tmpdata['options_page'] != '':
            # print(tmp_dict_json['options_page'],tmp_document_id)
                tmp_options_page = [eval(tmpdata['options_page'])]
        else:
            tmp_options_page = []
        if len(tmp_options_page) != 0:
            # print(tmp_options_page[0]['group_detail'])
            tmp_status_group = False
            if status_groupid == True:
                if len(tmp_options_page) != 0:
                    if 'group_detail' in tmp_options_page[0]:
                        tmp_group_detail = tmp_options_page[0]['group_detail']
                        if 'group_status' in tmp_group_detail:
                            if tmp_group_detail['group_status'] == True:
                                tmp_status_group = True
                                tmpstepnum = tmp_group_detail['step_num']
        if tmpdata['documentJson'] != None:
            documentJson_result = eval(tmpdata['documentJson'])
            documentName = documentJson_result['document_name']
            documentType = documentJson_result['document_type']
        else:
            documentName = None
            documentType = None
        if tmpdata['urgent_type'] != None:
            documentUrgentType = tmpdata['urgent_type']
            if documentUrgentType == 'I':
                documentUrgentString = 'ด่วนมาก'
            elif documentUrgentType == 'U':
                documentUrgentString = 'ด่วน'
            elif documentUrgentType == 'M':
                documentUrgentString = 'ปกติ'
        tmp_biz_info = None
        tmpdept_name = None
        tmprolename = None
        tmprole_level = None
        if tmpdata['biz_info'] != None:
            if tmpdata['biz_info'] != 'None':
                if tmpdata['biz_info'] != '':
                    eval_biz_info = json.dumps(tmpdata['biz_info'])
                    eval_biz_info = json.loads(eval_biz_info)
                    # print(eval_biz_info)
                    eval_biz_info = eval(eval_biz_info)
                    # eval_biz_info
                    # print(eval_biz_info)
                    if 'role_name' in eval_biz_info:
                        tmprolename =  eval_biz_info['role_name']                                
                    if 'dept_name' in eval_biz_info:
                        tmpdept_name =  eval_biz_info['dept_name']                               
                    if 'role_level' in eval_biz_info:
                        tmprole_level =  eval_biz_info['role_level']
                    if 'dept_name' in eval_biz_info:  
                        tmp_biz_info = {
                            'tax_id':eval_biz_info['id_card_num'],
                            'role_name' : tmprolename,
                            'dept_name' : tmpdept_name,
                            'role_level' : tmprole_level            
                        }                                
                    elif 'dept_name' not in eval_biz_info:
                        tmp_biz_info = {
                            'tax_id':eval_biz_info['id_card_num'],
                            'role_name' : eval_biz_info['role_name'],
                            'dept_name' : [],
                            'role_level' : eval_biz_info['role_level']               
                        }
        dateTime_String = tmp_send_time
        th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
        ts = int(time.time())
        date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
        datetime_display = int(dateTime_String.timestamp())
        date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
        yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
        time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
        old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
        if date_time_today == date_time_db:
            date_display_show = time_show_db
        else:
            if year_today == yar_db:
                date_display_show = convert_datetime_TH_2_display(datetime_display)
            else:
                date_display_show = old_year
    # print(email_step_sum_w)
        if tmp_status_group == True:
            for ui in range(len(tmpstepnum)):
                intstepnum = tmpstepnum[ui] - 1
                try:
                    for w in range(len(email_step_sum_w[intstepnum])):
                        tmp_req_email.append(email_step_sum_w[intstepnum][w])
                except Exception as e:
                    tmp_req_email = []
        if tmpdocument_status == status:       
            if len(list_sum) < limit:
                sum_row_tooffset = x+1
                list_sum.append({
                    'group_email':tmp_req_email,
                    'group_id':None,
                    'group_status':tmp_status_group,
                    'sidCode':tmp_sicode,
                    'document_name':documentName,
                    'document_type':tmp_document_type,
                    'document_urgent':documentUrgentType,
                    'document_urgent_string':documentUrgentString,
                    'dateTime_String':str(dateTime_String).split('+')[0],
                    'dateTime_String_TH_1':th_dateTime_2,
                    'dateTime_display':date_display_show,
                    'document_id':tmp_document_id,
                    'stamp_all':tmp_sign_page_options,
                    'options_page_document':tmp_options_page,
                    'max_step':tmpstepmax,
                    'step_now':tmpstepnow,
                    # 'dateTime_String_TH_2':th_dateTime_2,
                    'date_String':str(dateTime_String).split(' ')[0],
                    'time_String':str(dateTime_String).split(' ')[1].split('+')[0],
                    'status_file_code':tmpdocument_status,
                    'status_file_string':res_status_file_string,
                    'dateTime':int(dateTime_String.timestamp()),
                    'tracking_id':tmp_tracking_id,
                    'sender_name':tmp_sender_name,
                    'sender_email':tmp_sender_email,
                    'file_name':tmp_file_name,
                    'document_business':tmp_biz_info,
                    'group':status_groupid,
                    'update_last':tmptime_update,
                    'update_last_String_TH_1':th_dateTime_2_last,
                    'update_last_display':date_last_display_show,
                    'update_last_String':tmptime_update_string,
                    'update_last_TimeStamp':tmptime_update_timestamp,
                    'sender_name_eng' : sender_name_eng
                    # 'importance':importance,
                    # 'importance_string':importance_string,
                    # 'last_digitsign':last_digitsign,
                    # 'time_expire':expiry_date
                })
        
        # if tmpdocument_status == status:       
        #     if len(list_sum) < limit:
        #         sum_row_tooffset = u+1
        #         list_sum.append({
        #             'group_email':tmp_req_email,
        #             'group_id':None,
        #             'group_status':tmp_status_group,
        #             'sidCode':tmp_sicode,
        #             'document_name':documentName,
        #             'document_type':tmp_document_type,
        #             'document_urgent':documentUrgentType,
        #             'document_urgent_string':documentUrgentString,
        #             'dateTime_String':str(dateTime_String).split('+')[0],
        #             'dateTime_String_TH_1':th_dateTime_2,
        #             'dateTime_display':date_display_show,
        #             'document_id':tmp_document_id,
        #             'stamp_all':tmp_sign_page_options,
        #             'options_page_document':tmp_options_page,
        #             'max_step':tmpstepmax,
        #             'step_now':tmpstepnow,
        #             # 'dateTime_String_TH_2':th_dateTime_2,
        #             'date_String':str(dateTime_String).split(' ')[0],
        #             'time_String':str(dateTime_String).split(' ')[1].split('+')[0],
        #             'status_file_code':tmpdocument_status,
        #             'status_file_string':res_status_file_string,
        #             'dateTime':int(dateTime_String.timestamp()),
        #             'tracking_id':tmp_tracking_id,
        #             'sender_name':tmp_sender_name,
        #             'sender_email':tmp_sender_email,
        #             'file_name':tmp_file_name,
        #             'document_business':tmp_biz_info
        #         })
            else:
                pass
        else:
            pass 
    return list_sum,sum_row_tooffset


# def recursive_select_recp_new_v1(emailUser,limit,offset,status,list_sum,sum_row_tooffset,document_type,tax_id,group_status,pick_datetime,sort_key):    
#     emailUser = emailUser
#     status = status
#     document_type = document_type
#     group_status = group_status
#     if limit != '':
#         limit = int(limit)
#     else:
#         limit = ''
#     if offset != '':
#         offset = int(offset)
#     else:
#         offset = ''
#     status = status
#     list_sum = list_sum
#     status_ACTIVE = 'ACTIVE'
#     search = "%'{}'%".format(emailUser)
#     search_tax_id = "'%''{}''%'".format(tax_id)
#     wheresql = ''    
#     before_datetime = None
#     after_datetime = None
#     if pick_datetime != None:
#         if pick_datetime != "":
#             pick_datetime = int(pick_datetime)
#             search_datetime = datetime.datetime.fromtimestamp(pick_datetime).strftime('%Y-%m-%d')
#             before_datetime = str(search_datetime) + 'T00:00:00'
#             after_datetime = str(search_datetime) + 'T23:59:59'
#     if sort_key == None:
#         ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
#     else:
#         if sort_key == 'desc':
#             ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
#         else:
#             ORDER_sql = ' ORDER BY "tb_send_detail".send_time ASC LIMIT :limit OFFSET :offset '
#     where_sql = 'WHERE status=:status AND "recipient_email" LIKE :recipient_email '
#     if tax_id != '':
#         if type(tax_id) is str:
#             where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id
#         elif type(tax_id) is list:
#             for n in tax_id:
#                 tmp_taxid = "'%''" + n + "''%'"
#                 where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + '))'
#             where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null)'
#     else:
#         where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR "tb_step_data".biz_info = :biz_info)'
#     if status != '':
#         where_sql += ' AND "tb_send_detail"."document_status" = :document_status '
#     if document_type != '':
#         where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
#     if group_status == "true":
#         where_sql += ' AND ("tb_send_detail"."group_id"=:group_idtmp OR "tb_send_detail"."group_id" IS NULL) '
#     if pick_datetime !=  None:
#         where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
#     where_sql += ORDER_sql
#     print(where_sql)
#     text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
#                 "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
#                 "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
#                 "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
#                 "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
#                 "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
#                 "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
#                 "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
#                 "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
#                 "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
#                 "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
#                 "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
#             FROM "tb_send_detail" \
#             INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
#             INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
#     with slave.connect() as connection:
#         result = connection.execute(text_sql\
#             ,status=status_ACTIVE,recipient_email=search,limit=limit,offset=offset,documentType=document_type,document_status='N',biz_info='',biz_info_none='None',group_idtmp='[]',group_idNone=None,before_datetime=before_datetime,after_datetime=after_datetime)
#         connection.close()
#     query = [dict(row) for row in result]
#     # if self.tax_id != '':
#     #     if type(self.tax_id) is str:
#     #         where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id
#     #     elif type(self.tax_id) is list:
#     #         for n in self.tax_id:
#     #             tmp_taxid = "'%''" + n + "''%'"
#     #             where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + '))'
#     #         where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null)'
#     # if document_type != '':
#     #     if tax_id != '':
#     #         query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#     #             .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#     #             .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#     #             .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
#     #             .filter(paper_lesssender.document_status=='N')\
#     #             .filter(paper_lessdocument.documentType==document_type)\
#     #             .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
#     #             .order_by(desc(paper_lesssender.send_time))\
#     #             .limit(limit)\
#     #             .offset(offset)\
#     #             .all()
#     #         if group_status == "true":
#     #             query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#     #                 .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#     #                 .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#     #                 .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
#     #                 .filter(paper_lesssender.document_status=='N')\
#     #                 .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id=='[]'))\
#     #                 .filter(paper_lessdocument.documentType==document_type)\
#     #                 .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
#     #                 .order_by(desc(paper_lesssender.send_time))\
#     #                 .limit(limit)\
#     #                 .offset(offset)\
#     #                 .all()
#     #     else:
#     #         query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#     #             .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#     #             .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#     #             .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
#     #             .filter(paper_lesssender.document_status=='N')\
#     #             .filter(paper_lessdocument.documentType==document_type)\
#     #             .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
#     #             .order_by(desc(paper_lesssender.send_time))\
#     #             .limit(limit)\
#     #             .offset(offset)\
#     #             .all()
#     #         if group_status == "true":
#     #             query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#     #                 .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#     #                 .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#     #                 .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
#     #                 .filter(paper_lesssender.document_status=='N')\
#     #                 .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id=='[]'))\
#     #                 .filter(paper_lessdocument.documentType==document_type)\
#     #                 .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
#     #                 .order_by(desc(paper_lesssender.send_time))\
#     #                 .limit(limit)\
#     #                 .offset(offset)\
#     #                 .all()
#     # else:
#     #     if tax_id != '':                       
#     #         query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#     #             .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#     #             .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#     #             .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
#     #             .filter(paper_lesssender.document_status=='N')\
#     #             .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
#     #             .order_by(desc(paper_lesssender.send_time))\
#     #             .limit(limit)\
#     #             .offset(offset)\
#     #             .all()    
#     #         if group_status == "true":  
#     #             query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#     #                 .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#     #                 .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#     #                 .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
#     #                 .filter(paper_lesssender.document_status=='N')\
#     #                 .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id=='[]'))\
#     #                 .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
#     #                 .order_by(desc(paper_lesssender.send_time))\
#     #                 .limit(limit)\
#     #                 .offset(offset)\
#     #                 .all()                    # .filter(~paper_lessdatastep.biz_info.contains(in_(["'%''5513213355654''%'"])))\
#     #     else:
#     #         query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#     #             .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#     #             .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#     #             .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
#     #             .filter(paper_lesssender.document_status=='N')\
#     #             .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
#     #             .order_by(desc(paper_lesssender.send_time))\
#     #             .limit(limit)\
#     #             .offset(offset)\
#     #             .all()
#     #         if group_status == "true": 
#     #             query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#     #                 .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#     #                 .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#     #                 .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
#     #                 .filter(paper_lesssender.document_status=='N')\
#     #                 .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id=='[]'))\
#     #                 .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
#     #                 .order_by(desc(paper_lesssender.send_time))\
#     #                 .limit(limit)\
#     #                 .offset(offset)\
#     #                 .all()
#     # for u in range(len(query_temp)):
#     #     arr_email_document = []
#     #     tmp_req_email = []
#     #     email_step_sum_w = []
#     #     for z in range(len(query_temp[u])):
#     #         if z == 0:
#     #             tmp_dict_json = query_temp[u][z].__dict__
#     #             if '_sa_instance_state' in tmp_dict_json:
#     #                 tmp_dict_json['_sa_instance_state'] = str(tmp_dict_json['_sa_instance_state']) 
#     #             tmp_sicode = tmp_dict_json['step_data_sid']
#     #             # tmp_sid_code_list.append(tmp_sicode)
#     #             tmp_send_time = tmp_dict_json['send_time']
#     #             tmp_document_id = tmp_dict_json['doc_id']
#     #             tmp_tracking_id = tmp_dict_json['tracking_id']
#     #             tmp_sender_name = tmp_dict_json['sender_name']
#     #             tmp_sender_email = tmp_dict_json['sender_email']
#     #             tmp_file_name = tmp_dict_json['file_name']
#     #             tmp_groupid = tmp_dict_json['group_id']
#     #             email_step_sum = tmp_dict_json['recipient_email']
#     #             if email_step_sum != None:
#     #                 email_step_sum = eval(email_step_sum)
#     #             # print(email_step_sum)
#     #             tmpstatus_detail = tmp_dict_json['status_details']
#     #             tmpdocument_status = tmp_dict_json['document_status']
#     #             tmpstepnow = tmp_dict_json['stepnow']
#     #             status_groupid = False
#     #             if tmp_groupid != None:
#     #                 tmp_groupid = eval(tmp_groupid)
#     #                 if len(tmp_groupid) != 0:
#     #                     status_groupid = True
#     #             if tmpstepnow != None:
#     #                 tmpstepnow = int(tmpstepnow)
#     #             tmpstepmax = tmp_dict_json['stepmax']
#     #             if tmpstepmax != None:
#     #                 tmpstepmax = int(tmpstepmax)
#     #             if tmpstatus_detail != None:
#     #                 tmpstatus_detail = eval(tmpstatus_detail)                            
#     #                 for z in range(len(tmpstatus_detail)):
#     #                     email_step_sum_w.append(tmpstatus_detail[z]['email'])

#     #                 if tmpdocument_status == 'N':
#     #                     for x in range(len(tmpstatus_detail)):
#     #                         if emailUser not in arr_email_document:
#     #                             if emailUser in tmpstatus_detail[x]['email']:
#     #                                 if tmpstatus_detail[x]['step_status_code'] == 'W':
#     #                                     arr_email_document.append(emailUser)
#     #                                     tmpdocument_status = tmpstatus_detail[x]['step_status_code']
#     #                                     break
#     #                                 else:
#     #                                     tmpdocument_status = tmpstatus_detail[x]['step_status_code']
#     #             if tmpdocument_status == 'Z':
#     #                 res_status_file_string = 'อยู่ในช่วงดำเนินการ'
#     #             elif tmpdocument_status == 'W':
#     #                 res_status_file_string = 'รอคุณอนุมัติ'
#     #             elif tmpdocument_status == 'N':
#     #                 res_status_file_string = 'กำลังดำเนินการ'
#     #             elif tmpdocument_status == 'R':
#     #                 res_status_file_string = 'เอกสารที่ส่งคืนแก้ไข'
#     #             else:
#     #                 res_status_file_string = ''
#     #         if z == 1:
#     #             tmp_document_type = None
#     #             tmp_dict_json = query_temp[u][z].__dict__
#     #             if '_sa_instance_state' in tmp_dict_json:
#     #                 tmp_dict_json['_sa_instance_state'] = str(tmp_dict_json['_sa_instance_state'])
#     #             tmp_sign_page_options = tmp_dict_json['sign_page_options']
#     #             tmp_document_type = tmp_dict_json['documentType']
#     #             tmp_options_page = []
#     #             if tmp_dict_json['options_page'] != None:
#     #                 if tmp_dict_json['options_page'] != '':
#     #                 # print(tmp_dict_json['options_page'],tmp_document_id)
#     #                     tmp_options_page = [eval(tmp_dict_json['options_page'])]
#     #             else:
#     #                 tmp_options_page = []
#     #             if len(tmp_options_page) != 0:
#     #                 # print(tmp_options_page[0]['group_detail'])
#     #                 tmp_status_group = False
#     #                 if status_groupid == True:
#     #                     if len(tmp_options_page) != 0:
#     #                         if 'group_detail' in tmp_options_page[0]:
#     #                             tmp_group_detail = tmp_options_page[0]['group_detail']
#     #                             if 'group_status' in tmp_group_detail:
#     #                                 if tmp_group_detail['group_status'] == True:
#     #                                     tmp_status_group = True
#     #                                     tmpstepnum = tmp_group_detail['step_num']
#     #             if tmp_dict_json['documentJson'] != None:
#     #                 documentJson_result = eval(tmp_dict_json['documentJson'])
#     #                 documentName = documentJson_result['document_name']
#     #                 documentType = documentJson_result['document_type']
#     #             else:
#     #                 documentName = None
#     #                 documentType = None
#     #             if tmp_dict_json['urgent_type'] != None:
#     #                 documentUrgentType = tmp_dict_json['urgent_type']
#     #                 if documentUrgentType == 'I':
#     #                     documentUrgentString = 'ด่วนมาก'
#     #                 elif documentUrgentType == 'U':
#     #                     documentUrgentString = 'ด่วน'
#     #                 elif documentUrgentType == 'M':
#     #                     documentUrgentString = 'ปกติ'
#     #         tmp_biz_info = None
#     #         tmpdept_name = None
#     #         tmprolename = None
#     #         tmprole_level = None
#     #         if z == 2:
#     #             if query_temp[u][z] != None:
#     #                 if query_temp[u][z] != 'None':
                        
#     #                     eval_biz_info = json.dumps(query_temp[u][z])
#     #                     eval_biz_info = json.loads(eval_biz_info)
#     #                     eval_biz_info = eval(eval_biz_info)
#     #                     # eval_biz_info
#     #                     # print(eval_biz_info)
#     #                     if 'role_name' in eval_biz_info:
#     #                         tmprolename = None
#     #                     if 'dept_name' in eval_biz_info:
#     #                         tmpdept_name = None
#     #                     if 'role_level' in eval_biz_info:
#     #                         tmprole_level = None
#     #                     if 'dept_name' in eval_biz_info:            
#     #                         tmp_biz_info = {
#     #                             'tax_id':eval_biz_info['id_card_num'],
#     #                             'role_name' : tmprolename,
#     #                             'dept_name' : tmpdept_name,
#     #                             'role_level' :tmprole_level             
#     #                         }                                
#     #                     elif 'dept_name' not in eval_biz_info:
#     #                         tmp_biz_info = {
#     #                             'tax_id':eval_biz_info['id_card_num'],
#     #                             'role_name' : eval_biz_info['role_name'],
#     #                             'dept_name' : [],
#     #                             'role_level' : eval_biz_info['role_level']               
#     #                         }
                
#     #         dateTime_String = tmp_send_time
#     #         th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
#     #         ts = int(time.time())
#     #         date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
#     #         year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
#     #         datetime_display = int(dateTime_String.timestamp())
#     #         date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
#     #         yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
#     #         time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
#     #         old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
#     #         if date_time_today == date_time_db:
#     #             date_display_show = time_show_db
#     #         else:
#     #             if year_today == yar_db:
#     #                 date_display_show = convert_datetime_TH_2_display(datetime_display)
#     #             else:
#     #                 date_display_show = old_year
#     #     if tmp_status_group == True:
#     #         for ui in range(len(tmpstepnum)):
#     #             intstepnum = tmpstepnum[ui] - 1
#     #             try:
#     #                 for w in range(len(email_step_sum_w[intstepnum])):
#     #                     tmp_req_email.append(email_step_sum_w[intstepnum][w])
#     #             except Exception as e:
#     #                 tmp_req_email = []    
#     for x in range(len(query)):
#         arr_email_document = []
#         tmp_req_email = []
#         email_step_sum_w = []
#         tmpdata = query[x]
#         tmp_sicode = tmpdata['step_data_sid']
#         # tmp_sid_code_list.append(tmp_sicode)
#         tmp_send_time = tmpdata['send_time']
#         tmp_document_id = tmpdata['doc_id']
#         tmp_tracking_id = tmpdata['tracking_id']
#         tmp_sender_name = tmpdata['sender_name']
#         tmp_sender_email = tmpdata['sender_email']
#         tmp_file_name = tmpdata['file_name']
#         tmp_groupid = tmpdata['group_id']
#         email_step_sum = tmpdata['recipient_email']
#         if email_step_sum != None:
#             email_step_sum = eval(email_step_sum)
#         tmpstatus_detail = tmpdata['status_details']
#         tmpdocument_status = tmpdata['document_status']
#         tmpstepnow = tmpdata['stepnow']
#         update_time = tmpdata['update_time']
#         status_groupid = False
#         if tmp_groupid != None:
#             if tmp_groupid != '':
#                 tmp_groupid = eval(tmp_groupid)
#                 if len(tmp_groupid) != 0:
#                     status_groupid = True
#         if tmpstepnow != None:
#             tmpstepnow = int(tmpstepnow)
#         tmpstepmax = tmpdata['stepmax']
#         if tmpstepmax != None:
#             tmpstepmax = int(tmpstepmax)
#         if tmpstatus_detail != None:
#             tmpstatus_detail = eval(tmpstatus_detail)                            
#             for z in range(len(tmpstatus_detail)):
#                 email_step_sum_w.append(tmpstatus_detail[z]['email'])

#             if tmpdocument_status == 'N':
#                 for x in range(len(tmpstatus_detail)):
#                     # print(tmp_sicode)
#                     # print(tmpstatus_detail[x])
#                     # email_step_sum_w.append(tmpstatus_detail[x]['email'])
#                     if emailUser not in arr_email_document:
#                         if emailUser in tmpstatus_detail[x]['email']:
#                             if tmpstatus_detail[x]['step_status_code'] == 'W':
#                                 arr_email_document.append(emailUser)
#                                 tmpdocument_status = tmpstatus_detail[x]['step_status_code']
#                                 break
#                             else:
#                                 tmpdocument_status = tmpstatus_detail[x]['step_status_code']
#         if tmpdocument_status == 'Z':
#             res_status_file_string = 'อยู่ในช่วงดำเนินการ'
#         elif tmpdocument_status == 'W':
#             res_status_file_string = 'รอคุณอนุมัติ'
#         elif tmpdocument_status == 'N':
#             res_status_file_string = 'กำลังดำเนินการ'
#         elif tmpdocument_status == 'R':
#             res_status_file_string = 'เอกสารที่ส่งคืนแก้ไข'
#         else:
#             res_status_file_string = 'เอกสารสมบูรณ์'
#         tmp_sign_page_options = tmpdata['sign_page_options']
#         tmp_document_type = tmpdata['documentType']
#         tmp_options_page = []
#         if tmpdata['options_page'] != None:
#             if tmpdata['options_page'] != '':
#             # print(tmp_dict_json['options_page'],tmp_document_id)
#                 tmp_options_page = [eval(tmpdata['options_page'])]
#         else:
#             tmp_options_page = []
#         if len(tmp_options_page) != 0:
#             # print(tmp_options_page[0]['group_detail'])
#             tmp_status_group = False
#             if status_groupid == True:
#                 if len(tmp_options_page) != 0:
#                     if 'group_detail' in tmp_options_page[0]:
#                         tmp_group_detail = tmp_options_page[0]['group_detail']
#                         if 'group_status' in tmp_group_detail:
#                             if tmp_group_detail['group_status'] == True:
#                                 tmp_status_group = True
#                                 tmpstepnum = tmp_group_detail['step_num']
#         if tmpdata['documentJson'] != None:
#             documentJson_result = eval(tmpdata['documentJson'])
#             documentName = documentJson_result['document_name']
#             documentType = documentJson_result['document_type']
#         else:
#             documentName = None
#             documentType = None
#         if tmpdata['urgent_type'] != None:
#             documentUrgentType = tmpdata['urgent_type']
#             if documentUrgentType == 'I':
#                 documentUrgentString = 'ด่วนมาก'
#             elif documentUrgentType == 'U':
#                 documentUrgentString = 'ด่วน'
#             elif documentUrgentType == 'M':
#                 documentUrgentString = 'ปกติ'
#         tmp_biz_info = None
#         tmpdept_name = None
#         tmprolename = None
#         tmprole_level = None
#         if tmpdata['biz_info'] != None:
#             if tmpdata['biz_info'] != 'None':
#                 if tmpdata['biz_info'] != '':
#                     eval_biz_info = json.dumps(tmpdata['biz_info'])
#                     eval_biz_info = json.loads(eval_biz_info)
#                     # print(eval_biz_info)
#                     eval_biz_info = eval(eval_biz_info)
#                     # eval_biz_info
#                     # print(eval_biz_info)
#                     if 'role_name' in eval_biz_info:
#                         tmprolename =  eval_biz_info['role_name']                                
#                     if 'dept_name' in eval_biz_info:
#                         tmpdept_name =  eval_biz_info['dept_name']                               
#                     if 'role_level' in eval_biz_info:
#                         tmprole_level =  eval_biz_info['role_level']
#                     if 'dept_name' in eval_biz_info:  
#                         tmp_biz_info = {
#                             'tax_id':eval_biz_info['id_card_num'],
#                             'role_name' : tmprolename,
#                             'dept_name' : tmpdept_name,
#                             'role_level' : tmprole_level            
#                         }                                
#                     elif 'dept_name' not in eval_biz_info:
#                         tmp_biz_info = {
#                             'tax_id':eval_biz_info['id_card_num'],
#                             'role_name' : eval_biz_info['role_name'],
#                             'dept_name' : [],
#                             'role_level' : eval_biz_info['role_level']               
#                         }
#         dateTime_String = tmp_send_time
#         th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
#         ts = int(time.time())
#         date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
#         year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
#         datetime_display = int(dateTime_String.timestamp())
#         date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
#         yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
#         time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
#         old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
#         if date_time_today == date_time_db:
#             date_display_show = time_show_db
#         else:
#             if year_today == yar_db:
#                 date_display_show = convert_datetime_TH_2_display(datetime_display)
#             else:
#                 date_display_show = old_year
#     # print(email_step_sum_w)
#         if tmp_status_group == True:
#             for ui in range(len(tmpstepnum)):
#                 intstepnum = tmpstepnum[ui] - 1
#                 try:
#                     for w in range(len(email_step_sum_w[intstepnum])):
#                         tmp_req_email.append(email_step_sum_w[intstepnum][w])
#                 except Exception as e:
#                     tmp_req_email = []
#         if tmpdocument_status == status:       
#             if len(list_sum) < limit:
#                 sum_row_tooffset = x+1
#                 list_sum.append({
#                     'group_email':tmp_req_email,
#                     'group_id':None,
#                     'group_status':tmp_status_group,
#                     'sidCode':tmp_sicode,
#                     'document_name':documentName,
#                     'document_type':tmp_document_type,
#                     'document_urgent':documentUrgentType,
#                     'document_urgent_string':documentUrgentString,
#                     'dateTime_String':str(dateTime_String).split('+')[0],
#                     'dateTime_String_TH_1':th_dateTime_2,
#                     'dateTime_display':date_display_show,
#                     'document_id':tmp_document_id,
#                     'stamp_all':tmp_sign_page_options,
#                     'options_page_document':tmp_options_page,
#                     'max_step':tmpstepmax,
#                     'step_now':tmpstepnow,
#                     # 'dateTime_String_TH_2':th_dateTime_2,
#                     'date_String':str(dateTime_String).split(' ')[0],
#                     'time_String':str(dateTime_String).split(' ')[1].split('+')[0],
#                     'status_file_code':tmpdocument_status,
#                     'status_file_string':res_status_file_string,
#                     'dateTime':int(dateTime_String.timestamp()),
#                     'tracking_id':tmp_tracking_id,
#                     'sender_name':tmp_sender_name,
#                     'sender_email':tmp_sender_email,
#                     'file_name':tmp_file_name,
#                     'document_business':tmp_biz_info,
#                     'group':status_groupid,
#                     'update_time' : update_time,
#                     'update_time_str': str(update_time)
#                     # 'importance':importance,
#                     # 'importance_string':importance_string,
#                     # 'last_digitsign':last_digitsign,
#                     # 'time_expire':expiry_date
#                 })
        
#         # if tmpdocument_status == status:       
#         #     if len(list_sum) < limit:
#         #         sum_row_tooffset = u+1
#         #         list_sum.append({
#         #             'group_email':tmp_req_email,
#         #             'group_id':None,
#         #             'group_status':tmp_status_group,
#         #             'sidCode':tmp_sicode,
#         #             'document_name':documentName,
#         #             'document_type':tmp_document_type,
#         #             'document_urgent':documentUrgentType,
#         #             'document_urgent_string':documentUrgentString,
#         #             'dateTime_String':str(dateTime_String).split('+')[0],
#         #             'dateTime_String_TH_1':th_dateTime_2,
#         #             'dateTime_display':date_display_show,
#         #             'document_id':tmp_document_id,
#         #             'stamp_all':tmp_sign_page_options,
#         #             'options_page_document':tmp_options_page,
#         #             'max_step':tmpstepmax,
#         #             'step_now':tmpstepnow,
#         #             # 'dateTime_String_TH_2':th_dateTime_2,
#         #             'date_String':str(dateTime_String).split(' ')[0],
#         #             'time_String':str(dateTime_String).split(' ')[1].split('+')[0],
#         #             'status_file_code':tmpdocument_status,
#         #             'status_file_string':res_status_file_string,
#         #             'dateTime':int(dateTime_String.timestamp()),
#         #             'tracking_id':tmp_tracking_id,
#         #             'sender_name':tmp_sender_name,
#         #             'sender_email':tmp_sender_email,
#         #             'file_name':tmp_file_name,
#         #             'document_business':tmp_biz_info
#         #         })
#             else:
#                 pass
#         else:
#             pass 
#     return list_sum,sum_row_tooffset

def recursive_select_recp_new_v1_update(emailUser,limit,offset,status,list_sum,sum_row_tooffset,document_type,tax_id,group_status,pick_datetime,sort_key,date_time_from_ts,tmptimeapprove=None):    
    emailUser = emailUser
    status = status
    document_type = document_type
    group_status = group_status
    date_time_from_ts = date_time_from_ts
    tmptimeapprove = tmptimeapprove
    if tmptimeapprove != None:
        tmptimeapprove = tmptimeapprove
    print ('date_time_from_ts:',date_time_from_ts)
    if limit != '':
        limit = int(limit)
    else:
        limit = ''
    if offset != '':
        offset = int(offset)
    else:
        offset = ''
    status = status
    list_sum = list_sum
    status_ACTIVE = 'ACTIVE'
    search = "%'{}'%".format(emailUser)
    search_tax_id = "'%''{}''%'".format(tax_id)
    wheresql = ''    
    before_datetime = None
    after_datetime = None
    if pick_datetime != None:
        if pick_datetime != "":
            pick_datetime = int(pick_datetime)
            search_datetime = datetime.datetime.fromtimestamp(pick_datetime).strftime('%Y-%m-%d')
            before_datetime = str(search_datetime) + 'T00:00:00'
            after_datetime = str(search_datetime) + 'T23:59:59'
    if tmptimeapprove == True:
        if sort_key == None:
            ORDER_sql = ' ORDER BY "tb_step_data".update_time DESC LIMIT :limit OFFSET :offset '
        else:
            if sort_key == 'desc':
                ORDER_sql = ' ORDER BY "tb_step_data".update_time DESC LIMIT :limit OFFSET :offset '
            else:
                ORDER_sql = ' ORDER BY "tb_step_data".update_time ASC LIMIT :limit OFFSET :offset '
    else:
        if sort_key == None:
            ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
        else:
            if sort_key == 'desc':
                ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
            else:
                ORDER_sql = ' ORDER BY "tb_send_detail".send_time ASC LIMIT :limit OFFSET :offset '
    where_sql = 'WHERE status=:status AND "recipient_email" LIKE :recipient_email '
    if tax_id != '':
        if type(tax_id) is str:
            where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id
        elif type(tax_id) is list:
            for n in tax_id:
                tmp_taxid = "'%''" + n + "''%'"
                where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + '))'
            where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null)'
    else:
        where_sql += ''
    if status != '':
        where_sql += ' AND "tb_send_detail"."document_status" = :document_status '
    if document_type != '':
        where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
    if group_status == "true":
        where_sql += ' AND ("tb_send_detail"."group_id"=:group_idtmp OR "tb_send_detail"."group_id" IS NULL) '
    if pick_datetime !=  None:
        where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
    if date_time_from_ts != None:
        where_sql += ' AND ("tb_step_data"."update_time" >= :date_time_from_ts) '
    where_sql += ORDER_sql
    # print(where_sql)
    text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
                "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
                "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
                "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
                "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
                "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
            FROM "tb_send_detail" \
            INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
            INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    with slave.connect() as connection:
        result = connection.execute(text_sql\
            ,status=status_ACTIVE,recipient_email=search,limit=limit,offset=offset,documentType=document_type,document_status='N',biz_info='',biz_info_none='None',group_idtmp='[]',group_idNone=None,before_datetime=before_datetime,after_datetime=after_datetime,date_time_from_ts=date_time_from_ts)
        connection.close()
    query = [dict(row) for row in result]
    for x in range(len(query)):
        arr_email_document = []
        tmp_req_email = []
        email_step_sum_w = []
        tmpdata = query[x]
        tmp_sicode = tmpdata['step_data_sid']
        # tmp_sid_code_list.append(tmp_sicode)
        tmp_send_time = tmpdata['send_time']
        tmp_document_id = tmpdata['doc_id']
        tmp_tracking_id = tmpdata['tracking_id']
        tmp_sender_name = tmpdata['sender_name']
        tmp_sender_email = tmpdata['sender_email']
        tmp_file_name = tmpdata['file_name']
        tmp_groupid = tmpdata['group_id']
        email_step_sum = tmpdata['recipient_email']
        if email_step_sum != None:
            email_step_sum = eval(email_step_sum)
        tmpstatus_detail = tmpdata['status_details']
        tmpdocument_status = tmpdata['document_status']
        tmpstepnow = tmpdata['stepnow']
        update_time = tmpdata['update_time']
        sender_name_eng = find_name_surename_by_username(tmp_sender_email)
        tmptime_update = update_time
        tmptime_update_timestamp = int(tmptime_update.timestamp())
        tmptime_update_string = str(update_time).split('+')[0]
        th_dateTime_2_last = convert_datetime_TH_2(tmptime_update_timestamp)
        ts = int(time.time())
        date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
        datetime_display_update = int(tmptime_update.timestamp())
        date_time_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%Y-%m-%d')
        yar_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%Y')
        time_show_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%H:%M')
        old_year = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%d/%m/%Y')
        if date_time_today == date_time_db:
            date_last_display_show = time_show_db
        else:
            if year_today == yar_db:
                date_last_display_show = convert_datetime_TH_2_display(datetime_display_update)
            else:
                date_last_display_show = old_year

        status_groupid = False
        if tmp_groupid != None:
            if tmp_groupid != '':
                tmp_groupid = eval(tmp_groupid)
                if len(tmp_groupid) != 0:
                    status_groupid = True
        if tmpstepnow != None:
            tmpstepnow = int(tmpstepnow)
        tmpstepmax = tmpdata['stepmax']
        if tmpstepmax != None:
            tmpstepmax = int(tmpstepmax)
        if tmpstatus_detail != None:
            tmpstatus_detail = eval(tmpstatus_detail)                            
            for z in range(len(tmpstatus_detail)):
                email_step_sum_w.append(tmpstatus_detail[z]['email'])

            if tmpdocument_status == 'N':
                for x in range(len(tmpstatus_detail)):
                    # print(tmp_sicode)
                    # print(tmpstatus_detail[x])
                    # email_step_sum_w.append(tmpstatus_detail[x]['email'])
                    if emailUser not in arr_email_document:
                        if emailUser in tmpstatus_detail[x]['email']:
                            if tmpstatus_detail[x]['step_status_code'] == 'W':
                                arr_email_document.append(emailUser)
                                tmpdocument_status = tmpstatus_detail[x]['step_status_code']
                                break
                            else:
                                tmpdocument_status = tmpstatus_detail[x]['step_status_code']
        if tmpdocument_status == 'Z':
            res_status_file_string = 'อยู่ในช่วงดำเนินการ'
        elif tmpdocument_status == 'W':
            res_status_file_string = 'รอคุณอนุมัติ'
        elif tmpdocument_status == 'N':
            res_status_file_string = 'กำลังดำเนินการ'
        elif tmpdocument_status == 'R':
            res_status_file_string = 'เอกสารที่ส่งคืนแก้ไข'
        else:
            res_status_file_string = 'เอกสารสมบูรณ์'
        tmp_sign_page_options = tmpdata['sign_page_options']
        tmp_document_type = tmpdata['documentType']
        tmp_options_page = []
        if tmpdata['options_page'] != None:
            if tmpdata['options_page'] != '':
            # print(tmp_dict_json['options_page'],tmp_document_id)
                tmp_options_page = [eval(tmpdata['options_page'])]
        else:
            tmp_options_page = []
        if len(tmp_options_page) != 0:
            # print(tmp_options_page[0]['group_detail'])
            tmp_status_group = False
            if status_groupid == True:
                if len(tmp_options_page) != 0:
                    if 'group_detail' in tmp_options_page[0]:
                        tmp_group_detail = tmp_options_page[0]['group_detail']
                        if 'group_status' in tmp_group_detail:
                            if tmp_group_detail['group_status'] == True:
                                tmp_status_group = True
                                tmpstepnum = tmp_group_detail['step_num']
        if tmpdata['documentJson'] != None:
            documentJson_result = eval(tmpdata['documentJson'])
            documentName = documentJson_result['document_name']
            documentType = documentJson_result['document_type']
        else:
            documentName = None
            documentType = None
        if tmpdata['urgent_type'] != None:
            documentUrgentType = tmpdata['urgent_type']
            if documentUrgentType == 'I':
                documentUrgentString = 'ด่วนมาก'
            elif documentUrgentType == 'U':
                documentUrgentString = 'ด่วน'
            elif documentUrgentType == 'M':
                documentUrgentString = 'ปกติ'
        tmp_biz_info = None
        tmpdept_name = None
        tmprolename = None
        tmprole_level = None
        if tmpdata['biz_info'] != None:
            if tmpdata['biz_info'] != 'None':
                if tmpdata['biz_info'] != '':
                    eval_biz_info = json.dumps(tmpdata['biz_info'])
                    eval_biz_info = json.loads(eval_biz_info)
                    # print(eval_biz_info)
                    eval_biz_info = eval(eval_biz_info)
                    # eval_biz_info
                    # print(eval_biz_info)
                    if 'role_name' in eval_biz_info:
                        tmprolename =  eval_biz_info['role_name']                                
                    if 'dept_name' in eval_biz_info:
                        tmpdept_name =  eval_biz_info['dept_name']                               
                    if 'role_level' in eval_biz_info:
                        tmprole_level =  eval_biz_info['role_level']
                    if 'dept_name' in eval_biz_info:  
                        tmp_biz_info = {
                            'tax_id':eval_biz_info['id_card_num'],
                            'role_name' : tmprolename,
                            'dept_name' : tmpdept_name,
                            'role_level' : tmprole_level            
                        }                                
                    elif 'dept_name' not in eval_biz_info:
                        tmp_biz_info = {
                            'tax_id':eval_biz_info['id_card_num'],
                            'role_name' : eval_biz_info['role_name'],
                            'dept_name' : [],
                            'role_level' : eval_biz_info['role_level']               
                        }
        dateTime_String = tmp_send_time
        th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
        ts = int(time.time())
        date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
        datetime_display = int(dateTime_String.timestamp())
        date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
        yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
        time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
        old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
        if date_time_today == date_time_db:
            date_display_show = time_show_db
        else:
            if year_today == yar_db:
                date_display_show = convert_datetime_TH_2_display(datetime_display)
            else:
                date_display_show = old_year
    # print(email_step_sum_w)
        if tmp_status_group == True:
            for ui in range(len(tmpstepnum)):
                intstepnum = tmpstepnum[ui] - 1
                try:
                    for w in range(len(email_step_sum_w[intstepnum])):
                        tmp_req_email.append(email_step_sum_w[intstepnum][w])
                except Exception as e:
                    tmp_req_email = []
        if tmpdocument_status == status:       
            if len(list_sum) < limit:
                sum_row_tooffset = x+1
                list_sum.append({
                    'group_email':tmp_req_email,
                    'group_id':None,
                    'group_status':tmp_status_group,
                    'sidCode':tmp_sicode,
                    'document_name':documentName,
                    'document_type':tmp_document_type,
                    'document_urgent':documentUrgentType,
                    'document_urgent_string':documentUrgentString,
                    'dateTime_String':str(dateTime_String).split('+')[0],
                    'dateTime_String_TH_1':th_dateTime_2,
                    'dateTime_display':date_display_show,
                    'document_id':tmp_document_id,
                    'stamp_all':tmp_sign_page_options,
                    'options_page_document':tmp_options_page,
                    'max_step':tmpstepmax,
                    'step_now':tmpstepnow,
                    # 'dateTime_String_TH_2':th_dateTime_2,
                    'date_String':str(dateTime_String).split(' ')[0],
                    'time_String':str(dateTime_String).split(' ')[1].split('+')[0],
                    'status_file_code':tmpdocument_status,
                    'status_file_string':res_status_file_string,
                    'dateTime':int(dateTime_String.timestamp()),
                    'tracking_id':tmp_tracking_id,
                    'sender_name':tmp_sender_name,
                    'sender_email':tmp_sender_email,
                    'file_name':tmp_file_name,
                    'document_business':tmp_biz_info,
                    'group':status_groupid,
                    'update_last':tmptime_update,
                    'update_last_String_TH_1':th_dateTime_2_last,
                    'update_last_display':date_last_display_show,
                    'update_last_String':tmptime_update_string,
                    'update_last_TimeStamp':tmptime_update_timestamp,
                    'sender_name_eng' : sender_name_eng
                    # 'importance':importance,
                    # 'importance_string':importance_string,
                    # 'last_digitsign':last_digitsign,
                    # 'time_expire':expiry_date
                })
            else:
                pass
        else:
            pass 
    return list_sum,sum_row_tooffset
    

# def recursive_select_recp_new_v1_update(emailUser,limit,offset,status,list_sum,sum_row_tooffset,document_type,tax_id,group_status,pick_datetime,sort_key,date_time_from_ts):    
#     emailUser = emailUser
#     status = status
#     document_type = document_type
#     group_status = group_status
#     date_time_from_ts = date_time_from_ts
#     print ('date_time_from_ts:',date_time_from_ts)
#     if limit != '':
#         limit = int(limit)
#     else:
#         limit = ''
#     if offset != '':
#         offset = int(offset)
#     else:
#         offset = ''
#     status = status
#     list_sum = list_sum
#     status_ACTIVE = 'ACTIVE'
#     search = "%'{}'%".format(emailUser)
#     search_tax_id = "'%''{}''%'".format(tax_id)
#     wheresql = ''    
#     before_datetime = None
#     after_datetime = None
#     if pick_datetime != None:
#         if pick_datetime != "":
#             pick_datetime = int(pick_datetime)
#             search_datetime = datetime.datetime.fromtimestamp(pick_datetime).strftime('%Y-%m-%d')
#             before_datetime = str(search_datetime) + 'T00:00:00'
#             after_datetime = str(search_datetime) + 'T23:59:59'
#     if sort_key == None:
#         ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
#     else:
#         if sort_key == 'desc':
#             ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
#         else:
#             ORDER_sql = ' ORDER BY "tb_send_detail".send_time ASC LIMIT :limit OFFSET :offset '
#     where_sql = 'WHERE status=:status AND "recipient_email" LIKE :recipient_email '
#     if tax_id != '':
#         if type(tax_id) is str:
#             where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id
#         elif type(tax_id) is list:
#             for n in tax_id:
#                 tmp_taxid = "'%''" + n + "''%'"
#                 where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + '))'
#             where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null)'
#     else:
#         where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR "tb_step_data".biz_info = :biz_info)'
#     if status != '':
#         where_sql += ' AND "tb_send_detail"."document_status" = :document_status '
#     if document_type != '':
#         where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
#     if group_status == "true":
#         where_sql += ' AND ("tb_send_detail"."group_id"=:group_idtmp OR "tb_send_detail"."group_id" IS NULL) '
#     if pick_datetime !=  None:
#         where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
#     if date_time_from_ts != None:
#         where_sql += ' AND ("tb_step_data"."update_time" >= :date_time_from_ts) '
#     where_sql += ORDER_sql
#     # print(where_sql)
#     text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
#                 "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
#                 "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
#                 "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
#                 "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
#                 "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
#                 "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
#                 "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
#                 "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
#                 "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
#                 "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
#                 "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
#             FROM "tb_send_detail" \
#             INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
#             INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
#     with slave.connect() as connection:
#         result = connection.execute(text_sql\
#             ,status=status_ACTIVE,recipient_email=search,limit=limit,offset=offset,documentType=document_type,document_status='N',biz_info='',biz_info_none='None',group_idtmp='[]',group_idNone=None,before_datetime=before_datetime,after_datetime=after_datetime,date_time_from_ts=date_time_from_ts)
#         connection.close()
#     query = [dict(row) for row in result]
#     for x in range(len(query)):
#         arr_email_document = []
#         tmp_req_email = []
#         email_step_sum_w = []
#         tmpdata = query[x]
#         tmp_sicode = tmpdata['step_data_sid']
#         # tmp_sid_code_list.append(tmp_sicode)
#         tmp_send_time = tmpdata['send_time']
#         tmp_document_id = tmpdata['doc_id']
#         tmp_tracking_id = tmpdata['tracking_id']
#         tmp_sender_name = tmpdata['sender_name']
#         tmp_sender_email = tmpdata['sender_email']
#         tmp_file_name = tmpdata['file_name']
#         tmp_groupid = tmpdata['group_id']
#         email_step_sum = tmpdata['recipient_email']
#         if email_step_sum != None:
#             email_step_sum = eval(email_step_sum)
#         tmpstatus_detail = tmpdata['status_details']
#         tmpdocument_status = tmpdata['document_status']
#         tmpstepnow = tmpdata['stepnow']
#         update_time = tmpdata['update_time']
#         status_groupid = False
#         if tmp_groupid != None:
#             if tmp_groupid != '':
#                 tmp_groupid = eval(tmp_groupid)
#                 if len(tmp_groupid) != 0:
#                     status_groupid = True
#         if tmpstepnow != None:
#             tmpstepnow = int(tmpstepnow)
#         tmpstepmax = tmpdata['stepmax']
#         if tmpstepmax != None:
#             tmpstepmax = int(tmpstepmax)
#         if tmpstatus_detail != None:
#             tmpstatus_detail = eval(tmpstatus_detail)                            
#             for z in range(len(tmpstatus_detail)):
#                 email_step_sum_w.append(tmpstatus_detail[z]['email'])

#             if tmpdocument_status == 'N':
#                 for x in range(len(tmpstatus_detail)):
#                     # print(tmp_sicode)
#                     # print(tmpstatus_detail[x])
#                     # email_step_sum_w.append(tmpstatus_detail[x]['email'])
#                     if emailUser not in arr_email_document:
#                         if emailUser in tmpstatus_detail[x]['email']:
#                             if tmpstatus_detail[x]['step_status_code'] == 'W':
#                                 arr_email_document.append(emailUser)
#                                 tmpdocument_status = tmpstatus_detail[x]['step_status_code']
#                                 break
#                             else:
#                                 tmpdocument_status = tmpstatus_detail[x]['step_status_code']
#         if tmpdocument_status == 'Z':
#             res_status_file_string = 'อยู่ในช่วงดำเนินการ'
#         elif tmpdocument_status == 'W':
#             res_status_file_string = 'รอคุณอนุมัติ'
#         elif tmpdocument_status == 'N':
#             res_status_file_string = 'กำลังดำเนินการ'
#         elif tmpdocument_status == 'R':
#             res_status_file_string = 'เอกสารที่ส่งคืนแก้ไข'
#         else:
#             res_status_file_string = 'เอกสารสมบูรณ์'
#         tmp_sign_page_options = tmpdata['sign_page_options']
#         tmp_document_type = tmpdata['documentType']
#         tmp_options_page = []
#         if tmpdata['options_page'] != None:
#             if tmpdata['options_page'] != '':
#             # print(tmp_dict_json['options_page'],tmp_document_id)
#                 tmp_options_page = [eval(tmpdata['options_page'])]
#         else:
#             tmp_options_page = []
#         if len(tmp_options_page) != 0:
#             # print(tmp_options_page[0]['group_detail'])
#             tmp_status_group = False
#             if status_groupid == True:
#                 if len(tmp_options_page) != 0:
#                     if 'group_detail' in tmp_options_page[0]:
#                         tmp_group_detail = tmp_options_page[0]['group_detail']
#                         if 'group_status' in tmp_group_detail:
#                             if tmp_group_detail['group_status'] == True:
#                                 tmp_status_group = True
#                                 tmpstepnum = tmp_group_detail['step_num']
#         if tmpdata['documentJson'] != None:
#             documentJson_result = eval(tmpdata['documentJson'])
#             documentName = documentJson_result['document_name']
#             documentType = documentJson_result['document_type']
#         else:
#             documentName = None
#             documentType = None
#         if tmpdata['urgent_type'] != None:
#             documentUrgentType = tmpdata['urgent_type']
#             if documentUrgentType == 'I':
#                 documentUrgentString = 'ด่วนมาก'
#             elif documentUrgentType == 'U':
#                 documentUrgentString = 'ด่วน'
#             elif documentUrgentType == 'M':
#                 documentUrgentString = 'ปกติ'
#         tmp_biz_info = None
#         tmpdept_name = None
#         tmprolename = None
#         tmprole_level = None
#         if tmpdata['biz_info'] != None:
#             if tmpdata['biz_info'] != 'None':
#                 if tmpdata['biz_info'] != '':
#                     eval_biz_info = json.dumps(tmpdata['biz_info'])
#                     eval_biz_info = json.loads(eval_biz_info)
#                     # print(eval_biz_info)
#                     eval_biz_info = eval(eval_biz_info)
#                     # eval_biz_info
#                     # print(eval_biz_info)
#                     if 'role_name' in eval_biz_info:
#                         tmprolename =  eval_biz_info['role_name']                                
#                     if 'dept_name' in eval_biz_info:
#                         tmpdept_name =  eval_biz_info['dept_name']                               
#                     if 'role_level' in eval_biz_info:
#                         tmprole_level =  eval_biz_info['role_level']
#                     if 'dept_name' in eval_biz_info:  
#                         tmp_biz_info = {
#                             'tax_id':eval_biz_info['id_card_num'],
#                             'role_name' : tmprolename,
#                             'dept_name' : tmpdept_name,
#                             'role_level' : tmprole_level            
#                         }                                
#                     elif 'dept_name' not in eval_biz_info:
#                         tmp_biz_info = {
#                             'tax_id':eval_biz_info['id_card_num'],
#                             'role_name' : eval_biz_info['role_name'],
#                             'dept_name' : [],
#                             'role_level' : eval_biz_info['role_level']               
#                         }
#         dateTime_String = tmp_send_time
#         th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
#         ts = int(time.time())
#         date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
#         year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
#         datetime_display = int(dateTime_String.timestamp())
#         date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
#         yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
#         time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
#         old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
#         if date_time_today == date_time_db:
#             date_display_show = time_show_db
#         else:
#             if year_today == yar_db:
#                 date_display_show = convert_datetime_TH_2_display(datetime_display)
#             else:
#                 date_display_show = old_year
#     # print(email_step_sum_w)
#         if tmp_status_group == True:
#             for ui in range(len(tmpstepnum)):
#                 intstepnum = tmpstepnum[ui] - 1
#                 try:
#                     for w in range(len(email_step_sum_w[intstepnum])):
#                         tmp_req_email.append(email_step_sum_w[intstepnum][w])
#                 except Exception as e:
#                     tmp_req_email = []
#         if tmpdocument_status == status:       
#             if len(list_sum) < limit:
#                 sum_row_tooffset = x+1
#                 list_sum.append({
#                     'group_email':tmp_req_email,
#                     'group_id':None,
#                     'group_status':tmp_status_group,
#                     'sidCode':tmp_sicode,
#                     'document_name':documentName,
#                     'document_type':tmp_document_type,
#                     'document_urgent':documentUrgentType,
#                     'document_urgent_string':documentUrgentString,
#                     'dateTime_String':str(dateTime_String).split('+')[0],
#                     'dateTime_String_TH_1':th_dateTime_2,
#                     'dateTime_display':date_display_show,
#                     'document_id':tmp_document_id,
#                     'stamp_all':tmp_sign_page_options,
#                     'options_page_document':tmp_options_page,
#                     'max_step':tmpstepmax,
#                     'step_now':tmpstepnow,
#                     # 'dateTime_String_TH_2':th_dateTime_2,
#                     'date_String':str(dateTime_String).split(' ')[0],
#                     'time_String':str(dateTime_String).split(' ')[1].split('+')[0],
#                     'status_file_code':tmpdocument_status,
#                     'status_file_string':res_status_file_string,
#                     'dateTime':int(dateTime_String.timestamp()),
#                     'tracking_id':tmp_tracking_id,
#                     'sender_name':tmp_sender_name,
#                     'sender_email':tmp_sender_email,
#                     'file_name':tmp_file_name,
#                     'document_business':tmp_biz_info,
#                     'group':status_groupid,
#                     'update_time' : update_time,
#                     'update_time_str' : str(update_time)
#                     # 'importance':importance,
#                     # 'importance_string':importance_string,
#                     # 'last_digitsign':last_digitsign,
#                     # 'time_expire':expiry_date
#                 })
#             else:
#                 pass
#         else:
#             pass 
#     return list_sum,sum_row_tooffset
    


def recursive_select_recp_new_v2(emailUser,limit,offset,status,list_sum,sum_row_tooffset,document_type,tax_id,sort_key,pick_datetime,tmptimeapprove=None):    
    emailUser = emailUser
    status = status
    status_ACTIVE = 'ACTIVE'
    tmp_sid_code_list = []
    document_type = document_type
    tmptimeapprove = tmptimeapprove
    if tmptimeapprove != None:
        tmptimeapprove = tmptimeapprove
    if limit != '':
        limit = int(limit)
    else:
        limit = ''
    if offset != '':
        offset = int(offset)
    else:
        offset = ''
    status = status
    list_sum = list_sum
    before_datetime = None
    after_datetime = None
    search = "%'{}'%".format(emailUser)
    search_tax_id = "%'{}'%".format(tax_id)
    where_sql = 'WHERE status=:status AND "recipient_email" LIKE :recipient_email '
    if pick_datetime != None:
        if pick_datetime != "":
            pick_datetime = int(pick_datetime)
            search_datetime = datetime.datetime.fromtimestamp(pick_datetime).strftime('%Y-%m-%d')
            before_datetime = str(search_datetime) + 'T00:00:00'
            after_datetime = str(search_datetime) + 'T23:59:59'
    if tmptimeapprove == True:
        if sort_key == None:
            ORDER_sql = ' ORDER BY "tb_step_data".update_time DESC LIMIT :limit OFFSET :offset '
        else:
            if sort_key == 'desc':
                ORDER_sql = ' ORDER BY "tb_step_data".update_time DESC LIMIT :limit OFFSET :offset '
            else:
                ORDER_sql = ' ORDER BY "tb_step_data".update_time ASC LIMIT :limit OFFSET :offset '
    else:
        if sort_key == None:
            ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
        else:
            if sort_key == 'desc':
                ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
            else:
                ORDER_sql = ' ORDER BY "tb_send_detail".send_time ASC LIMIT :limit OFFSET :offset '
    if status != '':
        where_sql += ' AND "tb_send_detail"."document_status" = :document_status '
    if document_type != '':
        where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
    if pick_datetime !=  None:
        where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
    if document_type != '':
        if tax_id != '':
            if type(tax_id) is str:
                where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id
            elif type(tax_id) is list:
                for n in tax_id:
                    tmp_taxid = "'%''" + n + "''%'"
                    where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + '))'
                where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null)'
            where_sql += ' AND ("tb_send_detail".document_status=:document_status)'
            where_sql += ORDER_sql
            text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                    "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                    "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                    "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                    "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                    "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                    "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
                    "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
                    "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
                    "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
                    "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
                    "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
                FROM "tb_send_detail" \
                INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
            with slave.connect() as connection:
                result = connection.execute(text_sql\
                    ,status=status_ACTIVE,document_status='N',recipient_email=search,limit=limit,offset=offset,documentType=document_type,biz_info='',biz_info_none='None',biz_info_null=None,before_datetime=before_datetime,after_datetime=after_datetime)
                connection.close()
            query = [dict(row) for row in result]
        else:
            query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
                .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
                .filter(paper_lesssender.document_status=='N')\
                .filter(paper_lessdocument.documentType==document_type)\
                .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
                .order_by(desc(paper_lesssender.send_time))\
                .limit(limit)\
                .offset(offset)\
                .all()
    else:
        # print(tax_id)
        if tax_id != '':          
            if type(tax_id) is str:
                where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id
            elif type(tax_id) is list:
                for n in tax_id:
                    tmp_taxid = "'%''" + n + "''%'"
                    where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + '))'
                where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null)'
            where_sql += ' AND ("tb_send_detail".document_status=:document_status)'
            where_sql += ORDER_sql
            text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                    "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                    "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                    "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                    "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                    "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                    "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
                    "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
                    "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
                    "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
                    "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
                    "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
                FROM "tb_send_detail" \
                INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
            # print(text_sql)
            with slave.connect() as connection:
                result = connection.execute(text_sql\
                    ,status=status_ACTIVE,document_status='N',recipient_email=search,limit=limit,offset=offset,documentType=document_type,biz_info='',biz_info_none='None',biz_info_null=None,before_datetime=before_datetime,after_datetime=after_datetime)
                connection.close()
            query = [dict(row) for row in result]
        else:
            query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
                .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
                .filter(paper_lesssender.document_status=='N')\
                .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
                .order_by(desc(paper_lesssender.send_time))\
                .limit(limit)\
                .offset(offset)\
                .all()
    # print(query)
    for x in range(len(query)):
        arr_email_document = []
        tmp_req_email = []
        email_step_sum_w = []
        tmpdata = query[x]
        tmp_sicode = tmpdata['step_data_sid']
        tmp_sid_code_list.append(tmp_sicode)
        tmp_send_time = tmpdata['send_time']
        tmp_document_id = tmpdata['doc_id']
        tmp_tracking_id = tmpdata['tracking_id']
        tmp_sender_name = tmpdata['sender_name']
        tmp_sender_email = tmpdata['sender_email']
        tmp_file_name = tmpdata['file_name']
        tmp_groupid = tmpdata['group_id']
        email_step_sum = tmpdata['recipient_email']
        update_time = tmpdata['update_time']

        sender_name_eng = find_name_surename_by_username(tmp_sender_email)

        tmptime_update = update_time
        tmptime_update_timestamp = int(tmptime_update.timestamp())
        tmptime_update_string = str(update_time).split('+')[0]
        th_dateTime_2_last = convert_datetime_TH_2(tmptime_update_timestamp)
        ts = int(time.time())
        date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
        datetime_display_update = int(tmptime_update.timestamp())
        date_time_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%Y-%m-%d')
        yar_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%Y')
        time_show_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%H:%M')
        old_year = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%d/%m/%Y')
        if date_time_today == date_time_db:
            date_last_display_show = time_show_db
        else:
            if year_today == yar_db:
                date_last_display_show = convert_datetime_TH_2_display(datetime_display_update)
            else:
                date_last_display_show = old_year

        if email_step_sum != None:
            email_step_sum = eval(email_step_sum)
        tmpstatus_detail = tmpdata['status_details']
        tmpdocument_status = tmpdata['document_status']
        tmpstepnow = tmpdata['stepnow']
        status_groupid = False
        if tmp_groupid != None:
            if tmp_groupid != '':
                tmp_groupid = eval(tmp_groupid)
                if len(tmp_groupid) != 0:
                    status_groupid = True
        if tmpstepnow != None:
            tmpstepnow = int(tmpstepnow)
        tmpstepmax = tmpdata['stepmax']
        if tmpstepmax != None:
            tmpstepmax = int(tmpstepmax)
        if tmpstatus_detail != None:
            tmpstatus_detail = eval(tmpstatus_detail)                            
            for z in range(len(tmpstatus_detail)):
                email_step_sum_w.append(tmpstatus_detail[z]['email'])

            if tmpdocument_status == 'N':
                for x in range(len(tmpstatus_detail)):
                    if emailUser not in arr_email_document:
                        if emailUser in tmpstatus_detail[x]['email']:
                            if tmpstatus_detail[x]['step_status_code'] == 'W':
                                arr_email_document.append(emailUser)
                                tmpdocument_status = tmpstatus_detail[x]['step_status_code']
                                break
                            else:
                                tmpdocument_status = tmpstatus_detail[x]['step_status_code']
        if tmpdocument_status == 'Z':
            res_status_file_string = 'อยู่ในช่วงดำเนินการ'
        elif tmpdocument_status == 'W':
            res_status_file_string = 'รอคุณอนุมัติ'
        elif tmpdocument_status == 'N':
            res_status_file_string = 'กำลังดำเนินการ'
        elif tmpdocument_status == 'R':
            res_status_file_string = 'เอกสารที่ส่งคืนแก้ไข'
        else:
            res_status_file_string = 'เอกสารสมบูรณ์'
        tmp_sign_page_options = tmpdata['sign_page_options']
        tmp_document_type = tmpdata['documentType']
        tmp_options_page = []
        if tmpdata['options_page'] != None:
            if tmpdata['options_page'] != '':
            # print(tmp_dict_json['options_page'],tmp_document_id)
                tmp_options_page = [eval(tmpdata['options_page'])]
        else:
            tmp_options_page = []
        if len(tmp_options_page) != 0:
            # print(tmp_options_page[0]['group_detail'])
            tmp_status_group = False
            if status_groupid == True:
                if len(tmp_options_page) != 0:
                    if 'group_detail' in tmp_options_page[0]:
                        tmp_group_detail = tmp_options_page[0]['group_detail']
                        if 'group_status' in tmp_group_detail:
                            if tmp_group_detail['group_status'] == True:
                                tmp_status_group = True
                                tmpstepnum = tmp_group_detail['step_num']
        if tmpdata['documentJson'] != None:
            documentJson_result = eval(tmpdata['documentJson'])
            documentName = documentJson_result['document_name']
            documentType = documentJson_result['document_type']
        else:
            documentName = None
            documentType = None
        if tmpdata['urgent_type'] != None:
            documentUrgentType = tmpdata['urgent_type']
            if documentUrgentType == 'I':
                documentUrgentString = 'ด่วนมาก'
            elif documentUrgentType == 'U':
                documentUrgentString = 'ด่วน'
            elif documentUrgentType == 'M':
                documentUrgentString = 'ปกติ'
        tmp_biz_info = None
        tmprole_name = None
        tmpdept_name = None
        tmprole_level = None
        if tmpdata['biz_info'] != None:
            if tmpdata['biz_info'] != 'None':
                if tmpdata['biz_info'] != '':
                    eval_biz_info = json.dumps(tmpdata['biz_info'])
                    eval_biz_info = json.loads(eval_biz_info)
                    eval_biz_info = eval(eval_biz_info)
                    if 'role_name' in eval_biz_info:
                        tmprole_name = eval_biz_info['role_name']
                    if 'dept_name' in eval_biz_info:
                        tmpdept_name = eval_biz_info['dept_name']
                    if 'role_level' in eval_biz_info:
                        tmprole_level = eval_biz_info['role_level']
                    if 'dept_name' in eval_biz_info:            
                        tmp_biz_info = {
                            'tax_id':eval_biz_info['id_card_num'],
                            'role_name' : tmprole_name,
                            'dept_name' : tmpdept_name,
                            'role_level' : tmprole_level             
                        }                                
                    elif 'dept_name' not in eval_biz_info:
                        tmp_biz_info = {
                            'tax_id':eval_biz_info['id_card_num'],
                            'role_name' : tmprole_name,
                            'dept_name' : [],
                            'role_level' : tmprole_level               
                        }
        dateTime_String = tmp_send_time
        th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
        ts = int(time.time())
        date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
        datetime_display = int(dateTime_String.timestamp())
        date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
        yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
        time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
        old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
        if date_time_today == date_time_db:
            date_display_show = time_show_db
        else:
            if year_today == yar_db:
                date_display_show = convert_datetime_TH_2_display(datetime_display)
            else:
                date_display_show = old_year

        if tmp_status_group == True:
            for ui in range(len(tmpstepnum)):
                intstepnum = tmpstepnum[ui] - 1
                try:
                    for w in range(len(email_step_sum_w[intstepnum])):
                        tmp_req_email.append(email_step_sum_w[intstepnum][w])
                except Exception as e:
                    tmp_req_email = []
        if tmpdocument_status == status:       
            if len(list_sum) < limit:
                sum_row_tooffset = x+1
                list_sum.append({
                    'group_email':tmp_req_email,
                    'group_id':None,
                    'group_status':tmp_status_group,
                    'sidCode':tmp_sicode,
                    'document_name':documentName,
                    'document_type':tmp_document_type,
                    'document_urgent':documentUrgentType,
                    'document_urgent_string':documentUrgentString,
                    'dateTime_String':str(dateTime_String).split('+')[0],
                    'dateTime_String_TH_1':th_dateTime_2,
                    'dateTime_display':date_display_show,
                    'document_id':tmp_document_id,
                    'stamp_all':tmp_sign_page_options,
                    'options_page_document':tmp_options_page,
                    'max_step':tmpstepmax,
                    'step_now':tmpstepnow,
                    'date_String':str(dateTime_String).split(' ')[0],
                    'time_String':str(dateTime_String).split(' ')[1].split('+')[0],
                    'status_file_code':tmpdocument_status,
                    'status_file_string':res_status_file_string,
                    'dateTime':int(dateTime_String.timestamp()),
                    'tracking_id':tmp_tracking_id,
                    'sender_name':tmp_sender_name,
                    'sender_email':tmp_sender_email,
                    'file_name':tmp_file_name,
                    'document_business':tmp_biz_info,
                    'group':status_groupid,
                    'update_last':tmptime_update,
                    'update_last_String_TH_1':th_dateTime_2_last,
                    'update_last_display':date_last_display_show,
                    'update_last_String':tmptime_update_string,
                    'update_last_TimeStamp':tmptime_update_timestamp,
                    'sender_name_eng' : sender_name_eng
                })
            else:
                pass
        else:
            pass 
    return list_sum,sum_row_tooffset


# def recursive_select_recp_new_v2(emailUser,limit,offset,status,list_sum,sum_row_tooffset,document_type,tax_id,sort_key,pick_datetime):    
#     emailUser = emailUser
#     status = status
#     status_ACTIVE = 'ACTIVE'
#     tmp_sid_code_list = []
#     document_type = document_type
#     if limit != '':
#         limit = int(limit)
#     else:
#         limit = ''
#     if offset != '':
#         offset = int(offset)
#     else:
#         offset = ''
#     status = status
#     list_sum = list_sum
#     before_datetime = None
#     after_datetime = None
#     search = "%'{}'%".format(emailUser)
#     search_tax_id = "%'{}'%".format(tax_id)
#     where_sql = 'WHERE status=:status AND "recipient_email" LIKE :recipient_email '
#     if pick_datetime != None:
#         if pick_datetime != "":
#             pick_datetime = int(pick_datetime)
#             search_datetime = datetime.datetime.fromtimestamp(pick_datetime).strftime('%Y-%m-%d')
#             before_datetime = str(search_datetime) + 'T00:00:00'
#             after_datetime = str(search_datetime) + 'T23:59:59'
#     if sort_key == None:
#         ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
#     else:
#         if sort_key == 'desc':
#             ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
#         else:
#             ORDER_sql = ' ORDER BY "tb_send_detail".send_time ASC LIMIT :limit OFFSET :offset '
#     if status != '':
#         where_sql += ' AND "tb_send_detail"."document_status" = :document_status '
#     if document_type != '':
#         where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
#     if pick_datetime !=  None:
#         where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
#     if document_type != '':
#         if tax_id != '':
#             if type(tax_id) is str:
#                 where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id
#             elif type(tax_id) is list:
#                 for n in tax_id:
#                     tmp_taxid = "'%''" + n + "''%'"
#                     where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + '))'
#                 where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null)'
#             where_sql += ' AND ("tb_send_detail".document_status=:document_status)'
#             where_sql += ORDER_sql
#             text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
#                     "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
#                     "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
#                     "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
#                     "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
#                     "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
#                     "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
#                     "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
#                     "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
#                     "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
#                     "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
#                     "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
#                 FROM "tb_send_detail" \
#                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
#                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
#             with slave.connect() as connection:
#                 result = connection.execute(text_sql\
#                     ,status=status_ACTIVE,document_status='N',recipient_email=search,limit=limit,offset=offset,documentType=document_type,biz_info='',biz_info_none='None',biz_info_null=None,before_datetime=before_datetime,after_datetime=after_datetime)
#                 connection.close()
#             query = [dict(row) for row in result]
#         else:
#             query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#                 .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#                 .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#                 .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
#                 .filter(paper_lesssender.document_status=='N')\
#                 .filter(paper_lessdocument.documentType==document_type)\
#                 .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
#                 .order_by(desc(paper_lesssender.send_time))\
#                 .limit(limit)\
#                 .offset(offset)\
#                 .all()
#     else:
#         # print(tax_id)
#         if tax_id != '':          
#             if type(tax_id) is str:
#                 where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id
#             elif type(tax_id) is list:
#                 for n in tax_id:
#                     tmp_taxid = "'%''" + n + "''%'"
#                     where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + '))'
#                 where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null)'
#             where_sql += ' AND ("tb_send_detail".document_status=:document_status)'
#             where_sql += ORDER_sql
#             text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
#                     "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
#                     "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
#                     "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
#                     "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
#                     "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
#                     "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
#                     "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
#                     "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
#                     "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
#                     "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
#                     "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
#                 FROM "tb_send_detail" \
#                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
#                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
#             print(text_sql)
#             with slave.connect() as connection:
#                 result = connection.execute(text_sql\
#                     ,status=status_ACTIVE,document_status='N',recipient_email=search,limit=limit,offset=offset,documentType=document_type,biz_info='',biz_info_none='None',biz_info_null=None,before_datetime=before_datetime,after_datetime=after_datetime)
#                 connection.close()
#             query = [dict(row) for row in result]
#         else:
#             query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#                 .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#                 .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#                 .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.recipient_email.like(search))\
#                 .filter(paper_lesssender.document_status=='N')\
#                 .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
#                 .order_by(desc(paper_lesssender.send_time))\
#                 .limit(limit)\
#                 .offset(offset)\
#                 .all()
#     print(query)
#     for x in range(len(query)):
#         arr_email_document = []
#         tmp_req_email = []
#         email_step_sum_w = []
#         tmpdata = query[x]
#         tmp_sicode = tmpdata['step_data_sid']
#         tmp_sid_code_list.append(tmp_sicode)
#         tmp_send_time = tmpdata['send_time']
#         tmp_document_id = tmpdata['doc_id']
#         tmp_tracking_id = tmpdata['tracking_id']
#         tmp_sender_name = tmpdata['sender_name']
#         tmp_sender_email = tmpdata['sender_email']
#         tmp_file_name = tmpdata['file_name']
#         tmp_groupid = tmpdata['group_id']
#         email_step_sum = tmpdata['recipient_email']
#         if email_step_sum != None:
#             email_step_sum = eval(email_step_sum)
#         tmpstatus_detail = tmpdata['status_details']
#         tmpdocument_status = tmpdata['document_status']
#         tmpstepnow = tmpdata['stepnow']
#         status_groupid = False
#         if tmp_groupid != None:
#             if tmp_groupid != '':
#                 tmp_groupid = eval(tmp_groupid)
#                 if len(tmp_groupid) != 0:
#                     status_groupid = True
#         if tmpstepnow != None:
#             tmpstepnow = int(tmpstepnow)
#         tmpstepmax = tmpdata['stepmax']
#         if tmpstepmax != None:
#             tmpstepmax = int(tmpstepmax)
#         if tmpstatus_detail != None:
#             tmpstatus_detail = eval(tmpstatus_detail)                            
#             for z in range(len(tmpstatus_detail)):
#                 email_step_sum_w.append(tmpstatus_detail[z]['email'])

#             if tmpdocument_status == 'N':
#                 for x in range(len(tmpstatus_detail)):
#                     if emailUser not in arr_email_document:
#                         if emailUser in tmpstatus_detail[x]['email']:
#                             if tmpstatus_detail[x]['step_status_code'] == 'W':
#                                 arr_email_document.append(emailUser)
#                                 tmpdocument_status = tmpstatus_detail[x]['step_status_code']
#                                 break
#                             else:
#                                 tmpdocument_status = tmpstatus_detail[x]['step_status_code']
#         if tmpdocument_status == 'Z':
#             res_status_file_string = 'อยู่ในช่วงดำเนินการ'
#         elif tmpdocument_status == 'W':
#             res_status_file_string = 'รอคุณอนุมัติ'
#         elif tmpdocument_status == 'N':
#             res_status_file_string = 'กำลังดำเนินการ'
#         elif tmpdocument_status == 'R':
#             res_status_file_string = 'เอกสารที่ส่งคืนแก้ไข'
#         else:
#             res_status_file_string = 'เอกสารสมบูรณ์'
#         tmp_sign_page_options = tmpdata['sign_page_options']
#         tmp_document_type = tmpdata['documentType']
#         tmp_options_page = []
#         if tmpdata['options_page'] != None:
#             if tmpdata['options_page'] != '':
#             # print(tmp_dict_json['options_page'],tmp_document_id)
#                 tmp_options_page = [eval(tmpdata['options_page'])]
#         else:
#             tmp_options_page = []
#         if len(tmp_options_page) != 0:
#             # print(tmp_options_page[0]['group_detail'])
#             tmp_status_group = False
#             if status_groupid == True:
#                 if len(tmp_options_page) != 0:
#                     if 'group_detail' in tmp_options_page[0]:
#                         tmp_group_detail = tmp_options_page[0]['group_detail']
#                         if 'group_status' in tmp_group_detail:
#                             if tmp_group_detail['group_status'] == True:
#                                 tmp_status_group = True
#                                 tmpstepnum = tmp_group_detail['step_num']
#         if tmpdata['documentJson'] != None:
#             documentJson_result = eval(tmpdata['documentJson'])
#             documentName = documentJson_result['document_name']
#             documentType = documentJson_result['document_type']
#         else:
#             documentName = None
#             documentType = None
#         if tmpdata['urgent_type'] != None:
#             documentUrgentType = tmpdata['urgent_type']
#             if documentUrgentType == 'I':
#                 documentUrgentString = 'ด่วนมาก'
#             elif documentUrgentType == 'U':
#                 documentUrgentString = 'ด่วน'
#             elif documentUrgentType == 'M':
#                 documentUrgentString = 'ปกติ'
#         tmp_biz_info = None
#         tmprole_name = None
#         tmpdept_name = None
#         tmprole_level = None
#         if tmpdata['biz_info'] != None:
#             if tmpdata['biz_info'] != 'None':
#                 if tmpdata['biz_info'] != '':
#                     eval_biz_info = json.dumps(tmpdata['biz_info'])
#                     eval_biz_info = json.loads(eval_biz_info)
#                     eval_biz_info = eval(eval_biz_info)
#                     if 'role_name' in eval_biz_info:
#                         tmprole_name = eval_biz_info['role_name']
#                     if 'dept_name' in eval_biz_info:
#                         tmpdept_name = eval_biz_info['dept_name']
#                     if 'role_level' in eval_biz_info:
#                         tmprole_level = eval_biz_info['role_level']
#                     if 'dept_name' in eval_biz_info:            
#                         tmp_biz_info = {
#                             'tax_id':eval_biz_info['id_card_num'],
#                             'role_name' : tmprole_name,
#                             'dept_name' : tmpdept_name,
#                             'role_level' : tmprole_level             
#                         }                                
#                     elif 'dept_name' not in eval_biz_info:
#                         tmp_biz_info = {
#                             'tax_id':eval_biz_info['id_card_num'],
#                             'role_name' : tmprole_name,
#                             'dept_name' : [],
#                             'role_level' : tmprole_level               
#                         }
#         dateTime_String = tmp_send_time
#         th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
#         ts = int(time.time())
#         date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
#         year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
#         datetime_display = int(dateTime_String.timestamp())
#         date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
#         yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
#         time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
#         old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
#         if date_time_today == date_time_db:
#             date_display_show = time_show_db
#         else:
#             if year_today == yar_db:
#                 date_display_show = convert_datetime_TH_2_display(datetime_display)
#             else:
#                 date_display_show = old_year

#         if tmp_status_group == True:
#             for ui in range(len(tmpstepnum)):
#                 intstepnum = tmpstepnum[ui] - 1
#                 try:
#                     for w in range(len(email_step_sum_w[intstepnum])):
#                         tmp_req_email.append(email_step_sum_w[intstepnum][w])
#                 except Exception as e:
#                     tmp_req_email = []
#         if tmpdocument_status == status:       
#             if len(list_sum) < limit:
#                 sum_row_tooffset = x+1
#                 list_sum.append({
#                     'group_email':tmp_req_email,
#                     'group_id':None,
#                     'group_status':tmp_status_group,
#                     'sidCode':tmp_sicode,
#                     'document_name':documentName,
#                     'document_type':tmp_document_type,
#                     'document_urgent':documentUrgentType,
#                     'document_urgent_string':documentUrgentString,
#                     'dateTime_String':str(dateTime_String).split('+')[0],
#                     'dateTime_String_TH_1':th_dateTime_2,
#                     'dateTime_display':date_display_show,
#                     'document_id':tmp_document_id,
#                     'stamp_all':tmp_sign_page_options,
#                     'options_page_document':tmp_options_page,
#                     'max_step':tmpstepmax,
#                     'step_now':tmpstepnow,
#                     'date_String':str(dateTime_String).split(' ')[0],
#                     'time_String':str(dateTime_String).split(' ')[1].split('+')[0],
#                     'status_file_code':tmpdocument_status,
#                     'status_file_string':res_status_file_string,
#                     'dateTime':int(dateTime_String.timestamp()),
#                     'tracking_id':tmp_tracking_id,
#                     'sender_name':tmp_sender_name,
#                     'sender_email':tmp_sender_email,
#                     'file_name':tmp_file_name,
#                     'document_business':tmp_biz_info,
#                     'group':status_groupid,
#                 })
#             else:
#                 pass
#         else:
#             pass 
#     return list_sum,sum_row_tooffset



def recursive_sender_status_new_v1(username,emailUser,limit,offset,status,list_sum,sum_row_tooffset,document_type,tax_id,group_status,tmptimeapprove=None):
        username = username
        emailUser = emailUser
        status = status
        document_type = document_type
        tmptimeapprove = tmptimeapprove
        if tmptimeapprove != None:
            tmptimeapprove = tmptimeapprove
        if limit != '':
            limit = int(limit)
        else:
            limit = ''
        if offset != '':
            offset = int(offset)
        else:
            offset = ''
        status = status
        list_sum = list_sum
        search_tax_id = "%'{}'%".format(tax_id)
        if tmptimeapprove == True:
            print ('TEMP_TRUEEEEE')
            if document_type != '':
                if tax_id != '':
                    query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info,paper_lessdatastep.update_time)\
                        .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                        .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                        .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                        .filter(paper_lesssender.document_status=='N')\
                        .filter(paper_lessdocument.documentType==document_type)\
                        .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
                        .order_by(desc(paper_lessdatastep.update_time))\
                        .limit(limit)\
                        .offset(offset)\
                        .all()
                    if group_status == "true":
                        query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info,paper_lessdatastep.update_time)\
                            .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                            .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                            .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                            .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id==[]))\
                            .filter(paper_lesssender.document_status=='N')\
                            .filter(paper_lessdocument.documentType==document_type)\
                            .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
                            .order_by(desc(paper_lessdatastep.update_time))\
                            .limit(limit)\
                            .offset(offset)\
                            .all()
                else:
                    query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info,paper_lessdatastep.update_time)\
                        .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                        .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                        .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                        .filter(paper_lesssender.document_status=='N')\
                        .filter(paper_lessdocument.documentType==document_type)\
                        .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
                        .order_by(desc(paper_lessdatastep.update_time))\
                        .limit(limit)\
                        .offset(offset)\
                        .all()
                    if group_status == "true":
                        query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info,paper_lessdatastep.update_time)\
                            .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                            .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                            .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                            .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id==[]))\
                            .filter(paper_lesssender.document_status=='N')\
                            .filter(paper_lessdocument.documentType==document_type)\
                            .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
                            .order_by(desc(paper_lessdatastep.update_time))\
                            .limit(limit)\
                            .offset(offset)\
                            .all()
            else:
                if tax_id != '':
                    query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info,paper_lessdatastep.update_time)\
                        .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                        .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                        .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                        .filter(paper_lesssender.document_status=='N')\
                        .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
                        .order_by(desc(paper_lessdatastep.update_time))\
                        .limit(limit)\
                        .offset(offset)\
                        .all()
                    if group_status == "true":
                        query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info,paper_lessdatastep.update_time)\
                            .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                            .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                            .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                            .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id==[]))\
                            .filter(paper_lesssender.document_status=='N')\
                            .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
                            .order_by(desc(paper_lessdatastep.update_time))\
                            .limit(limit)\
                            .offset(offset)\
                            .all()
                else:
                    query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info,paper_lessdatastep.update_time)\
                        .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                        .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                        .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                        .filter(paper_lesssender.document_status=='N')\
                        .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
                        .order_by(desc(paper_lessdatastep.update_time))\
                        .limit(limit)\
                        .offset(offset)\
                        .all()
                    if group_status == "true":
                        query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info,paper_lessdatastep.update_time)\
                            .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                            .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                            .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                            .filter(paper_lesssender.document_status=='N')\
                            .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id==[]))\
                            .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
                            .order_by(desc(paper_lessdatastep.update_time))\
                            .limit(limit)\
                            .offset(offset)\
                            .all()
        else:
            if document_type != '':
                if tax_id != '':
                    query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
                        .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                        .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                        .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                        .filter(paper_lesssender.document_status=='N')\
                        .filter(paper_lessdocument.documentType==document_type)\
                        .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
                        .order_by(desc(paper_lesssender.send_time))\
                        .limit(limit)\
                        .offset(offset)\
                        .all()
                    if group_status == "true":
                        query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
                            .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                            .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                            .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                            .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id==[]))\
                            .filter(paper_lesssender.document_status=='N')\
                            .filter(paper_lessdocument.documentType==document_type)\
                            .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
                            .order_by(desc(paper_lesssender.send_time))\
                            .limit(limit)\
                            .offset(offset)\
                            .all()
                else:
                    query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
                        .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                        .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                        .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                        .filter(paper_lesssender.document_status=='N')\
                        .filter(paper_lessdocument.documentType==document_type)\
                        .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
                        .order_by(desc(paper_lesssender.send_time))\
                        .limit(limit)\
                        .offset(offset)\
                        .all()
                    if group_status == "true":
                        query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
                            .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                            .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                            .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                            .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id==[]))\
                            .filter(paper_lesssender.document_status=='N')\
                            .filter(paper_lessdocument.documentType==document_type)\
                            .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
                            .order_by(desc(paper_lesssender.send_time))\
                            .limit(limit)\
                            .offset(offset)\
                            .all()
            else:
                if tax_id != '':
                    query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
                        .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                        .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                        .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                        .filter(paper_lesssender.document_status=='N')\
                        .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
                        .order_by(desc(paper_lesssender.send_time))\
                        .limit(limit)\
                        .offset(offset)\
                        .all()
                    if group_status == "true":
                        query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
                            .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                            .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                            .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                            .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id==[]))\
                            .filter(paper_lesssender.document_status=='N')\
                            .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
                            .order_by(desc(paper_lesssender.send_time))\
                            .limit(limit)\
                            .offset(offset)\
                            .all()
                else:
                    query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
                        .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                        .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                        .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                        .filter(paper_lesssender.document_status=='N')\
                        .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
                        .order_by(desc(paper_lesssender.send_time))\
                        .limit(limit)\
                        .offset(offset)\
                        .all()
                    if group_status == "true":
                        query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
                            .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
                            .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
                            .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
                            .filter(paper_lesssender.document_status=='N')\
                            .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id==[]))\
                            .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
                            .order_by(desc(paper_lesssender.send_time))\
                            .limit(limit)\
                            .offset(offset)\
                            .all() 
        for u in range(len(query_temp)):
            arr_email_document = []
            tmp_req_email = []
            email_step_sum_w = []
            for z in range(len(query_temp[u])):
                if z == 0:
                    tmp_dict_json = query_temp[u][z].__dict__
                    if '_sa_instance_state' in tmp_dict_json:
                        tmp_dict_json['_sa_instance_state'] = str(tmp_dict_json['_sa_instance_state']) 
                    tmp_sicode = tmp_dict_json['step_data_sid']
                    # tmp_sid_code_list.append(tmp_sicode)
                    tmp_send_time = tmp_dict_json['send_time']
                    tmp_document_id = tmp_dict_json['doc_id']
                    tmp_tracking_id = tmp_dict_json['tracking_id']
                    tmp_sender_name = tmp_dict_json['sender_name']
                    tmp_sender_email = tmp_dict_json['sender_email']
                    tmp_file_name = tmp_dict_json['file_name']
                    tmp_groupid = tmp_dict_json['group_id']
                    email_step_sum = tmp_dict_json['recipient_email']
                    sender_name_eng = find_name_surename_by_username(tmp_sender_email)
                    if email_step_sum != None:
                        email_step_sum = eval(email_step_sum)
                    # print(email_step_sum)
                    tmpstatus_detail = tmp_dict_json['status_details']
                    tmpdocument_status = tmp_dict_json['document_status']
                    tmpstepnow = tmp_dict_json['stepnow']
                    status_groupid = False
                    if tmp_groupid != None:
                        tmp_groupid = eval(tmp_groupid)
                        if len(tmp_groupid) != 0:
                            status_groupid = True
                    if tmpstepnow != None:
                        tmpstepnow = int(tmpstepnow)
                    tmpstepmax = tmp_dict_json['stepmax']
                    if tmpstepmax != None:
                        tmpstepmax = int(tmpstepmax)
                    if tmpstatus_detail != None:
                        tmpstatus_detail = eval(tmpstatus_detail)                            
                        for z in range(len(tmpstatus_detail)):
                            email_step_sum_w.append(tmpstatus_detail[z]['email'])

                        if tmpdocument_status == 'N':
                            for x in range(len(tmpstatus_detail)):
                                # print(tmp_sicode)
                                # print(tmpstatus_detail[x])
                                # email_step_sum_w.append(tmpstatus_detail[x]['email'])
                                if emailUser not in arr_email_document:
                                    if emailUser in tmpstatus_detail[x]['email']:
                                        if tmpstatus_detail[x]['step_status_code'] == 'W':
                                            arr_email_document.append(emailUser)
                                            tmpdocument_status = tmpstatus_detail[x]['step_status_code']
                                            break
                                        else:
                                            tmpdocument_status = tmpstatus_detail[x]['step_status_code']
                    # print(email_step_sum_w)
                    if tmpdocument_status == 'Z':
                        res_status_file_string = 'อยู่ในช่วงดำเนินการ'
                    elif tmpdocument_status == 'W':
                        res_status_file_string = 'รอคุณอนุมัติ'
                    elif tmpdocument_status == 'N':
                        res_status_file_string = 'กำลังดำเนินการ'
                    elif tmpdocument_status == 'R':
                        res_status_file_string = 'เอกสารที่ส่งคืนแก้ไข'
                    else:
                        res_status_file_string = ''
                                        # else:

                    # print(tmpstatus_detail)
                if z == 1:
                    tmp_document_type = None
                    tmp_dict_json = query_temp[u][z].__dict__
                    if '_sa_instance_state' in tmp_dict_json:
                        tmp_dict_json['_sa_instance_state'] = str(tmp_dict_json['_sa_instance_state'])
                    tmp_sign_page_options = tmp_dict_json['sign_page_options']
                    tmp_document_type = tmp_dict_json['documentType']
                    tmp_options_page = []
                    if tmp_dict_json['options_page'] != None:
                        if tmp_dict_json['options_page'] != '':
                        # print(tmp_dict_json['options_page'],tmp_document_id)
                            tmp_options_page = [eval(tmp_dict_json['options_page'])]
                    else:
                        tmp_options_page = []
                    tmp_status_group = False
                    if len(tmp_options_page) != 0:
                        # print(tmp_options_page[0]['group_detail'])
                        tmp_status_group = False
                        if status_groupid == True:
                            if len(tmp_options_page) != 0:
                                if 'group_detail' in tmp_options_page[0]:
                                    tmp_group_detail = tmp_options_page[0]['group_detail']
                                    if 'group_status' in tmp_group_detail:
                                        if tmp_group_detail['group_status'] == True:
                                            tmp_status_group = True
                                            tmpstepnum = tmp_group_detail['step_num']
                                    # if 'step_num' in tmp_group_detail:
                                    #     tmp_status_group = True
                                    #     tmp_group_stepnum = tmp_group_detail['step_num']
                        # if 'group_detail' in tmp_options_page[0]:
                        #     if 'group_status' in tmp_options_page[0]['group_detail']:
                        #         tmpgroupdetails = tmp_options_page[0]['group_detail']
                        #         if tmpgroupdetails['group_status'] == True:
                        #             tmpstepnum = tmpgroupdetails['step_num']
                                    # print(tmpstepnum)
                    if tmp_dict_json['documentJson'] != None:
                        documentJson_result = eval(tmp_dict_json['documentJson'])
                        documentName = documentJson_result['document_name']
                        documentType = documentJson_result['document_type']
                    else:
                        documentName = None
                        documentType = None
                    if tmp_dict_json['urgent_type'] != None:
                        documentUrgentType = tmp_dict_json['urgent_type']
                        if documentUrgentType == 'I':
                            documentUrgentString = 'ด่วนมาก'
                        elif documentUrgentType == 'U':
                            documentUrgentString = 'ด่วน'
                        elif documentUrgentType == 'M':
                            documentUrgentString = 'ปกติ'
                tmp_biz_info = None
                if z == 2:
                    if query_temp[u][z] != None:
                        if query_temp[u][z] != 'None':
                            
                            # eval_biz_info = json.dumps(tmp_dict_json['biz_info'])
                            eval_biz_info = json.dumps(query_temp[u][z])
                            eval_biz_info = json.loads(eval_biz_info)
                            eval_biz_info = eval(eval_biz_info)
                            if 'role_name' in eval_biz_info:
                                tmprole_name = eval_biz_info['role_name']
                            if 'role_level' in eval_biz_info:
                                tmprole_level = eval_biz_info['role_level']
                            if 'dept_name' in eval_biz_info:
                                tmpdept_name = eval_biz_info['dept_name']
                            if 'dept_name' in eval_biz_info:                        
                                tmp_biz_info = {
                                    'tax_id':eval_biz_info['id_card_num'],
                                    'role_name' : tmprole_name,
                                    'dept_name' : tmpdept_name,
                                    'role_level' : tmprole_level            
                                }                                
                            elif 'dept_name' not in eval_biz_info:
                                tmp_biz_info = {
                                    'tax_id':eval_biz_info['id_card_num'],
                                    'role_name' : tmprole_name,
                                    'dept_name' : [],
                                    'role_level' : tmprole_level            
                                }

                if z == 3:
                    tmptime_update = (query_temp[u][z])
                    tmptime_update_timestamp = int(tmptime_update.timestamp())
                    tmptime_update_string = str(tmptime_update).split('+')[0]
                    th_dateTime_2_last = convert_datetime_TH_2(int(tmptime_update.timestamp()))
                    # print(th_dateTime_2_last,tmptime_update)
                    ts = int(time.time())
                    date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
                    datetime_display_update = int(tmptime_update.timestamp())
                    date_time_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%Y-%m-%d')
                    yar_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%Y')
                    time_show_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%H:%M')
                    old_year = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%d/%m/%Y')
                    if date_time_today == date_time_db:
                        date_last_display_show = time_show_db
                    else:
                        if year_today == yar_db:
                            date_last_display_show = convert_datetime_TH_2_display(datetime_display_update)
                        else:
                            date_last_display_show = old_year

                dateTime_String = tmp_send_time
                th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
                ts = int(time.time())
                date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
                datetime_display = int(dateTime_String.timestamp())
                date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
                yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
                time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
                old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
                if date_time_today == date_time_db:
                    date_display_show = time_show_db
                else:
                    if year_today == yar_db:
                        date_display_show = convert_datetime_TH_2_display(datetime_display)
                    else:
                        date_display_show = old_year
                # print(email_step_sum_w)
            if tmp_status_group == True:
                for ui in range(len(tmpstepnum)):
                    intstepnum = tmpstepnum[ui] - 1
                    print(intstepnum,email_step_sum_w,tmp_sicode)
                    try:
                        for w in range(len(email_step_sum_w[intstepnum])):
                            tmp_req_email.append(email_step_sum_w[intstepnum][w])    
                    except Exception as e:
                        print(str(e))
                
              
            if tmpdocument_status == status:       
                if len(list_sum) < limit:
                    # sum_row_tooffset = sum_row_tooffset + 1 
                    # 100
                    sum_row_tooffset = u+1
                    list_sum.append({
                        'group_email':tmp_req_email,
                        'group_id':None,
                        'group_status':tmp_status_group,
                        'sidCode':tmp_sicode,
                        'document_name':documentName,
                        'document_type':tmp_document_type,
                        'document_urgent':documentUrgentType,
                        'document_urgent_string':documentUrgentString,
                        'dateTime_String':str(dateTime_String).split('+')[0],
                        'dateTime_String_TH_1':th_dateTime_2,
                        'dateTime_display':date_display_show,
                        'document_id':tmp_document_id,
                        'stamp_all':tmp_sign_page_options,
                        'options_page_document':tmp_options_page,
                        'max_step':tmpstepmax,
                        'step_now':tmpstepnow,
                        # 'dateTime_String_TH_2':th_dateTime_2,
                        'date_String':str(dateTime_String).split(' ')[0],
                        'time_String':str(dateTime_String).split(' ')[1].split('+')[0],
                        'status_file_code':tmpdocument_status,
                        'status_file_string':res_status_file_string,
                        'dateTime':int(dateTime_String.timestamp()),
                        'tracking_id':tmp_tracking_id,
                        'sender_name':tmp_sender_name,
                        'sender_email':tmp_sender_email,
                        'file_name':tmp_file_name,
                        'document_business':tmp_biz_info,
                        'update_last':tmptime_update,
                        'update_last_String_TH_1':th_dateTime_2_last,
                        'update_last_display':date_last_display_show,
                        'update_last_String':tmptime_update_string,
                        'update_last_TimeStamp':tmptime_update_timestamp,
                        'sender_name_eng' : sender_name_eng
                    })
                else:
                    # sum_row_tooffset = sum_row_tooffset + 1
                    # 13
                    pass
            else:
                # sum_row_tooffset = sum_row_tooffset + 1 
                # 32
                pass 
            # sum_row_tooffset = sum_row_tooffset + 1 
        list_sum = sorted(list_sum, key=lambda k: k['dateTime'], reverse=True)
        if tmptimeapprove == True:
            list_sum = sorted(list_sum, key=lambda k: k['update_last_TimeStamp'], reverse=True)
        return list_sum,sum_row_tooffset


# def recursive_sender_status_new_v1(username,emailUser,limit,offset,status,list_sum,sum_row_tooffset,document_type,tax_id,group_status):
#         username = username
#         emailUser = emailUser
#         status = status
#         document_type = document_type
#         if limit != '':
#             limit = int(limit)
#         else:
#             limit = ''
#         if offset != '':
#             offset = int(offset)
#         else:
#             offset = ''
#         status = status
#         list_sum = list_sum
#         search_tax_id = "%'{}'%".format(tax_id)
#         if document_type != '':
#             if tax_id != '':
#                 query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#                     .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#                     .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#                     .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
#                     .filter(paper_lesssender.document_status=='N')\
#                     .filter(paper_lessdocument.documentType==document_type)\
#                     .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
#                     .order_by(desc(paper_lesssender.send_time))\
#                     .limit(limit)\
#                     .offset(offset)\
#                     .all()
#                 if group_status == "true":
#                     query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#                         .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#                         .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#                         .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
#                         .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id==[]))\
#                         .filter(paper_lesssender.document_status=='N')\
#                         .filter(paper_lessdocument.documentType==document_type)\
#                         .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
#                         .order_by(desc(paper_lesssender.send_time))\
#                         .limit(limit)\
#                         .offset(offset)\
#                         .all()
#             else:
#                 query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#                     .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#                     .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#                     .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
#                     .filter(paper_lesssender.document_status=='N')\
#                     .filter(paper_lessdocument.documentType==document_type)\
#                     .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
#                     .order_by(desc(paper_lesssender.send_time))\
#                     .limit(limit)\
#                     .offset(offset)\
#                     .all()
#                 if group_status == "true":
#                     query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#                         .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#                         .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#                         .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
#                         .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id==[]))\
#                         .filter(paper_lesssender.document_status=='N')\
#                         .filter(paper_lessdocument.documentType==document_type)\
#                         .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
#                         .order_by(desc(paper_lesssender.send_time))\
#                         .limit(limit)\
#                         .offset(offset)\
#                         .all()
#         else:
#             if tax_id != '':
#                 query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#                     .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#                     .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#                     .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
#                     .filter(paper_lesssender.document_status=='N')\
#                     .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
#                     .order_by(desc(paper_lesssender.send_time))\
#                     .limit(limit)\
#                     .offset(offset)\
#                     .all()
#                 if group_status == "true":
#                     query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#                         .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#                         .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#                         .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
#                         .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id==[]))\
#                         .filter(paper_lesssender.document_status=='N')\
#                         .filter(paper_lessdatastep.biz_info.like(search_tax_id))\
#                         .order_by(desc(paper_lesssender.send_time))\
#                         .limit(limit)\
#                         .offset(offset)\
#                         .all()
#             else:
#                 query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#                     .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#                     .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#                     .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
#                     .filter(paper_lesssender.document_status=='N')\
#                     .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
#                     .order_by(desc(paper_lesssender.send_time))\
#                     .limit(limit)\
#                     .offset(offset)\
#                     .all()
#                 if group_status == "true":
#                     query_temp = db.session.query(paper_lesssender,paper_lessdocument,paper_lessdatastep.biz_info)\
#                         .join(paper_lessdocument, paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
#                         .join(paper_lessdatastep, paper_lessdatastep.sid==paper_lesssender.step_data_sid)\
#                         .filter(paper_lesssender.status=='ACTIVE').filter(paper_lesssender.send_user==username)\
#                         .filter(paper_lesssender.document_status=='N')\
#                         .filter(or_(paper_lesssender.group_id==None,paper_lesssender.group_id==[]))\
#                         .filter(or_(paper_lessdatastep.biz_info=='None',paper_lessdatastep.biz_info==''))\
#                         .order_by(desc(paper_lesssender.send_time))\
#                         .limit(limit)\
#                         .offset(offset)\
#                         .all()
#         for u in range(len(query_temp)):
#             arr_email_document = []
#             tmp_req_email = []
#             email_step_sum_w = []
#             for z in range(len(query_temp[u])):
#                 if z == 0:
#                     tmp_dict_json = query_temp[u][z].__dict__
#                     if '_sa_instance_state' in tmp_dict_json:
#                         tmp_dict_json['_sa_instance_state'] = str(tmp_dict_json['_sa_instance_state']) 
#                     tmp_sicode = tmp_dict_json['step_data_sid']
#                     # tmp_sid_code_list.append(tmp_sicode)
#                     tmp_send_time = tmp_dict_json['send_time']
#                     tmp_document_id = tmp_dict_json['doc_id']
#                     tmp_tracking_id = tmp_dict_json['tracking_id']
#                     tmp_sender_name = tmp_dict_json['sender_name']
#                     tmp_sender_email = tmp_dict_json['sender_email']
#                     tmp_file_name = tmp_dict_json['file_name']
#                     tmp_groupid = tmp_dict_json['group_id']
#                     email_step_sum = tmp_dict_json['recipient_email']
#                     if email_step_sum != None:
#                         email_step_sum = eval(email_step_sum)
#                     # print(email_step_sum)
#                     tmpstatus_detail = tmp_dict_json['status_details']
#                     tmpdocument_status = tmp_dict_json['document_status']
#                     tmpstepnow = tmp_dict_json['stepnow']
#                     status_groupid = False
#                     if tmp_groupid != None:
#                         tmp_groupid = eval(tmp_groupid)
#                         if len(tmp_groupid) != 0:
#                             status_groupid = True
#                     if tmpstepnow != None:
#                         tmpstepnow = int(tmpstepnow)
#                     tmpstepmax = tmp_dict_json['stepmax']
#                     if tmpstepmax != None:
#                         tmpstepmax = int(tmpstepmax)
#                     if tmpstatus_detail != None:
#                         tmpstatus_detail = eval(tmpstatus_detail)                            
#                         for z in range(len(tmpstatus_detail)):
#                             email_step_sum_w.append(tmpstatus_detail[z]['email'])

#                         if tmpdocument_status == 'N':
#                             for x in range(len(tmpstatus_detail)):
#                                 # print(tmp_sicode)
#                                 # print(tmpstatus_detail[x])
#                                 # email_step_sum_w.append(tmpstatus_detail[x]['email'])
#                                 if emailUser not in arr_email_document:
#                                     if emailUser in tmpstatus_detail[x]['email']:
#                                         if tmpstatus_detail[x]['step_status_code'] == 'W':
#                                             arr_email_document.append(emailUser)
#                                             tmpdocument_status = tmpstatus_detail[x]['step_status_code']
#                                             break
#                                         else:
#                                             tmpdocument_status = tmpstatus_detail[x]['step_status_code']
#                     # print(email_step_sum_w)
#                     if tmpdocument_status == 'Z':
#                         res_status_file_string = 'อยู่ในช่วงดำเนินการ'
#                     elif tmpdocument_status == 'W':
#                         res_status_file_string = 'รอคุณอนุมัติ'
#                     elif tmpdocument_status == 'N':
#                         res_status_file_string = 'กำลังดำเนินการ'
#                     elif tmpdocument_status == 'R':
#                         res_status_file_string = 'เอกสารที่ส่งคืนแก้ไข'
#                     else:
#                         res_status_file_string = ''
#                                         # else:

#                     # print(tmpstatus_detail)
#                 if z == 1:
#                     tmp_document_type = None
#                     tmp_dict_json = query_temp[u][z].__dict__
#                     if '_sa_instance_state' in tmp_dict_json:
#                         tmp_dict_json['_sa_instance_state'] = str(tmp_dict_json['_sa_instance_state'])
#                     tmp_sign_page_options = tmp_dict_json['sign_page_options']
#                     tmp_document_type = tmp_dict_json['documentType']
#                     tmp_options_page = []
#                     if tmp_dict_json['options_page'] != None:
#                         if tmp_dict_json['options_page'] != '':
#                         # print(tmp_dict_json['options_page'],tmp_document_id)
#                             tmp_options_page = [eval(tmp_dict_json['options_page'])]
#                     else:
#                         tmp_options_page = []
#                     tmp_status_group = False
#                     if len(tmp_options_page) != 0:
#                         # print(tmp_options_page[0]['group_detail'])
#                         tmp_status_group = False
#                         if status_groupid == True:
#                             if len(tmp_options_page) != 0:
#                                 if 'group_detail' in tmp_options_page[0]:
#                                     tmp_group_detail = tmp_options_page[0]['group_detail']
#                                     if 'group_status' in tmp_group_detail:
#                                         if tmp_group_detail['group_status'] == True:
#                                             tmp_status_group = True
#                                             tmpstepnum = tmp_group_detail['step_num']
#                                     # if 'step_num' in tmp_group_detail:
#                                     #     tmp_status_group = True
#                                     #     tmp_group_stepnum = tmp_group_detail['step_num']
#                         # if 'group_detail' in tmp_options_page[0]:
#                         #     if 'group_status' in tmp_options_page[0]['group_detail']:
#                         #         tmpgroupdetails = tmp_options_page[0]['group_detail']
#                         #         if tmpgroupdetails['group_status'] == True:
#                         #             tmpstepnum = tmpgroupdetails['step_num']
#                                     # print(tmpstepnum)
#                     if tmp_dict_json['documentJson'] != None:
#                         documentJson_result = eval(tmp_dict_json['documentJson'])
#                         documentName = documentJson_result['document_name']
#                         documentType = documentJson_result['document_type']
#                     else:
#                         documentName = None
#                         documentType = None
#                     if tmp_dict_json['urgent_type'] != None:
#                         documentUrgentType = tmp_dict_json['urgent_type']
#                         if documentUrgentType == 'I':
#                             documentUrgentString = 'ด่วนมาก'
#                         elif documentUrgentType == 'U':
#                             documentUrgentString = 'ด่วน'
#                         elif documentUrgentType == 'M':
#                             documentUrgentString = 'ปกติ'
#                 tmp_biz_info = None
#                 if z == 2:
#                     if query_temp[u][z] != None:
#                         if query_temp[u][z] != 'None':
#                             eval_biz_info = json.dumps(query_temp[u][z])
#                             eval_biz_info = json.loads(eval_biz_info)
#                             eval_biz_info = eval(eval_biz_info)
#                             if 'role_name' in eval_biz_info:
#                                 tmprole_name = eval_biz_info['role_name']
#                             if 'role_level' in eval_biz_info:
#                                 tmprole_level = eval_biz_info['role_level']
#                             if 'dept_name' in eval_biz_info:
#                                 tmpdept_name = eval_biz_info['dept_name']
#                             if 'dept_name' in eval_biz_info:                        
#                                 tmp_biz_info = {
#                                     'tax_id':eval_biz_info['id_card_num'],
#                                     'role_name' : tmprole_name,
#                                     'dept_name' : tmpdept_name,
#                                     'role_level' : tmprole_level            
#                                 }                                
#                             elif 'dept_name' not in eval_biz_info:
#                                 tmp_biz_info = {
#                                     'tax_id':eval_biz_info['id_card_num'],
#                                     'role_name' : tmprole_name,
#                                     'dept_name' : [],
#                                     'role_level' : tmprole_level            
#                                 }
                    
#                 dateTime_String = tmp_send_time
#                 th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
#                 ts = int(time.time())
#                 date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
#                 year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
#                 datetime_display = int(dateTime_String.timestamp())
#                 date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
#                 yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
#                 time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
#                 old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
#                 if date_time_today == date_time_db:
#                     date_display_show = time_show_db
#                 else:
#                     if year_today == yar_db:
#                         date_display_show = convert_datetime_TH_2_display(datetime_display)
#                     else:
#                         date_display_show = old_year
#                 # print(email_step_sum_w)
#             if tmp_status_group == True:
#                 for ui in range(len(tmpstepnum)):
#                     intstepnum = tmpstepnum[ui] - 1
#                     print(intstepnum,email_step_sum_w,tmp_sicode)
#                     try:
#                         for w in range(len(email_step_sum_w[intstepnum])):
#                             tmp_req_email.append(email_step_sum_w[intstepnum][w])    
#                     except Exception as e:
#                         print(str(e))
                
              
#             if tmpdocument_status == status:       
#                 if len(list_sum) < limit:
#                     # sum_row_tooffset = sum_row_tooffset + 1 
#                     # 100
#                     sum_row_tooffset = u+1
#                     list_sum.append({
#                         'group_email':tmp_req_email,
#                         'group_id':None,
#                         'group_status':tmp_status_group,
#                         'sidCode':tmp_sicode,
#                         'document_name':documentName,
#                         'document_type':tmp_document_type,
#                         'document_urgent':documentUrgentType,
#                         'document_urgent_string':documentUrgentString,
#                         'dateTime_String':str(dateTime_String).split('+')[0],
#                         'dateTime_String_TH_1':th_dateTime_2,
#                         'dateTime_display':date_display_show,
#                         'document_id':tmp_document_id,
#                         'stamp_all':tmp_sign_page_options,
#                         'options_page_document':tmp_options_page,
#                         'max_step':tmpstepmax,
#                         'step_now':tmpstepnow,
#                         # 'dateTime_String_TH_2':th_dateTime_2,
#                         'date_String':str(dateTime_String).split(' ')[0],
#                         'time_String':str(dateTime_String).split(' ')[1].split('+')[0],
#                         'status_file_code':tmpdocument_status,
#                         'status_file_string':res_status_file_string,
#                         'dateTime':int(dateTime_String.timestamp()),
#                         'tracking_id':tmp_tracking_id,
#                         'sender_name':tmp_sender_name,
#                         'sender_email':tmp_sender_email,
#                         'file_name':tmp_file_name,
#                         'document_business':tmp_biz_info
#                     })
#                 else:
#                     # sum_row_tooffset = sum_row_tooffset + 1
#                     # 13
#                     pass
#             else:
#                 # sum_row_tooffset = sum_row_tooffset + 1 
#                 # 32
#                 pass 
#             # sum_row_tooffset = sum_row_tooffset + 1 
#         return list_sum,sum_row_tooffset

class select_admin_3:   
    def select_show_businessConfig_v1(self,level_admin,tax_id):
        self.tax_id = tax_id
        self.level_admin = level_admin
        data = None
        try:
            if self.level_admin == 0:
                with slave.connect() as connection:
                    result = connection.execute(text('''SELECT "id","tax_id","theme_color","path_logo","datetime","status",\
                    "transactionMax","storageMax","create_date","update_date" FROM "tb_bizPaperless" WHERE "tax_id"=:tax_id '''),tax_id=self.tax_id)
                    connection.close()
            elif self.level_admin == 1:
                with slave.connect() as connection:
                    result = connection.execute(text('''SELECT "id","tax_id","theme_color","path_logo","create_date","update_date" FROM "tb_bizPaperless" WHERE "tax_id"=:tax_id '''),tax_id=self.tax_id)
                    connection.close()
            tmp_query = [dict(row) for row in result]
            if len(tmp_query) != 0:
                for x in range(len(tmp_query)):
                    data = tmp_query[x]
                    if data['update_date'] != None:
                        data['update_date'] = str(data['update_date'])
                    if data['create_date'] != None:
                        data['create_date'] = str(data['create_date'])
                    if data['datetime'] != None:
                        data['datetime'] = str(data['datetime'])
                return {'result':'OK','messageText':data}
            else:
                return {'result':'ER','messageText':None}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def select_document_tologline_v1(self):
        try:
            ts = int(time.time())
            start_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y 00:00:00')
            end_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y 23:59:59')
            print(start_time,end_time)
            self.start_time = start_time
            self.end_time = end_time
            arrtemp_template = []
            with slave.connect() as connection:
                result = connection.execute(text('''SELECT COUNT("id") FROM "tb_step_data" WHERE "upload_time">=:start_time AND "upload_time"<=:end_time '''),start_time=self.start_time,end_time=self.end_time)
                connection.close()
            tmp_query = [dict(row) for row in result]
            # print(tmp_query)
            if len(tmp_query) != 0:
                for x in range(len(tmp_query)):
                    tmpcount_document = tmp_query[x]['count']
                return {'result':'OK','messageText':tmpcount_document}
            else:
                return {'result':'ER','messageText':None}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def select_taxid_admin_v1(self):
        try:
            arrtemp_template = []
            with slave.connect() as connection:
                result = connection.execute(text('''SELECT "transactionId","bizTax","bizInfoJson","bizRole" FROM "tb_bizProfile" '''))
                connection.close()
            tmp_query = [dict(row) for row in result]
            if len(tmp_query) != 0 :
                for j in range(len(tmp_query)):
                    if 'bizTax' in tmp_query[j]:
                        tmpbizTax = tmp_query[j]
                        arrtemp_template.append(tmpbizTax)
                        # print(tmp_query[j])
                return {'result':'OK','messageText':arrtemp_template}
            else:
                return {'result':'ER','messageText':None}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}
    
    def select_stepdata_admin_v1(self,taxid):
        try:
            ts = int(time.time())
            start_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y 00:00:00')
            end_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y 23:59:59')
            print(start_time,end_time)
            self.taxid = taxid
            self.start_time = start_time
            self.end_time = end_time
            arrtemp_template = []
            with slave.connect() as connection:
                result = connection.execute(text('''SELECT "step_data_sid","data_json","update_time","send_time","biz_info" \
                    FROM "view_document" WHERE "biz_info"!='None' AND "send_time">=:start_time AND "send_time"<=:end_time '''),start_time=self.start_time,end_time=self.end_time)
                connection.close()
            tmp_query = [dict(row) for row in result]
            if len(tmp_query) != 0:
                for x in range(len(tmp_query)):
                    arrtemp_template.append(tmp_query[x])
                return {'result':'OK','messageText':arrtemp_template}
            else:
                return {'result':'ER','messageText':None}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def select_stepdata_admin_all_v1(self,taxid):
        try:
            ts = int(time.time())
            self.taxid = taxid
            self.taxid_tmp = "%'{}'%".format(self.taxid)
            arrtemp_template = []
            with slave.connect() as connection:
                result = connection.execute(text('SELECT COUNT("doc_id") FROM "view_document" WHERE biz_info!=:biz_info AND biz_info LIKE :taxid '),biz_info='None',taxid=self.taxid_tmp)
                connection.close()
            tmp_query = [dict(row) for row in result]
            if len(tmp_query) != 0:
                for x in range(len(tmp_query)):
                    tmp_query[x]['tax_id'] = self.taxid
                return {'result':'OK','messageText':tmp_query}
            else:
                return {'result':'ER','messageText':None}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def select_data_admin_bizpaperless_v1(self):
        try:
            # self.taxid = taxid
            arrtemp_template = []
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "tax_id","transactionMax","transactionNow","storageMax","storageNow" FROM "tb_bizPaperless"'))
                connection.close()
            tmp_query = [dict(row) for row in result]
            if len(tmp_query) != 0:
                return {'result':'OK','messageText':tmp_query}
            else:
                return {'result':'ER','messageText':None}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

class select_3:
    def select_track_v3(self,tracking):
        self.tracking = tracking
        try:
            sql = ''' SELECT
                    tb_send_detail.tracking_id AS "tracking_id" ,
                    tb_send_detail.tracking_id AS "tracking" ,
                    tb_send_detail.sender_email AS "sender_email",
                    tb_send_detail.sender_name AS "sender_name",
                    tb_send_detail.send_time  AS "send_time",
                    tb_send_detail.sender_position  AS "sender_position",
                    tb_track_paper."step_Code"  AS "step_code",
                    tb_send_detail.step_data_sid  AS "step_data_sid",
                    tb_send_detail.doc_id  AS "document_Id",
                    tb_send_detail.file_name  AS "file_name",
                    tb_send_detail.template_webhook  AS "template_webhook",
                    tb_send_detail.email_center  AS "email_center",
                    tb_send_detail.status  AS "status",
                    tb_send_detail.list_ref  AS "list_ref",
                    tb_doc_detail.options_page  AS "options_page_document",
                    tb_doc_detail.sign_page_options  AS "stamp_all",
                    tb_doc_detail.timest  AS "document_time",
                    tb_doc_detail."documentJson"  AS "document_details",
                    tb_doc_detail.fileid  AS "file_id",
                    tb_doc_detail.urgent_type  AS "urgent_code",
                    tb_doc_detail.digit_sign  AS "digit_sign",
                    tb_doc_detail.attempted_folder  AS "attempted_folder",
                    tb_step_data.view_details  AS "view_details",
                    tb_step_data."qrCode_position"  AS "qrCode_position",
                    tb_pdf_storage.string_sign  AS "string_sign",
                    tb_step_data.data_json  AS "data_json"	
                FROM
                    tb_track_paper
                    INNER JOIN tb_step_data ON tb_step_data.sid = tb_track_paper.step_data_sid
                    INNER JOIN tb_send_detail ON tb_send_detail.step_data_sid = tb_track_paper.step_data_sid
                    INNER JOIN tb_doc_detail ON tb_doc_detail.step_id = tb_track_paper.step_data_sid
                    INNER JOIN tb_pdf_storage ON tb_pdf_storage.fid = tb_send_detail.file_id 
                WHERE
                    tb_track_paper.tracking =:tmptracking 
                '''
            with slave.connect() as connection:
                result = connection.execute(text(sql),tmptracking=self.tracking)
                connection.close()
            query = [dict(row) for row in result]
            if len(query) == 0:                
                sql = ''' SELECT
                    tb_send_detail.tracking_id AS "tracking_id" ,
                    tb_send_detail.tracking_id AS "tracking" ,
                    tb_send_detail.sender_email AS "sender_email",
                    tb_send_detail.sender_name AS "sender_name",
                    tb_send_detail.send_time  AS "send_time",
                    tb_send_detail.sender_position  AS "sender_position",
                    tb_track_paper."step_Code"  AS "step_code",
                    tb_send_detail.step_data_sid  AS "step_data_sid",
                    tb_send_detail.doc_id  AS "document_Id",
                    tb_send_detail.file_name  AS "file_name",
                    tb_send_detail.template_webhook  AS "template_webhook",
                    tb_send_detail.email_center  AS "email_center",
                    tb_send_detail.status  AS "status",
                    tb_send_detail.list_ref  AS "list_ref",
                    tb_doc_detail.options_page  AS "options_page_document",
                    tb_doc_detail.sign_page_options  AS "stamp_all",
                    tb_doc_detail.timest  AS "document_time",
                    tb_doc_detail."documentJson"  AS "document_details",
                    tb_doc_detail.fileid  AS "file_id",
                    tb_doc_detail.urgent_type  AS "urgent_code",
                    tb_doc_detail.digit_sign  AS "digit_sign",
                    tb_doc_detail.attempted_folder  AS "attempted_folder",
                    tb_step_data.view_details  AS "view_details",
                    tb_step_data."qrCode_position"  AS "qrCode_position",
                    tb_pdf_storage.string_sign  AS "string_sign",
                    tb_step_data.data_json  AS "data_json"	
                FROM
                    tb_track_paper
                    INNER JOIN tb_step_data ON tb_step_data.sid = tb_track_paper.step_data_sid
                    INNER JOIN tb_send_detail ON tb_send_detail.step_data_sid = tb_track_paper.step_data_sid
                    INNER JOIN tb_doc_detail ON tb_doc_detail.step_id = tb_track_paper.step_data_sid
                    INNER JOIN tb_pdf_storage ON tb_pdf_storage.fid = tb_send_detail.file_id 
                WHERE
                    tb_send_detail.doc_id =:tmptracking 
                '''
                with slave.connect() as connection:
                    result = connection.execute(text(sql),tmptracking=self.tracking)
                    connection.close()
                query = [dict(row) for row in result]
            for x in range(len(query)):
                tmpmdata = query[x]
                tmpsend_time = tmpmdata['send_time']
                tmpsend_time_timestamp = int(tmpsend_time.timestamp())
                tmpmdata['send_time_display'] = convert_datetime_TH_2_display_sendTime(tmpsend_time_timestamp)
                tmpmdata['send_time_string'] = str(tmpsend_time).split('+')[0]
                tmpmdata['generate_time'] = convert_datetime_TH_2_display_sendTime(tmpsend_time_timestamp)
                tmpmdata['generate_time_string'] = str(tmpsend_time).split('+')[0]
                tmpstep_code = tmpmdata['step_code']
                tmpmdata['template_detail'] = {}
                sql = '''select tb_step_template."step_Name",tb_step_template.condition_temp from tb_step_template where "step_Code" = :tmpstepcode and "status" = :tmpstatus '''
                with slave.connect() as connection:
                    result_template = connection.execute(text(sql),tmpstepcode=tmpstep_code,tmpstatus='ACTIVE')
                    connection.close()
                query_template = [dict(row) for row in result_template]
                for i in range(len(query_template)):
                    tmpmdata['template_detail'] = query_template[i]
                try:
                    tmpmdata['status_service'] = eval(str(tmpmdata['status_service']))
                except Exception as e:
                    tmpmdata['status_service'] = None
                if tmpmdata['list_ref'] != "[]" or tmpmdata['list_ref'] != None:
                    tmpmdata['list_ref'] = eval(tmpmdata['list_ref'])
                else:
                    tmpmdata['list_ref'] = tmpmdata['list_ref']
                if tmpmdata['options_page_document'] != None:
                    tmpmdata['options_page_document'] = [tmpmdata['options_page_document']]
                else:
                    tmpmdata['options_page_document'] = []
                tmpmdata['document_time'] = int(tmpmdata['document_time'])
                tmpmdata['document_details'] = eval(tmpmdata['document_details'])
                tmpmdata['document_details_string'] = str(tmpmdata['document_details'])
                tmpmdata['file_id'] = int(tmpmdata['file_id'])
                tmpmdata['digit_sign'] = bool(tmpmdata['digit_sign'])
                try:
                    tmpmdata['view_details'] = eval(tmpmdata['view_details'])
                except Exception as e:
                    tmpmdata['view_details'] = None
                try:
                    tmpmdata['qrCode_position'] = eval(tmpmdata['qrCode_position'])
                except Exception as e:
                    tmpmdata['qrCode_position'] = None
                tmpmdata['qrCode_status'] = False
                if tmpmdata['qrCode_position'] != None and str(tmpmdata['qrCode_position']).replace(' ','') != '':
                    tmpmdata['qrCode_status'] = True     
                step_infomation = eval(tmpmdata['data_json'])                
                if 'step_num' in step_infomation:
                    step_infomation = [step_infomation]           
                tmpmdata['file_user_status_detail'] = []
                if 'step_num' in step_infomation:
                    status_step_sum = ''
                    sum_status_step_list = []
                    list_check_step = []
                    json_step_info_2 = {}
                    step_list_data = []
                    step_ = step_infomation
                    time_success = None
                    step_time_1 = []
                    sendtime = tmpmdata['send_time']
                    step_num = step_infomation['step_num']
                    tmpmdata['step_info'] = step_infomation
                    json_step_info_2['step_status'] = ''
                    for u in range(len(step_['step_detail'])):
                        step_2 = step_['step_detail'][u]
                        for k in range(len(step_2['activity_code'])):
                            if step_2['activity_code'][k] == 'A03':
                                json_step_info = {}
                                json_step_info['activity_status'] = step_2['activity_status'][k]
                                if json_step_info['activity_status'] == 'Complete' or json_step_info['activity_status'] == 'Reject':
                                    json_step_info['activity_time'] = step_2['activity_time'][k]
                                else:
                                    json_step_info['activity_time'] = None
                                json_step_info['one_email'] = step_2['one_email']
                                #process หา timeline
                                if (step_2['activity_status'][k] == 'Complete' or step_2['activity_status'][k] =='Reject' or step_2['activity_status'][k] == 'Approve'):
                                    t1 = str(step_2['activity_time'][k])
                                    time_success = change_to_Timestamp(t1)
                                    step_time_1.append(time_success)
                                #สิ้นสุดการหา timeline
                                query_name_account = paper_lesslogin.query.filter(paper_lesslogin.citizen_data.contains(step_2['one_email'])).all()
                                if len(query_name_account) != 0:
                                    tmp_account_name = eval(query_name_account[0].citizen_data)
                                    try:
                                        tmp_account_name = tmp_account_name['first_name_th'] + ' ' + tmp_account_name['last_name_th']
                                    except Exception as e:
                                        tmp_account_name=None
                                else:
                                    tmp_account_name = None
                                json_step_info['account_name'] = tmp_account_name
                                json_step_info['step_num'] = step_num

                                list_check_step.append(json_step_info['activity_status'])
                                step_list_data.append(json_step_info)
                            elif step_2['activity_code'][k] == 'A04':
                                json_step_info = {}
                                json_step_info['activity_status'] = step_2['activity_status'][k]
                                if json_step_info['activity_status'] == 'Complete' or json_step_info['activity_status'] == 'Reject':
                                    json_step_info['activity_time'] = step_2['activity_time'][k]
                                else:
                                    json_step_info['activity_time'] = None
                                json_step_info['one_email'] = step_2['one_email']
                                #process หา timeline
                                if (step_2['activity_status'][k] == 'Complete' or step_2['activity_status'][k] =='Reject' or step_2['activity_status'][k] == 'Approve'):
                                    t1 = str(step_2['activity_time'][k])
                                    time_success = change_to_Timestamp(t1)
                                    step_time_1.append(time_success)
                                #สิ้นสุดการหา timeline
                                query_name_account = paper_lesslogin.query.filter(paper_lesslogin.citizen_data.contains(step_2['one_email'])).all()
                                if len(query_name_account) != 0:
                                    tmp_account_name = eval(query_name_account[0].citizen_data)
                                    try:
                                        tmp_account_name = tmp_account_name['first_name_th'] + ' ' + tmp_account_name['last_name_th']
                                    except Exception as e:
                                        tmp_account_name=None
                                else:
                                    tmp_account_name = None
                                json_step_info['account_name'] = tmp_account_name
                                json_step_info['step_num'] = step_num

                                list_check_step.append(json_step_info['activity_status'])
                                step_list_data.append(json_step_info)
                            elif step_2['activity_code'][k] == 'A05':
                                json_step_info = {}
                                json_step_info['activity_status'] = step_2['activity_status'][k]
                                if json_step_info['activity_status'] == 'Complete' or json_step_info['activity_status'] == 'Reject':
                                    json_step_info['activity_time'] = step_2['activity_time'][k]
                                else:
                                    json_step_info['activity_time'] = None
                                json_step_info['one_email'] = step_2['one_email']
                                #process หา timeline
                                if (step_2['activity_status'][k] == 'Complete' or step_2['activity_status'][k] =='Reject' or step_2['activity_status'][k] == 'Approve'):
                                    t1 = str(step_2['activity_time'][k])
                                    time_success = change_to_Timestamp(t1)
                                    step_time_1.append(time_success)
                                #สิ้นสุดการหา timeline
                                query_name_account = paper_lesslogin.query.filter(paper_lesslogin.citizen_data.contains(step_2['one_email'])).all()
                                if len(query_name_account) != 0:
                                    tmp_account_name = eval(query_name_account[0].citizen_data)
                                    try:
                                        tmp_account_name = tmp_account_name['first_name_th'] + ' ' + tmp_account_name['last_name_th']
                                    except Exception as e:
                                        tmp_account_name=None
                                else:
                                    tmp_account_name = None
                                json_step_info['account_name'] = tmp_account_name
                                json_step_info['step_num'] = step_num

                                list_check_step.append(json_step_info['activity_status'])
                                step_list_data.append(json_step_info)
                        json_step_info_2['step_info'] = step_list_data
                        if json_step_info_2['step_status'] == '':
                            if 'Reject' in list_check_step:
                                json_step_info_2['step_status'] = 'Reject'
                            elif 'Incomplete' in list_check_step:
                                json_step_info_2['step_status'] = 'Incomplete'
                            elif 'Pending' in list_check_step:
                                json_step_info_2['step_status'] = 'Incomplete'
                            else:
                                json_step_info_2['step_status'] = 'Complete'
                        else:
                            if 'Complete' in list_check_step:
                                json_step_info_2['step_status'] = 'Complete'
                        sum_status_step_list.append(json_step_info_2['step_status'])
                        timeline_ = getTimeline(sendtime,step_time_1)
                        list_timeline = getlistTimeline(sendtime,step_time_1)
                    tmpmdata['list_timeline'] = list_timeline
                    tmpmdata['timeline'] = timeline_
                    tmpmdata['file_user_status_detail'].append(json_step_info_2)
                    if 'Reject' in sum_status_step_list:
                        status_step_sum = 'Reject'
                        sendtime = tmpmdata['send_time']
                        timing_ = timing(time_success,sendtime)
                        tmpmdata['timing'] = timing_
                    elif 'Incomplete' in sum_status_step_list:
                        status_step_sum = 'Incomplete'
                        now = datetime.datetime.now()
                        sendtime = tmpmdata['send_time']
                        timing_ = timing(datetime.datetime.timestamp(now),sendtime)
                        tmpmdata['timing'] = timing_
                    elif 'Pending' in sum_status_step_list:
                        status_step_sum = 'Incomplete'
                        now = datetime.datetime.now()
                        sendtime = tmpmdata['send_time']
                        timing_ = timing(datetime.datetime.timestamp(now),sendtime)
                        tmpmdata['timing'] = timing_
                    elif 'Complete' in sum_status_step_list:
                        status_step_sum = 'Complete'
                        sendtime = tmpmdata['send_time']
                        timing_ = timing(time_success,sendtime)
                        tmpmdata['timing'] = timing_
                    elif 'Approve' in sum_status_step_list:
                        status_step_sum = 'Complete'
                        sendtime = tmpmdata['send_time']
                        timing_ = timing(time_success,sendtime)
                        tmpmdata['timing'] = timing_
                    else:
                        status_step_sum = 'Complete'
                        sendtime = tmpmdata['send_time']
                        timing_ = timing(time_success,sendtime)
                        tmpmdata['timing'] = timing_

                    # if 'Reject' in sum_status_step_list:
                    #     status_step_sum = 'Reject'
                    #     for u in range(len(step_['step_detail'])):
                    #         step_2 = step_['step_detail'][u]
                    #         for k in range(len(step_2['activity_code'])):
                    #             if self.emailUser == step_2['one_email']:
                    #                 json_data_res['file_user_status'] = 'Reject'
                    #             # json_data_res['file_user_status'] = step_2['activity_status'][k]
                    # elif 'Incomplete' in sum_status_step_list:
                    #     status_step_sum = 'Incomplete'
                    #     for u in range(len(step_['step_detail'])):
                    #         step_2 = step_['step_detail'][u]
                    #         json_data_res['file_user_status'] = step_2['activity_status'][k]
                    # elif 'Pending' in sum_status_step_list:
                    #     status_step_sum = 'Incomplete'
                    #     for u in range(len(step_['step_detail'])):
                    #         step_2 = step_['step_detail'][u]
                    #         if self.emailUser == step_2['one_email']:
                    #             for k in range(len(step_2['activity_code'])):
                    #                     if step_2['activity_code'][k] == 'A03':
                    #                         json_data_res['file_user_status'] = step_2['activity_status'][k]
                    # else:
                    #     status_step_sum = 'Complete'
                        # for u in range(len(step_['step_detail'])):
                        #     step_2 = step_['step_detail'][u]
                        #     if self.emailUser == step_2['one_email']:
                        #         for k in range(len(step_2['activity_code'])):
                        #                 if step_2['activity_code'][k] == 'A03':
                        #                     json_data_res['file_user_status'] = step_2['activity_status'][k]
                    tmpmdata['file_status_sum'] = status_step_sum
                else:
                    status_step_sum = ''
                    sum_status_step_list = []
                    alr_mail = []
                    time_success = None
                    step_time_1 = []
                    sendtime = tmpmdata['send_time']
                    tmpmdata['step_info'] = step_infomation
                    for i in range(len(step_infomation)):
                        list_check_step = []
                        json_step_info_2 = {}
                        step_list_data = []
                        step_ = step_infomation[i]
                        step_num = step_infomation[i]['step_num']
                        json_step_info_2['step_status'] = ''
                        for u in range(len(step_['step_detail'])):
                            step_2 = step_['step_detail'][u]
                            for k in range(len(step_2['activity_code'])):
                                if step_2['activity_code'][k] == 'A03':
                                    json_step_info = {}
                                    json_step_info['activity_status'] = step_2['activity_status'][k]
                                    if json_step_info['activity_status'] == 'Complete' or json_step_info['activity_status'] == 'Reject':
                                        json_step_info['activity_time'] = step_2['activity_time'][k]
                                    else:
                                        json_step_info['activity_time'] = None
                                    json_step_info['one_email'] = step_2['one_email']
                                    query_name_account = paper_lesslogin.query.filter(paper_lesslogin.citizen_data.contains(step_2['one_email'])).all()
                                    # print('activity_time',step_2['activity_time'][k])
                                    # print('activity_status',step_2['activity_status'][k])
                                    #process หา timeline
                                    if (step_2['activity_status'][k] == 'Complete' or step_2['activity_status'][k] =='Reject' or step_2['activity_status'][k] == 'Approve'):
                                        t1 = str(step_2['activity_time'][k])
                                        print ('else activity_time',t1)
                                        time_success = change_to_Timestamp(t1)
                                        step_time_1.append(time_success)
                                    #สิ้นสุดการหา timeline
                                    if len(query_name_account) != 0:
                                        try:
                                            tmp_account_name = eval(query_name_account[0].citizen_data)
                                            tmp_account_name = tmp_account_name['first_name_th'] + ' ' + tmp_account_name['last_name_th']
                                        except Exception as e:
                                            tmp_account_name = None
                                            exc_type, exc_obj, exc_tb = sys.exc_info()
                                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                            print(exc_type, fname, exc_tb.tb_lineno)

                                    else:
                                        tmp_account_name = None
                                    json_step_info['step_num'] = step_num
                                    json_step_info['account_name'] = tmp_account_name
                                    list_check_step.append(json_step_info['activity_status'])
                                    step_list_data.append(json_step_info)
                                elif step_2['activity_code'][k] == 'A04':
                                    json_step_info = {}
                                    json_step_info['activity_status'] = step_2['activity_status'][k]
                                    if json_step_info['activity_status'] == 'Complete' or json_step_info['activity_status'] == 'Reject':
                                        json_step_info['activity_time'] = step_2['activity_time'][k]
                                    else:
                                        json_step_info['activity_time'] = None
                                    json_step_info['one_email'] = step_2['one_email']
                                    query_name_account = paper_lesslogin.query.filter(paper_lesslogin.citizen_data.contains(step_2['one_email'])).all()
                                    # print('activity_time',step_2['activity_time'][k])
                                    # print('activity_status',step_2['activity_status'][k])
                                    #process หา timeline
                                    if (step_2['activity_status'][k] == 'Complete' or step_2['activity_status'][k] =='Reject' or step_2['activity_status'][k] == 'Approve'):
                                        t1 = str(step_2['activity_time'][k])
                                        print ('else activity_time',t1)
                                        time_success = change_to_Timestamp(t1)
                                        step_time_1.append(time_success)
                                    #สิ้นสุดการหา timeline
                                    if len(query_name_account) != 0:
                                        try:
                                            tmp_account_name = eval(query_name_account[0].citizen_data)
                                            tmp_account_name = tmp_account_name['first_name_th'] + ' ' + tmp_account_name['last_name_th']
                                        except Exception as e:
                                            tmp_account_name = None
                                            exc_type, exc_obj, exc_tb = sys.exc_info()
                                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                            print(exc_type, fname, exc_tb.tb_lineno)

                                    else:
                                        tmp_account_name = None
                                    json_step_info['step_num'] = step_num
                                    json_step_info['account_name'] = tmp_account_name
                                    list_check_step.append(json_step_info['activity_status'])
                                    step_list_data.append(json_step_info)
                                elif step_2['activity_code'][k] == 'A05':
                                    json_step_info = {}
                                    json_step_info['activity_status'] = step_2['activity_status'][k]
                                    if json_step_info['activity_status'] == 'Complete' or json_step_info['activity_status'] == 'Reject':
                                        json_step_info['activity_time'] = step_2['activity_time'][k]
                                    else:
                                        json_step_info['activity_time'] = None
                                    json_step_info['one_email'] = step_2['one_email']
                                    query_name_account = paper_lesslogin.query.filter(paper_lesslogin.citizen_data.contains(step_2['one_email'])).all()
                                    # print('activity_time',step_2['activity_time'][k])
                                    # print('activity_status',step_2['activity_status'][k])
                                    #process หา timeline
                                    if (step_2['activity_status'][k] == 'Complete' or step_2['activity_status'][k] =='Reject' or step_2['activity_status'][k] == 'Approve'):
                                        t1 = str(step_2['activity_time'][k])
                                        print ('else activity_time',t1)
                                        time_success = change_to_Timestamp(t1)
                                        step_time_1.append(time_success)
                                    #สิ้นสุดการหา timeline
                                    if len(query_name_account) != 0:
                                        try:
                                            tmp_account_name = eval(query_name_account[0].citizen_data)
                                            tmp_account_name = tmp_account_name['first_name_th'] + ' ' + tmp_account_name['last_name_th']
                                        except Exception as e:
                                            tmp_account_name = None
                                            exc_type, exc_obj, exc_tb = sys.exc_info()
                                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                            print(exc_type, fname, exc_tb.tb_lineno)

                                    else:
                                        tmp_account_name = None
                                    json_step_info['step_num'] = step_num
                                    json_step_info['account_name'] = tmp_account_name
                                    list_check_step.append(json_step_info['activity_status'])
                                    step_list_data.append(json_step_info)
                            json_step_info_2['step_info'] = step_list_data
                            if json_step_info_2['step_status'] == '':
                                if 'Reject' in list_check_step:
                                    json_step_info_2['step_status'] = 'Reject'
                                elif 'Incomplete' in list_check_step:
                                    json_step_info_2['step_status'] = 'Incomplete'
                                elif 'Pending' in list_check_step:
                                    json_step_info_2['step_status'] = 'Incomplete'
                                else:
                                    json_step_info_2['step_status'] = 'Complete'
                            else:
                                if 'Complete' in list_check_step:
                                    json_step_info_2['step_status'] = 'Complete'
                            sum_status_step_list.append(json_step_info_2['step_status'])
                        timeline_ = getTimeline(sendtime,step_time_1)
                        tmpmdata['timeline'] = timeline_ 
                        list_timeline = getlistTimeline(sendtime,step_time_1)
                        tmpmdata['list_timeline'] = list_timeline

                        tmpmdata['file_user_status_detail'].append(json_step_info_2)
                    if 'Reject' in sum_status_step_list:
                        status_step_sum = 'Reject'
                        sendtime = tmpmdata['send_time']
                        timing_ = timing(time_success,sendtime)
                        tmpmdata['timing'] = timing_
                    elif 'Incomplete' in sum_status_step_list:
                        status_step_sum = 'Incomplete'
                        now = datetime.datetime.now()
                        sendtime = tmpmdata['send_time']
                        timing_ = timing(datetime.datetime.timestamp(now),sendtime)
                        tmpmdata['timing'] = timing_
                    elif 'Pending' in sum_status_step_list:
                        status_step_sum = 'Incomplete'
                        now = datetime.datetime.now()
                        sendtime = tmpmdata['send_time']
                        timing_ = timing(datetime.datetime.timestamp(now),sendtime)
                        tmpmdata['timing'] = timing_
                    else:
                        status_step_sum = 'Complete'
                        sendtime = tmpmdata['send_time']
                        timing_ = timing(time_success,sendtime)
                        tmpmdata['timing'] = timing_
                    tmpmdata['file_status_sum'] = status_step_sum

                # tmpmdata['digit_sign'] = bool(tmpmdata['digit_sign'])
                # tmpmdata['digit_sign'] = bool(tmpmdata['digit_sign'])
                # tmpmdata['digit_sign'] = bool(tmpmdata['digit_sign'])
                # tmpmdata['send_time_display'] = convert_datetime_TH_2_display_sendTime(tmpsend_time_timestamp)
                return {'result':'OK','messageText':tmpmdata}
        except Exception as e:
            print(str(e))
            return {'result':'ER','messageText':str(e)}

    def select_trackinggroup_version2(self,group_id):
        self.group_id = group_id
        where_sql = 'WHERE id=:group_id ' 
        try:
            tmptracking_group = ''
            # text_sql = text('SELECT * FROM "tb_group_document" ' + where_sql)
            text_sql = text('SELECT "id","sid_group","data_group","updatetime","email_group","status","create_by","update_by","step_group",\
            "pdf_org","pdf_sign","step_group_detail","group_data_json","group_other","email_view_group","hash_id","tracking_group",\
            "status_group","group_title","group_name","bizinfo","group_status","cover_page",\
            "calculate_fieds","maxstep","email_middle","html_data","doctype_group","bizinfo_group" FROM "tb_group_document_2" ' + where_sql)
            with engine.connect() as connection:
                result_all = connection.execute(text_sql \
                        ,group_id=self.group_id)
                connection.close()
            query_temp = [dict(row) for row in result_all]
            query_temp = query_temp[0]
            if 'tracking_group' in query_temp:
                tmptracking_group = query_temp['tracking_group']
            if 'group_other' in query_temp:
                tmpgroup_other = eval(query_temp['group_other'])
                tmpgroup_color = tmpgroup_other[0]['color']
            if 'sid_group' in query_temp:
                tmpsid_group = eval(query_temp['sid_group'])
            return {'result':'OK','tracking_group':tmptracking_group,'group_color':tmpgroup_color,'sid_group':tmpsid_group}
        except Exception as e:
            return {'result':'ER','message':str(e)}
        
    def select_onebiz_transaction_v1(self,tax_id):
        self.tax_id = tax_id        
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
        this_date = str(st).split(' ')[0]
        year = int(this_date.split('/')[2])
        month = int(this_date.split('/')[1])
        search_tax_id = "'%''{}''%'".format(self.tax_id)
        try:
            day_back = calendar.monthrange(year, month)
            day_start = str(year) + '/' + str(month) + '/' + str(day_back[0]+1) + ' ' + '00:00:00'
            day_end = str(year) + '/' + str(month) + '/' + str(day_back[1]) + ' ' + '00:00:00'
            where_sql = 'WHERE biz_info LIKE '+search_tax_id+' AND (upload_time>=:day_start AND upload_time<=:day_end) ' 
            text_sql = text('SELECT COUNT("id") FROM "tb_step_data" ' + where_sql)
            with slave.connect() as connection:
                result_all = connection.execute(text_sql \
                        ,tax_id='',tax_id_2='',day_start=day_start,day_end=day_end)
                connection.close()
            query_temp = [dict(row) for row in result_all]
            query_temp = query_temp[0]
            if 'count' in query_temp:
                return {'result':'OK','count':query_temp['count']}
            else:
                return {'result':'ER','count':0}
        except Exception as e:
            return {'result':'ER','message':str(e)}

    def select_trackinggroup_v1(self,group_id):
        self.group_id = group_id
        where_sql = 'WHERE id=:group_id ' 
        try:
            tmptracking_group = ''
            # text_sql = text('SELECT * FROM "tb_group_document" ' + where_sql)
            text_sql = '''SELECT
                    "tb_group_document"."id",
                    "sid_group",
                    "data_group",
                    "updatetime",
                    "email_group",
                    "tb_group_document"."status",
                    "create_by",
                    "update_by",
                    "step_group",
                    "pdf_org",
                    "pdf_sign",
                    "step_group_detail",
                    "group_data_json",
                    "group_other",
                    "email_view_group",
                    "hash_id",
                    "tracking_group",
                    "status_group",
                    "group_title",
                    "group_name",
                    "document_type",
                    "bizinfo",
                    "group_status",
                    "cover_page",
                    "calculate_fieds",
                    "maxstep",
                    "email_middle",
                    "html_data" ,
                    "tb_bizPaperless"."customer_type"
                FROM
                    "tb_group_document"
                    INNER JOIN "tb_bizPaperless" ON "tb_group_document".bizinfo LIKE '%' || "tb_bizPaperless".tax_id || '%' 
                WHERE
                    "tb_group_document"."id" = :group_id '''
            with slave.connect() as connection:
                result_all = connection.execute(text(text_sql) \
                        ,group_id=self.group_id)
            connection.close()
            query_temp = [dict(row) for row in result_all]
            query_temp = query_temp[0]
            if 'tracking_group' in query_temp:
                tmptracking_group = query_temp['tracking_group']
            if 'group_other' in query_temp:
                tmpgroup_other = eval(query_temp['group_other'])
                tmpgroup_color = tmpgroup_other[0]['color']
            if 'sid_group' in query_temp:
                tmpsid_group = eval(query_temp['sid_group'])
            if 'customer_type' in query_temp:
                query_customer_type = query_temp['customer_type']
            # if 'bizinfo' in query_temp:
            #     try:
            #         tmpbizinfo = eval(query_temp['bizinfo'])
            #     except Exception as e:
            #         tmpbizinfo = None
            #     tmptaxid = tmpbizinfo['id_card_num']
            # if tmpbizinfo != None:
            #     sql = ''' select "customer_type" from "tb_bizPaperless" where "tax_id" = :strtmptaxid '''
            #     with slave.connect() as connection:
            #         result_taxid = connection.execute(text(sql) \
            #                 ,strtmptaxid=tmptaxid)
            #     connection.close()
            #     query_customer_type= [dict(row) for row in result_taxid]
            return {'result':'OK','tracking_group':tmptracking_group,'group_color':tmpgroup_color,'sid_group':tmpsid_group,'tax_type':query_customer_type}
        except Exception as e:
            return {'result':'ER','message':str(e)}
        finally:
            connection.close()


    def select_document_sender_v1(self,typequery,username,email_one,limit,offset,document_type,keyword,status,tax_id,sort_key,group_status=None,pick_datetime=None,tmptimeapprove=None):
        self.typequery = typequery
        self.email_one = email_one
        self.username = username
        self.tax_id = tax_id
        self.limit = ''
        self.offset = ''
        self.group_status = group_status
        self.pick_datetime = pick_datetime
        self.before_datetime = None
        self.after_datetime = None
        if limit != '':
            self.limit = int(limit)
        if offset != '':
            self.offset = int(offset)
        self.document_type = document_type
        self.keyword = keyword
        self.status = status
        self.tmptimeapprove = tmptimeapprove
        if self.tmptimeapprove != None:
            self.tmptimeapprove = tmptimeapprove
        status_ACTIVE = 'ACTIVE'
        self.all_status = ['W','N','Z']
        if sort_key != None:
            self.sort_key = sort_key.lower()
        else:
            self.sort_key = sort_key
        search = "%'{}'%".format(self.email_one)
        search_keyword = "%{}%".format(self.keyword)
        search_tax_id = "'%''{}''%'".format(self.tax_id)
        if self.pick_datetime != None:
            if self.pick_datetime != "":
                self.pick_datetime = int(self.pick_datetime)
                self.search_datetime = datetime.datetime.fromtimestamp(self.pick_datetime).strftime('%Y-%m-%d')
                self.before_datetime = str(self.search_datetime) + 'T00:00:00'
                self.after_datetime = str(self.search_datetime) + 'T23:59:59'
        # print(self.before_datetime,self.after_datetime)
        # print(self.pick_datetime)
        arr_list_sum = []
        sum_row_tooffset = 0
        keep_lenstatus = []
        list_arr = []
        tmp_sid_code_list =  []
        tmp_list = []      
        a = 0       
        count_rowDocument = 0
        count_rowDocument_StatusActive = 0
        count_rowDocument_StatusReject = 0
        count_rowDocument_StatusCancel = 0
        statusFile_count_approve = 0
        statusFile_count_pendding = 0
        statusFile_count_reject = 0
        statusFile_count_wait = 0
        list_temp_query = []
        tmp_sid_code_list = []
        arr_gruop = []
        arr_group_sid = []
        tmp_arr_sid = []
        tmp_group_id = None
        json_Data = {}
        str_time = (time.time())
        if self.tmptimeapprove == True:
            if self.sort_key == None:
                ORDER_sql = ' ORDER BY "tb_step_data".update_time DESC LIMIT :limit OFFSET :offset '
            else:
                if self.sort_key == 'desc':
                    ORDER_sql = ' ORDER BY "tb_step_data".update_time DESC LIMIT :limit OFFSET :offset '
                else:
                    ORDER_sql = ' ORDER BY "tb_step_data".update_time ASC LIMIT :limit OFFSET :offset '
        else:
            if self.sort_key == None:
                ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
            else:
                if self.sort_key == 'desc':
                    ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
                else:
                    ORDER_sql = ' ORDER BY "tb_send_detail".send_time ASC LIMIT :limit OFFSET :offset '
        where_sql = 'WHERE status=:status AND "send_user"=:send_user '
        if self.tax_id != '':
            where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id
        else:
            where_sql += ''
        if self.pick_datetime != None:
            where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) ' 
        if typequery == 'sender':            
            if self.group_status == "true":
                where_sql += ' AND ("tb_send_detail"."group_id" = :group_statustmp OR "tb_send_detail"."group_id" IS NULL) '
            where_sql += ORDER_sql
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid '+ where_sql )\
                    ,status=status_ACTIVE,send_user=self.username,limit=self.limit,offset=self.offset,biz_info='',biz_info_none='None',group_statustmp=[],group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query = [dict(row) for row in result]
            # print('sender len query',len(query))
        elif typequery == 'sender_filter':
            if self.status in self.all_status:
                for i in range(self.limit):
                    if i > 0:
                        self.offset = self.offset + self.limit
                    if len(arr_list_sum) < self.limit:
                        arr_list_sum,sum_row_tooffset = recursive_sender_status_new_v1(self.username,self.email_one,self.limit,self.offset,self.status,arr_list_sum,sum_row_tooffset,self.document_type,self.tax_id,self.group_status,self.tmptimeapprove)
                        keep_lenstatus = arr_list_sum
                        sum_row_tooffset = self.offset + sum_row_tooffset
                        if len(keep_lenstatus) == len(arr_list_sum):
                            a = a + 1
                            if a == 5:
                                list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
                                json_Data['document'] = list_arr
                                json_Data['offset'] = sum_row_tooffset
                                return {'result':'OK','messageText':json_Data}                    
                    else:
                        list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
                        json_Data['document'] = list_arr
                        json_Data['offset'] = sum_row_tooffset
                        return {'result':'OK','messageText':json_Data} 
                list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
                json_Data['document'] = list_arr
                json_Data['offset'] = sum_row_tooffset
                # print(len(list_arr))
                return {'result':'OK','messageText':json_Data}
            if self.status != '':
                where_sql += ' AND "tb_send_detail"."document_status" = :document_status '
            if self.document_type != '':
                where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
            if self.group_status == "true":
                where_sql += ' AND ("tb_send_detail"."group_id" = :group_statustmp OR "tb_send_detail"."group_id" IS NULL) '
            if self.pick_datetime != None:
                where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) ' 
            where_sql += ORDER_sql
            text_sql = text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
                INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
            # print(text_sql , self.status)
            with slave.connect() as connection:
                result = connection.execute(text_sql\
                    ,status=status_ACTIVE,send_user=self.username,limit=self.limit,offset=self.offset,documentType=self.document_type,document_status=self.status,biz_info='',biz_info_none='None',group_statustmp=[],group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query = [dict(row) for row in result]
        elif typequery == 'sender_search':
            if self.document_type != '':
                where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
            if self.keyword != '':
                where_sql += 'AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword) '
            if self.pick_datetime != None:
                where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) ' 
            where_sql += ORDER_sql
            text_sql = text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
                INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
            with slave.connect() as connection:
                result = connection.execute(text_sql\
                    ,status=status_ACTIVE,send_user=self.username,limit=self.limit,offset=self.offset,documentType=self.document_type,keyword=search_keyword,biz_info='',biz_info_none='None',group_statustmp='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query = [dict(row) for row in result]
        # print('len sender',len(query))
        try:
            for x in range(len(query)):
                arr_email_document = []
                tmp_req_email = []
                email_step_sum_w = []
                tmp_dict_json = query[x]
                tmp_document_type = None
                tmp_sicode = tmp_dict_json['step_data_sid']
                tmp_sid_code_list.append(tmp_sicode)
                tmp_send_time = tmp_dict_json['send_time']
                tmp_document_id = tmp_dict_json['doc_id']
                tmp_tracking_id = tmp_dict_json['tracking_id']
                tmp_sender_name = tmp_dict_json['sender_name']
                tmp_sender_email = tmp_dict_json['sender_email']
                tmp_file_name = tmp_dict_json['file_name']
                tmp_groupid = tmp_dict_json['group_id']
                email_step_sum = tmp_dict_json['recipient_email']
                update_time = tmp_dict_json['update_time']
                sender_name_eng = find_name_surename_by_username(tmp_sender_email)
                tmptime_update = update_time
                tmptime_update_timestamp = int(tmptime_update.timestamp())
                tmptime_update_string = str(update_time).split('+')[0]
                th_dateTime_2_last = convert_datetime_TH_2(tmptime_update_timestamp)
                ts = int(time.time())
                date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
                datetime_display_update = int(tmptime_update.timestamp())
                date_time_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%Y-%m-%d')
                yar_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%Y')
                time_show_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%H:%M')
                old_year = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%d/%m/%Y')
                if date_time_today == date_time_db:
                    date_last_display_show = time_show_db
                else:
                    if year_today == yar_db:
                        date_last_display_show = convert_datetime_TH_2_display(datetime_display_update)
                    else:
                        date_last_display_show = old_year
                
                if email_step_sum != None:
                    email_step_sum = eval(email_step_sum)
                # print(email_step_sum)
                tmpstatus_detail = tmp_dict_json['status_details']
                tmpdocument_status = tmp_dict_json['document_status']
                tmpstepnow = tmp_dict_json['stepnow']
                status_groupid = False
                if tmp_groupid != None:
                    tmp_groupid = eval(tmp_groupid)
                    if len(tmp_groupid) != 0:
                        status_groupid = True
                if tmpstepnow != None:
                    tmpstepnow = int(tmpstepnow)
                tmpstepmax = tmp_dict_json['stepmax']
                if tmpstepmax != None:
                    tmpstepmax = int(tmpstepmax)
                if tmpstatus_detail != None:
                    tmpstatus_detail = eval(tmpstatus_detail)                            
                    for z in range(len(tmpstatus_detail)):
                        email_step_sum_w.append(tmpstatus_detail[z]['email'])

                    if tmpdocument_status == 'N':
                        for x in range(len(tmpstatus_detail)):
                            if self.email_one not in arr_email_document:
                                if self.email_one in tmpstatus_detail[x]['email']:
                                    if tmpstatus_detail[x]['step_status_code'] == 'W':
                                        arr_email_document.append(self.email_one)
                                        tmpdocument_status = tmpstatus_detail[x]['step_status_code']
                                        break
                                    else:
                                        tmpdocument_status = tmpstatus_detail[x]['step_status_code']
                if tmpdocument_status == 'Z':
                    res_status_file_string = 'อยู่ในช่วงดำเนินการ'
                elif tmpdocument_status == 'W':
                    res_status_file_string = 'รอคุณอนุมัติ'
                elif tmpdocument_status == 'N':
                    res_status_file_string = 'กำลังดำเนินการ'
                elif tmpdocument_status == 'R':
                    res_status_file_string = 'เอกสารที่ส่งคืนแก้ไข'
                else:
                    res_status_file_string = 'เอกสารสมบูรณ์'
                tmp_sign_page_options = tmp_dict_json['sign_page_options']
                tmp_document_type = tmp_dict_json['documentType']
                tmp_options_page = []
                if tmp_dict_json['options_page'] != None:
                    if tmp_dict_json['options_page'] != '':
                        tmp_options_page = [eval(tmp_dict_json['options_page'])]
                else:
                    tmp_options_page = []
                if len(tmp_options_page) != 0:
                    tmp_status_group = False
                    if status_groupid == True:
                        if len(tmp_options_page) != 0:
                            if 'group_detail' in tmp_options_page[0]:
                                tmp_group_detail = tmp_options_page[0]['group_detail']
                                if 'group_status' in tmp_group_detail:
                                    if tmp_group_detail['group_status'] == True:
                                        tmp_status_group = True
                                        tmpstepnum = tmp_group_detail['step_num']
                if tmp_dict_json['documentJson'] != None:
                    documentJson_result = eval(tmp_dict_json['documentJson'])
                    documentName = documentJson_result['document_name']
                    documentType = documentJson_result['document_type']
                else:
                    documentName = None
                    documentType = None
                if tmp_dict_json['urgent_type'] != None:
                    documentUrgentType = tmp_dict_json['urgent_type']
                    if documentUrgentType == 'I':
                        documentUrgentString = 'ด่วนมาก'
                    elif documentUrgentType == 'U':
                        documentUrgentString = 'ด่วน'
                    elif documentUrgentType == 'M':
                        documentUrgentString = 'ปกติ'
                tmp_biz_info = None
                tmprole_name = None
                tmprole_level = None
                tmpdept_name = None
                # แก้
                if self.tax_id != '':
                    eval_biz_info = json.dumps(tmp_dict_json['biz_info'])
                    eval_biz_info = json.loads(eval_biz_info)
                    eval_biz_info = eval(eval_biz_info)
                    if 'role_name' in eval_biz_info:
                        tmprole_name = eval_biz_info['role_name']
                    if 'role_level' in eval_biz_info:
                        tmprole_level = eval_biz_info['role_level']
                    if 'dept_name' in eval_biz_info:
                        tmpdept_name = eval_biz_info['dept_name']
                    if 'dept_name' in eval_biz_info:                        
                        tmp_biz_info = {
                            'tax_id':eval_biz_info['id_card_num'],
                            'role_name' : tmprole_name,
                            'dept_name' : tmpdept_name,
                            'role_level' : tmprole_level            
                        }                                
                    elif 'dept_name' not in eval_biz_info:
                        tmp_biz_info = {
                            'tax_id':eval_biz_info['id_card_num'],
                            'role_name' : tmprole_name,
                            'dept_name' : [],
                            'role_level' : tmprole_level            
                        }
                            
                dateTime_String = tmp_send_time
                th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
                ts = int(time.time())
                date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
                datetime_display = int(dateTime_String.timestamp())
                date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
                yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
                time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
                old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
                if date_time_today == date_time_db:
                    date_display_show = time_show_db
                else:
                    if year_today == yar_db:
                        date_display_show = convert_datetime_TH_2_display(datetime_display)
                    else:
                        date_display_show = old_year
                try:
                    if tmp_status_group == True:
                        for ui in range(len(tmpstepnum)):
                            intstepnum = tmpstepnum[ui] - 1
                            # print(intstepnum)
                            for w in range(len(email_step_sum_w[intstepnum])):
                                tmp_req_email.append(email_step_sum_w[intstepnum][w])
                except Exception as e:
                    tmp_req_email = []
                list_arr.append({
                    'group_email':tmp_req_email,
                    'group_id':None,
                    'group_status':tmp_status_group,
                    'sidCode':tmp_sicode,
                    'document_name':documentName,
                    'document_type':tmp_document_type,
                    'document_urgent':documentUrgentType,
                    'document_urgent_string':documentUrgentString,
                    'dateTime_String':str(dateTime_String).split('+')[0],
                    'dateTime_String_TH_1':th_dateTime_2,
                    'dateTime_display':date_display_show,
                    'document_id':tmp_document_id,
                    'stamp_all':tmp_sign_page_options,
                    'options_page_document':tmp_options_page,
                    'max_step':tmpstepmax,
                    'step_now':tmpstepnow,
                    'date_String':str(dateTime_String).split(' ')[0],
                    'time_String':str(dateTime_String).split(' ')[1].split('+')[0],
                    'status_file_code':tmpdocument_status,
                    'status_file_string':res_status_file_string,
                    'dateTime':int(dateTime_String.timestamp()),
                    'tracking_id':tmp_tracking_id,
                    'sender_name':tmp_sender_name,
                    'sender_email':tmp_sender_email,
                    'file_name':tmp_file_name,
                    'document_business':tmp_biz_info,
                    'update_last':tmptime_update,
                    'update_last_String_TH_1':th_dateTime_2_last,
                    'update_last_display':date_last_display_show,
                    'update_last_String':tmptime_update_string,
                    'update_last_TimeStamp':tmptime_update_timestamp,
                    'sender_name_eng' : sender_name_eng
                })
            list_arr = sorted(list_arr, key=lambda k: k['dateTime'], reverse=True)
            if self.tmptimeapprove == True:
                list_arr = sorted(list_arr, key=lambda k: k['update_last_TimeStamp'], reverse=True)
            json_Data['document'] = list_arr
            return {'result':'OK','messageText':json_Data}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(e)} 


    # def select_document_sender_v1(self,typequery,username,email_one,limit,offset,document_type,keyword,status,tax_id,sort_key,group_status=None,pick_datetime=None):
    #     self.typequery = typequery
    #     self.email_one = email_one
    #     self.username = username
    #     self.tax_id = tax_id
    #     self.limit = ''
    #     self.offset = ''
    #     self.group_status = group_status
    #     self.pick_datetime = pick_datetime
    #     self.before_datetime = None
    #     self.after_datetime = None
    #     if limit != '':
    #         self.limit = int(limit)
    #     if offset != '':
    #         self.offset = int(offset)
    #     self.document_type = document_type
    #     self.keyword = keyword
    #     self.status = status
    #     status_ACTIVE = 'ACTIVE'
    #     self.all_status = ['W','N','Z']
    #     if sort_key != None:
    #         self.sort_key = sort_key.lower()
    #     else:
    #         self.sort_key = sort_key
    #     search = "%'{}'%".format(self.email_one)
    #     search_keyword = "%{}%".format(self.keyword)
    #     search_tax_id = "'%''{}''%'".format(self.tax_id)
    #     if self.pick_datetime != None:
    #         if self.pick_datetime != "":
    #             self.pick_datetime = int(self.pick_datetime)
    #             self.search_datetime = datetime.datetime.fromtimestamp(self.pick_datetime).strftime('%Y-%m-%d')
    #             self.before_datetime = str(self.search_datetime) + 'T00:00:00'
    #             self.after_datetime = str(self.search_datetime) + 'T23:59:59'
    #     print(self.before_datetime,self.after_datetime)
    #     print(self.pick_datetime)
    #     arr_list_sum = []
    #     sum_row_tooffset = 0
    #     keep_lenstatus = []
    #     list_arr = []
    #     tmp_sid_code_list =  []
    #     tmp_list = []      
    #     a = 0       
    #     count_rowDocument = 0
    #     count_rowDocument_StatusActive = 0
    #     count_rowDocument_StatusReject = 0
    #     count_rowDocument_StatusCancel = 0
    #     statusFile_count_approve = 0
    #     statusFile_count_pendding = 0
    #     statusFile_count_reject = 0
    #     statusFile_count_wait = 0
    #     list_temp_query = []
    #     tmp_sid_code_list = []
    #     arr_gruop = []
    #     arr_group_sid = []
    #     tmp_arr_sid = []
    #     tmp_group_id = None
    #     json_Data = {}
    #     str_time = (time.time())
    #     if self.sort_key == None:
    #         ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
    #     else:
    #         if self.sort_key == 'desc':
    #             ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
    #         else:
    #             ORDER_sql = ' ORDER BY "tb_send_detail".send_time ASC LIMIT :limit OFFSET :offset '
    #     where_sql = 'WHERE status=:status AND "send_user"=:send_user '
    #     if self.tax_id != '':
    #         where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id
    #     else:
    #         where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR "tb_step_data".biz_info = :biz_info)'
    #     if self.pick_datetime != None:
    #         where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) ' 
    #     if typequery == 'sender':            
    #         if self.group_status == "true":
    #             where_sql += ' AND ("tb_send_detail"."group_id" = :group_statustmp OR "tb_send_detail"."group_id" IS NULL) '
    #         where_sql += ORDER_sql
    #         with slave.connect() as connection:
    #             result = connection.execute(text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid '+ where_sql )\
    #                 ,status=status_ACTIVE,send_user=self.username,limit=self.limit,offset=self.offset,biz_info='',biz_info_none='None',group_statustmp=[],group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
    #             connection.close()
    #         query = [dict(row) for row in result]
    #         print('sender len query',len(query))
    #     elif typequery == 'sender_filter':
    #         if self.status in self.all_status:
    #             for i in range(self.limit):
    #                 if i > 0:
    #                     self.offset = self.offset + self.limit
    #                 if len(arr_list_sum) < self.limit:
    #                     arr_list_sum,sum_row_tooffset = recursive_sender_status_new_v1(self.username,self.email_one,self.limit,self.offset,self.status,arr_list_sum,sum_row_tooffset,self.document_type,self.tax_id,self.group_status)
    #                     keep_lenstatus = arr_list_sum
    #                     sum_row_tooffset = self.offset + sum_row_tooffset
    #                     if len(keep_lenstatus) == len(arr_list_sum):
    #                         a = a + 1
    #                         if a == 5:
    #                             list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
    #                             json_Data['document'] = list_arr
    #                             json_Data['offset'] = sum_row_tooffset
    #                             return {'result':'OK','messageText':json_Data}                    
    #                 else:
    #                     list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
    #                     json_Data['document'] = list_arr
    #                     json_Data['offset'] = sum_row_tooffset
    #                     return {'result':'OK','messageText':json_Data} 
    #             list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
    #             json_Data['document'] = list_arr
    #             json_Data['offset'] = sum_row_tooffset
    #             print(len(list_arr))
    #             return {'result':'OK','messageText':json_Data}
    #         if self.status != '':
    #             where_sql += ' AND "tb_send_detail"."document_status" = :document_status '
    #         if self.document_type != '':
    #             where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
    #         if self.group_status == "true":
    #             where_sql += ' AND ("tb_send_detail"."group_id" = :group_statustmp OR "tb_send_detail"."group_id" IS NULL) '
    #         if self.pick_datetime != None:
    #             where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) ' 
    #         where_sql += ORDER_sql
    #         text_sql = text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
    #             INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #             INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #         print(text_sql , self.status)
    #         with slave.connect() as connection:
    #             result = connection.execute(text_sql\
    #                 ,status=status_ACTIVE,send_user=self.username,limit=self.limit,offset=self.offset,documentType=self.document_type,document_status=self.status,biz_info='',biz_info_none='None',group_statustmp=[],group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
    #             connection.close()
    #         query = [dict(row) for row in result]
    #     elif typequery == 'sender_search':
    #         if self.document_type != '':
    #             where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
    #         if self.keyword != '':
    #             where_sql += 'AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword) '
    #         if self.pick_datetime != None:
    #             where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) ' 
    #         where_sql += ORDER_sql
    #         text_sql = text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
    #             INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #             INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #         with slave.connect() as connection:
    #             result = connection.execute(text_sql\
    #                 ,status=status_ACTIVE,send_user=self.username,limit=self.limit,offset=self.offset,documentType=self.document_type,keyword=search_keyword,biz_info='',biz_info_none='None',group_statustmp='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
    #             connection.close()
    #         query = [dict(row) for row in result]
    #     # print('len sender',len(query))
    #     try:
    #         for x in range(len(query)):
    #             arr_email_document = []
    #             tmp_req_email = []
    #             email_step_sum_w = []
    #             tmp_dict_json = query[x]
    #             tmp_document_type = None
    #             tmp_sicode = tmp_dict_json['step_data_sid']
    #             tmp_sid_code_list.append(tmp_sicode)
    #             tmp_send_time = tmp_dict_json['send_time']
    #             tmp_document_id = tmp_dict_json['doc_id']
    #             tmp_tracking_id = tmp_dict_json['tracking_id']
    #             tmp_sender_name = tmp_dict_json['sender_name']
    #             tmp_sender_email = tmp_dict_json['sender_email']
    #             tmp_file_name = tmp_dict_json['file_name']
    #             tmp_groupid = tmp_dict_json['group_id']
    #             email_step_sum = tmp_dict_json['recipient_email']
    #             if email_step_sum != None:
    #                 email_step_sum = eval(email_step_sum)
    #             # print(email_step_sum)
    #             tmpstatus_detail = tmp_dict_json['status_details']
    #             tmpdocument_status = tmp_dict_json['document_status']
    #             tmpstepnow = tmp_dict_json['stepnow']
    #             status_groupid = False
    #             if tmp_groupid != None:
    #                 tmp_groupid = eval(tmp_groupid)
    #                 if len(tmp_groupid) != 0:
    #                     status_groupid = True
    #             if tmpstepnow != None:
    #                 tmpstepnow = int(tmpstepnow)
    #             tmpstepmax = tmp_dict_json['stepmax']
    #             if tmpstepmax != None:
    #                 tmpstepmax = int(tmpstepmax)
    #             if tmpstatus_detail != None:
    #                 tmpstatus_detail = eval(tmpstatus_detail)                            
    #                 for z in range(len(tmpstatus_detail)):
    #                     email_step_sum_w.append(tmpstatus_detail[z]['email'])

    #                 if tmpdocument_status == 'N':
    #                     for x in range(len(tmpstatus_detail)):
    #                         if self.email_one not in arr_email_document:
    #                             if self.email_one in tmpstatus_detail[x]['email']:
    #                                 if tmpstatus_detail[x]['step_status_code'] == 'W':
    #                                     arr_email_document.append(self.email_one)
    #                                     tmpdocument_status = tmpstatus_detail[x]['step_status_code']
    #                                     break
    #                                 else:
    #                                     tmpdocument_status = tmpstatus_detail[x]['step_status_code']
    #             if tmpdocument_status == 'Z':
    #                 res_status_file_string = 'อยู่ในช่วงดำเนินการ'
    #             elif tmpdocument_status == 'W':
    #                 res_status_file_string = 'รอคุณอนุมัติ'
    #             elif tmpdocument_status == 'N':
    #                 res_status_file_string = 'กำลังดำเนินการ'
    #             elif tmpdocument_status == 'R':
    #                 res_status_file_string = 'เอกสารที่ส่งคืนแก้ไข'
    #             else:
    #                 res_status_file_string = 'เอกสารสมบูรณ์'
    #             tmp_sign_page_options = tmp_dict_json['sign_page_options']
    #             tmp_document_type = tmp_dict_json['documentType']
    #             tmp_options_page = []
    #             if tmp_dict_json['options_page'] != None:
    #                 if tmp_dict_json['options_page'] != '':
    #                     tmp_options_page = [eval(tmp_dict_json['options_page'])]
    #             else:
    #                 tmp_options_page = []
    #             if len(tmp_options_page) != 0:
    #                 tmp_status_group = False
    #                 if status_groupid == True:
    #                     if len(tmp_options_page) != 0:
    #                         if 'group_detail' in tmp_options_page[0]:
    #                             tmp_group_detail = tmp_options_page[0]['group_detail']
    #                             if 'group_status' in tmp_group_detail:
    #                                 if tmp_group_detail['group_status'] == True:
    #                                     tmp_status_group = True
    #                                     tmpstepnum = tmp_group_detail['step_num']
    #             if tmp_dict_json['documentJson'] != None:
    #                 documentJson_result = eval(tmp_dict_json['documentJson'])
    #                 documentName = documentJson_result['document_name']
    #                 documentType = documentJson_result['document_type']
    #             else:
    #                 documentName = None
    #                 documentType = None
    #             if tmp_dict_json['urgent_type'] != None:
    #                 documentUrgentType = tmp_dict_json['urgent_type']
    #                 if documentUrgentType == 'I':
    #                     documentUrgentString = 'ด่วนมาก'
    #                 elif documentUrgentType == 'U':
    #                     documentUrgentString = 'ด่วน'
    #                 elif documentUrgentType == 'M':
    #                     documentUrgentString = 'ปกติ'
    #             tmp_biz_info = None
    #             tmprole_name = None
    #             tmprole_level = None
    #             tmpdept_name = None
    #             # แก้
    #             if self.tax_id != '':
    #                 eval_biz_info = json.dumps(tmp_dict_json['biz_info'])
    #                 eval_biz_info = json.loads(eval_biz_info)
    #                 eval_biz_info = eval(eval_biz_info)
    #                 if 'role_name' in eval_biz_info:
    #                     tmprole_name = eval_biz_info['role_name']
    #                 if 'role_level' in eval_biz_info:
    #                     tmprole_level = eval_biz_info['role_level']
    #                 if 'dept_name' in eval_biz_info:
    #                     tmpdept_name = eval_biz_info['dept_name']
    #                 if 'dept_name' in eval_biz_info:                        
    #                     tmp_biz_info = {
    #                         'tax_id':eval_biz_info['id_card_num'],
    #                         'role_name' : tmprole_name,
    #                         'dept_name' : tmpdept_name,
    #                         'role_level' : tmprole_level            
    #                     }                                
    #                 elif 'dept_name' not in eval_biz_info:
    #                     tmp_biz_info = {
    #                         'tax_id':eval_biz_info['id_card_num'],
    #                         'role_name' : tmprole_name,
    #                         'dept_name' : [],
    #                         'role_level' : tmprole_level            
    #                     }
                            
    #             dateTime_String = tmp_send_time
    #             th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
    #             ts = int(time.time())
    #             date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    #             year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
    #             datetime_display = int(dateTime_String.timestamp())
    #             date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
    #             yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
    #             time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
    #             old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
    #             if date_time_today == date_time_db:
    #                 date_display_show = time_show_db
    #             else:
    #                 if year_today == yar_db:
    #                     date_display_show = convert_datetime_TH_2_display(datetime_display)
    #                 else:
    #                     date_display_show = old_year
    #             try:
    #                 if tmp_status_group == True:
    #                     for ui in range(len(tmpstepnum)):
    #                         intstepnum = tmpstepnum[ui] - 1
    #                         # print(intstepnum)
    #                         for w in range(len(email_step_sum_w[intstepnum])):
    #                             tmp_req_email.append(email_step_sum_w[intstepnum][w])
    #             except Exception as e:
    #                 tmp_req_email = []
    #             list_arr.append({
    #                 'group_email':tmp_req_email,
    #                 'group_id':None,
    #                 'group_status':tmp_status_group,
    #                 'sidCode':tmp_sicode,
    #                 'document_name':documentName,
    #                 'document_type':tmp_document_type,
    #                 'document_urgent':documentUrgentType,
    #                 'document_urgent_string':documentUrgentString,
    #                 'dateTime_String':str(dateTime_String).split('+')[0],
    #                 'dateTime_String_TH_1':th_dateTime_2,
    #                 'dateTime_display':date_display_show,
    #                 'document_id':tmp_document_id,
    #                 'stamp_all':tmp_sign_page_options,
    #                 'options_page_document':tmp_options_page,
    #                 'max_step':tmpstepmax,
    #                 'step_now':tmpstepnow,
    #                 'date_String':str(dateTime_String).split(' ')[0],
    #                 'time_String':str(dateTime_String).split(' ')[1].split('+')[0],
    #                 'status_file_code':tmpdocument_status,
    #                 'status_file_string':res_status_file_string,
    #                 'dateTime':int(dateTime_String.timestamp()),
    #                 'tracking_id':tmp_tracking_id,
    #                 'sender_name':tmp_sender_name,
    #                 'sender_email':tmp_sender_email,
    #                 'file_name':tmp_file_name,
    #                 'document_business':tmp_biz_info
    #             })
    #         list_arr = sorted(list_arr, key=lambda k: k['dateTime'], reverse=True)
    #         json_Data['document'] = list_arr
    #         return {'result':'OK','messageText':json_Data}
    #     except Exception as e:
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         print(exc_type, fname, exc_tb.tb_lineno)
    #         return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(e)} 

    

    def select_document_sender_count_v1(self,typequery,username,email_one,document_type,tax_id,keyword,group_status=None,pick_datetime=None):
        self.typequery = typequery
        self.username = username
        self.email_one = email_one
        self.document_type = document_type
        self.tax_id = tax_id
        self.keyword = keyword
        self.group_status = group_status
        self.pick_datetime = pick_datetime
        self.before_datetime = None
        self.after_datetime = None
        sid_list = []
        sid_list_email = []
        json_Data = {}
        list_arr = []
        list_json = []
        tmp_list = []
        status_ACTIVE = 'ACTIVE'
        count_rowDocument = 0
        count_rowDocument_StatusActive = 0
        count_rowDocument_StatusReject = 0
        count_rowDocument_StatusCancel = 0
        statusFile_count_approve = 0
        statusFile_count_pendding = 0
        statusFile_count_reject = 0
        statusFile_count_wait = 0
        statusFile_count_Z = 0
        list_temp_query = []
        tmp_sid_code_list = []
        arr_gruop = []
        arr_group_sid = []
        tmp_arr_sid = []
        tmp_group_id = None
        query_temp = 0
        str_time = (time.time())
        # search = "%'{}'%".format(self.email_one) 
        search_tax_id = "'%''{}''%'".format(self.tax_id)
        search_keyword = "%{}%".format(self.keyword)
        if self.pick_datetime != None:
            if self.pick_datetime != "":
                self.pick_datetime = int(self.pick_datetime)
                self.search_datetime = datetime.datetime.fromtimestamp(self.pick_datetime).strftime('%Y-%m-%d')
                self.before_datetime = str(self.search_datetime) + 'T00:00:00'
                self.after_datetime = str(self.search_datetime) + 'T23:59:59'
        print(self.before_datetime,self.after_datetime)
        print(self.pick_datetime)
        ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
        where_sql = 'WHERE status=:status AND "send_user"=:send_user' 
        if self.tax_id != '':
            where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
        else:
            where_sql += ''
        if self.document_type != '':     
            where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
        if self.keyword != '':
            where_sql += ' AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword)'  
        if self.group_status == "true":
            where_sql += ' AND ("tb_send_detail"."group_id" =:group_idtmp OR "tb_send_detail"."group_id" IS NULL)'            
        if self.pick_datetime != None:
            where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '  
        text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
            INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
            INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
        if typequery == 'sender_sum':
            ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
            where_sql = 'WHERE status=:status AND "send_user"=:send_user '
            if self.tax_id != '':
                where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id    
            if self.pick_datetime != None:
                where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '  
            with slave.connect() as connection:
                result_all = connection.execute(text_sql \
                    ,status=status_ACTIVE,send_user=username,document_type=self.document_type,biz_info_none='None',biz_info='',group_idtmp=[],before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                where_sql += ' AND "tb_send_detail".document_status=:r_status'   
                if self.tax_id != '':
                    where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
                else:
                    where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)' 
                if self.group_status == "true":
                    where_sql += ' AND ("tb_send_detail"."group_id" =:group_idtmp OR "tb_send_detail"."group_id" IS NULL)'       
                text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                # ---------------------------------
                # text_sql_str = text('SELECT "tb_send_detail".* FROM "tb_send_detail" \
                #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                # ---------------------------------
                text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                    "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                    "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                    "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                    "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                    "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                    "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
                    FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                result_r = connection.execute(text_sql \
                    ,status=status_ACTIVE,send_user=username,r_status='R',biz_info_none='None',biz_info='',group_idtmp=[],before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                result_y = connection.execute(text_sql \
                    ,status=status_ACTIVE,send_user=username,r_status='Y',biz_info_none='None',biz_info='',group_idtmp=[],before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                result_n = connection.execute(text_sql_str \
                    ,status=status_ACTIVE,send_user=username,r_status='N',biz_info_none='None',biz_info='',group_idtmp=[],before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query_temp = [dict(row) for row in result_all]
            statusFile_count_reject = [dict(row) for row in result_r]
            statusFile_count_approve = [dict(row) for row in result_y]
            query = [dict(row) for row in result_n]
        elif typequery == 'sender_sum_filter':
            ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC '
            where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
            if self.pick_datetime != None:
                where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '  
            with slave.connect() as connection:
                result_all = connection.execute(text_sql \
                    ,status=status_ACTIVE,send_user=username,document_type=self.document_type,biz_info_none='None',biz_info='',group_idtmp=[],before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                # print(text_sql)
                where_sql += ' AND "tb_send_detail".document_status=:r_status'
                if self.tax_id != '':
                    where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
                else:
                    where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'   
                text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                # -------------------------------------------------------
                # text_sql_str = text('SELECT "tb_send_detail".* FROM "tb_send_detail" \
                #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                # -------------------------------------------------------
                text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                    "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                    "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                    "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                    "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                    "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                    "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
                    FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                result_r = connection.execute(text_sql \
                    ,status=status_ACTIVE,send_user=username,r_status='R',document_type=self.document_type,biz_info_none='None',biz_info='',group_idtmp='[]',before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                result_y = connection.execute(text_sql \
                    ,status=status_ACTIVE,send_user=username,r_status='Y',document_type=self.document_type,biz_info_none='None',biz_info='',group_idtmp='[]',before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                result_n = connection.execute(text_sql_str \
                    ,status=status_ACTIVE,send_user=username,r_status='N',document_type=self.document_type,biz_info_none='None',biz_info='',group_idtmp='[]',before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query_temp = [dict(row) for row in result_all]
            statusFile_count_reject = [dict(row) for row in result_r]
            statusFile_count_approve = [dict(row) for row in result_y]
            query = [dict(row) for row in result_n]
        elif typequery == 'sender_sum_search':
            ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
            where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
            if self.pick_datetime != None:
                where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '  
            with slave.connect() as connection:
                result_all = connection.execute(text_sql \
                    ,status=status_ACTIVE,send_user=username,document_type=self.document_type,biz_info_none='None',biz_info='',keyword=search_keyword,group_idtmp=[],before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                # print(text_sql)
                where_sql += ' AND "tb_send_detail".document_status=:r_status'
                if self.tax_id != '':
                    where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
                else:
                    where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'     
                if self.keyword != '':
                    where_sql += ' AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword) '  
                if self.document_type != '':     
                    where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
                # if self.tax_id != '':
                #     where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
                # else:
                #     where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'   
                text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                    "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                    "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                    "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                    "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                    "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                    "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
                    FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                result_r = connection.execute(text_sql \
                    ,status=status_ACTIVE,send_user=username,r_status='R',document_type=self.document_type,biz_info_none='None',biz_info='',keyword=search_keyword,group_idtmp=[],before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                result_y = connection.execute(text_sql \
                    ,status=status_ACTIVE,send_user=username,r_status='Y',document_type=self.document_type,biz_info_none='None',biz_info='',keyword=search_keyword,group_idtmp=[],before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                result_n = connection.execute(text_sql_str \
                    ,status=status_ACTIVE,send_user=username,r_status='N',document_type=self.document_type,biz_info_none='None',biz_info='',keyword=search_keyword,group_idtmp=[],before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query_temp = [dict(row) for row in result_all]
            statusFile_count_reject = [dict(row) for row in result_r]
            statusFile_count_approve = [dict(row) for row in result_y]
            query = [dict(row) for row in result_n]
        
        print(statusFile_count_reject , statusFile_count_approve)
        statusFile_count_reject = statusFile_count_reject[0]['count']
        statusFile_count_approve = statusFile_count_approve[0]['count']
        query_temp = query_temp[0]['count']
        try:
            end_time = (time.time())
            arr = []
            for u in range(len(query)):
                arr_email_document = []
                tmp_req_email = []
                tmp_dict_json = query[u]
                tmpdocument_status = tmp_dict_json['document_status']
                tmpstatus_detail = tmp_dict_json['status_details']
                if tmpstatus_detail != None:
                    tmpstatus_detail = eval(tmpstatus_detail)
                    if tmpdocument_status == 'N':
                        for x in range(len(tmpstatus_detail)):
                            if self.email_one not in arr_email_document:
                                if self.email_one in tmpstatus_detail[x]['email']:
                                    if tmpstatus_detail[x]['step_status_code'] == 'W':
                                        arr_email_document.append(self.email_one)
                                        tmpdocument_status = tmpstatus_detail[x]['step_status_code']
                                        break
                                    else:
                                        tmpdocument_status = tmpstatus_detail[x]['step_status_code']
                        
                if tmpdocument_status == 'W':
                    statusFile_count_wait = statusFile_count_wait + 1
                elif tmpdocument_status == 'Z':
                    statusFile_count_Z = statusFile_count_Z + 1
                else:
                    statusFile_count_pendding = statusFile_count_pendding + 1
            json_Data['status_document']  = {
                'status_z':statusFile_count_Z,
                'incomplete':statusFile_count_pendding,
                'complete':statusFile_count_approve,
                'reject':statusFile_count_reject,
                'wait':statusFile_count_wait
            }
            json_Data['sum_document'] = query_temp
            return {'result':'OK','messageText':json_Data}
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(ex)}
        

    # def select_document_sender_count_v1(self,typequery,username,email_one,document_type,tax_id,keyword,group_status=None):
    #     self.typequery = typequery
    #     self.username = username
    #     self.email_one = email_one
    #     self.document_type = document_type
    #     self.tax_id = tax_id
    #     self.keyword = keyword
    #     self.group_status = group_status
    #     sid_list = []
    #     sid_list_email = []
    #     json_Data = {}
    #     list_arr = []
    #     list_json = []
    #     tmp_list = []
    #     status_ACTIVE = 'ACTIVE'
    #     count_rowDocument = 0
    #     count_rowDocument_StatusActive = 0
    #     count_rowDocument_StatusReject = 0
    #     count_rowDocument_StatusCancel = 0
    #     statusFile_count_approve = 0
    #     statusFile_count_pendding = 0
    #     statusFile_count_reject = 0
    #     statusFile_count_wait = 0
    #     statusFile_count_Z = 0
    #     list_temp_query = []
    #     tmp_sid_code_list = []
    #     arr_gruop = []
    #     arr_group_sid = []
    #     tmp_arr_sid = []
    #     tmp_group_id = None
    #     query_temp = 0
    #     str_time = (time.time())
    #     # search = "%'{}'%".format(self.email_one) 
    #     search_tax_id = "'%''{}''%'".format(self.tax_id)
    #     search_keyword = "%{}%".format(self.keyword)
    #     ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
    #     where_sql = 'WHERE status=:status AND "send_user"=:send_user' 
    #     if self.tax_id != '':
    #         where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
    #     else:
    #         where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'
    #     if self.document_type != '':     
    #         where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
    #     if self.keyword != '':
    #         where_sql += ' AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword)'  
    #     if self.group_status == "true":
    #         where_sql += ' AND ("tb_send_detail"."group_id" =:group_idtmp OR "tb_send_detail"."group_id" IS NULL)'            
    #     text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
    #         INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #         INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #     if typequery == 'sender_sum':
    #         ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
    #         where_sql = 'WHERE status=:status AND "send_user"=:send_user '
    #         if self.tax_id != '':
    #             where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id    
    #         with slave.connect() as connection:
    #             result_all = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,send_user=username,document_type=self.document_type,biz_info_none='None',biz_info='',group_idtmp=[])
    #             where_sql += ' AND "tb_send_detail".document_status=:r_status'   
    #             if self.tax_id != '':
    #                 where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
    #             else:
    #                 where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)' 
    #             if self.group_status == "true":
    #                 where_sql += ' AND ("tb_send_detail"."group_id" =:group_idtmp OR "tb_send_detail"."group_id" IS NULL)'       
    #             text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             # ---------------------------------
    #             # text_sql_str = text('SELECT "tb_send_detail".* FROM "tb_send_detail" \
    #             #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #             #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             # ---------------------------------
    #             text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                 "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                 "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                 "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                 "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                 "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                 "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
    #                 FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             result_r = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,send_user=username,r_status='R',biz_info_none='None',biz_info='',group_idtmp=[])
    #             result_y = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,send_user=username,r_status='Y',biz_info_none='None',biz_info='',group_idtmp=[])
    #             result_n = connection.execute(text_sql_str \
    #                 ,status=status_ACTIVE,send_user=username,r_status='N',biz_info_none='None',biz_info='',group_idtmp=[])
    #             connection.close()
    #         query_temp = [dict(row) for row in result_all]
    #         statusFile_count_reject = [dict(row) for row in result_r]
    #         statusFile_count_approve = [dict(row) for row in result_y]
    #         query = [dict(row) for row in result_n]
    #     elif typequery == 'sender_sum_filter':
    #         ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC '
    #         where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
    #         with slave.connect() as connection:
    #             result_all = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,send_user=username,document_type=self.document_type,biz_info_none='None',biz_info='',group_idtmp=[])
    #             print(text_sql)
    #             where_sql += ' AND "tb_send_detail".document_status=:r_status'
    #             if self.tax_id != '':
    #                 where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
    #             else:
    #                 where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'   
    #             text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             # -------------------------------------------------------
    #             # text_sql_str = text('SELECT "tb_send_detail".* FROM "tb_send_detail" \
    #             #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #             #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             # -------------------------------------------------------
    #             text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                 "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                 "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                 "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                 "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                 "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                 "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
    #                 FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             result_r = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,send_user=username,r_status='R',document_type=self.document_type,biz_info_none='None',biz_info='',group_idtmp='[]')
    #             result_y = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,send_user=username,r_status='Y',document_type=self.document_type,biz_info_none='None',biz_info='',group_idtmp='[]')
    #             result_n = connection.execute(text_sql_str \
    #                 ,status=status_ACTIVE,send_user=username,r_status='N',document_type=self.document_type,biz_info_none='None',biz_info='',group_idtmp='[]')
    #             connection.close()
    #         query_temp = [dict(row) for row in result_all]
    #         statusFile_count_reject = [dict(row) for row in result_r]
    #         statusFile_count_approve = [dict(row) for row in result_y]
    #         query = [dict(row) for row in result_n]
    #     elif typequery == 'sender_sum_search':
    #         ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
    #         where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
    #         with slave.connect() as connection:
    #             result_all = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,send_user=username,document_type=self.document_type,biz_info_none='None',biz_info='',keyword=search_keyword,group_idtmp=[])
    #             print(text_sql)
    #             where_sql += ' AND "tb_send_detail".document_status=:r_status'
    #             if self.tax_id != '':
    #                 where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
    #             else:
    #                 where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'     
    #             if self.keyword != '':
    #                 where_sql += ' AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword) '  
    #             if self.document_type != '':     
    #                 where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
    #             # if self.tax_id != '':
    #             #     where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
    #             # else:
    #             #     where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'   
    #             text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                 "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                 "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                 "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                 "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                 "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                 "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
    #                 FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             result_r = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,send_user=username,r_status='R',document_type=self.document_type,biz_info_none='None',biz_info='',keyword=search_keyword,group_idtmp=[])
    #             result_y = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,send_user=username,r_status='Y',document_type=self.document_type,biz_info_none='None',biz_info='',keyword=search_keyword,group_idtmp=[])
    #             result_n = connection.execute(text_sql_str \
    #                 ,status=status_ACTIVE,send_user=username,r_status='N',document_type=self.document_type,biz_info_none='None',biz_info='',keyword=search_keyword,group_idtmp=[])
    #             connection.close()
    #         query_temp = [dict(row) for row in result_all]
    #         statusFile_count_reject = [dict(row) for row in result_r]
    #         statusFile_count_approve = [dict(row) for row in result_y]
    #         query = [dict(row) for row in result_n]
        
    #     print(statusFile_count_reject , statusFile_count_approve)
    #     statusFile_count_reject = statusFile_count_reject[0]['count']
    #     statusFile_count_approve = statusFile_count_approve[0]['count']
    #     query_temp = query_temp[0]['count']
    #     try:
    #         end_time = (time.time())
    #         arr = []
    #         for u in range(len(query)):
    #             arr_email_document = []
    #             tmp_req_email = []
    #             tmp_dict_json = query[u]
    #             tmpdocument_status = tmp_dict_json['document_status']
    #             tmpstatus_detail = tmp_dict_json['status_details']
    #             if tmpstatus_detail != None:
    #                 tmpstatus_detail = eval(tmpstatus_detail)
    #                 if tmpdocument_status == 'N':
    #                     for x in range(len(tmpstatus_detail)):
    #                         if self.email_one not in arr_email_document:
    #                             if self.email_one in tmpstatus_detail[x]['email']:
    #                                 if tmpstatus_detail[x]['step_status_code'] == 'W':
    #                                     arr_email_document.append(self.email_one)
    #                                     tmpdocument_status = tmpstatus_detail[x]['step_status_code']
    #                                     break
    #                                 else:
    #                                     tmpdocument_status = tmpstatus_detail[x]['step_status_code']
                        
    #             if tmpdocument_status == 'W':
    #                 statusFile_count_wait = statusFile_count_wait + 1
    #             elif tmpdocument_status == 'Z':
    #                 statusFile_count_Z = statusFile_count_Z + 1
    #             else:
    #                 statusFile_count_pendding = statusFile_count_pendding + 1
    #         json_Data['status_document']  = {
    #             'status_z':statusFile_count_Z,
    #             'incomplete':statusFile_count_pendding,
    #             'complete':statusFile_count_approve,
    #             'reject':statusFile_count_reject,
    #             'wait':statusFile_count_wait
    #         }
    #         json_Data['sum_document'] = query_temp
    #         return {'result':'OK','messageText':json_Data}
    #     except Exception as ex:
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         print(exc_type, fname, exc_tb.tb_lineno)
    #         return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(ex)}
    
    def select_document_v2(self,date_start,date_end,document_id,sender_email,recipient_email,tax_id,documentType,limit,text):
        tmp_list_result = []
        tmp_list_result2 = []
        self.date_start = date_start
        self.date_end = date_end
        self.document_id = document_id
        self.sender_email = sender_email
        self.recipient_email = recipient_email
        self.tax_id = tax_id
        self.documentType = documentType
        self.limit = limit
        self.text = text
        limit_ch = self.limit
        tmp_list_sid_code = []
        count_document = 0
        count_rowDocument = 0
        count_rowDocument_StatusActive = 0
        count_rowDocument_StatusReject = 0
        count_rowDocument_StatusCancel = 0
        statusFile_count_approve = 0
        statusFile_count_pendding = 0
        statusFile_count_reject = 0
        statusFile_count_wait = 0
        step_time = []

        step_time_total = []
        t1 = None
        t2 = None

        sum_Document = 0
        Complete_Approve = 0
        Incomplete_Pendding = 0
        Reject = 0
        Wait = 0

        query_document_tmp = None
        query_document_tmp2 = None

        query_document_tmp_Active = 0
        query_document_tmp_Reject = 0
        query_document_tmp_count = 0

        try:

            if (limit_ch == ''):
                limit_ch = 1000
            elif (limit_ch != ''):
                limit_ch = self.limit
                if limit_ch > 1000:
                    limit_ch = 1000

            
            # query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').count()
            # query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').count()
           
            
            if self.tax_id == 'citizen' :
                if self.tax_id != '' and self.text != '' and self.document_id == '' and self.sender_email == '' and self.recipient_email == '' and self.documentType == '':
                    query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.options_page.contains(self.text)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).limit(limit_ch).all()
                    query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.options_page.contains(self.text)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                    query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.options_page.contains(self.text)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                    print('citizen tax_id,text')
                elif self.date_start != '' and self.date_end != '' : # date_start ไม่ว่าง , date_end ไม่ว่าง
                    if self.document_id =='':
                        if self.sender_email != '' and self.tax_id != '' and self.recipient_email != '' and self.documentType != '': # ใส่ทั้งหมด
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                            # query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()

                            query_document_tmp2 = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            eval_biz_info = eval(query_document_tmp2[0].biz_info)
                            # print ('eval_biz_info: ',eval_biz_info['id_card_num'])
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                            print('all put')

                        elif self.sender_email != '': # ใส่ sender_email

                            if self.sender_email != '' and self.tax_id != '' and self.recipient_email == '' and self.documentType != '': # ไม่ใส่ recipient_email
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                                # query_document_tmp2 = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                                # eval_biz_info = eval(query_document_tmp2[0].biz_info)
                                # query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType.contains(self.documentType)).filter(eval_biz_info['id_card_num'] == self.tax_id).limit(limit_ch).all()

                                print('non recipient')

                            elif self.tax_id == '' and self.recipient_email != '' and self.documentType != '': # ไม่ใส่ tax_id
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).count()
                                print('non tax')

                            elif self.documentType == '' and self.recipient_email != '' and self.tax_id != '': # ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                print('non documentType')

                            elif self.tax_id == '' and self.recipient_email == '' and self.documentType != '': # ไม่ใส่ recipient_email // ไม่ใส่ tax_id
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).count()
                                print('only sender , documentType')

                            elif self.documentType == '' and self.recipient_email == '' and self.tax_id != '': # ไม่ใส่ recipient_email // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                print('only sender , tax_id')

                            elif self.tax_id == '' and self.documentType == '' and self.recipient_email == '': # ไม่ใส่ tax_id // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                print('only sender , recipient_email')

                            elif self.tax_id == '' and self.recipient_email == '' and self.documentType == '': # ไม่ใส่ recipient_email // ไม่ใส่ tax_id // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).count()
                                print('only sender')

                        elif self.recipient_email != '': # ใส่ recipient_email

                            if self.tax_id != '' and self.sender_email == '' and self.documentType == '': # ไม่ใส่ sender_email // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                print('non sender_email ,documentType')

                            elif self.tax_id == '' and self.sender_email == '' and self.documentType != '':# ไม่ใส่ sender_email // ไม่ใส่ tax_id
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                print('only recipient , documentType')

                            elif self.tax_id == '' and self.sender_email == '' and self.documentType == '':# ไม่ใส่ sender_email // ไม่ใส่ tax_id // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                print('only recipient')

                        elif self.tax_id == '' and self.recipient_email == '' and self.sender_email == '' and self.documentType != '': # ใส่ documentType
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.documentType.contains(self.documentType)).count()
                            print('only documenType')

                        elif self.tax_id != '' and self.recipient_email == ''and self.sender_email == ''and self.documentType == '': # ใส่ tax_id
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                            print('tax_id')

                        elif self.tax_id != '' and self.recipient_email == ''and self.sender_email == ''and self.documentType != '': # ใส่ tax_id,documentType
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                            print('tax_id , documenType')

                        elif self.sender_email == '' and self.tax_id == '' and self.recipient_email == ''and self.documentType == '': #ไม่ใส่อะไรเลย
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).count()
                            print('non put')

                    elif self.document_id != '':# กรอกช่อง id
                        date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                        date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                        co_str = len(self.document_id)
                        # print (co_str)
                        if co_str > 13 : # ใส่ doc_id
                            # print ('doc_id')
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.doc_id.contains(self.document_id)).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.doc_id.contains(self.document_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.doc_id.contains(self.document_id)).count()
                        elif co_str <= 13 : # ใส่ tracking_id
                            # print ('tracking_id')
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.tracking_id.contains(self.document_id)).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.tracking_id.contains(self.document_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.tracking_id.contains(self.document_id)).count()
                        print ('have id')
                elif self.date_start != '' and self.date_end == '' : # date_start ไม่ว่าง , date_end ว่าง
                    if self.document_id =='':
                        if self.sender_email != '' and self.tax_id != '' and self.recipient_email != ''and self.documentType != '': # ใส่ทั้งหมด
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                            query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                            print('all put2')

                        elif self.sender_email != '': # ใส่ sender_email

                            if self.tax_id != '' and self.recipient_email == '' and self.documentType != '': # ไม่ใส่ recipient_email
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                                print('non recipient2')

                            elif self.tax_id == '' and self.recipient_email != '' and self.documentType != '': # ไม่ใส่ tax_id
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).count()
                                print('non tax2')

                            elif self.documentType == '' and self.recipient_email != '' and self.tax_id != '': # ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                print('non documentType2')

                            elif self.tax_id == '' and self.recipient_email == '' and self.documentType != '': # ไม่ใส่ recipient_email // ไม่ใส่ tax_id
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).count()
                                print('only sender , documentType2')

                            elif self.documentType == '' and self.recipient_email == '' and self.tax_id != '': # ไม่ใส่ recipient_email // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                print('only sender , tax_id 2')

                            elif self.tax_id == '' and self.documentType == '' and self.recipient_email != '': # ไม่ใส่ tax_id // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                print('only sender , recipient_email2')

                            elif self.tax_id == '' and self.recipient_email == '' and self.documentType == '': # ไม่ใส่ recipient_email // ไม่ใส่ tax_id // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).count()
                                print('only sender2')

                        elif self.recipient_email != '': # ใส่ recipient_email

                            if self.tax_id != '' and self.sender_email == '' and self.documentType == '': # ไม่ใส่ sender_email // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                print('non sender_email2')

                            elif self.tax_id == '' and self.sender_email == '' and self.documentType != '':# ไม่ใส่ sender_email // ไม่ใส่ tax_id
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                print('only recipient , documentType2')

                            elif self.tax_id == '' and self.sender_email == '' and self.documentType == '':# ไม่ใส่ sender_email // ไม่ใส่ tax_id // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                print('only recipient2')

                        elif self.tax_id == '' and self.recipient_email == ''and self.sender_email == ''and self.documentType != '': # ใส่ documentType
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                            query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.documentType.contains(self.documentType)).count()
                            print('only documenType2')

                        elif self.tax_id != '' and self.recipient_email == '' and self.sender_email == '' and self.documentType == '': # ใส่ tax_id
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                            query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                            print('tax_id2')

                        elif self.tax_id != '' and self.recipient_email == ''and self.sender_email == ''and self.documentType != '': # ใส่ tax_id,documentType
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                            query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                            print('tax_id , documenType2')

                        elif self.sender_email == '' and self.tax_id == '' and self.recipient_email == '': #ไม่ใส่อะไรเลย
                            date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time>=date_start_tmp).filter(view_document.send_time<=date_end_tmp).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time>=date_start_tmp).filter(view_document.send_time<=date_end_tmp).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time>=date_start_tmp).filter(view_document.send_time<=date_end_tmp).count()
                            print('non put2')

                    elif self.document_id != '':# กรอกช่อง id
                        date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                        co_str = len(self.document_id)
                        # print (co_str)
                        if co_str > 13 : # ใส่ doc_id
                            # print ('doc_id')
                            query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time>=date_start_tmp).filter(view_document.doc_id.contains(self.document_id)).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time>=date_start_tmp).filter(view_document.doc_id.contains(self.document_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time>=date_start_tmp).filter(view_document.doc_id.contains(self.document_id)).count()
                        elif co_str <= 13 : # ใส่ tracking_id
                            # print ('tracking_id')
                            query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time>=date_start_tmp).filter(view_document.tracking_id.contains(self.document_id)).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time>=date_start_tmp).filter(view_document.tracking_id.contains(self.document_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time>=date_start_tmp).filter(view_document.tracking_id.contains(self.document_id)).count()
                        print ('have id2')
                elif self.date_start == '' and self.date_end != '' : # date_start ว่าง , date_end ไม่ว่าง
                    query_document_tmp = []
                    query_document_tmp_Active = 0
                    query_document_tmp_Reject = 0
                elif self.date_start == '' and self.date_end == '' : # date_start ว่าง , date_end ว่าง
                    if self.document_id != '':   # กรอกช่อง id
                        co_str = len(self.document_id)
                        # print (co_str)
                        if co_str > 13 :
                            # print ('doc_id')
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.doc_id.contains(self.document_id)).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.doc_id.contains(self.document_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.doc_id.contains(self.document_id)).count()
                        elif co_str <= 13 :
                            # print ('tracking_id')
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.tracking_id.contains(self.document_id)).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.tracking_id.contains(self.document_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.tracking_id.contains(self.document_id)).count()
                        print ('have id4')

                    if self.document_id =='': # ไม่กรอก id
                        if self.sender_email != '' and self.tax_id != '' and self.recipient_email != '' and self.documentType != '' : # ใส่ทั้งหมด

                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                            print('all put4')

                        elif self.sender_email != '': # ใส่ sender_email

                            if self.tax_id != '' and self.recipient_email == '' and self.documentType != '': # ไม่ใส่ recipient_email

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                                print('non recipient4')

                            elif self.tax_id == '' and self.recipient_email != '' and self.documentType != '': # ไม่ใส่ tax_id
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).count()
                                print('non tax4')

                            elif self.documentType == '' and self.recipient_email != '' and self.tax_id != '': # ไม่ใส่ documentType

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                print('non documentType2')

                            elif self.tax_id == '' and self.recipient_email == '' and self.documentType != '': # ไม่ใส่ recipient_email // ไม่ใส่ tax_id

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).count()
                                print('only sender4')

                            elif self.documentType == '' and self.recipient_email == '' and self.tax_id != '': # ไม่ใส่ recipient_email // ไม่ใส่ documentType

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                print('only sender , tax_id 3')

                            elif self.tax_id == '' and self.documentType == '' and self.recipient_email != '': # ไม่ใส่ tax_id // ไม่ใส่ documentType

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                print('only sender , recipient_email 3')

                            elif self.tax_id == '' and self.recipient_email == '' and self.documentType == '': # ไม่ใส่ recipient_email // ไม่ใส่ tax_id // ไม่ใส่ documentType

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).count()
                                print('only sender4')

                        elif self.recipient_email != '': # ใส่ recipient_email
                            if self.tax_id != '' and self.sender_email == '' and self.documentType == '': # ไม่ใส่ sender_email // ไม่ใส่ documentType

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.recipient_email.contains(self.recipient_email)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                                print('non sender_email 4')

                            elif self.tax_id == '' and self.sender_email == '' and self.documentType != '':# ไม่ใส่ sender_email // ไม่ใส่ tax_id

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                print('only recipient , documentType4')

                            elif self.tax_id == '' and self.sender_email == '' and self.documentType == '':# ไม่ใส่ sender_email // ไม่ใส่ tax_id // ไม่ใส่ documentType

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.recipient_email.contains(self.recipient_email)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                print('only recipient4')

                        elif self.tax_id == '' and self.recipient_email == ''and self.sender_email == ''and self.documentType != '': # ใส่ documentType

                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.documentType.contains(self.documentType)).count()
                            print('only documenType4')

                        elif self.tax_id != '' and self.recipient_email == ''and self.sender_email == ''and self.documentType == '': # ใส่ tax_id
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).count()
                            print('tax_id4')

                        elif self.tax_id != '' and self.recipient_email == '' and self.sender_email == ''and self.documentType != '': # ใส่ tax_id,documentType

                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(or_(view_document.biz_info == 'None',view_document.biz_info == None)).filter(view_document.documentType.contains(self.documentType)).count()
                            print('tax_id , documenType 4')


                        elif self.sender_email == '' and self.tax_id == '' and self.recipient_email == ''and self.documentType == '':#ไม่ใส่อะไรเลย
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').count()
                            print ('No anything')
                
            else :
                print ('ELSEEEEEE')
                if self.tax_id != '' and self.text != '' and self.document_id == '' and self.sender_email == '' and self.recipient_email == '' and self.documentType == '':
                    print('else tax_id,text')
                    query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.options_page.contains(self.text)).limit(limit_ch).all()
                    query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.options_page.contains(self.text)).count()
                    query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.options_page.contains(self.text)).count()
                elif self.date_start != '' and self.date_end != '' : # date_start ไม่ว่าง , date_end ไม่ว่าง
                    if self.document_id =='':
                        if self.sender_email != '' and self.tax_id != '' and self.recipient_email != '' and self.documentType != '': # ใส่ทั้งหมด
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                            # query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()

                            query_document_tmp2 = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            eval_biz_info = eval(query_document_tmp2[0].biz_info)
                            # print ('eval_biz_info: ',eval_biz_info['id_card_num'])
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(eval_biz_info['id_card_num'] == self.tax_id).filter(view_document.options_page.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(eval_biz_info['id_card_num'] == self.tax_id).filter(view_document.options_page.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(eval_biz_info['id_card_num'] == self.tax_id).filter(view_document.options_page.contains(self.documentType)).count()
                            print('all put')

                        elif self.sender_email != '': # ใส่ sender_email

                            if self.sender_email != '' and self.tax_id != '' and self.recipient_email == '' and self.documentType != '': # ไม่ใส่ recipient_email
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                                # query_document_tmp2 = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                                # eval_biz_info = eval(query_document_tmp2[0].biz_info)
                                # query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType.contains(self.documentType)).filter(eval_biz_info['id_card_num'] == self.tax_id).limit(limit_ch).all()

                                print('non recipient')

                            elif self.tax_id == '' and self.recipient_email != '' and self.documentType != '': # ไม่ใส่ tax_id
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).count()
                                print('non tax')

                            elif self.documentType == '' and self.recipient_email != '' and self.tax_id != '': # ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(view_document.biz_info.contains(self.tax_id)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                print('non documentType')

                            elif self.tax_id == '' and self.recipient_email == '' and self.documentType != '': # ไม่ใส่ recipient_email // ไม่ใส่ tax_id
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).count()
                                print('only sender , documentType')

                            elif self.documentType == '' and self.recipient_email == '' and self.tax_id != '': # ไม่ใส่ recipient_email // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                print('only sender , tax_id')

                            elif self.tax_id == '' and self.documentType == '' and self.recipient_email == '': # ไม่ใส่ tax_id // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                print('only sender , recipient_email')

                            elif self.tax_id == '' and self.recipient_email == '' and self.documentType == '': # ไม่ใส่ recipient_email // ไม่ใส่ tax_id // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).count()
                                print('only sender')

                        elif self.recipient_email != '': # ใส่ recipient_email

                            if self.tax_id != '' and self.sender_email == '' and self.documentType == '': # ไม่ใส่ sender_email // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                print('non sender_email ,documentType')

                            elif self.tax_id == '' and self.sender_email == '' and self.documentType != '':# ไม่ใส่ sender_email // ไม่ใส่ tax_id
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                print('only recipient , documentType')

                            elif self.tax_id == '' and self.sender_email == '' and self.documentType == '':# ไม่ใส่ sender_email // ไม่ใส่ tax_id // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                print('only recipient')

                        elif self.tax_id == '' and self.recipient_email == '' and self.sender_email == '' and self.documentType != '': # ใส่ documentType
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.documentType.contains(self.documentType)).count()
                            print('only documenType')

                        elif self.tax_id != '' and self.recipient_email == ''and self.sender_email == ''and self.documentType == '': # ใส่ tax_id
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.biz_info.contains(self.tax_id)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.biz_info.contains(self.tax_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.biz_info.contains(self.tax_id)).count()
                            print('tax_id')

                        elif self.tax_id != '' and self.recipient_email == ''and self.sender_email == ''and self.documentType != '': # ใส่ tax_id,documentType
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                            print('tax_id , documenType')

                        elif self.sender_email == '' and self.tax_id == '' and self.recipient_email == ''and self.documentType == '': #ไม่ใส่อะไรเลย
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).count()
                            print('non put')

                    elif self.document_id != '':# กรอกช่อง id
                        date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                        date_end_tmp = datetime.datetime.fromtimestamp(self.date_end)
                        co_str = len(self.document_id)
                        # print (co_str)
                        if co_str > 13 : # ใส่ doc_id
                            # print ('doc_id')
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.doc_id.contains(self.document_id)).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.doc_id.contains(self.document_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.doc_id.contains(self.document_id)).count()
                        elif co_str <= 13 : # ใส่ tracking_id
                            # print ('tracking_id')
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.tracking_id.contains(self.document_id)).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.tracking_id.contains(self.document_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.tracking_id.contains(self.document_id)).count()
                        print ('have id')
                elif self.date_start != '' and self.date_end == '' : # date_start ไม่ว่าง , date_end ว่าง
                    if self.document_id =='':
                        if self.sender_email != '' and self.tax_id != '' and self.recipient_email != ''and self.documentType != '': # ใส่ทั้งหมด
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                            query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                            print('all put2')

                        elif self.sender_email != '': # ใส่ sender_email

                            if self.tax_id != '' and self.recipient_email == '' and self.documentType != '': # ไม่ใส่ recipient_email
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                                print('non recipient2')

                            elif self.tax_id == '' and self.recipient_email != '' and self.documentType != '': # ไม่ใส่ tax_id
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).count()
                                print('non tax2')

                            elif self.documentType == '' and self.recipient_email != '' and self.tax_id != '': # ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(view_document.biz_info.contains(self.tax_id)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                print('non documentType2')

                            elif self.tax_id == '' and self.recipient_email == '' and self.documentType != '': # ไม่ใส่ recipient_email // ไม่ใส่ tax_id
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).count()
                                print('only sender , documentType2')

                            elif self.documentType == '' and self.recipient_email == '' and self.tax_id != '': # ไม่ใส่ recipient_email // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                print('only sender , tax_id 2')

                            elif self.tax_id == '' and self.documentType == '' and self.recipient_email != '': # ไม่ใส่ tax_id // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                print('only sender , recipient_email2')

                            elif self.tax_id == '' and self.recipient_email == '' and self.documentType == '': # ไม่ใส่ recipient_email // ไม่ใส่ tax_id // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.sender_email.contains(self.sender_email)).count()
                                print('only sender2')



                        elif self.recipient_email != '': # ใส่ recipient_email

                            if self.tax_id != '' and self.sender_email == '' and self.documentType == '': # ไม่ใส่ sender_email // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                print('non sender_email2')

                            elif self.tax_id == '' and self.sender_email == '' and self.documentType != '':# ไม่ใส่ sender_email // ไม่ใส่ tax_id
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                print('only recipient , documentType2')

                            elif self.tax_id == '' and self.sender_email == '' and self.documentType == '':# ไม่ใส่ sender_email // ไม่ใส่ tax_id // ไม่ใส่ documentType
                                date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                                date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                                query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                print('only recipient2')

                        elif self.tax_id == '' and self.recipient_email == ''and self.sender_email == ''and self.documentType != '': # ใส่ documentType
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                            query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.documentType.contains(self.documentType)).count()
                            print('only documenType2')

                        elif self.tax_id != '' and self.recipient_email == '' and self.sender_email == '' and self.documentType == '': # ใส่ tax_id
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                            query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.biz_info.contains(self.tax_id)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.biz_info.contains(self.tax_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.biz_info.contains(self.tax_id)).count()
                            print('tax_id2')

                        elif self.tax_id != '' and self.recipient_email == ''and self.sender_email == ''and self.documentType != '': # ใส่ tax_id,documentType
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                            query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time<=date_end_tmp).filter(view_document.send_time>=date_start_tmp).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                            print('tax_id , documenType2')

                        elif self.sender_email == '' and self.tax_id == '' and self.recipient_email == '': #ไม่ใส่อะไรเลย
                            date_end_tmp = datetime.datetime.fromtimestamp(time.time())
                            date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                            query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time>=date_start_tmp).filter(view_document.send_time<=date_end_tmp).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time>=date_start_tmp).filter(view_document.send_time<=date_end_tmp).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time>=date_start_tmp).filter(view_document.send_time<=date_end_tmp).count()
                            print('non put2')

                    elif self.document_id != '':# กรอกช่อง id
                        date_start_tmp = datetime.datetime.fromtimestamp(self.date_start)
                        co_str = len(self.document_id)
                        # print (co_str)
                        if co_str > 13 : # ใส่ doc_id
                            # print ('doc_id')
                            query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time>=date_start_tmp).filter(view_document.doc_id.contains(self.document_id)).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time>=date_start_tmp).filter(view_document.doc_id.contains(self.document_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time>=date_start_tmp).filter(view_document.doc_id.contains(self.document_id)).count()
                        elif co_str <= 13 : # ใส่ tracking_id
                            # print ('tracking_id')
                            query_document_tmp = view_document.query.order_by(asc(view_document.send_time)).filter(view_document.send_time>=date_start_tmp).filter(view_document.tracking_id.contains(self.document_id)).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.send_time>=date_start_tmp).filter(view_document.tracking_id.contains(self.document_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.send_time>=date_start_tmp).filter(view_document.tracking_id.contains(self.document_id)).count()
                        print ('have id2')
                elif self.date_start == '' and self.date_end != '' : # date_start ว่าง , date_end ไม่ว่าง
                    query_document_tmp = []
                    query_document_tmp_Active = 0
                    query_document_tmp_Reject = 0
                elif self.date_start == '' and self.date_end == '' : # date_start ว่าง , date_end ว่าง
                    if self.document_id != '':   # กรอกช่อง id
                        co_str = len(self.document_id)
                        # print (co_str)
                        if co_str > 13 :
                            # print ('doc_id')
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.doc_id.contains(self.document_id)).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.doc_id.contains(self.document_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.doc_id.contains(self.document_id)).count()
                        elif co_str <= 13 :
                            # print ('tracking_id')
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.tracking_id.contains(self.document_id)).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.tracking_id.contains(self.document_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.tracking_id.contains(self.document_id)).count()
                        print ('have id4')

                    if self.document_id =='': # ไม่กรอก id
                        if self.sender_email != '' and self.tax_id != '' and self.recipient_email != '' and self.documentType != '' : # ใส่ทั้งหมด

                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                            print('all put4')

                        elif self.sender_email != '': # ใส่ sender_email

                            if self.tax_id != '' and self.recipient_email == '' and self.documentType != '': # ไม่ใส่ recipient_email

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                                print('non recipient4')

                            elif self.tax_id == '' and self.recipient_email != '' and self.documentType != '': # ไม่ใส่ tax_id
                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).count()
                                print('non tax4')

                            elif self.documentType == '' and self.recipient_email != '' and self.tax_id != '': # ไม่ใส่ documentType

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(view_document.biz_info.contains(self.tax_id)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType.contains(self.documentType)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                print('non documentType2')

                            elif self.tax_id == '' and self.recipient_email == '' and self.documentType != '': # ไม่ใส่ recipient_email // ไม่ใส่ tax_id

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.documentType == self.documentType).count()
                                print('only sender4')

                            elif self.documentType == '' and self.recipient_email == '' and self.tax_id != '': # ไม่ใส่ recipient_email // ไม่ใส่ documentType

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                print('only sender , tax_id 3')

                            elif self.tax_id == '' and self.documentType == '' and self.recipient_email != '': # ไม่ใส่ tax_id // ไม่ใส่ documentType

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                print('only sender , recipient_email 3')

                            elif self.tax_id == '' and self.recipient_email == '' and self.documentType == '': # ไม่ใส่ recipient_email // ไม่ใส่ tax_id // ไม่ใส่ documentType

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.sender_email.contains(self.sender_email)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.sender_email.contains(self.sender_email)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.sender_email.contains(self.sender_email)).count()
                                print('only sender4')

                        elif self.recipient_email != '': # ใส่ recipient_email
                            if self.tax_id != '' and self.sender_email == '' and self.documentType == '': # ไม่ใส่ sender_email // ไม่ใส่ documentType

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.biz_info.contains(self.tax_id)).count()
                                print('non sender_email 4')

                            elif self.tax_id == '' and self.sender_email == '' and self.documentType != '':# ไม่ใส่ sender_email // ไม่ใส่ tax_id

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.recipient_email.contains(self.recipient_email)).filter(view_document.documentType == self.documentType).count()
                                print('only recipient , documentType4')

                            elif self.tax_id == '' and self.sender_email == '' and self.documentType == '':# ไม่ใส่ sender_email // ไม่ใส่ tax_id // ไม่ใส่ documentType

                                query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.recipient_email.contains(self.recipient_email)).limit(limit_ch).all()
                                query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.recipient_email.contains(self.recipient_email)).count()
                                print('only recipient4')

                        elif self.tax_id == '' and self.recipient_email == ''and self.sender_email == ''and self.documentType != '': # ใส่ documentType

                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.documentType.contains(self.documentType)).count()
                            print('only documenType4')

                        elif self.tax_id != '' and self.recipient_email == ''and self.sender_email == ''and self.documentType == '': # ใส่ tax_id
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.biz_info.contains(self.tax_id)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.biz_info.contains(self.tax_id)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.biz_info.contains(self.tax_id)).count()
                            print('tax_id4')

                        elif self.tax_id != '' and self.recipient_email == '' and self.sender_email == ''and self.documentType != '': # ใส่ tax_id,documentType

                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').filter(view_document.biz_info.contains(self.tax_id)).filter(view_document.documentType.contains(self.documentType)).count()
                            print('tax_id , documenType 4')


                        elif self.sender_email == '' and self.tax_id == '' and self.recipient_email == ''and self.documentType == '':#ไม่ใส่อะไรเลย
                            query_document_tmp = view_document.query.order_by(desc(view_document.send_time)).limit(limit_ch).all()
                            query_document_tmp_Active = view_document.query.filter(view_document.status == 'ACTIVE').count()
                            query_document_tmp_Reject = view_document.query.filter(view_document.status == 'REJECT').count()
                            print ('No anything')
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}        
        try:
            if len(query_document_tmp) == 0 or query_document_tmp == None:
                return {'result':'ER','messageText':'data not found'}
            elif len(query_document_tmp) !=0 :
                tmp_data = {}
                documentJson_result = None
                string_list_timeline = ''
                concat_steptimeline = ''
                for u in range(len(query_document_tmp)):
                    sid_email = query_document_tmp[u].step_data_sid
                    jsonData_eval = eval(query_document_tmp[u].data_json)
                    arr_step_info = []
                    timestamp_info = []
                    step_time_1 = []
                    step_timeline = []
                    result = None
                    timing_1 = None
                    lis_details = []
                    list_string_timing = []
                    list_options_page = []

                    if 'step_num' in jsonData_eval:
                        step_status = ''
                        step_before = ''
                        my_step = ''
                        res_status_file = 'Y'
                        arr_step_totle = []
                        json_data_info = jsonData_eval
                        details_email_reject = []
                        details_email_incomplete = []
                        if 'step_detail' in json_data_info:
                            for s in range(len(json_data_info['step_detail'])):
                                json_info_step2 = {}
                                for su in range(len(json_data_info['step_detail'][s]['activity_code'])):
                                    oneMail = json_data_info['step_detail'][s]['one_email']
                                    step_2 = json_data_info['step_detail'][s]
                                    # if str(oneMail).replace(' ','').lower() == self.emailUser:
                                    if json_data_info['step_detail'][s]['activity_code'][su] == 'A03':
                                        print(timestamp_info)
                                        print(sid_email)
                                        if my_step == '':
                                            if json_data_info['step_detail'][s]['activity_status'][su] == 'Complete':
                                                step_status = 'Complete'
                                                timestemp = int(time.mktime(datetime.datetime.strptime(json_data_info['step_detail'][s]['activity_time'][su], "%Y-%m-%d %H:%M:%S").timetuple()))
                                                timestamp_info.append(timestemp)
                                                t1 = step_2['activity_time'][su]
                                                t2 = int(time.mktime(datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S").timetuple()))
                                                step_time_1.append(t2)
                                            elif json_data_info['step_detail'][s]['activity_status'][su] == 'Approve':
                                                step_status = 'Complete'
                                                timestemp = int(time.mktime(datetime.datetime.strptime(json_data_info['step_detail'][s]['activity_time'][su], "%Y-%m-%d %H:%M:%S").timetuple()))
                                                timestamp_info.append(timestemp)
                                                t1 = step_2['activity_time'][su]
                                                t2 = int(time.mktime(datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S").timetuple()))
                                                step_time_1.append(t2)
                                            elif json_data_info['step_detail'][s]['activity_status'][su] == 'Reject':
                                                step_status = 'Reject'
                                                timestemp = int(time.mktime(datetime.datetime.strptime(json_data_info['step_detail'][s]['activity_time'][su], "%Y-%m-%d %H:%M:%S").timetuple()))
                                                timestamp_info.append(timestemp)
                                                t1 = step_2['activity_time'][su]
                                                t2 = int(time.mktime(datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S").timetuple()))
                                                step_time_1.append(t2)
                                            else:
                                                try:
                                                    step_status  = 'Incomplete'
                                                    # t1 = step_2['activity_time'][su]
                                                    # t2 = int(time.mktime(datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S").timetuple()))
                                                    # step_time_1.append(t2)
                                                    details_email_incomplete.append({'email':json_data_info['step_detail'][s]['one_email'],'step_num':json_data_info['step_num']})
                                                except Exception as ex:
                                                    step_status = 'Incomplete'
                                        arr_step_info.append(step_status)
                                        arr_step_info.append(step_before)
                        print(arr_step_info)
                        if 'Reject' in arr_step_info:
                            res_status_file = 'R'
                            res_status_file_string = 'เอกสารปฏิเสธอนุมัติ'
                        elif 'Complete' in arr_step_info:
                            res_status_file = 'Y'
                            res_status_file_string = 'อนุมัติแล้ว'
                        elif 'Waitting' in arr_step_info:
                            res_status_file = 'W'
                            res_status_file_string = 'รออนุมัติ'
                        elif 'Incomplete' in arr_step_info or 'Pendding' in arr_step_info:
                            res_status_file = 'N'
                            res_status_file_string = 'กำลังดำเนินการ'
                        else:
                            res_status_file_string = 'อนุมัติแล้ว'
                        if res_status_file == 'W':
                            statusFile_count_wait = statusFile_count_wait + 1
                        elif res_status_file == 'Y':
                            statusFile_count_approve = statusFile_count_approve + 1
                        elif res_status_file == 'R':
                            statusFile_count_reject = statusFile_count_reject + 1
                        else:
                            statusFile_count_pendding = statusFile_count_pendding + 1
                        string_timing = ''
                        dateTime_String = query_document_tmp[u].send_time
                        start_send_time = dateTime_String.timestamp()
                        now = datetime.datetime.now()
                        timing = (now.timestamp()) - start_send_time
                        timing_1 = convert_hr_min_sec_v1(int(timing))
                        for yy in range(len(timing_1)):
                            if timing_1[yy] > 0:
                                if yy == 0:
                                    type_date = " วัน "
                                elif yy == 1:
                                    type_date = " ชั่วโมง "
                                elif yy == 2:
                                    type_date = " นาที "
                                elif yy == 3:
                                    type_date = " วินาที "
                                string_timing += str(timing_1[yy]) + type_date
                        # list_string_timing.append(string_timing)
                        # string_timing = ''
                        print ('list_steptime1',step_time_1)
                        if(len(step_time_1) != 0):
                            for i in range(len(step_time_1)):
                                if(i==0):
                                    print ('เริ่มต้น : ',start_send_time)
                                    result = step_time_1[i] - start_send_time
                                    # print ('เริ่มต้น - ลำดับ1ที่เซนอนุมัติ',result)
                                    list_timeline = convert_hr_min_sec_v1(int(result))
                                    # print ('เริ่มต้น - ลำดับ1ที่เซนอนุมัติ : ',list_timeline)
                                    for yy in range(len(list_timeline)):
                                        if list_timeline[yy] > 0:
                                            if yy == 0:
                                                type_date = " วัน "
                                            elif yy == 1:
                                                type_date = " ชั่วโมง "
                                            elif yy == 2:
                                                type_date = " นาที "
                                            elif yy == 3:
                                                type_date = " วินาที "
                                            string_list_timeline += str(list_timeline[yy]) + type_date
                                    print('เริ่มต้น - ลำดับ1ที่เซนอนุมัติ (string)',string_list_timeline)
                                    step_timeline.append(string_list_timeline)
                                    string_list_timeline = ''
                                else:
                                    result = step_time_1[i] - step_time_1[i-1]
                                    # print ('ลำดับปัจจุบัน- ลำดับก่อนหน้า',result)
                                    list_timeline = convert_hr_min_sec_v1(int(result))
                                    for yy in range(len(list_timeline)):
                                        if list_timeline[yy] > 0:
                                            if yy == 0:
                                                type_date = " วัน "
                                            elif yy == 1:
                                                type_date = " ชั่วโมง "
                                            elif yy == 2:
                                                type_date = " นาที "
                                            elif yy == 3:
                                                type_date = " วินาที "
                                            string_list_timeline += str(list_timeline[yy]) + type_date
                                    print('เริ่มต้น - ลำดับก่อนหน้า (string)',string_list_timeline)
                                    step_timeline.append(string_list_timeline)
                            print ("สรุปเวลาการเซ็นแต่ละลำดับ :",step_timeline)
                            concat_steptimeline += 'ระยะเวลาดำเนินการ\n'
                            for j in range(len(step_timeline)):
                                if(j == (len(step_timeline))-1):
                                    concat_steptimeline += '-ลำดับที่ ' +str(j+1)+ ' : ' + str(step_timeline[j])
                                else:
                                    concat_steptimeline += '-ลำดับที่ ' +str(j+1)+ ' : ' + str(step_timeline[j]) + '\n'
                            print ('concat_steptimeline',concat_steptimeline)
                        elif(len(step_time_1) == 0):
                            concat_steptimeline += 'อยู่ระหว่างดำเนินการ'

                        # string_details_avg_time = ''
                        string_details_avg_time = 'ระยะเวลาทั้งหมดที่เอกสารถูกดำเนินการ\n'
                        if len(timestamp_info) != 0:
                            # end_time_document = timestamp_info[-1]
                            # result_start_and_end = end_time_document - start_send_time
                            end_time_document = timestamp_info[-1]
                            result_start_and_end = end_time_document - start_send_time
                            list_day_hr_min_sec = convert_hr_min_sec_v1(int(result_start_and_end))
                            for yy in range(len(list_day_hr_min_sec)):
                                if list_day_hr_min_sec[yy] > 0:
                                    if yy == 0:
                                        type_date = " วัน "
                                    elif yy == 1:
                                        type_date = " ชั่วโมง "
                                    elif yy == 2:
                                        type_date = " นาที "
                                    elif yy == 3:
                                        type_date = " วินาที "
                                    string_details_avg_time += str(list_day_hr_min_sec[yy]) + type_date
                        print(string_details_avg_time)
                        if res_status_file == 'N':
                            string_details_avg_time = ""
                        # th_dateTime_1 = convert_datetime_TH_1(int(dateTime_String.timestamp()))
                        th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
                        ts = int(time.time())
                        date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
                        datetime_display = int(dateTime_String.timestamp())
                        date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
                        yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
                        time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
                        old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
                        if date_time_today == date_time_db:
                            date_display_show = time_show_db
                        else:
                            if year_today == yar_db:
                                date_display_show = convert_datetime_TH_2_display(datetime_display)
                            else:
                                date_display_show = old_year
                        string_remark_description = ''
                        title_remark = ''
                        if res_status_file == 'R':
                            if len(details_email_reject) != 0:
                                for o in range(len(details_email_reject)):
                                    query_data = paper_lesslogin.query.filter(paper_lesslogin.citizen_data.contains(details_email_reject[o]['email'])).all()
                                    data_json_name = eval(query_data[0].citizen_data)['first_name_th'] + ' ' + eval(query_data[0].citizen_data)['last_name_th']
                                    # print(data_json_name)
                                    details_msg = {}
                                    details_msg['reject_by'] = details_email_reject[o]['email']
                                    details_msg['reject_in_step_num'] = (details_email_reject[o]['step_num'])
                                    details_msg['reject_in_datetime'] = details_email_reject[o]['datetime']
                                    title_remark = 'ยกเลิกโดย ลำดับที่ ' + str(details_email_reject[o]['step_num'])
                                    datetime_display = convert_datetime_TH_2(int(details_email_reject[o]['datetime_string']))
                                    string_remark_description +=  '\n-' + data_json_name + '\nวันที่ ' + datetime_display
                                    lis_details.append(details_msg)
                        elif res_status_file == 'N':
                            if len(details_email_incomplete) != 0:
                                for oi in range(len(details_email_incomplete)):
                                    tmp_step_num_list_0 = details_email_incomplete[0]['step_num']
                                    tmp_step_num_list = details_email_incomplete[oi]['step_num']
                                    if details_email_incomplete[oi]['email'] == None or details_email_incomplete[oi]['email'] == 'None':
                                        continue
                                    if tmp_step_num_list_0 == tmp_step_num_list:
                                        query_data = paper_lesslogin.query.filter(paper_lesslogin.citizen_data.contains(details_email_incomplete[oi]['email'])).all()
                                        try:
                                            data_json_name = eval(query_data[0].citizen_data)['first_name_th'] + ' ' + eval(query_data[0].citizen_data)['last_name_th']
                                        except Exception as e:
                                            data_json_name = details_email_incomplete[oi]['email']

                                        details_msg = {}
                                        details_msg['pending_by'] = details_email_incomplete[oi]['email']
                                        details_msg['pending_in_step_num'] = (details_email_incomplete[oi]['step_num'])
                                        title_remark = 'รอการอนุมัติ ลำดับที่ ' + str(details_email_incomplete[oi]['step_num'])
                                        string_remark_description += '\n-' + data_json_name + ''
                                        lis_details.append(details_msg)
                    else:
                        step_status = ''
                        res_status_file = 'Y'
                        step_before = ''
                        step_list_before = []
                        step_list_ = []
                        step_list_next = []
                        arr_step_totle = []
                        step_me = ''
                        step_sum_status = []
                        sum_status_step_list = []
                        list_check_step = []
                        step_list_data = []
                        max_step = (len(jsonData_eval))
                        step_infomation = jsonData_eval
                        sum_status_step = []
                        details_email_reject = []
                        details_email_incomplete = []
                        lis_details = []
                        for i in range(len(step_infomation)):
                            list_check_step = []
                            json_step_info_2 = {}
                            step_list_data = []
                            step_ = step_infomation[i]
                            step_num = step_infomation[i]['step_num']
                            json_step_info_2['step_status'] = ''
                            for m in range(len(step_['step_detail'])):
                                oneMail = step_['step_detail'][m]['one_email']
                                # if str(oneMail).replace(' ','').lower() == self.emailUser:
                                #     step_me = step_infomation[i]['step_num']
                                #     step_me = int(step_me) - 1
                                step_2 = step_['step_detail'][m]
                                for k in range(len(step_2['activity_code'])):
                                    if step_2['activity_code'][k] == 'A03':
                                        # print()
                                        if step_2['activity_status'][k] == 'Complete':
                                            timestemp = int(time.mktime(datetime.datetime.strptime(step_2['activity_time'][k], "%Y-%m-%d %H:%M:%S").timetuple()))
                                            timestamp_info.append(timestemp)
                                            t1 = step_2['activity_time'][k]
                                            t2 = int(time.mktime(datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S").timetuple()))
                                            step_time_1.append(t2)
                                        elif step_2['activity_status'][k] == 'Approve':
                                            timestemp = int(time.mktime(datetime.datetime.strptime(step_2['activity_time'][k], "%Y-%m-%d %H:%M:%S").timetuple()))
                                            timestamp_info.append(timestemp)
                                            t1 = step_2['activity_time'][k]
                                            t2 = int(time.mktime(datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S").timetuple()))
                                            step_time_1.append(t2)
                                        elif step_2['activity_status'][k] == 'Reject':
                                            timestemp = int(time.mktime(datetime.datetime.strptime(step_2['activity_time'][k], "%Y-%m-%d %H:%M:%S").timetuple()))
                                            timestamp_info.append(timestemp)
                                            t1 = step_2['activity_time'][k]
                                            t2 = int(time.mktime(datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S").timetuple()))
                                            step_time_1.append(t2)
                                        json_step_info = {}
                                        json_step_info['activity_status'] = step_2['activity_status'][k]
                                        json_step_info['one_email'] = step_2['one_email']
                                        json_step_info['step_num'] = step_num
                                        list_check_step.append(json_step_info['activity_status'])
                                        step_list_data.append(json_step_info)
                                # print ('Round time', step_time_1)
                                json_step_info_2['step_info'] = step_list_data
                                if json_step_info_2['step_status'] == '':
                                    if 'Reject' in list_check_step:
                                        for kz in range(len(step_2['activity_code'])):
                                            if step_2['activity_code'][kz] == 'A03':
                                                details_email_reject.append({'email':step_2['one_email'],'step_num':step_num,'datetime':step_2['activity_time'][kz],'datetime_string':time.mktime(datetime.datetime.strptime(step_2['activity_time'][kz], "%Y-%m-%d %H:%M:%S").timetuple())})
                                        json_step_info_2['step_status'] = 'Reject'
                                    elif 'Complete' in list_check_step:
                                        json_step_info_2['step_status'] = 'Complete'
                                    elif 'Approve' in list_check_step:
                                        json_step_info_2['step_status'] = 'Complete'
                                    elif 'Incomplete' in list_check_step:
                                        # details_email_incomplete.append({'email':step_2['one_email'],'step_num':step_num})
                                        json_step_info_2['step_status'] = 'Incomplete'
                                    elif 'Pending' in list_check_step:
                                        # details_email_incomplete.append({'email':step_2['one_email'],'step_num':step_num})
                                        json_step_info_2['step_status'] = 'Incomplete'
                                    else:
                                        json_step_info_2['step_status'] = 'Complete'
                                if json_step_info_2['step_status'] == 'Incomplete':
                                    if 'Reject' in list_check_step:
                                        json_step_info_2['step_status'] = 'Reject'
                                    elif 'Complete' in list_check_step:
                                        json_step_info_2['step_status'] = 'Complete'
                                    elif 'Approve' in list_check_step:
                                        json_step_info_2['step_status'] = 'Complete'
                                    elif 'Incomplete' in list_check_step:
                                        details_email_incomplete.append({'email':step_2['one_email'],'step_num':step_num})
                                        json_step_info_2['step_status'] = 'Incomplete'
                                    elif 'Pending' in list_check_step:
                                        details_email_incomplete.append({'email':step_2['one_email'],'step_num':step_num})
                                        json_step_info_2['step_status'] = 'Incomplete'
                                    else:
                                        json_step_info_2['step_status'] = 'Complete'

                                sum_status_step_list.append(json_step_info_2['step_status'])
                            sum_status_step.append(json_step_info_2['step_status'])
                            arr_step_info.append(json_step_info_2['step_status'])
                        index_mystep = step_me
                        print(sid_email)
                        print(arr_step_info)
                        if 'Reject' in arr_step_info:
                            res_status_file = 'R'
                            res_status_file_string = 'เอกสารปฏิเสธอนุมัติ'
                        elif 'Incomplete_1' in arr_step_info or 'Pending_1' in arr_step_info:
                            res_status_file = 'W'
                            res_status_file_string = 'รออนุมัติ'
                        elif 'Incomplete' in arr_step_info or 'Pendding' in arr_step_info:
                            res_status_file = 'N'
                            res_status_file_string = 'กำลังดำเนินการ'
                        elif 'Wait__' in arr_step_info:
                            res_status_file = 'Z'
                            res_status_file_string = 'อยู่ในช่วงดำเนินการ'
                        elif 'Waitting' in arr_step_info:
                            res_status_file = 'W'
                            res_status_file_string = 'รออนุมัติ'
                        else:
                            res_status_file_string = 'อนุมัติแล้ว'
                        if res_status_file == 'W':
                            statusFile_count_wait = statusFile_count_wait + 1
                        elif res_status_file == 'Y':
                            statusFile_count_approve = statusFile_count_approve + 1
                        elif res_status_file == 'R':
                            statusFile_count_reject = statusFile_count_reject + 1
                        else:
                            statusFile_count_pendding = statusFile_count_pendding + 1
                        string_timing = ''
                        dateTime_String = query_document_tmp[u].send_time
                        start_send_time = dateTime_String.timestamp()
                        now = datetime.datetime.now()
                        timing = (now.timestamp()) - start_send_time
                        timing_1 = convert_hr_min_sec_v1(int(timing))
                        for yy in range(len(timing_1)):
                            if timing_1[yy] > 0:
                                if yy == 0:
                                    type_date = " วัน "
                                elif yy == 1:
                                    type_date = " ชั่วโมง "
                                elif yy == 2:
                                    type_date = " นาที "
                                elif yy == 3:
                                    type_date = " วินาที "
                                string_timing += str(timing_1[yy]) + type_date
                        # list_string_timing.append(string_timing)
                        # string_timing = ''
                        print ('list_steptime1',step_time_1)
                        if(len(step_time_1) != 0):
                            string_list_timeline = ''
                            for i in range(len(step_time_1)):
                                if(i==0):
                                    print ('เริ่มต้น : ',start_send_time)
                                    result = step_time_1[i] - start_send_time
                                    # print ('เริ่มต้น - ลำดับ1ที่เซนอนุมัติ',result)
                                    list_timeline = convert_hr_min_sec_v1(int(result))
                                    # print ('เริ่มต้น - ลำดับ1ที่เซนอนุมัติ : ',list_timeline)
                                    for yy in range(len(list_timeline)):
                                        if list_timeline[yy] > 0:
                                            if yy == 0:
                                                type_date = " วัน "
                                            elif yy == 1:
                                                type_date = " ชั่วโมง "
                                            elif yy == 2:
                                                type_date = " นาที "
                                            elif yy == 3:
                                                type_date = " วินาที "
                                            string_list_timeline += str(list_timeline[yy]) + type_date
                                    print('เริ่มต้น - ลำดับ1ที่เซนอนุมัติ (string)',string_list_timeline)
                                    step_timeline.append(string_list_timeline)
                                else:
                                    result = step_time_1[i] - step_time_1[i-1]
                                    # print ('ลำดับปัจจุบัน- ลำดับก่อนหน้า',result)
                                    list_timeline = convert_hr_min_sec_v1(int(result))
                                    for yy in range(len(list_timeline)):
                                        if list_timeline[yy] > 0:
                                            if yy == 0:
                                                type_date = " วัน "
                                            elif yy == 1:
                                                type_date = " ชั่วโมง "
                                            elif yy == 2:
                                                type_date = " นาที "
                                            elif yy == 3:
                                                type_date = " วินาที "
                                            string_list_timeline += str(list_timeline[yy]) + type_date
                                    print('เริ่มต้น - ลำดับก่อนหน้า (string)',string_list_timeline)
                                    step_timeline.append(string_list_timeline)
                                    string_list_timeline = ''
                            print ("สรุปเวลาการเซ็นแต่ละลำดับ :",step_timeline)
                            concat_steptimeline = ''
                            concat_steptimeline += 'ระยะเวลาดำเนินการ\n'
                            for j in range(len(step_timeline)):
                                if(j == (len(step_timeline))-1):
                                    concat_steptimeline += '-ลำดับที่ ' +str(j+1)+ ' : ' + str(step_timeline[j])
                                else:
                                    concat_steptimeline += '-ลำดับที่ ' +str(j+1)+ ' : ' + str(step_timeline[j]) + '\n'
                            print ('concat_steptimeline',concat_steptimeline)
                        elif(len(step_time_1) == 0):
                            concat_steptimeline += 'อยู่ระหว่างดำเนินการ'

                        # string_details_avg_time = ''
                        string_details_avg_time = 'ระยะเวลาทั้งหมดที่เอกสารถูกดำเนินการ\n'
                        if len(timestamp_info) != 0:
                            # end_time_document = timestamp_info[-1]
                            # result_start_and_end = end_time_document - start_send_time
                            end_time_document = timestamp_info[-1]
                            result_start_and_end = end_time_document - start_send_time
                            list_day_hr_min_sec = convert_hr_min_sec_v1(int(result_start_and_end))
                            print(end_time_document,start_send_time)
                            print(timestamp_info)
                            for yy in range(len(list_day_hr_min_sec)):
                                if list_day_hr_min_sec[yy] > 0:
                                    if yy == 0:
                                        type_date = " วัน "
                                    elif yy == 1:
                                        type_date = " ชั่วโมง "
                                    elif yy == 2:
                                        type_date = " นาที "
                                    elif yy == 3:
                                        type_date = " วินาที "
                                    string_details_avg_time += str(list_day_hr_min_sec[yy]) + type_date
                        print(string_details_avg_time)
                        if res_status_file == 'N':
                            string_details_avg_time = ""
                        # th_dateTime_1 = convert_datetime_TH_1(int(dateTime_String.timestamp()))
                        th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
                        ts = int(time.time())
                        date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
                        datetime_display = int(dateTime_String.timestamp())
                        date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
                        yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
                        time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
                        old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
                        if date_time_today == date_time_db:
                            date_display_show = time_show_db
                        else:
                            if year_today == yar_db:
                                date_display_show = convert_datetime_TH_2_display(datetime_display)
                            else:
                                date_display_show = old_year
                        string_remark_description = ''
                        title_remark = ''
                        if res_status_file == 'R':
                            if len(details_email_reject) != 0:
                                for o in range(len(details_email_reject)):
                                    query_data = paper_lesslogin.query.filter(paper_lesslogin.citizen_data.contains(details_email_reject[o]['email'])).all()
                                    try:
                                        data_json_name = eval(query_data[0].citizen_data)['first_name_th'] + ' ' + eval(query_data[0].citizen_data)['last_name_th']
                                    except Exception as e:
                                        data_json_name = details_email_incomplete[oi]['email']
                                    # print(data_json_name)
                                    details_msg = {}
                                    details_msg['reject_by'] = details_email_reject[o]['email']
                                    details_msg['reject_in_step_num'] = details_email_reject[o]['step_num']
                                    details_msg['reject_in_datetime'] = details_email_reject[o]['datetime']
                                    title_remark = 'ยกเลิกโดย ลำดับที่ ' + details_email_reject[o]['step_num']
                                    datetime_display = convert_datetime_TH_2(int(details_email_reject[o]['datetime_string']))
                                    string_remark_description +=  '\n-' + data_json_name + '\nวันที่ ' + datetime_display
                                    lis_details.append(details_msg)
                        elif res_status_file == 'N':
                            if len(details_email_incomplete) != 0:
                                for oi in range(len(details_email_incomplete)):
                                    tmp_step_num_list_0 = details_email_incomplete[0]['step_num']
                                    tmp_step_num_list = details_email_incomplete[oi]['step_num']
                                    if tmp_step_num_list_0 == tmp_step_num_list:
                                        query_data = paper_lesslogin.query.filter(paper_lesslogin.citizen_data.contains(details_email_incomplete[oi]['email'])).all()
                                        try:
                                            data_json_name = eval(query_data[0].citizen_data)['first_name_th'] + ' ' + eval(query_data[0].citizen_data)['last_name_th']
                                        except Exception as e:
                                            data_json_name = details_email_incomplete[oi]['email']

                                        details_msg = {}
                                        details_msg['pending_by'] = details_email_incomplete[oi]['email']
                                        details_msg['pending_in_step_num'] = details_email_incomplete[oi]['step_num']
                                        
                                        title_remark = 'รอการอนุมัติ ลำดับที่ ' + str(details_email_incomplete[oi]['step_num'])
                                        string_remark_description += '\n-' + data_json_name + ''
                                        lis_details.append(details_msg)
                    tmp_json = {}
                    ts = int(time.time())
                    date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
                    dateTime_timestamp = int((query_document_tmp[u].send_time).timestamp())
                    date_time_db = datetime.datetime.fromtimestamp(dateTime_timestamp).strftime('%Y-%m-%d')
                    yar_db = datetime.datetime.fromtimestamp(dateTime_timestamp).strftime('%Y')
                    time_show_db = datetime.datetime.fromtimestamp(dateTime_timestamp).strftime('%H:%M')
                    old_year = datetime.datetime.fromtimestamp(dateTime_timestamp).strftime('%d/%m/%Y')
                    if date_time_today == date_time_db:
                        date_display_show = time_show_db
                    else:
                        if year_today == yar_db:
                            date_display_show = convert_datetime_TH_2_display(dateTime_timestamp)
                        else:
                            date_display_show = old_year

                    if query_document_tmp[u].urgent_type != None:
                        documentUrgentType = query_document_tmp[u].urgent_type
                        if documentUrgentType == 'I':
                            documentUrgentString = 'ด่วนมาก'
                        elif documentUrgentType == 'U':
                            documentUrgentString = 'ด่วน'
                        elif documentUrgentType == 'M':
                            documentUrgentString = 'ปกติ'

                    if query_document_tmp[u].documentJson != None:
                        documentJson_result = eval(query_document_tmp[u].documentJson)
                        print(documentJson_result)
                        documentName = documentJson_result['document_name']
                        documentType = documentJson_result['document_type']
                    else:
                        documentName = None
                        documentType = None



                    tmp_json['send_time'] = query_document_tmp[u].send_time
                    tmp_json['dateTime'] = dateTime_timestamp
                    tmp_json['dateTime_String'] = str(query_document_tmp[u].send_time).split('+')[0]
                    tmp_json['dateTime_String_TH_1'] = convert_datetime_TH_2(dateTime_timestamp)
                    tmp_json['dateTime_display'] = date_display_show
                    tmp_json['date_String'] = str(query_document_tmp[u].send_time).split(' ')[0]
                    tmp_json['time_String'] = str(query_document_tmp[u].send_time).split(' ')[1].split('+')[0]

                    tmp_json['document_urgent_string'] = documentUrgentString
                    tmp_json['document_name'] = documentName
                    tmp_json['document_type'] = documentType
                    tmp_json['sender_name'] = query_document_tmp[u].sender_name
                    tmp_json['sender_email'] = query_document_tmp[u].sender_email
                    if tmp_json['sender_name'] == 'null null':
                        tmp_json['sender_name'] = tmp_json['sender_email']
                    tmp_json['recipient_email'] = eval(query_document_tmp[u].recipient_email)
                    tmp_json['document_id'] = query_document_tmp[u].doc_id
                    tmp_json['tracking_id'] = query_document_tmp[u].tracking_id
                    tmp_json['file_name'] = query_document_tmp[u].file_name
                    if query_document_tmp[u].string_pdf != None:
                        tmp_json['status_original_pdf_file'] = True
                    else:
                        tmp_json['status_original_pdf_file'] = False
                    if query_document_tmp[u].string_sign != None:
                        tmp_json['status_sign_pdf_file'] = True
                    else:
                        tmp_json['status_sign_pdf_file'] = False
                    # tmp_json['data_json'] = eval(query_document_tmp[u].data_json)
                    tmp_json['fid'] = query_document_tmp[u].fid
                    # tmp_json['document_type'] = query_document_tmp[u].documentType
                    # tmp_json['documentJson'] = query_document_tmp[u].documentJson
                    tmp_json['digit_sign'] = query_document_tmp[u].digit_sign
                    tmp_json['document_urgent'] = query_document_tmp[u].urgent_type

                    option_eval=eval(query_document_tmp[u].options_page)
                    list_options_page.append(option_eval)
                    tmp_json['options_page'] = list_options_page

                    tmp_json['stamp_all'] = query_document_tmp[u].sign_page_options
                    tmp_json['sidCode'] = query_document_tmp[u].step_data_sid
                    try:
                        tmp_json['email_center'] = eval(query_document_tmp[u].email_center)
                    except Exception as e:
                        tmp_json['email_center'] = query_document_tmp[u].email_center
                    # if เช็คค่า null ของ attempted_folder -v-
                    tmp_json['attempted_folder'] = query_document_tmp[u].attempted_folder
                    tmp_json['status_file_code'] = res_status_file
                    tmp_json['status_file_details'] = lis_details
                    tmp_json['status_file_string'] = res_status_file_string
                    tmp_json['string_details_avg_time'] = string_details_avg_time
                    tmp_json['timeline'] = concat_steptimeline
                    tmp_json['timing'] = string_timing
                    tmp_json['remark_description'] = title_remark + string_remark_description

                    tmp_json['step_Name'] = query_document_tmp[u].step_Name
                    tmp_json['documentDetails'] = query_document_tmp[u].documentDetails
                    tmp_json['condition_temp'] = query_document_tmp[u].condition_temp
                    tmp_json['step_Code'] = query_document_tmp[u].step_Code
                    tmp_json['status'] = query_document_tmp[u].status
                    # if tmp_json['status'] == 'ACTIVE':
                    #     count_Active += 1
                    # elif tmp_json['status'] == 'REJECT':
                    #    count_Reject += 1


                    tmp_biz_info = (query_document_tmp[u].biz_info)
                    if tmp_biz_info == 'None':
                        tmp_biz_info = 'None'
                        list_biz = []
                        dict_biz= {}
                        dict_biz['id'] = None
                        dict_biz['id_card_num'] = None
                        dict_biz['first_name_eng'] = None
                        dict_biz['first_name_th'] = None
                        list_biz.append(dict_biz)
                        tmp_json['biz_detail'] = list_biz

                    else :
                        tmp_biz_info = eval(tmp_biz_info)
                        if 'id' in tmp_biz_info:
                            tmp_id_biz = tmp_biz_info['id']
                            tmp_id_card_num_biz = tmp_biz_info['id_card_num']
                            tmp_first_name_eng_biz = tmp_biz_info['first_name_eng']
                            tmp_first_name_th_biz = tmp_biz_info['first_name_th']
                        tmp_json['biz_detail'] = [{'id':tmp_id_biz,'id_card_num':tmp_id_card_num_biz,'first_name_eng':tmp_first_name_eng_biz,'first_name_th':tmp_first_name_th_biz}]

                    # print (u)
                    sum_Document = sum_Document+1

                    if ((u+1) == len(query_document_tmp)):
                        last_time = (tmp_json['send_time'])
                        dt_object = int(datetime.datetime.timestamp(last_time))


                    tmp_list_result.append(tmp_json)
                tmp_data['data'] = tmp_list_result
                query_document_tmp_count = query_document_tmp_Active + query_document_tmp_Reject
                tmp_data['sum_Document'] = query_document_tmp_count

                # tmp_data['Document_Status_Details']
                Document_Status_Details  = [{
                    'Incomplete_Pendding':statusFile_count_pendding,
                    'Complete_Approve':statusFile_count_approve,
                    'Reject':statusFile_count_reject
                }]

                tmp_data['Document_Status'] = [{
                    'ACTIVE':query_document_tmp_Active,
                    'REJECT':query_document_tmp_Reject
                }]

                tmp_list_result2.append(tmp_data)
                return {'result':'OK','last_time':dt_object,'messageText':tmp_list_result2}
            else:
                return {'result':'ER','messageText':'data not found'}
        except exc.SQLAlchemyError as ex:
            db.session.rollback()
            raise
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            db.session.rollback()
            raise
            return {'result':'ER','messageText':'cant select','messageER':str(e)}
        finally:
            db.session.close()

    def select_profileGetstatus_v1(self,email_one):
        self.email_one = email_one
        search_email = "%'{}'%".format(self.email_one)
        where_sql = 'WHERE p_emailthai=:email or p_userid=:email or p_emailthai2=:email or p_emailthai3=:email or employee_email LIKE :search_email ' 
        try:
            tmpchat_noti = True
            tmpemail_noti = True
            text_sql = text('SELECT "p_id","p_username","p_userid","p_updateTime","p_webHook","p_sign","p_emailUser","p_emailthai",\
            "p_taskchat","p_todo","p_doing","p_done","p_options","p_signca","chat_noti","email_noti",\
            "permission_id" \
            FROM "tb_userProfile" ' + where_sql)
            with slave.connect() as connection:
                result_all = connection.execute(text_sql \
                        ,email=self.email_one,search_email=search_email)
                connection.close()
            query_temp = [dict(row) for row in result_all]
            query_temp = query_temp[0]
            if 'chat_noti' in query_temp:
                tmpchat_noti = query_temp['chat_noti']
            if 'email_noti' in query_temp:
                tmpemail_noti = query_temp['email_noti']
            return {'result':'OK','status_chat':tmpchat_noti,'status_email':tmpemail_noti}
        except Exception as e:
            print(str(e))
            return {'result':'ER','message':str(e)}

    def select_recp_count_v1(self,typequery,email_one,document_type,tax_id,keyword,group_status=None,pick_datetime=None):
        self.typequery = typequery
        self.email_one = email_one
        self.document_type = document_type
        self.tax_id = tax_id
        self.keyword = keyword
        self.group_status = group_status
        self.pick_datetime = pick_datetime
        self.before_datetime = None
        self.after_datetime = None
        status_ACTIVE = 'ACTIVE'
        sid_list = []
        sid_list_email = []
        json_Data = {}
        list_arr = []
        list_json = []
        tmp_list = []             
        count_rowDocument = 0
        count_rowDocument_StatusActive = 0
        count_rowDocument_StatusReject = 0
        count_rowDocument_StatusCancel = 0
        statusFile_count_approve = 0
        statusFile_count_pendding = 0
        statusFile_count_reject = 0
        statusFile_count_wait = 0
        statusFile_count_Z = 0
        list_temp_query = []
        tmp_sid_code_list = []
        arr_gruop = []
        arr_group_sid = []
        tmp_arr_sid = []
        tmp_group_id = None
        query_temp = 0
        str_time = (time.time())
        search = "%'{}'%".format(self.email_one) 
        search_tax_id = "'%''{}''%'".format(self.tax_id)
        search_keyword = "%{}%".format(self.keyword)
        if self.pick_datetime != None:
            if self.pick_datetime != "":
                self.pick_datetime = int(self.pick_datetime)
                self.search_datetime = datetime.datetime.fromtimestamp(self.pick_datetime).strftime('%Y-%m-%d')
                self.before_datetime = str(self.search_datetime) + 'T00:00:00'
                self.after_datetime = str(self.search_datetime) + 'T23:59:59'
        # print(self.before_datetime,self.after_datetime)
        # print(self.pick_datetime)
        # search_tax_id = "'%''{}''%'".format(self.tax_id)
        ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
        where_sql = 'WHERE status=:status AND "recipient_email" LIKE :recipient_email ' 
        # print(self.tax_id)
        if self.tax_id != '':
            if type(self.tax_id) is str:
                where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
            elif type(self.tax_id) is list:
                for n in self.tax_id:
                    tmp_taxid = "'%''" + n + "''%'"
                    where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + ')) '
                where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null) '
                # where_sql += ' AND ("tb_step_data".biz_info != ANY(:biz_info_data)) AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null)'
        else:
            where_sql += ''
        # print(self.document_type)
        if self.document_type != '':     
            where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
        if self.keyword != '':
            where_sql += ' AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword)'  
        # if self.group_status == True:
        #     where_sql += ' AND ("tb_send_detail"."group_id" = :group_status OR "tb_send_detail"."group_id" = :group_statusNone) '
        if self.pick_datetime != None:
            where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '   
        if self.group_status == "true":
            where_sql += ' AND ("tb_send_detail"."group_id" = :group_status OR "tb_send_detail"."group_id" IS NULL) ' 
        text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
            INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
            INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
        # print(where_sql)
            
        if typequery == 'sum':
            ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
            where_sql = 'WHERE status=:status AND "recipient_email" LIKE :recipient_email '
            if self.tax_id != '':
                where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id 
            if self.group_status == "true":
                where_sql += ' AND ("tb_send_detail"."group_id" = :group_status OR "tb_send_detail"."group_id" IS NULL) '   
            if self.pick_datetime != None:
                where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) ' 
            with slave.connect() as connection:
                result_all = connection.execute(text_sql \
                    ,status=status_ACTIVE,recipient_email=search,document_type=self.document_type,biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                where_sql += ' AND "tb_send_detail".document_status=:r_status'   
                if self.tax_id != '':
                    where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
                else:
                    where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'     
                text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                # -----------------------------------------
                # text_sql_str = text('SELECT "tb_send_detail".* FROM "tb_send_detail" \
                #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                # ------------------------------------------
                text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                    "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                    "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                    "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                    "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                    "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                    "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
                    FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                result_r = connection.execute(text_sql \
                    ,status=status_ACTIVE,recipient_email=search,r_status='R',biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                result_y = connection.execute(text_sql \
                    ,status=status_ACTIVE,recipient_email=search,r_status='Y',biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                result_n = connection.execute(text_sql_str \
                    ,status=status_ACTIVE,recipient_email=search,r_status='N',biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query_temp = [dict(row) for row in result_all]
            statusFile_count_reject = [dict(row) for row in result_r]
            statusFile_count_approve = [dict(row) for row in result_y]
            query = [dict(row) for row in result_n]
        elif typequery == 'sum_filter':
            ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
            where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
            with slave.connect() as connection:
                if self.group_status == "true":
                    where_sql += ' AND ("tb_send_detail"."group_id" = :group_status OR "tb_send_detail"."group_id" IS NULL) ' 
                if self.pick_datetime != None:
                    where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '  
                result_all = connection.execute(text_sql \
                    ,status=status_ACTIVE,recipient_email=search,document_type=self.document_type,biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                where_sql += ' AND "tb_send_detail".document_status=:r_status'
                if self.tax_id != '':
                    where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
                else:
                    where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'   
                text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                # -----------------------------------------------------
                # text_sql_str = text('SELECT "tb_send_detail".* FROM "tb_send_detail" \
                #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                # ------------------------------------------------------
                text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                    "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                    "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                    "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                    "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                    "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                    "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
                    FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                result_r = connection.execute(text_sql \
                    ,status=status_ACTIVE,recipient_email=search,r_status='R',document_type=self.document_type,biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                result_y = connection.execute(text_sql \
                    ,status=status_ACTIVE,recipient_email=search,r_status='Y',document_type=self.document_type,biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                result_n = connection.execute(text_sql_str \
                    ,status=status_ACTIVE,recipient_email=search,r_status='N',document_type=self.document_type,biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query_temp = [dict(row) for row in result_all]
            statusFile_count_reject = [dict(row) for row in result_r]
            statusFile_count_approve = [dict(row) for row in result_y]
            query = [dict(row) for row in result_n]
        elif typequery == 'sum_recipient_search':
            try:
                ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
                where_sql = 'WHERE status=:status AND "recipient_email" LIKE :recipient_email '
                if self.pick_datetime != None:
                    where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) ' 
                with slave.connect() as connection:
                    result_all = connection.execute(text_sql \
                        ,status=status_ACTIVE,recipient_email=search,document_type=self.document_type,biz_info_none='None',biz_info='',keyword=search_keyword,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                    where_sql += ' AND "tb_send_detail".document_status=:r_status'   
                    if self.tax_id != '':
                        where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
                    else:
                        where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'     
                    if self.keyword != '':
                        where_sql += ' AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword) '  
                    if self.document_type != '':     
                        where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
                    if self.group_status == True:
                        where_sql += ' AND ("tb_send_detail"."group_id" = :group_status OR "tb_send_detail"."group_id" = :group_statusNone) '  
                    text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
                        INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                        INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                    text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                        "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                        "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                        "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                        "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                        "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                        "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
                        FROM "tb_send_detail" \
                        INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                        INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                    result_r = connection.execute(text_sql \
                        ,status=status_ACTIVE,recipient_email=search,r_status='R',biz_info_none='None',biz_info='',keyword=search_keyword,document_type=self.document_type,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                    result_y = connection.execute(text_sql \
                        ,status=status_ACTIVE,recipient_email=search,r_status='Y',biz_info_none='None',biz_info='',keyword=search_keyword,document_type=self.document_type,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                    result_n = connection.execute(text_sql_str \
                        ,status=status_ACTIVE,recipient_email=search,r_status='N',biz_info_none='None',biz_info='',keyword=search_keyword,document_type=self.document_type,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                    connection.close()
                query_temp = [dict(row) for row in result_all]
                statusFile_count_reject = [dict(row) for row in result_r]
                statusFile_count_approve = [dict(row) for row in result_y]
                query = [dict(row) for row in result_n]
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(e)}
        elif typequery == 'sum_recipient_external':
            ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
            if self.document_type != '':  
                where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
            if self.group_status == "true":
                where_sql += ' AND ("tb_send_detail"."group_id" = :group_status OR "tb_send_detail"."group_id" IS NULL) ' 
            if self.pick_datetime != None:
                where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '  
            with slave.connect() as connection:
                result_all = connection.execute(text_sql \
                    ,status=status_ACTIVE,recipient_email=search,document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,biz_info_data=self.tax_id,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                where_sql += ' AND "tb_send_detail".document_status=:r_status'
                
                # print(where_sql)
                text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                # ------------------------------------------------------
                text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                    "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                    "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                    "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                    "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                    "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                    "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
                    FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                result_r = connection.execute(text_sql \
                    ,status=status_ACTIVE,recipient_email=search,r_status='R',document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,biz_info_data=self.tax_id,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                result_y = connection.execute(text_sql \
                    ,status=status_ACTIVE,recipient_email=search,r_status='Y',document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,biz_info_data=self.tax_id,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                result_n = connection.execute(text_sql_str \
                    ,status=status_ACTIVE,recipient_email=search,r_status='N',document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,biz_info_data=self.tax_id,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query_temp = [dict(row) for row in result_all]
            statusFile_count_reject = [dict(row) for row in result_r]
            statusFile_count_approve = [dict(row) for row in result_y]
            query = [dict(row) for row in result_n]
        elif typequery == 'sum_filter_recipient_external':
            ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
            if self.document_type != '':  
                where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
            if self.group_status == "true":
                where_sql += ' AND ("tb_send_detail"."group_id" = :group_status OR "tb_send_detail"."group_id" IS NULL) ' 
            if self.pick_datetime != None:
                where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '  
            with slave.connect() as connection:
                result_all = connection.execute(text_sql \
                    ,status=status_ACTIVE,recipient_email=search,document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                where_sql += ' AND "tb_send_detail".document_status=:r_status'
                # if type(self.tax_id) is str:
                #     where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
                # elif type(self.tax_id) is list:
                #     for n in self.tax_id:
                #         tmp_taxid = "'%''" + n + "''%'"
                #         where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + ')) '
                #     where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null) ' 
                text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                # -----------------------------------------------------
                # text_sql_str = text('SELECT "tb_send_detail".* FROM "tb_send_detail" \
                #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                # ------------------------------------------------------
                text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                    "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                    "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                    "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                    "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                    "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                    "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
                    FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                # print(where_sql)
                result_r = connection.execute(text_sql \
                    ,status=status_ACTIVE,recipient_email=search,r_status='R',document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                result_y = connection.execute(text_sql \
                    ,status=status_ACTIVE,recipient_email=search,r_status='Y',document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                result_n = connection.execute(text_sql_str \
                    ,status=status_ACTIVE,recipient_email=search,r_status='N',document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query_temp = [dict(row) for row in result_all]
            statusFile_count_reject = [dict(row) for row in result_r]
            statusFile_count_approve = [dict(row) for row in result_y]
            query = [dict(row) for row in result_n]
        elif typequery == 'sum_search_recipient_external':
            try:
                ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
                where_sql += ' AND status=:status AND "recipient_email" LIKE :recipient_email '
                if self.pick_datetime != None:
                    where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '  
                with slave.connect() as connection:
                    result_all = connection.execute(text_sql \
                        ,status=status_ACTIVE,recipient_email=search,document_type=self.document_type,biz_info_none='None',biz_info='',keyword=search_keyword,biz_info_null=None,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                    where_sql += ' AND "tb_send_detail".document_status=:r_status'   
                    # if self.tax_id != '':
                    #     where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
                    # else:
                    #     where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'     
                    if self.keyword != '':
                        where_sql += ' AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword) '  
                    if self.document_type != '':     
                        where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
                    text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
                        INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                        INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                    text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                        "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                        "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                        "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                        "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                        "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                        "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
                        FROM "tb_send_detail" \
                        INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                        INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
                    result_r = connection.execute(text_sql \
                        ,status=status_ACTIVE,recipient_email=search,r_status='R',biz_info_none='None',biz_info='',keyword=search_keyword,document_type=self.document_type,biz_info_null=None,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                    result_y = connection.execute(text_sql \
                        ,status=status_ACTIVE,recipient_email=search,r_status='Y',biz_info_none='None',biz_info='',keyword=search_keyword,document_type=self.document_type,biz_info_null=None,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                    result_n = connection.execute(text_sql_str \
                        ,status=status_ACTIVE,recipient_email=search,r_status='N',biz_info_none='None',biz_info='',keyword=search_keyword,document_type=self.document_type,biz_info_null=None,group_status='[]',group_statusNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                    connection.close()
                query_temp = [dict(row) for row in result_all]
                statusFile_count_reject = [dict(row) for row in result_r]
                statusFile_count_approve = [dict(row) for row in result_y]
                query = [dict(row) for row in result_n]
            except Exception as e:
                print(str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(e)}
        
        statusFile_count_reject = statusFile_count_reject[0]['count']
        statusFile_count_approve = statusFile_count_approve[0]['count']
        query_temp = query_temp[0]['count']
        try:
            end_time = (time.time())
            arr = []
            for u in range(len(query)):
                arr_email_document = []
                tmp_req_email = []
                tmp_dict_json = query[u]
                tmpdocument_status = tmp_dict_json['document_status']
                tmpstatus_detail = tmp_dict_json['status_details']
                if tmpstatus_detail != None:
                    tmpstatus_detail = eval(tmpstatus_detail)
                    if tmpdocument_status == 'N':
                        for x in range(len(tmpstatus_detail)):
                            if self.email_one not in arr_email_document:
                                if self.email_one in tmpstatus_detail[x]['email']:
                                    if tmpstatus_detail[x]['step_status_code'] == 'W':
                                        arr_email_document.append(self.email_one)
                                        tmpdocument_status = tmpstatus_detail[x]['step_status_code']
                                        break
                                    else:
                                        tmpdocument_status = tmpstatus_detail[x]['step_status_code']
                if tmpdocument_status == 'W':
                    statusFile_count_wait = statusFile_count_wait + 1
                elif tmpdocument_status == 'Z':
                    statusFile_count_Z = statusFile_count_Z + 1
                else:
                    statusFile_count_pendding = statusFile_count_pendding + 1
            # print(statusFile_count_Z,statusFile_count_pendding,statusFile_count_approve,statusFile_count_reject,statusFile_count_wait)
            json_Data['status_document']  = {
                'status_z':statusFile_count_Z,
                'incomplete':statusFile_count_pendding,
                'complete':statusFile_count_approve,
                'reject':statusFile_count_reject,
                'wait':statusFile_count_wait
            }
            json_Data['sum_document'] = query_temp
            return {'result':'OK','messageText':json_Data}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(e)}

    # def select_recp_count_v1(self,typequery,email_one,document_type,tax_id,keyword,group_status=None):
    #     self.typequery = typequery
    #     self.email_one = email_one
    #     self.document_type = document_type
    #     self.tax_id = tax_id
    #     self.keyword = keyword
    #     self.group_status = group_status
    #     status_ACTIVE = 'ACTIVE'
    #     sid_list = []
    #     sid_list_email = []
    #     json_Data = {}
    #     list_arr = []
    #     list_json = []
    #     tmp_list = []             
    #     count_rowDocument = 0
    #     count_rowDocument_StatusActive = 0
    #     count_rowDocument_StatusReject = 0
    #     count_rowDocument_StatusCancel = 0
    #     statusFile_count_approve = 0
    #     statusFile_count_pendding = 0
    #     statusFile_count_reject = 0
    #     statusFile_count_wait = 0
    #     statusFile_count_Z = 0
    #     list_temp_query = []
    #     tmp_sid_code_list = []
    #     arr_gruop = []
    #     arr_group_sid = []
    #     tmp_arr_sid = []
    #     tmp_group_id = None
    #     query_temp = 0
    #     str_time = (time.time())
    #     search = "%'{}'%".format(self.email_one) 
    #     search_tax_id = "'%''{}''%'".format(self.tax_id)
    #     search_keyword = "%{}%".format(self.keyword)
    #     # search_tax_id = "'%''{}''%'".format(self.tax_id)
    #     ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
    #     where_sql = 'WHERE status=:status AND "recipient_email" LIKE :recipient_email ' 
    #     # print(self.tax_id)
    #     if self.tax_id != '':
    #         if type(self.tax_id) is str:
    #             where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
    #         elif type(self.tax_id) is list:
    #             for n in self.tax_id:
    #                 tmp_taxid = "'%''" + n + "''%'"
    #                 where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + ')) '
    #             where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null) '
    #             # where_sql += ' AND ("tb_step_data".biz_info != ANY(:biz_info_data)) AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null)'
    #     else:
    #         where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'
    #     # print(self.document_type)
    #     if self.document_type != '':     
    #         where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
    #     if self.keyword != '':
    #         where_sql += ' AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword)'  
    #     # if self.group_status == True:
    #     #     where_sql += ' AND ("tb_send_detail"."group_id" = :group_status OR "tb_send_detail"."group_id" = :group_statusNone) '
        
    #     if self.group_status == "true":
    #         where_sql += ' AND ("tb_send_detail"."group_id" = :group_status OR "tb_send_detail"."group_id" IS NULL) ' 
    #     text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
    #         INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #         INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #     # print(where_sql)
            
    #     if typequery == 'sum':
    #         ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
    #         where_sql = 'WHERE status=:status AND "recipient_email" LIKE :recipient_email '
    #         if self.tax_id != '':
    #             where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id 
    #         if self.group_status == "true":
    #             where_sql += ' AND ("tb_send_detail"."group_id" = :group_status OR "tb_send_detail"."group_id" IS NULL) '   
    #         with slave.connect() as connection:
    #             result_all = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,recipient_email=search,document_type=self.document_type,biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None)
    #             where_sql += ' AND "tb_send_detail".document_status=:r_status'   
    #             if self.tax_id != '':
    #                 where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
    #             else:
    #                 where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'     
    #             text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             # -----------------------------------------
    #             # text_sql_str = text('SELECT "tb_send_detail".* FROM "tb_send_detail" \
    #             #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #             #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             # ------------------------------------------
    #             text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                 "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                 "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                 "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                 "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                 "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                 "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
    #                 FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             result_r = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,recipient_email=search,r_status='R',biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None)
    #             result_y = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,recipient_email=search,r_status='Y',biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None)
    #             result_n = connection.execute(text_sql_str \
    #                 ,status=status_ACTIVE,recipient_email=search,r_status='N',biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None)
    #             connection.close()
    #         query_temp = [dict(row) for row in result_all]
    #         statusFile_count_reject = [dict(row) for row in result_r]
    #         statusFile_count_approve = [dict(row) for row in result_y]
    #         query = [dict(row) for row in result_n]
    #     elif typequery == 'sum_filter':
    #         ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
    #         where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
    #         with slave.connect() as connection:
    #             if self.group_status == "true":
    #                 where_sql += ' AND ("tb_send_detail"."group_id" = :group_status OR "tb_send_detail"."group_id" IS NULL) ' 
    #             result_all = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,recipient_email=search,document_type=self.document_type,biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None)
    #             where_sql += ' AND "tb_send_detail".document_status=:r_status'
    #             if self.tax_id != '':
    #                 where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
    #             else:
    #                 where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'   
    #             text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             # -----------------------------------------------------
    #             # text_sql_str = text('SELECT "tb_send_detail".* FROM "tb_send_detail" \
    #             #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #             #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             # ------------------------------------------------------
    #             text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                 "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                 "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                 "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                 "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                 "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                 "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
    #                 FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             result_r = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,recipient_email=search,r_status='R',document_type=self.document_type,biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None)
    #             result_y = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,recipient_email=search,r_status='Y',document_type=self.document_type,biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None)
    #             result_n = connection.execute(text_sql_str \
    #                 ,status=status_ACTIVE,recipient_email=search,r_status='N',document_type=self.document_type,biz_info_none='None',biz_info='',group_status='[]',group_statusNone=None)
    #             connection.close()
    #         query_temp = [dict(row) for row in result_all]
    #         statusFile_count_reject = [dict(row) for row in result_r]
    #         statusFile_count_approve = [dict(row) for row in result_y]
    #         query = [dict(row) for row in result_n]
    #     elif typequery == 'sum_recipient_search':
    #         try:
    #             ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
    #             where_sql = 'WHERE status=:status AND "recipient_email" LIKE :recipient_email '
    #             with slave.connect() as connection:
    #                 result_all = connection.execute(text_sql \
    #                     ,status=status_ACTIVE,recipient_email=search,document_type=self.document_type,biz_info_none='None',biz_info='',keyword=search_keyword,group_status='[]',group_statusNone=None)
    #                 where_sql += ' AND "tb_send_detail".document_status=:r_status'   
    #                 if self.tax_id != '':
    #                     where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
    #                 else:
    #                     where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'     
    #                 if self.keyword != '':
    #                     where_sql += ' AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword) '  
    #                 if self.document_type != '':     
    #                     where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
    #                 if self.group_status == True:
    #                     where_sql += ' AND ("tb_send_detail"."group_id" = :group_status OR "tb_send_detail"."group_id" = :group_statusNone) '  
    #                 text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
    #                     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #                 text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                     "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                     "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                     "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                     "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                     "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                     "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
    #                     FROM "tb_send_detail" \
    #                     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #                 result_r = connection.execute(text_sql \
    #                     ,status=status_ACTIVE,recipient_email=search,r_status='R',biz_info_none='None',biz_info='',keyword=search_keyword,document_type=self.document_type,group_status='[]',group_statusNone=None)
    #                 result_y = connection.execute(text_sql \
    #                     ,status=status_ACTIVE,recipient_email=search,r_status='Y',biz_info_none='None',biz_info='',keyword=search_keyword,document_type=self.document_type,group_status='[]',group_statusNone=None)
    #                 result_n = connection.execute(text_sql_str \
    #                     ,status=status_ACTIVE,recipient_email=search,r_status='N',biz_info_none='None',biz_info='',keyword=search_keyword,document_type=self.document_type,group_status='[]',group_statusNone=None)
    #                 connection.close()
    #             query_temp = [dict(row) for row in result_all]
    #             statusFile_count_reject = [dict(row) for row in result_r]
    #             statusFile_count_approve = [dict(row) for row in result_y]
    #             query = [dict(row) for row in result_n]
    #         except Exception as e:
    #             exc_type, exc_obj, exc_tb = sys.exc_info()
    #             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #             print(exc_type, fname, exc_tb.tb_lineno)
    #             return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(e)}
    #     elif typequery == 'sum_recipient_external':
    #         ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
    #         if self.document_type != '':  
    #             where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
    #         if self.group_status == "true":
    #             where_sql += ' AND ("tb_send_detail"."group_id" = :group_status OR "tb_send_detail"."group_id" IS NULL) ' 
    #         with slave.connect() as connection:
    #             result_all = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,recipient_email=search,document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,biz_info_data=self.tax_id,group_status='[]',group_statusNone=None)
    #             where_sql += ' AND "tb_send_detail".document_status=:r_status'
                
    #             # print(where_sql)
    #             text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             # ------------------------------------------------------
    #             text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                 "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                 "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                 "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                 "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                 "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                 "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
    #                 FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             result_r = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,recipient_email=search,r_status='R',document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,biz_info_data=self.tax_id,group_status='[]',group_statusNone=None)
    #             result_y = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,recipient_email=search,r_status='Y',document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,biz_info_data=self.tax_id,group_status='[]',group_statusNone=None)
    #             result_n = connection.execute(text_sql_str \
    #                 ,status=status_ACTIVE,recipient_email=search,r_status='N',document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,biz_info_data=self.tax_id,group_status='[]',group_statusNone=None)
    #             connection.close()
    #         query_temp = [dict(row) for row in result_all]
    #         statusFile_count_reject = [dict(row) for row in result_r]
    #         statusFile_count_approve = [dict(row) for row in result_y]
    #         query = [dict(row) for row in result_n]
    #     elif typequery == 'sum_filter_recipient_external':
    #         ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
    #         if self.document_type != '':  
    #             where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
    #         if self.group_status == "true":
    #             where_sql += ' AND ("tb_send_detail"."group_id" = :group_status OR "tb_send_detail"."group_id" IS NULL) ' 
    #         with slave.connect() as connection:
    #             result_all = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,recipient_email=search,document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,group_status='[]',group_statusNone=None)
    #             where_sql += ' AND "tb_send_detail".document_status=:r_status'
    #             # if type(self.tax_id) is str:
    #             #     where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
    #             # elif type(self.tax_id) is list:
    #             #     for n in self.tax_id:
    #             #         tmp_taxid = "'%''" + n + "''%'"
    #             #         where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + ')) '
    #             #     where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null) ' 
    #             text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             # -----------------------------------------------------
    #             # text_sql_str = text('SELECT "tb_send_detail".* FROM "tb_send_detail" \
    #             #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #             #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             # ------------------------------------------------------
    #             text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                 "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                 "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                 "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                 "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                 "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                 "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
    #                 FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #             print(where_sql)
    #             result_r = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,recipient_email=search,r_status='R',document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,group_status='[]',group_statusNone=None)
    #             result_y = connection.execute(text_sql \
    #                 ,status=status_ACTIVE,recipient_email=search,r_status='Y',document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,group_status='[]',group_statusNone=None)
    #             result_n = connection.execute(text_sql_str \
    #                 ,status=status_ACTIVE,recipient_email=search,r_status='N',document_type=self.document_type,biz_info_none='None',biz_info='',biz_info_null=None,group_status='[]',group_statusNone=None)
    #             connection.close()
    #         query_temp = [dict(row) for row in result_all]
    #         statusFile_count_reject = [dict(row) for row in result_r]
    #         statusFile_count_approve = [dict(row) for row in result_y]
    #         query = [dict(row) for row in result_n]
    #     elif typequery == 'sum_search_recipient_external':
    #         try:
    #             ORDER_sql = 'ORDER BY "tb_send_detail".send_time DESC '
    #             where_sql += ' AND status=:status AND "recipient_email" LIKE :recipient_email '
    #             with slave.connect() as connection:
    #                 result_all = connection.execute(text_sql \
    #                     ,status=status_ACTIVE,recipient_email=search,document_type=self.document_type,biz_info_none='None',biz_info='',keyword=search_keyword,biz_info_null=None,group_status='[]',group_statusNone=None)
    #                 where_sql += ' AND "tb_send_detail".document_status=:r_status'   
    #                 # if self.tax_id != '':
    #                 #     where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id  
    #                 # else:
    #                 #     where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR ' + ' "tb_step_data".biz_info = :biz_info)'     
    #                 if self.keyword != '':
    #                     where_sql += ' AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword) '  
    #                 if self.document_type != '':     
    #                     where_sql += ' AND "tb_doc_detail"."documentType"=:document_type'
    #                 text_sql = text('SELECT COUNT("tb_send_detail"."id") FROM "tb_send_detail" \
    #                     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #                 text_sql_str = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                     "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                     "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                     "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                     "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                     "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                     "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign" \
    #                     FROM "tb_send_detail" \
    #                     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #                 result_r = connection.execute(text_sql \
    #                     ,status=status_ACTIVE,recipient_email=search,r_status='R',biz_info_none='None',biz_info='',keyword=search_keyword,document_type=self.document_type,biz_info_null=None,group_status='[]',group_statusNone=None)
    #                 result_y = connection.execute(text_sql \
    #                     ,status=status_ACTIVE,recipient_email=search,r_status='Y',biz_info_none='None',biz_info='',keyword=search_keyword,document_type=self.document_type,biz_info_null=None,group_status='[]',group_statusNone=None)
    #                 result_n = connection.execute(text_sql_str \
    #                     ,status=status_ACTIVE,recipient_email=search,r_status='N',biz_info_none='None',biz_info='',keyword=search_keyword,document_type=self.document_type,biz_info_null=None,group_status='[]',group_statusNone=None)
    #                 connection.close()
    #             query_temp = [dict(row) for row in result_all]
    #             statusFile_count_reject = [dict(row) for row in result_r]
    #             statusFile_count_approve = [dict(row) for row in result_y]
    #             query = [dict(row) for row in result_n]
    #         except Exception as e:
    #             print(str(e))
    #             exc_type, exc_obj, exc_tb = sys.exc_info()
    #             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #             print(exc_type, fname, exc_tb.tb_lineno)
    #             return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(e)}
        
    #     statusFile_count_reject = statusFile_count_reject[0]['count']
    #     statusFile_count_approve = statusFile_count_approve[0]['count']
    #     query_temp = query_temp[0]['count']
    #     try:
    #         end_time = (time.time())
    #         arr = []
    #         for u in range(len(query)):
    #             arr_email_document = []
    #             tmp_req_email = []
    #             tmp_dict_json = query[u]
    #             tmpdocument_status = tmp_dict_json['document_status']
    #             tmpstatus_detail = tmp_dict_json['status_details']
    #             if tmpstatus_detail != None:
    #                 tmpstatus_detail = eval(tmpstatus_detail)
    #                 if tmpdocument_status == 'N':
    #                     for x in range(len(tmpstatus_detail)):
    #                         if self.email_one not in arr_email_document:
    #                             if self.email_one in tmpstatus_detail[x]['email']:
    #                                 if tmpstatus_detail[x]['step_status_code'] == 'W':
    #                                     arr_email_document.append(self.email_one)
    #                                     tmpdocument_status = tmpstatus_detail[x]['step_status_code']
    #                                     break
    #                                 else:
    #                                     tmpdocument_status = tmpstatus_detail[x]['step_status_code']
    #             if tmpdocument_status == 'W':
    #                 statusFile_count_wait = statusFile_count_wait + 1
    #             elif tmpdocument_status == 'Z':
    #                 statusFile_count_Z = statusFile_count_Z + 1
    #             else:
    #                 statusFile_count_pendding = statusFile_count_pendding + 1
    #         # print(statusFile_count_Z,statusFile_count_pendding,statusFile_count_approve,statusFile_count_reject,statusFile_count_wait)
    #         json_Data['status_document']  = {
    #             'status_z':statusFile_count_Z,
    #             'incomplete':statusFile_count_pendding,
    #             'complete':statusFile_count_approve,
    #             'reject':statusFile_count_reject,
    #             'wait':statusFile_count_wait
    #         }
    #         json_Data['sum_document'] = query_temp
    #         return {'result':'OK','messageText':json_Data}
    #     except Exception as e:
    #         print(str(e))
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         print(exc_type, fname, exc_tb.tb_lineno)
    #         return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(e)}

    def select_recp_new_v1(self,typequery,email_one,limit,offset,document_type,keyword,status,tax_id,sort_key,group_status=None,pick_datetime=None,timestamp=None,tmptimeapprove=None):
        self.typequery = typequery
        self.email_one = email_one
        self.tax_id = tax_id
        self.limit = ''
        self.offset = ''
        if limit != '':
            self.limit = int(limit)
        if offset != '':
            self.offset = int(offset)
        self.document_type = document_type
        self.keyword = keyword
        self.status = status
        self.group_status = group_status
        status_ACTIVE = 'ACTIVE'
        self.all_status = ['W','N','Z']
        if sort_key != None:
            self.sort_key = sort_key.lower()
        else:
            self.sort_key = sort_key
        self.before_datetime = None
        self.after_datetime = None
        self.pick_datetime = pick_datetime
        self.timestamp = timestamp
        self.tmptimeapprove = tmptimeapprove
        if self.tmptimeapprove != None:
            self.tmptimeapprove = tmptimeapprove
        if self.pick_datetime != None:
            if self.pick_datetime != "":
                self.pick_datetime = int(self.pick_datetime)
                self.search_datetime = datetime.datetime.fromtimestamp(self.pick_datetime).strftime('%Y-%m-%d')
                self.before_datetime = str(self.search_datetime) + 'T00:00:00'
                self.after_datetime = str(self.search_datetime) + 'T23:59:59'
        # print(self.before_datetime,self.after_datetime)
        # print(self.pick_datetime)
        search = "%'{}'%".format(self.email_one)
        search_keyword = "%{}%".format(self.keyword)
        search_tax_id = "'%''{}''%'".format(self.tax_id)
        arr_list_sum = []
        sum_row_tooffset = 0
        keep_lenstatus = []
        list_arr = []
        tmp_sid_code_list =  []
        tmp_list = []      
        a = 0       
        count_rowDocument = 0
        count_rowDocument_StatusActive = 0
        count_rowDocument_StatusReject = 0
        count_rowDocument_StatusCancel = 0
        statusFile_count_approve = 0
        statusFile_count_pendding = 0
        statusFile_count_reject = 0
        statusFile_count_wait = 0
        list_temp_query = []
        tmp_sid_code_list = []
        arr_gruop = []
        arr_group_sid = []
        tmp_arr_sid = []
        tmp_group_id = None
        json_Data = {}
        str_time = (time.time())
        # print(self.tax_id)
        if self.tmptimeapprove == True:
            if self.sort_key == None:
                ORDER_sql = ' ORDER BY "tb_step_data".update_time DESC LIMIT :limit OFFSET :offset '
            else:
                if self.sort_key == 'desc':
                    ORDER_sql = ' ORDER BY "tb_step_data".update_time DESC LIMIT :limit OFFSET :offset '
                else:
                    ORDER_sql = ' ORDER BY "tb_step_data".update_time ASC LIMIT :limit OFFSET :offset '
        else:
            if self.sort_key == None:
                ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
            else:
                if self.sort_key == 'desc':
                    ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
                else:
                    ORDER_sql = ' ORDER BY "tb_send_detail".send_time ASC LIMIT :limit OFFSET :offset '
        where_sql = 'WHERE status=:status AND "recipient_email" LIKE :recipient_email '
        # bizinfo = ["'%''5513213355654''%'","'%''3897235192540''%'","'%''6529446796215''%'"]
        # print(dict(bizinfo))
        # bizinfo = "'{"'%''5513213355654''%'","'%''3897235192540''%'","'%''6529446796215''%'"}'"
        if self.tax_id != '':
            if type(self.tax_id) is str:
                where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id
            elif type(self.tax_id) is list:
                for n in self.tax_id:
                    tmp_taxid = "'%''" + n + "''%'"
                    where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + '))'
                where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null)'
        else:
            where_sql += ''
        
        if typequery == 'recipient':
            with slave.connect() as connection:
                if self.group_status == "true":
                    where_sql += ' AND ("tb_send_detail"."group_id"=:group_idtmp OR "tb_send_detail"."group_id" IS NULL) '
                if self.pick_datetime != None:
                    where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '                    
                where_sql += ORDER_sql
                print(where_sql)
                # print(where_sql)
                # result = connection.execute(text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
                #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid '+ where_sql)\
                #     ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,biz_info='',biz_info_none='None')
                result = connection.execute(text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                        "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                        "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                        "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                        "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                        "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                        "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
                        "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
                        "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
                        "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
                        "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
                        "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
                    FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid '+ where_sql)\
                    ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,biz_info='',biz_info_none='None',group_idtmp='[]',group_idNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query = [dict(row) for row in result]
        elif typequery == 'recipient_update':
            date_time_from_ts = datetime.datetime.fromtimestamp(int(self.timestamp)).strftime('%Y-%m-%d %H:%M:%S')
            with slave.connect() as connection:
                if self.group_status == "true":
                    where_sql += ' AND ("tb_send_detail"."group_id"=:group_idtmp OR "tb_send_detail"."group_id" IS NULL) '
                if self.pick_datetime != None:
                    where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '   
                if self.timestamp != None:
                    where_sql += ' AND ("tb_step_data"."update_time" >= :date_time_from_ts) '                 
                where_sql += ORDER_sql
                # print(where_sql)
                # result = connection.execute(text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
                #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid '+ where_sql)\
                #     ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,biz_info='',biz_info_none='None')
                result = connection.execute(text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                        "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                        "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                        "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                        "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                        "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                        "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
                        "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
                        "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
                        "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
                        "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
                        "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
                    FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid '+ where_sql)\
                    ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,biz_info='',biz_info_none='None',group_idtmp='[]',group_idNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime,date_time_from_ts=date_time_from_ts)
                connection.close()
            query = [dict(row) for row in result]
        elif typequery == 'recipient_search':
            if self.document_type != '':
                where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
            if self.keyword != '':
                where_sql += 'AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword) '
            if self.pick_datetime != None:
                where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
            where_sql += ORDER_sql
            # print(where_sql)
            text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                        "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                        "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                        "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                        "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                        "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                        "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
                        "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
                        "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
                        "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
                        "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
                        "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
                        FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
            with slave.connect() as connection:
                result = connection.execute(text_sql\
                    ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,documentType=self.document_type,keyword=search_keyword,biz_info='',biz_info_none='None',before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query = [dict(row) for row in result]
        elif typequery == 'recipient_filter':
            if self.status in self.all_status:
                for i in range(self.limit):
                    if i > 0:
                        self.offset = self.offset + self.limit
                    if len(arr_list_sum) < self.limit:
                        arr_list_sum,sum_row_tooffset = recursive_select_recp_new_v1(self.email_one,self.limit,self.offset,self.status,arr_list_sum,sum_row_tooffset,self.document_type,self.tax_id,self.group_status,self.pick_datetime,self.sort_key,self.tmptimeapprove)
                        keep_lenstatus = arr_list_sum
                        sum_row_tooffset = self.offset + sum_row_tooffset
                        if len(keep_lenstatus) == len(arr_list_sum):
                            a = a + 1
                            if a == 5:
                                list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
                                json_Data['document'] = list_arr
                                json_Data['offset'] = sum_row_tooffset
                                return {'result':'OK','messageText':json_Data}                    
                    else:
                        list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
                        json_Data['document'] = list_arr
                        json_Data['offset'] = sum_row_tooffset
                        return {'result':'OK','messageText':json_Data} 
                list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
                json_Data['document'] = list_arr
                json_Data['offset'] = sum_row_tooffset
                print(len(list_arr))
                return {'result':'OK','messageText':json_Data}
            if self.status != '':
                where_sql += ' AND "tb_send_detail"."document_status" = :document_status '
            if self.document_type != '':
                where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
            if self.group_status == "true":
                where_sql += ' AND ("tb_send_detail"."group_id"=:group_idtmp OR "tb_send_detail"."group_id" IS NULL) '
            if self.pick_datetime != None:
                where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
            where_sql += ORDER_sql
            # text_sql = text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
            #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
            #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
            text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                        "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                        "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                        "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                        "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                        "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                        "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
                        "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
                        "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
                        "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
                        "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
                        "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
                    FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
            # print(text_sql , self.status)
            with slave.connect() as connection:
                result = connection.execute(text_sql\
                    ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,documentType=self.document_type,document_status=self.status,biz_info='',biz_info_none='None',group_idtmp='[]',group_idNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query = [dict(row) for row in result]
        elif typequery == 'recipient_filter_update':
            date_time_from_ts = datetime.datetime.fromtimestamp(int(self.timestamp)).strftime('%Y-%m-%d %H:%M:%S')
            if self.status in self.all_status:
                for i in range(self.limit):
                    if i > 0:
                        self.offset = self.offset + self.limit
                    if len(arr_list_sum) < self.limit:
                        arr_list_sum,sum_row_tooffset = recursive_select_recp_new_v1_update(self.email_one,self.limit,self.offset,self.status,arr_list_sum,sum_row_tooffset,self.document_type,self.tax_id,self.group_status,self.pick_datetime,self.sort_key,date_time_from_ts)
                        keep_lenstatus = arr_list_sum
                        sum_row_tooffset = self.offset + sum_row_tooffset
                        if len(keep_lenstatus) == len(arr_list_sum):
                            a = a + 1
                            if a == 5:
                                list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
                                json_Data['document'] = list_arr
                                json_Data['offset'] = sum_row_tooffset
                                print ('json_Data:',json_Data)
                                return {'result':'OK','messageText':json_Data}                    
                    else:
                        list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
                        json_Data['document'] = list_arr
                        json_Data['offset'] = sum_row_tooffset
                        return {'result':'OK','messageText':json_Data} 
                list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
                json_Data['document'] = list_arr
                json_Data['offset'] = sum_row_tooffset
                # print(len(list_arr))
                return {'result':'OK','messageText':json_Data}
            if self.status != '':
                where_sql += ' AND "tb_send_detail"."document_status" = :document_status '
            if self.document_type != '':
                where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
            if self.group_status == "true":
                where_sql += ' AND ("tb_send_detail"."group_id"=:group_idtmp OR "tb_send_detail"."group_id" IS NULL) '
            if self.pick_datetime != None:
                where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
            if self.timestamp != None:
                where_sql += ' AND ("tb_step_data"."update_time" >= :date_time_from_ts) '
            where_sql += ORDER_sql
            # text_sql = text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
            #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
            #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
            text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                        "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                        "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                        "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                        "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                        "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                        "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
                        "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
                        "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
                        "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
                        "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
                        "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
                    FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
            # print(text_sql , self.status)
            with slave.connect() as connection:
                result = connection.execute(text_sql\
                    ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,documentType=self.document_type,document_status=self.status,biz_info='',biz_info_none='None',group_idtmp='[]',group_idNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime,date_time_from_ts=date_time_from_ts)
                connection.close()
            query = [dict(row) for row in result]
        elif typequery == 'recipient_external':
            if self.pick_datetime != None:
                where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) ' 
            with slave.connect() as connection:
                where_sql += ORDER_sql
                result = connection.execute(text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                        "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                        "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                        "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                        "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                        "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                        "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
                        "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
                        "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
                        "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
                        "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
                        "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
                    FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid '+ where_sql)\
                    ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,biz_info_data=self.tax_id,biz_info='',biz_info_none='None',biz_info_null=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query = [dict(row) for row in result]
            # print(self.tax_id)
        elif typequery == 'recipient_external_search':
            if self.document_type != '':
                where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
            if self.keyword != '':
                where_sql += 'AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword) '
            if self.pick_datetime != None:
                where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
            where_sql += ORDER_sql
            text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                        "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                        "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                        "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                        "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                        "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                        "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
                        "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
                        "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
                        "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
                        "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
                        "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
                        FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
            with slave.connect() as connection:
                result = connection.execute(text_sql\
                    ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,documentType=self.document_type,keyword=search_keyword,biz_info='',biz_info_none='None',biz_info_null=None,group_idtmp='[]',group_idNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query = [dict(row) for row in result]
        elif typequery == 'filter_recipient_external':
            # date_time_from_ts = datetime.datetime.fromtimestamp(int(self.timestamp)).strftime('%Y-%m-%d %H:%M:%S')
            if self.status in self.all_status:
                for i in range(self.limit):
                    if i > 0:
                        self.offset = self.offset + self.limit
                        # print(self.offset)
                    # print(len(arr_list_sum),self.limit)
                    if len(arr_list_sum) < self.limit:
                        arr_list_sum,sum_row_tooffset = recursive_select_recp_new_v2(self.email_one,self.limit,self.offset,self.status,arr_list_sum,sum_row_tooffset,self.document_type,self.tax_id,self.sort_key,self.pick_datetime,self.tmptimeapprove)
                        keep_lenstatus = arr_list_sum
                        sum_row_tooffset = self.offset + sum_row_tooffset
                        if len(keep_lenstatus) == len(arr_list_sum):
                            a = a + 1
                            if a == 5:
                                list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
                                json_Data['document'] = list_arr
                                json_Data['offset'] = sum_row_tooffset
                                return {'result':'OK','messageText':json_Data}                    
                    else:
                        list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
                        json_Data['document'] = list_arr
                        json_Data['offset'] = sum_row_tooffset
                        return {'result':'OK','messageText':json_Data} 
                list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
                json_Data['document'] = list_arr
                json_Data['offset'] = sum_row_tooffset
                # print(len(list_arr))
                return {'result':'OK','messageText':json_Data}
            if self.status != '':
                where_sql += ' AND "tb_send_detail"."document_status" = :document_status '
            if self.document_type != '':
                where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
            if self.group_status == "true":
                where_sql += ' AND ("tb_send_detail"."group_id"=:group_idtmp OR "tb_send_detail"."group_id" IS NULL) '
            if self.pick_datetime != None:
                where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
            where_sql += ORDER_sql
            # text_sql = text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
            #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
            #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
            text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
                        "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
                        "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
                        "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
                        "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
                        "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
                        "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
                        "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
                        "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
                        "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
                        "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
                        "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
                    FROM "tb_send_detail" \
                    INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
                    INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
            # print(text_sql , self.status)
            with slave.connect() as connection:
                result = connection.execute(text_sql\
                    ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,documentType=self.document_type,document_status=self.status,biz_info='',biz_info_none='None',biz_info_null=None,group_idtmp='[]',group_idNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
                connection.close()
            query = [dict(row) for row in result]
        
        try:
            # max_ts = max(query,key=lambda item:item['update_time'])['update_time']
            # print ('max_ts:',max_ts)
            for x in range(len(query)):
                arr_email_document = []
                tmp_req_email = []
                email_step_sum_w = []
                tmpdata = query[x]
                tmp_sicode = tmpdata['step_data_sid']
                tmp_sid_code_list.append(tmp_sicode)
                tmp_send_time = tmpdata['send_time']
                tmp_document_id = tmpdata['doc_id']
                tmp_tracking_id = tmpdata['tracking_id']
                tmp_sender_name = tmpdata['sender_name']
                tmp_sender_email = tmpdata['sender_email']
                tmp_file_name = tmpdata['file_name']
                tmp_groupid = tmpdata['group_id']
                email_step_sum = tmpdata['recipient_email']
                update_time = tmpdata['update_time']       

                sender_name_eng = find_name_surename_by_username(tmp_sender_email)

                tmptime_update = update_time
                tmptime_update_timestamp = int(tmptime_update.timestamp())
                tmptime_update_string = str(update_time).split('+')[0]
                th_dateTime_2_last = convert_datetime_TH_2(tmptime_update_timestamp)
                ts = int(time.time())
                date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
                datetime_display_update = int(tmptime_update.timestamp())
                date_time_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%Y-%m-%d')
                yar_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%Y')
                time_show_db = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%H:%M')
                old_year = datetime.datetime.fromtimestamp(datetime_display_update).strftime('%d/%m/%Y')
                if date_time_today == date_time_db:
                    date_last_display_show = time_show_db
                else:
                    if year_today == yar_db:
                        date_last_display_show = convert_datetime_TH_2_display(datetime_display_update)
                    else:
                        date_last_display_show = old_year
                
                if email_step_sum != None:
                    email_step_sum = eval(email_step_sum)
                tmpstatus_detail = tmpdata['status_details']
                tmpdocument_status = tmpdata['document_status']
                tmpstepnow = tmpdata['stepnow']
                tmp_data_document = tmpdata['data_document']
                tmpdatadocument = None
                status_groupid = False
                if tmp_groupid != None:
                    if tmp_groupid != '':
                        tmp_groupid = eval(tmp_groupid)
                        if len(tmp_groupid) != 0:
                            status_groupid = True
                if tmpstepnow != None:
                    tmpstepnow = int(tmpstepnow)
                tmpstepmax = tmpdata['stepmax']
                if tmpstepmax != None:
                    tmpstepmax = int(tmpstepmax)
                if tmpstatus_detail != None:
                    tmpstatus_detail = eval(tmpstatus_detail)                            
                    for z in range(len(tmpstatus_detail)):
                        email_step_sum_w.append(tmpstatus_detail[z]['email'])

                    if tmpdocument_status == 'N':
                        for x in range(len(tmpstatus_detail)):
                            # print(tmp_sicode)
                            # print(tmpstatus_detail[x])
                            # email_step_sum_w.append(tmpstatus_detail[x]['email'])
                            if self.email_one not in arr_email_document:
                                if self.email_one in tmpstatus_detail[x]['email']:
                                    if tmpstatus_detail[x]['step_status_code'] == 'W':
                                        arr_email_document.append(self.email_one)
                                        tmpdocument_status = tmpstatus_detail[x]['step_status_code']
                                        break
                                    else:
                                        tmpdocument_status = tmpstatus_detail[x]['step_status_code']
                if tmpdocument_status == 'Z':
                    res_status_file_string = 'อยู่ในช่วงดำเนินการ'
                elif tmpdocument_status == 'W':
                    res_status_file_string = 'รอคุณอนุมัติ'
                elif tmpdocument_status == 'N':
                    res_status_file_string = 'กำลังดำเนินการ'
                elif tmpdocument_status == 'R':
                    res_status_file_string = 'เอกสารที่ส่งคืนแก้ไข'
                else:
                    res_status_file_string = 'เอกสารสมบูรณ์'
                tmp_sign_page_options = tmpdata['sign_page_options']
                tmp_document_type = tmpdata['documentType']
                tmp_options_page = []
                if tmpdata['options_page'] != None:
                    if tmpdata['options_page'] != '':
                    # print(tmp_dict_json['options_page'],tmp_document_id)
                        tmp_options_page = [eval(tmpdata['options_page'])]
                else:
                    tmp_options_page = []
                if len(tmp_options_page) != 0:
                    # print(tmp_options_page[0]['group_detail'])
                    tmp_status_group = False
                    if status_groupid == True:
                        if len(tmp_options_page) != 0:
                            if 'group_detail' in tmp_options_page[0]:
                                tmp_group_detail = tmp_options_page[0]['group_detail']
                                if 'group_status' in tmp_group_detail:
                                    if tmp_group_detail['group_status'] == True:
                                        tmp_status_group = True
                                        tmpstepnum = tmp_group_detail['step_num']
                if tmpdata['documentJson'] != None:
                    documentJson_result = eval(tmpdata['documentJson'])
                    documentName = documentJson_result['document_name']
                    documentType = documentJson_result['document_type']
                else:
                    documentName = None
                    documentType = None
                if tmpdata['urgent_type'] != None:
                    documentUrgentType = tmpdata['urgent_type']
                    if documentUrgentType == 'I':
                        documentUrgentString = 'ด่วนมาก'
                    elif documentUrgentType == 'U':
                        documentUrgentString = 'ด่วน'
                    elif documentUrgentType == 'M':
                        documentUrgentString = 'ปกติ'
                tmp_biz_info = None
                tmpdept_name = None
                tmprolename = None
                tmprole_level = None
                if tmpdata['biz_info'] != None:
                    if tmpdata['biz_info'] != 'None':
                        if tmpdata['biz_info'] != '':
                            eval_biz_info = json.dumps(tmpdata['biz_info'])
                            eval_biz_info = json.loads(eval_biz_info)
                            # print(eval_biz_info)
                            eval_biz_info = eval(eval_biz_info)
                            # eval_biz_info
                            # print(eval_biz_info)
                            if 'role_name' in eval_biz_info:
                                tmprolename =  eval_biz_info['role_name']                                
                            if 'dept_name' in eval_biz_info:
                                tmpdept_name =  eval_biz_info['dept_name']                               
                            if 'role_level' in eval_biz_info:
                                tmprole_level =  eval_biz_info['role_level']
                            if 'dept_name' in eval_biz_info:  
                                tmp_biz_info = {
                                    'tax_id':eval_biz_info['id_card_num'],
                                    'role_name' : tmprolename,
                                    'dept_name' : tmpdept_name,
                                    'role_level' : tmprole_level            
                                }                                
                            elif 'dept_name' not in eval_biz_info:
                                tmp_biz_info = {
                                    'tax_id':eval_biz_info['id_card_num'],
                                    'role_name' : eval_biz_info['role_name'],
                                    'dept_name' : [],
                                    'role_level' : eval_biz_info['role_level']               
                                }
                dateTime_String = tmp_send_time
                th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
                ts = int(time.time())
                date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
                datetime_display = int(dateTime_String.timestamp())
                date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
                yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
                time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
                old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
                if date_time_today == date_time_db:
                    date_display_show = time_show_db
                else:
                    if year_today == yar_db:
                        date_display_show = convert_datetime_TH_2_display(datetime_display)
                    else:
                        date_display_show = old_year
            # print(email_step_sum_w)
                if tmp_status_group == True:
                    for ui in range(len(tmpstepnum)):
                        intstepnum = tmpstepnum[ui] - 1
                        try:
                            for w in range(len(email_step_sum_w[intstepnum])):
                                tmp_req_email.append(email_step_sum_w[intstepnum][w])
                        except Exception as e:
                            tmp_req_email = []
                list_arr.append({
                    'group_email':tmp_req_email,
                    'group_id':None,
                    'group_status':tmp_status_group,
                    'sidCode':tmp_sicode,
                    'document_name':documentName,
                    'document_type':tmp_document_type,
                    'document_urgent':documentUrgentType,
                    'document_urgent_string':documentUrgentString,
                    'dateTime_String':str(dateTime_String).split('+')[0],
                    'dateTime_String_TH_1':th_dateTime_2,
                    'dateTime_display':date_display_show,
                    'document_id':tmp_document_id,
                    'stamp_all':tmp_sign_page_options,
                    'options_page_document':tmp_options_page,
                    'max_step':tmpstepmax,
                    'step_now':tmpstepnow,
                    # 'dateTime_String_TH_2':th_dateTime_2,
                    'date_String':str(dateTime_String).split(' ')[0],
                    'time_String':str(dateTime_String).split(' ')[1].split('+')[0],
                    'status_file_code':tmpdocument_status,
                    'status_file_string':res_status_file_string,
                    'dateTime':int(dateTime_String.timestamp()),
                    'tracking_id':tmp_tracking_id,
                    'sender_name':tmp_sender_name,
                    'sender_email':tmp_sender_email,
                    'file_name':tmp_file_name,
                    'document_business':tmp_biz_info,
                    'group':status_groupid,
                    'data_document':tmpdatadocument,
                    'update_last':tmptime_update,
                    'update_last_String_TH_1':th_dateTime_2_last,
                    'update_last_display':date_last_display_show,
                    'update_last_String':tmptime_update_string,
                    'update_last_TimeStamp':tmptime_update_timestamp,
                    'sender_name_eng' : sender_name_eng
                    # 'update_time' : update_time,
                    # 'update_time_str' : str(update_time)
                    # 'importance':importance,
                    # 'importance_string':importance_string,
                    # 'last_digitsign':last_digitsign,
                    # 'time_expire':expiry_date
                })
            list_arr = sorted(list_arr, key=lambda k: k['dateTime'], reverse=True)
            # print ('self.tmptimeapprove:',self.tmptimeapprove)
            if self.tmptimeapprove == True:
                list_arr = sorted(list_arr, key=lambda k: k['update_last_TimeStamp'], reverse=True)
            json_Data['document'] = list_arr
            json_Data['offset'] = self.offset + self.limit
            return {'result':'OK','messageText':json_Data}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(e)}

    # def select_recp_new_v1(self,typequery,email_one,limit,offset,document_type,keyword,status,tax_id,sort_key,group_status=None,pick_datetime=None,timestamp=None):
    #     self.typequery = typequery
    #     self.email_one = email_one
    #     self.tax_id = tax_id
    #     self.limit = ''
    #     self.offset = ''
    #     if limit != '':
    #         self.limit = int(limit)
    #     if offset != '':
    #         self.offset = int(offset)
    #     self.document_type = document_type
    #     self.keyword = keyword
    #     self.status = status
    #     self.group_status = group_status
    #     status_ACTIVE = 'ACTIVE'
    #     self.all_status = ['W','N','Z']
    #     if sort_key != None:
    #         self.sort_key = sort_key.lower()
    #     else:
    #         self.sort_key = sort_key
    #     self.before_datetime = None
    #     self.after_datetime = None
    #     self.pick_datetime = pick_datetime
    #     self.timestamp = timestamp
    #     if self.pick_datetime != None:
    #         if self.pick_datetime != "":
    #             self.pick_datetime = int(self.pick_datetime)
    #             self.search_datetime = datetime.datetime.fromtimestamp(self.pick_datetime).strftime('%Y-%m-%d')
    #             self.before_datetime = str(self.search_datetime) + 'T00:00:00'
    #             self.after_datetime = str(self.search_datetime) + 'T23:59:59'
    #     print(self.before_datetime,self.after_datetime)
    #     print(self.pick_datetime)
    #     search = "%'{}'%".format(self.email_one)
    #     search_keyword = "%{}%".format(self.keyword)
    #     search_tax_id = "'%''{}''%'".format(self.tax_id)
    #     arr_list_sum = []
    #     sum_row_tooffset = 0
    #     keep_lenstatus = []
    #     list_arr = []
    #     tmp_sid_code_list =  []
    #     tmp_list = []      
    #     a = 0       
    #     count_rowDocument = 0
    #     count_rowDocument_StatusActive = 0
    #     count_rowDocument_StatusReject = 0
    #     count_rowDocument_StatusCancel = 0
    #     statusFile_count_approve = 0
    #     statusFile_count_pendding = 0
    #     statusFile_count_reject = 0
    #     statusFile_count_wait = 0
    #     list_temp_query = []
    #     tmp_sid_code_list = []
    #     arr_gruop = []
    #     arr_group_sid = []
    #     tmp_arr_sid = []
    #     tmp_group_id = None
    #     json_Data = {}
    #     str_time = (time.time())
    #     # print(self.tax_id)
    #     if self.sort_key == None:
    #         ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
    #     else:
    #         if self.sort_key == 'desc':
    #             ORDER_sql = ' ORDER BY "tb_send_detail".send_time DESC LIMIT :limit OFFSET :offset '
    #         else:
    #             ORDER_sql = ' ORDER BY "tb_send_detail".send_time ASC LIMIT :limit OFFSET :offset '
    #     where_sql = 'WHERE status=:status AND "recipient_email" LIKE :recipient_email '
    #     # bizinfo = ["'%''5513213355654''%'","'%''3897235192540''%'","'%''6529446796215''%'"]
    #     # print(dict(bizinfo))
    #     # bizinfo = "'{"'%''5513213355654''%'","'%''3897235192540''%'","'%''6529446796215''%'"}'"
    #     if self.tax_id != '':
    #         if type(self.tax_id) is str:
    #             where_sql += ' AND "tb_step_data".biz_info LIKE ' + search_tax_id
    #         elif type(self.tax_id) is list:
    #             for n in self.tax_id:
    #                 tmp_taxid = "'%''" + n + "''%'"
    #                 where_sql += ' AND ("tb_step_data".biz_info NOT LIKE (' + tmp_taxid + '))'
    #             where_sql += ' AND ("tb_step_data".biz_info != :biz_info_none AND "tb_step_data".biz_info != :biz_info AND "tb_step_data".biz_info IS NOT :biz_info_null)'
    #     else:
    #         where_sql += ' AND ("tb_step_data".biz_info = :biz_info_none OR "tb_step_data".biz_info = :biz_info)'
        
    #     if typequery == 'recipient':
    #         with slave.connect() as connection:
    #             if self.group_status == "true":
    #                 where_sql += ' AND ("tb_send_detail"."group_id"=:group_idtmp OR "tb_send_detail"."group_id" IS NULL) '
    #             if self.pick_datetime != None:
    #                 where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '                    
    #             where_sql += ORDER_sql
    #             print(where_sql)
    #             # result = connection.execute(text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
    #             #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #             #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid '+ where_sql)\
    #             #     ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,biz_info='',biz_info_none='None')
    #             result = connection.execute(text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                     "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                     "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                     "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                     "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                     "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                     "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
    #                     "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
    #                     "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
    #                     "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
    #                     "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
    #                     "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
    #                 FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid '+ where_sql)\
    #                 ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,biz_info='',biz_info_none='None',group_idtmp='[]',group_idNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
    #             connection.close()
    #         query = [dict(row) for row in result]
    #     elif typequery == 'recipient_update':
    #         date_time_from_ts = datetime.datetime.fromtimestamp(int(self.timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    #         with slave.connect() as connection:
    #             if self.group_status == "true":
    #                 where_sql += ' AND ("tb_send_detail"."group_id"=:group_idtmp OR "tb_send_detail"."group_id" IS NULL) '
    #             if self.pick_datetime != None:
    #                 where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '   
    #             if self.timestamp != None:
    #                 where_sql += ' AND ("tb_step_data"."update_time" >= :date_time_from_ts) '                 
    #             where_sql += ORDER_sql
    #             print(where_sql)
    #             # result = connection.execute(text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
    #             #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #             #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid '+ where_sql)\
    #             #     ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,biz_info='',biz_info_none='None')
    #             result = connection.execute(text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                     "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                     "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                     "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                     "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                     "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                     "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
    #                     "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
    #                     "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
    #                     "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
    #                     "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
    #                     "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
    #                 FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid '+ where_sql)\
    #                 ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,biz_info='',biz_info_none='None',group_idtmp='[]',group_idNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime,date_time_from_ts=date_time_from_ts)
    #             connection.close()
    #         query = [dict(row) for row in result]
    #     elif typequery == 'recipient_search':
    #         if self.document_type != '':
    #             where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
    #         if self.keyword != '':
    #             where_sql += 'AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword) '
    #         if self.pick_datetime != None:
    #             where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
    #         where_sql += ORDER_sql
    #         print(where_sql)
    #         text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                     "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                     "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                     "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                     "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                     "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                     "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
    #                     "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
    #                     "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
    #                     "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
    #                     "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
    #                     "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
    #                     FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #         with slave.connect() as connection:
    #             result = connection.execute(text_sql\
    #                 ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,documentType=self.document_type,keyword=search_keyword,biz_info='',biz_info_none='None',before_datetime=self.before_datetime,after_datetime=self.after_datetime)
    #             connection.close()
    #         query = [dict(row) for row in result]
    #     elif typequery == 'recipient_filter':
    #         if self.status in self.all_status:
    #             for i in range(self.limit):
    #                 if i > 0:
    #                     self.offset = self.offset + self.limit
    #                 if len(arr_list_sum) < self.limit:
    #                     arr_list_sum,sum_row_tooffset = recursive_select_recp_new_v1(self.email_one,self.limit,self.offset,self.status,arr_list_sum,sum_row_tooffset,self.document_type,self.tax_id,self.group_status,self.pick_datetime,self.sort_key)
    #                     keep_lenstatus = arr_list_sum
    #                     sum_row_tooffset = self.offset + sum_row_tooffset
    #                     if len(keep_lenstatus) == len(arr_list_sum):
    #                         a = a + 1
    #                         if a == 5:
    #                             list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
    #                             json_Data['document'] = list_arr
    #                             json_Data['offset'] = sum_row_tooffset
    #                             return {'result':'OK','messageText':json_Data}                    
    #                 else:
    #                     list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
    #                     json_Data['document'] = list_arr
    #                     json_Data['offset'] = sum_row_tooffset
    #                     return {'result':'OK','messageText':json_Data} 
    #             list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
    #             json_Data['document'] = list_arr
    #             json_Data['offset'] = sum_row_tooffset
    #             print(len(list_arr))
    #             return {'result':'OK','messageText':json_Data}
    #         if self.status != '':
    #             where_sql += ' AND "tb_send_detail"."document_status" = :document_status '
    #         if self.document_type != '':
    #             where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
    #         if self.group_status == "true":
    #             where_sql += ' AND ("tb_send_detail"."group_id"=:group_idtmp OR "tb_send_detail"."group_id" IS NULL) '
    #         if self.pick_datetime != None:
    #             where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
    #         where_sql += ORDER_sql
    #         # text_sql = text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
    #         #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #         #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #         text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                     "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                     "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                     "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                     "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                     "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                     "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
    #                     "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
    #                     "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
    #                     "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
    #                     "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
    #                     "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
    #                 FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #         # print(text_sql , self.status)
    #         with slave.connect() as connection:
    #             result = connection.execute(text_sql\
    #                 ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,documentType=self.document_type,document_status=self.status,biz_info='',biz_info_none='None',group_idtmp='[]',group_idNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
    #             connection.close()
    #         query = [dict(row) for row in result]
    #     elif typequery == 'recipient_filter_update':
    #         date_time_from_ts = datetime.datetime.fromtimestamp(int(self.timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    #         if self.status in self.all_status:
    #             for i in range(self.limit):
    #                 if i > 0:
    #                     self.offset = self.offset + self.limit
    #                 if len(arr_list_sum) < self.limit:
    #                     arr_list_sum,sum_row_tooffset = recursive_select_recp_new_v1_update(self.email_one,self.limit,self.offset,self.status,arr_list_sum,sum_row_tooffset,self.document_type,self.tax_id,self.group_status,self.pick_datetime,self.sort_key,date_time_from_ts)
    #                     keep_lenstatus = arr_list_sum
    #                     sum_row_tooffset = self.offset + sum_row_tooffset
    #                     if len(keep_lenstatus) == len(arr_list_sum):
    #                         a = a + 1
    #                         if a == 5:
    #                             list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
    #                             json_Data['document'] = list_arr
    #                             json_Data['offset'] = sum_row_tooffset
    #                             print ('json_Data:',json_Data)
    #                             return {'result':'OK','messageText':json_Data}                    
    #                 else:
    #                     list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
    #                     json_Data['document'] = list_arr
    #                     json_Data['offset'] = sum_row_tooffset
    #                     return {'result':'OK','messageText':json_Data} 
    #             list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
    #             json_Data['document'] = list_arr
    #             json_Data['offset'] = sum_row_tooffset
    #             print(len(list_arr))
    #             return {'result':'OK','messageText':json_Data}
    #         if self.status != '':
    #             where_sql += ' AND "tb_send_detail"."document_status" = :document_status '
    #         if self.document_type != '':
    #             where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
    #         if self.group_status == "true":
    #             where_sql += ' AND ("tb_send_detail"."group_id"=:group_idtmp OR "tb_send_detail"."group_id" IS NULL) '
    #         if self.pick_datetime != None:
    #             where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
    #         if self.timestamp != None:
    #             where_sql += ' AND ("tb_step_data"."update_time" >= :date_time_from_ts) '
    #         where_sql += ORDER_sql
    #         # text_sql = text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
    #         #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #         #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #         text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                     "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                     "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                     "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                     "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                     "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                     "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
    #                     "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
    #                     "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
    #                     "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
    #                     "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
    #                     "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
    #                 FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #         # print(text_sql , self.status)
    #         with slave.connect() as connection:
    #             result = connection.execute(text_sql\
    #                 ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,documentType=self.document_type,document_status=self.status,biz_info='',biz_info_none='None',group_idtmp='[]',group_idNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime,date_time_from_ts=date_time_from_ts)
    #             connection.close()
    #         query = [dict(row) for row in result]
    #     elif typequery == 'recipient_external':
    #         if self.pick_datetime != None:
    #             where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) ' 
    #         with slave.connect() as connection:
    #             where_sql += ORDER_sql
    #             result = connection.execute(text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                     "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                     "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                     "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                     "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                     "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                     "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
    #                     "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
    #                     "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
    #                     "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
    #                     "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
    #                     "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
    #                 FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid '+ where_sql)\
    #                 ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,biz_info_data=self.tax_id,biz_info='',biz_info_none='None',biz_info_null=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
    #             connection.close()
    #         query = [dict(row) for row in result]
    #         print(self.tax_id)
    #     elif typequery == 'recipient_external_search':
    #         if self.document_type != '':
    #             where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
    #         if self.keyword != '':
    #             where_sql += 'AND ("tb_send_detail"."sender_name" LIKE :keyword OR "tb_send_detail"."doc_id" LIKE :keyword OR "tb_doc_detail"."options_page" LIKE :keyword) '
    #         if self.pick_datetime != None:
    #             where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
    #         where_sql += ORDER_sql
    #         text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                     "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                     "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                     "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                     "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                     "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                     "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
    #                     "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
    #                     "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
    #                     "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
    #                     "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
    #                     "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
    #                     FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #         with slave.connect() as connection:
    #             result = connection.execute(text_sql\
    #                 ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,documentType=self.document_type,keyword=search_keyword,biz_info='',biz_info_none='None',biz_info_null=None,group_idtmp='[]',group_idNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
    #             connection.close()
    #         query = [dict(row) for row in result]
    #     elif typequery == 'filter_recipient_external':
    #         if self.status in self.all_status:
    #             for i in range(self.limit):
    #                 if i > 0:
    #                     self.offset = self.offset + self.limit
    #                     print(self.offset)
    #                 print(len(arr_list_sum),self.limit)
    #                 if len(arr_list_sum) < self.limit:
    #                     arr_list_sum,sum_row_tooffset = recursive_select_recp_new_v2(self.email_one,self.limit,self.offset,self.status,arr_list_sum,sum_row_tooffset,self.document_type,self.tax_id,self.sort_key,self.pick_datetime)
    #                     keep_lenstatus = arr_list_sum
    #                     sum_row_tooffset = self.offset + sum_row_tooffset
    #                     if len(keep_lenstatus) == len(arr_list_sum):
    #                         a = a + 1
    #                         if a == 5:
    #                             list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
    #                             json_Data['document'] = list_arr
    #                             json_Data['offset'] = sum_row_tooffset
    #                             return {'result':'OK','messageText':json_Data}                    
    #                 else:
    #                     list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
    #                     json_Data['document'] = list_arr
    #                     json_Data['offset'] = sum_row_tooffset
    #                     return {'result':'OK','messageText':json_Data} 
    #             list_arr = sorted(arr_list_sum, key=lambda k: k['dateTime'], reverse=True)
    #             json_Data['document'] = list_arr
    #             json_Data['offset'] = sum_row_tooffset
    #             print(len(list_arr))
    #             return {'result':'OK','messageText':json_Data}
    #         if self.status != '':
    #             where_sql += ' AND "tb_send_detail"."document_status" = :document_status '
    #         if self.document_type != '':
    #             where_sql += ' AND "tb_doc_detail"."documentType" = :documentType '
    #         if self.group_status == "true":
    #             where_sql += ' AND ("tb_send_detail"."group_id"=:group_idtmp OR "tb_send_detail"."group_id" IS NULL) '
    #         if self.pick_datetime != None:
    #             where_sql += ' AND ("tb_send_detail"."send_time" BETWEEN (:before_datetime) AND (:after_datetime)) '
    #         where_sql += ORDER_sql
    #         # text_sql = text('SELECT "tb_send_detail".*,"tb_doc_detail".*,"tb_step_data".* FROM "tb_send_detail" \
    #         #     INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #         #     INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #         text_sql = text('SELECT "tb_send_detail"."id","tb_send_detail"."send_user","tb_send_detail"."send_time",\
    #                     "tb_send_detail"."send_time","tb_send_detail"."status","tb_send_detail"."sender_name","tb_send_detail"."sender_email",\
    #                     "tb_send_detail"."sender_position","tb_send_detail"."file_id","tb_send_detail"."file_name","tb_send_detail"."tracking_id",\
    #                     "tb_send_detail"."step_code","tb_send_detail"."step_data_sid","tb_send_detail"."doc_id","tb_send_detail"."sender_biz_info",\
    #                     "tb_send_detail"."template_webhook","tb_send_detail"."email_center","tb_send_detail"."recipient_email",\
    #                     "tb_send_detail"."status_details","tb_send_detail"."document_status","tb_send_detail"."group_id","tb_send_detail"."stepnow",\
    #                     "tb_send_detail"."stepmax","tb_send_detail"."time_expire","tb_send_detail"."importance","tb_send_detail"."eform_id","tb_send_detail"."last_digitsign",\
    #                     "tb_doc_detail"."timest","tb_doc_detail"."step_id","tb_doc_detail"."typefile","tb_doc_detail"."fileid","tb_doc_detail"."document_id","tb_doc_detail"."id",\
    #                     "tb_doc_detail"."documentJson","tb_doc_detail"."documentType","tb_doc_detail"."urgent_type","tb_doc_detail"."digit_sign","tb_doc_detail"."attempted_folder","tb_doc_detail"."sign_page_options",\
    #                     "tb_doc_detail"."options_page","tb_doc_detail"."data_document",\
    #                     "tb_step_data"."id","tb_step_data"."sid","tb_step_data"."data_json","tb_step_data"."update_time","tb_step_data"."data_json_Upload","tb_step_data"."upload_time","tb_step_data"."biz_info",\
    #                     "tb_step_data"."view_details","tb_step_data"."qrCode_position" \
    #                 FROM "tb_send_detail" \
    #                 INNER JOIN "tb_doc_detail" ON "tb_doc_detail".step_id = "tb_send_detail".step_data_sid \
    #                 INNER JOIN "tb_step_data" ON "tb_step_data".sid = "tb_send_detail".step_data_sid ' + where_sql)
    #         # print(text_sql , self.status)
    #         with slave.connect() as connection:
    #             result = connection.execute(text_sql\
    #                 ,status=status_ACTIVE,recipient_email=search,limit=self.limit,offset=self.offset,documentType=self.document_type,document_status=self.status,biz_info='',biz_info_none='None',biz_info_null=None,group_idtmp='[]',group_idNone=None,before_datetime=self.before_datetime,after_datetime=self.after_datetime)
    #             connection.close()
    #         query = [dict(row) for row in result]
        
    #     try:
    #         # max_ts = max(query,key=lambda item:item['update_time'])['update_time']
    #         # print ('max_ts:',max_ts)
    #         for x in range(len(query)):
    #             arr_email_document = []
    #             tmp_req_email = []
    #             email_step_sum_w = []
    #             tmpdata = query[x]
    #             tmp_sicode = tmpdata['step_data_sid']
    #             tmp_sid_code_list.append(tmp_sicode)
    #             tmp_send_time = tmpdata['send_time']
    #             tmp_document_id = tmpdata['doc_id']
    #             tmp_tracking_id = tmpdata['tracking_id']
    #             tmp_sender_name = tmpdata['sender_name']
    #             tmp_sender_email = tmpdata['sender_email']
    #             tmp_file_name = tmpdata['file_name']
    #             tmp_groupid = tmpdata['group_id']
    #             email_step_sum = tmpdata['recipient_email']
    #             update_time = tmpdata['update_time']                
    #             if email_step_sum != None:
    #                 email_step_sum = eval(email_step_sum)
    #             tmpstatus_detail = tmpdata['status_details']
    #             tmpdocument_status = tmpdata['document_status']
    #             tmpstepnow = tmpdata['stepnow']
    #             tmp_data_document = tmpdata['data_document']
    #             tmpdatadocument = None
    #             status_groupid = False
    #             if tmp_groupid != None:
    #                 if tmp_groupid != '':
    #                     tmp_groupid = eval(tmp_groupid)
    #                     if len(tmp_groupid) != 0:
    #                         status_groupid = True
    #             if tmpstepnow != None:
    #                 tmpstepnow = int(tmpstepnow)
    #             tmpstepmax = tmpdata['stepmax']
    #             if tmpstepmax != None:
    #                 tmpstepmax = int(tmpstepmax)
    #             if tmpstatus_detail != None:
    #                 tmpstatus_detail = eval(tmpstatus_detail)                            
    #                 for z in range(len(tmpstatus_detail)):
    #                     email_step_sum_w.append(tmpstatus_detail[z]['email'])

    #                 if tmpdocument_status == 'N':
    #                     for x in range(len(tmpstatus_detail)):
    #                         # print(tmp_sicode)
    #                         # print(tmpstatus_detail[x])
    #                         # email_step_sum_w.append(tmpstatus_detail[x]['email'])
    #                         if self.email_one not in arr_email_document:
    #                             if self.email_one in tmpstatus_detail[x]['email']:
    #                                 if tmpstatus_detail[x]['step_status_code'] == 'W':
    #                                     arr_email_document.append(self.email_one)
    #                                     tmpdocument_status = tmpstatus_detail[x]['step_status_code']
    #                                     break
    #                                 else:
    #                                     tmpdocument_status = tmpstatus_detail[x]['step_status_code']
    #             if tmpdocument_status == 'Z':
    #                 res_status_file_string = 'อยู่ในช่วงดำเนินการ'
    #             elif tmpdocument_status == 'W':
    #                 res_status_file_string = 'รอคุณอนุมัติ'
    #             elif tmpdocument_status == 'N':
    #                 res_status_file_string = 'กำลังดำเนินการ'
    #             elif tmpdocument_status == 'R':
    #                 res_status_file_string = 'เอกสารที่ส่งคืนแก้ไข'
    #             else:
    #                 res_status_file_string = 'เอกสารสมบูรณ์'
    #             tmp_sign_page_options = tmpdata['sign_page_options']
    #             tmp_document_type = tmpdata['documentType']
    #             tmp_options_page = []
    #             if tmpdata['options_page'] != None:
    #                 if tmpdata['options_page'] != '':
    #                 # print(tmp_dict_json['options_page'],tmp_document_id)
    #                     tmp_options_page = [eval(tmpdata['options_page'])]
    #             else:
    #                 tmp_options_page = []
    #             if len(tmp_options_page) != 0:
    #                 # print(tmp_options_page[0]['group_detail'])
    #                 tmp_status_group = False
    #                 if status_groupid == True:
    #                     if len(tmp_options_page) != 0:
    #                         if 'group_detail' in tmp_options_page[0]:
    #                             tmp_group_detail = tmp_options_page[0]['group_detail']
    #                             if 'group_status' in tmp_group_detail:
    #                                 if tmp_group_detail['group_status'] == True:
    #                                     tmp_status_group = True
    #                                     tmpstepnum = tmp_group_detail['step_num']
    #             if tmpdata['documentJson'] != None:
    #                 documentJson_result = eval(tmpdata['documentJson'])
    #                 documentName = documentJson_result['document_name']
    #                 documentType = documentJson_result['document_type']
    #             else:
    #                 documentName = None
    #                 documentType = None
    #             if tmpdata['urgent_type'] != None:
    #                 documentUrgentType = tmpdata['urgent_type']
    #                 if documentUrgentType == 'I':
    #                     documentUrgentString = 'ด่วนมาก'
    #                 elif documentUrgentType == 'U':
    #                     documentUrgentString = 'ด่วน'
    #                 elif documentUrgentType == 'M':
    #                     documentUrgentString = 'ปกติ'
    #             tmp_biz_info = None
    #             tmpdept_name = None
    #             tmprolename = None
    #             tmprole_level = None
    #             if tmpdata['biz_info'] != None:
    #                 if tmpdata['biz_info'] != 'None':
    #                     if tmpdata['biz_info'] != '':
    #                         eval_biz_info = json.dumps(tmpdata['biz_info'])
    #                         eval_biz_info = json.loads(eval_biz_info)
    #                         # print(eval_biz_info)
    #                         eval_biz_info = eval(eval_biz_info)
    #                         # eval_biz_info
    #                         # print(eval_biz_info)
    #                         if 'role_name' in eval_biz_info:
    #                             tmprolename =  eval_biz_info['role_name']                                
    #                         if 'dept_name' in eval_biz_info:
    #                             tmpdept_name =  eval_biz_info['dept_name']                               
    #                         if 'role_level' in eval_biz_info:
    #                             tmprole_level =  eval_biz_info['role_level']
    #                         if 'dept_name' in eval_biz_info:  
    #                             tmp_biz_info = {
    #                                 'tax_id':eval_biz_info['id_card_num'],
    #                                 'role_name' : tmprolename,
    #                                 'dept_name' : tmpdept_name,
    #                                 'role_level' : tmprole_level            
    #                             }                                
    #                         elif 'dept_name' not in eval_biz_info:
    #                             tmp_biz_info = {
    #                                 'tax_id':eval_biz_info['id_card_num'],
    #                                 'role_name' : eval_biz_info['role_name'],
    #                                 'dept_name' : [],
    #                                 'role_level' : eval_biz_info['role_level']               
    #                             }
    #             dateTime_String = tmp_send_time
    #             th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
    #             ts = int(time.time())
    #             date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    #             year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
    #             datetime_display = int(dateTime_String.timestamp())
    #             date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
    #             yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
    #             time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
    #             old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
    #             if date_time_today == date_time_db:
    #                 date_display_show = time_show_db
    #             else:
    #                 if year_today == yar_db:
    #                     date_display_show = convert_datetime_TH_2_display(datetime_display)
    #                 else:
    #                     date_display_show = old_year
    #         # print(email_step_sum_w)
    #             if tmp_status_group == True:
    #                 for ui in range(len(tmpstepnum)):
    #                     intstepnum = tmpstepnum[ui] - 1
    #                     try:
    #                         for w in range(len(email_step_sum_w[intstepnum])):
    #                             tmp_req_email.append(email_step_sum_w[intstepnum][w])
    #                     except Exception as e:
    #                         tmp_req_email = []
    #             list_arr.append({
    #                 'group_email':tmp_req_email,
    #                 'group_id':None,
    #                 'group_status':tmp_status_group,
    #                 'sidCode':tmp_sicode,
    #                 'document_name':documentName,
    #                 'document_type':tmp_document_type,
    #                 'document_urgent':documentUrgentType,
    #                 'document_urgent_string':documentUrgentString,
    #                 'dateTime_String':str(dateTime_String).split('+')[0],
    #                 'dateTime_String_TH_1':th_dateTime_2,
    #                 'dateTime_display':date_display_show,
    #                 'document_id':tmp_document_id,
    #                 'stamp_all':tmp_sign_page_options,
    #                 'options_page_document':tmp_options_page,
    #                 'max_step':tmpstepmax,
    #                 'step_now':tmpstepnow,
    #                 # 'dateTime_String_TH_2':th_dateTime_2,
    #                 'date_String':str(dateTime_String).split(' ')[0],
    #                 'time_String':str(dateTime_String).split(' ')[1].split('+')[0],
    #                 'status_file_code':tmpdocument_status,
    #                 'status_file_string':res_status_file_string,
    #                 'dateTime':int(dateTime_String.timestamp()),
    #                 'tracking_id':tmp_tracking_id,
    #                 'sender_name':tmp_sender_name,
    #                 'sender_email':tmp_sender_email,
    #                 'file_name':tmp_file_name,
    #                 'document_business':tmp_biz_info,
    #                 'group':status_groupid,
    #                 'data_document':tmpdatadocument,
    #                 'update_time' : update_time,
    #                 'update_time_str' : str(update_time)
    #                 # 'importance':importance,
    #                 # 'importance_string':importance_string,
    #                 # 'last_digitsign':last_digitsign,
    #                 # 'time_expire':expiry_date
    #             })
    #         list_arr = sorted(list_arr, key=lambda k: k['dateTime'], reverse=True)
    #         json_Data['document'] = list_arr
    #         json_Data['offset'] = self.offset + self.limit
    #         return {'result':'OK','messageText':json_Data}
    #     except Exception as e:
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         print(exc_type, fname, exc_tb.tb_lineno)
    #         return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(e)}

    def select_doc_id_onebox_v2(self,sidcode):
        self.sidcode = sidcode
        tmp_json = {}
        try:
            query_tmp = paper_lessdocument.query.with_entities(paper_lessdocument.document_id,paper_lessdocument.documentJson).filter(paper_lessdocument.step_id == self.sidcode).first()  
            if query_tmp != None and query_tmp != [] and query_tmp != '':
                doc_id = str(query_tmp[0])
                doc_type_name = eval(str(query_tmp[1]))
                doc_type_name = doc_type_name['document_type'] + '/' + doc_type_name['document_name']
                print (doc_id)
                print (doc_type_name)
                # return (query_tmp)
                return {'result':'OK','messageText':str(doc_id),'messageText2':str(doc_type_name)}
            else:
                return {'result':'ER','messageText':None}
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            db.session.rollback()
            raise
            return {'result':'ER','messageText':str(ex)} 

    def select_doc_id_onebox(self,sidcode):
        self.sidcode = sidcode
        tmp_json = {}
        try:
            query_tmp = paper_lessdocument.query.with_entities(paper_lessdocument.document_id,paper_lessdocument.documentJson).filter(paper_lessdocument.step_id == self.sidcode).first()  
            if query_tmp != None and query_tmp != [] and query_tmp != '':
                doc_id = str(query_tmp[0])
                doc_type_name = eval(str(query_tmp[1]))
                doc_type_name = doc_type_name['document_type'] + '/' + doc_type_name['document_name']
                print (doc_id)
                print (doc_type_name)
                # return (query_tmp)
                return {'result':'OK','messageText':str(doc_id),'messageText2':str(doc_type_name)}
            else:
                return {'result':'ER','messageText':None}

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            db.session.rollback()
            raise
            return {'result':'ER','messageText':str(ex)}

    def select_deptname_onebox(self,sid_code):
        try:
            self.sid_code = sid_code
            query_select_dept = paper_lessdatastep.query.with_entities(paper_lessdatastep.biz_info).filter(paper_lessdatastep.sid == self.sid_code).first()
            if query_select_dept != None and query_select_dept != '':
                query_select_dept = eval(str(query_select_dept[0]))
                if 'dept_name' in query_select_dept:
                    # dept_name = query_select_dept['dept_name'][0]
                    if query_select_dept['dept_name'] != []:
                        dept_name = query_select_dept['dept_name'][0]
                    elif query_select_dept['dept_name'] == []:
                        dept_name = 'อื่นๆ'
                    # if dept_name == []
                else :
                    dept_name = 'อื่นๆ'
                print ('dept_name: ',dept_name)
                return {'result':'OK','messageText':dept_name,'status_Code':200,'messageER':None}
            else:
                dept_name = 'อื่นๆ'
                return {'result':'OK','messageText':dept_name,'status_Code':200,'messageER':None}
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(ex)}

    def select_tax_id_to_onebox_v2(self,sidcode,tax_id):
        self.sidcode = sidcode
        self.tax_id = tax_id
        try:
            tq = db.session.query(\
                paper_lessdocument,
                paper_lessdatastep,
                paper_lesssender
            )\
            .join(paper_lesssender,paper_lesssender.step_data_sid==paper_lessdocument.step_id)\
            .join(paper_lessdatastep,paper_lessdatastep.sid==paper_lessdocument.step_id)\
            .filter(paper_lessdocument.step_id==self.sidcode)\
            .first()
            tmp_biz_info = None
            tmp_usersender = None
            # print(tq[1])
            for u in range(len(tq)):
                # print(u)
                tmpjson = tq[u].__dict__
                if '_sa_instance_state' in tmpjson:
                    del tmpjson['_sa_instance_state']
                if u == 0:
                    # print(tmpjson)
                    tmp_document_type = tmpjson['documentType']
                    documentJson = eval(str(tmpjson['documentJson']))
                    doc_name_type = str(documentJson['document_type']+'/'+documentJson['document_name'])
                if u == 1:
                    tmp_biz_info = tmpjson['biz_info']
                if u == 2:
                    tmp_usersender = tmpjson['send_user']
                if tmp_biz_info == 'None':
                    tmp_biz_info = None
            if tmp_biz_info != None:
                try:
                    tmp_biz_info = eval(tmp_biz_info)
                    tmp_id_card_num = tmp_biz_info['id_card_num']
                    print('id_card_num: ',tmp_id_card_num)
                    return {'result':'OK','messageText':str(tmp_id_card_num),'messageText2':doc_name_type}
                except Exception as e:
                    tax_id = None
                    tmp_id_card_num =None
            else:
                return {'result':'ER'}            
        except Exception as e:
            print(str(e))
            return {'result':'ER','messageText':str(e)}

    def select_auto_grouptemplate_v1(self,daygroup_auto,timegroup_auto):
        self.daygroup_auto = daygroup_auto
        self.timegroup_auto = timegroup_auto
        arrtemp_template = []
        self.daygroup_auto = "%'{}'%".format(self.daygroup_auto)
        self.timegroup_auto = "%'{}'%".format(self.timegroup_auto)
        try:
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "id","group_name","group_code","template","document_type","group_title","step_group","status","create_date","update_date","group_data","biz_info","create_by","update_by",\
                "use_status","cover_page","tid","group_color","email_middle","timegroup_auto","daygroup_auto"\
                FROM "tb_group_template" WHERE status=:status AND daygroup_auto LIKE :daygroup_auto AND timegroup_auto LIKE :timegroup_auto '),status='ACTIVE',daygroup_auto= self.daygroup_auto,timegroup_auto=self.timegroup_auto)
                connection.close()
            tmp_query = [dict(row) for row in result]
            if len(tmp_query) != 0 :
                for j in range(len(tmp_query)):
                    if 'tid' in tmp_query[j]:
                        tmp_tid = tmp_query[j]['tid']
                        arrtemp_template.append(tmp_tid)
                        # print(tmp_query[j])
                return {'result':'OK','messageText':arrtemp_template}
            else:
                return {'result':'ER','messageText':None}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}
        
    def select_auto_groupv2template_v1(self,daygroup_auto,timegroup_auto):
        self.daygroup_auto = daygroup_auto
        self.timegroup_auto = timegroup_auto
        arrtemp_template = []
        self.daygroup_auto = "%'{}'%".format(self.daygroup_auto)
        self.timegroup_auto = "%'{}'%".format(self.timegroup_auto)
        try:
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "id","group_name","group_code","template","document_type","group_title","step_group","status","create_date","update_date","group_data","biz_info","create_by","update_by",\
                "use_status","cover_page","tid","group_color","email_middle","timegroup_auto","daygroup_auto"\
                FROM "tb_group_template_2" WHERE status=:status AND daygroup_auto LIKE :daygroup_auto AND timegroup_auto LIKE :timegroup_auto '),status='ACTIVE',daygroup_auto= self.daygroup_auto,timegroup_auto=self.timegroup_auto)
                connection.close()
            tmp_query = [dict(row) for row in result]
            if len(tmp_query) != 0 :
                for j in range(len(tmp_query)):
                    if 'tid' in tmp_query[j]:
                        tmp_tid = tmp_query[j]['tid']
                        arrtemp_template.append(tmp_tid)
                        # print(tmp_query[j])
                return {'result':'OK','messageText':arrtemp_template}
            else:
                return {'result':'ER','messageText':None}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def select_querystatus_group_v1(self,group_id):
        self.group_id = group_id
        arr_tmpstatus = []
        tmpstatusresult = 'N'
        try:
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "tb_group_document"."document_type","tb_group_document"."status_group","tb_group_document"."email_middle" FROM "tb_group_document" WHERE "id"=:group_id'),group_id=self.group_id)
                connection.close()
            tmp_query = [dict(row) for row in result]
            # print(tmp_query)
            if len(tmp_query) != 0:
                for n in range(len(tmp_query)):
                    if 'status_group' in tmp_query[n]:
                        tmp_document_type = tmp_query[n]['document_type']
                        tmp_status_group = eval(tmp_query[n]['status_group'])
                        for z in range(len(tmp_status_group)):
                            tmpstatus = tmp_status_group[z]['status']
                            arr_tmpstatus.append(tmpstatus)
                    if 'email_middle' in tmp_query[n]:
                        tmpemail_middle = tmp_query[n]['email_middle']
                        if tmpemail_middle != None:
                            tmpemail_middle = eval(tmpemail_middle)
                        else:
                            tmpemail_middle = None
                if 'Incomplete' in arr_tmpstatus:
                    tmpstatusresult = 'N'
                else:
                    tmpstatusresult = 'Y'
                return {'result':'OK','messageText':tmpstatusresult,'email_middle':tmpemail_middle,'document_type':tmp_document_type}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def select_querystatus_group_version2(self,group_id):
        self.group_id = group_id
        arr_tmpstatus = []
        tmpstatusresult = 'N'
        try:
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "tb_group_document_2"."status_group","tb_group_document_2"."email_middle" FROM "tb_group_document_2" WHERE "id"=:group_id'),group_id=self.group_id)
            connection.close()
            tmp_query = [dict(row) for row in result]
            if len(tmp_query) != 0:
                for n in range(len(tmp_query)):
                    if 'status_group' in tmp_query[n]:
                        # tmp_document_type = tmp_query[n]['document_type']
                        tmp_status_group = eval(tmp_query[n]['status_group'])
                        for z in range(len(tmp_status_group)):
                            tmpstatus = tmp_status_group[z]['status']
                            arr_tmpstatus.append(tmpstatus)
                    if 'email_middle' in tmp_query[n]:
                        tmpemail_middle = tmp_query[n]['email_middle']
                        if tmpemail_middle != None:
                            tmpemail_middle = eval(tmpemail_middle)
                        else:
                            tmpemail_middle = None
                if 'Incomplete' in arr_tmpstatus:
                    tmpstatusresult = 'N'
                else:
                    tmpstatusresult = 'Y'
                return {'result':'OK','messageText':tmpstatusresult,'email_middle':tmpemail_middle}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}


    # def select_BizProfile_for_onebox(self,bizTax):
    #     self.bizTax = bizTax
    #     result_Tax = paper_lessbizProfile.query.with_entities(paper_lessbizProfile.bizInfoJson).filter(paper_lessbizProfile.bizInfoJson.contains(self.bizTax)).first()
    #     if result_Tax != None:
    #         return {'result':'OK','messageText':result_Tax}
    #     else:
    #         return {'result':'ER','messageER':'not found BizProfile'}
    
    def select_BizProfile_for_onebox(self,bizTax):
        self.bizTax = bizTax
        with slave.connect() as connection:
            result = connection.execute(text('SELECT "bizInfoJson" FROM "tb_bizProfile" WHERE "bizTax"=:bizTaxID '),bizTaxID=self.bizTax)
            result_Tax = [dict(row) for row in result]
            connection.close()
        result_Tax = result_Tax[0]['bizInfoJson']
        arr = [result_Tax]
        result_Tax = tuple(arr)
        if len(result_Tax) != 0:
            return {'result':'OK','messageText': (result_Tax)}
        else:
            return {'result':'ER','messageER':'not found BizProfile'}

    def select_citizen_login_v1(self,username):
        self.username = username
        try:
            with slave.connect() as connection:
                result = connection.execute(text('SELECT * FROM "tb_citizen_Login" WHERE "username"=:username'),username=self.username)                
                tmp_query = [dict(row) for row in result]
            connection.close()
            if len(tmp_query) != 0:
                return {'result':'OK','messageText':tmp_query}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}
        finally:
            connection.close()

    def select_citizenlogin_bizpaperless(self,username,tax_id):
        self.username = username
        self.tax_id = tax_id
        try:
            with engine.connect() as connection:
                result = connection.execute(text('SELECT username,citizen_data FROM "tb_citizen_Login" WHERE "username"=:username'),username=self.username)                
                tmp_query = [dict(row) for row in result]

                result = connection.execute(text('SELECT "tax_id","theme_color",path_logo,"status","transactionMax","storageMax","transactionNow","storageNow","eform_status" FROM "tb_bizPaperless" WHERE "tax_id"=:val'),val=self.tax_id)
                tmp_query2 = [dict(row) for row in result]
            connection.close()
            if len(tmp_query) != 0 and len(tmp_query2) != 0:
                return {'result':'OK','messageText':tmp_query,'messageText2':tmp_query2[0]}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}
        finally:
            connection.close()
     
    def select_data_processlog_v1(self,processId):
        self.processId = processId
        with slave.connect() as connection:
            result = connection.execute(text('SELECT "id","name_process","status","datetime","document","urlapi","datetime_update","group_id","email" \
            FROM "tb_process_request" WHERE "id"=:id'),id=self.processId)
            connection.close()
            # result = connection.execute(text('SELECT * FROM "tb_process_request" WHERE "id"=:id'),id=self.processId)
            # connection.close()
        try:
            tmp_query = [dict(row) for row in result]
            if len(tmp_query) != 0:
                return {'result':'OK','messageText':tmp_query}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def select_data_alert_v1(self,time_alert_again):
        self.time_alert_again = time_alert_again
        with slave.connect() as connection:
            # result = connection.execute(text('SELECT * FROM "tb_schedule_alert_document" WHERE "time_alert_again"<=:time_alert_again AND "status"=:status'),time_alert_again=self.time_alert_again,status='ACTIVE')
            # connection.close()
            result = connection.execute(text('SELECT "id","email","time_alert_last","sid","status","update_last","time_alert_again" \
            FROM "tb_schedule_alert_document" WHERE "time_alert_again"<=:time_alert_again AND "status"=:status'),time_alert_again=self.time_alert_again,status='ACTIVE')
            connection.close()
        try:
            tmp_query = [dict(row) for row in result]
            # print(tmp_query)
            if len(tmp_query) != 0:
                return {'result':'OK','messageText':tmp_query}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def select_data_alert_documentlog_v1(self,email_thai,time_alert_again):
        self.email_thai = email_thai
        self.time_alert_again = time_alert_again
        with slave.connect() as connection:
            result = connection.execute(text('SELECT "id","email","time_alert_last","sid","status","update_last","time_alert_again" FROM "tb_schedule_alert_document" WHERE "email" IN :email'),email=self.email_thai)
            connection.close()
            # result = connection.execute(text('SELECT * FROM "tb_schedule_alert_document" WHERE "email" IN :email'),email=self.email_thai)
            # connection.close()
        try:
            tmp_query = [dict(row) for row in result]
            if len(tmp_query) != 0:
                return {'result':'OK','messageText':tmp_query}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    # def select_status_document_v1(self):
    #     tmp_time_now = int(time.time())
    #     with engine.connect() as connection:
    #         result = connection.execute(text('SELECT "tb_send_detail"."stepnow","tb_doc_detail"."options_page","tb_send_detail"."doc_id","tb_send_detail"."step_data_sid","tb_step_data"."update_time","tb_send_detail"."status_details" FROM "tb_send_detail" INNER JOIN "tb_step_data" ON "step_data_sid" = "sid" INNER JOIN "tb_doc_detail" ON "step_data_sid" = "step_id" WHERE "document_status"=:val AND "status"=:status ORDER BY "send_time" DESC'),val='N',status='ACTIVE')
    #         connection.close()
    #     with engine.connect() as connection:
    #         result_profile = connection.execute(text('SELECT "p_emailthai","p_emailUser","p_options" FROM "tb_userProfile"'))
    #         connection.close()
    #     tmp_query = [dict(row) for row in result]
    #     tmp_query_profile = [dict(row) for row in result_profile]
    #     arr_tmpemail = []
    #     arr_sidcode = []
    #     tmp_result_json = []
    #     for x in range(len(tmp_query)):
    #         tmp_arr_email = []
    #         tmpjsonquery = tmp_query[x]
    #         tmpjsonquery['status_noti'] = False
    #         tmpjsonquery['email_noti'] = None
    #         tmpjsonquery['noti_time'] = None
    #         tmpstep_now = int(tmpjsonquery['stepnow'])
    #         if 'options_page' in tmpjsonquery:
    #             tmpoption_page = tmpjsonquery['options_page']
    #             if tmpoption_page != None:
    #                 tmpoption_page = eval(tmpoption_page)
    #                 if 'group_detail' in tmpoption_page:
    #                     tmpgroup_detail = tmpoption_page['group_detail']
    #                     if 'group_status' in tmpgroup_detail:
    #                         tmp_group_status = tmpgroup_detail['group_status']
    #                         tmp_step_num = tmpgroup_detail['step_num']
    #                         if tmp_group_status == True:
    #                             if tmpstep_now in  tmp_step_num:
    #                                 arr_sidcode.append(tmpjsonquery['step_data_sid'])
    #                                 # print(tmpjsonquery)
    #         if 'update_time' in tmpjsonquery:
    #             tmpjsonquery['update_time'] = timestring_to_timestamp(tmpjsonquery['update_time'])
    #             tmpjsonquery['oneday_plus'] = tmpjsonquery['update_time'] + 86400
    #             tmpjsonquery['oneday_plus_2'] = tmpjsonquery['update_time']
    #         #     if tmp_time_now >= tmpjsonquery['oneday_plus']:
    #         #         tmpjsonquery['status_noti'] = True
    #         if 'status_details' in tmpjsonquery:
    #             if tmpjsonquery['status_details'] != None:
    #                 tmpjsonquery['status_details'] = eval(tmpjsonquery['status_details'])
    #                 tmp_step_detail = tmpjsonquery['status_details']
    #                 for i in range(len(tmp_step_detail)):
    #                     if 'step_status_code' in tmp_step_detail[i]:
    #                         if tmp_step_detail[i]['step_status_code'] == 'W':
    #                             for j in range(len(tmp_step_detail[i]['email'])):
    #                                 tmp_arr_email.append(tmp_step_detail[i]['email'][j])
    #                                 arr_tmpemail.append(tmp_step_detail[i]['email'][j])
    #                             tmpjsonquery['email_noti'] = tmp_arr_email
            
    #         tmpjsonquery['expire_time'] = timestamp_to_strtime(int(tmpjsonquery['oneday_plus_2']))
    #         tmp_query[x]['status_details'] = []
    #     for i in range(len(tmp_query)):
    #         tmp_step_data_sid = tmp_query[i]['step_data_sid']
    #         if tmp_step_data_sid in arr_sidcode:
    #             pass
    #         else:
    #             tmp_result_json.append(tmp_query[i])
    #     return filter_calculate_email_user_v1(tmp_result_json,tmp_query_profile)
    #         # print()

    def select_status_document_v1(self):
        tmp_time_now = int(time.time())
        with slave.connect() as connection:
            result = connection.execute(text('SELECT "tb_send_detail"."stepnow","tb_doc_detail"."options_page","tb_send_detail"."doc_id","tb_send_detail"."step_data_sid","tb_step_data"."update_time","tb_send_detail"."status_details" FROM "tb_send_detail" INNER JOIN "tb_step_data" ON "step_data_sid" = "sid" INNER JOIN "tb_doc_detail" ON "step_data_sid" = "step_id" WHERE "document_status"=:val AND "status"=:status ORDER BY "send_time" DESC'),val='N',status='ACTIVE')
            connection.close()
        with slave.connect() as connection:
            result_profile = connection.execute(text('SELECT "p_emailthai","p_emailUser","p_options" FROM "tb_userProfile"'))
            connection.close()
        tmp_query = [dict(row) for row in result]
        tmp_query_profile = [dict(row) for row in result_profile]
        arr_tmpemail = []
        arr_sidcode = []
        tmp_result_json = []
        for x in range(len(tmp_query)):
            tmp_arr_email = []
            tmpjsonquery = tmp_query[x]
            tmpjsonquery['status_noti'] = False
            tmpjsonquery['email_noti'] = None
            tmpjsonquery['noti_time'] = None
            tmpstep_now = int(tmpjsonquery['stepnow'])
            # if 'options_page' in tmpjsonquery:
            #     tmpoption_page = tmpjsonquery['options_page']
            #     if tmpoption_page != None:
            #         tmpoption_page = eval(tmpoption_page)
            #         if 'group_detail' in tmpoption_page:
            #             tmpgroup_detail = tmpoption_page['group_detail']
            #             if 'group_status' in tmpgroup_detail:
            #                 tmp_group_status = tmpgroup_detail['group_status']
            #                 tmp_step_num = tmpgroup_detail['step_num']
            #                 if tmp_group_status == True:
            #                     if tmpstep_now in  tmp_step_num:
            #                         arr_sidcode.append(tmpjsonquery['step_data_sid'])
            # print(len(arr_sidcode))
            if 'update_time' in tmpjsonquery:
                tmpjsonquery['update_time'] = timestring_to_timestamp(tmpjsonquery['update_time'])
                tmpjsonquery['oneday_plus'] = tmpjsonquery['update_time'] + 86400
                tmpjsonquery['oneday_plus_2'] = tmpjsonquery['update_time']
            #     if tmp_time_now >= tmpjsonquery['oneday_plus']:
            #         tmpjsonquery['status_noti'] = True
            if 'status_details' in tmpjsonquery:
                if tmpjsonquery['status_details'] != None:
                    tmpjsonquery['status_details'] = eval(tmpjsonquery['status_details'])
                    tmp_step_detail = tmpjsonquery['status_details']
                    for i in range(len(tmp_step_detail)):
                        if 'step_status_code' in tmp_step_detail[i]:
                            if tmp_step_detail[i]['step_status_code'] == 'W':
                                for j in range(len(tmp_step_detail[i]['email'])):
                                    tmp_arr_email.append(tmp_step_detail[i]['email'][j])
                                    arr_tmpemail.append(tmp_step_detail[i]['email'][j])
                                tmpjsonquery['email_noti'] = tmp_arr_email
            
            tmpjsonquery['expire_time'] = timestamp_to_strtime(int(tmpjsonquery['oneday_plus_2']))
            tmp_query[x]['status_details'] = []
        for i in range(len(tmp_query)):
            tmp_step_data_sid = tmp_query[i]['step_data_sid']
            if tmp_step_data_sid in arr_sidcode:
                pass
            else:
                tmp_result_json.append(tmp_query[i])
        return filter_calculate_email_user_v1(tmp_result_json,tmp_query_profile)
            # print()

class insert_3:
    def insert_secret_key_forservice(self,tmpserviceName,public,private,code):
        self.tmpserviceName = tmpserviceName
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            with engine.connect() as connection:
                result_insert = connection.execute('INSERT INTO tb_connex ("serviceName", "public", "private", "code", "create_date" ) VALUES (%s,%s,%s,%s,%s) RETURNING "id"',self.tmpserviceName,None,None,self.data,st)
                for row in result_insert:
                    id = dict(row) 
                connection.close()
            if result_insert != None:
                return {'result':'OK','messageText':id}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            print(str(e))

    def insert_status_notification_v2(self,tmp_userid):
        try:
            # query_result = db.session.query(paper_lessuserProfile).all()
            self.userid = tmp_userid
            query_result = paper_lessuserProfile.query.filter(paper_lessuserProfile.p_userid == self.userid).all()
            datajson_update = {'notification_status': {'notificationOneChat': {'status': False, 'config': 1, 'time_rang': {'start_time': '08:00', 'end_time': '20:00'}}, 'notificationEmail': {'status': False}}, 'biz_default': ''}
            for u in range(len(query_result)):
                tmpjson = query_result[u].__dict__
                if tmpjson['p_options'] == None:
                    query_result[u].chat_noti = bool('False')
                    query_result[u].email_noti = bool('False')
                    query_result[u].p_options = str(datajson_update)
                else:
                    p_option = eval(str(tmpjson['p_options']))
                    chat = p_option['notification_status']['notificationOneChat']
                    email = p_option['notification_status']['notificationEmail']
                    chat_status = chat['status']
                    if 'status' in email:
                        email_status = False
                    else:
                        email_status = True
                    query_result[u].chat_noti = bool(chat_status)
                    query_result[u].email_noti = bool(email_status)
            db.session.commit()
            return {'result':'OK','messageText':'insert success'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200
            
    def insert_status_notification(self):
        try:
            # query_result = db.session.query(paper_lessuserProfile).all()
            query_result = paper_lessuserProfile.query.all()
            datajson_update = {'notification_status': {'notificationOneChat': {'status': False, 'config': '1', 'time_rang': {'start_time': '08:00', 'end_time': '20:00'}}, 'notificationEmail': {'status': False}}, 'biz_default': ''}
            for u in range(len(query_result)):
                tmpjson = query_result[u].__dict__
                if tmpjson['p_options'] == None:
                    query_result[u].chat_noti = 'False'
                    query_result[u].email_noti = 'False'
                    query_result[u].p_options = str(datajson_update)
                else:
                    p_option = eval(str(tmpjson['p_options']))
                    chat = p_option['notification_status']['notificationOneChat']
                    email = p_option['notification_status']['notificationEmail']
                    chat_status = chat['status']
                    email_status = email['status']
                    query_result[u].chat_noti = str(chat_status)
                    query_result[u].email_noti = str(email_status)
            db.session.commit()
            return {'result':'OK','messageText':'insert success'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200
            
    def insert_transaction_ocrv1(self,sid,data):
        self.sid = sid
        self.data = data
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            with engine.connect() as connection:
                result_insert = connection.execute('INSERT INTO tb_transaction_ocr ("sid", "data_thai", "data_eng", "data_sum", "datetime" ) VALUES (%s,%s,%s,%s,%s) RETURNING "id"',self.sid,None,None,self.data,st)
                for row in result_insert:
                    id = dict(row) 
                connection.close()
            if result_insert != None:
                return {'result':'OK','messageText':id}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def insert_process_request_v1(self,name_process,document,urlapi,group_id,emailuser):
        self.name_process = name_process
        self.document = document
        self.urlapi = urlapi
        self.group_id = group_id
        self.emailuser = emailuser
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            with engine.connect() as connection:
                result_insert = connection.execute('INSERT INTO tb_process_request ("name_process", "status", "datetime", "document", "urlapi" ,"group_id","email") VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING "id"',self.name_process,'ONPROCESS',str(st),self.document,self.urlapi,self.group_id,self.emailuser)
                # print(result_insert.__dict__)
                for row in result_insert:
                    process_id = dict(row) 
                connection.close()
            if result_insert != None:
                return {'result':'OK','messageText':process_id}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def insert_data_alert_documentlog_v2(self,tuple_data_insert):   
        self.tuple_data_insert = tuple_data_insert
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            with engine.connect() as connection:
                result_insert = connection.execute('INSERT INTO tb_schedule_alert_document ("email", "time_alert_last", "sid", "status", "update_last", "time_alert_again") VALUES (%s,%s,%s,%s,%s,%s)',self.tuple_data_insert)
                connection.close()
            if result_insert != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def insert_data_alert_documentlog_v1(self,email,time_alert_last,sid,time_alert_again):   
        self.email = email
        self.time_alert_last = time_alert_last
        self.sid = sid
        self.time_alert_again = time_alert_again
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            with engine.connect() as connection:
                result_insert = connection.execute(text('INSERT INTO tb_schedule_alert_document ("email", "time_alert_last", "sid", "status", "update_last", "time_alert_again") VALUES (:email,:time_alert_last,:sid,:status,:update_last,:time_alert_again)'),\
                    email=self.email,time_alert_last=self.time_alert_last,sid=self.sid,status='ACTIVE',update_last=st,time_alert_again=self.time_alert_again)
                connection.close()
            if result_insert != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

class update_3:
    def update_picprofile_v1(self,picstring,username):
        self.picstring = picstring
        self.username = username
        with engine.connect() as connection:
            result_update = connection.execute('UPDATE "tb_userProfile" SET "pic_profile"=%s WHERE "p_username"=%s ',(self.picstring),str(self.username))
            connection.close()
        if result_update != None:
            return {'result':'OK','messageText':'success'}
        else:
            return {'result':'ER','messageText':'fail'}

    def update_DataSc_Bi_v1(self,sid_group,jsondata):
        self.sid_group = sid_group
        self.jsondata = jsondata
        tmpliststatus = []
        try:
            for sid in self.sid_group:
                with slave.connect() as connection:
                    result = connection.execute('SELECT "options_page","document_id" FROM "tb_doc_detail" WHERE "step_id"=%s ',sid)
                    connection.close()
                tmp_query = [dict(row) for row in result]
                if 'options_page' in tmp_query[0]:
                    tmpoptionsPage = tmp_query[0]['options_page']
                    tmpoptionsPage = eval(tmpoptionsPage)
                    tmpdocument_id = tmp_query[0]['document_id']
                    if 'service_properties' in tmpoptionsPage:
                        tmpservice_properties = tmpoptionsPage['service_properties']
                        for x in range(len(tmpservice_properties)):
                            tmp_name_service = tmpservice_properties[x]['name_service']
                            tmp_status = tmpservice_properties[x]['status']
                            if tmp_name_service == 'GROUP':
                                if tmp_status == True:
                                    tmp_other = tmpservice_properties[x]['other'][0]
                                    if 'properties' in tmp_other:
                                        tmppropertiesData = tmp_other['properties']
                                        for x in range(len(tmppropertiesData)):
                                            element = tmppropertiesData[x]
                                            tmpname = element['name']
                                            tmpvalue = element['value']
                                            # print(tmpdocument_id)
                                            for y in range(len(self.jsondata)):
                                                tmpjsonDataBi = self.jsondata[y]
                                                if tmpjsonDataBi['Document_ID'] == tmpdocument_id:
                                                    for key in tmpjsonDataBi.keys():
                                                        if key == tmpname:
                                                            element['value'] = tmpjsonDataBi[key]
                with engine.connect() as connection:
                    result_update = connection.execute('UPDATE tb_doc_detail SET "options_page"=%s WHERE "step_id"=%s ',str(tmpoptionsPage),sid)
                    connection.close()
                if result_update != None:
                    tmpliststatus.append('OK') 
                else:
                    tmpliststatus.append('OK')
            if 'ER' in tmpliststatus:
                return {'result':'ER','messageText':'fail'}
            return {'result':'OK','messageText':'success'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_HtmlData_Bi_v1(self,group_id,htmldata,jsondata=None,average=None):
        self.group_id = group_id
        self.htmldata = htmldata
        if jsondata == None:
            self.jsondata = None
        else:
            self.jsondata = jsondata
        if average == None:
            self.average = None
        else:
            self.average = average
        try:
            with engine.connect() as connection:
                # result_update = connection.execute('UPDATE tb_group_document SET "html_data"=%s,"json_data"=%s WHERE "id"=%s ',str(self.htmldata),str(self.jsondata),self.group_id)
                result_update = connection.execute('UPDATE tb_group_document SET "html_data"=%s,"json_data"=%s,"average_data"=%s WHERE "id"=%s ',str(self.htmldata),str(self.jsondata),str(self.average),self.group_id)
                connection.close()
            if result_update != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_pdf_rejectordelete_v1(self,fid,pdfdata):
        self.fid = fid
        self.pdfdata = pdfdata
        try:
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE tb_pdf_storage SET "pdf_rejectorcancle"=%s WHERE "fid"=%s ',self.pdfdata,self.fid)
                connection.close()
            if result_update != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_step_table_template_v10(self,step_code,step_data,step_max,username,email,step_name,step_Description,templateString,qrCode_position,documentDetails,urgent_type,condition_string,webhook=None,email_center=None,template_biz=None,formula_temp=None,digit_sign=None,page_sign_options=None,options_page=None,use_status=None,time_expire=None,importance=None,last_digit_sign=None):
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        self.step_code = step_code
        self.step_data = step_data
        self.step_max = step_max
        self.username = username
        self.email = email
        self.step_name = step_name
        self.step_Description = step_Description
        self.templateString = json.dumps(templateString)
        self.qrCode_position = qrCode_position
        self.documentDetails = documentDetails
        self.urgent_type = urgent_type
        self.condition_string = condition_string
        self.webhook = webhook
        self.email_center = email_center
        self.template_biz = template_biz
        self.formula_temp= str(formula_temp)
        self.digit_sign= digit_sign
        self.page_sign_options = page_sign_options
        self.options_page = str(options_page)
        self.time_expire = time_expire
        self.importance = importance
        self.last_digit_sign = last_digit_sign
        if use_status != None:
            self.use_status = use_status
        else:
            self.use_status = 'ACTIVE'
        total_time = None
        if self.time_expire != None :
            time_ex_eval = eval(self.time_expire)
            status = time_ex_eval['status']
            if status == True:
                data_ex = eval(str(time_ex_eval['data_ex']))
                day = data_ex['day']
                hour = data_ex['hour']
                total_time = (int(day) * 24) + int(hour)
        # mod = total_time % 24
        # hour = int(total_time / 24)
        # print('mod',mod)
        # print('hour',hour)
        try:
            update_steptable = paper_lessstep.query.filter_by(step_Code=str(self.step_code),status='ACTIVE').first()
            if update_steptable != None:
                self.status = 'REJECT'
                self.status_Update = str(st)
                insert_template = paper_lessstep(step_Code=str(update_steptable.step_Code),step_Data=update_steptable.step_Data,step_Max=update_steptable.step_Max,username=self.username,email=self.email,DateTime=update_steptable.DateTime,step_Description=update_steptable.step_Description,step_Name=update_steptable.step_Name,step_Upload=update_steptable.step_Upload,template_images=update_steptable.template_images,template_biz=update_steptable.template_biz,qrCode_position=update_steptable.qrCode_position,status=self.status,status_Update=self.status_Update,documentDetails=update_steptable.documentDetails,urgent_type=update_steptable.urgent_type,condition_temp=update_steptable.condition_temp,webhook=update_steptable.webhook,email_center=update_steptable.email_center,formula_temp=update_steptable.formula_temp,digit_sign=update_steptable.digit_sign,page_sign_options=update_steptable.page_sign_options,options_page=update_steptable.options_page,status_use=update_steptable.status_use,time_expire=update_steptable.time_expire,importance_doc=update_steptable.importance_doc,last_digit_sign=update_steptable.last_digit_sign)
                db.session.add(insert_template)
                db.session.flush()
                db.session.commit()
                update_steptable.condition_temp = self.condition_string
                update_steptable.step_Data = self.step_data
                update_steptable.step_Max = self.step_max
                update_steptable.step_Description = self.step_Description
                update_steptable.DateTime = str(st)
                update_steptable.step_Name = self.step_name
                update_steptable.template_images = self.templateString
                update_steptable.qrCode_position = self.qrCode_position
                update_steptable.documentDetails = self.documentDetails
                update_steptable.urgent_type = self.urgent_type
                update_steptable.webhook = self.webhook
                update_steptable.email_center = self.email_center
                update_steptable.template_biz = self.template_biz
                update_steptable.formula_temp = self.formula_temp
                update_steptable.digit_sign = self.digit_sign
                update_steptable.page_sign_options = self.page_sign_options
                update_steptable.options_page = self.options_page
                update_steptable.status_use = self.use_status
                update_steptable.time_expire = total_time
                update_steptable.importance_doc = self.importance
                update_steptable.last_digit_sign = self.last_digit_sign
                db.session.commit()
                return {'result':'OK','messageText':'update OK!'}
            else:
                return {'result':'ER','messageText':'not found'}
        except Exception as ex:
            return {'result':'ER','messageText':str(ex)}

    def update_process_onprocess_status_v1(self,process_id,email_thai,sid,status,errMesg,errCode):
        self.process_id = process_id
        self.email_thai = email_thai
        self.sid = sid
        self.status = status
        self.errMesg = errMesg
        self.errCode = errCode
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            with slave.connect() as connection:
                # result_select = connection.execute(text('SELECT * FROM "tb_process_request" WHERE "id"=:id'),id=self.process_id)
                # connection.close()
                result_select = connection.execute(text('SELECT "id","name_process","status",\
                "datetime","document","urlapi","datetime_update","group_id","email" FROM "tb_process_request" WHERE "id"=:id'),id=self.process_id)
                connection.close()
            tmp_query = [dict(row) for row in result_select]
            if len(tmp_query) != 0:
                tmp_data= tmp_query[0]
                tmp_document = tmp_data['document']
                if tmp_document != None:
                    tmp_document = eval(tmp_document)
                    for z in range(len(tmp_document)):
                        if 'sid' in tmp_document[z]:
                            tmpemail = tmp_document[z]['email']
                            tmpsidcode = tmp_document[z]['sid']
                            if tmpsidcode == self.sid:
                                if self.status == 'SUCCESS':
                                    tmp_document[z]['status_document'] = 'Complete'
                                else:
                                    tmp_document[z]['status_document'] = 'FAIL'
                                    tmp_document[z]['errorMessage'] = self.errMesg
                                    tmp_document[z]['errorCode'] = self.errCode
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE tb_process_request SET "document"=%s,"datetime_update"=%s WHERE "id"=%s',str(tmp_document),str(st),self.process_id)
                connection.close()
            if result_update != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_process_id_log_status_v2(self,process_id,name_process,status,document_status,group_id,email_thai):   
        self.process_id = process_id
        self.name_process = name_process
        self.status = status
        self.document_status = document_status
        self.group_id = group_id
        self.email_thai = email_thai
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            with slave.connect() as connection:
                result_select = connection.execute(text('SELECT * FROM "tb_group_document_2" WHERE "id"=:id AND "status"=:status'),id=self.group_id,status='ACTIVE')
                connection.close()
            tmp_query = [dict(row) for row in result_select]
            # print(tmp_query)
            if 'status_group' in tmp_query[0]:
                tmpqueryjson = tmp_query[0]
                tmpstatus_group = tmpqueryjson['status_group']
                if tmpstatus_group != None:
                    tmpstatus_group = eval(tmpstatus_group)
                for n in range(len(tmpstatus_group)):
                    tmpemailOne = tmpstatus_group[n]['email_one']
                    if self.email_thai in tmpemailOne:
                        tmpstatus_group[n]['status'] = 'Complete'
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE tb_group_document SET "status_group"=%s WHERE "id"=%s AND "status"=%s',str(tmpstatus_group),self.group_id,'ACTIVE')
                connection.close()
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE tb_process_request SET "name_process"=%s,"status"=%s,"document"=%s,"datetime_update"=%s WHERE "id"=%s',self.name_process,self.status,self.document_status,str(st),self.process_id)
                connection.close()
            if result_update != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}


    def update_process_id_log_status_v1(self,process_id,name_process,status,document_status,group_id,email_thai):   
        self.process_id = process_id
        self.name_process = name_process
        self.status = status
        self.document_status = document_status
        self.group_id = group_id
        self.email_thai = email_thai
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        tmpstatus = 'Incomplete'
        if self.status == 'SUCCESS':
            tmpstatus = 'Complete'
        try:
            connection = engine.connect()
            result_select = connection.execute(text('SELECT * FROM "tb_group_document" WHERE "id"=:id AND "status"=:status'),id=self.group_id,status='ACTIVE')
            tmp_query = [dict(row) for row in result_select]
            if 'status_group' in tmp_query[0]:
                tmpqueryjson = tmp_query[0]
                tmpstatus_group = tmpqueryjson['status_group']
                if tmpstatus_group != None:
                    tmpstatus_group = eval(tmpstatus_group)
                for n in range(len(tmpstatus_group)):
                    tmpemailOne = tmpstatus_group[n]['email_one']
                    if self.email_thai in tmpemailOne:
                        tmpstatus_group[n]['status'] = tmpstatus
            sql = '''
                    UPDATE tb_group_document 
                    SET "status_group" =:tmpstatus_group
                    WHERE
                        "id" =:tmpgroup_id
                        AND "status" =:tmpstatus;
                '''
            sql += '''
                    UPDATE tb_process_request 
                    SET "name_process" =:tmpname_process,
                    "status" =:tmpstatus_process,
                    "document" =:tmpdocument,
                    "datetime_update" =:tmpdatetime_update 
                    WHERE
                        "id" =:tmpprocess_id;
                '''
            result_update = connection.execute(text(sql),tmpstatus_group=str(tmpstatus_group),tmpgroup_id=self.group_id,tmpstatus='ACTIVE',tmpname_process=self.name_process,tmpstatus_process=self.status,tmpdocument=self.document_status,tmpdatetime_update=str(st),tmpprocess_id=self.process_id)
            connection.close()
            if result_update != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}
        finally:
            connection.close()

    def update_data_alert_documentlog_sendchat_v1(self,tuple_data_update):   
        self.tuple_data_update = tuple_data_update
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE tb_schedule_alert_document SET "time_alert_last"=%s,"time_alert_again"=%s,"update_last"=%s WHERE "email"=%s',self.tuple_data_update)
                connection.close()
            if result_update != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_data_alert_documentlog_v2(self,tuple_data_update):   
        self.tuple_data_update = tuple_data_update
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        print(self.tuple_data_update)
        try:
            with engine.connect() as connection:
                result_update = connection.execute('UPDATE tb_schedule_alert_document SET "sid"=%s,"update_last"=%s,"time_alert_again"=%s WHERE "email"=%s',self.tuple_data_update)
                connection.close()
            if result_update != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_data_alert_documentlog_v1(self,email,time_alert_last,sid,time_alert_again):
        self.email = email
        self.time_alert_last = time_alert_last
        self.sid = sid
        self.time_alert_again = time_alert_again
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            with engine.connect() as connection:
                result_update = connection.execute(text('UPDATE "tb_schedule_alert_document" SET "time_alert_last"=:time_alert_last ,"update_last"=:update_last,"time_alert_again"=:time_alert_again,\
                    "sid"=:sid WHERE "tb_schedule_alert_document"."email"=:email'),\
                    email=self.email,time_alert_last=self.time_alert_last,sid=self.sid,status='ACTIVE',update_last=st,time_alert_again=self.time_alert_again)
                connection.close()
            if result_update != None:
                return {'result':'OK','messageText':'success'}
            else:
                return {'result':'ER','messageText':'fail'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            return {'result':'ER','messageText':str(e)}


            