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

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
from cebsMain import *
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg
from PkgCebsHandler import ModCebsMotorApi


'''
MOTO处理过程的L3模块

#模块可能被WinMain和Calib调用，所以初始化需要传入Father进去

'''
class clsL2_MotoProc(ModCebsCom.clsL0_MedCFlib):
    if (ModCebsCom.GL_CEBS_MOTOAPI_INSTALLED_SET == True):
        instL1MotoDrvApi = ModCebsMotorApi.clsL1_MotoDrvApi()
    
    #附带的prtFlag参数，用来表示是哪一种窗体调用的，这样MOTO过程才能得到正确的父句柄，并执行打印函数
    #prtFlag=1: WinMainForm,  prtFlag=2: CalibForm
    def __init__(self, father, prtFlag):
        super(clsL2_MotoProc, self).__init__()
        self.identity = None;
        self.instL4WinForm = father
        self.prtFlag = prtFlag
        ModCebsCom.clsL0_MedCFlib.med_init_plate_parameter(self)       
        #打印到文件专用
        self.instL1ConfigOpr = ModCebsCfg.clsL1_ConfigOpr()
        self.funcMotoLogTrace("L2MOTO: Instance start test!")

    def funcMotoLogTrace(self, myString):
        if (self.prtFlag == 1):
            self.instL4WinForm.med_debug_print(myString)
        elif (self.prtFlag == 2):
            self.instL4WinForm.calib_print_log(myString)
        else:
            pass
        
    #Normal moving with limitation    
    def funcMotoCalaMoveOneStep(self, scale, dir):
        #10um
        if (scale == 1):
            actualScale = 10;
        #100um
        elif (scale == 2):
            actualScale = 100;
        #200um
        elif (scale == 3):
            actualScale = 200;
        #500um
        elif (scale == 4):
            actualScale = 500;
        #1mm
        elif (scale == 5):
            actualScale = 1000;
        #2mm
        elif (scale == 6):
            actualScale = 2000;
        #5mm
        elif (scale == 7):
            actualScale = 5000;
        #1cm
        elif (scale == 8):
            actualScale = 10000;
        #2cm
        elif (scale == 9):
            actualScale = 20000;
        #5cm
        elif (scale == 10):
            actualScale = 50000;
        #radioCalaH96l: 99000
        elif (scale == 11):
            actualScale = (ModCebsCom.GL_CEBS_HB_TARGET_96_SD_XDIR_NBR-1) * (ModCebsCom.GL_CEBS_HB_TARGET_96_SD_HOLE_DIS)
        #radioCalaH96s: 63000
        elif (scale == 12):
            actualScale = (ModCebsCom.GL_CEBS_HB_TARGET_96_SD_YDIR_NBR-1) * (ModCebsCom.GL_CEBS_HB_TARGET_96_SD_HOLE_DIS)
        #radioCalaH48l
        elif (scale == 13):
            actualScale = (ModCebsCom.GL_CEBS_HB_TARGET_48_SD_XDIR_NBR-1) * (ModCebsCom.GL_CEBS_HB_TARGET_48_SD_HOLE_DIS)
        #radioCalaH48s
        elif (scale == 14):
            actualScale = (ModCebsCom.GL_CEBS_HB_TARGET_48_SD_YDIR_NBR-1) * (ModCebsCom.GL_CEBS_HB_TARGET_48_SD_HOLE_DIS)
        #radioCalaH24l: 19.3*5 = 96.5mm
        elif (scale == 15):
            actualScale = (ModCebsCom.GL_CEBS_HB_TARGET_24_SD_XDIR_NBR-1) * (ModCebsCom.GL_CEBS_HB_TARGET_24_SD_HOLE_DIS)
        #radioCalaH24s: 85.25 - 13.67*2 = 57.91
        elif (scale == 16):
            actualScale = (ModCebsCom.GL_CEBS_HB_TARGET_24_SD_YDIR_NBR-1) * (ModCebsCom.GL_CEBS_HB_TARGET_24_SD_HOLE_DIS)
        #radioCalaH12l
        elif (scale == 17):
            actualScale = (ModCebsCom.GL_CEBS_HB_TARGET_12_SD_XDIR_NBR-1) * (ModCebsCom.GL_CEBS_HB_TARGET_12_SD_HOLE_DIS)
        #radioCalaH12s
        elif (scale == 18):
            actualScale = (ModCebsCom.GL_CEBS_HB_TARGET_12_SD_YDIR_NBR-1) * (ModCebsCom.GL_CEBS_HB_TARGET_12_SD_HOLE_DIS)
        #radioCalaH6l: 127.5-24.5*2 = 78.4mm
        elif (scale == 19):
            actualScale = (ModCebsCom.GL_CEBS_HB_TARGET_6_SD_XDIR_NBR-1) * (ModCebsCom.GL_CEBS_HB_TARGET_6_SD_HOLE_DIS)
        #radioCalaH6s: 85.3-23.05*2 = 39.2mm
        elif (scale == 20):
            actualScale = (ModCebsCom.GL_CEBS_HB_TARGET_6_SD_YDIR_NBR-1) * (ModCebsCom.GL_CEBS_HB_TARGET_6_SD_HOLE_DIS)
        else:
            actualScale = 10;
        Old_Px = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] #X-Axis
        Old_Py = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] #Y-Axis

        #Not specify this action to each real plastic board, but addiction to mechanical platform.
        #UP DIRECTION - Y add
        if (dir == "UP"):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] += actualScale;
            if (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] > ModCebsCom.GL_CEBS_HB_MECHNICAL_PLATFORM_Y_MAX):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] = ModCebsCom.GL_CEBS_HB_MECHNICAL_PLATFORM_Y_MAX;
                
        #DOWN DIRECTION - Y sub
        elif (dir == "DOWN"):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] -= actualScale;
            if (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] < 0):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] = 0;
                
        #LEFT DIRECTION - X sub
        elif (dir == "LEFT"):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] -= actualScale;
            if (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] < 0):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] = 0;
                
        #RIGHT DIRECTION - X add
        elif (dir == "RIGHT"):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] += actualScale;
            if (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] > ModCebsCom.GL_CEBS_HB_MECHNICAL_PLATFORM_X_MAX):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] = ModCebsCom.GL_CEBS_HB_MECHNICAL_PLATFORM_X_MAX;
        
        #Error case
        else:
            pass
        print("L2MOTO: Moving one step! Scale=%d, Dir=%s. Old pos X/Y=%d/%d, New pos X/Y=%d/%d" % (scale, dir, Old_Px, Old_Py, ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]));
        if (self.funcMotoMove2AxisPos(Old_Px, Old_Py, ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]) > 0):
            return 1;
        else:
            self.instL1ConfigOpr.medErrorLog("L2MOTO: funcMotoCalaMoveOneStep error!")
            return -2;

    #Force Moving function, with scale = 1cm=10mm=10000um
    def funcMotoFmCalaMoveOneStep(self, dir):
        actualScale = 10000;
        Old_Px = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] #X-Axis
        Old_Py = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] #Y-Axis

        #Not specify this action to each real plastic board, but addiction to mechanical platform.
        #UP DIRECTION - Y add
        if (dir == "UP"):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] += actualScale;
                
        #DOWN DIRECTION - Y sub
        elif (dir == "DOWN"):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] -= actualScale;
                
        #LEFT DIRECTION - X sub
        elif (dir == "LEFT"):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] -= actualScale;
                
        #RIGHT DIRECTION - X add
        elif (dir == "RIGHT"):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] += actualScale;
        
        #Error case
        else:
            pass
        print("L2MOTO: Moving one step! Scale=1cm, Dir=%s. Old pos X/Y=%d/%d, New pos X/Y=%d/%d" % (dir, Old_Px, Old_Py, ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]));
        if (self.funcMotoMove2AxisPos(Old_Px, Old_Py, ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]) > 0):
            return 1;
        else:
            self.instL1ConfigOpr.medErrorLog("L2MOTO: funcMotoFmCalaMoveOneStep error!")
            return -2;
    
    def funcMotoBackZero(self):
        return self.funcMotoMove2HoleNbr(0);
        #print("L2MOTO: Running Zero Position!")

    def funcMotoMove2Start(self):
        print("L2MOTO: Move to start position - Left/up!")
        xWidth = ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[0];
        yHeight = ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[1];
        if (xWidth <= 0 or yHeight <= 0):
            print("L2MOTO: Error set of calibration, xWidth/yHeight=%d/%d!" %(xWidth, yHeight))
            return -1, ("L2MOTO: Error set of calibration, xWidth/yHeight=%d/%d!" %(xWidth, yHeight));
        res = self.funcMotoMove2HoleNbr(1)
        print("L2MOTO: Feedback get from funcMotoMove2HoleNbr = ", res)
        if (res > 0):
            return res, "L2MOTO: Success!"
        else:
            self.instL1ConfigOpr.medErrorLog("L2MOTO: funcMotoMove2Start Failure!")
            return res, "L2MOTO: Failure!"

    #Fetch moto actual status, especially the moto is still under running
    #To be finished function!
    def funcMotoRunningStatusInquery(self):
        return False;

    def funcMotoStop(self):
        if (ModCebsCom.GL_CEBS_MOTOAPI_INSTALLED_SET == True):
            self.instL1ConfigOpr.medCmdLog("L2MOTO: Send full stop command to moto!")
            res = self.instL1MotoDrvApi.moto_proc_full_stop()
            if (res < 0):
                print("L2MOTO: funcMotoStop() execute error!")
                return -1
        return 1
    
    def funcMotoResume(self):
        print("L2MOTO: Resume action running...")
        return 1;

    '''
          左下角的坐标，存在X1/Y1上， 右上角的坐标，存在X2/Y2上 
          这种方式，符合坐标系的习惯：小值在X1/Y1中，大值在X2/Y2中
    LEFT-BOTTOM for X1/Y1 save in [0/1], RIGHT-UP for X2/Y2 save in [2/3]
    '''    
    '这个移动算法跟显微镜的放置方式息息相关'
    def funcMotoMove2HoleNbr(self, holeIndex):
        time.sleep(1)
        if (holeIndex == 0):
            xTargetHoleNbr = 0;
            yTargetHoleNbr = 0;
            newPosX = 0;
            newPosY = 0;
        else:
            xTargetHoleNbr = ((holeIndex-1) % ModCebsCom.GL_CEBS_HB_HOLE_X_NUM) + 1;
            yTargetHoleNbr = ((holeIndex-1) // ModCebsCom.GL_CEBS_HB_HOLE_X_NUM) + 1;
            newPosX = int(ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] + (xTargetHoleNbr-1)*ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE);
            newPosY = int(ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] - (yTargetHoleNbr-1)*ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE);
        print("L2MOTO: Moving to working hole=%d, newPosX/Y=%d/%d." % (holeIndex, newPosX, newPosY))
        if (self.funcMotoMove2AxisPos(ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1], newPosX, newPosY) > 0):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] = newPosX;
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] = newPosY;
            print("L2MOTO: Finished once!")
            return 1;
        else:
            print("L2MOTO: funcMotoMove2HoleNbr() error get feedback from funcMotoMove2AxisPos.")
            self.instL1ConfigOpr.medErrorLog("L2MOTO: Error get feedback from funcMotoMove2AxisPos")
            return -2;

    def funcMotoMove2AxisPos(self, curPx, curPy, newPx, newPy):
        print("L2MOTO: funcMotoMove2AxisPos. Current XY=%d/%d, New=%d/%d" %(curPx, curPy, newPx, newPy))
        if (ModCebsCom.GL_CEBS_MOTOAPI_INSTALLED_SET == True):
            self.instL1ConfigOpr.medCmdLog(("L2MOTO: Send command to moto, with par in (um): current XY=%d/%d, New=%d/%d" %(curPx, curPy, newPx, newPy)));
            if (self.instL1MotoDrvApi.moto_proc_move_to_axis_postion(curPx, curPy, newPx, newPy) < 0):
                print("L2MOTO: funcMotoMove2AxisPos() run error!")
                self.instL1ConfigOpr.medErrorLog("L2MOTO: funcMotoMove2AxisPos get error!")
                return -1
            else:
                return 1
        else:
            return 2
    
    
    
    
    
    
        