'''
Created on 2018年12月10日

@author: Administrator
'''

import random
import time
from multiprocessing import Queue, Process, Pool
from PkgL1vmHandler.ModSysConfig import *
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL1vmHandler.ModVmConsole import *

from PkgL2svrUniv import ModCebsHuicobus
from PkgL3cebsMk2Handler.ModCebsCom import *
from PkgL3cebsMk2Handler.ModCebsCfg import *

from PkgL3cebsMk2Handler import ModCebsCalib
from PkgL3cebsMk2Handler import ModCebsCtrlSchd
from PkgL3cebsMk2Handler import ModCebsGpar
from PkgL3cebsMk2Handler import ModCebsMeng
from PkgL3cebsMk2Handler import ModCebsStest
from PkgL3cebsMk2Handler import ModCebsFspc
from PkgL3cebsMk2Handler import ModCebsMoto
from PkgL3cebsMk2Handler import ModCebsVision


'''
#
# START OF THIS PROGRAM
#
'''   
#项目主入口
def prj_cebsmk2_main_entry():
    '''
    #
    # PAR0: 初始化VM级别的全局参数，以及启动界面
    #
    '''        
    #初始化VM任务层面的参数
    TUP_GL_CFG = tupGlbCfg()
    
    '''
    #
    # PAR1: 全局参数的初始化
    #
    '''
#     #STEP0：判定ini文件是否存在
#     cfgPar = clsL1_ConfigOpr()
#     cfgPar.loadInitFileAndInitGlComPar()
# 
#     #STEP1: INI FILE CONFIGURATION, 初始化配置文件
#     cfgPar.func_read_global_par_from_cfg_file();  #读取本地文件的配置数据，并写入全局变量中来
#     
#     #STEP2: 选择缺省的板孔产品型号
#     GLPLT_PAR_OFC.med_init_plate_product_type()
#     #更新参数 ->这个参数可能会随时更新
#     GLPLT_PAR_OFC.med_init_plate_parameter()

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

    #VM Task
    VmConslTaskInst = tupTaskVmConsl(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_VMCONSL
    initMsg['content'] = ""
    VmConslTaskInst.msg_send_in(initMsg)
    VmConslTaskInst.tup_dbg_print("Create VM task success!")

    #HUICOBUS Basic service Task
    HuicobusTaskInst = ModCebsHuicobus.TupClsCebsHuicobusItf(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_HUICOBUS
    mbuf={}
    mbuf['uplayer'] = TUP_TASK_ID_HUICOBUS
    initMsg['content'] = mbuf
    HuicobusTaskInst.msg_send_in(initMsg)
    HuicobusTaskInst.tup_dbg_print("Create HUICOBUS task success!")

    #Calib Task
    CalibTaskInst = ModCebsCalib.tupTaskCalib(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_CALIB
    initMsg['content'] = ""
    CalibTaskInst.msg_send_in(initMsg)
    CalibTaskInst.tup_dbg_print("Create CALIB task success!")
      
    #CtrlSchd Task
    CtrlSchdTaskInst = ModCebsCtrlSchd.tupTaskCtrlSchd(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_CTRL_SCHD
    CtrlSchdTaskInst.msg_send_in(initMsg)    
    CtrlSchdTaskInst.tup_dbg_print("Create CTRL SCHD task success!")
     
    #Gpar Task
    GparTaskInst = ModCebsGpar.tupTaskGpar(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_GPAR
    GparTaskInst.msg_send_in(initMsg)
    GparTaskInst.tup_dbg_print("Create GPAR task success!")
 
    #Meng Task
    MengTaskInst = ModCebsMeng.tupTaskMeng(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_MENG
    MengTaskInst.msg_send_in(initMsg)    
    MengTaskInst.tup_dbg_print("Create MENG task success!")
 
    #Stest Task
    StestTaskInst = ModCebsStest.tupTaskStest(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_STEST
    StestTaskInst.msg_send_in(initMsg)    
    StestTaskInst.tup_dbg_print("Create STEST task success!")
 
    #Fspc Task
    FspcTaskInst = ModCebsFspc.tupTaskFspc(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_FSPC
    FspcTaskInst.msg_send_in(initMsg)    
    FspcTaskInst.tup_dbg_print("Create FSPC task success!")
         
    #Moto Task
    MotoTaskInst = ModCebsMoto.tupTaskMoto(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_MOTO
    MotoTaskInst.msg_send_in(initMsg)
    MotoTaskInst.tup_dbg_print("Create MOTO task success!")
 
    #Vision Task
    VisionTaskInst = ModCebsVision.tupTaskVision(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_VISION
    VisionTaskInst.msg_send_in(initMsg)
    VisionTaskInst.tup_dbg_print("Create VISION task success!")


    '''
    #
    # PAR3: 程序结束后，清理各个任务
    #
    '''
    #CLOSE ALL TASK: total 12 tasks
    '''
    print("Project CEBS terminate all existing tasks Start!")
    VmConslTaskInst.task_stop()
    HuicobusTaskInst.task_stop()
    CalibTaskInst.task_stop()
    CtrlSchdTaskInst.task_stop()
    GparTaskInst.task_stop()
    MengTaskInst.task_stop()
    StestTaskInst.task_stop()
    FspcTaskInst.task_stop()
    MotoTaskInst.task_stop()
    VisionTaskInst.task_stop()
    print("Project CEBS terminate all existing tasks Accomplish!")
    '''
    '''
    #
    # END OF THIS PROGRAM
    #
    '''      
    
    
    
    