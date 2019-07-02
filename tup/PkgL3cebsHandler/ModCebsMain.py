# -*- coding: utf-8 -*-
# @Author: qwang011
# @Date:   2019-04-19 15:34:54
# @Last Modified 2019-05-09
# @Last Modified time: 2019-05-09 11:44:27


import random
import time
import json
from multiprocessing import Queue, Process
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL1vmHandler.ModVmConsole import *
from PkgL3cebsHandler.ModCebsCom import *
from PkgL3cebsHandler.ModCebsCfg import *
from PkgL3cebsHandler import ModRedisOpr
from PkgL2svrUniv import ModCebsDba
from PkgL2svrUniv.ModCebsHuicobus import *


class tupTaskMain(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    _STM_MOTO_MV = 4
    _STM_PILOT = 5

    def __init__(self, glPar):
        tupTaskTemplate.__init__(
            self, taskid=TUP_TASK_ID_BASIC, taskName="TASK_MAIN", glTabEntry=glPar)
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_CALIB, self)
        self.fsm_set(TUP_STM_NULL)
        # STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT,
                             self.fsm_msg_init_rcv_handler)
        # START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        print("set global  paras")
        redisObj = ModRedisOpr.tupRedisOpr()
        redisConn = redisObj.fun_redis_get_connect()
#         print("redisConn",redisConn)
        GLCFG_PAR_OFC.init_sys_config()
        GLPLT_PAR_OFC.init_sys_config()
        GLVIS_PAR_OFC.init_sys_config()
        GLSPS_PAR_OFC.init_sys_config()
        GLFSPC_PAR_OFC.init_sys_config()
        syconfig = {
            "name": "configure",
            "owner": "system",
            "parameter": {
                "groups": [
                    {
                        "groupname": "版型选择",
                        "list": [
                            {"paraname": "托盘类型", "type": "choice", "max": "", "min": "", "value": "0", "items": [
                                "96孔板", "48孔板", "24孔板", "12孔板", "6孔板", "384孔板"], "note":"choice info"}
                        ]
                    }, {
                        "groupname": "全局参数设置",
                        "list": [
                            {"paraname": "拍照后自动识别", "type": "checkbox", "max": "",
                                "min": "", "value": True, "note": "Note info"}
                        ]
                    }]
            }
        }
        tasksch = {
            "groupname": "计划任务设置",
            "list": [
                {"paraname": "启动计划任务", "type": "checkbox", "max": "",
                    "min": "", "value": False, "note": "Note info"},
                {"paraname": "定时自动拍照", "type": "checkbox", "max": "",
                    "min": "", "value": True, "note": "Note info"},
                {"paraname": "定点拍照", "type": "checkbox", "max": "",
                    "min": "", "value": True, "note": "Note info"},
                {"paraname": "定时拍照时间间隔", "type": "int", "max": "100",
                  "min": "0", "value": getattr(GLVIS_PAR_OFC, "PIC_AUTO_WORKING_TTI_IN_MIN"), "note": "单位：秒"}
            ]
        }
        
        pic_pos = {
            "groupname": "图片存储位置",
            "list": [
                {"paraname": "未识别照片目录", "type": "string", "max": "",
                    "min": "", "value": getattr(GLCFG_PAR_OFC, "PIC_ABS_ORIGIN_PATH"), "note": "Note info"},
                {"paraname": "已识别照片目录", "type": "string", "max": "",
                    "min": "", "value": getattr(GLCFG_PAR_OFC, "PIC_ABS_MIDDLE_PATH"), "note": "Note info"},
            ]
        }
        coor_sys_set = {
            "groupname": "坐标系设置",
            "list": [
                {"paraname": "左下X坐标", "type": "int", "max": "37000",
                    "min": "0", "value": getattr(GLPLT_PAR_OFC, "HB_POS_IN_UM[0]"), "note": "单位：UM"},
                {"paraname": "左下Y坐标", "type": "int", "max": "37000",
                    "min": "0", "value": getattr(GLPLT_PAR_OFC, "HB_POS_IN_UM[1]"), "note": "单位：UM"},
                {"paraname": "右上X坐标", "type": "int", "max": "157000",
                    "min": "120000", "value": getattr(GLPLT_PAR_OFC, "HB_POS_IN_UM[2]"), "note": "单位：UM"},
                {"paraname": "右上Y坐标", "type": "int", "max": "127000",
                   "min": "90000", "value": getattr(GLPLT_PAR_OFC, "HB_POS_IN_UM[3]"), "note": "单位：UM"}
            ]
        }
        
        pic_clfy_par_set = {
            "groupname": "图片识别参数设置",
            "list": [
                {"paraname": "小尺寸门限", "type": "int", "max": "",
                "min": "", "value": getattr(GLVIS_PAR_OFC, "SMALL_LOW_LIMIT"), "note": "单位：像素"},
                {"paraname": "小-中尺寸门限", "type": "int", "max": "",
                "min": "", "value": getattr(GLVIS_PAR_OFC, "SMALL_MID_LIMIT"), "note": "单位：像素"},
                {"paraname": "中-大尺寸门限", "type": "int", "max": "",
                "min": "", "value": getattr(GLVIS_PAR_OFC, "MID_BIG_LIMIT"), "note": "单位：像素"},
                {"paraname": "大尺寸门限", "type": "int", "max": "",
                "min": "", "value": getattr(GLVIS_PAR_OFC, "BIG_UPPER_LIMIT"), "note": "单位：像素"},
                {"paraname": "输出图像叠加标定", "type": "checkbox", "max": "",
                "min": "", "value": True, "note": "Note info"}
            ]
        }
        vid_par_set = {
            "groupname": "视频参数设置",
            "list":[
                {"paraname": "开启视频记录", "type": "checkbox", "max": "",
                "min": "", "value": True, "note": "Note info"},
                {"paraname": "视频时长", "type": "int", "max": "60",
                "min": "0", "value": getattr(GLVIS_PAR_OFC, "CAPTURE_DUR_IN_SEC"), "note": "单位：秒"}
            ]
        }
        
        moto_par_set = {
            "groupname": "马达参数",
            "list":[
                {"paraname": "增速加速度", "type": "int", "max": "",
                "min": "", "value":getattr(GLSPS_PAR_OFC, "MOTOR_MAX_SPD"), "note": "单位：metre every second square second"},
                {"paraname": "减速加速度", "type": "int", "max": "",
                "min": "", "value": getattr(GLSPS_PAR_OFC, "MOTOR_MAX_ACC"), "note": "单位：metre every second square second"},
                {"paraname": "移动速度", "type": "int", "max": "",
                "min": "", "value": getattr(GLSPS_PAR_OFC, "MOTOR_MAX_DEACC"), "note": "单位：metre every second square second"},
                {"paraname": "归零速度", "type": "int", "max": "",
                "min": "", "value": getattr(GLSPS_PAR_OFC, "MOTOR_ZERO_SPD"), "note": "单位：metre every second"},
                {"paraname": "归零减速度", "type": "int", "max": "",
                "min": "", "value": getattr(GLSPS_PAR_OFC, "MOTOR_ZERO_ACC"), "note": "单位：metre every second"},
                {"paraname": "回退步数", "type": "int", "max": "",
                "min": "", "value": getattr(GLSPS_PAR_OFC, "MOTOR_BACK_STEP"),"note": "单位：步"},
            ]
        }
        
        print(msgContent)
        
        syconfig["parameter"]["groups"].append(tasksch)
        syconfig["parameter"]["groups"].append(coor_sys_set)
        syconfig["parameter"]["groups"].append(pic_clfy_par_set)
        syconfig["parameter"]["groups"].append(vid_par_set)
        syconfig["parameter"]["groups"].append(pic_pos)
        syconfig["parameter"]["groups"].append(moto_par_set)
        
        redisConn.set("sysconfig",json.dumps(syconfig))
        print("redisConn", redisConn["sysconfig"])
        
#         cls = ModCebsDba.TupClsCebsDbaItf()
#         initDict = cls.cebs_result_init_conf_Read({'cmd': 'read'})
#         print('**************************')
#         print(initDict[1])
#         print('------------------------')
#         print(GLPLT_PAR_OFC)
#         print(getattr(GLPLT_PAR_OFC,"HB_POS_IN_UM[1]"))
        # print(dir(GLPLT_PAR_OFC))
        #{'objid': 1, 'objname': 'objtest0422add', 'objtype': 5, 'uid': 'UID4621503', 'dir_origin': '/www/abcadd', 'dir_middle': '/var/t0add', 'confid': 1, 'fixpoint': True, 'autovideo': True, 'autodist': True, 'addset': True, 'autocap': True, 'autoperiod': 4220, 'videotime': 4220, 'slimit': 220, 'smlimit': 220, 'mblimit': 220, 'blimit': 220, 'accspeed': 40, 'decspeed': 220, 'movespeed': 40, 'zero_spd': 220, 'zero_dec': 40, 'back_step': 220, 'platetype': 1, 'calitime': '2019-05-07 12:06:30.353618', 'caliuid': 'UID4621503', 'left_bot_x': 40, 'left_bot_y': 220, 'right_up_x': 40, 'right_up_y': 220}

        return TUP_SUCCESS
