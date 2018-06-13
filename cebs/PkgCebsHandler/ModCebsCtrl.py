'''
Created on 2018年5月2日

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

class classCtrlThread(QThread):
    signal_print_log = pyqtSignal(str) #申明信号
    signal_ctrl_start = pyqtSignal() #申明给主函数使用
    signal_ctrl_stop = pyqtSignal()  #申明给主函数使用
    signal_ctrl_zero = pyqtSignal()  #申明给主函数使用
    signal_ctrl_clas_start = pyqtSignal() #申明给主函数使用
    signal_ctrl_clas_stop = pyqtSignal()  #申明给主函数使用
    signal_ctrl_calib_start = pyqtSignal() #申明给主函数使用
    signal_ctrl_calib_stop = pyqtSignal()  #申明给主函数使用
    
    #状态机控制
    __CEBS_STM_CTRL_NULL =      0;
    __CEBS_STM_CTRL_INIT =      1;
    __CEBS_STM_CTRL_CAP_PIC =   2;
    __CEBS_STM_CTRL_CLAS =      3;
    __CEBS_STM_CTRL_CALIB =     4;
    __CEBS_STM_CTRL_ERR =       5;
    __CEBS_STM_CTRL_INVALID =   0xFF;

    def __init__(self,parent=None):
        super(classCtrlThread,self).__init__(parent)
        self.identity = None;
        self.times = -1;
        self.objInitCfg=ModCebsCfg.ConfigOpr();
        self.objMoto=ModCebsMoto.classMotoProcess();
        self.objVision=ModCebsVision.classVisionProcess();
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_NULL;
        
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

        #状态机初始化
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
        
    def setIdentity(self,text):
        self.identity = text

    def setTakePicWorkRemainNumber(self, val):
        self.times = int(val)+1
    
    def transferLogTrace(self, string):
        self.signal_print_log.emit(string)
        
    #拍照
    def funcTakePicStart(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.signal_print_log.emit("CTRL: funcTakePicStart请先完成上一个任务！")
            return -1;
        #新状态
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CAP_PIC;
        #马达起点
        if (self.objMoto.funcMotoMove2Start() < 0):
            self.signal_print_log.emit("CTRL: 马达移动错误！")
            return -2;
        self.times = ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH+1;
        self.signal_print_log.emit("CTRL: 启动拍照： 拍照次数=%d." %(self.times-1))
        self.objInitCfg.createBatch(ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX);

    #停止拍照
    #这是高级技巧！
    def funcTakePicStop(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_CAP_PIC):
            self.signal_print_log.emit("CTRL: funcTakePicStop请先完成上一个任务！")
            return -1;        
        self.times = 1
        #强行停止会造成系统死机
#         self.signal_print_log.emit("CTRL: 停止拍照，剩余次数=%d." %(self.times))
#         ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX +=1;
#         self.objInitCfg.updateCtrlCntInfo();
#         self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
        return 1;
        #马达归零：无意义的动作
#         if (self.objMoto.funcMotoBackZero() < 0):
#             self.signal_print_log.emit("系统归位错误！")
#             self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_ERR;
#             return -1;
#         else:
#             self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
#             return 1;

    #托盘归位到初始态
    def funcCtrlMotoBackZero(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.signal_print_log.emit("CTRL: funcCtrlMotoBackZero请先完成上一个任务！")
            return -1;
        self.signal_print_log.emit("CTRL: 马达位置归零...")
        if (self.objMoto.funcMotoBackZero() < 0):
            self.signal_print_log.emit("CTRL: 系统归位错误！")
            self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_ERR;
            return -1;
        else:
            self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
            return 1;
    
    #本地函数    
    def funcCameraCapture(self, capIndex):
        curOne = ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH + 1 - capIndex;
        if ((curOne > ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH) or (curOne < 1)):
            self.signal_print_log.emit("CTRL: 拍照序号错误！")
            return -1;
        self.objVision.funcVisionCapture(ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX, curOne);
        print("CTRL: Taking picture once! Current Batch=%d and Index =%d" % (ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX, curOne));
        self.objInitCfg.addBatchFile(ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX, curOne)
        #提前移动到下一个干活的位置
        nextOne = curOne + 1;
        #如果已经是最后一个位置，则归位到零位
        if ((nextOne <= ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH) and (nextOne >=1)):
            if (self.objMoto.funcMotoMove2HoleNbr(nextOne) < 0):
                self.signal_print_log.emit("CTRL: 马达移动错误！")
                return -1;
        else:
            if (self.objMoto.funcMotoBackZero() < 0):
                self.signal_print_log.emit("CTRL: 系统归位错误！")
                return -2;
    
    def funcVisionClasStart(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.signal_print_log.emit("CTRL: funcVisionClasStart请先完成上一个任务！")
            return -1;        
        self.objVision.funcVisionClasStart()
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CLAS;
    
    def funcVisionClasStop(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_CLAS):
            self.signal_print_log.emit("CTRL: funcVisionClasStop请先完成上一个任务！")
            return -1;
        self.objVision.funcVisionClasEnd()
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;

    def funcCtrlCalibStart(self):
        if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_INIT):
            self.signal_print_log.emit("CTRL: funcCtrlCalibStart请先完成上一个任务！")
            return -1;        
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_CALIB;
    
    def funcCtrlCalibStop(self):
        #print(self.CTRL_STM_STATE)
#         if (self.CTRL_STM_STATE != self.__CEBS_STM_CTRL_CALIB):
#             self.signal_print_log.emit("CTRL: funcCtrlCalibStop请先完成上一个任务！")
#             return -1;
        self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
        
    def funcCtrlGetRightStatus(self):
        if (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_INIT):
            return 1;
        else:
            return -1;
        
    def run(self):
        while True:
            time.sleep(1)
            if (self.CTRL_STM_STATE == self.__CEBS_STM_CTRL_CAP_PIC):
                self.times -= 1;
                if (self.times > 0):
                    self.signal_print_log.emit(str("CTRL: 拍照进行时：当前剩余次数=" + str(self.times)))
                    self.funcCameraCapture(self.times);
                    ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT += 1;
                    #控制停止的所作所为
                elif (self.times == 0):
                    self.signal_print_log.emit("CTRL: 停止拍照，剩余次数=%d." %(self.times))
                    ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX +=1;
                    self.objInitCfg.updateCtrlCntInfo();
                    self.CTRL_STM_STATE = self.__CEBS_STM_CTRL_INIT;
        
        
        