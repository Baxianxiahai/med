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


class tupTaskUiGpar(tupClassUiBasic):
    _STM_WORKING = 5    #从5开始属于任务私有部分

    def __init__(self, glPar):
        tupClassUiBasic.__init__(self, taskidUb=TUP_TASK_ID_UI_GPAR, taskNameUb="TASK_UI_GPAR", glParUb=glPar)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_GPAR_UI_SWITCH, self.fsm_msg_ui_focus_rcv_handler)
        #业务处理函数
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_GPAR_PIC_TRAIN_RESP, self.fsm_msg_pic_train_resp_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_GPAR_PIC_FCC_RESP, self.fsm_msg_pic_flu_cell_count_resp_rcv_handler)
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    #清理各项操作 - 重载
    def func_ui_click_basic_close(self):
        print("I am func_ui_click_gpar_close!")
        self.msg_send(TUP_MSGID_GPAR_CLOSE_REQ, TUP_TASK_ID_GPAR, "")
                
    #业务处理部分
    def fsm_msg_pic_train_resp_rcv_handler(self, msgContent):
        if (msgContent['res'] < 0):
            self.funcDebugPrint2Qt("Open train picture failure!");
        else:
            if (self.fatherUiObj != ''):
                self.fatherUiObj.gpar_callback_train_resp(msgContent['fileName'])
        return TUP_SUCCESS;
    
    #复用上面的显示过程
    def fsm_msg_pic_flu_cell_count_resp_rcv_handler(self, msgContent):
        if (msgContent['res'] < 0):
            self.funcDebugPrint2Qt("Open Flu Cell Count picture failure!");
        else:
            if (self.fatherUiObj != ''):
                self.fatherUiObj.gpar_callback_train_resp(msgContent['fileName'])
        return TUP_SUCCESS;

    #将界面参数传递给业务模块
    def funcGparInitBascPar(self, orgWidth, orgHeight, cfyWidth, cfyHeight):
        mbuf = {}
        mbuf['orgWidth'] = orgWidth
        mbuf['orgHeight'] = orgHeight
        mbuf['cfyWidth'] = cfyWidth
        mbuf['cfyHeight'] = cfyHeight
        self.msg_send(TUP_MSGID_GPAR_INIT_INF, TUP_TASK_ID_GPAR, mbuf)
                
    #主界面承接过来的执行函数   
    def func_ui_click_pic_train(self, fileName, liPar1, liPar2, liPar3, liPar4, addupSet, gePar1, gePar2, gePar3, gePar4):
        print("I am func_ui_click_pic_train!")
        #LC:before click train you need to send message to refresh train pars
        mbuf={}
        mbuf['baseLimit'] = liPar1; 
        mbuf['small2Mid'] = liPar2;
        mbuf['mid2Big'] = liPar3;
        mbuf['bigLimit'] = liPar4;
        mbuf['addupSet'] = addupSet;
        mbuf['genrPar1'] = gePar1;
        mbuf['genrPar2'] = gePar2;
        mbuf['genrPar3'] = gePar3;
        mbuf['genrPar4'] = gePar4;
        self.msg_send(TUP_MSGID_GPAR_REFRESH_PAR, TUP_TASK_ID_VISION, mbuf) 
        mbuf={}
        mbuf['fileName'] = fileName
        self.msg_send(TUP_MSGID_GPAR_PIC_TRAIN_REQ, TUP_TASK_ID_GPAR, mbuf)
    
    def func_ui_click_gpar_refresh_par(self):
        print("I am func_ui_click_gpar_refresh_par!")
        mbuf={}
        mbuf['baseLimit'] = GLVIS_PAR_OFC.SMALL_LOW_LIMIT 
        mbuf['small2Mid'] = GLVIS_PAR_OFC.SMALL_MID_LIMIT 
        mbuf['mid2Big'] = GLVIS_PAR_OFC.MID_BIG_LIMIT 
        mbuf['bigLimit'] = GLVIS_PAR_OFC.BIG_UPPER_LIMIT
        mbuf['addupSet'] = GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET
        mbuf['genrPar1'] = GLVIS_PAR_OFC.CFY_THD_GENR_PAR1
        mbuf['genrPar2'] = GLVIS_PAR_OFC.CFY_THD_GENR_PAR2
        mbuf['genrPar3'] = GLVIS_PAR_OFC.CFY_THD_GENR_PAR3
        mbuf['genrPar4'] = GLVIS_PAR_OFC.CFY_THD_GENR_PAR4
        self.msg_send(TUP_MSGID_GPAR_REFRESH_PAR, TUP_TASK_ID_VISION, mbuf)        
    
    #荧光细胞计数        
    def func_ui_click_gpar_flu_cell_cnt(self, fileName, liPar1, liPar2, liPar3, liPar4, addupSet, gePar1, gePar2, gePar3, gePar4):
        print("I am func_ui_click_gpar_flu_cell_cnt!")
        mbuf={}
        mbuf['baseLimit'] = liPar1; 
        mbuf['small2Mid'] = liPar2;
        mbuf['mid2Big'] = liPar3;
        mbuf['bigLimit'] = liPar4;
        mbuf['addupSet'] = addupSet;
        mbuf['genrPar1'] = gePar1;
        mbuf['genrPar2'] = gePar2;
        mbuf['genrPar3'] = gePar3;
        mbuf['genrPar4'] = gePar4;
        self.msg_send(TUP_MSGID_GPAR_REFRESH_PAR, TUP_TASK_ID_VISION, mbuf) 
        mbuf={}
        mbuf['fileName'] = fileName 
        self.msg_send(TUP_MSGID_GPAR_PIC_FCC_REQ, TUP_TASK_ID_GPAR, mbuf)
        

        
        
        

















