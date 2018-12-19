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

#Local include
from cebsL4Ui import *
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg
from PkgCebsHandler import ModCebsVision
from PkgCebsHandler import ModCebsMoto


zCebsCamPicCapInHole = 0
zCebsCamPicCapAction = False

#校准处理过程
#模块只能被CalibForm调用，所以打印只会打到CalibForm上去
class clsL3_CalibProc(object):
    def __init__(self, father):
        super(clsL3_CalibProc, self).__init__()
        self.identity = None;
        self.instL4CalibForm = father
        self.camerEnableFlag = False;
        self.instL1ConfigOpr=ModCebsCfg.clsL1_ConfigOpr();
        self.instL2MotoProc=ModCebsMoto.clsL2_MotoProc(self.instL4CalibForm);
        self.initParameter();

    def initParameter(self):
        #STEP1: 判定产品型号
        ModCebsCom.GLPLT_PAR_OFC.med_init_plate_product_type()
        #STEP2：初始化工作环境
        ModCebsCom.GLPLT_PAR_OFC.med_init_plate_parameter()
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
        #STEP4:设想缺省摄像头图片
        rect = self.instL4CalibForm.label_calib_RtCam_Fill.geometry()
        filePicInit = QtGui.QPixmap('calibInitWorm.jpg').scaled(rect.width(), rect.height())
        self.instL4CalibForm.label_calib_RtCam_Fill.setPixmap(filePicInit)
        #STE5: DebugTrace
        self.funcCalibLogTrace("L3CALIB: Instance start test!")
                        
    def setIdentity(self,text):
        self.identity = text

    def funcCalibLogTrace(self, myString):
        self.instL4CalibForm.med_debug_print(myString)

    def funcActiveTrig(self):
        self.funcCalibPilotCameraEnable()

    def funcCleanWorkingEnv(self):
        if (self.instL2MotoProc.funcMotoRunningStatusInquery() == True):
            self.instL2MotoProc.funcMotoStop()        

    def funcRecoverWorkingEnv(self):
        self.instL2MotoProc.funcMotoStop();   

    def funcCheckHoldNumber(self, holeNbr):
        if (holeNbr <= 0):
            return 1;
        if (holeNbr >= ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH):
            return ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH
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

    '''     
          本函数本来是使用菜单激活的，目前可以做到固定到界面中，所以不再需要该激活过程
          但函数过程依然保留

    #Using different function/api to find the right position
    #pos = self.instL4CalibForm.size()
    #pos = self.instL4CalibForm.rect()
    #geometry will return (left, top, width, height)
    
    #再取得位置信息
    #取得位置信息，是为了做浮动式视频界面，新的视频流嵌入到UI中，故而不再需要这个功能了
    pos = self.instL4CalibForm.geometry()
    ModCebsCom.GLVIS_PAR_OFC.CAMERA_DISPLAY_POS_X = pos.x() + 420
    ModCebsCom.GLVIS_PAR_OFC.CAMERA_DISPLAY_POS_Y = pos.y() + 10
    '''
    def funcCalibPilotCameraEnable(self):
        #先判定摄像头状态，放置重入
        if (self.camerEnableFlag == True):
            self.funcCalibLogTrace("L3CALIB: Camera already open, can not enabled again!")
            return 1;
        self.funcCalibLogTrace("L3CALIB: Pilot camera start to open...")
        print("L3CALIB: CAM NBR = ", ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR)
        #做必要的判定，放置是无效摄像头，实际上，没整到位
        if (ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR < 0):
            self.funcCalibLogTrace("L3CALIB: Camera is not yet installed!") 
            return -1;
    
        #真正启动
        self.instL2CalibCamDisThd = clsL2_CalibCamDispThread(self.instL4CalibForm, 2)
        self.instL2CalibCamDisThd.setIdentity("TASK_CalibCameraDisplay")
        self.instL2CalibCamDisThd.start();
        self.instL2CalibCamDisThd.funcCalibCameraDispStart()
        self.camerEnableFlag = True
    
    '''
    NEW FUN: 捕获VIDEO中的图像
        这个是DISP中的子功能，不再需要单独获得摄像头的权限
        这个截面启动正常之后，DISP就启动了
    '''
    def funcCalibPilotCameraCapture(self, holeNbr):
        if (holeNbr <= 0 ) or (holeNbr > ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH):
            self.funcCalibLogTrace("L3CALIB: Camera capture function, holeNbr = %d not in right range!" % (holeNbr))
            return -1
        if (self.instL2CalibCamDisThd.funcCalibCameraDispChkVidCap() == False):
            self.funcCalibLogTrace("L3CALIB: Camera capture function, display task not in right state and can not make capture!")
            return -1          
        #Transfer state
        global zCebsCamPicCapInHole
        zCebsCamPicCapInHole = holeNbr;
        self.instL2CalibCamDisThd.funcCalibCameraDispSetVidCap();
            
    #FINISH all the pilot functions
    #完成校准，准备离开
    def funcCtrlCalibComp(self):
        if (self.camerEnableFlag == True):
            self.instL2CalibCamDisThd.funcCalibCameraDispStop()
            self.camerEnableFlag = False
        #准备替换为基础库函数
        ModCebsCom.GLPLT_PAR_OFC.med_update_plate_parameter()
        #如果发生了图像截取操作，需要更新批次号
        global zCebsCamPicCapAction
        if (zCebsCamPicCapAction == True):
            ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX += 1
            self.instL1ConfigOpr.updateCtrlCntInfo()

    def funcCalibMove(self, parMoveScale, parMoveDir):
        self.instL2MotoProc.funcMotoCalaMoveOneStep(parMoveScale, parMoveDir);
        self.funcCalibLogTrace("L3CALIB: Moving one step. Current position XY=[%d/%d]." % (ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0], ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1]))

    def funcCalibForceMove(self, parMoveDir):
        self.instL2MotoProc.funcMotoFmCalaMoveOneStep(parMoveDir);
        self.funcCalibLogTrace("L3CALIB: Force moving one step. Current position XY=[%d/%d]." % (ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0], ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1]))

    '''
          左下角的坐标，存在X1/Y1上， 右上角的坐标，存在X2/Y2上 
          这种方式，符合坐标系的习惯：小值在X1/Y1中，大值在X2/Y2中
    LEFT-BOTTOM for X1/Y1 save in [0/1], RIGHT-UP for X2/Y2 save in [2/3]
    '''    

    '左下角的坐标，存在X1/Y1上'    
    def funcCalibLeftDown(self):
        ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[0] = ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0];
        ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[1] = ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1];
        #准备去掉，替换为简化库函数
        #self.funcUpdateHoleBoardPar()
        ModCebsCom.GLPLT_PAR_OFC.med_update_plate_parameter()
        iniObj = ModCebsCfg.clsL1_ConfigOpr();
        iniObj.updateSectionPar();
        self.funcCalibLogTrace("L3CALIB: LeftDown Axis set! XY=%d/%d." % (ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[0], ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[1]))
    
    '右上角的坐标，存在X2/Y2上'
    def funcCalibRightUp(self):
        ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[2] = ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0];
        ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[3] = ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1];
        #准备去掉，替换为简化库函数
        #self.funcUpdateHoleBoardPar()
        ModCebsCom.GLPLT_PAR_OFC.med_update_plate_parameter()
        iniObj = ModCebsCfg.clsL1_ConfigOpr();
        iniObj.updateSectionPar();
        self.funcCalibLogTrace("L3CALIB: RightUp Axis set!  XY=%d/%d." % (ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[2], ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[3]))       

    def funcCalibGetSpsRights(self, par):
        self.instL2MotoProc.funcGetSpsRights(par);

    def funcCalibRelSpsRights(self, par):
        self.instL2MotoProc.funcRelSpsRights(par);


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
        self.instL4CalibForm.med_debug_print(myString)
                
    def funcCalibMotoPilotStart(self):
        self.cntCtrl = ModCebsCom.GL_CEBS_PILOT_WOKING_ROUNDS_MAX+1;

    def funcCalibMotoPilotStop(self):
        self.cntCtrl = 1;

    #OPTIMIZE PILOT WORKING METHOD
    def funcMotoCalibPilotWorkingOnces(self):
        self.instMotoHandler.funcMotoMove2HoleNbr(1);
        self.instMotoHandler.funcMotoMove2HoleNbr(ModCebsCom.GLPLT_PAR_OFC.HB_HOLE_X_NUM);
        self.instMotoHandler.funcMotoMove2HoleNbr(ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_96_SD_BATCH_MAX);
        self.instMotoHandler.funcMotoMove2HoleNbr(ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_96_SD_BATCH_MAX - ModCebsCom.GLPLT_PAR_OFC.HB_HOLE_X_NUM + 1);
        #LC:add run all hole test stability
#         for i in range(1,97):
#             self.instMotoHandler.funcMotoMove2HoleNbr(i)  
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
    __CEBS_STM_CDT_VID_CAP =   4;
    __CEBS_STM_CDT_STOP =      5;
    __CEBS_STM_CDT_ERR =       6;
    __CEBS_STM_CDT_FIN =       7; #为了主动让任务退出的
    __CEBS_STM_CDT_INVALID =   0xFF;
    
    def __init__(self, father, startOption):
        super(clsL2_CalibCamDispThread, self).__init__()
        self.identity = None;
        self.cap = ''
        self.CDT_STM_STATE = self.__CEBS_STM_CDT_NULL;
        self.instL4CalibForm = father
        self.CDT_STM_STATE = self.__CEBS_STM_CDT_INIT;
        self.instL1ConfigOpr = ModCebsCfg.clsL1_ConfigOpr();
        if (startOption == 1):
            self.CDT_STM_STATE = self.__CEBS_STM_CDT_FIN;
        self.camRtFillWidth = 0;
        self.camRtFillHeight = 0;
        self.funcCalibCamDisLogTrace("L2CALCMDI: Instance start test!")

    def setIdentity(self,text):
        self.identity = text

    def funcCalibCamDisLogTrace(self, myString):
        self.instL4CalibForm.med_debug_print(myString)

    def funcCalibCameraDispStateGet(self):
        return self.CDT_STM_STATE
    
    def funcCalibCameraDispChkVidCap(self):
        if (self.CDT_STM_STATE == self.__CEBS_STM_CDT_VID_SHOW):
            return True
        else:
            return False

    def funcCalibCameraDispSetVidCap(self):
        self.CDT_STM_STATE = self.__CEBS_STM_CDT_VID_CAP
    
    #启动状态必须严格检查
    def funcCalibCameraDispStart(self):
        if (self.CDT_STM_STATE == self.__CEBS_STM_CDT_INIT):
            self.CDT_STM_STATE = self.__CEBS_STM_CDT_CAM_INIT;
        else:
            self.funcCalibCamDisLogTrace("L2CALCMDI: Error STM transfer!");
    
    def funcCamDisRtInit(self):
        ModCebsCom.GLHLR_PAR_OFC.CHS_CAM_MUTEX.acquire(5)
        #确定是否安装
        if (ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR < 0):
            ModCebsCom.GLHLR_PAR_OFC.CHS_CAM_MUTEX.release()
            return -1;
        #正常打开
        self.cap = cv.VideoCapture(ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR)
        self.cap.set(3, ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_RES_WITDH)
        self.cap.set(4, ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_RES_HEIGHT)
        #设置位置
        rect = self.instL4CalibForm.label_calib_RtCam_Fill.geometry()
        self.camRtFillWidth = rect.width()
        self.camRtFillHeight = rect.height()
        
        #判定是否正常打开
        if not self.cap.isOpened():
            self.cap.release()
            cv.destroyAllWindows()
            ModCebsCom.GLHLR_PAR_OFC.CHS_CAM_MUTEX.release()
            return -2
        #之前需要独立的界面，现在不需要了
        #Prepare to show window
        #cv.namedWindow('CAMERA CAPTURED', 0)
        #cv.resizeWindow('CAMERA CAPTURED', 800, 600);
        #Not yet able to embed vision into UI, so has to put at another side
        #cv.moveWindow('CAMERA CAPTURED', 0, ModCebsCom.GLVIS_PAR_OFC.CAMERA_DISPLAY_POS_Y)
        return 1

    #任意状态均可以停止，从而任意状态都可以转移到STOP
    def funcCalibCameraDispStop(self):
        self.CDT_STM_STATE = self.__CEBS_STM_CDT_STOP;
        #组赛式释放
        while True:
            if (self.CDT_STM_STATE != self.__CEBS_STM_CDT_STOP):
                ModCebsCom.GLHLR_PAR_OFC.CHS_CAM_MUTEX.release()
                return 1;
            time.sleep(0.1)
                
    #主任务
    def run(self):
        self.capFrame = ''
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
                if (self.funcCamDisRtInit() < 0):
                    self.instL1ConfigOpr.medErrorLog("L2CALCMDI: Cannot open webcam, run exit!")
                    print("L2CALCMDI: Cannot open webcam, run exit!")
                    self.CDT_STM_STATE = self.__CEBS_STM_CDT_ERR
                    return -1;
                else:
                    self.CDT_STM_STATE = self.__CEBS_STM_CDT_VID_SHOW;
           
            #输出摄像头    
            elif (self.CDT_STM_STATE == self.__CEBS_STM_CDT_VID_SHOW):
                time.sleep(0.001)
                try:
                    ret, frame = self.cap.read()
                except Exception:
                    break;
                if (ret == True):
                    #cv.imshow('CAMERA CAPTURED', frame)
                    #height, width, bytesPerComponent = frame.shape
                    height, width = frame.shape[:2]
                    if frame.ndim == 3:
                        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                    elif frame.ndim == 2:
                        rgb = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
                    temp_image = QtGui.QImage(rgb.flatten(), width, height, QtGui.QImage.Format_RGB888)
                    temp_pixmap = QtGui.QPixmap.fromImage(temp_image)
                    self.instL4CalibForm.label_calib_RtCam_Fill.setPixmap(temp_pixmap.scaled(self.camRtFillWidth, self.camRtFillHeight))
                    self.capFrame = frame
                    waitKey(50)

            #将数据存入到文件中    
            elif (self.CDT_STM_STATE == self.__CEBS_STM_CDT_VID_CAP):
                #白平衡算法
                B,G,R = cv.split(self.capFrame)
                bMean = cv.mean(B)
                gMean = cv.mean(G)
                rMean = cv.mean(R)
                kb = (bMean[0] + gMean[0] + rMean[0])/(3*bMean[0]+0.0001)
                kg = (bMean[0] + gMean[0] + rMean[0])/(3*gMean[0]+0.0001)
                kr = (bMean[0] + gMean[0] + rMean[0])/(3*rMean[0]+0.0001)
                B = B * kb
                G = G * kg
                R = R * kr
                outputFrame = cv.merge([B, G, R])
                obj=ModCebsCfg.clsL1_ConfigOpr();
                global zCebsCamPicCapInHole
                fileName = obj.combineFileNameWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, zCebsCamPicCapInHole)
                global zCebsCamPicCapAction
                if (zCebsCamPicCapAction == False):
                    self.instL1ConfigOpr.createBatch(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX);
                self.instL1ConfigOpr.addNormalBatchFile(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, zCebsCamPicCapInHole)
                cv.imwrite(fileName, outputFrame)
                ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT += 1
                print("Remaining counter = ", ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT)
                #最终退出校准之前，需要将批次号+1
                zCebsCamPicCapAction = True #这个设置为TRUE，才表示真的干了这件事
                self.funcCalibCamDisLogTrace("L2CALCMDI: Capture and save file, batch=%d, fileNbr=%d" % (ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, zCebsCamPicCapInHole));
                #某个批次的文件存储
                self.CDT_STM_STATE = self.__CEBS_STM_CDT_VID_SHOW
            
            #销毁现场摄像头
            elif (self.CDT_STM_STATE == self.__CEBS_STM_CDT_STOP):
                try:
                    self.cap.release()
                except Exception:
                    pass
                try:
                    cv.destroyAllWindows()
                except Exception:
                    pass
                print("L2CALCMDI: Task finished and run exit!")
                self.CDT_STM_STATE = self.__CEBS_STM_CDT_INITSTOP
                return 1;
            
            #无效状态
            else:
                return 2;                  
                    

 
            
