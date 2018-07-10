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
from form_qt.cebsmainform import Ui_cebsMainWindow    # 瀵煎叆鐢熸垚mainForm.py閲岀敓鎴愮殑绫�
from form_qt.cebscalibform import Ui_cebsCalibForm      # 瀵煎叆鐢熸垚calibForm.py閲岀敓鎴愮殑绫�

#Local Class
from PkgCebsHandler import ModCebsCom  #Common Support module
from PkgCebsHandler import ModCebsMoto
from PkgCebsHandler import ModCebsCtrl
from PkgCebsHandler import ModCebsVision
from PkgCebsHandler import ModCebsCfg
from PkgCebsHandler import ModCebsCalib

#Main Windows
class cebsMainWindow(QtWidgets.QMainWindow, Ui_cebsMainWindow):
    signal_mainwin_unvisible = pyqtSignal()  #鐢虫槑缁欎富鍑芥暟浣跨敤    
    
    def __init__(self):    
        super(cebsMainWindow, self).__init__()  
        self.setupUi(self)
        self.initUI()
        
        #蹇呴』浣跨敤鎴愬憳鍑芥暟锛屾墠鑳戒繚璇佸瓙FORM鐨勭敓鍛藉懆鏈�
        self.calibForm = cebsCalibForm()
        self.objMoto = ModCebsMoto.classMotoProcess();

        #鍥哄畾淇″彿閲忚缃�
        self.calibForm.signal_mainwin_visible.connect(self.funcMainWinVisible);
        self.signal_mainwin_unvisible.connect(self.funcMainWinUnvisible);
        
        #璇诲彇閰嶇疆鏂囦欢鍙傛暟
        objInitCfg=ModCebsCfg.ConfigOpr()
        objInitCfg.readGlobalPar();
        objInitCfg.updateCtrlCntInfo()
        
        #鍚姩绗竴涓共娲荤殑瀛愯繘绋�
        self.threadCtrl = ModCebsCtrl.classCtrlThread()
        self.threadCtrl.setIdentity("CtrlThread")
        self.threadCtrl.signal_print_log.connect(self.slot_print_trigger)  #鎺ユ敹淇″彿
        self.threadCtrl.signal_ctrl_start.connect(self.threadCtrl.funcTakePicStart) #鍙戦�佷俊鍙�
        self.threadCtrl.signal_ctrl_stop.connect(self.threadCtrl.funcTakePicStop)  #鍙戦�佷俊鍙�
        self.threadCtrl.signal_ctrl_clas_start.connect(self.threadCtrl.funcVisionClasStart) #鍙戦�佷俊鍙�
        self.threadCtrl.signal_ctrl_clas_stop.connect(self.threadCtrl.funcVisionClasStop)  #鍙戦�佷俊鍙�
        self.threadCtrl.signal_ctrl_calib_start.connect(self.threadCtrl.funcCtrlCalibStart) #鍙戦�佷俊鍙�
        self.threadCtrl.signal_ctrl_calib_stop.connect(self.threadCtrl.funcCtrlCalibStop)  #鍙戦�佷俊鍙�
        self.threadCtrl.signal_ctrl_zero.connect(self.threadCtrl.funcCtrlMotoBackZero)  #鍙戦�佷俊鍙�
        self.threadCtrl.start();

        #鍚姩绗簩涓共娲荤殑瀛愯繘绋�
        self.threadVision = ModCebsVision.classVisionThread()
        self.threadVision.setIdentity("VisionThread")
        self.threadVision.signal_print_log.connect(self.slot_print_trigger)
        self.threadVision.start();

        #鍒濆鍖栭厤缃�
        self.funcMainFormSetEquInitStatus();

    def initUI(self):
        self.statusBar().showMessage('鐘舵�佹爮: ')
        self.setGeometry(10, 30, 1024, 768)

        exitAction = QAction(QIcon('.\icon_res\q10.ico'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('閫�鍑哄簲鐢ㄧ▼搴�')
        exitAction.triggered.connect(qApp.quit)
        toolbar = self.addToolBar('EXIT')  
        toolbar.addAction(exitAction)

    def initParameter(self):
        pass

    #File Open Method, for reference
    def test_openMsg(self):  
        file, ok=QFileDialog.getOpenFileName(self,"鎵撳紑","C:/","All Files (*);;Text Files (*.txt)")  
        self.statusbar.showMessage(file)

    #鏍稿績鍑芥暟
    def cebs_print_log(self, info):
        strOld = self.textEdit_runProgress.toPlainText()
        #閲囩敤鍏ㄥ眬缂栬緫
        #strOut = strOld + "\n>> " + time.asctime() + " " + info;
        #self.textEdit_runProgress.setText(strOut);
        #閲囩敤姝ｅ父鐨刟ppend鏂规硶
        strOut = ">> " + time.asctime() + " " + info;
        self.textEdit_runProgress.append(strOut);
        self.textEdit_runProgress.moveCursor(QtGui.QTextCursor.End)
        #鍚庨潰涓や釜鎿嶄綔涓嶅鍔犱篃娌″暐澶ч棶棰橈紝浣嗙粰浜嗘垜浠洿澶氱殑鎿嶄綔绾跨储
        self.textEdit_runProgress.ensureCursorVisible()
        self.textEdit_runProgress.insertPlainText("")

    def slot_print_trigger(self, info):
        self.cebs_print_log(info)

    def slot_ctrl_start(self):
        self.cebs_print_log("MAIN: 鎷嶇収寮�濮嬶紒")
        #self.funcMainFormSetEquInitStatus();
        self.threadCtrl.signal_ctrl_start.emit()
        
    def slot_ctrl_stop(self):
        self.cebs_print_log("MAIN: 鎷嶇収鍋滄锛�")
        self.threadCtrl.signal_ctrl_stop.emit()

    def slot_ctrl_zero(self):
        #self.funcMainFormSetEquInitStatus();
        self.cebs_print_log("MAIN: 绯荤粺褰掗浂锛�")
        self.threadCtrl.signal_ctrl_zero.emit()

    def slot_ctrl_vclas_start(self):
        #self.funcMainFormSetEquInitStatus();
        self.cebs_print_log("MAIN: 鍚姩鍥惧儚璇嗗埆锛�")
        self.threadCtrl.signal_ctrl_clas_start.emit()

    def slot_ctrl_vclas_stop(self):
        self.cebs_print_log("MAIN: 鍋滄鍥惧儚璇嗗埆锛�")
        self.threadCtrl.signal_ctrl_clas_stop.emit()

    def slot_ctrl_calib(self):
        if (self.threadCtrl.funcCtrlGetRightStatus() < 0):
            self.cebs_print_log("MAIN: CALIB涓婁竴涓换鍔¤繕鏈畬鎴愶紒")
            return -1;
        #self.funcMainFormSetEquInitStatus();
        self.cebs_print_log("MAIN: 寮�濮嬫牎鍑嗭紒")
        self.threadCtrl.signal_ctrl_calib_start.emit()
        if not self.calibForm.isVisible():
            self.signal_mainwin_unvisible.emit()
            self.calibForm.show()

    def funcMainWinVisible(self):
        #鍐嶆墽琛岄�昏緫
        if not self.isVisible():
            self.show()
        #鍐嶅皢鐘舵�佹満鏀硅繃鏉�
        self.threadCtrl.signal_ctrl_calib_stop.emit()
        self.cebs_print_log("MAIN: 鏍″噯缁撴潫锛�")

    def funcMainWinUnvisible(self):
        if self.isVisible():
            self.hide()

    def slot_runpg_clear(self):
        self.textEdit_runProgress.clear();

    #Test functions
    def slot_runpg_test(self):
        res = {}
        self.cebs_print_log("TEST: " + str(res))

    #鏈潵鐢ㄤ簬寮哄埗鎺у埗锛岀幇鍦ㄦ湁浜咰TRL灞傞潰鐨勭姸鎬佹満涔嬪悗锛屾殏鏃朵笉鐢ㄤ簡銆�
    #寮哄埗鎺у埗鐨勫潖澶勯潪甯告槑鏄撅細鍔ㄤ綔閮ㄤ欢鍦ㄥ潖浜虹媯鐐归紶鏍囩殑鎯呭喌涓嬶紝鍙兘浼氶亣鍒版崯鍧�
    def funcMainFormSetEquInitStatus(self):
        self.objMoto.funcMotoStop() #鍋滄椹揪

#Calibration Widget
class cebsCalibForm(QtWidgets.QWidget, Ui_cebsCalibForm):
    signal_mainwin_visible = pyqtSignal() #鐢虫槑缁欎富鍑芥暟浣跨敤

    def __init__(self):    
        super(cebsCalibForm, self).__init__()  
        self.setupUi(self)
        #蹇呴』浣跨敤鎴愬憳鍑芥暟锛屾墠鑳戒繚璇佸瓙FORM鐨勭敓鍛藉懆鏈�
        self.calibProc = ModCebsCalib.classCalibProcess(self)
        
    #鏍″噯鎵撳嵃
    def calib_print_log(self, info):
        strOut = ">> " + time.asctime() + " " + info;
        self.textEdit_calib_runProgress.append(strOut);
        self.textEdit_calib_runProgress.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_calib_runProgress.ensureCursorVisible()
        self.textEdit_calib_runProgress.insertPlainText("")
        
    #鏍″噯绉诲姩
    def slot_calib_move(self):
        #璇诲彇杩愬姩鍒诲害
        radioCala05mm = self.radioButton_calib_05mm.isChecked();
        radioCala1mm = self.radioButton_calib_1mm.isChecked();
        radioCala5mm = self.radioButton_calib_5mm.isChecked();
        radioCala1cm = self.radioButton_calib_1cm.isChecked();
        radioCala5cm = self.radioButton_calib_5cm.isChecked();
        if (radioCala05mm == 1):
            parMoveScale = 1;
        elif (radioCala1mm == 1):
            parMoveScale = 2;
        elif (radioCala5mm == 1):
            parMoveScale = 3;
        elif (radioCala1cm == 1):
            parMoveScale = 4;
        elif (radioCala5cm == 1):
            parMoveScale = 5;
        else:
            parMoveScale = 1;
        #璇诲彇杩愬姩鏂瑰悜
        radioCalaUp = self.radioButton_calib_y_plus.isChecked();
        radioCalaDown = self.radioButton_calib_y_minus.isChecked();
        radioCalaLeft = self.radioButton_calib_x_minus.isChecked();
        radioCalaRight = self.radioButton_calib_x_plus.isChecked();
        if (radioCalaUp == 1):
            parMoveDir = 1;
        elif (radioCalaDown == 1):
            parMoveDir = 2;
        elif (radioCalaLeft == 1):
            parMoveDir = 3;
        elif (radioCalaRight == 1):
            parMoveDir = 4;
        else:
            parMoveDir = 1;
        self.calibProc.funcCalibMove(parMoveScale, parMoveDir);
    
    #鏍″噯宸︿笂
    def slot_calib_left_up(self):
        self.calibProc.funcCalibLeftUp();
    
    #鏍″噯鍙充笅
    def slot_calib_right_bottom(self):
        self.calibProc.funcCalibRightBottom();
    
    #鏍″噯宸℃父
    def slot_calib_pilot(self):
        self.calibProc.funcCalibPilotStart();

    #鏍″噯宸℃父鍋滄
    def slot_calib_pilot_stop(self):
        self.calibProc.funcCalibPilotStop();

    #鐣岄潰鎸夐挳缁撴潫
    def slot_calib_close(self):
        self.calibProc.funcCtrlCalibComp()
        self.signal_mainwin_visible.emit()
        self.close()

    #閲嶈浇绯荤粺鐨勫叧闂嚱鏁�
    def closeEvent(self, event):
        self.calibProc.funcRecoverWorkingEnv()
        self.signal_mainwin_visible.emit()
        self.close()

#Main App entry
def main_form():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = cebsMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

#SYSTEM ENTRY
if __name__ == '__main__':
    print("[CEBS] ", time.asctime(), ", System starting...\n" );
    main_form()
    
    
