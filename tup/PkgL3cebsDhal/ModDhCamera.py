'''
Created on 2019年6月4日

@author: Administrator
'''

from PkgL3cebsDhal.cebsConfig import *
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


class clsCebsDhCamera():
    '''
    #
    #全局所能支持摄像头的类型
    #为了简化COM模块的设计，所支持的摄像头描述符并不放在COM模块中，而是直接放在这个模块中
    #
    # OBVIOUS_UCMOS10000KPA - 白光拍摄
    # OBVIOUS_E3ISPM05000KPA - 高端荧光拍摄
    #
    # :
    ###########################DEFAULT device as following########################################################################
        \\ZJLPC\root\cimv2:Win32_PnPEntity.DeviceID="IUSB3\\ROOT_HUB30\\4&127B4E9D&0"
        \\ZJLPC\root\cimv2:Win32_PnPEntity.DeviceID="USB\\VID_03F0&PID_034A\\5&3566C2AE&0&11"
        \\ZJLPC\root\cimv2:Win32_PnPEntity.DeviceID="USB\\VID_03F0&PID_034A&MI_00\\6&17EA4430&0&0000"
        \\ZJLPC\root\cimv2:Win32_PnPEntity.DeviceID="HID\\VID_03F0&PID_034A&MI_00\\7&1E807635&0&0000"
        \\ZJLPC\root\cimv2:Win32_PnPEntity.DeviceID="USB\\VID_03F0&PID_034A&MI_01\\6&17EA4430&0&0001"
        \\ZJLPC\root\cimv2:Win32_PnPEntity.DeviceID="HID\\VID_03F0&PID_034A&MI_01&COL01\\7&556C78D&0&0000"
        \\ZJLPC\root\cimv2:Win32_PnPEntity.DeviceID="HID\\VID_03F0&PID_034A&MI_01&COL02\\7&556C78D&0&0001"
        \\ZJLPC\root\cimv2:Win32_PnPEntity.DeviceID="USB\\VID_15D9&PID_0A4F\\5&3566C2AE&0&12"
        \\ZJLPC\root\cimv2:Win32_PnPEntity.DeviceID="HID\\VID_15D9&PID_0A4F\\6&37A0AA42&0&0000"
        \\ZJLPC\root\cimv2:Win32_PnPEntity.DeviceID="USB\\VID_0547&PID_114C\\5&3566C2AE&0&17"
    ############################################################################################################################### 
    #  We just extract last time as our defined target normally.
    # 
    '''
    _TUP_VISION_DESC_LIST = [\
        {'name':'OBVIOUS_UCMOS10000KPA', 'desc':'VID_0547&PID_6010', 'width':3584, 'height':2748, 'usage':'通用白光场景型号'},\
        {'name':'OBVIOUS_E3ISPM05000KPA', 'desc':'VID_0547&PID_114C', 'width':2448, 'height':2048, 'usage':'荧光尝试1，放弃'},\
        {'name':'TOUPCAM_E3ISPM06300KPB', 'desc':'VID_0547&PID_1217', 'width':3072, 'height':2048, 'usage':'荧光目标型号'},\
        {'name':'TOUPCAM_UCMOS05100KPA', 'desc':'VID_0547&PID_6510','width':2592,'height':1944, 'usage':'新华医院独有白光型号'},\
        {'name':'MS60', 'desc':'VID_04B4&PID_B630','width':3072,'height':2048, 'usage':'明美摄像头'},\
        {'name':'MS50-T-3', 'desc':'VID_04B4&PID_B504','width':2592,'height':1944, 'usage':'低配版明美摄像头'},\
        ]
    #分辨率必须根据设备型号，重新选择 #DEFAULT SELCTION
    TUP_VISION_CAMBER_RES_WIDTH = 2592
    TUP_VISION_CAMBER_RES_HEIGHT = 1944

    
    def __init__(self):    
        super(clsCebsDhCamera, self).__init__()  
    
    
    '''
    #
    # 摄像头参数的本地初始化过程
    # In: ???
    #
    '''    
    def tup_dhal_camera_update_context(self, glParCamera):
        pass
    

    '''
    #
    # 摄像头操作过程
    # In: ???
    #
    '''      
    def tup_dhal_camera_cap_pic(self, picFileName):
        pass
    
    def tup_dhal_camera_cap_video(self, videoFileName, durInSec):
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    
    