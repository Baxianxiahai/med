'''
Created on 2018年12月10日

@author: Administrator
'''

import random
import time
from multiprocessing import Queue, Process
from PkgVmHandler import ModVmCfg
from PkgVmHandler import ModVmLayer
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg

from PkgVmHandler import ModVmConsole
from PkgVmHandler import ModVmTimer
from PkgCetkHandler import ModCetkCalib
from PkgCetkHandler import ModCetkCtrlSchd
from PkgCetkHandler import ModCetkGpar
from PkgCetkHandler import ModCetkMeng
from PkgCetkHandler import ModCetkMoto
from PkgCetkHandler import ModCetkVision

from cebsTkL4Ui import *


#项目主入口
def prj_cebs_main_entry():
    #Init basic parameters
    initMsg = {}
    initMsg['mid'] = ModVmCfg.TUP_MSGID_INIT
    initMsg['src'] = ModVmCfg.TUP_TASK_ID_MAIN_ENTRY
    initMsg['content'] = ""

    #VM Task
    VmConslTaskInst = ModVmConsole.tupTaskVmConsl();
    initMsg['dst'] = ModVmCfg.TUP_TASK_ID_VMCONSL
    VmConslTaskInst.msg_send_in(initMsg)
    VmConslTaskInst.tup_dbg_print("Create VM task success!")
    
    #Timer Task
    TimerTaskInst = ModVmTimer.tupTaskTimer();
    initMsg['dst'] = ModVmCfg.TUP_TASK_ID_TIMER
    TimerTaskInst.msg_send_in(initMsg)
    TimerTaskInst.tup_dbg_print("Create TIMER task success!")
    
    #Calib Task
    CalibTaskInst = ModCetkCalib.tupTaskCalib();
    initMsg['dst'] = ModVmCfg.TUP_TASK_ID_CALIB
    CalibTaskInst.msg_send_in(initMsg)
    CalibTaskInst.tup_dbg_print("Create CALIB task success!")
    
    #CtrlSchd Task
    CtrlSchdTaskInst = ModCetkCtrlSchd.tupTaskCtrlSchd();
    initMsg['dst'] = ModVmCfg.TUP_TASK_ID_CTRL_SCHD
    CtrlSchdTaskInst.msg_send_in(initMsg)    
    CtrlSchdTaskInst.tup_dbg_print("Create CTRL SCHD task success!")
    
    #Gpar Task
    GparTaskInst = ModCetkGpar.tupTaskGpar();
    initMsg['dst'] = ModVmCfg.TUP_TASK_ID_GPAR
    GparTaskInst.msg_send_in(initMsg)
    GparTaskInst.tup_dbg_print("Create GPAR task success!")
    
    #Meng Task
    MengTaskInst = ModCetkMeng.tupTaskMeng();
    initMsg['dst'] = ModVmCfg.TUP_TASK_ID_MENG
    MengTaskInst.msg_send_in(initMsg)    
    MengTaskInst.tup_dbg_print("Create MENG task success!")
    
    #Moto Task
    MotoTaskInst = ModCetkMoto.tupTaskMoto();
    initMsg['dst'] = ModVmCfg.TUP_TASK_ID_MOTO
    MotoTaskInst.msg_send_in(initMsg)
    MotoTaskInst.tup_dbg_print("Create MOTO task success!")
        
    #Vision Task
    VisionTaskInst = ModCetkVision.tupTaskVision();
    initMsg['dst'] = ModVmCfg.TUP_TASK_ID_VISION
    VisionTaskInst.msg_send_in(initMsg)
    VisionTaskInst.tup_dbg_print("Create VISION task success!")
    
    #MAIN_UI
    MainUiTaskInst = SEUI_L4_MainWindow();
    initMsg['dst'] = ModVmCfg.TUP_TASK_ID_UI_MAIN
    MainUiTaskInst.msg_send_in(initMsg)            
    MainUiTaskInst.tup_dbg_print("Create MAIN UI task success!")















    
    