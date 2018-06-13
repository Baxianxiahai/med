'''
Created on 2018年5月17日

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
        
        #初始化不同目标板子的数量
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

        #初始化板孔参数
        self.funcInitHoleBoardPar();
        
        #清理现场
        self.funcCleanWorkingEnv()

        #启动第三个干活的子进程
        self.threadCalibMotoPilot = classCalibPilotThread()
        self.threadCalibMotoPilot.setIdentity("CalibPilotThread")
        self.threadCalibMotoPilot.signal_calib_print_log.connect(self.funcLogTrace) #接收信号
        self.threadCalibMotoPilot.signal_calib_moto_pilot.connect(self.threadCalibMotoPilot.funcCalibMotoPilotSart) #发送启动信号
        self.threadCalibMotoPilot.signal_calib_pilot_stop.connect(self.threadCalibMotoPilot.funcCalibMotoPilotStop) #发送停止信号
        self.threadCalibMotoPilot.start();
        
    def setIdentity(self,text):
        self.identity = text

    def funcLogTrace(self, myString):
        self.calibForm.calib_print_log(myString)

    def funcCleanWorkingEnv(self):
        #将马达复位到零点
        self.objMotoProc.funcMotoStop();
        #停止图像识别
        self.objVision.funcVisionClasEnd()

    def funcRecoverWorkingEnv(self):
        #将马达复位到零点
        self.objMotoProc.funcMotoStop();
    
    #初始化板孔参数
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
        #再考虑真实情况下的覆盖
        #真正的校准在校准过程中进行更新
        if (ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] !=0):
            xWidth = ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[0];
            yHeight = ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[3];
            ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = xWidth / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
            ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = yHeight / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
        else:
            pass        
    
    def funcUpdateHoleBoardPar(self):
        #更新系统级参数
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
        ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = (ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[0]) / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
        ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = (ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[3]) / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);

    #托盘四周巡游
    def funcCalibPilotStart(self):
        self.funcLogTrace("CALIB: 系统校准巡视开始...")
        self.threadCalibMotoPilot.signal_calib_moto_pilot.emit()

    #巡游停止
    def funcCalibPilotStop(self):
        self.funcLogTrace("CALIB: 系统校准巡视停止...")
        self.threadCalibMotoPilot.signal_calib_pilot_stop.emit()

    #处理校准过程完成的动作
    def funcCtrlCalibComp(self):
        self.funcUpdateHoleBoardPar()
        #控制比特位
        self.funcRecoverWorkingEnv();

    def funcCalibMove(self, parMoveScale, parMoveDir):
        #调用处理函数
        obj = ModCebsMoto.classMotoProcess();
        obj.funcMotoCalaMoveOneStep(parMoveScale, parMoveDir);
        self.funcLogTrace("CALIB: Moving one step. Current position XY=[%d/%d]." % (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]))
        
    def funcCalibLeftUp(self):
        #存入新坐标
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0];
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1];
        #更新系统参数
        self.funcUpdateHoleBoardPar()
        #更新配置文件参数
        iniObj = ModCebsCfg.ConfigOpr();
        iniObj.updateSectionPar();
        self.funcLogTrace("CALIB: LeftUp Axis set! XY=%d/%d." % (ModCebsCom.GL_CEBS_HB_POS_IN_UM[0], ModCebsCom.GL_CEBS_HB_POS_IN_UM[1]))

    def funcCalibRightBottom(self):
        #存入新坐标
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0];
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1];
        #更新系统参数
        self.funcUpdateHoleBoardPar()
        #更新配置文件参数
        iniObj = ModCebsCfg.ConfigOpr();
        iniObj.updateSectionPar();
        self.funcLogTrace("CALIB: RightBottom Axis set!  XY=%d/%d." % (ModCebsCom.GL_CEBS_HB_POS_IN_UM[2], ModCebsCom.GL_CEBS_HB_POS_IN_UM[3]))    
    
    
    
#校准巡视独立的线程
class classCalibPilotThread(QThread):
    signal_calib_print_log = pyqtSignal(str) #申明信号
    signal_calib_moto_pilot = pyqtSignal() #申明给CebsCtrl启动本任务功能的信号
    signal_calib_pilot_stop = pyqtSignal() #申明给CebsCtrl启动本任务功能的信号

    def __init__(self,parent=None):
        super(classCalibPilotThread,self).__init__(parent)
        self.identity = None;
        self.cntCtrl = -1;
        self.objMotoProc = ModCebsMoto.classMotoProcess();

    def setIdentity(self,text):
        self.identity = text
        
    def funcCalibMotoPilotSart(self):
        self.cntCtrl = ModCebsCom.GL_CEBS_PILOT_WOKING_ROUNDS_MAX+1;

    #这是高级技巧！
    def funcCalibMotoPilotStop(self):
            self.cntCtrl = 1;

    def funcMotoCalibPilotWorkingOnces(self):
        #移动到左上
        self.objMotoProc.funcMotoMove2HoleNbr(1);
        #移动到右上
        self.objMotoProc.funcMotoMove2HoleNbr(ModCebsCom.GL_CEBS_HB_HOLE_X_NUM);
        #移动到左下
        self.objMotoProc.funcMotoMove2HoleNbr(ModCebsCom.GL_CEBS_HB_TARGET_96_SD_BATCH_MAX - ModCebsCom.GL_CEBS_HB_HOLE_X_NUM + 1);
        #移动到右下
        self.objMotoProc.funcMotoMove2HoleNbr(ModCebsCom.GL_CEBS_HB_TARGET_96_SD_BATCH_MAX);
                
    def run(self):
        while True:
            time.sleep(1)
            self.cntCtrl -= 1;
            if (self.cntCtrl > 0):
                self.signal_calib_print_log.emit("CALIB: Running Calibration pilot process! roundIndex = %d" % (self.cntCtrl))
                self.funcMotoCalibPilotWorkingOnces();
            #STOP标识位
            elif (self.cntCtrl == 0): 
                self.signal_calib_print_log.emit("CALIB: Stop Calibration pilot!")
                #停止马达
                self.objMotoProc.funcMotoStop();


    
