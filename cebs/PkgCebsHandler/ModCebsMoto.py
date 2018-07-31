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

#Local include
from cebsMain import *
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg
from PkgCebsHandler import ModCebsMotorApi

class classMotoProcess(object):
    if (ModCebsCom.GL_CEBS_MOTOAPI_INSTALLED_SET == True):
        ObjMotorApi = ModCebsMotorApi.MotorClass()
    
    def __init__(self):
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
            xWidth = ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[2];
            yHeight = ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[3];
            ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = xWidth / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
            ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = yHeight / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
        else:
            pass
        
        #打印到文件专用
        self.objInitCfg = ModCebsCfg.ConfigOpr()
        
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
        print("MOTO: Moving one step! Scale=%d, Dir=%s. Old pos X/Y=%d/%d, New pos X/Y=%d/%d" % (scale, dir, Old_Px, Old_Py, ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]));
        if (self.funcMotoMove2AxisPos(Old_Px, Old_Py, ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]) > 0):
            return 1;
        else:
            self.objInitCfg.medErrorLog("MOTO: funcMotoCalaMoveOneStep error!")
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
        print("MOTO: Moving one step! Scale=1cm, Dir=%s. Old pos X/Y=%d/%d, New pos X/Y=%d/%d" % (dir, Old_Px, Old_Py, ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]));
        if (self.funcMotoMove2AxisPos(Old_Px, Old_Py, ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]) > 0):
            return 1;
        else:
            self.objInitCfg.medErrorLog("MOTO: funcMotoFmCalaMoveOneStep error!")
            return -2;
    
    def funcMotoBackZero(self):
        return self.funcMotoMove2HoleNbr(0);
        #print("MOTO: Running Zero Position!")

    def funcMotoMove2Start(self):
        print("MOTO: Move to start position - Left/up!")
        xWidth = ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[2];
        yHeight = ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[3];
        if (xWidth <= 0 or yHeight <= 0):
            print("MOTO: Error set of calibration, xWidth/yHeight=%d/%d!" %(xWidth, yHeight))
            return -1, ("MOTO: Error set of calibration, xWidth/yHeight=%d/%d!" %(xWidth, yHeight));
        res = self.funcMotoMove2HoleNbr(1)
        print("MOTO: Feedback get from funcMotoMove2HoleNbr = ", res)
        if (res > 0):
            return res, "MOTO: Success!"
        else:
            self.objInitCfg.medErrorLog("MOTO: funcMotoMove2Start Failure!")
            return res, "MOTO: Failure!"

    #Fetch moto actual status, especially the moto is still under running
    #To be finished function!
    def funcMotoRunningStatusInquery(self):
        return False;

    def funcMotoStop(self):
        print("MOTO: funcMotoStop running...")
        if (ModCebsCom.GL_CEBS_MOTOAPI_INSTALLED_SET == True):
            res = self.ObjMotorApi.moto_proc_full_stop()
            if (res < 0):
                print("MOTO: funcMotoStop error!")
                return -1
        return 1
    
    def funcMotoResume(self):
        print("MOTO: Resume action running...")
        return 1;
    
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
            newPosX = int(ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] - (xTargetHoleNbr-1)*ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE);
            newPosY = int(ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] + (yTargetHoleNbr-1)*ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE);
        print("MOTO: Moving to working hole=%d, newPosX/Y=%d/%d." % (holeIndex, newPosX, newPosY))
        if (self.funcMotoMove2AxisPos(ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1], newPosX, newPosY) > 0):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] = newPosX;
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] = newPosY;
            print("MOTO: Finished once!")
            return 1;
        else:
            print("MOTO: Error get feedback from funcMotoMove2AxisPos.")
            self.objInitCfg.medErrorLog("MOTO: Error get feedback from funcMotoMove2AxisPos")
            return -2;

    def funcMotoMove2AxisPos(self, curPx, curPy, newPx, newPy):
        print("MOTO: funcMotoMove2AxisPos. Current XY=%d/%d, New=%d/%d" %(curPx, curPy, newPx, newPy))
        if (ModCebsCom.GL_CEBS_MOTOAPI_INSTALLED_SET == True):
            if (self.ObjMotorApi.moto_proc_move_to_axis_postion(curPx, curPy, newPx, newPy) < 0):
                print("MOTO: funcMotoMove2AxisPos run error!")
                self.objInitCfg.medErrorLog("MOTO: funcMotoMove2AxisPos get error!")
                return -1
            else:
                return 1
        else:
            return 2
    
    
    
    
    
    
        