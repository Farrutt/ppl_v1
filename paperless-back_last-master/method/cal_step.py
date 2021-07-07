from db.db_method import *
from db.db_method_4 import *

def cal_sender_status_document_v1(flowjson):
    tmp_jsonData_eval = []
    arr_step_info = []
    result_list_sum = []
    jsonData_eval = flowjson
    if 'step_num' in jsonData_eval:
        tmp_jsonData_eval.append(jsonData_eval)
        jsonData_eval = tmp_jsonData_eval
    if 'step_num' in jsonData_eval:
        step_status = ''
        step_before = ''
        res_status_file = 'Y'
        arr_step_totle = []
        json_data_info = jsonData_eval
        step_infomation = jsonData_eval
        tmp_list_email = []
        tmp_email_status = []
        
        tmp_status_sum = []
        email_step_sum = []
        tmp_list_status_document = []
        step_num = json_data_info['step_num']
        for i in range(len(step_infomation)):
            list_check_step = []
            json_step_info_2 = {}
            step_list_data = []
            step_status = []
            step_email = []
            # step_num = step_infomation[i]['step_num']
            json_step_info_2['step_status'] = ''
            tmp_step_detail = step_infomation['step_detail']
            for u in range(len(tmp_step_detail)):
                tmp_arr_step_detail = tmp_step_detail[u]
                tmp_status = tmp_arr_step_detail['activity_status']
                tmp_code = tmp_arr_step_detail['activity_code']
                tmp_email = str(tmp_arr_step_detail['one_email']).replace(' ','').lower()
                for s in range(len(tmp_code)):
                    if tmp_code[s] == 'A03':
                        step_status.append(tmp_status[s])
                        step_email.append(tmp_email)
            email_step_sum.append(step_email)
            if 'Reject' in step_status:
                tmp_status_sum.append('Reject')
            elif 'Approve' in step_status:
                tmp_status_sum.append('Complete')
            elif 'Complete' in step_status:
                tmp_status_sum.append('Complete')
            elif 'Incomplete' in step_status:
                tmp_status_sum.append('Incomplete')
            elif 'Pending' in step_status:
                tmp_status_sum.append('Incomplete')
            else:
                tmp_status_sum.append('Complete')

        if 'step_detail' in json_data_info:
            for s in range(len(json_data_info['step_detail'])):
                tmp_json_step = {}
                tmp_step_detail = json_data_info['step_detail']
                tmp_arr_step_detail_2 = tmp_step_detail[s]
                oneMail = str(json_data_info['step_detail'][s]['one_email']).replace(' ','').lower()
                tmp_step_del_1 = int(step_num) - 1
                step_num_int2 = int(step_num)
                tmp_list_email.append(oneMail)
                tmp_activity_code = tmp_arr_step_detail_2['activity_code']
                tmp_activity_status = tmp_arr_step_detail_2['activity_status']
                for hh in range(len(tmp_activity_code)):
                    if tmp_activity_code[hh] == 'A03':
                        tmp_get_status = tmp_activity_status[hh]
                        if tmp_get_status == 'Reject':
                            str_status_email = 'R'
                        elif tmp_get_status == 'Incomplete' or tmp_get_status == 'Pending':
                            str_status_email = 'N'
                        elif tmp_get_status == 'Complete' or tmp_get_status == 'Approve':
                            str_status_email = 'Y'
                        tmp_email_status.append(str_status_email)
                tmp_json_step['email'] = tmp_list_email
                tmp_json_step['step_num'] = step_num
                step_status_code = 'Y'
                if tmp_status_sum[tmp_step_del_1] == 'Reject':
                    step_status_code = 'R'
                elif tmp_status_sum[tmp_step_del_1] == 'Incomplete':
                    step_status_code = 'N'
                elif tmp_status_sum[tmp_step_del_1] == 'Complete':
                    step_status_code = 'Y'
                if step_num == '1' and step_status_code == 'N':
                    step_status_code = 'W'
                
                if step_status_code == 'W':
                    step_now = int(step_num)
                tmp_json_step['step_status_code'] = step_status_code
                tmp_json_step['status'] = tmp_email_status
                tmp_json_step['step_status'] = tmp_status_sum[tmp_step_del_1]
            tmp_list_status_document.append(step_status_code)
            result_list_sum.append(tmp_json_step)
            if 'R' in tmp_list_status_document:
                status_document = 'R'
            elif 'N' in tmp_list_status_document:
                status_document = 'N'
            elif 'Y' in tmp_list_status_document:
                status_document = 'Y'
            else:
                status_document = 'N'
            result_to_user = {
                'data_document':result_list_sum,
                'status_document':status_document,
                'max_step':1,
                'step_now':step_now
            }                                    
    else:
        step_now = 0
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
        tmp_status_sum = []
        arr_email_list = []
        email_step_sum = []
        tmp_list_status_document = []
        status_document = ''
        result_to_user = []
        for i in range(len(step_infomation)):
            list_check_step = []
            json_step_info_2 = {}
            step_list_data = []
            step_status = []
            step_email = []
            step_ = step_infomation[i]
            step_num = step_infomation[i]['step_num']
            json_step_info_2['step_status'] = ''
            tmp_step_detail = step_['step_detail']
            for u in range(len(tmp_step_detail)):
                tmp_arr_step_detail = tmp_step_detail[u]
                tmp_status = tmp_arr_step_detail['activity_status']
                tmp_code = tmp_arr_step_detail['activity_code']
                tmp_email = str(tmp_arr_step_detail['one_email']).replace(' ','').lower()
                for s in range(len(tmp_code)):
                    if tmp_code[s] == 'A03' or tmp_code[s] == 'A04':
                        step_status.append(tmp_status[s])
                        step_email.append(tmp_email)
            email_step_sum.append(step_email)
            if 'Reject' in step_status:
                tmp_status_sum.append('Reject')
            elif 'Approve' in step_status:
                tmp_status_sum.append('Complete')
            elif 'Complete' in step_status:
                tmp_status_sum.append('Complete')
            elif 'Incomplete' in step_status:
                tmp_status_sum.append('Incomplete')
            elif 'Pending' in step_status:
                tmp_status_sum.append('Incomplete')
            else:
                tmp_status_sum.append('Complete')
        for zzi in range(len(step_infomation)):
            tmp_list_step = []
            tmp_json_step = {}
            tmp_list_email = []
            tmp_email_status = []
            list_check_step = []
            json_step_info_2 = {}
            step_list_data = []
            step_status = []
            str_status_email = ''
            step_ = step_infomation[zzi]
            step_num = step_infomation[zzi]['step_num']
            index_step_num = zzi
            json_step_info_2['step_status'] = ''
            tmp_step_detail = step_['step_detail']
            for zi in range(len(tmp_step_detail)):
                tmp_arr_step_detail_2 = tmp_step_detail[zi]
                oneMail = str(tmp_arr_step_detail_2['one_email']).replace(' ','').lower()
                tmp_step_del_1 = int(step_num) - 1
                step_num_int2 = int(step_num)
                tmp_list_email.append(oneMail)
                tmp_activity_code = tmp_arr_step_detail_2['activity_code']
                tmp_activity_status = tmp_arr_step_detail_2['activity_status']
                for hh in range(len(tmp_activity_code)):
                    if tmp_activity_code[hh] == 'A03':
                        tmp_get_status = tmp_activity_status[hh]
                        if tmp_get_status == 'Reject':
                            str_status_email = 'R'
                        elif tmp_get_status == 'Incomplete' or tmp_get_status == 'Pending':
                            str_status_email = 'N'
                        elif tmp_get_status == 'Complete' or tmp_get_status == 'Approve':
                            str_status_email = 'Y'
                        tmp_email_status.append(str_status_email)
                    if tmp_activity_code[hh] == 'A04':
                        tmp_get_status = tmp_activity_status[hh]
                        if tmp_get_status == 'Reject':
                            str_status_email = 'R'
                        elif tmp_get_status == 'Incomplete' or tmp_get_status == 'Pending':
                            str_status_email = 'N'
                        elif tmp_get_status == 'Complete' or tmp_get_status == 'Approve':
                            str_status_email = 'Y'
                        tmp_email_status.append(str_status_email)
                tmp_json_step['email'] = tmp_list_email
                tmp_json_step['step_num'] = step_num
                step_status_code = 'Y'
                # print(tmp_status_sum)
                if tmp_status_sum[tmp_step_del_1] == 'Reject':
                    step_status_code = 'R'
                elif tmp_status_sum[tmp_step_del_1] == 'Incomplete':
                    step_status_code = 'N'
                elif tmp_status_sum[tmp_step_del_1] == 'Complete':
                    step_status_code = 'Y'
                # if step_num == '1' and step_status_code == 'N':
                #     step_status_code = 'W'
                tmp_json_step['step_status_code'] = step_status_code
                tmp_json_step['step_status'] = tmp_status_sum[tmp_step_del_1]
                tmp_json_step['status'] = tmp_email_status
                
            tmp_list_status_document.append(step_status_code)
            result_list_sum.append(tmp_json_step)
        
        if 'R' in tmp_list_status_document:
            status_document = 'R'
            step_now = max_step
        elif 'N' in tmp_list_status_document:
            status_document = 'N'
        elif 'Y' in tmp_list_status_document:
            status_document = 'Y'
            step_now = max_step
        else:
            status_document = 'Y'
        if status_document == 'N':
            for uu in range(len(result_list_sum)):
                tmp_step_num = result_list_sum[uu]['step_num']
                tmp_email = result_list_sum[uu]['email']
                tmp_step_status_code = result_list_sum[uu]['step_status_code']
                tmp_index_step_next = int(tmp_step_num)
                # step_now = int(tmp_step_num)
                if tmp_step_status_code == 'Y':   
                    temp_detail = result_list_sum   
                    temp_detail[uu]['step_status_code'] = 'N'                 
                    if temp_detail[tmp_index_step_next]['step_status_code'] != 'Y':
                        if temp_detail[tmp_index_step_next]['step_status_code'] == 'N':
                            temp_detail[tmp_index_step_next]['step_status_code'] = 'W'
                        for z in range(tmp_index_step_next,len(temp_detail),1):
                            tmp_step_num = temp_detail[z]['step_num']
                            tmp_email = temp_detail[z]['email']
                            tmp_step_status_code = temp_detail[z]['step_status_code']
                            if tmp_step_status_code == 'N':
                                temp_detail[z]['step_status_code'] = 'Z'
                if tmp_step_num == '1' and tmp_step_status_code == 'N':
                    step_now = int(tmp_step_num)
                    result_list_sum[uu]['step_status_code'] = 'W'
                    for z in range(tmp_index_step_next,len(result_list_sum),1):
                        if tmp_step_status_code == 'N':
                            result_list_sum[z]['step_status_code'] = 'Z'
                if tmp_step_status_code == 'W':
                    step_now = int(tmp_step_num)
                # else:
                #     step_now = int(tmp_step_num)
                        
                            # print(temp_detail[z])
            # print(temp_detail)
            # print(result_list_sum)
        result_to_user = {
            'data_document':result_list_sum,
            'status_document':status_document,
            'max_step':max_step,
            'step_now':step_now
        }
    return {'result':'OK','messageText':result_to_user}

def cal_dataJson_stepWH_v1(data_json):
    try:
        arr_tmp = []
        if 'step_detail' in data_json:
            arr_tmp.append(data_json)
            data_json = arr_tmp
        arr_result = []
        for n in range(len(data_json)):
            arr_status = []
            # print(data_json[n])
            arr_email = []
            arr_time = []
            tmpdata = data_json[n]
            tmp_stepnum = tmpdata['step_num']
            tmp_step_detail = tmpdata['step_detail']
            tmprf_step = tmpdata['rf_step']
            # statusApprove = False
            for u in range(len(tmp_step_detail)):
                tmpstepdetail =  tmp_step_detail[u]
                tmponeemail = tmpstepdetail['one_email']
                tmpactivity_code = tmpstepdetail['activity_code']
                # tmpactivity_time = None
                if tmponeemail != '':
                    for z in range(len(tmpactivity_code)):
                        if tmpactivity_code[z] == "A03":
                            tmpemail = tmponeemail
                            tmpactivity_time = None
                            tmpactivity_status = tmpstepdetail['activity_status'][z]
                            # print(tmpactivity_status)
                            if tmpactivity_status == "Approve":
                                tmpemail = tmponeemail
                                tmpactivity_time = tmpstepdetail['activity_time'][z]
                            elif tmpactivity_status == "Complete":
                                tmpemail = tmponeemail
                                tmpactivity_time = tmpstepdetail['activity_time'][z]
                            arr_status.append(tmpactivity_status)
                            arr_time.append(tmpactivity_time)
                            # else:
                            #     if tmpactivity_time == None:
                            #         tmpemail = tmponeemail
                            #         tmpactivity_time = None
                    arr_email.append(tmponeemail)
            arr_name = fine_name_surename_list(arr_email)
            approve_name = fine_name_surename(tmpemail)
            for x in range(len(arr_status)):
                if arr_status[x] == 'Complete' or arr_status[x] == 'Approve':
                    tmpactivity_status = 'Complete'
                    tmpemail = arr_email[x]
                    tmpactivity_time = arr_time[x]
                    approve_name = fine_name_surename(tmpemail)
            res = {
                "step_num":tmp_stepnum,
                "one_email":arr_email,
                "name_surname":arr_name,
                "approve_time":tmpactivity_time,
                "email_approve":tmpemail,
                "name_approve":approve_name,
                "status":tmpactivity_status,
                "ref_step":tmprf_step,
                # "status":arr_status
            }
            arr_result.append(res)
        return {'result':'OK','messageText':arr_result}
    except Exception as e:
        print(str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result': 'ER', 'messageText': str(e),'status_Code':200}

def cal_status_group_v1(group_status):
    try:
        arr_status = []
        for u in range(len(group_status)):
            tmpdata = group_status[u]
            tmpstatus = tmpdata['status']
            arr_status.append(tmpstatus)
        tmplenstatus = len(arr_status)
        status_sum = "N"
        if arr_status.count("Complete") == tmplenstatus:
            status_sum = "Y"
        return {'result':'OK','messageText':status_sum}
    except Exception as e:
        return {'result':'ER','messageText':str(e)}