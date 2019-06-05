'''
Created on 2019年6月4日

@author: Administrator
'''

from PkgL1vmHandler.ModVmLayer import *
from PkgL3cebsDhal.cebsConfig import *
from PkgL3cebsDhal.ModDhPlate import *
import os
import platform
import time
import urllib3
import json

class clsCebsDhPicfile(clsCebsDhPlate):
    PIC_ORIGIN_PATH = r"pic_origin";
    PIC_MIDDLE_PATH = r"pic_middle";
    #配置参数
    PIC_TAKING_FIX_POINT_SET = False; 
    #增加二次曝光功能试图解决图片模糊的问题
    PIC_SECOND_AUTOEXPO_SET = False
    #After taking picture, whether the pic identification will be run automatically
    #拍照后是否自动识别
    PIC_CLASSIFIED_AFTER_TAKE_SET = False;
    #Whether taking picture will be happened automatically after starting.
    #设备启动后是否自动工作-界面叫定时自动拍照
    PIC_AUTO_WORKING_AFTER_START_SET = False;    
    #模糊度阈值       NF3
    PIC_BLURRY_LIMIT = 5000
    #Auto taking picture TTI times in minutes
    #定时工作时长间隔
    PIC_AUTO_WORKING_TTI_IN_MIN = 60;
    #TEMP USAGE VARIABLES => 用于浮动式界面展示，暂时不用
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
    #图像识别中所用到的部分参数：将根据算法演进
    CFY_THD_GENR_PAR1 = 0
    CFY_THD_GENR_PAR2 = 0
    CFY_THD_GENR_PAR3 = 0
    CFY_THD_GENR_PAR4 = 0
    #FOLLOWING DYNAMIC PARAMETERS SET
    #Global parameter set for PICTURE
    PIC_WORK_DIR = ''
    PIC_ABS_ORIGIN_PATH = "";
    PIC_ABS_MIDDLE_PATH = "";
    #是否需要继续试用？待明确
    PIC_PROC_BATCH_INDEX = 0;
    PIC_PROC_CLAS_INDEX = 0;  #Pointer to the batch of not yet classified.
    PIC_PROC_REMAIN_CNT = 0;  #Pointer to remaining un-classified pictures
    PIC_FLU_CLAS_INDEX = 0    #指向FLU的指针起点
    PIC_FLU_REMAIN_CNT = 0    #剩余的FLU数量
    
    
    '''
    # 工作逻辑设计
    # - 收到数据库的配置文件以后，才开始干活
    # - 多个模块可以独立的对自己的工作环境进行初始化，相互之间不干扰
    # - 将这个初始化放在ModCebsBasic基类中，用于接收初始化消息，简化各个业务模块的处理过程
    #
    '''
    def __init__(self):    
        super(clsCebsDhPicfile, self).__init__()  


    '''
    #
    # 初始化处理过程
    #
    '''    
    #给上层提供服务的函数
    #以该参数为原型strTupGlParPic
    def tup_dhal_picFile_update_context(self, glParPic):
        self.PIC_ORIGIN_PATH = glParPic['PIC_ORIGIN_PATH']
        self.PIC_MIDDLE_PATH = glParPic['PIC_MIDDLE_PATH']
        if (glParPic['PIC_TAKING_FIX_POINT_SET'] == True):
            self.PIC_TAKING_FIX_POINT_SET = True
        else:
            self.PIC_TAKING_FIX_POINT_SET = False
        if (glParPic['PIC_SECOND_AUTOEXPO_SET'] == True):
            self.PIC_SECOND_AUTOEXPO_SET = True
        else:
            self.PIC_SECOND_AUTOEXPO_SET = False
        if (glParPic['PIC_CLASSIFIED_AFTER_TAKE_SET'] == True):
            self.PIC_CLASSIFIED_AFTER_TAKE_SET = True
        else:
            self.PIC_CLASSIFIED_AFTER_TAKE_SET = False
        if (glParPic['PIC_AUTO_WORKING_AFTER_START_SET'] == True):
            self.PIC_AUTO_WORKING_AFTER_START_SET = True
        else:
            self.PIC_AUTO_WORKING_AFTER_START_SET = False
        self.PIC_BLURRY_LIMIT = glParPic['PIC_BLURRY_LIMIT']
        self.PIC_AUTO_WORKING_TTI_IN_MIN = glParPic['PIC_AUTO_WORKING_TTI_IN_MIN']
        self.SMALL_LOW_LIMIT = glParPic['SMALL_LOW_LIMIT']
        self.SMALL_MID_LIMIT = glParPic['SMALL_MID_LIMIT']
        self.MID_BIG_LIMIT = glParPic['MID_BIG_LIMIT']
        self.BIG_UPPER_LIMIT = glParPic['BIG_UPPER_LIMIT']
        if (glParPic['CLAS_RES_ADDUP_SET'] == True):
            self.CLAS_RES_ADDUP_SET = True
        else:
            self.CLAS_RES_ADDUP_SET = False
        if (glParPic['CAPTURE_ENABLE'] == True):
            self.CAPTURE_ENABLE = True
        else:
            self.CAPTURE_ENABLE = False
        self.CAPTURE_DUR_IN_SEC = glParPic['CAPTURE_DUR_IN_SEC']
        if (glParPic['PIC_SCALE_ENABLE_FLAG'] == True):
            self.PIC_SCALE_ENABLE_FLAG = True
        else:
            self.PIC_SCALE_ENABLE_FLAG = False
        self.CFY_THD_GENR_PAR1 = glParPic['CFY_THD_GENR_PAR1']
        self.CFY_THD_GENR_PAR2 = glParPic['CFY_THD_GENR_PAR2']
        self.CFY_THD_GENR_PAR3 = glParPic['CFY_THD_GENR_PAR3']
        self.CFY_THD_GENR_PAR4 = glParPic['CFY_THD_GENR_PAR4']
        
        #处理文件目录部分
        self.PIC_WORK_DIR = os.getcwd()+ self.osDifferentStr()
        #JUDGE WORKING DIR
        self.PIC_ABS_ORIGIN_PATH = self.PIC_WORK_DIR + self.PIC_ORIGIN_PATH
        flag = os.path.exists(self.PIC_ABS_ORIGIN_PATH)
        if (flag == False):
            os.mkdir(self.PIC_ABS_ORIGIN_PATH)
        self.PIC_ABS_ORIGIN_PATH += self.osDifferentStr()
        #JUDGE MID PIC WOKRING DIR
        self.PIC_ABS_MIDDLE_PATH = self.PIC_WORK_DIR + self.PIC_MIDDLE_PATH
        flag = os.path.exists(self.PIC_ABS_MIDDLE_PATH)
        if (flag == False):
            os.mkdir(self.PIC_ABS_MIDDLE_PATH)
        self.PIC_ABS_MIDDLE_PATH += self.osDifferentStr()
        return TUP_SUCCESS

    def osDifferentStr(self):
        sysstr = platform.system()
        if(sysstr =="Windows"):
            return '\\'
        elif(sysstr == "Linux"):
            return '/'
        else:
            return '/'

    '''
    #
    # 文件名字处理过程
    #
    '''   
    def func_dhal_picFile_combinePicName(self, batch, fileNbr):
        return str("batch#" + str(batch) + "FileName#" + str(self.tup_dhal_plate_index_to_hole_lable(fileNbr)))

    def func_dhal_picFile_combineVideoName(self, batch, fileNbr):
        return str("batch#" + str(batch) + "VideoName#" + str(self.tup_dhal_plate_index_to_hole_lable(fileNbr)))

    def func_dhal_picFile_combinePicNameWithDir(self, batch, fileNbr):
        fileName = str("batch#" + str(batch) + "FileName#" + str(self.tup_dhal_plate_index_to_hole_lable(fileNbr)))
        return str(self.PIC_ABS_ORIGIN_PATH) + fileName + '.jpg'

    def func_dhal_picFile_combineVideoNameWithDir(self, batch, fileNbr):
        fileName = str("batch#" + str(batch) + "FileName#" + str(self.tup_dhal_plate_index_to_hole_lable(fileNbr)))
        return str(self.PIC_ABS_ORIGIN_PATH) + fileName + '.mp4'  #.mp4, .avi
























    