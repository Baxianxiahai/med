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


class tupTaskUiCalib(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    _STM_DEACT  = 4 #界面没激活

    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_UI_CALIB, taskName="TASK_UI_CALIB", glTabEntry=glPar)
        self.fsm_set(TUP_STM_NULL)
        self.fatherUiObj = ''   #父对象界面，双向通信
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TIME_OUT, self.fsm_msg_time_out_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_UI_SWITCH, self.fsm_msg_ui_focus_rcv_handler)

        #业务部分
        #视频流处理完成后需要通知界面，并显示在界面上。这里是通过文件交换的，而非实时内存图片，因为内部消息不支持qt文件对象通过dict数据格式进行交换
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_VDISP_RESP, self.fsm_msg_calib_vdisp_resp_rcv_handler)
        
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_DEACT)
        return TUP_SUCCESS;

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_DEACT)
        return TUP_SUCCESS;
        
    def fsm_msg_time_out_rcv_handler(self, msgContent):
        return TUP_SUCCESS;

    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(msgContent);
        return TUP_SUCCESS;
    
    #界面切换进来
    def fsm_msg_ui_focus_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_CALIB_OPEN_REQ, TUP_TASK_ID_CALIB, "")
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;

    #业务功能
    def fsm_msg_calib_vdisp_resp_rcv_handler(self, msgContent):
        if (self.fatherUiObj == ''):
            print("CALIB_UI task lose 1 print message due to time sync.")
            return TUP_SUCCESS;
        if (msgContent['res'] >= 0):
            self.fatherUiObj.cetk_calib_disp_cam(msgContent['fileName'])        
        return TUP_SUCCESS;
    
    #将界面对象传递给本任务，以便将打印信息送到界面上
    def funcSaveFatherInst(self, instance):
        self.fatherUiObj = instance
    
    def funcDebugPrint2Qt(self, string):
        if (self.fatherUiObj == ''):
            print("CALIB_UI task lose 1 print message due to time sync.")
        else:
            self.fatherUiObj.cetk_debug_print(str(string))
            
    #主界面承接过来的执行函数
    def func_ui_click_pilot_mv(self, scale, dir):
        print("I am func_ui_click_pilot_mv!")

    def func_ui_click_force_move(self, dir):
        print("I am func_ui_click_force_move!")

    def func_ui_click_right_up_set(self):
        print("I am func_ui_click_right_up_set!")

    def func_ui_click_left_down_set(self):
        print("I am func_ui_click_left_down_set!")

    def func_ui_click_pilot_start(self):
        print("I am func_ui_click_pilot_start!")

    def func_ui_click_pilot_stop(self):
        print("I am func_ui_click_pilot_stop!")
        
    def func_ui_click_pilot_move_0(self):
        print("I am func_ui_click_pilot_move_0!")        
        
    def func_ui_click_pilot_move_n(self, holeNbr):
        print("I am func_ui_click_pilot_move_n!")
        
    def func_ui_click_cap_pic_by_hole(self, holeNbr):
        print("I am func_ui_click_cap_pic_by_hole!")        
    
    #清理各项操作：CALIB有遗留马达效应，所以需要发送控制命令给干活的CALIB
    def func_ui_click_calib_close(self):
        print("I am func_ui_click_calib_close!")
        self.msg_send(TUP_MSGID_CALIB_CLOSE_REQ, TUP_TASK_ID_CALIB, "")
        
    #界面切走
    def func_ui_click_calib_switch_to_main(self):
        print("I am func_ui_click_calib_switch_to_main!")
        self.fsm_set(self._STM_DEACT)        




