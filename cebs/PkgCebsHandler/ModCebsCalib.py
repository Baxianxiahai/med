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
from PkgCebsHandler import ModCebsCtrl



class classCalibProcess(object):
    def __init__(self, father):
        super(classCalibProcess, self).__init__()
        self.identity = None;
        self.calibForm = father
        self.objInitCfg=ModCebsCfg.ConfigOpr();
        self.objMotoProc=ModCebsMoto.classMotoProcess();
        self.objVision=ModCebsVision.classVisionProcess();
        
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

        self.funcInitHoleBoardPar();
        self.funcCleanWorkingEnv()

        self.threadCalibMotoPilot = classCalibPilotThread()
        self.threadCalibMotoPilot.setIdentity("CalibPilotThread")
        self.threadCalibMotoPilot.signal_calib_print_log.connect(self.funcLogTrace)
        self.threadCalibMotoPilot.signal_calib_pilot_start.connect(self.threadCalibMotoPilot.funcCalibMotoPilotStart)
        self.threadCalibMotoPilot.signal_calib_pilot_stop.connect(self.threadCalibMotoPilot.funcCalibMotoPilotStop)
        self.threadCalibMotoPilot.start();
        
        #SETUP 2nd task
        self.threadCameraDisp = classCalibCameraDispThread()
        self.threadCameraDisp.setIdentity("CalibCameraDisplay")
        self.threadCameraDisp.signal_calib_print_log.connect(self.funcLogTrace)
        self.threadCameraDisp.signal_calib_camdisp_start.connect(self.threadCameraDisp.funcCalibCameraDispStart)
        self.threadCameraDisp.signal_calib_camdisp_stop.connect(self.threadCameraDisp.funcCalibCameraDispStop)
        self.threadCameraDisp.start();
        
        #Get CalibForm position
        #self.cfCameraX, self.cfCameraY = self.calibForm.geometry()
        #print("CameraX/Y = %d/%d" %(self.cfCameraX, self.cfCameraY))        
        
    def setIdentity(self,text):
        self.identity = text

    def funcLogTrace(self, myString):
        self.calibForm.calib_print_log(myString)

    def funcCleanWorkingEnv(self):
        if (self.objMotoProc.funcMotoRunningStatusInquery() == True):
            self.objMotoProc.funcMotoStop()        
        self.objVision.funcVisionClasEnd()

    def funcRecoverWorkingEnv(self):
        self.objMotoProc.funcMotoStop();
    
    def funcInitHoleBoardPar(self):
        if (ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE == 0 or ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE == 0 or ModCebsCom.GL_CEBS_HB_HOLE_X_NUM == 0 or ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM == 0):
            if (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_96_STANDARD):
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 12;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 8;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
            elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_48_STANDARD):
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 8;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 6;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
            elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_32_STANDARD):
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 8;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 4;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_32_SD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_32_SD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
            elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_12_STANDARD):
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 4;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 3;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
            else:
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 12;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 8;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_BOARD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_BOARD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);

        if (ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] !=0):
            xWidth = ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[0];
            yHeight = ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[3];
            ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = xWidth / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
            ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = yHeight / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
        else:
            pass        
    
    def funcUpdateHoleBoardPar(self):
        if (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_96_STANDARD):
            ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 12;
            ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 8;
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_48_STANDARD):
            ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 8;
            ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 6;
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_32_STANDARD):
            ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 8;
            ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 4;
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_12_STANDARD):
            ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 4;
            ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 3;
        else:
            ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 12;
            ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 8;
        ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = (ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[2]) / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
        ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = (ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[3]) / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);

    def funcCheckHoldNumber(self, holeNbr):
        if (holeNbr <= 0):
            return 1;
        if (holeNbr >= ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH):
            return ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH
        return holeNbr

    def funcCalibPilotStart(self):
        self.funcLogTrace("CALIB: PILOT STARTING...")
        self.threadCalibMotoPilot.signal_calib_pilot_start.emit()

    def funcCalibPilotMove0(self):
        self.funcLogTrace("CALIB: Move to Hole#0 point.")
        res, string = self.objMotoProc.funcMotoMove2Start()
        if (res < 0):
            self.funcLogTrace("CALIB: Moving to start point error!")
            return -2;
        print("CALIB: " + string)
        return 1;
        
    def funcCalibPilotMoven(self, holeNbr):
        outputStr = "CALIB: Starting move to Hole#%d point." % (holeNbr)
        self.funcLogTrace(outputStr)
        newHoldNbr = self.funcCheckHoldNumber(holeNbr)
        res = self.objMotoProc.funcMotoMove2HoleNbr(newHoldNbr)
        if (res < 0):
            outputStr = "CALIB: Move to Hole#%d point error!" % (newHoldNbr)
            self.funcLogTrace(outputStr)
            return -1;
        else:
            outputStr = "CALIB: Move to Hole#%d point success!" % (newHoldNbr)
            self.funcLogTrace(outputStr)
            return 1;
    
    def funcCalibPilotStop(self):
        self.funcLogTrace("CALIB: PILOT STOP...")
        self.threadCalibMotoPilot.signal_calib_pilot_stop.emit()
        self.threadCameraDisp.signal_calib_camdisp_stop.emit()

    #Using different function/api to find the right position
    #pos = self.calibForm.size()
    #pos = self.calibForm.rect()
    #geometry will return (left, top, width, height)
    def funcCalibPilotCameraEnable(self):
        self.funcLogTrace("CALIB: PILOT CEMERA ENABLE...")
        pos = self.calibForm.geometry()
        ModCebsCom.GL_CEBS_CAMERA_DISPLAY_POS_X = pos.x() + 420
        ModCebsCom.GL_CEBS_CAMERA_DISPLAY_POS_Y = pos.y() + 10
        #print(ModCebsCom.GL_CEBS_CAMERA_DISPLAY_POS_X, ModCebsCom.GL_CEBS_CAMERA_DISPLAY_POS_Y)    
        self.threadCameraDisp.signal_calib_camdisp_start.emit()

    #FINISH all the pilot functions
    def funcCtrlCalibComp(self):
        self.threadCameraDisp.signal_calib_camdisp_stop.emit()
        self.funcUpdateHoleBoardPar()
        self.funcRecoverWorkingEnv()

    def funcCalibMove(self, parMoveScale, parMoveDir):
        obj = ModCebsMoto.classMotoProcess();
        obj.funcMotoCalaMoveOneStep(parMoveScale, parMoveDir);
        self.funcLogTrace("CALIB: Moving one step. Current position XY=[%d/%d]." % (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]))

    def funcCalibForceMove(self, parMoveDir):
        obj = ModCebsMoto.classMotoProcess();
        obj.funcMotoFmCalaMoveOneStep(parMoveDir);
        self.funcLogTrace("CALIB: Force moving one step. Current position XY=[%d/%d]." % (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]))
        
    def funcCalibRightUp(self):
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0];
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1];
        self.funcUpdateHoleBoardPar()
        iniObj = ModCebsCfg.ConfigOpr();
        iniObj.updateSectionPar();
        self.funcLogTrace("CALIB: RightBottom Axis set!  XY=%d/%d." % (ModCebsCom.GL_CEBS_HB_POS_IN_UM[2], ModCebsCom.GL_CEBS_HB_POS_IN_UM[3]))       

    def funcCalibLeftDown(self):
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0];
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1];
        self.funcUpdateHoleBoardPar()
        iniObj = ModCebsCfg.ConfigOpr();
        iniObj.updateSectionPar();
        self.funcLogTrace("CALIB: LeftUp Axis set! XY=%d/%d." % (ModCebsCom.GL_CEBS_HB_POS_IN_UM[0], ModCebsCom.GL_CEBS_HB_POS_IN_UM[1]))
    
class classCalibPilotThread(QThread):
    signal_calib_print_log = pyqtSignal(str)
    signal_calib_pilot_start = pyqtSignal()
    signal_calib_pilot_stop = pyqtSignal()

    def __init__(self,parent=None):
        super(classCalibPilotThread,self).__init__(parent)
        self.identity = None;
        self.cntCtrl = -1;
        self.objMotoProc = ModCebsMoto.classMotoProcess();

    def setIdentity(self,text):
        self.identity = text
        
    def funcCalibMotoPilotStart(self):
        self.cntCtrl = ModCebsCom.GL_CEBS_PILOT_WOKING_ROUNDS_MAX+1;

    def funcCalibMotoPilotStop(self):
            self.cntCtrl = 1;

    #OPTIMIZE PILOT WORKING METHOD
    def funcMotoCalibPilotWorkingOnces(self):
        self.objMotoProc.funcMotoMove2HoleNbr(1);
        self.objMotoProc.funcMotoMove2HoleNbr(ModCebsCom.GL_CEBS_HB_HOLE_X_NUM);
        self.objMotoProc.funcMotoMove2HoleNbr(ModCebsCom.GL_CEBS_HB_TARGET_96_SD_BATCH_MAX);
        self.objMotoProc.funcMotoMove2HoleNbr(ModCebsCom.GL_CEBS_HB_TARGET_96_SD_BATCH_MAX - ModCebsCom.GL_CEBS_HB_HOLE_X_NUM + 1);
                
    def run(self):
        while True:
            time.sleep(1)
            self.cntCtrl -= 1;
            if (self.cntCtrl > 0):
                self.signal_calib_print_log.emit("CALIB: Running Calibration pilot process! roundIndex = %d" % (self.cntCtrl))
                self.funcMotoCalibPilotWorkingOnces();
            #STOP
            elif (self.cntCtrl == 0): 
                self.signal_calib_print_log.emit("CALIB: Stop Calibration pilot!")
                self.objMotoProc.funcMotoStop();


class classCalibCameraDispThread(QThread):
    signal_calib_print_log = pyqtSignal(str)
    signal_calib_camdisp_start = pyqtSignal()
    signal_calib_camdisp_stop = pyqtSignal()

    def __init__(self,parent=None):
        super(classCalibCameraDispThread,self).__init__(parent)
        self.identity = None;
        self.runFlag = False;
        self.cap = ''

    def setIdentity(self,text):
        self.identity = text
        
    def funcCalibCameraDispStart(self):
        self.runFlag = True;

    def funcCalibCameraDispStop(self):
        self.runFlag = False;
        try:
            self.cap.release()
        except Exception:
            pass
        try:
            cv.destroyAllWindows()
        except Exception:
            pass

    def run(self):
        while True:
            time.sleep(1)
            if (self.runFlag == True):
                print("Active the camera display!")
                self.cap = cv.VideoCapture(ModCebsCom.GL_CEBS_VISION_CAMBER_NBR)
                break;
        if not self.cap.isOpened():
            self.objInitCfg.medErrorLog("CALIB: Cannot open webcam!")
            return -1;
        #Prepare to show window
        cv.namedWindow('CAMERA CAPTURED', 0)
        cv.resizeWindow('CAMERA CAPTURED', 640, 480);
        cv.moveWindow('CAMERA CAPTURED', ModCebsCom.GL_CEBS_CAMERA_DISPLAY_POS_X, ModCebsCom.GL_CEBS_CAMERA_DISPLAY_POS_Y)
        while True:
            time.sleep(0.01)
            try:
                ret, frame = self.cap.read()
            except Exception:
                break;
            if (self.runFlag == True) and (ret == True):
                cv.imshow('CAMERA CAPTURED', frame)
                waitKey(100)
            else:
                break;

