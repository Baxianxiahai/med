'''
Created on 2018/5/2

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

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

#Local include
from cebsMain import *
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg
from PkgCebsHandler import ModCebsVision
from PkgCebsHandler import ModCebsMoto

#模块只能被WinMain调用，所以打印只会打到WinMain上去
class clsL3_CtrlSchdThread(QThread):
    sgL4MainWinPrtLog = pyqtSignal(str) #DECLAR SIGNAL
    sgL3CtrlCapStart = pyqtSignal() #DECLAR USED FOR MAIN FUNCTIONS
    sgL3CtrlCapStop = pyqtSignal()  #DECLAR USED FOR MAIN FUNCTIONS
    sgL3CtrlMotoZero = pyqtSignal()  #DECLAR USED FOR MAIN FUNCTIONS
    sgL3CtrlClfyStart = pyqtSignal() #DECLAR USED FOR MAIN FUNCTIONS
    sgL3CtrlClfyStop = pyqtSignal()  #DECLAR USED FOR MAIN FUNCTIONS
    sgL3CtrlCalibStart = pyqtSignal() #DECLAR USED FOR MAIN FUNCTIONS
    sgL3CtrlCalibStop = pyqtSignal()  #DECLAR USED FOR MAIN FUNCTIONS
    
    #STATE MACHINE
    __CEBS_STM_CTRL_NULL =      0;
    __CEBS_STM_CTRL_INIT =      1;
    __CEBS_STM_CTRL_CAP_PIC =   2;
    __CEBS_STM_CTRL_CLAS =      3;
    __CEBS_STM_CTRL_CALIB =     4;
    __CEBS_STM_CTRL_ERR =       5;
    __CEBS_STM_CTRL_INVALID =   0xFF;

    def __init__(self, father):
        super(clsL3_CtrlSchdThread, self).__init__()
        self.identity = None;
        self.capTimes = -1;
        self.instL4WinMainForm = father
        self.instL1ConfigOpr=ModCebsCfg.clsL1_ConfigOpr();
        self.instL2MotoProc=ModCebsMoto.clsL2_MotoProc(self.instL4WinMainForm, 1);
        self.instL2VisCapProc=ModCebsVision.clsL2_VisCapProc(self.instL4WinMainForm, 1);
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_NULL;
        
        #INIT DIFFERENT TARGET BOARDS AND NUMBERS
        if (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_96_STANDARD):
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_BATCH_MAX;
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_48_STANDARD):
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_BATCH_MAX;
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_24_STANDARD):
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_24_SD_BATCH_MAX;
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_12_STANDARD):
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_BATCH_MAX;
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_6_STANDARD):
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_6_SD_BATCH_MAX;
        else:
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_BATCH_MAX;

        #INIT STM
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
        
        
    def setIdentity(self,text):
        self.identity = text

    def setTakePicWorkRemainNumber(self, val):
        self.capTimes = int(val)+1
    
    def transferLogTrace(self, string):
        self.sgL4MainWinPrtLog.emit(string)
        
    #TAKE PICTURE
    def funcTakePicStart(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.sgL4MainWinPrtLog.emit("L3CTRLST: funcTakePicStart PLS FINISH LAST TASK！")
            return -1;
        #NEW STATE
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CAP_PIC;
        #JUDGE WHETHER TAKING PICTURE IS FIXED POSITION OR NOT
        if (ModCebsCom.GL_CEBS_PIC_TAKING_FIX_POINT_SET == False):
            #MOTO START POINT
            res, string = self.instL2MotoProc.funcMotoMove2Start()
            if (res < 0):
                self.sgL4MainWinPrtLog.emit("L3CTRLST: MOTO MOVING ERROR！")
                self.sgL4MainWinPrtLog.emit(string)
                return -2;
        self.capTimes = ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH+1;
        self.sgL4MainWinPrtLog.emit("L3CTRLST: START TAKING PICTURE: REMAINING TIMES=%d." %(self.capTimes-1))
        self.instL1ConfigOpr.createBatch(ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX);

    #STOP TAKING PICTURE
    #THIS IS HIGH LEVEL SKILLS
    def funcTakePicStop(self):
        if (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_INIT):
            self.sgL4MainWinPrtLog.emit("L3CTRLST: funcTakePicStop Already finished, no action！")
            self.capTimes = 1
            return 1;
        if (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CAP_PIC):
            self.capTimes = 1
        return 1;

    #PLATE RUN TO INIT POSITION
    def funcCtrlMotoBackZero(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.sgL4MainWinPrtLog.emit("L3CTRLST: funcCtrlMotoBackZero PLS FINISH LAST TASK！")
            return -1;
        self.sgL4MainWinPrtLog.emit("L3CTRLST: MOTO RUN TO ZERO...")
        if (self.instL2MotoProc.funcMotoBackZero() < 0):
            self.sgL4MainWinPrtLog.emit("L3CTRLST: SYSTME RUN TO ZERO GET ERROR FEEDBACK!")
            self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_ERR;
            return -1;
        else:
            self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
            self.sgL4MainWinPrtLog.emit("L3CTRLST: SYSTME RUN TO ZERO SUCCESSFUL!")
            return 1;
    
    #LOCAL FUNCTIONS  
    def funcCameraCapture(self, capIndex):
        curOne = ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH + 1 - capIndex;
        if ((curOne > ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH) or (curOne < 1)):
            self.sgL4MainWinPrtLog.emit("L3CTRLST: TAKING PICTURE SERIAL NUMBER ERROR!")
            return -1;
        self.instL2VisCapProc.funcVisionCapture(ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX, curOne);
        print("L3CTRLST: Taking picture once! Current Batch=%d and Index =%d" % (ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX, curOne));
        self.instL1ConfigOpr.addBatchFile(ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX, curOne)
        #MOVINT TO NEXT WORKIN POSITION IN ADVANCE
        nextOne = curOne + 1;
        
        #Using FIX Point set to un-make the moto moving step
        if (ModCebsCom.GL_CEBS_PIC_TAKING_FIX_POINT_SET == True):
            return 1;
        
        #IF ALREADY LAST POSITION, RUN TO ZERO
        if ((nextOne <= ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH) and (nextOne >=1)):
            if (self.instL2MotoProc.funcMotoMove2HoleNbr(nextOne) < 0):
                self.sgL4MainWinPrtLog.emit("L3CTRLST: MOTO MOVE ERROR!")
                return -1;
        else:
            if (self.instL2MotoProc.funcMotoBackZero() < 0):
                self.sgL4MainWinPrtLog.emit("L3CTRLST: SYSTEM RUN TO ZERO ERROR!")
                return -2;
        return 1;
    
    def funcVisionClasStart(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.sgL4MainWinPrtLog.emit("L3CTRLST: funcVisionClasStart PLS FINISH LAST TASK IN ADVANCE！")
            return -1;
        if (ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT <=0):
            self.sgL4MainWinPrtLog.emit("L3CTRLST: No remaining picture to classify, no action!")
            return -1;
        self.instL2VisCapProc.funcVisionClasStart()
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CLAS;
    
    def funcVisionClasStop(self):
        self.instL2VisCapProc.funcVisionClasEnd()
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;

    def funcCtrlCalibStart(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.sgL4MainWinPrtLog.emit("L3CTRLST: funcCtrlCalibStart PLS FINISH LAST TASK IN ADVANCE!")
            return -1;
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CALIB;
    
    def funcCtrlCalibStop(self):
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
        
    def funcCtrlGetRightStatus(self):
        if (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_INIT):
            return 1;
        else:
            return -1;
        
    def run(self):
        while True:
            time.sleep(1)
            if (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CAP_PIC):
                self.capTimes -= 1;
                if (self.capTimes > 0):
                    self.sgL4MainWinPrtLog.emit(str("L3CTRLST: TAKING PICTURE, REMAINING TIMES=" + str(self.capTimes)))
                    self.funcCameraCapture(self.capTimes);
                    ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT += 1;
                    #CONTROL STOP ACTIONS
                elif (self.capTimes == 0):
                    self.sgL4MainWinPrtLog.emit("L3CTRLST: STOP TAKING PICTURE, REMAINING TIMES=%d." %(self.capTimes))
                    ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX +=1;
                    self.instL1ConfigOpr.updateCtrlCntInfo();
                    self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
        
        
        