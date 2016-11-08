#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv,  codecs, cStringIO
import os,sys,time
from config import *
from filter_score import *
from upload_pnp_result import *


test_week = '2016WW' + str(int(time.strftime("%W")) + 1)


def write_csv():

    with open('P&P_format.csv', 'wb') as f:
        fieldnames = ['test_case_name','test_case_id', 'test_case_order','hpqc_project','work_week','test_set_name','test_case_value','test_case_unit','test_case_hsd','test_status','test_iterations','test_exec_date']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for case in case_list:
            case.update(platform_info)
            if work_week:
                case.update(work_week)
            else:
                case.update({'work_week':test_week})
            if case['test_case_id'] in case_list_A:
                case.update({'test_set_name':test_set[0]})
            elif case['test_case_id'] in case_list_B:
                case.update({'test_set_name':test_set[1]})
            else:
                print "no defined case id"
            writer.writerow(case)

def remove_tmp(dir,postfix):


    if os.path.isdir(dir):
        for file in os.listdir(dir):
            remove_tmp(dir+'/'+file,postfix)
    else:
        if os.path.splitext(dir)[1] == postfix:
            os.remove(dir)

def auto_upload(raw_result):
    write_csv()
    parse_score(raw_result)
    auto_upload_process()
    print case_info




#if __name__ == "__main__":
#    write_csv()
#    currDir = sys.path[0]
#    print currDir
#    parse_score()
#    auto_upload()
    #parse_score()
    #result_file_name = "P&P2QC"
    #os.remove(result_file_name,".csv")
    #remove_tmp(currDir,".csv")