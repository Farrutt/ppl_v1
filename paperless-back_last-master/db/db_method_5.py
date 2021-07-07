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
from method.document import *


class insert_5():
    

    def insert_contactus_v1(self,name,company_name,phone_no,email,title,message):
        self.name = name
        self.company_name = company_name
        self.phone_no = phone_no
        self.email = email
        self.title = title
        self.message = message
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        try:
            with engine.connect() as connection:
                result_insert = connection.execute('INSERT INTO tb_contactus ("name", "company_name", "phone_no","email","title","message","datetime") VALUES (%s,%s,%s,%s,%s,%s,%s) ', self.name,self.company_name,self.phone_no,self.email,self.title,self.message,str(st))
            connection.close()
            return ({'result':'OK','messageText':'success','messageER':None,'status_Code':200})            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200})
    
    def insert_package_main_enhance(self,tax_id,datetimeStart,datetimeEnd,package_main,package_Enhance):
        self.tax_id = tax_id
        self.datetimeStart = datetimeStart
        self.datetimeEnd = datetimeEnd
        self.package_main = package_main
        self.package_Enhance = package_Enhance    
        try:
            data_list = []
            count_list = []
            list_pk_enhance = []
            transactionMax = 0
            storageMax = 0
            eformMax = 0
            userMax = 0
            caMax = 0
            oneboxMax = 0
            date_now = datetime.datetime.now()
            date_now_str = date_now.strftime('%Y-%m-%d %H:%M:%S')
            if self.package_main != None and self.datetimeStart != None and self.datetimeEnd != None:
                dateStart_str = datetime.datetime.fromtimestamp(self.datetimeStart).strftime('%Y-%m-%d %H:%M:%S')
                dateEnd_str = datetime.datetime.fromtimestamp(self.datetimeEnd).strftime('%Y-%m-%d %H:%M:%S')
                dateStart = datetime.datetime.strptime(dateStart_str, '%Y-%m-%d %H:%M:%S')
                dateEnd = datetime.datetime.strptime(dateEnd_str, '%Y-%m-%d %H:%M:%S')
                data_list.append(self.package_main)
                count_list.append(1)
                for codeEnhance in self.package_Enhance:
                    data_list.append(codeEnhance['code'])
                    count_list.append(codeEnhance['count'])
                data_tuple = tuple(data_list)
                with engine.connect() as connection:
                    result_select = connection.execute(text('''SELECT * FROM "tb_bizPaperless" WHERE "tax_id" =:tax_id '''),tax_id=self.tax_id)
                    data_tax = [dict(row) for row in result_select]
                    connection.close()
                data_tax = data_tax[0]
                if data_tax['package_Main_id'] != '' and data_tax['package_Main_id'] != None:
                    return {'result':'ER','messageText':{'data': self.tax_id,'status': 'business already has a main package'}}
                if data_tax['transactionNow'] == None:
                    transactionNow = 0
                else:
                    transactionNow = data_tax['transactionNow']
                if data_tax['storageNow'] == None:
                    storageNow = 0
                else:
                    storageNow = data_tax['storageNow']
                if data_tax['eformNow'] == None:
                    eformNow = 0
                else:
                    eformNow = data_tax['eformNow']
                if data_tax['userNow'] == None:
                    userNow = 0
                else:
                    userNow = data_tax['userNow']
                if data_tax['caNow'] == None:
                    caNow = 0
                else:
                    caNow = data_tax['caNow']
                if data_tax['oneboxNow'] == None:
                    oneboxNow = 0
                else:
                    oneboxNow = data_tax['oneboxNow']
                package_main = str(self.package_main)
                package_Enhance = str(self.package_Enhance)                
            else:
                with engine.connect() as connection:
                    result_enhance = connection.execute(text('''SELECT "package_Main_id","package_Enhance_id" FROM "tb_bizPaperless" WHERE "tax_id" =:tax_id '''),tax_id=self.tax_id)
                    result = [dict(row) for row in result_enhance]
                    connection.close()
                
                package_Main = result[0]['package_Main_id']
                package_EnhanceOld = result[0]['package_Enhance_id']
                if package_Main == '' or package_Main == None:
                    return {'result':'ER','messageText':{'data': 'กรุณาสมัครแพ็กเกจหลักก่อนใช้งาน','status': 'insert package Enhance fail'}}
                package_EnhanceOld = eval(package_EnhanceOld)            
                data_list.append(package_Main)
                count_list.append(1)
                for dt in package_EnhanceOld:
                    for dt2 in self.package_Enhance:
                        if dt2['code'] == dt['code']:
                            count_dt = dt2['count'] + dt['count']
                            data_list.append(dt2['code'])
                            count_list.append(count_dt)
                            list_pk_enhance.append({"code": dt2['code'], "count": count_dt})
                    if dt['code'] not in data_list:
                        data_list.append(dt['code'])
                        count_list.append(dt['count'])
                        list_pk_enhance.append({"code": dt['code'], "count": dt['count']})                    
                for dt3 in self.package_Enhance:
                    if dt3['code'] not in data_list:
                        data_list.append(dt3['code'])
                        count_list.append(dt3['count'])
                        list_pk_enhance.append({"code": dt3['code'], "count": dt3['count']})
                package_main = str(package_Main)
                package_Enhance = str(list_pk_enhance)
                data_tuple = tuple(data_list)

            with engine.connect() as connection:
                result_select = connection.execute(text('''SELECT * FROM "tb_cost_package" WHERE "code_service" IN :codelist '''),codelist=data_tuple)
                result = [dict(row) for row in result_select]
                connection.close()
            print('lenQuery',len(result))
            for data in result:
                code_service = data['code_service']
                for i in range(len(data_list)):
                    if code_service == data_list[i]:
                        transactionMax += (data['transactions'] * count_list[i])
                        storageMax += (data['storage_gb'] * count_list[i])
                        eformMax += (data['e_form'] * count_list[i])
                        userMax += (data['support_user'] * count_list[i])
                        caMax += (data['support_ca'] * count_list[i])
                        oneboxMax += (data['one_box_gb'] * count_list[i])        
            with engine.connect() as connection:
                if self.package_main != None and self.datetimeStart != None and self.datetimeEnd != None:
                    r = relativedelta(dateStart, dateEnd)
                    aroundMax = abs((r.years * 12) + r.months)
                    around = 0
                    result_update = connection.execute('UPDATE "tb_bizPaperless" SET "update_date"=%s,"transactionMax"=%s,"transactionNow"=%s,"storageMax"=%s,"storageNow"=%s,"eformMax"=%s,"eformNow"=%s,"userMax"=%s,"userNow"=%s,"caMax"=%s,"caNow"=%s,"oneboxMax"=%s,"oneboxNow"=%s \
                        ,"datetime_first"=%s,"datetime_last"=%s,"datetime_around"=%s,"around"=%s,"aroundMax"=%s,"package_Main_id"=%s,"package_Enhance_id"=%s \
                        WHERE "tax_id"=%s RETURNING "tax_id"' ,date_now_str,transactionMax,transactionNow,storageMax,storageNow,eformMax,eformNow,userMax,userNow,caMax,caNow,oneboxMax,oneboxNow,dateStart_str,dateEnd_str,dateStart_str,around,aroundMax,package_main,package_Enhance,self.tax_id)
                    tmp_result = [dict(row) for row in result_update]
                else:
                    result_update = connection.execute('UPDATE "tb_bizPaperless" SET "update_date"=%s,"transactionMax"=%s,"storageMax"=%s,"eformMax"=%s,"userMax"=%s,"caMax"=%s,"oneboxMax"=%s,"package_Main_id"=%s,"package_Enhance_id"=%s \
                        WHERE "tax_id"=%s RETURNING "tax_id"' ,date_now_str,transactionMax,storageMax,eformMax,userMax,caMax,oneboxMax,package_main,package_Enhance,self.tax_id)
                    tmp_result = [dict(row) for row in result_update]
                result_status = connection.execute('UPDATE "tb_bizPaperless" SET "status"=true WHERE "transactionNow" < "transactionMax" and "storageNow" < ("storageMax" * 1073741824) and "tax_id"=%s RETURNING "tax_id"' ,self.tax_id)
                result_st = [dict(row) for row in result_status]
                connection.close()
            return {'result':'OK','messageText':{'data': tmp_result[0],'status': 'insert package success'}}

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(ex)}
    
    def insert_package_v1(self,code_service,name_service,type_service,transactions,eform,support_user,support_ca,storage,one_box,back_up,offer,implement,cost_month):
        self.code_service = code_service
        self.name_service = name_service
        self.type_service = type_service
        self.transactions = transactions
        self.eform = eform
        self.support_user = support_user
        self.support_ca = support_ca
        self.storage = storage
        self.one_box = one_box
        self.back_up = back_up
        self.offer = offer
        self.implement = implement
        self.cost_month = cost_month        
        try:
            status = 'true'
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            with engine.connect() as connection:
                get_code_service = connection.execute('SELECT "code_service" FROM "tb_cost_package" WHERE "code_service"=%s',self.code_service)
                get_code = [dict(row) for row in get_code_service]
                if len(get_code) == 0:
                    insert_package =  connection.execute('insert into tb_cost_package ("code_service","name_service","type_service","transactions","e_form","support_user","support_ca","storage_gb","one_box_gb","back_up","offer","implement","cost_month","updatetime","status") \
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) \
                    RETURNING "code_service"',self.code_service,self.name_service,self.type_service,self.transactions,self.eform,self.support_user,self.support_ca,self.storage,self.one_box,self.back_up,self.offer,self.implement,self.cost_month,st,status)
                    tmp = [dict(row) for row in insert_package]
                    connection.close()
                    return {'result':'OK','messageText':{'data': tmp[0]['code_service'],'status': 'insert package success'}}
                else:
                    return {'result':'ER','messageText':{'data': self.code_service,'status': 'Duplicate Code Service'}}  
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(ex)}
  
class select_5(): 
    def check_around_package_v1(self,datetimeNow):
        dt = ''
        arr_list = []
        data_list = []
        count_list = []
        self.datetimeNow = datetimeNow
        try:
            # date_now = datetime(2020, 6, 5, 00, 00) 
            # date_now = date_now.isoformat(' ')
            date_now = datetime.datetime.strptime(self.datetimeNow, '%Y-%m-%d %H:%M:%S')             
            # date_now = datetime.now()
            date_now_str = date_now.strftime('%Y-%m-%d %H:%M:%S')
            day_now = int(date_now.strftime('%d'))
            # print('day_now',day_now)
            max_day_now = calendar.monthrange(date_now.year, date_now.month)[1]
            date_old = date_now + relativedelta(months=-1)
            max_day_old = calendar.monthrange(date_old.year, date_old.month)[1]
            if day_now == max_day_now and max_day_now < max_day_old :
                dt1 = date_old.strftime('%Y-%m-'+ str(max_day_now) +' 00:00:00')
                dt2= date_old.strftime('%Y-%m-'+ str(max_day_old) +' 23:59:59')
            elif day_now > max_day_old:
                dt = 'null'
            else:
                dt1 = date_old.strftime('%Y-%m-%d 00:00:00')
                dt2= date_old.strftime('%Y-%m-%d 23:59:59') 

            with engine.connect() as connection:
                result_update = connection.execute('UPDATE "tb_bizPaperless" SET "status"=false WHERE ("transactionNow" >= "transactionMax" or "storageNow" >= ("storageMax" * 1073741824)) and status = true RETURNING "tax_id"')
                result2 = [dict(row) for row in result_update]
                connection.close() 

            print(dt1,dt2)
            if dt != 'null':
                with engine.connect() as connection:
                    result_select = connection.execute(text('''SELECT * FROM "tb_bizPaperless" WHERE "datetime_around"<=:dt2 and "transactionMax" != 0 '''),dt1=dt1,dt2=dt2)
                    resultQuery = [dict(row) for row in result_select]
                    connection.close()  
            
            if len(resultQuery) != 0 :
                for data in resultQuery:
                    data_list = []
                    count_list = []
                    cost_sum = 0
                    tax_id = data['tax_id']
                    status = data['status']
                    transactionsMax = data['transactionMax']
                    storageMax = data['storageMax']
                    transactionsNow = data['transactionNow']
                    storageNow = data['storageNow']
                    eformMax = data['eformMax']
                    eformNow = data['eformNow']
                    userMax = data['userMax']
                    userNow = data['userNow']
                    caMax = data['caMax']
                    caNow = data['caNow']
                    oneboxMax = data['oneboxMax']
                    oneboxNow = data['oneboxNow']
                    datetime_first = data['datetime_first']
                    datetime_last = data['datetime_last']
                    datetime_around = data['datetime_around']
                    dt_ard_check = datetime_around.strftime('%Y-%m-%d %H:%M:%S')
                    dt_ard_check = datetime.datetime.strptime(dt_ard_check, '%Y-%m-%d %H:%M:%S') 
                    dt_now_check = datetime.datetime.strptime(dt1, '%Y-%m-%d %H:%M:%S') 
                    around = data['around']
                    aroundMax = data['aroundMax']
                    package_Main = data['package_Main_id']
                    package_Enhance = data['package_Enhance_id']
                    package_Enhance_list = eval(package_Enhance)
                    around = around + 1 
                    datearound = date_now_str
                    if dt_ard_check < dt_now_check:
                        datearound = datetime_around + relativedelta(months=+1)
                                        
                    data_list.append(package_Main)
                    count_list.append(1)
                    for codeEnhance in package_Enhance_list:
                        data_list.append(codeEnhance['code'])
                        count_list.append(codeEnhance['count'])
                    data_tuple = tuple(data_list)

                    with engine.connect() as connection:
                        result_select = connection.execute(text('''SELECT "code_service","cost_month" FROM "tb_cost_package" WHERE "code_service" IN :codelist '''),codelist=data_tuple)
                        result_cost = [dict(row) for row in result_select]
                        for data2 in result_cost:
                            code_service = data2['code_service']
                            for i in range(len(data_list)):
                                if code_service == data_list[i]:
                                    cost_sum += (int(data2['cost_month']) * int(count_list[i]))

                        insert_history_package =  connection.execute('insert into "tb_history_package" ("tax_id","status","transactionMax","storageMax","transactionNow","storageNow","eformMax","eformNow","userMax","userNow","caMax","caNow","oneboxMax","oneboxNow" \
                            ,"datetime_first","datetime_last","datetime_around","around","aroundMax","package_Main_id","package_Enhance_id","cost_sum") values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) \
                            RETURNING "tax_id"',tax_id,status,transactionsMax,storageMax,transactionsNow,storageNow,eformMax,eformNow,userMax,userNow,caMax,caNow,oneboxMax,oneboxNow,datetime_first,datetime_last,datearound,around,aroundMax,package_Main,package_Enhance,cost_sum)
                        result_his = [dict(row) for row in insert_history_package]
                        connection.close()
 
                    if len(result_his) != 0 :
                        print('insert success')
                        tax_id  = result_his[0]['tax_id']  
                        if around == aroundMax :
                            status = 'false'  
                            transactionsMax = 0
                            storageMax = 0
                            eformMax = 0
                            userMax = 0
                            caMax = 0
                            oneboxMax = 0
                            around = 0
                            aroundMax = 0
                            datetime_first = datearound
                            datetime_last = datearound
                            datetime_around = datearound
                            package_Main = ''                           
                            package_Enhance = '[]'
                            with engine.connect() as connection:
                                result_update = connection.execute('UPDATE "tb_bizPaperless" SET "status"=%s,"update_date"=%s,"transactionMax"=%s,"storageMax"=%s,"eformMax"=%s,"userMax"=%s,"caMax"=%s,"oneboxMax"=%s,"datetime_first"=%s,"datetime_last"=%s,"datetime_around"=%s,"around"=%s,"aroundMax"=%s,"package_Main_id"=%s,"package_Enhance_id"=%s \
                                    WHERE "tax_id"=%s RETURNING "id"' ,status,date_now_str,transactionsMax,storageMax,eformMax,userMax,caMax,oneboxMax,datetime_first,datetime_last,date_now_str,around,aroundMax,package_Main,package_Enhance,tax_id)
                                tmp_result = [dict(row) for row in result_update]
                                connection.close()
                        else:
                            with engine.connect() as connection:
                                result_update = connection.execute('UPDATE "tb_bizPaperless" SET "update_date"=%s,"datetime_around"=%s,"around"=%s \
                                    WHERE "tax_id"=%s RETURNING "id"',date_now_str,datearound,around,tax_id)
                                tmp_result = [dict(row) for row in result_update]
                                connection.close()
                        print('update success')
                        arr_list.append({
                            "tax_id" : tax_id
                            })
            
            return {'result':'OK','messageText':{'taxID_update': arr_list,'status': 'check around success'}}

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(ex)}

    def select_package_v1(self,code_service):
        self.code_service = code_service      
        try:
            if self.code_service != None:
                with engine.connect() as connection:
                    result_select = connection.execute(text('''SELECT * FROM "tb_cost_package" WHERE "code_service"=:code_servicd '''),code_servicd=self.code_service)
                    result = [dict(row) for row in result_select]
                    connection.close()
            else:
                with engine.connect() as connection:
                    result_select = connection.execute(text('''SELECT * FROM "tb_cost_package" order by "type_service" desc,"code_service" asc '''))
                    result = [dict(row) for row in result_select]
                    connection.close()
            print('len()',len(result))
            list_arr = []
            for result in result:             
                list_arr.append({
                    "code_service" : result['code_service'],
                    "name_service" : result['name_service'],
                    "type_service" : result['type_service'],
                    "transactions" : result['transactions'],
                    "eform" : result['e_form'],
                    "support_user" : result['support_user'],
                    "support_ca" : result['support_ca'],
                    "storage" : result['storage_gb'],
                    "one_box" : result['one_box_gb'],
                    "back_up" : result['back_up'],
                    "offer" : result['offer'],
                    "implement" : result['implement'],
                    "cost_month" : result['cost_month'],
                    "updatetime" : str(result['updatetime'])
                }) 
            return {'result':'OK','messageText':list_arr}
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(ex)}
    
    def select_sum_cost(self,tax_id):
        self.tax_id = tax_id  
        list_arr = []
        list_cost_month = []
        cost_sum_all = 0    
        try:
            with engine.connect() as connection:
                result_select = connection.execute(text('''SELECT * FROM "tb_history_package" WHERE "tax_id"=:tax_id '''),tax_id=self.tax_id)
            result = [dict(row) for row in result_select]
            connection.close()

            print('len()',len(result))
            if len(result) != 0 :
                for data in result:    
                    cost_sum = data['cost_sum'] 
                    cost_sum_all += cost_sum
                    around_Now = data['around']
                    around_Max = data['aroundMax']
                    datetime_around = data['datetime_around']
                    datetime_around_str = datetime_around.strftime('%Y-%m-%d %H:%M:%S')    
                    datetime_first = data['datetime_first']  
                    datetime_first_str = datetime_first.strftime('%Y-%m-%d %H:%M:%S') 
                    datetime_last =  data['datetime_last']   
                    datetime_last_str = datetime_last.strftime('%Y-%m-%d %H:%M:%S') 
                    list_cost_month.append({
                        "around" : around_Now,
                        "datetime_around" : datetime_around_str,
                        "cost_month" : cost_sum,
                    })    

            else:
                with engine.connect() as connection: 
                    result_select = connection.execute(text('''SELECT * FROM "tb_bizPaperless" WHERE ("package_Main_id" != '' or "package_Main_id" IS NOT NULL) and tax_id =:taxId '''),taxId=self.tax_id)
                    resultQuery = [dict(row) for row in result_select]
                    connection.close()  
                data_list = []
                count_list = []
                if len(resultQuery) != 0:
                    datetime_first = resultQuery[0]['datetime_first']
                    datetime_first_str = datetime_first.strftime('%Y-%m-%d %H:%M:%S')
                    datetime_last = resultQuery[0]['datetime_last']
                    datetime_last_str = datetime_last.strftime('%Y-%m-%d %H:%M:%S') 
                    datetime_around = resultQuery[0]['datetime_around']
                    datetime_around_str = datetime_around.strftime('%Y-%m-%d %H:%M:%S')  
                    around = resultQuery[0]['around']
                    around_Max = resultQuery[0]['aroundMax']
                    package_Main = resultQuery[0]['package_Main_id']                    
                    package_Enhance_list = eval(resultQuery[0]['package_Enhance_id'])
                    data_list.append(package_Main)
                    count_list.append(1)
                    for codeEnhance in package_Enhance_list:
                        data_list.append(codeEnhance['code'])
                        count_list.append(codeEnhance['count'])
                    data_tuple = tuple(data_list)

                    with engine.connect() as connection:
                        result_select = connection.execute(text('''SELECT "code_service","cost_month" FROM "tb_cost_package" WHERE "code_service" IN :codelist '''),codelist=data_tuple)
                        result_cost = [dict(row) for row in result_select]
                        if len(result_cost) != 0:
                            for data2 in result_cost:
                                code_service = data2['code_service']
                                for i in range(len(data_list)):
                                    if code_service == data_list[i]:
                                        cost_sum_all += (int(data2['cost_month']) * int(count_list[i]))
                else:
                    return {'result':'OK','messageText':'No package'}
            list_arr.append({
                "datetime_first" : datetime_first_str,
                "datetime_last" : datetime_last_str,
                "around_cost_month" : list_cost_month,
                "cost_sum_all" : cost_sum_all,
                "around_max" : around_Max
            }) 
            return {'result':'OK','messageText':list_arr}
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(ex)}

    def check_storage_business(self,tax_id):
        self.tax_id = tax_id      
        try:
            print(self.tax_id)
            if self.tax_id != None and self.tax_id != '':
                with engine.connect() as connection:
                    result_select = connection.execute(text('''SELECT * FROM "tb_bizPaperless" WHERE "tax_id"=:tax_id'''),tax_id=self.tax_id)
                result = [dict(row) for row in result_select]
                connection.close()
            else:
                with engine.connect() as connection:
                    result_select = connection.execute(text('''SELECT * FROM "tb_bizPaperless" WHERE "transactionMax" IS NOT NULL and "storageMax" IS NOT NULL and "transactionNow" IS NOT NULL and "storageNow" IS NOT NULL '''))
                result = [dict(row) for row in result_select]
                connection.close()

            print('len()',len(result))
            list_arr = []
            if len(result) != 0 :
                for u in result:                
                    result = u
                    print(result['transactionMax'])
                    if result['status'] == False and result['transactionMax'] == 0:
                        list_arr.append({
                            "tax_id" : result['tax_id'],
                            "No package" : 'กรุณาสมัครแพ็กก่อนใช้งานด้วยค่ะ',
                            "statusUpload-document" : 'false'
                        })  
                    else: 
                        persent_transaction = result['transactionNow'] * 100 / result['transactionMax']
                        persent_storage = result['storageNow'] * 100 / (result['storageMax'] * 1073741824)  
                        status = result['status']  
                        tax_id = result['tax_id']  
                        if persent_transaction >= 100 or persent_storage >= 100:
                            status = 'false'
                            with engine.connect() as connection:
                                result_update = connection.execute('UPDATE "tb_bizPaperless" SET "status"=false WHERE "tax_id" = %s',tax_id)
                                result2 = [dict(row) for row in result_update]
                                connection.close() 
                        list_arr.append({
                            "tax_id" : tax_id,
                            "persent_transaction" : str(persent_transaction) +'%',
                            "persent_storage" : str(persent_storage) +'%',
                            "statusUpload-document" : status
                        }) 
            return {'result':'OK','messageText':list_arr}
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(ex)}

    def select_package_business(self,tax_id):
        self.tax_id = tax_id      
        try:
            if self.tax_id != None:
                with engine.connect() as connection:
                    result_select = connection.execute(text('''SELECT * FROM "tb_bizPaperless" WHERE "tax_id"=:tax_id '''),tax_id=self.tax_id)
                    result = [dict(row) for row in result_select]
                    connection.close()
            else:
                with engine.connect() as connection:
                    result_select = connection.execute(text('''SELECT * FROM "tb_bizPaperless" '''))
                    result = [dict(row) for row in result_select]
                    connection.close()
            print('len()',len(result))
            list_arr = []
            for result in result:  
                datetime_first = result['datetime_first']
                datetime_last =  result['datetime_last']
                datetime_around = result['datetime_around']
                update_date = result['update_date']    
                if result['package_Main_id'] != '' and result['package_Main_id'] != None:  
                    datetime_first = datetime_first.strftime('%Y-%m-%d %H:%M:%S')
                    datetime_last = datetime_last.strftime('%Y-%m-%d %H:%M:%S')
                    package_Main = result['package_Main_id']
                    package_Enhance = eval(result['package_Enhance_id'])
                    transactionMax = result['transactionMax']
                    transactionNow = result['transactionNow']
                    storageMax = result['storageMax']
                    storageNow = result['storageNow']
                    eformMax = result['eformMax']
                    eformNow = result['eformNow']
                    userMax = result['userMax']
                    userNow = result['userNow']
                    caMax = result['caMax']
                    caNow = result['caNow']
                    oneboxMax = result['oneboxMax']
                    oneboxNow = result['oneboxNow']
                    datetime_first = datetime_first
                    datetime_last =  datetime_last
                    datetime_around = datetime_around
                    aroundNow = result['around']
                    aroundMax = result['aroundMax']
                    status =  result['status']
                    update_date = update_date
                else:
                    package_Main = 'No package'
                    package_Enhance = 'No package'
                    transactionMax = 0
                    if result['transactionNow'] != '' and result['transactionNow'] != None:
                        transactionNow = result['transactionNow']
                    else:
                        transactionNow = 0
                    storageMax = 0
                    if result['storageNow'] != '' and result['storageNow'] != None:
                        storageNow = result['storageNow']
                    else:
                        storageNow = 0                    
                    eformMax = 0
                    if result['eformNow'] != '' and result['eformNow'] != None:
                        eformNow = result['eformNow']
                    else:
                        eformNow = 0                    
                    userMax = 0
                    if result['userNow'] != '' and result['userNow'] != None:
                        userNow = result['userNow']
                    else:
                        userNow = 0                    
                    caMax = 0
                    if result['caNow'] != '' and result['caNow'] != None:
                        caNow = result['caNow']
                    else:
                        caNow = 0                      
                    oneboxMax = 0
                    if result['oneboxNow'] != '' and result['oneboxNow'] != None:
                        oneboxNow = result['oneboxNow']
                    else:
                        oneboxNow = 0                     
                    datetime_first = ""
                    datetime_last =  ""
                    if result['datetime_around'] != '' and result['datetime_around'] != None:
                        datetime_around = datetime_around.strftime('%Y-%m-%d %H:%M:%S')
                        datetime_around = datetime_around
                    else:
                        datetime_around = ""                
                    aroundNow = 0
                    aroundMax = 0
                    status =  'false'
                    if result['update_date'] != '' and result['update_date'] != None:
                        update_date = update_date.strftime('%Y-%m-%d %H:%M:%S')
                        update_date = update_date
                    else:
                        update_date = "" 
                    
                list_arr.append({
                        "tax_id" : result['tax_id'],
                        "package_Main" : package_Main,
                        "package_Enhance" : package_Enhance,
                        "transactionMax" : transactionMax,
                        "transactionNow" : transactionNow,
                        "storageMax" : storageMax,
                        "storageNow" : storageNow,
                        "eformMax" : eformMax,
                        "eformNow" : eformNow,
                        "userMax" : userMax,
                        "userNow" : userNow,
                        "caMax" : caMax,
                        "caNow" : caNow,
                        "oneboxMax" : oneboxMax,
                        "oneboxNow" : oneboxNow,
                        "datetime_first" : datetime_first,
                        "datetime_last" : datetime_last,
                        "datetime_around" : datetime_around,
                        "aroundNow" : aroundNow,
                        "aroundMax" : aroundMax,
                        "status" : status,
                        "update_date" : update_date
                    }) 
            return {'result':'OK','messageText':list_arr}
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(ex)}
    
class update_5():
    def update_Configservice_business(self,jsondataconfig,tax_id):
        self.tax_id = tax_id
        self.jsondataconfig = str(jsondataconfig)
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        try:
            with engine.connect() as connection:
                result_insert = connection.execute('UPDATE "tb_bizPaperless" SET "config"=%s,"update_date"=%s  WHERE "tax_id"=%s', self.jsondataconfig,str(st),self.tax_id)
                connection.close()
            return ({'result':'OK','messageText':'success','messageER':None,'status_Code':200})            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200})

    def update_package_v1(self,code_service,name_service,type_service,transactions,eform,support_user,support_ca,storage,one_box,back_up,offer,implement,cost_month):
        self.code_service = code_service
        self.name_service = name_service
        self.type_service = type_service
        self.transactions = transactions
        self.eform = eform
        self.support_user = support_user
        self.support_ca = support_ca
        self.storage = storage
        self.one_box = one_box
        self.back_up = back_up
        self.offer = offer
        self.implement = implement
        self.cost_month = cost_month        
        try:
            status = 'true'
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            with engine.connect() as connection:
                get_code_service = connection.execute('SELECT "code_service" FROM "tb_cost_package" WHERE "code_service"=%s',self.code_service)
                get_code = [dict(row) for row in get_code_service]
                if len(get_code) != 0:
                    update_package =  connection.execute('UPDATE "tb_cost_package" SET "name_service"=%s,"type_service"=%s,"transactions"=%s,"e_form"=%s,"support_user"=%s,"support_ca"=%s,"storage_gb"=%s,"one_box_gb"=%s,"back_up"=%s,"offer"=%s,"implement"=%s,"cost_month"=%s,"updatetime"=%s \
                    WHERE "code_service"=%s RETURNING "code_service"',self.name_service,self.type_service,self.transactions,self.eform,self.support_user,self.support_ca,self.storage,self.one_box,self.back_up,self.offer,self.implement,self.cost_month,st,self.code_service)
                    tmp = [dict(row) for row in update_package]
                    connection.close()
                    return {'result':'OK','messageText':{'data': tmp[0]['code_service'],'status': 'update package success'}}
                else:
                    return {'result':'ER','messageText':{'data': self.code_service,'status': 'code_service not found'}}                
            
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(ex)}
        
class delete_5():
    def delete_package_v1(self,code_service):
        self.code_service = code_service     
        try:
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            with engine.connect() as connection:
                get_code_service = connection.execute('SELECT "code_service" FROM "tb_cost_package" WHERE "code_service"=%s',self.code_service)
                get_code = [dict(row) for row in get_code_service]
                if len(get_code) != 0:
                    delete_package =  connection.execute('DELETE FROM "tb_cost_package" WHERE "code_service"=%s',self.code_service)
                    connection.close()
                    return {'result':'OK','messageText':{'data': self.code_service,'status': 'Delete package success'}}
                else:
                    return {'result':'ER','messageText':{'data': self.code_service,'status': 'code_service not found'}}                
            
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(ex)}
        