'''
Created on 2018年12月8日

@author: Administrator
'''

import random, json
import time
from multiprocessing import Queue, Process
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL1vmHandler.ModVmConsole import *
from PkgL3cebsHandler.ModCebsCom import *
from PkgL3cebsHandler.ModCebsCfg import *
from PkgL3cebsHandler import ModRedisOpr


class tupTaskCalib(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    _STM_MOTO_MV = 4
    _STM_PILOT = 5
    
    CAM_DISP_SET = True
    timerDisplay = ''
    TIMER_DISP_CYCLE = 0.4
    
    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_CALIB, taskName="TASK_CALIB", glTabEntry=glPar)
        # ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_CALIB, self)
        self.fsm_set(TUP_STM_NULL)
        # STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_com_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_EXIT, self.fsm_com_msg_exit_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_com_msg_test_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)
        
        # 业务处理部分
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_OPEN_REQ, self.fsm_msg_open_req_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_CLOSE_REQ, self.fsm_msg_close_req_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_VDISP_RESP, self.fsm_msg_cam_disp_resp_rcv_handler)

        # 校准移动命令
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_MOMV_DIR_REQ, self.fsm_msg_moto_mv_dir_req_rcv_handler)
        self.add_stm_combine(self._STM_MOTO_MV, TUP_MSGID_CALIB_MOMV_DIR_RESP, self.fsm_msg_moto_mv_dir_resp_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_MOFM_DIR_REQ, self.fsm_msg_moto_force_move_dir_req_rcv_handler)
        self.add_stm_combine(self._STM_MOTO_MV, TUP_MSGID_CALIB_MOFM_DIR_RESP, self.fsm_msg_moto_force_move_dir_resp_rcv_handler)
        
        # 校准设置
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_RIGHT_UP_SET, self.fsm_msg_right_up_set_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_LEFT_DOWN_SET, self.fsm_msg_left_down_set_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_MOMV_START, self.fsm_msg_momv_start_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_MOMV_HOLEN, self.fsm_msg_momv_holen_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_PIC_CAP_HOLEN, self.fsm_msg_pic_cap_holen_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CAL_BLURRY_RET_VALUE, self.fsm_msg_cal_blurry_rcv_handler)
        # 巡游
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_CALIB_PILOT_START, self.fsm_msg_pilot_start_rcv_handler)
        self.add_stm_combine(self._STM_PILOT, TUP_MSGID_CALIB_PILOT_MV_HN_RESP, self.fsm_msg_pilot_mv_hn_resp_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_CALIB_PILOT_STOP, self.fsm_msg_pilot_stop_rcv_handler)

        # STEST
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_STEST_CALIB_INQ, self.fsm_msg_stest_inq_rcv_handler)

        # START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        # STEP1：初始化工作环境
        self.func_clean_working_env()
        
        # STEP2: 干活的定时器
        self.timerDisplay = ''
        
        # STEP3: 巡游的控制单元
        self.pilotCnt = 0
        self.pilotPos = 0
        
#         print("set calib  config")
#         redisObj = ModRedisOpr.tupRedisOpr()
#         redisConn = redisObj.fun_redis_get_connect()
#         calibconfig = {
#             "name":"debug",
#             "owner":"system",
#             "parameter":{
#                 "groups":[
#                     {"groupname":"运动刻度",
#                      "list":[
#                          {"paraname": "10um", "type": "radio", "action": "Move"},
#                          {"paraname":"100um", "type":"radio", "action":"Move"},
#                          {"paraname":"200um", "type":"radio", "action":"Move"},
#                          {"paraname":"500um", "type":"radio", "action":"Move"},
#                          {"paraname":"1mm", "type":"radio", "action":"Move"},
#                          {"paraname":"2mm", "type":"radio", "action":"Move"},
#                          {"paraname": "5mm", "type": "radio", "action": "Move"},
#                          {"paraname":"1cm", "type":"radio", "action":"Move"},
#                          {"paraname":"2cm", "type":"radio", "action":"Move"},
#                          {"paraname":"5cm", "type":"radio", "action":"Move"},
#                          {"paraname":"96孔长边", "type":"radio", "action":"Move"},
#                          {"paraname":"96孔短边", "type":"radio", "action":"Move"},
#                          {"paraname": "48孔长边", "type": "radio", "action": "Move"},
#                          {"paraname":"48孔短边", "type":"radio", "action":"Move"},
#                          {"paraname":"24孔长边", "type":"radio", "action":"Move"},
#                          {"paraname":"24孔短边", "type":"radio", "action":"Move"},
#                          {"paraname":"12孔长边", "type":"radio", "action":"Move"},
#                          {"paraname":"12孔短边", "type":"radio", "action":"Move"},
#                          {"paraname":"6孔长边", "type":"radio", "action":"Move"},
#                          {"paraname":"6孔短边", "type":"radio", "action":"Move"},
#                          ]
#                     }, {"groupname":"运动方向",
#                         "list":[
#                             {"paraname":"up", "type":"button", "action":"up"},
#                             {"paraname":"down", "type":"button", "action":"down"},
#                             {"paraname":"left", "type":"button", "action":"left"},
#                             {"paraname":"right", "type":"button", "action":"right"}
#                             ]
#                     }, {"groupname":"坐标设置",
#                         "list":[
#                             {"paraname":"设置左上", "type":"button", "action":"set left up"},
#                             {"paraname":"设置右下", "type":"button", "action":"set right down"}
#                             ]
#                     }, {"groupname":"运动设置",
#                         "list":[
#                             {"paraname":"移动到起点", "type":"button", "action":""},
#                             {"paraname":"移动到#号孔", "type":"button", "action":""},
#                             {"paraname": "", "type": "int", "max": "", "min": "", "value": 1, "note":"单位： 孔"},
#                             {"paraname":"立即拍照", "type":"button", "action":""},
#                             {"paraname":"校准巡游", "type":"button", "action":""},
#                             {"paraname":"停止巡游", "type":"button", "action":""},
#                             {"paraname":"当前照片模糊值", "type":"int",
#                              "max": "100", "min": "0", "value": getattr(GLVIS_PAR_OFC, 'PIC_BLURRY_LIMIT'), "note": "单位:"}
#                             ]
#                     }
#                 ]}
#             }
#         redisConn.set("calibconfig", json.dumps(calibconfig))
#         jsonInput = {}
#         jsonInput['src'] = "ZH_Medicine_cali_config"
#         jsonInput['hlContent'] = calibconfig
#         print('[hlContent]:', jsonInput['hlContent'])
#         jsonInput['ts'] = msgContent['ts']
#         mqttpublish = self.func_data_send(jsonInput)
#         
        return TUP_SUCCESS;

    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_CALIB, msgContent)
        return TUP_SUCCESS;
        
    # 打开摄像头
    def fsm_msg_open_req_rcv_handler(self, msgContent):
        if (self.CAM_DISP_SET == True):
            self.timerDisplay = self.tup_timer_start(self.TIMER_DISP_CYCLE, self.func_timer_display_process)
        
        '''
        #每进来一次，照片批次号都被更新一次
        #为什么：因为操作摄像头的读取很麻烦，如果不这样做，会导致摄像头存下的照片相互之间重叠，为了简化这个逻辑，每次校准进来都主动+1批次号码
        #
        #固定先更新批次号码+1，简化这个参数的控制
        #而且在一次校准更新中，批次号只能+1，不能重复。如果想要增加更多，需要多次进来
        #另外，每一次进来，固定+1，从而简化这个东西的操控
        '''
        self.updateBatCntWithIniFileSyned(True, 0, 0)
        self.createBatSectAndIniSyned(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX);
        return TUP_SUCCESS;
    
    # 传回来的显示结果
    def fsm_msg_cam_disp_resp_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_CALIB_VDISP_RESP, TUP_TASK_ID_UI_CALIB, msgContent)
        return TUP_SUCCESS;
    
    # 移动动作需要等待MOTO反馈并解锁状态
    def fsm_msg_moto_mv_dir_req_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_MOTO_MV)
        mbuf = {}
        mbuf['scale'] = msgContent['scale']
        mbuf['dir'] = msgContent['dir']
        mbuf['maxTry'] = GLSPS_PAR_OFC.MOTOR_MAX_RETRY_TIMES
        self.msg_send(TUP_MSGID_CALIB_MOMV_DIR_REQ, TUP_TASK_ID_MOTO, mbuf)
        return TUP_SUCCESS;

    def fsm_msg_moto_mv_dir_resp_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        self.msg_send(TUP_MSGID_CALIB_MOMV_DIR_RESP, TUP_TASK_ID_UI_CALIB, msgContent)
        return TUP_SUCCESS;

    def fsm_msg_moto_force_move_dir_req_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_MOTO_MV)
        mbuf = {}
        mbuf['dir'] = msgContent['dir']
        mbuf['maxTry'] = GLSPS_PAR_OFC.MOTOR_MAX_RETRY_TIMES
        self.msg_send(TUP_MSGID_CALIB_MOFM_DIR_REQ, TUP_TASK_ID_MOTO, msgContent)
        return TUP_SUCCESS;

    def fsm_msg_moto_force_move_dir_resp_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        self.msg_send(TUP_MSGID_CALIB_MOFM_DIR_RESP, TUP_TASK_ID_UI_CALIB, msgContent)
        return TUP_SUCCESS;

    # 关闭摄像头与马达
    def fsm_msg_close_req_rcv_handler(self, msgContent):
        # 摄像头采集
        self.func_clean_working_env()
        # 停止马达
        self.msg_send(TUP_MSGID_CTRS_MOTO_STOP, TUP_TASK_ID_MOTO, '')
        return TUP_SUCCESS;
        
    # STEST查询校准工作状态
    def fsm_msg_stest_inq_rcv_handler(self, msgContent):
        mbuf = {}
        # LC:right/up always be 0
        if (GLPLT_PAR_OFC.HB_POS_IN_UM[0] != 0) and (GLPLT_PAR_OFC.HB_POS_IN_UM[1] != 0) and (GLPLT_PAR_OFC.HB_POS_IN_UM[2] == 0) and (GLPLT_PAR_OFC.HB_POS_IN_UM[3] == 0):
            mbuf['calibStatus'] = 1
        else:
            mbuf['calibStatus'] = -1
        self.msg_send(TUP_MSGID_STEST_CALIB_FDB, TUP_TASK_ID_UI_STEST, mbuf)
        return TUP_SUCCESS; 
        
    def funcCalibLogTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_CALIB, myString)
        # SAVE INTO MED FILE
        self.medCmdLog(str(myString))
        # PRINT to local
        self.tup_dbg_print(str(myString))
        return
        
    # 抑制本地打印，实在是太多了
    def funcCalibErrTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_CALIB, myString)
        # SAVE INTO MED FILE
        self.medErrorLog(str(myString));
        # PRINT to local
        self.tup_err_print(str(myString))
        return
    
    # 打开定时器干活
    def func_timer_display_process(self):
        self.msg_send(TUP_MSGID_CALIB_VDISP_REQ, TUP_TASK_ID_VISION, '')
        self.timerDisplay = self.tup_timer_start(self.TIMER_DISP_CYCLE, self.func_timer_display_process)
        
    # 业务函数    
    def func_clean_working_env(self):
        # 停止摄像头显示
        if (self.timerDisplay != ''):
            self.tup_timer_stop(self.timerDisplay)
        # 停止马达
        self.fsm_set(self._STM_ACTIVE)

    # 设置参数
    def fsm_msg_right_up_set_rcv_handler(self, msgContent):
        GLPLT_PAR_OFC.HB_POS_IN_UM[2] = GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0];
        GLPLT_PAR_OFC.HB_POS_IN_UM[3] = GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1];
        GLPLT_PAR_OFC.med_update_plate_parameter()
        self.updateStaticSectionEnvPar();
        self.funcCalibLogTrace(str("L3CALIB: RightUp Axis set!  XY=%d/%d." % (GLPLT_PAR_OFC.HB_POS_IN_UM[2], GLPLT_PAR_OFC.HB_POS_IN_UM[3])))      
        return TUP_SUCCESS;

    # 设置参数
    def fsm_msg_left_down_set_rcv_handler(self, msgContent):
        GLPLT_PAR_OFC.HB_POS_IN_UM[0] = GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[0];
        GLPLT_PAR_OFC.HB_POS_IN_UM[1] = GLPLT_PAR_OFC.HB_CUR_POS_IN_UM[1];
        GLPLT_PAR_OFC.med_update_plate_parameter()
        self.updateStaticSectionEnvPar();
        self.funcCalibLogTrace("L3CALIB: LeftDown Axis set! XY=%d/%d." % (GLPLT_PAR_OFC.HB_POS_IN_UM[0], GLPLT_PAR_OFC.HB_POS_IN_UM[1]))
        return TUP_SUCCESS;

    # 移动命令
    def fsm_msg_momv_start_rcv_handler(self, msgContent):
        self.funcCalibLogTrace("L3CALIB: Move to Hole#0 point.")
        mbuf = {}
        mbuf['maxTry'] = GLSPS_PAR_OFC.MOTOR_MAX_RETRY_TIMES   
        self.msg_send(TUP_MSGID_CALIB_MOMV_START, TUP_TASK_ID_MOTO, mbuf)
        return TUP_SUCCESS;

    # 移动命令
    def fsm_msg_momv_holen_rcv_handler(self, msgContent):
        holeIndex = int(msgContent['holeNbr'])
        newHoldNbr = self.funcCheckHoldNumber(holeIndex)
        mbuf = {}
        mbuf['holeNbr'] = newHoldNbr
        mbuf['maxTry'] = GLSPS_PAR_OFC.MOTOR_MAX_RETRY_TIMES
        self.funcCalibLogTrace(str("L3CALIB: Move to Hole#%d point." % (int(msgContent['holeNbr']))))
        self.msg_send(TUP_MSGID_CALIB_MOMV_HOLEN, TUP_TASK_ID_MOTO, mbuf)
        return TUP_SUCCESS;

    def funcCheckHoldNumber(self, holeNbr):
        if (holeNbr <= 0):
            return 1;
        if (holeNbr >= GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH):
            return GLPLT_PAR_OFC.HB_PIC_ONE_WHOLE_BATCH
        return holeNbr

    # 截图命令
    def fsm_msg_pic_cap_holen_rcv_handler(self, msgContent):
        holeIndex = int(msgContent['holeNbr'])
        newHoldNbr = self.funcCheckHoldNumber(holeIndex)
        # 生成文件
        fileName = self.combineFileNameWithDir(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, newHoldNbr)
        self.addNormalBatchFile(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, newHoldNbr)
        mbuf = {}
        mbuf['holeNbr'] = newHoldNbr
        mbuf['fileName'] = fileName
        self.funcCalibLogTrace(str("L3CALIB: Capture picture with Hole#%d point." % (int(msgContent['holeNbr']))))
        self.msg_send(TUP_MSGID_CALIB_PIC_CAP_HOLEN, TUP_TASK_ID_VISION, mbuf)
        
        '''
        #更新文件记录
        #这里稍微冒一些风险：就是拍照和记录没有成功，但这里已经记录了
        #在实际使用的时候，这种风向比较小。重启程序，这部分记录UnClassifiedCounter会重新计算的
        #如果客户非常在意这种风险，需要给这个消息增加一个反馈消息，指示是否成功。如果不成功则不更新ini文件记录，那样就完美了
        #过程不困难，但比较累赘。这里考虑的是简要的过程。
        '''
        self.updateBatCntWithIniFileSyned(False, 1, 0)
        self.addNormalBatchFile(GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX, newHoldNbr)
        
        return TUP_SUCCESS;
    
    def fsm_msg_cal_blurry_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_CAL_BLURRY_RET_VALUE, TUP_TASK_ID_UI_CALIB, msgContent)
        return TUP_SUCCESS;
    
    # 巡游开始
    def fsm_msg_pilot_start_rcv_handler(self, msgContent):
        self.pilotCnt = 0
        self.pilotPos = 0
        self.funcCalibLogTrace(str("L3CALIB: Pilot round #0 movement start!"))
        mbuf = {}
        mbuf['holeNbr'] = int(1)
        mbuf['maxTry'] = GLSPS_PAR_OFC.MOTOR_MAX_RETRY_TIMES
        self.msg_send(TUP_MSGID_CALIB_PILOT_MV_HN_REQ, TUP_TASK_ID_MOTO, mbuf);
        self.fsm_set(self._STM_PILOT)
        return TUP_SUCCESS;
    
    # 巡游持续
    def fsm_msg_pilot_mv_hn_resp_rcv_handler(self, msgContent):
        mbuf = {}
        self.pilotPos += 1
        if (self.pilotPos >= 4):
            self.pilotPos = 0
            self.pilotCnt += 1
            # 打印内容，不期望跟结束之间产生冲突矛盾
            if (self.pilotCnt < GLSPS_PAR_OFC.PILOT_WOKING_ROUNDS_MAX):
                self.funcCalibLogTrace(str("L3CALIB: Pilot round #%d movement start!" % (self.pilotCnt)))
        # 结束的时刻
        if (self.pilotCnt >= GLSPS_PAR_OFC.PILOT_WOKING_ROUNDS_MAX):
            self.msg_send(TUP_MSGID_CALIB_PILOT_STOP, TUP_TASK_ID_MOTO, "");
            self.funcCalibLogTrace(str("L3CALIB: Pilot movement accomplished successful!"))
            self.fsm_set(self._STM_ACTIVE)
            return TUP_SUCCESS;
        # 正常继续
        if (self.pilotPos == 0):
            mbuf['holeNbr'] = int(1)
        elif (self.pilotPos == 1):
            mbuf['holeNbr'] = int(GLPLT_PAR_OFC.HB_HOLE_X_NUM)
        elif (self.pilotPos == 2):
            mbuf['holeNbr'] = int(GLPLT_PAR_OFC.HB_TARGET_96_SD_BATCH_MAX)
        elif (self.pilotPos == 3):
            mbuf['holeNbr'] = int(GLPLT_PAR_OFC.HB_TARGET_96_SD_BATCH_MAX - GLPLT_PAR_OFC.HB_HOLE_X_NUM + 1)
        mbuf['maxTry'] = GLSPS_PAR_OFC.MOTOR_MAX_RETRY_TIMES
        self.msg_send(TUP_MSGID_CALIB_PILOT_MV_HN_REQ, TUP_TASK_ID_MOTO, mbuf);
        return TUP_SUCCESS;    
    
    # 巡游停止
    def fsm_msg_pilot_stop_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_CALIB_PILOT_STOP, TUP_TASK_ID_MOTO, "");
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;
        
