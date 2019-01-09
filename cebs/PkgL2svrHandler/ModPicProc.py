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
        #执行中值滤波，模糊一点，去噪声
        dst1=cv.erode(grayImg, kernel)
        dst2= cv.medianBlur(dst1, 5)
        return dst2
    
    #黑白图像膨胀
    def tup_dilate(self, grayImg, size):
        #gray=cv.cvtColor(img,cv.COLOR_RGB2GRAY)
        #ret, binary=cv.threshold(img, 0, 255,cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        #获得结构元素
        #第一个参数：结构元素形状，这里是矩形
        #第二个参数：结构元素大小
        kernel=cv.getStructuringElement(cv.MORPH_RECT, (size, size))
        #执行膨胀
        dst1=cv.dilate(grayImg, kernel)
        dst2= cv.medianBlur(dst1, 5)
        return dst2

    #彩色图像腐蚀
    def tup_color_erode(self, colorImg, size):
        gray=cv.cvtColor(colorImg, cv.COLOR_RGB2GRAY)
        ret, binary=cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        #获得结构元素
        #第一个参数：结构元素形状，这里是矩形
        #第二个参数：结构元素大小
        kernel=cv.getStructuringElement(cv.MORPH_RECT, (size, size))
        #执行腐蚀
        dst1=cv.erode(binary, kernel)
        dst2= cv.medianBlur(dst1, 5)
        return dst2
    
    #彩色图像膨胀
    def tup_color_dilate(self, colorImg, size):
        gray=cv.cvtColor(colorImg,cv.COLOR_RGB2GRAY)
        ret, binary=cv.threshold(gray, 0, 255,cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        #获得结构元素
        #第一个参数：结构元素形状，这里是矩形
        #第二个参数：结构元素大小
        kernel=cv.getStructuringElement(cv.MORPH_RECT, (size, size))
        #执行膨胀
        dst1=cv.dilate(binary, kernel)
        dst2= cv.medianBlur(dst1, 5)
        return dst2

    #Gray transaction: 灰度化
    def tup_color2gray_adaptive(self, colorImg, size):
        new = np.zeros(colorImg.shape, np.uint8)
        for i in range(new.shape[0]):  #Axis-y/height/Rows
            for j in range(new.shape[1]):
                (b,g,r) = colorImg[i,j]
                #加权平均法
                new[i,j] = int(0.3*float(b) + 0.59*float(g) + 0.11*float(r))&0xFF
        #Middle value filter: 中值滤波
        blur= cv.medianBlur(new, 5)
        midGray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
        #Adaptive bin-translation: 自适应二值化
        # ADAPTIVE_THRESH_MEAN_C ADAPTIVE_THRESH_GAUSSIAN_C
        binGray = cv.adaptiveThreshold(midGray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, size, 0)
        #medianBlur
        binRes= cv.GaussianBlur(binGray, (5,5), 1.5) 
        return binRes
    
    
    '''
    #
    # Input:
    # grayInputImg - 输入灰度图像
    # areaMin， areaMax - 面积判决门限
    # ceMin, ceMax - 椭圆度判决门限
    # areaTextFlag - 面积文字是否叠加
    # ceTextFlag - 椭圆度文字是否叠加
    # 
    # Output:
    # outputImg - 图像
    # rect - 找到的最小外接矩阵
    # totalCnt - 总共数量
    # findCnt - 满足条件数量
    # outCt - 外部凸点集合，外包络图
    # outBox - 外接矩形
    #
    '''
    def tup_find_contours(self, grayInputImg, areaMin, areaMax, ceMin, ceMax, areaTextFlag, ceTextFlag):
        ret, binImg = cv.threshold(grayInputImg, 130, 255, cv.THRESH_BINARY)
        _, contours, hierarchy = cv.findContours(binImg, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) #RETR_TREE, RETR_CCOMP
        outputImg = cv.cvtColor(binImg, cv.COLOR_GRAY2BGR)
        #Analysis one by one: 分别分析
        totalCnt=0
        findCnt=0
        outCt=''
        outBox=''
        outRect=''
        for c in contours:
            totalCnt += 1
            M = cv.moments(c)
            cX = int(M["m10"] / (M["m00"]+0.01))
            cY = int(M["m01"] / (M["m00"]+0.01))
            cArea = cv.contourArea(c)
            rect = cv.minAreaRect(c)
            box = cv.boxPoints(rect)
            box =np.int0(box)  #将其转化为整数
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
                outCt = c
                outBox = box
                outRect = rect
                findCnt += 1
                cv.drawContours(outputImg, c, -1, (0,0,255), 2)
                #cv.drawContours(outputImg, [box], 0, (0,0,255), 2)
                if (areaTextFlag == True):
                    cv.putText(outputImg, str(cArea), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                if (ceTextFlag == True):
                    cv.putText(outputImg, str(cE), (cX + 20, cY + 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        if findCnt>0:
            #print("Internal Rect = ", outRect)
            #print("Internal Box = ", outBox)
            return outputImg, outRect, totalCnt, findCnt, outCt, outBox
        else:
            return -1, -1, 0, 0, 0, 0

    #用于掩模
    def tup_find_max_contours(self, grayInputImg, areaMin, areaMax, ceMin, ceMax, areaTextFlag, ceTextFlag):
        ret, binImg = cv.threshold(grayInputImg, 130, 255, cv.THRESH_BINARY)
        _, contours, hierarchy = cv.findContours(binImg, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) #RETR_TREE, RETR_CCOMP CHAIN_APPROX_SIMPLE  CHAIN_APPROX_NONE
        outputImg = cv.cvtColor(binImg, cv.COLOR_GRAY2BGR)
        #Analysis one by one: 分别分析
        totalCnt=0
        findCnt=0
        outCt=''
        outBox=''
        outRect=''
        maxArea=0
        for c in contours:
            totalCnt += 1
            M = cv.moments(c)
            cX = int(M["m10"] / (M["m00"]+0.01))
            cY = int(M["m01"] / (M["m00"]+0.01))
            cArea = cv.contourArea(c)
            rect = cv.minAreaRect(c)
            box = cv.boxPoints(rect)
            box =np.int0(box)  #将其转化为整数
            #width / height: 长宽,总有 width>=height  
            width, height = rect[1]
            if (width > height):
                cE = height / (width+0.001)
            else:
                cE = width / (height+0.001)
            cE = round(cE, 2)

            #分类
            if (cArea < areaMin) or (cArea > areaMax) or (cE < ceMin) or (cE > ceMax) or (cArea <= maxArea):
                pass
            else:
                maxArea = cArea
                outCt = c
                outBox = box
                outRect = rect
                findCnt = 1
                cv.drawContours(outputImg, c, -1, (0, 0, 255), 1)
                #cv.drawContours(outputImg, [box], 0, (0,0,255), 2)
                if (areaTextFlag == True):
                    cv.putText(outputImg, str(cArea), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                if (ceTextFlag == True):
                    cv.putText(outputImg, str(cE), (cX + 20, cY + 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        if findCnt>0:
            #print("Internal Rect = ", outRect)
            #print("Internal Box = ", outBox)
            return outputImg, outRect, totalCnt, findCnt, outCt, outBox
        else:
            return -1, -1, 0, 0, 0, 0
        
    #将图像inImg中的box部分截取出来
    def tup_copy_box_img(self, inImg, box):
        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x1 = min(Xs)
        x2 = max(Xs)
        y1 = min(Ys)
        y2 = max(Ys)
        height = y2 - y1
        width = x2 - x1
        print(width, height)
        outImg = np.zeros(inImg.shape, np.uint8)
        for j in range(y1, y1+height):
            for i in range(x1, x1+width):
                outImg[j, i] = inImg[j, i]
        return outImg
    
    '''
    #
    #灰度去燥外框综合算法
    #
    # INPUT=================
    # colImg - 彩色图像
    # dilateBlkSize - 膨胀系数
    # erodeBlkSize - 腐蚀系数
    # areaMin - 最小面积门限
    # areaMax - 最大面积门限
    # ceMin - 最小圆形度门限
    # ceMax - 最大圆形度门限
    # ceMax - 最大圆形度门限
    # areaTextFlag - 面积文字叠加标签
    # ceTextFlag - 圆形度叠加标签
    #
    # OUTPUT=================
    # outputImg - 图像
    # rect - 找到的最小外接矩阵
    # totalCnt - 总共数量
    # findCnt - 满足条件数量
    # outCt - 外部凸点集合，外包络图
    # outBox - 外接矩形    #
    '''
    def tup_contours_itp(self, colImg, dilateBlkSize, erodeBlkSize, areaMin, areaMax, ceMin, ceMax, areaTextFlag, ceTextFlag):
        #第1步：灰度图像
        grayImg = self.tup_color2gray_adaptive(colImg, dilateBlkSize)
        #第2步，去噪声
        nfImg = self.tup_erode(grayImg, erodeBlkSize)
        #第3步，寻找外框
        outputImg, rect, totalCnt, findCnt, outCt, outBox = self.tup_find_contours(nfImg, areaMin, areaMax, ceMin, ceMax, areaTextFlag, ceTextFlag)
        return outputImg, rect, totalCnt, findCnt, outCt, outBox

    def tup_max_contours_itp(self, colImg, dilateBlkSize, erodeBlkSize, areaMin, areaMax, ceMin, ceMax, areaTextFlag, ceTextFlag):
        #第1步：灰度图像
        grayImg = self.tup_color2gray_adaptive(colImg, dilateBlkSize)
        #第2步，去噪声
        nfImg = self.tup_erode(grayImg, erodeBlkSize)
        #第3步，寻找外框
        outputImg, rect, totalCnt, findCnt, outCt, outBox = self.tup_find_max_contours(nfImg, areaMin, areaMax, ceMin, ceMax, areaTextFlag, ceTextFlag)
        return outputImg, rect, totalCnt, findCnt, outCt, outBox
    
    
    #通过圆形寻找边界
    def tup_cal_xy_line(self, radCent, angle, outRect):
        x0 = radCent[0]
        y0 = radCent[1]
        (height, width) = outRect
        #竖线
        if (angle == 90) or (angle == -90):
            x1, y1 = x0, 0
            x2, y2 = x0, height
            return ((int(x1), int(y1)), (int(x2), int(y2)))
        #横线
        k = math.tan(angle/180.0*math.pi)
        if k==0:
            x1, y1 = 0, y0
            x2, y2 = width, y0
            return ((int(x1), int(y1)), (int(x2), int(y2)))
        #y = y0+k*(x-x0)
        x1 = 0
        y1 = y0+k*(x1-x0)
        if (y1 < 0):
            y1 = 0
            x1 = x0+(y1-y0)/k
        if (y1 > height):
            y1 = height
            x1 = x0+(y1-y0)/k
        x2=width
        y2 = y0+k*(x2-x0)
        if (y2 < 0):
            y2 = 0
            x2 = x0+(y2-y0)/k
        if (y2 > height):
            y2 = height
            x2 = x0+(y2-y0)/k
        return ((int(x1), int(y1)), (int(x2), int(y2)))
    
    #切掉右边图像
    #图像直接拷贝是不合适的，需要使用imgIn.copy()函数才靠谱
    def tup_cut_left_img(self, imgIn, radCent, angle):
        imgRight = imgIn.copy()
        sp = imgIn.shape
        #竖线
        if (angle == 90) or (angle == -90):
            for j in range(0, sp[1]):
                x = radCent[0]
                for i in range(0, int(x)):
                    imgRight[j, i] = (0, 0, 0)
            return imgRight
        k = math.tan(angle/180.0*math.pi)
        #横线
        if (k==0):
            return imgRight
        #正常线
        for j in range(0, sp[0]):
            x = radCent[0] + (j-radCent[1])/k
            right = int(x)+1
            if (right >= sp[1]):
                right = sp[1]
            for i in range(0, right):
                imgRight[j, i] = (0, 0, 0)
        return imgRight

    #使用outCt，将一副图像抽取出来
    def tup_cut_out_contour_img(self, imgIn, outCt):
        return imgIn




        