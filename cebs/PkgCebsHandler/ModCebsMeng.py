'''
Created on 2018年10月18日

@author: Administrator
'''

import random
import sys
import time
import json
import os
import re
import urllib
import http
import socket
import struct

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

#Local include
from cebsMain import *
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg




class clsL3_MengProc(object):
    '''
    classdocs
    '''
    def __init__(self, father):
        super(clsL3_MengProc, self).__init__()
        self.identity = None;
        self.instL4MengForm = father
        self.objInitCfg=ModCebsCfg.clsL1_ConfigOpr();
        #启动专属服务
        self.objMdcThd = ModCebsMoto.clsL1_MdcThd(self, 1);
        self.objMdcThd.setIdentity("TASK_MotoDrvCtrlThread"+str(self.instL4MengForm))
        self.objMdcThd.sgL4MainWinPrtLog.connect(self.funcDebugPrint)
        self.objMdcThd.start();

    def funcDebugPrint(self, myString):
        self.instL4MengForm.med_debug_print(myString)

    def funcGetSpsRights(self, par):
        self.objMdcThd.funcGetSpsRights(par);

    def funcRelSpsRights(self, par):
        self.objMdcThd.funcRelSpsRights(par);
    
    #命令生成    
    def funcSendCmd2Moto(self, cmdId, par1, par2, par3, par4):
        return self.objMdcThd.funcSendMengCmd(cmdId, par1, par2, par3, par4)
        
#         #self.funcDebugPrint("MPC: CmdId=%d, par1/2/3/4=%d/%d/%d/%d" %(cmdId, par1, par2, par3, par4))
#         #Build MODBUS COMMAND:系列化
#         fmt = ">BBiiii";
#         byteDataBuf = struct.pack(fmt, ModCebsCom.GLSPS_PAR_OFC.SPS_MENGPAR_ADDR, cmdId, par1, par2, par3, par4)
#         #print("0x%x - 0x%x" % (byteDataBuf[0], byteDataBuf[1]))
#         crc = self.objMdcThd.funcCacCrc(byteDataBuf, ModCebsCom.GLSPS_PAR_OFC.SPS_MENGPAR_CMD_LEN)
#         fmt = "<H";
#         byteCrc = struct.pack(fmt, crc)
#         byteDataBuf += byteCrc
#         #打印完整的BYTE系列
#         index=0
#         outBuf=''
#         while index < ModCebsCom.GLSPS_PAR_OFC.SPS_MENGPAR_CMD_LEN+2:
#             outBuf += str("%02X " % (byteDataBuf[index]))
#             index+=1
#         self.instL4MengForm.med_debug_print("L3MEP: SND CMD = " + outBuf)
#         res, Buf = self.objMdcThd.funcCmdSend(byteDataBuf)
#         if (res > 0):
#             return Buf
#         else:
#             return res




        