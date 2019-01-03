'''
Created on 2018/4/29

@author: hitpony
'''

####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-

import sys
import time
from multiprocessing import freeze_support
from PkgL3cebsHandler import ModCebsPrjEntry



'''
####程序包体系
- tupMain: 主入口
- PkgL1vmHandler：VM层的公共服务
- PkgL2svrHandler：公共服务接口和模块
- PkgL3cebsHandler：Cebs项目的任务模块
- PkgL4ceuiHandler：Cebs项目的界面
'''


####################################################
# 项目设置与选择
####################################################
PRJ_SET_CEBS        = 1
PRJ_SET_CEBS_MK2    = 2
PRJ_SET_MPLYAER     = 3
PRJ_SET_CUR         = PRJ_SET_CEBS
####################################################


#Pyinstaller打包多进程程序出错解决办法    https://blog.csdn.net/zyc121561/article/details/82941056
#运行时会出错，表现为进程不断增加至占满电脑CPU死机 
#SYSTEM ENTRY
if __name__ == '__main__':
    if (PRJ_SET_CUR  == PRJ_SET_CEBS):
        freeze_support() 
        print("[CEBS] ", time.asctime(), ", System starting...\n" );
        ModCebsPrjEntry.prj_cebs_main_entry();
    else:
        print("[NOBODY] ", time.asctime(), ", System starting and existing!\n" );














