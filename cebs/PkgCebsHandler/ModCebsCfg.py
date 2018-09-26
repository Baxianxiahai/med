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
            self.CReader.set("Env","holeboard, left_up X-axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[0]))
            self.CReader.set("Env","holeboard, left_up Y-axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[1]))
            self.CReader.set("Env","holeboard, right bot X-Axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[2]))
            self.CReader.set("Env","holeboard, right bot Y-Axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[3]))
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
            self.CReader.write(open(self.filePath, "w"))
        #REWRITE FILE TO AVOID INI FILE ERROR
        if (self.CReader['Env']['workdir'] != str(os.getcwd()+ self.osDifferentStr())):
            self.updateSectionPar()


    def readGlobalPar(self):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX = int(self.CReader['Counter']['PicBatchCnt']);
        ModCebsCom.GL_CEBS_PIC_PROC_CLAS_INDEX = int(self.CReader['Counter']['PicBatchClas']);
        ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT = int(self.CReader['Counter']['PicRemainCnt']);
        ModCebsCom.GL_CEBS_HB_TARGET_TYPE = self.CReader['Env']['holeboard_type'];
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] = int(self.CReader['Env']['holeboard, left_up X-axis']);
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] = int(self.CReader['Env']['holeboard, left_up Y-axis']);
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] = int(self.CReader['Env']['holeboard, right bot X-axis']);
        ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] = int(self.CReader['Env']['holeboard, right bot Y-axis']);
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
        res = self.recheckRemaingUnclasBatchFile()
        if (res != ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT):
            print("CFG: Error find during re-check remaining un-clas pictures! Stored=%d, actual=%d." % (ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT, res))
            ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT = res
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
            self.CReader.set("Env","holeboard, left_up X-axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[0]))
            self.CReader.set("Env","holeboard, left_up Y-axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[1]))
            self.CReader.set("Env","holeboard, right bot X-Axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[2]))
            self.CReader.set("Env","holeboard, right bot Y-Axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[3]))
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
            self.CReader.set("Env","holeboard, left_up X-axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[0]))
            self.CReader.set("Env","holeboard, left_up Y-axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[1]))
            self.CReader.set("Env","holeboard, right bot X-Axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[2]))
            self.CReader.set("Env","holeboard, right bot Y-Axis", str(ModCebsCom.GL_CEBS_HB_POS_IN_UM[3]))
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
            self.CReader.set("Counter","PicBatchClas", str(ModCebsCom.GL_CEBS_PIC_PROC_CLAS_INDEX))
            self.CReader.set("Counter","PicRemainCnt", str(ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT))
            
        else:
            self.CReader.remove_section("Counter")
            self.CReader.add_section("Counter")
            self.CReader.set("Counter","PicBatchCnt", str(ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX))
            self.CReader.set("Counter","PicBatchClas", str(ModCebsCom.GL_CEBS_PIC_PROC_CLAS_INDEX))
            self.CReader.set("Counter","PicRemainCnt", str(ModCebsCom.GL_CEBS_PIC_PROC_REMAIN_CNT))
        fd = open(self.filePath, 'w')
        self.CReader.write(fd)
        fd.close()

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

    def addBatchFile(self, batch, fileNbr):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        batchStr = "batch#" + str(batch)
        fileName = self.combineFileName(batch, fileNbr)
        fileClas = str("batchFileClas#" + str(fileNbr))
        self.CReader.set(batchStr, fileName, self.combineFileNameWithDir(batch, fileNbr))
        self.CReader.set(batchStr, fileClas, 'no')
        try:
            fd = open(self.filePath, 'w')
        except Exception as err:  
            print("CFG: Open file failure, err = " + str(err))
            return -1;
        finally:
            self.CReader.write(fd)
            fd.close()

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
        batchStr = "batch#" + str(batch)
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


    #FETCH UN-CLASSIFIED FILE FOR ONE BATCH, WITH FIRST TARGET ONLY
    #这个函数只是用来找到最后一个未识别图像的起点，而并不是总共还有多少图像未识别
    def getUnclasBatchFileAtFirstIndex(self, batch):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        batchStr = "batch#" + str(batch)
        if (self.CReader.has_section(batchStr) == False):
            return -1;
        #SEARCH ALL CONFIGURATION KEY and 'DEFAULT' key
        for key in self.CReader[batchStr]:
            #print("key = %s, Creader = %s" %(str(key), str(self.CReader[batchStr][key])))
            if (('batchfileclas#' in key) and (self.CReader[batchStr][key] == 'no')):
                temps = key[len('batchfileclas#'):]
                tempi = int(temps)
                return tempi;
        #NOT FIND
        return -2;

    #SEARCH GLOBAL WETHER UN-FINISHED PICTURE EXIST
    #目标是找到未识别图像的第一个目标
    def findUnclasFileBatchAndFileNbr(self):
        start = ModCebsCom.GL_CEBS_PIC_PROC_CLAS_INDEX;
        end = ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX;
        #搜索的时候，可能会出现start==end的情况，然后就停止了
        for index in range(start, end+1):
            fileNbr = self.getUnclasBatchFileAtFirstIndex(index);
            if (fileNbr >= 0):
                ModCebsCom.GL_CEBS_PIC_PROC_CLAS_INDEX = index;
                self.updateCtrlCntInfo()
                return index, fileNbr;
        return -1, -1;

    #FETCH UN-CLASSIFIED FILE FOR ONE BATCH, WITH TOTAL NUMBER
    #寻找所有未识别图像数量
    def getUnclasBatchFileWithTotalNbr(self, batch):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        batchStr = "batch#" + str(batch)
        if (self.CReader.has_section(batchStr) == False):
            return -1;
        #SEARCH ALL CONFIGURATION KEY and 'DEFAULT' key
        totalNbr = 0
        for key in self.CReader[batchStr]:
            #print("key = %s, Creader = %s" %(str(key), str(self.CReader[batchStr][key])))
            if (('batchfileclas#' in key) and (self.CReader[batchStr][key] == 'no')):
                totalNbr +=1
        #FINAL RESULT
        return totalNbr
    
    #FETCH ALL REMAINING UNCLAS BATCH FILES TOTAL NUMBER
    #寻找所有还未识别图像的总数
    def recheckRemaingUnclasBatchFile(self):
        start = ModCebsCom.GL_CEBS_PIC_PROC_CLAS_INDEX;
        end = ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX;
        res = 0;
        for index in range(start, end+1):
            fileNbr = self.getUnclasBatchFileWithTotalNbr(index);
            if (fileNbr > 0):
                res += fileNbr
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

    #RECORD ERROR LOG FILE SAVING, WITH YMDHMS and basic information!
    def medErrorLog(self, inputStr):
        head = '\r[CEBS] ' + time.strftime("%Y/%m/%d %H:%M:%S") + ' [ERR] '
        outputStr = head + inputStr
        with open(ModCebsCom.GL_CEBS_ERR_LOG_FILE_NAME_SET, 'a+') as f:
            f.write(outputStr)

