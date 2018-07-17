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
from form_qt.cebsmainform import Ui_cebsMainWindow
from form_qt.cebscalibform import Ui_cebsCalibForm

#Local Class
from PkgCebsHandler import ModCebsCom  #Common Support module
from PkgCebsHandler import ModCebsMoto
from PkgCebsHandler import ModCebsCtrl
from PkgCebsHandler import ModCebsVision
from PkgCebsHandler import ModCebsCfg
from PkgCebsHandler import ModCebsCalib

#Main Windows
class cebsMainWindow(QtWidgets.QMainWindow, Ui_cebsMainWindow):
    signal_mainwin_unvisible = pyqtSignal()
    
    def __init__(self):    
        super(cebsMainWindow, self).__init__()  
        self.setupUi(self)
        self.initUI()
        
        self.calibForm = cebsCalibForm()
        self.objMoto = ModCebsMoto.classMotoProcess();

        self.calibForm.signal_mainwin_visible.connect(self.funcMainWinVisible);
        self.signal_mainwin_unvisible.connect(self.funcMainWinUnvisible);
        
        objInitCfg=ModCebsCfg.ConfigOpr()
        objInitCfg.readGlobalPar();
        objInitCfg.updateCtrlCntInfo()
        
        self.threadCtrl = ModCebsCtrl.classCtrlThread()
        self.threadCtrl.setIdentity("CtrlThread")
        self.threadCtrl.signal_print_log.connect(self.slot_print_trigger)
        self.threadCtrl.signal_ctrl_start.connect(self.threadCtrl.funcTakePicStart)
        self.threadCtrl.signal_ctrl_stop.connect(self.threadCtrl.funcTakePicStop)
        self.threadCtrl.signal_ctrl_clas_start.connect(self.threadCtrl.funcVisionClasStart)
        self.threadCtrl.signal_ctrl_clas_stop.connect(self.threadCtrl.funcVisionClasStop)
        self.threadCtrl.signal_ctrl_calib_start.connect(self.threadCtrl.funcCtrlCalibStart)
        self.threadCtrl.signal_ctrl_calib_stop.connect(self.threadCtrl.funcCtrlCalibStop)
        self.threadCtrl.signal_ctrl_zero.connect(self.threadCtrl.funcCtrlMotoBackZero)
        self.threadCtrl.start();

        self.threadVision = ModCebsVision.classVisionThread()
        self.threadVision.setIdentity("VisionThread")
        self.threadVision.signal_print_log.connect(self.slot_print_trigger)
        self.threadVision.start();

        self.funcMainFormSetEquInitStatus();

    def initUI(self):
        self.statusBar().showMessage('SYSTEM START: ')
        self.setGeometry(10, 30, 1024, 768)

        exitAction = QAction(QIcon('.\icon_res\q10.ico'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('EXIT SYSTEM')
        exitAction.triggered.connect(qApp.quit)
        toolbar = self.addToolBar('EXIT')  
        toolbar.addAction(exitAction)

    def initParameter(self):
        pass

    #File Open Method, for reference
    def test_openMsg(self):  
        file, ok=QFileDialog.getOpenFileName(self,"OPEN FILE","C:/","All Files (*);;Text Files (*.txt)")  
        self.statusbar.showMessage(file)

    def cebs_print_log(self, info):
        strOld = self.textEdit_runProgress.toPlainText()
        #strOut = strOld + "\n>> " + time.asctime() + " " + info;
        #self.textEdit_runProgress.setText(strOut);
        strOut = ">> " + time.asctime() + " " + info;
        self.textEdit_runProgress.append(strOut);
        self.textEdit_runProgress.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_runProgress.ensureCursorVisible()
        self.textEdit_runProgress.insertPlainText("")

    def slot_print_trigger(self, info):
        self.cebs_print_log(info)

    def slot_ctrl_start(self):
        self.cebs_print_log("MAIN: START...")
        #self.funcMainFormSetEquInitStatus();
        self.threadCtrl.signal_ctrl_start.emit()
        
    def slot_ctrl_stop(self):
        self.cebs_print_log("MAIN: STOP!")
        self.threadCtrl.signal_ctrl_stop.emit()

    def slot_ctrl_zero(self):
        #self.funcMainFormSetEquInitStatus();
        self.cebs_print_log("MAIN: RUN TO ZERO!")
        self.threadCtrl.signal_ctrl_zero.emit()

    def slot_ctrl_vclas_start(self):
        #self.funcMainFormSetEquInitStatus();
        self.cebs_print_log("MAIN: PIC IDENTIFY START")
        self.threadCtrl.signal_ctrl_clas_start.emit()

    def slot_ctrl_vclas_stop(self):
        self.cebs_print_log("MAIN: PIC IDENTIFY STOP")
        self.threadCtrl.signal_ctrl_clas_stop.emit()

    def slot_ctrl_calib(self):
        if (self.threadCtrl.funcCtrlGetRightStatus() < 0):
            self.cebs_print_log("MAIN: CALIB ERROR1!")
            return -1;
        #self.funcMainFormSetEquInitStatus();
        self.cebs_print_log("MAIN: CALIB ACTION!")
        self.threadCtrl.signal_ctrl_calib_start.emit()
        if not self.calibForm.isVisible():
            self.signal_mainwin_unvisible.emit()
            self.calibForm.show()

    def funcMainWinVisible(self):
        if not self.isVisible():
            self.show()
        self.threadCtrl.signal_ctrl_calib_stop.emit()
        self.cebs_print_log("MAIN: CALIB UI CHANGED!")

    def funcMainWinUnvisible(self):
        if self.isVisible():
            self.hide()

    def slot_runpg_clear(self):
        self.textEdit_runProgress.clear();

    #Test functions
    def slot_runpg_test(self):
        res = {}
        self.cebs_print_log("TEST: " + str(res))

    def funcMainFormSetEquInitStatus(self):
        self.objMoto.funcMotoStop()

#Calibration Widget
class cebsCalibForm(QtWidgets.QWidget, Ui_cebsCalibForm):
    signal_mainwin_visible = pyqtSignal()

    def __init__(self):    
        super(cebsCalibForm, self).__init__()  
        self.setupUi(self)
        self.calibProc = ModCebsCalib.classCalibProcess(self)
        
    def calib_print_log(self, info):
        strOut = ">> " + time.asctime() + " " + info;
        self.textEdit_calib_runProgress.append(strOut);
        self.textEdit_calib_runProgress.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_calib_runProgress.ensureCursorVisible()
        self.textEdit_calib_runProgress.insertPlainText("")
        
    def slot_calib_move(self):
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
    
    def slot_calib_left_up(self):
        self.calibProc.funcCalibLeftUp();
    
    def slot_calib_right_bottom(self):
        self.calibProc.funcCalibRightBottom();
    
    def slot_calib_pilot(self):
        self.calibProc.funcCalibPilotStart();

    def slot_calib_pilot_stop(self):
        self.calibProc.funcCalibPilotStop();

    def slot_calib_close(self):
        self.calibProc.funcCtrlCalibComp()
        self.signal_mainwin_visible.emit()
        self.close()

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
    
    
