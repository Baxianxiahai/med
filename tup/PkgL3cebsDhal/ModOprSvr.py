'''
Created on 2019年6月3日

@author: Administrator
'''

import configparser
import os
import platform
import time
import urllib3
import json

#公共数据操作API
from PkgL2svrUniv.ModCebsDba import TupClsCebsDbaItf

#硬件虚拟映射
from PkgL3cebsDhal.cebsConfig import *
from PkgL3cebsDhal.cebsDyndef import *
from PkgL3cebsDhal.ModDhCamera import *
from PkgL3cebsDhal.ModDhLogfile import *
from PkgL3cebsDhal.ModDhPicfile import *
from PkgL3cebsDhal.ModDhMotosps import *
from PkgL3cebsDhal.ModDhPlate import *


#正式服务API，给上层提供标准操作
class clsCebsDhalOprSvr(clsCebsDhCamera, clsCebsDhLogfile, clsCebsDhPicfile, clsCebsDhMotosps, clsCebsDhPlate):
    def __init__(self):
        super(clsCebsDhalOprSvr, self).__init__()  
    
    #访问CEBS_DBA数据
    def tup_dhal_oprSvr_GetConfig(self):
        flag, res = TupClsCebsDbaItf.tup_hstDba_GetConfig('')
        if (flag > 0):
            snd = strTupGlParConfig
            snd['PAR_FILE']['PIC_ORIGIN_PATH'] = res['cebs_object_profile']['dir_origin']
            snd['PAR_FILE']['PIC_MIDDLE_PATH'] = res['cebs_object_profile']['dir_middle']
            snd['PAR_PLATE']['HB_TARGET_TYPE'] = res['cebs_cali_profile']['platetype']
            snd['PAR_PLATE']['HB_CALI_POS_IN_UM'][0] = res['cebs_cali_profile']['left_bot_x']
            snd['PAR_PLATE']['HB_CALI_POS_IN_UM'][1] = res['cebs_cali_profile']['left_bot_y']
            snd['PAR_PLATE']['HB_CALI_POS_IN_UM'][2] = res['cebs_cali_profile']['right_up_x']
            snd['PAR_PLATE']['HB_CALI_POS_IN_UM'][3] = res['cebs_cali_profile']['right_up_y']
            snd['PAR_PIC']['PIC_TAKING_FIX_POINT_SET'] = res['cebs_config_eleg']['fixpoint']
            snd['PAR_PIC']['PIC_SECOND_AUTOEXPO_SET'] = res['cebs_config_eleg']['autovideo']
            snd['PAR_PIC']['PIC_CLASSIFIED_AFTER_TAKE_SET'] = res['cebs_config_eleg']['autoclfy']
            snd['PAR_PIC']['PIC_AUTO_WORKING_AFTER_START_SET'] = res['cebs_config_eleg']['autowork']
            snd['PAR_PIC']['PIC_BLURRY_LIMIT'] = res['cebs_config_eleg']['blurylimit']
            snd['PAR_PIC']['PIC_AUTO_WORKING_TTI_IN_MIN'] = res['cebs_config_eleg']['autoperiod']
            snd['PAR_PIC']['SMALL_LOW_LIMIT'] = res['cebs_config_eleg']['slimit']
            snd['PAR_PIC']['SMALL_MID_LIMIT'] = res['cebs_config_eleg']['smlimit']
            snd['PAR_PIC']['MID_BIG_LIMIT'] = res['cebs_config_eleg']['mblimit']
            snd['PAR_PIC']['BIG_UPPER_LIMIT'] = res['cebs_config_eleg']['blimit']
            snd['PAR_PIC']['CLAS_RES_ADDUP_SET'] = res['cebs_config_eleg']['addset']
            snd['PAR_PIC']['CAPTURE_ENABLE'] = res['cebs_config_eleg']['autocap']
            snd['PAR_PIC']['CAPTURE_DUR_IN_SEC'] = res['cebs_config_eleg']['videotime']
            snd['PAR_MOTO']['MOTOR_CUR_SPD'] = res['cebs_config_eleg']['movespeed']
            snd['PAR_MOTO']['MOTOR_CUR_ACC'] = res['cebs_config_eleg']['accspeed']
            snd['PAR_MOTO']['MOTOR_CUR_DEACC'] = res['cebs_config_eleg']['decspeed']
            snd['PAR_MOTO']['MOTOR_CUR_ZERO_SPD'] = res['cebs_config_eleg']['zero_spd']
            snd['PAR_MOTO']['MOTOR_CUR_ZERO_ACC'] = res['cebs_config_eleg']['zero_dec']
            snd['PAR_MOTO']['MOTOR_BACK_STEPS'] = res['cebs_config_eleg']['back_step']            
            return 1, res
        else:
            return -1, ''
    
    #strTupGlParConfig做为入参
    def tup_dhal_oprSvr_InitConfigPar(self, inputData):
        #FILE部分
        self.tup_dhal_picFile_update_context(inputData['PAR_FILE'], inputData['PAR_PIC'])
        self.tup_dhal_plate_update_context(inputData['PAR_PLATE']['HB_TARGET_TYPE'])
        self.tup_dhal_plate_update_calib(inputData['PAR_PLATE']['HB_CALI_POS_IN_UM'])
        self.tup_dhal_motosps_update_context(inputData['PAR_MOTO'])
        return TUP_SUCCESS






















    