#!/usr/bin/python
# coding: utf-8

import string
import sys
import xlwt
import time
import multiprocessing
from jenkinsapi.jenkins import *
from jenkinsapi.job import *
from jenkinsapi.build import Build
from jenkinsapi.utils.crumb_requester import CrumbRequester

def run():
    var = input("請輸入需要build的project : (e.g.RD1_H5_Client_25_Build or ALL)" )
    print("You entered " + str(var))
    if var == 'ALL':
        i=0
        pn=[]
        with open ('data.txt','r') as f:
            for line in f:
                line=line.strip('\n')
                pn.append(list(map(str,line.split(','))))
                print (len(pn))
            for i in range (len(pn)):
                project=str(pn[0][i])
                tag=str(pn[1][i])
                buildType=str(pn[2][i])
                multi(project, tag, buildType)
                print (pn[0][i])
                print (pn[1][i])
                print (pn[2][i])
    else:
        tag = input("請輸入tag : (e.g.1.0.2)" )
        buildType = input("請輸入buildType : (e.g.直接build遊戲)" )
        multi(var, tag, buildType)

def thread(project, tag, buildType):
    print("*------專案 : " + project + "------*")
    print("*------tag : " + tag + "------------------------*")
    print("*------buildType : " + buildType +"----------*" )
    '''JENKINS_URL = "http://192.168.4.125:8080"
    JENKINS_USER = "qa"
    JENKINS_PASSWORD = "qa"
    token = "fc6b3df05ca3f99fc6609ad7ec171133"
    job = project
    crumb=CrumbRequester(username=JENKINS_USER, password=JENKINS_PASSWORD, baseurl=JENKINS_URL)
    j = Jenkins(JENKINS_URL, username=JENKINS_USER, password=JENKINS_PASSWORD, requester=crumb)
    params = {'tag':tag ,'buildType':buildType}
    j.build_job(job,params)'''
    print("*------寫入紀錄黨-------------------------*")
    book = xlwt.Workbook(encoding = "utf-8", style_compression = 0)
    sheet = book.add_sheet("sheet1", cell_overwrite_ok = True)
    sheet.write(0, 0, "project")
    sheet.write(1, 0, project)
    sheet.write(0, 1, "版本")
    sheet.write(1, 1, tag)
    sheet.write(0, 2, "最後更新時間")
    sheet.write(1, 2, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    book.save("record.xls")
    print("*------Done-------------------------------*")


def multi(project, tag, buildType):
    jobs = []
    p = multiprocessing.Process(target=thread, args=(project, tag, buildType))
    jobs.append(p)
    p.start()

if __name__ == '__main__':
    run()