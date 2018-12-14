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

class tupTaskCalib(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    _STM_CAM_DISP = 4
    _STM_MOTO_MV = 5
    
    CAM_DISP_SET = True
    timerDisplay = ''
    TIMER_DISP_CYCLE = 0.4
    
    
    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_CALIB, taskName="TASK_CALIB", glTabEntry=glPar)
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_CALIB, self)
        self.fsm_set(TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)
        
        #业务处理部分
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_OPEN_REQ, self.fsm_msg_open_req_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_CLOSE_REQ, self.fsm_msg_close_req_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_VDISP_RESP, self.fsm_msg_cam_disp_resp_rcv_handler)

        #校准移动命令
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_MOMV_DIR_REQ, self.fsm_msg_moto_mv_dir_req_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_MOMV_DIR_RESP, self.fsm_msg_moto_mv_dir_resp_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_MOFM_DIR_REQ, self.fsm_msg_moto_force_move_dir_req_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_MOFM_DIR_RESP, self.fsm_msg_moto_force_move_dir_resp_rcv_handler)
        
        #校准设置
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_RIGHT_UP_SET, self.fsm_msg_right_up_set_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_LEFT_DOWN_SET, self.fsm_msg_left_down_set_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_MOMV_START, self.fsm_msg_momv_start_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_MOMV_HOLEN, self.fsm_msg_momv_holen_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_PIC_CAP_HOLEN, self.fsm_msg_pic_cap_holen_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_PILOT_START, self.fsm_msg_pilot_start_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_PILOT_STOP, self.fsm_msg_pilot_start_rcv_handler)

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

    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_CALIB, msgContent)
        return TUP_SUCCESS;
        
    #打开摄像头
    def fsm_msg_open_req_rcv_handler(self, msgContent):
        if (self.CAM_DISP_SET == True):
            self.timerDisplay = self.tup_timer_start(self.TIMER_DISP_CYCLE, self.func_timer_display_process)
        self.fsm_set(self._STM_CAM_DISP)
        
        '''
        #每进来一次，照片批次号都被更新一次
        #为什么：因为操作摄像头的读取很麻烦，如果不这样做，会导致摄像头存下的照片相互之间重叠，为了简化这个逻辑，每次校准进来都主动+1批次号码
        
        #这部分代码还有问题，后面待完善
        '''
        #ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX += 1
        #self.createBatch(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX);
        return TUP_SUCCESS;
    
    #传回来的显示结果
    def fsm_msg_cam_disp_resp_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_CALIB_VDISP_RESP, TUP_TASK_ID_UI_CALIB, msgContent)
        return TUP_SUCCESS;
    
    #移动动作需要等待MOTO反馈并解锁状态
    def fsm_msg_moto_mv_dir_req_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_MOTO_MV)
        self.msg_send(TUP_MSGID_CALIB_MOMV_DIR_REQ, TUP_TASK_ID_MOTO, msgContent)
        return TUP_SUCCESS;

    def fsm_msg_moto_mv_dir_resp_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        self.msg_send(TUP_MSGID_CALIB_MOMV_DIR_RESP, TUP_TASK_ID_UI_CALIB, msgContent)
        return TUP_SUCCESS;

    def fsm_msg_moto_force_move_dir_req_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_MOTO_MV)
        self.msg_send(TUP_MSGID_CALIB_MOFM_DIR_REQ, TUP_TASK_ID_MOTO, msgContent)
        return TUP_SUCCESS;

    def fsm_msg_moto_force_move_dir_resp_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        self.msg_send(TUP_MSGID_CALIB_MOFM_DIR_RESP, TUP_TASK_ID_UI_CALIB, msgContent)
        return TUP_SUCCESS;

    #关闭摄像头与马达
    def fsm_msg_close_req_rcv_handler(self, msgContent):
        #摄像头采集
        self.func_clean_working_env()
        #停止马达
        self.msg_send(TUP_MSGID_NORM_MOTO_STOP, TUP_TASK_ID_MOTO, '')
        return TUP_SUCCESS;
        
    def funcCalibLogTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_CALIB, myString)
        #SAVE INTO MED FILE
        self.medCmdLog(str(myString))
        #PRINT to local
        #self.tup_dbg_print(str(myString))
        return
    
    def funcCalibErrTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_CALIB, myString)
        #SAVE INTO MED FILE
        self.medErrorLog(str(myString));
        #PRINT to local
        #self.tup_err_print(str(myString))
        return
    
    #打开定时器干活
    def func_timer_display_process(self):
        self.msg_send(TUP_MSGID_CALIB_VDISP_REQ, TUP_TASK_ID_VISION, '')
        self.timerDisplay = self.tup_timer_start(self.TIMER_DISP_CYCLE, self.func_timer_display_process)
        
    #业务函数    
    def func_clean_working_env(self):
        #停止摄像头显示
        if (self.timerDisplay != ''):
            self.tup_timer_stop(self.timerDisplay)
        #停止马达
        self.fsm_set(self._STM_ACTIVE)

    #设置参数
    def fsm_msg_right_up_set_rcv_handler(self, msgContent):
        ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[2] = ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0];
        ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[3] = ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1];
        ModCebsCom.GLPLT_PAR_OFC.med_update_plate_parameter()
        self.updateSectionPar();
        self.funcCalibLogTrace(str("L3CALIB: RightUp Axis set!  XY=%d/%d." % (ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[2], ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[3])))      
        return TUP_SUCCESS;

    #设置参数
    def fsm_msg_left_down_set_rcv_handler(self, msgContent):
        ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[0] = ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0];
        ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[1] = ModCebsCom.GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1];
        ModCebsCom.GLPLT_PAR_OFC.med_update_plate_parameter()
        self.updateSectionPar();
        self.funcCalibLogTrace("L3CALIB: LeftDown Axis set! XY=%d/%d." % (ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[0], ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[1]))
        return TUP_SUCCESS;

    #移动命令
    def fsm_msg_momv_start_rcv_handler(self, msgContent):
        self.funcCalibLogTrace("L3CALIB: Move to Hole#0 point.")
        self.msg_send(TUP_MSGID_CALIB_MOMV_START, TUP_TASK_ID_MOTO, '')
        return TUP_SUCCESS;

    #移动命令
    def fsm_msg_momv_holen_rcv_handler(self, msgContent):
        holeIndex = int(msgContent['holeNbr'])
        newHoldNbr = self.funcCheckHoldNumber(holeIndex)
        mbuf={}
        mbuf['holeNbr'] = newHoldNbr        
        self.funcCalibLogTrace(str("L3CALIB: Move to Hole#%d point." % (int(msgContent['holeNbr']))))
        self.msg_send(TUP_MSGID_CALIB_MOMV_HOLEN, TUP_TASK_ID_MOTO, mbuf)
        return TUP_SUCCESS;

    def funcCheckHoldNumber(self, holeNbr):
        if (holeNbr <= 0):
            return 1;
        if (holeNbr >= ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH):
            return ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH
        return holeNbr

    #截图命令
    def fsm_msg_pic_cap_holen_rcv_handler(self, msgContent):
        holeIndex = int(msgContent['holeNbr'])
        newHoldNbr = self.funcCheckHoldNumber(holeIndex)
        mbuf={}
        mbuf['holeNbr'] = newHoldNbr        
        self.funcCalibLogTrace(str("L3CALIB: Capture picture with Hole#%d point." % (int(msgContent['holeNbr']))))
        self.msg_send(TUP_MSGID_CALIB_PIC_CAP_HOLEN, TUP_TASK_ID_VISION, mbuf)
        return TUP_SUCCESS;
    
    #巡游开始
    def fsm_msg_pilot_start_rcv_handler(self, msgContent):
        return TUP_SUCCESS;
    
    #巡游停止
    def fsm_msg_pilot_stop_rcv_handler(self, msgContent):
        return TUP_SUCCESS;



        
        
        