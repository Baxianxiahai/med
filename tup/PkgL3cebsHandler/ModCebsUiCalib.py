'''
Created on 2018年12月11日

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
from PkgL3cebsHandler.ModCebsUiBasic import *


class tupTaskUiCalib(tupClassUiBasic):
    _STM_WORKING = 5    #从5开始属于任务私有部分

    def __init__(self, glPar):
        tupClassUiBasic.__init__(self, taskidUb=TUP_TASK_ID_UI_CALIB, taskNameUb="TASK_UI_CALIB", glParUb=glPar)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_UI_SWITCH, self.fsm_msg_ui_focus_rcv_handler)
        #业务部分
        #视频流处理完成后需要通知界面，并显示在界面上。这里是通过文件交换的，而非实时内存图片，因为内部消息不支持qt文件对象通过dict数据格式进行交换
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_VDISP_RESP, self.fsm_msg_calib_vdisp_resp_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_MOMV_DIR_RESP, self.fsm_msg_momv_dir_resp_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_MOFM_DIR_RESP, self.fsm_msg_force_move_dir_resp_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CAL_BLURRY_RET_VALUE,self.fsm_msg_cal_blurry_handler)
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    
    #界面切换进来 - 重载
    def fsm_msg_ui_focus_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_CALIB_OPEN_REQ, TUP_TASK_ID_CALIB, "")
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;

    #清理各项操作：CALIB有遗留马达效应，所以需要发送控制命令给干活的CALIB
    def func_ui_click_basic_close(self):
        print("I am func_ui_click_calib_close!")
        self.msg_send(TUP_MSGID_CALIB_CLOSE_REQ, TUP_TASK_ID_CALIB, "")
        self.msg_send(TUP_MSGID_CTRL_SCHD_SWITCH_ON, TUP_TASK_ID_CTRL_SCHD, "")
        self.msg_send(TUP_MSGID_MAIN_UI_SWITCH,TUP_TASK_ID_VISION,"")
        
        
        
        return
    
    '''
    #业务功能
    #之前采用了文件模式，目前采用指针对象模式
    #为啥没有将图像采集及展示全部放在UI界面中：为了对摄像头的访问进行排序处理，防止同步抢占的问题
    #self.fatherUiObj.cetk_calib_disp_cam(msgContent['fileName'])
    '''
    def fsm_msg_calib_vdisp_resp_rcv_handler(self, msgContent):
        if (self.fatherUiObj == ''):
            print("CALIB_UI task lose 1 print message due to time sync.")
            return TUP_SUCCESS;
        if (msgContent['res'] >= 0) and (GLVIS_PAR_OFC.CALIB_VDISP_OJB != ''):
            self.fatherUiObj.cetk_calib_disp_cam_by_obj(GLVIS_PAR_OFC.CALIB_VDISP_OJB)
            return TUP_SUCCESS;
        else:
            return TUP_FAILURE;
        
    #将马达移动的结果提示在界面上
    def fsm_msg_momv_dir_resp_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(str(msgContent))
        return TUP_SUCCESS;    

    def fsm_msg_force_move_dir_resp_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(str(msgContent))
        return TUP_SUCCESS;    
    
    def fsm_msg_cal_blurry_handler(self, msgContent):   
        if (self.fatherUiObj == ''):
            print("CAL_UI task lose 1 print message due to time sync.")
        else:      
            self.fatherUiObj.cal_callback_blurry_ret(msgContent['res'])
        return TUP_SUCCESS;         
    #主界面承接过来的执行函数
    def func_ui_click_pilot_mv(self, scale, dir):
        print("I am func_ui_click_pilot_mv!")
        mbuf={}
        mbuf['scale'] = scale
        mbuf['dir'] = dir
        self.msg_send(TUP_MSGID_CALIB_MOMV_DIR_REQ, TUP_TASK_ID_CALIB, mbuf)
        return
    
    def func_ui_click_force_move(self, dir):
        print("I am func_ui_click_force_move!")
        mbuf={}
        mbuf['dir'] = dir
        self.msg_send(TUP_MSGID_CALIB_MOFM_DIR_REQ, TUP_TASK_ID_CALIB, mbuf)
        return

    def func_ui_click_right_up_set(self):
        print("I am func_ui_click_right_up_set!")
        mbuf={}
        self.msg_send(TUP_MSGID_CALIB_RIGHT_UP_SET, TUP_TASK_ID_CALIB, mbuf)
        return

    def func_ui_click_left_down_set(self):
        print("I am func_ui_click_left_down_set!")
        mbuf={}
        self.msg_send(TUP_MSGID_CALIB_LEFT_DOWN_SET, TUP_TASK_ID_CALIB, mbuf)
        return

    def func_ui_click_pilot_start(self):
        print("I am func_ui_click_pilot_start!")
        self.msg_send(TUP_MSGID_CALIB_PILOT_START, TUP_TASK_ID_CALIB, "")
        return

    def func_ui_click_pilot_stop(self):
        print("I am func_ui_click_pilot_stop!")
        self.msg_send(TUP_MSGID_CALIB_PILOT_STOP, TUP_TASK_ID_CALIB, "")
        return
        
    def func_ui_click_pilot_move_0(self):
        print("I am func_ui_click_pilot_move_0!")        
        self.msg_send(TUP_MSGID_CALIB_MOMV_START, TUP_TASK_ID_CALIB, "")
        return
        
    def func_ui_click_pilot_move_n(self, holeNbr):
        print("I am func_ui_click_pilot_move_n!")
        mbuf={}
        mbuf['holeNbr'] = holeNbr
        self.msg_send(TUP_MSGID_CALIB_MOMV_HOLEN, TUP_TASK_ID_CALIB, mbuf)
        return
        
    def func_ui_click_cap_pic_by_hole(self, holeNbr):
        print("I am func_ui_click_cap_pic_by_hole!")
        mbuf={}
        mbuf['holeNbr'] = holeNbr
        self.msg_send(TUP_MSGID_CALIB_PIC_CAP_HOLEN, TUP_TASK_ID_CALIB, mbuf)
        return                   
    





