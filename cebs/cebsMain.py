'''
Created on 2018/4/29

@author: hitpony
'''

####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-

import sys
import time


#老模式已经不能工作了
# GL_MAIN_WORK_MODE_CEBSL4UI = 1
# GL_MAIN_WORK_MODE_VM_TASK = 2
# GL_MAIN_CUR_WORK_MODE = GL_MAIN_WORK_MODE_VM_TASK

#SYSTEM ENTRY
if __name__ == '__main__':
    print("[CEBS] ", time.asctime(), ", System starting...\n" );
    
#     #传统模式
#     if (GL_MAIN_CUR_WORK_MODE == GL_MAIN_WORK_MODE_CEBSL4UI):
#         import cebsL4Ui     
#         cebsL4Ui.cebs_l4ui_main_form_entry();
# 
#     #新模式
#     else:
    import cebsTkL4Ui
    from PkgCetkHandler import ModCetkPrjEntry
    ModCetkPrjEntry.prj_cebs_main_entry();
    


