#!/usr/bin/python
# coding: utf-8
import pandas
from openpyxl import load_workbook
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
    f=open('record.csv','w')
    f.write('Project,版本,最後更新時間,備註\n')
    f.close
    var = input("請輸入需要build的project : (e.g.RD1_H5_Client_25_Build or ALL)" )
    print("You entered " + str(var))
    if var == 'ALL':
        i=0
        pn=[]
        with open ('data.txt','r') as f:
            for line in f:
                #print(line)
                line=line.strip('\n')
                pn.append(list(map(str,line.split(','))))
                #print (len(pn))
            for i in range (len(pn)):
                project=str(pn[0][i])
                tag=str(pn[1][i])
                buildType=str(pn[2][i])
                multi(project, tag, buildType)
                #print (pn[0][i])
                #print (pn[1][i])
                #print (pn[2][i])
    else:
        tag = input("請輸入tag : (e.g.1.0.2)" )
        buildType = input("請輸入buildType : (e.g.直接Build遊戲)" )
        multi(var, tag, buildType)

def thread(project, tag, buildType):
    print("*------專案 : " + project + "------*")
    print("*------tag : " + tag + "------------------------*")
    print("*------buildType : " + buildType +"----------*" )
    try:
        JENKINS_URL = "http://192.168.4.125:8080"
        JENKINS_USER = "qa"
        JENKINS_PASSWORD = "qa"
        token = "fc6b3df05ca3f99fc6609ad7ec171133"
        job = project
        crumb=CrumbRequester(username=JENKINS_USER, password=JENKINS_PASSWORD, baseurl=JENKINS_URL)
        j = Jenkins(JENKINS_URL, username=JENKINS_USER, password=JENKINS_PASSWORD, requester=crumb)
        params = {'tag':tag ,'buildType':buildType}
        j.build_job(job,params)
        print("*------寫入紀錄檔-------------------------*")
        f = open("record.csv","a")
        f.write(project+",")
        f.write(tag+",")
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
        f.close
        print("*------Done-------------------------------*")

    except Exception as e:
        print("*------寫入紀錄檔-------------------------*")
        f = open("record.csv","a")
        f.write(project+",")
        f.write(tag+",")
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+",")
        f.write("Build fail\n")
        f.close
        print("*------Build fail please check the data is correct.------*")
        pass

def multi(project, tag, buildType):
    jobs = []
    p = multiprocessing.Process(target=thread, args=(project, tag, buildType))
    jobs.append(p)
    p.start()

if __name__ == '__main__':
    run()