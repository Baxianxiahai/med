'''
Created on 2018年12月8日

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

from PyQt5 import QtGui

class tupTaskGpar(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    _STM_TRAINING = 4
    
    #模块中的局部变量
    picDirFile = ''
    orgPicWidth = 0
    orgPicHeight = 0
    cfyPicWidth = 0
    cfyPicHeight = 0
    timerTrain = ''
    timerTrainCnt = 0

    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_GPAR, taskName="TASK_GPAR", glTabEntry=glPar)
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_GPAR, self)
        self.fsm_set(TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_GPAR_INIT_INF, self.fsm_msg_init_inf_rcv_handler)

        #业务处理部分
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_GPAR_CLOSE_REQ, self.fsm_msg_close_req_rcv_handler)
        '''
        #通过文件进行训练结果的交换，无法在任务里直接处理。结果必须送到界面任务中进行处理
        #同一个消息，在不同任务之间进行交换，简化系统设计的技巧
        #至于为啥一定要通过这里的交换，一方面是为了隔离，另一方面，将充分利用状态机，去除无效的界面事件，放置对硬件和算法处理的不适当过程
        #这里还没考虑定时器机制，未来看诉求
        '''
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_GPAR_PIC_TRAIN_REQ, self.fsm_msg_pic_train_req_rcv_handler)
        self.add_stm_combine(self._STM_TRAINING, TUP_MSGID_GPAR_PIC_TRAIN_RESP, self.fsm_msg_pic_train_resp_rcv_handler)
        
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.picDirFile = ''
        self.orgPicWidth = 0
        self.orgPicHeight = 0
        self.cfyPicWidth = 0
        self.cfyPicHeight = 0
        self.timerTrain = ''
        self.timerTrainCnt = 0
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;

    def funcGparLogTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_GPAR, myString)
        #SAVE INTO MED FILE
        self.medCmdLog(str(myString))
        #PRINT to local
        self.tup_dbg_print(str(myString))
        return
    
    def funcGparErrTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_GPAR, myString)
        #SAVE INTO MED FILE
        self.medErrorLog(str(myString));
        #PRINT to local
        self.tup_err_print(str(myString))
        return        

    '''
    SERVICE PROCESSING
    '''
    def fsm_msg_init_inf_rcv_handler(self, msgContent):
        self.orgPicWidth = msgContent['orgWidth']
        self.orgPicHeight = msgContent['orgHeight']
        self.cfyPicWidth = msgContent['cfyWidth']
        self.cfyPicHeight = msgContent['cfyHeight']
 
    def fsm_msg_pic_train_req_rcv_handler(self, msgContent):
        self.funcGparLogTrace("Picture training starting!")
        self.msg_send(TUP_MSGID_GPAR_PIC_TRAIN_REQ, TUP_TASK_ID_VISION, msgContent)
        self.fsm_set(self._STM_TRAINING)
        self.timerTrainCnt = 0
        self.timerTrain = self.tup_timer_start(1, self.func_timer_train_process)
        return TUP_SUCCESS

    def fsm_msg_pic_train_resp_rcv_handler(self, msgContent):
        self.funcGparLogTrace("Picture training accomplish!")
        self.tup_timer_stop(self.timerTrain)
        self.msg_send(TUP_MSGID_GPAR_PIC_TRAIN_RESP, TUP_TASK_ID_UI_GPAR, msgContent)
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS
    
    def func_timer_train_process(self):
        self.timerTrainCnt += 1
        if (self.timerTrainCnt >= 100):
            self.timerTrainCnt = 0;
            self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_GPAR, "Time out to wait training, failure!")
            mbuf = {}
            mbuf['res'] = -3
            self.msg_send(TUP_MSGID_GPAR_PIC_TRAIN_RESP, TUP_TASK_ID_UI_GPAR, mbuf)
            self.fsm_set(self._STM_ACTIVE)
        #RESTART
        else:
            mbuf = ("Picture training progress: %d" % (self.timerTrainCnt))
            self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_GPAR, mbuf)
            self.timerTrain = self.tup_timer_start(1, self.func_timer_train_process)

    def fsm_msg_close_req_rcv_handler(self, msgContent):
        self.func_clean_working_env()
        return TUP_SUCCESS;
    
    #业务函数
    def func_clean_working_env(self):
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
