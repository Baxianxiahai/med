'''
Created on 2019年1月3日

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
import datetime
import string
import ctypes 
import random
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math
from   ctypes import c_uint8

#自有的视频处理库函数
class TupClsPicProc(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

    #黑白图像腐蚀 #cv.imshow("erode",dst)
    def tup_erode(self, grayImg, size):
        #gray=cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        #ret, binary=cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        #获得结构元素
        #第一个参数：结构元素形状，这里是矩形
        #第二个参数：结构元素大小
        kernel=cv.getStructuringElement(cv.MORPH_RECT, (size, size))
        #执行腐蚀
        dst=cv.erode(grayImg, kernel)
        return dst
    
    #黑白图像膨胀
    def tup_dilate(self, grayImg, size):
        #gray=cv.cvtColor(img,cv.COLOR_RGB2GRAY)
        #ret, binary=cv.threshold(img, 0, 255,cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        #获得结构元素
        #第一个参数：结构元素形状，这里是矩形
        #第二个参数：结构元素大小
        kernel=cv.getStructuringElement(cv.MORPH_RECT, (size, size))
        #执行膨胀
        dst=cv.dilate(grayImg, kernel)
        return dst

    #彩色图像腐蚀
    def tup_color_erode(self, colorImg, size):
        gray=cv.cvtColor(colorImg, cv.COLOR_RGB2GRAY)
        ret, binary=cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        #获得结构元素
        #第一个参数：结构元素形状，这里是矩形
        #第二个参数：结构元素大小
        kernel=cv.getStructuringElement(cv.MORPH_RECT, (size, size))
        #执行腐蚀
        dst=cv.erode(binary, kernel)
        return dst
    
    #彩色图像膨胀
    def tup_color_dilate(self, colorImg, size):
        gray=cv.cvtColor(colorImg,cv.COLOR_RGB2GRAY)
        ret, binary=cv.threshold(gray, 0, 255,cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        #获得结构元素
        #第一个参数：结构元素形状，这里是矩形
        #第二个参数：结构元素大小
        kernel=cv.getStructuringElement(cv.MORPH_RECT, (size, size))
        #执行膨胀
        dst=cv.dilate(binary, kernel)
        return dst
    
    #
    # grayInputImg - 输入灰度图像
    # areaMin， areaMax - 面积判决门限
    # ceMin, ceMax - 椭圆度判决门限
    # areaTextFlag - 面积文字是否叠加
    # ceTextFlag - 椭圆度文字是否叠加
    #
    def tup_max_contours(self, grayInputImg, areaMin, areaMax, ceMin, ceMax, areaTextFlag, ceTextFlag):
        ret, binImg = cv.threshold(grayInputImg, 130, 255, cv.THRESH_BINARY)
        _, contours, hierarchy = cv.findContours(binImg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) #RETR_TREE, RETR_CCOMP
        outputImg = cv.cvtColor(binImg, cv.COLOR_GRAY2BGR)
        mask = np.zeros((grayInputImg.shape[0]+2, grayInputImg.shape[1]+2), np.uint8)
        mask[:] = 1
        #Analysis one by one: 分别分析
        for c in contours:
            M = cv.moments(c)
            cX = int(M["m10"] / (M["m00"]+0.01))
            cY = int(M["m01"] / (M["m00"]+0.01))
            cArea = cv.contourArea(c)
            rect = cv.minAreaRect(c)
            #width / height: 长宽,总有 width>=height  
            width, height = rect[1]
            if (width > height):
                cE = height / (width+0.001)
            else:
                cE = width / (height+0.001)
            cE = round(cE, 2)

            #分类
            if (cArea < areaMin) or (cArea > areaMax) or (cE < ceMin) or (cE > ceMax):
                pass
            else:
                cv.drawContours(outputImg, c, -1, (0,0,255), 2)
                if (areaTextFlag == True):
                    cv.putText(outputImg, str(cArea), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                if (ceTextFlag == True):
                    cv.putText(outputImg, str(cE), (cX + 20, cY + 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                return outputImg, rect
        return -1, -1
        











        