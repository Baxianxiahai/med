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
        self.threadCalibMotoPilot.signal_calib_moto_pilot.connect(self.threadCalibMotoPilot.funcCalibMotoPilotSart)
        self.threadCalibMotoPilot.signal_calib_pilot_stop.connect(self.threadCalibMotoPilot.funcCalibMotoPilotStop)
        self.threadCalibMotoPilot.start();
        
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

    def funcCalibPilotStart(self):
        self.funcLogTrace("CALIB: PILOT STARTING...")
        self.threadCalibMotoPilot.signal_calib_moto_pilot.emit()

    def funcCalibPilotStop(self):
        self.funcLogTrace("CALIB: PILOT STOP...")
        self.threadCalibMotoPilot.signal_calib_pilot_stop.emit()

    def funcCtrlCalibComp(self):
        self.funcUpdateHoleBoardPar()
        self.funcRecoverWorkingEnv()

    def funcCalibMove(self, parMoveScale, parMoveDir):
        obj = ModCebsMoto.classMotoProcess();
        obj.funcMotoCalaMoveOneStep(parMoveScale, parMoveDir);
        self.funcLogTrace("CALIB: Moving one step. Current position XY=[%d/%d]." % (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]))
        
    def funcCalibLeftDown(self):
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0];
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1];
        self.funcUpdateHoleBoardPar()
        iniObj = ModCebsCfg.ConfigOpr();
        iniObj.updateSectionPar();
        self.funcLogTrace("CALIB: LeftUp Axis set! XY=%d/%d." % (ModCebsCom.GL_CEBS_HB_POS_IN_UM[0], ModCebsCom.GL_CEBS_HB_POS_IN_UM[1]))

    def funcCalibRightUp(self):
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0];
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1];
        self.funcUpdateHoleBoardPar()
        iniObj = ModCebsCfg.ConfigOpr();
        iniObj.updateSectionPar();
        self.funcLogTrace("CALIB: RightBottom Axis set!  XY=%d/%d." % (ModCebsCom.GL_CEBS_HB_POS_IN_UM[2], ModCebsCom.GL_CEBS_HB_POS_IN_UM[3]))       
    
class classCalibPilotThread(QThread):
    signal_calib_print_log = pyqtSignal(str)
    signal_calib_moto_pilot = pyqtSignal()
    signal_calib_pilot_stop = pyqtSignal()

    def __init__(self,parent=None):
        super(classCalibPilotThread,self).__init__(parent)
        self.identity = None;
        self.cntCtrl = -1;
        self.objMotoProc = ModCebsMoto.classMotoProcess();

    def setIdentity(self,text):
        self.identity = text
        
    def funcCalibMotoPilotSart(self):
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


    
