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
import sys

class clsCebsDhPicfile(clsCebsDhPlate):
    dhalPicfileOriginPath = r"pic_origin";
    dhalPicfileMiddlePath = r"pic_middle";
    #配置参数
    dhalPicfileTakingFixPointSet = False; 
    #增加二次曝光功能试图解决图片模糊的问题
    dhalPicfileSecondAutoExpoSet = False
    #After taking picture, whether the pic identification will be run automatically
    #拍照后是否自动识别
    dhalPicfileClassifiedAfterTakeSet = False;
    #Whether taking picture will be happened automatically after starting.
    #设备启动后是否自动工作-界面叫定时自动拍照
    dhalPicfileAutoWorkingAfterStartSet = False;    
    #模糊度阈值       NF3
    dhalPicfileBlurryLimit = 5000
    #Auto taking picture TTI times in minutes
    #定时工作时长间隔
    dhalPicfileAutoWorkingTtiInMin = 60;
    #TEMP USAGE VARIABLES => 用于浮动式界面展示，暂时不用
    #VISION calibration set
    dhalPicfileSmallLowLimit = 200;
    dhalPicfileSmallMidLimit = 500;
    dhalPicfileMidBigLimit = 2000;
    dhalPicfileBigUpperLimit = 5000;
    #VISION CLASSIFICATION RESULT ADDUP (输出图像叠加标记)
    dhalPicfileClasResAddupSet = True;
    #VIDEO CAPTURE ENABLE OR NOT (视频录制参数)
    dhalPicfileVideoCapEnable = True;
    dhalPicfileVideoDurInSec = 3;
    #SCALE ENABLE SET
    dhalPicfileScaleEnableSet = False;
    #图像识别中所用到的部分参数：将根据算法演进
    dhalPicfileCfyThdGenrPar1 = 0
    dhalPicfileCfyThdGenrPar2 = 0
    dhalPicfileCfyThdGenrPar3 = 0
    dhalPicfileCfyThdGenrPar4 = 0
    #FOLLOWING DYNAMIC PARAMETERS SET
    #Global parameter set for PICTURE
    dhalPicfileWorkDir = ''
    dhalPicfileAbsOriginPath = "";
    dhalPicfileAbsMiddlePath = "";
    
    #控制拍摄的参数
    dhalPicfileCapBatchIndex = 0;
    dhalPicfileCapHoleIndex = 0;
    
    #控制识别的参数
    dhalPicfileFileAttr = 'normal'
    dhalPicfileClfyBatchNbr = 0;
    dhalPicfileClfyHoleNbr = 0;
    dhalPicfileClfyOriginAbsFn = '';
    dhalPicfileClfyMidAbsFn = '';
    dhalPicfileClfyVideoAbsFn = '';
    
    
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
    def tup_dhal_picFile_update_context(self, glParFile, glParPic):
        self.dhalPicfileOriginPath = glParFile['PIC_ORIGIN_PATH']
        self.dhalPicfileMiddlePath = glParFile['PIC_MIDDLE_PATH']
        if (glParPic['PIC_TAKING_FIX_POINT_SET'] == True):
            self.dhalPicfileTakingFixPointSet = True
        else:
            self.dhalPicfileTakingFixPointSet = False
        if (glParPic['PIC_SECOND_AUTOEXPO_SET'] == True):
            self.dhalPicfileSecondAutoExpoSet = True
        else:
            self.dhalPicfileSecondAutoExpoSet = False
        if (glParPic['PIC_CLASSIFIED_AFTER_TAKE_SET'] == True):
            self.dhalPicfileClassifiedAfterTakeSet = True
        else:
            self.dhalPicfileClassifiedAfterTakeSet = False
        if (glParPic['PIC_AUTO_WORKING_AFTER_START_SET'] == True):
            self.dhalPicfileAutoWorkingAfterStartSet = True
        else:
            self.dhalPicfileAutoWorkingAfterStartSet = False
        self.dhalPicfileBlurryLimit = glParPic['PIC_BLURRY_LIMIT']
        self.dhalPicfileAutoWorkingTtiInMin = glParPic['PIC_AUTO_WORKING_TTI_IN_MIN']
        self.dhalPicfileSmallLowLimit = glParPic['SMALL_LOW_LIMIT']
        self.dhalPicfileSmallMidLimit = glParPic['SMALL_MID_LIMIT']
        self.dhalPicfileMidBigLimit = glParPic['MID_BIG_LIMIT']
        self.dhalPicfileBigUpperLimit = glParPic['BIG_UPPER_LIMIT']
        if (glParPic['CLAS_RES_ADDUP_SET'] == True):
            self.dhalPicfileClasResAddupSet = True
        else:
            self.dhalPicfileClasResAddupSet = False
        if (glParPic['VIDEO_CAPTURE_ENABLE'] == True):
            self.dhalPicfileVideoCapEnable = True
        else:
            self.dhalPicfileVideoCapEnable = False
        self.dhalPicfileVideoDurInSec = glParPic['VIDEO_CAPTURE_DUR_IN_SEC']
        self.dhalPicfileCfyThdGenrPar1 = glParPic['CFY_THD_GENR_PAR1']
        self.dhalPicfileCfyThdGenrPar2 = glParPic['CFY_THD_GENR_PAR2']
        self.dhalPicfileCfyThdGenrPar3 = glParPic['CFY_THD_GENR_PAR3']
        self.dhalPicfileCfyThdGenrPar4 = glParPic['CFY_THD_GENR_PAR4']
        
        #ORIGIN图片目录处理过程
        self.dhalPicfileWorkDir = os.getcwd()+ self.osDifferentStr()
        if sys.platform.startswith("linux"):
            self.dhalPicfileAbsOriginPath = _TUP_CEBS_UBUNTU_FILE_STORAGE_DIR_PREFIX + self.dhalPicfileOriginPath
        if sys.platform.startswith("win32"):
            self.dhalPicfileAbsOriginPath = self.dhalPicfileWorkDir + self.dhalPicfileOriginPath
        flag = os.path.exists(self.dhalPicfileAbsOriginPath)
        if (flag == False):
            os.mkdir(self.dhalPicfileAbsOriginPath)
        self.dhalPicfileAbsOriginPath += self.osDifferentStr()

        #MIDDLE图片目录处理过程
        if sys.platform.startswith("linux"):
            self.dhalPicfileAbsMiddlePath = _TUP_CEBS_UBUNTU_FILE_STORAGE_DIR_PREFIX + self.dhalPicfileMiddlePath
        if sys.platform.startswith("win32"):
            self.dhalPicfileAbsMiddlePath = self.dhalPicfileWorkDir + self.dhalPicfileMiddlePath
        flag = os.path.exists(self.dhalPicfileAbsMiddlePath)
        if (flag == False):
            os.mkdir(self.dhalPicfileAbsMiddlePath)
        self.dhalPicfileAbsMiddlePath += self.osDifferentStr()
        
        #RETURN
        return TUP_SUCCESS
    
    def osDifferentStr(self):
        sysstr = platform.system()
        if(sysstr =="Windows"):
            return '\\'
        elif(sysstr == "Linux"):
            return '/'
        else:
            return '/'

    #更新批次号
    def tup_dhal_picFile_update_batch_nbr(self, batchNbr):
        self.dhalPicfileCapBatchIndex = batchNbr
    
    #获取当前批次号+孔位号
    def tup_dhal_picFile_get_batch_and_hole_nbr(self):
        return self.dhalPicfileCapBatchIndex, self.dhalPicfileCapHoleIndex
    
    #判定是否还可以继续移动到下一个孔位
    #孔位是从1-N计数的
    def tup_dhal_picFile_move_to_next_hole(self):
        if (self.dhalPicfileCapHoleIndex < self.dhalPlatePicOneWholeBatch):
            self.dhalPicfileCapHoleIndex = self.dhalPicfileCapHoleIndex+1
            return TUP_SUCCESS, self.dhalPicfileCapHoleIndex
        else:
            return TUP_FAILURE, 0
    
    #更新批次号
    #入参：strTupGlParUnclfyPic
    def tup_dhal_picFile_update_unclfy_nbr(self, inputData):
        self.dhalPicfileFileAttr = inputData['UNCLFY_FILE_ATTR']
        self.dhalPicfileClfyBatchNbr = inputData['UNCLFY_BATCH_NBR']
        self.dhalPicfileClfyHoleNbr = inputData['UNCLFY_HOLE_NBR']
        self.dhalPicfileClfyOriginAbsFn = inputData['UNCLFY_ORIGIN_ABS_FN']
        self.dhalPicfileClfyMidAbsFn = inputData['UNCLFY_MID_ABS_FN']
        self.dhalPicfileClfyVideoAbsFn = inputData['UNCLFY_VIDEO_ABS_FN']


    '''
    #
    # 文件名字处理过程
    #
    '''   
    def func_dhal_picFile_combinePicName(self, batch, fileNbr):
        return str("batch#" + str(batch) + "hole#" + str(self.tup_dhal_plate_index_to_hole_lable(fileNbr))) + "_org"

    def func_dhal_picFile_combineVideoName(self, batch, fileNbr):
        return str("batch#" + str(batch) + "hole#" + str(self.tup_dhal_plate_index_to_hole_lable(fileNbr))) + "_video"

    def func_dhal_picFile_combineMidName(self, batch, fileNbr):
        return str("batch#" + str(batch) + "hole#" + str(self.tup_dhal_plate_index_to_hole_lable(fileNbr))) + "_cfy"

    def func_dhal_picFile_combinePicNameWithDir(self, batch, fileNbr):
        fileName = self.func_dhal_picFile_combinePicName(batch, fileNbr)
        return str(self.dhalPicfileAbsOriginPath) + fileName + '.jpg'

    def func_dhal_picFile_combineVideoNameWithDir(self, batch, fileNbr):
        fileName = self.func_dhal_picFile_combineMidName(batch, fileNbr)
        return str(self.dhalPicfileAbsOriginPath) + fileName + '.mp4'  #.mp4, .avi

    def func_dhal_picFile_combineMidNameWithDir(self, batch, fileNbr):
        fileName = self.func_dhal_picFile_combineMidName(batch, fileNbr)
        return str(self.dhalPicfileAbsMiddlePath) + fileName + '.jpg'
    
    #向上提供的服务
    def tup_dhal_picFile_GenFn_with_AbsDir(self):
        picFn =  self.func_dhal_picFile_combinePicNameWithDir(self.dhalPicfileCapBatchIndex, self.dhalPicfileCapHoleIndex)
        midFn =  self.func_dhal_picFile_combineOutputPicFnWithDir(self.dhalPicfileCapBatchIndex, self.dhalPicfileCapHoleIndex)
        videoFn =  self.func_dhal_picFile_combineVideoNameWithDir(self.dhalPicfileCapBatchIndex, self.dhalPicfileCapHoleIndex)
        return picFn, midFn, videoFn





















    