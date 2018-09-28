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
import datetime
import string
import ctypes 
import threading
import random
import cv2 as cv
import numpy as np  
from ctypes import c_uint8
from cv2 import waitKey

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *

#Local include
from cebsMain import *
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg
from PkgCebsHandler import ModCebsVision
from PkgCebsHandler import ModCebsMoto


#校准处理过程
#模块只能被CalibForm调用，所以打印只会打到CalibForm上去
class clsL3_CalibProc(object):
    def __init__(self, father):
        super(clsL3_CalibProc, self).__init__()
        self.identity = None;
        self.instL4CalibForm = father
        self.camerEnableFlag = False;
        self.instL1ConfigOpr=ModCebsCfg.clsL1_ConfigOpr();
        self.instL2MotoProc=ModCebsMoto.clsL2_MotoProc(self.instL4CalibForm, 2);
        self.initParameter();

    def initParameter(self):
        #STEP1: 判定产品型号
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
        #STEP2：初始化工作环境
        self.funcInitHoleBoardPar();
        self.funcCleanWorkingEnv()
        #STEP3：初始化Pilot任务
        self.instL2CalibPiThd = clsL2_CalibPilotThread(self.instL4CalibForm, self.instL2MotoProc)
        self.instL2CalibPiThd.setIdentity("TASK_CalibPilotThread")
        self.instL2CalibPiThd.sgL3CalibFormPrtLog.connect(self.funcCalibLogTrace)
        self.instL2CalibPiThd.sgL2PiStart.connect(self.instL2CalibPiThd.funcCalibMotoPilotStart)
        self.instL2CalibPiThd.sgL2PiStop.connect(self.instL2CalibPiThd.funcCalibMotoPilotStop)
        self.instL2CalibPiThd.start();
        #STEP3：初始化摄像头视频展示任务，这一步的目的是为了初始化下面这个变量
        #还有好处：即便没有手动激活过这个，在退出时依然可以操作该Handler，不然就会出现崩溃的情况，从而简化了异常处理
        self.instL2CalibCamDisThd = clsL2_CalibCamDispThread(self.instL4CalibForm, 1);
        self.instL2CalibCamDisThd.setIdentity("TASK_CalibCameraDisplay")
        self.instL2CalibCamDisThd.start();
        #STE4: DebugTrace
        self.funcCalibLogTrace("L3CALIB: Instance start test!")
                        
    def setIdentity(self,text):
        self.identity = text

    def funcCalibLogTrace(self, myString):
        self.instL4CalibForm.calib_print_log(myString)

    def funcCleanWorkingEnv(self):
        if (self.instL2MotoProc.funcMotoRunningStatusInquery() == True):
            self.instL2MotoProc.funcMotoStop()        

    def funcRecoverWorkingEnv(self):
        self.instL2MotoProc.funcMotoStop();
    
    def funcInitHoleBoardPar(self):
        if (ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE == 0 or ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE == 0 or ModCebsCom.GL_CEBS_HB_HOLE_X_NUM == 0 or ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM == 0):
            if (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_96_STANDARD):
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_XDIR_NBR;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_YDIR_NBR;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
            elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_48_STANDARD):
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_XDIR_NBR;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_YDIR_NBR;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
            elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_24_STANDARD):
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = ModCebsCom.GL_CEBS_HB_TARGET_24_SD_XDIR_NBR;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = ModCebsCom.GL_CEBS_HB_TARGET_24_SD_YDIR_NBR;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_24_SD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_24_SD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
            elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_12_STANDARD):
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_XDIR_NBR;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_YDIR_NBR;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
            elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_6_STANDARD):
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = ModCebsCom.GL_CEBS_HB_TARGET_6_SD_XDIR_NBR;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = ModCebsCom.GL_CEBS_HB_TARGET_6_SD_YDIR_NBR;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_6_SD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_6_SD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
            else:
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_XDIR_NBR;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_YDIR_NBR;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);

        if (ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] !=0):
            xWidth = ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[0];
            yHeight = ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[1];
            ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = xWidth / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
            ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = yHeight / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
        else:
            pass        
    
    def funcUpdateHoleBoardPar(self):
        if (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_96_STANDARD):
            ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_XDIR_NBR;
            ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_YDIR_NBR;
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_48_STANDARD):
            ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_XDIR_NBR;
            ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_YDIR_NBR;
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_24_STANDARD):
            ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = ModCebsCom.GL_CEBS_HB_TARGET_24_SD_XDIR_NBR;
            ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = ModCebsCom.GL_CEBS_HB_TARGET_24_SD_YDIR_NBR;
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_12_STANDARD):
            ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_XDIR_NBR;
            ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_YDIR_NBR;
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_6_STANDARD):
            ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = ModCebsCom.GL_CEBS_HB_TARGET_6_SD_XDIR_NBR;
            ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = ModCebsCom.GL_CEBS_HB_TARGET_6_SD_YDIR_NBR;
        else:
            ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_XDIR_NBR;
            ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_YDIR_NBR;
        ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = (ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[0]) / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
        ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = (ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[1]) / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);

    def funcCheckHoldNumber(self, holeNbr):
        if (holeNbr <= 0):
            return 1;
        if (holeNbr >= ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH):
            return ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH
        return holeNbr

    def funcCalibPilotStart(self):
        self.funcCalibLogTrace("L3CALIB: PILOT STARTING...")
        self.instL2CalibPiThd.sgL2PiStart.emit()

    def funcCalibPilotMove0(self):
        self.funcCalibLogTrace("L3CALIB: Move to Hole#0 point.")
        res, string = self.instL2MotoProc.funcMotoMove2Start()
        if (res < 0):
            self.funcCalibLogTrace("L3CALIB: Moving to start point error!")
            return -2;
        print("L3CALIB: " + string)
        return 1;
        
    def funcCalibPilotMoven(self, holeNbr):
        outputStr = "L3CALIB: Starting move to Hole#%d point." % (holeNbr)
        self.funcCalibLogTrace(outputStr)
        newHoldNbr = self.funcCheckHoldNumber(holeNbr)
        res = self.instL2MotoProc.funcMotoMove2HoleNbr(newHoldNbr)
        if (res < 0):
            outputStr = "L3CALIB: Move to Hole#%d point error!" % (newHoldNbr)
            self.funcCalibLogTrace(outputStr)
            return -1;
        else:
            outputStr = "L3CALIB: Move to Hole#%d point success!" % (newHoldNbr)
            self.funcCalibLogTrace(outputStr)
            return 1;
    
    #之前这里还同步停止摄像头的显示，其实是不需要停止的，巡游可以在不停止显示摄像头的情况下开始或者停止的
    def funcCalibPilotStop(self):
        self.funcCalibLogTrace("L3CALIB: PILOT STOP...")
        self.instL2CalibPiThd.sgL2PiStop.emit()
        
    #Using different function/api to find the right position
    #pos = self.instL4CalibForm.size()
    #pos = self.instL4CalibForm.rect()
    #geometry will return (left, top, width, height)
    def funcCalibPilotCameraEnable(self):
        #先判定摄像头状态，放置重入
        if (self.camerEnableFlag == True):
            self.funcCalibLogTrace("L3CALIB: Camera already open, can not enabled again!")
            return 1;
        self.funcCalibLogTrace("L3CALIB: Pilot camera start to open...")
        #再取得位置信息
        pos = self.instL4CalibForm.geometry()
        ModCebsCom.GL_CEBS_CAMERA_DISPLAY_POS_X = pos.x() + 420
        ModCebsCom.GL_CEBS_CAMERA_DISPLAY_POS_Y = pos.y() + 10
        #做必要的判定，放置是无效摄像头
        print("L3CALIB: Exiting STM=%d, CamId=%d" % (self.instL2CalibCamDisThd.funcCalibCameraDispStateGet(), ModCebsCom.GL_CEBS_VISION_CAMBER_NBR))
        if (ModCebsCom.GL_CEBS_VISION_CAMBER_NBR == ''):
            return -1;
        #真正启动
        self.instL2CalibCamDisThd = clsL2_CalibCamDispThread(self.instL4CalibForm, 2)
        self.instL2CalibCamDisThd.setIdentity("TASK_CalibCameraDisplay")
        self.instL2CalibCamDisThd.start();
        self.instL2CalibCamDisThd.funcCalibCameraDispStart()
        self.camerEnableFlag = True

    #FINISH all the pilot functions
    #完成校准，准备离开
    def funcCtrlCalibComp(self):
        if (self.camerEnableFlag == True):
            self.instL2CalibCamDisThd.funcCalibCameraDispStop()
            self.camerEnableFlag = False
        self.funcUpdateHoleBoardPar()
        #暂时不做过于复杂的MOTO控制，交给界面手动来进行
        #self.funcRecoverWorkingEnv()

    def funcCalibMove(self, parMoveScale, parMoveDir):
        self.instL2MotoProc.funcMotoCalaMoveOneStep(parMoveScale, parMoveDir);
        self.funcCalibLogTrace("L3CALIB: Moving one step. Current position XY=[%d/%d]." % (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]))

    def funcCalibForceMove(self, parMoveDir):
        self.instL2MotoProc.funcMotoFmCalaMoveOneStep(parMoveDir);
        self.funcCalibLogTrace("L3CALIB: Force moving one step. Current position XY=[%d/%d]." % (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]))

    '''
          左下角的坐标，存在X1/Y1上， 右上角的坐标，存在X2/Y2上 
          这种方式，符合坐标系的习惯：小值在X1/Y1中，大值在X2/Y2中
    LEFT-BOTTOM for X1/Y1 save in [0/1], RIGHT-UP for X2/Y2 save in [2/3]
    '''    

    '左下角的坐标，存在X1/Y1上'    
    def funcCalibLeftDown(self):
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0];
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1];
        self.funcUpdateHoleBoardPar()
        iniObj = ModCebsCfg.clsL1_ConfigOpr();
        iniObj.updateSectionPar();
        self.funcCalibLogTrace("L3CALIB: LeftDown Axis set! XY=%d/%d." % (ModCebsCom.GL_CEBS_HB_POS_IN_UM[0], ModCebsCom.GL_CEBS_HB_POS_IN_UM[1]))
    
    '右上角的坐标，存在X2/Y2上'
    def funcCalibRightUp(self):
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0];
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1];
        self.funcUpdateHoleBoardPar()
        iniObj = ModCebsCfg.clsL1_ConfigOpr();
        iniObj.updateSectionPar();
        self.funcCalibLogTrace("L3CALIB: RightUp Axis set!  XY=%d/%d." % (ModCebsCom.GL_CEBS_HB_POS_IN_UM[2], ModCebsCom.GL_CEBS_HB_POS_IN_UM[3]))       




'''
巡游任务模块

#Pilot thread, control moto moving and accomplish activities
#只可能被CalibForm调用，所以father传进去后，只能被它锁调用

这个任务模块典型的采用了信号槽的方式进行通信，以便被其它模块锁控制。这个方式必须在初始化的是将任务静态启动起来，
在后期的动态生产过程中不得二次启动该任务模块，这个方式有些限制的。

'''
class clsL2_CalibPilotThread(QThread):
    sgL3CalibFormPrtLog = pyqtSignal(str)
    sgL2PiStart = pyqtSignal()
    sgL2PiStop = pyqtSignal()

    def __init__(self, father, instMotoHandler):
        super(clsL2_CalibPilotThread, self).__init__()
        self.identity = None;
        self.instL4CalibForm = father
        self.instMotoHandler = instMotoHandler
        self.cntCtrl = -1;
        '''简化Class调用过程
        #self.instL2MotoProc = ModCebsMoto.clsL2_MotoProc(self.instL4CalibForm, 2);
        '''
        self.funcCalibPiLogTrace("L2CALPI: Instance start test!")

    def setIdentity(self,text):
        self.identity = text

    def funcCalibPiLogTrace(self, myString):
        self.instL4CalibForm.calib_print_log(myString)
                
    def funcCalibMotoPilotStart(self):
        self.cntCtrl = ModCebsCom.GL_CEBS_PILOT_WOKING_ROUNDS_MAX+1;

    def funcCalibMotoPilotStop(self):
        self.cntCtrl = 1;

    #OPTIMIZE PILOT WORKING METHOD
    def funcMotoCalibPilotWorkingOnces(self):
        self.instMotoHandler.funcMotoMove2HoleNbr(1);
        self.instMotoHandler.funcMotoMove2HoleNbr(ModCebsCom.GL_CEBS_HB_HOLE_X_NUM);
        self.instMotoHandler.funcMotoMove2HoleNbr(ModCebsCom.GL_CEBS_HB_TARGET_96_SD_BATCH_MAX);
        self.instMotoHandler.funcMotoMove2HoleNbr(ModCebsCom.GL_CEBS_HB_TARGET_96_SD_BATCH_MAX - ModCebsCom.GL_CEBS_HB_HOLE_X_NUM + 1);
                
    def run(self):
        while True:
            time.sleep(1)
            self.cntCtrl -= 1;
            if (self.cntCtrl > 0):
                self.sgL3CalibFormPrtLog.emit("L2CALPI: Running calibration pilot process! roundIndex = %d" % (self.cntCtrl))
                self.funcMotoCalibPilotWorkingOnces();
            #STOP
            elif (self.cntCtrl == 0): 
                self.sgL3CalibFormPrtLog.emit("L2CALPI: Stop calibration pilot!")
                self.instMotoHandler.funcMotoStop();




'''
摄像头显示任务模块

#Camera display thread, control camera video and easy calibration action
#只可能被CalibForm调用，所以father传进去后，只能被它锁调用

这个任务模块典型的采用了传统的任务启动方式，采取全动态启动与停止方式。这个方式下不建议采用信号槽，而是使用状态机来操控，更为稳健

'''
class clsL2_CalibCamDispThread(threading.Thread):      
    #STATE MACHINE
    __CEBS_STM_CDT_NULL =      0;
    __CEBS_STM_CDT_INIT =      1;
    __CEBS_STM_CDT_CAM_INIT =  2;
    __CEBS_STM_CDT_VID_SHOW =  3;
    __CEBS_STM_CDT_STOP =      4;
    __CEBS_STM_CDT_ERR =       5;
    __CEBS_STM_CDT_FIN =       6; #为了主动让任务退出的
    __CEBS_STM_CDT_INVALID =   0xFF;
    
    def __init__(self, father, startOption):
        super(clsL2_CalibCamDispThread, self).__init__()
        self.identity = None;
        self.cap = ''
        self.CDT_STM_STATE = self.__CEBS_STM_CDT_NULL;
        self.instL4CalibForm = father
        self.CDT_STM_STATE = self.__CEBS_STM_CDT_INIT;
        if (startOption == 1):
            self.CDT_STM_STATE = self.__CEBS_STM_CDT_FIN;
        self.funcCalibCamDisLogTrace("L2CALCMDI: Instance start test!")

    def setIdentity(self,text):
        self.identity = text

    def funcCalibCamDisLogTrace(self, myString):
        self.instL4CalibForm.calib_print_log(myString)

    def funcCalibCameraDispStateGet(self):
        return self.CDT_STM_STATE
    
    #启动状态必须严格检查
    def funcCalibCameraDispStart(self):
        if (self.CDT_STM_STATE == self.__CEBS_STM_CDT_INIT):
            self.CDT_STM_STATE = self.__CEBS_STM_CDT_CAM_INIT;
        else:
            self.funcCalibCamDisLogTrace("L2CALCMDI: Error STM transfer!");
    
    #任意状态均可以停止，从而任意状态都可以转移到STOP
    def funcCalibCameraDispStop(self):
        self.CDT_STM_STATE = self.__CEBS_STM_CDT_STOP;
                        
    #主任务
    def run(self):
        while True:
            #创建即退出
            if (self.CDT_STM_STATE == self.__CEBS_STM_CDT_FIN):
                return -1
            
            #等待干活
            elif (self.CDT_STM_STATE == self.__CEBS_STM_CDT_INIT):
                time.sleep(1)
            
            #初始化摄像头
            elif (self.CDT_STM_STATE == self.__CEBS_STM_CDT_CAM_INIT):
                time.sleep(0.1)
                print("L2CALCMDI: Active the camera display!")
                print("ModCebsCom.GL_CEBS_VISION_CAMBER_NBR = ", ModCebsCom.GL_CEBS_VISION_CAMBER_NBR)
                self.cap = cv.VideoCapture(ModCebsCom.GL_CEBS_VISION_CAMBER_NBR)
                self.cap.set(3, ModCebsCom.GL_CEBS_VISION_CAMBER_RES_WITDH)
                self.cap.set(4, ModCebsCom.GL_CEBS_VISION_CAMBER_RES_HEIGHT)             
                if not self.cap.isOpened():
                    self.instL1ConfigOpr.medErrorLog("L2CALCMDI: Cannot open webcam, run exit!")
                    self.CDT_STM_STATE = self.__CEBS_STM_CDT_INIT;
                    return -2;
                #Prepare to show window
                cv.namedWindow('CAMERA CAPTURED', 0)
                cv.resizeWindow('CAMERA CAPTURED', 800, 600);
                #Not yet able to embed vision into UI, so has to put at another side
                #cv.moveWindow('CAMERA CAPTURED', ModCebsCom.GL_CEBS_CAMERA_DISPLAY_POS_X, ModCebsCom.GL_CEBS_CAMERA_DISPLAY_POS_Y)
                cv.moveWindow('CAMERA CAPTURED', 0, ModCebsCom.GL_CEBS_CAMERA_DISPLAY_POS_Y)
                self.CDT_STM_STATE = self.__CEBS_STM_CDT_VID_SHOW;
            
            #输出摄像头    
            elif (self.CDT_STM_STATE == self.__CEBS_STM_CDT_VID_SHOW):    
                time.sleep(0.001)
                try:
                    ret, frame = self.cap.read()
                except Exception:
                    break;
                if (ret == True):
                    cv.imshow('CAMERA CAPTURED', frame)
                    waitKey(50)  

            #销毁现场摄像头
            elif (self.CDT_STM_STATE == self.__CEBS_STM_CDT_STOP):
                time.sleep(0.2)
                try:
                    self.cap.release()
                except Exception:
                    pass
                try:
                    cv.destroyAllWindows()
                except Exception:
                    pass                
                print("L2CALCMDI: Task finished and run exit!")
                return 1;
            
            #无效状态
            else:
                return 2;                  
                    

 
            
