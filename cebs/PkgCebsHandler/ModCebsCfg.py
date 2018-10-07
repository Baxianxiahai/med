'''
Created on 2018/5/4

@author: Administrator
'''

####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-


import configparser
import os
import platform
import time
from PkgCebsHandler import ModCebsCom


'''
配置模块
'''
class clsL1_ConfigOpr(object):
    def __init__(self):
        self.filePath = ModCebsCom.GL_CEBS_CFG_FILE_NAME
        self.initGlobalPar()

    #INIT ALL STORAGE AREA
    def initGlobalPar(self):
        #JUDGE WORKING DIR
        ModCebsCom.GL_CEBS_PIC_ABS_ORIGIN_PATH = os.getcwd()+ self.osDifferentStr() + ModCebsCom.GL_CEBS_PIC_ORIGIN_PATH
        flag = os.path.exists(ModCebsCom.GL_CEBS_PIC_ABS_ORIGIN_PATH)
        if (flag == False):
            os.mkdir(ModCebsCom.GL_CEBS_PIC_ABS_ORIGIN_PATH)
        ModCebsCom.GL_CEBS_PIC_ABS_ORIGIN_PATH += self.osDifferentStr()
        #JUDGE MID PIC WOKRING DIR
        ModCebsCom.GL_CEBS_PIC_ABS_MIDDLE_PATH = os.getcwd()+ self.osDifferentStr() + ModCebsCom.GL_CEBS_PIC_MIDDLE_PATH
        flag = os.path.exists(ModCebsCom.GL_CEBS_PIC_ABS_MIDDLE_PATH)
        if (flag == False):
            os.mkdir(ModCebsCom.GL_CEBS_PIC_ABS_MIDDLE_PATH)
        ModCebsCom.GL_CEBS_PIC_ABS_MIDDLE_PATH += self.osDifferentStr()
        #JUDGE CREATE INIT FILE OR NOT
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        flag = os.path.exists(self.filePath)
        if (flag == False):
            self.CReader.add_section("Env")
            self.CReader.set("Env","workdir", str(os.getcwd()+ self.osDifferentStr()))
            self.CReader.set("Env","pic_origin", str(ModCebsCom.GL_CEBS_PIC_ABS_ORIGIN_PATH))
            self.CReader.set("Env","pic_middle", str(ModCebsCom.GL_CEBS_PIC_ABS_MIDDLE_PATH))
            self.CReader.set("Env","holeboard_type", str(ModCebsCom.GL_CEBS_HB_TARGET_TYPE))
            self.CReader.set("Env","holeboard, left_bot X-axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[0]))
            self.CReader.set("Env","holeboard, left_bot Y-axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[1]))
            self.CReader.set("Env","holeboard, right_up X-Axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[2]))
            self.CReader.set("Env","holeboard, right_up Y-Axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[3]))
            self.CReader.set("Env","pic taking fix point set", str(ModCebsCom.GL_CEBS_PIC_TAKING_FIX_POINT_SET))
            self.CReader.set("Env","pic classification set", str(ModCebsCom.GL_CEBS_PIC_CLASSIFIED_AFTER_TAKE_SET))
            self.CReader.set("Env","pic auto-work after start set", str(ModCebsCom.GL_CEBS_PIC_AUTO_WORKING_AFTER_START_SET))
            self.CReader.set("Env","pic auto-work tti", str(ModCebsCom.GL_CEBS_PIC_AUTO_WORKING_TTI_IN_MIN))
            self.CReader.set("Env","vision camera nbr", str(ModCebsCom.GL_CEBS_VISION_CAMBER_NBR))
            self.CReader.set("Env","vision small-low limit", str(ModCebsCom.GL_CEBS_VISION_SMALL_LOW_LIMIT))
            self.CReader.set("Env","vision small-mid limit", str(ModCebsCom.GL_CEBS_VISION_SMALL_MID_LIMIT))
            self.CReader.set("Env","vision mid-big limit", str(ModCebsCom.GL_CEBS_VISION_MID_BIG_LIMIT))
            self.CReader.set("Env","vision big-upper limit", str(ModCebsCom.GL_CEBS_VISION_BIG_UPPER_LIMIT))
            self.CReader.set("Env","vision res addup set", str(ModCebsCom.GL_CEBS_VISION_CLAS_RES_ADDUP_SET))
            self.CReader.set("Env","video capture enable set", str(ModCebsCom.GL_CEBS_VIDEO_CAPTURE_ENABLE))
            self.CReader.set("Env","video capture dur in sec", str(ModCebsCom.GL_CEBS_VIDEO_CAPTURE_DUR_IN_SEC))
            self.CReader.add_section("Counter")
            self.CReader.set("Counter","PicBatchCnt", "0")
            self.CReader.set("Counter","PicBatchClas", "0")
            self.CReader.set("Counter","PicRemainCnt", "0")
            self.CReader.set("Counter","PicBatFluClas", "0")
            self.CReader.set("Counter","PicRemFluCnt", "0")
            self.CReader.write(open(self.filePath, "w"))
        #REWRITE FILE TO AVOID INI FILE ERROR
        if (self.CReader['Env']['workdir'] != str(os.getcwd()+ self.osDifferentStr())):
            self.updateSectionPar()


    '''
    * STEP1:
    *    控制参数读取及更新过程
    *
    '''   
    #初始化读取全局图像
    def readGlobalPar(self):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX = int(self.CReader['Counter']['PicBatchCnt']);
        ModCebsCom.GL_CEBS_PIC_PROC_CLAS_INDEX = int(self.CReader['Counter']['PicBatchClas']);
        ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT = int(self.CReader['Counter']['PicRemainCnt']);
        ModCebsCom.GL_CEBS_PIC_FLU_CLAS_INDEX = int(self.CReader['Counter']['PicBatFluClas']);
        ModCebsCom.GL_CEBS_PIC_FLU_REMAIN_CNT = int(self.CReader['Counter']['PicRemFluCnt']);
        ModCebsCom.GL_CEBS_HB_TARGET_TYPE = self.CReader['Env']['holeboard_type'];
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] = int(self.CReader['Env']['holeboard, left_bot X-axis']);
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] = int(self.CReader['Env']['holeboard, left_bot Y-axis']);
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] = int(self.CReader['Env']['holeboard, right_up X-axis']);
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] = int(self.CReader['Env']['holeboard, right_up Y-axis']);
        tmp = self.CReader['Env']['pic taking fix point set']
        if (tmp == 'True'):
            ModCebsCom.GL_CEBS_PIC_TAKING_FIX_POINT_SET = True
        else:
            ModCebsCom.GL_CEBS_PIC_TAKING_FIX_POINT_SET = False
        tmp = self.CReader['Env']['pic classification set']
        if (tmp == 'True'):
            ModCebsCom.GL_CEBS_PIC_CLASSIFIED_AFTER_TAKE_SET = True
        else:
            ModCebsCom.GL_CEBS_PIC_CLASSIFIED_AFTER_TAKE_SET = False
        tmp = self.CReader['Env']['pic auto-work after start set']
        if (tmp == 'True'):
            ModCebsCom.GL_CEBS_PIC_AUTO_WORKING_AFTER_START_SET = True
        else:
            ModCebsCom.GL_CEBS_PIC_AUTO_WORKING_AFTER_START_SET = False
        ModCebsCom.GL_CEBS_PIC_AUTO_WORKING_TTI_IN_MIN = int(self.CReader['Env']['pic auto-work tti']);
        ModCebsCom.GL_CEBS_VISION_CAMBER_NBR = int(self.CReader['Env']['vision camera nbr']);
        ModCebsCom.GL_CEBS_VISION_SMALL_LOW_LIMIT = int(self.CReader['Env']['vision small-low limit']);
        ModCebsCom.GL_CEBS_VISION_SMALL_MID_LIMIT = int(self.CReader['Env']['vision small-mid limit']);
        ModCebsCom.GL_CEBS_VISION_MID_BIG_LIMIT = int(self.CReader['Env']['vision mid-big limit']);
        ModCebsCom.GL_CEBS_VISION_BIG_UPPER_LIMIT = int(self.CReader['Env']['vision big-upper limit']);
        tmp = self.CReader['Env']['vision res addup set']
        if (tmp == 'True'):
            ModCebsCom.GL_CEBS_VISION_CLAS_RES_ADDUP_SET = True
        else:
            ModCebsCom.GL_CEBS_VISION_CLAS_RES_ADDUP_SET = False
        tmp = self.CReader['Env']['video capture enable set']
        if (tmp == 'True'):
            ModCebsCom.GL_CEBS_VIDEO_CAPTURE_ENABLE = True
        else:
            ModCebsCom.GL_CEBS_VIDEO_CAPTURE_ENABLE = False
        ModCebsCom.GL_CEBS_VIDEO_CAPTURE_DUR_IN_SEC = int(self.CReader['Env']['video capture dur in sec']);
        #In case of store error, re-caculate remaining unclas-pictures
        #为了防止统计错误，重新根据
        res = self.recheckRemaingUnclasBatchFile(ModCebsCom.GL_CEBS_FILE_ATT_NORMAL)
        if (res != ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT):
            print("CFG: Error find during re-check remaining un-clas normal pictures and recovered! Stored=%d, actual=%d." % (ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT, res))
            ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT = res
            self.updateSectionPar()
        #为了防止统计错误，重新扫描并计算荧光图像数量
        res = self.recheckRemaingUnclasBatchFile(ModCebsCom.GL_CEBS_FILE_ATT_FLUORESCEN)
        if (res != ModCebsCom.GL_CEBS_PIC_FLU_REMAIN_CNT):
            print("CFG: Error find during re-check remaining un-clas Fluorescen pictures and recovered! Stored=%d, actual=%d." % (ModCebsCom.GL_CEBS_PIC_FLU_REMAIN_CNT, res))
            ModCebsCom.GL_CEBS_PIC_FLU_REMAIN_CNT = res
            self.updateSectionPar()
            
    def getSection(self):
        return self.CReader.sections()

    def getdic(self, section):
        s={}
        for k,v in self.CReader.items(section):
            s[k]=v
        return s

    def osDifferentStr(self):
        sysstr = platform.system()
        if(sysstr =="Windows"):
            return '\\'
        elif(sysstr == "Linux"):
            return '/'
        else:
            return '/'

    def updateSectionPar(self):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')        
        if (self.CReader.has_section("Env") == False):
            self.CReader.add_section("Env")
            self.CReader.set("Env","workdir", str(os.getcwd()+ self.osDifferentStr()))
            self.CReader.set("Env","pic_origin", str(ModCebsCom.GL_CEBS_PIC_ABS_ORIGIN_PATH))
            self.CReader.set("Env","pic_middle", str(ModCebsCom.GL_CEBS_PIC_ABS_MIDDLE_PATH))
            self.CReader.set("Env","holeboard_type", str(ModCebsCom.GL_CEBS_HB_TARGET_TYPE))
            self.CReader.set("Env","holeboard, left_bot X-axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[0]))
            self.CReader.set("Env","holeboard, left_bot Y-axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[1]))
            self.CReader.set("Env","holeboard, right_up X-Axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[2]))
            self.CReader.set("Env","holeboard, right_up Y-Axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[3]))
            self.CReader.set("Env","pic taking fix point set", str(ModCebsCom.GL_CEBS_PIC_TAKING_FIX_POINT_SET))
            self.CReader.set("Env","pic classification set", str(ModCebsCom.GL_CEBS_PIC_CLASSIFIED_AFTER_TAKE_SET))
            self.CReader.set("Env","pic auto-work after start set", str(ModCebsCom.GL_CEBS_PIC_AUTO_WORKING_AFTER_START_SET))
            self.CReader.set("Env","pic auto-work tti", str(ModCebsCom.GL_CEBS_PIC_AUTO_WORKING_TTI_IN_MIN))
            self.CReader.set("Env","vision camera nbr", str(ModCebsCom.GL_CEBS_VISION_CAMBER_NBR))
            self.CReader.set("Env","vision small-low limit", str(ModCebsCom.GL_CEBS_VISION_SMALL_LOW_LIMIT))
            self.CReader.set("Env","vision small-mid limit", str(ModCebsCom.GL_CEBS_VISION_SMALL_MID_LIMIT))
            self.CReader.set("Env","vision mid-big limit", str(ModCebsCom.GL_CEBS_VISION_MID_BIG_LIMIT))
            self.CReader.set("Env","vision big-upper limit", str(ModCebsCom.GL_CEBS_VISION_BIG_UPPER_LIMIT))
            self.CReader.set("Env","vision res addup set", str(ModCebsCom.GL_CEBS_VISION_CLAS_RES_ADDUP_SET))
            self.CReader.set("Env","video capture enable set", str(ModCebsCom.GL_CEBS_VIDEO_CAPTURE_ENABLE))
            self.CReader.set("Env","video capture dur in sec", str(ModCebsCom.GL_CEBS_VIDEO_CAPTURE_DUR_IN_SEC))
        else:
            self.CReader.remove_section("Env")
            self.CReader.add_section("Env")        
            self.CReader.set("Env","workdir", str(os.getcwd()+ self.osDifferentStr()))
            self.CReader.set("Env","pic_origin", str(ModCebsCom.GL_CEBS_PIC_ABS_ORIGIN_PATH))
            self.CReader.set("Env","pic_middle", str(ModCebsCom.GL_CEBS_PIC_ABS_MIDDLE_PATH))
            self.CReader.set("Env","holeboard_type", str(ModCebsCom.GL_CEBS_HB_TARGET_TYPE))
            self.CReader.set("Env","holeboard, left_bot X-axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[0]))
            self.CReader.set("Env","holeboard, left_bot Y-axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[1]))
            self.CReader.set("Env","holeboard, right_up X-Axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[2]))
            self.CReader.set("Env","holeboard, right_up Y-Axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[3]))
            self.CReader.set("Env","pic taking fix point set", str(ModCebsCom.GL_CEBS_PIC_TAKING_FIX_POINT_SET))
            self.CReader.set("Env","pic classification set", str(ModCebsCom.GL_CEBS_PIC_CLASSIFIED_AFTER_TAKE_SET))
            self.CReader.set("Env","pic auto-work after start set", str(ModCebsCom.GL_CEBS_PIC_AUTO_WORKING_AFTER_START_SET))
            self.CReader.set("Env","pic auto-work tti", str(ModCebsCom.GL_CEBS_PIC_AUTO_WORKING_TTI_IN_MIN))
            self.CReader.set("Env","vision camera nbr", str(ModCebsCom.GL_CEBS_VISION_CAMBER_NBR))
            self.CReader.set("Env","vision small-low limit", str(ModCebsCom.GL_CEBS_VISION_SMALL_LOW_LIMIT))
            self.CReader.set("Env","vision small-mid limit", str(ModCebsCom.GL_CEBS_VISION_SMALL_MID_LIMIT))
            self.CReader.set("Env","vision mid-big limit", str(ModCebsCom.GL_CEBS_VISION_MID_BIG_LIMIT))
            self.CReader.set("Env","vision big-upper limit", str(ModCebsCom.GL_CEBS_VISION_BIG_UPPER_LIMIT))
            self.CReader.set("Env","vision res addup set", str(ModCebsCom.GL_CEBS_VISION_CLAS_RES_ADDUP_SET))
            self.CReader.set("Env","video capture enable set", str(ModCebsCom.GL_CEBS_VIDEO_CAPTURE_ENABLE))
            self.CReader.set("Env","video capture dur in sec", str(ModCebsCom.GL_CEBS_VIDEO_CAPTURE_DUR_IN_SEC))
        #回写                    
        fd = open(self.filePath, 'w')
        self.CReader.write(fd)
        fd.close()
                
    #FILLING GLOBAL CONTROL DATA
    def updateCtrlCntInfo(self):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        if (self.CReader.has_section("Counter") == False):
            self.CReader.add_section("Counter")
            self.CReader.set("Counter","PicBatchCnt", str(ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX))
            #普通图像
            self.CReader.set("Counter","PicBatchClas", str(ModCebsCom.GL_CEBS_PIC_PROC_CLAS_INDEX))
            self.CReader.set("Counter","PicRemainCnt", str(ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT))
            #荧光图像控制参数
            self.CReader.set("Counter","PicBatFluClas", str(ModCebsCom.GL_CEBS_PIC_FLU_CLAS_INDEX))
            self.CReader.set("Counter","PicRemFluCnt", str(ModCebsCom.GL_CEBS_PIC_FLU_REMAIN_CNT))
            
        else:
            self.CReader.remove_section("Counter")
            self.CReader.add_section("Counter")
            self.CReader.set("Counter","PicBatchCnt", str(ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX))
            #普通图像
            self.CReader.set("Counter","PicBatchClas", str(ModCebsCom.GL_CEBS_PIC_PROC_CLAS_INDEX))
            self.CReader.set("Counter","PicRemainCnt", str(ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT))
            #荧光图像控制参数
            self.CReader.set("Counter","PicBatFluClas", str(ModCebsCom.GL_CEBS_PIC_FLU_CLAS_INDEX))
            self.CReader.set("Counter","PicRemFluCnt", str(ModCebsCom.GL_CEBS_PIC_FLU_REMAIN_CNT))
        fd = open(self.filePath, 'w')
        self.CReader.write(fd)
        fd.close()


    '''
    * STEP2:
    *    单个文件处理过程
    *
    '''   
    #新增加一个批次时，需要创建批次表头
    def createBatch(self, batch):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        batchStr = "batch#" + str(batch)
        if (self.CReader.has_section(batchStr) == True):
            self.CReader.remove_section(batchStr)
            self.CReader.add_section(batchStr)
        else:
            self.CReader.add_section(batchStr)
        self.CReader.set(batchStr, "batch number", str(batch))
        self.CReader.set(batchStr, "work time", str(time.asctime()))
        fd = open(self.filePath, 'w')
        self.CReader.write(fd)
        fd.close()

    #增加普通文件
    def addNormalBatchFile(self, batch, fileNbr):
        return self.addBatchFileInElement(batch, fileNbr, ModCebsCom.GL_CEBS_FILE_ATT_NORMAL)
    
    #增加荧光文件
    def addFluBatchFile(self, batch, fileNbr):
        return self.addBatchFileInElement(batch, fileNbr, ModCebsCom.GL_CEBS_FILE_ATT_FLUORESCEN)
    
    def addBatchFileInElement(self, batch, fileNbr, eleTag):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        batchStr = "batch#" + str(batch)
        fileName = self.combineFileName(batch, fileNbr)
        fileClas = str("batchFileClas#" + str(fileNbr))
        fileAtt = str("batchFileAtt#" + str(fileNbr))
        self.CReader.set(batchStr, fileName, self.combineFileNameWithDir(batch, fileNbr))
        self.CReader.set(batchStr, fileClas, 'no')
        self.CReader.set(batchStr, fileAtt, eleTag)
        try:
            fd = open(self.filePath, 'w')
        except Exception as err:  
            print("CFG: Open file failure, err = " + str(err))
            return -1;
        finally:
            self.CReader.write(fd)
            fd.close()

    '''
    * STEP3:
    *    文件名字处理过程
    *
    '''   
    #READ CONTROL FILE
    def getStoredFileName(self, batch, fileNbr):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        batchStr = "batch#" + str(batch)
        fileName = self.combineFileName(batch, fileNbr)
        res = self.CReader[batchStr][fileName];
        return res;

    #Without file path
    def getStoredFileNukeName(self, batch, fileNbr):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        fileName = self.combineFileName(batch, fileNbr)
        res = fileName + '.jpg'
        return res;

    def combineFileName(self, batch, fileNbr):
        return str("batch#" + str(batch) + "FileName#" + str(fileNbr))

    def combineFileNameWithDir(self, batch, fileNbr):
        fileName = str("batch#" + str(batch) + "FileName#" + str(fileNbr))
        return str(ModCebsCom.GL_CEBS_PIC_ABS_ORIGIN_PATH) + fileName + '.jpg'
    
    def combineFileNameVideoWithDir(self, batch, fileNbr):
        fileName = str("batch#" + str(batch) + "FileName#" + str(fileNbr))
        return str(ModCebsCom.GL_CEBS_PIC_ABS_ORIGIN_PATH) + fileName + '.mp4'  #.mp4, .avi


    '''
    * STEP4:
    *    搜索某种特性的批次和文件名字
    *
    #SEARCH GLOBAL WETHER UN-FINISHED PICTURE EXIST
    #TARGET to find the very first picture
    * 目标是找到第一个满足条件的函数
    * 为了方便复制该函数，将这个函数中原先使用的子函数集合进来，简化函数的编写，不然显得过于累赘
    * 将该函数改造为通用函数，简化设计
    * 这是本模块内部函数，从而将字符串等信息影藏在本模块内部，简化其它模块的设计，以及未来的维护
    *
    * 输入条件：eleTag = {'normal'，'flu'}
    * 输出：    BatchIndex, fileNbrIndex
    '''
    def findUnclasFileBatchAndFileNbr(self, eleTag):
        start = ModCebsCom.GL_CEBS_PIC_PROC_CLAS_INDEX;
        end = ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX;
        #Refresh CReader to be lastest one
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        #Under searching start==end, it is stop. So we extend the range a little bit bigger.
        fileNbr = -1
        for index in range(start, end+1):
            #Find the very first picture which fulfill the condition, but not the whole number of unclassified pictures.
            batchStr = "batch#" + str(index)
            if (self.CReader.has_section(batchStr) == False):
                return -1, -1;
            #SEARCH ALL CONFIGURATION KEY and 'DEFAULT' key
            flag = False
            for key in self.CReader[batchStr]:
                #Find the very first element
                if (('batchfileclas#' in key) and (self.CReader[batchStr][key] == 'no')):
                    temps = key[len('batchfileclas#'):]
                    tempi = int(temps)
                    if (self.CReader[batchStr][str("batchfileatt#" + str(tempi))] == eleTag):
                        fileNbr = tempi;
                        flag = True;
                        break;
            #YES and FOUND!
            if (flag == True):
                break;
        #Find the result!
        if (fileNbr >= 0):
            ModCebsCom.GL_CEBS_PIC_PROC_CLAS_INDEX = index;
            self.updateCtrlCntInfo()
            return index, fileNbr;
        else:
            return -2, -2;

    #可以被其它模块调用的函数
    def findNormalUnclasFileBatchAndNbr(self):
        return self.findUnclasFileBatchAndFileNbr(ModCebsCom.GL_CEBS_FILE_ATT_NORMAL)

    #可以被其它模块调用的函数
    def findFluUnclasFileBatchAndNbr(self):
        return self.findUnclasFileBatchAndFileNbr(ModCebsCom.GL_CEBS_FILE_ATT_FLUORESCEN)


    '''
    * STEP5:
    *    寻找某种特性的总文件数量，目的是复核，防止各种原因造成的错误
    *
    *
    #FETCH UN-CLASSIFIED FILE FOR ONE BATCH, WITH TOTAL NUMBER
    #寻找所有未识别图像数量
    *
    #FETCH ALL REMAINING UNCLAS BATCH FILES TOTAL NUMBER
    #寻找所有还未识别图像的总数
    *
    * 输入条件：eleTag = {'normal'，'flu'}
    * 输出：totalUnclassBatchFiles，总未识别的文件数量
    '''
    def recheckRemaingUnclasBatchFile(self, eleTag):
        start = ModCebsCom.GL_CEBS_PIC_PROC_CLAS_INDEX;
        end = ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX;
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        res = 0;
        for index in range(start, end+1):
            batchStr = "batch#" + str(index)
            #如果发现不合法就结束
            if (self.CReader.has_section(batchStr) == False):
                break
            #SEARCH ALL CONFIGURATION KEY and 'DEFAULT' key
            totalNbr = 0
            for key in self.CReader[batchStr]:
                if (('batchfileclas#' in key) and (self.CReader[batchStr][key] == 'no')):
                    temps = key[len('batchfileclas#'):]
                    tempi = int(temps)
                    if (self.CReader[batchStr][str("batchfileatt#" + str(tempi))] == eleTag):
                        totalNbr +=1
            if (totalNbr > 0):
                res += totalNbr
        return res
                
    #UPDATE CATEGORY PICTURE INFORMATION
    def updateUnclasFileAsClassified(self, batch, fileNbr):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        batchStr = "batch#" + str(batch)
        fileName = self.combineFileName(batch, fileNbr)
        fileClas = str("batchFileClas#" + str(fileNbr))
        self.CReader.set(batchStr, fileName, self.combineFileNameWithDir(batch, fileNbr))
        self.CReader.set(batchStr, fileClas, 'yes')
        fd = open(self.filePath, 'w')
        self.CReader.write(fd)
        fd.close()
            
    def updEleUncFileAsClf(self, batch, fileNbr, eleTag):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        batchStr = "batch#" + str(batch)
        fileName = self.combineFileName(batch, fileNbr)
        fileClas = str("batchFileClas#" + str(fileNbr))
        self.CReader.set(batchStr, fileName, self.combineFileNameWithDir(batch, fileNbr))
        self.CReader.set(batchStr, fileClas, 'yes')
        fd = open(self.filePath, 'w')
        self.CReader.write(fd)
        fd.close()

    def updateNormalUnclasFileAsClassified(self, batch, fileNbr):
        return self.updEleUncFileAsClf(batch, fileNbr, ModCebsCom.GL_CEBS_FILE_ATT_NORMAL)

    def updateFluUnclasFileAsClassified(self, batch, fileNbr):
        return self.updEleUncFileAsClf(batch, fileNbr, ModCebsCom.GL_CEBS_FILE_ATT_FLUORESCEN)

    '''
    * STEP6:
    *    公共的打印及错误处理过程
    *
    '''   
    #RECORD ERROR LOG FILE SAVING, WITH YMDHMS and basic information!
    def medErrorLog(self, inputStr):
        head = '\r[CEBS] ' + time.strftime("%Y/%m/%d %H:%M:%S") + ' [ERR] '
        outputStr = head + inputStr
        with open(ModCebsCom.GL_CEBS_ERR_LOG_FILE_NAME_SET, 'a+') as f:
            f.write(outputStr)

    #RECORD COMMAND LOG FILE SAVING, WITH YMDHMS and basic information!
    def medCmdLog(self, inputStr):
        head = '\r[CEBS] ' + time.strftime("%Y/%m/%d %H:%M:%S") + ' [CMD] '
        outputStr = head + inputStr
        with open(ModCebsCom.GL_CEBS_CMD_LOG_FILE_NAME_SET, 'a+') as f:
            f.write(outputStr)




