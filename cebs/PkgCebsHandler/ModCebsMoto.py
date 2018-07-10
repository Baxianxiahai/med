'''
Created on 2018楠烇拷5閺堬拷8閺冿拷

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

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

#Local include
from cebsMain import *
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg
from PkgCebsHandler import ModCebsMotorApi

#缁撅箑鐣剧粔璇插З閻ㄥ嫬鐡熼弶澶哥秴缂冾喕濞囬悽顭掔窗 0 =閵嗭拷 鐞涖劎銇氭径宥勭秴娴ｅ秶鐤�
#               1-96 =閵嗗顒滅敮鍝ユ畱閺夊灝鐡熸担宥囩枂
class classMotoProcess(object):
    ObjMotorApi = ModCebsMotorApi.MotorClass()
    
    def __init__(self):
        #閸忓牐顓哥粻妤�鐔�绾拷闁劌鍨�
        #ObjMotorApi = ModCebsMotorApi.MotorClass()
        if (ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE == 0 or ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE == 0 or ModCebsCom.GL_CEBS_HB_HOLE_X_NUM == 0 or ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM == 0):
            if (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_96_STANDARD):
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 12;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 8;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
            elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_48_STANDARD):
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 8;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 6;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
            elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_32_STANDARD):
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 8;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 4;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_32_SD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_32_SD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
            elif (ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_12_STANDARD):
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 4;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 3;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
            else:
                ModCebsCom.GL_CEBS_HB_HOLE_X_NUM = 12;
                ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM = 8;
                ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_BOARD_X_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
                ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = ModCebsCom.GL_CEBS_HB_TARGET_BOARD_Y_MAX / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
        #閸愬秷锟藉啳妾婚惇鐔风杽閹懎鍠屾稉瀣畱鐟曞棛娲�
        #閻喐顒滈惃鍕墡閸戝棗婀弽鈥冲櫙鏉╁洨鈻兼稉顓＄箻鐞涘本娲块弬锟�
        if (ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] !=0 or ModCebsCom.GL_CEBS_HB_POS_IN_UM[3] !=0):
            xWidth = ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[0];
            yHeight = ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[3];
            ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE = xWidth / (ModCebsCom.GL_CEBS_HB_HOLE_X_NUM-1);
            ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE = yHeight / (ModCebsCom.GL_CEBS_HB_HOLE_Y_NUM-1);
        else:
            pass
         
    def funcMotoCalaMoveOneStep(self, scale, dir):
        if (scale == 1):
            actualScale = 500;
        elif (scale == 2):
            actualScale = 1000;
        elif (scale == 3):
            actualScale = 5000;
        elif (scale == 4):
            actualScale = 10000;
        elif (scale == 5):
            actualScale = 50000;
        else:
            actualScale = 0;
        Old_Px = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] 
        Old_Py = ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]
        if (dir == 1):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] += actualScale;
            if ((ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_96_STANDARD) and (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] > ModCebsCom.GL_CEBS_HB_TARGET_96_SD_Y_MAX)):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_Y_MAX;
            elif ((ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_48_STANDARD) and (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] > ModCebsCom.GL_CEBS_HB_TARGET_48_SD_Y_MAX)):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_Y_MAX;
            elif ((ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_32_STANDARD) and (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] > ModCebsCom.GL_CEBS_HB_TARGET_32_SD_Y_MAX)):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] = ModCebsCom.GL_CEBS_HB_TARGET_32_SD_Y_MAX;
            elif ((ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_12_STANDARD) and (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] > ModCebsCom.GL_CEBS_HB_TARGET_12_SD_Y_MAX)):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_Y_MAX;
            elif (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] > ModCebsCom.GL_CEBS_HB_TARGET_BOARD_Y_MAX):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] = ModCebsCom.GL_CEBS_HB_TARGET_BOARD_Y_MAX;
            else:
                pass
        elif (dir == 2):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] -= actualScale;
            if (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] < 0):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] = 0;
        elif (dir == 3):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] -= actualScale;
            if (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] < 0):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] = 0;
        elif (dir == 4):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] += actualScale;
            if ((ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_96_STANDARD) and (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] > ModCebsCom.GL_CEBS_HB_TARGET_96_SD_X_MAX)):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] = ModCebsCom.GL_CEBS_HB_TARGET_96_SD_X_MAX;
            elif ((ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_48_STANDARD) and (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] > ModCebsCom.GL_CEBS_HB_TARGET_48_SD_X_MAX)):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] = ModCebsCom.GL_CEBS_HB_TARGET_48_SD_X_MAX;
            elif ((ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_32_STANDARD) and (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] > ModCebsCom.GL_CEBS_HB_TARGET_32_SD_X_MAX)):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] = ModCebsCom.GL_CEBS_HB_TARGET_32_SD_X_MAX;
            elif ((ModCebsCom.GL_CEBS_HB_TARGET_TYPE == ModCebsCom.GL_CEBS_HB_TARGET_12_STANDARD) and (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] > ModCebsCom.GL_CEBS_HB_TARGET_12_SD_X_MAX)):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] = ModCebsCom.GL_CEBS_HB_TARGET_12_SD_X_MAX;
            elif (ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] > ModCebsCom.GL_CEBS_HB_TARGET_BOARD_X_MAX):
                ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] = ModCebsCom.GL_CEBS_HB_TARGET_BOARD_X_MAX;
            else:
                pass
        else:
            pass
        print("MOTO: Moving one step! Scale=%d, Dir=%d. Old pos X/Y=%d/%d, New pos X/Y=%d/%d" % (scale, dir, Old_Px, Old_Py, ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]));
        if (self.funcMotoMove2AxisPos(Old_Px, Old_Py, ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1]) > 0):
            return 1;
        else:
            return -2;
        return 1;
    
    def funcMotoBackZero(self):
        return self.funcMotoMove2HoleNbr(0);
        #print("MOTO: Running Zero Position!")

    def funcMotoMove2Start(self):
        print("MOTO: Move to start!")
        #濞夈劍鍓伴敍姘箯娑撳﹦娈慩鏉炲瓨娓剁亸蹇嬶拷涔婇張锟芥径褋锟藉倸褰告稉瀣畱X閺堬拷婢堆嶇礉閼板鐏忥拷
        xWidth = ModCebsCom.GL_CEBS_HB_POS_IN_UM[2] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[0];
        yHeight = ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] - ModCebsCom.GL_CEBS_HB_POS_IN_UM[3];
        if (xWidth <= 0 or yHeight <= 0):
            print("MOTO: Error set of calibration, xWidth/yHeight=%d/%d!" %(xWidth, yHeight))
            return -1;
        return self.funcMotoMove2HoleNbr(1);
        #print("MOTO: Running Start Position!")

    #閺嗗倹妞傛稉宥夋付鐟曚胶娈戞潻鍥┾柤
    def funcMotoStop(self):
        #print("MOTO: Stop!")
        print("MOTO: funcMotoStop")
        self.ObjMotorApi.moto_proc_full_stop()
        return 1;
    
    #閺嗗倹妞傛稉宥夋付鐟曚胶娈戞潻鍥┾柤
    def funcMotoResume(self):
        print("MOTO: Resume action!")
        return 1;
    
    def funcMotoMove2HoleNbr(self, holeIndex):
        time.sleep(1)
        #鐠侊紕鐣婚弬鎵畱閻╊喗鐖ｆ担宥囩枂
        if (holeIndex == 0):
            xTargetHoleNbr = 0;
            yTargetHoleNbr = 0;
            newPosX = 0;
            newPosY = 0;
        else:
            #鐞涘矉绱�1-12閿涳拷, 閸掓绱�1-8閿涳拷
            xTargetHoleNbr = ((holeIndex-1) % ModCebsCom.GL_CEBS_HB_HOLE_X_NUM) + 1;
            yTargetHoleNbr = ((holeIndex-1) // ModCebsCom.GL_CEBS_HB_HOLE_X_NUM) + 1;
            newPosX = int(ModCebsCom.GL_CEBS_HB_POS_IN_UM[0] + (xTargetHoleNbr-1)*ModCebsCom.GL_CEBS_HB_WIDTH_X_SCALE);
            newPosY = int(ModCebsCom.GL_CEBS_HB_POS_IN_UM[1] - (yTargetHoleNbr-1)*ModCebsCom.GL_CEBS_HB_HEIGHT_Y_SCALE);
        print("MOTO: Moving to working hole=%d, newPosX/Y=%d/%d." % (holeIndex, newPosX, newPosY))
        #閻喎鐤勭粔璇插З鏉╁洨鈻�
        if (self.funcMotoMove2AxisPos(ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0], ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1], newPosX, newPosY) > 0):
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[0] = newPosX;
            ModCebsCom.GL_CEBS_CUR_POS_IN_UM[1] = newPosY;
            return 1;
        else:
            return -2;
        print("MOTO: Finished once!")

    #娴犲骸缍嬮崜宥勭娑擃亜娼楅弽鍥┬╅崝銊ュ煂閸欙缚绔存稉顏呮煀閸ф劖鐖�
    #闂囷拷鐟曚礁鐨㈤崸鎰垼鏉烆剚宕叉稉楦垮墻閸愬弶鏆�
    def funcMotoMove2AxisPos(self, curPx, curPy, newPx, newPy):
        print("MOTO: funcMotoMove2AxisPos", curPx, curPy, newPx, newPy)
        self.ObjMotorApi.moto_proc_move_to_axis_postion(curPx, curPy, newPx, newPy)
        return 1;
        