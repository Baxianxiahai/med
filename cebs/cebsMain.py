'''
Created on 2018/4/29

@author: hitpony
'''

####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-

'''
SYSTEM DESIGN FRAMEWORK, 系统设计框架
MAIN => 主入口
    |--SEUI_L4_MainWindow => 主界面
        |---clsL3_CtrlSchdThread => 控制调度线程
            |---clsL2_VisCapProc => 图像抓取过程 
            |---clsL2_VisCfyProc => 图像识别线程
            |---clsL2_MotoProc => 马达控制任务
                |---clsL1_MotoDrvApi => 马达驱动接口
    |---SEUI_L4_CalibForm => 校准界面
        |---clsL3_CalibProc => 校准任务
            |---clsL2_CalibPilotThread => 校准巡游线程
            |---clsL2_CalibCamDispThread => 摄像头显示视频线程
            |---clsL2_MotoProc => 马达控制任务
                |---clsL1_MotoDrvApi => 马达驱动接口
    |---SEUI_L4_GparForm => 参数设置界面
        |---clsL3_GparProc => 参数填写接口
    |---CommonLib
        |---clsL1_ConfigOpr => 本地配置文件接口
            |---clsL0_MedCfgPar => 配置参数
            |---clsL0_MedPlatePar => 托盘参数
            |---clsL0_MedPicPar=> 图像参数
            |---clsL0_MedSpsPar=> 串口参数
            |---clsL0_MedHandlerPar=> 全局对象和临界资源锁参数
    |---SEUI_L4_MengForm => 马达工程模式界面
        |---clsL3_MengProc => 马达工程模式参数填写接口
                |---clsL1_MdcThd => 自研马达控制器任务

线程启动过程
    SEUI_L4_MainWindow
        -> clsL3_CtrlSchdThread  => 调度任务，静态，已经完善对该状态的改造
                |---clsL1_MdcThd => 自研马达控制器任务 - 被启动第一个线程
    -> SEUI_L4_CalibForm
        -> clsL3_CalibProc
            -> clsL2_CalibPilotThread  =>巡游任务，静态，简单的工作任务，使用信号槽触发，不需要状态机
            -> clsL2_CalibCamDispThread  => 摄像头显示图像任务，动态
                |---clsL1_MdcThd => 自研马达控制器任务 - 被启动第二个线程
    -> SEUI_L4_GparForm
    -> SEUI_L4_MengForm
                |---clsL1_MdcThd => 自研马达控制器任务 - 被启动第三个线程

注意：信号槽，只能在线程和任务之间传递，所以普通的CLASS是不能增加信号槽的，设计机制时需要注意

'''

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
import platform

#System lib
from PyQt5 import QtWidgets, QtGui, QtCore,QtWebEngineWidgets
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
from form_qt.cebsmengform import Ui_cebsMengForm
from form_qt.cebsBroswerForm import Ui_BroswerForm

#Local Class
from PkgCebsHandler import ModCebsCom  #Common Support module
from PkgCebsHandler import ModCebsMoto
from PkgCebsHandler import ModCebsCtrlSchd
from PkgCebsHandler import ModCebsVision
from PkgCebsHandler import ModCebsCfg
from PkgCebsHandler import ModCebsCalib
from PkgCebsHandler import ModCebsGpar
from PkgCebsHandler import ModCebsMeng


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
        #SYSTEM LEVEL UI INIT, 系统级别的界面初始化
        self.setupUi(self)
        #USER LAVEL UI INIT, 用户级别的界面初始化
        self.initUI()
        #HARDWARE LEVEL INIT, 硬件初始化
        self.initParameter()
        
    def initUI(self):
        self.statusBar().showMessage('SYSTEM START ')
        self.setGeometry(10, 30, 1024, 768)
        exitAction = QAction(QIcon('.\icon_res\cebsExit.ico'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('EXIT SYSTEM')
        exitAction.triggered.connect(qApp.quit)
        toolbar = self.addToolBar('EXIT')  
        toolbar.addAction(exitAction)

        aboutAction = QAction(QIcon('.\icon_res\cebsAbout.ico'), '&About', self)
        aboutAction.setShortcut('Ctrl+A')
        aboutAction.setStatusTip('ABOUT SYSTEM - 上海小慧智能科技有限公司, 上海纳贤路800号科海大厦302-5')
        #aboutAction.triggered.connect(self.aboutCompanyBox())
        toolbar = self.addToolBar('About')  
        toolbar.addAction(aboutAction)


    #MUST Load global parameters, to initialize different UI and update the stored parameters.
    def initParameter(self):
        '''
        ModCebsCom.clsL0_MedCFlib.med_cfl_test1(self)
        c = ModCebsCom.clsL0_MedCFlib.med_cfl_add(self, 1, 2)
        print("Test result = %d" % (c))
        '''
        #STEP1: INI FILE CONFIGURATION, 初始化配置文件
        self.instL1ConfigOpr=ModCebsCfg.clsL1_ConfigOpr()
        self.instL1ConfigOpr.func_read_global_par_from_cfg_file()
        self.instL1ConfigOpr.func_read_global_par_from_cfg_file();  #读取本地文件的配置数据，并写入全局变量中来
        self.instL1ConfigOpr.updateCtrlCntInfo() #更新进度控制参量
        #STEP2: START SUB-UI, 启动子界面        
        self.instL4CalibForm = SEUI_L4_CalibForm()
        self.instL4GparForm = SEUI_L4_GparForm()
        self.instL4MengForm = SEUI_L4_MengForm()
        # self.instL4BroserForm=SEUI_L4_BroswerForm()
        #STEP3: CONNECT SIGNAL SLOT, 连接信号槽
        self.sgL4MainWinUnvisible.connect(self.funcMainWinUnvisible);
        self.instL4CalibForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        self.instL4GparForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        self.instL4MengForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        # self.instL4BroserForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        #STEP4: CONTROL SCHEDULE MODULE INIT, 控制调度模块初始化
        self.instL3CtrlSchdThd = ModCebsCtrlSchd.clsL3_CtrlSchdThread(self)
        self.instL3CtrlSchdThd.setIdentity("TASK_CtrlScheduleThread")
        self.instL3CtrlSchdThd.sgL4MainWinPrtLog.connect(self.slot_print_trigger)
        self.instL3CtrlSchdThd.sgL3CtrlCapStartNormal.connect(self.instL3CtrlSchdThd.funcTakePicStartNormal)
        self.instL3CtrlSchdThd.sgL3CtrlCapStartFlu.connect(self.instL3CtrlSchdThd.funcTakePicStartFlu)
        self.instL3CtrlSchdThd.sgL3CtrlCapStop.connect(self.instL3CtrlSchdThd.funcTakePicStop)
        self.instL3CtrlSchdThd.sgL3CtrlClfyStartNormal.connect(self.instL3CtrlSchdThd.funcVisionClasStartNormal)
        self.instL3CtrlSchdThd.sgL3CtrlClfyStartFlu.connect(self.instL3CtrlSchdThd.funcVisionClasStartFlu)
        self.instL3CtrlSchdThd.sgL3CtrlClfyStop.connect(self.instL3CtrlSchdThd.funcVisionClasStop)
        self.instL3CtrlSchdThd.sgL3CtrlCalibStart.connect(self.instL3CtrlSchdThd.funcCtrlCalibStart)
        self.instL3CtrlSchdThd.sgL3CtrlCalibStop.connect(self.instL3CtrlSchdThd.funcCtrlCalibStop)
        self.instL3CtrlSchdThd.sgL3CtrlMotoZero.connect(self.instL3CtrlSchdThd.funcCtrlMotoBackZero)
        self.instL3CtrlSchdThd.start();
        #STEP5: SET MOTO AND RELEVANT HARDWARE STATUS, 设置马达等物理硬件状态
        self.funcMainFormSetEquInitStatus();
        #STEP6: INTELLEGENT INIT CAMERA, 智能初始化摄像头#Detect all valid camera
        '''
                    方法一：搞定了，但长久初始化一个线程空间，没必要，简化模式的使用
        self.instL3VisCapProc = ModCebsVision.clsL2_VisCapProc(self, 1);
        res = self.instL3VisCapProc.funcVisionDetectAllCamera()
        '''
        res = ModCebsVision.clsL2_VisCapProc.funcVisionDetectAllCamera(self)
        self.slot_print_trigger(res)
        #STEP8:抢占硬件资源
        ModCebsCom.GLHLR_PAR_OFC.CHS_MOTO_MUTEX.acquire(5)
        self.instL3CtrlSchdThd.funcCtrlGetSpsRights(1)
        #STEP9: SEND BACK-ZERO SIGNAL TO MOTO, 发送归零信号给马达 #MAKE MOTO GO BACK TO ZERO
        self.instL3CtrlSchdThd.sgL3CtrlMotoZero.emit()

    def aboutCompanyBox(self):
        QMessageBox.about(self, '公司信息', '上海小慧智能科技有限公司, 上海纳贤路800号，科海大厦3楼')   
        
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
    #  SLOT FUNCTION, 槽函数部分
    #    DO NOT MODIFY FUNCTION NAMES, 以下部分为系统接口对应的槽函数，函数命名不得动
    #
    #
    def slot_print_trigger(self, info):
        self.med_debug_print(info)

    #Start taking picture
    def slot_ctrl_start_normal(self):
        self.med_debug_print("L4MAIN: Taking normal picture start......")
        self.instL3CtrlSchdThd.sgL3CtrlCapStartNormal.emit()

    #Start taking picture
    def slot_ctrl_start_flu(self):
        self.med_debug_print("L4MAIN: Taking Fluorescen picture start......")
        self.instL3CtrlSchdThd.sgL3CtrlCapStartFlu.emit()
    
    #Stop taking picture
    def slot_ctrl_stop(self):
        self.med_debug_print("L4MAIN: Taking picture stop......")
        self.instL3CtrlSchdThd.sgL3CtrlCapStop.emit()

    #Control moto run to Zero position
    def slot_ctrl_zero(self):
        self.med_debug_print("L4MAIN: Moto run to zero position......")
        self.instL3CtrlSchdThd.sgL3CtrlMotoZero.emit()

    #Start vision classification
    def slot_ctrl_vclas_start_normal(self):
        self.med_debug_print("L4MAIN: Normal picture classification starting......")
        self.instL3CtrlSchdThd.sgL3CtrlClfyStartNormal.emit()

    #Start vision classification
    def slot_ctrl_vclas_start_flu(self):
        self.med_debug_print("L4MAIN: Fluorescen picture classification starting......")
        self.instL3CtrlSchdThd.sgL3CtrlClfyStartFlu.emit()

    #Stop vision classification
    def slot_ctrl_vclas_stop(self):
        self.med_debug_print("L4MAIN: Picture classification stop......")
        self.instL3CtrlSchdThd.sgL3CtrlClfyStop.emit()

    #Enter calibration session
    def slot_ctrl_calib(self):
        if (self.instL3CtrlSchdThd.funcCtrlGetRightStatus() < 0):
            self.med_debug_print("L4MAIN: CALIB error!")
            return -1;
        self.med_debug_print("L4MAIN: Calibration start!")
        self.instL3CtrlSchdThd.sgL3CtrlCalibStart.emit()
        if not self.instL4CalibForm.isVisible():
            self.sgL4MainWinUnvisible.emit()
            #抢占硬件资源
            ModCebsCom.GLHLR_PAR_OFC.CHS_MOTO_MUTEX.acquire(5)
            self.instL4CalibForm.instL3CalibProc.funcCalibGetSpsRights(2);
            self.instL4CalibForm.show()

    #Enter parameter setting session
    def slot_gpar_start(self):
        self.med_debug_print("L4MAIN: Global parameter set start......")
        if not self.instL4GparForm.isVisible():
            self.sgL4MainWinUnvisible.emit()
            #这里的申请，是为了后面回到主界面，做visualWin时，统一再次抢资源所用，不然会造成不同情况下处理过程不一致的情况
            ModCebsCom.GLHLR_PAR_OFC.CHS_MOTO_MUTEX.acquire(5)
            self.instL4GparForm.show()

    #Enter Moto Engineering Mode
    def slot_meng_sel(self):
        self.med_debug_print("L4MAIN: Moto Engineering start......")
        if not self.instL4MengForm.isVisible():
            self.sgL4MainWinUnvisible.emit()
            #抢占硬件资源
            ModCebsCom.GLHLR_PAR_OFC.CHS_MOTO_MUTEX.acquire(5)
            self.instL4MengForm.funcGetLowLevelResource(3);
            self.instL4MengForm.show()

    #Enter Selection Active Hole Target Mode
    def slot_saht_sel(self):
        self.instL4BroserForm = SEUI_L4_BroswerForm()
        self.instL4BroserForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        self.med_debug_print("L4MAIN: Active Hole Selection start......")
        if not self.instL4BroserForm.isVisible():
            self.sgL4MainWinUnvisible.emit()
            self.instL4BroserForm.show()

    #Clean log window
    def slot_runpg_clear(self):
        self.textEdit_runProgress.clear();

    #Test functions
    def slot_runpg_test(self):
        res = {'nothing!'}
        self.med_debug_print("TEST: " + str(res))
        obj = ModCebsVision.clsL2_VisCapProc(self)
        obj.algoVisGetRadians(ModCebsCom.GLPLT_PAR_OFC.med_get_radians_len_in_us(), "ref.jpg", "scale_ref.jpg")

    #
    #  SLOT FUNCTION, 槽函数部分
    #    DO NOT MODIFY SLOT FUNCTIONS NAME, 以下部分为系统接口对应的槽函数，函数命名不得动
    #
    #
    #Control UI visible
    def funcMainWinVisible(self):
        if not self.isVisible():
            self.show()
        self.instL3CtrlSchdThd.sgL3CtrlCalibStop.emit()
        #抢占硬件资源
        ModCebsCom.GLHLR_PAR_OFC.CHS_MOTO_MUTEX.acquire(5)
        self.instL3CtrlSchdThd.funcCtrlGetSpsRights(1)
        self.med_debug_print("L4MAIN: Main form welcome to come back!")

    #Control UI un-visible
    def funcMainWinUnvisible(self):
        if self.isVisible():
            self.hide()
            self.med_debug_print("L4MAIN: Main form hide!")
        #释放硬件资源
        self.instL3CtrlSchdThd.funcCtrlRelSpsRights(1)
        ModCebsCom.GLHLR_PAR_OFC.CHS_MOTO_MUTEX.release()

    '''采用简化模式，省的启动那么多类的Instance
    #self.instL2MotoProc = ModCebsMoto.clsL2_MotoProc(self, 1) #第一种选择
    #if (self.instL2MotoProc.funcMotoRunningStatusInquery() == True):
    #    self.instL2MotoProc.funcMotoStop()
    '''
    #Local function
    def funcMainFormSetEquInitStatus(self):
        if (ModCebsMoto.clsL2_MotoProc.funcMotoRunningStatusInquery(self) == True):
            ModCebsMoto.clsL2_MotoProc.funcMotoStop(self)



#第二主入口
#Calibration Widget
class SEUI_L4_CalibForm(QtWidgets.QWidget, Ui_cebsCalibForm):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()
    sgL4CalibFormActiveTrig = pyqtSignal()

    def __init__(self):    
        super(SEUI_L4_CalibForm, self).__init__()  
        self.setupUi(self)
        self.instL3CalibProc = ModCebsCalib.clsL3_CalibProc(self)
        self.sgL4CalibFormActiveTrig.connect(self.instL3CalibProc.funcActiveTrig)
        self.instL1ConfigOpr1 = ModCebsCfg.clsL1_ConfigOpr()
        
    def med_debug_print(self, info):
        strOut = ">> " + time.asctime() + " " + info;
        self.textEdit_calib_runProgress.append(strOut);
        self.textEdit_calib_runProgress.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_calib_runProgress.ensureCursorVisible()
        self.textEdit_calib_runProgress.insertPlainText("")       
        
    #
    #  SLOT FUNCTION, 槽函数部分
    #    DO NOT MODIFY SLOT FUNCTION NAMES, 以下部分为系统接口对应的槽函数，函数命名不得动
    #
    # 
    def slot_calib_pilot_move_up(self):
        time.sleep(0.1)
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
        
        self.instL3CalibProc.funcCalibMove(parMoveScale, "UP");
        
    def slot_calib_pilot_move_down(self):
        time.sleep(0.1)
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
        
        self.instL3CalibProc.funcCalibMove(parMoveScale, "DOWN");    
        
    def slot_calib_pilot_move_left(self):
        time.sleep(0.1)
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
        
        self.instL3CalibProc.funcCalibMove(parMoveScale, "LEFT"); 
        
    def slot_calib_pilot_move_right(self):
        time.sleep(0.1)
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
        
        self.instL3CalibProc.funcCalibMove(parMoveScale, "RIGHT"); 
    '''
    def slot_calib_pilot_move_up(self): 
        self.timer=QTimer()
        self.timer.setInterval(1)
        self.timer.start()
        self.timer.timeout.connect(self.onTimerOutUp) 
        
    def slot_calib_pilot_move_up_released(self):
        self.timer.stop()    
    
    def slot_calib_pilot_move_down(self): 
        self.timer=QTimer()
        self.timer.setInterval(1)
        self.timer.start()
        self.timer.timeout.connect(self.onTimerOutDown) 
        
    def slot_calib_pilot_move_down_released(self):
        self.timer.stop()
        
    def slot_calib_pilot_move_left(self): 
        self.timer=QTimer()
        self.timer.setInterval(1)
        self.timer.start()
        self.timer.timeout.connect(self.onTimerOutLeft) 
        
    def slot_calib_pilot_move_left_released(self):
        self.timer.stop()
        
    def slot_calib_pilot_move_right(self): 
        self.timer=QTimer()
        self.timer.setInterval(1)
        self.timer.start()
        self.timer.timeout.connect(self.onTimerOutRight)
        
    def slot_calib_pilot_move_right_released(self):
        self.timer.stop()          
    ''' 
    '''            
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
    '''
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
            holeNbr = int(self.lineEdit_pilot_move_n.text())
        except Exception: 
            holeNbr = 1;
        self.instL3CalibProc.funcCalibPilotMoven(holeNbr);
    
    #CAMERA ENABLE: Not support any more!
    def slot_calib_pilot_camera_enable(self):
        self.instL3CalibProc.funcCalibPilotCameraEnable();

    #CAMERA CAPTURE: new function support
    def slot_calib_pilot_camera_cap(self):
        try:
            holeNbr = int(self.lineEdit_pilot_move_n.text())
        except Exception: 
            holeNbr = 1;        
        self.instL3CalibProc.funcCalibPilotCameraCapture(holeNbr);

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
        self.close()

    def closeEvent(self, event):
        self.instL3CalibProc.funcRecoverWorkingEnv()
        #释放硬件资源
        self.instL3CalibProc.funcCalibRelSpsRights(2)
        ModCebsCom.GLHLR_PAR_OFC.CHS_MOTO_MUTEX.release()
        self.sgL4MainWinVisible.emit()
        self.close()


#3rd Main Entry, 第三主入口
#Calibration Widget
class SEUI_L4_GparForm(QtWidgets.QWidget, Ui_cebsGparForm):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()

    def __init__(self):    
        super(SEUI_L4_GparForm, self).__init__()  
        self.setupUi(self)
        self.instL3GparProc = ModCebsGpar.clsL3_GparProc(self)
        self.instL1ConfigOpr2=ModCebsCfg.clsL1_ConfigOpr()
        #Update UI interface last time parameter setting
        self.funcGlobalParReadSet2Ui()

    def med_debug_print(self, info):
        strOut = ">> " + time.asctime() + " " + info;
        self.textEdit_gpar_cmd_log.append(strOut);
        self.textEdit_gpar_cmd_log.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_gpar_cmd_log.ensureCursorVisible()
        self.textEdit_gpar_cmd_log.insertPlainText("")        

    
    '''
    *得到文件目录
    directory1 = QFileDialog.getExistingDirectory(self, "选取文件夹", "C:/")
    * 打开文件
    files, ok1 = QFileDialog.getOpenFileNames(self, "多文件选择", "C:/", "All Files (*);;Text Files (*.txt)")
    * 存储文件
    fileName2, ok2 = QFileDialog.getSaveFileName(self, 文件保存", "C:/", "All Files (*);;Text Files (*.txt)")    
    '''
    def slot_gpar_pic_file_load(self):
        if ('Windows' in platform.system()):
            fileName, _ = QFileDialog.getOpenFileName(self, "选取文件", "D:\\", "All Files (*);;Text Files (*.txt)")   #设置文件扩展名过滤,注意用双分号间隔
        else:
            fileName, _ = QFileDialog.getOpenFileName(self, "选取文件", "/home/", "All Files (*);;Text Files (*.txt)")   #设置文件扩展名过滤,注意用双分号间隔
        #将文件导入到目标框中
        if (fileName != ''):
            self.instL3GparProc.funcPicFileLoad(fileName)

    def slot_gpar_pic_train(self):
        #Firstly read parameter into classified variable sets, to let Train Func use.
        self.funcReadVisParToCfySets();    #获取SAV
        #在训练之前，需要将系统参数保存在临时变量中，借助于全局变量的传递，进行算法训练。一旦完成，还要再回写。
        savetmp = ModCebsCom.GLVIS_PAR_SAV   #将SAV值传给临时变量
        ModCebsCom.GLVIS_PAR_OFC = ModCebsCom.GLVIS_PAR_SAV   #将SAV值传给OFC
        self.instL3GparProc.funcPicFileTrain()              #训练
        ModCebsCom.GLVIS_PAR_OFC = savetmp                  #SAV给OFC
        
    #
    #  SERVICE FUNCTION PART, 业务函数部分
    #
    #
    #Local function
    def funcGlobalParReadSave(self):
        ModCebsCom.GLVIS_PAR_OFC.PIC_CLASSIFIED_AFTER_TAKE_SET = self.checkBox_gpar_autoIdf.isChecked();
        ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_AFTER_START_SET = self.checkBox_gpar_autoPic.isChecked();
        ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET = self.checkBox_gpar_picFixPos.isChecked();
        try: 
            ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR = int(self.lineEdit_gpar_camera_nbr.text());
        except Exception: 
            ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR = -1;
        try: 
            ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN = int(self.lineEdit_gpar_picTti.text());
        except Exception: 
            ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN = 60;
            
#         try: 
#             ModCebsCom.GLVIS_PAR_OFC.saveLowLimit(int(self.lineEdit_gpar_vision_small_low_limit.text()))
#         except Exception: 
#             ModCebsCom.GLVIS_PAR_OFC.saveLowLimit(200)
#         try: 
#             ModCebsCom.GLVIS_PAR_OFC.saveMidLimit(int(self.lineEdit_gpar_vision_small_mid_limit.text()))
#         except Exception: 
#             ModCebsCom.GLVIS_PAR_OFC.saveMidLimit(500)
#         try: 
#             ModCebsCom.GLVIS_PAR_OFC.saveBigLimit(int(self.lineEdit_gpar_vision_mid_big_limit.text()))
#         except Exception: 
#             ModCebsCom.GLVIS_PAR_OFC.saveBigLimit(2000)
#         try: 
#             ModCebsCom.GLVIS_PAR_OFC.saveUpperLimit(int(self.lineEdit_gpar_vision_big_upper_limit.text()))
#         except Exception: 
#             ModCebsCom.GLVIS_PAR_OFC.saveUpperLimit(2000)
        ModCebsCom.GLVIS_PAR_OFC.saveAddupSet(self.checkBox_gpar_vision_res_addup.isChecked())
        ModCebsCom.GLVIS_PAR_OFC.saveCapEnable(self.checkBox_gpar_video_enable.isChecked())
        try: 
            ModCebsCom.GLVIS_PAR_OFC.saveCapDur(int(self.lineEdit_gpar_video_input.text()))
        except Exception: 
            ModCebsCom.GLVIS_PAR_OFC.saveCapDur(3)
        #HB-TYPE SELECTION
        radioGparHts96 = self.radioButton_gpar_bts_96.isChecked();
        radioGparHts48 = self.radioButton_gpar_bts_48.isChecked();
        radioGparHts24 = self.radioButton_gpar_bts_24.isChecked();
        radioGparHts12 = self.radioButton_gpar_bts_12.isChecked();
        radioGparHts6 = self.radioButton_gpar_bts_6.isChecked();
        
        ModCebsCom.GLVIS_PAR_OFC.SMALL_LOW_LIMIT = ModCebsCom.GLVIS_PAR_SAV.SMALL_LOW_LIMIT
        ModCebsCom.GLVIS_PAR_OFC.SMALL_MID_LIMIT = ModCebsCom.GLVIS_PAR_SAV.SMALL_MID_LIMIT
        ModCebsCom.GLVIS_PAR_OFC.MID_BIG_LIMIT = ModCebsCom.GLVIS_PAR_SAV.MID_BIG_LIMIT
        ModCebsCom.GLVIS_PAR_OFC.BIG_UPPER_LIMIT = ModCebsCom.GLVIS_PAR_SAV.BIG_UPPER_LIMIT
         
        option = 0;
        if (radioGparHts96 == 1): option = 96
        elif (radioGparHts48 == 1): option = 48
        elif (radioGparHts24 == 1): option = 24
        elif (radioGparHts12 == 1): option = 12
        elif (radioGparHts6 == 1): option = 6
        else: option = 6
        ModCebsCom.GLPLT_PAR_OFC.med_select_plate_board_type(option)
        #FINAL UPDATE         
        self.instL1ConfigOpr2.updateSectionPar()

    #Using global parameter set to UI during launch
    def funcGlobalParReadSet2Ui(self):
        self.checkBox_gpar_picFixPos.setChecked(ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET)
        self.checkBox_gpar_autoIdf.setChecked(ModCebsCom.GLVIS_PAR_OFC.PIC_CLASSIFIED_AFTER_TAKE_SET)
        self.checkBox_gpar_autoPic.setChecked(ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_AFTER_START_SET)
        self.lineEdit_gpar_camera_nbr.setText(str(ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR))
        self.lineEdit_gpar_picTti.setText(str(ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN))
        self.lineEdit_gpar_vision_small_low_limit.setText(str(ModCebsCom.GLVIS_PAR_OFC.SMALL_LOW_LIMIT))
        self.lineEdit_gpar_vision_small_mid_limit.setText(str(ModCebsCom.GLVIS_PAR_OFC.SMALL_MID_LIMIT))
        self.lineEdit_gpar_vision_mid_big_limit.setText(str(ModCebsCom.GLVIS_PAR_OFC.MID_BIG_LIMIT))
        self.lineEdit_gpar_vision_big_upper_limit.setText(str(ModCebsCom.GLVIS_PAR_OFC.BIG_UPPER_LIMIT))
        self.checkBox_gpar_vision_res_addup.setChecked(ModCebsCom.GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET)
        self.checkBox_gpar_video_enable.setChecked(ModCebsCom.GLVIS_PAR_OFC.CAPTURE_ENABLE)
        self.lineEdit_gpar_video_input.setText(str(ModCebsCom.GLVIS_PAR_OFC.CAPTURE_DUR_IN_SEC))
        if (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_96_STANDARD):
            self.radioButton_gpar_bts_96.setChecked(True)
        elif (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_48_STANDARD):
            self.radioButton_gpar_bts_48.setChecked(True)
        elif (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_24_STANDARD):
            self.radioButton_gpar_bts_24.setChecked(True)
        elif (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_12_STANDARD):
            self.radioButton_gpar_bts_12.setChecked(True)
        elif (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_6_STANDARD):
            self.radioButton_gpar_bts_6.setChecked(True)
        else:
            self.radioButton_gpar_bts_96.setChecked(True)

    def funcReadVisParToCfySets(self):
        try: 
            ModCebsCom.GLVIS_PAR_SAV.saveLowLimit(int(self.lineEdit_gpar_vision_small_low_limit.text()))
        except Exception: 
            ModCebsCom.GLVIS_PAR_SAV.saveLowLimit(200)
        try: 
            ModCebsCom.GLVIS_PAR_SAV.saveMidLimit(int(self.lineEdit_gpar_vision_small_mid_limit.text()))
        except Exception: 
            ModCebsCom.GLVIS_PAR_SAV.saveMidLimit(500)
        try: 
            ModCebsCom.GLVIS_PAR_SAV.saveBigLimit(int(self.lineEdit_gpar_vision_mid_big_limit.text()))
        except Exception: 
            ModCebsCom.GLVIS_PAR_SAV.saveBigLimit(2000)
        try: 
            ModCebsCom.GLVIS_PAR_SAV.saveUpperLimit(int(self.lineEdit_gpar_vision_big_upper_limit.text()))
        except Exception: 
            ModCebsCom.GLVIS_PAR_SAV.saveUpperLimit(2000)
        ModCebsCom.GLVIS_PAR_SAV.saveAddupSet(self.checkBox_gpar_vision_res_addup.isChecked())
        ModCebsCom.GLVIS_PAR_SAV.saveCapEnable(self.checkBox_gpar_video_enable.isChecked())
        try: 
            ModCebsCom.GLVIS_PAR_SAV.saveCapDur(int(self.lineEdit_gpar_video_input.text()))
        except Exception: 
            ModCebsCom.GLVIS_PAR_SAV.saveCapDur(3)    

    #
    #  SLOT FUNCTION, 槽函数部分
    #    DO NOT MODIFY FUNCTION NAMES, 以下部分为系统接口对应的槽函数，函数命名不得动
    #    compl和giveup函数必须将释放mutex的动作放在closeEvent中统一完成，不然会造成完不成的情况
    #
    #    
    def slot_gpar_compl(self):
        self.funcGlobalParReadSave()
        self.close()

    #Give up and not save parameters
    def slot_gpar_giveup(self):
        self.close()

    #Clear the command log text box
    def slot_gpar_clear(self):
        self.textEdit_gpar_cmd_log.clear();  
              
    #Give up and not save parameters
    def closeEvent(self, event):
        self.instL3GparProc.funcRecoverWorkingEnv()
        ModCebsCom.GLHLR_PAR_OFC.CHS_MOTO_MUTEX.release()
        self.sgL4MainWinVisible.emit()
        self.close()


#4rd Main Entry, 第四主入口
#Meng Widget
class SEUI_L4_MengForm(QtWidgets.QWidget, Ui_cebsMengForm):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()

    def __init__(self):    
        super(SEUI_L4_MengForm, self).__init__()  
        self.setupUi(self)
        self.instL3MengProc = ModCebsMeng.clsL3_MengProc(self)
        self.instL1ConfigOpr3=ModCebsCfg.clsL1_ConfigOpr()

    def med_debug_print(self, info):
        strOut = ">> " + time.asctime() + " " + info;
        self.textEdit_meng_trace_log.append(strOut);
        self.textEdit_meng_trace_log.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_meng_trace_log.ensureCursorVisible()
        self.textEdit_meng_trace_log.insertPlainText("")        
    #
    #  SLOT FUNCTION, 槽函数部分
    #    DO NOT MODIFY FUNCTION NAMES, 以下部分为系统接口对应的槽函数，函数命名不得动
    #
    #    
    def slot_meng_compl(self):
        self.close()

    #Give up and not save parameters
    def slot_meng_giveup(self):
        self.close()

    #Send the command out
    def slot_meng_cmd_send(self):
        text_list = self.listWidget_meng_cmd.selectedItems()
        text = [i.text() for i in list(text_list)]
        if (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_SHK_HAND) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_SHK_HAND_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_WK_MODE) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_SET_WK_MODE_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_ACC) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_SET_ACC_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_DEACC) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_SET_DEACC_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_PPC) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_SET_PPC_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_MV_SPD) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_SET_MV_SPD_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_ZO_SPD) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_SET_ZO_SPD_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_ZO_ACC) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_SET_ZO_ACC_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_INT_SP) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_SET_INT_SP_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_MV_PULS) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_MV_PULS_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_MV_SPD) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_MV_SPD_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_MV_ZERO) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_MV_ZERO_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_STP_IMD) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_STP_IMD_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_STP_NOR) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_STP_NOR_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_INQ_EN) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_INQ_EN_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_INQ_RUN) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_INQ_RUN_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_INQ_STATUS) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_INQ_STATUS_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_TEST_PULES) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_TEST_PULES_CMID
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_EXTI_DELAY_TIME_CMID) > 0):
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_SET_EXTI_DELAY_TIME_CMID
        else:
            cmd = ModCebsCom.GLSPS_PAR_OFC.SPS_SHK_HAND_CMID
        
        try: 
            par1 = int(self.lineEdit_meng_par1.text());
        except Exception: 
            par1 = -1;
        try: 
            par2 = int(self.lineEdit_meng_par2.text());
        except Exception: 
            par2 = -1;
        try: 
            par3 = int(self.lineEdit_meng_par3.text());
        except Exception: 
            par3 = -1;
        try: 
            par4 = int(self.lineEdit_meng_par4.text());
        except Exception: 
            par4 = -1;            
                       
        #self.med_debug_print("MENG: Cmd = %d, Par1/2/3/4=%d/%d/%d/%d" % (cmd, par1, par2, par3, par4))
        res = self.instL3MengProc.funcSendCmd2Moto(cmd, par1, par2, par3, par4)
        self.lineEdit_meng_cmd_par.setText(str(res))
        
    #Clear the command log text box
    def slot_meng_trace_clear(self):
        self.textEdit_meng_trace_log.clear();

    #Give up and not save parameters
    def closeEvent(self, event):
        self.funcRelLowLevelResource(3)
        ModCebsCom.GLHLR_PAR_OFC.CHS_MOTO_MUTEX.release()
        self.sgL4MainWinVisible.emit()
        self.close()

    def funcGetLowLevelResource(self, par):
        self.instL3MengProc.funcGetSpsRights(par)

    def funcRelLowLevelResource(self, par):
        self.instL3MengProc.funcRelSpsRights(par)
        
                
class SEUI_L4_BroswerForm(QtWidgets.QMainWindow, Ui_BroswerForm):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()
    def __init__(self):
        super(SEUI_L4_BroswerForm, self).__init__()
        self.setupUi(self)
        self.openBroswer()
    def openBroswer(self):
        print("[CEBS]  Open Broswer is Start")
        config=ModCebsCfg.clsL1_ConfigOpr()
        name,configure=config.GetMachineTagandConfigure()
        number=int(configure.split("_")[0])
        if number==96:
            row=8
            column=12
        else:
            row=0
            column=0
        url="http://127.0.0.1/work/QtWeb1.html?row="+str(row)+"&column="+str(column)+"&name="+name
        self.broswer=QtWebEngineWidgets.QWebEngineView()
        self.broswer.load(QtCore.QUrl(url))
        self.setCentralWidget(self.broswer)

    def closeEvent(self, event):
        config = ModCebsCfg.clsL1_ConfigOpr()
        config.SetDishRowandColumn()
        self.sgL4MainWinVisible.emit()
        self.close()

        
'''
'高级技巧，还未搞定'
'https://www.cnblogs.com/WSX1994/articles/9092331.html'

探索使得加载更加人性化和自动化
'''
def load_data(sp):
    for i in range(1, 2):              #模拟主程序加载过程 
        time.sleep(1)                   # 加载数据
        sp.showMessage("加载... {0}%".format(i * 10), QtCore.Qt.AlignHCenter |QtCore.Qt.AlignBottom, QtCore.Qt.black)
        QtWidgets.qApp.processEvents()  # 允许主进程处理事件

#THE MAIN ENTRY: 第0主入口，MAIN函数部分
#Main App entry
def main_form():
    app = QtWidgets.QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("cebsStart.jpg"))
    splash.showMessage("加载...0%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    splash.resize(1202, 800)
    splash.show()
    load_data(splash)
    QtWidgets.qApp.processEvents()
    mainWindow = SEUI_L4_MainWindow()
    mainWindow.show()
    splash.hide()
    sys.exit(app.exec_())

#SYSTEM ENTRY
if __name__ == '__main__':
    print("[CEBS] ", time.asctime(), ", System starting...\n" );
    main_form()