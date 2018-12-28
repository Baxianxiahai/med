'''
Created on 2018年12月28日

@author: Administrator
'''

####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-

import sys
import time
import platform
import os
import cv2 as cv
from PyQt5 import QtWidgets, QtGui, QtCore,QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, qApp, QAction, QFileDialog, QTextEdit, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon
#from PyQt5.uic import loadUi

#Local Class
from PkgVmHandler.ModVmLayer import *
from PkgCebsHandler.ModCebsCom import *
from PkgCebsHandler.ModCebsCfg import *

#Form class
from form_qt.cebsmainform import Ui_cebsMainWindow

#UI Class
import PkgCeuiHandler.ModCeuiCalib
import PkgCeuiHandler.ModCeuiGpar
import PkgCeuiHandler.ModCeuiMeng
import PkgCeuiHandler.ModCeuiStest
import PkgCeuiHandler.ModCeuiAhole







'''
#SEUI => System Entry UI，表示系统级的主入口
第一主入口
Main Windows

主菜单分解：
    #自测 - Stest
    #工参 - Gpar
    #马达 - Meng
    #板孔 - Browse
    #校准 - Calib
    #拍照 - Main - Pic
    #识别 - Main - Cfy
    #设置 - Sset
'''
class SEUI_L4_MainWindow(QtWidgets.QMainWindow, Ui_cebsMainWindow, clsL1_ConfigOpr):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()

    def __init__(self, TaskInstMainUi, TaskInstCalibUi, TaskInstGparUi, TaskInstMengUi, TaskInstStestUi, TaskInstBrowUi):    
        super(SEUI_L4_MainWindow, self).__init__()
        #CASE1:
        #SYSTEM LEVEL UI INIT, 系统级别的界面初始化
        self.setupUi(self)
        #USER LAVEL UI INIT, 用户级别的界面初始化
        self.initUI()

        #CASE2
        #存储任务对象指针，以便双向通信
        self.TkMainUi = TaskInstMainUi
        self.TkCalibUi = TaskInstCalibUi
        self.TkGparUi = TaskInstGparUi
        self.TkMengUi = TaskInstMengUi
        self.TkStestUi = TaskInstStestUi
        self.TkBrowUi = TaskInstBrowUi

        #CASE3: HARDWARE LEVEL INIT, 硬件初始化
        self.initParameter()
        
    def initUI(self):
        self.statusBar().showMessage('SYSTEM START ')
        self.setGeometry(10, 30, 1024, 768)
        exitAction = QAction(QIcon('.\icon_res\cebsExit.ico'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('EXIT SYSTEM')
        #exitAction.triggered.connect(qApp.quit)
        exitAction.triggered.connect(self.quit)
        toolbar = self.addToolBar('EXIT')  
        toolbar.addAction(exitAction)
        aboutAction = QAction(QIcon('.\icon_res\cebsAbout.ico'), '&About', self)
        aboutAction.setShortcut('Ctrl+A')
        aboutAction.setStatusTip('ABOUT SYSTEM - 上海小慧智能科技有限公司, 上海纳贤路800号科海大厦302-5')
        #aboutAction.triggered.connect(self.aboutCompanyBox())
        toolbar = self.addToolBar('About')  
        toolbar.addAction(aboutAction)
        #主菜单跟命令关联
        #自测
        self.actionMenuStestProc.triggered.connect(self.slot_Stest_sel)
        self.actionMenuStestRndCmd.triggered.connect(self.slot_runpg_test)
        #工参 
        self.actionMenuGparSet.triggered.connect(self.slot_gpar_start)
        #马达
        self.actionMenuMengMode.triggered.connect(self.slot_meng_sel)
        self.actionMenuMengZero.triggered.connect(self.slot_ctrl_zero)
        #板孔
        self.actionMenuBrowseSelect.triggered.connect(self.slot_saht_sel)
        #校准
        self.actionMenuCalibMode.triggered.connect(self.slot_ctrl_calib)
        #拍照
        self.actionMenuPicNorStart.triggered.connect(self.slot_ctrl_start_normal)
        self.actionMenuPicFluStart.triggered.connect(self.slot_ctrl_start_flu)
        self.actionMenuPicStop.triggered.connect(self.slot_ctrl_stop)
        #识别
        self.actionMenuCfyNorStart.triggered.connect(self.slot_ctrl_vclas_start_normal)
        self.actionMenuCfyFluStart.triggered.connect(self.slot_ctrl_vclas_start_flu)
        self.actionMenuCfyStop.triggered.connect(self.slot_ctrl_vclas_stop)
        #设置
        self.actionMenuSsetExit.triggered.connect(self.quit)
        self.actionMenuSsetAbout.triggered.connect(self.about)
        
        

    #MUST Load global parameters, to initialize different UI and update the stored parameters.
    def initParameter(self):
        #STEP1: START SUB-UI, 启动子界面        
        self.instL4CalibForm = PkgCeuiHandler.ModCeuiCalib.SEUI_L4_CalibForm(self.TkCalibUi)
        self.instL4GparForm = PkgCeuiHandler.ModCeuiGpar.SEUI_L4_GparForm(self.TkGparUi)
        self.instL4MengForm = PkgCeuiHandler.ModCeuiMeng.SEUI_L4_MengForm(self.TkMengUi)
        self.instL4StestForm = PkgCeuiHandler.ModCeuiStest.SEUI_L4_StestForm(self.TkStestUi)
        #self.instL4BroserForm = PkgCeuiHandler.ModCeuiAhole.SEUI_L4_BroswerForm(self.TkBrowUi)
        
        #STEP2: CONNECT SIGNAL SLOT, 连接信号槽
        self.sgL4MainWinUnvisible.connect(self.funcMainWinUnvisible);
        self.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        self.instL4CalibForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        self.instL4GparForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        self.instL4MengForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        self.instL4StestForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        #self.instL4BroserForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        
        #STEP3: 使用传递指针的方式
        self.TkMainUi.funcSaveFatherInst(self)

    def aboutCompanyBox(self):
        QMessageBox.about(self, '公司信息', '上海小慧智能科技有限公司, 上海纳贤路800号，科海大厦3楼')   
        
    #File Open Method, for reference
    def test_openMsg(self):  
        file, ok=QFileDialog.getOpenFileName(self,"OPEN FILE","C:/","All Files (*);;Text Files (*.txt)")  
        self.statusbar.showMessage(file)

    #strOut = strOld + "\n>> " + str(time.asctime()) + " " + str(info);
    #self.textEdit_runProgress.setText(strOut);
    def cetk_debug_print(self, info):
        time.sleep(0.01)
        strOld = self.textEdit_runProgress.toPlainText()
        strOut = ">> " + str(time.asctime()) + " " + str(info);
        self.textEdit_runProgress.append(strOut);
        self.textEdit_runProgress.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_runProgress.ensureCursorVisible()
        self.textEdit_runProgress.insertPlainText("")
    
    '''
    #  SLOT FUNCTION, 槽函数部分
    #    DO NOT MODIFY FUNCTION NAMES, 以下部分为系统接口对应的槽函数，函数命名不得动
    #
    '''
    #Start taking picture
    def slot_ctrl_start_normal(self):
        #self.cetk_debug_print("L4MAIN: Taking normal picture start......")
        self.TkMainUi.func_ui_click_cap_start_nor();

    #Start taking picture
    def slot_ctrl_start_flu(self):
        #self.cetk_debug_print("L4MAIN: Taking Fluorescen picture start......")
        self.TkMainUi.func_ui_click_cap_start_flu();
    
    #Stop taking picture
    def slot_ctrl_stop(self):
        #self.cetk_debug_print("L4MAIN: Taking picture stop......")
        self.TkMainUi.func_ui_click_cap_stop();

    #Control moto run to Zero position
    def slot_ctrl_zero(self):
        #self.cetk_debug_print("L4MAIN: Moto run to zero position......")
        self.TkMainUi.func_ui_click_move_zero();

    #Start vision classification
    def slot_ctrl_vclas_start_normal(self):
        #self.cetk_debug_print("L4MAIN: Normal picture classification starting......")
        self.TkMainUi.func_ui_click_clf_start_nor();

    #Start vision classification
    def slot_ctrl_vclas_start_flu(self):
        #self.cetk_debug_print("L4MAIN: Fluorescen picture classification starting......")
        self.TkMainUi.func_ui_click_clf_start_flu();

    #Stop vision classification
    def slot_ctrl_vclas_stop(self):
        #self.cetk_debug_print("L4MAIN: Picture classification stop......")
        self.TkMainUi.func_ui_click_clf_stop();

    #Enter calibration session
    def slot_ctrl_calib(self):
        self.cetk_debug_print("L4MAIN: Calibration start!")
        if not self.instL4CalibForm.isVisible():
            self.TkMainUi.func_ui_click_calib_start();
            self.sgL4MainWinUnvisible.emit()
            self.instL4CalibForm.show()
            #指示CALIB界面进入事件
            self.instL4CalibForm.switchOn()

    #Enter parameter setting session
    def slot_gpar_start(self):
        self.cetk_debug_print("L4MAIN: Global parameter set start......")
        if not self.instL4GparForm.isVisible():
            self.TkMainUi.func_ui_click_gpar_start();
            self.sgL4MainWinUnvisible.emit()
            self.instL4GparForm.show()
            #指示GPAR界面进入事件
            self.instL4GparForm.switchOn()

    #Enter Moto Engineering Mode
    def slot_meng_sel(self):
        self.cetk_debug_print("L4MAIN: Moto Engineering start......")
        if not self.instL4MengForm.isVisible():
            self.TkMainUi.func_ui_click_meng_start();
            self.sgL4MainWinUnvisible.emit()
            self.instL4MengForm.show()
            #指示MENG界面进入事件
            self.instL4MengForm.switchOn()

    #Enter Selection Active Hole Target Mode
    def slot_saht_sel(self):
        self.cetk_debug_print("L4MAIN: Active Hole Selection function under construction......")
        #if not self.instL4BroserForm.isVisible():
            #self.sgL4MainWinUnvisible.emit()
            #self.instL4BroserForm.show()

    #Clean log window
    def slot_runpg_clear(self):
        self.textEdit_runProgress.clear();

    #Test functions
    def slot_runpg_test(self):
        #res = {'nothing!'}
        #self.cetk_debug_print("TEST: " + str(res))
        #obj = ModCebsVision.clsL2_VisCapProc(self)
        #obj.algoVisGetRadians(ModCebsCom.GLPLT_PAR_OFC.med_get_radians_len_in_us(), "ref.jpg", "scale_ref.jpg")
        
        self.TkMainUi.funcPrintTestCalledByQt("TEST! Send test msg to UI_MAIN and then send back to UI show by signal slot.")


    #密钥过程的处理方法
    def mainui_callback_chk_pswd_failure(self):
        self.close()

    #Enter Self Test Procedure
    def slot_Stest_sel(self):
        self.cetk_debug_print("L4MAIN: Stest start......")
        if not self.instL4StestForm.isVisible():
            self.TkMainUi.func_ui_click_stest_start();
            self.sgL4MainWinUnvisible.emit()
            self.instL4StestForm.show()
            #指示STEST界面进入事件
            self.instL4StestForm.switchOn()


    '''
    #  SLOT FUNCTION, 槽函数部分
    #    DO NOT MODIFY SLOT FUNCTIONS NAME, 以下部分为系统接口对应的槽函数，函数命名不得动
    #
    '''
    #Control UI visible
    def funcMainWinVisible(self):
        if not self.isVisible():
            self.show()
            self.TkMainUi.func_ui_click_main_start();
        self.cetk_debug_print("L4MAIN: Main form welcome to come back!")

    #Control UI un-visible
    def funcMainWinUnvisible(self):
        self.cetk_debug_print("L4MAIN: Main form hide!")
        if self.isVisible():
            self.hide()
    
    #自己制造的结束函数，代替qApp.quit()方式，目的是为了菜单上的退出函数的截获，从而可以做一些硬件清理的事            
    def quit(self):
        self.close()

    def about(self):
        self.cetk_debug_print("版权所有：上海小慧智能科技有限公司, 上海纳贤路800号，科海大厦3楼")

    #需要捕获关闭界面的事件，然后将其通知给所有的其它任务，关闭硬件设备，然后再行退出主界面
    def closeEvent(self, event):
        self.TkMainUi.func_ui_click_main_prog_exit();
        time.sleep(1)
        self.close()


















