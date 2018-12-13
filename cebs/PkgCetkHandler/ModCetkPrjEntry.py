'''
Created on 2018年12月10日

@author: Administrator
'''

import random
import time
from multiprocessing import Queue, Process, Pool
from PkgVmHandler.ModVmCfg import *
from PkgVmHandler.ModVmLayer import *
from PkgCebsHandler.ModCebsCom import *
from PkgCebsHandler.ModCebsCfg import *
from PkgVmHandler.ModVmConsole import *
from PkgVmHandler.ModVmTimer import *

from PkgCetkHandler import ModCetkCalib
from PkgCetkHandler import ModCetkCtrlSchd
from PkgCetkHandler import ModCetkGpar
from PkgCetkHandler import ModCetkMeng
from PkgCetkHandler import ModCetkMoto
from PkgCetkHandler import ModCetkVision
from PkgCetkHandler import ModCetkUiMain
from PkgCetkHandler import ModCetkUiCalib
from PkgCetkHandler import ModCetkUiGpar
from PkgCetkHandler import ModCetkUiMeng

import cebsTkL4Ui


#项目主入口
def prj_cebs_main_entry():
    #初始化全局变量表
    TUP_GL_CFG = tupGlbCfg()
    
    #START APP and UI：展示启动页面
    app, splash = cebsTkL4Ui.cetk_start_app()
    
    #Init message and prepare send to all task, to make them transferred into ACTIVE state
    initMsg = {}
    initMsg['mid'] = TUP_MSGID_INIT
    initMsg['src'] = TUP_TASK_ID_TUPCONSL
    initMsg['content'] = ""

    #VM Task
    VmConslTaskInst = tupTaskVmConsl(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_VMCONSL
    VmConslTaskInst.msg_send_in(initMsg)
    VmConslTaskInst.tup_dbg_print("Create VM task success!")
    
    #Timer Task
    TimerTaskInst = tupTaskTimer(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_TIMER
    TimerTaskInst.msg_send_in(initMsg)
    TimerTaskInst.tup_dbg_print("Create TIMER task success!")

    #UI_MAIN
    MainUiTaskInst = ModCetkUiMain.tupTaskUiMain(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_UI_MAIN
    MainUiTaskInst.msg_send_in(initMsg)            
    MainUiTaskInst.tup_dbg_print("Create MAIN UI task success!")

    #UI_CALIB
    CalibUiTaskInst = ModCetkUiCalib.tupTaskUiCalib(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_UI_CALIB
    CalibUiTaskInst.msg_send_in(initMsg)            
    CalibUiTaskInst.tup_dbg_print("Create CALIB UI task success!")

    #UI_GPAR
    GparUiTaskInst = ModCetkUiGpar.tupTaskUiGpar(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_UI_GPAR
    GparUiTaskInst.msg_send_in(initMsg)            
    GparUiTaskInst.tup_dbg_print("Create GPAR UI task success!")

    #UI_MENG
    MengUiTaskInst = ModCetkUiMeng.tupTaskUiMeng(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_UI_MENG
    MengUiTaskInst.msg_send_in(initMsg)            
    MengUiTaskInst.tup_dbg_print("Create MENG UI task success!")
        
    #Calib Task
    CalibTaskInst = ModCetkCalib.tupTaskCalib(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_CALIB
    CalibTaskInst.msg_send_in(initMsg)
    CalibTaskInst.tup_dbg_print("Create CALIB task success!")
    
    #CtrlSchd Task
    CtrlSchdTaskInst = ModCetkCtrlSchd.tupTaskCtrlSchd(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_CTRL_SCHD
    CtrlSchdTaskInst.msg_send_in(initMsg)    
    CtrlSchdTaskInst.tup_dbg_print("Create CTRL SCHD task success!")
    
    #Gpar Task
    GparTaskInst = ModCetkGpar.tupTaskGpar(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_GPAR
    GparTaskInst.msg_send_in(initMsg)
    GparTaskInst.tup_dbg_print("Create GPAR task success!")

    #Meng Task
    MengTaskInst = ModCetkMeng.tupTaskMeng(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_MENG
    MengTaskInst.msg_send_in(initMsg)    
    MengTaskInst.tup_dbg_print("Create MENG task success!")

    #Moto Task
    MotoTaskInst = ModCetkMoto.tupTaskMoto(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_MOTO
    MotoTaskInst.msg_send_in(initMsg)
    MotoTaskInst.tup_dbg_print("Create MOTO task success!")

    #Vision Task
    VisionTaskInst = ModCetkVision.tupTaskVision(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_VISION
    VisionTaskInst.msg_send_in(initMsg)
    VisionTaskInst.tup_dbg_print("Create VISION task success!")
               
    #FINAL QT UI：真正启动界面APP
    cebsTkL4Ui.cetk_show_app(app, splash, MainUiTaskInst, CalibUiTaskInst, GparUiTaskInst, MengUiTaskInst, 0)
    
    #CLOSE ALL TASK: total 12 tasks
    print("Project CETK terminate all existing tasks!")
    VmConslTaskInst.terminate()
    TimerTaskInst.terminate()
    MainUiTaskInst.terminate()
    CalibUiTaskInst.terminate()
    GparUiTaskInst.terminate()
    MengUiTaskInst.terminate()
    CalibTaskInst.terminate()
    CtrlSchdTaskInst.terminate()
    GparTaskInst.terminate()
    MengTaskInst.terminate()
    MotoTaskInst.terminate()
    VisionTaskInst.terminate()
    
    
    
    
    
    