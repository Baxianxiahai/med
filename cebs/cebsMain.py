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

#SYSTEM ENTRY
if __name__ == '__main__':
    print("[CEBS] ", time.asctime(), ", System starting...\n" );
    ModCetkPrjEntry.prj_cebs_main_entry();
    


