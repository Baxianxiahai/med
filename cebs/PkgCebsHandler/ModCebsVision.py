'''
Created on 2018年5月4日

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
        pass
         
    def funcVisionCapture(self, batch, fileNbr):
        # 选取摄像头，0为笔记本内置的摄像头，1,2···为外接的摄像头**
        cap = cv.VideoCapture(0)#括号里的数和ls /dev/video*　结果有关
        # Check if the webcam is opened correctly
        if not cap.isOpened():
            #raise IOError("Cannot open webcam")
            print("VS_CAP: Cannot open webcam!, Batch/Nbr=%d/%d" % (batch, fileNbr))
            return -1;

        #定义摄像头的分辨率
        cap.set(4,720)
        #大量的错和坑出现在这里
        #第一个参数是路径和文件名
        #第二个参数是视频格式，“MPEG”是一**种标准格式，百度fourcc可见各种格式
        #第二个参数（fourcc）如果设置为-1，允许实时选择视频格式
        #fourcc = cv.VideoWriter_fourcc(*"MPEG")
        #fourcc=-1**
        # 第三个参数则是镜头快慢的，20为正常，小于二十为慢镜头**
        #out = cv.VideoWriter('c://output.avi',fourcc,20,(640,480))
        ret, frame = cap.read()
        if (ret == True):
            frame = cv.flip(frame, 1)# 在帧上进行操作
            frame = cv.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_AREA)
            #cv.imshow('Input', frame)
            obj=ModCebsCfg.ConfigOpr();
            fileName = obj.combineFileNameWithDir(batch, fileNbr)
            cv.imwrite(fileName, frame)
        cap.release()
        cv.destroyAllWindows()
        return 1;

    def funcVisionClasStart(self):
        ModCebsCom.GL_CEBS_PIC_CLAS_FLAG = True;

    def funcVisionClasEnd(self):
        ModCebsCom.GL_CEBS_PIC_CLAS_FLAG = False;

#主处理任务模块
class classVisionThread(QThread):
    signal_print_log = pyqtSignal(str) #申明发送信号
    signal_vision_start = pyqtSignal()  #申明发送给主函数的信号，暂时未使用
    signal_vision_stop = pyqtSignal()   #申明发送给主函数的信号，暂时未使用

    def __init__(self,parent=None):
        super(classVisionThread,self).__init__(parent)
        self.identity = None;
        self.objInitCfg=ModCebsCfg.ConfigOpr();
        
    def setIdentity(self,text):
        self.identity = text

    def funcVisionProc(self):
        batch, fileNbr = self.objInitCfg.findUnclasFileBatchAndFileNbr();
        if (batch < 0):
            ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT = 0;
            self.signal_print_log.emit("VS_CLAS: 图片识别完成： 还剩照片数量=%d." %(ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT))
            self.objInitCfg.updateCtrlCntInfo();
            return;
        fileName = self.objInitCfg.getStoredFileName(batch, fileNbr);
        if (fileName == None):
            ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT = 0;
            self.signal_print_log.emit("VS_CLAS图片识别完成： 还剩照片数量=%d." %(ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT))
            self.objInitCfg.updateCtrlCntInfo();
            return;
        #真正的处理过程
        print("VISION CLAS: Batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
        self.funcVisionClassify(fileName);
        ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT -= 1;
        self.objInitCfg.updateUnclasFileAsClassified(batch, fileNbr);
        self.signal_print_log.emit("VS_CLAS图片识别完成： 还剩照片数量=%d." %(ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT))
    
    #对着图像进行处理
    def funcVisionClassify(self, filename):
        time.sleep(random.random()*10)
        
    def run(self):
        while True:
            time.sleep(1)
            if ((ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT > 0) and (ModCebsCom.GL_CEBS_PIC_CLAS_FLAG == True)):
                self.funcVisionProc();
                pass
        
        
        
        