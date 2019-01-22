'''
Created on 2019年1月22日

@author: Administrator
'''

import random
import time
from multiprocessing import Queue, Process
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL3cebsHandler.ModCebsCom import *
from PkgL3cebsHandler.ModCebsCfg import *
from PkgL1vmHandler.ModVmConsole import *

from PyQt5 import QtGui

class tupTaskFspc(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    _STM_TRAINING = 4
    _STM_FCC = 5
    
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












