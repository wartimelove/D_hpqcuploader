# -*- coding: utf-8 -*-
from __future__ import division

__author__ = 'ruipengx'

#from __future__ import division
import os,time
#import xdrlib ,sys
#import xlrd,xlwt
import csv,sys
import getopt


from HPQC_API import create_case_to_hpqc
from HPQC_API import update_case_to_hpqc
from common import *

def upload(local_csv,line=None,project=None,test_week=None):
#def upload(local_csv,**keyword):
    filename = local_csv
    #if keyword.has_key('line'):
    #    print keyword['name']
    #else:
    #    print "no line"
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                if line:
                    if reader.line_num == int(line):
                        update_case_series(row,project=project,week=test_week)
                        upload_result_hpqc(case_info)
                        break
                    else:
                        continue
                else:
                    if reader.line_num == 1:
                        continue
                    else:
                        update_case_series(row,project=project,week=test_week)
                        upload_result_hpqc(case_info)

        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

def auto_upload_process():
    csv_file = "P&P_result.csv"
    upload(csv_file)


if __name__ == "__main__":
    csv_file = "P&P2QC.csv"
    #if len(sys.argv[1:]) == 1:

     #   csv_file = sys.argv[1]
     #   upload(csv_file)
    if len(sys.argv[1:]) == 0:
        upload(csv_file)
    else:
        short_opt = 'c:hn:d'
        long_opt = ['line=','test_week=','project=','file=']
        opts, args = getopt.getopt(sys.argv[1:], short_opt, long_opt)
        line=''
        project=''
        test_week=''
        for op,value in opts:
            if op == '-h':
                print help_info
                os._exit(0)
            if op == '--line':
                line = value
            elif op == "--file":
                csv_file = value
            elif op == "--project":
                project = value
            elif op == "--test_week":
                test_week = value
            else:
                continue
        upload(csv_file,line=line,project=project,test_week=test_week)
