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
from PkgL3cebsHandler.ModCebsCom import *
from PkgL3cebsHandler.ModCebsCfg import *
from PkgL1vmHandler.ModVmConsole import *

from PyQt5 import QtGui

class tupTaskFspc(tupTaskTemplate, clsL1_ConfigOpr):
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
        parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(parIn[0]) == False):
            mbuf['res'] = -1
            self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s1_proc(parIn)
        if (ret == False):
            mbuf['res'] = -2
            self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicS1.jpg'
        mbuf['totalCnt'] = totalCnt
        self.funcVisionLogTrace(str("Step1 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_cmd_s2_req_rcv_handler(self, msgContent):
        parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(parIn[0]) == False):
            mbuf['res'] = -1
            self.msg_send(TUP_MSGID_FSPC_CMD_S2_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s2_proc(parIn)
        if (ret == False):
            mbuf['res'] = -2
            self.msg_send(TUP_MSGID_FSPC_CMD_S2_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicS2.jpg'
        mbuf['totalCnt'] = totalCnt
        self.funcVisionLogTrace(str("Step2 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S2_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_cmd_s3_req_rcv_handler(self, msgContent):
        parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(parIn[0]) == False):
            mbuf['res'] = -1
            self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s3_proc(parIn)
        if (ret == False):
            mbuf['res'] = -2
            self.msg_send(TUP_MSGID_FSPC_CMD_S3_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicS3.jpg'
        mbuf['totalCnt'] = totalCnt
        self.funcVisionLogTrace(str("Step3 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S3_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_cmd_s4_req_rcv_handler(self, msgContent):
        parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(parIn[0]) == False):
            mbuf['res'] = -1
            self.msg_send(TUP_MSGID_FSPC_CMD_S4_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s4_proc(parIn)
        if (ret == False):
            mbuf['res'] = -2
            self.msg_send(TUP_MSGID_FSPC_CMD_S4_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicS4.jpg'
        mbuf['totalCnt'] = totalCnt
        self.funcVisionLogTrace(str("Step4 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S4_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_cmd_s5_req_rcv_handler(self, msgContent):
        parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(parIn[0]) == False):
            mbuf['res'] = -1
            self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s5_proc(parIn)
        if (ret == False):
            mbuf['res'] = -2
            self.msg_send(TUP_MSGID_FSPC_CMD_S5_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicS5.jpg'
        mbuf['totalCnt'] = totalCnt
        self.funcVisionLogTrace(str("Step5 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S5_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_cmd_s6_req_rcv_handler(self, msgContent):
        parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(parIn[0]) == False):
            mbuf['res'] = -1
            self.msg_send(TUP_MSGID_FSPC_CMD_S1_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s6_proc(parIn)
        if (ret == False):
            mbuf['res'] = -2
            self.msg_send(TUP_MSGID_FSPC_CMD_S6_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicS6.jpg'
        mbuf['totalCnt'] = totalCnt
        self.funcVisionLogTrace(str("Step6 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S6_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_cmd_s7_req_rcv_handler(self, msgContent):
        parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(parIn[0]) == False):
            mbuf['res'] = -1
            self.msg_send(TUP_MSGID_FSPC_CMD_S7_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_s7_proc(parIn)
        if (ret == False):
            mbuf['res'] = -2
            self.msg_send(TUP_MSGID_FSPC_CMD_S7_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicS7.jpg'
        mbuf['totalCnt'] = totalCnt
        self.funcVisionLogTrace(str("Step7 result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_S7_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_cmd_sum_req_rcv_handler(self, msgContent):
        parIn = self.proc_decode_rcv_par_list(msgContent)
        mbuf={}
        if (os.path.exists(parIn[0]) == False):
            mbuf['res'] = -1
            self.msg_send(TUP_MSGID_FSPC_CMD_SUM_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        ret, totalCnt = self.func_cmd_sum_proc(parIn)
        if (ret == False):
            mbuf['res'] = -2
            self.msg_send(TUP_MSGID_FSPC_CMD_SUM_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
            return TUP_SUCCESS;
        #Final feedback
        mbuf['res'] = 1
        mbuf['fileName'] = 'fspcPicSum.jpg'
        mbuf['totalCnt'] = totalCnt
        self.funcVisionLogTrace(str("Step sum result = %d" % (totalCnt)));
        self.msg_send(TUP_MSGID_FSPC_CMD_SUM_RESP, TUP_TASK_ID_UI_FSPC, mbuf)
        return TUP_SUCCESS;

    def proc_decode_rcv_par_list(self, msgContent):
        fileName = msgContent['fileName'];
        markLine = msgContent['markLine'];
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
        parRes = (fileName, markLine, areaMin, areaMax, areaDilate, areaErode, cellMin, cellMax, raduisMin, raduisMax, cellDilate, cellErode, cellCe, cellDist, addupSet)
        return parRes

    def func_cmd_s1_proc(self, inputPar):
        return False, 1

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





