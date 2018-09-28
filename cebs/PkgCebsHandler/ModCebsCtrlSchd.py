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
    __CEBS_STM_CTRL_CAP_PIC =   2;  #抓取图片
    __CEBS_STM_CTRL_CAP_CMPL =  3;
    __CEBS_STM_CTRL_CFY_PROC =  4;  #识别处理图片
    __CEBS_STM_CTRL_CFY_CMPL =  5;
    __CEBS_STM_CTRL_CALIB =     6;  #校准过程
    __CEBS_STM_CTRL_ERR =       7;
    __CEBS_STM_CTRL_INVALID =   0xFF;

    def __init__(self, father):
        super(clsL3_CtrlSchdThread, self).__init__()
        self.identity = None;
        self.capTimes = -1;
        self.instL4WinMainForm = father
        self.instL1ConfigOpr=ModCebsCfg.clsL1_ConfigOpr();
        self.instL2MotoProc=ModCebsMoto.clsL2_MotoProc(self.instL4WinMainForm, 1);
        self.instL2VisCapProc=ModCebsVision.clsL2_VisCapProc(self.instL4WinMainForm, 1);
        self.instL2VisCfyProc=ModCebsVision.clsL2_VisCfyProc(self.instL4WinMainForm);
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
        self.funcCtrlSchdDebugPrint("L3CTRLST: Instance start test!")
    
    '''
          基础函数部分
    '''        
    def setIdentity(self,text):
        self.identity = text

    def funcCtrlStateGet(self):
        return self.CTRL_STM_STATE

    def funcCtrlSchdDebugPrint(self, string):
        self.sgL4MainWinPrtLog.emit(string)

    def funcResetWkStatus(self):
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;

    '''
          执行界面控制命令函数部分
    '''                        
    #TAKE PICTURE
    def funcTakePicStart(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.funcCtrlSchdDebugPrint("L3CTRLST: Please finish last action firstly！")
            return -1;
        #JUDGE WHETHER TAKING PICTURE IS FIXED POSITION OR NOT
        if (ModCebsCom.GL_CEBS_PIC_TAKING_FIX_POINT_SET == False):
            #MOTO START POINT
            res, string = self.instL2MotoProc.funcMotoMove2Start()
            if (res < 0):
                self.funcCtrlSchdDebugPrint("L3CTRLST: Moto movement error！")
                self.funcCtrlSchdDebugPrint(string)
                return -2;
        self.capTimes = ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH+1;
        self.funcCtrlSchdDebugPrint("L3CTRLST: Start to take picture, remaining TIMES=%d." %(self.capTimes-1))
        self.instL1ConfigOpr.createBatch(ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX);
        #NEW STATE
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CAP_PIC;

    #STOP TAKING PICTURE
    def funcTakePicStop(self):
        if (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_INIT):
            self.funcCtrlSchdDebugPrint("L3CTRLST: funcTakePicStop Already finished, no action！")
        elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CAP_PIC):
            self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CAP_CMPL
        else:
            self.funcCtrlSchdDebugPrint("L3CTRLST: funcTakePicStop wrong click, no action！")

    #CLASSIFICATION
    def funcVisionClasStart(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.funcCtrlSchdDebugPrint("L3CTRLST: funcVisionClasStart Please finish last action firstly！")
            return -1;
        if (ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT <=0):
            self.funcCtrlSchdDebugPrint("L3CTRLST: No remaining picture to classify, no action!")
            return -2;
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CFY_PROC;
    
    def funcVisionClasStop(self):
        if (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_INIT):
            self.funcCtrlSchdDebugPrint("L3CTRLST: funcVisionClasStop Already finished, no action！")
        elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CFY_PROC):
            self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CFY_CMPL
        else:
            self.funcCtrlSchdDebugPrint("L3CTRLST: funcVisionClasStop wrong click, no action！")

    #CALIBRATION
    def funcCtrlCalibStart(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.funcCtrlSchdDebugPrint("L3CTRLST: funcCtrlCalibStart Please finish last action firstly!")
            return -1;
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CALIB;
    
    def funcCtrlCalibStop(self):
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;

    #PLATE RUN TO INIT POSITION
    def funcCtrlMotoBackZero(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.funcCtrlSchdDebugPrint("L3CTRLST: funcCtrlMotoBackZero Please finish last action firstly！")
            return -1;
        self.funcCtrlSchdDebugPrint("L3CTRLST: Moto run to zero position...")
        if (self.instL2MotoProc.funcMotoBackZero() < 0):
            self.funcCtrlSchdDebugPrint("L3CTRLST: System run to zero get error feedback!")
            self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_ERR;
            return -1;
        else:
            self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
            self.funcCtrlSchdDebugPrint("L3CTRLST: System run to zero successful!")
            return 1;
        
    '''
          支持函数部分
    '''                        
    #LOCAL FUNCTIONS  
    def funcCameraCapture(self, capIndex):
        curOne = ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH + 1 - capIndex;
        if ((curOne > ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH) or (curOne < 1)):
            self.funcCtrlSchdDebugPrint("L3CTRLST: Taking picture but serial number error!")
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
                self.funcCtrlSchdDebugPrint("L3CTRLST: Moto run error!")
                return -1;
        else:
            if (self.instL2MotoProc.funcMotoBackZero() < 0):
                self.funcCtrlSchdDebugPrint("L3CTRLST: System run to zero error!")
                return -2;
        return 1;
    
    def setTakePicWorkRemainNumber(self, val):
        self.capTimes = int(val)+1
           
    def funcCtrlGetRightStatus(self):
        if (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_INIT):
            return 1;
        else:
            return -1;

    '''
          任务主程序
    '''                        
    def run(self):
        while True:
            pass
            
            #初始化等待
            if (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_INIT):
                time.sleep(1)
 
            #批量抓取照片
            elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CAP_PIC):
                self.capTimes -= 1;
                if (self.capTimes > 0):
                    self.funcCtrlSchdDebugPrint(str("L3CTRLST: Taking picture, remaining TIMES=" + str(self.capTimes)))
                    self.funcCameraCapture(self.capTimes);
                    ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT += 1;
                #CONTROL STOP ACTIONS
                else:
                    self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CAP_CMPL
             
            #批量抓取完成，需要做最后一次的清理工作
            elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CAP_CMPL):
                self.funcCtrlSchdDebugPrint("L3CTRLST: Stop taking picture, remaining  TIMES=%d." %(self.capTimes))
                ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX +=1;
                self.instL1ConfigOpr.updateCtrlCntInfo();
                self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
             
            #批量处理识别照片
            elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CFY_PROC):
                self.instL2VisCfyProc.funcVisionProc();
                if (ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT <= 0):
                    self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CFY_CMPL
             
            #批量识别完毕
            elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CFY_CMPL):
                self.funcCtrlSchdDebugPrint("L3VISCFY: Finish all picture classification!")
                #是否需要更新文件？留下入口
                self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT
            
            #错误状态
            elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_ERR):
                self.funcCtrlSchdDebugPrint("L3VISCFY: Error state come back!")
                self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT
            
            #校准状态
            elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CALIB):
                time.sleep(1)
             
            #重大错误，退出进程
            else:
                self.funcCtrlSchdDebugPrint("L3VISCFY: Critical error found in CTRL STM, pls restart your program!")
                return 1;
              
            
            
            
            
            
            
            
        
        