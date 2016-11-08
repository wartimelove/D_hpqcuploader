#!/usr/bin/python
# -*- coding: UTF-8 -*-


import os
import string
import csv
import time

def geomean(l):
    result = 1
    for i in range(len(l)):
        result = result * pow(float(l[i]), 1 / float(len(l)))
    return result


def median(l):
    if len(l) < 1:
        return None
    else:
        return sorted(l)[len(l) / 2]


def setresult(outputlist, position, score, iteration):
    outputlist[position]['test_case_value'] = str(score)
    #outputlist[position]['work_week'] = '2016WW' + str(week)
    outputlist[position]['test_iterations'] = iteration
    outputlist[position]['test_exec_date'] = time.strftime('%Y-%m-%d', time.localtime())
    outputlist[position]['test_status'] = 'Passed'


def result_process(inputlist, outputlist, position_out, result, first_condition, first_field, second_condition='d', second_field='Configuration', err=0, third_condition='d', third_field='Configuration'):
    subresult = []
    iteration = '0'
    for position_in in range(len(inputlist)):
        rows_in = inputlist[position_in]
        if first_condition in rows_in[first_field]:
            if second_condition in rows_in[second_field]:
                if third_condition in rows_in[third_field]:
                    if iteration != rows_in[' Iteration']:
                        iteration = rows_in[' Iteration']
                        if len(subresult) != 0:
                            result.append(geomean(subresult))
                        subresult = []
                    subresult.append(inputlist[position_in + err][' ScoreValue'])
    if len(subresult) != 0:
        result.append(geomean(subresult))
    if len(result) == 0:
        print 'Score not found!'
    else:
        setresult(outputlist, position_out, median(result), int(iteration) + 1)

def parse_score(raw_result):
    with open(raw_result) as f:
        f_dic = csv.DictReader(f)
        inputlist = list(f_dic)


    with open('P&P_format.csv') as f:
        f_csv = csv.reader(f)
        headings = next(f_csv)
        f.seek(0, 0)
        f_dic = csv.DictReader(f)
        outputlist = list(f_dic)


    for position_out in range(len(outputlist)):
        rows_out = outputlist[position_out]
        result = []
        if rows_out['test_case_id'] == '2529':
            result_process(inputlist, outputlist, position_out, result, 'Linpack Score', ' ScoreName')

        if rows_out['test_case_id'] == '2531':
            result_process(inputlist, outputlist, position_out, result, 'Skt0-Skt0', ' ScoreName', 'Latency_matrix', ' Subworkload')

        if rows_out['test_case_id'] == '2532':
            result_process(inputlist, outputlist, position_out, result, 'Skt0-Skt1', ' ScoreName', 'Latency_matrix', ' Subworkload')

        if rows_out['test_case_id'] == '2533':
            result_process(inputlist, outputlist, position_out, result, 'Skt0-Skt0', ' ScoreName', 'Bandwidth_matrix', ' Subworkload')

        if rows_out['test_case_id'] == '2534':
            result_process(inputlist, outputlist, position_out, result, 'Skt0-Skt1', ' ScoreName', 'Bandwidth_matrix', ' Subworkload')

        if rows_out['test_case_id'] == '2535':
            result_process(inputlist, outputlist, position_out, result, '20000_lat(ns)', ' ScoreName', 'RunAll', ' Subworkload')

        if rows_out['test_case_id'] == '2536':
            result_process(inputlist, outputlist, position_out, result, '20000_bw(MB/s)', ' ScoreName', 'RunAll', ' Subworkload')

        if rows_out['test_case_id'] == '2537':
            result_process(inputlist, outputlist, position_out, result, '00000_lat(ns)', ' ScoreName', 'RunAll', ' Subworkload')

        if rows_out['test_case_id'] == '2538':
            result_process(inputlist, outputlist, position_out, result, '00000_bw(MB/s)', ' ScoreName', 'RunAll', ' Subworkload')

        if rows_out['test_case_id'] == '2541':
            result_process(inputlist, outputlist, position_out, result, 'NumCopies=2', ' Parameters', 'CINT', ' ScoreValue', 1)

        if rows_out['test_case_id'] == '2542':
            result_process(inputlist, outputlist, position_out, result, 'NumCopies=2', ' Parameters', 'CFP', ' ScoreValue', 1)

        if rows_out['test_case_id'] == '7085':
            result_process(inputlist, outputlist, position_out, result, 'NumCopies=1', ' Parameters', 'CFP', ' ScoreValue', 1)

        if rows_out['test_case_id'] == '7086':
            result_process(inputlist, outputlist, position_out, result, 'NumCopies=1', ' Parameters', 'CINT', ' ScoreValue', 1)

        if rows_out['test_case_id'] == '2530':
            result_process(inputlist, outputlist, position_out, result, 'Triad', ' ScoreName', 'streamServer', ' Workload')

        if rows_out['test_case_id'] == '8492':
            result_process(inputlist, outputlist, position_out, result, 'NumCopies=2', ' Parameters', 'CINT', ' ScoreValue', 1, '456.hmmer', ' Subworkload')


###########################
    with open('P&P_result.csv', 'wb') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headings)
        f_dic = csv.DictWriter(f, headings)
        f_dic.writerows(outputlist)



