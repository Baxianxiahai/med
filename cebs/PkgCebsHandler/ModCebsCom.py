'''
Created on 2018/5/2

@author: Administrator
'''

####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-

import random
import sys
import time
import json
import os
import re
import urllib
import http
import socket


'''

PART1: 全局定义的变量，不需要封装

'''
#STATIC CONFIGURATION AND CAN NOT MODIFY BY HAND
GL_CEBS_ERR_LOG_FILE_NAME_SET = r"cebsErrLog.txt"
GL_CEBS_VISION_CLAS_RESULT_FILE_NAME_SET = r"cebsVsClas.log";
GL_CEBS_CMD_LOG_FILE_NAME_SET = r"cebsCmdLog.txt"
#ROUNDS of auto-pilot run
GL_CEBS_PILOT_WOKING_ROUNDS_MAX = 5;
#SERIAL COM NUMBER => THIS NEED SET IN THE BEGINNING, CAN NOT WAIT UNTIL SYSTEM START!
#SO WHOLE DESIGN LOGIC OF MOTO-API SHOULD RE-DONE!
#NOT YET USE FOLLOWING PORT SETTING.
GL_CEBS_COM_NUMBER_SET = 11;



'''

PART2: 配置文件及控制参数

'''

class clsL0_MedComCfgPar():
    #FOLLOWING DYNAMIC PARAMETERS SET
    #Global parameter set for PICTURE
    PIC_PROC_BATCH_INDEX = 0;
    PIC_PROC_CLAS_INDEX = 0;  #Pointer to the batch of not yet classified.
    PIC_PROC_REMAIN_CNT = 0;  #Pointer to remaining un-classified pictures
    PIC_FLU_CLAS_INDEX = 0    #指向FLU的指针起点
    PIC_FLU_REMAIN_CNT = 0    #剩余的FLU数量
    PIC_ORIGIN_PATH = r"pic_origin";
    PIC_MIDDLE_PATH = r"pic_middle";
    PIC_ABS_ORIGIN_PATH = "";
    PIC_ABS_MIDDLE_PATH = "";
    #FILE ATTRIBUTE
    FILE_ATT_NORMAL = 'normal';
    FILE_ATT_FLUORESCEN = 'flu';  #荧光 Fluorescen
    CFG_FILE_NAME = r"cebsConfig.ini";
    
    #初始化
    def __init__(self):    
        super(clsL0_MedComCfgPar, self).__init__()  
        pass
    
    def funcTest(self):
        pass
    
GLCFG_PAR_OFC = clsL0_MedComCfgPar()




'''

PART2: 板孔相关的参量，需要封装

#COMMON LIB FUNCTIONS, to simplify the whole design.
CURRENTLY STILL IN TEST PHASE, TO BE ENLARGED FURTHER

这个封装类还使用到了一个技巧：外部直接访问，而不用通过public函数访问，这样简化外部操作

'''
class clsL0_MedComPlatePar():
    #MEACHNICAL HARDWARE PLATFORM SCOPE DEFINATION
    HB_MECHNICAL_PLATFORM_X_MAX = 120000;
    HB_MECHNICAL_PLATFORM_Y_MAX = 110000;
    
    #CONTROL AXIS DIRECTION
    HB_TARGET_96_STANDARD = "96_STANDARD";
    HB_TARGET_96_SD_X_MAX = 120000;
    HB_TARGET_96_SD_Y_MAX = 90000;
    HB_TARGET_96_SD_BATCH_MAX = 96;
    HB_TARGET_96_SD_XDIR_NBR = 12;
    HB_TARGET_96_SD_YDIR_NBR = 8;
    HB_TARGET_96_SD_HOLE_DIS = 9000;  #in UM
    HB_TARGET_96_SD_HOLE_RAD = 6500;  #中值直径in UM，(顶+底)/2
     
    HB_TARGET_48_STANDARD = "48_STANDARD";
    HB_TARGET_48_SD_X_MAX = 120000;
    HB_TARGET_48_SD_Y_MAX = 90000;
    HB_TARGET_48_SD_BATCH_MAX = 48;
    HB_TARGET_48_SD_XDIR_NBR = 8;
    HB_TARGET_48_SD_YDIR_NBR = 6;
    HB_TARGET_48_SD_HOLE_DIS = 12000;  #in UM
    HB_TARGET_48_SD_HOLE_RAD = 8500;  #中值直径in UM，(顶+底)/2
     
    HB_TARGET_24_STANDARD = "24_STANDARD";
    HB_TARGET_24_SD_X_MAX = 120000;
    HB_TARGET_24_SD_Y_MAX = 90000;
    HB_TARGET_24_SD_BATCH_MAX = 24;
    HB_TARGET_24_SD_XDIR_NBR = 8;
    HB_TARGET_24_SD_YDIR_NBR = 6;
    HB_TARGET_24_SD_HOLE_DIS = 20000;  #in UM
    HB_TARGET_24_SD_HOLE_RAD = 15000;  #中值直径in UM，(顶+底)/2
     
    HB_TARGET_12_STANDARD = "12_STANDARD";
    HB_TARGET_12_SD_X_MAX = 120000;
    HB_TARGET_12_SD_Y_MAX = 90000;
    HB_TARGET_12_SD_BATCH_MAX = 12;
    HB_TARGET_12_SD_XDIR_NBR = 4;
    HB_TARGET_12_SD_YDIR_NBR = 3;
    HB_TARGET_12_SD_HOLE_DIS = 27000;  #in UM
    HB_TARGET_12_SD_HOLE_RAD = 19000;  #中值直径in UM，(顶+底)/2
     
    HB_TARGET_6_STANDARD = "6_STANDARD";
    HB_TARGET_6_SD_X_MAX = 120000;
    HB_TARGET_6_SD_Y_MAX = 90000;
    HB_TARGET_6_SD_BATCH_MAX = 6;
    HB_TARGET_6_SD_XDIR_NBR = 3;
    HB_TARGET_6_SD_YDIR_NBR = 2;
    HB_TARGET_6_SD_HOLE_DIS = 40000;  #in UM
    HB_TARGET_6_SD_HOLE_RAD = 30000;  #中值直径in UM，(顶+底)/2
    
    #ACTION SELCTION
    HB_TARGET_TYPE = HB_TARGET_96_STANDARD;
    HB_PIC_ONE_WHOLE_BATCH = HB_TARGET_96_SD_BATCH_MAX;
    
    HB_HOLE_X_NUM = 0;          #HOW MANY BOARD HOLES， X DIRECTION
    HB_HOLE_Y_NUM = 0;          #HOW MANY BOARD HOLES，Y DIRECTION
    HB_WIDTH_X_SCALE = 0;       #HOW MANY BOARD HOLES， X DIRECTION
    HB_HEIGHT_Y_SCALE = 0;      #HOW MANY BOARD HOLES，Y DIRECTION
    
    '''
    *左下角的坐标，存在X1/Y1上， 右上角的坐标，存在X2/Y2上 
    *这种方式，符合坐标系的习惯：小值在X1/Y1中，大值在X2/Y2中
    LEFT-BOTTOM for X1/Y1 save in [0/1], RIGHT-UP for X2/Y2 save in [2/3]
    '''
    HB_POS_IN_UM = [0, 0, 0, 0];  #USING INT, um, 96 HOLES, POSITION OF = X1/Y1(LEFT-DOWN), X2/Y2(RIGHT-UP)
    HB_CUR_POS_IN_UM = [0, 0];  #USING INT, um, POSITION X/Y AXIS
    
    #初始化
    def __init__(self):    
        super(clsL0_MedComPlatePar, self).__init__()  
        pass

    def med_cfl_test1(self):
        global GL_CEBS_COM_NUMBER_SET
        print("Test functions! Global parameter Nbr Set = %d" % (GL_CEBS_COM_NUMBER_SET))
        pass

    def med_cfl_add(self, a, b):
        return a+b
    
    #INIT PLATE PRODUCT TYPE, 初始化孔板产品型号
    def med_init_plate_product_type(self):
        if (self.HB_TARGET_TYPE == self.HB_TARGET_96_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_96_SD_BATCH_MAX;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_48_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_48_SD_BATCH_MAX;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_24_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_24_SD_BATCH_MAX;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_12_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_12_SD_BATCH_MAX;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_6_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_6_SD_BATCH_MAX;
        else:
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_96_SD_BATCH_MAX;

    #INIT PLATE PARAMETER, 初始化孔板参数
    def med_init_plate_parameter(self):

        if (self.HB_WIDTH_X_SCALE == 0 or self.HB_HEIGHT_Y_SCALE == 0 or self.HB_HOLE_X_NUM == 0 or self.HB_HOLE_Y_NUM == 0):
            if (self.HB_TARGET_TYPE == self.HB_TARGET_96_STANDARD):
                self.HB_HOLE_X_NUM = self.HB_TARGET_96_SD_XDIR_NBR
                self.HB_HOLE_Y_NUM = self.HB_TARGET_96_SD_YDIR_NBR
                self.HB_WIDTH_X_SCALE = self.HB_TARGET_96_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
                self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_96_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
            elif (self.HB_TARGET_TYPE == self.HB_TARGET_48_STANDARD):
                self.HB_HOLE_X_NUM = self.HB_TARGET_48_SD_XDIR_NBR
                self.HB_HOLE_Y_NUM = self.HB_TARGET_48_SD_YDIR_NBR
                self.HB_WIDTH_X_SCALE = self.HB_TARGET_48_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
                self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_48_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
            elif (self.HB_TARGET_TYPE == self.HB_TARGET_24_STANDARD):
                self.HB_HOLE_X_NUM = self.HB_TARGET_24_SD_XDIR_NBR
                self.HB_HOLE_Y_NUM = self.HB_TARGET_24_SD_YDIR_NBR
                self.HB_WIDTH_X_SCALE = self.HB_TARGET_24_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
                self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_24_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
            elif (self.HB_TARGET_TYPE == self.HB_TARGET_12_STANDARD):
                self.HB_HOLE_X_NUM = self.HB_TARGET_12_SD_XDIR_NBR
                self.HB_HOLE_Y_NUM = self.HB_TARGET_12_SD_YDIR_NBR
                self.HB_WIDTH_X_SCALE = self.HB_TARGET_12_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
                self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_12_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
            elif (self.HB_TARGET_TYPE == self.HB_TARGET_6_STANDARD):
                self.HB_HOLE_X_NUM = self.HB_TARGET_6_SD_XDIR_NBR
                self.HB_HOLE_Y_NUM = self.HB_TARGET_6_SD_YDIR_NBR
                self.HB_WIDTH_X_SCALE = self.HB_TARGET_6_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
                self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_6_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
            else:
                self.HB_HOLE_X_NUM = self.HB_TARGET_96_SD_XDIR_NBR
                self.HB_HOLE_Y_NUM = self.HB_TARGET_96_SD_YDIR_NBR
                self.HB_WIDTH_X_SCALE = self.HB_TARGET_96_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
                self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_96_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
        if (self.HB_POS_IN_UM[0] !=0 or self.HB_POS_IN_UM[1] !=0 or self.HB_POS_IN_UM[2] !=0 or self.HB_POS_IN_UM[3] !=0):
            #小坐标是左下角，大坐标是右上角
            xWidth = self.HB_POS_IN_UM[2] - self.HB_POS_IN_UM[0];
            yHeight = self.HB_POS_IN_UM[3] - self.HB_POS_IN_UM[1];
            self.HB_WIDTH_X_SCALE = xWidth / (self.HB_HOLE_X_NUM-1);
            self.HB_HEIGHT_Y_SCALE = yHeight / (self.HB_HOLE_Y_NUM-1);
        else:
            pass

    #UPDATE PLATE PARAMETERS, 更新孔板参数
    def med_update_plate_parameter(self):
        if (self.HB_TARGET_TYPE == self.HB_TARGET_96_STANDARD):
            self.HB_HOLE_X_NUM = self.HB_TARGET_96_SD_XDIR_NBR;
            self.HB_HOLE_Y_NUM = self.HB_TARGET_96_SD_YDIR_NBR;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_48_STANDARD):
            self.HB_HOLE_X_NUM = self.HB_TARGET_48_SD_XDIR_NBR;
            self.HB_HOLE_Y_NUM = self.HB_TARGET_48_SD_YDIR_NBR;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_24_STANDARD):
            self.HB_HOLE_X_NUM = self.HB_TARGET_24_SD_XDIR_NBR;
            self.HB_HOLE_Y_NUM = self.HB_TARGET_24_SD_YDIR_NBR;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_12_STANDARD):
            self.HB_HOLE_X_NUM = self.HB_TARGET_12_SD_XDIR_NBR;
            self.HB_HOLE_Y_NUM = self.HB_TARGET_12_SD_YDIR_NBR;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_6_STANDARD):
            self.HB_HOLE_X_NUM = self.HB_TARGET_6_SD_XDIR_NBR;
            self.HB_HOLE_Y_NUM = self.HB_TARGET_6_SD_YDIR_NBR;
        else:
            self.HB_HOLE_X_NUM = self.HB_TARGET_96_SD_XDIR_NBR;
            self.HB_HOLE_Y_NUM = self.HB_TARGET_96_SD_YDIR_NBR;
        self.HB_WIDTH_X_SCALE = (self.HB_POS_IN_UM[2] - self.HB_POS_IN_UM[0]) / (self.HB_HOLE_X_NUM-1);
        self.HB_HEIGHT_Y_SCALE = (self.HB_POS_IN_UM[3] - self.HB_POS_IN_UM[1]) / (self.HB_HOLE_Y_NUM-1);
    
    def med_select_plate_board_type(self, option):
        if (option == 96):
            self.HB_TARGET_TYPE = self.HB_TARGET_96_STANDARD;
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_96_SD_BATCH_MAX;
        elif (option == 48):
            self.HB_TARGET_TYPE = self.HB_TARGET_48_STANDARD;
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_48_SD_BATCH_MAX;
        elif (option == 24):
            self.HB_TARGET_TYPE = self.HB_TARGET_24_STANDARD;
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_24_SD_BATCH_MAX;
        elif (option == 12):
            self.HB_TARGET_TYPE = self.HB_TARGET_12_STANDARD;
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_12_SD_BATCH_MAX;
        elif (option == 6):
            self.HB_TARGET_TYPE = self.HB_TARGET_6_STANDARD;
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_6_SD_BATCH_MAX;
        else:
            self.HB_TARGET_TYPE = self.HB_TARGET_96_STANDARD;
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_96_SD_BATCH_MAX;
    
    #获取弧长的参考基准长度，使用us为单位
    #实际是一度条件下的定点连线长度，考虑到误差，1度条件下不再去区分直线与弧线的差异
    def med_get_std_one_degree_radians_len_in_us(self):
        pi = 3.1415926
        if (self.HB_TARGET_TYPE == self.HB_TARGET_96_STANDARD):
            return (self.HB_TARGET_96_SD_HOLE_RAD *pi)/360
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_48_STANDARD):
            return (self.HB_TARGET_48_SD_HOLE_RAD *pi)/360
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_24_STANDARD):
            return (self.HB_TARGET_24_SD_HOLE_RAD *pi)/360
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_12_STANDARD):
            return (self.HB_TARGET_12_SD_HOLE_RAD *pi)/360
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_6_STANDARD):
            return (self.HB_TARGET_6_SD_HOLE_RAD *pi)/360
        else:
            return (self.HB_TARGET_96_SD_HOLE_RAD *pi)/360
    
    #半径
    def med_get_radians_len_in_us(self):
        if (self.HB_TARGET_TYPE == self.HB_TARGET_96_STANDARD):
            return self.HB_TARGET_96_SD_HOLE_RAD/2
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_48_STANDARD):
            return self.HB_TARGET_48_SD_HOLE_RAD/2
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_24_STANDARD):
            return self.HB_TARGET_24_SD_HOLE_RAD/2
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_12_STANDARD):
            return self.HB_TARGET_12_SD_HOLE_RAD/2
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_6_STANDARD):
            return self.HB_TARGET_6_SD_HOLE_RAD/2
        else:
            return self.HB_TARGET_96_SD_HOLE_RAD/2
        
#定义全局变量以及操作函数
GLPLT_PAR_OFC = clsL0_MedComPlatePar()



'''
PART3: 图像相关的参量

#封装
#VISION calibration set
视频图像识别参数的封装，方便对整个参数集合进行操作
方便对参数进行维护，包括增删
'''
class clsL0_MedComPicPar():
    #Fix point to take picture or not? Formally auto-working shall set as False.
    #定点拍照
    PIC_TAKING_FIX_POINT_SET = False; 
    #After taking picture, whether the pic identification will be run automatically
    #拍照后是否自动识别
    PIC_CLASSIFIED_AFTER_TAKE_SET = True;
    #Whether taking picture will be happened automatically after starting.
    #设备启动后是否自动工作
    PIC_AUTO_WORKING_AFTER_START_SET = True;
    #Auto taking picture TTI times in minutes
    #定时工作时长间隔
    PIC_AUTO_WORKING_TTI_IN_MIN = 60;
    #CAMERA NUMBER
    VISION_CAMBER_NBR = -1;
    #896*684 is basic resolution! 896*684 / 1792*1374 / 3584*2748
    VISION_CAMBER_RES_WITDH = 3584; #1792;
    VISION_CAMBER_RES_HEIGHT = 2748; #1374;
    #TEMP USAGE VARIABLES => 用于浮动式界面展示，暂时不用
    #CAMERA_DISPLAY_POS_X = 0;
    #CAMERA_DISPLAY_POS_Y = 0;
    #MAX search window of camera
    VISION_MAX_CAMERA_SEARCH = 15;
    #VISION calibration set
    SMALL_LOW_LIMIT = 200;
    SMALL_MID_LIMIT = 500;
    MID_BIG_LIMIT = 2000;
    BIG_UPPER_LIMIT = 5000;
    #VISION CLASSIFICATION RESULT ADDUP (输出图像叠加标记)
    CLAS_RES_ADDUP_SET = True;
    #VIDEO CAPTURE ENABLE OR NOT (视频录制参数)
    CAPTURE_ENABLE = True;
    CAPTURE_DUR_IN_SEC = 3;
    #SCALE ENABLE SET
    PIC_SCALE_ENABLE_FLAG = False;
    #图像识别中所用到的部分参数：将根据算法演进，待完善
    CFY_THD_PAR1 = 1
    CFY_THD_PAR2 = 2
    CFY_THD_PAR3 = 3
    CFY_THD_PAR4 = 4
    
    
    def __init__(self):    
        super(clsL0_MedComPicPar, self).__init__()  
        pass
    
    def saveLowLimit(self, par):
        self.SMALL_LOW_LIMIT = par

    def saveMidLimit(self, par):
        self.SMALL_MID_LIMIT = par

    def saveBigLimit(self, par):
        self.MID_BIG_LIMIT = par

    def saveUpperLimit(self, par):
        self.BIG_UPPER_LIMIT = par

    def saveAddupSet(self, par):
        self.CLAS_RES_ADDUP_SET = par

    def saveCapEnable(self, par):
        self.CAPTURE_ENABLE = par

    def saveCapDur(self, par):
        self.CAPTURE_DUR_IN_SEC = par
                
#定义全局变量以及操作函数
GLVIS_PAR_OFC = clsL0_MedComPicPar()
GLVIS_PAR_SAV = clsL0_MedComPicPar()


'''
PART3: 串口指令

#封装
方便对参数进行维护，包括增删
'''
class clsL0_MedSpsPar():

    SPS_SHK_HAND = '设备握手（shake_hand）'
    SPS_SET_WK_MODE = '设置工作模式（set_wk_mode）'
    SPS_SET_ACC = '设置加速度（set_acc）'
    SPS_SET_DEACC = '设置减速度（set_deacc）'
    SPS_SET_PPC = '设置一圈步伐（set_pules_per_cycle）'
    SPS_SET_MV_SPD = '设置移动速度（set_mv_spd）'
    SPS_SET_ZO_SPD = '设置归零速度（set_zero_spd）'
    SPS_SET_ZO_ACC = '设置归零加速度（set_zero_acc）'
    SPS_SET_INT_SP = '设置靠边后退步伐（set_int_steps）'
    SPS_MV_PULS = '移动步伐（mv_pules）'
    SPS_MV_SPD = '移动速度（mv_spd）'
    SPS_MV_ZERO = '归零（mv_zero）'
    SPS_STP_IMD = '立即停止（stop_imd）'
    SPS_STP_NOR = '缓慢停止（stop_nor)'
    SPS_INQ_EN = '查询激活状态（inq_enable）'
    SPS_INQ_RUN = '查询运行状态（inq_run）'
    SPS_INQ_STATUS = '查询一般状态（inq_status）'
    SPS_TEST_PULES = '测试脉冲数（test_pules)'
    SPS_SET_EXTI_DELAY_TIME = '设置限位器触发迟滞（set_exti_delay_time)'
    SPS_SHK_HAND_CMID = 0x20
    SPS_SET_WK_MODE_CMID = 0x21
    SPS_SET_ACC_CMID = 0x22
    SPS_SET_DEACC_CMID = 0x23
    SPS_SET_PPC_CMID = 0x24
    SPS_SET_MV_SPD_CMID = 0x25
    SPS_SET_ZO_SPD_CMID = 0x26
    SPS_SET_ZO_ACC_CMID = 0x27
    SPS_SET_INT_SP_CMID = 0x28
    SPS_MV_PULS_CMID = 0x30
    SPS_MV_SPD_CMID = 0x31
    SPS_MV_ZERO_CMID = 0x32
    SPS_STP_IMD_CMID = 0x33
    SPS_STP_NOR_CMID = 0x34
    SPS_INQ_EN_CMID = 0x35
    SPS_INQ_RUN_CMID = 0x36
    SPS_INQ_STATUS_CMID = 0x37
    SPS_TEST_PULES_CMID = 0x38
    SPS_SET_EXTI_DELAY_TIME_CMID = 0x39
    
    SPS_MENGPAR_ADDR  = 0x77
    SPS_MENGPAR_CMD_LEN = 18
    
    MOTOR_STEPS_PER_ROUND = 12800   #NF0
    MOTOR_MAX_SPD = 6  #NF1 rad/s
    MOTOR_MAX_ACC = 3  #NF1 rad/s2
    MOTOR_MAX_DEACC = 3  #NF1 rad/s2
    MOTOR_ZERO_SPD = 6 #NF1 rad/s
    MOTOR_ZERO_ACC = 3 #NF1 rad/s2
    MOTOR_DIS_MM_PER_ROUND = 3.1415926*20*1.05
    MOTOR_STEPS_PER_DISTANCE_MM = MOTOR_STEPS_PER_ROUND / MOTOR_DIS_MM_PER_ROUND
    MOTOR_STEPS_PER_DISTANCE_UM = MOTOR_STEPS_PER_ROUND / MOTOR_DIS_MM_PER_ROUND / 1000    
    
    def __init__(self):    
        super(clsL0_MedSpsPar, self).__init__()  
        pass
    
    def funcTest(self, par):
        pass
                
#定义全局变量以及操作函数
GLSPS_PAR_OFC = clsL0_MedSpsPar()


