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
from PkgVmHandler.ModVmCfg import *
from PkgVmHandler.ModVmLayer import *
from PkgCebsHandler.ModCebsCom import *
from PkgCebsHandler.ModCebsCfg import *
from PkgVmHandler.ModVmConsole import *

class tupTaskUiStest(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    _STM_DEACT  = 4 #界面没激活

    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_UI_STEST, taskName="TASK_UI_STEST", glTabEntry=glPar)
        self.fsm_set(TUP_STM_NULL)
        self.fatherUiObj = ''   #父对象界面，双向通信
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_com_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_EXIT, self.fsm_com_msg_exit_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_com_msg_test_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_STEST_UI_SWITCH, self.fsm_msg_ui_focus_rcv_handler)
        #业务态

        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_STEST_MOTO_FDB, self.fsm_msg_moto_fdb_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_STEST_CAM_FDB, self.fsm_msg_cam_fdb_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_STEST_CALIB_FDB, self.fsm_msg_calib_fdb_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_STEST_CTRL_SCHD_FDB, self.fsm_msg_ctrl_schd_fdb_rcv_handler)
        
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_DEACT)
        return TUP_SUCCESS;

    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(msgContent);
        return TUP_SUCCESS;
   
    #界面切换进来
    def fsm_msg_ui_focus_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;
        
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
    
    #将界面对象传递给本任务，以便将打印信息送到界面上
    def funcSaveFatherInst(self, instance):
        self.fatherUiObj = instance
    
    def funcDebugPrint2Qt(self, string):
        if (self.fatherUiObj == ''):
            print("STEST_UI task lose 1 print message due to time sync.")
        else:
            self.fatherUiObj.cetk_debug_print(str(string))
            
    #主界面承接过来的执行函数
    def func_ui_click_stest_self_test_start(self):
        print("I am func_ui_click_stest_self_test_start!")
        self.msg_send(TUP_MSGID_STEST_MOTO_INQ, TUP_TASK_ID_STEST, "")
        self.msg_send(TUP_MSGID_STEST_CAM_INQ, TUP_TASK_ID_STEST, "")
        self.msg_send(TUP_MSGID_STEST_CALIB_INQ, TUP_TASK_ID_CALIB, "")
        self.msg_send(TUP_MSGID_STEST_CTRL_SCHD_INQ, TUP_TASK_ID_CTRL_SCHD, "")

    def func_ui_click_stest_self_test_stop(self):
        print("I am func_ui_click_stest_self_test_stop!")

    #清理各项操作：工程模式均为阻塞式工作模式，暂时不需要再去通知STEST任务模块
    def func_ui_click_stest_close(self):
        print("I am func_ui_click_stest_close!")
        #self.msg_send(TUP_MSGID_STEST_CLOSE_REQ, TUP_TASK_ID_STEST, "")
        return TUP_SUCCESS;
            
    #界面切走
    def func_ui_click_stest_switch_to_main(self):
        print("I am func_ui_click_stest_switch_to_main!")
        self.fsm_set(self._STM_DEACT)      
        return TUP_SUCCESS;
        




























        
        
        
        
        
        