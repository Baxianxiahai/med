'''
Created on 2018年12月8日

@author: Administrator
'''

import random
import sys
import time
import json
import os
import re
import urllib
import http
import socket
import datetime
import string
import ctypes 
import random
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math
from   ctypes import c_uint8
import win32com.client  #pip install pyWin32
from win32com.client import GetObject
#import usb.core
#from   cv2 import waitKey
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot

from multiprocessing import Queue, Process
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL3cebsHandler.ModCebsCom import *
from PkgL3cebsHandler.ModCebsCfg import *
from PkgL1vmHandler.ModVmConsole import *
from _overlapped import NULL

#from cebsTkL4Ui import *

class tupTaskVision(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    #主界面，干活拍照
    _STM_MAIN_UI_ACT = 4
    #校准模式下图像直接读取
    _STM_CALIB_UI_ACT = 5
    #参数模式下图像直接读取
    _STM_GPAR_UI_ACT = 6
    #STEST模式
    _STM_STEST_UI_ACT = 7
    
    #摄像头初始化之后的对象指针
    camera_nbr = -1 #摄像头ID
    capInit = ''    #视频对象句柄


    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_VISION, taskName="TASK_VISION", glTabEntry=glPar)
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(TUP_TASK_ID_VISION, self)
        self.capInit = ''
        self.WORM_CLASSIFY_base = GLVIS_PAR_OFC.SMALL_LOW_LIMIT;
        self.WORM_CLASSIFY_small2mid = GLVIS_PAR_OFC.SMALL_MID_LIMIT;
        self.WORM_CLASSIFY_mid2big = GLVIS_PAR_OFC.MID_BIG_LIMIT;
        self.WORM_CLASSIFY_big2top = GLVIS_PAR_OFC.BIG_UPPER_LIMIT;
        self.WORM_CLASSIFY_addupSet = GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET;
        self.FLU_CELL_COUNT_genr_par1 = GLVIS_PAR_OFC.CFY_THD_GENR_PAR1
        self.FLU_CELL_COUNT_genr_par2 = GLVIS_PAR_OFC.CFY_THD_GENR_PAR2
        self.FLU_CELL_COUNT_genr_par3 = GLVIS_PAR_OFC.CFY_THD_GENR_PAR3
        self.FLU_CELL_COUNT_genr_par4 = GLVIS_PAR_OFC.CFY_THD_GENR_PAR4
        #想办法整到函数本地去
        self.fsm_set(TUP_STM_NULL)

        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_com_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_EXIT, self.fsm_com_msg_exit_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_com_msg_test_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_HW_REL, self.fsm_msg_vision_hw_release_rcv_handler)
        
        #通知界面切换
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_MAIN_UI_SWITCH, self.fsm_msg_main_ui_switch_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_UI_SWITCH, self.fsm_msg_calib_ui_switch_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_GPAR_UI_SWITCH, self.fsm_msg_gpar_ui_switch_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_STEST_UI_SWITCH, self.fsm_msg_stest_ui_switch_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_GPAR_REFRESH_PAR, self.fsm_msg_refresh_par_rcv_handler)

        #CALIB校准模式下的视频摄像头+抓图指令  CALIB校准界面下的抓图指令
        self.add_stm_combine(self._STM_CALIB_UI_ACT, TUP_MSGID_CALIB_VDISP_REQ, self.fsm_msg_calib_video_display_req_rcv_handler)
        self.add_stm_combine(self._STM_CALIB_UI_ACT, TUP_MSGID_CALIB_PIC_CAP_HOLEN, self.fsm_msg_calib_pic_cap_holen_rcv_handler)

        #MAIN主界面业务模式下的抓图指令
        self.add_stm_combine(self._STM_MAIN_UI_ACT, TUP_MSGID_CTRS_PIC_CAP_REQ, self.fsm_msg_main_ctrs_pic_cap_req_rcv_handler)
        self.add_stm_combine(self._STM_MAIN_UI_ACT, TUP_MSGID_CTRS_FLU_CAP_REQ, self.fsm_msg_main_ctrs_flu_cap_req_rcv_handler)

        #MAIN主界面模式下的图像识别
        self.add_stm_combine(self._STM_MAIN_UI_ACT, TUP_MSGID_CTRS_PIC_CLFY_REQ, self.fsm_msg_main_ctrs_pic_clfy_req_rcv_handler)
        self.add_stm_combine(self._STM_MAIN_UI_ACT, TUP_MSGID_CTRS_FLU_CLFY_REQ, self.fsm_msg_main_ctrs_flu_clfy_req_rcv_handler)
        
        #GPAR训练图像
        self.add_stm_combine(self._STM_GPAR_UI_ACT, TUP_MSGID_GPAR_PIC_TRAIN_REQ, self.fsm_msg_pic_train_req_rcv_handler)
        self.add_stm_combine(self._STM_GPAR_UI_ACT, TUP_MSGID_GPAR_PIC_FCC_REQ, self.fsm_msg_pic_flu_cell_count_req_rcv_handler)
        
        #STEST模式
        self.add_stm_combine(self._STM_STEST_UI_ACT, TUP_MSGID_STEST_CAM_INQ, self.fsm_msg_stest_cam_inq_rcv_handler)
        
        
        #切换状态机
        self.fsm_set(TUP_STM_INIT)
        #START TASK
        self.task_run()
    
    '''
    #
    #摄像头初始化
    #https://docs.opencv.org/3.3.0/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
    enum   cv::VideoCaptureProperties { 
       cv::CAP_PROP_POS_MSEC =0, 
       cv::CAP_PROP_POS_FRAMES =1, 
       cv::CAP_PROP_POS_AVI_RATIO =2, 
       cv::CAP_PROP_FRAME_WIDTH =3, 
       cv::CAP_PROP_FRAME_HEIGHT =4, 
       cv::CAP_PROP_FPS =5, 
       cv::CAP_PROP_FOURCC =6, 
       cv::CAP_PROP_FRAME_COUNT =7, 
       cv::CAP_PROP_FORMAT =8, 
       cv::CAP_PROP_MODE =9, 
       cv::CAP_PROP_BRIGHTNESS =10, 
       cv::CAP_PROP_CONTRAST =11, 
       cv::CAP_PROP_SATURATION =12, 
       cv::CAP_PROP_HUE =13, 
       cv::CAP_PROP_GAIN =14, 
       cv::CAP_PROP_EXPOSURE =15, 
       cv::CAP_PROP_CONVERT_RGB =16, 
       cv::CAP_PROP_WHITE_BALANCE_BLUE_U =17, 
       cv::CAP_PROP_RECTIFICATION =18, 
       cv::CAP_PROP_MONOCHROME =19, 
       cv::CAP_PROP_SHARPNESS =20, 
       cv::CAP_PROP_AUTO_EXPOSURE =21, 
       cv::CAP_PROP_GAMMA =22, 
       cv::CAP_PROP_TEMPERATURE =23, 
       cv::CAP_PROP_TRIGGER =24, 
       cv::CAP_PROP_TRIGGER_DELAY =25, 
       cv::CAP_PROP_WHITE_BALANCE_RED_V =26, 
       cv::CAP_PROP_ZOOM =27, 
       cv::CAP_PROP_FOCUS =28, 
       cv::CAP_PROP_GUID =29, 
       cv::CAP_PROP_ISO_SPEED =30, 
       cv::CAP_PROP_BACKLIGHT =32, 
       cv::CAP_PROP_PAN =33, 
       cv::CAP_PROP_TILT =34, 
       cv::CAP_PROP_ROLL =35, 
       cv::CAP_PROP_IRIS =36, 
       cv::CAP_PROP_SETTINGS =37, 
       cv::CAP_PROP_BUFFERSIZE =38, 
       cv::CAP_PROP_AUTOFOCUS =39 
     } 
    #
    #
    '''    
    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        #全局搜索摄像头
        self.camera_nbr = -1
        p = clsCamDevHdl()
        self.camera_nbr = p.dhSearchRunCam()
        res = "L2VISCAP: Valid camera number = " + str(self.camera_nbr)     
        self.funcVisionLogTrace(str(res))
        #INIT
        if (self.camera_nbr < 0):
            self.funcVisionErrTrace("L2VISCAP: Camera not yet installed, init error!");
            return TUP_FAILURE;
        #正确的情况
        try:
            self.capInit = cv.VideoCapture(self.camera_nbr) #CHECK WITH ls /dev/video*　RESULT
            self.capInit.set(3, GLVIS_PAR_OFC.VISION_CAMBER_RES_WITDH)
            self.capInit.set(4, GLVIS_PAR_OFC.VISION_CAMBER_RES_HEIGHT)
            print("CAP_PROP_BRIGHTNESS = ", self.capInit.get(cv.CAP_PROP_BRIGHTNESS))
            print("CAP_PROP_EXPOSURE = ", self.capInit.get(cv.CAP_PROP_EXPOSURE))
            print("CAP_PROP_ZOOM = ", self.capInit.get(cv.CAP_PROP_ZOOM))
            print("CAP_PROP_FOCUS = ", self.capInit.get(cv.CAP_PROP_FOCUS))
            print("CAP_PROP_GAIN = ", self.capInit.get(cv.CAP_PROP_GAIN))
            print("CAP_PROP_WHITE_BALANCE_BLUE_U = ", self.capInit.get(cv.CAP_PROP_WHITE_BALANCE_BLUE_U))
            if not self.capInit.isOpened():
                self.capInit.release()
        except Exception:
            cv.destroyAllWindows()
            self.funcVisionErrTrace("L2VISCAP: Camera not installed, but open error!");
            return TUP_FAILURE;
        self.funcVisionLogTrace("L2VISCAP: Camera open successful!");
        return TUP_SUCCESS;

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;

    #释放所有的硬件资源
    def fsm_msg_vision_hw_release_rcv_handler(self, msgContent):
        if (self.camera_nbr >= 0):
            try:
                self.capInit.release()
                cv.destroyAllWindows()
            except Exception:
                pass
        return TUP_SUCCESS;

    def fsm_msg_main_ui_switch_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_MAIN_UI_ACT)
        return TUP_SUCCESS;
    
    def fsm_msg_calib_ui_switch_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_CALIB_UI_ACT)
        return TUP_SUCCESS;

    def fsm_msg_gpar_ui_switch_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_GPAR_UI_ACT)
        return TUP_SUCCESS;    

    def fsm_msg_stest_ui_switch_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_STEST_UI_ACT)
        return TUP_SUCCESS;    
    
    def fsm_msg_refresh_par_rcv_handler(self, msgContent):
        self.WORM_CLASSIFY_base = msgContent['baseLimit'];
        self.WORM_CLASSIFY_small2mid = msgContent['small2Mid'];
        self.WORM_CLASSIFY_mid2big = msgContent['mid2Big'];
        self.WORM_CLASSIFY_big2top = msgContent['bigLimit'];
        self.WORM_CLASSIFY_addupSet = msgContent['addupSet'];
        self.FLU_CELL_COUNT_genr_par1 = msgContent['genrPar1'];
        self.FLU_CELL_COUNT_genr_par2 = msgContent['genrPar2'];
        self.FLU_CELL_COUNT_genr_par3 = msgContent['genrPar3'];
        self.FLU_CELL_COUNT_genr_par4 = msgContent['genrPar4'];
        return TUP_SUCCESS;

    #STEST业务
    def fsm_msg_stest_cam_inq_rcv_handler(self, msgContent):
        mbuf={}
        if (self.camera_nbr < 0) or (self.capInit == ''):
            mbuf['camOpen'] = -1
        else:
            mbuf['camOpen'] = 1
        self.msg_send(TUP_MSGID_STEST_CAM_FDB, TUP_TASK_ID_STEST, mbuf)
        return TUP_SUCCESS;

    def funcVisionLogTrace(self, myString):
        if (self.state == self._STM_MAIN_UI_ACT):
            self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MAIN, myString)
        elif (self.state == self._STM_CALIB_UI_ACT):
            self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_CALIB, myString)
        elif (self.state == self._STM_GPAR_UI_ACT):
            self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_GPAR, myString)
        else:
            self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MAIN, myString)
        #SAVE INTO MED FILE
        self.medCmdLog(str(myString))
        #PRINT to local
        self.tup_dbg_print(str(myString))
        return
    
    def funcVisionErrTrace(self, myString):
        if (self.state == self._STM_MAIN_UI_ACT):
            self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MAIN, myString)
        elif (self.state == self._STM_CALIB_UI_ACT):
            self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_CALIB, myString)
        else:
            self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MAIN, myString)
        #SAVE INTO MED FILE
        self.medErrorLog(str(myString));
        #PRINT to local
        self.tup_err_print(str(myString))
        return
    
    '''
    #
    # 本函数需要通过QT的过程截获图像并通过全局变量传递给UI，从而实现实时显示
    #
    #传递文件回去给显示界面
    #暂时没找到其它更好的办法，所以只能采用文件传输的方式
    #尝试使用去全局变量传递视频图像对象
    #本来是通过文件读取，目前改为了对象指针共享，效率要高些
    #cv.imwrite("tempCalibDisp.jpg", outFrame)
    #mbuf['fileName'] = "tempCalibDisp.jpg"
    #
    #正确处理过程：这是主要通过全局变量传递的复杂数据对象
    #其它的COM数据主要还是一些简单的共享参数信息
    #
    '''
    def fsm_msg_calib_video_display_req_rcv_handler(self, msgContent):
        mbuf={}
        if self.capInit == '':
            mbuf['res'] = -1
            self.msg_send(TUP_MSGID_CALIB_VDISP_RESP, TUP_TASK_ID_CALIB, mbuf)
            return TUP_FAILURE;
        #CAPTURE PICTURE
        ret, outFrame = self.func_cap_qt_frame()        
        if (ret <0):
            mbuf['res'] = -2
            self.msg_send(TUP_MSGID_CALIB_VDISP_RESP, TUP_TASK_ID_CALIB, mbuf)
            return TUP_FAILURE;
        GLVIS_PAR_OFC.CALIB_VDISP_OJB = outFrame
        mbuf['res'] = 1
        mbuf['ComObj'] = True
        self.msg_send(TUP_MSGID_CALIB_VDISP_RESP, TUP_TASK_ID_CALIB, mbuf)
        return TUP_SUCCESS;      

    #传递文件回去给显示界面
    def fsm_msg_calib_pic_cap_holen_rcv_handler(self, msgContent):
        holeNbr = msgContent['holeNbr']
        fileName = msgContent['fileName']
        if self.capInit == '':
            self.funcVisionErrTrace("VISION: capture error as not init camera!")
            return TUP_FAILURE;
        #CAPTURE PICTURE
        ret, outFrame = self.func_cap_one_frame()
        if (ret <0):
            self.funcVisionErrTrace("VISION: capture picture error!")
            return TUP_FAILURE;
        cv.imwrite(fileName, outFrame)
        self.funcVisionLogTrace("VISION: Capture and save file, batch=%d, fileNbr=%d, fn=%s" % (GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, holeNbr, fileName));
        return TUP_SUCCESS;
    
    #主界面模式下拍照
    def fsm_msg_main_ctrs_pic_cap_req_rcv_handler(self, msgContent):
        fnPic = msgContent['fnPic']
        fnScale = msgContent['fnScale']
        fnVideo = msgContent['fnVideo']
        vdCtrl = msgContent['vdCtrl']
        sclCtrl = msgContent['sclCtrl']
        vdDur = msgContent['vdDur']
        res = self.func_pic_vid_cap_and_save_file(fnPic, fnScale, fnVideo, vdCtrl, sclCtrl, vdDur);
        mbuf={}
        mbuf['res'] = res
        self.msg_send(TUP_MSGID_CTRS_PIC_CAP_RESP, TUP_TASK_ID_CTRL_SCHD, mbuf)
        return TUP_SUCCESS;
    
    #FLU图像拍摄的功能还未完善，暂时使用了白光拍摄的手法
    def fsm_msg_main_ctrs_flu_cap_req_rcv_handler(self, msgContent):
        fnPic = msgContent['fnPic']
        fnScale = msgContent['fnScale']
        fnVideo = msgContent['fnVideo']
        vdCtrl = msgContent['vdCtrl']
        sclCtrl = msgContent['sclCtrl']
        vdDur = msgContent['vdDur']
        res = self.func_pic_vid_cap_and_save_file(fnPic, fnScale, fnVideo, vdCtrl, sclCtrl, vdDur);
        mbuf={}
        mbuf['res'] = res
        self.msg_send(TUP_MSGID_CTRS_FLU_CAP_RESP, TUP_TASK_ID_CTRL_SCHD, mbuf)
        return TUP_SUCCESS;

    #识别算法
    def fsm_msg_main_ctrs_pic_clfy_req_rcv_handler(self, msgContent):
        fileName = msgContent['fileName']
        fileNukeName = msgContent['fileNukeName']
        ctrl = msgContent['ctrl']
        addupSet = msgContent['addupSet']
        res, outputFn, outText= self.func_vision_worm_clasification(fileName, fileNukeName, ctrl, addupSet);
        mbuf={}
        mbuf['res'] = res
        mbuf['outputFn'] = outputFn
        mbuf['outText'] = outText
        print(mbuf['res'])
        print(mbuf['outputFn'])
        print(mbuf['outText'])
        self.msg_send(TUP_MSGID_CRTS_PIC_CLFY_RESP, TUP_TASK_ID_CTRL_SCHD, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_main_ctrs_flu_clfy_req_rcv_handler(self, msgContent):
        fileName = msgContent['fileName']
        fileNukeName = msgContent['fileNukeName']
        ctrl = msgContent['ctrl']
        addupSet = msgContent['addupSet']
        res = self.func_vision_worm_clasification(fileName, fileNukeName, ctrl, addupSet);
        mbuf={}
        mbuf['res'] = res
        self.msg_send(TUP_MSGID_CRTS_FLU_CLFY_RESP, TUP_TASK_ID_CTRL_SCHD, mbuf)
        return TUP_SUCCESS;
    
    #GPAR中的训练过程
    def fsm_msg_pic_train_req_rcv_handler(self, msgContent):
        picFile = msgContent['fileName']
        mbuf={}
        if (os.path.exists(picFile) == False):
            mbuf['res'] = -1
            self.msg_send(TUP_MSGID_GPAR_PIC_TRAIN_RESP, TUP_TASK_ID_GPAR, mbuf)
            return TUP_SUCCESS;
        self.func_vision_worm_clasification(picFile, 'tempPic.jpg', True, self.WORM_CLASSIFY_addupSet)
        if (os.path.exists('tempPic.jpg') == False):
            mbuf['res'] = -2
            self.msg_send(TUP_MSGID_GPAR_PIC_TRAIN_RESP, TUP_TASK_ID_GPAR, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'tempPic.jpg'
        self.msg_send(TUP_MSGID_GPAR_PIC_TRAIN_RESP, TUP_TASK_ID_GPAR, mbuf)
        return TUP_SUCCESS;

    #GPAR中的荧光细胞计数过程
    def fsm_msg_pic_flu_cell_count_req_rcv_handler(self, msgContent):
        picOrgFile = msgContent['fileName']
        mbuf={}
        if (os.path.exists(picOrgFile) == False):
            mbuf['res'] = -1
            self.msg_send(TUP_MSGID_GPAR_PIC_FCC_RESP, TUP_TASK_ID_GPAR, mbuf)
            return TUP_SUCCESS;
        totalCnt = self.func_vision_flu_cell_count(picOrgFile, 'tempPic.jpg', self.FLU_CELL_COUNT_genr_par1, self.WORM_CLASSIFY_base, self.WORM_CLASSIFY_big2top, self.FLU_CELL_COUNT_genr_par2, self.WORM_CLASSIFY_addupSet)
        if (os.path.exists('tempPic.jpg') == False):
            mbuf['res'] = -2
            self.msg_send(TUP_MSGID_GPAR_PIC_FCC_RESP, TUP_TASK_ID_GPAR, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'tempPic.jpg'
        mbuf['nbr'] = totalCnt
        self.funcVisionLogTrace(str("Final counter = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_GPAR_PIC_FCC_RESP, TUP_TASK_ID_GPAR, mbuf)
        return TUP_SUCCESS;









    '''
    #SERVICE PART: 业务部分的函数，功能处理函数
    #获取图像的函数
    '''
    #输出OpenCV可以识别的格式 => 为了本地存储只用
    def func_cap_one_frame(self):
        try:
            ret, frame = self.capInit.read()
        except Exception:
            pass
        if (ret != True):
            return -1,_;
        frame = cv.flip(frame, 1)#Operation in frame
        frame = cv.resize(frame, None, fx=1, fy=1, interpolation=cv.INTER_AREA)
        #白平衡算法
        B,G,R = cv.split(frame)
        bMean = cv.mean(B)
        gMean = cv.mean(G)
        rMean = cv.mean(R)
        kb = (bMean[0] + gMean[0] + rMean[0])/(3*bMean[0]+0.0001)
        kg = (bMean[0] + gMean[0] + rMean[0])/(3*gMean[0]+0.0001)
        kr = (bMean[0] + gMean[0] + rMean[0])/(3*rMean[0]+0.0001)
        B = B * kb
        G = G * kg
        R = R * kr
        outputFrame = cv.merge([B, G, R])
        return 1, outputFrame
    
    #输出QT格式
    def func_cap_qt_frame(self):
        try:
            ret, frame = self.capInit.read()
        except Exception:
            pass
        if (ret != True):
            return -1,_;
        
        height, width = frame.shape[:2]
        if frame.ndim == 3:
            rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        elif frame.ndim == 2:
            rgb = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
        temp_image = QtGui.QImage(rgb.flatten(), width, height, QtGui.QImage.Format_RGB888)
        temp_pixmap = QtGui.QPixmap.fromImage(temp_image)
        return 1, temp_pixmap






    '''
    #
    #NEW截获图像
    #
    # fnPic: 图片文件名字
    # fnScale: 需要增加为带尺度的文件名字
    # fnVideo: 视频文件名字
    # vdCtrl: 控制是否需要拍摄视频
    #
    '''
    def func_pic_vid_cap_and_save_file(self, fnPic, fnScale, fnVideo, vdCtrl, sclCtrl, vdDur):
        try:
            if not self.capInit.isOpened():
                self.funcVisionErrTrace("L2VISCAP: Cannot open webcam!")
                self.capInit.release()
        except Exception:
            cv.destroyAllWindows()            
            return -1;
        #正确的情况
        width = int(self.capInit.get(cv.CAP_PROP_FRAME_WIDTH) + 0.5)
        height = int(self.capInit.get(cv.CAP_PROP_FRAME_HEIGHT) + 0.5)
        fps = 20
        #ret, frame = self.capInit.read()
        ret = self.capInit.grab()
        if (ret == False):
            return -1
        
        ret, frame = self.capInit.retrieve()
        ret, frame = self.capInit.retrieve()
        if (ret == True):
            frame = cv.flip(frame, 1)#Operation in frame
            frame = cv.resize(frame, None, fx=1, fy=1, interpolation=cv.INTER_AREA)
            #白平衡算法
            B,G,R = cv.split(frame)
            bMean = cv.mean(B)
            gMean = cv.mean(G)
            rMean = cv.mean(R)
            print("L2VISCAP: Mean B/G/R = %d/%d/%d" %(bMean[0], gMean[0], rMean[0]))
            kb = (bMean[0] + gMean[0] + rMean[0])/(3*bMean[0]+0.0001)
            kg = (bMean[0] + gMean[0] + rMean[0])/(3*gMean[0]+0.0001)
            kr = (bMean[0] + gMean[0] + rMean[0])/(3*rMean[0]+0.0001)
            B = B * kb
            G = G * kg
            R = R * kr
            outputFrame = cv.merge([B, G, R])
            cv.imwrite(fnPic, outputFrame)
            if sclCtrl == True:
                self.proc_algo_vis_get_radians(GLPLT_PAR_OFC.med_get_radians_len_in_us(), fnPic, fnScale)
        if (ret == True) and (vdCtrl == True):
            #Video capture with 3 second
            fourcc = cv.VideoWriter_fourcc(*'mp4v')  #mp4v(.mp4), XVID(.avi)
            out = cv.VideoWriter(fnVideo, fourcc, fps, (width, height))
            cnt = 0
            targetCnt = fps * vdDur;
            while self.capInit.isOpened():
                cnt += 1
                ret, frame = self.capInit.read()
                if ret:
                    frame = cv.flip(frame, 0)
                    #write the flipped frame
                    time.sleep(1.0/fps)
                    out.write(frame)
                    if cnt >= targetCnt:
                        break
                else:
                    break
            out.release()
            return 2;
        return 1;
    

    #计算弧度的方式
    #INPUT: refRadInUm, 孔半径长度，um单位
    #OUTPUT: 对应比例关系
    def proc_algo_vis_get_radians(self, refRadInUm, dirFn, newFileFn):
        #Reading file: 读取文件
        if (os.path.exists(dirFn) == False):
            errStr = "L2VISCFY: File %s not exist!" % (dirFn)
            self.medErrorLog(errStr);
            print("L2VISCFY: File %s not exist!" % (dirFn))
            return;
        try:
            inputImg = cv.imread(dirFn)
        except Exception as err:
            print("L2VISCFY: Read file error, errinfo = ", str(err))
            return;
        #图像分块
        orgH = inputImg.shape[0]
        orgW = inputImg.shape[1]
        imgLeftUp = inputImg[0:orgH//3, 0:orgW//3]
        imgRightUp = inputImg[0:orgH//3, orgW*2//3:orgW]
        imgLeftBot = inputImg[orgH*2//3:orgH, 0:orgW//3]
        imgRightBot = inputImg[orgH*2//3:orgH, orgW*2//3:orgW]
        arcLenMax = math.sqrt((orgH//3) * (orgH//3) + (orgW//3) * (orgW//3))*2
        #print("Max Arc length = ", arcLenMax)
        #比较
        flagIndex = 0
        arcSave = 0
        stdRatio = 0
        #PART1
        arcLen, lenSqrRatio, resImgLU = self.proc_algo_vis_find_max_edge(refRadInUm, imgLeftUp)
        #print("LU Length/baseline = %f/%f" % (arcLen, lenSqrRatio))
        if (arcLen < arcLenMax) and (lenSqrRatio < 1) and (lenSqrRatio > 0.1) and (arcLen > arcSave):
            flagIndex = 1
            arcSave = arcLen
            stdRatio = lenSqrRatio
        #PART2
        arcLen, lenSqrRatio, resImgRU = self.proc_algo_vis_find_max_edge(refRadInUm, imgRightUp)
        #print("RU Length/baseline = %f/%f" % (arcLen, lenSqrRatio))
        if (arcLen < arcLenMax) and (lenSqrRatio < 1) and (lenSqrRatio > 0.1) and (arcLen > arcSave):
            flagIndex = 2
            arcSave = arcLen
            stdRatio = lenSqrRatio
        #PART3
        arcLen, lenSqrRatio, resImgLB = self.proc_algo_vis_find_max_edge(refRadInUm, imgLeftBot)
        #print("LB Length/baseline = %f/%f" % (arcLen, lenSqrRatio))
        if (arcLen < arcLenMax) and (lenSqrRatio < 1) and (lenSqrRatio > 0.1) and (arcLen > arcSave):
            flagIndex = 3
            arcSave = arcLen
            stdRatio = lenSqrRatio
        #PART4
        arcLen, lenSqrRatio, resImgRB = self.proc_algo_vis_find_max_edge(refRadInUm, imgRightBot)
        #print("RB Length/baseline = %f/%f" % (arcLen, lenSqrRatio))
        if (arcLen < arcLenMax) and (lenSqrRatio < 1) and (lenSqrRatio > 0.1) and (arcLen > arcSave):
            flagIndex = 4
            arcSave = arcLen
            stdRatio = lenSqrRatio
        #SHOW
        '''
        if (flagIndex == 1):
            print("Result = resImgLU")
            #cv.line(resImgLU, start, end, (0, 0, 255))
            cv.imshow("resImgLU", resImgLU)
        if (flagIndex == 2):
            print("Result = resImgRU")
            #cv.line(resImgRU, start, end, (0, 0, 255))
            cv.imshow("resImgRU", resImgRU)
        if (flagIndex == 3):
            print("Result = resImgLB")
            #cv.line(resImgLB, start, end, (0, 0, 255))
            cv.imshow("resImgLB", resImgLB)
        if (flagIndex == 4):
            print("Result = resImgRB")
            #cv.line(resImgRB, start, end, (0, 0, 255))
            cv.imshow("resImgRB", resImgRB)
        '''
        #1mm = 1000um的标尺
        ptLen = int(500*stdRatio)
        sp = inputImg.shape
        start = (sp[1]-100, sp[0]-20)
        end = (start[0] + ptLen, start[1])
        #原始图像
        cv.line(inputImg, start, end, (0, 0, 255))
        cv.putText(inputImg, '500um', (start[0], start[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        #cv.imshow("inputImg", inputImg)
        cv.imwrite(newFileFn, inputImg)


    '''
    * 参考文档： https://blog.csdn.net/sinat_36458870/article/details/78825571
    #寻找边缘算法，待优化
    '''
    def proc_algo_vis_find_max_edge(self, refRadInUm, inputImg):
        #噪声处理过程
        new = np.zeros(inputImg.shape, np.uint8)    
        #Gray transaction: 灰度化
        for i in range(new.shape[0]):  #Axis-y/height/Rows
            for j in range(new.shape[1]):
                (b,g,r) = inputImg[i,j]
                #加权平均法
                new[i,j] = int(0.3*float(b) + 0.59*float(g) + 0.11*float(r))&0xFF
        #Middle value filter: 中值滤波
        blur= cv.medianBlur(new, 5)
        midGray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
        #Adaptive bin-translation: 自适应二值化
        binGray = cv.adaptiveThreshold(midGray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 43, 5)   # ADAPTIVE_THRESH_MEAN_C ADAPTIVE_THRESH_GAUSSIAN_C
        binRes= cv.GaussianBlur(binGray, (5,5), 1.5) #medianBlur
        #cv.imshow('Adaptive Bin', binRes)
        corImg = cv.cvtColor(binRes, cv.COLOR_GRAY2BGR)
        #高斯模糊,降低噪声  
        blurred = cv.GaussianBlur(corImg,(3, 3), 0)  
        #灰度图像  
        gray=cv.cvtColor(blurred, cv.COLOR_RGB2GRAY)  
        #图像梯度  
        xgrad=cv.Sobel(gray, cv.CV_16SC1, 1, 0)   #cv.CV_32F
        ygrad=cv.Sobel(gray, cv.CV_16SC1, 0, 1)  
        #计算边缘  
        #50和150参数必须符合1：3或者1：2  
        edge_output=cv.Canny(xgrad, ygrad, 50, 100)  
        #cv.imshow("edge", edge_output)
        _, contours, _ = cv.findContours(edge_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        #Output graphic: 输出图形
        outputImg = cv.cvtColor(edge_output, cv.COLOR_GRAY2BGR)
        mask = np.zeros((edge_output.shape[0]+2, edge_output.shape[1]+2), np.uint8)
        mask[:] = 1
        maxC = ''
        #求最大弧长
        arcLenMax = 0
        for c in contours:
            arcLen = cv.arcLength(c, False)
            #cArea = cv.contourArea(c)
            if (arcLen > arcLenMax):
                maxC = c
                arcLenMax = arcLen
        #print("arcLenMax = ", arcLenMax)
        # compute the center of the contour
        M = cv.moments(maxC)
        cX = int(M["m10"] / (M["m00"]+0.01))
        cY = int(M["m01"] / (M["m00"]+0.01))
        #4th method: 第四种方法
        rect = cv.minAreaRect(maxC)
        width, height = rect[1]
        if (width > height):
            tmp = width
            width = height
            height = tmp
        cE = width / (height+0.001)
        cE = round(cE, 2)
        cv.drawContours(outputImg, maxC, -1, (0, 0, 255), 2)                    
        cv.putText(outputImg, str(cE), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        #画最小外接框
        box = cv.boxPoints(rect)
        box = np.int0(box)
        cv.drawContours(outputImg, [box], -1, (0, 0, 255), 1)
        
        #cv.imshow("result", outputImg)  
        newRadians = (height * height / (4 * width) + width)/2
        #print("newRadians =%d, width/height=%d/%d" % (newRadians, width, height))
        #newRadians = height * math.sqrt(1 + height*height/4/width/width)/2
        baseLine = newRadians/refRadInUm
        return arcLenMax, baseLine, outputImg




    '''
    #
    #
    #CLASSFICATION: 分类
    #
    #Classified processing: 分类总处理
    #outCtrlFlag: 控制输出方式，是否直接使用fileNukeName而不增加文件名字选项
    #addupSet: 是否叠加文字输出
    #
    #
    '''
    def func_vision_worm_clasification(self, fileName, fileNukeName, outCtrlFlag, addupSet):
        #Reading file: 读取文件
        if (os.path.exists(fileName) == False):
            errStr = "L2VISCFY: File %s not exist!" % (fileName)
            self.medErrorLog(errStr);
            print("L2VISCFY: File %s not exist!" % (fileName))
            return -1,fileName,str(NULL);
        try:
            inputImg = cv.imread(fileName)
        except Exception as err:
            print("L2VISCFY: Read file error, errinfo = ", str(err))
            return -2;

        #Processing procedure: 处理过程
        binImg = self.proc_vision_worm_binvalue(inputImg)
        nfImg = self.proc_vision_worm_remove_noise(binImg)
        outputImg, outText = self.func_vision_worm_find_contours(nfImg, inputImg, addupSet)
        if (outCtrlFlag == True):
            outputFn = fileNukeName
        else:
            outputFn = GLCFG_PAR_OFC.PIC_MIDDLE_PATH + '/' + "result_" + fileNukeName
        cv.imwrite(outputFn, outputImg)
            
        #Save log record: 存储干活的log记录
        f = open(GL_CEBS_VISION_CLAS_RESULT_FILE_NAME_SET, "a+")
        a = '[%s], vision worm classification ones, save result as [%s] with output [%s].\n' % (time.asctime(), outputFn, str(outText))
        f.write(a)
        f.flush()
        f.close()
        #Show result or not: 根据指令，是否显示文件
        cv.destroyAllWindows()
        return 1,outputFn,str(outText)

    def proc_vision_worm_binvalue(self, img):
        new = np.zeros(img.shape, np.uint8)
        #Gray transaction: 灰度化
        for i in range(new.shape[0]):  #Axis-y/height/Rows
            for j in range(new.shape[1]):
                (b,g,r) = img[i,j]
                #加权平均法
                new[i,j] = int(0.3*float(b) + 0.59*float(g) + 0.11*float(r))&0xFF
        #Middle value filter: 中值滤波
        blur= cv.medianBlur(new, 5)
        midGray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
        #cv.imshow('Middle Blur', midGray)
        #Adaptive bin-translation: 自适应二值化
        binGray = cv.adaptiveThreshold(midGray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 43, 5)   # ADAPTIVE_THRESH_MEAN_C ADAPTIVE_THRESH_GAUSSIAN_C
        binRes= cv.GaussianBlur(binGray, (5,5), 1.5) #medianBlur
        #cv.imshow('Adaptive Bin', binRes)
        return binRes;
    
    def proc_vision_worm_remove_noise(self, img):
        #Enlarge + Erosion: shape translation 膨胀+腐蚀等形态学变化  
        kerne1 = np.ones((7, 7), np.uint8)  
        img_erosin = cv.erode(img, kerne1, iterations=1)
        #2nd time mid-value filter: 再次中值滤波
        midFilter= cv.medianBlur(img_erosin, 5)
        #Fix bin-value: 固定二值化
        ret, binImg = cv.threshold(midFilter, 130, 255, cv.THRESH_BINARY)
        #cv.imshow("img_erosin and Noise removal", binImg)
        return binImg;
    
    #https://www.cnblogs.com/llfisher/p/6557611.html
    #https://www.cnblogs.com/nanyangzp/p/3496486.html
    #偏心率：以质心为中心，所有点到X轴的长度综合，相比Y周的长度总和，他们之间的比值。
    #圆形=1，长条就是斜率
    # E = (M20-M02+4M11)/A, Mjk = EE(x-xA)^j * (y-yA)^k, (j+k阶矩)，A为面积
    #http://wenku.baidu.com/link?url=4ZSLxGBKE3LBf2mdxDs0VJ1cjJ3hxqeORu-3mfXO23gGBqf5LyjqZ4AHFCMLeP32xEKkoj5tPsWHdvA2ovmuKiRDKN6YHFO9G7JOzBWWrMC
    
    #http://blog.csdn.net/app_12062011/article/details/51953030
    #E = sqrt(1-I^2)
    #I = (u20+u02-sqrt(4u11*u11(u20-u02)*(u20-u02))/(u20+u02+sqrt(4u11*u11(u20-u02)*(u20-u02))
    def func_vision_worm_find_contours(self, nfImg, orgImg, addupSet):
        #Init output figure
        outText = {'totalNbr':0, 'bigAlive':0, 'bigDead':0, 'middleAlive':0, 'middleDead':0, 'smallAlive':0, 'smallDead':0, 'totalAlive':0, 'totalDead':0}
        outText['totalNbr'] = 0
        outText['bigAlive'] = 0
        outText['bigDead'] = 0
        outText['middleAlive'] = 0
        outText['middleDead'] = 0
        outText['smallAlive'] = 0
        outText['smallDead'] = 0
        outText['totalAlive'] = 0
        outText['totalDead'] = 0
        
        #Searching out-form shape: 找到轮廓
        _, contours, hierarchy = cv.findContours(nfImg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) #RETR_TREE, RETR_CCOMP
        #contours = contours[0] if imutils.is_cv() else contours[1]
        
        #Output graphic: 输出图形
        outputImg = cv.cvtColor(nfImg, cv.COLOR_GRAY2BGR)
        mask = np.zeros((orgImg.shape[0]+2, orgImg.shape[1]+2), np.uint8)
        mask[:] = 1
        #Analysis one by one: 分别分析
        for c in contours:
            #External retangle: 外矩形框
            (x,y,w,h)=cv.boundingRect(c)
            pointx=x+w/2
            pointy=y+h/2
            # compute the center of the contour
            M = cv.moments(c)
            cX = int(M["m10"] / (M["m00"]+0.01))
            cY = int(M["m01"] / (M["m00"]+0.01))
            seed_point = (cX, cY)
            #Shape square: 轮廓面积
            cArea = cv.contourArea(c)
            #Shape length: 轮廓弧长
            cPerimeter = cv.arcLength(c,True)
            
            #4th method: 第四种方法
            rect = cv.minAreaRect(c)
            #width / height: 长宽,总有 width>=height  
            width, height = rect[1]
            if (width > height):
                cE = height / (width+0.001)
            else:
                cE = width / (height+0.001)
            cE = round(cE, 2)
    
            #Finally not use flood algorithms: 最终决定不采用flood算法
            #print(self.WORM_CLASSIFY_base)
            if cArea < self.WORM_CLASSIFY_base:
                pass
            elif cArea < self.WORM_CLASSIFY_small2mid:
                outText['totalNbr'] +=1
                #cv.floodFill(outputImg, mask, seed_point,(0,0,255))
                cv.drawContours(outputImg, c, -1, (0,0,255), 2)  
                if (cE < 0.5):
                    outText['smallDead'] +=1
                    outText['totalDead'] +=1
                else:
                    outText['smallAlive'] +=1
                    outText['totalAlive'] +=1               
                cv.putText(outputImg, str(cE), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            elif cArea < self.WORM_CLASSIFY_mid2big:
                outText['totalNbr'] +=1
                #cv.floodFill(outputImg, mask, seed_point,(0,255,0))  
                cv.drawContours(outputImg, c, -1, (0,255,0), 2)
                if (cE < 0.5):
                    outText['middleDead'] +=1
                    outText['totalDead'] +=1
                else:
                    outText['middleAlive'] +=1
                    outText['totalAlive'] +=1            
                cv.putText(outputImg, str(cE), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            elif cArea < self.WORM_CLASSIFY_big2top:
                outText['totalNbr'] +=1
                #cv.floodFill(outputImg, mask, seed_point,(255,0,0))  
                cv.drawContours(outputImg, c, -1, (255,0,0), 2)
                if (cE < 0.5):
                    outText['bigDead'] +=1
                    outText['totalDead'] +=1
                else:
                    outText['bigAlive'] +=1
                    outText['totalAlive'] +=1                        
                cv.putText(outputImg, str(cE), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        #叠加统计结果
        if (addupSet == True):
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(outputImg, str("XHT: " + str(outText)), (10, 30), font, 0.7, (0, 0, 255), 2, cv.LINE_AA)
        return outputImg, outText;




    '''
    #
    #操控算法的核心参数有这么些，需要通过训练得到理想的结果
    #
    #tarBlkSize, =41, 必须是奇数，指示高斯自适应二值化的分块大小，通常跟目标的尺寸大小差不多
    #cAreaMin, =100, 最小面积，通过这个方式去掉噪点
    #cAreaMax, =500, 最大面积，通过这个方式去掉不可靠的垃圾
    #ceMin, =20(NF2定标), 圆形门限
    #叠加面积属性
    #
    '''
    #细胞识别函数
    def func_vision_flu_cell_count(self, fileName, fileNukeName, tarBlkSize, cAreaMin, cAreaMax, ceMin, addupSet):
        #处理参数，确保奇数性质的参数
        if ((tarBlkSize//2)*2) == tarBlkSize:
            tarBlkSize +=1
        ceMin = ceMin/100
        #使用LOCAL方式进行叠加，不再使用全局属性，简化处理
        outputText = {'totalNbr':0, 'validNbr':0}
        
        #Reading file: 读取文件
        if (os.path.exists(fileName) == False):
            errStr = "L2VISCFY: File %s not exist!" % (fileName)
            self.medErrorLog(errStr);
            print("L2VISCFY: File %s not exist!" % (fileName))
            return -1;
        try:
            inputImg = cv.imread(fileName)
        except Exception as err:
            print("L2VISCFY: Read file error, errinfo = ", str(err))
            return -2;
        #正常干活过程
        #第一步：灰度图像
        new = np.zeros(inputImg.shape, np.uint8)
        #Gray transaction: 灰度化
        for i in range(new.shape[0]):  #Axis-y/height/Rows
            for j in range(new.shape[1]):
                (b,g,r) = inputImg[i,j]
                #加权平均法
                new[i,j] = int(0.3*float(b) + 0.59*float(g) + 0.11*float(r))&0xFF
        #Middle value filter: 中值滤波
        blur= cv.medianBlur(new, 5)
        midGray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
        #Adaptive bin-translation: 自适应二值化
        binGray = cv.adaptiveThreshold(midGray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, tarBlkSize, 0)   # ADAPTIVE_THRESH_MEAN_C ADAPTIVE_THRESH_GAUSSIAN_C
        binRes= cv.GaussianBlur(binGray, (5,5), 1.5) #medianBlur
        
        #第二步，去噪声
        kerne1 = np.ones((7, 7), np.uint8)  
        img_erosin = cv.erode(binRes, kerne1, iterations=1)
        #2nd time mid-value filter: 再次中值滤波
        midFilter= cv.medianBlur(img_erosin, 5)
        #Fix bin-value: 固定二值化
        ret, binImg = cv.threshold(midFilter, 130, 255, cv.THRESH_BINARY)
        
        #第三步，寻找外框
        #Searching out-form shape: 找到轮廓
        _, contours, hierarchy = cv.findContours(binImg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) #RETR_TREE, RETR_CCOMP
        
        #Output graphic: 输出图形
        outputImg = cv.cvtColor(binImg, cv.COLOR_GRAY2BGR)
        mask = np.zeros((inputImg.shape[0]+2, inputImg.shape[1]+2), np.uint8)
        mask[:] = 1
        #Analysis one by one: 分别分析
        for c in contours:
            outputText['totalNbr'] +=1
            M = cv.moments(c)
            cX = int(M["m10"] / (M["m00"]+0.01))
            cY = int(M["m01"] / (M["m00"]+0.01))
            cArea = cv.contourArea(c)
            rect = cv.minAreaRect(c)
            #width / height: 长宽,总有 width>=height  
            width, height = rect[1]
            if (width > height):
                cE = height / (width+0.001)
            else:
                cE = width / (height+0.001)
            cE = round(cE, 2)

            #分类
            if (cArea < cAreaMin) or (cE < ceMin) or (cArea > cAreaMax):
                pass
            else:
                outputText['validNbr'] +=1
                cv.drawContours(outputImg, c, -1, (0,0,255), 2)
                cv.putText(outputImg, str(cArea), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        #整体叠加输出
        if (addupSet == True):
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(outputImg, str("XHT: " + str(outputText)), (10, 30), font, 0.7, (0, 0, 255), 2, cv.LINE_AA)
        
        #最后一步，反馈结果
        outputFn = fileNukeName
        cv.imwrite(outputFn, outputImg)

        #Save log record: 存储干活的log记录
        f = open(GL_CEBS_VISION_CLAS_RESULT_FILE_NAME_SET, "a+")
        a = '[%s], Flu cell counting, save result as [%s] with output [%s].\n' % (time.asctime(), outputFn, str(outputText))
        f.write(a)
        f.flush()
        f.close()
        
        #CLEAN SITES ENV.
        cv.destroyAllWindows()
        return outputText['validNbr']













#搜索摄像头进程：调用的win32com必须在进程里面干活，所以只能采用这种创造进程的方式干搜索设备号
class clsCamDevHdl():
    def __init__(self, ):
        pass

    #搜索摄像头
    def dhSearchRunCam(self):
        pCamRead = Process(target=self.dhFetchUsbCamId, args=())
        pCamRead.start()
        pCamRead.join(5)
        #读取文件，得到camId
        with open('tempCamId.txt','r') as f:
            a = f.read()
        camId = int(a)
        return camId
        
    #独立读取的进程函数
    #进程跟咱们的文件交互，这里投机取巧采用了临时文件交换，不然内存交互找不到简易的方式
    def dhFetchUsbCamId(self):
        wmi = win32com.client.GetObject("winmgmts:")
        camId = -2
        for usb in wmi.InstancesOf ("win32_usbcontrollerdevice"):
            if "VID_0547&PID_6010" in usb.Dependent:
                searchText = "VID_0547&PID_6010"
                indexStart = usb.Dependent.find(searchText)
                textLen = len(searchText)
                textContent = usb.Dependent[indexStart+textLen:]
                result={}
                step=0;
                for item in textContent.split('&'):
                    result[step] = item
                    step+=1
                try:
                    camId = int(result[2])
                except Exception:
                    camId = -1
        #存入临时文件
        f = open("tempCamId.txt", "w+")
        a = ("%d" % (camId))
        f.write(a)
        f.flush()
        f.close()










