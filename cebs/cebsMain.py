'''
Created on 2018/4/29

@author: hitpony
'''

####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-

import sys
import time
import cebsTkL4Ui
from PkgCetkHandler import ModCetkPrjEntry

from PkgCetkHandler import ModCetkPrjEntry
#Pyinstaller打包多进程程序出错解决办法    https://blog.csdn.net/zyc121561/article/details/82941056
#运行时会出错，表现为进程不断增加至占满电脑CPU死机 
from multiprocessing import freeze_support
#SYSTEM ENTRY
if __name__ == '__main__':
    freeze_support() 
    print("[CEBS] ", time.asctime(), ", System starting...\n" );
    ModCetkPrjEntry.prj_cebs_main_entry();


