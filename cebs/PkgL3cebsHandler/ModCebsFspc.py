'''
Created on 2019年1月22日

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
import multiprocessing
from   ctypes import c_uint8
from ctypes import *
import win32com.client  #pip install pyWin32
from win32com.client import GetObject
#import usb.core
#from   cv2 import waitKey
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from multiprocessing import Queue, Process
from _overlapped import NULL

from multiprocessing import Queue, Process

from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL1vmHandler.ModVmConsole import *
from PkgL2svrHandler.ModPicProc import *
from PkgL3cebsHandler.ModCebsCom import *
from PkgL3cebsHandler.ModCebsCfg import *
from PkgL1vmHandler import ModVmLayer


from PyQt5 import QtGui

class tupTaskFspc(tupTaskTemplate, clsL1_ConfigOpr, TupClsPicProc):
    _STM_ACTIVE = 3
    
    #模块中的局部变量
    fspcOutCt = 0;      #外部包络        c = cv.findContours
    fspcMinRect = 0;    #最小外接正方形    rect = cv.minAreaRect(c)
    fspcOutBox = 0;     #外部多边形    OutBox = cv.boxPoints(rect)
    fspcOutCtPoly = 0;  #将外包络转换为多边形 OutCtPoly = cv.convexHull(c)
    fspcCircles = 0;    #使用霍夫变换，得到的所有圆形列表清单
    fspcGdCircles = 0;  #搜索到好的圆形
    fspcCkCircles = 0;  #复核之后的圆形
    fspcValidCnt = 0;   #寻找到的圆形数量
    
    #控制前面的步伐是否做过，而且是否成功，不然后面是不能直接执行的
    fspcSucFlagS1 = False
    fspcSucFlagS2 = False
    fspcSucFlagS3 = False
    fspcSucFlagS4 = False
    fspcSucFlagS5 = False
    fspcSucFlagS6 = False
    fspcSucFlagS7 = False
    
    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_FSPC, taskName="TASK_FSPC", glTabEntry=glPar)
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_FSPC, self)
        self.fsm_set(TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_com_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_EXIT, self.fsm_com_msg_exit_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_com_msg_test_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)

        #业务处理部分
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_FSPC_CMD_S1_REQ, self.fsm_msg_cmd_s1_req_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_FSPC_CMD_S2_REQ, self.fsm_msg_cmd_s2_req_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_FSPC_CMD_S3_REQ, self.fsm_msg_cmd_s3_req_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_FSPC_CMD_S4_REQ, self.fsm_msg_cmd_s4_req_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_FSPC_CMD_S5_REQ, self.fsm_msg_cmd_s5_req_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_FSPC_CMD_S6_REQ, self.fsm_msg_cmd_s6_req_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_FSPC_CMD_S7_REQ, self.fsm_msg_cmd_s7_req_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_FSPC_CMD_SUM_REQ, self.fsm_msg_cmd_sum_req_rcv_handler)
        
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

        
    '''
    #
    #模块初始化
    #
    '''
    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;

    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_FSPC, msgContent)
        return TUP_SUCCESS;

    def funcFspcLogTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_FSPC, myString)
        #SAVE INTO MED FILE
        self.medCmdLog(str(myString))
        #PRINT to local
        self.tup_dbg_print(str(myString))
        return
    
    def funcFspcErrTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_FSPC, myString)
        #SAVE INTO MED FILE
        self.medErrorLog(str(myString));
        #PRINT to local
        self.tup_err_print(str(myString))
        return        



    '''
    #
    #SERVICE PROCESSING
    #
    '''
    def fsm_msg_cmd_s1_req_rcv_handler(self, msgContent):
        #parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(msgContent['fileName']) == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'File not exist!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s1_proc(msgContent)
        if (ret == False):
            mbuf['res'] = -2
            string = str('Error find %d' % (totalCnt))
            mbuf['errInfo'] = string
            self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf = self.proc_mbuf_fix_fill(mbuf, totalCnt, 1)
        self.funcFspcLogTrace(str("Step1 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        self.fspcSucFlagS1 = True
        return TUP_SUCCESS;

    def fsm_msg_cmd_s2_req_rcv_handler(self, msgContent):
        mbuf={}
        if (os.path.exists('fspcPicS1.jpg') == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'File not exist!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S2_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        if (self.fspcSucFlagS1 == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'Previous step not done!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S2_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s2_proc(msgContent)
        if (ret == False):
            mbuf['res'] = -2
            string = str('Error find %d' % (totalCnt))
            mbuf['errInfo'] = string
            self.msg_send(TUP_MSGID_FSPC_CMD_S2_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf = self.proc_mbuf_fix_fill(mbuf, totalCnt, 2)
        self.funcFspcLogTrace(str("Step2 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S2_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        self.fspcSucFlagS2 = True
        return TUP_SUCCESS;

    def fsm_msg_cmd_s3_req_rcv_handler(self, msgContent):
        mbuf={}
        if (os.path.exists('fspcPicS2.jpg') == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'File not exist!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        if (self.fspcSucFlagS2 == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'Previous step not done!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S2_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s3_proc(msgContent)
        if (ret == False):
            mbuf['res'] = -2
            string = str('Error find %d' % (totalCnt))
            mbuf['errInfo'] = string
            self.msg_send(TUP_MSGID_FSPC_CMD_S3_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf = self.proc_mbuf_fix_fill(mbuf, totalCnt, 3)
        self.funcFspcLogTrace(str("Step3 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S3_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        self.fspcSucFlagS3 = True
        return TUP_SUCCESS;

    def fsm_msg_cmd_s4_req_rcv_handler(self, msgContent):
        mbuf={}
        if (os.path.exists('fspcPicS3.jpg') == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'File not exist!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S4_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        if (self.fspcSucFlagS3 == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'Previous step not done!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S2_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s4_proc(msgContent)
        if (ret == False):
            mbuf['res'] = -2
            string = str('Error find %d' % (totalCnt))
            mbuf['errInfo'] = string
            self.msg_send(TUP_MSGID_FSPC_CMD_S4_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf = self.proc_mbuf_fix_fill(mbuf, totalCnt, 4)
        mbuf['findCnt'] = self.fspcValidCnt
        self.funcFspcLogTrace(str("Step4 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S4_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        self.fspcSucFlagS4 = True
        return TUP_SUCCESS;

    def fsm_msg_cmd_s5_req_rcv_handler(self, msgContent):
        mbuf={}
        if (os.path.exists('fspcPicS4.jpg') == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'File not exist!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        if (self.fspcSucFlagS4 == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'Previous step not done!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S2_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s5_proc(msgContent)
        if (ret == False):
            mbuf['res'] = -2
            string = str('Error find %d' % (totalCnt))
            mbuf['errInfo'] = string
            self.msg_send(TUP_MSGID_FSPC_CMD_S5_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf = self.proc_mbuf_fix_fill(mbuf, totalCnt, 5)
        mbuf['findCnt'] = self.fspcValidCnt
        self.funcFspcLogTrace(str("Step5 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S5_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        self.fspcSucFlagS5 = True
        return TUP_SUCCESS;

    def fsm_msg_cmd_s6_req_rcv_handler(self, msgContent):
        mbuf={}
        if (os.path.exists('fspcPicS5.jpg') == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'File not exist!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        if (self.fspcSucFlagS5 == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'Previous step not done!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S2_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s6_proc(msgContent)
        if (ret == False):
            mbuf['res'] = -2
            string = str('Error find %d' % (totalCnt))
            mbuf['errInfo'] = string
            self.msg_send(TUP_MSGID_FSPC_CMD_S6_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf = self.proc_mbuf_fix_fill(mbuf, totalCnt, 6)
        mbuf['findCnt'] = self.fspcValidCnt
        self.funcFspcLogTrace(str("Step6 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S6_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        self.fspcSucFlagS6 = True
        return TUP_SUCCESS;

    def fsm_msg_cmd_s7_req_rcv_handler(self, msgContent):
        mbuf={}
        if (os.path.exists('fspcPicS6.jpg') == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'File not exist!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S7_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        if (self.fspcSucFlagS6 == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'Previous step not done!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S2_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s7_proc(msgContent)
        if (ret == False):
            mbuf['res'] = -2
            string = str('Error find %d' % (totalCnt))
            mbuf['errInfo'] = string
            self.msg_send(TUP_MSGID_FSPC_CMD_S7_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf = self.proc_mbuf_fix_fill(mbuf, totalCnt, 7)
        mbuf['findCnt'] = self.fspcValidCnt
        self.funcFspcLogTrace(str("Step7 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S7_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        self.fspcSucFlagS7 = True
        return TUP_SUCCESS;

    def fsm_msg_cmd_sum_req_rcv_handler(self, msgContent):
        mbuf={}
        if (os.path.exists(msgContent['fileName']) == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'File not exist!'
            self.msg_send(TUP_MSGID_FSPC_CMD_SUM_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_sum_proc(msgContent)
        if (ret == False):
            mbuf['res'] = -2
            string = str('Error find %d' % (totalCnt))
            mbuf['errInfo'] = string
            self.msg_send(TUP_MSGID_FSPC_CMD_SUM_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicSum.jpg'
        mbuf['fileName1'] = 'fspcPicSum1.jpg'
        mbuf['fileName2'] = 'fspcPicSum2.jpg'
        mbuf['totalCnt'] = totalCnt
        mbuf['errInfo'] = ''
        self.funcFspcLogTrace(str("Step sum result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_SUM_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;
    
    def proc_mbuf_fix_fill(self, mbuf, totalCnt, index):
        mbuf['res'] = 1
        mbuf['fileName1'] = str('fspcPicS%d1.jpg' %(index))
        mbuf['fileName2'] = str('fspcPicS%d2.jpg' %(index))
        mbuf['fileName3'] = str('fspcPicS%d3.jpg' %(index))
        mbuf['fileName4'] = str('fspcPicS%d4.jpg' %(index))
        mbuf['fileName5'] = str('fspcPicS%d5.jpg' %(index))
        mbuf['fileName']  = str('fspcPicS%d.jpg' %(index))
        mbuf['totalCnt'] = totalCnt
        mbuf['errInfo'] = ''
        return mbuf
    
    '''
    #所有支持的参数，但这里再次解码，并利用序号控制程序，并不是特别好，还不如直接使用消息中带有含义的字符串直接引用，反而泛化能力更强。
    #目前这个函数并未启用
    '''
    def proc_decode_rcv_par_list(self, msgContent):
        fileName = msgContent['fileName'];
        markLine = msgContent['markLine'];
        markWidth = msgContent['markWidth'];
        areaMin = msgContent['areaMin'];
        areaMax = msgContent['areaMax'];
        areaDilate = msgContent['areaDilate'];
        areaErode = msgContent['areaErode'];
        cellMin = msgContent['cellMin'];
        cellMax = msgContent['cellMax'];
        raduisMin = msgContent['raduisMin'];
        raduisMax = msgContent['raduisMax'];
        cellDilate = msgContent['cellDilate'];
        cellErode = msgContent['cellErode'];
        cellCe = msgContent['cellCe'];
        cellDist = msgContent['cellDist'];
        trainDelay = msgContent['trainDelay'];
        addupSet = msgContent['addupSet'];
        parRes = (fileName, markLine, markWidth, areaMin, areaMax, areaDilate, areaErode, cellMin, cellMax, raduisMin, \
                raduisMax, cellDilate, cellErode, cellCe, cellDist, trainDelay, addupSet)
        return parRes
    
    
    
    '''
    #命令处理过程
    '''
   #找黄线
    def func_cmd_s1_proc(self, inputPar):
        #Reading file: 读取文件。这里采用了处理中文文件名字的技巧，不是直接从opencv中读取
        try:
            inputImg = cv.imdecode(np.fromfile(inputPar['fileName'], dtype=np.uint8), cv.IMREAD_COLOR)
        except Exception as err:
            print("FSPC: Read file error, errinfo = ", str(err))
            return False, -1
        #寻找人工标定  #寻找标定线 寻找右下半部分  #寻找黄色标定线： 人工标定的方式，在参数选择上需要固定一种特征，而且保持一定的稳定性，不然无法兑付
        #图像解析度需要保持稳定
        #两种直线寻找方案都验证了，都好使！
        #线宽也作为参数了！
        self.funcFspcLogTrace("FSPC: stack Stage1, Finding yellow marked line!")
        b, g, r = cv.split(inputImg)
        grayImg = cv.cvtColor(inputImg, cv.COLOR_BGR2GRAY)
        delImg = grayImg - b
        diImg = self.tup_dilate(delImg, inputPar['markDilate'])
        ctImg, self.fspcMinRect, totalCnt, findCnt, self.fspcOutCt, self.fspcOutBox = self.tup_find_max_contours(diImg, inputPar['markArea'], inputPar['markArea']*10, 0.001, 0.5, True, True)
        cv.imwrite("fspcPicS11.jpg", ctImg)
        if (findCnt!=1):
            return False, findCnt
        #生成外围图
        yelImg = inputImg.copy()
        cv.drawContours(yelImg, self.fspcOutCt, -1, self._COL_D_RED, 2)
        cv.imwrite("fspcPicS12.jpg", yelImg)
        lineOutImg = self.tup_cut_line_out_img(inputImg, self.fspcMinRect[0], self.fspcMinRect[2], inputPar['markWidth'])
        cv.imwrite("fspcPicS1.jpg", lineOutImg)
        return True, 3
    
    #确定正方形
    def func_cmd_s2_proc(self, inputPar):
        try:
            inputImg = cv.imdecode(np.fromfile('fspcPicS1.jpg', dtype=np.uint8), cv.IMREAD_COLOR)
        except Exception as err:
            print("FSPC: Read file error, errinfo = ", str(err))
            return False, -1
        #使用黄色线，将正方形区域框定下来，然后再寻找外接框
        #可以考虑使用，使用下面的技巧（多边形技巧），将这个定点多边形搞出来，然后取出限定正方形内的多边形图像
        self.funcFspcLogTrace("FSPC: stack Stage2, Finding retangle area!")
        tpList = self.tup_find_retg_area(inputImg, self.fspcMinRect, inputPar['markLine']/100)
        tpListImg = inputImg.copy()
        cv.drawContours(tpListImg, [tpList], -1, self._COL_D_BLUE, 2)
        cv.imwrite("fspcPicS21.jpg", tpListImg)
        rtgImg = self.tup_copy_contour_img(inputImg, tpList)
        cv.imwrite("fspcPicS2.jpg", rtgImg)   
        return True, 2
    
    #抠出区域面积图形
    def func_cmd_s3_proc(self, inputPar):
        try:
            inputImg = cv.imdecode(np.fromfile('fspcPicS2.jpg', dtype=np.uint8), cv.IMREAD_COLOR)
        except Exception as err:
            print("FSPC: Read file error, errinfo = ", str(err))
            return False, -1
        self.funcFspcLogTrace("FSPC: stack Stage3, fix working contour area!")
        targetImg, self.fspcMinRect, totalCnt, findCnt, self.fspcOutCt, self.fspcOutBox = \
            self.tup_max_contours_itp(inputImg, inputPar['areaDilate'], inputPar['areaErode'], inputPar['areaMin'], inputPar['areaMax'], 0.001, 1, True, True)
        if (findCnt <= 0):
            return False, findCnt;
        cv.imwrite("fspcPicS31.jpg", targetImg)
        tar1Img = inputImg.copy()
        cv.drawContours(tar1Img, self.fspcOutCt, -1, self._COL_D_RED, 2)
        cv.imwrite("fspcPicS32.jpg", tar1Img)
        self.fspcOutCtPoly = cv.convexHull(self.fspcOutCt)
        tar2Img = inputImg.copy()
        cv.drawContours(tar2Img, self.fspcOutCt, -1, self._COL_D_BLUE, 2)
        cv.imwrite("fspcPicS33.jpg", tar1Img)
        tar3Img = inputImg.copy()
        tar4Img = cv.polylines(tar3Img, [self.fspcOutCtPoly], True, self._COL_D_RED, 2)
        cv.fillPoly(tar4Img, [self.fspcOutCtPoly], 255)
        cv.imwrite("fspcPicS34.jpg", tar4Img)
        cropImg = self.tup_copy_contour_img(inputImg, self.fspcOutCt)
        cv.imwrite("fspcPicS3.jpg", cropImg)
        if (findCnt != 1):
            return False, findCnt;
        return True, 5
    
    #得到聚合细胞圆的分布
    def func_cmd_s4_proc(self, inputPar):
        try:
            inputImg = cv.imdecode(np.fromfile('fspcPicS3.jpg', dtype=np.uint8), cv.IMREAD_COLOR)
        except Exception as err:
            print("FSPC: Read file error, errinfo = ", str(err))
            return False, -1
        #霍夫变换找圆形算法
        #cirRadMin/cirRadMax - 圆形范围
        #ceMin - 圆形距离
        algoSelction = 1
        self.funcFspcLogTrace("FSPC: stack Stage4, Hough transform to find potential candidates!")
        if (algoSelction == 1):
            outputImg, findCnt, self.fspcCircles = self.tup_itp_hough_transform(inputImg, inputPar['raduisMin'], inputPar['raduisMax'], inputPar['cellDist'])
            totalCnt = findCnt
        #图像形态学算法
        elif (algoSelction == 2):
            outputImg, rect, totalCnt, findCnt, outCt, outBox = \
                self.tup_itp_morphology_transform(inputImg, inputPar['cellDilate'], inputPar['cellErode'], \
                inputPar['cellMin'], inputPar['cellMax'], inputPar['cellCe']/100.0, 1, True, True)
        cv.imwrite("fspcPicS4.jpg", outputImg)
        self.fspcValidCnt = findCnt
        self.funcFspcLogTrace("FSPC: stack Stage4, find total %d!" % (self.fspcValidCnt))
        return True, 1
    
    #去圈外的图像
    def func_cmd_s5_proc(self, inputPar):
        try:
            inputImg = cv.imdecode(np.fromfile('fspcPicS3.jpg', dtype=np.uint8), cv.IMREAD_COLOR)
        except Exception as err:
            print("FSPC: Read file error, errinfo = ", str(err))
            return False, -1        
        self.funcFspcLogTrace("FSPC: stack Stage5, Removing outer wrong findings!")
        self.fspcGdCircles, badCircles = self.tup_remove_ex_contour_circle(self.fspcOutCt, self.fspcCircles)
        judgeCircleImg = inputImg.copy()
        for element in self.fspcGdCircles[0]:
            cv.circle(judgeCircleImg, (element[0], element[1]), element[2], self._COL_D_RED, 2)
        for element in badCircles[0]:
            cv.circle(judgeCircleImg, (element[0], element[1]), element[2], self._COL_D_BLUE, 2)
        cv.drawContours(judgeCircleImg, self.fspcOutCt, -1, self._COL_D_YELLOW, 3)
        cv.imwrite("fspcPicS5.jpg", judgeCircleImg)
        self.fspcValidCnt = len(self.fspcGdCircles[0])
        self.funcFspcLogTrace("FSPC: stack Stage5, find total %d!" % (self.fspcValidCnt))
        return True, 1
    
    #去伪存真
    def func_cmd_s6_proc(self, inputPar):
        try:
            inputImg = cv.imdecode(np.fromfile('fspcPicS3.jpg', dtype=np.uint8), cv.IMREAD_COLOR)
        except Exception as err:
            print("FSPC: Read file error, errinfo = ", str(err))
            return False, -1
        #传统方式干活
        tradImg, rect, totalCnt, findCnt, outCt, outBox = self.tup_itp_morphology_transform(inputImg, inputPar['cellDilate'], inputPar['cellErode'], \
                inputPar['cellMin'], inputPar['cellMax'], inputPar['cellCe']/100.0, 1, True, True)
        cv.imwrite("fspcPicS61.jpg", tradImg)
        #新方法干活
        outputImg, detectImg, totalCnt, findCnt, self.fspcCkCircles = self.tup_itp_circle_img_filter_out(inputImg, self.fspcGdCircles, \
            inputPar['cellDilate'], inputPar['cellErode'], inputPar['cellMin'], inputPar['cellMax'], inputPar['cellCe']/100.0, 1, True, True)
        cv.imwrite("fspcPicS62.jpg", detectImg)
        cv.imwrite("fspcPicS6.jpg", outputImg)
        self.fspcValidCnt = findCnt
        self.funcFspcLogTrace("FSPC: stack Stage6, find total %d!" % (self.fspcValidCnt))
        return True, 3

    def func_cmd_s7_proc(self, inputPar):
        return False, 1

    def func_cmd_sum_proc(self, inputPar):
        return False, 1





