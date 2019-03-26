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
from PkgL1vmHandler.ModVmLayer import *
from PkgL3cebsHandler.ModCebsCom import *
from PkgL3cebsHandler.ModCebsCfg import *


#Form class
from form_qt.cebsSahtForm import Ui_cebsSahtForm



#6th Main Entry, 第六主入口
#Broswer Widget
class SEUI_L4_SahtForm(QtWidgets.QMainWindow, Ui_cebsSahtForm, clsL1_ConfigOpr):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()
    def __init__(self, TaskInstSahtUi):
        super(SEUI_L4_SahtForm, self).__init__()
        self.TkSahtUi = TaskInstSahtUi
        self.setupUi(self)
        #self.openBroswer()
        
    def openBroswer(self):
        print("[CEBS]  Open Saht is Start")
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
        print("I am Saht and enter again!")

    def closeEvent(self, event):
        #config = clsL1_ConfigOpr()
        #config.SetDishRowandColumn()
        self.sgL4MainWinVisible.emit()
        self.close()





