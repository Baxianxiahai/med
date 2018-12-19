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
from form_qt.cebsBroswerForm import Ui_BroswerForm

#Local Class
from PkgVmHandler import ModVmCfg
from PkgVmHandler import ModVmLayer
from PkgCebsHandler import ModCebsCom  #Common Support module
from PkgCebsHandler import ModCebsCfg




'''
#SEUI => System Entry UI，表示系统级的主入口
第一主入口
Main Windows
'''
class SEUI_L4_MainWindow(QtWidgets.QMainWindow, Ui_cebsMainWindow, ModCebsCfg.clsL1_ConfigOpr):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()

    def __init__(self, TaskInstMainUi, TaskInstCalibUi, TaskInstGparUi, TaskInstMenUi, TaskInstBrowUi):    
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
        self.TkMenUi = TaskInstMenUi
        self.TkBrowUi = TaskInstBrowUi

        #CASE3: HARDWARE LEVEL INIT, 硬件初始化
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
#         #STEP1: INI FILE CONFIGURATION, 初始化配置文件
#         self.func_read_global_par_from_cfg_file();  #读取本地文件的配置数据，并写入全局变量中来
#         self.updateCtrlCntInfo() #更新进度控制参量

        #STEP2: START SUB-UI, 启动子界面        
        self.instL4CalibForm = SEUI_L4_CalibForm(self.TkCalibUi)
        self.instL4GparForm = SEUI_L4_GparForm(self.TkGparUi)
        self.instL4MengForm = SEUI_L4_MengForm(self.TkMenUi)
        #self.instL4BroserForm=SEUI_L4_BroswerForm(self.TkBrowUi)
        
        #STEP3: CONNECT SIGNAL SLOT, 连接信号槽
        self.sgL4MainWinUnvisible.connect(self.funcMainWinUnvisible);
        self.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        self.instL4CalibForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        self.instL4GparForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        self.instL4MengForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        #self.instL4BroserForm.sgL4MainWinVisible.connect(self.funcMainWinVisible);
        
        #STEP4: 使用传递指针的方式
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

    #Enter parameter setting session
    def slot_gpar_start(self):
        self.cetk_debug_print("L4MAIN: Global parameter set start......")
        if not self.instL4GparForm.isVisible():
            self.TkMainUi.func_ui_click_gpar_start();
            self.sgL4MainWinUnvisible.emit()
            self.instL4GparForm.show()

    #Enter Moto Engineering Mode
    def slot_meng_sel(self):
        self.cetk_debug_print("L4MAIN: Moto Engineering start......")
        if not self.instL4MengForm.isVisible():
            self.TkMainUi.func_ui_click_meng_start();
            self.sgL4MainWinUnvisible.emit()
            self.instL4MengForm.show()

    #Enter Selection Active Hole Target Mode
    def slot_saht_sel(self):
        self.cetk_debug_print("L4MAIN: Active Hole Selection start......")
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



#第二主入口
#Calibration Widget
class SEUI_L4_CalibForm(QtWidgets.QWidget, Ui_cebsCalibForm, ModCebsCfg.clsL1_ConfigOpr):
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
#         try:
#             self.instL3CalibProc.funcCtrlCalibComp()
#         except Exception:
#             self.instL1ConfigOpr1.medErrorLog("L4CALIBMAIN: Execute instL3CalibProc.funcCtrlCalibComp() get error feedback.")
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

#3rd Main Entry, 第三主入口
#Calibration Widget
class SEUI_L4_GparForm(QtWidgets.QWidget, Ui_cebsGparForm, ModCebsCfg.clsL1_ConfigOpr):
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
        self.funcGlobalParReadSet2Ui()
        #将参数传递给业务模块
        self.rectOrg = self.label_gpar_pic_origin_fill.geometry()
        self.rectCfy = self.label_gpar_pic_cfy_fill.geometry()
        self.TkGparUi.funcGparInitBascPar(self.rectOrg.width(), self.rectOrg.height(), self.rectCfy.width(), self.rectCfy.height())
        self.picOrgFile = ''       

    def cetk_debug_print(self, info):
        time.sleep(0.01)
        strOut = ">> " + str(time.asctime()) + " " + str(info);
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
            self.picOrgFile = fileName
            img = QtGui.QPixmap(fileName)
            img=img.scaled(self.rectOrg.width(), self.rectOrg.height())
            self.label_gpar_pic_origin_fill.setPixmap(img)

    def slot_gpar_pic_train(self):
        if (self.picOrgFile == ''):
            return;
        #Firstly read parameter into classified variable sets, to let Train Func use.
        self.funcReadVisParToCfySets();    #获取SAV
        #在训练之前，需要将系统参数保存在临时变量中，借助于全局变量的传递，进行算法训练。一旦完成，还要再回写。
        savetmp = ModCebsCom.GLVIS_PAR_SAV   #将SAV值传给临时变量
        ModCebsCom.GLVIS_PAR_OFC = ModCebsCom.GLVIS_PAR_SAV   #将SAV值传给OFC
        self.TkGparUi.func_ui_click_pic_train(self.picOrgFile)
        ModCebsCom.GLVIS_PAR_OFC = savetmp                  #SAV给OFC
    
    def gpar_callback_train_resp(self, fileName):
        img = QtGui.QPixmap(fileName)
        img=img.scaled(self.rectCfy.width(), self.rectCfy.height())
        self.label_gpar_pic_cfy_fill.setPixmap(img)
        
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
            ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN = int(self.lineEdit_gpar_picTti.text());
        except Exception: 
            ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN = 60;
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
        self.updateStaticSectionEnvPar()

    #Using global parameter set to UI during launch
    def funcGlobalParReadSet2Ui(self):
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
        self.TkGparUi.func_ui_click_gpar_refresh_par()
        self.close()

    #Clear the command log text box
    def slot_gpar_clear(self):
        self.textEdit_gpar_cmd_log.clear();  
              
    #Give up and not save parameters
    def slot_gpar_giveup(self):
        self.close()

    #Give up and not save parameters
    def closeEvent(self, event):
        self.TkGparUi.func_ui_click_gpar_close()
        self.TkGparUi.func_ui_click_gpar_switch_to_main()
        self.sgL4MainWinVisible.emit()
        self.close()


#4rd Main Entry, 第四主入口
#Meng Widget
class SEUI_L4_MengForm(QtWidgets.QWidget, Ui_cebsMengForm, ModCebsCfg.clsL1_ConfigOpr):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()

    def __init__(self, TaskInstGparUi):    
        super(SEUI_L4_MengForm, self).__init__()
        #CASE1: 
        self.setupUi(self)

        #CASE2: 
        self.TkMengUi = TaskInstGparUi
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
        
class SEUI_L4_BroswerForm(QtWidgets.QMainWindow, Ui_BroswerForm, ModCebsCfg.clsL1_ConfigOpr):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()
    def __init__(self, TaskInstBrowUi):
        super(SEUI_L4_BroswerForm, self).__init__()
        self.TkBrowUi = TaskInstBrowUi
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

def cetk_show_app(app, splash, TkMainUi, TkCalibUi, TkGparUi, TkMenUi, TkBrowUi):
    QtWidgets.qApp.processEvents()
    mainWindow = SEUI_L4_MainWindow(TkMainUi, TkCalibUi, TkGparUi, TkMenUi, TkBrowUi)
    mainWindow.show()
    cetk_hide_startup_pic(splash)
    sys.exit(app.exec_())
    print("Main App done!")
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
    print("Main App done!")
    return
    
    