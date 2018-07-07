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
from form_qt.cebsmainform import Ui_cebsMainWindow    # 导入生成mainForm.py里生成的类
from form_qt.cebscalibform import Ui_cebsCalibForm      # 导入生成calibForm.py里生成的类

#Local Class
from PkgCebsHandler import ModCebsCom  #Common Support module
from PkgCebsHandler import ModCebsMoto
from PkgCebsHandler import ModCebsCtrl
from PkgCebsHandler import ModCebsVision
from PkgCebsHandler import ModCebsCfg
from PkgCebsHandler import ModCebsCalib

#Main Windows
class cebsMainWindow(QtWidgets.QMainWindow, Ui_cebsMainWindow):
    signal_mainwin_unvisible = pyqtSignal()  #申明给主函数使用    
    
    def __init__(self):    
        super(cebsMainWindow, self).__init__()  
        self.setupUi(self)
        self.initUI()
        
        #必须使用成员函数，才能保证子FORM的生命周期
        self.calibForm = cebsCalibForm()
        self.objMoto = ModCebsMoto.classMotoProcess();

        #固定信号量设置
        self.calibForm.signal_mainwin_visible.connect(self.funcMainWinVisible);
        self.signal_mainwin_unvisible.connect(self.funcMainWinUnvisible);
        
        #读取配置文件参数
        objInitCfg=ModCebsCfg.ConfigOpr()
        objInitCfg.readGlobalPar();
        objInitCfg.updateCtrlCntInfo()
        
        #启动第一个干活的子进程
        self.threadCtrl = ModCebsCtrl.classCtrlThread()
        self.threadCtrl.setIdentity("CtrlThread")
        self.threadCtrl.signal_print_log.connect(self.slot_print_trigger)  #接收信号
        self.threadCtrl.signal_ctrl_start.connect(self.threadCtrl.funcTakePicStart) #发送信号
        self.threadCtrl.signal_ctrl_stop.connect(self.threadCtrl.funcTakePicStop)  #发送信号
        self.threadCtrl.signal_ctrl_clas_start.connect(self.threadCtrl.funcVisionClasStart) #发送信号
        self.threadCtrl.signal_ctrl_clas_stop.connect(self.threadCtrl.funcVisionClasStop)  #发送信号
        self.threadCtrl.signal_ctrl_calib_start.connect(self.threadCtrl.funcCtrlCalibStart) #发送信号
        self.threadCtrl.signal_ctrl_calib_stop.connect(self.threadCtrl.funcCtrlCalibStop)  #发送信号
        self.threadCtrl.signal_ctrl_zero.connect(self.threadCtrl.funcCtrlMotoBackZero)  #发送信号
        self.threadCtrl.start();

        #启动第二个干活的子进程
        self.threadVision = ModCebsVision.classVisionThread()
        self.threadVision.setIdentity("VisionThread")
        self.threadVision.signal_print_log.connect(self.slot_print_trigger)
        self.threadVision.start();

        #初始化配置
        self.funcMainFormSetEquInitStatus();

    def initUI(self):
        self.statusBar().showMessage('状态栏: ')
        self.setGeometry(10, 30, 1024, 768)

        exitAction = QAction(QIcon('.\icon_res\q10.ico'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('退出应用程序')
        exitAction.triggered.connect(qApp.quit)
        toolbar = self.addToolBar('EXIT')  
        toolbar.addAction(exitAction)

    def initParameter(self):
        pass

    #File Open Method, for reference
    def test_openMsg(self):  
        file, ok=QFileDialog.getOpenFileName(self,"打开","C:/","All Files (*);;Text Files (*.txt)")  
        self.statusbar.showMessage(file)

    #核心函数
    def cebs_print_log(self, info):
        strOld = self.textEdit_runProgress.toPlainText()
        #采用全局编辑
        #strOut = strOld + "\n>> " + time.asctime() + " " + info;
        #self.textEdit_runProgress.setText(strOut);
        #采用正常的append方法
        strOut = ">> " + time.asctime() + " " + info;
        self.textEdit_runProgress.append(strOut);
        self.textEdit_runProgress.moveCursor(QtGui.QTextCursor.End)
        #后面两个操作不增加也没啥大问题，但给了我们更多的操作线索
        self.textEdit_runProgress.ensureCursorVisible()
        self.textEdit_runProgress.insertPlainText("")

    def slot_print_trigger(self, info):
        self.cebs_print_log(info)

    def slot_ctrl_start(self):
        self.cebs_print_log("MAIN: 拍照开始！")
        #self.funcMainFormSetEquInitStatus();
        self.threadCtrl.signal_ctrl_start.emit()
        
    def slot_ctrl_stop(self):
        self.cebs_print_log("MAIN: 拍照停止！")
        self.threadCtrl.signal_ctrl_stop.emit()

    def slot_ctrl_zero(self):
        #self.funcMainFormSetEquInitStatus();
        self.cebs_print_log("MAIN: 系统归零！")
        self.threadCtrl.signal_ctrl_zero.emit()

    def slot_ctrl_vclas_start(self):
        #self.funcMainFormSetEquInitStatus();
        self.cebs_print_log("MAIN: 启动图像识别！")
        self.threadCtrl.signal_ctrl_clas_start.emit()

    def slot_ctrl_vclas_stop(self):
        self.cebs_print_log("MAIN: 停止图像识别！")
        self.threadCtrl.signal_ctrl_clas_stop.emit()

    def slot_ctrl_calib(self):
        if (self.threadCtrl.funcCtrlGetRightStatus() < 0):
            self.cebs_print_log("MAIN: CALIB上一个任务还未完成！")
            return -1;
        #self.funcMainFormSetEquInitStatus();
        self.cebs_print_log("MAIN: 开始校准！")
        self.threadCtrl.signal_ctrl_calib_start.emit()
        if not self.calibForm.isVisible():
            self.signal_mainwin_unvisible.emit()
            self.calibForm.show()

    def funcMainWinVisible(self):
        #再执行逻辑
        if not self.isVisible():
            self.show()
        #再将状态机改过来
        self.threadCtrl.signal_ctrl_calib_stop.emit()
        self.cebs_print_log("MAIN: 校准结束！")

    def funcMainWinUnvisible(self):
        if self.isVisible():
            self.hide()

    def slot_runpg_clear(self):
        self.textEdit_runProgress.clear();

    #Test functions
    def slot_runpg_test(self):
        res = {}
        self.cebs_print_log("TEST: " + str(res))

    #本来用于强制控制，现在有了CTRL层面的状态机之后，暂时不用了。
    #强制控制的坏处非常明显：动作部件在坏人狂点鼠标的情况下，可能会遇到损坏
    def funcMainFormSetEquInitStatus(self):
        self.objMoto.funcMotoStop() #停止马达

#Calibration Widget
class cebsCalibForm(QtWidgets.QWidget, Ui_cebsCalibForm):
    signal_mainwin_visible = pyqtSignal() #申明给主函数使用

    def __init__(self):    
        super(cebsCalibForm, self).__init__()  
        self.setupUi(self)
        #必须使用成员函数，才能保证子FORM的生命周期
        self.calibProc = ModCebsCalib.classCalibProcess(self)
        
    #校准打印
    def calib_print_log(self, info):
        strOut = ">> " + time.asctime() + " " + info;
        self.textEdit_calib_runProgress.append(strOut);
        self.textEdit_calib_runProgress.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_calib_runProgress.ensureCursorVisible()
        self.textEdit_calib_runProgress.insertPlainText("")
        
    #校准移动
    def slot_calib_move(self):
        #读取运动刻度
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
        #读取运动方向
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
    
    #校准左上
    def slot_calib_left_up(self):
        self.calibProc.funcCalibLeftUp();
    
    #校准右下
    def slot_calib_right_bottom(self):
        self.calibProc.funcCalibRightBottom();
    
    #校准巡游
    def slot_calib_pilot(self):
        self.calibProc.funcCalibPilotStart();

    #校准巡游停止
    def slot_calib_pilot_stop(self):
        self.calibProc.funcCalibPilotStop();

    #界面按钮结束
    def slot_calib_close(self):
        self.calibProc.funcCtrlCalibComp()
        self.signal_mainwin_visible.emit()
        self.close()

    #重载系统的关闭函数
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
    
    
