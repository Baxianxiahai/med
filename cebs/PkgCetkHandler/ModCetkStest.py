'''
Created on 2018年12月25日

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

class tupTaskStest(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3

    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_STEST, taskName="TASK_STEST", glTabEntry=glPar)
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_STEST, self)
        self.fsm_set(TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_com_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_EXIT, self.fsm_com_msg_exit_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_com_msg_test_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)
        
        #业务处理部分
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_STEST_MOTO_INQ, self.fsm_msg_moto_inq_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_STEST_CAM_INQ, self.fsm_msg_cam_inq_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_STEST_MOTO_FDB, self.fsm_msg_moto_fdb_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_STEST_CAM_FDB, self.fsm_msg_cam_fdb_rcv_handler)
        
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        time.sleep(0.5) #WAIT FOR OTHER TASK STARTUP
        return TUP_SUCCESS;

    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_STEST, msgContent)
        return TUP_SUCCESS;

    def fsm_msg_moto_inq_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_STEST_MOTO_INQ, TUP_TASK_ID_MOTO, msgContent)
        return TUP_SUCCESS;

    def fsm_msg_cam_inq_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_STEST_CAM_INQ, TUP_TASK_ID_VISION, msgContent)
        return TUP_SUCCESS;

    def fsm_msg_moto_fdb_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_STEST_MOTO_FDB, TUP_TASK_ID_UI_STEST, msgContent)
        return TUP_SUCCESS;

    def fsm_msg_cam_fdb_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_STEST_CAM_FDB, TUP_TASK_ID_UI_STEST, msgContent)
        return TUP_SUCCESS;

    def funcStestLogTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_STEST, myString)
        #SAVE INTO MED FILE
        self.medCmdLog(str(myString))
        #PRINT to local
        self.tup_dbg_print(str(myString))
        return
    
    def funcStestErrTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_STEST, myString)
        #SAVE INTO MED FILE
        self.medErrorLog(str(myString));
        #PRINT to local
        self.tup_err_print(str(myString))
        return        
    

    
    
    
    
    
    
    
    
    
    
    
    
    