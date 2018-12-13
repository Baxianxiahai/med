'''
Created on 2018年12月8日

@author: Administrator
'''

import random
import time
import threading
from multiprocessing import Queue, Process
from PkgVmHandler.ModVmCfg import *


'''
全局常量
'''
TUP_SUCCESS = 1
TUP_FAILURE = -1
#三个基础状态
TUP_STM_NULL = 0
TUP_STM_INIT = 1
TUP_STM_COMN = 2
#给入口参数做初始化
TUP_INIT_VALUE = -1
#定时器相关定义
TUP_TIMER_ONE_TIME  = 1
TUP_TIMER_PERIOD    = 2
#PROCE or THREAD MODE
TUP_TASK_PROCESS_MODE = 1
TUP_TASK_THREAD_MODE = 2
TUP_TASK_CUR_MOD = TUP_TASK_THREAD_MODE

'''
全局配置参数

技巧1： self.timerTab = [{'tid':i, 'type':'oneTime', 'cnt':0, 'act': False} for i in range(self.TUP_TIMER_MAX)]

技巧2： self.timerTab = [{'tid':i, 'type':'oneTime', 'cnt':0, 'act': False} for i in range(self.TUP_TIMER_MAX)]
'''
class tupGlbCfg():
    def __init__(self):
        self.dbg_level = 1
        self.TUP_MSGID_MAX = 1000;
        self.TUP_STATE_MAX = 50;
        self.TUP_TASK_MAX = 200;
        self.TUP_TIMER_MAX = 200;
        self.queTab = [Queue() for i in range(self.TUP_TASK_MAX)]
        self.timerTab = [{'type':TUP_TIMER_ONE_TIME, 'cnt':0, 'act': False} for i in range(self.TUP_TIMER_MAX)]

'''
基础任务模板
'''
class tupTaskTemplate():
    taskId = 0;
    taskName = '';
    glTab = '';
    queue = '';
    process = '';
    state = 0;
    msgStateMatrix = []
    
    def __init__(self, taskid, taskName, glTabEntry):
        super(tupTaskTemplate, self).__init__()
        self.taskId = taskid;
        self.taskName = taskName;
        self.glTab = glTabEntry;
        self.queue = self.glTab.queTab[taskid];
        self.process = '';
        self.state = 0;
        self.msgStateMatrix = [[TUP_INIT_VALUE for i in range(self.glTab.TUP_MSGID_MAX)] for j in range(self.glTab.TUP_STATE_MAX)]
        self.task_create();
        
    def get_task_id(self):
        return self.taskId

    def get_task_name(self):
        return self.taskName

    def get_task_queue(self):
        return self.queue

    def get_task_process(self):
        return self.process

    def fsm_set(self, newState):
        if (newState < 0) or (newState >= self.glTab.TUP_STATE_MAX):
            self.tup_err_print("[VM ERR] fsm_set Error.")
            return -1;
        self.state = newState
        return 1;
    
    def fsm_get(self):
        return self.state

    def msg_send_in(self, msg):
        self.queue.put(msg)
        if (self.glTab.dbg_level == 1):
            self.tup_trace(str(msg))

    def msg_send_out(self, taskDestId, msg):
        if (taskDestId <0) or (taskDestId >= self.glTab.TUP_TASK_MAX):
            self.tup_err_print("Wrong Task Id.")
            return TUP_FAILURE;
        #print("MsgQue = ", TUP_GL_CFG.queTab[taskDestId])
        self.glTab.queTab[taskDestId].put(msg)
        if (self.glTab.dbg_level == 1):
            self.tup_trace(str(msg))

    def msg_send(self, mid, dst, content):
        msgSnd = {}
        msgSnd['mid'] = mid
        msgSnd['src'] = self.taskId
        msgSnd['dst'] = dst
        msgSnd['content'] = content
        if (self.taskId == dst):
            self.msg_send_in(msgSnd)
        else:
            self.msg_send_out(dst, msgSnd)            

    def add_stm_combine(self, state, msgid, proc):
        if (state < 0) or (state >= self.glTab.TUP_STATE_MAX) or (msgid < 0) or (msgid >= self.glTab.TUP_MSGID_MAX):
            self.tup_err_print("Add_stm_combine Error.")
            return -1
        self.msgStateMatrix[state][msgid] = proc
        return 1
    
    #进程和线程方法
    def task_create(self):
        #线程模式
        if (TUP_TASK_CUR_MOD == TUP_TASK_THREAD_MODE):
            self.process = threading.Thread(target=self.task_handler_enginee, args=(self.queue,))
        #进程模式
        else:
            self.process = Process(target=self.task_handler_enginee, args=(self.queue,))
            
    def task_handler_enginee(self, myque):
        while True:
            result = myque.get()
            msgId = int(result['mid'])
            srcId = int(result['src'])
            dstId = int(result['dst'])
            msgCont = result['content']
            if (msgId <0) or (msgId >= self.glTab.TUP_MSGID_MAX):
                self.tup_err_print("Wrong msgId parameter.")
                continue
            if (srcId <0) or (srcId >= self.glTab.TUP_TASK_MAX):
                self.tup_err_print("Wrong srcId parameter.")
                continue
            if (dstId <0) or (dstId >= self.glTab.TUP_TASK_MAX):
                self.tup_err_print("Wrong dstId parameter.")
                continue
            if (dstId != self.taskId):
                self.tup_err_print("Wrong destination module, self srcId = %d, dstId=%d." % (self.taskId, dstId) )
                continue
            #CASE1: 首先确定COMN状态机，忽略当前的消息执行
            if self.msgStateMatrix[TUP_STM_COMN][msgId] != TUP_INIT_VALUE:
                proc = self.msgStateMatrix[TUP_STM_COMN][msgId]
                if (proc(msgCont) == TUP_FAILURE):
                    self.tup_err_print("Proc execute error, Src/Dst/MsgId=%d/%d/%d, MsgContent=%s" % (srcId, dstId, msgId, str(msgCont)))
                continue
            #CASE2: NOT EXIST
            if self.msgStateMatrix[self.state][msgId] == TUP_INIT_VALUE:
                self.tup_err_print("Un-valid state-message set, inc State/MsgId=%d/%d" % (self.state, msgId))
                continue
            #CASE3: EXIST RIGHT STM
            proc = self.msgStateMatrix[self.state][msgId]
            if (proc(msgCont) == TUP_FAILURE):
                self.tup_err_print("Proc execute error, Src/Dst/MsgId=%d/%d/%d, MsgContent=%s" % (srcId, dstId, msgId, str(msgCont)))
            continue

    def task_run(self):
        self.process.start()

    def tup_trace(self, string):
        print(time.asctime(), ", [TRC] [", self.taskName, "]: ", str(string))

    def tup_dbg_print(self, string):
        print(time.asctime(), ", [DBG] [", self.taskName, "]: ", str(string))
        
    def tup_err_print(self, string):
        print(time.asctime(), ", [ERR] [", self.taskName, "]: ", str(string))
    
    #秒级定时器
    def tup_timer_start(self, durInSec, funcCb):
        timer = threading.Timer(durInSec, funcCb)
        if timer == '':
            self.tup_err_print("Create timer error!")
            return
        timer.start()
        return timer

    def tup_timer_stop(self, timer):
        timer.cancel()
        
        
