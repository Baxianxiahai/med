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
from PkgL1vmHandler.ModVmLayer import *
from PkgL2svrHandler.headHstapi import *
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
class clsCebsDhalOprSvr(TupClsCebsDbaItf, clsCebsDhCamera, clsCebsDhLogfile, clsCebsDhPicfile, clsCebsDhMotosps, clsCebsDhPlate):
    def __init__(self):
        super(clsCebsDhalOprSvr, self).__init__()  
    
    
    
    
    '''
    #
    # Procedure: Set Configuration
    #
    #    - 本过程将由控制模块启动并获取系统参数
    #    - 一旦参数不存在，需要考虑将DEFAULT参数强行写入到数据库中，待完善
    #    - 是否需要增加TUP标签，为后台区分不同的设备，待完善
    #
    '''
    #将收到的hst标准接口TUP_HST_PCT_GET_CONFIG_OUT参量转化为内部消息内容
    #出参：内部消息模板strTupGlParConfig
    def func_dhal_oprSvr_translate_HstConfig_to_glParConfig(self, inputData):
        outputData = strTupGlParConfig
        outputData['PAR_FILE']['PIC_ORIGIN_PATH'] = inputData['cebs_object_profile']['dir_origin']
        outputData['PAR_FILE']['PIC_MIDDLE_PATH'] = inputData['cebs_object_profile']['dir_middle']
        outputData['PAR_PLATE']['HB_TARGET_TYPE'] = inputData['cebs_cali_profile']['platetype']
        outputData['PAR_PLATE']['HB_CALI_POS_IN_UM'][0] = inputData['cebs_cali_profile']['left_bot_x']
        outputData['PAR_PLATE']['HB_CALI_POS_IN_UM'][1] = inputData['cebs_cali_profile']['left_bot_y']
        outputData['PAR_PLATE']['HB_CALI_POS_IN_UM'][2] = inputData['cebs_cali_profile']['right_up_x']
        outputData['PAR_PLATE']['HB_CALI_POS_IN_UM'][3] = inputData['cebs_cali_profile']['right_up_y']
        outputData['PAR_PIC']['PIC_TAKING_FIX_POINT_SET'] = inputData['cebs_config_eleg']['fixpoint']
        outputData['PAR_PIC']['PIC_SECOND_AUTOEXPO_SET'] = inputData['cebs_config_eleg']['autovideo']
        outputData['PAR_PIC']['PIC_CLASSIFIED_AFTER_TAKE_SET'] = inputData['cebs_config_eleg']['autoclfy']
        outputData['PAR_PIC']['PIC_AUTO_WORKING_AFTER_START_SET'] = inputData['cebs_config_eleg']['autowork']
        outputData['PAR_PIC']['PIC_BLURRY_LIMIT'] = inputData['cebs_config_eleg']['blurylimit']
        outputData['PAR_PIC']['PIC_AUTO_WORKING_TTI_IN_MIN'] = inputData['cebs_config_eleg']['autoperiod']
        outputData['PAR_PIC']['SMALL_LOW_LIMIT'] = inputData['cebs_config_eleg']['slimit']
        outputData['PAR_PIC']['SMALL_MID_LIMIT'] = inputData['cebs_config_eleg']['smlimit']
        outputData['PAR_PIC']['MID_BIG_LIMIT'] = inputData['cebs_config_eleg']['mblimit']
        outputData['PAR_PIC']['BIG_UPPER_LIMIT'] = inputData['cebs_config_eleg']['blimit']
        outputData['PAR_PIC']['CLAS_RES_ADDUP_SET'] = inputData['cebs_config_eleg']['addset']
        outputData['PAR_PIC']['VIDEO_CAPTURE_ENABLE'] = inputData['cebs_config_eleg']['autocap']
        outputData['PAR_PIC']['VIDEO_CAPTURE_DUR_IN_SEC'] = inputData['cebs_config_eleg']['videotime']
        outputData['PAR_MOTO']['MOTOR_CUR_SPD'] = inputData['cebs_config_eleg']['movespeed']
        outputData['PAR_MOTO']['MOTOR_CUR_ACC'] = inputData['cebs_config_eleg']['accspeed']
        outputData['PAR_MOTO']['MOTOR_CUR_DEACC'] = inputData['cebs_config_eleg']['decspeed']
        outputData['PAR_MOTO']['MOTOR_CUR_ZERO_SPD'] = inputData['cebs_config_eleg']['zero_spd']
        outputData['PAR_MOTO']['MOTOR_CUR_ZERO_ACC'] = inputData['cebs_config_eleg']['zero_acc']
        outputData['PAR_MOTO']['MOTOR_BACK_STEPS'] = inputData['cebs_config_eleg']['back_step']
        return outputData

    #访问CEBS_DBA数据获取系统配置参数
    #入参：失败成功标签
    #出参： 内部消息模板strTupGlParConfig
    def tup_dhal_oprSvr_GetConfig_and_update(self):
        flag, res = self.tup_hstDba_GetConfig('aaa')
        if (flag > 0):
            outputData = self.func_dhal_oprSvr_translate_HstConfig_to_glParConfig(res)
            self.tup_dhal_oprSvr_UpdateConfigPar(outputData)
            return TUP_SUCCESS, outputData
        else:
            #Step1: 创建DEFAULT参数
            #Step2：将缺省参数存入数据库表单中
            #Step3：更新本地变量
            #Step4：返回缺省数据参数
            return TUP_FAILURE, ''

    #动态参数模板 - strTupGlParConfig做为入参
    #该函数可能会用在第一次初始化，也可能会在后期做参数更新
    def tup_dhal_oprSvr_UpdateConfigPar(self, inputData):
        #FILE部分
        self.tup_dhal_picFile_update_context(inputData['PAR_FILE'], inputData['PAR_PIC'])
        self.tup_dhal_plate_update_context(inputData['PAR_PLATE']['HB_TARGET_TYPE'])
        self.tup_dhal_plate_update_calib(inputData['PAR_PLATE']['HB_CALI_POS_IN_UM'])
        self.tup_dhal_motosps_update_context(inputData['PAR_MOTO'])
        return TUP_SUCCESS
    
    
    
    
    '''
    #
    # Procedure: Set configuration
    #
    #  - 注意：这个过程本来是从HUICOBUS过来的，需要：
    #        1) 先将HUICOBUS消息格式转化为内部消息格式
    #        2) 然后，存入本地
    #        3) 最后，调用本过程并将其存入数据库表单中
    #
    '''    
     #为了存储数据到数据库，将内部参数格式转化为全局hstApi格式，并存入数据库
    def func_dhal_oprSvr_translate_glParConfig_to_SetConfig(self, inputData):
        outputData = TUP_HST_PCT_SET_CONFIG_OUT
        outputData['cebs_object_profile']['dir_origin'] = inputData['PAR_FILE']['PIC_ORIGIN_PATH']
        outputData['cebs_object_profile']['dir_middle'] = inputData['PAR_FILE']['PIC_MIDDLE_PATH']
        outputData['cebs_cali_profile']['platetype'] = inputData['PAR_PLATE']['HB_TARGET_TYPE']
        outputData['cebs_cali_profile']['left_bot_x'] = inputData['PAR_PLATE']['HB_CALI_POS_IN_UM'][0]
        outputData['cebs_cali_profile']['left_bot_y'] = inputData['PAR_PLATE']['HB_CALI_POS_IN_UM'][1]
        outputData['cebs_cali_profile']['right_up_x'] = inputData['PAR_PLATE']['HB_CALI_POS_IN_UM'][2]
        outputData['cebs_cali_profile']['right_up_y'] = inputData['PAR_PLATE']['HB_CALI_POS_IN_UM'][3]
        outputData['cebs_config_eleg']['fixpoint'] = inputData['PAR_PIC']['PIC_TAKING_FIX_POINT_SET']
        outputData['cebs_config_eleg']['autovideo'] = inputData['PAR_PIC']['PIC_SECOND_AUTOEXPO_SET']
        outputData['cebs_config_eleg']['autoclfy'] = inputData['PAR_PIC']['PIC_CLASSIFIED_AFTER_TAKE_SET']
        outputData['cebs_config_eleg']['autowork'] = inputData['PAR_PIC']['PIC_AUTO_WORKING_AFTER_START_SET']
        outputData['cebs_config_eleg']['blurylimit'] = inputData['PAR_PIC']['PIC_BLURRY_LIMIT']
        outputData['cebs_config_eleg']['autoperiod'] = inputData['PAR_PIC']['PIC_AUTO_WORKING_TTI_IN_MIN']
        outputData['cebs_config_eleg']['slimit'] = inputData['PAR_PIC']['SMALL_LOW_LIMIT']
        outputData['cebs_config_eleg']['smlimit'] = inputData['PAR_PIC']['SMALL_MID_LIMIT']
        outputData['cebs_config_eleg']['mblimit'] = inputData['PAR_PIC']['MID_BIG_LIMIT']
        outputData['cebs_config_eleg']['blimit'] = inputData['PAR_PIC']['BIG_UPPER_LIMIT']
        outputData['cebs_config_eleg'] = inputData['addset']['PAR_PIC']['CLAS_RES_ADDUP_SET']
        outputData['cebs_config_eleg']['autocap'] = inputData['PAR_PIC']['VIDEO_CAPTURE_ENABLE']
        outputData['cebs_config_eleg']['videotime'] = inputData['PAR_PIC']['VIDEO_CAPTURE_DUR_IN_SEC']
        outputData['cebs_config_eleg']['movespeed'] = inputData['PAR_MOTO']['MOTOR_CUR_SPD']
        outputData['cebs_config_eleg']['accspeed'] = inputData['PAR_MOTO']['MOTOR_CUR_ACC']
        outputData['cebs_config_eleg']['decspeed'] = inputData['PAR_MOTO']['MOTOR_CUR_DEACC']
        outputData['cebs_config_eleg']['zero_spd'] = inputData['PAR_MOTO']['MOTOR_CUR_ZERO_SPD']
        outputData['cebs_config_eleg']['zero_dec'] = inputData['PAR_MOTO']['MOTOR_CUR_ZERO_ACC']
        outputData['cebs_config_eleg']['back_step'] = inputData['PAR_MOTO']['MOTOR_BACK_STEPS']
        return outputData   
    
    #入参：内部消息模板格式strTupGlParConfig，可能继续更新其它模块
    #出参：成败
    #如果存入数据库失败，则放弃本次参数的更新，确保内存与数据库之间的一致性
    def tup_dhal_oprSvr_SetConfig_and_update(self, inputData):
        outputData = self.func_dhal_oprSvr_translate_glParConfig_to_SetConfig(inputData)
        flag, res = self.tup_hstDba_SetConfig(outputData)
        if (flag > 0):
            self.tup_dhal_oprSvr_UpdateConfigPar(outputData)
            return TUP_SUCCESS
        else:
            return TUP_FAILURE
     
     
     
    '''
    #
    # Procedure: Update Calibration
    #
    #  - 注意：这个过程本来是从HUICOBUS过来的，需要：
    #        1) 先将HUICOBUS消息格式转化为内部消息格式
    #        2) 然后，存入本地
    #        3) 最后，调用本过程并将其存入数据库表单中
    #
    '''        
    #入参：内部消息模板strTupGlParPlate
    #出参：hst标准接口TUP_HST_PCT_UPDATE_CALI_PAR_IN
    def func_dhal_oprSvr_traslate_CalibPar_to_glParPlate(self, inputData):
        outputData = TUP_HST_PCT_UPDATE_CALI_PAR_IN
        outputData['cebs_cali_profile']['platetype'] = inputData['PAR_PLATE']['HB_TARGET_TYPE']
        outputData['cebs_cali_profile']['left_bot_x'] = inputData['PAR_PLATE']['HB_CALI_POS_IN_UM'][0]
        outputData['cebs_cali_profile']['left_bot_y'] = inputData['PAR_PLATE']['HB_CALI_POS_IN_UM'][1]
        outputData['cebs_cali_profile']['right_up_x'] = inputData['PAR_PLATE']['HB_CALI_POS_IN_UM'][2]
        outputData['cebs_cali_profile']['right_up_y'] = inputData['PAR_PLATE']['HB_CALI_POS_IN_UM'][3]
        return outputData
    
    #入参：内部消息模板strTupGlParPlate
    #出参：成败
    def tup_dhal_oprSvr_UpdateCaliPar_and_update(self, inputData):
        outputData = self.func_dhal_oprSvr_traslate_CalibPar_to_glParPlate(inputData)
        flag, res = self.tup_hstDba_SetConfig(outputData)
        if (flag > 0):
            self.tup_dhal_plate_update_context(inputData['HB_TARGET_TYPE'])
            self.tup_dhal_plate_update_calib(inputData['HB_CALI_POS_IN_UM'])
            return TUP_SUCCESS
        else:
            return TUP_FAILURE


    '''
    #
    # Procedure: Add batch number
    #
    # - 注意：如果批次号获取失败，则直接从系统定义的某个特殊批次号开始运行
    #
    '''        
    #入参：无
    #出参：成败
    def tup_dhal_oprSvr_AddBatchNbr_and_update(self):
        inputData = TUP_HST_PCT_ADD_BATCH_NBR_IN
        flag, res = self.tup_hstDba_AddBatchNbr(inputData)
        if (flag > 0):
            batchNbr = res['cebs_batch_info']['snbatch']
            self.tup_dhal_picFile_update_batch_nbr(batchNbr)
            return TUP_SUCCESS
        else:
            self.tup_dhal_picFile_update_batch_nbr(_TUP_CEBS_FAIL_BATCH_START)
            return TUP_FAILURE
    
    
        
    '''
    #
    # Procedure: Fetch un-classification parameters
    #
    # - 注意：
    #
    '''
    #入参：fileAttr - 文件属性，是'normal'白光，还是'flu'荧光
    #出参：成败
    def tup_dhal_oprSvr_hstUnclfyPar_and_update(self, fileAttr):
        inputData = TUP_HST_PCT_READ_UNCLFY_PAR_IN
        inputData['file-attr'] = fileAttr
        flag, res = self.tup_hstDba_ReadUncfyPar(inputData)
        inputData = strTupGlParUnclfyPic
        if (flag > 0):
            inputData['UNCLFY_FILE_ATTR'] = res['file-attr']
            inputData['UNCLFY_BATCH_NBR'] = res['batchNbr']
            inputData['UNCLFY_HOLE_NBR'] = res['holeNbr']
            inputData['UNCLFY_ORIGIN_ABS_FN'] = res['fileAbsOrigin']
            inputData['UNCLFY_MID_ABS_FN'] = res['fileAbsMiddle']
            inputData['UNCLFY_VIDEO_ABS_FN'] = res['fileAbsVideo']
            self.tup_dhal_picFile_update_unclfy_nbr(inputData)
            return TUP_SUCCESS
        else:
            inputData['UNCLFY_FILE_ATTR'] = ''
            inputData['UNCLFY_BATCH_NBR'] = -1
            inputData['UNCLFY_HOLE_NBR'] = 0
            inputData['UNCLFY_ORIGIN_ABS_FN'] = ''
            inputData['UNCLFY_MID_ABS_FN'] = ''
            inputData['UNCLFY_VIDEO_ABS_FN'] = ''
            self.tup_dhal_picFile_update_unclfy_nbr(inputData)
            return TUP_FAILURE
        
    
    

# - 增加普通图像抓取 hstAddPicCap
# - 增加荧光图像抓取 hstAddFluCap
# - 更新普通图像识别 hstUpdatePicCfy
# - 更新荧光图像识别 hstUpdateFluCfy
# - 读取普通图片 hstReadPic
# - 读取荧光图片 hstReadFlu
# - 更新图片统计 hstUpdateStatis
# - 更新用户日志 hstUpdateUserLog

















    