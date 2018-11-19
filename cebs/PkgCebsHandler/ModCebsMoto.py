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
import serial
import serial.tools.list_ports
import struct

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
from cebsMain import *
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg
from PkgCebsHandler import ModCebsMotorApi



'''
全局变量初始化
全局变量设定，从而只干一次，不然每次随着moto模块的初始化，要搞两次，这就会出问题了
'''
L1MOTO_API_SELECTION = False  #外购API方式-True，自研驱动-False

if L1MOTO_API_SELECTION == True:
    instL1MotoDrvApiFlag = True
    try:
        instL1MotoDrvApi = ModCebsMotorApi.clsL1_MotoDrvApi()
    except Exception:
        instL1MotoDrvApiFlag = False
    print("L2MOTO: Status of Moto driver =", instL1MotoDrvApiFlag)
else:
    instL1MotoDrvApiFlag = False
    print("L2MOTO: Using self-designed board!")


'''
MOTO处理过程的L3模块

#模块可能被WinMain和Calib调用，所以初始化需要传入Father进去
'''
class clsL2_MotoProc(object):
    def __init__(self, father):
        super(clsL2_MotoProc, self).__init__()
        self.identity = None;
        self.instL4WinForm = father
        ModCebsCom.GLPLT_PAR_OFC.med_init_plate_parameter()
        self.motoSpsDrvVer = -2
        #打印到文件专用
        self.instL1ConfigOpr = ModCebsCfg.clsL1_ConfigOpr()
        #外购方式
        if L1MOTO_API_SELECTION == True:
            if (instL1MotoDrvApiFlag == True):
                self.motoSpsDrvVer = instL1MotoDrvApi.getDrvVerNbr()
            #Trigger
            self.funcMotoLogTrace("L2MOTO: Instance start test!")
            if (self.motoSpsDrvVer == -2):
                self.funcMotoLogTrace("L2MOTO: Fetch moto hardware driver ver nbr (%s), but initialize failure!" % str(self.motoSpsDrvVer))
            elif (self.motoSpsDrvVer == -1):
                self.funcMotoLogTrace("L2MOTO: Fetch moto hardware driver ver nbr (%s), but can not read success!" % str(self.motoSpsDrvVer))
            else:
                self.funcMotoLogTrace("L2MOTO: Fetch moto hardware driver ver nbr = %s" % str(self.motoSpsDrvVer))
        #第二部分：启动马达控制的具体逻辑
        #自研部分肯定启动，简化程序的设计
        self.objMdcThd = ModCebsMoto.clsL1_MdcThd(self.instL4WinForm, 2);
        self.objMdcThd.setIdentity("TASK_MotoDrvCtrlThread"+str(self.instL4WinForm))
        self.objMdcThd.sgL4MainWinPrtLog.connect(self.funcMotoLogTrace)
        self.objMdcThd.start();

    def funcMotoLogTrace(self, myString):
        self.instL4WinForm.med_debug_print(myString)
        
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
            actualScale = (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_96_SD_XDIR_NBR-1) * (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_96_SD_HOLE_DIS)
        #radioCalaH96s: 63000
        elif (scale == 12):
            actualScale = (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_96_SD_YDIR_NBR-1) * (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_96_SD_HOLE_DIS)
        #radioCalaH48l
        elif (scale == 13):
            actualScale = (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_48_SD_XDIR_NBR-1) * (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_48_SD_HOLE_DIS)
        #radioCalaH48s
        elif (scale == 14):
            actualScale = (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_48_SD_YDIR_NBR-1) * (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_48_SD_HOLE_DIS)
        #radioCalaH24l: 19.3*5 = 96.5mm
        elif (scale == 15):
            actualScale = (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_24_SD_XDIR_NBR-1) * (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_24_SD_HOLE_DIS)
        #radioCalaH24s: 85.25 - 13.67*2 = 57.91
        elif (scale == 16):
            actualScale = (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_24_SD_YDIR_NBR-1) * (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_24_SD_HOLE_DIS)
        #radioCalaH12l
        elif (scale == 17):
            actualScale = (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_12_SD_XDIR_NBR-1) * (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_12_SD_HOLE_DIS)
        #radioCalaH12s
        elif (scale == 18):
            actualScale = (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_12_SD_YDIR_NBR-1) * (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_12_SD_HOLE_DIS)
        #radioCalaH6l: 127.5-24.5*2 = 78.4mm
        elif (scale == 19):
            actualScale = (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_6_SD_XDIR_NBR-1) * (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_6_SD_HOLE_DIS)
        #radioCalaH6s: 85.3-23.05*2 = 39.2mm
        elif (scale == 20):
            actualScale = (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_6_SD_YDIR_NBR-1) * (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_6_SD_HOLE_DIS)
        else:
            actualScale = 10;
        Old_Px = ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0] #X-Axis
        Old_Py = ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1] #Y-Axis

        #Not specify this action to each real plastic board, but addiction to mechanical platform.
        #UP DIRECTION - Y add
        if (dir == "UP"):
            ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1] += actualScale;
            if (ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1] > ModCebsCom.GLPLT_PAR_OFC.HB_MECHNICAL_PLATFORM_Y_MAX):
                ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1] = ModCebsCom.GLPLT_PAR_OFC.HB_MECHNICAL_PLATFORM_Y_MAX;
                
        #DOWN DIRECTION - Y sub
        elif (dir == "DOWN"):
            ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1] -= actualScale;
            if (ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1] < 0):
                ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1] = 0;
                
        #LEFT DIRECTION - X sub
        elif (dir == "LEFT"):
            ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0] -= actualScale;
            if (ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0] < 0):
                ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0] = 0;
                
        #RIGHT DIRECTION - X add
        elif (dir == "RIGHT"):
            ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0] += actualScale;
            if (ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0] > ModCebsCom.GLPLT_PAR_OFC.HB_MECHNICAL_PLATFORM_X_MAX):
                ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0] = ModCebsCom.GLPLT_PAR_OFC.HB_MECHNICAL_PLATFORM_X_MAX;
        
        #Error case
        else:
            pass
        print("L2MOTO: Moving one step! Scale=%d, Dir=%s. Old pos X/Y=%d/%d, New pos X/Y=%d/%d" % (scale, dir, Old_Px, Old_Py, ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0], ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1]));
        if (self.funcMotoMove2AxisPos(Old_Px, Old_Py, ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0], ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1]) > 0):
            return 1;
        else:
            self.instL1ConfigOpr.medErrorLog("L2MOTO: funcMotoCalaMoveOneStep error!")
            return -2;

    #Force Moving function, with scale = 1cm=10mm=10000um
    def funcMotoFmCalaMoveOneStep(self, dir):
        actualScale = 10000;
        Old_Px = ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0] #X-Axis
        Old_Py = ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1] #Y-Axis

        #Not specify this action to each real plastic board, but addiction to mechanical platform.
        #UP DIRECTION - Y add
        if (dir == "UP"):
            ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1] += actualScale;
                
        #DOWN DIRECTION - Y sub
        elif (dir == "DOWN"):
            ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1] -= actualScale;
                
        #LEFT DIRECTION - X sub
        elif (dir == "LEFT"):
            ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0] -= actualScale;
                
        #RIGHT DIRECTION - X add
        elif (dir == "RIGHT"):
            ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0] += actualScale;
        
        #Error case
        else:
            pass
        print("L2MOTO: Moving one step! Scale=1cm, Dir=%s. Old pos X/Y=%d/%d, New pos X/Y=%d/%d" % (dir, Old_Px, Old_Py, ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0], ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1]));
        if (self.funcMotoMove2AxisPos(Old_Px, Old_Py, ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0], ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1]) > 0):
            return 1;
        else:
            self.instL1ConfigOpr.medErrorLog("L2MOTO: funcMotoFmCalaMoveOneStep error!")
            return -2;
    
    def funcMotoBackZero(self):
        print("L2MOTO: Running Zero Position!")
        #自研
        if (L1MOTO_API_SELECTION == False):
            return self.objMdcThd.funcExecMoveZero()
        #外购
        else:
            return self.funcMotoMove2HoleNbr(0);

    def funcMotoMove2Start(self):
        print("L2MOTO: Move to start position - Left/up!")
        xWidth = ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[0] - ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[2];
        yHeight = ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[1] - ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[3];
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
        self.instL1ConfigOpr.medCmdLog("L2MOTO: Send full stop command to moto!")
        #自研部分
        if (L1MOTO_API_SELECTION == False):
            return self.objMdcThd.funcExecStopNormal()
        #外部采购
        else:
            if (instL1MotoDrvApiFlag == True):
                res = instL1MotoDrvApi.moto_proc_full_stop()
                if (res < 0):
                    print("L2MOTO: funcMotoStop() execute error!")
                    return -1
            return -2
    
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
            xTargetHoleNbr = ((holeIndex-1) % ModCebsCom.GLPLT_PAR_OFC.HB_HOLE_X_NUM) + 1;
            yTargetHoleNbr = ((holeIndex-1) // ModCebsCom.GLPLT_PAR_OFC.HB_HOLE_X_NUM) + 1;
            newPosX = int(ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[0] + (xTargetHoleNbr-1)*ModCebsCom.GLPLT_PAR_OFC.HB_WIDTH_X_SCALE);
            newPosY = int(ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[3] - (yTargetHoleNbr-1)*ModCebsCom.GLPLT_PAR_OFC.HB_HEIGHT_Y_SCALE);
        print("L2MOTO: Moving to working hole=%d, newPosX/Y=%d/%d." % (holeIndex, newPosX, newPosY))
        if (self.funcMotoMove2AxisPos(ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0], ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1], newPosX, newPosY) > 0):
            ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0] = newPosX;
            ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1] = newPosY;
            print("L2MOTO: Finished once!")
            return 1;
        else:
            print("L2MOTO: funcMotoMove2HoleNbr() error get feedback from funcMotoMove2AxisPos.")
            self.instL1ConfigOpr.medErrorLog("L2MOTO: Error get feedback from funcMotoMove2AxisPos")
            return -2;

    def funcMotoMove2AxisPos(self, curPx, curPy, newPx, newPy):
        print("L2MOTO: funcMotoMove2AxisPos. Current XY=%d/%d, New=%d/%d" %(curPx, curPy, newPx, newPy))
        #自研部分
        if (L1MOTO_API_SELECTION == False):
            self.objMdcThd.funcExecMoveDistance((newPx-curPx)*ModCebsCom.GLSPS_PAR_OFC.MOTOR_STEPS_PER_DISTANCE_UM, (newPy-curPy)**ModCebsCom.GLSPS_PAR_OFC.MOTOR_STEPS_PER_DISTANCE_UM);
            return 1
        #外购部分
        else:
            if (instL1MotoDrvApiFlag == True):
                self.instL1ConfigOpr.medCmdLog(("L2MOTO: Send command to moto, with par in (um): current XY=%d/%d, New=%d/%d" %(curPx, curPy, newPx, newPy)));
                if (instL1MotoDrvApi.moto_proc_move_to_axis_postion(curPx, curPy, newPx, newPy) < 0):
                    print("L2MOTO: funcMotoMove2AxisPos() run error!")
                    self.instL1ConfigOpr.medErrorLog("L2MOTO: funcMotoMove2AxisPos get error!")
                    return -1
                else:
                    return 1
            else:
                return 2
    
    def funcGetSpsRights(self, par):
        self.objMdcThd.funcGetSpsRights(par);

    def funcRelSpsRights(self, par):
        self.objMdcThd.funcRelSpsRights(par);    
    
    
    
    
'''

自研马达控制器的驱动API函数
考虑到马达的外部控制命令必须使用状态机和异步式，所以这里采用状态机来操控
接口支持MODBUS协议，自定义格式，未来可以考虑扩充支持其它格式

'''        
class clsL1_MdcThd(QThread):
    sgL4MainWinPrtLog = pyqtSignal(str) #DECLAR SIGNAL
    
    #STATE MACHINE
    __CEBS_STM_MDCT_NULL =      0
    __CEBS_STM_MDCT_INIT =      1
    __CEBS_STM_MDCT_SPS_RGT =   2
    __CEBS_STM_MDCT_CMD_SND =   3   #单控发送指令
    __CEBS_STM_MDCT_CMD_EXEC =  4   #批量指令模式
    __CEBS_STM_MDCT_CMD_EXE_ZO =  5
    __CEBS_STM_MDCT_CMD_EXE_MV =  6
    __CEBS_STM_MDCT_CMD_CMPL =  7
    __CEBS_STM_MDCT_REL_RGT =   8
    __CEBS_STM_MDCT_INVALID =   0xFF;
    MDCT_STM_STATE = 0;

    #CONTROL MDCT USAGE
    __CEBS_MDCT_SPS_USAGE_MAIN_CTRL =   1;
    __CEBS_MDCT_SPS_USAGE_CALIB_UI =    2;
    __CEBS_MDCT_SPS_USAGE_MENG_UI =     3;
    MDCT_SPS_USAGE = 0;
    
    #CONTROL EXEC WORK STATE
    MDCT_CTRL_CNT = 0;
    
    #Kernal control parameter of serial port usage
    IsSerialOpenOk = False
    serialFd = serial.Serial()
    targetComPortString = ''

    def __init__(self, father, flag):
        super(clsL1_MdcThd, self).__init__()
        self.identity = None;
        self.capTimes = -1;
        self.instL4WinMainForm = father
        self.triggerFlag = flag
        self.instL1ConfigOpr=ModCebsCfg.clsL1_ConfigOpr();
        self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_INIT;
        
        #INIT STM
        self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_INIT;
        self.funcMdctdDebugPrint("L1MDCT: Instance start!")
    
    '''
          基础函数部分
    '''        
    def setIdentity(self,text):
        self.identity = text

    def funcCtrlStateGet(self):
        return self.MDCT_STM_STATE
    
    def funcMdctdDebugPrint(self, string):
        if self.triggerFlag == 1:
            self.sgL4MainWinPrtLog.emit(string)
        if self.triggerFlag == 2:
            self.sgL4MainWinPrtLog.emit(string)

    '''
    1: MAIN UI and CTRL SCHEDULE task called
    2: CALIB UI called
    3: MENG engineering UI called
    '''
    def funcGetSpsRights(self, par):
        self.MDCT_SPS_USAGE = par
#         cnt = 0;
#         while (cnt < 10) and (self.MDCT_SPS_USAGE != 0):
#             cnt += 1
#             time.sleep(0.1)
#             print("self.MDCT_SPS_USAGE = ", self.MDCT_SPS_USAGE)
        self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_SPS_RGT;
        self.funcMdctdDebugPrint("L1MDCT: Initialize SPS port, called father = %d" % (self.MDCT_SPS_USAGE))

    def funcRelSpsRights(self, par):
        if (self.MDCT_SPS_USAGE != par):
            self.funcMdctdDebugPrint("L1MDCT: Not same father called release procedure!")
        self.MDCT_SPS_USAGE = 0;
        self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_REL_RGT;

    def funcResetWkStatus(self):
        self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_INIT;    
    
    #计算CRC
    def funcCacCrc(self, buf, length):
        wCRC = 0xFFFF;
        index=0
        while index < length:
            wCRCOut = self.funcCrcOneChar(buf[index], wCRC)
            wCRC = wCRCOut
            index += 1
        wHi = wCRC // 256;
        wLo = wCRC % 256;
        wCRC = (wHi << 8) | wLo;
        return wCRC;

    #计算CRC支持功能
    def funcCrcOneChar(self, cDataIn, wCRCIn):
        wCheck = 0;
        wCRCIn = wCRCIn ^ cDataIn;
        i=0;
        while i<8:
            wCheck = wCRCIn & 1;
            wCRCIn = wCRCIn >> 1;
            wCRCIn = wCRCIn & 0x7fff;
            if (wCheck == 1):
                wCRCIn = wCRCIn ^ 0xa001;
            wCRCIn = wCRCIn & 0xffff;
            i += 1
        return wCRCIn;

    #初始化串口
    def funcInitSps(self):
        self.IsSerialOpenOk = False
        plist = list(serial.tools.list_ports.comports())
        self.targetComPortString = 'Prolific USB-to-Serial Comm Port ('
        self.drvVerNbr = -1
        if len(plist) <= 0:
            self.instL1ConfigOpr.medErrorLog("L1MDCT: Not serial device installed!")
            self.funcMdctdDebugPrint("L1MDCT: Not serial device installed!")
        else:
            maxList = len(plist)
            searchComPartString = ''
            for index in range(0, maxList):
                self.instL1ConfigOpr.medErrorLog("L1MDCT: " + str(plist[index]))
                plistIndex =list(plist[index])
                print(plistIndex)
                #Find right COM#
                for comPortStr in plistIndex:
                    indexStart = comPortStr.find(self.targetComPortString)
                    indexEnd = comPortStr.find(')')
                    if (indexStart >= 0) and (indexEnd >=0) and (indexEnd > len(self.targetComPortString)):
                        searchComPartString = comPortStr[len(self.targetComPortString):indexEnd]
            if searchComPartString == '':
                self.funcMdctdDebugPrint("L1MDCT: Can not find right serial port!")
                self.instL1ConfigOpr.medErrorLog("L1MDCT: Can not find right serial port!")
                return -1
            else:
                print("L1MDCT: Serial port is to open = ", searchComPartString)
                self.funcMdctdDebugPrint("L1MDCT: Serial port is to open = " + str(searchComPartString))
                serialName = searchComPartString
            try:
                self.serialFd = serial.Serial(serialName, 9600, timeout = 0.2)
            except Exception:
                self.IsSerialOpenOk = False
                self.funcMdctdDebugPrint("L1MDCT: Serial exist, but can't open!")
                return -1
            self.IsSerialOpenOk = True
            self.funcMdctdDebugPrint("L1MDCT: Success open serial port!")
            return 1
    
    #用于支持单个任务模式
    def funcSendMengCmd(self, cmdId, par1, par2, par3, par4):
        if (self.MDCT_STM_STATE != self.__CEBS_STM_MDCT_CMD_SND):
            self.funcMdctdDebugPrint("L1MDCT: Not in SND state and can not continue support this command!")
            return -1,0
        return self.funcSendCmdPack(cmdId, par1, par2, par3, par4)
    
    #命令打包
    def funcSendCmdPack(self, cmdId, par1, par2, par3, par4):
        #Build MODBUS COMMAND:系列化
        fmt = ">BBiiii";
        byteDataBuf = struct.pack(fmt, ModCebsCom.GLSPS_PAR_OFC.SPS_MENGPAR_ADDR, cmdId, par1, par2, par3, par4)
        crc = self.funcCacCrc(byteDataBuf, ModCebsCom.GLSPS_PAR_OFC.SPS_MENGPAR_CMD_LEN)
        fmt = "<H";
        byteCrc = struct.pack(fmt, crc)
        byteDataBuf += byteCrc
        #打印完整的BYTE系列
        index=0
        outBuf=''
        while index < (ModCebsCom.GLSPS_PAR_OFC.SPS_MENGPAR_CMD_LEN+2):
            outBuf += str("%02X " % (byteDataBuf[index]))
            index+=1
        self.funcMdctdDebugPrint("L1MDCT: SND CMD = " + outBuf)
        res, Buf = self.funcCmdSend(byteDataBuf)
        if (res > 0):
            return Buf
        else:
            return res

    #单条命令的执行
    def funcCmdSend(self, cmd):
        #正常状态
        if(self.IsSerialOpenOk == False):
            self.funcMdctdDebugPrint("L1MDCT: Serial not opened, cant not send command!")
            return -2,0
        #串口的确已经被打开了
        self.serialFd.readline()
        self.serialFd.write(cmd)
        rcvBuf = self.serialFd.readline()
        if (len(rcvBuf) > 1):
            while (rcvBuf[len(rcvBuf)-1] == 0x0A):
                rcvBuf2 = self.serialFd.readline()
                rcvBuf += rcvBuf2
        length = len(rcvBuf)
        if (length <=0):
            self.funcMdctdDebugPrint("L1MDCT: Nothing received. RCV BUF = " + str(rcvBuf))
            return -3,0
        outBuf = ''
        for i in range(length):
            outBuf += ("%02X "%(rcvBuf[i]))
        self.funcMdctdDebugPrint("L1MDCT: RCV BUF = " + outBuf)
        #Check CRC
        targetCrc = rcvBuf[length-2] + (rcvBuf[length-1]<<8)
        rcvCrc = self.funcCacCrc(rcvBuf, length-2)
        if (rcvCrc != targetCrc):
            self.funcMdctdDebugPrint("L1MDCT: Receive CRC Error!")
            return -4,0
        if (rcvBuf[0] != cmd[0]):
            self.funcMdctdDebugPrint("L1MDCT: Receive EquId Error!")
            return -5,0
        fmt = ">i";
        upBuf = rcvBuf[3:7]
        outPar = struct.unpack(fmt, upBuf)
        return 1, outPar[0]
    
    #批量处理时的初始化
    def funcBatInitPar(self):
        if (self.MDCT_STM_STATE != self.__CEBS_STM_MDCT_CMD_EXEC):
            self.funcMdctdDebugPrint("L1MDCT: Not in EXEC state and can not continue support this command!")
            return -1,0
        #设置一圈步伐
        self.funcSendCmdPack(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_PPC_CMID, ModCebsCom.GLSPS_PAR_OFC.MOTOR_STEPS_PER_ROUND, 0, 0, 0)
        #设置激活
        self.funcSendCmdPack(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_WK_MODE_CMID, 1, 1, 0, 0)
        #设置速度
        self.funcSendCmdPack(ModCebsCom.GLSPS_PAR_OFC.SPS_MV_SPD_CMID, ModCebsCom.GLSPS_PAR_OFC.MOTOR_MAX_SPD, ModCebsCom.GLSPS_PAR_OFC.MOTOR_MAX_SPD, 0, 0)
        #设置加速度
        self.funcSendCmdPack(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_ACC_CMID, ModCebsCom.GLSPS_PAR_OFC.MOTOR_MAX_ACC, ModCebsCom.GLSPS_PAR_OFC.MOTOR_MAX_ACC, 0, 0)
        #设置加速度
        self.funcSendCmdPack(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_DEACC_CMID, ModCebsCom.GLSPS_PAR_OFC.MOTOR_MAX_DEACC, ModCebsCom.GLSPS_PAR_OFC.MOTOR_MAX_DEACC, 0, 0)
        #设置归零速度
        self.funcSendCmdPack(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_ZO_SPD_CMID, ModCebsCom.GLSPS_PAR_OFC.MOTOR_ZERO_SPD, ModCebsCom.GLSPS_PAR_OFC.MOTOR_ZERO_SPD, 0, 0)
        #设置归零加速度
        self.funcSendCmdPack(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_ZO_ACC_CMID, ModCebsCom.GLSPS_PAR_OFC.MOTOR_ZERO_ACC, ModCebsCom.GLSPS_PAR_OFC.MOTOR_ZERO_ACC, 0, 0)
        #全部停止
        self.funcSendCmdPack(ModCebsCom.GLSPS_PAR_OFC.SPS_STP_IMD_CMID, 1, 1, 0, 0)
    
    #连续带监控的命令执行
    def funcExecMoveZero(self):
        if (self.MDCT_STM_STATE != self.__CEBS_STM_MDCT_CMD_EXEC):
            self.funcMdctdDebugPrint("L1MDCT: Exec move zero, not in EXEC state and can not continue support this command!")
            return -1
        self.MDCT_CTRL_CNT = 30
        self.funcSendCmdPack(ModCebsCom.GLSPS_PAR_OFC.SPS_MV_ZERO_CMID, 1, 1, 0, 0)
        self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_CMD_EXE_ZO
        return 1

    def funcExecStopNormal(self):
        if (self.MDCT_STM_STATE != self.__CEBS_STM_MDCT_CMD_EXEC):
            self.funcMdctdDebugPrint("L1MDCT: Exec stop normal, not in EXEC state and can not continue support this command!")
            return -1
        self.funcSendCmdPack(ModCebsCom.GLSPS_PAR_OFC.SPS_STP_NOR_CMID, 1, 1, 0, 0)
        return 1

    #连续带监控的命令执行：速度模式
    def funcExecMoveSpeed(self, par1, par2):
        if (self.MDCT_STM_STATE != self.__CEBS_STM_MDCT_CMD_EXEC):
            self.funcMdctdDebugPrint("L1MDCT: Exec move speed, not in EXEC state and can not continue support this command!")
            return -1
        #定标10
        input1 = int(par1 * 10)
        input2 = int(par2 * 10)
        self.MDCT_CTRL_CNT = 30
        self.funcSendCmdPack(ModCebsCom.GLSPS_PAR_OFC.SPS_MV_SPD_CMID, input1, input2, 0, 0)
        self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_CMD_EXE_MV
        return 1

    #连续带监控的命令执行：距离模式
    def funcExecMoveDistance(self, par1, par2):
        if (self.MDCT_STM_STATE != self.__CEBS_STM_MDCT_CMD_EXEC):
            self.funcMdctdDebugPrint("L1MDCT: Exec move distance, not in EXEC state and can not continue support this command!")
            return -1
        #定标NF0
        input1 = int(par1)
        input2 = int(par2)
        self.MDCT_CTRL_CNT = 30
        self.funcSendCmdPack(ModCebsCom.GLSPS_PAR_OFC.SPS_MV_PULS_CMID, input1, input2, 0, 0)
        self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_CMD_EXE_MV
        return 1
    
    #标准指令
    def funcInqueryRunningStatus(self):
        res = self.funcSendCmdPack(ModCebsCom.GLSPS_PAR_OFC.SPS_INQ_RUN_CMID, 1, 1, 1, 1)
        print("Res = ", res)
        if res == 0:
            return True
        else:
            return False




    
    '''
          任务主程序
    '''                        
    def run(self):
        while True:
            
            #初始化等待
            if (self.MDCT_STM_STATE == self.__CEBS_STM_MDCT_INIT):
                #self.funcMdctdDebugPrint("L1MDCT: I am alive! State = %d" % (self.MDCT_STM_STATE))
                time.sleep(1)

            elif (self.MDCT_STM_STATE == self.__CEBS_STM_MDCT_SPS_RGT):
                self.funcMdctdDebugPrint("L1MDCT: Get communication rights and start init port!")
                localCnt = 0
                flag = -1
                while (localCnt < 10) and (flag < 0):
                    flag = self.funcInitSps()
                    localCnt += 1
                    time.sleep(0.2)
                    print("L1MDCT: Fetch SPS port try times = ", localCnt)
                if (flag > 0):
                    self.funcMdctdDebugPrint("L1MDCT: Init sps port successful!")
                    if (self.MDCT_SPS_USAGE == self.__CEBS_MDCT_SPS_USAGE_MENG_UI):
                        self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_CMD_SND
                    else:
                        self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_CMD_EXEC
                        self.funcBatInitPar()
                else:
                    self.funcMdctdDebugPrint("L1MDCT: Init sps port failured!")
                    self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_INIT
            
            #MENG working state
            elif (self.MDCT_STM_STATE == self.__CEBS_STM_MDCT_CMD_SND):
                #self.funcMdctdDebugPrint("L1MDCT: I am in SND state, waiting for command coming!")
                time.sleep(1)
            
            #Moto working state
            elif (self.MDCT_STM_STATE == self.__CEBS_STM_MDCT_CMD_EXEC):
                self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_CMD_CMPL
                #self.funcMdctdDebugPrint("L1MDCT: I am in EXEC state!")
                time.sleep(1)

            #Batch working mode, ZERO moving
            elif (self.MDCT_STM_STATE == self.__CEBS_STM_MDCT_CMD_EXE_ZO):
                self.MDCT_CTRL_CNT -= 1
                if (self.MDCT_CTRL_CNT >0):
                    if (self.funcInqueryRunningStatus() == False):
                        self.funcMdctdDebugPrint("L1MDCT: Waiting for ZERO task complete, counter = %d!" % (self.MDCT_CTRL_CNT))
                        time.sleep(1)
                    else:
                        self.MDCT_CTRL_CNT = 0
                        self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_CMD_EXEC
                        self.funcMdctdDebugPrint("L1MDCT: Task complete!")
                else:
                    self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_CMD_EXEC
                    self.funcMdctdDebugPrint("L1MDCT: Time out reached, go back to EXEC state!")

            #Batch working mode, Normal moving
            elif (self.MDCT_STM_STATE == self.__CEBS_STM_MDCT_CMD_EXE_MV):
                self.MDCT_CTRL_CNT -= 1
                if (self.MDCT_CTRL_CNT >0):
                    if (self.funcInqueryRunningStatus() == False):
                        self.funcMdctdDebugPrint("L1MDCT: Waiting for move task complete, counter = %d!" % (self.MDCT_CTRL_CNT))
                        time.sleep(1)
                    else:
                        self.MDCT_CTRL_CNT = 0
                        self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_CMD_EXEC
                        self.funcMdctdDebugPrint("L1MDCT: Move task complete!")
                else:
                    self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_CMD_EXEC
                    self.funcMdctdDebugPrint("L1MDCT: Time out reached, go back to EXEC state!")

            #暂时未用的状态：可能用来被其它之用
            elif (self.MDCT_STM_STATE == self.__CEBS_STM_MDCT_CMD_CMPL):
                self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_CMD_EXEC
                #self.funcMdctdDebugPrint("L1MDCT: I am in CMPL state, now go back to EXEC state!")

            elif (self.MDCT_STM_STATE == self.__CEBS_STM_MDCT_REL_RGT):
                self.IsSerialOpenOk = False
                self.serialFd.close()
                self.MDCT_STM_STATE = self.__CEBS_STM_MDCT_INIT
                self.funcMdctdDebugPrint("L1MDCT: Release Resource!")
                #time.sleep(1)

            else:
                self.funcMdctdDebugPrint("L1MDCT: Error state!")


        