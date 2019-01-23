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
        #初始化参数
        self.func_read_par_from_com_and_set2ui()
        #将参数传递给业务模块
        self.rectPic = self.label_pic_fspc_fill.geometry()
        #self.TkGparUi.funcGparInitBascPar(self.rectPic.width(), self.rectPic.height(), self.rectCfy.width(), self.rectCfy.height())
        self.picFile = ''
        #一定要清理掉原始图像，防止二次操作时误操作
        self.label_pic_fspc_fill.clear()
        self.lineEdit_fspc_pic_file_load.clear()

    def cetk_debug_print(self, info):
        time.sleep(0.01)
        strOut = ">> " + str(time.asctime()) + " " + str(info);
        self.textEdit_fspc_cmd_log.append(strOut);
        self.textEdit_fspc_cmd_log.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_fspc_cmd_log.ensureCursorVisible()
        self.textEdit_fspc_cmd_log.insertPlainText("")
                
    #界面的二次进入触发事件
    def switchOn(self):
        self.initParameter()

    def closeEvent(self, event):
        #关闭钩子
        self.TkFspcUi.func_ui_click_fspc_close()
        #关闭切换界面钩子
        self.TkFspcUi.func_ui_click_fspc_switch_to_main()
        #QT本身的界面切换
        self.sgL4MainWinVisible.emit()
        self.close()


    def slot_clear(self):
        self.textEdit_fspc_cmd_log.clear();

    def slot_giveup(self):
        self.close()

    def slot_cmpl(self):
        self.func_update_par_and_write_ini()
        self.close()
        
        
        
    '''
    *得到文件目录
    directory1 = QFileDialog.getExistingDirectory(self, "选取文件夹", "C:/")
    * 打开文件
    files, ok1 = QFileDialog.getOpenFileNames(self, "多文件选择", "C:/", "All Files (*);;Text Files (*.txt)")
    * 存储文件
    fileName2, ok2 = QFileDialog.getSaveFileName(self, 文件保存", "C:/", "All Files (*);;Text Files (*.txt)")    
    '''
    def slot_file_load(self):
        if ('Windows' in platform.system()):
            fileName, _ = QFileDialog.getOpenFileName(self, "选取文件", "D:\\", "All Files (*);;Text Files (*.txt)")   #设置文件扩展名过滤,注意用双分号间隔
        else:
            fileName, _ = QFileDialog.getOpenFileName(self, "选取文件", "/home/", "All Files (*);;Text Files (*.txt)")   #设置文件扩展名过滤,注意用双分号间隔
        self.lineEdit_fspc_pic_file_load.setText(str(fileName))
        #将文件导入到目标框中
        if (fileName != ''):
            self.picFile = fileName
            img = QtGui.QPixmap(fileName)
            #固定位置显示
            img=img.scaled(self.rectPic.width(), self.rectPic.height())
            self.label_pic_fspc_fill.setPixmap(img)


    def slot_cmd_s1(self):
        if (self.picFile == ''):
            return;
        parRes = self.func_read_fpsc_par()
        self.TkFspcUi.func_ui_click_cmd_s1(self.picFile, parRes)
        
    def slot_cmd_s2(self):
        if (self.picFile == ''):
            return;
        parRes = self.func_read_fpsc_par()
        self.TkFspcUi.func_ui_click_cmd_s2(self.picFile, parRes)

    def slot_cmd_s3(self):
        if (self.picFile == ''):
            return;
        parRes = self.func_read_fpsc_par()
        self.TkFspcUi.func_ui_click_cmd_s3(self.picFile, parRes)

    def slot_cmd_s4(self):
        if (self.picFile == ''):
            return;
        parRes = self.func_read_fpsc_par()
        self.TkFspcUi.func_ui_click_cmd_s4(self.picFile, parRes)

    def slot_cmd_s5(self):
        if (self.picFile == ''):
            return;
        parRes = self.func_read_fpsc_par()
        self.TkFspcUi.func_ui_click_cmd_s5(self.picFile, parRes)
    
    def slot_cmd_s6(self):
        if (self.picFile == ''):
            return;
        parRes = self.func_read_fpsc_par()
        self.TkFspcUi.func_ui_click_cmd_s6(self.picFile, parRes)
    
    def slot_cmd_s7(self):
        if (self.picFile == ''):
            return;
        parRes = self.func_read_fpsc_par()
        self.TkFspcUi.func_ui_click_cmd_s7(self.picFile, parRes)
    
    def slot_cmd_sum(self):
        if (self.picFile == ''):
            return;
        parRes = self.func_read_fpsc_par()
        self.TkFspcUi.func_ui_click_cmd_sum(self.picFile, parRes)
    
    #调整参数后的图像显示
    def fspc_callback_cmd_exec_resp(self, fileName):
        if (fileName != ''):
            img = QtGui.QPixmap(fileName)
            #固定位置显示
            img=img.scaled(self.rectPic.width(), self.rectPic.height())
            self.label_pic_fspc_fill.setPixmap(img)    
    
    #
    #  SERVICE FUNCTION PART, 业务函数部分
    #
    #
    #Local function
    #读取到UI界面上
    def func_read_par_from_com_and_set2ui(self):
        self.lineEdit_fspc_mark_line.setText(str(ModCebsCom.GLFSPC_PAR_OFC.FSPC_COEF_MARK_LINE))
        self.lineEdit_fspc_coef_area_min.setText(str(ModCebsCom.GLFSPC_PAR_OFC.FSPC_COEF_AREA_MIN))
        self.lineEdit_fspc_coef_area_max.setText(str(ModCebsCom.GLFSPC_PAR_OFC.FSPC_COEF_AREA_MAX))
        self.lineEdit_fspc_coef_area_dilate.setText(str(ModCebsCom.GLFSPC_PAR_OFC.FSPC_COEF_AREA_DILATE))
        self.lineEdit_fspc_coef_area_erode.setText(str(ModCebsCom.GLFSPC_PAR_OFC.FSPC_COEF_AREA_ERODE))
        self.lineEdit_fspc_coef_cell_min.setText(str(ModCebsCom.GLFSPC_PAR_OFC.FSPC_COEF_CELL_MIN))
        self.lineEdit_fspc_coef_cell_max.setText(str(ModCebsCom.GLFSPC_PAR_OFC.FSPC_COEF_CELL_MAX))
        self.lineEdit_fspc_coef_raduis_min.setText(str(ModCebsCom.GLFSPC_PAR_OFC.FSPC_COEF_RADUIS_MIN))
        self.lineEdit_fspc_coef_raduis_max.setText(str(ModCebsCom.GLFSPC_PAR_OFC.FSPC_COEF_RADUIS_MAX))
        self.lineEdit_fspc_coef_cell_dilate.setText(str(ModCebsCom.GLFSPC_PAR_OFC.FSPC_COEF_CELL_DILATE))
        self.lineEdit_fspc_coef_cell_erode.setText(str(ModCebsCom.GLFSPC_PAR_OFC.FSPC_COEF_CELL_ERODE))
        self.lineEdit_fspc_coef_cell_ce.setText(str(ModCebsCom.GLFSPC_PAR_OFC.FSPC_COEF_CELL_CE))
        self.lineEdit_fspc_coef_cell_raduis_dist.setText(str(ModCebsCom.GLFSPC_PAR_OFC.FSPC_COEF_CELL_DIST))
        self.checkBox_fspc_output_addup.setChecked(ModCebsCom.GLFSPC_PAR_OFC.FSPC_ADDUP_SET)
    
    #读取界面上的参数并写入到INI配置文件
    def func_update_par_and_write_ini(self):
        #SAVE INTO COM VAR
        parRes = self.func_read_fpsc_par();
        (GLFSPC_PAR_OFC.FSPC_COEF_MARK_LINE, \
        GLFSPC_PAR_OFC.FSPC_COEF_AREA_MIN, \
        GLFSPC_PAR_OFC.FSPC_COEF_AREA_MAX, \
        GLFSPC_PAR_OFC.FSPC_COEF_AREA_DILATE, \
        GLFSPC_PAR_OFC.FSPC_COEF_AREA_ERODE, \
        GLFSPC_PAR_OFC.FSPC_COEF_CELL_MIN, \
        GLFSPC_PAR_OFC.FSPC_COEF_CELL_MAX, \
        GLFSPC_PAR_OFC.FSPC_COEF_RADUIS_MIN, \
        GLFSPC_PAR_OFC.FSPC_COEF_RADUIS_MAX, \
        GLFSPC_PAR_OFC.FSPC_COEF_CELL_DILATE, \
        GLFSPC_PAR_OFC.FSPC_COEF_CELL_ERODE, \
        GLFSPC_PAR_OFC.FSPC_COEF_CELL_CE, \
        GLFSPC_PAR_OFC.FSPC_COEF_CELL_DIST, \
        GLFSPC_PAR_OFC.FSPC_ADDUP_SET) = parRes
        #FINAL UPDATE
        self.updateFpscSectionCtrlPar()
 
    #读取荧光堆叠训练参数
    def func_read_fpsc_par(self):
        #黄线部分
        parMarkLine=150
        try: 
            parMarkLine = int(self.lineEdit_fspc_mark_line.text())
        except Exception: 
            pass
        #区域部分
        parAreaMin=10000
        try: 
            parAreaMin = int(self.lineEdit_fspc_coef_area_min.text())
        except Exception: 
            pass
        parAreaMax=100000
        try: 
            parAreaMax = int(self.lineEdit_fspc_coef_area_max.text())
        except Exception: 
            pass
        parAreaDilate=12
        try: 
            parAreaDilate = int(self.lineEdit_fspc_coef_area_dilate.text())
        except Exception: 
            pass
        parAreaErode=5
        try: 
            parAreaErode = int(self.lineEdit_fspc_coef_area_erode.text())
        except Exception: 
            pass
        #细胞部分
        parCellMin=920
        try: 
            parCellMin = int(self.lineEdit_fspc_coef_cell_min.text())
        except Exception: 
            pass        
        parCellMax=1500
        try: 
            parCellMax = int(self.label_fspc_coef_cell_max.text())
        except Exception: 
            pass
        parRaduisMin=19
        try: 
            parRaduisMin = int(self.label_fspc_coef_raduis_min.text())
        except Exception: 
            pass
        parRaduisMax=23
        try: 
            parRaduisMax = int(self.label_fspc_coef_raduis_max.text())
        except Exception: 
            pass
        parCellDilate=61
        try: 
            parCellDilate = int(self.lineEdit_fspc_coef_cell_dilate.text())
        except Exception: 
            pass
        parCellErode=5
        try: 
            parCellErode = int(self.lineEdit_fspc_coef_cell_erode.text())
        except Exception: 
            pass
        parCellCe=50
        try: 
            parCellCe = int(self.lineEdit_fspc_coef_cell_ce.text())
        except Exception: 
            pass
        parCellDist=30
        try: 
            parCellDist = int(self.label_fspc_coef_cell_raduis_dist.text())
        except Exception: 
            pass
        #标定
        addupSet = self.checkBox_fspc_output_addup.isChecked()
        #RETURN
        parRes = (parMarkLine, parAreaMin, parAreaMax, parAreaDilate, parAreaErode, parCellMin, parCellMax, parRaduisMin, parRaduisMax, parCellDilate, parCellErode, parCellCe, parCellDist, addupSet)
        return parRes

        
        
            
    
    
    
    
    
    
    



