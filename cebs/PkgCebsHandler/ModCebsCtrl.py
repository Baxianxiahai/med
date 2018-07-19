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

class classCtrlThread(QThread):
    signal_print_log = pyqtSignal(str) #DECLAR SIGNAL
    signal_ctrl_start = pyqtSignal() #DECLAR USED FOR MAIN FUNCTIONS
    signal_ctrl_stop = pyqtSignal()  #DECLAR USED FOR MAIN FUNCTIONS
    signal_ctrl_zero = pyqtSignal()  #DECLAR USED FOR MAIN FUNCTIONS
    signal_ctrl_clas_start = pyqtSignal() #DECLAR USED FOR MAIN FUNCTIONS
    signal_ctrl_clas_stop = pyqtSignal()  #DECLAR USED FOR MAIN FUNCTIONS
    signal_ctrl_calib_start = pyqtSignal() #DECLAR USED FOR MAIN FUNCTIONS
    signal_ctrl_calib_stop = pyqtSignal()  #DECLAR USED FOR MAIN FUNCTIONS
    
    #STATE MACHINE
    __CEBS_STM_CTRL_NULL =      0;
    __CEBS_STM_CTRL_INIT =      1;
    __CEBS_STM_CTRL_CAP_PIC =   2;
    __CEBS_STM_CTRL_CLAS =      3;
    __CEBS_STM_CTRL_CALIB =     4;
    __CEBS_STM_CTRL_ERR =       5;
    __CEBS_STM_CTRL_INVALID =   0xFF;

    def __init__(self,parent=None):
        super(classCtrlThread,self).__init__(parent)
        self.identity = None;
        self.times = -1;
        self.objInitCfg=ModCebsCfg.ConfigOpr();
        self.objMoto=ModCebsMoto.classMotoProcess();
        self.objVision=ModCebsVision.classVisionProcess();
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_NULL;
        
        #INIT DIFFERENT TARGET BOARDS AND NUMBERS
        if (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_96_STANDARD):
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_BATCH_MAX;
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_48_STANDARD):
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_BATCH_MAX;
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_32_STANDARD):
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_32_SD_BATCH_MAX;
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_12_STANDARD):
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_BATCH_MAX;
        else:
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_BOARD_BATCH_MAX;

        #INIT STM
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
        
    def setIdentity(self,text):
        self.identity = text

    def setTakePicWorkRemainNumber(self, val):
        self.times = int(val)+1
    
    def transferLogTrace(self, string):
        self.signal_print_log.emit(string)
        
    #TAKE PICTURE
    def funcTakePicStart(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.signal_print_log.emit("CTRL: funcTakePicStart PLS FINISH LAST TASK！")
            return -1;
        #NEW STATE
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CAP_PIC;
        #JUDGE WHETHER TAKING PICTURE IS FIXED POSITION OR NOT
        if (ModCebsCom.GL_CEBS_TAKING_PIC_FIX_POINT_SET == False):
            #MOTO START POINT
            if (self.objMoto.funcMotoMove2Start() < 0):
                self.signal_print_log.emit("CTRL: MOTO MOVING ERROR！")
                return -2;
        self.times = ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH+1;
        self.signal_print_log.emit("CTRL: START TAKING PICTURE: REMAINING TIMES=%d." %(self.times-1))
        self.objInitCfg.createBatch(ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX);

    #STOP TAKING PICTURE
    #THIS IS HIGH LEVEL SKILLS
    def funcTakePicStop(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_CAP_PIC):
            self.signal_print_log.emit("CTRL: funcTakePicStop PLS FINISH LAST TASK！")
            return -1;        
        self.times = 1
        #STOP TAKING PICTURE MIGHT DAMAGE WHOLE SYSTEM
#         self.signal_print_log.emit("CTRL: STOP PICTURE TAKING, REMAINING TIMES=%d." %(self.times))
#         ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX +=1;
#         self.objInitCfg.updateCtrlCntInfo();
#         self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
        return 1;
        #MOTO RUN TO ZERO POSITION: NONE-VALUABLE ACTIONS
#         if (self.objMoto.funcMotoBackZero() < 0):
#             self.signal_print_log.emit("SYSTME RUN TO ZERO ERROR!")
#             self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_ERR;
#             return -1;
#         else:
#             self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
#             return 1;

    #PLATE RUN TO INIT POSITION
    def funcCtrlMotoBackZero(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.signal_print_log.emit("CTRL: funcCtrlMotoBackZero PLS FINISH LAST TASK！")
            return -1;
        self.signal_print_log.emit("CTRL: MOTO RUN TO ZERO...")
        if (self.objMoto.funcMotoBackZero() < 0):
            self.signal_print_log.emit("CTRL: SYSTME RUN TO ZERO ERROR!")
            self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_ERR;
            return -1;
        else:
            self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
            return 1;
    
    #LOCAL FUNCTIONS  
    def funcCameraCapture(self, capIndex):
        curOne = ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH + 1 - capIndex;
        if ((curOne > ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH) or (curOne < 1)):
            self.signal_print_log.emit("CTRL: TAKING PICTURE SERIAL NUMBER ERROR!")
            return -1;
        self.objVision.funcVisionCapture(ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX, curOne);
        print("CTRL: Taking picture once! Current Batch=%d and Index =%d" % (ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX, curOne));
        self.objInitCfg.addBatchFile(ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX, curOne)
        #MOVINT TO NEXT WORKIN POSITION IN ADVANCE
        nextOne = curOne + 1;
        #IF ALREADY LAST POSITION, RUN TO ZERO
        if ((nextOne <= ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH) and (nextOne >=1)):
            if (self.objMoto.funcMotoMove2HoleNbr(nextOne) < 0):
                self.signal_print_log.emit("CTRL: MOTO MOVE ERROR!")
                return -1;
        else:
            if (self.objMoto.funcMotoBackZero() < 0):
                self.signal_print_log.emit("CTRL: SYSTEM RUN TO ZERO ERROR!")
                return -2;
    
    def funcVisionClasStart(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.signal_print_log.emit("CTRL: funcVisionClasStart PLS FINISH LAST TASK IN ADVANCE！")
            return -1;        
        self.objVision.funcVisionClasStart()
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CLAS;
    
    def funcVisionClasStop(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_CLAS):
            self.signal_print_log.emit("CTRL: funcVisionClasStop PLS FINISH LAST TASK IN ADVANCE!")
            return -1;
        self.objVision.funcVisionClasEnd()
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;

    def funcCtrlCalibStart(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.signal_print_log.emit("CTRL: funcCtrlCalibStart PLS FINISH LAST TASK IN ADVANCE!")
            return -1;        
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CALIB;
    
    def funcCtrlCalibStop(self):
        #print(self.CTRL_STM_STATE)
#         if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_CALIB):
#             self.signal_print_log.emit("CTRL: funcCtrlCalibStop PLS FINISH LAST TASK！")
#             return -1;
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
                self.times -= 1;
                if (self.times > 0):
                    self.signal_print_log.emit(str("CTRL: TAKING PICTURE, REMAINING TIMES=" + str(self.times)))
                    self.funcCameraCapture(self.times);
                    ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT += 1;
                    #CONTROL STOP ACTIONS
                elif (self.times == 0):
                    self.signal_print_log.emit("CTRL: STOP TAKING PICTURE, REMAINING TIMES=%d." %(self.times))
                    ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX +=1;
                    self.objInitCfg.updateCtrlCntInfo();
                    self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
        
        
        