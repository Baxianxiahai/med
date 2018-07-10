'''
Created on 2018骞�5鏈�17鏃�

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
        
        #鍒濆鍖栦笉鍚岀洰鏍囨澘瀛愮殑鏁伴噺
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

        #鍒濆鍖栨澘瀛斿弬鏁�
        self.funcInitHoleBoardPar();
        
        #娓呯悊鐜板満
        self.funcCleanWorkingEnv()

        #鍚姩绗笁涓共娲荤殑瀛愯繘绋�
        self.threadCalibMotoPilot = classCalibPilotThread()
        self.threadCalibMotoPilot.setIdentity("CalibPilotThread")
        self.threadCalibMotoPilot.signal_calib_print_log.connect(self.funcLogTrace) #鎺ユ敹淇″彿
        self.threadCalibMotoPilot.signal_calib_moto_pilot.connect(self.threadCalibMotoPilot.funcCalibMotoPilotSart) #鍙戦�佸惎鍔ㄤ俊鍙�
        self.threadCalibMotoPilot.signal_calib_pilot_stop.connect(self.threadCalibMotoPilot.funcCalibMotoPilotStop) #鍙戦�佸仠姝俊鍙�
        self.threadCalibMotoPilot.start();
        
    def setIdentity(self,text):
        self.identity = text

    def funcLogTrace(self, myString):
        self.calibForm.calib_print_log(myString)

    def funcCleanWorkingEnv(self):
        #灏嗛┈杈惧浣嶅埌闆剁偣
        self.objMotoProc.funcMotoStop();
        #鍋滄鍥惧儚璇嗗埆
        self.objVision.funcVisionClasEnd()

    def funcRecoverWorkingEnv(self):
        #灏嗛┈杈惧浣嶅埌闆剁偣
        self.objMotoProc.funcMotoStop();
    
    #鍒濆鍖栨澘瀛斿弬鏁�
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
        #鍐嶈�冭檻鐪熷疄鎯呭喌涓嬬殑瑕嗙洊
        #鐪熸鐨勬牎鍑嗗湪鏍″噯杩囩▼涓繘琛屾洿鏂�
        if (ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] !=0):
            xWidth = ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[0];
            yHeight = ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[3];
            ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = xWidth / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
            ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = yHeight / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
        else:
            pass        
    
    def funcUpdateHoleBoardPar(self):
        #鏇存柊绯荤粺绾у弬鏁�
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

    #鎵樼洏鍥涘懆宸℃父
    def funcCalibPilotStart(self):
        self.funcLogTrace("CALIB: 绯荤粺鏍″噯宸¤寮�濮�...")
        self.threadCalibMotoPilot.signal_calib_moto_pilot.emit()

    #宸℃父鍋滄
    def funcCalibPilotStop(self):
        self.funcLogTrace("CALIB: 绯荤粺鏍″噯宸¤鍋滄...")
        self.threadCalibMotoPilot.signal_calib_pilot_stop.emit()

    #澶勭悊鏍″噯杩囩▼瀹屾垚鐨勫姩浣�
    def funcCtrlCalibComp(self):
        self.funcUpdateHoleBoardPar()
        #鎺у埗姣旂壒浣�
        self.funcRecoverWorkingEnv()

    def funcCalibMove(self, parMoveScale, parMoveDir):
        #璋冪敤澶勭悊鍑芥暟
        obj = ModCebsMoto.classMotoProcess();
        obj.funcMotoCalaMoveOneStep(parMoveScale, parMoveDir);
        self.funcLogTrace("CALIB: Moving one step. Current position XY=[%d/%d]." % (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]))
        
    def funcCalibLeftUp(self):
        #瀛樺叆鏂板潗鏍�
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0];
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1];
        #鏇存柊绯荤粺鍙傛暟
        self.funcUpdateHoleBoardPar()
        #鏇存柊閰嶇疆鏂囦欢鍙傛暟
        iniObj = ModCebsCfg.ConfigOpr();
        iniObj.updateSectionPar();
        self.funcLogTrace("CALIB: LeftUp Axis set! XY=%d/%d." % (ModCebsCom.GL_CEBS_HB_POS_IN_UM[0], ModCebsCom.GL_CEBS_HB_POS_IN_UM[1]))

    def funcCalibRightBottom(self):
        #瀛樺叆鏂板潗鏍�
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0];
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1];
        #鏇存柊绯荤粺鍙傛暟
        self.funcUpdateHoleBoardPar()
        #鏇存柊閰嶇疆鏂囦欢鍙傛暟
        iniObj = ModCebsCfg.ConfigOpr();
        iniObj.updateSectionPar();
        self.funcLogTrace("CALIB: RightBottom Axis set!  XY=%d/%d." % (ModCebsCom.GL_CEBS_HB_POS_IN_UM[2], ModCebsCom.GL_CEBS_HB_POS_IN_UM[3]))    
    
    
    
#鏍″噯宸¤鐙珛鐨勭嚎绋�
class classCalibPilotThread(QThread):
    signal_calib_print_log = pyqtSignal(str) #鐢虫槑淇″彿
    signal_calib_moto_pilot = pyqtSignal() #鐢虫槑缁機ebsCtrl鍚姩鏈换鍔″姛鑳界殑淇″彿
    signal_calib_pilot_stop = pyqtSignal() #鐢虫槑缁機ebsCtrl鍚姩鏈换鍔″姛鑳界殑淇″彿

    def __init__(self,parent=None):
        super(classCalibPilotThread,self).__init__(parent)
        self.identity = None;
        self.cntCtrl = -1;
        self.objMotoProc = ModCebsMoto.classMotoProcess();

    def setIdentity(self,text):
        self.identity = text
        
    def funcCalibMotoPilotSart(self):
        self.cntCtrl = ModCebsCom.GL_CEBS_PILOT_WOKING_ROUNDS_MAX+1;

    #杩欐槸楂樼骇鎶�宸э紒
    def funcCalibMotoPilotStop(self):
            self.cntCtrl = 1;

    def funcMotoCalibPilotWorkingOnces(self):
        #绉诲姩鍒板乏涓�
        self.objMotoProc.funcMotoMove2HoleNbr(1);
        #绉诲姩鍒板彸涓�
        self.objMotoProc.funcMotoMove2HoleNbr(ModCebsCom.GL_CEBS_HB_HOLE_X_NUM);
        #绉诲姩鍒板乏涓�
        self.objMotoProc.funcMotoMove2HoleNbr(ModCebsCom.GL_CEBS_HB_TARGET_96_SD_BATCH_MAX - ModCebsCom.GL_CEBS_HB_HOLE_X_NUM + 1);
        #绉诲姩鍒板彸涓�
        self.objMotoProc.funcMotoMove2HoleNbr(ModCebsCom.GL_CEBS_HB_TARGET_96_SD_BATCH_MAX);
                
    def run(self):
        while True:
            time.sleep(1)
            self.cntCtrl -= 1;
            if (self.cntCtrl > 0):
                self.signal_calib_print_log.emit("CALIB: Running Calibration pilot process! roundIndex = %d" % (self.cntCtrl))
                self.funcMotoCalibPilotWorkingOnces();
            #STOP鏍囪瘑浣�
            elif (self.cntCtrl == 0): 
                self.signal_calib_print_log.emit("CALIB: Stop Calibration pilot!")
                #鍋滄椹揪
                self.objMotoProc.funcMotoStop();


    
