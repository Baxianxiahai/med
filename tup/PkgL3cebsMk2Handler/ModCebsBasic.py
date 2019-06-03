'''
Created on 2019年1月25日

@author: Administrator
'''

import random
import time
from multiprocessing import Queue, Process
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL1vmHandler.ModVmConsole import *
from PkgL3cebsMk2Handler.ModCebsCom import *
from PkgL3cebsMk2Handler.ModCebsCfg import *


'''
目前能够聚合的内容并不多
公共处理函数部分，需要进一步通过某种技巧，将其泛化：比如CALIB任务与CALIB-UI任务模块之间，界面展示的内容就有相关性
'''
class tupTaskBasic(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    
    def __init__(self, taskidUb, taskNameUb, glParUb):
        tupTaskTemplate.__init__(self, taskid=taskidUb, taskName=taskNameUb, glTabEntry=glParUb)
        self.fsm_set(TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_com_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_EXIT, self.fsm_com_msg_exit_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_com_msg_test_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)    
    
    #缺省处理，各个任务自己重载
    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;
    
    #缺省处理，各个任务自己重载
    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MAIN, msgContent)
        return TUP_SUCCESS;
    
    #缺省处理，各个任务自己重载
    def funcBasicLogTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MAIN, myString)
        #SAVE INTO MED FILE
        self.medCmdLog(str(myString))
        #PRINT to local
        self.tup_dbg_print(str(myString))
        return
    
    #缺省处理，各个任务自己重载    
    #抑制本地打印，实在是太多了
    def funcBasicErrTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MAIN, myString)
        #SAVE INTO MED FILE
        self.medErrorLog(str(myString));
        #PRINT to local
        self.tup_err_print(str(myString))
        return

















   