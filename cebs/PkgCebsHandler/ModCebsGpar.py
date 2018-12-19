'''
Created on 2018/7/21

@author: Administrator
'''

####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-

import random
import sys
import time
import json
import os
import re
import urllib
import http
import socket
#import cv2 as cv

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

#Local include
from cebsL4Ui import *
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg
from PkgVmHandler.ModVmCfg import TUP_MSGID_TRACE, TUP_TASK_ID_UI_GPAR


class clsL3_GparProc(object):
    def __init__(self, father):
        super(clsL3_GparProc, self).__init__()
        self.identity = None;
        self.instL4GparForm = father
        self.objInitCfg=ModCebsCfg.clsL1_ConfigOpr();
        rect = self.instL4GparForm.label_gpar_pic_origin_fill.geometry()
        self.orgPicWidth = rect.width()
        self.orgPicHeight = rect.height()
        rect = self.instL4GparForm.label_gpar_pic_cfy_fill.geometry()
        self.cfyPicWidth = rect.width()
        self.cfyPicHeight = rect.height()
        self.picDirFile = ''

    def funcCtrlSchdDebugPrint(self, myString):
        self.instL4GparForm.med_debug_print(myString)
                
    #Do nothting
    def funcRecoverWorkingEnv(self):
        pass
    
    #Load file
    def funcPicFileLoad(self, dirFn):
        self.picDirFile = dirFn
        print("input file name = ", dirFn)
        img = QtGui.QPixmap(dirFn)
        img=img.scaled(self.orgPicWidth,self.orgPicHeight)
        self.instL4GparForm.label_gpar_pic_origin_fill.setPixmap(img)
        self.funcCtrlSchdDebugPrint("GPAR: Load once!")
        
    #Train files
    def funcPicFileTrain(self):
        if (self.picDirFile == ''):
            return -1
        obj = ModCebsVision.clsL2_VisCfyProc(self.instL4GparForm)
        obj.funcVisionNormalClassifyDirect(self.picDirFile, 'tempPic.jpg')
        if (os.path.exists('tempPic.jpg') == False):
            return -2
        img = QtGui.QPixmap('tempPic.jpg')
        img=img.scaled(self.cfyPicWidth,self.cfyPicHeight)
        self.instL4GparForm.label_gpar_pic_cfy_fill.setPixmap(img)
        self.funcCtrlSchdDebugPrint("GPAR: Train done once!")
        
        
















