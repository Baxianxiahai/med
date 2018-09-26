'''
Created on 2018/4/29

@author: hitpony
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
import hashlib
from ctypes import *
import serial
import serial.tools.list_ports
import string

#System lib
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, qApp, QAction, QFileDialog, QTextEdit
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon

#Form class
from form_qt.cebsmainform import Ui_cebsMainWindow
from form_qt.cebscalibform import Ui_cebsCalibForm
from form_qt.cebsgparform import Ui_cebsGparForm

#Local Class
from PkgCebsHandler import ModCebsCom  #Common Support module
from PkgCebsHandler import ModCebsMoto
from PkgCebsHandler import ModCebsCtrl
from PkgCebsHandler import ModCebsVision
from PkgCebsHandler import ModCebsCfg
from PkgCebsHandler import ModCebsCalib
from PkgCebsHandler import ModCebsGpar

'''
系统设计框架
MAIN => 主入口
    |--SEUI_L4_MainWindow => 主界面
        |---SEUI_L4_CalibForm => 校准界面
        |---SEUI_L4_GparForm => 参数设置界面
            |---clsL3_CtrlSchdThread => 控制调度线程
            |---clsL3_VisCfyThread => 图像识别线程
                |---clsL2_VisCapProc => 图像抓取过程
            |---clsL3_CalibProc => 校准任务
                |---clsL2_CalibPilotThread => 校准巡游线程
                |---clsL2_CalibCamDispThread => 摄像头显示视频线程
                |---clsL2_MotoProc => 马达控制任务
                    |---clsL1_MotoDrvApi => 马达驱动接口
                    |---clsL1_GparProc => 参数填写接口
                    |---clsL1_ConfigOpr => 本地配置文件接口
                        |---clsL0_MedCFlib => 公共函数库

线程启动过程
    SEUI_L4_MainWindow
        -> clsL3_CtrlSchdThread
        -> clsL3_VisCfyThread
        -> SEUI_L4_CalibForm
            -> clsL3_CalibProc
                -> clsL2_CalibPilotThread
                -> clsL2_CalibCamDispThread
        -> SEUI_L4_GparForm

注意：信号槽，只能在线程和任务之间传递，所以普通的CLASS是不能增加信号槽的，设计机制时需要注意

'''

'''
#SEUI => System Entry UI，表示系统级的主入口
第一主入口
Main Windows
'''
class SEUI_L4_MainWindow(QtWidgets.QMainWindow, Ui_cebsMainWindow):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()

    def __init__(self):    
        super(SEUI_L4_MainWindow, self).__init__()
        #系统级别的界面初始化
        self.setupUi(self)
        #用户级别的界面初始化
        self.initUI()
        #硬件初始化
        self.initParameter()
        
    def initUI(self):
        self.statusBar().showMessage('SYSTEM START ')
        self.setGeometry(10, 30, 1024, 768)
        exitAction = QAction(QIcon('.\icon_res\q10.ico'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('EXIT SYSTEM')
        exitAction.triggered.connect(qApp.quit)
        toolbar = self.addToolBar('EXIT')  
        toolbar.addAction(exitAction)

    #MUST Load global parameters, to initialize different UI and update the stored parameters.
    def initParameter(self):
        '''
        ModCebsCom.clsL0_MedCFlib.med_cfl_test1(self)
        c = ModCebsCom.clsL0_MedCFlib.med_cfl_add(self, 1, 2)
        print("Test result = %d" % (c))
        '''
        #STEP1: 初始化配置文件
        self.instL1ConfigOpr=ModCebsCfg.clsL1_ConfigOpr()
        self.instL1ConfigOpr.readGlobalPar();
        self.instL1ConfigOpr.updateCtrlCntInfo()
        #STEP2: 启动子界面        
        self.instL4CalibForm = SEUI_L4_CalibForm()
        self.instL4GparForm = SEUI_L4_GparForm()
        #STEP3: 连接信号槽
        self.instL4CalibForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        self.instL4GparForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        self.sgL4MainWinUnvisible.connect(self.funcMainWinUnvisible);
        #STEP4: 控制调度模块初始化
        self.instL3CtrlSchdThd = ModCebsCtrl.clsL3_CtrlSchdThread(self)
        self.instL3CtrlSchdThd.setIdentity("TASK_CtrlScheduleThread")
        self.instL3CtrlSchdThd.sgL4MainWinPrtLog.connect(self.slot_print_trigger)
        self.instL3CtrlSchdThd.sgL3CtrlCapStart.connect(self.instL3CtrlSchdThd.funcTakePicStart)
        self.instL3CtrlSchdThd.sgL3CtrlCapStop.connect(self.instL3CtrlSchdThd.funcTakePicStop)
        self.instL3CtrlSchdThd.sgL3CtrlClfyStart.connect(self.instL3CtrlSchdThd.funcVisionClasStart)
        self.instL3CtrlSchdThd.sgL3CtrlClfyStop.connect(self.instL3CtrlSchdThd.funcVisionClasStop)
        self.instL3CtrlSchdThd.sgL3CtrlCalibStart.connect(self.instL3CtrlSchdThd.funcCtrlCalibStart)
        self.instL3CtrlSchdThd.sgL3CtrlCalibStop.connect(self.instL3CtrlSchdThd.funcCtrlCalibStop)
        self.instL3CtrlSchdThd.sgL3CtrlMotoZero.connect(self.instL3CtrlSchdThd.funcCtrlMotoBackZero)
        self.instL3CtrlSchdThd.start();
        #STEP5: 图像识别模块初始化
        self.instL3VisCfyThd = ModCebsVision.clsL3_VisCfyThread(self)
        self.instL3VisCfyThd.setIdentity("TASK_VisionClassifyThread")
        self.instL3VisCfyThd.sgL4MainWinPrtLog.connect(self.slot_print_trigger)
        self.instL3VisCfyThd.start();
        #STEP6: 设置马达等物理硬件状态
        self.funcMainFormSetEquInitStatus();
        #STEP7: 智能初始化摄像头#Detect all valid camera
        '''
                    方法一：搞定了，但长久初始化一个线程空间，没必要，简化模式的使用
        self.instL3VisCapProc = ModCebsVision.clsL2_VisCapProc(self, 1);
        res = self.instL3VisCapProc.funcVisionDetectAllCamera()
        '''
        res = ModCebsVision.clsL2_VisCapProc.funcVisionDetectAllCamera(self)
        self.slot_print_trigger(res)
        #STEP8: 发送归零信号给马达 #MAKE MOTO GO BACK TO ZERO
        self.instL3CtrlSchdThd.sgL3CtrlMotoZero.emit()
        
    #File Open Method, for reference
    def test_openMsg(self):  
        file, ok=QFileDialog.getOpenFileName(self,"OPEN FILE","C:/","All Files (*);;Text Files (*.txt)")  
        self.statusbar.showMessage(file)

    def med_debug_print(self, info):
        strOld = self.textEdit_runProgress.toPlainText()
        #strOut = strOld + "\n>> " + time.asctime() + " " + info;
        #self.textEdit_runProgress.setText(strOut);
        strOut = ">> " + time.asctime() + " " + info;
        self.textEdit_runProgress.append(strOut);
        self.textEdit_runProgress.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_runProgress.ensureCursorVisible()
        self.textEdit_runProgress.insertPlainText("")
    
    #
    #  槽函数部分
    #    以下部分为系统接口对应的槽函数，函数命名不得动
    #
    #
    def slot_print_trigger(self, info):
        self.med_debug_print(info)

    #Start taking picture
    def slot_ctrl_start(self):
        self.med_debug_print("L4MAIN: Taking Picture start...")
        self.instL3CtrlSchdThd.sgL3CtrlCapStart.emit()
    
    #Stop taking picture
    def slot_ctrl_stop(self):
        self.med_debug_print("L4MAIN: Taking Picture stop!")
        self.instL3CtrlSchdThd.sgL3CtrlCapStop.emit()

    #Control moto run to Zero position
    def slot_ctrl_zero(self):
        self.med_debug_print("L4MAIN: RUN TO ZERO!")
        self.instL3CtrlSchdThd.sgL3CtrlMotoZero.emit()

    #Start vision classification
    def slot_ctrl_vclas_start(self):
        self.med_debug_print("L4MAIN: Picture Classification starting...")
        self.instL3CtrlSchdThd.sgL3CtrlClfyStart.emit()

    #Stop vision classification
    def slot_ctrl_vclas_stop(self):
        self.med_debug_print("L4MAIN: Picture Classification stop.")
        self.instL3CtrlSchdThd.sgL3CtrlClfyStop.emit()

    #Enter calibration session
    def slot_ctrl_calib(self):
        if (self.instL3CtrlSchdThd.funcCtrlGetRightStatus() < 0):
            self.med_debug_print("L4MAIN: CALIB ERROR1!")
            return -1;
        self.med_debug_print("L4MAIN: CALIB ACTION!")
        self.instL3CtrlSchdThd.sgL3CtrlCalibStart.emit()
        if not self.instL4CalibForm.isVisible():
            self.sgL4MainWinUnvisible.emit()
            self.instL4CalibForm.show()

    #Enter parameter setting session
    def slot_gpar_start(self):
        self.med_debug_print("L4MAIN: PARAMETER SETTING ACTION!")
        #self.instL3CtrlSchdThd.sgL3CtrlCalibStart.emit()
        if not self.instL4GparForm.isVisible():
            self.sgL4MainWinUnvisible.emit()
            self.instL4GparForm.show()

    #Clean log window
    def slot_runpg_clear(self):
        self.textEdit_runProgress.clear();

    #Test functions
    def slot_runpg_test(self):
        res = {}
        self.med_debug_print("TEST: " + str(res))


    #
    #  槽函数部分
    #    以下部分为系统接口对应的槽函数，函数命名不得动
    #
    #
    #Control UI visible
    def funcMainWinVisible(self):
        if not self.isVisible():
            self.show()
        self.instL3CtrlSchdThd.sgL3CtrlCalibStop.emit()
        self.med_debug_print("L4MAIN: WELCOME COME BACK!")

    #Control UI un-visible
    def funcMainWinUnvisible(self):
        if self.isVisible():
            self.hide()

    #Local function
    def funcMainFormSetEquInitStatus(self):
        '''采用简化模式，省的启动那么多类的Instance
        #self.instL2MotoProc = ModCebsMoto.clsL2_MotoProc(self, 1) #第一种选择
        #if (self.instL2MotoProc.funcMotoRunningStatusInquery() == True):
        #    self.instL2MotoProc.funcMotoStop()
        '''
        if (ModCebsMoto.clsL2_MotoProc.funcMotoRunningStatusInquery(self) == True):
            ModCebsMoto.clsL2_MotoProc.funcMotoStop(self)            




#第二主入口
#Calibration Widget
class SEUI_L4_CalibForm(QtWidgets.QWidget, Ui_cebsCalibForm):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()

    def __init__(self):    
        super(SEUI_L4_CalibForm, self).__init__()  
        self.setupUi(self)
        self.instL3CalibProc = ModCebsCalib.clsL3_CalibProc(self)
        self.instL1ConfigOpr1 = ModCebsCfg.clsL1_ConfigOpr()
        
    def calib_print_log(self, info):
        strOut = ">> " + time.asctime() + " " + info;
        self.textEdit_calib_runProgress.append(strOut);
        self.textEdit_calib_runProgress.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_calib_runProgress.ensureCursorVisible()
        self.textEdit_calib_runProgress.insertPlainText("")
        
        
    #
    #  槽函数部分
    #    以下部分为系统接口对应的槽函数，函数命名不得动
    #
    #        
    def slot_calib_move(self):
        #SCALE
        radioCala10um = self.radioButton_calib_10um.isChecked();
        radioCala100um = self.radioButton_calib_100um.isChecked();
        radioCala200um = self.radioButton_calib_200um.isChecked();
        radioCala500um = self.radioButton_calib_500um.isChecked();
        radioCala1mm = self.radioButton_calib_1mm.isChecked();
        radioCala2mm = self.radioButton_calib_2mm.isChecked();
        radioCala5mm = self.radioButton_calib_5mm.isChecked();
        radioCala1cm = self.radioButton_calib_1cm.isChecked();
        radioCala2cm = self.radioButton_calib_2cm.isChecked();
        radioCala5cm = self.radioButton_calib_5cm.isChecked();
        radioCalaH96l = self.radioButton_calib_hole96_l.isChecked();
        radioCalaH96s = self.radioButton_calib_hole96_s.isChecked();
        radioCalaH48l = self.radioButton_calib_hole48_l.isChecked();
        radioCalaH48s = self.radioButton_calib_hole48_s.isChecked();
        radioCalaH24l = self.radioButton_calib_hole24_l.isChecked();
        radioCalaH24s = self.radioButton_calib_hole24_s.isChecked();
        radioCalaH12l = self.radioButton_calib_hole12_l.isChecked();
        radioCalaH12s = self.radioButton_calib_hole12_s.isChecked();
        radioCalaH6l = self.radioButton_calib_hole6_l.isChecked();
        radioCalaH6s = self.radioButton_calib_hole6_s.isChecked();
        if (radioCala10um == 1):
            parMoveScale = 1;
        elif (radioCala100um == 1):
            parMoveScale = 2;
        elif (radioCala200um == 1):
            parMoveScale = 3;
        elif (radioCala500um == 1):
            parMoveScale = 4;
        elif (radioCala1mm == 1):
            parMoveScale = 5;
        elif (radioCala2mm == 1):
            parMoveScale = 6;
        elif (radioCala5mm == 1):
            parMoveScale = 7;
        elif (radioCala1cm == 1):
            parMoveScale = 8;
        elif (radioCala2cm == 1):
            parMoveScale = 9;
        elif (radioCala5cm == 1):
            parMoveScale = 10;
        #To be completed
        elif (radioCalaH96l == 1):
            parMoveScale = 11;
        elif (radioCalaH96s == 1):
            parMoveScale = 12;
        elif (radioCalaH48l == 1):
            parMoveScale = 13;
        elif (radioCalaH48s == 1):
            parMoveScale = 14;
        elif (radioCalaH24l == 1):
            parMoveScale = 15;
        elif (radioCalaH24s == 1):
            parMoveScale = 16;
        elif (radioCalaH12l == 1):
            parMoveScale = 17;
        elif (radioCalaH12s == 1):
            parMoveScale = 18;
        elif (radioCalaH6l == 1):
            parMoveScale = 19;
        elif (radioCalaH6s == 1):
            parMoveScale = 20;
        else:
            parMoveScale = 1;
        
        #
        radioCalaUp = self.radioButton_calib_y_plus.isChecked();
        radioCalaDown = self.radioButton_calib_y_minus.isChecked();
        radioCalaLeft = self.radioButton_calib_x_minus.isChecked();
        radioCalaRight = self.radioButton_calib_x_plus.isChecked();
        if (radioCalaUp == 1):
            parMoveDir = "UP";
        elif (radioCalaDown == 1):
            parMoveDir = "DOWN";
        elif (radioCalaLeft == 1):
            parMoveDir = "LEFT";
        elif (radioCalaRight == 1):
            parMoveDir = "RIGHT";
        else:
            parMoveDir = "UP";
        self.instL3CalibProc.funcCalibMove(parMoveScale, parMoveDir);
    
    def slot_calib_right_up(self):
        self.instL3CalibProc.funcCalibRightUp();
    
    def slot_calib_left_down(self):
        self.instL3CalibProc.funcCalibLeftDown();
    
    def slot_calib_pilot_start(self):
        self.instL3CalibProc.funcCalibPilotStart();

    def slot_calib_pilot_stop(self):
        self.instL3CalibProc.funcCalibPilotStop();

    def slot_calib_pilot_move_0(self):
        self.instL3CalibProc.funcCalibPilotMove0();

    def slot_calib_pilot_move_n(self):
        try:
            boardNbr = int(self.lineEdit_pilot_move_n.text())
        except Exception: 
            boardNbr = 1;
        self.instL3CalibProc.funcCalibPilotMoven(boardNbr);

    def slot_calib_pilot_camera_enable(self):
        self.instL3CalibProc.funcCalibPilotCameraEnable();

    def slot_calib_fm_up(self):
        self.instL3CalibProc.funcCalibForceMove('UP');
    
    def slot_calib_fm_down(self):
        self.instL3CalibProc.funcCalibForceMove('DOWN');

    def slot_calib_fm_left(self):
        self.instL3CalibProc.funcCalibForceMove('LEFT');

    def slot_calib_fm_right(self):
        self.instL3CalibProc.funcCalibForceMove('RIGHT');
    
    def slot_calib_close(self):
        try:
            self.instL3CalibProc.funcCtrlCalibComp()
        except Exception:
            self.instL1ConfigOpr1.medErrorLog("L4CALIBMAIN: Execute instL3CalibProc.funcCtrlCalibComp() get error feedback.")
        self.sgL4MainWinVisible.emit()
        self.close()


    #
    #  业务函数部分
    #
    #
    def closeEvent(self, event):
        self.instL3CalibProc.funcRecoverWorkingEnv()
        self.sgL4MainWinVisible.emit()
        self.close()


#第三主入口
#Calibration Widget
class SEUI_L4_GparForm(QtWidgets.QWidget, Ui_cebsGparForm):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()

    def __init__(self):    
        super(SEUI_L4_GparForm, self).__init__()  
        self.setupUi(self)
        self.instL1GparProc = ModCebsGpar.clsL1_GparProc(self)
        self.instL1ConfigOpr2=ModCebsCfg.clsL1_ConfigOpr()
        #Update UI interface last time parameter setting
        self.funcGlobalParReadSet2Ui()
        
    #
    #  槽函数部分
    #    以下部分为系统接口对应的槽函数，函数命名不得动
    #
    #    
    def slot_gpar_compl(self):
        #self.instL1GparProc.funcCtrlCalibComp()
        self.funcGlobalParReadSave()
        self.sgL4MainWinVisible.emit()
        self.close()

    #Give up and not save parameters
    def slot_gpar_giveup(self):
        self.sgL4MainWinVisible.emit()
        self.close()

    #
    #  业务函数部分
    #
    #
    #Local function
    def funcGlobalParReadSave(self):
        ModCebsCom.GL_CEBS_PIC_CLASSIFIED_AFTER_TAKE_SET = self.checkBox_gpar_autoIdf.isChecked();
        ModCebsCom.GL_CEBS_PIC_AUTO_WORKING_AFTER_START_SET = self.checkBox_gpar_autoPic.isChecked();
        ModCebsCom.GL_CEBS_PIC_TAKING_FIX_POINT_SET = self.checkBox_gpar_picFixPos.isChecked();
        try: 
            ModCebsCom.GL_CEBS_PIC_AUTO_WORKING_TTI_IN_MIN = int(self.lineEdit_gpar_picTti.text());
        except Exception: 
            ModCebsCom.GL_CEBS_PIC_AUTO_WORKING_TTI_IN_MIN = 60;
        try: 
            ModCebsCom.GL_CEBS_VISION_SMALL_LOW_LIMIT = int(self.lineEdit_gpar_vision_small_low_limit.text());
        except Exception: 
            ModCebsCom.GL_CEBS_VISION_SMALL_LOW_LIMIT = 200;
        try: 
            ModCebsCom.GL_CEBS_VISION_SMALL_MID_LIMIT = int(self.lineEdit_gpar_vision_small_mid_limit.text());
        except Exception: 
            ModCebsCom.GL_CEBS_VISION_SMALL_MID_LIMIT = 500;
        try: 
            ModCebsCom.GL_CEBS_VISION_MID_BIG_LIMIT = int(self.lineEdit_gpar_vision_mid_big_limit.text());
        except Exception: 
            ModCebsCom.GL_CEBS_VISION_MID_BIG_LIMIT = 2000;
        try: 
            ModCebsCom.GL_CEBS_VISION_BIG_UPPER_LIMIT = int(self.lineEdit_gpar_vision_big_upper_limit.text());
        except Exception: 
            ModCebsCom.GL_CEBS_VISION_BIG_UPPER_LIMIT = 2000;
        try: 
            ModCebsCom.GL_CEBS_VISION_CAMBER_NBR = int(self.lineEdit_gpar_camera_nbr.text());
        except Exception: 
            ModCebsCom.GL_CEBS_VISION_CAMBER_NBR = 0;
        ModCebsCom.GL_CEBS_VISION_CLAS_RES_ADDUP_SET = self.checkBox_gpar_vision_res_addup.isChecked();
        ModCebsCom.GL_CEBS_VIDEO_CAPTURE_ENABLE = self.checkBox_gpar_video_enable.isChecked();
        try: 
            ModCebsCom.GL_CEBS_VIDEO_CAPTURE_DUR_IN_SEC = int(self.lineEdit_gpar_video_input.text());
        except Exception: 
            ModCebsCom.GL_CEBS_VIDEO_CAPTURE_DUR_IN_SEC = 3;
        #HB-TYPE SELECTION
        radioGparHts96 = self.radioButton_gpar_bts_96.isChecked();
        radioGparHts48 = self.radioButton_gpar_bts_48.isChecked();
        radioGparHts24 = self.radioButton_gpar_bts_24.isChecked();
        radioGparHts12 = self.radioButton_gpar_bts_12.isChecked();
        radioGparHts6 = self.radioButton_gpar_bts_6.isChecked();
        if (radioGparHts96 == 1):
            ModCebsCom.GL_CEBS_HB_TARGET_TYPE = ModCebsCom.GL_CEBS_HB_TARGET_96_STANDARD;
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_BATCH_MAX;
        elif (radioGparHts48 == 1):
            ModCebsCom.GL_CEBS_HB_TARGET_TYPE = ModCebsCom.GL_CEBS_HB_TARGET_48_STANDARD;
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_BATCH_MAX;
        elif (radioGparHts24 == 1):
            ModCebsCom.GL_CEBS_HB_TARGET_TYPE = ModCebsCom.GL_CEBS_HB_TARGET_24_STANDARD;
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_24_SD_BATCH_MAX;
        elif (radioGparHts12 == 1):
            ModCebsCom.GL_CEBS_HB_TARGET_TYPE = ModCebsCom.GL_CEBS_HB_TARGET_12_STANDARD;
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_BATCH_MAX;
        elif (radioGparHts6 == 1):
            ModCebsCom.GL_CEBS_HB_TARGET_TYPE = ModCebsCom.GL_CEBS_HB_TARGET_6_STANDARD;
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_6_SD_BATCH_MAX;
        else:
            ModCebsCom.GL_CEBS_HB_TARGET_TYPE = ModCebsCom.GL_CEBS_HB_TARGET_96_STANDARD;
            ModCebsCom.GL_CEBS_PIC_ONE_WHOLE_BATCH = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_BATCH_MAX;
        #FINAL UPDATE         
        self.instL1ConfigOpr2.updateSectionPar()

    #Using global parameter set to UI during launch
    def funcGlobalParReadSet2Ui(self):
        self.checkBox_gpar_picFixPos.setChecked(ModCebsCom.GL_CEBS_PIC_TAKING_FIX_POINT_SET)
        self.checkBox_gpar_autoIdf.setChecked(ModCebsCom.GL_CEBS_PIC_CLASSIFIED_AFTER_TAKE_SET)
        self.checkBox_gpar_autoPic.setChecked(ModCebsCom.GL_CEBS_PIC_AUTO_WORKING_AFTER_START_SET)
        self.lineEdit_gpar_picTti.setText(str(ModCebsCom.GL_CEBS_PIC_AUTO_WORKING_TTI_IN_MIN))
        self.lineEdit_gpar_vision_small_low_limit.setText(str(ModCebsCom.GL_CEBS_VISION_SMALL_LOW_LIMIT))
        self.lineEdit_gpar_vision_small_mid_limit.setText(str(ModCebsCom.GL_CEBS_VISION_SMALL_MID_LIMIT))
        self.lineEdit_gpar_vision_mid_big_limit.setText(str(ModCebsCom.GL_CEBS_VISION_MID_BIG_LIMIT))
        self.lineEdit_gpar_vision_big_upper_limit.setText(str(ModCebsCom.GL_CEBS_VISION_BIG_UPPER_LIMIT))
        self.checkBox_gpar_vision_res_addup.setChecked(ModCebsCom.GL_CEBS_VISION_CLAS_RES_ADDUP_SET)
        self.lineEdit_gpar_camera_nbr.setText(str(ModCebsCom.GL_CEBS_VISION_CAMBER_NBR))
        self.checkBox_gpar_video_enable.setChecked(ModCebsCom.GL_CEBS_VIDEO_CAPTURE_ENABLE)
        self.lineEdit_gpar_video_input.setText(str(ModCebsCom.GL_CEBS_VIDEO_CAPTURE_DUR_IN_SEC))
        if (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_96_STANDARD):
            self.radioButton_gpar_bts_96.setChecked(True)
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_48_STANDARD):
            self.radioButton_gpar_bts_48.setChecked(True)
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_24_STANDARD):
            self.radioButton_gpar_bts_24.setChecked(True)
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_12_STANDARD):
            self.radioButton_gpar_bts_12.setChecked(True)
        elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_6_STANDARD):
            self.radioButton_gpar_bts_6.setChecked(True)
        else:
            self.radioButton_gpar_bts_96.setChecked(True)

        
    #Give up and not save parameters
    def closeEvent(self, event):
        #self.instL1GparProc.funcRecoverWorkingEnv()
        self.sgL4MainWinVisible.emit()
        self.close()


#第0主入口，MAIN函数部分
#Main App entry
def main_form():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = SEUI_L4_MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

#SYSTEM ENTRY
if __name__ == '__main__':
    print("[CEBS] ", time.asctime(), ", System starting...\n" );
    main_form()
    
    
