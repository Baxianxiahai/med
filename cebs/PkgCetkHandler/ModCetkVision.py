'''
Created on 2018年12月8日

@author: Administrator
'''

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
from ctypes import c_uint8
import win32com.client  #pip install pyWin32
import usb.core

from multiprocessing import Queue, Process
from PkgVmHandler import ModVmCfg
from PkgVmHandler import ModVmLayer
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
from cebsTkL4Ui import *
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg
from cv2 import waitKey

class tupTaskVision(ModVmLayer.tupTaskTemplate):
    _STM_ACTIVE = 3
    #主界面，干活拍照
    _STM_MAIN_UI_ACT = 4
    #校准模式下图像直接读取
    _STM_CALIB_UI_ACT = 5

    def __init__(self):
        ModVmLayer.tupTaskTemplate.__init__(self, taskid=ModVmCfg.TUP_TASK_ID_VISION, taskName="TASK_VISION")
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_VISION, self)
        self.capInit = ''
        self.fsm_set(ModVmLayer.TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(ModVmLayer.TUP_STM_INIT, ModVmCfg.TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_TIME_OUT, self.fsm_msg_time_out_rcv_handler)
        #通知界面切换
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_MAIN_UI_SWITCH, self.fsm_msg_main_ui_switch_rcv_handler)
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_CALIB_UI_SWITCH, self.fsm_msg_calib_ui_switch_rcv_handler)

        #校准模式下的抓图指令
        self.add_stm_combine(self._STM_CALIB_UI_ACT, ModVmCfg.TUP_MSGID_PIC_CAP_REQ, self.fsm_msg_calib_pic_cap_req_rcv_handler)

        #主界面业务模式下的抓图指令
        self.add_stm_combine(self._STM_MAIN_UI_ACT, ModVmCfg.TUP_MSGID_PIC_CAP_REQ, self.fsm_msg_main_pic_cap_req_rcv_handler)
        self.add_stm_combine(self._STM_MAIN_UI_ACT, ModVmCfg.TUP_MSGID_PIC_CLFY_REQ, self.fsm_msg_main_pic_clfy_req_rcv_handler)
        
        #切换状态机
        self.fsm_set(ModVmLayer.TUP_STM_INIT)
        #START TASK
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        time.sleep(0.5) #WAIT FOR OTHER TASK STARTUP
        self.instL1ConfigOpr = ModCebsCfg.clsL1_ConfigOpr()
        self.tup_dbg_print("L2VISCAP: Instance start test!")
        self.funcVisionLogTrace("L2VISCAP: Instance start test!")
        #全局搜索摄像头
        res = self.funcVisionDetectAllCamera()
        self.funcVisionLogTrace(str(res))
        #INIT
        if (self.funcGetCamRightAndInit() < 0):
            self.tup_err_print("L2VISCAP: Init CAM error!")
            self.funcVisionLogTrace("L2VISCAP: Init CAM error!")
            return ModVmLayer.TUP_FAILURE;
        else:
            self.fsm_set(self._STM_ACTIVE)
            return ModVmLayer.TUP_SUCCESS;

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return ModVmLayer.TUP_SUCCESS;
        
    def fsm_msg_time_out_rcv_handler(self, msgContent):
        return ModVmLayer.TUP_SUCCESS;

    def fsm_msg_main_ui_switch_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_MAIN_UI_ACT)
        return ModVmLayer.TUP_SUCCESS;

    def fsm_msg_calib_ui_switch_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_CALIB_UI_ACT)
        return ModVmLayer.TUP_SUCCESS;

    def funcVisionLogTrace(self, myString):
        msgSnd = {}
        msgSnd['mid'] = ModVmCfg.TUP_MSGID_TRACE
        msgSnd['src'] = self.taskId
        msgSnd['content'] = myString
        self.fsm_set(self._STM_ACTIVE)
        if (self.state == self._STM_MAIN_UI_ACT):
            msgSnd['dst'] = ModVmCfg.TUP_TASK_ID_UI_MAIN
            self.msg_send_out(ModVmCfg.TUP_TASK_ID_UI_MAIN, msgSnd)
        elif (self.state == self._STM_CALIB_UI_ACT):
            msgSnd['dst'] = ModVmCfg.TUP_TASK_ID_UI_CALIB
            self.msg_send_out(ModVmCfg.TUP_TASK_ID_UI_CALIB, msgSnd)
        else:
            msgSnd['dst'] = ModVmCfg.TUP_TASK_ID_UI_MAIN
            self.msg_send_out(ModVmCfg.TUP_TASK_ID_UI_MAIN, msgSnd)

    def fsm_msg_calib_pic_cap_req_rcv_handler(self, msgContent):
        scale = int(msgContent['scale'])
        self.funcMotoMoveOneStep(scale, dir)        
        return ModVmLayer.TUP_SUCCESS;

    def fsm_msg_main_pic_cap_req_rcv_handler(self, msgContent):
        return ModVmLayer.TUP_SUCCESS;

    def fsm_msg_main_pic_clfy_req_rcv_handler(self, msgContent):
        return ModVmLayer.TUP_SUCCESS;

    '''
    SERVICE PART: 业务部分的函数，功能处理函数
    '''
    #搜索摄像头
    def funcVisionDetectAllCamera(self):
        res = "L2VISCAP: Valid camera number = "
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
                    ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR = int(result[2])
                except Exception:
                    ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR = -1
        return res + str(ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR)
    
    #初始化摄像头
    def funcGetCamRightAndInit(self):
        if (ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR < 0):
            self.tup_err_print("L2VISCAP: Camera not yet installed!");
            self.funcVisionLogTrace("L2VISCAP: Camera not yet installed!");
            return -1;
        else:
            self.capInit = cv.VideoCapture(ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR) #CHECK WITH ls /dev/video*　RESULT
            self.capInit.set(3, ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_RES_WITDH)
            self.capInit.set(4, ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_RES_HEIGHT)
            return 1;
    
    #截获图像
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
            if ModCebsCom.GLVIS_PAR_OFC.PIC_SCALE_ENABLE_FLAG == True:
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

























