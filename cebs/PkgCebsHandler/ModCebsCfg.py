'''
Created on 2018年5月4日

@author: Administrator
'''

####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-


import configparser
import os
import platform
import time
from PkgCebsHandler import ModCebsCom


class ConfigOpr(object):
    def __init__(self):
        self.filePath = ModCebsCom.GL_CEBS_CFG_FILE_NAME
        self.initGlobalPar()

    #初始化所有的存储区
    def initGlobalPar(self):
        #判定捕获图像的工作文件目录
        ModCebsCom.GL_CEBS_PIC_ABS_ORIGIN_PATH = os.getcwd()+ self.osDifferentStr() + ModCebsCom.GL_CEBS_PIC_ORIGIN_PATH
        flag = os.path.exists(ModCebsCom.GL_CEBS_PIC_ABS_ORIGIN_PATH)
        if (flag == False):
            os.mkdir(ModCebsCom.GL_CEBS_PIC_ABS_ORIGIN_PATH)
        ModCebsCom.GL_CEBS_PIC_ABS_ORIGIN_PATH += self.osDifferentStr()
        #判定中间图像的工作文件目录
        ModCebsCom.GL_CEBS_PIC_ABS_MIDDLE_PATH = os.getcwd()+ self.osDifferentStr() + ModCebsCom.GL_CEBS_PIC_MIDDLE_PATH
        flag = os.path.exists(ModCebsCom.GL_CEBS_PIC_ABS_MIDDLE_PATH)
        if (flag == False):
            os.mkdir(ModCebsCom.GL_CEBS_PIC_ABS_MIDDLE_PATH)
        ModCebsCom.GL_CEBS_PIC_ABS_MIDDLE_PATH += self.osDifferentStr()
        #判定是否需要创建ini文件
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
            self.CReader.add_section("Counter")
            self.CReader.set("Counter","PicBatchCnt", "0")
            self.CReader.set("Counter","PicBatchClas", "0")
            self.CReader.set("Counter","PicRemainCnt", "0")
            self.CReader.write(open(self.filePath, "w"))
        #为了防止ini文件中信息错误，重新写入
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
        fd = open(self.filePath, 'w')
        self.CReader.write(fd)
        fd.close()
                
    #写入全局控制数据
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

    #读取控制文件
    def getStoredFileName(self, batch, fileNbr):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        batchStr = "batch#" + str(batch)
        fileName = self.combineFileName(batch, fileNbr)
        res = self.CReader[batchStr][fileName];
        return res;

    def combineFileName(self, batch, fileNbr):
        return str("batch#" + str(batch) + "FileName#" + str(fileNbr))

    def combineFileNameWithDir(self, batch, fileNbr):
        fileName = str("batch#" + str(batch) + "FileName#" + str(fileNbr))
        return str(ModCebsCom.GL_CEBS_PIC_ABS_ORIGIN_PATH) + fileName + '.jpg'
    
    #得到某一个BTACH的未分类的第一个文件
    def getUnclasBatchFile(self, batch):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(self.filePath, encoding='utf8')
        batchStr = "batch#" + str(batch)
        if (self.CReader.has_section(batchStr) == False):
            return -1;
        # 遍历配置组的key, 与'DEFAULT'组的key
        for key in self.CReader[batchStr]:
            #print(key, self.CReader[batchStr][key])
            if (('batchfileclas#' in key) and (self.CReader[batchStr][key] == 'no')):
                temps = key[len('batchfileclas#'):]
                tempi = int(temps)
                return tempi;
        #没找到
        return -2;
    
    #全局搜索是否存在还未完成的图像
    def findUnclasFileBatchAndFileNbr(self):
        start = ModCebsCom.GL_CEBS_PIC_PROC_CLAS_INDEX;
        end = ModCebsCom.GL_CEBS_PIC_PROC_BATCH_INDEX;
        for index in range(start, end):
            fileNbr = self.getUnclasBatchFile(index);
            if (fileNbr >= 0):
                ModCebsCom.GL_CEBS_PIC_PROC_CLAS_INDEX = index;
                self.updateCtrlCntInfo()
                return index, fileNbr;
        return -1, -1;
                
    #更新分类后的图像文件信息
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


