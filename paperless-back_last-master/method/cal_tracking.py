# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config

def get_random_string(length):
    random_list = []
    for i in range(length):
        random_list.append(random.choice(
            string.ascii_uppercase + string.digits))
    return random_list

def gen_digit_tracking(tracking):
    list_char = []
    list_char_new = []
    num_count = 13
    sum_digit = 0
    try:
        for i in range(len(tracking)):
            char = tracking[i]
            check_int = char.isnumeric()
            if check_int == False:
                char = int(ord(char))
            elif check_int == True:
                char = int(char)
            list_char.append(char)
            char = char*num_count
            num_count = num_count-1
            list_char_new.append(char)
        for j in range(len(list_char_new)):
            # print ('list_char_new',list_char_new[j])
            sum_digit = sum_digit+list_char_new[j]
        sum_digit = (sum_digit % 11)
        sum_digit = abs(11 - sum_digit)
        str_sum_digit = str(sum_digit)
        last_digit = str_sum_digit[-1]
        tracking_new = tracking+last_digit
        return {'result':'OK','status_Code':200,'messageText':str(tracking_new)}
    except Exception as e:
        print(str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','status_Code':200,'messageText':str(e)}

def check_digit_tracking(tracking):
    list_char = []
    list_char_new = []
    num_count = 13
    sum_digit = 0
    last_tracking = tracking[-1]
    first_digit = tracking[:-1]
    try:
        for i in range(len(first_digit)):
            char = first_digit[i]
            check_int = char.isnumeric()
            if check_int == False:
                char = int(ord(char))
            elif check_int == True:
                char = int(char)
            list_char.append(char)
            char = char*num_count
            num_count = num_count-1
            list_char_new.append(char)
        for j in range(len(list_char_new)):
            # print ('list_char_new',list_char_new[j])
            sum_digit = sum_digit+list_char_new[j]
        sum_digit = (sum_digit % 11)
        sum_digit = abs(11 - sum_digit)
        str_sum_digit = str(sum_digit)
        last_digit = str_sum_digit[-1]
        if str(last_digit) == str(last_tracking):
            check_digit = True
        else:
            check_digit = False
        return check_digit
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','status_Code':200,'messageText':str(e)}