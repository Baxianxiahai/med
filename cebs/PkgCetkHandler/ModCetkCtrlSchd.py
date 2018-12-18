'''
Created on 2018年12月8日

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

    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_CTRL_SCHD, taskName="TASK_CTRL_SCHD", glTabEntry=glPar)
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_CTRL_SCHD, self)
        self.fsm_set(TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)
        
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
        
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        #控制图像工作的序号
        self.picSeqCnt = 0  #图像识别次序号
        
        #搜索到的图像识别批次和文件临时号：这个信息是必须的，不然需要每次都传给下面的模块然后再传回来，太累赘
        self.cfyBat = 0;
        self.cfyFileNbr = 0;
                        
        #TEST测试区域

        return TUP_SUCCESS;

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;

    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MAIN, msgContent)
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
        self.msg_send(TUP_MSGID_CTRS_MOTO_ZERO_REQ, TUP_TASK_ID_MOTO, "")
        return TUP_SUCCESS;

    def fsm_msg_moto_zero_resp_rcv_handler(self, msgContent):
        if (msgContent['res'] >= 0):
            self.funcCtrlSchdLogTrace("L3SCHD: Moto move zero execute successful!")
        else:
            self.funcCtrlSchdLogTrace("L3SCHD: Moto move zero execute failure!")
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;


    '''
    #PIC图像读取过程
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
        self.createBatSectAndIniSyned(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX);
        
        #生成文件名字
        fnPic = self.combineFileNameWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        fnScale = self.combineScaleFileNameWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        fnVideo = self.combineFileNameVideoWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        vdCtrl = ModCebsCom.GLVIS_PAR_OFC.CAPTURE_ENABLE 
        
        #移动到合适孔位，然后拍摄
        mbuf={}
        if (ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET == True):
            mbuf['fnPic'] = fnPic
            mbuf['fnScale'] = fnScale
            mbuf['fnVideo'] = fnVideo
            mbuf['vdCtrl'] = vdCtrl
            self.msg_send(TUP_MSGID_CTRS_PIC_CAP_REQ, TUP_TASK_ID_VISION, mbuf)
        else:
            mbuf['holeNbr'] = self.picSeqCnt
            self.msg_send(TUP_MSGID_CTRS_MOTO_MV_HN_REQ, TUP_TASK_ID_MOTO, mbuf)
        return TUP_SUCCESS;
    
    #STEP2马达运动
    def fsm_msg_ctrs_moto_mv_hn_resp_rcv_handler(self, msgContent):
        #生成文件名字
        fnPic = self.combineFileNameWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        fnScale = self.combineScaleFileNameWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        fnVideo = self.combineFileNameVideoWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        vdCtrl = ModCebsCom.GLVIS_PAR_OFC.CAPTURE_ENABL
        
        mbuf={}
        mbuf['fnPic'] = fnPic
        mbuf['fnScale'] = fnScale
        mbuf['fnVideo'] = fnVideo
        mbuf['vdCtrl'] = vdCtrl
        
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
        self.addNormalBatchFile(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        #处理视频文件部分
        if ModCebsCom.GLVIS_PAR_OFC.CAPTURE_ENABL == True:
            self.updBatchFileVideo(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        
        #准备处理下一次
        self.picSeqCnt += 1
        if (self.picSeqCnt > ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH):
            self.funcCtrlSchdLogTrace("L3SCHD: Normal picture capture accomplish successful!")
            self.fsm_set(self._STM_ACTIVE)            
            return TUP_SUCCESS;

        #生成文件名字
        fnPic = self.combineFileNameWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        fnScale = self.combineScaleFileNameWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        fnVideo = self.combineFileNameVideoWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        vdCtrl = ModCebsCom.GLVIS_PAR_OFC.CAPTURE_ENABL

        #继续干活
        mbuf={}
        if (ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET == True):
            mbuf['fnPic'] = fnPic
            mbuf['fnScale'] = fnScale
            mbuf['fnVideo'] = fnVideo
            mbuf['vdCtrl'] = vdCtrl
            self.msg_send(TUP_MSGID_CTRS_PIC_CAP_REQ, TUP_TASK_ID_VISION, mbuf)
        else:
            mbuf['holeNbr'] = self.picSeqCnt
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
        self.createBatSectAndIniSyned(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX);

        #生成文件名字
        fnPic = self.combineFileNameWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        fnScale = self.combineScaleFileNameWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        fnVideo = self.combineFileNameVideoWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        vdCtrl = ModCebsCom.GLVIS_PAR_OFC.CAPTURE_ENABLE
        
        #移动到合适孔位，然后拍摄
        mbuf={}
        if (ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET == False):
            mbuf['fnPic'] = fnPic
            mbuf['fnScale'] = fnScale
            mbuf['fnVideo'] = fnVideo
            mbuf['vdCtrl'] = vdCtrl
            self.msg_send(TUP_MSGID_CTRS_FLU_CAP_REQ, TUP_TASK_ID_VISION, mbuf)
        else:
            mbuf['holeNbr'] = self.picSeqCnt
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
        self.addFluBatchFile(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        
        #准备处理下一次
        self.picSeqCnt += 1
        if (self.picSeqCnt > ModCebsCom.GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH):
            self.funcCtrlSchdLogTrace("L3SCHD: Flu picture capture accomplish successful!")
            self.fsm_set(self._STM_ACTIVE)
            return TUP_SUCCESS;

        #生成文件名字
        fnPic = self.combineFileNameWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        fnScale = self.combineScaleFileNameWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        fnVideo = self.combineFileNameVideoWithDir(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, self.picSeqCnt)
        vdCtrl = ModCebsCom.GLVIS_PAR_OFC.CAPTURE_ENABL
        
        #继续干活
        mbuf={}
        if (ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET == False):
            mbuf['fnPic'] = fnPic
            mbuf['fnScale'] = fnScale
            mbuf['fnVideo'] = fnVideo
            mbuf['vdCtrl'] = vdCtrl
            self.msg_send(TUP_MSGID_CTRS_FLU_CAP_REQ, TUP_TASK_ID_VISION, mbuf)
        else:
            mbuf['holeNbr'] = self.picSeqCnt
            self.msg_send(TUP_MSGID_CTRS_MOTO_MV_HN_REQ, TUP_TASK_ID_MOTO, mbuf)
        return TUP_SUCCESS;


    '''
    #PIC图像停止
    '''    
    def fsm_msg_capture_pic_stop_rcv_handler(self, msgContent):
        self.funcCtrlSchdLogTrace("L3SCHD: Picture capture stop successful!")
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;
    



    
    
    '''
    #PIC图像识别完整过程
    '''
    #图像识别处理-从界面收到
    def fsm_msg_classify_normal_pic_start_rcv_handler(self, msgContent):
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Start to classify normal picture!")
        self.fsm_set(self._STM_PIC_CFY_EXEC)
        
        #读取当前需要做图像识别的批次号
        batch, fileNbr = self.findNormalUnclasFileBatchAndNbr();
        mbuf={}
        self.cfyBat = batch;
        self.cfyFileNbr = fileNbr;
        if (batch < 0):
            self.updateBatCntWithIniFileSyned(False, ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT*(-1), 0)
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Picture classification not found: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_FAILURE;
        
        #CREATE FILE NAME
        fileName = self.getStoredFileName(batch, fileNbr);
        fileNukeName = self.getStoredFileNukeName(batch, fileNbr)
        if (fileName == None) or (fileNukeName == None):
            self.updateBatCntWithIniFileSyned(False, ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT*(-1), 0)
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Picture classification finished: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_FAILURE;

        #REAL PROCESSING PROCEDURE
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Normal picture batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
        #发送给VISION任务模块
        mbuf['fileName'] = fileName
        mbuf['fileNukeName'] = fileNukeName
        mbuf['ctrl'] = False
        self.msg_send(TUP_MSGID_CTRS_PIC_CLFY_REQ, TUP_TASK_ID_VISION, mbuf)
        return TUP_SUCCESS;
    
    #图像识别后的结果-从VISION得到
    def fsm_msg_classify_pic_accomplish_rcv_handler(self, msgContent):
        res = msgContent['res']
        if (res < 0):
            self.funcCtrlSchdErrTrace("L3CTRLSCHD: Normal picture classification failure, remaining NUMBRES=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_FAILURE;

        #更新成功完成后的文件信息
        self.updateBatCntWithIniFileSyned(False, -1, 0)
        self.updateUnclasFileAsClassified(self.cfyBat, self.cfyFileNbr, ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT, ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT);
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Normal picture classification finished, remaining NUMBRES=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))

        #选在下一次需要后续处理的新文件号
        batch, fileNbr = self.findNormalUnclasFileBatchAndNbr();
        mbuf={}
        self.cfyBat = batch;
        self.cfyFileNbr = fileNbr;        
        if (batch < 0):
            self.updateBatCntWithIniFileSyned(False, ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT*(-1), 0)
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Picture classification not found: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_SUCCESS;
        
        #CREATE FILE NAME
        fileName = self.getStoredFileName(batch, fileNbr);
        fileNukeName = self.getStoredFileNukeName(batch, fileNbr)
        if (fileName == None) or (fileNukeName == None):
            self.updateBatCntWithIniFileSyned(False, ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT*(-1), 0)
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Picture classification finished: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_SUCCESS;
        
        #ctrl: 控制输出方式，使用fileName还是fileNukeName
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Normal picture batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
        #发送给VISION任务模块
        mbuf['fileName'] = fileName
        mbuf['fileNukeName'] = fileNukeName
        mbuf['ctrl'] = False
        self.msg_send(TUP_MSGID_CTRS_PIC_CLFY_REQ, TUP_TASK_ID_VISION, mbuf)
        return TUP_SUCCESS;
    







    '''
    #FLU图像识别完整过程
    '''
    def fsm_msg_classify_flu_pic_start_rcv_handler(self, msgContent):
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Start to classify flu picture!")
        self.fsm_set(self._STM_FLU_CFY_EXEC)

        #读取当前需要做图像识别的批次号
        batch, fileNbr = self.findFluUnclasFileBatchAndNbr();
        mbuf={}
        self.cfyBat = batch;
        self.cfyFileNbr = fileNbr;        
        if (batch < 0):
            self.updateBatCntWithIniFileSyned(False, 0, ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT*(-1))
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Picture classification not found: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_FAILURE;
        
        #CREATE FILE NAME
        fileName = self.getStoredFileName(batch, fileNbr);
        fileNukeName = self.getStoredFileNukeName(batch, fileNbr)
        if (fileName == None) or (fileNukeName == None):
            self.updateBatCntWithIniFileSyned(False, 0, ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT*(-1))
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Picture classification finished: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_FAILURE;

        #REAL PROCESSING PROCEDURE
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Normal picture batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
        #发送给VISION任务模块
        mbuf['fileName'] = fileName
        mbuf['fileNukeName'] = fileNukeName
        mbuf['ctrl'] = False
        self.msg_send(TUP_MSGID_CTRS_FLU_CLFY_REQ, TUP_TASK_ID_VISION, mbuf)
        return TUP_SUCCESS;
        
    #图像识别后的结果    
    def fsm_msg_classify_flu_accomplish_rcv_handler(self, msgContent):
        res = msgContent['res']
        if (res < 0):
            self.funcCtrlSchdErrTrace("L3CTRLSCHD: Normal picture classification failure, remaining NUMBRES=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_FAILURE;

        #更新成功完成后的文件信息
        self.updateBatCntWithIniFileSyned(False, 0, -1)
        self.updateUnclasFileAsClassified(self.cfyBat, self.cfyFileNbr, ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT, ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT);
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Normal picture classification finished, remaining NUMBRES=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))

        #选在下一次需要后续处理的新文件号
        batch, fileNbr = self.findFluUnclasFileBatchAndNbr();
        mbuf={}
        self.cfyBat = batch;
        self.cfyFileNbr = fileNbr;        
        if (batch < 0):
            self.updateBatCntWithIniFileSyned(False, 0, ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT*(-1))
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Picture classification not found: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_SUCCESS;
        
        #CREATE FILE NAME
        fileName = self.getStoredFileName(batch, fileNbr);
        fileNukeName = self.getStoredFileNukeName(batch, fileNbr)
        if (fileName == None) or (fileNukeName == None):
            self.updateBatCntWithIniFileSyned(False, 0, ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT*(-1))
            self.funcCtrlSchdLogTrace("L3CTRLSCHD: Picture classification finished: remaining NUMBERS=%d." %(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_SUCCESS;

        #REAL PROCESSING PROCEDURE
        self.funcCtrlSchdLogTrace("L3CTRLSCHD: Normal picture batch/FileNbr=%d/%d, FileName=%s." %(batch, fileNbr, fileName))
        #发送给VISION任务模块
        mbuf['fileName'] = fileName
        mbuf['fileNukeName'] = fileNukeName
        mbuf['ctrl'] = False
        self.msg_send(TUP_MSGID_CTRS_FLU_CLFY_REQ, TUP_TASK_ID_VISION, mbuf)
        return TUP_SUCCESS;    


    
    '''
    #停止识别
    '''    
    def fsm_msg_classify_pic_stop_rcv_handler(self, msgContent):
        self.funcCtrlSchdLogTrace("L3SCHD: Picture classification stop successful!")
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;        























