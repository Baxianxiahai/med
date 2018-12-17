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
from PkgVmHandler.ModVmCfg import *
from PkgVmHandler.ModVmLayer import *
from PkgCebsHandler.ModCebsCom import *
from PkgCebsHandler.ModCebsCfg import *
from PkgVmHandler.ModVmConsole import *

#from cebsTkL4Ui import *

class tupTaskVision(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    #主界面，干活拍照
    _STM_MAIN_UI_ACT = 4
    #校准模式下图像直接读取
    _STM_CALIB_UI_ACT = 5
    #参数模式下图像直接读取
    _STM_GPAR_UI_ACT = 6
    
    #摄像头初始化之后的对象指针
    capInit = ''

    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_VISION, taskName="TASK_VISION", glTabEntry=glPar)
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(TUP_TASK_ID_VISION, self)
        self.capInit = ''
        self.HST_VISION_WORM_CLASSIFY_base = ModCebsCom.GLVIS_PAR_OFC.SMALL_LOW_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_small2mid = ModCebsCom.GLVIS_PAR_OFC.SMALL_MID_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_mid2big = ModCebsCom.GLVIS_PAR_OFC.MID_BIG_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_big2top = ModCebsCom.GLVIS_PAR_OFC.BIG_UPPER_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_pic_filepath = ModCebsCom.GLCFG_PAR_OFC.PIC_MIDDLE_PATH + '/'
        self.HST_VISION_WORM_CLASSIFY_pic_filename = "1.jpg"
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output = {'totalNbr':0, 'bigAlive':0, 'bigDead':0, 'middleAlive':0, 'middleDead':0, 'smallAlive':0, 'smallDead':0, 'totalAlive':0, 'totalDead':0}
        self.fsm_set(TUP_STM_NULL)

        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        
        #通知界面切换
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_MAIN_UI_SWITCH, self.fsm_msg_main_ui_switch_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_UI_SWITCH, self.fsm_msg_calib_ui_switch_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_GPAR_UI_SWITCH, self.fsm_msg_gpar_ui_switch_rcv_handler)
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
        
        #切换状态机
        self.fsm_set(TUP_STM_INIT)
        #START TASK
        self.task_run()
    
    #摄像头初始化
    def fsm_msg_init_rcv_handler(self, msgContent):
        #全局搜索摄像头
        p = clsCamDevHdl()
        ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR = p.dhSearchRunCam()
        res = "L2VISCAP: Valid camera number = " + str(ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR)     
        self.funcVisionLogTrace(str(res))
        #INIT
        if (ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR < 0):
            self.funcVisionErrTrace("L2VISCAP: Camera not yet installed, init error!");
            return TUP_FAILURE;
        #正确的情况
        self.capInit = cv.VideoCapture(ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_NBR) #CHECK WITH ls /dev/video*　RESULT
        self.capInit.set(3, ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_RES_WITDH)
        self.capInit.set(4, ModCebsCom.GLVIS_PAR_OFC.VISION_CAMBER_RES_HEIGHT)
        if not self.capInit.isOpened():
            self.capInit.release()
            cv.destroyAllWindows()
            self.funcVisionErrTrace("L2VISCAP: Camera not installed, but open error!");
            return TUP_FAILURE;
        else:
            self.fsm_set(self._STM_ACTIVE)
            self.funcVisionLogTrace("L2VISCAP: Camera open successful!");
            return TUP_SUCCESS;

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
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

    def fsm_msg_refresh_par_rcv_handler(self, msgContent):
        self.funcVisRefreshPar();
        return TUP_SUCCESS;

    def funcVisionLogTrace(self, myString):
        if (self.state == self._STM_MAIN_UI_ACT):
            self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MAIN, myString)
        elif (self.state == self._STM_CALIB_UI_ACT):
            self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_CALIB, myString)
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
    
    
    #传递文件回去给显示界面
    #暂时没找到其它更好的办法，所以只能采用文件传输的方式
    #尝试使用去全局变量传递视频图像对象
    def fsm_msg_calib_video_display_req_rcv_handler(self, msgContent):
        mbuf={}
        if self.capInit == '':
            mbuf['res'] = -1
            self.msg_send(TUP_MSGID_CALIB_VDISP_RESP, TUP_TASK_ID_CALIB, mbuf)
            return TUP_FAILURE;
        #CAPTURE PICTURE
        ret, outFrame = self.funcCapQtFrame()        
        if (ret <0):
            mbuf['res'] = -2
            self.msg_send(TUP_MSGID_CALIB_VDISP_RESP, TUP_TASK_ID_CALIB, mbuf)
            return TUP_FAILURE;
        #正确处理过程：这是主要通过全局变量传递的复杂数据对象
        #其它的COM数据主要还是一些简单的共享参数信息
        ModCebsCom.GLVIS_PAR_OFC.CALIB_VDISP_OJB = outFrame
        mbuf['res'] = 1
        mbuf['ComObj'] = True
        #本来是通过文件读取，目前改为了对象指针共享，效率要高些
        #cv.imwrite("tempCalibDisp.jpg", outFrame)
        #mbuf['fileName'] = "tempCalibDisp.jpg"
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
        ret, outFrame = self.funcCap1Frame()
        if (ret <0):
            self.funcVisionErrTrace("VISION: capture picture error!")
            return TUP_FAILURE;
        cv.imwrite(fileName, outFrame)
        self.funcVisionLogTrace("VISION: Capture and save file, batch=%d, fileNbr=%d, fn=%s" % (ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, holeNbr, fileName));
        return TUP_SUCCESS;
    
    #主界面模式下拍照
    def fsm_msg_main_ctrs_pic_cap_req_rcv_handler(self, msgContent):
        fnPic = msgContent['fnPic']
        fnScale = msgContent['fnScale']
        fnVideo = msgContent['fnVideo']
        vdCtrl = msgContent['vdCtrl']
        res = self.funcPicVidCapAndSaveFile(fnPic, fnScale, fnVideo, vdCtrl);
        mbuf={}
        mbuf['res'] = res
        self.msg_send(TUP_MSGID_CTRS_PIC_CAP_RESP, TUP_TASK_ID_CTRL_SCHD, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_main_ctrs_flu_cap_req_rcv_handler(self, msgContent):
        mbuf={}
        self.msg_send(TUP_MSGID_CTRS_FLU_CAP_RESP, TUP_TASK_ID_CTRL_SCHD, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_main_ctrs_pic_clfy_req_rcv_handler(self, msgContent):
        #识别算法
        fileName = msgContent['fileName']
        fileNukeName = msgContent['fileNukeName']
        ctrl = msgContent['ctrl']
        self.func_vision_worm_clasification(fileName, fileNukeName, ctrl);
        mbuf={}
        self.msg_send(TUP_MSGID_CRTS_PIC_CLFY_RESP, TUP_TASK_ID_CTRL_SCHD, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_main_ctrs_flu_clfy_req_rcv_handler(self, msgContent):
        mbuf={}
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
        self.func_vision_worm_clasification(picFile, 'tempPic.jpg', True)
        if (os.path.exists('tempPic.jpg') == False):
            mbuf['res'] = -2
            self.msg_send(TUP_MSGID_GPAR_PIC_TRAIN_RESP, TUP_TASK_ID_GPAR, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'tempPic.jpg'
        self.msg_send(TUP_MSGID_GPAR_PIC_TRAIN_RESP, TUP_TASK_ID_GPAR, mbuf)
        return TUP_SUCCESS;


    '''
    SERVICE PART: 业务部分的函数，功能处理函数
    '''
    #输出OpenCV可以识别的格式 => 为了本地存储只用
    def funcCap1Frame(self):
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
    def funcCapQtFrame(self):
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
    def funcPicVidCapAndSaveFile(self, fnPic, fnScale, fnVideo, vdCtrl):
        if not self.capInit.isOpened():
            self.funcVisionErrTrace("L2VISCAP: Cannot open webcam!")
            self.capInit.release()
            cv.destroyAllWindows()            
            return -1;
        width = int(self.capInit.get(cv.CAP_PROP_FRAME_WIDTH) + 0.5)
        height = int(self.capInit.get(cv.CAP_PROP_FRAME_HEIGHT) + 0.5)
        fps = 20
        ret, frame = self.capInit.read()
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
            if ModCebsCom.GLVIS_PAR_OFC.PIC_SCALE_ENABLE_FLAG == True:
                self.algoVisGetRadians(ModCebsCom.GLPLT_PAR_OFC.med_get_radians_len_in_us(), fnPic, fnScale)
        if (ret == True) and (vdCtrl == True):
            #Video capture with 3 second
            fourcc = cv.VideoWriter_fourcc(*'mp4v')  #mp4v(.mp4), XVID(.avi)
            out = cv.VideoWriter(fnVideo, fourcc, fps, (width, height))
            cnt = 0
            targetCnt = fps * ModCebsCom.GLVIS_PAR_OFC.CAPTURE_DUR_IN_SEC
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

    #之前的函数，待删去
    #截获图像
#     def funcVisionCapture(self, batch, fileNbr, forceFlag):
#         if not self.capInit.isOpened():
#             self.funcVisionErrTrace("L2VISCAP: Cannot open webcam!, Batch/Nbr=%d/%d" % (batch, fileNbr))
#             self.capInit.release()
#             cv.destroyAllWindows()            
#             return -1;
#         width = int(self.capInit.get(cv.CAP_PROP_FRAME_WIDTH) + 0.5)
#         height = int(self.capInit.get(cv.CAP_PROP_FRAME_HEIGHT) + 0.5)
#         fps = 20
#         time.sleep(1)
#         ret, frame = self.capInit.read()
#         if (ret == True):
#             frame = cv.flip(frame, 1)#Operation in frame
#             frame = cv.resize(frame, None, fx=1, fy=1, interpolation=cv.INTER_AREA)
#             #白平衡算法
#             B,G,R = cv.split(frame)
#             bMean = cv.mean(B)
#             gMean = cv.mean(G)
#             rMean = cv.mean(R)
#             print("L2VISCAP: Mean B/G/R = %d/%d/%d" %(bMean[0], gMean[0], rMean[0]))
#             kb = (bMean[0] + gMean[0] + rMean[0])/(3*bMean[0]+0.0001)
#             kg = (bMean[0] + gMean[0] + rMean[0])/(3*gMean[0]+0.0001)
#             kr = (bMean[0] + gMean[0] + rMean[0])/(3*rMean[0]+0.0001)
#             B = B * kb
#             G = G * kg
#             R = R * kr
#             outputFrame = cv.merge([B, G, R])
#             fileName = clsL1_ConfigOpr.combineFileNameWithDir(batch, fileNbr)
#             cv.imwrite(fileName, outputFrame)
#             scaleFn = clsL1_ConfigOpr.combineScaleFileNameWithDir(batch, fileNbr)
#             if ModCebsCom.GLVIS_PAR_OFC.PIC_SCALE_ENABLE_FLAG == True:
#                 self.algoVisGetRadians(ModCebsCom.GLPLT_PAR_OFC.med_get_radians_len_in_us(), fileName, scaleFn)
#         if (forceFlag == True):
#             return 1;
#         if (ret == True) and (ModCebsCom.GLVIS_PAR_OFC.CAPTURE_ENABLE == True):
#             #Video capture with 3 second
#             fourcc = cv.VideoWriter_fourcc(*'mp4v')  #mp4v(.mp4), XVID(.avi)
#             fileNameVideo = clsL1_ConfigOpr.combineFileNameVideoWithDir(batch, fileNbr)
#             out = cv.VideoWriter(fileNameVideo, fourcc, fps, (width, height))
#             cnt = 0
#             targetCnt = fps * ModCebsCom.GLVIS_PAR_OFC.CAPTURE_DUR_IN_SEC
#             while self.capInit.isOpened():
#                 cnt += 1
#                 ret, frame = self.capInit.read()
#                 if ret:
#                     frame = cv.flip(frame, 0)
#                     #write the flipped frame
#                     time.sleep(1.0/fps)
#                     out.write(frame)
#                     if cnt >= targetCnt:
#                         break
#                 else:
#                     break
#             out.release()
#             return 2;
#         return 1;
      
      
    #计算弧度的方式
    #INPUT: refRadInUm, 孔半径长度，um单位
    #OUTPUT: 对应比例关系
    def algoVisGetRadians(self, refRadInUm, dirFn, newFileFn):
        #Reading file: 读取文件
        if (os.path.exists(dirFn) == False):
            errStr = "L2VISCFY: File %s not exist!" % (dirFn)
            self.medErrorLog(errStr);
            print("L2VISCFY: File %s not exist!" % (dirFn))
            return;
        self.HST_VISION_WORM_CLASSIFY_pic_filename = dirFn
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
        arcLen, lenSqrRatio, resImgLU = self.algoVisFindMaxEdge(refRadInUm, imgLeftUp)
        #print("LU Length/baseline = %f/%f" % (arcLen, lenSqrRatio))
        if (arcLen < arcLenMax) and (lenSqrRatio < 1) and (lenSqrRatio > 0.1) and (arcLen > arcSave):
            flagIndex = 1
            arcSave = arcLen
            stdRatio = lenSqrRatio
        #PART2
        arcLen, lenSqrRatio, resImgRU = self.algoVisFindMaxEdge(refRadInUm, imgRightUp)
        #print("RU Length/baseline = %f/%f" % (arcLen, lenSqrRatio))
        if (arcLen < arcLenMax) and (lenSqrRatio < 1) and (lenSqrRatio > 0.1) and (arcLen > arcSave):
            flagIndex = 2
            arcSave = arcLen
            stdRatio = lenSqrRatio
        #PART3
        arcLen, lenSqrRatio, resImgLB = self.algoVisFindMaxEdge(refRadInUm, imgLeftBot)
        #print("LB Length/baseline = %f/%f" % (arcLen, lenSqrRatio))
        if (arcLen < arcLenMax) and (lenSqrRatio < 1) and (lenSqrRatio > 0.1) and (arcLen > arcSave):
            flagIndex = 3
            arcSave = arcLen
            stdRatio = lenSqrRatio
        #PART4
        arcLen, lenSqrRatio, resImgRB = self.algoVisFindMaxEdge(refRadInUm, imgRightBot)
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
    def algoVisFindMaxEdge(self, refRadInUm, inputImg):
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
    CLASSFICATION: 分类
    '''
    def funcVisRefreshPar(self):
        self.HST_VISION_WORM_CLASSIFY_base = ModCebsCom.GLVIS_PAR_OFC.SMALL_LOW_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_small2mid = ModCebsCom.GLVIS_PAR_OFC.SMALL_MID_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_mid2big = ModCebsCom.GLVIS_PAR_OFC.MID_BIG_LIMIT;
        self.HST_VISION_WORM_CLASSIFY_big2top = ModCebsCom.GLVIS_PAR_OFC.BIG_UPPER_LIMIT;
    
    '''
    * 核心的识别函数，其它任务调用的主入口
    *
    *    用于普通白光照片的识别处理过程
    *
    '''    
#     def funcVisionNormalClassifyProc(self):
#         self.funcVisRefreshPar()
#         batch, fileNbr = self.findNormalUnclasFileBatchAndNbr();
#         if (batch < 0):
#             ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT = 0;
#             self.funcVisionLogTrace("L2VISCFY: Picture classification not finished: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
#             self.updateCtrlCntInfo();
#             return -1;
#         fileName = self.getStoredFileName(batch, fileNbr);
#         fileNukeName = self.getStoredFileNukeName(batch, fileNbr)
#         if (fileName == None) or (fileNukeName == None):
#             ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT = 0;
#             self.funcVisionLogTrace("L2VISCFY: Picture classification finished: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
#             self.updateCtrlCntInfo();
#             return -2;
#         #REAL PROCESSING PROCEDURE
#         print("L2VISCFY: Normal picture batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
#         self.func_vision_worm_clasification(fileName, fileNukeName, False);
#         ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT -= 1;
#         #Update classified files
#         self.updateUnclasFileAsClassified(batch, fileNbr);
#         self.funcVisionLogTrace("L2VISCFY: Normal picture classification finished, remaining NUMBRES=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
#         self.updateCtrlCntInfo();
#         return 1;
        
#     def func_vision_worm_input_processing(self, inputStr):
#         try:
#             if ((inputStr['cfBase'] < inputStr['cfSmall2MidIndex']) and (inputStr['cfSmall2MidIndex'] < inputStr['cfMid2BigIndex']) and (inputStr['cfMid2BigIndex'] < inputStr['cfBig2TopIndex'])):
#                 self.HST_VISION_WORM_CLASSIFY_base = inputStr['cfBase'];
#                 self.HST_VISION_WORM_CLASSIFY_small2mid = inputStr['cfSmall2MidIndex'];
#                 self.HST_VISION_WORM_CLASSIFY_mid2big = inputStr['cfMid2BigIndex'];
#                 self.HST_VISION_WORM_CLASSIFY_big2top = inputStr['cfBig2TopIndex'];
#                 self.HST_VISION_WORM_CLASSIFY_pic_filename = inputStr['fileName'];
#             else:
#                 print("L2VISCFY: func_vision_worm_input_processing on input error!")
#         except Exception as err:
#             text = "L2VISCFY: func_vision_worm_input_processing on input error = %s" % str(err)
#             print("L2VISCFY: Input error = ", text);


    def func_vision_worm_binvalue_proc(self, img):
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
    
    def func_vision_worm_remove_noise_proc(self, img):
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
    def func_vision_worm_find_contours(self, nfImg, orgImg):
        #Init output figure
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalNbr'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['bigAlive'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['bigDead'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['middleAlive'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['middleDead'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['smallAlive'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['smallDead'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalAlive'] = 0
        self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalDead'] = 0
        
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
            #print(self.HST_VISION_WORM_CLASSIFY_base)
            if cArea < self.HST_VISION_WORM_CLASSIFY_base:
                pass
            elif cArea < self.HST_VISION_WORM_CLASSIFY_small2mid:
                self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalNbr'] +=1
                #cv.floodFill(outputImg, mask, seed_point,(0,0,255))
                cv.drawContours(outputImg, c, -1, (0,0,255), 2)  
                if (cE < 0.5):
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['smallDead'] +=1
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalDead'] +=1
                else:
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['smallAlive'] +=1
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalAlive'] +=1               
                cv.putText(outputImg, str(cE), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            elif cArea < self.HST_VISION_WORM_CLASSIFY_mid2big:
                self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalNbr'] +=1
                #cv.floodFill(outputImg, mask, seed_point,(0,255,0))  
                cv.drawContours(outputImg, c, -1, (0,255,0), 2)
                if (cE < 0.5):
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['middleDead'] +=1
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalDead'] +=1
                else:
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['middleAlive'] +=1
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalAlive'] +=1            
                cv.putText(outputImg, str(cE), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            elif cArea < self.HST_VISION_WORM_CLASSIFY_big2top:
                self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalNbr'] +=1
                #cv.floodFill(outputImg, mask, seed_point,(255,0,0))  
                cv.drawContours(outputImg, c, -1, (255,0,0), 2)
                if (cE < 0.5):
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['bigDead'] +=1
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalDead'] +=1
                else:
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['bigAlive'] +=1
                    self.HST_VISION_WORM_CLASSIFY_pic_sta_output['totalAlive'] +=1                        
                cv.putText(outputImg, str(cE), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        #叠加统计结果
        if (ModCebsCom.GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET == True):
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(outputImg, str(self.HST_VISION_WORM_CLASSIFY_pic_sta_output), (10, 30), font, 0.7, (0, 0, 255), 2, cv.LINE_AA)
        return outputImg;

    #Classified processing: 分类总处理
    #outCtrlFlag: 控制输出方式，是否直接使用fileNukeName而不增加文件名字选项
    def func_vision_worm_clasification(self, fileName, fileNukeName, outCtrlFlag):
        #Reading file: 读取文件
        if (os.path.exists(fileName) == False):
            errStr = "L2VISCFY: File %s not exist!" % (fileName)
            self.medErrorLog(errStr);
            print("L2VISCFY: File %s not exist!" % (fileName))
            return;
        self.HST_VISION_WORM_CLASSIFY_pic_filename = fileName
        try:
            inputImg = cv.imread(fileName)
        except Exception as err:
            print("L2VISCFY: Read file error, errinfo = ", str(err))
            return;

        #Processing procedure: 处理过程
        binImg = self.func_vision_worm_binvalue_proc(inputImg)
        nfImg = self.func_vision_worm_remove_noise_proc(binImg)
        outputImg = self.func_vision_worm_find_contours(nfImg, inputImg)
        if (outCtrlFlag == True):
            outputFn = fileNukeName
        else:
            outputFn = self.HST_VISION_WORM_CLASSIFY_pic_filepath + "result_" + fileNukeName
        print("L2VISCFY: OutputFn = %s, nuke name = %s" %(outputFn, fileNukeName))
        cv.imwrite(outputFn, outputImg)
            
        #Save log record: 存储干活的log记录
        f = open(ModCebsCom.GL_CEBS_VISION_CLAS_RESULT_FILE_NAME_SET, "a+")
        a = '[%s], vision worm classification ones, save result as [%s] with output [%s].\n' % (time.asctime(), outputFn, str(self.HST_VISION_WORM_CLASSIFY_pic_sta_output))
        f.write(a)
        f.close()
        
        #Show result or not: 根据指令，是否显示文件
        cv.destroyAllWindows()

    '''
    * 核心的识别函数，其它任务调用的主入口
    *
    *    用于荧光照片的识别处理过程
    *
    '''    
#     def funcVisionFluClassifyProc(self):
#         self.funcVisRefreshPar()
#         batch, fileNbr = self.findFluUnclasFileBatchAndNbr();
#         print("batch/FileNbr=%d/%d" % (batch, fileNbr))
#         if (batch < 0):
#             ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT = 0;
#             self.funcVisionLogTrace("L2VISCFY: Picture flu classification not finished: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT))
#             self.updateCtrlCntInfo();
#             return;
#         fileName = self.getStoredFileName(batch, fileNbr);
#         fileNukeName = self.getStoredFileNukeName(batch, fileNbr)
#         if (fileName == None) or (fileNukeName == None):
#             ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT = 0;
#             self.funcVisionLogTrace("L2VISCFY: Picture flu classification finished: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT))
#             self.updateCtrlCntInfo();
#             return;
#         #REAL PROCESSING PROCEDURE
#         print("L2VISCFY: Flu picture batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
#         self.algoVisFluWormCaculate(fileName, fileNukeName);
#         ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT -= 1;
#         #Update classified files
#         self.updateUnclasFileAsClassified(batch, fileNbr);
#         self.funcVisionLogTrace("L2VISCFY: Flu picture classification finished, remaining NUMBRES=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT))
#         self.updateCtrlCntInfo();
#         return;
#     
#     #荧光处理算法过程
#     def algoVisFluWormCaculate(self, fileName, fileNukeName):
#         self.funcVisionLogTrace("L2VISCFY: Flu picture classification simulation algorithms demo, to be finsihed!")



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










