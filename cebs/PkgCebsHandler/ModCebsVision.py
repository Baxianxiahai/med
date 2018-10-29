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
import matplotlib.pyplot as plt
import math
#import imutils
from ctypes import c_uint8
#import argparse
#import math
import win32com.client  #pip install pyWin32
import usb.core

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

#Local include
from cebsMain import *
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg
from cv2 import waitKey


'''

图像获取的任务模块
        
#模块可能被WinMain和Calib调用，所以初始化需要传入Father进去

#         #SELFCT CAMERA，#0-NOTEBOOK INTERNAL CAMERA，#1,#2 - EXTERNAL CAMERA
#         self.cap = cv.VideoCapture(ModCebsCom.GLPIC_PAR_OFC.VISION_CAMBER_NBR) #CHECK WITH ls /dev/video*　RESULT
#         if not self.cap.isOpened():
#             self.instL1ConfigOpr.medErrorLog("L2VISCAP: Cannot open webcam!")
#             print("L2VISCAP: Cannot open webcam!")
#             return -1;
#         #Set working resolution
#         self.cap.set(3, ModCebsCom.GL_CEBS_VISION_CAMBER_RES_WITDH)
#         self.cap.set(4, ModCebsCom.GL_CEBS_VISION_CAMBER_RES_HEIGHT)
#         self.width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH) + 0.5)
#         self.height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT) + 0.5)
#         print("L2VISCAP: Width/Height = %d/%d" % (self.width, self.height))
#         self.fps = 20

'''
class clsL2_VisCapProc(object):
    def __init__(self, winFormHandler):
        super(clsL2_VisCapProc, self).__init__()
        self.identity = None;
        self.instL4WinForm = winFormHandler
        self.instL1ConfigOpr = ModCebsCfg.clsL1_ConfigOpr()
        self.capInit = ''
        self.funcVisCapLogTrace("L2VISCAP: Instance start test!")
        
    def funcVisCapLogTrace(self, myString):
        self.instL4WinForm.med_debug_print(myString)
        
    def funcVisionDetectAllCamera(self):
        res = "L2VISCAP: Valid camera number = "
#         MaxDetectNbr = ModCebsCom.GLVIS_PAR_OFC.VISION_MAX_CAMERA_SEARCH
#         for index in range(0, MaxDetectNbr):
#             cap = cv.VideoCapture(index)
#             if cap.isOpened():
#                 res = res + str(index) + ", "
#                 cap.release()
#             cv.destroyAllWindows()
        #New finding camaer way
        wmi = win32com.client.GetObject ("winmgmts:")
        for usb in wmi.InstancesOf ("win32_usbcontrollerdevice"):
            if "VID_0547&PID_6010" in usb.Dependent:
                searchText = "VID_0547&PID_6010"
                indexStart = usb.Dependent.find(searchText)
                textLen = len(searchText)
                textContent = usb.Dependent[indexStart+textLen:]
                result={}
                step=0;
                for item in textContent.split('&'):
                    result[step] = item
                    step+=1
                try:
                    ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR = result[2]
                except Exception:
                    ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR = -1
        return res + str(ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR)
    
    #Init the camera resolution, iso set every capture time. 这样可以避免每次对焦的长时间消耗
    def funcVisBatCapStart(self):
        if (ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR < 0):
            self.funcVisCapLogTrace("L2VISCAP: Camera not yet installed!");
            return -1;
        else:
            self.capInit = cv.VideoCapture(ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR) #CHECK WITH ls /dev/video*　RESULT
            self.capInit.set(3, ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_RES_WITDH)
            self.capInit.set(4, ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_RES_HEIGHT)
            #time.sleep(5)
            return 1;

    def funcVisBatCapStop(self):
        self.capInit.release()
        cv.destroyAllWindows()
    
    '''     
    #SELFCT CAMERA，#0-NOTEBOOK INTERNAL CAMERA，#1,#2 - EXTERNAL CAMERA
    #cap = cv.VideoCapture(ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR) #CHECK WITH ls /dev/video*　RESULT
    #Check if the webcam is opened correctly
    *
    * forFlag: 使用这个来对付初始化时的跳过标签，不然在视频模式下需要等待太长时间
    *
    '''
    def funcVisionCapture(self, batch, fileNbr, forceFlag):
        if not self.capInit.isOpened():
            #raise IOError("Cannot open webcam")
            self.instL1ConfigOpr.medErrorLog("L2VISCAP: Cannot open webcam!")
            print("L2VISCAP: Cannot open webcam!, Batch/Nbr=%d/%d" % (batch, fileNbr))
            self.capInit.release()
            cv.destroyAllWindows()            
            return -1;

        width = int(self.capInit.get(cv.CAP_PROP_FRAME_WIDTH) + 0.5)
        height = int(self.capInit.get(cv.CAP_PROP_FRAME_HEIGHT) + 0.5)
        fps = 20
        #print("L2VISCAP: Width/Height = %d/%d" % (width, height))
        time.sleep(1)
        
        #MASSIVE ERROR!
        #1st par is path and file name
        #2nd par is video format, “MPEG” is **standard， BAIDU fourcc could find more
        #2nd par（fourcc） = -1，means allow select video format
        #fourcc = cv.VideoWriter_fourcc(*"MPEG")
        #fourcc=-1**
        #3rd par is carmera speed，20 is normal，less than 20 is slow**
        #out = cv.VideoWriter('c://output.avi',fourcc,20,(640,480))
        ret, frame = self.capInit.read()
        if (ret == True):
            frame = cv.flip(frame, 1)#Operation in frame
            #frame = cv.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_AREA)
            frame = cv.resize(frame, None, fx=1, fy=1, interpolation=cv.INTER_AREA)
            #白平衡算法
            B,G,R = cv.split(frame)
            bMean = cv.mean(B)
            gMean = cv.mean(G)
            rMean = cv.mean(R)
            print("L2VISCAP: Mean B/G/R = %d/%d/%d" %(bMean[0], gMean[0], rMean[0]))
            kb = (bMean[0] + gMean[0] + rMean[0])/(3*bMean[0]+0.0001)
            kg = (bMean[0] + gMean[0] + rMean[0])/(3*gMean[0]+0.0001)
            kr = (bMean[0] + gMean[0] + rMean[0])/(3*rMean[0]+0.0001)
            B = B * kb
            G = G * kg
            R = R * kr
            outputFrame = cv.merge([B, G, R])
            
            #Show picture
            #cv.imshow('Input', frame)
            obj=ModCebsCfg.clsL1_ConfigOpr();
            fileName = obj.combineFileNameWithDir(batch, fileNbr)
            cv.imwrite(fileName, outputFrame)
            #cv.imshow("Final output", frame)
            #waitKey(2000)
            #time.sleep(2)
            
            #存储scale文件
            scaleFn = obj.combineScaleFileNameWithDir(batch, fileNbr)
            self.algoVisGetRadians(ModCebsCom.GLPLT_PAR_OFC.med_get_radians_len_in_us(), fileName, scaleFn)
        
        #Video capture
        #Ref: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
        #fourcc code: http://www.fourcc.org/codecs.php
        if (forceFlag == True):
            return 1;
        if (ret == True) and (ModCebsCom.GLVIS_PAR_OFC.CAPTURE_ENABLE == True):
            #Video capture with 3 second
            fourcc = cv.VideoWriter_fourcc(*'mp4v')  #mp4v(.mp4), XVID(.avi)
            fileNameVideo = obj.combineFileNameVideoWithDir(batch, fileNbr)
            out = cv.VideoWriter(fileNameVideo, fourcc, fps, (width, height))
            cnt = 0
            targetCnt = fps * ModCebsCom.GLVIS_PAR_OFC.CAPTURE_DUR_IN_SEC
            while self.capInit.isOpened():
                cnt += 1
                ret, frame = self.capInit.read()
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
            return 2;
        return 1;
      
      
    #计算弧度的方式
    #INPUT: refRadInUm, 孔半径长度，um单位
    #OUTPUT: 对应比例关系
    def algoVisGetRadians(self, refRadInUm, dirFn, newFileFn):
        #Reading file: 读取文件
        if (os.path.exists(dirFn) == False):
            errStr = "L2VISCFY: File %s not exist!" % (dirFn)
            self.medErrorLog(errStr);
            print("L2VISCFY: File %s not exist!" % (dirFn))
            return;
        self.HST_VISION_WORM_CLASSIFY_pic_filename = dirFn
        try:
            inputImg = cv.imread(dirFn)
        except Exception as err:
            print("L2VISCFY: Read file error, errinfo = ", str(err))
            return;
        #图像分块
        orgH = inputImg.shape[0]
        orgW = inputImg.shape[1]
        imgLeftUp = inputImg[0:orgH//3, 0:orgW//3]
        imgRightUp = inputImg[0:orgH//3, orgW*2//3:orgW]
        imgLeftBot = inputImg[orgH*2//3:orgH, 0:orgW//3]
        imgRightBot = inputImg[orgH*2//3:orgH, orgW*2//3:orgW]
        arcLenMax = math.sqrt((orgH//3) * (orgH//3) + (orgW//3) * (orgW//3))*2
        #print("Max Arc length = ", arcLenMax)
        
        #比较
        flagIndex = 0
        arcSave = 0
        stdRatio = 0
        #PART1
        arcLen, lenSqrRatio, resImgLU = self.algoVisFindMaxEdge(refRadInUm, imgLeftUp)
        #print("LU Length/baseline = %f/%f" % (arcLen, lenSqrRatio))
        if (arcLen < arcLenMax) and (lenSqrRatio < 1) and (lenSqrRatio > 0.1) and (arcLen > arcSave):
            flagIndex = 1
            arcSave = arcLen
            stdRatio = lenSqrRatio
        #PART2
        arcLen, lenSqrRatio, resImgRU = self.algoVisFindMaxEdge(refRadInUm, imgRightUp)
        #print("RU Length/baseline = %f/%f" % (arcLen, lenSqrRatio))
        if (arcLen < arcLenMax) and (lenSqrRatio < 1) and (lenSqrRatio > 0.1) and (arcLen > arcSave):
            flagIndex = 2
            arcSave = arcLen
            stdRatio = lenSqrRatio
        #PART3
        arcLen, lenSqrRatio, resImgLB = self.algoVisFindMaxEdge(refRadInUm, imgLeftBot)
        #print("LB Length/baseline = %f/%f" % (arcLen, lenSqrRatio))
        if (arcLen < arcLenMax) and (lenSqrRatio < 1) and (lenSqrRatio > 0.1) and (arcLen > arcSave):
            flagIndex = 3
            arcSave = arcLen
            stdRatio = lenSqrRatio
        #PART4
        arcLen, lenSqrRatio, resImgRB = self.algoVisFindMaxEdge(refRadInUm, imgRightBot)
        #print("RB Length/baseline = %f/%f" % (arcLen, lenSqrRatio))
        if (arcLen < arcLenMax) and (lenSqrRatio < 1) and (lenSqrRatio > 0.1) and (arcLen > arcSave):
            flagIndex = 4
            arcSave = arcLen
            stdRatio = lenSqrRatio
        #SHOW
        '''
        if (flagIndex == 1):
            print("Result = resImgLU")
            #cv.line(resImgLU, start, end, (0, 0, 255))
            cv.imshow("resImgLU", resImgLU)
        if (flagIndex == 2):
            print("Result = resImgRU")
            #cv.line(resImgRU, start, end, (0, 0, 255))
            cv.imshow("resImgRU", resImgRU)
        if (flagIndex == 3):
            print("Result = resImgLB")
            #cv.line(resImgLB, start, end, (0, 0, 255))
            cv.imshow("resImgLB", resImgLB)
        if (flagIndex == 4):
            print("Result = resImgRB")
            #cv.line(resImgRB, start, end, (0, 0, 255))
            cv.imshow("resImgRB", resImgRB)
        '''
        #1mm = 1000um的标尺
        ptLen = int(500*stdRatio)
        sp = inputImg.shape
        start = (sp[1]-100, sp[0]-20)
        end = (start[0] + ptLen, start[1])
        #原始图像
        cv.line(inputImg, start, end, (0, 0, 255))
        cv.putText(inputImg, '500um', (start[0], start[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        #cv.imshow("inputImg", inputImg)
        cv.imwrite(newFileFn, inputImg)
        
    '''
    * 参考文档： https://blog.csdn.net/sinat_36458870/article/details/78825571
    #寻找边缘算法，待优化
    '''
    def algoVisFindMaxEdge(self, refRadInUm, inputImg):
        #噪声处理过程
        new = np.zeros(inputImg.shape, np.uint8)    
        #Gray transaction: 灰度化
        for i in range(new.shape[0]):  #Axis-y/height/Rows
            for j in range(new.shape[1]):
                (b,g,r) = inputImg[i,j]
                #加权平均法
                new[i,j] = int(0.3*float(b) + 0.59*float(g) + 0.11*float(r))&0xFF
        #Middle value filter: 中值滤波
        blur= cv.medianBlur(new, 5)
        midGray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
        #Adaptive bin-translation: 自适应二值化
        binGray = cv.adaptiveThreshold(midGray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 43, 5)   # ADAPTIVE_THRESH_MEAN_C ADAPTIVE_THRESH_GAUSSIAN_C
        binRes= cv.GaussianBlur(binGray, (5,5), 1.5) #medianBlur
        #cv.imshow('Adaptive Bin', binRes)
        corImg = cv.cvtColor(binRes, cv.COLOR_GRAY2BGR)
        #高斯模糊,降低噪声  
        blurred = cv.GaussianBlur(corImg,(3, 3), 0)  
        #灰度图像  
        gray=cv.cvtColor(blurred, cv.COLOR_RGB2GRAY)  
        #图像梯度  
        xgrad=cv.Sobel(gray, cv.CV_16SC1, 1, 0)   #cv.CV_32F
        ygrad=cv.Sobel(gray, cv.CV_16SC1, 0, 1)  
        #计算边缘  
        #50和150参数必须符合1：3或者1：2  
        edge_output=cv.Canny(xgrad, ygrad, 50, 100)  
        #cv.imshow("edge", edge_output)
        _, contours, _ = cv.findContours(edge_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        #Output graphic: 输出图形
        outputImg = cv.cvtColor(edge_output, cv.COLOR_GRAY2BGR)
        mask = np.zeros((edge_output.shape[0]+2, edge_output.shape[1]+2), np.uint8)
        mask[:] = 1
        maxC = ''
        #求最大弧长
        arcLenMax = 0
        for c in contours:
            arcLen = cv.arcLength(c, False)
            #cArea = cv.contourArea(c)
            if (arcLen > arcLenMax):
                maxC = c
                arcLenMax = arcLen
        #print("arcLenMax = ", arcLenMax)
        # compute the center of the contour
        M = cv.moments(maxC)
        cX = int(M["m10"] / (M["m00"]+0.01))
        cY = int(M["m01"] / (M["m00"]+0.01))
        #4th method: 第四种方法
        rect = cv.minAreaRect(maxC)
        width, height = rect[1]
        if (width > height):
            tmp = width
            width = height
            height = tmp
        cE = width / (height+0.001)
        cE = round(cE, 2)
        cv.drawContours(outputImg, maxC, -1, (0, 0, 255), 2)                    
        cv.putText(outputImg, str(cE), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        #画最小外接框
        box = cv.boxPoints(rect)
        box = np.int0(box)
        cv.drawContours(outputImg, [box], -1, (0, 0, 255), 1)
        
        #cv.imshow("result", outputImg)  
        newRadians = (height * height / (4 * width) + width)/2
        #print("newRadians =%d, width/height=%d/%d" % (newRadians, width, height))
        #newRadians = height * math.sqrt(1 + height*height/4/width/width)/2
        baseLine = newRadians/refRadInUm
        return arcLenMax, baseLine, outputImg
    
    
    
    
    
      
        
'''

图像处理过程的任务模块：常驻内存的静态任务过程，可以被过程化控制
        
#MAIN PROCESSING MODULE: 循环处理线程
#模块只能被WinMain调用，所以打印只会打到WinMain上去

'''
class clsL2_VisCfyProc(ModCebsCfg.clsL1_ConfigOpr):
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

    def __init__(self, father):
        super(clsL2_VisCfyProc, self).__init__()
        self.identity = None;
        self.instL4WinForm = father
        self.HST_VISION_WORM_CLASSIFY_base = ModCebsCom.GLVIS_PAR_OFC.SMALL_LOW_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_small2mid = ModCebsCom.GLVIS_PAR_OFC.SMALL_MID_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_mid2big = ModCebsCom.GLVIS_PAR_OFC.MID_BIG_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_big2top = ModCebsCom.GLVIS_PAR_OFC.BIG_UPPER_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_pic_filepath = ModCebsCom.GLCFG_PAR_OFC.PIC_MIDDLE_PATH + '/'
        self.HST_VISION_WORM_CLASSIFY_pic_filename = "1.jpg"
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output = {'totalNbr':0, 'bigAlive':0, 'bigDead':0, 'middleAlive':0, 'middleDead':0, 'smallAlive':0, 'smallDead':0, 'totalAlive':0, 'totalDead':0}
        self.funcVisCfyLogTrace("L2VISCFY: Instance start test!")
        
    def funcVisCfyLogTrace(self, myString):
        self.instL4WinForm.med_debug_print(myString)
    
    
    
    '''
    * 核心的识别函数，其它任务调用的主入口
    *
    *    用于普通白光照片的识别处理过程
    *
    '''    
    def funcVisionNormalClassifyProc(self):
        batch, fileNbr = self.findNormalUnclasFileBatchAndNbr();
        if (batch < 0):
            ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT = 0;
            self.funcVisCfyLogTrace("L2VISCFY: Picture classification not finished: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.updateCtrlCntInfo();
            return;
        fileName = self.getStoredFileName(batch, fileNbr);
        fileNukeName = self.getStoredFileNukeName(batch, fileNbr)
        if (fileName == None) or (fileNukeName == None):
            ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT = 0;
            self.funcVisCfyLogTrace("L2VISCFY: Picture classification finished: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.updateCtrlCntInfo();
            return;
        #REAL PROCESSING PROCEDURE
        print("L2VISCFY: Normal picture batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
        self.func_vision_worm_clasification(fileName, fileNukeName, False);
        ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT -= 1;
        #Update classified files
        self.updateUnclasFileAsClassified(batch, fileNbr);
        self.funcVisCfyLogTrace("L2VISCFY: Normal picture classification finished, remaining NUMBRES=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
        self.updateCtrlCntInfo();
        return;


    def funcVisionNormalClassifyDirect(self, dirFn, tmpFn):
        return self.func_vision_worm_clasification(dirFn, tmpFn, True);
        
        
    def func_vision_worm_input_processing(self, inputStr):
        try:
            if ((inputStr['cfBase'] < inputStr['cfSmall2MidIndex']) and (inputStr['cfSmall2MidIndex'] < inputStr['cfMid2BigIndex']) and (inputStr['cfMid2BigIndex'] < inputStr['cfBig2TopIndex'])):
                self.HST_VISION_WORM_CLASSIFY_base = inputStr['cfBase'];
                self.HST_VISION_WORM_CLASSIFY_small2mid = inputStr['cfSmall2MidIndex'];
                self.HST_VISION_WORM_CLASSIFY_mid2big = inputStr['cfMid2BigIndex'];
                self.HST_VISION_WORM_CLASSIFY_big2top = inputStr['cfBig2TopIndex'];
                self.HST_VISION_WORM_CLASSIFY_pic_filename = inputStr['fileName'];
            else:
                print("L2VISCFY: func_vision_worm_input_processing on input error!")
        except Exception as err:
            text = "L2VISCFY: func_vision_worm_input_processing on input error = %s" % str(err)
            print(text);



    def func_vision_worm_binvalue_proc(self, img):
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
    
    
    
    def func_vision_worm_remove_noise_proc(self, img):
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
        #Init output figure
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalNbr'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['bigAlive'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['bigDead'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['middleAlive'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['middleDead'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['smallAlive'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['smallDead'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalAlive'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalDead'] = 0
        
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
        #叠加统计结果
        if (ModCebsCom.GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET == True):
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(outputImg, str(self.HST_VISION_WORM_CLASSIFY_pic_sta_output), (10, 30), font, 0.7, (0, 0, 255), 2, cv.LINE_AA)
        return outputImg;

    #Classified processing: 分类总处理
    #outCtrlFlag: 控制输出方式，是否直接使用fileNukeName而不增加文件名字选项
    def func_vision_worm_clasification(self, fileName, fileNukeName, outCtrlFlag):
        #Reading file: 读取文件
        if (os.path.exists(fileName) == False):
            errStr = "L2VISCFY: File %s not exist!" % (fileName)
            self.medErrorLog(errStr);
            print("L2VISCFY: File %s not exist!" % (fileName))
            return;
        self.HST_VISION_WORM_CLASSIFY_pic_filename = fileName
        try:
            inputImg = cv.imread(fileName)
        except Exception as err:
            print("L2VISCFY: Read file error, errinfo = ", str(err))
            return;

        #Processing procedure: 处理过程
        binImg = self.func_vision_worm_binvalue_proc(inputImg)
        nfImg = self.func_vision_worm_remove_noise_proc(binImg)
        outputImg = self.func_vision_worm_find_contours(nfImg, inputImg)
        if (outCtrlFlag == True):
            outputFn = fileNukeName
        else:
            outputFn = self.HST_VISION_WORM_CLASSIFY_pic_filepath + "result_" + fileNukeName
        print("L2VISCFY: OutputFn = %s, nuke name = %s" %(outputFn, fileNukeName))
        cv.imwrite(outputFn, outputImg)
            
        #Save log record: 存储干活的log记录
        f = open(ModCebsCom.GL_CEBS_VISION_CLAS_RESULT_FILE_NAME_SET, "a+")
        a = '[%s], vision worm classification ones, save result as [%s] with output [%s].\n' % (time.asctime(), outputFn, str(self.HST_VISION_WORM_CLASSIFY_pic_sta_output))
        f.write(a)
        f.close()
        
        #Show result or not: 根据指令，是否显示文件
        cv.destroyAllWindows()


    '''
    * 核心的识别函数，其它任务调用的主入口
    *
    *    用于荧光照片的识别处理过程
    *
    '''    
    def funcVisionFluClassifyProc(self):
        batch, fileNbr = self.findFluUnclasFileBatchAndNbr();
        print("batch/FileNbr=%d/%d" % (batch, fileNbr))
        if (batch < 0):
            ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT = 0;
            self.funcVisCfyLogTrace("L2VISCFY: Picture flu classification not finished: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT))
            self.updateCtrlCntInfo();
            return;
        fileName = self.getStoredFileName(batch, fileNbr);
        fileNukeName = self.getStoredFileNukeName(batch, fileNbr)
        if (fileName == None) or (fileNukeName == None):
            ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT = 0;
            self.funcVisCfyLogTrace("L2VISCFY: Picture flu classification finished: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT))
            self.updateCtrlCntInfo();
            return;
        #REAL PROCESSING PROCEDURE
        print("L2VISCFY: Flu picture batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
        self.algoVisFluWormCaculate(fileName, fileNukeName);
        ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT -= 1;
        #Update classified files
        self.updateUnclasFileAsClassified(batch, fileNbr);
        self.funcVisCfyLogTrace("L2VISCFY: Flu picture classification finished, remaining NUMBRES=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT))
        self.updateCtrlCntInfo();
        return;
    
    #荧光处理算法过程
    def algoVisFluWormCaculate(self, fileName, fileNukeName):
        self.funcVisCfyLogTrace("L2VISCFY: Flu picture classification simulation algorithms demo, to be finsihed!")


    
















    
    
        