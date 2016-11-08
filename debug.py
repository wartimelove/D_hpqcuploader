#!/usr/bin/python
# -*- coding: UTF-8 -*-



from hpqcuploader import PnP2HPQC



scoresFilePath = 'C:\\SVSHARE\\Maple\\Results\\weekly_performance_2016_11_01__10_25_51\\scores.csv'




if __name__ == "__main__":
    PnP2HPQC.auto_upload(scoresFilePath)