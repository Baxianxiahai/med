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
from form_qt.cebsgparform import Ui_cebsGparForm



'''
#
#3rd Main Entry, 第三主入口
#Calibration Widget
#
# 参数需要在INI文件、内存全局变量GLVIS_PAR_OFC，界面呈现之间保持同步
# 本模块设计的逻辑是
# 1) 系统启动的时候，由PrjEntry将参数从ini文件读取到GLVIS_PAR_OFC全局内存中
# 2) 然后在GPAR初始化时，将去全局变量读取到界面中
# 3) 如果界面参数有效改变了，则需要先更新到内存全局变量OFC，然后写到ini文件中
# 4) 如果界面参数无效改变了，则不要求更新内存全局变量OFC，且将该参数传递到VISION模块中，防止中间的临时过程污染VISION后续处理
# 5) GPAR界面二次进入时，需要重新装载全局变量到界面上，确保上次的操作（完成存储、放弃参数）是可靠的
#
'''
class SEUI_L4_GparForm(QtWidgets.QWidget, Ui_cebsGparForm, clsL1_ConfigOpr):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()

    def __init__(self, TaskInstGparUi):    
        super(SEUI_L4_GparForm, self).__init__()
        #CASE1: UI PART
        self.setupUi(self)

        #CASE2: WORKING TASK
        #使用传递指针的方式
        self.TkGparUi = TaskInstGparUi
        self.TkGparUi.funcSaveFatherInst(self)
        
        #CASE3: INTI PARAMETERS
        self.initParameter()
        
        #Update UI interface last time parameter setting
    def initParameter(self):
        self.func_read_par_from_com_and_set2ui()
        #将参数传递给业务模块
        self.rectOrg = self.label_gpar_pic_origin_fill.geometry()
        self.rectCfy = self.label_gpar_pic_cfy_fill.geometry()
        self.TkGparUi.funcGparInitBascPar(self.rectOrg.width(), self.rectOrg.height(), self.rectCfy.width(), self.rectCfy.height())
        self.picOrgFile = ''
        #一定要清理掉原始图像，防止二次操作时误操作
        self.label_gpar_pic_origin_fill.clear()
        self.label_gpar_pic_cfy_fill.clear()
        self.lineEdit_gpar_pic_file_load.clear()

    def cetk_debug_print(self, info):
        time.sleep(0.01)
        strOut = ">> " + str(time.asctime()) + " " + str(info);
        self.textEdit_gpar_cmd_log.append(strOut);
        self.textEdit_gpar_cmd_log.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_gpar_cmd_log.ensureCursorVisible()
        self.textEdit_gpar_cmd_log.insertPlainText("")
    
    #增加一个切换后重新更新参数的函数，不然在放弃的时候，无效参数设置还处于激活状态
    def switchOn(self):
        self.initParameter()
    
    '''
    *得到文件目录
    directory1 = QFileDialog.getExistingDirectory(self, "选取文件夹", "C:/")
    * 打开文件
    files, ok1 = QFileDialog.getOpenFileNames(self, "多文件选择", "C:/", "All Files (*);;Text Files (*.txt)")
    * 存储文件
    fileName2, ok2 = QFileDialog.getSaveFileName(self, 文件保存", "C:/", "All Files (*);;Text Files (*.txt)")    
    '''
    def slot_gpar_pic_file_load(self):
        if ('Windows' in platform.system()):
            fileName, _ = QFileDialog.getOpenFileName(self, "选取文件", "D:\\", "All Files (*);;Text Files (*.txt)")   #设置文件扩展名过滤,注意用双分号间隔
        else:
            fileName, _ = QFileDialog.getOpenFileName(self, "选取文件", "/home/", "All Files (*);;Text Files (*.txt)")   #设置文件扩展名过滤,注意用双分号间隔
        self.lineEdit_gpar_pic_file_load.setText(str(fileName))
        #将文件导入到目标框中
        if (fileName != ''):
            self.picOrgFile = fileName
            img = QtGui.QPixmap(fileName)
            img=img.scaled(self.rectOrg.width(), self.rectOrg.height())
            self.label_gpar_pic_origin_fill.setPixmap(img)

    #使用临时参数进行识别
    def slot_gpar_pic_train(self):
        if (self.picOrgFile == ''):
            return;
        l1, l2, l3, l4, add, g1, g2, g3, g4 = self.func_read_vis_train_par()
        self.TkGparUi.func_ui_click_pic_train(self.picOrgFile, l1, l2, l3, l4, add, g1, g2, g3, g4)
    
    def gpar_callback_train_resp(self, fileName):
        img = QtGui.QPixmap(fileName)
        img=img.scaled(self.rectCfy.width(), self.rectCfy.height())
        self.label_gpar_pic_cfy_fill.setPixmap(img)

    #使用临时参数进行识别
    def slot_gpar_flu_cell_cnt(self):
        if (self.picOrgFile == ''):
            return;
        l1, l2, l3, l4, add, g1, g2, g3, g4 = self.func_read_vis_train_par()
        self.TkGparUi.func_ui_click_gpar_flu_cell_cnt(self.picOrgFile, l1, l2, l3, l4, add, g1, g2, g3, g4);
        
    #
    #  SERVICE FUNCTION PART, 业务函数部分
    #
    #
    #Local function
    #读取到UI界面上
    def func_read_par_from_com_and_set2ui(self):
        self.checkBox_gpar_picFixPos.setChecked(ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET)
        self.checkBox_gpar_autoIdf.setChecked(ModCebsCom.GLVIS_PAR_OFC.PIC_CLASSIFIED_AFTER_TAKE_SET)
        self.checkBox_gpar_autoPic.setChecked(ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_AFTER_START_SET)
        self.lineEdit_gpar_picTti.setText(str(ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN))
        self.lineEdit_gpar_vision_small_low_limit.setText(str(ModCebsCom.GLVIS_PAR_OFC.SMALL_LOW_LIMIT))
        self.lineEdit_gpar_vision_small_mid_limit.setText(str(ModCebsCom.GLVIS_PAR_OFC.SMALL_MID_LIMIT))
        self.lineEdit_gpar_vision_mid_big_limit.setText(str(ModCebsCom.GLVIS_PAR_OFC.MID_BIG_LIMIT))
        self.lineEdit_gpar_vision_big_upper_limit.setText(str(ModCebsCom.GLVIS_PAR_OFC.BIG_UPPER_LIMIT))
        self.checkBox_gpar_vision_res_addup.setChecked(ModCebsCom.GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET)
        self.checkBox_gpar_video_enable.setChecked(ModCebsCom.GLVIS_PAR_OFC.CAPTURE_ENABLE)
        self.lineEdit_gpar_video_input.setText(str(ModCebsCom.GLVIS_PAR_OFC.CAPTURE_DUR_IN_SEC))
        if (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_96_STANDARD):
            self.radioButton_gpar_bts_96.setChecked(True)
        elif (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_48_STANDARD):
            self.radioButton_gpar_bts_48.setChecked(True)
        elif (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_24_STANDARD):
            self.radioButton_gpar_bts_24.setChecked(True)
        elif (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_12_STANDARD):
            self.radioButton_gpar_bts_12.setChecked(True)
        elif (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_6_STANDARD):
            self.radioButton_gpar_bts_6.setChecked(True)
        else:
            self.radioButton_gpar_bts_96.setChecked(True)
        #通用系数部分
        self.lineEdit_gpar_vision_coef1.setText(str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR1))
        self.lineEdit_gpar_vision_coef2.setText(str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR2))
        self.lineEdit_gpar_vision_coef3.setText(str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR3))
        self.lineEdit_gpar_vision_coef4.setText(str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR4))
    
    #读取界面上的参数并写入到INI配置文件
    def func_update_par_and_write_ini(self):
        #SAVE INTO COM VAR
        GLVIS_PAR_OFC.SMALL_LOW_LIMIT, GLVIS_PAR_OFC.SMALL_MID_LIMIT, GLVIS_PAR_OFC.MID_BIG_LIMIT, GLVIS_PAR_OFC.BIG_UPPER_LIMIT, \
            GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET, GLVIS_PAR_OFC.CFY_THD_GENR_PAR1, GLVIS_PAR_OFC.CFY_THD_GENR_PAR2, GLVIS_PAR_OFC.CFY_THD_GENR_PAR3,\
            GLVIS_PAR_OFC.CFY_THD_GENR_PAR4 = self.func_read_vis_train_par();
        #其它静态部分参数
        GLVIS_PAR_OFC.PIC_CLASSIFIED_AFTER_TAKE_SET = self.checkBox_gpar_autoIdf.isChecked();
        GLVIS_PAR_OFC.PIC_AUTO_WORKING_AFTER_START_SET = self.checkBox_gpar_autoPic.isChecked();
        GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET = self.checkBox_gpar_picFixPos.isChecked();
        try: 
            GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN = int(self.lineEdit_gpar_picTti.text());
        except Exception: 
            GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN = 60;
        GLVIS_PAR_OFC.saveCapEnable(self.checkBox_gpar_video_enable.isChecked())
        try: 
            GLVIS_PAR_OFC.saveCapDur(int(self.lineEdit_gpar_video_input.text()))
        except Exception: 
            GLVIS_PAR_OFC.saveCapDur(3)
        #HB-TYPE SELECTION
        radioGparHts96 = self.radioButton_gpar_bts_96.isChecked();
        radioGparHts48 = self.radioButton_gpar_bts_48.isChecked();
        radioGparHts24 = self.radioButton_gpar_bts_24.isChecked();
        radioGparHts12 = self.radioButton_gpar_bts_12.isChecked();
        radioGparHts6 = self.radioButton_gpar_bts_6.isChecked();
        #托盘型号
        option = 0;
        if (radioGparHts96 == 1): option = 96
        elif (radioGparHts48 == 1): option = 48
        elif (radioGparHts24 == 1): option = 24
        elif (radioGparHts12 == 1): option = 12
        elif (radioGparHts6 == 1): option = 6
        else: option = 6
        GLPLT_PAR_OFC.med_select_plate_board_type(option)
        #FINAL UPDATE
        self.updateStaticSectionEnvPar()

    #读取核心训练参数
    def func_read_vis_train_par(self):
        liPar1=200
        try: 
            liPar1 = int(self.lineEdit_gpar_vision_small_low_limit.text())
        except Exception: 
            pass
        liPar2=500
        try: 
            liPar2 = int(self.lineEdit_gpar_vision_small_mid_limit.text())
        except Exception: 
            pass
        liPar3=2000
        try: 
            liPar3 = int(self.lineEdit_gpar_vision_mid_big_limit.text())
        except Exception: 
            pass
        liPar4=5000
        try: 
            liPar4 = int(self.lineEdit_gpar_vision_big_upper_limit.text())
        except Exception: 
            pass
        addupSet = self.checkBox_gpar_vision_res_addup.isChecked()
        #通用参数部分
        gePar1 = 1
        try: 
            gePar1 = int(self.lineEdit_gpar_vision_coef1.text())
        except Exception: 
            pass
        gePar2 = 1
        try: 
            gePar2 = int(self.lineEdit_gpar_vision_coef2.text())
        except Exception: 
            pass
        gePar3 = 1
        try: 
            gePar3 = int(self.lineEdit_gpar_vision_coef3.text())
        except Exception: 
            pass
        gePar4 = 1
        try: 
            gePar4 = int(self.lineEdit_gpar_vision_coef4.text())
        except Exception: 
            pass
        #RETURN
        return liPar1, liPar2, liPar3, liPar4, addupSet, gePar1, gePar2, gePar3, gePar4


    #
    #  SLOT FUNCTION, 槽函数部分
    #    DO NOT MODIFY FUNCTION NAMES, 以下部分为系统接口对应的槽函数，函数命名不得动
    #    compl和giveup函数必须将释放mutex的动作放在closeEvent中统一完成，不然会造成完不成的情况
    #
    #    
    def slot_gpar_compl(self):
        self.func_update_par_and_write_ini()
        self.close()

    #Clear the command log text box
    def slot_gpar_clear(self):
        self.textEdit_gpar_cmd_log.clear();  
              
    #Give up and not save parameters
    def slot_gpar_giveup(self):
        self.close()

    #Give up and not save parameters
    def closeEvent(self, event):
        #必须将参数的更新放在这个地方：如果是存储，则将最终的参数传进去，如果是放弃，则将系统缺省参数传进去
        self.TkGparUi.func_ui_click_gpar_refresh_par()
        #关闭钩子
        self.TkGparUi.func_ui_click_gpar_close()
        #关闭切换界面钩子
        self.TkGparUi.func_ui_click_gpar_switch_to_main()
        #QT本身的界面切换
        self.sgL4MainWinVisible.emit()
        self.close()
