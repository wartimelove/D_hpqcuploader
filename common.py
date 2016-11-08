from __future__ import division

__author__ = 'ruipengx'

import re
import math,csv
import time
from HPQC_API import create_case_to_hpqc
from HPQC_API import update_case_to_hpqc

"""
    PnP
        Performance                                                                (test_case_id,  test_case_order)
            MLC Bandwidth scaling - DelayScaling (20000 delay)_BW                  (2536, 1)
            MLC Bandwidth scaling - DelayScaling (20000 delay)_Latency(ns)         (2535, 2)
            MLC Bandwidth scaling -ThreadScaling_allThreads_BW                     (2538, 3)
            MLC Bandwidth scaling -ThreadScaling_allThreads_Latency(ns)            (2537, 4)
            MLC local idle latency (ns)                                            (2531, 5)
            MLC local peak BW (GB per sec)                                         (2533, 6)
            MLC remote idle latency (ns)                                           (2532, 7)
            MLC remote peak BW (GB per sec)                                        (2534, 8)
            MP Linpack (Gflops per sec)                                            (2529, 9)
            SPEC CPU 2006 speed disable autoparallelization_float                  (2540, 10)
            SPEC CPU 2006 speed disable autoparallelization_int                    (2539, 11)
            SPECfp_rate(score)                                                     (2542, 12)
            SPECint_rate (score)                                                   (2541, 13)
            Stream Triad (GB per sec)                                              (2530, 14)
            Boot Time to Redhat (second)	                                          (7089, 15)
            Boot Time to Suse (second)	                                          (7088, 16)
            Boot Time to UEFI (second)	                                          (7087, 17)
            Boot Time to windows (second)                                          (7090, 18)
            micperf DGEMM on Redhat (Gflops per sec)	                            (7072, 19)
            micperf DGEMM on Suse (Gflops per sec)	                                (7068, 20)
            micperf HPLINPACK on Redhat(Gflops per sec)	                         (7075, 21)
            micperf HPLINPACK on Suse(Gflops per sec)	                            (7071,	 22)
            micperf SGEMM on Redhat (Gflops per sec)	                            (7073, 23)
            micperf SGEMM on Suse (Gflops per sec)	                                (7069, 24)
            micperf STREAM on Redhat (GB per sec)	                                (7074, 25)
            micperf STREAM on Suse (GB per sec)	                                   (7070, 26)
            Trinity MiniApp AMG (speed vs hopper)	                                (7082,27)
            Trinity MiniApp Geomean score (speed vs hopper)	                      (7084,28)
            Trinity MiniApp GTC (speed vs hopper)	                                (7078,29)
            Trinity MiniApp MILC (speed vs hopper)	                                (7079,30)
            Trinity MiniApp MiniDFT small size (speed vs hopper)	                  (7083,31)
            Trinity MiniApp MiniFe (speed vs hopper)	                            (7081,	32)
            Trinity MiniApp miniGhost (speed vs hopper)	                         (7080, 33)
            Trinity MiniApp SNAP (speed vs hopper)	                                (7077, 34)
            Trinity MiniApp UMT (speed vs hopper)                                  (7076,	 35)

        Power
            Average Core Frequency(MHz)                                            (4089, 36)
            Normalized Score                                                       (4090, 37)
            SPECpower 100 precent load (ssj_ops)                                   (2527, 38)
            SPECpower Active Idle (W)                                              (2528, 39)
            SPECpower score                                                        (2526, 40)

"""

## intel week time is different with system define.
#test_week = str(int(time.strftime("%W")) + 1)
#test_time = time.strftime("%Y"+"WW"+test_week)
#test_time = time.strftime("%Y"+"WW"+"%W")

case_info = {   'hpqc_project'    : 'Test_HPQC',
                    'work_week'       : '2016WW13',
                    'test_set_name'   : 'PnP-QJL9',
                    'test_case_id'    : '4090',
                    'test_case_order' : '16',
                    'test_case_value' : '',
                    'test_case_unit'  : 'MB/Sec',
                    'test_case_hsd'   : '',
                    'test_status'     : 'Passed',
                    'test_iterations' : '3',
                    'test_exec_date'  : '2016-04-22'
                    #'subtype_id'       :  'AUTO'

                }

help_info = '''For upload_pnp_result,support long option [--file,--project,--line],and short option -h.
e.x "python upload_pnp_result.py --file=P&P2QC.csv --line=5, --test_week=2016WW24"'''

upload_fail_case = []

def update_case_info(key,value):

    case_info.update({ key : value })
    #print case_info

def update_case_series(series,project=None,week=None):

    update_case_info('hpqc_project',series[3])
    update_case_info('work_week',series[4])
    update_case_info('test_set_name',series[5])
    update_case_info('test_case_id',series[1])
    update_case_info('test_case_order',series[2])
    update_case_info('test_case_value',series[6])
    update_case_info('test_case_unit',series[7])
    update_case_info('test_case_hsd',series[8])
    update_case_info('test_status',series[9])
    update_case_info('test_iterations',series[10])
    update_case_info('test_exec_date',series[11])
    if project:
        update_case_info('hpqc_project',project)
    if week:
        update_case_info('work_week',week)
    #print case_info

def update_info(case_info):
    ret_update = update_case_to_hpqc(case_info)
    if ret_update==1:
            print 'update success!'
    else:
            print 'update fail!'
            upload_fail_case.append(case_info['test_case_id'])


def upload_result_hpqc(case_info):
    if case_info.get('test_case_value'):
        print "Uploading case",case_info.get('test_case_id') ,"..."*30
        ret = create_case_to_hpqc(case_info)
        if ret == 1:
            print 'create success!'
            update_info(case_info)
        elif ret == -1:
            print 'create fail!'
            upload_fail_case.append(case_info['test_case_id'])
            with open('upload_fail.csv', 'wb') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(upload_fail_case)
			
        else:
            update_info(case_info)
			

    else:
        return None



def mlc_bandwidth_delayscaling_20000_bw(results):
    test_scores=[]
    for result in results:
        if '20000_bw(MB/s)' in result and 'loaded_latency' in result:
            test_case_score=float(result[-1])
            #print test_case_value
            test_case_id=2536
            test_case_order=1
            test_case_unit='MB/s'
            #update_case_to_hpqc(test_case_id,test_case_order,test_case_value,test_case_unit)
            print test_case_score
            test_scores.append(test_case_score)
    test_case_value =  round(sum(test_scores)/len(test_scores),2)
    print test_case_value

    upload_result_hpqc(test_case_id,test_case_order,test_case_value,test_case_unit)

def mlc_bandwidth_delayscaling_20000_latency(results):
    test_scores=[]
    for result in results:
        if '20000_lat(ns)' in result and 'loaded_latency' in result:
            test_case_score=float(result[-1])
            test_case_id=2535
            test_case_order=2
            test_case_unit='ns'
            # upload_result_hpqc(test_case_id,test_case_order,test_case_value,test_case_unit)
            print test_case_score
            test_scores.append(test_case_score)
        #print test_case_value
    #test_case_value =  round(sum(test_scores)/len(test_scores),2)
    #print test_case_value

def mlc_threadscaling_allThreads_bw(results):
    test_scores=[]
    for result in results:
        if '00000_bw(MB/s)' in result and 'RunAll' in result:
            test_case_score=float(result[-1])
            test_case_id=2538
            test_case_order=3
            test_case_unit='MB/s'
            # upload_result_hpqc(test_case_id,test_case_order,test_case_value,test_case_unit)
            print test_case_score
            test_scores.append(test_case_score)
        #print test_case_value
    #test_case_value =  round(sum(test_scores)/len(test_scores),2)
    #print test_case_value

def mlc_threadscaling_allThreads_latency(results):
    test_scores=[]
    for result in results:
        if '00000_lat(ns)' in result and 'RunAll' in result:
            test_case_score=float(result[-1])
            test_case_id=2537
            test_case_order=4
            test_case_unit='ns'
            # upload_result_hpqc(test_case_id,test_case_order,test_case_value,test_case_unit)
            print test_case_score
            test_scores.append(test_case_score)
        #print test_case_value
    #test_case_value =  round(sum(test_scores)/len(test_scores),2)
    #print test_case_value

def mp_linpack(results):
    test_scores=[]
    for result in results:
         if 'Linpack Score(GFlops)' in result:
            print result[-1]
            test_case_score=float(result[-1])
            test_case_id=2529
            test_case_order=9
            test_case_unit='GFlops'
            # upload_result_hpqc(test_case_id,test_case_order,test_case_value,test_case_unit)
            print test_case_score
            test_scores.append(test_case_score)

    #test_case_value =  round(sum(test_scores)/len(test_scores),2)
    #print test_case_value


def mlc_local_idle_latency(results):
    test_scores=[]
    for result in results:
        if 'Latency_matrix' in result and 'Skt0-Skt0' in result:
            test_case_score=float(result[-1])
            test_case_id=2531
            test_case_order=5
            test_case_unit='ns'
          #  upload_result_hpqc(test_case_id,test_case_order,test_case_value,test_case_unit)
            print test_case_score
            test_scores.append(test_case_score)
    #test_case_value =  round(sum(test_scores)/len(test_scores),2)
    #print test_case_value


def mlc_remote_idle_latency(results):
    test_scores=[]
    for result in results:
        if 'Latency_matrix' in result and 'Skt0-Skt1' in result:
            test_case_score=float(result[-1])
            test_case_id=2532
            test_case_order=7
            test_case_unit='ns'
          #  upload_result_hpqc(test_case_id,test_case_order,test_case_value,test_case_unit)
            print test_case_score
            test_scores.append(test_case_score)
    #test_case_value =  round(sum(test_scores)/len(test_scores),2)
    #print test_case_value


def mlc_local_peak_bw(results):
    test_scores=[]
    for result in results:
        if 'Bandwidth_matrix' in result and 'Skt0-Skt0' in result:
            test_case_score=float(result[-1])
            test_case_id=2533
            test_case_order=6
            test_case_unit='GB/s'
           # upload_result_hpqc(test_case_id,test_case_order,test_case_value,test_case_unit)
            print test_case_score
            test_scores.append(test_case_score)
    #test_case_value =  round(sum(test_scores)/len(test_scores),2)
    #print test_case_value/1000


def mlc_remote_peak_bw(results):
    test_scores=[]
    for result in results:
        if 'Bandwidth_matrix' in result and 'Skt0-Skt1' in result:
            test_case_score=float(result[-1])
            test_case_id=2534
            test_case_order=8
            test_case_unit='GB/s'
            #upload_result_hpqc(test_case_id,test_case_order,test_case_value,test_case_unit)
            print test_case_score
            test_scores.append(test_case_score)
    #test_case_value =  round(sum(test_scores)/len(test_scores),2)
    #print test_case_value/1000

def stream_triad(results):
    test_scores=[]
    test_iterations=[]
    for result in results:
        if 'NTW_Bandwidth' in result and 'Triad' in result:
            test_iteration = int(result[3])
            test_case_score=float(result[-1])
            test_case_id=2530
            test_case_order=14
            test_case_unit='GB/s'
            print test_case_score
            test_iterations.append(test_iteration)
            test_scores.append(test_case_score)
    print test_iterations
    test_iteration =  max(test_iterations) + 1
    print test_iteration
    test_case_value =  round(sum(test_scores)/len(test_scores),1)
    print test_case_value
    #update_case_info('work_week',test_time)
    #update_case_info('test_case_id',test_case_id)
    #update_case_info('test_case_order',test_case_order)
    #update_case_info('test_case_value',test_case_value)
    #update_case_info('test_case_unit',test_case_unit)
    #update_case_info('test_iterations',test_iteration)
    #upload_result_hpqc(case_info)

def speccpu_hammer_rate(results):
    test_scores=[]
    for result in results:
        if '456.hmmer' in result and 'Score' in result :
            #value_list =
            test_case_score=float(result[-1])
            #print test_case_value
            test_case_id=2530
            test_case_order=14
            test_case_unit='GB/s'
            print test_case_score
            test_scores.append(test_case_score)
          #  upload_result_hpqc(test_case_id,test_case_order,test_case_value,test_case_unit)
    #test_case_value =  round(sum(test_scores)/len(test_scores),2)
    #print test_case_value

def speccpu_int_rate(results):
    test_scores=[]
    for result in results:
            if  'Score' in result:
                test_case_id=2541
                test_case_order=13
                test_case_unit='score'
                count = 0
                for n in result:
                    if re.search('rate', n) :
                            #and re.search('CINT',n):
                        test_case_score=float(result[-1])
                        #print test_case_score

                        test_scores.append(test_case_score)
                        break
    test_score_pro = 1
    test_scores = test_scores[0:12]
    print test_scores
    for i in test_scores:
        test_score_pro = test_score_pro * float(i)
    print len(test_scores)
    test_case_value = pow(test_score_pro,1/len(test_scores))
    print test_case_value


    #end_value = pow(test_score_pro,1/len(test_score))
   #print end_value

def speccpu_fp_rate(results):
    test_scores=[]
    for result in results:
            if  'Score' in result:
                test_case_id=2541
                test_case_order=13
                test_case_unit='score'
                count = 0
                for n in result:
                    if re.search('rate', n) :
                            #and re.search('CINT',n):
                        test_case_score=float(result[-1])
                        #print test_case_score

                        test_scores.append(test_case_score)
                        break
    test_score_pro = 1
    test_scores = test_scores[12:29]
    print test_scores
    for i in test_scores:
        test_score_pro = test_score_pro * float(i)
    print len(test_scores)
    test_case_value = pow(test_score_pro,1/len(test_scores))
    print test_case_value

    

def speccpu_int_speed(results):
    test_scores=[]
    for result in results:
            if  'Score' in result:
                test_case_id=2541
                test_case_order=13
                test_case_unit='score'
                count = 0
                for n in result:
                    if re.search('speed', n) :
                            #and re.search('CINT',n):
                        test_case_score=float(result[-1])
                        #print test_case_score

                        test_scores.append(test_case_score)
                        break
    test_score_pro = 1
    test_scores = test_scores[0:12]
    print test_scores
    for i in test_scores:
        test_score_pro = test_score_pro * float(i)
    print len(test_scores)
    test_case_value = pow(test_score_pro,1/len(test_scores))
    print test_case_value



def speccpu_fp_speed(results):
    test_scores=[]
    for result in results:
            if  'Score' in result:
                test_case_id=2541
                test_case_order=13
                test_case_unit='score'
                count = 0
                for n in result:
                    if re.search('speed', n) :
                            #and re.search('CINT',n):
                        test_case_score=float(result[-1])
                        #print test_case_score

                        test_scores.append(test_case_score)
                        break
    test_score_pro = 1
    test_scores = test_scores[12:29]
    print test_scores
    for i in test_scores:
        test_score_pro = test_score_pro * float(i)

    print len(test_scores)
    test_case_value = pow(test_score_pro,1/len(test_scores))
    print test_case_value

def cpu_100percent(results):
    csv_values=[]
    for result in results:
            csv_value=result[4]
            csv_values.append(csv_value)
    test_score=[]
    for value in csv_values[1:]:
        test_frequency = float(value)
        test_score.append(test_frequency)
    print len(test_score)
    test_case_value =  round(sum(test_score)/len(test_score),3)
    print test_case_value

