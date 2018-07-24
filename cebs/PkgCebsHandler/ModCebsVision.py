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
        MaxDetectNbr = 100
        res = "Valid camera number: "
        for index in range(0, MaxDetectNbr):
            cap = cv.VideoCapture(index)
            if cap.isOpened():
                res = res + str(index) + ", "
        return res
         
    def funcVisionCapture(self, batch, fileNbr):
        #SELFCT CAMERA，#0-NOTEBOOK INTERNAL CAMERA，#1,#2 - EXTERNAL CAMERA
        cap = cv.VideoCapture(ModCebsCom.GL_CEBS_VISION_CAMBER_NBR) #CHECK WITH ls /dev/video*　RESULT
        # Check if the webcam is opened correctly
        if not cap.isOpened():
            #raise IOError("Cannot open webcam")
            self.objInitCfg.medErrorLog("VS_CAP: Cannot open webcam!")
            print("VS_CAP: Cannot open webcam!, Batch/Nbr=%d/%d" % (batch, fileNbr))
            return -1;

        #DEFINE PIC GRADULARITY
        cap.set(4,1440)
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

#MAIN PROCESSING MODULE
class classVisionThread(QThread):
    signal_print_log = pyqtSignal(str) #DECLAR MAIN FUNCTIONS
    signal_vision_start = pyqtSignal()  #DECLAR MAIN FUNCTIONS, NOT USED
    signal_vision_stop = pyqtSignal()   #DECLAR MAIN FUNCTIONS, NOT USED

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
            self.signal_print_log.emit("VS_CLAS: PICTURE IDENTIFY NOT FINISHED: REMAINING NUMBERS=%d." %(ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT))
            self.objInitCfg.updateCtrlCntInfo();
            return;
        fileName = self.objInitCfg.getStoredFileName(batch, fileNbr);
        if (fileName == None):
            ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT = 0;
            self.signal_print_log.emit("VS_CLASPICTURE IDENTIFY FINISHED: REMAINING NUMBERS=%d." %(ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT))
            self.objInitCfg.updateCtrlCntInfo();
            return;
        #REAL PROCESSING PROCEDURE
        print("VISION CLAS: Batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
        self.funcVisionClassify(fileName);
        ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT -= 1;
        self.objInitCfg.updateUnclasFileAsClassified(batch, fileNbr);
        self.signal_print_log.emit("VS_CLAS PIC IDENTIFY： REMAINING NUMBRES=%d." %(ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT))
    
    #PIC PROC
    def funcVisionClassify(self, filename):
        time.sleep(random.random()*10)
        
    def run(self):
        while True:
            time.sleep(1)
            if ((ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT > 0) and (ModCebsCom.GL_CEBS_PIC_CLAS_FLAG == True)):
                self.funcVisionProc();
                pass
        
        
        
        