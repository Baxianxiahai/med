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
    #RGB颜色数组定义
    _COL_A_RED = [255, 0, 0]
    _COL_A_GREEN = [0, 255, 0]
    _COL_A_BLUE = [0, 0, 255]
    _COL_A_BLACK = [0, 0, 0]
    _COL_A_WITHE = [255, 255, 255]
    _COL_A_CHING = [0, 255, 255]
    _COL_A_YELLOW = [255, 255, 0]
    _COL_A_DEEPRED = [255, 0, 255]
    
    #BGR颜色字典定义
    _COL_D_RED = (0, 0, 255)
    _COL_D_GREEN = (0, 255, 0)
    _COL_D_BLUE = (255, 0, 0)
    _COL_D_BLACK = (0, 0, 0)
    _COL_D_WHITE = (255, 255, 255)
    _COL_D_CHING = (255, 255, 0)
    _COL_D_YELLOW = (0, 255, 255)
    _COL_D_DEEPRED = (255, 0, 255)

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
                cv.drawContours(outputImg, c, -1, self._COL_D_RED, 2)
                #cv.drawContours(outputImg, [box], 0, self._COL_D_RED, 2)
                if (areaTextFlag == True):
                    cv.putText(outputImg, str(cArea), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, self._COL_D_GREEN, 1)
                if (ceTextFlag == True):
                    cv.putText(outputImg, str(cE), (cX + 20, cY + 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, self._COL_D_BLUE, 1)
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
                cv.drawContours(outputImg, c, -1, self._COL_D_RED, 1)
                #cv.drawContours(outputImg, [box], 0, self._COL_D_RED, 2)
                if (areaTextFlag == True):
                    cv.putText(outputImg, str(cArea), (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, self._COL_D_GREEN, 1)
                if (ceTextFlag == True):
                    cv.putText(outputImg, str(cE), (cX + 20, cY + 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, self._COL_D_BLUE, 1)
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
        outImg = np.zeros(inImg.shape, np.uint8)
        for j in range(y1, y1+height):
            for i in range(x1, x1+width):
                outImg[j, i] = inImg[j, i]
        return outImg
    
    #将图像inImg中的box部分截取出来
    #fillPoly使用了255系数，这个对应到RED的颜色ARRAY，实际上在颜色上是BLUE。在对照时，又需要改回到RED进行判定
    #BLUE是缺省的抠图颜色体系，这是本函数规定的，人眼最不敏感的，故而是惯例吧吧
    def tup_copy_contour_img(self, inImg, contour):
        outCt2 = cv.convexHull(contour)
        tmpImg = inImg.copy()
        outImg = inImg.copy()
        cv.fillPoly(tmpImg, [outCt2], 255)
        sp = inImg.shape
        height, width = sp[0], sp[1]
        for j in range(0, height):
            for i in range(0, width):
                if (tmpImg[j, i][0] == self._COL_A_RED[0]) and (tmpImg[j, i][1] == self._COL_A_RED[1]) and (tmpImg[j, i][2] == self._COL_A_RED[2]):
                    outImg[j, i] = inImg[j, i]
                else:
                    outImg[j, i] = [0, 0, 0]
        return outImg
    
    
    '''
    #
    #图像形态学处理综合算法
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
    def tup_itp_morphology_transform(self, colImg, dilateBlkSize, erodeBlkSize, areaMin, areaMax, ceMin, ceMax, areaTextFlag, ceTextFlag):
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
    

    '''
    #通过外接最小长方形，寻找过中心点的长轴直线，该直线需要顶到图像的两端，将图像一分为二
    #通过这个方式，可以将图像的左手或者右手部分切分出来
    #
    #radCent - 中心坐标
    #angle - 角度
    #imgHgWd - 图像尺寸
    #输出：起点和重点坐标
    '''
    def tup_cal_rect_line(self, radCent, angle, imgHgWd):
        x0, y0 = radCent[0], radCent[1]
        (height, width) = imgHgWd
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
    
    
    '''
    #
    #
    #通过拟合函数，得到一个图像或者轮廓的长轴直线，该直线顶到图像的边界
    #该函数的目标也是为了下一步将图像进行切分
    #
    #inImg - 彩色图像
    #contour - 轮廓
    #输出：起点和重点坐标
    #
    #这个方式在应用上，更加泛化一些
    #
    '''
    def tup_siml_line_by_contour(self, inImg, contour):
        height, width = inImg.shape[:2]
        [vx, vy, x, y] = cv.fitLine(contour, cv.DIST_L2, 0, 0.01, 0.01)
        if vx == 0:
            k = vy / 0.001
        else:
            k = vy/vx
        x0, y0 = x, y
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
    
    
    '''
    #
    #保留右边或者左边的图像：需要根据角度进行合理判定
    #这个函数，左右手系的选择，这里已经做了
    #如果在实际应用的时候，角度不同时均为右手系，则不用分双边判定
    #
    #图像直接拷贝是不合适的，需要使用imgIn.copy()函数才靠谱
    #
    '''
    def tup_cut_line_out_img(self, imgIn, radCent, angle):
        imgLeft = imgIn.copy()
        imgRight = imgIn.copy()
        sp = imgIn.shape
        #特殊竖线
        if (angle == 90) or (angle == -90):
            for i in range(0, sp[0]):
                x = radCent[0]
                right = int(x)+1
                if (right >= sp[1]):
                    right = sp[1]
                for j in range(right, sp[1]):
                    imgLeft[i, j] = self._COL_D_BLACK
            for i in range(0, sp[0]):
                x = radCent[0]
                right = int(x)+1
                if (right >= sp[1]):
                    right = sp[1]
                for j in range(0, right):
                    imgRight[i, j] = self._COL_D_BLACK
            if (angle > 0):
                imgRem = imgLeft
            else:
                imgRem = imgRight
            return imgRem
        #正常处理
        k = math.tan(angle/180.0*math.pi)
        #横线
        if (k==0):
            return imgLeft, imgRight
        #正常线
        for i in range(0, sp[0]):
            x = radCent[0] + (i-radCent[1])/k
            right = int(x)+1
            if (right >= sp[1]):
                right = sp[1]
            for j in range(right, sp[1]):
                imgLeft[i, j] = self._COL_D_BLACK
        for i in range(0, sp[0]):
            x = radCent[0] + (i-radCent[1])/k
            right = int(x)+1
            if (right >= sp[1]):
                right = sp[1]
            for j in range(0, right):
                imgRight[i, j] = self._COL_D_BLACK
        if (angle > 0):
            imgRem = imgLeft
        else:
            imgRem = imgRight
        return imgRem

    #基于一个最小外接长方形，求左手系和右手系的正方形定点
    #同上，需要分左右手系
    def tup_find_retg_area(self, imgIn, minRectIn):
        angle = minRectIn[2]
        tpList = np.array([[0,0],[0,0],[0,0],[0,0],[0,0]], np.int32)
        sin = math.sin(angle/180.0*math.pi)
        cos = math.cos(angle/180.0*math.pi)
        sp = imgIn.shape
        (imgH, imgW) = (sp[0], sp[1])
        (mrW, mrH) = minRectIn[1]
        (x0, y0) = minRectIn[0]
        leftPx = x0 - cos*mrW/2
        leftPy = y0 - sin*mrW/2
        rightPx = x0 + cos*mrW/2
        rightPy = y0 + sin*mrW/2
        if (leftPx<0): leftPx=0;
        if (leftPx>=imgW): leftPx=imgW-1;
        if (leftPy<0): leftPy=0;
        if (leftPy>=imgH): leftPy=imgH-1;
        if (rightPx<0): rightPx=0;
        if (rightPx>=imgW): rightPx=imgW-1;
        if (rightPy<0): rightPy=0;
        if (rightPy>=imgH): rightPy=imgH-1;
        #4nd point
        if (minRectIn[2] > 0):
            angle -= 90
        else:
            angle += 90
        sin = math.sin(angle/180.0*math.pi)
        cos = math.cos(angle/180.0*math.pi)
        (x0, y0) = (rightPx, rightPy)
        r4Px = x0 + cos*mrW
        r4Py = y0 + sin*mrW
        if (r4Px<0): r4Px=0;
        if (r4Px>=imgW): r4Px=imgW-1;
        if (r4Py<0): r4Py=0;
        if (r4Py>=imgH): r4Py=imgH-1;
        #5nd point
        if (minRectIn[2] > 0):
            angle -= 90
        else:
            angle += 90
        sin = math.sin(angle/180.0*math.pi)
        cos = math.cos(angle/180.0*math.pi)
        (x0, y0) = (r4Px, r4Py)
        r5Px = x0 + cos*mrW
        r5Py = y0 + sin*mrW
        if (r5Px<0): r5Px=0;
        if (r5Px>=imgW): r5Px=imgW-1;
        if (r5Py<0): r5Py=0;
        if (r5Py>=imgH): r5Py=imgH-1;
        #Return
        if (minRectIn[2] > 0):
            tpList[1] = [int(rightPx), int(rightPy)]
            tpList[1] = [int(minRectIn[0][0]), int(minRectIn[0][1])]
            tpList[2] = [int(leftPx), int(leftPy)]
            tpList[3] = [int(r4Px), int(r4Py)]
            tpList[4] = [int(r5Px), int(r5Py)]
        else:
            tpList[0] = [int(leftPx), int(leftPy)]
            tpList[1] = [int(minRectIn[0][0]), int(minRectIn[0][1])]
            tpList[2] = [int(rightPx), int(rightPy)]
            tpList[3] = [int(r4Px), int(r4Py)]
            tpList[4] = [int(r5Px), int(r5Py)]
        return tpList
    

    #霍夫变换求圆形算法
    #圆形切割，寻找圆形图像
    #imgIn - 输入图像，彩色
    #minRad - 最小半径
    #maxRad - 最大半径
    #minDist - 圆形之间的距离
    #OUTOUT-圆形数值
    def tup_find_circle_area(self, imgIn, minRad, maxRad, minDist):
        grayImg = cv.cvtColor(imgIn, cv.COLOR_BGR2GRAY)
        blurImg = cv.medianBlur(grayImg, 3)
        #bgrImg = cv.cvtColor(blurImg, cv.COLOR_GRAY2BGR)  #变换回去，这里不需要
        circles = cv.HoughCircles(blurImg, cv.HOUGH_GRADIENT, 1.5, minDist, param1=100, param2=10, minRadius=minRad, maxRadius=maxRad)
        findCnt = 0
        try:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                findCnt+=1
                #cv.circle(imgIn,(i[0], i[1]), i[2], self._COL_D_RED, 2)
        except Exception:
            pass
        return findCnt, circles

    #霍夫变换方法集成使用
    #参数取值范围保护
    def tup_itp_hough_transform(self, imgIn, minRad, maxRad, minDist):
        if (minDist<=0):
            minDist=1
        if (minRad<=0):
            minRad=1
        if (maxRad<=1):
            maxRad=2
        if (maxRad < minRad):
            maxRad = minRad
        findCnt, circles = self.tup_find_circle_area(imgIn, minRad, maxRad, minDist)
        if (findCnt == 0):
            return -1, -1
        outImg = imgIn.copy()
        for i in circles[0, :]:
            cv.circle(outImg,(i[0], i[1]), i[2], self._COL_D_RED, 1)
        return outImg, findCnt, circles
    
    #通用显示照片方法
    def tup_img_show(self, imgIn, title):
        winapi = ctypes.windll.user32
        height = winapi.GetSystemMetrics(1)
        width = winapi.GetSystemMetrics(0)
        print("Width/Height=", width, height)
        sp = imgIn.shape
        coef1 = math.ceil(height/sp[0])
        coef2 = math.ceil(width/sp[1])
        if (coef1>coef2):
            coef = coef1
        else:
            coef = coef2
        cv.namedWindow(title, cv.WINDOW_NORMAL)
        cv.resizeWindow(title, sp[0]//coef, sp[1]//coef)
        cv.imshow(title, imgIn)
        cv.waitKey()


























    
    
        




        