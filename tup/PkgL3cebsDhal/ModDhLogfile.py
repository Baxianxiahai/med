'''
Created on 2019年6月4日

@author: Administrator
'''

import time
from PkgL3cebsDhal.cebsConfig import *

class clsCebsDhLogfile():
    #
    # 固定配置参数部分
    #

    
    def __init__(self):    
        super(clsCebsDhLogfile, self).__init__()  


    #RECORD ERROR LOG FILE SAVING, WITH YMDHMS and basic information!
    def tupErrorLog(self, inputStr):
        head = '\r[CEBS] ' + time.strftime("%Y/%m/%d %H:%M:%S") + ' [ERR] '
        outputStr = head + inputStr
        with open(_TUP_CEBS_ERR_LOG_FILE_NAME_SET, 'a+') as f:
            f.write(outputStr)

    #RECORD COMMAND LOG FILE SAVING, WITH YMDHMS and basic information!
    def tupCmdLog(self, inputStr):
        head = '\r[CEBS] ' + time.strftime("%Y/%m/%d %H:%M:%S") + ' [CMD] '
        outputStr = head + inputStr
        with open(_TUP_CEBS_CMD_LOG_FILE_NAME_SET, 'a+') as f:
            f.write(outputStr)    