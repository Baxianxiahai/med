'''
Created on 2018年12月10日

@author: Administrator
'''

import random
import time
from multiprocessing import Queue, Process
from PkgVmHandler import ModVmCfg
from PkgVmHandler import ModVmLayer
from PkgVmHandler import ModVmConsole
from PkgVmHandler import ModVmTimer

#项目主入口
def prj_cebs_main_entry():
    initMsg = {}
    '''
    while True:
        time.sleep(1)
        initMsg['mid'] = ModVmCfg.TUP_MSGID_RESTART
        initMsg['src'] = ModVmCfg.TUP_TASK_ID_TEST
        initMsg['dst'] = ModVmCfg.TUP_TASK_ID_VMCONSL
        initMsg['content'] = "test> " + str(random.random())
        myTaskInst.msg_send_in(initMsg)
    '''
    initMsg['mid'] = ModVmCfg.TUP_MSGID_INIT
    initMsg['src'] = ModVmCfg.TUP_TASK_ID_MAIN_ENTRY
    initMsg['content'] = ""
    #initMsg['content'] = "test> " + str(random.random())

    #VM Task
    VmConslTaskInst = ModVmConsole.tupTaskVmConsl();
    initMsg['dst'] = ModVmCfg.TUP_TASK_ID_VMCONSL
    VmConslTaskInst.msg_send_in(initMsg)
    
    #Timer Task
    TimerTaskInst = ModVmTimer.tupTaskTimer();
    initMsg['dst'] = ModVmCfg.TUP_TASK_ID_TIMER
    TimerTaskInst.msg_send_in(initMsg)    
    
    
    
    
    
    
    