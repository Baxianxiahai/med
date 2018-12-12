'''
Created on 2018年12月11日

@author: Administrator
'''

import random
import time
from multiprocessing import Queue, Process
from PkgVmHandler.ModVmCfg import *
from PkgVmHandler.ModVmLayer import *
from PkgCebsHandler.ModCebsCom import *
from PkgCebsHandler.ModCebsCfg import *
from PkgVmHandler.ModVmConsole import *
from PkgVmHandler.ModVmTimer import *


class tupTaskUiGpar(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3

    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_UI_GPAR, taskName="TASK_UI_GPAR", glTabEntry=glPar)
        self.fsm_set(TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TIME_OUT, self.fsm_msg_time_out_rcv_handler)
        self.fsm_set(TUP_STM_INIT)
        #START TASK
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        time.sleep(0.5) #WAIT FOR OTHER TASK STARTUP
        return TUP_SUCCESS;

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;
        
    def fsm_msg_time_out_rcv_handler(self, msgContent):
        return TUP_SUCCESS;

    #主界面承接过来的执行函数
    def func_ui_click_pic_file_load(self, fn):
        print("I am func_ui_click_pic_file_load!")
    
    def func_ui_click_pic_train(self):
        print("I am func_ui_click_pic_train!")
        
    def func_ui_click_gpar_close(self):
        print("I am func_ui_click_gpar_close!")
        
    #切换界面
    def func_ui_click_gpar_switch_to_main(self):
        print("I am func_ui_click_gpar_switch_to_main!")               
        
        
        
        
        
        
        
        
        

















