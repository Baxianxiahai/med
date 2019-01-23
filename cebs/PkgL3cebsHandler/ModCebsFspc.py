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
    test = 0

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
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicS1.jpg'
        mbuf['fileName1'] = 'fspcPicS11.jpg'
        mbuf['fileName2'] = 'fspcPicS12.jpg'
        mbuf['totalCnt'] = totalCnt
        mbuf['errInfo'] = ''
        self.funcFspcLogTrace(str("Step1 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_cmd_s2_req_rcv_handler(self, msgContent):
        #parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(msgContent['fileName']) == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'File not exist!'
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
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicS2.jpg'
        mbuf['fileName1'] = 'fspcPicS21.jpg'
        mbuf['fileName2'] = 'fspcPicS22.jpg'
        mbuf['totalCnt'] = totalCnt
        mbuf['errInfo'] = ''
        self.funcFspcLogTrace(str("Step2 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S2_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_cmd_s3_req_rcv_handler(self, msgContent):
        #parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(msgContent['fileName']) == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'File not exist!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s3_proc(msgContent)
        if (ret == False):
            mbuf['res'] = -2
            string = str('Error find %d' % (totalCnt))
            mbuf['errInfo'] = string
            self.msg_send(TUP_MSGID_FSPC_CMD_S3_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicS3.jpg'
        mbuf['fileName1'] = 'fspcPicS31.jpg'
        mbuf['fileName2'] = 'fspcPicS32.jpg'
        mbuf['totalCnt'] = totalCnt
        mbuf['errInfo'] = ''
        self.funcFspcLogTrace(str("Step3 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S3_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_cmd_s4_req_rcv_handler(self, msgContent):
        #parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(msgContent['fileName']) == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'File not exist!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S4_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s4_proc(msgContent)
        if (ret == False):
            mbuf['res'] = -2
            string = str('Error find %d' % (totalCnt))
            mbuf['errInfo'] = string
            self.msg_send(TUP_MSGID_FSPC_CMD_S4_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicS4.jpg'
        mbuf['fileName1'] = 'fspcPicS41.jpg'
        mbuf['fileName2'] = 'fspcPicS42.jpg'
        mbuf['totalCnt'] = totalCnt
        mbuf['errInfo'] = ''
        self.funcFspcLogTrace(str("Step4 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S4_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_cmd_s5_req_rcv_handler(self, msgContent):
        #parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(msgContent['fileName']) == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'File not exist!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s5_proc(msgContent)
        if (ret == False):
            mbuf['res'] = -2
            string = str('Error find %d' % (totalCnt))
            mbuf['errInfo'] = string
            self.msg_send(TUP_MSGID_FSPC_CMD_S5_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicS5.jpg'
        mbuf['fileName1'] = 'fspcPicS51.jpg'
        mbuf['fileName2'] = 'fspcPicS52.jpg'
        mbuf['totalCnt'] = totalCnt
        mbuf['errInfo'] = ''
        self.funcFspcLogTrace(str("Step5 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S5_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_cmd_s6_req_rcv_handler(self, msgContent):
        #parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(msgContent['fileName']) == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'File not exist!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s6_proc(msgContent)
        if (ret == False):
            mbuf['res'] = -2
            string = str('Error find %d' % (totalCnt))
            mbuf['errInfo'] = string
            self.msg_send(TUP_MSGID_FSPC_CMD_S6_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicS6.jpg'
        mbuf['fileName1'] = 'fspcPicS61.jpg'
        mbuf['fileName2'] = 'fspcPicS62.jpg'
        mbuf['totalCnt'] = totalCnt
        mbuf['errInfo'] = ''
        self.funcFspcLogTrace(str("Step6 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S6_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_cmd_s7_req_rcv_handler(self, msgContent):
        #parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(msgContent['fileName']) == False):
            mbuf['res'] = -1
            mbuf['errInfo'] = 'File not exist!'
            self.msg_send(TUP_MSGID_FSPC_CMD_S7_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s7_proc(msgContent)
        if (ret == False):
            mbuf['res'] = -2
            string = str('Error find %d' % (totalCnt))
            mbuf['errInfo'] = string
            self.msg_send(TUP_MSGID_FSPC_CMD_S7_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicS7.jpg'
        mbuf['fileName1'] = 'fspcPicS71.jpg'
        mbuf['fileName2'] = 'fspcPicS72.jpg'
        mbuf['totalCnt'] = totalCnt
        mbuf['errInfo'] = ''
        self.funcFspcLogTrace(str("Step7 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S7_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_cmd_sum_req_rcv_handler(self, msgContent):
        #parIn = self.proc_decode_rcv_par_list(msgContent)
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
    
    #指出的参数！
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
        addupSet = msgContent['addupSet'];
        parRes = (fileName, markLine, markWidth, areaMin, areaMax, areaDilate, areaErode, cellMin, cellMax, raduisMin, raduisMax, cellDilate, cellErode, cellCe, cellDist, addupSet)
        return parRes
    
    
    
    
    
    
    '''
    #命令处理过程
    '''
    def func_cmd_s1_proc(self, inputPar):
        #处理参数
        #使用LOCAL方式进行叠加，不再使用全局属性，简化处理
        outputText = {'totalNbr':0, 'validNbr':0}
        
        #Reading file: 读取文件
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
        ctImg, rect, totalCnt, findCnt, outCt, outBox = self.tup_find_max_contours(diImg, inputPar['markArea'], inputPar['markArea']*10, 0.001, 0.5, True, True)
        cv.imwrite("fspcPicS11.jpg", ctImg)
        if (findCnt!=1):
            return False, findCnt
        testFlag = False
        if (testFlag == True):
            cv.drawContours(ctImg, outCt, -1, self._COL_D_YELLOW, 2)
            self.tup_img_show(ctImg, "S1: Finding Yellow Line")
            sp = ctImg.shape
            #(startPoint, endPoint) = self.tup_cal_rect_line(rect[0], rect[2], (sp[0], sp[1]))
            (startPoint, endPoint) = self.tup_siml_line_by_contour(ctImg, outCt)
            cv.line(inputImg, startPoint, endPoint, self._COL_D_RED, 2)
            self.tup_img_show(inputImg, "S1: Line Cut Image result")
        #生成外围图
        yelImg = inputImg.copy()
        cv.drawContours(yelImg, outCt, -1, self._COL_D_RED, 3)
        cv.imwrite("fspcPicS12.jpg", yelImg)
        lineOutImg = self.tup_cut_line_out_img(inputImg, rect[0], rect[2], inputPar['markWidth'])
        cv.imwrite("fspcPicS1.jpg", lineOutImg)
        return True, 3



    def func_cmd_s2_proc(self, inputPar):
        return False, 1

    def func_cmd_s3_proc(self, inputPar):
        return False, 1

    def func_cmd_s4_proc(self, inputPar):
        return False, 1

    def func_cmd_s5_proc(self, inputPar):
        return False, 1

    def func_cmd_s6_proc(self, inputPar):
        return False, 1

    def func_cmd_s7_proc(self, inputPar):
        return False, 1

    def func_cmd_sum_proc(self, inputPar):
        return False, 1





