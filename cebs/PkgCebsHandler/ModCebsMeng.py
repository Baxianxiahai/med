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


MENGPAR_ADDR = 0x77
MENGPAR_CMD_LEN = 18

class clsL3_MengProc(object):
    '''
    classdocs
    '''
    def __init__(self, father):
        super(clsL3_MengProc, self).__init__()
        self.identity = None;
        self.instL4MengForm = father
        self.objInitCfg=ModCebsCfg.clsL1_ConfigOpr();

    def funcDebugPrint(self, myString):
        self.instL4MengForm.med_debug_print(myString)
    
    #命令生成    
    def funcSendCmd2Moto(self, cmdId, par1, par2, par3, par4):
        self.funcDebugPrint("MPC: CmdId=%d, par1/2/3/4=%d/%d/%d/%d" %(cmdId, par1, par2, par3, par4))
        #Build MODBUS COMMAND:系列化
        fmt = ">BBiiii";
        byteDataBuf = struct.pack(fmt, MENGPAR_ADDR, cmdId, par1, par2, par3, par4)
        print("0x%x - 0x%x" % (byteDataBuf[0], byteDataBuf[1]))
        crc = self.funcCacCrc(byteDataBuf, MENGPAR_CMD_LEN)
        fmt = "<H";
        byteCrc = struct.pack(fmt, crc)
        byteDataBuf += byteCrc
        #打印完整的BYTE系列
        index=0
        outBuf=''
        while index < MENGPAR_CMD_LEN+2:
            outBuf += str("%X " % (byteDataBuf[index]))
            index+=1
        self.instL4MengForm.med_debug_print("MENGPAR: SND CMD = " + outBuf)
        
    def funcCacCrc(self, buf, length):
        wCRC = 0xFFFF;
        index=0
        while index < length:
            wCRCOut = self.funcCrcOneChar(buf[index], wCRC)
            wCRC = wCRCOut
            index += 1
        wHi = wCRC // 256;
        wLo = wCRC % 256;
        wCRC = (wHi << 8) | wLo;
        return wCRC;

    def funcCrcOneChar(self, cDataIn, wCRCIn):
        wCheck = 0;
        wCRCIn = wCRCIn ^ cDataIn;
        i=0;
        while i<8:
            wCheck = wCRCIn & 1;
            wCRCIn = wCRCIn >> 1;
            wCRCIn = wCRCIn & 0x7fff;
            if (wCheck == 1):
                wCRCIn = wCRCIn ^ 0xa001;
            wCRCIn = wCRCIn & 0xffff;
            i += 1
        return wCRCIn;






        