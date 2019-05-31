'''
Created on 2018年12月8日

@author: Administrator
'''

import random
import time
from multiprocessing import Queue, Process
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL3cebsMk2Handler.ModCebsCom import *
from PkgL3cebsMk2Handler.ModCebsCfg import *
from PkgL1vmHandler.ModVmConsole import *


class tupTaskCtrlSchd(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    #拍照阶段
    _STM_PIC_CAP_EXEC = 4
    _STM_FLU_CAP_EXEC = 5
    #识别阶段
    _STM_PIC_CFY_EXEC = 6
    _STM_FLU_CFY_EXEC = 7
    #归零阶段
    _STM_ZERO_EXEC = 8
    _STM_DEACT = 9
    
    #TIMER1
    #启动后是否自动干活的定时器，因为要等待归零，所以必须等待一会儿
    timerStartWorkDirAfterMvZero = ''
    TIMER_DUR_START_WK_AFTER_ZERO = 15

    #TIMER2
    #启动第二个定时器：定时自动拍照
    timerStartWorkDirAfterFixTti = ''
    
    #TIMER3
    #密码验证并控制是否继续干活
    timerMdcPswdChk = ''
    TIMER_DUR_MDC_PSWD_CHK = 60*60  #保留一个小时


    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_CTRL_SCHD, taskName="TASK_CTRL_SCHD", glTabEntry=glPar)
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_CTRL_SCHD, self)
        self.fsm_set(TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_com_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_EXIT, self.fsm_com_msg_exit_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_com_msg_test_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CRTS_MDC_CHK_PSWD_RESP, self.fsm_msg_mdc_pswd_chk_resp_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_HW_REL, self.fsm_msg_ctrl_schd_hw_release_rcv_handler) #有可能启动定时器，需要退出
        
        #控制业务逻辑
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CTRL_SCHD_SWITCH_ON, self.fsm_msg_switch_on_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CTRL_SCHD_SWITCH_OFF, self.fsm_msg_switch_off_rcv_handler)

        #业务干活过程-归零
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CTRL_SCHD_MV_ZERO, self.fsm_msg_move_back_zero_rcv_handler)
        self.add_stm_combine(self._STM_ZERO_EXEC, TUP_MSGID_CTRS_MOTO_ZERO_RESP, self.fsm_msg_moto_zero_resp_rcv_handler)
        
        #业务干活过程-拍照-强制开始和停止-PICTURE
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CTRL_SCHD_CAPPIC_START, self.fsm_msg_capture_normal_pic_rcv_handler)
        self.add_stm_combine(self._STM_PIC_CAP_EXEC, TUP_MSGID_CTRL_SCHD_CAPPIC_STOP, self.fsm_msg_capture_pic_stop_rcv_handler)

        #业务干活过程-拍照-启动之后，PICTURE图像读取的控制过程
        self.add_stm_combine(self._STM_PIC_CAP_EXEC, TUP_MSGID_CTRS_MOTO_MV_HN_RESP, self.fsm_msg_ctrs_moto_mv_hn_resp_rcv_handler)
        self.add_stm_combine(self._STM_PIC_CAP_EXEC, TUP_MSGID_CTRS_PIC_CAP_RESP, self.fsm_msg_ctrs_pic_cap_resp_rcv_handler)

        #业务干活过程-拍照-强制开始和停止-FLU荧光
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CTRL_SCHD_CAPFLU_START, self.fsm_msg_capture_flu_pic_rcv_handler)
        self.add_stm_combine(self._STM_FLU_CAP_EXEC, TUP_MSGID_CTRL_SCHD_CAPPIC_STOP, self.fsm_msg_capture_pic_stop_rcv_handler)

        #业务干活过程-拍照-启动之后，FLU荧光图像读取的控制过程
        self.add_stm_combine(self._STM_FLU_CAP_EXEC, TUP_MSGID_CTRS_MOTO_MV_HN_RESP, self.fsm_msg_ctrs_moto_mv_hn_resp_rcv_handler)
        self.add_stm_combine(self._STM_FLU_CAP_EXEC, TUP_MSGID_CTRS_FLU_CAP_RESP, self.fsm_msg_ctrs_flu_cap_resp_rcv_handler)

        #业务干活过程-识别图像 - 启动停止命令
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CTRL_SCHD_CFYPIC_START, self.fsm_msg_classify_normal_pic_start_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CTRL_SCHD_CFYFLU_START, self.fsm_msg_classify_flu_pic_start_rcv_handler)
        self.add_stm_combine(self._STM_PIC_CFY_EXEC, TUP_MSGID_CTRL_SCHD_CFYPIC_STOP, self.fsm_msg_classify_pic_stop_rcv_handler)
        self.add_stm_combine(self._STM_FLU_CFY_EXEC, TUP_MSGID_CTRL_SCHD_CFYPIC_STOP, self.fsm_msg_classify_pic_stop_rcv_handler)

        #业务干活过程-识别图像-运行过程反馈
        self.add_stm_combine(self._STM_PIC_CFY_EXEC, TUP_MSGID_CRTS_PIC_CLFY_RESP, self.fsm_msg_classify_pic_accomplish_rcv_handler)
        self.add_stm_combine(self._STM_FLU_CFY_EXEC, TUP_MSGID_CRTS_FLU_CLFY_RESP, self.fsm_msg_classify_flu_accomplish_rcv_handler)
        
        #STEST查询
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_STEST_CTRL_SCHD_INQ, self.fsm_msg_stest_inq_rcv_handler)
        
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    def __del__(self):
        try:
            self.tup_timer_stop(self.timerMdcPswdChk)
            self.tup_timer_stop(self.timerStartWorkDirAfterMvZero)
            self.tup_timer_stop(self.timerStartWorkDirAfterFixTti)
        except Exception:
            pass

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        #控制图像工作的序号
        self.picSeqCnt = 0  #图像识别次序号
        
        #搜索到的图像识别批次和文件临时号：这个信息是必须的，不然需要每次都传给下面的模块然后再传回来，太累赘
        self.cfyBat = 0;
        self.cfyFileNbr = 0;

        #启动定时器，准备自动干活
        if (GLVIS_PAR_OFC.PIC_AUTO_WORKING_AFTER_START_SET == True):
            self.timerStartWorkDirAfterMvZero = self.tup_timer_start(self.TIMER_DUR_START_WK_AFTER_ZERO, self.func_timer_start_work_after_mv_zero)
        
        #查询PSWD
        time.sleep(1)
        self.msg_send(TUP_MSGID_CRTS_MDC_CHK_PSWD_REQ, TUP_TASK_ID_MOTO, "")
        
        #TEST测试区域

        return TUP_SUCCESS;

    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MAIN, msgContent)
        return TUP_SUCCESS;

    #CHECK PSWD
    def fsm_msg_mdc_pswd_chk_resp_rcv_handler(self, msgContent):
        res = msgContent['res']
        pswd = msgContent['pswd']
        
        #start timer
        if (res < 0) or (self.func_pswd_check(pswd) != True):
            self.timerMdcPswdChk = self.tup_timer_start(self.TIMER_DUR_MDC_PSWD_CHK, self.func_timer_start_after_check_pswd_failure)        
        return TUP_SUCCESS;
    
    #停止定时器的操作
    def fsm_msg_ctrl_schd_hw_release_rcv_handler(self, msgContent):
        try:
            if (self.timerMdcPswdChk != ''):
                self.tup_timer_stop(self.timerMdcPswdChk)
        except Exception:
            pass
        try:
            if (self.timerStartWorkDirAfterMvZero != ''):
                self.tup_timer_stop(self.timerStartWorkDirAfterMvZero)
        except Exception:
            pass
        try:
            if (self.timerStartWorkDirAfterFixTti != ''):
                self.tup_timer_stop(self.timerStartWorkDirAfterFixTti)
        except Exception:
            pass
        return TUP_SUCCESS;
    
    def funcCtrlSchdLogTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MAIN, myString)
        #SAVE INTO MED FILE
        self.medCmdLog(str(myString))
        #PRINT to local
        self.tup_dbg_print(str(myString))
        return
    
    def funcCtrlSchdErrTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MAIN, myString)
        #SAVE INTO MED FILE
        self.medErrorLog(str(myString));
        #PRINT to local
        self.tup_err_print(str(myString))
        return        
    
    #通知界面，退出程序
    def func_timer_start_after_check_pswd_failure(self):
        self.msg_send(TUP_MSGID_CRTS_MDC_CHK_PSWD_RESP, TUP_TASK_ID_UI_MAIN, "")
        return
    
    #检查PSWD
    def func_pswd_check(self, input):
        res = 0;
        for i in range(0, 16):
            mask = 1<<(2*i+1)
            tmp = input & mask;
            tmp = tmp>>(i+1)
            res += tmp;
        if (res == 0xAB56):
            return True;
        else:
            return False;

    
    '''
    #业务处理部分 - 界面切换
    '''
    #切换处理
    def fsm_msg_switch_on_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;

    def fsm_msg_switch_off_rcv_handler(self, msgContent):
        #停止正在识别或者读取的图像
        self.fsm_set(self._STM_DEACT)
        return TUP_SUCCESS;


    '''
    #归零过程
    '''    
    #归零处理
    def fsm_msg_move_back_zero_rcv_handler(self, msgContent):
        self.funcCtrlSchdLogTrace("L3SCHD: Start to move zero!")
        self.fsm_set(self._STM_ZERO_EXEC)
        mbuf={}
        mbuf['maxTry'] = GLSPS_PAR_OFC.MOTOR_MAX_RETRY_TIMES
        self.msg_send(TUP_MSGID_CTRS_MOTO_ZERO_REQ, TUP_TASK_ID_MOTO, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_moto_zero_resp_rcv_handler(self, msgContent):
        if (msgContent['res'] >= 0):
            self.funcCtrlSchdLogTrace("L3SCHD: Moto move zero execute successful!")
        else:
            self.funcCtrlSchdLogTrace("L3SCHD: Moto move zero execute failure!")
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;


    '''
    #
    #PIC图像读取过程
    #
    # fnPic - 图像文件的名字
    # fnScale - Scale标识的文件名字
    # fnVideo - 视频文件名字
    # vdCtrl - 视频是否拍摄的控制指示，TRUE-拍，FALSE-不拍
    # sclCtlr - 指示scale标尺图像是否拍摄，TRUE-拍，FALSE-不拍
    # vdDur - 视频长度，秒为单位
    # 
    # 这些控制参考，下同
    #
    '''    
    #拍摄处理
    #STEP1: 启动
    def fsm_msg_capture_normal_pic_rcv_handler(self, msgContent):
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Start to take normal picture!")
        self.fsm_set(self._STM_PIC_CAP_EXEC)
        #先初始化工作序号
        self.picSeqCnt = 1
        #更新批次存储文件
        self.updateBatCntWithIniFileSyned(True, 0, 0)
        self.createBatSectAndIniSyned(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX);
    
        #生成文件名字
        fnPic = self.combineFileNameWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        fnScale = self.combineScaleFileNameWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        fnVideo = self.combineFileNameVideoWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        vdCtrl = GLVIS_PAR_OFC.CAPTURE_ENABLE 
        sclCtrl = GLVIS_PAR_OFC.PIC_SCALE_ENABLE_FLAG
        vdDur = GLVIS_PAR_OFC.CAPTURE_DUR_IN_SEC
        print('fnPic',fnPic)
        print('fnScale',fnScale)
        print('fnVideo',fnVideo)
        print('vdCtrl',vdCtrl)
        print('sclCtrl',sclCtrl)
        
        time.sleep(0.2)
        #移动到合适孔位，然后拍摄 
        mbuf={}
        if (GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET == True):
            mbuf['fnPic'] = fnPic
            mbuf['fnScale'] = fnScale
            mbuf['fnVideo'] = fnVideo
            mbuf['vdCtrl'] = vdCtrl
            mbuf['sclCtrl'] = sclCtrl
            mbuf['vdDur'] = vdDur
            self.msg_send(TUP_MSGID_CTRS_PIC_CAP_REQ, TUP_TASK_ID_VISION, mbuf)
        else:
            mbuf['holeNbr'] = self.func_cvt_index2hole(self.picSeqCnt)
            mbuf['maxTry'] = GLSPS_PAR_OFC.MOTOR_MAX_RETRY_TIMES
            self.msg_send(TUP_MSGID_CTRS_MOTO_MV_HN_REQ, TUP_TASK_ID_MOTO, mbuf)
        
        return TUP_SUCCESS;
    
    #STEP2马达运动
    def fsm_msg_ctrs_moto_mv_hn_resp_rcv_handler(self, msgContent):
        #生成文件名字
     
        fnPic = self.combineFileNameWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        fnScale = self.combineScaleFileNameWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        fnVideo = self.combineFileNameVideoWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        vdCtrl = GLVIS_PAR_OFC.CAPTURE_ENABLE
        sclCtrl = GLVIS_PAR_OFC.PIC_SCALE_ENABLE_FLAG
        vdDur = GLVIS_PAR_OFC.CAPTURE_DUR_IN_SEC
        
        mbuf={}
        mbuf['fnPic'] = fnPic
        mbuf['fnScale'] = fnScale
        mbuf['fnVideo'] = fnVideo
        mbuf['vdCtrl'] = vdCtrl
        mbuf['sclCtrl'] = sclCtrl
        mbuf['vdDur'] = vdDur
        time.sleep(0.2)
        #两个消息共享该控制消息，故而需要分别控制
        
        if (self.fsm_get() == self._STM_PIC_CAP_EXEC):
            self.msg_send(TUP_MSGID_CTRS_PIC_CAP_REQ, TUP_TASK_ID_VISION, mbuf)
        elif (self.fsm_get() == self._STM_FLU_CAP_EXEC):
            self.msg_send(TUP_MSGID_CTRS_FLU_CAP_REQ, TUP_TASK_ID_VISION, mbuf)   
        return TUP_SUCCESS;
    
    #STEP3获得了图像，然后进入下一次运动
    def fsm_msg_ctrs_pic_cap_resp_rcv_handler(self, msgContent):
        #错误处理
        
        res = msgContent['res']
        if res < 0:
            self.funcCtrlSchdLogTrace("L3SCHD: Error feedback get from camera and can not continue!")
            self.fsm_set(self._STM_ACTIVE)            
            return TUP_SUCCESS;
        
        #如果成功，则更新剩余待识别的图片数量
        self.updateBatCntWithIniFileSyned(False, 1, 0)
        #处理上一次成功的图像读取过程
        self.addNormalBatchFile(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        #处理视频文件部分
        if GLVIS_PAR_OFC.CAPTURE_ENABLE == True:
            self.updBatchFileVideo(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        
        #准备处理下一次
        self.picSeqCnt += 1
        if (self.picSeqCnt > GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH):
            self.funcCtrlSchdLogTrace("L3SCHD: Normal picture capture accomplish successful!")
            self.msg_send(TUP_MSGID_CTRL_SCHD_MV_ZERO, TUP_TASK_ID_CTRL_SCHD, "")
            self.fsm_set(self._STM_ACTIVE)
            #是否触发拍照完成后自动识别
            if (GLVIS_PAR_OFC.PIC_CLASSIFIED_AFTER_TAKE_SET == True):
                self.msg_send(TUP_MSGID_CTRL_SCHD_CFYPIC_START, TUP_TASK_ID_CTRL_SCHD, "")
            return TUP_SUCCESS;

        #生成文件名字
        fnPic = self.combineFileNameWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        fnScale = self.combineScaleFileNameWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        fnVideo = self.combineFileNameVideoWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        vdCtrl = GLVIS_PAR_OFC.CAPTURE_ENABLE
        sclCtrl = GLVIS_PAR_OFC.PIC_SCALE_ENABLE_FLAG
        vdDur = GLVIS_PAR_OFC.CAPTURE_DUR_IN_SEC
        
        #继续干活
        mbuf={}
        if (GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET == True):
            mbuf['fnPic'] = fnPic
            mbuf['fnScale'] = fnScale
            mbuf['fnVideo'] = fnVideo
            mbuf['vdCtrl'] = vdCtrl
            mbuf['sclCtrl'] = sclCtrl
            mbuf['vdDur'] = vdDur
            self.msg_send(TUP_MSGID_CTRS_PIC_CAP_REQ, TUP_TASK_ID_VISION, mbuf)
        else:
            mbuf['holeNbr'] = self.func_cvt_index2hole(self.picSeqCnt)
            mbuf['maxTry'] = GLSPS_PAR_OFC.MOTOR_MAX_RETRY_TIMES
            self.msg_send(TUP_MSGID_CTRS_MOTO_MV_HN_REQ, TUP_TASK_ID_MOTO, mbuf)
        return TUP_SUCCESS;


    '''
    #FLU图像读取过程
    #复用马达运动
    '''    
    def fsm_msg_capture_flu_pic_rcv_handler(self, msgContent):
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Start to take flu picture!")
        self.fsm_set(self._STM_FLU_CAP_EXEC)
        #先初始化工作序号
        self.picSeqCnt = 1
        #更新批次存储文件
        self.updateBatCntWithIniFileSyned(True, 0, 0)
        self.createBatSectAndIniSyned(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX);

        #生成文件名字
        fnPic = self.combineFileNameWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        fnScale = self.combineScaleFileNameWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        fnVideo = self.combineFileNameVideoWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        vdCtrl = GLVIS_PAR_OFC.CAPTURE_ENABLE
        sclCtrl = GLVIS_PAR_OFC.PIC_SCALE_ENABLE_FLAG
        vdDur = GLVIS_PAR_OFC.CAPTURE_DUR_IN_SEC
        
        #移动到合适孔位，然后拍摄
        mbuf={}
        if (GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET == True):
            mbuf['fnPic'] = fnPic
            mbuf['fnScale'] = fnScale
            mbuf['fnVideo'] = fnVideo
            mbuf['vdCtrl'] = vdCtrl
            mbuf['sclCtrl'] = sclCtrl
            mbuf['vdDur'] = vdDur
            self.msg_send(TUP_MSGID_CTRS_FLU_CAP_REQ, TUP_TASK_ID_VISION, mbuf)
        else:
            mbuf['holeNbr'] = self.func_cvt_index2hole(self.picSeqCnt)
            mbuf['maxTry'] = GLSPS_PAR_OFC.MOTOR_MAX_RETRY_TIMES
            self.msg_send(TUP_MSGID_CTRS_MOTO_MV_HN_REQ, TUP_TASK_ID_MOTO, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_ctrs_flu_cap_resp_rcv_handler(self, msgContent):
        #错误处理
        res = msgContent['res']
        if res < 0:
            self.funcCtrlSchdLogTrace("L3SCHD: Error feedback get from camera and can not continue!")
            self.fsm_set(self._STM_ACTIVE)            
            return TUP_SUCCESS;

        #如果成功，更新剩余待识别的图片数量
        self.updateBatCntWithIniFileSyned(False, 0, 1)
        #处理上一次成功的图像读取过程
        self.addFluBatchFile(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        
        #准备处理下一次
        self.picSeqCnt += 1
        if (self.picSeqCnt > GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH):
            self.funcCtrlSchdLogTrace("L3SCHD: Flu picture capture accomplish successful!")
            self.msg_send(TUP_MSGID_CTRL_SCHD_MV_ZERO, TUP_TASK_ID_CTRL_SCHD, "")
            self.fsm_set(self._STM_ACTIVE)
            return TUP_SUCCESS;

        #生成文件名字
        fnPic = self.combineFileNameWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        fnScale = self.combineScaleFileNameWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        fnVideo = self.combineFileNameVideoWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.func_cvt_index2hole(self.picSeqCnt))
        vdCtrl = GLVIS_PAR_OFC.CAPTURE_ENABLE
        sclCtrl = GLVIS_PAR_OFC.PIC_SCALE_ENABLE_FLAG
        vdDur = GLVIS_PAR_OFC.CAPTURE_DUR_IN_SEC
        
        #继续干活
        mbuf={}
        if (GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET == True):
            mbuf['fnPic'] = fnPic
            mbuf['fnScale'] = fnScale
            mbuf['fnVideo'] = fnVideo
            mbuf['vdCtrl'] = vdCtrl
            mbuf['sclCtrl'] = sclCtrl
            mbuf['vdDur'] = vdDur
            self.msg_send(TUP_MSGID_CTRS_FLU_CAP_REQ, TUP_TASK_ID_VISION, mbuf)
        else:
            mbuf['holeNbr'] = self.func_cvt_index2hole(self.picSeqCnt)
            mbuf['maxTry'] = GLSPS_PAR_OFC.MOTOR_MAX_RETRY_TIMES
            self.msg_send(TUP_MSGID_CTRS_MOTO_MV_HN_REQ, TUP_TASK_ID_MOTO, mbuf)
        return TUP_SUCCESS;
    
    #走S形路线
    _MOD_CTRL_SCHD_HB96 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,\
                           24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13,\
                           25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,\
                           48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37,\
                           49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,\
                           72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 61,\
                           73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84,\
                           96, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85,\
                           ];
                           
    _MOD_CTRL_SCHD_HB48 = [0, 1, 2, 3, 4, 5, 6, 7, 8,\
                           16, 15, 14, 13, 12, 11, 10, 9,\
                           17, 18, 19, 20, 21, 22, 23, 24,\
                           32, 31, 30, 29, 28, 27, 26, 25,\
                           33, 34, 35, 36, 37, 38, 39, 40,\
                           48, 47, 46, 45, 44, 43, 42, 41,\
                           ];
                           
    _MOD_CTRL_SCHD_HB24 = [0, 1, 2, 3, 4, 5, 6,\
                           12, 11, 10, 9, 8, 7,\
                           13, 14, 15, 16, 17, 18,\
                           24, 23, 22, 21, 20, 19,\
                           ];
    _MOD_CTRL_SCHD_HB12 = [0, 1, 2, 3, 4,\
                           8, 7, 6, 5,\
                           9, 10, 11, 12,\
                           ];
    _MOD_CTRL_SCHD_HB6 = [0, 1, 2, 3,\
                          6, 5, 4,\
                          ];
    def func_cvt_index2hole(self, index):
        if (GLPLT_PAR_OFC.HB_TARGET_TYPE == GLPLT_PAR_OFC.HB_TARGET_96_STANDARD):
            return self._MOD_CTRL_SCHD_HB96[index];
        if (GLPLT_PAR_OFC.HB_TARGET_TYPE == GLPLT_PAR_OFC.HB_TARGET_48_STANDARD):
            return self._MOD_CTRL_SCHD_HB48[index];
        if (GLPLT_PAR_OFC.HB_TARGET_TYPE == GLPLT_PAR_OFC.HB_TARGET_24_STANDARD):
            return self._MOD_CTRL_SCHD_HB24[index];
        if (GLPLT_PAR_OFC.HB_TARGET_TYPE == GLPLT_PAR_OFC.HB_TARGET_12_STANDARD):
            return self._MOD_CTRL_SCHD_HB12[index];
        if (GLPLT_PAR_OFC.HB_TARGET_TYPE == GLPLT_PAR_OFC.HB_TARGET_6_STANDARD):
            return self._MOD_CTRL_SCHD_HB6[index];     
        else:
            return index;


    '''
    #PIC图像停止
    '''    
    def fsm_msg_capture_pic_stop_rcv_handler(self, msgContent):
        self.funcCtrlSchdLogTrace("L3SCHD: Picture capture stop successful!")
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;
    



    
    
    '''
    #PIC图像识别完整过程
    #
    #    fileName - 指示输出文件名，带目录结构
    #    fileNukeName - 指示文件名，带result标签
    #    ctrl - 指示是佛使用fileNukeName。True: fileNukeName, False: fileName
    #    addupSet - 指示输出的文件中是否需要叠加文字
    #    下同
    #
    #
    '''
    #图像识别处理-从界面收到
    def fsm_msg_classify_normal_pic_start_rcv_handler(self, msgContent):
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Start to classify normal picture!")
        self.fsm_set(self._STM_PIC_CFY_EXEC)
        
        #判定是否结束
        if (GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT<=0):
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Normal picture classification accomplished.")
            self.fsm_set(self._STM_ACTIVE)
            return TUP_SUCCESS;
        
        #读取当前需要做图像识别的批次号
        batch, fileNbr = self.findNormalUnclasFileBatchAndNbr();
        mbuf={}
        self.cfyBat = batch;
        self.cfyFileNbr = fileNbr;
        if (batch < 0):
            self.updateBatCntWithIniFileSyned(False, GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT*(-1), 0)
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Normal picture classification not found: remaining NUMBERS=%d." %(GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
        
        #CREATE FILE NAME
        fileName = self.getStoredFileName(batch, fileNbr);
        fileNukeName = self.getStoredFileNukeName(batch, fileNbr)
        if (fileName == None) or (fileNukeName == None):
            self.updateBatCntWithIniFileSyned(False, GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT*(-1), 0)
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Picture classification finished: remaining NUMBERS=%d." %(GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_FAILURE;

        #REAL PROCESSING PROCEDURE
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Normal picture batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
        #发送给VISION任务模块
        mbuf['fileName'] = fileName
        mbuf['fileNukeName'] = fileNukeName
        mbuf['ctrl'] = False
        mbuf['addupSet'] = GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET
        self.msg_send(TUP_MSGID_CTRS_PIC_CLFY_REQ, TUP_TASK_ID_VISION, mbuf)
        return TUP_SUCCESS;
    
    #图像识别后的结果-从VISION得到
    def fsm_msg_classify_pic_accomplish_rcv_handler(self, msgContent):
        res = msgContent['res']
        outText = msgContent['outText']
        print("outText",outText)
        if (res < 0):
            self.funcCtrlSchdErrTrace("L3CTRLSCHD: Normal picture classification failure, remaining NUMBRES=%d." %(GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))

        #不成功则继续搜索下一个文件，而不能直接结束

        #更新成功完成后的文件信息
        self.updateBatCntWithIniFileSyned(False, -1, 0)
        self.updateCfyCntWithIniFileSyned(self.cfyBat, self.cfyFileNbr, GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT, GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT);
        self.updateUnclasFileAsClassified(self.cfyBat, self.cfyFileNbr, outText)
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Normal picture classification finished, remaining NUMBRES=%d." %(GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))

        #选在下一次需要后续处理的新文件号
        batch, fileNbr = self.findNormalUnclasFileBatchAndNbr();
        mbuf={}
        self.cfyBat = batch;
        self.cfyFileNbr = fileNbr;        
        if (batch < 0):
            self.updateBatCntWithIniFileSyned(False, GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT*(-1), 0)
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Normal picture classification not found: remaining NUMBERS=%d." %(GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_SUCCESS;
        
        #CREATE FILE NAME
        fileName = self.getStoredFileName(batch, fileNbr);
        fileNukeName = self.getStoredFileNukeName(batch, fileNbr)
        if (fileName == None) or (fileNukeName == None):
            self.updateBatCntWithIniFileSyned(False, GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT*(-1), 0)
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Normal picture classification finished: remaining NUMBERS=%d." %(GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_SUCCESS;
        
        #ctrl: 控制输出方式，使用fileName还是fileNukeName
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Normal picture batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
        #发送给VISION任务模块
        mbuf['fileName'] = fileName
        mbuf['fileNukeName'] = fileNukeName
        mbuf['ctrl'] = False
        mbuf['addupSet'] = GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET
        self.msg_send(TUP_MSGID_CTRS_PIC_CLFY_REQ, TUP_TASK_ID_VISION, mbuf)
        return TUP_SUCCESS;
    







    '''
    #FLU图像识别完整过程
    '''
    def fsm_msg_classify_flu_pic_start_rcv_handler(self, msgContent):
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Start to classify flu picture!")
        self.fsm_set(self._STM_FLU_CFY_EXEC)

        #判定是否结束
        if (GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT<=0):
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Flu picture classification accomplished.")
            self.fsm_set(self._STM_ACTIVE)
            return TUP_SUCCESS;

        #读取当前需要做图像识别的批次号
        batch, fileNbr = self.findFluUnclasFileBatchAndNbr();
        mbuf={}
        self.cfyBat = batch;
        self.cfyFileNbr = fileNbr;        
        if (batch < 0):
            self.updateBatCntWithIniFileSyned(False, 0, GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT*(-1))
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Flu picture classification not found: remaining NUMBERS=%d." %(GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_FAILURE;
        
        #CREATE FILE NAME
        fileName = self.getStoredFileName(batch, fileNbr);
        fileNukeName = self.getStoredFileNukeName(batch, fileNbr)
        if (fileName == None) or (fileNukeName == None):
            self.updateBatCntWithIniFileSyned(False, 0, GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT*(-1))
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Flu picture classification finished: remaining NUMBERS=%d." %(GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_FAILURE;

        #REAL PROCESSING PROCEDURE
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Flu picture batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
        #发送给VISION任务模块
        mbuf['fileName'] = fileName
        mbuf['fileNukeName'] = fileNukeName
        mbuf['ctrl'] = False
        mbuf['addupSet'] = GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET
        self.msg_send(TUP_MSGID_CTRS_FLU_CLFY_REQ, TUP_TASK_ID_VISION, mbuf)
        return TUP_SUCCESS;
        
    #图像识别后的结果    
    def fsm_msg_classify_flu_accomplish_rcv_handler(self, msgContent):
        res = msgContent['res']
        outText = msgContent['outText']
        if (res < 0):
            self.funcCtrlSchdErrTrace("L3CTRLSCHD: Flu picture classification failure, remaining NUMBRES=%d." %(GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_FAILURE;

        #更新成功完成后的文件信息
        self.updateBatCntWithIniFileSyned(False, 0, -1)
        self.updateCfyCntWithIniFileSyned(self.cfyBat, self.cfyFileNbr, GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT, GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT);
        self.updateUnclasFileAsClassified(self.cfyBat, self.cfyFileNbr, outText)
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Flu picture classification finished, remaining NUMBRES=%d." %(GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))

        #选在下一次需要后续处理的新文件号
        batch, fileNbr = self.findFluUnclasFileBatchAndNbr();
        mbuf={}
        self.cfyBat = batch;
        self.cfyFileNbr = fileNbr;        
        if (batch < 0):
            self.updateBatCntWithIniFileSyned(False, 0, GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT*(-1))
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Flu picture classification not found: remaining NUMBERS=%d." %(GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_SUCCESS;
        
        #CREATE FILE NAME
        fileName = self.getStoredFileName(batch, fileNbr);
        fileNukeName = self.getStoredFileNukeName(batch, fileNbr)
        if (fileName == None) or (fileNukeName == None):
            self.updateBatCntWithIniFileSyned(False, 0, GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT*(-1))
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Flu picture classification finished: remaining NUMBERS=%d." %(GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_SUCCESS;

        #REAL PROCESSING PROCEDURE
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Flu picture batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
        #发送给VISION任务模块
        mbuf['fileName'] = fileName
        mbuf['fileNukeName'] = fileNukeName
        mbuf['ctrl'] = False
        mbuf['addupSet'] = GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET
        self.msg_send(TUP_MSGID_CTRS_FLU_CLFY_REQ, TUP_TASK_ID_VISION, mbuf)
        return TUP_SUCCESS;    


    
    '''
    #停止识别
    '''    
    def fsm_msg_classify_pic_stop_rcv_handler(self, msgContent):
        self.funcCtrlSchdLogTrace("L3SCHD: Picture classification stop successful!")
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;        


    #定时器处理过程
    def func_timer_start_work_after_mv_zero(self):
        self.msg_send(TUP_MSGID_CTRL_SCHD_CAPPIC_START, TUP_TASK_ID_CTRL_SCHD, "")
        #启动下一个TTI定时器，以便继续干活
        self.timerStartWorkDirAfterFixTti = self.tup_timer_start(GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN*60, self.func_timer_start_work_after_fix_tti)
        return

    #TTI定时器到点后，再次自动干活
    def func_timer_start_work_after_fix_tti(self):
        #周期定时器重复启动
        self.timerStartWorkDirAfterFixTti = self.tup_timer_start(GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN*60, self.func_timer_start_work_after_fix_tti)
        #触发任务
        self.msg_send(TUP_MSGID_CTRL_SCHD_CAPPIC_START, TUP_TASK_ID_CTRL_SCHD, "")
        return

    #STEST查询过程
    def fsm_msg_stest_inq_rcv_handler(self, msgContent):
        mbuf={}
        mbuf['picBatch'] = GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX
        mbuf['cfyPicBatch'] = GLCFG_PAR_OFC.PIC_PROC_CLAS_INDEX
        mbuf['cfyFluBatch'] = GLCFG_PAR_OFC.PIC_FLU_CLAS_INDEX
        mbuf['cfyPicRemCnt'] = GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT
        mbuf['cfyFluRemCnt'] = GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT
        mbuf['hbType'] = GLPLT_PAR_OFC.HB_TARGET_TYPE
        self.msg_send(TUP_MSGID_STEST_CTRL_SCHD_FDB, TUP_TASK_ID_UI_STEST, mbuf)
        return TUP_SUCCESS;       




















