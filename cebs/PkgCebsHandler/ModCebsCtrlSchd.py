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
    sgL3CtrlCapStartNormal = pyqtSignal() #DECLAR USED FOR MAIN FUNCTIONS
    sgL3CtrlCapStartFlu = pyqtSignal() #DECLAR USED FOR MAIN FUNCTIONS
    sgL3CtrlCapStop = pyqtSignal()  #DECLAR USED FOR MAIN FUNCTIONS
    sgL3CtrlMotoZero = pyqtSignal()  #DECLAR USED FOR MAIN FUNCTIONS
    sgL3CtrlClfyStartNormal = pyqtSignal() #DECLAR USED FOR MAIN FUNCTIONS
    sgL3CtrlClfyStartFlu = pyqtSignal() #DECLAR USED FOR MAIN FUNCTIONS
    sgL3CtrlClfyStop = pyqtSignal()  #DECLAR USED FOR MAIN FUNCTIONS
    sgL3CtrlCalibStart = pyqtSignal() #DECLAR USED FOR MAIN FUNCTIONS
    sgL3CtrlCalibStop = pyqtSignal()  #DECLAR USED FOR MAIN FUNCTIONS
    
    #STATE MACHINE
    __CEBS_STM_CTRL_NULL =      0;
    __CEBS_STM_CTRL_INIT =      1;
    __CEBS_STM_CTRL_CAP_PIC_NOR =   2;  #抓取图片
    __CEBS_STM_CTRL_CAP_NOR_CMPL =  3;
    __CEBS_STM_CTRL_CFY_PROC_NOR =  4;  #识别处理图片
    __CEBS_STM_CTRL_CFY_CMPL_NOR =  5;
    __CEBS_STM_CTRL_CAP_PIC_FLU =   6;  #抓取图片
    __CEBS_STM_CTRL_CAP_FLU_CMPL =  7;
    __CEBS_STM_CTRL_CFY_PROC_FLU =  8;  #识别处理图片
    __CEBS_STM_CTRL_CFY_CMPL_FLU =  9;
    __CEBS_STM_CTRL_CALIB =     10;  #校准过程
    __CEBS_STM_CTRL_ERR =       11;
    __CEBS_STM_CTRL_INVALID =   0xFF;

    def __init__(self, father):
        super(clsL3_CtrlSchdThread, self).__init__()
        self.identity = None;
        self.capTimes = -1;
        self.instL4WinMainForm = father
        self.instL1ConfigOpr=ModCebsCfg.clsL1_ConfigOpr();
        self.instL2MotoProc=ModCebsMoto.clsL2_MotoProc(self.instL4WinMainForm);
        self.instL2VisCapProc=ModCebsVision.clsL2_VisCapProc(self.instL4WinMainForm);
        self.instL2VisCfyProc=ModCebsVision.clsL2_VisCfyProc(self.instL4WinMainForm);
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_NULL;
        
        #INIT DIFFERENT TARGET BOARDS AND NUMBERS
        if (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_96_STANDARD):
            ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH = ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_96_SD_BATCH_MAX;
        elif (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_48_STANDARD):
            ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH = ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_48_SD_BATCH_MAX;
        elif (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_24_STANDARD):
            ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH = ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_24_SD_BATCH_MAX;
        elif (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_12_STANDARD):
            ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH = ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_12_SD_BATCH_MAX;
        elif (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_6_STANDARD):
            ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH = ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_6_SD_BATCH_MAX;
        else:
            ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH = ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_96_SD_BATCH_MAX;

        #INIT STM
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
        self.funcCtrlSchdDebugPrint("L3CTRLST: Instance start!")
    
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
    #TAKE PICTURE NORMAL
    def funcTakePicStartNormal(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.funcCtrlSchdDebugPrint("L3CTRLST: Please finish last action firstly！")
            return -1;
        #JUDGE WHETHER TAKING PICTURE IS FIXED POSITION OR NOT
        if (ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET == False):
            #MOTO START POINT
            res, string = self.instL2MotoProc.funcMotoMove2Start()
            if (res < 0):
                self.funcCtrlSchdDebugPrint("L3CTRLST: Moto movement error！")
                self.funcCtrlSchdDebugPrint(string)
                return -2;
        self.instL1ConfigOpr.createBatch(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX);
        #NEW STATE
        print("point test A")
        self.instL2VisCapProc.funcVisBatCapStart();
        print("point test B")
        #去掉初始3-4张黑屏幕的照片
        self.funcCamCapInBatch(ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH, ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_NORMAL, True);
        self.funcCamCapInBatch(ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH, ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_NORMAL, True);
        self.funcCamCapInBatch(ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH, ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_NORMAL, True);
        self.funcCamCapInBatch(ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH, ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_NORMAL, True);
        print("point test C")
        self.funcCtrlSchdDebugPrint("L3CTRLST: Normal picture starting progress...")
        self.capTimes = ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH+1;
        self.funcCtrlSchdDebugPrint("L3CTRLST: Start to take normal picture, remaining TIMES=%d." %(self.capTimes-1))
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CAP_PIC_NOR;

    #TAKE PICTURE FLU
    def funcTakePicStartFlu(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.funcCtrlSchdDebugPrint("L3CTRLST: Please finish last action firstly！")
            return -1;
        #JUDGE WHETHER TAKING PICTURE IS FIXED POSITION OR NOT
        if (ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET == False):
            #MOTO START POINT
            res, string = self.instL2MotoProc.funcMotoMove2Start()
            if (res < 0):
                self.funcCtrlSchdDebugPrint("L3CTRLST: Moto movement error！")
                self.funcCtrlSchdDebugPrint(string)
                return -2;
        self.instL1ConfigOpr.createBatch(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX);
        
        #NEW STATE
        self.instL2VisCapProc.funcVisBatCapStart();
        
        #去掉初始3-4张黑屏幕的照片
        self.funcCamCapInBatch(ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH, ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_FLUORESCEN, True);
        self.funcCamCapInBatch(ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH, ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_FLUORESCEN, True);
        self.funcCamCapInBatch(ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH, ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_FLUORESCEN, True);
        self.funcCamCapInBatch(ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH, ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_FLUORESCEN, True);
        self.funcCtrlSchdDebugPrint("L3CTRLST: Flu picture starting progress...")
        self.capTimes = ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH+1;
        self.funcCtrlSchdDebugPrint("L3CTRLST: Start to take flu picture, remaining TIMES=%d." %(self.capTimes-1))
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CAP_PIC_FLU;
        
    #STOP TAKING PICTURE
    def funcTakePicStop(self):
        if (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_INIT):
            self.funcCtrlSchdDebugPrint("L3CTRLST: funcTakePicStop Already finished, no action！")
        elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CAP_PIC_NOR):
            self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CAP_NOR_CMPL
        elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CAP_PIC_FLU):
            self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CAP_FLU_CMPL
        else:
            self.funcCtrlSchdDebugPrint("L3CTRLST: funcTakePicStop wrong click, no action！")

    #CLASSIFICATION NORMAL
    def funcVisionClasStartNormal(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.funcCtrlSchdDebugPrint("L3CTRLST: funcVisionClasStartNormal Please finish last action firstly！")
            return -1;
        if (ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT <=0):
            self.funcCtrlSchdDebugPrint("L3CTRLST: No remaining normal picture to classify, no action!")
            return -2;
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CFY_PROC_NOR;

    #CLASSIFICATION FLU
    def funcVisionClasStartFlu(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.funcCtrlSchdDebugPrint("L3CTRLST: funcVisionClasStartNormal Please finish last action firstly！")
            return -1;
        if (ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT <=0):
            self.funcCtrlSchdDebugPrint("L3CTRLST: No remaining flu picture to classify, no action!")
            return -2;
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CFY_PROC_FLU;
            
    def funcVisionClasStop(self):
        if (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_INIT):
            self.funcCtrlSchdDebugPrint("L3CTRLST: funcVisionClasStop Already finished, no action！")
        elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CFY_PROC_NOR):
            self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CFY_CMPL_NOR
        elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CFY_PROC_FLU):
            self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CFY_CMPL_FLU
        else:
            self.funcCtrlSchdDebugPrint("L3CTRLST: funcVisionClasStop wrong click, no action！")

    #CALIBRATION
    def funcCtrlCalibStart(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.funcCtrlSchdDebugPrint("L3CTRLST: funcCtrlCalibStart Please finish last action firstly!")
            return -1;
        #给CalibForm下的CalibTask一个驱动信号，以便完成该干的事
        self.instL4WinMainForm.instL4CalibForm.sgL4CalibFormActiveTrig.emit()
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
    * 支持函数部分
    * 
    * Input: forceFlag, 指明是否跳过视频部分
    *        fmtFlag, Normal or Flu格式
    '''                        
    #LOCAL FUNCTIONS  
    def funcCamCapInBatch(self, capIndex, fmFlag, forceFlag):
        #计算当前批次
        curOne = ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH + 1 - capIndex;
        if ((curOne > ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH) or (curOne < 1)):
            self.funcCtrlSchdDebugPrint("L3CTRLST: Taking picture but serial number error!")
            return -1;
        #获取图像
        ret = self.instL2VisCapProc.funcVisionCapture(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, curOne, forceFlag);
        print("L3CTRLST: Taking picture once! Current Batch=%d and Index =%d" % (ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, curOne));
        #存盘
        if (fmFlag == ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_NORMAL):
            self.instL1ConfigOpr.addNormalBatchFile(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, curOne)
        if (fmFlag == ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_FLUORESCEN):
            self.instL1ConfigOpr.addFluBatchFile(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, curOne)
        #Video captured
        if (ret == 2):
            self.instL1ConfigOpr.updBatchFileVideo(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, curOne)
        #MOVINT TO NEXT WORKIN POSITION IN ADVANCE
        nextOne = curOne + 1;
        #Using FIX Point set to un-make the moto moving step
        if (ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET == True):
            return 1;
        #IF ALREADY LAST POSITION, RUN TO ZERO
        if ((nextOne <= ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH) and (nextOne >=1)):
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

    def funcCtrlGetSpsRights(self, par):
        self.instL2MotoProc.funcGetSpsRights(par);

    def funcCtrlRelSpsRights(self, par):
        self.instL2MotoProc.funcRelSpsRights(par);



    '''
          任务主程序
    '''                        
    def run(self):
        while True:
            
            #初始化等待
            if (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_INIT):
                time.sleep(1)
 
            #批量抓取照片-NORMAL的白光照片
            elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CAP_PIC_NOR):
                self.capTimes -= 1;
                if (self.capTimes > 0):
                    self.funcCtrlSchdDebugPrint(str("L3CTRLST: Taking normal picture, remaining TIMES=" + str(self.capTimes-1)))
                    self.funcCamCapInBatch(self.capTimes, ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_NORMAL, False);
                    ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT += 1;
                #CONTROL STOP ACTIONS
                else:
                    self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CAP_NOR_CMPL
             
            #批量抓取完成，需要做最后一次的清理工作 NORMAL
            elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CAP_NOR_CMPL):
                self.funcCtrlSchdDebugPrint("L3CTRLST: Stop taking normal picture, remaining  TIMES=%d." %(self.capTimes-1))
                ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX +=1;
                self.instL1ConfigOpr.updateCtrlCntInfo();
                self.instL2VisCapProc.funcVisBatCapStop();
                self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
             
            #批量处理识别照片 NORMAL
            elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CFY_PROC_NOR):
                self.instL2VisCfyProc.funcVisionNormalClassifyProc();
                if (ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT <= 0):
                    self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CFY_CMPL_NOR
             
            #批量识别完毕 NORMAL
            elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CFY_CMPL_NOR):
                self.funcCtrlSchdDebugPrint("L3VISCFY: Finish all normal picture classification!")
                #是否需要更新文件？留下入口
                self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT
            
            #批量抓取照片-FLU
            elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CAP_PIC_FLU):
                self.capTimes -= 1;
                if (self.capTimes > 0):
                    self.funcCtrlSchdDebugPrint(str("L3CTRLST: Taking flu picture, remaining TIMES=" + str(self.capTimes-1)))
                    self.funcCamCapInBatch(self.capTimes, ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_FLUORESCEN, False);
                    ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT += 1;
                #CONTROL STOP ACTIONS
                else:
                    self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CAP_FLU_CMPL           
            
            #批量抓取完成，需要做最后一次的清理工作 FLU
            elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CAP_FLU_CMPL):
                self.funcCtrlSchdDebugPrint("L3CTRLST: Stop taking flu picture, remaining  TIMES=%d." %(self.capTimes-1))
                ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX +=1;
                self.instL1ConfigOpr.updateCtrlCntInfo();
                self.instL2VisCapProc.funcVisBatCapStop();
                self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
                
            #批量处理识别照片 FLU
            elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CFY_PROC_FLU):
                self.instL2VisCfyProc.funcVisionFluClassifyProc();
                if (ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT <= 0):
                    self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CFY_CMPL_FLU
             
            #批量识别完毕 FLU
            elif (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CFY_CMPL_FLU):
                self.funcCtrlSchdDebugPrint("L3VISCFY: Finish all flu picture classification!")
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
              
            
            
            
            
            
            
            
        
        