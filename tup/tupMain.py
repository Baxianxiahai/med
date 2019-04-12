'''
Created on 2018/4/29

@author: hitpony
'''

####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-

# import sys
import time
from multiprocessing import freeze_support
    

'''
####程序包体系
- tupMain: 主入口
- PkgL1vmHandler：VM层的公共服务
- PkgL2svrHandler：公共服务接口和模块
- PkgL3cebsHandler：Cebs项目的任务模块
- PkgL4ceuiHandler：Cebs项目的界面

- TupMain
    -> PrjEntry
        -> L4 Ceui Main QT Task （QT界面任务）
            -> L4 Ceui QT xxx Task
        -> L3 CebsUiXxx Task （QT界面接口任务）
            -> L3 CebsUiBasic基类
                -> L3CFG: clsL1_ConfigOpr
                -> L2 Service: TupClsPicProc
                -> L1VMLayer: tupTaskTemplate
        -> L3 Moto Task    （马达处理任务）
            -> L3 CebsUiBasic基类
                -> L3CFG: clsL1_ConfigOpr
                -> L2 Service: TupClsPicPro\=
                -> L1VMLayer: tupTaskTemplate
        -> L3 Vision Task    （摄像头处理任务）
            -> L3 CebsUiBasic基类
                -> L3CFG: clsL1_ConfigOpr
                -> L2Service: TupClsPicProc
                -> L1VMLayer: tupTaskTemplate
        -> L3 CebsXxx Task    （业务逻辑处理任务）
            -> L3 CebsBasic基类
                -> L3CFG: clsL1_ConfigOpr
                -> L2Service: TupClsPicProc
                -> L1VMLayer: tupTaskTemplate
            
'''


####################################################
# 项目设置与选择
####################################################
PRJ_SET_CEBS        = 1 #基于PC
PRJ_SET_CEBS_MK2    = 2 #基于VCD+MDC
PRJ_SET_MPLYAER     = 3 #演示
PRJ_SET_FAWS        = 4 #秤项
PRJ_SET_CUR         = PRJ_SET_CEBS
####################################################


#Pyinstaller打包多进程程序出错解决办法    https://blog.csdn.net/zyc121561/article/details/82941056
#运行时会出错，表现为进程不断增加至占满电脑CPU死机 
#SYSTEM ENTRY
from PkgL3cebsHandler import ModCebsPrjEntry
if __name__ == '__main__':
    if (PRJ_SET_CUR  == PRJ_SET_CEBS):
        freeze_support() 
        print("[CEBS] ", time.asctime(), ", System starting...\n" );
        ModCebsPrjEntry.prj_cebs_main_entry();
    elif (PRJ_SET_CUR  == PRJ_SET_CEBS_MK2):
        freeze_support() 
        print("[CEBS-Mk2] ", time.asctime(), ", System starting...\n" );
        ModCebsPrjEntry.prj_cebs_main_entry();
    else:
        print("[NOBODY] ", time.asctime(), ", System starting and existing!\n" );















