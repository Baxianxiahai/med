'''
Created on 2019年6月3日

@author: Administrator
'''

import configparser
import os
import platform
import time
import urllib3
import json

#公共数据操作API
from PkgL2svrUniv.ModCebsDba import TupClsCebsDbaItf

#硬件虚拟映射
from PkgL3cebsDhal.cebsConfig import *
from PkgL3cebsDhal.cebsDyndef import *
from PkgL3cebsDhal.ModDhCamera import *
from PkgL3cebsDhal.ModDhLogfile import *
from PkgL3cebsDhal.ModDhPicfile import *
from PkgL3cebsDhal.ModDhMotosps import *
from PkgL3cebsDhal.ModDhPlate import *


#正式服务API，给上层提供标准操作
class clsCebsDhalOprSvr(clsCebsDhCamera, clsCebsDhLogfile, clsCebsDhPicfile, clsCebsDhMotosps, clsCebsDhPlate):
    def __init__(self):
        super(clsCebsDhalOprSvr, self).__init__()  
    
    def tup_dhal_oprSvr_GetConfig(self):
        flag, res = TupClsCebsDbaItf.tup_hstDba_GetConfig(self, 'null', 'null')
        if (flag > 0):
            pass
            #save to local variable
        return flag, res






















    