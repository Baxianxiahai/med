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

from PkgCetkHandler import ModCetkCalib
from PkgCetkHandler import ModCetkCtrlSchd
from PkgCetkHandler import ModCetkGpar
from PkgCetkHandler import ModCetkMeng
from PkgCetkHandler import ModCetkStest
from PkgCetkHandler import ModCetkMoto
from PkgCetkHandler import ModCetkVision
from PkgCetkHandler import ModCetkUiMain
from PkgCetkHandler import ModCetkUiCalib
from PkgCetkHandler import ModCetkUiGpar
from PkgCetkHandler import ModCetkUiMeng
from PkgCetkHandler import ModCetkUiStest

import cebsTkL4Ui



'''
#
# START OF THIS PROGRAM
#
'''   
#项目主入口
def prj_cebs_main_entry():
    '''
    #
    # PAR0: 初始化VM级别的全局参数，以及启动界面
    #
    '''        
    #初始化VM任务层面的参数
    TUP_GL_CFG = tupGlbCfg()
    
    #START APP and UI：展示启动页面
    app, splash = cebsTkL4Ui.cetk_start_app()
        
    '''
    #
    # PAR1: 全局参数的初始化
    #
    '''
    #STEP0：判定ini文件是否存在
    cfgPar = clsL1_ConfigOpr()
    cfgPar.loadInitFileAndInitGlComPar()

    #STEP1: INI FILE CONFIGURATION, 初始化配置文件
    cfgPar.func_read_global_par_from_cfg_file();  #读取本地文件的配置数据，并写入全局变量中来
    
    #STEP2: 选择缺省的板孔产品型号
    GLPLT_PAR_OFC.med_init_plate_product_type()
    #更新参数 ->这个参数可能会随时更新
    GLPLT_PAR_OFC.med_init_plate_parameter()

    #STEP3: 
    
    
    '''
    #
    # PAR2: 创建各项任务
    #
    '''
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

    #UI_STEST
    StestUiTaskInst = ModCetkUiStest.tupTaskUiStest(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_UI_STEST
    StestUiTaskInst.msg_send_in(initMsg)            
    StestUiTaskInst.tup_dbg_print("Create STEST UI task success!")
        
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

    #Stest Task
    StestTaskInst = ModCetkStest.tupTaskStest(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_STEST
    StestTaskInst.msg_send_in(initMsg)    
    StestTaskInst.tup_dbg_print("Create STEST task success!")
    
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

    '''
    #
    # PAR3: 正式进入用户界面
    #
    '''
    #FINAL QT UI：真正启动界面APP
    cebsTkL4Ui.cetk_show_app(app, splash, MainUiTaskInst, CalibUiTaskInst, GparUiTaskInst, MengUiTaskInst, StestUiTaskInst, 0)



    '''
    #
    # PAR4: 程序结束后，清理各个任务
    #
    '''    
    #CLOSE ALL TASK: total 12 tasks
    print("Project CETK terminate all existing tasks Start!")
    VmConslTaskInst.task_stop()
    MainUiTaskInst.task_stop()
    CalibUiTaskInst.task_stop()
    GparUiTaskInst.task_stop()
    MengUiTaskInst.task_stop()
    StestUiTaskInst.task_stop()
    CalibTaskInst.task_stop()
    CtrlSchdTaskInst.task_stop()
    GparTaskInst.task_stop()
    MengTaskInst.task_stop()
    StestTaskInst.task_stop()
    MotoTaskInst.task_stop()
    VisionTaskInst.task_stop()
    print("Project CETK terminate all existing tasks Accomplish!")
    
    '''
    #
    # END OF THIS PROGRAM
    #
    '''      
    
    
    
    