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
from form_qt.cebsstestform import Ui_cebsStestForm

        
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




