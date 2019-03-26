'''
Created on 2018年12月28日

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


class tupTaskUiSaht(tupClassUiBasic):
    _STM_WORKING = 5    #从5开始属于任务私有部分

    def __init__(self, glPar):
        tupClassUiBasic.__init__(self, taskidUb=TUP_TASK_ID_UI_SAHT, taskNameUb="TASK_UI_SAHT", glParUb=glPar)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_SAHT_UI_SWITCH, self.fsm_msg_ui_focus_rcv_handler)
        #业务态
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    #业务状态处理过程
    #主界面承接过来的执行函数
    def func_ui_click_saht_self_test_stop(self):
        print("I am func_ui_click_saht_self_test_stop!")


        



