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
from form_qt.cebscalibform import Ui_cebsCalibForm




#第二主入口
#Calibration Widget
class SEUI_L4_CalibForm(QtWidgets.QWidget, Ui_cebsCalibForm, clsL1_ConfigOpr):
    sgL4MainWinUnvisible = pyqtSignal()
    sgL4MainWinVisible = pyqtSignal()
    sgL4CalibFormActiveTrig = pyqtSignal()

    def __init__(self, TaskInstCalibUi):    
        super(SEUI_L4_CalibForm, self).__init__()
        #CASE1: UI PART
        self.setupUi(self)

        #CASE2: WORKING TASK
        self.TkCalibUi = TaskInstCalibUi
        #使用传递指针的方式
        self.TkCalibUi.funcSaveFatherInst(self)
        
        #CASE3: INTI PARAMETERS
        self.initParameter()
    
    def initParameter(self):
        #载入缺省图像
        self.calibRect = self.label_calib_RtCam_Fill.geometry()
        if (os.path.exists('calibInitWorm.jpg') == True):
            self.filePicInit = QtGui.QPixmap('calibInitWorm.jpg').scaled(self.calibRect.width(), self.calibRect.height())
            self.label_calib_RtCam_Fill.setPixmap(self.filePicInit)
        
    def cetk_debug_print(self, info):
        time.sleep(0.01)
        strOut = ">> " + str(time.asctime()) + " " + str(info);
        self.textEdit_calib_runProgress.append(strOut);
        self.textEdit_calib_runProgress.moveCursor(QtGui.QTextCursor.End)
        self.textEdit_calib_runProgress.ensureCursorVisible()
        self.textEdit_calib_runProgress.insertPlainText("")       
    
    #界面的二次进入触发事件
    def switchOn(self):
        print("I am CALIB and enter again!")
    
    #
    #  SLOT FUNCTION, 槽函数部分
    #    DO NOT MODIFY SLOT FUNCTION NAMES, 以下部分为系统接口对应的槽函数，函数命名不得动
    #
    #
    #给TkCalibUi回调的处理过程
    def cal_callback_blurry_ret(self,res):
        self.lineEdit_current_pic_blurry_value.setText(str(res))
        
    def slot_calib_pilot_move_up(self):
        time.sleep(0.1)
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
        self.TkCalibUi.func_ui_click_pilot_mv(parMoveScale, "UP");
        
    def slot_calib_pilot_move_down(self):
        time.sleep(0.1)
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
        self.TkCalibUi.func_ui_click_pilot_mv(parMoveScale, "DOWN");
        
    def slot_calib_pilot_move_left(self):
        time.sleep(0.1)
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
        self.TkCalibUi.func_ui_click_pilot_mv(parMoveScale, "LEFT");
        
    def slot_calib_pilot_move_right(self):
        time.sleep(0.1)
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
        self.TkCalibUi.func_ui_click_pilot_mv(parMoveScale, "RIGHT");
        
        
    '''
    def slot_calib_pilot_move_up(self): 
        self.timer=QTimer()
        self.timer.setInterval(1)
        self.timer.start()
        self.timer.timeout.connect(self.onTimerOutUp) 
        
    def slot_calib_pilot_move_up_released(self):
        self.timer.stop()    
    
    def slot_calib_pilot_move_down(self): 
        self.timer=QTimer()
        self.timer.setInterval(1)
        self.timer.start()
        self.timer.timeout.connect(self.onTimerOutDown) 
        
    def slot_calib_pilot_move_down_released(self):
        self.timer.stop()
        
    def slot_calib_pilot_move_left(self): 
        self.timer=QTimer()
        self.timer.setInterval(1)
        self.timer.start()
        self.timer.timeout.connect(self.onTimerOutLeft) 
        
    def slot_calib_pilot_move_left_released(self):
        self.timer.stop()
        
    def slot_calib_pilot_move_right(self): 
        self.timer=QTimer()
        self.timer.setInterval(1)
        self.timer.start()
        self.timer.timeout.connect(self.onTimerOutRight)
        
    def slot_calib_pilot_move_right_released(self):
        self.timer.stop()          
    ''' 
    '''            
    def slot_calib_move(self):
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
        self.instL3CalibProc.funcCalibMove(parMoveScale, parMoveDir);
    '''
    def slot_calib_right_up(self):
        self.TkCalibUi.func_ui_click_right_up_set();
    
    def slot_calib_left_down(self):
        self.TkCalibUi.func_ui_click_left_down_set();
    
    def slot_calib_pilot_start(self):
        self.TkCalibUi.func_ui_click_pilot_start();

    def slot_calib_pilot_stop(self):
        self.TkCalibUi.func_ui_click_pilot_stop();

    def slot_calib_pilot_move_0(self):
        self.TkCalibUi.func_ui_click_pilot_move_0();

    def slot_calib_pilot_move_n(self):
        try:
            holeNbr = int(self.lineEdit_pilot_move_n.text())
        except Exception: 
            holeNbr = 1;
        self.TkCalibUi.func_ui_click_pilot_move_n(holeNbr);
    
    #CAMERA ENABLE: Not support any more!
#     def slot_calib_pilot_camera_enable(self):
#         self.instL3CalibProc.funcCalibPilotCameraEnable();

    #CAMERA CAPTURE: new function support
    def slot_calib_pilot_camera_cap(self):
        try:
            holeNbr = int(self.lineEdit_pilot_move_n.text())
        except Exception: 
            holeNbr = 1;        
        self.TkCalibUi.func_ui_click_cap_pic_by_hole(holeNbr);

    def slot_calib_fm_up(self):
        self.TkCalibUi.func_ui_click_force_move('UP');
    
    def slot_calib_fm_down(self):
        self.TkCalibUi.func_ui_click_force_move('DOWN');

    def slot_calib_fm_left(self):
        self.TkCalibUi.func_ui_click_force_move('LEFT');

    def slot_calib_fm_right(self):
        self.TkCalibUi.func_ui_click_force_move('RIGHT');
    
    def slot_calib_close(self):
        self.close()

    def closeEvent(self, event):
        self.TkCalibUi.func_ui_click_basic_close()
        self.TkCalibUi.func_ui_click_basic_switch_to_main()
        self.sgL4MainWinVisible.emit()
        self.close()

    def cetk_calib_disp_cam(self, fileName):
        if (os.path.exists(fileName) == True):
            temp_pixmap = QtGui.QPixmap(fileName).scaled(self.calibRect.width(), self.calibRect.height())
            self.label_calib_RtCam_Fill.setPixmap(temp_pixmap)

    def cetk_calib_disp_cam_by_obj(self, picObj):
        self.label_calib_RtCam_Fill.setPixmap(picObj.scaled(self.calibRect.width(), self.calibRect.height()))




