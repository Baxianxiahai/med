'''
Created on 2019年1月22日

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
from PkgL1vmHandler.ModVmLayer import *
from PkgL3cebsHandler.ModCebsCom import *
from PkgL3cebsHandler.ModCebsCfg import *


#Form class
from form_qt.cebsfspcform import Ui_cebsFspcForm



#6th Main Entry, 第六主入口
#Broswer Widget
class SEUI_L4_FspcForm(QtWidgets.QMainWindow, Ui_cebsFspcForm, clsL1_ConfigOpr):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()
    def __init__(self, TaskInstFspcUi):
        super(SEUI_L4_FspcForm, self).__init__()

        #CASE1: UI PART
        self.setupUi(self)

        #CASE2: WORKING TASK
        #使用传递指针的方式
        self.TkFspcUi = TaskInstFspcUi
        self.TkFspcUi.funcSaveFatherInst(self)

        #CASE3: INTI PARAMETERS
        self.initParameter()

        #Update UI interface last time parameter setting
    def initParameter(self):
        pass

    def cetk_debug_print(self, info):
        time.sleep(0.01)
        strOut = ">> " + str(time.asctime()) + " " + str(info);
        self.textEdit_fspc_cmd_log.append(strOut);
        self.textEdit_fspc_cmd_log.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_fspc_cmd_log.ensureCursorVisible()
        self.textEdit_fspc_cmd_log.insertPlainText("")
                
    #界面的二次进入触发事件
    def switchOn(self):
        print("I am Fspc and enter again!")

    def closeEvent(self, event):
        #config = clsL1_ConfigOpr()
        #config.SetDishRowandColumn()
        self.sgL4MainWinVisible.emit()
        self.close()











