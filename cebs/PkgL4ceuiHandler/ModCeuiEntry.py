'''
Created on 2018年12月28日

@author: Administrator
'''


####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-

import sys
import time
from PyQt5 import QtWidgets, QtGui, QtCore,QtWebEngineWidgets

#Local Class
from PkgL1vmHandler.ModVmLayer import *
from PkgL3cebsHandler.ModCebsCom import *
from PkgL3cebsHandler.ModCebsCfg import *


#UI Class
from PkgL4ceuiHandler.ModCeuiMain import *


'''
'高级技巧，还未搞定'
'https://www.cnblogs.com/WSX1994/articles/9092331.html'

探索使得加载更加人性化和自动化
'''
def cebs_start_app():
    app = QtWidgets.QApplication(sys.argv)
    splash = cebs_show_startup_pic()
    return app, splash

def cebs_load_data(sp):
    for i in range(1, 2):              #模拟主程序加载过程 
        time.sleep(1)                   # 加载数据
        sp.showMessage("加载... {0}%".format(i * 10), QtCore.Qt.AlignHCenter |QtCore.Qt.AlignBottom, QtCore.Qt.black)
        QtWidgets.qApp.processEvents()  # 允许主进程处理事件

def cebs_show_startup_pic():
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("cebsStart.jpg"))
    splash.showMessage("加载...0%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    splash.resize(1202, 800)
    splash.show()
    cebs_load_data(splash)
    return splash    

def cebs_hide_startup_pic(splash):
    splash.hide()

def cebs_show_app(app, splash, TkMainUi, TkCalibUi, TkGparUi, TkMengUi, tkStestUi, TkSahtUi):
    QtWidgets.qApp.processEvents()
    mainWindow = SEUI_L4_MainWindow(TkMainUi, TkCalibUi, TkGparUi, TkMengUi, tkStestUi, TkSahtUi)
    mainWindow.show()
    cebs_hide_startup_pic(splash)
    #换用新机制，不然整个应用程序退出不成功
    app.exec_()
    return    

#THE MAIN ENTRY: 第0主入口，MAIN函数部分
#这个是聚合部分，放在一起进行显示和启动
def cebs_l4ui_main_form_entry(TkMainUi, TkCalibUi, TkGparUi, TkMenUi):
    app = QtWidgets.QApplication(sys.argv)
    splash = cebs_show_startup_pic()
    QtWidgets.qApp.processEvents()
    mainWindow = SEUI_L4_MainWindow(TkMainUi,TkCalibUi, TkGparUi, TkMenUi)
    mainWindow.show()
    cebs_hide_startup_pic(splash)
    sys.exit(app.exec_())
    return





