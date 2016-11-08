# -*- coding: utf-8 -*-
from __future__ import division

#from __future__ import division
import os
import xdrlib ,sys
import xlrd,xlwt
import csv
import time


from HPQC_API import create_case_to_hpqc
from HPQC_API import update_case_to_hpqc
from common import *


def update(case_name):
    #result_file = file('20160524_PTU-CPU.csv', 'rb')
    result_file = file('scores.csv', 'rb')
    try:
        results = csv.reader(result_file)
        case_name(results)

    except IOError:
        pass
    finally:
        result_file.close()

def main():
    #update(mlc_bandwidth_delayscaling_20000_bw)
    #update(mlc_bandwidth_delayscaling_20000_latency)
    #update(mlc_threadscaling_allThreads_bw)
    #update(mlc_threadscaling_allThreads_latency)
    #update(mp_linpack)
    #update(mlc_local_idle_latency)
    #update(mlc_remote_idle_latency)
    #update(mlc_local_peak_bw)
    #update(mlc_remote_peak_bw)
    update(stream_triad)
    #update(speccpu_hammer_rate)
    #update(speccpu_int_rate)
    #update(speccpu_fp_rate)
    #update(speccpu_int_speed)
    #update(speccpu_fp_speed)


    #update(cpu_100percent)


if __name__ == "__main__":
        main()
