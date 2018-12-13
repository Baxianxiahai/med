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
from PkgVmHandler.ModVmTimer import *

class tupTaskCalib(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    _STM_CAM_DISP = 4

    timerDisplay = ''
    
    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_CALIB, taskName="TASK_CALIB", glTabEntry=glPar)
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_CALIB, self)
        self.fsm_set(TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TIME_OUT, self.fsm_msg_time_out_rcv_handler)
        
        #业务处理部分
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_CLOSE_REQ, self.fsm_msg_close_req_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_OPEN_REQ, self.fsm_msg_open_req_rcv_handler)
        self.add_stm_combine(self._STM_CAM_DISP, TUP_MSGID_CALIB_VDISP_RESP, self.fsm_msg_cam_disp_resp_rcv_handler)

        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        #STEP1: 判定产品型号
        GLPLT_PAR_OFC.med_init_plate_product_type()

        #STEP2：初始化工作环境
        GLPLT_PAR_OFC.med_init_plate_parameter()
        self.func_clean_working_env()
        
        #干活的定时器
        self.timerDisplay = ''
        return TUP_SUCCESS;

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;
        
    def fsm_msg_time_out_rcv_handler(self, msgContent):
        return TUP_SUCCESS;
    
    #打开摄像头
    def fsm_msg_open_req_rcv_handler(self, msgContent):
        self.timerDisplay = self.tup_timer_start(0.05, self.func_timer_display_process)
        self.fsm_set(self._STM_CAM_DISP)
        return TUP_SUCCESS;
    
    #传回来的显示结果
    def fsm_msg_cam_disp_resp_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_CALIB_VDISP_RESP, TUP_TASK_ID_UI_CALIB, msgContent)
        return TUP_SUCCESS;

    #关闭摄像头与马达
    def fsm_msg_close_req_rcv_handler(self, msgContent):
        self.func_clean_working_env()
        return TUP_SUCCESS;
        
    def funcCalibLogTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_CALIB, myString)
        #SAVE INTO MED FILE
        self.medCmdLog(str(myString))
        #PRINT to local
        self.tup_dbg_print(str(myString))
        return
    
    def funcCalibErrTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_CALIB, myString)
        #SAVE INTO MED FILE
        self.medErrorLog(str(myString));
        #PRINT to local
        self.tup_err_print(str(myString))
        return
    
    #打开定时器干活
    def func_timer_display_process(self):
        self.msg_send(TUP_MSGID_CALIB_VDISP_REQ, TUP_TASK_ID_VISION, '')
        self.timerDisplay = self.tup_timer_start(0.05, self.func_timer_display_process)
        
    #业务函数    
    def func_clean_working_env(self):
        #停止摄像头显示
        if (self.timerDisplay != ''):
            self.tup_timer_stop(self.timerDisplay)
        #停止马达
        self.fsm_set(self._STM_ACTIVE)














        
        
        