#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config.db_config import *

db = db_init

if type_product =='uat':
    status_db_r = "paper_less_uat"
    # status_db_r = "paper_less_slave"
    status_db_rw = "paper_less_uat"
elif type_product =='prod':
    status_db_rw = "paper_less_master"
    status_db_r = "paper_less_slave"
elif type_product == 'dev':
    status_db_r = "paper_lessdev"
    status_db_rw = "paper_lessdev"
elif type_product =='poc':
    status_db_rw = "paper_less_master"
    status_db_r = "paper_less_slave"


class tb_group_template_2(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_group_template_2"

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String)
    group_code = db.Column(db.String)
    template = db.Column(db.TIMESTAMP(timezone=True))
    group_title = db.Column(db.String)
    step_group = db.Column(db.String)
    status = db.Column(db.String)
    create_date = db.Column(db.String)
    update_date = db.Column(db.String)
    group_data = db.Column(db.String)
    biz_info = db.Column(db.String)
    create_by = db.Column(db.String)
    update_by = db.Column(db.String)
    use_status = db.Column(db.String)
    cover_page = db.Column(db.String)
    tid = db.Column(db.String)
    group_color = db.Column(db.String)
    email_middle = db.Column(db.String)
    timegroup_auto = db.Column(db.String)
    daygroup_auto = db.Column(db.String)
    email_step = db.Column(db.String)
    status_doing_auto = db.Column(db.String)

    def __init__(self,group_name,group_code,template,group_title,step_group,status,create_date,update_date,group_data,biz_info,create_by,update_by,use_status,cover_page,tid,group_color,email_middle,timegroup_auto,daygroup_auto,email_step,status_doing_auto):
        self.group_name = group_name
        self.group_code = group_code
        self.template = template
        self.group_title = group_title
        self.step_group = step_group
        self.status = status
        self.create_date = create_date
        self.update_date = update_date
        self.group_data = group_data
        self.biz_info = biz_info
        self.create_by = create_by
        self.update_by = update_by
        self.use_status = use_status
        self.cover_page = cover_page
        self.tid = tid
        self.group_color = group_color
        self.email_middle = email_middle
        self.timegroup_auto = timegroup_auto
        self.daygroup_auto = daygroup_auto
        self.email_step = email_step
        self.status_doing_auto = status_doing_auto

    def __repr__(self):
        return '<id {},group_name {},group_code {},template {},group_title {},step_group {},status {},create_date {},update_date {},group_data {},biz_info {},create_by {},update_by {},use_status {},cover_page {},tid {},group_color {},email_middle {},timegroup_auto {},daygroup_auto {},email_step {},status_doing_auto {}>'.format(self.id,self.group_name,self.group_code,self.template,self.group_title,self.step_group,self.status,self.create_date,self.update_date,self.group_data,self.biz_info,self.create_by,self.update_by,self.use_status,self.cover_page,self.tid,self.group_color,self.email_middle,self.timegroup_auto,self.daygroup_auto,self.email_step,self.status_doing_auto)

# class tb_group_template_2(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_group_template_2"

#     id = db.Column(db.Integer, primary_key=True)
#     group_name = db.Column(db.String)
#     group_code = db.Column(db.String)
#     template = db.Column(db.TIMESTAMP(timezone=True))
#     group_title = db.Column(db.String)
#     step_group = db.Column(db.String)
#     status = db.Column(db.String)
#     create_date = db.Column(db.String)
#     update_date = db.Column(db.String)
#     group_data = db.Column(db.String)
#     biz_info = db.Column(db.String)
#     create_by = db.Column(db.String)
#     update_by = db.Column(db.String)
#     use_status = db.Column(db.String)
#     cover_page = db.Column(db.String)
#     tid = db.Column(db.String)
#     group_color = db.Column(db.String)
#     email_middle = db.Column(db.String)
#     timegroup_auto = db.Column(db.String)
#     daygroup_auto = db.Column(db.String)
#     email_step = db.Column(db.String)
#     status_doing_auto = db.Column(db.String)

#     def __init__(self,group_name,group_code,template,group_title,step_group,status,create_date,update_date,group_data,biz_info,create_by,update_by,use_status,cover_page,tid,group_color,email_middle,timegroup_auto,daygroup_auto,email_step,status_doing_auto):
#         self.group_name = group_name
#         self.group_code = group_code
#         self.template = template
#         self.group_title = group_title
#         self.step_group = step_group
#         self.status = status
#         self.create_date = create_date
#         self.update_date = update_date
#         self.group_data = group_data
#         self.biz_info = biz_info
#         self.create_by = create_by
#         self.update_by = update_by
#         self.use_status = use_status
#         self.cover_page = cover_page
#         self.tid = tid
#         self.group_color = group_color
#         self.email_middle = email_middle
#         self.timegroup_auto = timegroup_auto
#         self.daygroup_auto = daygroup_auto
#         self.email_step = email_step
#         self.status_doing_auto = status_doing_auto

#     def __repr__(self):
#         return '<id {},group_name {},group_code {},template {},group_title {},step_group {},status {},create_date {},update_date {},group_data {},biz_info {},create_by {},update_by {},use_status {},cover_page {},tid {},group_color {},email_middle {},timegroup_auto {},daygroup_auto {},email_step {},status_doing_auto {}>'.format(self.id,self.group_name,self.group_code,self.template,self.group_title,self.step_group,self.status,self.create_date,self.update_date,self.group_data,self.biz_info,self.create_by,self.update_by,self.use_status,self.cover_page,self.tid,self.group_color,self.email_middle,self.timegroup_auto,self.daygroup_auto,self.email_step,self.status_doing_auto)


class tb_group_document_2(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_group_document_2"

    id = db.Column(db.Integer, primary_key=True)
    sid_group = db.Column(db.String)
    data_group = db.Column(db.String)
    updatetime = db.Column(db.TIMESTAMP(timezone=True))
    email_group = db.Column(db.String)
    status = db.Column(db.String)
    create_by = db.Column(db.String)
    update_by = db.Column(db.String)
    step_group = db.Column(db.String)
    pdf_org = db.Column(db.String)
    pdf_sign = db.Column(db.String)
    step_group_detail = db.Column(db.String)
    group_data_json = db.Column(db.String)
    group_other = db.Column(db.String)
    email_view_group = db.Column(db.String)
    hash_id = db.Column(db.String)
    tracking_group = db.Column(db.String)
    status_group = db.Column(db.String)
    group_title = db.Column(db.String)
    group_name = db.Column(db.String)
    bizinfo = db.Column(db.String)
    group_status = db.Column(db.String)
    cover_page = db.Column(db.String)
    calculate_fieds = db.Column(db.String)
    maxstep  = db.Column(db.String)
    email_middle = db.Column(db.String)
    html_data = db.Column(db.String)
    json_data = db.Column(db.String)
    doctype_group = db.Column(db.String)
    bizinfo_group = db.Column(db.String)

    def __init__(self,sid_group,data_group,updatetime,email_group,status,create_by,update_by,step_group,pdf_org,pdf_sign,step_group_detail,group_data_json,group_other,email_view_group,hash_id,tracking_group,status_group,group_title,group_name,bizinfo,group_status,cover_page,calculate_fieds,maxstep,email_middle,html_data,json_data,doctype_group,bizinfo_group):
        self.sid_group = sid_group
        self.data_group = data_group
        self.updatetime = updatetime
        self.email_group = email_group
        self.status = status
        self.create_by = create_by
        self.update_by = update_by
        self.step_group = step_group
        self.pdf_org = pdf_org
        self.pdf_sign = pdf_sign
        self.step_group_detail = step_group_detail
        self.group_data_json = group_data_json
        self.group_other = group_other
        self.email_view_group = email_view_group
        self.hash_id = hash_id
        self.tracking_group = tracking_group
        self.status_group = status_group
        self.group_title = group_title
        self.group_name = group_name
        self.bizinfo = bizinfo
        self.group_status = group_status
        self.cover_page = cover_page
        self.calculate_fieds = calculate_fieds
        self.maxstep = maxstep
        self.email_middle = email_middle
        self.html_data = html_data
        self.json_data = json_data
        self.doctype_group = doctype_group
        self.bizinfo_group = bizinfo_group

    def __repr__(self):
        return '<id {},sid_group {},data_group {},updatetime {},email_group {},status {},create_by {},update_by {},step_group {},pdf_org {},pdf_sign {},step_group_detail {},group_data_json {},group_other {},email_view_group {},hash_id {},tracking_group {},status_group {},group_title {},group_name {},bizinfo {},group_status {},cover_page {},calculate_fieds {},maxstep {},email_middle {},html_data {},json_data {},doctype_group {},bizinfo_group {}>'.format(self.id,self.sid_group,self.data_group,self.updatetime,self.email_group,self.status,self.create_by,self.update_by,self.step_group,self.pdf_org,self.pdf_sign,self.step_group_detail,self.group_data_json,self.group_other,self.email_view_group,self.hash_id,self.tracking_group,self.status_group,self.group_title,self.group_name,self.bizinfo,self.group_status,self.cover_page,self.calculate_fieds,self.maxstep,self.email_middle,self.html_data,self.json_data,self.doctype_group,self.bizinfo_group)

# class tb_group_document_2(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_group_document_2"

#     id = db.Column(db.Integer, primary_key=True)
#     sid_group = db.Column(db.String)
#     data_group = db.Column(db.String)
#     updatetime = db.Column(db.TIMESTAMP(timezone=True))
#     email_group = db.Column(db.String)
#     status = db.Column(db.String)
#     create_by = db.Column(db.String)
#     update_by = db.Column(db.String)
#     step_group = db.Column(db.String)
#     pdf_org = db.Column(db.String)
#     pdf_sign = db.Column(db.String)
#     step_group_detail = db.Column(db.String)
#     group_data_json = db.Column(db.String)
#     group_other = db.Column(db.String)
#     email_view_group = db.Column(db.String)
#     hash_id = db.Column(db.String)
#     tracking_group = db.Column(db.String)
#     status_group = db.Column(db.String)
#     group_title = db.Column(db.String)
#     group_name = db.Column(db.String)
#     bizinfo = db.Column(db.String)
#     group_status = db.Column(db.String)
#     cover_page = db.Column(db.String)
#     calculate_fieds = db.Column(db.String)
#     maxstep  = db.Column(db.String)
#     email_middle = db.Column(db.String)
#     html_data = db.Column(db.String)
#     json_data = db.Column(db.String)
#     doctype_group = db.Column(db.String)
#     bizinfo_group = db.Column(db.String)

#     def __init__(self,sid_group,data_group,updatetime,email_group,status,create_by,update_by,step_group,pdf_org,pdf_sign,step_group_detail,group_data_json,group_other,email_view_group,hash_id,tracking_group,status_group,group_title,group_name,bizinfo,group_status,cover_page,calculate_fieds,maxstep,email_middle,html_data,json_data,doctype_group,bizinfo_group):
#         self.sid_group = sid_group
#         self.data_group = data_group
#         self.updatetime = updatetime
#         self.email_group = email_group
#         self.status = status
#         self.create_by = create_by
#         self.update_by = update_by
#         self.step_group = step_group
#         self.pdf_org = pdf_org
#         self.pdf_sign = pdf_sign
#         self.step_group_detail = step_group_detail
#         self.group_data_json = group_data_json
#         self.group_other = group_other
#         self.email_view_group = email_view_group
#         self.hash_id = hash_id
#         self.tracking_group = tracking_group
#         self.status_group = status_group
#         self.group_title = group_title
#         self.group_name = group_name
#         self.bizinfo = bizinfo
#         self.group_status = group_status
#         self.cover_page = cover_page
#         self.calculate_fieds = calculate_fieds
#         self.maxstep = maxstep
#         self.email_middle = email_middle
#         self.html_data = html_data
#         self.json_data = json_data
#         self.doctype_group = doctype_group
#         self.bizinfo_group = bizinfo_group

#     def __repr__(self):
#         return '<id {},sid_group {},data_group {},updatetime {},email_group {},status {},create_by {},update_by {},step_group {},pdf_org {},pdf_sign {},step_group_detail {},group_data_json {},group_other {},email_view_group {},hash_id {},tracking_group {},status_group {},group_title {},group_name {},bizinfo {},group_status {},cover_page {},calculate_fieds {},maxstep {},email_middle {},html_data {},json_data {},doctype_group {},bizinfo_group {}>'.format(self.id,self.sid_group,self.data_group,self.updatetime,self.email_group,self.status,self.create_by,self.update_by,self.step_group,self.pdf_org,self.pdf_sign,self.step_group_detail,self.group_data_json,self.group_other,self.email_view_group,self.hash_id,self.tracking_group,self.status_group,self.group_title,self.group_name,self.bizinfo,self.group_status,self.cover_page,self.calculate_fieds,self.maxstep,self.email_middle,self.html_data,self.json_data,self.doctype_group,self.bizinfo_group)




class paper_lesstrack(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_track_paper'

    tid = db.Column(db.Integer, primary_key=True)
    tracking = db.Column(db.String)
    t_dateTime = db.Column(db.TIMESTAMP(timezone=True))
    Step = db.Column(db.String)
    convert_id = db.Column(db.Integer)
    file_id = db.Column(db.Integer)
    step_Code = db.Column(db.String)
    step_data_sid = db.Column(db.String)
    hash_sid_code = db.Column(db.String)

    def __init__(self, tracking, t_dateTime, Step, convert_id, file_id, step_Code, step_data_sid,hash_sid_code):
        self.tracking = tracking
        self.t_dateTime = t_dateTime
        self.Step = Step
        self.convert_id = convert_id
        self.file_id = file_id
        self.step_Code = step_Code
        self.step_data_sid = step_data_sid
        self.hash_sid_code = hash_sid_code

    def __repr__(self):
        return '<tid {},tracking {},t_dateTime {},Step {},convert_id {},file_id {},step_Code {},step_data_sid {},hash_sid_code {}>'.format(self.tid, self.tracking, self.t_dateTime, self.Step, self.convert_id, self.file_id, self.step_Code, self.step_data_sid,self.hash_sid_code)

# class paper_lesstrack(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_track_paper'

#     tid = db.Column(db.Integer, primary_key=True)
#     tracking = db.Column(db.String)
#     t_dateTime = db.Column(db.TIMESTAMP(timezone=True))
#     Step = db.Column(db.String)
#     convert_id = db.Column(db.Integer)
#     file_id = db.Column(db.Integer)
#     step_Code = db.Column(db.String)
#     step_data_sid = db.Column(db.String)
#     hash_sid_code = db.Column(db.String)

#     def __init__(self, tracking, t_dateTime, Step, convert_id, file_id, step_Code, step_data_sid,hash_sid_code):
#         self.tracking = tracking
#         self.t_dateTime = t_dateTime
#         self.Step = Step
#         self.convert_id = convert_id
#         self.file_id = file_id
#         self.step_Code = step_Code
#         self.step_data_sid = step_data_sid
#         self.hash_sid_code = hash_sid_code

#     def __repr__(self):
#         return '<tid {},tracking {},t_dateTime {},Step {},convert_id {},file_id {},step_Code {},step_data_sid {},hash_sid_code {}>'.format(self.tid, self.tracking, self.t_dateTime, self.Step, self.convert_id, self.file_id, self.step_Code, self.step_data_sid,self.hash_sid_code)

class paper_lesspdf(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_pdf_storage'

    fid = db.Column(db.Integer, primary_key=True)
    string_pdf = db.Column(db.String)
    hash_pdf = db.Column(db.String)
    string_sign = db.Column(db.String)
    hash_sign = db.Column(db.String)
    pdf_rejectorcancle = db.Column(db.String)
    path_pdf = db.Column(db.String)
    path_sign = db.Column(db.String)
    path = db.Column(db.String)
    path_rejectorcancle = db.Column(db.String)

    def __init__(self, string_pdf, hash_pdf, string_sign, hash_sign,pdf_rejectorcancle,path_pdf,path_sign,path,path_rejectorcancle):
        self.string_pdf = string_pdf
        self.hash_pdf = hash_pdf
        self.string_sign = string_sign
        self.hash_sign = hash_sign
        self.pdf_rejectorcancle = pdf_rejectorcancle
        self.path_pdf = path_pdf
        self.path_sign = path_sign
        self.path = path
        self.path_rejectorcancle = path_rejectorcancle

    def __repr__(self):
        return '<fid {},string_pdf {},hash_pdf {},string_sign {},hash_sign {},pdf_rejectorcancle {},path_pdf {},path_sign {},path {},path_rejectorcancle {}>'.format(self.fid, self.string_pdf, self.hash_pdf, self.string_sign, self.hash_sign,self.pdf_rejectorcancle,self.path_pdf,self.path_sign,self.path,self.path_rejectorcancle)

# class paper_lesspdf(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_pdf_storage'

#     fid = db.Column(db.Integer, primary_key=True)
#     string_pdf = db.Column(db.String)
#     hash_pdf = db.Column(db.String)
#     string_sign = db.Column(db.String)
#     hash_sign = db.Column(db.String)
#     pdf_rejectorcancle = db.Column(db.String)
#     path_pdf = db.Column(db.String)
#     path_sign = db.Column(db.String)
#     path = db.Column(db.String)
#     path_rejectorcancle = db.Column(db.String)

#     def __init__(self, string_pdf, hash_pdf, string_sign, hash_sign,pdf_rejectorcancle,path_pdf,path_sign,path,path_rejectorcancle):
#         self.string_pdf = string_pdf
#         self.hash_pdf = hash_pdf
#         self.string_sign = string_sign
#         self.hash_sign = hash_sign
#         self.pdf_rejectorcancle = pdf_rejectorcancle
#         self.path_pdf = path_pdf
#         self.path_sign = path_sign
#         self.path = path
#         self.path_rejectorcancle = path_rejectorcancle

#     def __repr__(self):
#         return '<fid {},string_pdf {},hash_pdf {},string_sign {},hash_sign {},pdf_rejectorcancle {},path_pdf {},path_sign {},path {},path_rejectorcancle {}>'.format(self.fid, self.string_pdf, self.hash_pdf, self.string_sign, self.hash_sign,self.pdf_rejectorcancle,self.path_pdf,self.path_sign,self.path,self.path_rejectorcancle)

class paper_lesslogerMail_sender(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_logerMail_sender'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    to_mail = db.Column(db.String)
    from_mail = db.Column(db.String)
    hash_to = db.Column(db.String)
    hash_from = db.Column(db.String)
    time = db.Column(db.TIMESTAMP(timezone=True))

    def __init__(self, status, to_mail, from_mail, hash_to,hash_from,time):
        self.status = status
        self.to_mail = to_mail
        self.from_mail = from_mail
        self.hash_to = hash_to
        self.hash_from = hash_from
        self.time = time

    def __repr__(self):
        return '<id {},status {},to_mail {},from_mail {},hash_to {},hash_from {},time {}>'.format(self.id, self.status, self.to_mail, self.from_mail, self.hash_to,self.hash_from,self.time)

# class paper_lesslogerMail_sender(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_logerMail_sender'

#     id = db.Column(db.Integer, primary_key=True)
#     status = db.Column(db.String)
#     to_mail = db.Column(db.String)
#     from_mail = db.Column(db.String)
#     hash_to = db.Column(db.String)
#     hash_from = db.Column(db.String)
#     time = db.Column(db.TIMESTAMP(timezone=True))

#     def __init__(self, status, to_mail, from_mail, hash_to,hash_from,time):
#         self.status = status
#         self.to_mail = to_mail
#         self.from_mail = from_mail
#         self.hash_to = hash_to
#         self.hash_from = hash_from
#         self.time = time

#     def __repr__(self):
#         return '<id {},status {},to_mail {},from_mail {},hash_to {},hash_from {},time {}>'.format(self.id, self.status, self.to_mail, self.from_mail, self.hash_to,self.hash_from,self.time)



class paper_lesstable(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_store_convert'

    cid = db.Column(db.Integer, primary_key=True)
    nameFile = db.Column(db.String)
    sizeFile = db.Column(db.String)
    c_dateTime = db.Column(db.TIMESTAMP(timezone=True))
    c_status = db.Column(db.String)

    def __init__(self, nameFile, sizeFile, c_dateTime, c_status):
        self.nameFile = nameFile
        self.sizeFile = sizeFile
        self.c_dateTime = c_dateTime
        self.c_status = c_status

    def __repr__(self):
        return '<cid {},nameFile {},sizeFile {},c_dateTime {},c_status {}>'.format(self.cid, self.nameFile, self.sizeFile, self.c_dateTime, self.c_status)

# class paper_lesstable(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_store_convert'

#     cid = db.Column(db.Integer, primary_key=True)
#     nameFile = db.Column(db.String)
#     sizeFile = db.Column(db.String)
#     c_dateTime = db.Column(db.TIMESTAMP(timezone=True))
#     c_status = db.Column(db.String)

#     def __init__(self, nameFile, sizeFile, c_dateTime, c_status):
#         self.nameFile = nameFile
#         self.sizeFile = sizeFile
#         self.c_dateTime = c_dateTime
#         self.c_status = c_status

#     def __repr__(self):
#         return '<cid {},nameFile {},sizeFile {},c_dateTime {},c_status {}>'.format(self.cid, self.nameFile, self.sizeFile, self.c_dateTime, self.c_status)


class paper_lesstransactionSftp(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_transactionSftp'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    folder_path = db.Column(db.String)
    date_time = db.Column(db.TIMESTAMP(timezone=True))
    document_type = db.Column(db.String)

    def __init__(self, status, folder_path,date_time,document_type):
        self.status = status
        self.folder_path = folder_path
        self.date_time = date_time
        self.document_type = document_type

    def __repr__(self):
        return '<id {},status {},folder_path {},date_time {},document_type {}>'.format(self.id, self.status,self.folder_path,self.date_time,self.document_type)

# class paper_lesstransactionSftp(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_transactionSftp'

#     id = db.Column(db.Integer, primary_key=True)
#     status = db.Column(db.String)
#     folder_path = db.Column(db.String)
#     date_time = db.Column(db.TIMESTAMP(timezone=True))
#     document_type = db.Column(db.String)

#     def __init__(self, status, folder_path,date_time,document_type):
#         self.status = status
#         self.folder_path = folder_path
#         self.date_time = date_time
#         self.document_type = document_type

#     def __repr__(self):
#         return '<id {},status {},folder_path {},date_time {},document_type {}>'.format(self.id, self.status,self.folder_path,self.date_time,self.document_type)


class paper_lessstep(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_step_template'

    sid = db.Column(db.Integer, primary_key=True)
    step_Code = db.Column(db.String)
    step_Data = db.Column(db.String)
    step_Max = db.Column(db.String)
    username = db.Column(db.String)
    email = db.Column(db.String)
    DateTime = db.Column(db.TIMESTAMP(timezone=True))
    step_Description = db.Column(db.String)
    step_Name = db.Column(db.String)
    step_Upload = db.Column(db.String)
    template_images = db.Column(db.String)
    template_biz = db.Column(db.String)
    qrCode_position = db.Column(db.String)
    status = db.Column(db.String)
    status_Update = db.Column(db.String)
    documentDetails = db.Column(db.String)
    urgent_type = db.Column(db.String)
    condition_temp = db.Column(db.String)
    webhook = db.Column(db.String)
    email_center = db.Column(db.String)
    formula_temp = db.Column(db.String)
    digit_sign = db.Column(db.String)
    page_sign_options = db.Column(db.String)
    options_page = db.Column(db.String)
    status_use = db.Column(db.String)
    time_expire = db.Column(db.String)
    importance_doc = db.Column(db.String)
    last_digit_sign = db.Column(db.String)
    status_ref = db.Column(db.String)

    def __init__(self, step_Code, step_Data, step_Max, username,step_Description, email, DateTime, step_Name,step_Upload,template_images,template_biz,qrCode_position,status,status_Update,documentDetails,urgent_type,condition_temp,webhook,email_center,formula_temp,digit_sign,page_sign_options,options_page,status_use,time_expire,importance_doc,last_digit_sign,status_ref):
        self.step_Code = step_Code
        self.step_Data = step_Data
        self.step_Max = step_Max
        self.username = username
        self.email = email
        self.DateTime = DateTime
        self.step_Description = step_Description
        self.step_Name = step_Name
        self.step_Upload = step_Upload
        self.template_images = template_images
        self.template_biz = template_biz
        self.qrCode_position = qrCode_position
        self.status = status
        self.status_Update = status_Update
        self.documentDetails = documentDetails
        self.urgent_type = urgent_type
        self.condition_temp = condition_temp
        self.webhook = webhook
        self.email_center = email_center
        self.formula_temp = formula_temp
        self.digit_sign = digit_sign
        self.page_sign_options = page_sign_options
        self.options_page = options_page
        self.status_use = status_use
        self.time_expire = time_expire
        self.importance_doc = importance_doc
        self.last_digit_sign = last_digit_sign
        self.status_ref = status_ref

    def __repr__(self):
        return '<sid {},step_Code {},step_Data {},step_Max {},username {},email {},DateTime {},step_Description {},step_Name {},step_Upload {},template_images {},template_biz {},qrCode_position {},status {},status_Update {},documentDetails {},urgent_type {},condition_temp {},webhook {},email_center {},formula_temp {},digit_sign {},page_sign_options {},options_page {},status_use {},time_expire {},importance_doc {},last_digit_sign {},status_ref {}>'.format(self.sid, self.step_Code, self.step_Data, self.step_Max, self.username, self.email, self.DateTime,self.step_Description, self.step_Name,self.step_Upload,self.template_images,self.template_biz,self.qrCode_position,self.status,self.status_Update,self.documentDetails,self.urgent_type,self.condition_temp,self.webhook,self.email_center,self.formula_temp,self.digit_sign,self.page_sign_options,self.options_page,self.status_use,self.time_expire,self.importance_doc,self.last_digit_sign,self.status_ref)


# class paper_lessstep(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_step_template'

#     sid = db.Column(db.Integer, primary_key=True)
#     step_Code = db.Column(db.String)
#     step_Data = db.Column(db.String)
#     step_Max = db.Column(db.String)
#     username = db.Column(db.String)
#     email = db.Column(db.String)
#     DateTime = db.Column(db.TIMESTAMP(timezone=True))
#     step_Description = db.Column(db.String)
#     step_Name = db.Column(db.String)
#     step_Upload = db.Column(db.String)
#     template_images = db.Column(db.String)
#     template_biz = db.Column(db.String)
#     qrCode_position = db.Column(db.String)
#     status = db.Column(db.String)
#     status_Update = db.Column(db.String)
#     documentDetails = db.Column(db.String)
#     urgent_type = db.Column(db.String)
#     condition_temp = db.Column(db.String)
#     webhook = db.Column(db.String)
#     email_center = db.Column(db.String)
#     formula_temp = db.Column(db.String)
#     digit_sign = db.Column(db.String)
#     page_sign_options = db.Column(db.String)
#     options_page = db.Column(db.String)
#     status_use = db.Column(db.String)
#     time_expire = db.Column(db.String)
#     importance_doc = db.Column(db.String)
#     last_digit_sign = db.Column(db.String)
#     status_ref = db.Column(db.String)

#     def __init__(self, step_Code, step_Data, step_Max, username,step_Description, email, DateTime, step_Name,step_Upload,template_images,template_biz,qrCode_position,status,status_Update,documentDetails,urgent_type,condition_temp,webhook,email_center,formula_temp,digit_sign,page_sign_options,options_page,status_use,time_expire,importance_doc,last_digit_sign,status_ref):
#         self.step_Code = step_Code
#         self.step_Data = step_Data
#         self.step_Max = step_Max
#         self.username = username
#         self.email = email
#         self.DateTime = DateTime
#         self.step_Description = step_Description
#         self.step_Name = step_Name
#         self.step_Upload = step_Upload
#         self.template_images = template_images
#         self.template_biz = template_biz
#         self.qrCode_position = qrCode_position
#         self.status = status
#         self.status_Update = status_Update
#         self.documentDetails = documentDetails
#         self.urgent_type = urgent_type
#         self.condition_temp = condition_temp
#         self.webhook = webhook
#         self.email_center = email_center
#         self.formula_temp = formula_temp
#         self.digit_sign = digit_sign
#         self.page_sign_options = page_sign_options
#         self.options_page = options_page
#         self.status_use = status_use
#         self.time_expire = time_expire
#         self.importance_doc = importance_doc
#         self.last_digit_sign = last_digit_sign
#         self.status_ref = status_ref

#     def __repr__(self):
#         return '<sid {},step_Code {},step_Data {},step_Max {},username {},email {},DateTime {},step_Description {},step_Name {},step_Upload {},template_images {},template_biz {},qrCode_position {},status {},status_Update {},documentDetails {},urgent_type {},condition_temp {},webhook {},email_center {},formula_temp {},digit_sign {},page_sign_options {},options_page {},status_use {},time_expire {},importance_doc {},last_digit_sign {},status_ref {}>'.format(self.sid, self.step_Code, self.step_Data, self.step_Max, self.username, self.email, self.DateTime,self.step_Description, self.step_Name,self.step_Upload,self.template_images,self.template_biz,self.qrCode_position,self.status,self.status_Update,self.documentDetails,self.urgent_type,self.condition_temp,self.webhook,self.email_center,self.formula_temp,self.digit_sign,self.page_sign_options,self.options_page,self.status_use,self.time_expire,self.importance_doc,self.last_digit_sign,self.status_ref)


class paper_lessdocumenttrash(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_document_trash'

    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String)
    email_update = db.Column(db.String)
    datetime = db.Column(db.TIMESTAMP(timezone=True))
    email_list = db.Column(db.String)

    def __init__(self, sid, email_update, datetime, email_list):
        self.sid = sid
        self.email_update = email_update
        self.datetime = datetime
        self.email_list = email_list

    def __repr__(self):
        return '<id {},sid {},send_time {},email_update {},datetime {}, email_list {}>'.format(self.id, self.sid, self.email_update, self.datetime, self.email_list)

# class paper_lessdocumenttrash(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_document_trash'

#     id = db.Column(db.Integer, primary_key=True)
#     sid = db.Column(db.String)
#     email_update = db.Column(db.String)
#     datetime = db.Column(db.TIMESTAMP(timezone=True))
    
#     email_list = db.Column(db.String)
#     def __init__(self, sid, email_update, datetime, email_list):
#         self.sid = sid
#         self.email_update = email_update
#         self.datetime = datetime
#         self.email_list = email_list

#     def __repr__(self):
#         return '<id {},sid {},send_time {},email_update {},datetime {}, email_list {}>'.format(self.id, self.sid, self.email_update, self.datetime, self.email_list)

class paper_lesssender(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_send_detail'

    id = db.Column(db.Integer, primary_key=True)
    send_user = db.Column(db.String)
    send_time = db.Column(db.TIMESTAMP(timezone=True))
    status = db.Column(db.String)
    sender_name = db.Column(db.String)
    sender_email = db.Column(db.String)
    sender_position = db.Column(db.String)
    file_id = db.Column(db.String)
    file_name = db.Column(db.String)
    tracking_id = db.Column(db.String)
    step_code = db.Column(db.String)
    step_data_sid = db.Column(db.String)
    doc_id = db.Column(db.String)
    template_webhook = db.Column(db.String)
    email_center = db.Column(db.String)
    recipient_email = db.Column(db.String)
    status_details = db.Column(db.String)
    document_status = db.Column(db.String)
    group_id = db.Column(db.String)
    stepnow = db.Column(db.String)
    stepmax = db.Column(db.String)
    status_service = db.Column(db.String)
    list_ref = db.Column(db.String)
    ref_document = db.Column(db.String)
    status_ref = db.Column(db.String)

    def __init__(self, send_user, send_time, status, sender_name, sender_email, sender_position, file_id, file_name, tracking_id, step_code, step_data_sid, doc_id,template_webhook,email_center,recipient_email,status_details,document_status,group_id,stepnow,stepmax,status_service,list_ref,ref_document,status_ref):
        self.send_user = send_user
        self.send_time = send_time
        self.status = status
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.sender_position = sender_position
        self.file_id = file_id
        self.file_name = file_name
        self.tracking_id = tracking_id
        self.step_code = step_code
        self.step_data_sid = step_data_sid
        self.doc_id = doc_id
        self.template_webhook = template_webhook
        self.email_center = email_center
        self.recipient_email = recipient_email
        self.status_details = status_details
        self.document_status = document_status
        self.group_id = group_id
        self.stepnow = stepnow
        self.stepmax = stepmax
        self.status_service = status_service
        self.list_ref= list_ref
        self.ref_document = ref_document
        self.status_ref = status_ref

    def __repr__(self):
        return '<id {},send_user {},send_time {},status {},sender_name {},sender_email {},sender_position {},file_id {},file_name {},tracking_id {},step_code {},step_data_sid {},doc_id {},template_webhook {},email_center {},recipient_email {},status_details {},document_status {},group_id {},stepnow {},stepmax {},status_service {},list_ref {},ref_document {},status_ref {}>'.format(self.id, self.send_user, self.send_time, self.status, self.sender_name, self.sender_email, self.sender_position, self.file_id, self.file_name, self.tracking_id, self.step_code, self.step_data_sid, self.doc_id,self.template_webhook,self.email_center,self.recipient_email,self.status_details,self.document_status,self.group_id,self.stepnow,self.stepmax,self.status_service,self.list_ref,self.ref_document,self.status_ref)

# class paper_lesssender(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_send_detail'

#     id = db.Column(db.Integer, primary_key=True)
#     send_user = db.Column(db.String)
#     send_time = db.Column(db.TIMESTAMP(timezone=True))
#     status = db.Column(db.String)
#     sender_name = db.Column(db.String)
#     sender_email = db.Column(db.String)
#     sender_position = db.Column(db.String)
#     file_id = db.Column(db.String)
#     file_name = db.Column(db.String)
#     tracking_id = db.Column(db.String)
#     step_code = db.Column(db.String)
#     step_data_sid = db.Column(db.String)
#     doc_id = db.Column(db.String)
#     template_webhook = db.Column(db.String)
#     email_center = db.Column(db.String)
#     recipient_email = db.Column(db.String)
#     status_details = db.Column(db.String)
#     document_status = db.Column(db.String)
#     group_id = db.Column(db.String)
#     stepnow = db.Column(db.String)
#     stepmax = db.Column(db.String)
#     status_service = db.Column(db.String)
#     list_ref = db.Column(db.String)
#     ref_document = db.Column(db.String)
#     status_ref = db.Column(db.String)

#     def __init__(self, send_user, send_time, status, sender_name, sender_email, sender_position, file_id, file_name, tracking_id, step_code, step_data_sid, doc_id,template_webhook,email_center,recipient_email,status_details,document_status,group_id,stepnow,stepmax,status_service,list_ref,ref_document,status_ref):
#         self.send_user = send_user
#         self.send_time = send_time
#         self.status = status
#         self.sender_name = sender_name
#         self.sender_email = sender_email
#         self.sender_position = sender_position
#         self.file_id = file_id
#         self.file_name = file_name
#         self.tracking_id = tracking_id
#         self.step_code = step_code
#         self.step_data_sid = step_data_sid
#         self.doc_id = doc_id
#         self.template_webhook = template_webhook
#         self.email_center = email_center
#         self.recipient_email = recipient_email
#         self.status_details = status_details
#         self.document_status = document_status
#         self.group_id = group_id
#         self.stepnow = stepnow
#         self.stepmax = stepmax
#         self.status_service = status_service
#         self.list_ref= list_ref
#         self.ref_document = ref_document
#         self.status_ref = status_ref

#     def __repr__(self):
#         return '<id {},send_user {},send_time {},status {},sender_name {},sender_email {},sender_position {},file_id {},file_name {},tracking_id {},step_code {},step_data_sid {},doc_id {},template_webhook {},email_center {},recipient_email {},status_details {},document_status {},group_id {},stepnow {},stepmax {},status_service {},list_ref {},ref_document {},status_ref {}>'.format(self.id, self.send_user, self.send_time, self.status, self.sender_name, self.sender_email, self.sender_position, self.file_id, self.file_name, self.tracking_id, self.step_code, self.step_data_sid, self.doc_id,self.template_webhook,self.email_center,self.recipient_email,self.status_details,self.document_status,self.group_id,self.stepnow,self.stepmax,self.status_service,self.list_ref,self.ref_document,self.status_ref)

class paper_lessdatastep(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_step_data'

    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String)
    data_json = db.Column(db.String)
    update_time = db.Column(db.TIMESTAMP(timezone=True))
    data_json_Upload = db.Column(db.String)
    upload_time = db.Column(db.String)
    biz_info = db.Column(db.String)
    view_details = db.Column(db.String)
    qrCode_position = db.Column(db.String)

    def __init__(self, sid, data_json, update_time, data_json_Upload, upload_time,biz_info,view_details,qrCode_position):
        self.sid = sid
        self.data_json = data_json
        self.update_time = update_time
        self.data_json_Upload = data_json_Upload
        self.upload_time = upload_time
        self.biz_info = biz_info
        self.view_details   = view_details
        self.qrCode_position = qrCode_position

    def __repr__(self):
        return '<id {},sid {},data_json {},update_time {},data_json_Upload {},upload_time {},biz_info {},view_details {},qrCode_position {}>'.format(self.id, self.sid, self.data_json, self.update_time, self.data_json_Upload, self.upload_time,self.biz_info,self.view_details,self.qrCode_position)

# class paper_lessdatastep(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_step_data'

#     id = db.Column(db.Integer, primary_key=True)
#     sid = db.Column(db.String)
#     data_json = db.Column(db.String)
#     update_time = db.Column(db.TIMESTAMP(timezone=True))
#     data_json_Upload = db.Column(db.String)
#     upload_time = db.Column(db.String)
#     biz_info = db.Column(db.String)
#     view_details = db.Column(db.String)
#     qrCode_position = db.Column(db.String)

#     def __init__(self, sid, data_json, update_time, data_json_Upload, upload_time,biz_info,view_details,qrCode_position):
#         self.sid = sid
#         self.data_json = data_json
#         self.update_time = update_time
#         self.data_json_Upload = data_json_Upload
#         self.upload_time = upload_time
#         self.biz_info = biz_info
#         self.view_details   = view_details
#         self.qrCode_position = qrCode_position

#     def __repr__(self):
#         return '<id {},sid {},data_json {},update_time {},data_json_Upload {},upload_time {},biz_info {},view_details {},qrCode_position {}>'.format(self.id, self.sid, self.data_json, self.update_time, self.data_json_Upload, self.upload_time,self.biz_info,self.view_details,self.qrCode_position)

class paper_lesssign(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_sign_data'

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.String)
    sign_json = db.Column(db.String)
    sid = db.Column(db.String)

    def __init__(self, file_id, sign_json, sid):
        self.file_id = file_id
        self.sign_json = sign_json
        self.sid = sid

    def __repr__(self):
        return '<id {},file_id {},sign_json {},sid {}>'.format(self.id, self.file_id, self.sign_json, self.sid)

# class paper_lesssign(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_sign_data'

#     id = db.Column(db.Integer, primary_key=True)
#     file_id = db.Column(db.String)
#     sign_json = db.Column(db.String)
#     sid = db.Column(db.String)

#     def __init__(self, file_id, sign_json, sid):
#         self.file_id = file_id
#         self.sign_json = sign_json
#         self.sid = sid

#     def __repr__(self):
#         return '<id {},file_id {},sign_json {},sid {}>'.format(self.id, self.file_id, self.sign_json, self.sid)

class paper_lessRecipient_user(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_recipient_user'

    id = db.Column(db.Integer, primary_key=True)
    recipient_email = db.Column(db.String)
    sid = db.Column(db.String)

    def __init__(self, recipient_email, sid):
        self.recipient_email = recipient_email
        self.sid = sid

    def __repr__(self):
        return '<id {},recipient_email {},sid {}>'.format(self.id, self.recipient_email, self.sid)

# class paper_lessRecipient_user(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_recipient_user'

#     id = db.Column(db.Integer, primary_key=True)
#     recipient_email = db.Column(db.String)
#     sid = db.Column(db.String)

#     def __init__(self, recipient_email, sid):
#         self.recipient_email = recipient_email
#         self.sid = sid

#     def __repr__(self):
#         return '<id {},recipient_email {},sid {}>'.format(self.id, self.recipient_email, self.sid)


class paper_lessdocument(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_doc_detail'

    id = db.Column(db.Integer, primary_key=True)
    timest = db.Column(db.String)
    step_id = db.Column(db.String)
    typefile = db.Column(db.String)
    fileid = db.Column(db.Integer)
    document_id = db.Column(db.String)
    documentJson = db.Column(db.String)
    documentType = db.Column(db.String)
    urgent_type = db.Column(db.String)
    digit_sign = db.Column(db.String)
    attempted_folder = db.Column(db.String)
    sign_page_options = db.Column(db.String)
    options_page = db.Column(db.String)
    data_document = db.Column(db.String)

    def __init__(self, timest, step_id, typefile, fileid, document_id,documentJson,documentType,urgent_type,digit_sign,attempted_folder,sign_page_options,options_page,data_document):
        self.timest = timest
        self.step_id = step_id
        self.typefile = typefile
        self.fileid = fileid
        self.document_id = document_id
        self.documentJson = documentJson
        self.documentType = documentType
        self.urgent_type = urgent_type
        self.digit_sign = digit_sign
        self.attempted_folder = attempted_folder
        self.sign_page_options = sign_page_options
        self.options_page = options_page
        self.data_document = data_document

    def __repr__(self):
        return '<id {},timest {},step_id {},typefile {},fileid {},document_id {},documentJson {},documentType {},urgent_type {},digit_sign {},attempted_folder {},sign_page_options {},options_page {},data_document {}>'.format(self.id, self.timest, self.step_id, self.typefile, self.fileid, self.document_id,self.documentJson,self.documentType,self.urgent_type,self.digit_sign,self.attempted_folder,self.sign_page_options,self.options_page,self.data_document)

# class paper_lessdocument(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_doc_detail'

#     id = db.Column(db.Integer, primary_key=True)
#     timest = db.Column(db.String)
#     step_id = db.Column(db.String)
#     typefile = db.Column(db.String)
#     fileid = db.Column(db.Integer)
#     document_id = db.Column(db.String)
#     documentJson = db.Column(db.String)
#     documentType = db.Column(db.String)
#     urgent_type = db.Column(db.String)
#     digit_sign = db.Column(db.String)
#     attempted_folder = db.Column(db.String)
#     sign_page_options = db.Column(db.String)
#     options_page = db.Column(db.String)
#     data_document = db.Column(db.String)

#     def __init__(self, timest, step_id, typefile, fileid, document_id,documentJson,documentType,urgent_type,digit_sign,attempted_folder,sign_page_options,options_page,data_document):
#         self.timest = timest
#         self.step_id = step_id
#         self.typefile = typefile
#         self.fileid = fileid
#         self.document_id = document_id
#         self.documentJson = documentJson
#         self.documentType = documentType
#         self.urgent_type = urgent_type
#         self.digit_sign = digit_sign
#         self.attempted_folder = attempted_folder
#         self.sign_page_options = sign_page_options
#         self.options_page = options_page
#         self.data_document = data_document

#     def __repr__(self):
#         return '<id {},timest {},step_id {},typefile {},fileid {},document_id {},documentJson {},documentType {},urgent_type {},digit_sign {},attempted_folder {},sign_page_options {},options_page {},data_document {}>'.format(self.id, self.timest, self.step_id, self.typefile, self.fileid, self.document_id,self.documentJson,self.documentType,self.urgent_type,self.digit_sign,self.attempted_folder,self.sign_page_options,self.options_page,self.data_document)

class paper_lessdocument_1(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_doc_detail_1'

    id = db.Column(db.Integer, primary_key=True)
    timest = db.Column(db.String)
    step_id = db.Column(db.String)
    typefile = db.Column(db.String)
    fileid = db.Column(db.Integer)
    document_id = db.Column(db.String)
    documentJson = db.Column(db.String)
    documentType = db.Column(db.String)
    urgent_type = db.Column(db.String)
    digit_sign = db.Column(db.String)
    attempted_folder = db.Column(db.String)
    sign_page_options = db.Column(db.String)
    options_page = db.Column(db.String)
    data_document = db.Column(db.String)

    def __init__(self, timest, step_id, typefile, fileid, document_id,documentJson,documentType,urgent_type,digit_sign,attempted_folder,sign_page_options,options_page,data_document):
        self.timest = timest
        self.step_id = step_id
        self.typefile = typefile
        self.fileid = fileid
        self.document_id = document_id
        self.documentJson = documentJson
        self.documentType = documentType
        self.urgent_type = urgent_type
        self.digit_sign = digit_sign
        self.attempted_folder = attempted_folder
        self.sign_page_options = sign_page_options
        self.options_page = options_page
        self.data_document = data_document

    def __repr__(self):
        return '<id {},timest {},step_id {},typefile {},fileid {},document_id {},documentJson {},documentType {},urgent_type {},digit_sign {},attempted_folder {},sign_page_options {},options_page {},data_document {}>'.format(self.id, self.timest, self.step_id, self.typefile, self.fileid, self.document_id,self.documentJson,self.documentType,self.urgent_type,self.digit_sign,self.attempted_folder,self.sign_page_options,self.options_page,self.data_document)


# class paper_lessdocument_1(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_doc_detail_1'

#     id = db.Column(db.Integer, primary_key=True)
#     timest = db.Column(db.String)
#     step_id = db.Column(db.String)
#     typefile = db.Column(db.String)
#     fileid = db.Column(db.Integer)
#     document_id = db.Column(db.String)
#     documentJson = db.Column(db.String)
#     documentType = db.Column(db.String)
#     urgent_type = db.Column(db.String)
#     digit_sign = db.Column(db.String)
#     attempted_folder = db.Column(db.String)
#     sign_page_options = db.Column(db.String)
#     options_page = db.Column(db.String)
#     data_document = db.Column(db.String)

#     def __init__(self, timest, step_id, typefile, fileid, document_id,documentJson,documentType,urgent_type,digit_sign,attempted_folder,sign_page_options,options_page,data_document):
#         self.timest = timest
#         self.step_id = step_id
#         self.typefile = typefile
#         self.fileid = fileid
#         self.document_id = document_id
#         self.documentJson = documentJson
#         self.documentType = documentType
#         self.urgent_type = urgent_type
#         self.digit_sign = digit_sign
#         self.attempted_folder = attempted_folder
#         self.sign_page_options = sign_page_options
#         self.options_page = options_page
#         self.data_document = data_document

#     def __repr__(self):
#         return '<id {},timest {},step_id {},typefile {},fileid {},document_id {},documentJson {},documentType {},urgent_type {},digit_sign {},attempted_folder {},sign_page_options {},options_page {},data_document {}>'.format(self.id, self.timest, self.step_id, self.typefile, self.fileid, self.document_id,self.documentJson,self.documentType,self.urgent_type,self.digit_sign,self.attempted_folder,self.sign_page_options,self.options_page,self.data_document)


class paper_lessmail(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_logerMail"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    to_mail = db.Column(db.String)
    from_mail = db.Column(db.String)
    qrcode_string = db.Column(db.Integer)
    hash_to = db.Column(db.String)
    hash_from = db.Column(db.String)
    url_qrcode = db.Column(db.String)
    time = db.Column(db.TIMESTAMP(timezone=True))
    sid = db.Column(db.String)
    qrcode_hash = db.Column(db.String)

    def __init__(self, status, to_mail, from_mail, qrcode_string, hash_to, hash_from, url_qrcode, time, sid, qrcode_hash):
        self.status = status
        self.to_mail = to_mail
        self.from_mail = from_mail
        self.qrcode_string = qrcode_string
        self.hash_to = hash_to
        self.hash_from = hash_from
        self.url_qrcode = url_qrcode
        self.time = time
        self.sid = sid
        self.qrcode_hash = qrcode_hash

    def __repr__(self):
        return '<id {},status {},to_mail {},from_mail {},qrcode_string {},hash_to {},hash_from {},url_qrcode {},time {},sid {},qrcode_hash {}>'.format(self.id, self.status, self.to_mail, self.from_mail, self.qrcode_string, self.hash_to, self.hash_from, self.url_qrcode, self.time, self.sid, self.qrcode_hash)

# class paper_lessmail(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_logerMail"

#     id = db.Column(db.Integer, primary_key=True)
#     status = db.Column(db.String)
#     to_mail = db.Column(db.String)
#     from_mail = db.Column(db.String)
#     qrcode_string = db.Column(db.Integer)
#     hash_to = db.Column(db.String)
#     hash_from = db.Column(db.String)
#     url_qrcode = db.Column(db.String)
#     time = db.Column(db.TIMESTAMP(timezone=True))
#     sid = db.Column(db.String)
#     qrcode_hash = db.Column(db.String)

#     def __init__(self, status, to_mail, from_mail, qrcode_string, hash_to, hash_from, url_qrcode, time, sid, qrcode_hash):
#         self.status = status
#         self.to_mail = to_mail
#         self.from_mail = from_mail
#         self.qrcode_string = qrcode_string
#         self.hash_to = hash_to
#         self.hash_from = hash_from
#         self.url_qrcode = url_qrcode
#         self.time = time
#         self.sid = sid
#         self.qrcode_hash = qrcode_hash

#     def __repr__(self):
#         return '<id {},status {},to_mail {},from_mail {},qrcode_string {},hash_to {},hash_from {},url_qrcode {},time {},sid {},qrcode_hash {}>'.format(self.id, self.status, self.to_mail, self.from_mail, self.qrcode_string, self.hash_to, self.hash_from, self.url_qrcode, self.time, self.sid, self.qrcode_hash)



class paper_lessrefCode(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_ref_doc"

    sid = db.Column(db.String)
    ref_Code = db.Column(db.String, primary_key=True)
    ref_Detail = db.Column(db.String)

    def __init__(self, sid, ref_Code, ref_Detail):
        self.sid = sid
        self.ref_Code = ref_Code
        self.ref_Detail = ref_Detail

    def __repr__(self):
        return '<sid {},ref_Code {},ref_Detail {}>'.format(self.sid, self.ref_Code, self.ref_Detail)

# class paper_lessrefCode(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_ref_doc"

#     sid = db.Column(db.String)
#     ref_Code = db.Column(db.String, primary_key=True)
#     ref_Detail = db.Column(db.String)

#     def __init__(self, sid, ref_Code, ref_Detail):
#         self.sid = sid
#         self.ref_Code = ref_Code
#         self.ref_Detail = ref_Detail

#     def __repr__(self):
#         return '<sid {},ref_Code {},ref_Detail {}>'.format(self.sid, self.ref_Code, self.ref_Detail)


class paper_lesstransactionChat(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_transactionChat"

    transactionCode = db.Column(db.Integer, primary_key=True)
    sidCode = db.Column(db.String)
    timeStamp = db.Column(db.TIMESTAMP(timezone=True))
    statusId = db.Column(db.String)
    OrderResult = db.Column(db.String)
    email_User = db.Column(db.String)
    statusSign = db.Column(db.String)
    stepNum = db.Column(db.String)
    sendChat = db.Column(db.String)
    urlSign = db.Column(db.String)
    propertyChat = db.Column(db.String)
    # image_url = db.Column(db.String)
    id_chat = db.Column(db.String)

    def __init__(self, sidCode, timeStamp, statusId, OrderResult, email_User, statusSign, stepNum, sendChat,urlSign,propertyChat,id_chat):
        self.sidCode = sidCode
        self.timeStamp = timeStamp
        self.statusId = statusId
        self.OrderResult = OrderResult
        self.email_User = email_User
        self.statusSign = statusSign
        self.stepNum = stepNum
        self.sendChat = sendChat
        self.urlSign  = urlSign
        self.propertyChat = propertyChat
        self.id_chat = id_chat

    def __repr__(self):
        return '<transactionCode {},sidCode {},timeStamp {},statusId {},OrderResult {},email_User {},statusSign {},stepNum {},sendChat {},urlSign {},propertyChat {},id_chat {}>'.format(self.transactionCode, self.sidCode, self.timeStamp, self.statusId, self.OrderResult, self.email_User, self.statusSign, self.stepNum, self.sendChat,self.urlSign,self.propertyChat,self.id_chat)

# class paper_lesstransactionChat(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_transactionChat"

#     transactionCode = db.Column(db.Integer, primary_key=True)
#     sidCode = db.Column(db.String)
#     timeStamp = db.Column(db.TIMESTAMP(timezone=True))
#     statusId = db.Column(db.String)
#     OrderResult = db.Column(db.String)
#     email_User = db.Column(db.String)
#     statusSign = db.Column(db.String)
#     stepNum = db.Column(db.String)
#     sendChat = db.Column(db.String)
#     urlSign = db.Column(db.String)
#     propertyChat = db.Column(db.String)
#     # image_url = db.Column(db.String)
#     id_chat = db.Column(db.String)

#     def __init__(self, sidCode, timeStamp, statusId, OrderResult, email_User, statusSign, stepNum, sendChat,urlSign,propertyChat,id_chat):
#         self.sidCode = sidCode
#         self.timeStamp = timeStamp
#         self.statusId = statusId
#         self.OrderResult = OrderResult
#         self.email_User = email_User
#         self.statusSign = statusSign
#         self.stepNum = stepNum
#         self.sendChat = sendChat
#         self.urlSign  = urlSign
#         self.propertyChat = propertyChat
#         self.id_chat = id_chat

#     def __repr__(self):
#         return '<transactionCode {},sidCode {},timeStamp {},statusId {},OrderResult {},email_User {},statusSign {},stepNum {},sendChat {},urlSign {},propertyChat {},id_chat {}>'.format(self.transactionCode, self.sidCode, self.timeStamp, self.statusId, self.OrderResult, self.email_User, self.statusSign, self.stepNum, self.sendChat,self.urlSign,self.propertyChat,self.id_chat)



class paper_lesstransactionChain(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_transactionChain"

    f_id = db.Column(db.Integer, primary_key=True)
    f_sid = db.Column(db.String)
    f_file_id = db.Column(db.String)
    f_transactionId = db.Column(db.String)
    f_timestamp = db.Column(db.TIMESTAMP(timezone=True))
    f_metadate = db.Column(db.String)
    f_userAccount = db.Column(db.String)
    f_row = db.Column(db.String)

    def __init__(self, f_sid, f_file_id, f_transactionId, f_timestamp, f_metadate, f_userAccount, f_row):
        self.f_sid = f_sid
        self.f_file_id = f_file_id
        self.f_transactionId = f_transactionId
        self.f_timestamp = f_timestamp
        self.f_metadate = f_metadate
        self.f_userAccount = f_userAccount
        self.f_row = f_row

    def __repr__(self):
        return '<f_sid {},f_file_id {},f_transactionId {},f_timestamp {},f_metadate {},f_userAccount {},f_row {}>'.format(self.f_sid, self.f_file_id, self.f_transactionId, self.f_timestamp, self.f_metadate, self.f_userAccount, self.f_row)

# class paper_lesstransactionChain(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_transactionChain"

#     f_id = db.Column(db.Integer, primary_key=True)
#     f_sid = db.Column(db.String)
#     f_file_id = db.Column(db.String)
#     f_transactionId = db.Column(db.String)
#     f_timestamp = db.Column(db.TIMESTAMP(timezone=True))
#     f_metadate = db.Column(db.String)
#     f_userAccount = db.Column(db.String)
#     f_row = db.Column(db.String)

#     def __init__(self, f_sid, f_file_id, f_transactionId, f_timestamp, f_metadate, f_userAccount, f_row):
#         self.f_sid = f_sid
#         self.f_file_id = f_file_id
#         self.f_transactionId = f_transactionId
#         self.f_timestamp = f_timestamp
#         self.f_metadate = f_metadate
#         self.f_userAccount = f_userAccount
#         self.f_row = f_row

#     def __repr__(self):
#         return '<f_sid {},f_file_id {},f_transactionId {},f_timestamp {},f_metadate {},f_userAccount {},f_row {}>'.format(self.f_sid, self.f_file_id, self.f_transactionId, self.f_timestamp, self.f_metadate, self.f_userAccount, self.f_row)


class paper_lessuserProfile(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_userProfile"

    p_id = db.Column(db.Integer, primary_key=True)
    p_username = db.Column(db.String)
    p_userid = db.Column(db.String)
    p_updateTime = db.Column(db.TIMESTAMP(timezone=True))
    p_webHook = db.Column(db.String)
    p_sign = db.Column(db.String)
    p_emailUser = db.Column(db.String)
    p_emailthai = db.Column(db.String)
    p_taskchat = db.Column(db.String)
    p_todo = db.Column(db.String)
    p_doing = db.Column(db.String)
    p_done = db.Column(db.String)
    p_options = db.Column(db.String)
    p_signca = db.Column(db.String)
    chat_noti = db.Column(db.String)
    email_noti = db.Column(db.String)
    permission_id = db.Column(db.String)

    def __init__(self, p_username, p_userid, p_updateTime, p_webHook,p_sign,p_emailUser,p_emailthai,p_taskchat,p_todo,p_doing,p_done,p_options,p_signca,chat_noti,email_noti,permission_id):
        self.p_username = p_username
        self.p_userid = p_userid
        self.p_updateTime = p_updateTime
        self.p_webHook = p_webHook
        self.p_sign = p_sign
        self.p_emailUser = p_emailUser
        self.p_emailthai = p_emailthai
        self.p_taskchat = p_taskchat
        self.p_todo = p_todo
        self.p_doing = p_doing
        self.p_done = p_done
        self.p_options = p_options
        self.p_signca = p_signca
        self.chat_noti = chat_noti
        self.email_noti = email_noti
        self.permission_id = permission_id

    def __repr__(self):
        return '<p_username {},p_userid {},p_updateTime {},p_webHook {},p_sign {},p_emailUser {},p_emailthai {},p_taskchat {},p_todo {},p_doing {},p_done {},p_options {},p_signca {},chat_noti {},email_noti {},permission_id {}>'.format(self.p_username, self.p_userid, self.p_updateTime, self.p_webHook,self.p_sign,self.p_emailUser,self.p_emailthai,self.p_taskchat,self.p_todo,self.p_doing,self.p_done,self.p_options,self.p_signca,self.chat_noti,self.email_noti,self.permission_id)


# class paper_lessuserProfile(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_userProfile"

#     p_id = db.Column(db.Integer, primary_key=True)
#     p_username = db.Column(db.String)
#     p_userid = db.Column(db.String)
#     p_updateTime = db.Column(db.TIMESTAMP(timezone=True))
#     p_webHook = db.Column(db.String)
#     p_sign = db.Column(db.String)
#     p_emailUser = db.Column(db.String)
#     p_emailthai = db.Column(db.String)
#     p_taskchat = db.Column(db.String)
#     p_todo = db.Column(db.String)
#     p_doing = db.Column(db.String)
#     p_done = db.Column(db.String)
#     p_options = db.Column(db.String)
#     p_signca = db.Column(db.String)
#     chat_noti = db.Column(db.String)
#     email_noti = db.Column(db.String)
#     permission_id = db.Column(db.String)

#     def __init__(self, p_username, p_userid, p_updateTime, p_webHook,p_sign,p_emailUser,p_emailthai,p_taskchat,p_todo,p_doing,p_done,p_options,p_signca,chat_noti,email_noti,permission_id):
#         self.p_username = p_username
#         self.p_userid = p_userid
#         self.p_updateTime = p_updateTime
#         self.p_webHook = p_webHook
#         self.p_sign = p_sign
#         self.p_emailUser = p_emailUser
#         self.p_emailthai = p_emailthai
#         self.p_taskchat = p_taskchat
#         self.p_todo = p_todo
#         self.p_doing = p_doing
#         self.p_done = p_done
#         self.p_options = p_options
#         self.p_signca = p_signca
#         self.chat_noti = chat_noti
#         self.email_noti = email_noti
#         self.permission_id = permission_id

#     def __repr__(self):
#         return '<p_username {},p_userid {},p_updateTime {},p_webHook {},p_sign {},p_emailUser {},p_emailthai {},p_taskchat {},p_todo {},p_doing {},p_done {},p_options {},p_signca {},chat_noti {},email_noti {},permission_id {}>'.format(self.p_username, self.p_userid, self.p_updateTime, self.p_webHook,self.p_sign,self.p_emailUser,self.p_emailthai,self.p_taskchat,self.p_todo,self.p_doing,self.p_done,self.p_options,self.p_signca,self.chat_noti,self.email_noti,self.permission_id)


class paper_lesslogin(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_citizen_Login"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String)
    username = db.Column(db.String)
    access_time = db.Column(db.TIMESTAMP(timezone=True))
    vertify_token = db.Column(db.String)
    access_token = db.Column(db.String)
    access_token_time = db.Column(db.String)
    access_token_begin = db.Column(db.String)
    one_access_token = db.Column(db.String)
    citizen_data = db.Column(db.String)
    hash_data = db.Column(db.String)
    biz_information = db.Column(db.String)
    secure_number = db.Column(db.String)
    ipaddress = db.Column(db.String)

    def __init__(self, account_id, username, access_time, vertify_token,access_token,access_token_time,access_token_begin,one_access_token,citizen_data,hash_data,biz_information,secure_number,ipaddress):
        self.account_id         = account_id
        self.username           = username
        self.access_time        = access_time
        self.vertify_token      = vertify_token
        self.access_token       = access_token
        self.access_token_time  = access_token_time
        self.access_token_begin = access_token_begin
        self.one_access_token   = one_access_token
        self.citizen_data       = citizen_data
        self.hash_data          = hash_data
        self.biz_information    = biz_information
        self.secure_number      = secure_number
        self.ipaddress          = ipaddress

    def __repr__(self):
        return '<account_id {},username {},access_time {},vertify_token {},access_token {},access_token_time {},access_token_begin {},one_access_token {},citizen_data {},hash_data {},biz_information {},secure_number {},ipaddress {}>'.format(self.account_id, self.username, self.access_time, self.vertify_token,self.access_token,self.access_token_time,self.access_token_begin,self.one_access_token,self.citizen_data,self.hash_data,self.biz_information,self.secure_number,self.ipaddress)

# class paper_lesslogin(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_citizen_Login"

#     id = db.Column(db.Integer, primary_key=True)
#     account_id = db.Column(db.String)
#     username = db.Column(db.String)
#     access_time = db.Column(db.TIMESTAMP(timezone=True))
#     vertify_token = db.Column(db.String)
#     access_token = db.Column(db.String)
#     access_token_time = db.Column(db.String)
#     access_token_begin = db.Column(db.String)
#     one_access_token = db.Column(db.String)
#     citizen_data = db.Column(db.String)
#     hash_data = db.Column(db.String)
#     biz_information = db.Column(db.String)
#     secure_number = db.Column(db.String)
#     ipaddress = db.Column(db.String)

#     def __init__(self, account_id, username, access_time, vertify_token,access_token,access_token_time,access_token_begin,one_access_token,citizen_data,hash_data,biz_information,secure_number,ipaddress):
#         self.account_id         = account_id
#         self.username           = username
#         self.access_time        = access_time
#         self.vertify_token      = vertify_token
#         self.access_token       = access_token
#         self.access_token_time  = access_token_time
#         self.access_token_begin = access_token_begin
#         self.one_access_token   = one_access_token
#         self.citizen_data       = citizen_data
#         self.hash_data          = hash_data
#         self.biz_information    = biz_information
#         self.secure_number      = secure_number
#         self.ipaddress          = ipaddress

#     def __repr__(self):
#         return '<account_id {},username {},access_time {},vertify_token {},access_token {},access_token_time {},access_token_begin {},one_access_token {},citizen_data {},hash_data {},biz_information {},secure_number {},ipaddress {}>'.format(self.account_id, self.username, self.access_time, self.vertify_token,self.access_token,self.access_token_time,self.access_token_begin,self.one_access_token,self.citizen_data,self.hash_data,self.biz_information,self.secure_number,self.ipaddress)


class paper_lesstransactionLogin(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_transactionLogin"

    transactionLogin = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    userid = db.Column(db.String)
    transactionCode = db.Column(db.String)
    date_time = db.Column(db.TIMESTAMP(timezone=True))
    ipaddress = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, username, userid,transactionCode,date_time,ipaddress,email):
        self.username               = username
        self.userid                 = userid
        self.transactionCode        = transactionCode
        self.date_time              = date_time
        self.ipaddress              = ipaddress
        self.email                  = email

    def __repr__(self):
        return '<username {},userid {},transactionCode {},date_time {},ipaddress {},email {}>'.format(self.username, self.userid, self.transactionCode, self.date_time,self.ipaddress,self.email)

# class paper_lesstransactionLogin(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_transactionLogin"

#     transactionLogin = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String)
#     userid = db.Column(db.String)
#     transactionCode = db.Column(db.String)
#     date_time = db.Column(db.TIMESTAMP(timezone=True))
#     ipaddress = db.Column(db.String)
#     email = db.Column(db.String)

#     def __init__(self, username, userid,transactionCode,date_time,ipaddress,email):
#         self.username               = username
#         self.userid                 = userid
#         self.transactionCode        = transactionCode
#         self.date_time              = date_time
#         self.ipaddress              = ipaddress
#         self.email                  = email

#     def __repr__(self):
#         return '<username {},userid {},transactionCode {},date_time {},ipaddress {},email {}>'.format(self.username, self.userid, self.transactionCode, self.date_time,self.ipaddress,self.email)


class paper_lessmessageComment(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_messageComment"

    comment_id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String)
    message_Comment = db.Column(db.String)
    time_Update = db.Column(db.TIMESTAMP(timezone=True))

    def __init__(self, sid, message_Comment,time_Update):
        self.sid               = sid
        self.message_Comment   = message_Comment
        self.time_Update       = time_Update

    def __repr__(self):
        return '<comment_id {},sid {},message_Comment {},time_Update {}>'.format(self.comment_id,self.sid,self.message_Comment,self.time_Update)

# class paper_lessmessageComment(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_messageComment"

#     comment_id = db.Column(db.Integer, primary_key=True)
#     sid = db.Column(db.String)
#     message_Comment = db.Column(db.String)
#     time_Update = db.Column(db.TIMESTAMP(timezone=True))

#     def __init__(self, sid, message_Comment,time_Update):
#         self.sid               = sid
#         self.message_Comment   = message_Comment
#         self.time_Update       = time_Update

#     def __repr__(self):
#         return '<comment_id {},sid {},message_Comment {},time_Update {}>'.format(self.comment_id,self.sid,self.message_Comment,self.time_Update)


class paper_lesstransactionMail(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_transactionMail"

    transactionCode = db.Column(db.Integer, primary_key=True)
    sidCode = db.Column(db.String)
    timeStamp = db.Column(db.TIMESTAMP(timezone=True))
    statusId = db.Column(db.String)
    OrderResult = db.Column(db.String)
    email_User = db.Column(db.String)
    statusSign = db.Column(db.String)
    stepNum = db.Column(db.String)
    sendMail = db.Column(db.String)
    urlSign = db.Column(db.String)
    propertyMail = db.Column(db.String)

    def __init__(self, sidCode, timeStamp,statusId,OrderResult,email_User,statusSign,stepNum,sendMail,urlSign,propertyMail):
        self.sidCode    = sidCode
        self.timeStamp  = timeStamp
        self.statusId   = statusId
        self.OrderResult= OrderResult
        self.email_User = email_User
        self.statusSign = statusSign
        self.stepNum    = stepNum
        self.sendMail   = sendMail
        self.urlSign    = urlSign
        self.propertyMail = propertyMail

    def __repr__(self):
        return '<sidCode {},timeStamp {},statusId {},OrderResult {},email_User {},statusSign {},stepNum {},sendMail {},urlSign {},propertyMail {}>'.format(self.sidCode,self.timeStamp,self.statusId,self.OrderResult,self.email_User,self.statusSign,self.stepNum,self.sendMail,self.urlSign,self.propertyMail)

# class paper_lesstransactionMail(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_transactionMail"

#     transactionCode = db.Column(db.Integer, primary_key=True)
#     sidCode = db.Column(db.String)
#     timeStamp = db.Column(db.TIMESTAMP(timezone=True))
#     statusId = db.Column(db.String)
#     OrderResult = db.Column(db.String)
#     email_User = db.Column(db.String)
#     statusSign = db.Column(db.String)
#     stepNum = db.Column(db.String)
#     sendMail = db.Column(db.String)
#     urlSign = db.Column(db.String)
#     propertyMail = db.Column(db.String)

#     def __init__(self, sidCode, timeStamp,statusId,OrderResult,email_User,statusSign,stepNum,sendMail,urlSign,propertyMail):
#         self.sidCode    = sidCode
#         self.timeStamp  = timeStamp
#         self.statusId   = statusId
#         self.OrderResult= OrderResult
#         self.email_User = email_User
#         self.statusSign = statusSign
#         self.stepNum    = stepNum
#         self.sendMail   = sendMail
#         self.urlSign    = urlSign
#         self.propertyMail = propertyMail

#     def __repr__(self):
#         return '<sidCode {},timeStamp {},statusId {},OrderResult {},email_User {},statusSign {},stepNum {},sendMail {},urlSign {},propertyMail {}>'.format(self.sidCode,self.timeStamp,self.statusId,self.OrderResult,self.email_User,self.statusSign,self.stepNum,self.sendMail,self.urlSign,self.propertyMail)



class paper_lessbizLogin(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_bizLogin"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String)
    biz_information = db.Column(db.String)
    username = db.Column(db.String)
    update_time = db.Column(db.TIMESTAMP(timezone=True))

    def __init__(self, account_id, biz_information,username,update_time):
        self.account_id    = account_id
        self.biz_information    = biz_information
        self.username       = username
        self.update_time    = update_time

    def __repr__(self):
        return '<id {},account_id {},biz_information {},username {},update_time {}>'.format(self.id,self.account_id,self.biz_information,self.username,self.update_time)

# class paper_lessbizLogin(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_bizLogin"

#     id = db.Column(db.Integer, primary_key=True)
#     account_id = db.Column(db.String)
#     biz_information = db.Column(db.String)
#     username = db.Column(db.String)
#     update_time = db.Column(db.TIMESTAMP(timezone=True))

#     def __init__(self, account_id, biz_information,username,update_time):
#         self.account_id    = account_id
#         self.biz_information    = biz_information
#         self.username       = username
#         self.update_time    = update_time

#     def __repr__(self):
#         return '<id {},account_id {},biz_information {},username {},update_time {}>'.format(self.id,self.account_id,self.biz_information,self.username,self.update_time)


class paper_lesstransactionPDF(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_transactionPDF"

    transactionId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    hash_pdf = db.Column(db.String)
    timelast = db.Column(db.TIMESTAMP(timezone=True))

    def __init__(self, username, hash_pdf,timelast):
        self.username    = username
        self.hash_pdf    = hash_pdf
        self.timelast       = timelast

    def __repr__(self):
        return '<transactionId {},username {},hash_pdf {},timelast {}>'.format(self.transactionId,self.username,self.hash_pdf,self.timelast)

# class paper_lesstransactionPDF(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_transactionPDF"

#     transactionId = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String)
#     hash_pdf = db.Column(db.String)
#     timelast = db.Column(db.TIMESTAMP(timezone=True))

#     def __init__(self, username, hash_pdf,timelast):
#         self.username    = username
#         self.hash_pdf    = hash_pdf
#         self.timelast       = timelast

#     def __repr__(self):
#         return '<transactionId {},username {},hash_pdf {},timelast {}>'.format(self.transactionId,self.username,self.hash_pdf,self.timelast)



class paper_lessbizProfile(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_bizProfile"

    transactionId = db.Column(db.Integer, primary_key=True)
    bizTax = db.Column(db.String)
    bizInfoJson = db.Column(db.String)
    bizRole = db.Column(db.String)

    def __init__(self, bizTax, bizInfoJson,bizRole):
        self.bizTax    = bizTax
        self.bizInfoJson    = bizInfoJson
        self.bizRole       = bizRole

    def __repr__(self):
        return '<transactionId {},bizTax {},bizInfoJson {},bizRole {}>'.format(self.transactionId,self.bizTax,self.bizInfoJson,self.bizRole)

# class paper_lessbizProfile(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_bizProfile"

#     transactionId = db.Column(db.Integer, primary_key=True)
#     bizTax = db.Column(db.String)
#     bizInfoJson = db.Column(db.String)
#     bizRole = db.Column(db.String)

#     def __init__(self, bizTax, bizInfoJson,bizRole):
#         self.bizTax    = bizTax
#         self.bizInfoJson    = bizInfoJson
#         self.bizRole       = bizRole

#     def __repr__(self):
#         return '<transactionId {},bizTax {},bizInfoJson {},bizRole {}>'.format(self.transactionId,self.bizTax,self.bizInfoJson,self.bizRole)

class paper_lesstoken_required(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_token_required"

    id = db.Column(db.Integer, primary_key=True)
    hash_one_access_token = db.Column(db.String)
    updatetime = db.Column(db.TIMESTAMP(timezone=True))
    access_token_system = db.Column(db.String)
    username = db.Column(db.String)
    email_thai = db.Column(db.String)
    expire_datetime = db.Column(db.TIMESTAMP(timezone=True))
    status_online = db.Column(db.String)

    def __init__(self, hash_one_access_token, updatetime,access_token_system,username,email_thai,expire_datetime,status_online):
        self.hash_one_access_token    = hash_one_access_token
        self.updatetime    = updatetime
        self.access_token_system = access_token_system
        self.username = username
        self.email_thai = email_thai
        self.expire_datetime = expire_datetime
        self.status_online = status_online

    def __repr__(self):
        return '<id {},hash_one_access_token {},updatetime {},access_token_system {},username {},email_thai {},expire_datetime {},status_online {}>'.format(self.id,self.hash_one_access_token,self.updatetime,self.access_token_system,self.username,self.email_thai,self.expire_datetime,self.status_online)

# class paper_lesstoken_required(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_token_required"

#     id = db.Column(db.Integer, primary_key=True)
#     hash_one_access_token = db.Column(db.String)
#     updatetime = db.Column(db.TIMESTAMP(timezone=True))
#     access_token_system = db.Column(db.String)
#     username = db.Column(db.String)
#     email_thai = db.Column(db.String)
#     expire_datetime = db.Column(db.TIMESTAMP(timezone=True))
#     status_online = db.Column(db.String)

#     def __init__(self, hash_one_access_token, updatetime,access_token_system,username,email_thai,expire_datetime,status_online):
#         self.hash_one_access_token    = hash_one_access_token
#         self.updatetime    = updatetime
#         self.access_token_system = access_token_system
#         self.username = username
#         self.email_thai = email_thai
#         self.expire_datetime = expire_datetime
#         self.status_online = status_online

#     def __repr__(self):
#         return '<id {},hash_one_access_token {},updatetime {},access_token_system {},username {},email_thai {},expire_datetime {},status_online {}>'.format(self.id,self.hash_one_access_token,self.updatetime,self.access_token_system,self.username,self.email_thai,self.expire_datetime,self.status_online)


class paper_lesstransactionLoad(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_transactionLoad"

    transactionId = db.Column(db.Integer, primary_key=True)
    sidCode = db.Column(db.String)
    count_download = db.Column(db.String)
    jsonInformation = db.Column(db.String)
    key_gen = db.Column(db.String)

    def __init__(self, sidCode, count_download,jsonInformation,key_gen):
        self.sidCode    = sidCode
        self.count_download    = count_download
        self.jsonInformation = jsonInformation
        self.key_gen = key_gen

    def __repr__(self):
        return '<transactionId {},sidCode {},count_download {},jsonInformation {},key_gen {}>'.format(self.transactionId,self.sidCode,self.count_download,self.jsonInformation,self.key_gen)

# class paper_lesstransactionLoad(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_transactionLoad"

#     transactionId = db.Column(db.Integer, primary_key=True)
#     sidCode = db.Column(db.String)
#     count_download = db.Column(db.String)
#     jsonInformation = db.Column(db.String)
#     key_gen = db.Column(db.String)

#     def __init__(self, sidCode, count_download,jsonInformation,key_gen):
#         self.sidCode    = sidCode
#         self.count_download    = count_download
#         self.jsonInformation = jsonInformation
#         self.key_gen = key_gen

#     def __repr__(self):
#         return '<transactionId {},sidCode {},count_download {},jsonInformation {},key_gen {}>'.format(self.transactionId,self.sidCode,self.count_download,self.jsonInformation,self.key_gen)


class paper_lesstransactionLoadQr(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_transactionLoadQr"

    transactionId = db.Column(db.Integer, primary_key=True)
    sidCode = db.Column(db.String)
    count_download = db.Column(db.String)
    jsonInformation = db.Column(db.String)
    key_gen = db.Column(db.String)

    def __init__(self, sidCode, count_download,jsonInformation,key_gen):
        self.sidCode    = sidCode
        self.count_download    = count_download
        self.jsonInformation = jsonInformation
        self.key_gen = key_gen

    def __repr__(self):
        return '<transactionId {},sidCode {},count_download {},jsonInformation {},key_gen {}>'.format(self.transactionId,self.sidCode,self.count_download,self.jsonInformation,self.key_gen)

# class paper_lesstransactionLoadQr(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_transactionLoadQr"

#     transactionId = db.Column(db.Integer, primary_key=True)
#     sidCode = db.Column(db.String)
#     count_download = db.Column(db.String)
#     jsonInformation = db.Column(db.String)
#     key_gen = db.Column(db.String)

#     def __init__(self, sidCode, count_download,jsonInformation,key_gen):
#         self.sidCode    = sidCode
#         self.count_download    = count_download
#         self.jsonInformation = jsonInformation
#         self.key_gen = key_gen

#     def __repr__(self):
#         return '<transactionId {},sidCode {},count_download {},jsonInformation {},key_gen {}>'.format(self.transactionId,self.sidCode,self.count_download,self.jsonInformation,self.key_gen)


class paper_lesstransactionQrCode(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_transactionQrCode"

    transactionId = db.Column(db.Integer, primary_key=True)
    sidCode = db.Column(db.String)
    qrCode_base64 = db.Column(db.String)
    qrCode_hash = db.Column(db.String)
    pdfqr_base64 = db.Column(db.String)
    pdfqr_hash = db.Column(db.String)
    qrCode_position = db.Column(db.String)
    qrCode_datetime = db.Column(db.TIMESTAMP(timezone=True))

    def __init__(self, sidCode, qrCode_base64,qrCode_hash,pdfqr_base64,pdfqr_hash,qrCode_position,qrCode_datetime):
        self.sidCode    = sidCode
        self.qrCode_base64    = qrCode_base64
        self.qrCode_hash = qrCode_hash
        self.pdfqr_base64 = pdfqr_base64
        self.pdfqr_hash = pdfqr_hash
        self.qrCode_position = qrCode_position
        self.qrCode_datetime = qrCode_datetime

    def __repr__(self):
        return '<transactionId {},sidCode {},qrCode_base64 {},qrCode_hash {},pdfqr_base64 {},pdfqr_hash {},qrCode_position {},qrCode_datetime {}>'.format(self.transactionId,self.sidCode,self.qrCode_base64,self.qrCode_hash,self.pdfqr_base64,self.pdfqr_hash,self.qrCode_position,self.qrCode_datetime)

# class paper_lesstransactionQrCode(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_transactionQrCode"

#     transactionId = db.Column(db.Integer, primary_key=True)
#     sidCode = db.Column(db.String)
#     qrCode_base64 = db.Column(db.String)
#     qrCode_hash = db.Column(db.String)
#     pdfqr_base64 = db.Column(db.String)
#     pdfqr_hash = db.Column(db.String)
#     qrCode_position = db.Column(db.String)
#     qrCode_datetime = db.Column(db.TIMESTAMP(timezone=True))

#     def __init__(self, sidCode, qrCode_base64,qrCode_hash,pdfqr_base64,pdfqr_hash,qrCode_position,qrCode_datetime):
#         self.sidCode    = sidCode
#         self.qrCode_base64    = qrCode_base64
#         self.qrCode_hash = qrCode_hash
#         self.pdfqr_base64 = pdfqr_base64
#         self.pdfqr_hash = pdfqr_hash
#         self.qrCode_position = qrCode_position
#         self.qrCode_datetime = qrCode_datetime

#     def __repr__(self):
#         return '<transactionId {},sidCode {},qrCode_base64 {},qrCode_hash {},pdfqr_base64 {},pdfqr_hash {},qrCode_position {},qrCode_datetime {}>'.format(self.transactionId,self.sidCode,self.qrCode_base64,self.qrCode_hash,self.pdfqr_base64,self.pdfqr_hash,self.qrCode_position,self.qrCode_datetime)


class paper_lessdocument_detail(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_document_detail"

    id = db.Column(db.Integer, primary_key=True)
    documentJson = db.Column(db.String)
    documentUser = db.Column(db.String)
    documentUpdate = db.Column(db.TIMESTAMP(timezone=True))
    documentStatus = db.Column(db.String)
    email = db.Column(db.String)
    documentType = db.Column(db.String)
    documentCode = db.Column(db.String)
    biz_info = db.Column(db.String)
    service_permission = db.Column(db.String)
    other_service_permission = db.Column(db.String)
    chat_bot = db.Column(db.String)

    def __init__(self, documentJson, documentUser,documentUpdate,documentStatus,email,documentType,documentCode,biz_info,service_permission,other_service_permission,chat_bot):
        self.documentJson    = documentJson
        self.documentUser    = documentUser
        self.documentUpdate = documentUpdate
        self.documentStatus = documentStatus
        self.email = email
        self.documentType = documentType
        self.documentCode = documentCode
        self.biz_info = biz_info
        self.service_permission = service_permission
        self.other_service_permission = other_service_permission
        self.chat_bot = chat_bot

    def __repr__(self):
        return '<id {},documentJson {},documentUser {},documentUpdate {},documentStatus {},email {},documentType {},documentCode {},biz_info {},service_permission {},other_service_permission {},chat_bot {}>'.format(self.id,self.documentJson,self.documentUser,self.documentUpdate,self.documentStatus,self.email,self.documentType,self.documentCode,self.biz_info,self.service_permission,self.other_service_permission,self.chat_bot)

# class paper_lessdocument_detail(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_document_detail"

#     id = db.Column(db.Integer, primary_key=True)
#     documentJson = db.Column(db.String)
#     documentUser = db.Column(db.String)
#     documentUpdate = db.Column(db.TIMESTAMP(timezone=True))
#     documentStatus = db.Column(db.String)
#     email = db.Column(db.String)
#     documentType = db.Column(db.String)
#     documentCode = db.Column(db.String)
#     biz_info = db.Column(db.String)
#     service_permission = db.Column(db.String)
#     other_service_permission = db.Column(db.String)
#     chat_bot = db.Column(db.String)

#     def __init__(self, documentJson, documentUser,documentUpdate,documentStatus,email,documentType,documentCode,biz_info,service_permission,other_service_permission,chat_bot):
#         self.documentJson    = documentJson
#         self.documentUser    = documentUser
#         self.documentUpdate = documentUpdate
#         self.documentStatus = documentStatus
#         self.email = email
#         self.documentType = documentType
#         self.documentCode = documentCode
#         self.biz_info = biz_info
#         self.service_permission = service_permission
#         self.other_service_permission = other_service_permission
#         self.chat_bot = chat_bot

#     def __repr__(self):
#         return '<id {},documentJson {},documentUser {},documentUpdate {},documentStatus {},email {},documentType {},documentCode {},biz_info {},service_permission {},other_service_permission {},chat_bot {}>'.format(self.id,self.documentJson,self.documentUser,self.documentUpdate,self.documentStatus,self.email,self.documentType,self.documentCode,self.biz_info,self.service_permission,self.other_service_permission,self.chat_bot)


class paper_lesstransactionfile(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_transactionfile"

    uid = db.Column(db.Integer, primary_key=True)
    json_data = db.Column(db.String)
    pathfolder = db.Column(db.String)
    folder_name = db.Column(db.String)
    attempted_id = db.Column(db.String)
    timeupdate = db.Column(db.TIMESTAMP(timezone=True))
    storage = db.Column(db.String)

    def __init__(self, json_data, pathfolder,folder_name,attempted_id,timeupdate,storage):
        self.json_data    = json_data
        self.pathfolder    = pathfolder
        self.folder_name = folder_name
        self.attempted_id = attempted_id
        self.timeupdate = timeupdate
        self.storage = storage

    def __repr__(self):
        return '<uid {},json_data {},pathfolder {},folder_name {},attempted_id {},timeupdate {},storage {}>'.format(self.uid,self.json_data,self.pathfolder,self.folder_name,self.attempted_id,self.timeupdate,self.storage)

# class paper_lesstransactionfile(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_transactionfile"

#     uid = db.Column(db.Integer, primary_key=True)
#     json_data = db.Column(db.String)
#     pathfolder = db.Column(db.String)
#     folder_name = db.Column(db.String)
#     attempted_id = db.Column(db.String)
#     timeupdate = db.Column(db.TIMESTAMP(timezone=True))
#     storage = db.Column(db.String)

#     def __init__(self, json_data, pathfolder,folder_name,attempted_id,timeupdate,storage):
#         self.json_data    = json_data
#         self.pathfolder    = pathfolder
#         self.folder_name = folder_name
#         self.attempted_id = attempted_id
#         self.timeupdate = timeupdate
#         self.storage = storage

#     def __repr__(self):
#         return '<uid {},json_data {},pathfolder {},folder_name {},attempted_id {},timeupdate {},storage {}>'.format(self.uid,self.json_data,self.pathfolder,self.folder_name,self.attempted_id,self.timeupdate,self.storage)


class paper_lesstransactionTask(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_transactionTaskChat"

    task_id = db.Column(db.Integer, primary_key=True)
    task_project_id = db.Column(db.String)
    task_sidCode = db.Column(db.String)
    task_uid = db.Column(db.String)
    task_state_id = db.Column(db.String)
    task_state_name = db.Column(db.String)
    task_timeupdate = db.Column(db.TIMESTAMP(timezone=True))
    task_order = db.Column(db.String)
    task_stepnum = db.Column(db.String)
    task_emailUser = db.Column(db.String)
    task_status = db.Column(db.String)
    task_sendChat = db.Column(db.String)
    task_message = db.Column(db.String)

    def __init__(self, task_project_id, task_sidCode,task_uid,task_state_id,task_state_name,task_timeupdate,task_order,task_stepnum,task_emailUser,task_status,task_sendChat,task_message):
        self.task_project_id    = task_project_id
        self.task_sidCode    = task_sidCode
        self.task_uid = task_uid
        self.task_state_id = task_state_id
        self.task_state_name = task_state_name
        self.task_timeupdate = task_timeupdate
        self.task_order = task_order
        self.task_stepnum = task_stepnum
        self.task_emailUser = task_emailUser
        self.task_status = task_status
        self.task_sendChat = task_sendChat
        self.task_message = task_message

    def __repr__(self):
        return '<task_id {},task_project_id {},task_sidCode {},task_uid {},task_state_id {},task_state_name {},task_timeupdate {},task_order {},task_stepnum {},task_emailUser {},task_status {},task_sendChat {},task_message {}>'.format(self.task_id,self.task_project_id,self.task_sidCode,self.task_uid,self.task_state_id,self.task_state_name,self.task_timeupdate,self.task_order,self.task_stepnum,self.task_emailUser,self.task_status,self.task_sendChat,self.task_message)

# class paper_lesstransactionTask(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_transactionTaskChat"

#     task_id = db.Column(db.Integer, primary_key=True)
#     task_project_id = db.Column(db.String)
#     task_sidCode = db.Column(db.String)
#     task_uid = db.Column(db.String)
#     task_state_id = db.Column(db.String)
#     task_state_name = db.Column(db.String)
#     task_timeupdate = db.Column(db.TIMESTAMP(timezone=True))
#     task_order = db.Column(db.String)
#     task_stepnum = db.Column(db.String)
#     task_emailUser = db.Column(db.String)
#     task_status = db.Column(db.String)
#     task_sendChat = db.Column(db.String)
#     task_message = db.Column(db.String)

#     def __init__(self, task_project_id, task_sidCode,task_uid,task_state_id,task_state_name,task_timeupdate,task_order,task_stepnum,task_emailUser,task_status,task_sendChat,task_message):
#         self.task_project_id    = task_project_id
#         self.task_sidCode    = task_sidCode
#         self.task_uid = task_uid
#         self.task_state_id = task_state_id
#         self.task_state_name = task_state_name
#         self.task_timeupdate = task_timeupdate
#         self.task_order = task_order
#         self.task_stepnum = task_stepnum
#         self.task_emailUser = task_emailUser
#         self.task_status = task_status
#         self.task_sendChat = task_sendChat
#         self.task_message = task_message

#     def __repr__(self):
#         return '<task_id {},task_project_id {},task_sidCode {},task_uid {},task_state_id {},task_state_name {},task_timeupdate {},task_order {},task_stepnum {},task_emailUser {},task_status {},task_sendChat {},task_message {}>'.format(self.task_id,self.task_project_id,self.task_sidCode,self.task_uid,self.task_state_id,self.task_state_name,self.task_timeupdate,self.task_order,self.task_stepnum,self.task_emailUser,self.task_status,self.task_sendChat,self.task_message)

class paper_lessnumber_document(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_number_document"

    document_current = db.Column(db.String)
    document_lenght = db.Column(db.String)
    document_type = db.Column(db.String,primary_key=True)

    def __init__(self, document_current, document_lenght,document_type):
        self.document_current    = document_current
        self.document_lenght    = document_lenght
        self.document_type = document_type

    def __repr__(self):
        return '<document_current {},document_lenght {},document_type {}>'.format(self.document_current,self.document_lenght,self.document_type)

# class paper_lessnumber_document(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_number_document"

#     document_current = db.Column(db.String)
#     document_lenght = db.Column(db.String)
#     document_type = db.Column(db.String,primary_key=True)

#     def __init__(self, document_current, document_lenght,document_type):
#         self.document_current    = document_current
#         self.document_lenght    = document_lenght
#         self.document_type = document_type

#     def __repr__(self):
#         return '<document_current {},document_lenght {},document_type {}>'.format(self.document_current,self.document_lenght,self.document_type)

class paper_lessaction_status(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_action_status"

    name_action = db.Column(db.String,primary_key=True)
    status = db.Column(db.String)

    def __init__(self, name_action, status):
        self.name_action    = name_action
        self.status    = status

    def __repr__(self):
        return '<name_action {},status {}>'.format(self.name_action,self.status)

# class paper_lessaction_status(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_action_status"

#     name_action = db.Column(db.String,primary_key=True)
#     status = db.Column(db.String)

#     def __init__(self, name_action, status):
#         self.name_action    = name_action
#         self.status    = status

#     def __repr__(self):
#         return '<name_action {},status {}>'.format(self.name_action,self.status)

class paper_lessbizPaperless(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_bizPaperless"

    id = db.Column(db.Integer, primary_key=True)
    tax_id = db.Column(db.String)
    theme_color = db.Column(db.String)
    path_logo = db.Column(db.String)
    datetime = db.Column(db.TIMESTAMP(timezone=True))

    def __init__(self, tax_id,theme_color,path_logo,datetime):
        self.tax_id   = tax_id
        self.theme_color = theme_color
        self.path_logo = path_logo
        self.datetime = datetime

    def __repr__(self):
        return '<id {},tax_id {},theme_color {},path_logo {},datetime {}>'.format(self.id,self.tax_id,self.theme_color,self.path_logo,self.datetime)

# class paper_lessbizPaperless(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_bizPaperless"

#     id = db.Column(db.Integer, primary_key=True)
#     tax_id = db.Column(db.String)
#     theme_color = db.Column(db.String)
#     path_logo = db.Column(db.String)
#     datetime = db.Column(db.TIMESTAMP(timezone=True))

#     def __init__(self, tax_id,theme_color,path_logo,datetime):
#         self.tax_id   = tax_id
#         self.theme_color = theme_color
#         self.path_logo = path_logo
#         self.datetime = datetime

#     def __repr__(self):
#         return '<id {},tax_id {},theme_color {},path_logo {},datetime {}>'.format(self.id,self.tax_id,self.theme_color,self.path_logo,self.datetime)

class tb_transactionlogrequest(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_transactionlogrequest"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    statuscode = db.Column(db.String)
    datetime = db.Column(db.TIMESTAMP(timezone=True))
    request = db.Column(db.String)
    url_request = db.Column(db.String)
    methods = db.Column(db.String)
    hash_token = db.Column(db.String)

    def __init__(self, message,statuscode,datetime,request,url_request,methods,hash_token):
        self.message   = message
        self.statuscode = statuscode
        self.datetime = datetime
        self.request = request
        self.url_request = url_request
        self.methods = methods
        self.hash_token = hash_token

    def __repr__(self):
        return '<id {},message {},statuscode {},datetime {},request {},url_request {},methods {},hash_token {}>'.format(self.id,self.message,self.statuscode,self.datetime,self.request,self.url_request,self.methods,self.hash_token)

# class tb_transactionlogrequest(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_transactionlogrequest"

#     id = db.Column(db.Integer, primary_key=True)
#     message = db.Column(db.String)
#     statuscode = db.Column(db.String)
#     datetime = db.Column(db.TIMESTAMP(timezone=True))
#     request = db.Column(db.String)
#     url_request = db.Column(db.String)
#     methods = db.Column(db.String)
#     hash_token = db.Column(db.String)

#     def __init__(self, message,statuscode,datetime,request,url_request,methods,hash_token):
#         self.message   = message
#         self.statuscode = statuscode
#         self.datetime = datetime
#         self.request = request
#         self.url_request = url_request
#         self.methods = methods
#         self.hash_token = hash_token

#     def __repr__(self):
#         return '<id {},message {},statuscode {},datetime {},request {},url_request {},methods {},hash_token {}>'.format(self.id,self.message,self.statuscode,self.datetime,self.request,self.url_request,self.methods,self.hash_token)


class tb_transactionexcel(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_transactionexcel"

    id = db.Column(db.Integer, primary_key=True)
    path_excel = db.Column(db.String)
    name_excel = db.Column(db.String)
    key_download = db.Column(db.String)
    datetime = db.Column(db.TIMESTAMP(timezone=True))
    username = db.Column(db.String)
    filter_key = db.Column(db.String)

    def __init__(self, path_excel,name_excel,key_download,datetime,username,filter_key):
        self.path_excel   = path_excel
        self.name_excel = name_excel
        self.key_download = key_download
        self.datetime = datetime
        self.username = username
        self.filter_key = filter_key

    def __repr__(self):
        return '<id {},path_excel {},name_excel {},key_download {},datetime {},username {},filter_key {}>'.format(self.id,self.path_excel,self.name_excel,self.key_download,self.datetime,self.username,self.filter_key)

# class tb_transactionexcel(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_transactionexcel"

#     id = db.Column(db.Integer, primary_key=True)
#     path_excel = db.Column(db.String)
#     name_excel = db.Column(db.String)
#     key_download = db.Column(db.String)
#     datetime = db.Column(db.TIMESTAMP(timezone=True))
#     username = db.Column(db.String)
#     filter_key = db.Column(db.String)

#     def __init__(self, path_excel,name_excel,key_download,datetime,username,filter_key):
#         self.path_excel   = path_excel
#         self.name_excel = name_excel
#         self.key_download = key_download
#         self.datetime = datetime
#         self.username = username
#         self.filter_key = filter_key

#     def __repr__(self):
#         return '<id {},path_excel {},name_excel {},key_download {},datetime {},username {},filter_key {}>'.format(self.id,self.path_excel,self.name_excel,self.key_download,self.datetime,self.username,self.filter_key)

class tb_transactionlog(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_transactionlog"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    status = db.Column(db.String)
    request = db.Column(db.String)
    datetime = db.Column(db.TIMESTAMP(timezone=True))
    url = db.Column(db.String)
    hash_token = db.Column(db.String)
    time = db.Column(db.String)

    def __init__(self, message,status,request,datetime,url,hash_token,time):
        self.message   = message
        self.status = status
        self.request = request
        self.datetime = datetime
        self.url = url
        self.hash_token = hash_token
        self.time = time

    def __repr__(self):
        return '<id {},message {},status {},request {},datetime {},url {},hash_token {},time {}>'.format(self.id,self.message,self.status,self.request,self.datetime,self.url,self.hash_token,self.time)

# class tb_transactionlog(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_transactionlog"

#     id = db.Column(db.Integer, primary_key=True)
#     message = db.Column(db.String)
#     status = db.Column(db.String)
#     request = db.Column(db.String)
#     datetime = db.Column(db.TIMESTAMP(timezone=True))
#     url = db.Column(db.String)
#     hash_token = db.Column(db.String)
#     time = db.Column(db.String)

#     def __init__(self, message,status,request,datetime,url,hash_token,time):
#         self.message   = message
#         self.status = status
#         self.request = request
#         self.datetime = datetime
#         self.url = url
#         self.hash_token = hash_token
#         self.time = time

#     def __repr__(self):
#         return '<id {},message {},status {},request {},datetime {},url {},hash_token {},time {}>'.format(self.id,self.message,self.status,self.request,self.datetime,self.url,self.hash_token,self.time)


class tb_transaction_servicelog(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_transaction_servicelog"

    id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String)
    status = db.Column(db.String)
    sidcode = db.Column(db.String)
    message_error = db.Column(db.String)
    datetime = db.Column(db.TIMESTAMP(timezone=True))
    hash_token = db.Column(db.String)


    def __init__(self, service_type,status,sidcode,message_error,datetime,hash_token):
        self.service_type   = service_type
        self.status = status
        self.sidcode = sidcode
        self.message_error = message_error
        self.datetime = datetime
        self.hash_token = hash_token

    def __repr__(self):
        return '<id {},service_type {},status {},sidcode {},message_error {},datetime {},hash_token {}>'.format(self.id,self.service_type,self.status,self.sidcode,self.message_error,self.datetime,self.hash_token)

# class tb_transaction_servicelog(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_transaction_servicelog"

#     id = db.Column(db.Integer, primary_key=True)
#     service_type = db.Column(db.String)
#     status = db.Column(db.String)
#     sidcode = db.Column(db.String)
#     message_error = db.Column(db.String)
#     datetime = db.Column(db.TIMESTAMP(timezone=True))
#     hash_token = db.Column(db.String)


#     def __init__(self, service_type,status,sidcode,message_error,datetime,hash_token):
#         self.service_type   = service_type
#         self.status = status
#         self.sidcode = sidcode
#         self.message_error = message_error
#         self.datetime = datetime
#         self.hash_token = hash_token

#     def __repr__(self):
#         return '<id {},service_type {},status {},sidcode {},message_error {},datetime {},hash_token {}>'.format(self.id,self.service_type,self.status,self.sidcode,self.message_error,self.datetime,self.hash_token)

class tb_loger_error(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_loger_error"

    id = db.Column(db.Integer, primary_key=True)
    message_error = db.Column(db.String)
    url = db.Column(db.String)
    datetime = db.Column(db.TIMESTAMP(timezone=True))


    def __init__(self, message_error,url,datetime):
        self.message_error   = message_error
        self.url = url
        self.datetime = datetime

    def __repr__(self):
        return '<id {},message_error {},url {},datetime {}>'.format(self.id,self.message_error,self.url,self.datetime)

# class tb_loger_error(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_loger_error"

#     id = db.Column(db.Integer, primary_key=True)
#     message_error = db.Column(db.String)
#     url = db.Column(db.String)
#     datetime = db.Column(db.TIMESTAMP(timezone=True))


#     def __init__(self, message_error,url,datetime):
#         self.message_error   = message_error
#         self.url = url
#         self.datetime = datetime

#     def __repr__(self):
#         return '<id {},message_error {},url {},datetime {}>'.format(self.id,self.message_error,self.url,self.datetime)

class tb_register_business(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_register_business"

    id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.String)
    taxid = db.Column(db.String)
    all_data = db.Column(db.String)
    approve_document = db.Column(db.String)
    result_document = db.Column(db.String)
    register_date = db.Column(db.TIMESTAMP(timezone=True))
    first_name_th = db.Column(db.String)
    first_name_eng = db.Column(db.String)
    porpor20_document = db.Column(db.String)


    def __init__(self, citizen_id,taxid,all_data,approve_document,result_document,register_date,first_name_th,first_name_eng,porpor20_document):
        self.citizen_id   = citizen_id
        self.taxid = taxid
        self.all_data = all_data
        self.approve_document = approve_document
        self.result_document = result_document
        self.register_date = register_date
        self.first_name_th = first_name_th
        self.first_name_eng = first_name_eng
        self.porpor20_document = porpor20_document

    def __repr__(self):
        return '<id {},citizen_id {},taxid {},all_data {},approve_document {},result_document {},register_date {},first_name_th {},first_name_eng {},porpor20_document {}>'.format(self.id,self.citizen_id,self.taxid,self.all_data,self.approve_document,self.result_document,self.register_date,self.first_name_th,self.first_name_eng,self.porpor20_document)

# class tb_register_business(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_register_business"

#     id = db.Column(db.Integer, primary_key=True)
#     citizen_id = db.Column(db.String)
#     taxid = db.Column(db.String)
#     all_data = db.Column(db.String)
#     approve_document = db.Column(db.String)
#     result_document = db.Column(db.String)
#     register_date = db.Column(db.TIMESTAMP(timezone=True))
#     first_name_th = db.Column(db.String)
#     first_name_eng = db.Column(db.String)
#     porpor20_document = db.Column(db.String)


#     def __init__(self, citizen_id,taxid,all_data,approve_document,result_document,register_date,first_name_th,first_name_eng,porpor20_document):
#         self.citizen_id   = citizen_id
#         self.taxid = taxid
#         self.all_data = all_data
#         self.approve_document = approve_document
#         self.result_document = result_document
#         self.register_date = register_date
#         self.first_name_th = first_name_th
#         self.first_name_eng = first_name_eng
#         self.porpor20_document = porpor20_document

#     def __repr__(self):
#         return '<id {},citizen_id {},taxid {},all_data {},approve_document {},result_document {},register_date {},first_name_th {},first_name_eng {},porpor20_document {}>'.format(self.id,self.citizen_id,self.taxid,self.all_data,self.approve_document,self.result_document,self.register_date,self.first_name_th,self.first_name_eng,self.porpor20_document)

class tb_register(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_register"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String)
    account_title_th = db.Column(db.String)
    first_name_th = db.Column(db.String)
    last_name_th = db.Column(db.String)
    account_title_eng = db.Column(db.String)
    first_name_eng = db.Column(db.String)
    last_name_eng = db.Column(db.String)
    id_card_type = db.Column(db.String)
    id_card_num = db.Column(db.String)
    email = db.Column(db.String)
    mobile_no = db.Column(db.String)
    birth_date = db.Column(db.TIMESTAMP(timezone=True))
    username = db.Column(db.String)
    account_email = db.Column(db.String)
    register_date = db.Column(db.TIMESTAMP(timezone=True))


    def __init__(self, account_id,account_title_th,first_name_th,last_name_th,account_title_eng,first_name_eng,last_name_eng,id_card_type,id_card_num,email,mobile_no,birth_date,username,account_email,register_date):
        self.account_id   = account_id
        self.account_title_th = account_title_th
        self.first_name_th = first_name_th
        self.last_name_th = last_name_th
        self.account_title_eng = account_title_eng
        self.first_name_eng = first_name_eng
        self.last_name_eng = last_name_eng
        self.id_card_type = id_card_type
        self.id_card_num = id_card_num
        self.email = email
        self.mobile_no = mobile_no
        self.birth_date = birth_date
        self.username = username
        self.account_email = account_email
        self.register_date = register_date

    def __repr__(self):
        return '<id {},account_id {},account_title_th {},first_name_th {},last_name_th {},account_title_eng {},first_name_eng {},last_name_eng {},id_card_type {},id_card_num {},email {},mobile_no {},birth_date {},username {},account_email {},register_date {}>'\
            .format(self.id,self.account_id,self.account_title_th,self.first_name_th,self.last_name_th,self.account_title_eng,self.first_name_eng,self.last_name_eng,self.id_card_type,self.id_card_num,self.email,self.mobile_no,self.birth_date,self.username,self.account_email,self.register_date)

# class tb_register(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_register"

#     id = db.Column(db.Integer, primary_key=True)
#     account_id = db.Column(db.String)
#     account_title_th = db.Column(db.String)
#     first_name_th = db.Column(db.String)
#     last_name_th = db.Column(db.String)
#     account_title_eng = db.Column(db.String)
#     first_name_eng = db.Column(db.String)
#     last_name_eng = db.Column(db.String)
#     id_card_type = db.Column(db.String)
#     id_card_num = db.Column(db.String)
#     email = db.Column(db.String)
#     mobile_no = db.Column(db.String)
#     birth_date = db.Column(db.TIMESTAMP(timezone=True))
#     username = db.Column(db.String)
#     account_email = db.Column(db.String)
#     register_date = db.Column(db.TIMESTAMP(timezone=True))


#     def __init__(self, account_id,account_title_th,first_name_th,last_name_th,account_title_eng,first_name_eng,last_name_eng,id_card_type,id_card_num,email,mobile_no,birth_date,username,account_email,register_date):
#         self.account_id   = account_id
#         self.account_title_th = account_title_th
#         self.first_name_th = first_name_th
#         self.last_name_th = last_name_th
#         self.account_title_eng = account_title_eng
#         self.first_name_eng = first_name_eng
#         self.last_name_eng = last_name_eng
#         self.id_card_type = id_card_type
#         self.id_card_num = id_card_num
#         self.email = email
#         self.mobile_no = mobile_no
#         self.birth_date = birth_date
#         self.username = username
#         self.account_email = account_email
#         self.register_date = register_date

#     def __repr__(self):
#         return '<id {},account_id {},account_title_th {},first_name_th {},last_name_th {},account_title_eng {},first_name_eng {},last_name_eng {},id_card_type {},id_card_num {},email {},mobile_no {},birth_date {},username {},account_email {},register_date {}>'\
#             .format(self.id,self.account_id,self.account_title_th,self.first_name_th,self.last_name_th,self.account_title_eng,self.first_name_eng,self.last_name_eng,self.id_card_type,self.id_card_num,self.email,self.mobile_no,self.birth_date,self.username,self.account_email,self.register_date)

class view_document(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "view_document"

    doc_id = db.Column(db.Integer, primary_key=True)
    step_data_sid = db.Column(db.String)
    tracking_id = db.Column(db.String)
    file_name = db.Column(db.String)
    send_time = db.Column(db.TIMESTAMP(timezone=True))
    sender_name = db.Column(db.String)
    sender_email = db.Column(db.String)
    data_json = db.Column(db.String)
    string_pdf = db.Column(db.String)
    string_sign = db.Column(db.String)
    fid = db.Column(db.String)
    documentType = db.Column(db.String)
    documentJson = db.Column(db.String)
    digit_sign = db.Column(db.String)
    urgent_type = db.Column(db.String)
    options_page = db.Column(db.String)
    sign_page_options = db.Column(db.String)
    recipient_email = db.Column(db.String)
    email_center = db.Column(db.String)
    attempted_folder = db.Column(db.String)
    biz_info = db.Column(db.String)
    step_Name = db.Column(db.String)
    documentDetails = db.Column(db.String)
    condition_temp = db.Column(db.String)
    step_Code = db.Column(db.String)
    status = db.Column(db.String)
    status_details = db.Column(db.String)
    document_status = db.Column(db.String)
    pdf_rejectorcancle = db.Column(db.String)
    update_time = db.Column(db.TIMESTAMP(timezone=True))



    def __init__(self, doc_id,step_data_sid,tracking_id,file_name,send_time,sender_name,sender_email,data_json,string_pdf,string_sign,fid,documentType,documentJson,digit_sign,urgent_type,options_page,sign_page_options,recipient_email,email_center,attempted_folder,biz_info,step_Name,documentDetails,condition_temp,step_Code,status,status_details,document_status,pdf_rejectorcancle,update_time):
        self.doc_id   = doc_id
        self.step_data_sid = step_data_sid
        self.tracking_id = tracking_id
        self.file_name = file_name
        self.send_time = send_time
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.data_json = data_json
        self.string_pdf = string_pdf
        self.string_sign = string_sign
        self.fid = fid
        self.documentType = documentType
        self.documentJson = documentJson
        self.digit_sign = digit_sign
        self.urgent_type = urgent_type
        self.options_page = options_page
        self.sign_page_options = sign_page_options
        self.recipient_email = recipient_email
        self.email_center = email_center
        self.attempted_folder = attempted_folder
        self.biz_info = biz_info
        self.step_Name = step_Name
        self.documentDetails = documentDetails
        self.condition_temp = condition_temp
        self.step_Code = step_Code
        self.status = status
        self.status_details = status_details
        self.document_status = document_status
        self.update_time = update_time
        self.pdf_rejectorcancle = pdf_rejectorcancle


    def __repr__(self):
        return '<doc_id {},step_data_sid {},tracking_id {},file_name {},send_time {},sender_name {},sender_email {},data_json {},string_pdf {},string_sign {},fid {},documentType {},documentJson {},digit_sign {},urgent_type {},options_page {},sign_page_options {},recipient_email {},email_center {},attempted_folder {},biz_info {},step_Name{},documentDetails{},condition_temp{},step_Code{},status{},status_details {},document_status {},update_time {},pdf_rejectorcancle {}>'.format(self.doc_id,self.step_data_sid,self.tracking_id,self.file_name,self.send_time,self.sender_name,self.sender_email,self.data_json,self.string_pdf,self.string_sign,self.fid,self.documentType,self.documentJson,self.digit_sign,self.urgent_type,self.options_page,self.sign_page_options,self.recipient_email,self.email_center,self.attempted_folder,self.biz_info,self.step_Name,self.documentDetails,self.condition_temp,self.step_Code,self.status,self.status_details,self.document_status,self.update_time,self.pdf_rejectorcancle)

# class view_document(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "view_document"

#     doc_id = db.Column(db.Integer, primary_key=True)
#     step_data_sid = db.Column(db.String)
#     tracking_id = db.Column(db.String)
#     file_name = db.Column(db.String)
#     send_time = db.Column(db.TIMESTAMP(timezone=True))
#     sender_name = db.Column(db.String)
#     sender_email = db.Column(db.String)
#     data_json = db.Column(db.String)
#     string_pdf = db.Column(db.String)
#     string_sign = db.Column(db.String)
#     fid = db.Column(db.String)
#     documentType = db.Column(db.String)
#     documentJson = db.Column(db.String)
#     digit_sign = db.Column(db.String)
#     urgent_type = db.Column(db.String)
#     options_page = db.Column(db.String)
#     sign_page_options = db.Column(db.String)
#     recipient_email = db.Column(db.String)
#     email_center = db.Column(db.String)
#     attempted_folder = db.Column(db.String)
#     biz_info = db.Column(db.String)
#     step_Name = db.Column(db.String)
#     documentDetails = db.Column(db.String)
#     condition_temp = db.Column(db.String)
#     step_Code = db.Column(db.String)
#     status = db.Column(db.String)
#     status_details = db.Column(db.String)
#     document_status = db.Column(db.String)
#     pdf_rejectorcancle = db.Column(db.String)
#     update_time = db.Column(db.TIMESTAMP(timezone=True))



#     def __init__(self, doc_id,step_data_sid,tracking_id,file_name,send_time,sender_name,sender_email,data_json,string_pdf,string_sign,fid,documentType,documentJson,digit_sign,urgent_type,options_page,sign_page_options,recipient_email,email_center,attempted_folder,biz_info,step_Name,documentDetails,condition_temp,step_Code,status,status_details,document_status,pdf_rejectorcancle,update_time):
#         self.doc_id   = doc_id
#         self.step_data_sid = step_data_sid
#         self.tracking_id = tracking_id
#         self.file_name = file_name
#         self.send_time = send_time
#         self.sender_name = sender_name
#         self.sender_email = sender_email
#         self.data_json = data_json
#         self.string_pdf = string_pdf
#         self.string_sign = string_sign
#         self.fid = fid
#         self.documentType = documentType
#         self.documentJson = documentJson
#         self.digit_sign = digit_sign
#         self.urgent_type = urgent_type
#         self.options_page = options_page
#         self.sign_page_options = sign_page_options
#         self.recipient_email = recipient_email
#         self.email_center = email_center
#         self.attempted_folder = attempted_folder
#         self.biz_info = biz_info
#         self.step_Name = step_Name
#         self.documentDetails = documentDetails
#         self.condition_temp = condition_temp
#         self.step_Code = step_Code
#         self.status = status
#         self.status_details = status_details
#         self.document_status = document_status
#         self.update_time = update_time
#         self.pdf_rejectorcancle = pdf_rejectorcancle


#     def __repr__(self):
#         return '<doc_id {},step_data_sid {},tracking_id {},file_name {},send_time {},sender_name {},sender_email {},data_json {},string_pdf {},string_sign {},fid {},documentType {},documentJson {},digit_sign {},urgent_type {},options_page {},sign_page_options {},recipient_email {},email_center {},attempted_folder {},biz_info {},step_Name{},documentDetails{},condition_temp{},step_Code{},status{},status_details {},document_status {},update_time {},pdf_rejectorcancle {}>'.format(self.doc_id,self.step_data_sid,self.tracking_id,self.file_name,self.send_time,self.sender_name,self.sender_email,self.data_json,self.string_pdf,self.string_sign,self.fid,self.documentType,self.documentJson,self.digit_sign,self.urgent_type,self.options_page,self.sign_page_options,self.recipient_email,self.email_center,self.attempted_folder,self.biz_info,self.step_Name,self.documentDetails,self.condition_temp,self.step_Code,self.status,self.status_details,self.document_status,self.update_time,self.pdf_rejectorcancle)

class tb_user_admin(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_user_admin"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    hash_data = db.Column(db.String)
    datetime_create = db.Column(db.TIMESTAMP(timezone=True))
    datetime_update = db.Column(db.TIMESTAMP(timezone=True))
    email_user = db.Column(db.String)
    status = db.Column(db.String)
    level_admin = db.Column(db.String)

    def __init__(self,username,hash_data,datetime_create,datetime_update,email_user,status,level_admin):
        self.username = username
        self.hash_data = hash_data
        self.datetime_create = datetime_create
        self.datetime_update = datetime_update
        self.email_user = email_user
        self.status = status
        self.level_admin = level_admin

    def __repr__(self):
        return '<id {}, username {},hash_data {},datetime_create {},datetime_update {},email_user {},status {},level_admin {}>'.format(self.id,self.username,self.hash_data,self.datetime_create,self.datetime_update,self.email_user,self.status,self.level_admin)

# class tb_user_admin(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_user_admin"

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String)
#     hash_data = db.Column(db.String)
#     datetime_create = db.Column(db.TIMESTAMP(timezone=True))
#     datetime_update = db.Column(db.TIMESTAMP(timezone=True))
#     email_user = db.Column(db.String)
#     status = db.Column(db.String)
#     level_admin = db.Column(db.String)

#     def __init__(self,username,hash_data,datetime_create,datetime_update,email_user,status,level_admin):
#         self.username = username
#         self.hash_data = hash_data
#         self.datetime_create = datetime_create
#         self.datetime_update = datetime_update
#         self.email_user = email_user
#         self.status = status
#         self.level_admin = level_admin

#     def __repr__(self):
#         return '<id {}, username {},hash_data {},datetime_create {},datetime_update {},email_user {},status {},level_admin {}>'.format(self.id,self.username,self.hash_data,self.datetime_create,self.datetime_update,self.email_user,self.status,self.level_admin)

class tb_group_document(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_group_document"

    id = db.Column(db.Integer, primary_key=True)
    sid_group = db.Column(db.String)
    data_group = db.Column(db.String)
    updatetime = db.Column(db.TIMESTAMP(timezone=True))
    email_group = db.Column(db.String)
    status = db.Column(db.String)
    create_by = db.Column(db.String)
    update_by = db.Column(db.String)
    step_group = db.Column(db.String)
    pdf_org = db.Column(db.String)
    pdf_sign = db.Column(db.String)
    step_group_detail = db.Column(db.String)
    group_data_json = db.Column(db.String)
    group_other = db.Column(db.String)
    email_view_group = db.Column(db.String)
    hash_id = db.Column(db.String)
    tracking_group = db.Column(db.String)
    status_group = db.Column(db.String)
    group_title = db.Column(db.String)
    group_name = db.Column(db.String)
    document_type = db.Column(db.String)
    bizinfo = db.Column(db.String)
    group_status = db.Column(db.String)
    cover_page = db.Column(db.String)
    calculate_fieds = db.Column(db.String)
    maxstep  = db.Column(db.String)
    email_middle = db.Column(db.String)
    html_data = db.Column(db.String)
    json_data = db.Column(db.String)

    def __init__(self,sid_group,data_group,updatetime,email_group,status,create_by,update_by,step_group,pdf_org,pdf_sign,step_group_detail,group_data_json,group_other,email_view_group,hash_id,tracking_group,status_group,group_title,group_name,document_type,bizinfo,group_status,cover_page,calculate_fieds,maxstep,email_middle,html_data,json_data):
        self.sid_group = sid_group
        self.data_group = data_group
        self.updatetime = updatetime
        self.email_group = email_group
        self.status = status
        self.create_by = create_by
        self.update_by = update_by
        self.step_group = step_group
        self.pdf_org = pdf_org
        self.pdf_sign = pdf_sign
        self.step_group_detail = step_group_detail
        self.group_data_json = group_data_json
        self.group_other = group_other
        self.email_view_group = email_view_group
        self.hash_id = hash_id
        self.tracking_group = tracking_group
        self.status_group = status_group
        self.group_title = group_title
        self.group_name = group_name
        self.document_type = document_type
        self.bizinfo = bizinfo
        self.group_status = group_status
        self.cover_page = cover_page
        self.calculate_fieds = calculate_fieds
        self.maxstep = maxstep
        self.email_middle = email_middle
        self.html_data = html_data
        self.json_data = json_data

    def __repr__(self):
        return '<id {},sid_group {},data_group {},updatetime {},email_group {},status {},create_by {},update_by {},step_group {},pdf_org {},pdf_sign {},step_group_detail {},group_data_json {},group_other {},email_view_group {},hash_id {},tracking_group {},status_group {},group_title {},group_name {},document_type {},bizinfo {},group_status {},cover_page {},calculate_fieds {},maxstep {},email_middle {},html_data {},json_data {}>'.format(self.id,self.sid_group,self.data_group,self.updatetime,self.email_group,self.status,self.create_by,self.update_by,self.step_group,self.pdf_org,self.pdf_sign,self.step_group_detail,self.group_data_json,self.group_other,self.email_view_group,self.hash_id,self.tracking_group,self.status_group,self.group_title,self.group_name,self.document_type,self.bizinfo,self.group_status,self.cover_page,self.calculate_fieds,self.maxstep,self.email_middle,self.html_data,self.json_data)

# class tb_group_document(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_group_document"

#     id = db.Column(db.Integer, primary_key=True)
#     sid_group = db.Column(db.String)
#     data_group = db.Column(db.String)
#     updatetime = db.Column(db.TIMESTAMP(timezone=True))
#     email_group = db.Column(db.String)
#     status = db.Column(db.String)
#     create_by = db.Column(db.String)
#     update_by = db.Column(db.String)
#     step_group = db.Column(db.String)
#     pdf_org = db.Column(db.String)
#     pdf_sign = db.Column(db.String)
#     step_group_detail = db.Column(db.String)
#     group_data_json = db.Column(db.String)
#     group_other = db.Column(db.String)
#     email_view_group = db.Column(db.String)
#     hash_id = db.Column(db.String)
#     tracking_group = db.Column(db.String)
#     status_group = db.Column(db.String)
#     group_title = db.Column(db.String)
#     group_name = db.Column(db.String)
#     document_type = db.Column(db.String)
#     bizinfo = db.Column(db.String)
#     group_status = db.Column(db.String)
#     cover_page = db.Column(db.String)
#     calculate_fieds = db.Column(db.String)
#     maxstep  = db.Column(db.String)
#     email_middle = db.Column(db.String)
#     html_data = db.Column(db.String)
#     json_data = db.Column(db.String)

#     def __init__(self,sid_group,data_group,updatetime,email_group,status,create_by,update_by,step_group,pdf_org,pdf_sign,step_group_detail,group_data_json,group_other,email_view_group,hash_id,tracking_group,status_group,group_title,group_name,document_type,bizinfo,group_status,cover_page,calculate_fieds,maxstep,email_middle,html_data,json_data):
#         self.sid_group = sid_group
#         self.data_group = data_group
#         self.updatetime = updatetime
#         self.email_group = email_group
#         self.status = status
#         self.create_by = create_by
#         self.update_by = update_by
#         self.step_group = step_group
#         self.pdf_org = pdf_org
#         self.pdf_sign = pdf_sign
#         self.step_group_detail = step_group_detail
#         self.group_data_json = group_data_json
#         self.group_other = group_other
#         self.email_view_group = email_view_group
#         self.hash_id = hash_id
#         self.tracking_group = tracking_group
#         self.status_group = status_group
#         self.group_title = group_title
#         self.group_name = group_name
#         self.document_type = document_type
#         self.bizinfo = bizinfo
#         self.group_status = group_status
#         self.cover_page = cover_page
#         self.calculate_fieds = calculate_fieds
#         self.maxstep = maxstep
#         self.email_middle = email_middle
#         self.html_data = html_data
#         self.json_data = json_data

#     def __repr__(self):
#         return '<id {},sid_group {},data_group {},updatetime {},email_group {},status {},create_by {},update_by {},step_group {},pdf_org {},pdf_sign {},step_group_detail {},group_data_json {},group_other {},email_view_group {},hash_id {},tracking_group {},status_group {},group_title {},group_name {},document_type {},bizinfo {},group_status {},cover_page {},calculate_fieds {},maxstep {},email_middle {},html_data {},json_data {}>'.format(self.id,self.sid_group,self.data_group,self.updatetime,self.email_group,self.status,self.create_by,self.update_by,self.step_group,self.pdf_org,self.pdf_sign,self.step_group_detail,self.group_data_json,self.group_other,self.email_view_group,self.hash_id,self.tracking_group,self.status_group,self.group_title,self.group_name,self.document_type,self.bizinfo,self.group_status,self.cover_page,self.calculate_fieds,self.maxstep,self.email_middle,self.html_data,self.json_data)

class tb_group_template(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = "tb_group_template"

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String)
    group_code = db.Column(db.String)
    template = db.Column(db.TIMESTAMP(timezone=True))
    document_type = db.Column(db.String)
    group_title = db.Column(db.String)
    step_group = db.Column(db.String)
    status = db.Column(db.String)
    create_date = db.Column(db.String)
    update_date = db.Column(db.String)
    group_data = db.Column(db.String)
    biz_info = db.Column(db.String)
    create_by = db.Column(db.String)
    update_by = db.Column(db.String)
    use_status = db.Column(db.String)
    cover_page = db.Column(db.String)
    tid = db.Column(db.String)
    group_color = db.Column(db.String)
    email_middle = db.Column(db.String)
    timegroup_auto = db.Column(db.String)
    daygroup_auto = db.Column(db.String)

    def __init__(self,group_name,group_code,template,document_type,group_title,step_group,status,create_date,update_date,group_data,biz_info,create_by,update_by,use_status,cover_page,tid,group_color,email_middle,timegroup_auto,daygroup_auto):
        self.group_name = group_name
        self.group_code = group_code
        self.template = template
        self.document_type = document_type
        self.group_title = group_title
        self.step_group = step_group
        self.status = status
        self.create_date = create_date
        self.update_date = update_date
        self.group_data = group_data
        self.biz_info = biz_info
        self.create_by = create_by
        self.update_by = update_by
        self.use_status = use_status
        self.cover_page = cover_page
        self.tid = tid
        self.group_color = group_color
        self.email_middle = email_middle
        self.timegroup_auto = timegroup_auto
        self.daygroup_auto = daygroup_auto

    def __repr__(self):
        return '<id {},group_name {},group_code {},template {},document_type {},group_title {},step_group {},status {},create_date {},update_date {},group_data {},biz_info {},create_by {},update_by {},use_status {},cover_page {},tid {},group_color {},email_middle {},timegroup_auto {},daygroup_auto {}>'.format(self.id,self.group_name,self.group_code,self.template,self.document_type,self.group_title,self.step_group,self.status,self.create_date,self.update_date,self.group_data,self.biz_info,self.create_by,self.update_by,self.use_status,self.cover_page,self.tid,self.group_color,self.email_middle,self.timegroup_auto,self.daygroup_auto)


# class tb_group_template(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = "tb_group_template"

#     id = db.Column(db.Integer, primary_key=True)
#     group_name = db.Column(db.String)
#     group_code = db.Column(db.String)
#     template = db.Column(db.TIMESTAMP(timezone=True))
#     document_type = db.Column(db.String)
#     group_title = db.Column(db.String)
#     step_group = db.Column(db.String)
#     status = db.Column(db.String)
#     create_date = db.Column(db.String)
#     update_date = db.Column(db.String)
#     group_data = db.Column(db.String)
#     biz_info = db.Column(db.String)
#     create_by = db.Column(db.String)
#     update_by = db.Column(db.String)
#     use_status = db.Column(db.String)
#     cover_page = db.Column(db.String)
#     tid = db.Column(db.String)
#     group_color = db.Column(db.String)
#     email_middle = db.Column(db.String)
#     timegroup_auto = db.Column(db.String)
#     daygroup_auto = db.Column(db.String)

#     def __init__(self,group_name,group_code,template,document_type,group_title,step_group,status,create_date,update_date,group_data,biz_info,create_by,update_by,use_status,cover_page,tid,group_color,email_middle,timegroup_auto,daygroup_auto):
#         self.group_name = group_name
#         self.group_code = group_code
#         self.template = template
#         self.document_type = document_type
#         self.group_title = group_title
#         self.step_group = step_group
#         self.status = status
#         self.create_date = create_date
#         self.update_date = update_date
#         self.group_data = group_data
#         self.biz_info = biz_info
#         self.create_by = create_by
#         self.update_by = update_by
#         self.use_status = use_status
#         self.cover_page = cover_page
#         self.tid = tid
#         self.group_color = group_color
#         self.email_middle = email_middle
#         self.timegroup_auto = timegroup_auto
#         self.daygroup_auto = daygroup_auto

#     def __repr__(self):
#         return '<id {},group_name {},group_code {},template {},document_type {},group_title {},step_group {},status {},create_date {},update_date {},group_data {},biz_info {},create_by {},update_by {},use_status {},cover_page {},tid {},group_color {},email_middle {},timegroup_auto {},daygroup_auto {}>'.format(self.id,self.group_name,self.group_code,self.template,self.document_type,self.group_title,self.step_group,self.status,self.create_date,self.update_date,self.group_data,self.biz_info,self.create_by,self.update_by,self.use_status,self.cover_page,self.tid,self.group_color,self.email_middle,self.timegroup_auto,self.daygroup_auto)


class paper_lesstranfer(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_transferuser'

    
    sid = db.Column(db.String)
    action_status = db.Column(db.String)
    step_num = db.Column(db.String)
    email_from = db.Column(db.String)
    email_to = db.Column(db.String)
    datetime = db.Column(db.TIMESTAMP(timezone=True))
    status = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
   
    def __init__(self, sid, action_status, step_num, email_from, email_to,datetime,status,email):
        self.sid = sid
        self.action_status = action_status
        self.step_num = step_num
        self.email_from = email_from
        self.email_to = email_to
        self.datetime = datetime
        self.status   = status
        self.email = email
    def __repr__(self):
        return '<id {},sid {},action_status {},step_num {},email_from {},email_to {},datetime {},status {},email {}>'.format(self.id, self.sid, self.action_status, self.step_num, self.email_from, self.email_to,self.datetime,self.status,self.email)

# class paper_lesstranfer(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_transferuser'

    
#     sid = db.Column(db.String)
#     action_status = db.Column(db.String)
#     step_num = db.Column(db.String)
#     email_from = db.Column(db.String)
#     email_to = db.Column(db.String)
#     datetime = db.Column(db.TIMESTAMP(timezone=True))
#     status = db.Column(db.String)
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String)
   
#     def __init__(self, sid, action_status, step_num, email_from, email_to,datetime,status,email):
#         self.sid = sid
#         self.action_status = action_status
#         self.step_num = step_num
#         self.email_from = email_from
#         self.email_to = email_to
#         self.datetime = datetime
#         self.status   = status
#         self.email = email
#     def __repr__(self):
#         return '<id {},sid {},action_status {},step_num {},email_from {},email_to {},datetime {},status {},email {}>'.format(self.id, self.sid, self.action_status, self.step_num, self.email_from, self.email_to,self.datetime,self.status,self.email)

class tb_schedule_alert_document(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_schedule_alert_document'

    
    id = db.Column(db.String,primary_key=True)
    email = db.Column(db.String)
    time_alert_last = db.Column(db.TIMESTAMP(timezone=True))
    sid = db.Column(db.String)
    status = db.Column(db.String)
    update_last = db.Column(db.TIMESTAMP(timezone=True))
    time_alert_again = db.Column(db.TIMESTAMP(timezone=True))
   
    def __init__(self, email, time_alert_last, sid, status, update_last,time_alert_again):
        self.email = email
        self.time_alert_last = time_alert_last
        self.sid = sid
        self.status = status
        self.update_last = update_last
        self.time_alert_again = time_alert_again

    def __repr__(self):
        return '<id {},email {},time_alert_last {},sid {},status {},update_last {},time_alert_again {}>'.format(self.id, self.email, self.time_alert_last, self.sid, self.status, self.update_last,self.time_alert_again)

# class tb_schedule_alert_document(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_schedule_alert_document'

    
#     id = db.Column(db.String,primary_key=True)
#     email = db.Column(db.String)
#     time_alert_last = db.Column(db.TIMESTAMP(timezone=True))
#     sid = db.Column(db.String)
#     status = db.Column(db.String)
#     update_last = db.Column(db.TIMESTAMP(timezone=True))
#     time_alert_again = db.Column(db.TIMESTAMP(timezone=True))
   
#     def __init__(self, email, time_alert_last, sid, status, update_last,time_alert_again):
#         self.email = email
#         self.time_alert_last = time_alert_last
#         self.sid = sid
#         self.status = status
#         self.update_last = update_last
#         self.time_alert_again = time_alert_again

#     def __repr__(self):
#         return '<id {},email {},time_alert_last {},sid {},status {},update_last {},time_alert_again {}>'.format(self.id, self.email, self.time_alert_last, self.sid, self.status, self.update_last,self.time_alert_again)

class tb_process_request(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_process_request'

    id = db.Column(db.String,primary_key=True)
    name_process = db.Column(db.String)
    status = db.Column(db.String)
    datetime = db.Column(db.TIMESTAMP(timezone=True))
    document = db.Column(db.String)
    urlapi = db.Column(db.String)
    datetime_update = db.Column(db.TIMESTAMP(timezone=True))
    group_id = db.Column(db.String)
    email = db.Column(db.String)
   
    def __init__(self, name_process, status, datetime, document, urlapi,datetime_update,group_id,email):
        self.name_process = name_process
        self.status = status
        self.datetime = datetime
        self.document = document
        self.urlapi = urlapi
        self.datetime_update = datetime_update
        self.group_id = group_id
        self.email = email

    def __repr__(self):
        return '<id {},name_process {},status {},datetime {},document {},urlapi {},datetime_update {},group_id {},email {}>'.format(self.id, self.name_process, self.status, self.datetime, self.document, self.urlapi,self.datetime_update,self.group_id,self.email)

# class tb_process_request(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_process_request'

#     id = db.Column(db.String,primary_key=True)
#     name_process = db.Column(db.String)
#     status = db.Column(db.String)
#     datetime = db.Column(db.TIMESTAMP(timezone=True))
#     document = db.Column(db.String)
#     urlapi = db.Column(db.String)
#     datetime_update = db.Column(db.TIMESTAMP(timezone=True))
#     group_id = db.Column(db.String)
#     email = db.Column(db.String)
   
#     def __init__(self, name_process, status, datetime, document, urlapi,datetime_update,group_id,email):
#         self.name_process = name_process
#         self.status = status
#         self.datetime = datetime
#         self.document = document
#         self.urlapi = urlapi
#         self.datetime_update = datetime_update
#         self.group_id = group_id
#         self.email = email

#     def __repr__(self):
#         return '<id {},name_process {},status {},datetime {},document {},urlapi {},datetime_update {},group_id {},email {}>'.format(self.id, self.name_process, self.status, self.datetime, self.document, self.urlapi,self.datetime_update,self.group_id,self.email)

class tb_transaction_ocr(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_transaction_ocr'

    id = db.Column(db.String,primary_key=True)
    sid = db.Column(db.String)
    data_thai = db.Column(db.String)
    data_eng = db.Column(db.String)
    data_sum = db.Column(db.String)
    datetime = db.Column(db.TIMESTAMP(timezone=True))
   
    def __init__(self, sid, data_thai, data_eng, data_sum, datetime):
        self.sid = sid
        self.data_thai = data_thai
        self.data_eng = data_eng
        self.data_sum = data_sum
        self.datetime = datetime

    def __repr__(self):
        return '<id {},sid {},data_thai {},data_eng {},data_sum {},datetime {}>'.format(self.id, self.sid, self.data_thai, self.data_eng, self.data_sum, self.datetime)

# class tb_transaction_ocr(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_transaction_ocr'

#     id = db.Column(db.String,primary_key=True)
#     sid = db.Column(db.String)
#     data_thai = db.Column(db.String)
#     data_eng = db.Column(db.String)
#     data_sum = db.Column(db.String)
#     datetime = db.Column(db.TIMESTAMP(timezone=True))
   
#     def __init__(self, sid, data_thai, data_eng, data_sum, datetime):
#         self.sid = sid
#         self.data_thai = data_thai
#         self.data_eng = data_eng
#         self.data_sum = data_sum
#         self.datetime = datetime

#     def __repr__(self):
#         return '<id {},sid {},data_thai {},data_eng {},data_sum {},datetime {}>'.format(self.id, self.sid, self.data_thai, self.data_eng, self.data_sum, self.datetime)

class paperless_draft(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_draft_document'

    id = db.Column(db.Integer, primary_key=True)
    data_json = db.Column(db.String)
    data_json_Upload = db.Column(db.String)
    biz_info = db.Column(db.String)
    qrCode_position = db.Column(db.String)
    recipient_email = db.Column(db.String)
    string_pdf = db.Column(db.String)
    documentJson = db.Column(db.String)
    options_page = db.Column(db.String)
    documentType = db.Column(db.String)
    status = db.Column(db.String)
    sender_email = db.Column(db.String)
    update_time = db.Column(db.String)
    tid = db.Column(db.String)
    template = db.Column(db.String)
    type_file = db.Column(db.String)
    folder_name = db.Column(db.String)
    email_center = db.Column(db.String)
    step_code = db.Column(db.String)
    attempted_name = db.Column(db.String)
    attach_data = db.Column(db.String)

    def __init__(self, data_json, data_json_Upload, biz_info,qrCode_position,recipient_email,string_pdf,documentJson,options_page,documentType,status,sender_email,update_time,tid,template,type_file,folder_name,email_center,step_code,attempted_name,attach_data):
        self.data_json = data_json
        self.data_json_Upload = data_json_Upload
        self.biz_info = biz_info
        self.qrCode_position = qrCode_position
        self.recipient_email = recipient_email
        self.string_pdf = string_pdf
        self.documentJson = documentJson
        self.options_page = options_page
        self.documentType = documentType
        self.status = status
        self.sender_email = sender_email
        self.update_time = update_time
        self.tid = tid
        self.template = template
        self.type_file = type_file
        self.folder_name = folder_name
        self.email_center = email_center
        self.step_code = step_code
        self.attempted_name = attempted_name
        self.attach_data = attach_data
    def __repr__(self):
        return '<id {},data_json {},data_json_Upload {},biz_info {},qrCode_position {},recipient_email {},string_pdf {},documentJson {},options_page {},documentType {},status {},sender_email {},update_time {},tid {},template {},type_file {},folder_name {},email_center {},step_code {},attempted_name {},attach_data {}>'.format(self.id,self.data_json,self.data_json_Upload,self.biz_info,self.qrCode_position,self.recipient_email,self.string_pdf,self.documentJson,self.options_page,self.documentType,self.status,self.sender_email,self.update_time,self.tid,self.template,self.type_file,self.folder_name,self.email_center,self.step_code,self.attempted_name,self.attach_data)

# class paperless_draft(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_draft_document'

#     id = db.Column(db.Integer, primary_key=True)
#     data_json = db.Column(db.String)
#     data_json_Upload = db.Column(db.String)
#     biz_info = db.Column(db.String)
#     qrCode_position = db.Column(db.String)
#     recipient_email = db.Column(db.String)
#     string_pdf = db.Column(db.String)
#     documentJson = db.Column(db.String)
#     options_page = db.Column(db.String)
#     documentType = db.Column(db.String)
#     status = db.Column(db.String)
#     sender_email = db.Column(db.String)
#     update_time = db.Column(db.String)
#     tid = db.Column(db.String)
#     template = db.Column(db.String)
#     type_file = db.Column(db.String)
#     folder_name = db.Column(db.String)
#     email_center = db.Column(db.String)
#     step_code = db.Column(db.String)
#     attempted_name = db.Column(db.String)
#     attach_data = db.Column(db.String)

#     def __init__(self, data_json, data_json_Upload, biz_info,qrCode_position,recipient_email,string_pdf,documentJson,options_page,documentType,status,sender_email,update_time,tid,template,type_file,folder_name,email_center,step_code,attempted_name,attach_data):
#         self.data_json = data_json
#         self.data_json_Upload = data_json_Upload
#         self.biz_info = biz_info
#         self.qrCode_position = qrCode_position
#         self.recipient_email = recipient_email
#         self.string_pdf = string_pdf
#         self.documentJson = documentJson
#         self.options_page = options_page
#         self.documentType = documentType
#         self.status = status
#         self.sender_email = sender_email
#         self.update_time = update_time
#         self.tid = tid
#         self.template = template
#         self.type_file = type_file
#         self.folder_name = folder_name
#         self.email_center = email_center
#         self.step_code = step_code
#         self.attempted_name = attempted_name
#         self.attach_data = attach_data
#     def __repr__(self):
#         return '<id {},data_json {},data_json_Upload {},biz_info {},qrCode_position {},recipient_email {},string_pdf {},documentJson {},options_page {},documentType {},status {},sender_email {},update_time {},tid {},template {},type_file {},folder_name {},email_center {},step_code {},attempted_name {},attach_data {}>'.format(self.id,self.data_json,self.data_json_Upload,self.biz_info,self.qrCode_position,self.recipient_email,self.string_pdf,self.documentJson,self.options_page,self.documentType,self.status,self.sender_email,self.update_time,self.tid,self.template,self.type_file,self.folder_name,self.email_center,self.step_code,self.attempted_name,self.attach_data)

class paperless_user_qrcode(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_user_qrcode'

    id = db.Column(db.Integer, primary_key=True)
    email_user = db.Column(db.String)
    url_qrcode = db.Column(db.String)
    path_qrcode = db.Column(db.String)
    token_url = db.Column(db.String)
    token_qr = db.Column(db.String)
    hash_value = db.Column(db.String)
    url_login_qrcode = db.Column(db.String)
    token_url_filter = db.Column(db.String)
    url_login_qrcode_new = db.Column(db.String)

    def __init__(self,email_user,url_qrcode,path_qrcode,token_url,token_qr,hash_value,url_login_qrcode,token_url_filter,url_login_qrcode_new):
        self.email_user = email_user
        self.url_qrcode = url_qrcode
        self.path_qrcode = path_qrcode
        self.token_url = token_url
        self.token_qr = token_qr
        self.hash_value = hash_value
        self.url_login_qrcode = url_login_qrcode
        self.token_url_filter = token_url_filter
        self.url_login_qrcode_new = url_login_qrcode_new
        
    def __repr__(self):
        return '<id {},email_user {},url_qrcode {},path_qrcode {},token_url {},token_qr {},hash_value {},url_login_qrcode {},token_url_filter {},url_login_qrcode_new {}>'.format(self.id,self.email_user,self.url_qrcode,self.path_qrcode,self.token_url,self.token_qr,self.hash_value,self.url_login_qrcode,self.token_url_filter,self.url_login_qrcode_new)

# class paperless_user_qrcode(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_user_qrcode'

#     id = db.Column(db.Integer, primary_key=True)
#     email_user = db.Column(db.String)
#     url_qrcode = db.Column(db.String)
#     path_qrcode = db.Column(db.String)
#     token_url = db.Column(db.String)
#     token_qr = db.Column(db.String)
#     hash_value = db.Column(db.String)
#     url_login_qrcode = db.Column(db.String)
#     token_url_filter = db.Column(db.String)
#     url_login_qrcode_new = db.Column(db.String)

#     def __init__(self,email_user,url_qrcode,path_qrcode,token_url,token_qr,hash_value,url_login_qrcode,token_url_filter,url_login_qrcode_new):
#         self.email_user = email_user
#         self.url_qrcode = url_qrcode
#         self.path_qrcode = path_qrcode
#         self.token_url = token_url
#         self.token_qr = token_qr
#         self.hash_value = hash_value
#         self.url_login_qrcode = url_login_qrcode
#         self.token_url_filter = token_url_filter
#         self.url_login_qrcode_new = url_login_qrcode_new
        
#     def __repr__(self):
#         return '<id {},email_user {},url_qrcode {},path_qrcode {},token_url {},token_qr {},hash_value {},url_login_qrcode {},token_url_filter {},url_login_qrcode_new {}>'.format(self.id,self.email_user,self.url_qrcode,self.path_qrcode,self.token_url,self.token_qr,self.hash_value,self.url_login_qrcode,self.token_url_filter,self.url_login_qrcode_new)

class paperless_pwd(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_pwd'

    id = db.Column(db.Integer, primary_key=True)
    pwd_id = db.Column(db.String)
    hash_pwd = db.Column(db.String)
    

    def __init__(self,pwd_id,hash_pwd):
        self.pwd_id = pwd_id
        self.hash_pwd = hash_pwd
        
    def __repr__(self):
        return '<id {},pwd_id {},hash_pwd {}>'.format(self.id,self.pwd_id,self.hash_pwd)

# class paperless_pwd(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_pwd'

#     id = db.Column(db.Integer, primary_key=True)
#     pwd_id = db.Column(db.String)
#     hash_pwd = db.Column(db.String)
    

#     def __init__(self,pwd_id,hash_pwd):
#         self.pwd_id = pwd_id
#         self.hash_pwd = hash_pwd
        
#     def __repr__(self):
#         return '<id {},pwd_id {},hash_pwd {}>'.format(self.id,self.pwd_id,self.hash_pwd)

class paperless_permission(db.Model):
    __bind_key__ = status_db_r
    __tablename__ = 'tb_permission'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    role_level = db.Column(db.String)
    permis_send_approve = db.Column(db.String)
    permis_create_doc = db.Column(db.String)
    permis_sign_doc = db.Column(db.String)
    permis_view_doc = db.Column(db.String)
    permis_cancel_doc = db.Column(db.String)
    permis_doc_format = db.Column(db.String)
    permis_doc_type = db.Column(db.String)
    update_time = db.Column(db.String)

    def __init__(self,name,role_level,permis_send_approve,permis_create_doc,permis_sign_doc,permis_view_doc,permis_cancel_doc,permis_doc_format,permis_doc_type,update_time):
        self.name = name
        self.role_level = role_level
        self.permis_send_approve = permis_send_approve
        self.permis_create_doc = permis_create_doc
        self.permis_sign_doc = permis_sign_doc
        self.permis_view_doc = permis_view_doc
        self.permis_cancel_doc = permis_cancel_doc
        self.permis_doc_format = permis_doc_format
        self.permis_doc_type = permis_doc_type
        self.update_time = update_time
    def __repr__(self):
        return '<id {},name {},role_level {},permis_send_approve {},permis_create_doc {},permis_sign_doc {},permis_view_doc {},permis_cancel_doc {},permis_doc_format {},permis_doc_type {},update_time {}>'.format(self.id,self.name,self.role_level,self.permis_send_approve,self.permis_create_doc,self.permis_sign_doc,self.permis_view_doc,self.permis_cancel_doc,self.permis_doc_format,self.permis_doc_type,self.update_time)


# class paperless_permission(db.Model_RW):
#     __bind_key__ = status_db_rw
#     __tablename__ = 'tb_permission'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     role_level = db.Column(db.String)
#     permis_send_approve = db.Column(db.String)
#     permis_create_doc = db.Column(db.String)
#     permis_sign_doc = db.Column(db.String)
#     permis_view_doc = db.Column(db.String)
#     permis_cancel_doc = db.Column(db.String)
#     permis_doc_format = db.Column(db.String)
#     permis_doc_type = db.Column(db.String)
#     update_time = db.Column(db.String)

#     def __init__(self,name,role_level,permis_send_approve,permis_create_doc,permis_sign_doc,permis_view_doc,permis_cancel_doc,permis_doc_format,permis_doc_type,update_time):
#         self.name = name
#         self.role_level = role_level
#         self.permis_send_approve = permis_send_approve
#         self.permis_create_doc = permis_create_doc
#         self.permis_sign_doc = permis_sign_doc
#         self.permis_view_doc = permis_view_doc
#         self.permis_cancel_doc = permis_cancel_doc
#         self.permis_doc_format = permis_doc_format
#         self.permis_doc_type = permis_doc_type
#         self.update_time = update_time
#     def __repr__(self):
#         return '<id {},name {},role_level {},permis_send_approve {},permis_create_doc {},permis_sign_doc {},permis_view_doc {},permis_cancel_doc {},permis_doc_format {},permis_doc_type {},update_time {}>'.format(self.id,self.name,self.role_level,self.permis_send_approve,self.permis_create_doc,self.permis_sign_doc,self.permis_view_doc,self.permis_cancel_doc,self.permis_doc_format,self.permis_doc_type,self.update_time)
