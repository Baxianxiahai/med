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
from PkgL3cebsHandler import ModCebsCom
import urllib3
import json


'''
配置模块
'''
class clsL1_ConfigOpr():
    def __init__(self):
        pass
        #self.loadInitFileAndInitGlComPar()

    '''
    * STEP0:
    *    读取ini文件，如果发现不存在还需要重新创建。如果发现某些部分不合法或者错误，则需要重新创建并补充完整
    *
    '''   
    #INIT ALL STORAGE AREA
    def loadInitFileAndInitGlComPar(self):
        #JUDGE WORKING DIR
        ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_ORIGIN_PATH = os.getcwd()+ self.osDifferentStr() + ModCebsCom.GLCFG_PAR_OFC.PIC_ORIGIN_PATH
        flag = os.path.exists(ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_ORIGIN_PATH)
        if (flag == False):
            os.mkdir(ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_ORIGIN_PATH)
        ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_ORIGIN_PATH += self.osDifferentStr()
        #JUDGE MID PIC WOKRING DIR
        ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_MIDDLE_PATH = os.getcwd()+ self.osDifferentStr() + ModCebsCom.GLCFG_PAR_OFC.PIC_MIDDLE_PATH
        flag = os.path.exists(ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_MIDDLE_PATH)
        if (flag == False):
            os.mkdir(ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_MIDDLE_PATH)
        ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_MIDDLE_PATH += self.osDifferentStr()
        #JUDGE CREATE INIT FILE OR NOT
        self.CReader=configparser.ConfigParser()
        self.CReader.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, encoding='utf8')
        flagExist = os.path.exists(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME)
        flagEvn = self.CReader.has_section("Env")
        flagCounter = self.CReader.has_section("Counter")
        if (flagExist == False) or (flagEvn == False):
            self.CReader.add_section("Env")
            self.CReader.set("Env","workdir", str(os.getcwd()+ self.osDifferentStr()))
            self.CReader.set("Env","pic_origin", str(ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_ORIGIN_PATH))
            self.CReader.set("Env","pic_middle", str(ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_MIDDLE_PATH))
            self.CReader.set("Env","holeboard_type", str(ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE))
            self.CReader.set("Env","holeboard, left_bot X-axis", str(ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[0]))
            self.CReader.set("Env","holeboard, left_bot Y-axis", str(ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[1]))
            self.CReader.set("Env","holeboard, right_up X-Axis", str(ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[2]))
            self.CReader.set("Env","holeboard, right_up Y-Axis", str(ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[3]))
            self.CReader.set("Env","pic taking fix point set", str(ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET))
            self.CReader.set("Env","pic classification set", str(ModCebsCom.GLVIS_PAR_OFC.PIC_CLASSIFIED_AFTER_TAKE_SET))
            self.CReader.set("Env","pic auto-work after start set", str(ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_AFTER_START_SET))
            self.CReader.set("Env","pic auto-work tti", str(ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN))
            self.CReader.set("Env","vision small-low limit", str(ModCebsCom.GLVIS_PAR_OFC.SMALL_LOW_LIMIT))
            self.CReader.set("Env","vision small-mid limit", str(ModCebsCom.GLVIS_PAR_OFC.SMALL_MID_LIMIT))
            self.CReader.set("Env","vision mid-big limit", str(ModCebsCom.GLVIS_PAR_OFC.MID_BIG_LIMIT))
            self.CReader.set("Env","vision big-upper limit", str(ModCebsCom.GLVIS_PAR_OFC.BIG_UPPER_LIMIT))
            self.CReader.set("Env","vision res addup set", str(ModCebsCom.GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET))
            self.CReader.set("Env","video capture enable set", str(ModCebsCom.GLVIS_PAR_OFC.CAPTURE_ENABLE))
            self.CReader.set("Env","video capture dur in sec", str(ModCebsCom.GLVIS_PAR_OFC.CAPTURE_DUR_IN_SEC))
            self.CReader.set("Env","classification general par1", str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR1))
            self.CReader.set("Env","classification general par2", str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR2))
            self.CReader.set("Env","classification general par3", str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR3))
            self.CReader.set("Env","classification general par4", str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR4))
        if (flagExist == False) or (flagCounter == False):
            self.CReader.add_section("Counter")
            self.CReader.set("Counter","PicBatchCnt", "0")
            self.CReader.set("Counter","PicBatchClas", "0")
            self.CReader.set("Counter","PicRemainCnt", "0")
            self.CReader.set("Counter","PicBatFluClas", "0")
            self.CReader.set("Counter","PicRemFluCnt", "0")
        if (flagExist == False) or (flagEvn == False) or (flagCounter == False):   
            self.CReader.write(open(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, "w"))
            
        #REWRITE FILE TO AVOID INI FILE ERROR
        if (self.CReader['Env']['workdir'] != str(os.getcwd()+ self.osDifferentStr())):
            self.updateStaticSectionEnvPar()
    '''
    * STEP1:
    *    控制参数读取及更新过程
    *
    '''   
    #初始化读取全局图像
    def func_read_global_par_from_cfg_file(self):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, encoding='utf8')
        #config par
        ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX = int(self.CReader['Counter']['PicBatchCnt']);
        ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_CLAS_INDEX = int(self.CReader['Counter']['PicBatchClas']);
        ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT = int(self.CReader['Counter']['PicRemainCnt']);
        ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_CLAS_INDEX = int(self.CReader['Counter']['PicBatFluClas']);
        ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT = int(self.CReader['Counter']['PicRemFluCnt']);
        #Platform par
        ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE = self.CReader['Env']['holeboard_type'];
        ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[0] = int(self.CReader['Env']['holeboard, left_bot X-axis']);
        ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[1] = int(self.CReader['Env']['holeboard, left_bot Y-axis']);
        ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[2] = int(self.CReader['Env']['holeboard, right_up X-axis']);
        ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[3] = int(self.CReader['Env']['holeboard, right_up Y-axis']);
        tmp = self.CReader['Env']['pic taking fix point set']
        if (tmp == 'True'):
            ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET = True
        else:
            ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET = False
        tmp = self.CReader['Env']['pic classification set']
        if (tmp == 'True'):
            ModCebsCom.GLVIS_PAR_OFC.PIC_CLASSIFIED_AFTER_TAKE_SET = True
        else:
            ModCebsCom.GLVIS_PAR_OFC.PIC_CLASSIFIED_AFTER_TAKE_SET = False
        tmp = self.CReader['Env']['pic auto-work after start set']
        if (tmp == 'True'):
            ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_AFTER_START_SET = True
        else:
            ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_AFTER_START_SET = False
        ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN = int(self.CReader['Env']['pic auto-work tti']);
        #New def
        ModCebsCom.GLVIS_PAR_OFC.saveLowLimit(int(self.CReader['Env']['vision small-low limit']));
        ModCebsCom.GLVIS_PAR_OFC.saveMidLimit(int(self.CReader['Env']['vision small-mid limit']));
        ModCebsCom.GLVIS_PAR_OFC.saveBigLimit(int(self.CReader['Env']['vision mid-big limit']));
        ModCebsCom.GLVIS_PAR_OFC.saveUpperLimit(int(self.CReader['Env']['vision big-upper limit']));
        tmp = self.CReader['Env']['vision res addup set']
        if (tmp == 'True'):
            ModCebsCom.GLVIS_PAR_OFC.saveAddupSet(True)
        else:
            ModCebsCom.GLVIS_PAR_OFC.saveAddupSet(False)
        tmp = self.CReader['Env']['video capture enable set']
        if (tmp == 'True'):
            ModCebsCom.GLVIS_PAR_OFC.saveCapEnable(True)
        else:
            ModCebsCom.GLVIS_PAR_OFC.saveCapEnable(False)
        ModCebsCom.GLVIS_PAR_OFC.saveCapDur(int(self.CReader['Env']['video capture dur in sec']))
        #通用参数部分
        try:
            ModCebsCom.GLVIS_PAR_OFC.saveGenrPar1(int(self.CReader['Env']['classification general par1']));
        except Exception:
            ModCebsCom.GLVIS_PAR_OFC.saveGenrPar1(1)
        try:
            ModCebsCom.GLVIS_PAR_OFC.saveGenrPar2(int(self.CReader['Env']['classification general par2']));
        except Exception:
            ModCebsCom.GLVIS_PAR_OFC.saveGenrPar2(1)
        try:
            ModCebsCom.GLVIS_PAR_OFC.saveGenrPar3(int(self.CReader['Env']['classification general par3']));
        except Exception:
            ModCebsCom.GLVIS_PAR_OFC.saveGenrPar3(1)
        try:
            ModCebsCom.GLVIS_PAR_OFC.saveGenrPar4(int(self.CReader['Env']['classification general par4']));
        except Exception:
            ModCebsCom.GLVIS_PAR_OFC.saveGenrPar4(1)
        
        #In case of store error, re-caculate remaining unclas-pictures
        #为了防止统计错误，重新根据
        res = self.recheckRemaingUnclasBatchFile(ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_NORMAL)
        if (res != ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT):
            print("CFG: Error find during re-check remaining un-clas normal pictures and recovered! Stored=%d, actual=%d." % (ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT, res))
            #ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT = res
            self.updateStaticSectionEnvPar()
            delta = res - ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT
            self.updateBatCntWithIniFileSyned(False, delta, 0)
        #为了防止统计错误，重新扫描并计算荧光图像数量
        res = self.recheckRemaingUnclasBatchFile(ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_FLUORESCEN)
        if (res != ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT):
            print("CFG: Error find during re-check remaining un-clas Fluorescen pictures and recovered! Stored=%d, actual=%d." % (ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT, res))
            #ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT = res
            delta = res - ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT
            self.updateBatCntWithIniFileSyned(False, 0, delta)
            self.updateStaticSectionEnvPar()
            
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
    
    #更新板孔参数配置文件
    def updateStaticSectionEnvPar(self):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, encoding='utf8')        
        if (self.CReader.has_section("Env") == False):
            self.CReader.add_section("Env")
            self.CReader.set("Env","workdir", str(os.getcwd()+ self.osDifferentStr()))
            self.CReader.set("Env","pic_origin", str(ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_ORIGIN_PATH))
            self.CReader.set("Env","pic_middle", str(ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_MIDDLE_PATH))
            self.CReader.set("Env","holeboard_type", str(ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE))
            self.CReader.set("Env","holeboard, left_bot X-axis", str(ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[0]))
            self.CReader.set("Env","holeboard, left_bot Y-axis", str(ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[1]))
            self.CReader.set("Env","holeboard, right_up X-Axis", str(ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[2]))
            self.CReader.set("Env","holeboard, right_up Y-Axis", str(ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[3]))
            self.CReader.set("Env","pic taking fix point set", str(ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET))
            self.CReader.set("Env","pic classification set", str(ModCebsCom.GLVIS_PAR_OFC.PIC_CLASSIFIED_AFTER_TAKE_SET))
            self.CReader.set("Env","pic auto-work after start set", str(ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_AFTER_START_SET))
            self.CReader.set("Env","pic auto-work tti", str(ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN))
            self.CReader.set("Env","vision small-low limit", str(ModCebsCom.GLVIS_PAR_OFC.SMALL_LOW_LIMIT))
            self.CReader.set("Env","vision small-mid limit", str(ModCebsCom.GLVIS_PAR_OFC.SMALL_MID_LIMIT))
            self.CReader.set("Env","vision mid-big limit", str(ModCebsCom.GLVIS_PAR_OFC.MID_BIG_LIMIT))
            self.CReader.set("Env","vision big-upper limit", str(ModCebsCom.GLVIS_PAR_OFC.BIG_UPPER_LIMIT))
            self.CReader.set("Env","vision res addup set", str(ModCebsCom.GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET))
            self.CReader.set("Env","video capture enable set", str(ModCebsCom.GLVIS_PAR_OFC.CAPTURE_ENABLE))
            self.CReader.set("Env","video capture dur in sec", str(ModCebsCom.GLVIS_PAR_OFC.CAPTURE_DUR_IN_SEC))
            self.CReader.set("Env","classification general par1", str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR1))
            self.CReader.set("Env","classification general par2", str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR2))
            self.CReader.set("Env","classification general par3", str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR3))
            self.CReader.set("Env","classification general par4", str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR4))
        else:
            self.CReader.remove_section("Env")
            self.CReader.add_section("Env")        
            self.CReader.set("Env","workdir", str(os.getcwd()+ self.osDifferentStr()))
            self.CReader.set("Env","pic_origin", str(ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_ORIGIN_PATH))
            self.CReader.set("Env","pic_middle", str(ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_MIDDLE_PATH))
            self.CReader.set("Env","holeboard_type", str(ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE))
            self.CReader.set("Env","holeboard, left_bot X-axis", str(ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[0]))
            self.CReader.set("Env","holeboard, left_bot Y-axis", str(ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[1]))
            self.CReader.set("Env","holeboard, right_up X-Axis", str(ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[2]))
            self.CReader.set("Env","holeboard, right_up Y-Axis", str(ModCebsCom.GLPLT_PAR_OFC.HB_POS_IN_UM[3]))
            self.CReader.set("Env","pic taking fix point set", str(ModCebsCom.GLVIS_PAR_OFC.PIC_TAKING_FIX_POINT_SET))
            self.CReader.set("Env","pic classification set", str(ModCebsCom.GLVIS_PAR_OFC.PIC_CLASSIFIED_AFTER_TAKE_SET))
            self.CReader.set("Env","pic auto-work after start set", str(ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_AFTER_START_SET))
            self.CReader.set("Env","pic auto-work tti", str(ModCebsCom.GLVIS_PAR_OFC.PIC_AUTO_WORKING_TTI_IN_MIN))
            self.CReader.set("Env","vision small-low limit", str(ModCebsCom.GLVIS_PAR_OFC.SMALL_LOW_LIMIT))
            self.CReader.set("Env","vision small-mid limit", str(ModCebsCom.GLVIS_PAR_OFC.SMALL_MID_LIMIT))
            self.CReader.set("Env","vision mid-big limit", str(ModCebsCom.GLVIS_PAR_OFC.MID_BIG_LIMIT))
            self.CReader.set("Env","vision big-upper limit", str(ModCebsCom.GLVIS_PAR_OFC.BIG_UPPER_LIMIT))
            self.CReader.set("Env","vision res addup set", str(ModCebsCom.GLVIS_PAR_OFC.CLAS_RES_ADDUP_SET))
            self.CReader.set("Env","video capture enable set", str(ModCebsCom.GLVIS_PAR_OFC.CAPTURE_ENABLE))
            self.CReader.set("Env","video capture dur in sec", str(ModCebsCom.GLVIS_PAR_OFC.CAPTURE_DUR_IN_SEC))
            self.CReader.set("Env","classification general par1", str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR1))
            self.CReader.set("Env","classification general par2", str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR2))
            self.CReader.set("Env","classification general par3", str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR3))
            self.CReader.set("Env","classification general par4", str(ModCebsCom.GLVIS_PAR_OFC.CFY_THD_GENR_PAR4))
        #回写                    
        fd = open(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, 'w')
        self.CReader.write(fd)
        fd.flush()
        fd.close()
    

    '''
    #单独的更新全局控制函数已经不能满足要求，必须将全局控制数与文件更新放在一起，才比较安全，不然会出现参数更新了，但配置文件并没有更新的情况
    #
    # BatFlg = True: +1，False: 不变  (这个是指针，所以只能不断增加)
    # PicRemDelta = delta部分，直接加或者减去
    # FluRemDelta = delta部分，直接加或者减去
    #
    # 本函数的应用，从最初完成后更新，改为进入以后直接更新，简化设计方案
    #
    '''
    def updateBatCntWithIniFileSyned(self, BatFlg, PicRemDelta, FluRemDelta):
        #处理控制系数
        if (BatFlg == True):
            ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX += 1
        ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT += PicRemDelta
        ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT += FluRemDelta

        #正式更新
        self.CReader=configparser.ConfigParser()
        self.CReader.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, encoding='utf8')
        if (self.CReader.has_section("Counter") == False):
            self.CReader.add_section("Counter")
            self.CReader.set("Counter","PicBatchCnt", str(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX))
            #普通图像
            self.CReader.set("Counter","PicBatchClas", str(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_CLAS_INDEX))
            self.CReader.set("Counter","PicRemainCnt", str(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            #荧光图像控制参数
            self.CReader.set("Counter","PicBatFluClas", str(ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_CLAS_INDEX))
            self.CReader.set("Counter","PicRemFluCnt", str(ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT))
            
        else:
            self.CReader.remove_section("Counter")
            self.CReader.add_section("Counter")
            self.CReader.set("Counter","PicBatchCnt", str(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX))
            #普通图像
            self.CReader.set("Counter","PicBatchClas", str(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_CLAS_INDEX))
            self.CReader.set("Counter","PicRemainCnt", str(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            #荧光图像控制参数
            self.CReader.set("Counter","PicBatFluClas", str(ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_CLAS_INDEX))
            self.CReader.set("Counter","PicRemFluCnt", str(ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT))
        fd = open(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, 'w')
        self.CReader.write(fd)
        fd.flush()
        fd.close()
    
    '''
    #
    #更新图像识别的计数器，并同步写到文件中去
    # PicCfyCur = 就是当前全局变量：变化太大，使用delta不好控制
    # FluCfyCur = 就是当前全局变量：变化太大，使用delta不好控制
    # PicRemCnt = 实际部分，不再使用加减法
    # FluRemCnt = 实际部分，不再使用加减法
    #
    '''
    def updateCfyCntWithIniFileSyned(self, PicCfyCur, FluCfyCur, PicRemCnt, FluRemCnt):
        #处理控制系数
        ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_CLAS_INDEX = PicCfyCur
        ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_CLAS_INDEX = FluCfyCur
        ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT = PicRemCnt
        ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT = FluRemCnt

        #正式更新
        self.CReader=configparser.ConfigParser()
        self.CReader.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, encoding='utf8')
        if (self.CReader.has_section("Counter") == False):
            self.CReader.add_section("Counter")
            self.CReader.set("Counter","PicBatchCnt", str(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX))
            #普通图像
            self.CReader.set("Counter","PicBatchClas", str(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_CLAS_INDEX))
            self.CReader.set("Counter","PicRemainCnt", str(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            #荧光图像控制参数
            self.CReader.set("Counter","PicBatFluClas", str(ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_CLAS_INDEX))
            self.CReader.set("Counter","PicRemFluCnt", str(ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT))
            
        else:
            self.CReader.remove_section("Counter")
            self.CReader.add_section("Counter")
            self.CReader.set("Counter","PicBatchCnt", str(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX))
            #普通图像
            self.CReader.set("Counter","PicBatchClas", str(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_CLAS_INDEX))
            self.CReader.set("Counter","PicRemainCnt", str(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT))
            #荧光图像控制参数
            self.CReader.set("Counter","PicBatFluClas", str(ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_CLAS_INDEX))
            self.CReader.set("Counter","PicRemFluCnt", str(ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT))
        fd = open(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, 'w')
        self.CReader.write(fd)
        fd.flush()
        fd.close()

    '''
    * STEP2:
    *    单个文件处理过程，批次处理过程
    *
    '''   
    '''
    #新增加一个批次时，需要创建批次表头
    #目前创建新的批次，只有两种可能性
    # 第一种：正常业务拍照+FLU
    # 第二种：校准过程中截图
    '''
    def createBatSectAndIniSyned(self, batch):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, encoding='utf8')
        batchStr = "batch#" + str(batch)
        if (self.CReader.has_section(batchStr) == True):
            self.CReader.remove_section(batchStr)
            self.CReader.add_section(batchStr)
        else:
            self.CReader.add_section(batchStr)
        self.CReader.set(batchStr, "batch number", str(batch))
        self.CReader.set(batchStr, "work time", str(time.asctime()))
        fd = open(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, 'w')
        self.CReader.write(fd)
        fd.flush()
        fd.close()

    #增加普通文件 => 写到ini文件中去
    def addNormalBatchFile(self, batch, fileNbr):
        return self.addBatchFileInElement(batch, fileNbr, ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_NORMAL)
    
    #增加荧光文件 => 写到ini文件中去
    def addFluBatchFile(self, batch, fileNbr):
        return self.addBatchFileInElement(batch, fileNbr, ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_FLUORESCEN)
    
    '''
    #基础函数过程
    #同一个图像在反复存储的情况下，这个函数是否不出错
    #
    # batch - 批次号
    # fileNbr - 文件序号
    # eleTag - 指明是normal还是flu的文件属性
    #
    #
    # fileName - 文件名字
    # fileClas - 文件是否已经被识别
    # fileAtt - 文件属性， 对应上面eleTag
    # fileVideoClag - 视频属性
    # cfyResWormNbr - 识别后线虫的统计数量，以字符串的形式展现
    #
    #
    '''
    def addBatchFileInElement(self, batch, fileNbr, eleTag):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, encoding='utf8')
        batchStr = "batch#" + str(batch)
        if (self.CReader.has_section(batchStr) == False):
            print("CFG: Batch not exist, batch = ", str(batchStr))
            return -1
        fileName = self.combineFileName(batch, fileNbr)
        fileClas = str("batchFileClas#" + str(fileNbr))
        fileAtt = str("batchFileAtt#" + str(fileNbr))
        fileVideoClag = str("batchFileVidFlag#" + str(fileNbr))
        cfyResWormNbr = str("cfyResWormNbr#" + str(fileNbr))
        self.CReader.set(batchStr, fileName, self.combineFileNameWithDir(batch, fileNbr))
        self.CReader.set(batchStr, fileClas, 'no')
        self.CReader.set(batchStr, fileAtt, eleTag)
        self.CReader.set(batchStr, fileVideoClag, 'no')
        self.CReader.set(batchStr, cfyResWormNbr, '')
        try:
            fd = open(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, 'w')
        except Exception as err:  
            print("CFG: Open file failure, err = " + str(err))
            return -2;
        finally:
            self.CReader.write(fd)
            fd.flush()
            fd.close()
    
    #更新文件的视频属性
    def updBatchFileVideo(self, batch, fileNbr):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, encoding='utf8')
        batchStr = "batch#" + str(batch)
        fileVidFlag = str("batchFileVidFlag#" + str(fileNbr))
        videoName = self.combineVideoName(batch, fileNbr)
        self.CReader.set(batchStr, fileVidFlag, 'yes')
        self.CReader.set(batchStr, videoName, self.combineFileNameVideoWithDir(batch, fileNbr))
        try:
            fd = open(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, 'w')
        except Exception as err:  
            print("CFG: Open file failure, err = " + str(err))
            return -1;
        finally:
            self.CReader.write(fd)
            fd.flush()
            fd.close()

    '''
    * STEP3:
    *    文件名字处理过程
    *
    '''   
    #READ CONTROL FILE
    def getStoredFileName(self, batch, fileNbr):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, encoding='utf8')
        batchStr = "batch#" + str(batch)
        fileName = self.combineFileName(batch, fileNbr)
        res = self.CReader[batchStr][fileName];
        return res;

    #Without file path
    def getStoredFileNukeName(self, batch, fileNbr):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, encoding='utf8')
        fileName = self.combineFileName(batch, fileNbr)
        res = fileName + '.jpg'
        return res;

    def combineFileName(self, batch, fileNbr):
        return str("batch#" + str(batch) + "FileName#" + self.func_cvt_indexfilehole(fileNbr))

    def combineScaleFileName(self, batch, fileNbr):
        return str("scale_batch#" + str(batch) + "FileName#" + self.func_cvt_indexfilehole(fileNbr))

    def combineVideoName(self, batch, fileNbr):
        return str("batch#" + str(batch) + "VideoName#" + self.func_cvt_indexfilehole(fileNbr))

    def combineFileNameWithDir(self, batch, fileNbr):  
        fileName = str("batch#" + str(batch) + "FileName#" + self.func_cvt_indexfilehole(fileNbr))
        return str(ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_ORIGIN_PATH) + fileName + '.jpg'

    def combineScaleFileNameWithDir(self, batch, fileNbr):
        fileName = str("scale_batch#" + str(batch) + "FileName#" + self.func_cvt_indexfilehole(fileNbr))
        return str(ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_ORIGIN_PATH) + fileName + '.jpg'
    
    def combineFileNameVideoWithDir(self, batch, fileNbr):

        fileName = str("batch#" + str(batch) + "FileName#" + self.func_cvt_indexfilehole(fileNbr))
        return str(ModCebsCom.GLCFG_PAR_OFC.PIC_ABS_ORIGIN_PATH) + fileName + '.mp4'  #.mp4, .avi


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
        if (eleTag == ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_NORMAL):
            start = ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_CLAS_INDEX;
        if (eleTag == ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_FLUORESCEN):
            start = ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_CLAS_INDEX;
        end = ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX;
        #Refresh CReader to be lastest one
        self.CReader=configparser.ConfigParser()
        self.CReader.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, encoding='utf8')
        #Under searching start==end, it is stop. So we extend the range a little bit bigger.
        fileNbr = -1
        for index in range(start, end+1):
            #Find the very first picture which fulfill the condition, but not the whole number of unclassified pictures.
            batchStr = "batch#" + str(index)
            if (self.CReader.has_section(batchStr) == False):
                continue;
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
        if ((fileNbr >= 0) and (eleTag == ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_NORMAL)):
            ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_CLAS_INDEX = index;
            self.updateCfyCntWithIniFileSyned(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_CLAS_INDEX, ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_CLAS_INDEX, ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT, ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT);
            #self.updateCtrlCntInfo()
            return index, fileNbr;
        elif ((fileNbr >= 0) and (eleTag == ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_FLUORESCEN)):
            ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_CLAS_INDEX = index;
            self.updateCfyCntWithIniFileSyned(ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_CLAS_INDEX, ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_CLAS_INDEX, ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_REMAIN_CNT, ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_REMAIN_CNT);
            #self.updateCtrlCntInfo()
            return index, fileNbr;
        else:
            return -2, -2;

    #可以被其它模块调用的函数
    def findNormalUnclasFileBatchAndNbr(self):
        return self.findUnclasFileBatchAndFileNbr(ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_NORMAL)

    #可以被其它模块调用的函数
    def findFluUnclasFileBatchAndNbr(self):
        return self.findUnclasFileBatchAndFileNbr(ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_FLUORESCEN)


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
        if (eleTag == ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_NORMAL):
            start = ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_CLAS_INDEX;
        if (eleTag == ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_FLUORESCEN):
            start = ModCebsCom.GLCFG_PAR_OFC.PIC_FLU_CLAS_INDEX;
        end = ModCebsCom.GLCFG_PAR_OFC.PIC_PROC_BATCH_INDEX;
        self.CReader=configparser.ConfigParser()
        self.CReader.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, encoding='utf8')
        res = 0;
        for index in range(start, end+1):
            batchStr = "batch#" + str(index)
            #如果发现不合法就继续，因为有可能出现批次中断的情况
            if (self.CReader.has_section(batchStr) == False):
                continue
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
    
    '''            
    #
    #UPDATE CATEGORY PICTURE INFORMATION
    #
    #
    # batch - 批次号
    # fileNbr - 文件编号
    # cfyWormNbr - 线虫识别数量，字符串系列
    # cfyCellCnt - 荧光细胞数量结果
    #
    '''
    def updateUnclasFileAsClassified(self, batch, fileNbr, cfyWormNbr):
        self.CReader=configparser.ConfigParser()
        self.CReader.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, encoding='utf8')
        batchStr = "batch#" + str(batch)
        fileName = self.combineFileName(batch, fileNbr)
        fileClas = str("batchFileClas#" + str(fileNbr))
        cfyResWormNbr = str("cfyResWormNbr#" + str(fileNbr))
        self.CReader.set(batchStr, fileName, self.combineFileNameWithDir(batch, fileNbr))
        self.CReader.set(batchStr, fileClas, 'yes')
        self.CReader.set(batchStr, cfyResWormNbr, str(cfyWormNbr))
        fd = open(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, 'w')
        self.CReader.write(fd)
        fd.flush()
        fd.close()

    '''
    #
    #下面三个函数暂时没有使用起来
    #
    # 已经明确，normal属性是在创建文件时，就存入到该文件的熟悉中
    #
    '''
#     def updateNormalUnclasFileAsClassified(self, batch, fileNbr):
#         return self.updEleUncFileAsClf(batch, fileNbr, ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_NORMAL)
# 
#     def updateFluUnclasFileAsClassified(self, batch, fileNbr):
#         return self.updEleUncFileAsClf(batch, fileNbr, ModCebsCom.GLCFG_PAR_OFC.FILE_ATT_FLUORESCEN)
#     
#     def updEleUncFileAsClf(self, batch, fileNbr, eleTag):
#         self.CReader=configparser.ConfigParser()
#         self.CReader.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, encoding='utf8')
#         batchStr = "batch#" + str(batch)
#         fileName = self.combineFileName(batch, fileNbr)
#         fileClas = str("batchfileclas#" + str(fileNbr))
#         fileAttr = str("batchfileatt#" + str(fileNbr))
#         self.CReader.set(batchStr, fileName, self.combineFileNameWithDir(batch, fileNbr))
#         self.CReader.set(batchStr, fileClas, 'yes')
#         self.CReader.set(batchStr, fileAttr, eleTag)
#         fd = open(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, 'w')
#         self.CReader.write(fd)
#         fd.close()



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

    '''获取机器标签和配置'''
    def GetMachineTagandConfigure(self):
        config=configparser.ConfigParser()
        config.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME,encoding="utf-8")
        tag=config.get("NAME",'name')
        configure=config.get("Env",'holeboard_type')
        return tag,configure
    def SetDishRowandColumn(self):
        config=configparser.ConfigParser()
        config.read(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME,encoding='utf-8')
        if "RowAndColumn" in config:
            pass
        else:
            config.add_section("RowAndColumn")
            config.write(open(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME,'w'))
        tag, configerture=self.GetMachineTagandConfigure()
        url="http://127.0.0.1/"+tag+".txt"
        http=urllib3.PoolManager()
        response=http.request("GET",url)
        data=response.data
        JsonData=json.loads(data)
        ColumnArray=[]
        for i in range(9):
            Column=[]
            for j in range(len(JsonData)):
                row=int(JsonData[j].split('_')[0])
                column=int(JsonData[j].split('_')[1])
                if i==row-1:
                    Column.append(column)
            ColumnArray.append(Column)
        config.set("RowAndColumn","Row1",json.dumps(ColumnArray[0]))
        config.set("RowAndColumn","Row2",json.dumps(ColumnArray[1]))
        config.set("RowAndColumn","Row3",json.dumps(ColumnArray[2]))
        config.set("RowAndColumn","Row4",json.dumps(ColumnArray[3]))
        config.set("RowAndColumn","Row5",json.dumps(ColumnArray[4]))
        config.set("RowAndColumn","Row6",json.dumps(ColumnArray[5]))
        config.set("RowAndColumn","Row7",json.dumps(ColumnArray[6]))
        config.set("RowAndColumn","Row8",json.dumps(ColumnArray[7]))
        config.set("RowAndColumn","Row9",json.dumps(ColumnArray[8]))
        config.write(open(ModCebsCom.GLCFG_PAR_OFC.CFG_FILE_NAME, 'w'))
        # for i in range(len(RowArray)):
        #     for j in range
# if __name__=="__main__":
#     a=clsL1_ConfigOpr()
#     name,config=a.GetMachineTagandConfigure()
#     print(name)
#     print(config)
    _MOD_CEBS_CFG_HB96 = ['A0', 'A1', 'A2', 'A3', 'A4','A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',\
                           'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12',\
                           'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12',\
                           'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12',\
                           'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12',\
                           'F1', 'F2', 'F3','F4', 'F5', 'F6', 'F7', 'F8' ,'F9', 'F10', 'F11', 'F12',\
                           'G1', 'G2', 'G3', 'G4','G5','G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12',\
                           'H1', 'H2', 'H3','H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12',\
                           ];
                           
    _MOD_CEBS_CFG_HB48 = ['A0', 'A1', 'A2', 'A3', 'A4','A5', 'A6', 'A7', 'A8',\
                           'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8',\
                           'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8',\
                           'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8',\
                           'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8',\
                           'F1', 'F2', 'F3','F4', 'F5', 'F6', 'F7', 'F8',\
                           ];
                           
    _MOD_CEBS_CFG_HB24 = ['A0', 'A1', 'A2', 'A3', 'A4','A5', 'A6',\
                           'B1', 'B2', 'B3', 'B4', 'B5', 'B6',\
                           'C1', 'C2', 'C3', 'C4', 'C5', 'C6',\
                           'D1', 'D2', 'D3', 'D4', 'D5', 'D6',\
                           ];
    _MOD_CEBS_CFG_HB12 = ['A0', 'A1', 'A2', 'A3', 'A4',\
                           'B1', 'B2', 'B3', 'B4',\
                           'C1', 'C2', 'C3', 'C4',\
                           ];
    _MOD_CEBS_CFG_HB6 = ['A0', 'A1', 'A2', 'A3',\
                         'B1', 'B2', 'B3',\
                          ];
    def func_cvt_indexfilehole(self,index):
        if (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_96_STANDARD):
            return self._MOD_CEBS_CFG_HB96[index];
        if (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_48_STANDARD):
            return self._MOD_CEBS_CFG_HB48[index];
        if (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_24_STANDARD):
            return self._MOD_CEBS_CFG_HB24[index];
        if (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_12_STANDARD):
            return self._MOD_CEBS_CFG_HB12[index];
        if (ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_TYPE == ModCebsCom.GLPLT_PAR_OFC.HB_TARGET_6_STANDARD):
            return self._MOD_CEBS_CFG_HB6[index];     
        else:
            return index;

