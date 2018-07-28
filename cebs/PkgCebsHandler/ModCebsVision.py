'''
Created on 2018/5/4

@author: Administrator
'''

####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-

import random
import sys
import time
import json
import os
import re
import urllib
import http
import socket
import datetime
import string
import ctypes 
import random
import cv2 as cv
import numpy as np  
#import matplotlib.pyplot as plt
#import imutils
from ctypes import c_uint8
#import argparse
#import math


from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

#Local include
from cebsMain import *
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg

class classVisionProcess(object):
    def __init__(self):
        self.objInitCfg = ModCebsCfg.ConfigOpr()
    
    def funcVisionDetectAllCamera(self):
        MaxDetectNbr = ModCebsCom.GL_CEBS_VISION_MAX_CAMERA_SEARCH
        res = "VALID CAMERA NUMBER: "
        for index in range(0, MaxDetectNbr):
            cap = cv.VideoCapture(index)
            if cap.isOpened():
                res = res + str(index) + ", "
        return res
         
    def funcVisionCapture(self, batch, fileNbr):
        time.sleep(1)
        #SELFCT CAMERA，#0-NOTEBOOK INTERNAL CAMERA，#1,#2 - EXTERNAL CAMERA
        cap = cv.VideoCapture(ModCebsCom.GL_CEBS_VISION_CAMBER_NBR) #CHECK WITH ls /dev/video*　RESULT
        # Check if the webcam is opened correctly
        if not cap.isOpened():
            #raise IOError("Cannot open webcam")
            self.objInitCfg.medErrorLog("VISION CLAS: Cannot open webcam!")
            print("VISION CLAS: Cannot open webcam!, Batch/Nbr=%d/%d" % (batch, fileNbr))
            return -1;
        
        #Picture capture
        #DEFINE PIC GRADULARITY
        cap.set(4, 1440)  #720
        width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH) + 0.5)
        height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT) + 0.5)
        fps = 20
        
        #MASSIVE ERROR!
        #1st par is path and file name
        #2nd par is video format, “MPEG” is **standard， BAIDU fourcc could find more
        #2nd par（fourcc） = -1，means allow select video format
        #fourcc = cv.VideoWriter_fourcc(*"MPEG")
        #fourcc=-1**
        #3rd par is carmera speed，20 is normal，less than 20 is slow**
        #out = cv.VideoWriter('c://output.avi',fourcc,20,(640,480))
        ret, frame = cap.read()
        if (ret == True):
            frame = cv.flip(frame, 1)#Operation in frame
            #frame = cv.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_AREA)
            frame = cv.resize(frame, None, fx=1, fy=1, interpolation=cv.INTER_AREA)
            #cv.imshow('Input', frame)
            obj=ModCebsCfg.ConfigOpr();
            fileName = obj.combineFileNameWithDir(batch, fileNbr)
            cv.imwrite(fileName, frame)
        
        #Video capture
        #Ref: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
        #fourcc code: http://www.fourcc.org/codecs.php
        if (ret == True) and (ModCebsCom.GL_CEBS_VIDEO_CAPTURE_ENABLE == True):
            #Video capture with 3 second
            fourcc = cv.VideoWriter_fourcc(*'mp4v')  #mp4v(.mp4), XVID(.avi)
            fileNameVideo = obj.combineFileNameVideoWithDir(batch, fileNbr)
            out = cv.VideoWriter(fileNameVideo, fourcc, fps, (width, height))
            cnt = 0
            targetCnt = fps * ModCebsCom.GL_CEBS_VIDEO_CAPTURE_DUR_IN_SEC
            while cap.isOpened():
                cnt += 1
                ret, frame = cap.read()
                if ret:
                    frame = cv.flip(frame, 0)
                    #write the flipped frame
                    time.sleep(1.0/fps)
                    out.write(frame)
                    if cnt >= targetCnt:
                        break
                else:
                    break
            out.release()
            
        #Release all resource
        cap.release()
        cv.destroyAllWindows()
        return 1;

    def funcVisionClasStart(self):
        ModCebsCom.GL_CEBS_PIC_CLAS_FLAG = True;

    def funcVisionClasEnd(self):
        ModCebsCom.GL_CEBS_PIC_CLAS_FLAG = False;

#MAIN PROCESSING MODULE
class classVisionThread(QThread, ModCebsCfg.ConfigOpr):
    signal_print_log = pyqtSignal(str) #DECLAR MAIN FUNCTIONS
    signal_vision_start = pyqtSignal()  #DECLAR MAIN FUNCTIONS, NOT USED
    signal_vision_stop = pyqtSignal()   #DECLAR MAIN FUNCTIONS, NOT USED

    #分类大小的参数定义
    HST_VISION_WORM_CLASSIFY_base = 0;
    HST_VISION_WORM_CLASSIFY_small2mid = 0;
    HST_VISION_WORM_CLASSIFY_mid2big = 0;
    HST_VISION_WORM_CLASSIFY_big2top = 0;
    
    #处理的图片和文档
    HST_VISION_WORM_CLASSIFY_pic_filepath = ""
    HST_VISION_WORM_CLASSIFY_pic_filename = ""
    
    #处理后的结果
    HST_VISION_WORM_CLASSIFY_pic_sta_output = {'totalNbr':0, 'bigAlive':0, 'bigDead':0, 'middleAlive':0, 'middleDead':0, 'smallAlive':0, 'smallDead':0, 'totalAlive':0, 'totalDead':0}


    def __init__(self,parent=None):
        super(classVisionThread,self).__init__(parent)
        self.identity = None;

        self.HST_VISION_WORM_CLASSIFY_base = ModCebsCom.GL_CEBS_VISION_SMALL_LOW_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_small2mid = ModCebsCom.GL_CEBS_VISION_SMALL_MID_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_mid2big = ModCebsCom.GL_CEBS_VISION_MID_BIG_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_big2top = ModCebsCom.GL_CEBS_VISION_BIG_UPPER_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_pic_filepath = ModCebsCom.GL_CEBS_PIC_MIDDLE_PATH + '/'
        self.HST_VISION_WORM_CLASSIFY_pic_filename = "1.jpg"
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output = {'totalNbr':0, 'bigAlive':0, 'bigDead':0, 'middleAlive':0, 'middleDead':0, 'smallAlive':0, 'smallDead':0, 'totalAlive':0, 'totalDead':0}
        
    def setIdentity(self,text):
        self.identity = text

    def funcVisionProc(self):
        batch, fileNbr = self.findUnclasFileBatchAndFileNbr();
        if (batch < 0):
            ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT = 0;
            self.signal_print_log.emit("VISION CLAS: PICTURE IDENTIFY NOT FINISHED: REMAINING NUMBERS=%d." %(ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT))
            self.updateCtrlCntInfo();
            return;
        fileName = self.getStoredFileName(batch, fileNbr);
        fileNukeName = self.getStoredFileNukeName(batch, fileNbr)
        if (fileName == None) or (fileNukeName == None):
            ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT = 0;
            self.signal_print_log.emit("VISION CLAS: VS_CLASPICTURE IDENTIFY FINISHED: REMAINING NUMBERS=%d." %(ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT))
            self.updateCtrlCntInfo();
            return;
        #REAL PROCESSING PROCEDURE
        print("VISION CLAS: Batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
        self.funcVisionClassify(fileName, fileNukeName);
        ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT -= 1;
        self.updateUnclasFileAsClassified(batch, fileNbr);
        self.signal_print_log.emit("VISION CLAS: PIC IDENTIFY： REMAINING NUMBRES=%d." %(ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT))
       
    #PIC PROC
    def funcVisionClassify(self, fileName, fileNukeName):
        #time.sleep(random.random()*10)
        self.func_vision_worm_clasification(fileName, fileNukeName)
        
    def func_vision_worm_input_processing(self, inputStr):
        try:
            if ((inputStr['cfBase'] < inputStr['cfSmall2MidIndex']) and (inputStr['cfSmall2MidIndex'] < inputStr['cfMid2BigIndex']) and (inputStr['cfMid2BigIndex'] < inputStr['cfBig2TopIndex'])):
                self.HST_VISION_WORM_CLASSIFY_base = inputStr['cfBase'];
                self.HST_VISION_WORM_CLASSIFY_small2mid = inputStr['cfSmall2MidIndex'];
                self.HST_VISION_WORM_CLASSIFY_mid2big = inputStr['cfMid2BigIndex'];
                self.HST_VISION_WORM_CLASSIFY_big2top = inputStr['cfBig2TopIndex'];
                self.HST_VISION_WORM_CLASSIFY_pic_filename = inputStr['fileName'];
            else:
                print("VISION CLAS: func_vision_worm_input_processing on input error!")
        except Exception as err:
            text = "VISION CLAS: func_vision_worm_input_processing on input error = %s" % str(err)
            print(text);

    def func_vision_worm_binvalue_test(self, img):
        new = np.zeros(img.shape, np.uint8)    
    
        #Gray transaction: 灰度化
        for i in range(new.shape[0]):  #Axis-y/height/Rows
            for j in range(new.shape[1]):
                (b,g,r) = img[i,j]
                #加权平均法
                new[i,j] = int(0.3*float(b) + 0.59*float(g) + 0.11*float(r))&0xFF
    
        #Middle value filter: 中值滤波
        blur= cv.medianBlur(new, 5)
        midGray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
        #cv.imshow('Middle Blur', midGray)
    
        #Adaptive bin-translation: 自适应二值化
        binGray = cv.adaptiveThreshold(midGray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 43, 5)   # ADAPTIVE_THRESH_MEAN_C ADAPTIVE_THRESH_GAUSSIAN_C
        binRes= cv.GaussianBlur(binGray, (5,5), 1.5) #medianBlur
        #cv.imshow('Adaptive Bin', binRes)
        return binRes;
    
    def func_vision_worm_remove_noise_test(self, img):
        #Enlarge + Erosion: shape translation 膨胀+腐蚀等形态学变化  
        kerne1 = np.ones((7, 7), np.uint8)  
        img_erosin = cv.erode(img, kerne1, iterations=1)
           
        #2nd time mid-value filter: 再次中值滤波
        midFilter= cv.medianBlur(img_erosin, 5)
        
        #Fix bin-value: 固定二值化
        ret, binImg = cv.threshold(midFilter, 130, 255, cv.THRESH_BINARY)
        #cv.imshow("img_erosin and Noise removal", binImg)
                
        return binImg;
    
    
    #https://www.cnblogs.com/llfisher/p/6557611.html
    #https://www.cnblogs.com/nanyangzp/p/3496486.html
    #偏心率：以质心为中心，所有点到X轴的长度综合，相比Y周的长度总和，他们之间的比值。
    #圆形=1，长条就是斜率
    # E = (M20-M02+4M11)/A, Mjk = EE(x-xA)^j * (y-yA)^k, (j+k阶矩)，A为面积
    #http://wenku.baidu.com/link?url=4ZSLxGBKE3LBf2mdxDs0VJ1cjJ3hxqeORu-3mfXO23gGBqf5LyjqZ4AHFCMLeP32xEKkoj5tPsWHdvA2ovmuKiRDKN6YHFO9G7JOzBWWrMC
    
    #http://blog.csdn.net/app_12062011/article/details/51953030
    #E = sqrt(1-I^2)
    #I = (u20+u02-sqrt(4u11*u11(u20-u02)*(u20-u02))/(u20+u02+sqrt(4u11*u11(u20-u02)*(u20-u02))
    def func_vision_worm_find_contours(self, nfImg, orgImg):
        #Searching out-form shape: 找到轮廓
        _, contours, hierarchy = cv.findContours(nfImg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) #RETR_TREE, RETR_CCOMP
        #contours = contours[0] if imutils.is_cv() else contours[1]
        
        #Output graphic: 输出图形
        outputImg = cv.cvtColor(nfImg, cv.COLOR_GRAY2BGR)
        mask = np.zeros((orgImg.shape[0]+2, orgImg.shape[1]+2), np.uint8)
        mask[:] = 1
        #Analysis one by one: 分别分析
        for c in contours:
            #External retangle: 外矩形框
            (x,y,w,h)=cv.boundingRect(c)
            pointx=x+w/2
            pointy=y+h/2
            # compute the center of the contour
            M = cv.moments(c)
            cX = int(M["m10"] / (M["m00"]+0.01))
            cY = int(M["m01"] / (M["m00"]+0.01))
            seed_point = (cX, cY)
            #Shape square: 轮廓面积
            cArea = cv.contourArea(c)
            #Shape length: 轮廓弧长
            cPerimeter = cv.arcLength(c,True)
            
            #4th method: 第四种方法
            rect = cv.minAreaRect(c)
            #width / height: 长宽,总有 width>=height  
            width, height = rect[1]
            if (width > height):
                cE = height / (width+0.001)
            else:
                cE = width / (height+0.001)
            cE = round(cE, 2)
    
            #Finally not use flood algorithms: 最终决定不采用flood算法
            #print(self.HST_VISION_WORM_CLASSIFY_base)
            if cArea < self.HST_VISION_WORM_CLASSIFY_base:
                pass
            elif cArea < self.HST_VISION_WORM_CLASSIFY_small2mid:
                self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalNbr'] +=1
                #cv.floodFill(outputImg, mask, seed_point,(0,0,255))
                cv.drawContours(outputImg, c, -1, (0,0,255), 2)  
                if (cE < 0.5):
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['smallDead'] +=1
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalDead'] +=1
                else:
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['smallAlive'] +=1
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalAlive'] +=1               
                cv.putText(outputImg, str(cE), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            elif cArea < self.HST_VISION_WORM_CLASSIFY_mid2big:
                self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalNbr'] +=1
                #cv.floodFill(outputImg, mask, seed_point,(0,255,0))  
                cv.drawContours(outputImg, c, -1, (0,255,0), 2)
                if (cE < 0.5):
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['middleDead'] +=1
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalDead'] +=1
                else:
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['middleAlive'] +=1
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalAlive'] +=1            
                cv.putText(outputImg, str(cE), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            elif cArea < self.HST_VISION_WORM_CLASSIFY_big2top:
                self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalNbr'] +=1
                #cv.floodFill(outputImg, mask, seed_point,(255,0,0))  
                cv.drawContours(outputImg, c, -1, (255,0,0), 2)
                if (cE < 0.5):
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['bigDead'] +=1
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalDead'] +=1
                else:
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['bigAlive'] +=1
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalAlive'] +=1                        
                cv.putText(outputImg, str(cE), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(outputImg, str(self.HST_VISION_WORM_CLASSIFY_pic_sta_output), (10, 30), font, 0.7, (0, 0, 255), 2, cv.LINE_AA)
        return outputImg;
        pass;

    #Classified processing: 分类总处理    
    def func_vision_worm_clasification(self, fileName, fileNukeName):
        #Reading file: 读取文件
        if (os.path.exists(fileName) == False):
            errStr = "VISION CLAS: File %s not exist!" % (fileName)
            self.medErrorLog(errStr);
            print("VISION CLAS: File %s not exist!" % (fileName))
            return;
        self.HST_VISION_WORM_CLASSIFY_pic_filename = fileName
        try:
            inputImg = cv.imread(fileName)
        except Exception as err:
            print("VISION CLAS: Read file error, errinfo = ", str(err))
            return;

        #Processing procedure: 处理过程
        binImg = self.func_vision_worm_binvalue_test(inputImg)
        nfImg = self.func_vision_worm_remove_noise_test(binImg)
        outputImg = self.func_vision_worm_find_contours(nfImg, inputImg)
        outputFn = self.HST_VISION_WORM_CLASSIFY_pic_filepath + "result_" + fileNukeName
        print("VISION CLAS: OutputFn = %s, nuke name = %s" %(outputFn, fileNukeName))
        cv.imwrite(outputFn, outputImg)
            
        #Save log record: 存储干活的log记录
        f = open(ModCebsCom.GL_CEBS_VISION_CLAS_RESULT_FILE_NAME_SET, "a+")
        a = '[%s], vision worm classification ones, save result as [%s] with output [%s].\n' % (time.asctime(), outputFn, str(self.HST_VISION_WORM_CLASSIFY_pic_sta_output))
        f.write(a)
        f.close()
        
        #Show result or not: 根据指令，是否显示文件
        cv.destroyAllWindows()
        
    def run(self):
        ctrlFlag = False
        ctrlInterest = False
        while True:
            time.sleep(1)
            if ((ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT > 0) and (ModCebsCom.GL_CEBS_PIC_CLAS_FLAG == True)):
                if (ctrlFlag == True):
                    ctrlFlag = True
                    ctrlInterest = False
                else:
                    ctrlFlag = True
                    ctrlInterest = False
                self.funcVisionProc();
            else:
                if (ctrlFlag == True):
                    ctrlFlag = False
                    ctrlInterest = True
                else:
                    ctrlFlag = False
                    ctrlInterest = False
            #Send signal to CebsCtrl to stop STM
            if (ctrlInterest == True):
                #self.signal_ctrl_clas_stop.emit()
                self.signal_print_log.emit("VISION CLAS: Finish all picture classification!")
        
        
        