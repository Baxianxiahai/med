'''
Created on 2018/4/29

@author: hitpony
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

#Form class
from form_qt.cebsmainform import Ui_cebsMainWindow
from form_qt.cebscalibform import Ui_cebsCalibForm
from form_qt.cebsgparform import Ui_cebsGparForm
from form_qt.cebsmengform import Ui_cebsMengForm
from form_qt.cebsstestform import Ui_cebsStestForm
from form_qt.cebsBroswerForm import Ui_BroswerForm

#Local Class
from PkgVmHandler.ModVmLayer import *
from PkgCebsHandler.ModCebsCom import *
from PkgCebsHandler.ModCebsCom import *
from PkgCebsHandler.ModCebsCfg import *








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
        self.instL4CalibForm = SEUI_L4_CalibForm(self.TkCalibUi)
        self.instL4GparForm = SEUI_L4_GparForm(self.TkGparUi)
        self.instL4MengForm = SEUI_L4_MengForm(self.TkMengUi)
        self.instL4StestForm = SEUI_L4_StestForm(self.TkStestUi)
        #self.instL4BroserForm=SEUI_L4_BroswerForm(self.TkBrowUi)
        
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







#第二主入口
#Calibration Widget
class SEUI_L4_CalibForm(QtWidgets.QWidget, Ui_cebsCalibForm, clsL1_ConfigOpr):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()
    sgL4CalibFormActiveTrig = pyqtSignal()

    def __init__(self, TaskInstCalibUi):    
        super(SEUI_L4_CalibForm, self).__init__()
        #CASE1: UI PART
        self.setupUi(self)

        #CASE2: WORKING TASK
        self.TkCalibUi = TaskInstCalibUi
        #使用传递指针的方式
        self.TkCalibUi.funcSaveFatherInst(self)
        
        #CASE3: INTI PARAMETERS
        self.initParameter()
    
    def initParameter(self):
        #载入缺省图像
        self.calibRect = self.label_calib_RtCam_Fill.geometry()
        if (os.path.exists('calibInitWorm.jpg') == True):
            self.filePicInit = QtGui.QPixmap('calibInitWorm.jpg').scaled(self.calibRect.width(), self.calibRect.height())
            self.label_calib_RtCam_Fill.setPixmap(self.filePicInit)
        
    def cetk_debug_print(self, info):
        time.sleep(0.01)
        strOut = ">> " + str(time.asctime()) + " " + str(info);
        self.textEdit_calib_runProgress.append(strOut);
        self.textEdit_calib_runProgress.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_calib_runProgress.ensureCursorVisible()
        self.textEdit_calib_runProgress.insertPlainText("")       
    
    #界面的二次进入触发事件
    def switchOn(self):
        print("I am CALIB and enter again!")
    
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
        self.TkCalibUi.func_ui_click_pilot_mv(parMoveScale, "UP");
        
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
        self.TkCalibUi.func_ui_click_pilot_mv(parMoveScale, "DOWN");
        
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
        self.TkCalibUi.func_ui_click_pilot_mv(parMoveScale, "LEFT");
        
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
        self.TkCalibUi.func_ui_click_pilot_mv(parMoveScale, "RIGHT");
        
        
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
        self.TkCalibUi.func_ui_click_right_up_set();
    
    def slot_calib_left_down(self):
        self.TkCalibUi.func_ui_click_left_down_set();
    
    def slot_calib_pilot_start(self):
        self.TkCalibUi.func_ui_click_pilot_start();

    def slot_calib_pilot_stop(self):
        self.TkCalibUi.func_ui_click_pilot_stop();

    def slot_calib_pilot_move_0(self):
        self.TkCalibUi.func_ui_click_pilot_move_0();

    def slot_calib_pilot_move_n(self):
        try:
            holeNbr = int(self.lineEdit_pilot_move_n.text())
        except Exception: 
            holeNbr = 1;
        self.TkCalibUi.func_ui_click_pilot_move_n(holeNbr);
    
    #CAMERA ENABLE: Not support any more!
#     def slot_calib_pilot_camera_enable(self):
#         self.instL3CalibProc.funcCalibPilotCameraEnable();

    #CAMERA CAPTURE: new function support
    def slot_calib_pilot_camera_cap(self):
        try:
            holeNbr = int(self.lineEdit_pilot_move_n.text())
        except Exception: 
            holeNbr = 1;        
        self.TkCalibUi.func_ui_click_cap_pic_by_hole(holeNbr);

    def slot_calib_fm_up(self):
        self.TkCalibUi.func_ui_click_force_move('UP');
    
    def slot_calib_fm_down(self):
        self.TkCalibUi.func_ui_click_force_move('DOWN');

    def slot_calib_fm_left(self):
        self.TkCalibUi.func_ui_click_force_move('LEFT');

    def slot_calib_fm_right(self):
        self.TkCalibUi.func_ui_click_force_move('RIGHT');
    
    def slot_calib_close(self):
        self.close()

    def closeEvent(self, event):
        self.TkCalibUi.func_ui_click_calib_close()
        self.TkCalibUi.func_ui_click_calib_switch_to_main()
        self.sgL4MainWinVisible.emit()
        self.close()

    def cetk_calib_disp_cam(self, fileName):
        if (os.path.exists(fileName) == True):
            temp_pixmap = QtGui.QPixmap(fileName).scaled(self.calibRect.width(), self.calibRect.height())
            self.label_calib_RtCam_Fill.setPixmap(temp_pixmap)

    def cetk_calib_disp_cam_by_obj(self, picObj):
        self.label_calib_RtCam_Fill.setPixmap(picObj.scaled(self.calibRect.width(), self.calibRect.height()))





'''
#
#3rd Main Entry, 第三主入口
#Calibration Widget
#
# 参数需要在INI文件、内存全局变量GLVIS_PAR_OFC，界面呈现之间保持同步
# 本模块设计的逻辑是
# 1) 系统启动的时候，由PrjEntry将参数从ini文件读取到GLVIS_PAR_OFC全局内存中
# 2) 然后在GPAR初始化时，将去全局变量读取到界面中
# 3) 如果界面参数有效改变了，则需要先更新到内存全局变量OFC，然后写到ini文件中
# 4) 如果界面参数无效改变了，则不要求更新内存全局变量OFC，且将该参数传递到VISION模块中，防止中间的临时过程污染VISION后续处理
# 5) GPAR界面二次进入时，需要重新装载全局变量到界面上，确保上次的操作（完成存储、放弃参数）是可靠的
#
'''
class SEUI_L4_GparForm(QtWidgets.QWidget, Ui_cebsGparForm, clsL1_ConfigOpr):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()

    def __init__(self, TaskInstGparUi):    
        super(SEUI_L4_GparForm, self).__init__()
        #CASE1: UI PART
        self.setupUi(self)

        #CASE2: WORKING TASK
        #使用传递指针的方式
        self.TkGparUi = TaskInstGparUi
        self.TkGparUi.funcSaveFatherInst(self)
        
        #CASE3: INTI PARAMETERS
        self.initParameter()
        
        #Update UI interface last time parameter setting
    def initParameter(self):
        self.func_read_par_from_com_and_set2ui()
        #将参数传递给业务模块
        self.rectOrg = self.label_gpar_pic_origin_fill.geometry()
        self.rectCfy = self.label_gpar_pic_cfy_fill.geometry()
        self.TkGparUi.funcGparInitBascPar(self.rectOrg.width(), self.rectOrg.height(), self.rectCfy.width(), self.rectCfy.height())
        self.picOrgFile = ''
        #一定要清理掉原始图像，防止二次操作时误操作
        self.label_gpar_pic_origin_fill.clear()
        self.label_gpar_pic_cfy_fill.clear()
        self.lineEdit_gpar_pic_file_load.clear()

    def cetk_debug_print(self, info):
        time.sleep(0.01)
        strOut = ">> " + str(time.asctime()) + " " + str(info);
        self.textEdit_gpar_cmd_log.append(strOut);
        self.textEdit_gpar_cmd_log.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_gpar_cmd_log.ensureCursorVisible()
        self.textEdit_gpar_cmd_log.insertPlainText("")
    
    #增加一个切换后重新更新参数的函数，不然在放弃的时候，无效参数设置还处于激活状态
    def switchOn(self):
        self.initParameter()
    
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
        self.lineEdit_gpar_pic_file_load.setText(str(fileName))
        #将文件导入到目标框中
        if (fileName != ''):
            self.picOrgFile = fileName
            img = QtGui.QPixmap(fileName)
            img=img.scaled(self.rectOrg.width(), self.rectOrg.height())
            self.label_gpar_pic_origin_fill.setPixmap(img)

    #使用临时参数进行识别
    def slot_gpar_pic_train(self):
        if (self.picOrgFile == ''):
            return;
        l1, l2, l3, l4, add, g1, g2, g3, g4 = self.func_read_vis_train_par()
        self.TkGparUi.func_ui_click_pic_train(self.picOrgFile, l1, l2, l3, l4, add, g1, g2, g3, g4)
    
    def gpar_callback_train_resp(self, fileName):
        img = QtGui.QPixmap(fileName)
        img=img.scaled(self.rectCfy.width(), self.rectCfy.height())
        self.label_gpar_pic_cfy_fill.setPixmap(img)

    #使用临时参数进行识别
    def slot_gpar_flu_cell_cnt(self):
        if (self.picOrgFile == ''):
            return;
        l1, l2, l3, l4, add, g1, g2, g3, g4 = self.func_read_vis_train_par()
        self.TkGparUi.func_ui_click_gpar_flu_cell_cnt(self.picOrgFile, l1, l2, l3, l4, add, g1, g2, g3, g4);
        
    #
    #  SERVICE FUNCTION PART, 业务函数部分
    #
    #
    #Local function
    #读取到UI界面上
    def func_read_par_from_com_and_set2ui(self):
        self.checkBox_gpar_picFixPos.setChecked(ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET)
        self.checkBox_gpar_autoIdf.setChecked(ModCebsCom.GLVIS_PAR_OFC.PIC_CLASSIFIED_AFTER_TAKE_SET)
        self.checkBox_gpar_autoPic.setChecked(ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_AFTER_START_SET)
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
        #通用系数部分
        self.lineEdit_gpar_vision_coef1.setText(str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR1))
        self.lineEdit_gpar_vision_coef2.setText(str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR2))
        self.lineEdit_gpar_vision_coef3.setText(str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR3))
        self.lineEdit_gpar_vision_coef4.setText(str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR4))
    
    #读取界面上的参数并写入到INI配置文件
    def func_update_par_and_write_ini(self):
        #SAVE INTO COM VAR
        GLVIS_PAR_OFC.SMALL_LOW_LIMIT, GLVIS_PAR_OFC.SMALL_MID_LIMIT, GLVIS_PAR_OFC.MID_BIG_LIMIT, GLVIS_PAR_OFC.BIG_UPPER_LIMIT, \
            GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET, GLVIS_PAR_OFC.CFY_THD_GENR_PAR1, GLVIS_PAR_OFC.CFY_THD_GENR_PAR2, GLVIS_PAR_OFC.CFY_THD_GENR_PAR3,\
            GLVIS_PAR_OFC.CFY_THD_GENR_PAR4 = self.func_read_vis_train_par();
        #其它静态部分参数
        GLVIS_PAR_OFC.PIC_CLASSIFIED_AFTER_TAKE_SET = self.checkBox_gpar_autoIdf.isChecked();
        GLVIS_PAR_OFC.PIC_AUTO_WORKING_AFTER_START_SET = self.checkBox_gpar_autoPic.isChecked();
        GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET = self.checkBox_gpar_picFixPos.isChecked();
        try: 
            GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN = int(self.lineEdit_gpar_picTti.text());
        except Exception: 
            GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN = 60;
        GLVIS_PAR_OFC.saveCapEnable(self.checkBox_gpar_video_enable.isChecked())
        try: 
            GLVIS_PAR_OFC.saveCapDur(int(self.lineEdit_gpar_video_input.text()))
        except Exception: 
            GLVIS_PAR_OFC.saveCapDur(3)
        #HB-TYPE SELECTION
        radioGparHts96 = self.radioButton_gpar_bts_96.isChecked();
        radioGparHts48 = self.radioButton_gpar_bts_48.isChecked();
        radioGparHts24 = self.radioButton_gpar_bts_24.isChecked();
        radioGparHts12 = self.radioButton_gpar_bts_12.isChecked();
        radioGparHts6 = self.radioButton_gpar_bts_6.isChecked();
        #托盘型号
        option = 0;
        if (radioGparHts96 == 1): option = 96
        elif (radioGparHts48 == 1): option = 48
        elif (radioGparHts24 == 1): option = 24
        elif (radioGparHts12 == 1): option = 12
        elif (radioGparHts6 == 1): option = 6
        else: option = 6
        GLPLT_PAR_OFC.med_select_plate_board_type(option)
        #FINAL UPDATE
        self.updateStaticSectionEnvPar()

    #读取核心训练参数
    def func_read_vis_train_par(self):
        liPar1=200
        try: 
            liPar1 = int(self.lineEdit_gpar_vision_small_low_limit.text())
        except Exception: 
            pass
        liPar2=500
        try: 
            liPar2 = int(self.lineEdit_gpar_vision_small_mid_limit.text())
        except Exception: 
            pass
        liPar3=2000
        try: 
            liPar3 = int(self.lineEdit_gpar_vision_mid_big_limit.text())
        except Exception: 
            pass
        liPar4=5000
        try: 
            liPar4 = int(self.lineEdit_gpar_vision_big_upper_limit.text())
        except Exception: 
            pass
        addupSet = self.checkBox_gpar_vision_res_addup.isChecked()
        #通用参数部分
        gePar1 = 1
        try: 
            gePar1 = int(self.lineEdit_gpar_vision_coef1.text())
        except Exception: 
            pass
        gePar2 = 1
        try: 
            gePar2 = int(self.lineEdit_gpar_vision_coef2.text())
        except Exception: 
            pass
        gePar3 = 1
        try: 
            gePar3 = int(self.lineEdit_gpar_vision_coef3.text())
        except Exception: 
            pass
        gePar4 = 1
        try: 
            gePar4 = int(self.lineEdit_gpar_vision_coef4.text())
        except Exception: 
            pass
        #RETURN
        return liPar1, liPar2, liPar3, liPar4, addupSet, gePar1, gePar2, gePar3, gePar4


    #
    #  SLOT FUNCTION, 槽函数部分
    #    DO NOT MODIFY FUNCTION NAMES, 以下部分为系统接口对应的槽函数，函数命名不得动
    #    compl和giveup函数必须将释放mutex的动作放在closeEvent中统一完成，不然会造成完不成的情况
    #
    #    
    def slot_gpar_compl(self):
        self.func_update_par_and_write_ini()
        self.close()

    #Clear the command log text box
    def slot_gpar_clear(self):
        self.textEdit_gpar_cmd_log.clear();  
              
    #Give up and not save parameters
    def slot_gpar_giveup(self):
        self.close()

    #Give up and not save parameters
    def closeEvent(self, event):
        #必须将参数的更新放在这个地方：如果是存储，则将最终的参数传进去，如果是放弃，则将系统缺省参数传进去
        self.TkGparUi.func_ui_click_gpar_refresh_par()
        #关闭钩子
        self.TkGparUi.func_ui_click_gpar_close()
        #关闭切换界面钩子
        self.TkGparUi.func_ui_click_gpar_switch_to_main()
        #QT本身的界面切换
        self.sgL4MainWinVisible.emit()
        self.close()



#4th Main Entry, 第四主入口
#Meng Widget
class SEUI_L4_MengForm(QtWidgets.QWidget, Ui_cebsMengForm, clsL1_ConfigOpr):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()

    def __init__(self, TaskInstMengUi):    
        super(SEUI_L4_MengForm, self).__init__()
        #CASE1: 
        self.setupUi(self)

        #CASE2: 
        self.TkMengUi = TaskInstMengUi
        #使用传递指针的方式
        self.TkMengUi.funcSaveFatherInst(self)
        
        #CASE3: 
        self.initParameter()
    
    def initParameter(self):
        pass        

    def cetk_debug_print(self, info):
        time.sleep(0.01)
        strOut = ">> " + str(time.asctime()) + " " + str(info);
        self.textEdit_meng_trace_log.append(strOut);
        self.textEdit_meng_trace_log.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_meng_trace_log.ensureCursorVisible()
        self.textEdit_meng_trace_log.insertPlainText("")
        
    #界面的二次进入触发事件
    def switchOn(self):
        print("I am MENG and enter again!")
        
    #
    #  SLOT FUNCTION, 槽函数部分
    #    DO NOT MODIFY FUNCTION NAMES, 以下部分为系统接口对应的槽函数，函数命名不得动
    #
    #    
    #Send the command out
    def slot_meng_cmd_send(self):
        text_list = self.listWidget_meng_cmd.selectedItems()
        text = [i.text() for i in list(text_list)]
        if (text == []):
            return
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
        elif (str(text).find(ModCebsCom.GLSPS_PAR_OFC.SPS_SET_EXTI_DELAY_TIME) > 0):
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
                       
        #self.cetk_debug_print("MENG: Cmd = %d, Par1/2/3/4=%d/%d/%d/%d" % (cmd, par1, par2, par3, par4))
        self.TkMengUi.func_ui_click_send_command(cmd, par1, par2, par3, par4)
        self.lineEdit_meng_cmd_par.setText("")
    
    #给TkMengUi回调的处理过程
    def meng_callback_cmd_exec_fb(self, res):
        self.lineEdit_meng_cmd_par.setText(str(res))
        
    #Clear the command log text box
    def slot_meng_trace_clear(self):
        self.textEdit_meng_trace_log.clear();

    def slot_meng_compl(self):
        self.close()

    #Give up and not save parameters
    def slot_meng_giveup(self):
        self.close()

    #Give up and not save parameters
    def closeEvent(self, event):
        self.TkMengUi.func_ui_click_meng_close()
        self.TkMengUi.func_ui_click_meng_switch_to_main()
        self.sgL4MainWinVisible.emit()
        self.close()
        

        
#5th Main Entry, 第五主入口
#Stest Widget
class SEUI_L4_StestForm(QtWidgets.QWidget, Ui_cebsStestForm, clsL1_ConfigOpr):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()

    def __init__(self, TaskInstStestUi):    
        super(SEUI_L4_StestForm, self).__init__()
        #CASE1: 
        self.setupUi(self)
        #CASE2: 
        self.TkStestUi = TaskInstStestUi
        #使用传递指针的方式
        self.TkStestUi.funcSaveFatherInst(self)
        #CASE3: 
        self.initParameter()
    
    def initParameter(self):
        pass        

    def cetk_debug_print(self, info):
        time.sleep(0.01)
        strOut = ">> " + str(time.asctime()) + " " + str(info);
        self.textEdit_Stest_Trace_log.append(strOut);
        self.textEdit_Stest_Trace_log.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_Stest_Trace_log.ensureCursorVisible()
        self.textEdit_Stest_Trace_log.insertPlainText("")
        
    #界面的二次进入触发事件
    def switchOn(self):
        print("I am Stest and enter again!")
        
    #
    #  SLOT FUNCTION, 槽函数部分
    #    DO NOT MODIFY FUNCTION NAMES, 以下部分为系统接口对应的槽函数，函数命名不得动
    #
    #               
    def slot_stest_start(self):
        self.TkStestUi.func_ui_click_stest_self_test_start()

    def slot_stest_stop(self):
        self.TkStestUi.func_ui_click_stest_self_test_stop()

    def stest_callback_fetch_moto_status(self, spsOpen, motoX, motoY):
        if (spsOpen > 0):
            self.checkBox_Stest_serial.setChecked(True)
        else:
            self.checkBox_Stest_serial.setChecked(False)
        if (motoX > 0):
            self.checkBox_Stest_moto_x.setChecked(True)
        else:
            self.checkBox_Stest_moto_x.setChecked(False)
        if (motoY > 0):
            self.checkBox_Stest_moto_y.setChecked(True)
        else:
            self.checkBox_Stest_moto_y.setChecked(False)
        return;

    def stest_callback_fetch_cam_status(self, camOpen):
        if (camOpen > 0):
            self.checkBox_Stest_camera.setChecked(True)
        else:
            self.checkBox_Stest_camera.setChecked(False)
        return;

    def stest_callback_fetch_calib_status(self, calibStatus):
        if (calibStatus > 0):
            self.checkBox_Stest_calib.setChecked(True)
        else:
            self.checkBox_Stest_calib.setChecked(False)
        return;

    def stest_callback_fetch_ctrl_schd_status(self, picBat, cfyPicBat, cfyFlubat, cfyPicRemCnt, cfyFluRemCnt, hbType):
        self.lineEdit_Stest_batch_nbr.setText(str(picBat))
        self.lineEdit_Stest_batch_cfy_pic.setText(str(cfyPicBat))
        self.lineEdit_Stest_batch_cfy_flu.setText(str(cfyFlubat))
        self.lineEdit_Stest_cfy_pic_rem_cnt.setText(str(cfyPicRemCnt))
        self.lineEdit_Stest_cfy_flu_rem_cnt.setText(str(cfyFluRemCnt))
        self.lineEdit_Stest_hb.setText(str(hbType))
        return;

    def slot_stest_clear(self):
        self.textEdit_Stest_Trace_log.clear();

    def slot_stest_compl(self):
        self.close()

    #Give up and not save parameters
    def closeEvent(self, event):
        self.TkStestUi.func_ui_click_stest_close()
        self.TkStestUi.func_ui_click_stest_switch_to_main()
        self.sgL4MainWinVisible.emit()
        self.close()



#6th Main Entry, 第六主入口
#Broswer Widget
class SEUI_L4_BroswerForm(QtWidgets.QMainWindow, Ui_BroswerForm, clsL1_ConfigOpr):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()
    def __init__(self, TaskInstBrowUi):
        super(SEUI_L4_BroswerForm, self).__init__()
        self.TkBrowUi = TaskInstBrowUi
        self.setupUi(self)
        self.openBroswer()
        
    def openBroswer(self):
        print("[CEBS]  Open Browser is Start")
        config=clsL1_ConfigOpr()
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
    
    #界面的二次进入触发事件
    def switchOn(self):
        print("I am BROWSE and enter again!")

    def closeEvent(self, event):
        config = clsL1_ConfigOpr()
        config.SetDishRowandColumn()
        self.sgL4MainWinVisible.emit()
        self.close()










        
'''
'高级技巧，还未搞定'
'https://www.cnblogs.com/WSX1994/articles/9092331.html'

探索使得加载更加人性化和自动化
'''
def cetk_start_app():
    app = QtWidgets.QApplication(sys.argv)
    splash = cetk_show_startup_pic()
    return app, splash

def cetk_load_data(sp):
    for i in range(1, 2):              #模拟主程序加载过程 
        time.sleep(1)                   # 加载数据
        sp.showMessage("加载... {0}%".format(i * 10), QtCore.Qt.AlignHCenter |QtCore.Qt.AlignBottom, QtCore.Qt.black)
        QtWidgets.qApp.processEvents()  # 允许主进程处理事件

def cetk_show_startup_pic():
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("cebsStart.jpg"))
    splash.showMessage("加载...0%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    splash.resize(1202, 800)
    splash.show()
    cetk_load_data(splash)
    return splash    

def cetk_hide_startup_pic(splash):
    splash.hide()

def cetk_show_app(app, splash, TkMainUi, TkCalibUi, TkGparUi, TkMengUi, tkStestUi, TkBrowUi):
    QtWidgets.qApp.processEvents()
    mainWindow = SEUI_L4_MainWindow(TkMainUi, TkCalibUi, TkGparUi, TkMengUi, tkStestUi, TkBrowUi)
    mainWindow.show()
    cetk_hide_startup_pic(splash)
    #换用新机制，不然整个应用程序退出不成功
    app.exec_()
    return    

#THE MAIN ENTRY: 第0主入口，MAIN函数部分
#这个是聚合部分，放在一起进行显示和启动
def cetk_l4ui_main_form_entry(TkMainUi, TkCalibUi, TkGparUi, TkMenUi):
    app = QtWidgets.QApplication(sys.argv)
    splash = cetk_show_startup_pic()
    QtWidgets.qApp.processEvents()
    mainWindow = SEUI_L4_MainWindow(TkMainUi, TkCalibUi, TkGparUi, TkMenUi)
    mainWindow.show()
    cetk_hide_startup_pic(splash)
    sys.exit(app.exec_())
    return
    
    