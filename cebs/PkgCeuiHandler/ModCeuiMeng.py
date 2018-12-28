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
from form_qt.cebsmengform import Ui_cebsMengForm




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
        
        
        
        
        
        
        