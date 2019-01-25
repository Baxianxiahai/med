'''
Created on 2018年12月25日

@author: Administrator
'''

####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-

import random
import time
import json
from multiprocessing import Queue, Process
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL1vmHandler.ModVmConsole import *
from PkgL3cebsHandler.ModCebsCom import *
from PkgL3cebsHandler.ModCebsCfg import *
from PkgL3cebsHandler.ModCebsUiBasic import *



class tupTaskUiStest(tupClassUiBasic):
    _STM_WORKING = 5    #从5开始属于任务私有部分

    def __init__(self, glPar):
        tupClassUiBasic.__init__(self, taskidUb=TUP_TASK_ID_UI_STEST, taskNameUb="TASK_UI_STEST", glParUb=glPar)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_STEST_UI_SWITCH, self.fsm_msg_ui_focus_rcv_handler)
        #业务态
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_STEST_MOTO_FDB, self.fsm_msg_moto_fdb_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_STEST_CAM_FDB, self.fsm_msg_cam_fdb_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_STEST_CALIB_FDB, self.fsm_msg_calib_fdb_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_STEST_CTRL_SCHD_FDB, self.fsm_msg_ctrl_schd_fdb_rcv_handler)
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    #业务状态处理过程
    #业务功能
    def fsm_msg_moto_fdb_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(str(msgContent))
        par1 = msgContent['spsOpen']
        if par1 > 0:
            par2 = msgContent['motoX']
            par3 = msgContent['motoY']
            self.fatherUiObj.stest_callback_fetch_moto_status(par1, par2, par3)
        else:
            self.fatherUiObj.stest_callback_fetch_moto_status(par1, -1, -1)
        return TUP_SUCCESS;
       
    #业务功能    
    def fsm_msg_cam_fdb_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(str(msgContent))
        par1 = msgContent['camOpen']
        if (self.fatherUiObj != ''):
            self.fatherUiObj.stest_callback_fetch_cam_status(par1)
        return TUP_SUCCESS;

    #业务功能    
    def fsm_msg_calib_fdb_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(str(msgContent))
        par1 = msgContent['calibStatus']
        if (self.fatherUiObj != ''):
            self.fatherUiObj.stest_callback_fetch_calib_status(par1)
        return TUP_SUCCESS;

    #业务功能    
    def fsm_msg_ctrl_schd_fdb_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(str(msgContent))
        picBat = msgContent['picBatch']
        cfyPicBat = msgContent['cfyPicBatch']
        cfyFlubat = msgContent['cfyFluBatch']
        cfyPicRemCnt = msgContent['cfyPicRemCnt']
        cfyFluRemCnt = msgContent['cfyFluRemCnt']
        hbType = msgContent['hbType']
        if (self.fatherUiObj != ''):
            self.fatherUiObj.stest_callback_fetch_ctrl_schd_status(picBat, cfyPicBat, cfyFlubat, cfyPicRemCnt, cfyFluRemCnt, hbType)
        return TUP_SUCCESS;
    
    #主界面承接过来的执行函数
    def func_ui_click_stest_self_test_start(self):
        print("I am func_ui_click_stest_self_test_start!")
        self.msg_send(TUP_MSGID_STEST_MOTO_INQ, TUP_TASK_ID_STEST, "")
        self.msg_send(TUP_MSGID_STEST_CAM_INQ, TUP_TASK_ID_STEST, "")
        self.msg_send(TUP_MSGID_STEST_CALIB_INQ, TUP_TASK_ID_CALIB, "")
        self.msg_send(TUP_MSGID_STEST_CTRL_SCHD_INQ, TUP_TASK_ID_CTRL_SCHD, "")

    def func_ui_click_stest_self_test_stop(self):
        print("I am func_ui_click_stest_self_test_stop!")






























        
        
        
        
        
        