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

#Main Windows
class cebsMainWindow(QtWidgets.QMainWindow, Ui_cebsMainWindow):
    signal_mainwin_unvisible = pyqtSignal()
    
    def __init__(self):    
        super(cebsMainWindow, self).__init__()  
        self.setupUi(self)
        self.initUI()
        
        #MUST Load global parameters, to initialize different UI and update the stored parameters.
        objInitCfg=ModCebsCfg.ConfigOpr()
        objInitCfg.readGlobalPar();
        objInitCfg.updateCtrlCntInfo()
        
        self.calibForm = cebsCalibForm()
        self.gparForm = cebsGparForm()
        self.objMoto = ModCebsMoto.classMotoProcess();

        self.calibForm.signal_mainwin_visible.connect(self.funcMainWinVisible);
        self.gparForm.signal_mainwin_visible.connect(self.funcMainWinVisible);
        self.signal_mainwin_unvisible.connect(self.funcMainWinUnvisible);
        
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

        #Detect all valid camera
        initObjVision = ModCebsVision.classVisionProcess();
        res = initObjVision.funcVisionDetectAllCamera()
        self.slot_print_trigger(res)

    def initUI(self):
        self.statusBar().showMessage('SYSTEM START ')
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

    #Start taking picture
    def slot_ctrl_start(self):
        self.cebs_print_log("MAIN: Taking Picture start...")
        self.threadCtrl.signal_ctrl_start.emit()
    
    #Stop taking picture
    def slot_ctrl_stop(self):
        self.cebs_print_log("MAIN: Taking Picture stop!")
        self.threadCtrl.signal_ctrl_stop.emit()

    #Control moto run to Zero position
    def slot_ctrl_zero(self):
        self.cebs_print_log("MAIN: RUN TO ZERO!")
        self.threadCtrl.signal_ctrl_zero.emit()

    #Start vision classification
    def slot_ctrl_vclas_start(self):
        self.cebs_print_log("MAIN: Picture Classification starting...")
        self.threadCtrl.signal_ctrl_clas_start.emit()

    #Stop vision classification
    def slot_ctrl_vclas_stop(self):
        self.cebs_print_log("MAIN: Picture Classification stop.")
        self.threadCtrl.signal_ctrl_clas_stop.emit()

    #Enter calibration session
    def slot_ctrl_calib(self):
        if (self.threadCtrl.funcCtrlGetRightStatus() < 0):
            self.cebs_print_log("MAIN: CALIB ERROR1!")
            return -1;
        self.cebs_print_log("MAIN: CALIB ACTION!")
        self.threadCtrl.signal_ctrl_calib_start.emit()
        if not self.calibForm.isVisible():
            self.signal_mainwin_unvisible.emit()
            self.calibForm.show()

    #Enter parameter setting session
    def slot_gpar_start(self):
        self.cebs_print_log("MAIN: PARAMETER SETTING ACTION!")
        #self.threadCtrl.signal_ctrl_calib_start.emit()
        if not self.gparForm.isVisible():
            self.signal_mainwin_unvisible.emit()
            self.gparForm.show()
            
    #Control UI visible
    def funcMainWinVisible(self):
        if not self.isVisible():
            self.show()
        self.threadCtrl.signal_ctrl_calib_stop.emit()
        self.cebs_print_log("MAIN: WELCOME COME BACK!")

    #Control UI un-visible
    def funcMainWinUnvisible(self):
        if self.isVisible():
            self.hide()

    #Clean log window
    def slot_runpg_clear(self):
        self.textEdit_runProgress.clear();

    #Test functions
    def slot_runpg_test(self):
        res = {}
        self.cebs_print_log("TEST: " + str(res))

    #Local function
    def funcMainFormSetEquInitStatus(self):
        if (self.objMoto.funcMotoRunningStatusInquery() == True):
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
        radioCalaHts96 = self.radioButton_calib_bts_96.isChecked();
        radioCalaHts48 = self.radioButton_calib_bts_48.isChecked();
        radioCalaHts24 = self.radioButton_calib_bts_32.isChecked();
        radioCalaHts12 = self.radioButton_calib_bts_12.isChecked();
        radioCalaHts6 = self.radioButton_calib_bts_6.isChecked();
        if (radioCalaHts96 == 1):
            parMoveHts = 1;
        elif (radioCalaHts48 == 1):
            parMoveHts = 2;
        elif (radioCalaHts24 == 1):
            parMoveHts = 3;
        elif (radioCalaHts12 == 1):
            parMoveHts = 4;
        elif (radioCalaHts6 == 1):
            parMoveHts = 5;
        else:
            parMoveHts = 1;
        #SELECT HOLE TYPE, but to be complete this function.
        ModCebsCom.GL_CEBS_HB_TARGET_TYPE_NBR = parMoveHts;
        
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
        self.calibProc.funcCalibMove(parMoveScale, parMoveDir);
    
    def slot_calib_right_up(self):
        self.calibProc.funcCalibRightUp();
    
    def slot_calib_left_down(self):
        self.calibProc.funcCalibLeftDown();
    
    def slot_calib_pilot_start(self):
        self.calibProc.funcCalibPilotStart();

    def slot_calib_pilot_stop(self):
        self.calibProc.funcCalibPilotStop();

    def slot_calib_pilot_move_0(self):
        self.calibProc.funcCalibPilotMove0();

    def slot_calib_pilot_move_n(self):
        try:
            boardNbr = int(self.lineEdit_pilot_move_n.text())
        except Exception: 
            boardNbr = 1;
        self.calibProc.funcCalibPilotMoven(boardNbr);

    def slot_calib_pilot_camera_enable(self):
        self.calibProc.funcCalibPilotCameraEnable();

    def slot_calib_fm_up(self):
        self.calibProc.funcCalibForceMove('UP');
    
    def slot_calib_fm_down(self):
        self.calibProc.funcCalibForceMove('DOWN');

    def slot_calib_fm_left(self):
        self.calibProc.funcCalibForceMove('LEFT');

    def slot_calib_fm_right(self):
        self.calibProc.funcCalibForceMove('RIGHT');
    
    def slot_calib_close(self):
        self.calibProc.funcCtrlCalibComp()
        self.signal_mainwin_visible.emit()
        self.close()

    def closeEvent(self, event):
        self.calibProc.funcRecoverWorkingEnv()
        self.signal_mainwin_visible.emit()
        self.close()


#Calibration Widget
class cebsGparForm(QtWidgets.QWidget, Ui_cebsGparForm):
    signal_mainwin_visible = pyqtSignal()

    def __init__(self):    
        super(cebsGparForm, self).__init__()  
        self.setupUi(self)
        self.gparProc = ModCebsGpar.classGparProcess(self)
        self.objInitCfg2=ModCebsCfg.ConfigOpr()
        #Update UI interface last time parameter setting
        self.funcGlobalParReadSet2Ui()
        
    #Give up and not save parameters
    def closeEvent(self, event):
        #self.gparProc.funcRecoverWorkingEnv()
        self.signal_mainwin_visible.emit()
        self.close()

    def slot_gpar_compl(self):
        #self.gparProc.funcCtrlCalibComp()
        self.funcGlobalParReadSave()
        self.signal_mainwin_visible.emit()
        self.close()

    #Give up and not save parameters
    def slot_gpar_giveup(self):
        self.signal_mainwin_visible.emit()
        self.close()

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
        self.objInitCfg2.updateSectionPar()

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
    
    
