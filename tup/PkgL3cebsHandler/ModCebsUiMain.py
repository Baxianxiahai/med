'''
Created on 2018年12月11日

@author: Administrator
'''

import random
import time
import sys
import json
import os
import re
import urllib
import http
import socket
from multiprocessing import Queue, Process
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL3cebsHandler.ModCebsCom import *
from PkgL3cebsHandler.ModCebsCfg import *
from PkgL1vmHandler.ModVmConsole import *
from PkgL3cebsHandler.ModCebsUiBasic import *




class tupTaskUiMain(tupClassUiBasic):
    _STM_WORKING = 5    #从5开始属于任务私有部分
    
    def __init__(self, glPar):
        tupClassUiBasic.__init__(self, taskidUb=TUP_TASK_ID_UI_MAIN, taskNameUb="TASK_UI_MAIN", glParUb=glPar)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_MAIN_UI_SWITCH, self.fsm_msg_ui_focus_rcv_handler)
        #测试消息，后面可以去掉
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_msg_print_test_inc_rcv_handler)
        #特殊功能：密码检查错误，退出程序
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CRTS_MDC_CHK_PSWD_RESP, self.fsm_msg_mdc_chk_pswd_resp_rcv_handler)
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()
    
    #延迟一秒，确保打印消息不丢失 - 重载
    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        time.sleep(1)
        #第一次界面启动，肯定在MAIN界面这儿，所以需要给CTRL_SCHD模块一个启动信号
        self.msg_send(TUP_MSGID_CTRL_SCHD_SWITCH_ON, TUP_TASK_ID_CTRL_SCHD, "")
        self.msg_send(TUP_MSGID_MAIN_UI_SWITCH, TUP_TASK_ID_MOTO, "") 
        self.msg_send(TUP_MSGID_MAIN_UI_SWITCH, TUP_TASK_ID_VISION, "") 
        #触发归零操作
        self.msg_send(TUP_MSGID_CTRL_SCHD_MV_ZERO, TUP_TASK_ID_CTRL_SCHD, "")
        return TUP_SUCCESS;

    def fsm_msg_print_test_inc_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(msgContent);
        return TUP_SUCCESS;
    
    #主界面承接过来的执行函数-测试函数
    def funcPrintTestCalledByQt(self, string):
        self.funcDebugPrint2Qt(string);


    #业务逻辑
    def fsm_msg_mdc_chk_pswd_resp_rcv_handler(self, msgContent):
        #调用父进程中的退出方法
        if (self.fatherUiObj == ''):
            print("MAIN_UI task lose 1 print message due to time sync.")
        else:
            self.fatherUiObj.mainui_callback_chk_pswd_failure();
        return TUP_SUCCESS;    

        
    '''
    #主界面承接过来的执行函数
    '''
    def func_ui_click_cap_start_nor(self):
        print("I am func_ui_click_cap_start_nor!")
        self.msg_send(TUP_MSGID_CTRL_SCHD_CAPPIC_START, TUP_TASK_ID_CTRL_SCHD, "")

    def func_ui_click_cap_start_flu(self):
        print("I am func_ui_click_cap_start_flu!")
        self.msg_send(TUP_MSGID_CTRL_SCHD_CAPFLU_START, TUP_TASK_ID_CTRL_SCHD, "")

    def func_ui_click_cap_stop(self):
        print("I am func_ui_click_cap_stop!")
        self.msg_send(TUP_MSGID_CTRL_SCHD_CAPPIC_STOP, TUP_TASK_ID_CTRL_SCHD, "")
    
    def func_ui_click_move_zero(self):
        print("I am func_ui_click_move_zero!")
        self.msg_send(TUP_MSGID_CTRL_SCHD_MV_ZERO, TUP_TASK_ID_CTRL_SCHD, "")

    def func_ui_click_clf_start_nor(self):
        print("I am func_ui_click_clf_start_nor!")
        self.msg_send(TUP_MSGID_CTRL_SCHD_CFYPIC_START, TUP_TASK_ID_CTRL_SCHD, "")

    def func_ui_click_clf_start_flu(self):
        print("I am func_ui_click_clf_start_flu!")        
        self.msg_send(TUP_MSGID_CTRL_SCHD_CFYFLU_START, TUP_TASK_ID_CTRL_SCHD, "")
        
    def func_ui_click_clf_stop(self):
        print("I am func_ui_click_clf_stop!")        
        self.msg_send(TUP_MSGID_CTRL_SCHD_CFYPIC_STOP, TUP_TASK_ID_CTRL_SCHD, "")
    
    #切换界面
    def func_ui_click_calib_start(self):
        print("I am func_ui_click_calib_start!")
        self.msg_send(TUP_MSGID_CALIB_UI_SWITCH, TUP_TASK_ID_UI_CALIB, "")
        self.msg_send(TUP_MSGID_CALIB_UI_SWITCH, TUP_TASK_ID_MOTO, "")
        self.msg_send(TUP_MSGID_CALIB_UI_SWITCH, TUP_TASK_ID_VISION, "")
        self.msg_send(TUP_MSGID_CTRL_SCHD_SWITCH_OFF, TUP_TASK_ID_CTRL_SCHD, "")     
        #执行命令
        #发送停止CAP， 发送CFY停止
        #转移状态
        self.fsm_set(self._STM_DEACT)
    
    #切换界面
    def func_ui_click_gpar_start(self):
        print("I am func_ui_click_gpar_start!")
        self.msg_send(TUP_MSGID_GPAR_UI_SWITCH, TUP_TASK_ID_UI_GPAR, "")
        self.msg_send(TUP_MSGID_GPAR_UI_SWITCH, TUP_TASK_ID_VISION, "")
        self.msg_send(TUP_MSGID_CTRL_SCHD_SWITCH_OFF, TUP_TASK_ID_CTRL_SCHD, "")     
        #执行命令 
        #转移状态
        self.fsm_set(self._STM_DEACT)

    #切换界面
    def func_ui_click_fspc_start(self):
        print("I am func_ui_click_fspc_start!")
        self.msg_send(TUP_MSGID_FSPC_UI_SWITCH, TUP_TASK_ID_UI_FSPC, "")
        self.msg_send(TUP_MSGID_CTRL_SCHD_SWITCH_OFF, TUP_TASK_ID_CTRL_SCHD, "")     
        #执行命令 
        #转移状态
        self.fsm_set(self._STM_DEACT)
    
    #切换界面
    def func_ui_click_meng_start(self):
        print("I am func_ui_click_meng_start!")    
        self.msg_send(TUP_MSGID_MENG_UI_SWITCH, TUP_TASK_ID_UI_MENG, "") 
        self.msg_send(TUP_MSGID_MENG_UI_SWITCH, TUP_TASK_ID_MOTO, "") 
        self.msg_send(TUP_MSGID_CTRL_SCHD_SWITCH_OFF, TUP_TASK_ID_CTRL_SCHD, "")     
        #执行命令 
        #转移状态
        self.fsm_set(self._STM_DEACT)

    #切换界面
    def func_ui_click_stest_start(self):
        print("I am func_ui_click_stest_start!")    
        self.msg_send(TUP_MSGID_STEST_UI_SWITCH, TUP_TASK_ID_UI_STEST, "") 
        self.msg_send(TUP_MSGID_STEST_UI_SWITCH, TUP_TASK_ID_MOTO, "") 
        self.msg_send(TUP_MSGID_STEST_UI_SWITCH, TUP_TASK_ID_VISION, "")
        #执行命令 
        #转移状态
        self.fsm_set(self._STM_DEACT)

    #切换界面
    def func_ui_click_main_start(self):
        print("I am func_ui_click_main_start!")
        self.msg_send(TUP_MSGID_MAIN_UI_SWITCH, TUP_TASK_ID_MOTO, "") 
        self.msg_send(TUP_MSGID_MAIN_UI_SWITCH, TUP_TASK_ID_VISION, "") 
        self.msg_send(TUP_MSGID_CTRL_SCHD_SWITCH_ON, TUP_TASK_ID_CTRL_SCHD, "")
        #执行命令 
        #转移状态
        self.fsm_set(self._STM_ACTIVE)


    #程序退出
    def func_ui_click_main_prog_exit(self):
        print("I am func_ui_click_main_prog_exit!")
        self.msg_send(TUP_MSGID_HW_REL, TUP_TASK_ID_MOTO, "")
        self.msg_send(TUP_MSGID_HW_REL, TUP_TASK_ID_VISION, "")
        self.msg_send(TUP_MSGID_HW_REL, TUP_TASK_ID_CTRL_SCHD, "")
        self.fsm_set(self._STM_ACTIVE)
    





