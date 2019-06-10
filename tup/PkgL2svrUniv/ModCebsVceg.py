'''
Created on 2019年6月10日

@author: Administrator

Mod name: Vision Classification Engine

'''

from PkgL2svrHandler.headHstapi import *
from PkgL2svrHandler.ModHstapi import *
from PkgL2svrHandler.headHstapi import *
from _tkinter import create


#业务处理类，继承基类的属性
class TupClsCebsVcegIft(TupClsHstapiBasic):
    '''
    classdocs
    '''

    '''
    #
    #设计逻辑：
    #
    #
    '''
    __HUIREST_ACTIONID_CEWORM_white_pic_cfy             = 27001
    __HUIREST_ACTIONID_CEWORM_flu_pic_cfy               = 27002
    __HUIREST_ACTIONID_CEWORM_fcc_pic_cfy               = 27003
    __HUIREST_ACTIONID_CEWORM_fspc_pic_cfy              = 27004
    __HUIREST_ACTIONID_CEWORM_white_video_cfy           = 27005
    __HUIREST_ACTIONID_CEWORM_colony_cfy                = 27010 #菌落识别
    __HUIREST_ACTIONID_CEWORM_cnn_pic_cfy               = 27020 #CNN算法尝试识别线虫
    __HUIREST_ACTIONID_CEWORM_cnn_colony_cfy            = 27021 #CNN算法尝试识别菌落
    
        
    def __init__(self):
        '''
        Constructor
        '''
        
    '''
    #
    # 通用统一的操作函数
    # In: hlBuf - parContent部分，以dict为结构
    # Out: parContent - 标准的解码后dict结构
    #
    '''
    def cebs_ceworm_white_pic_operation(self, hlBuf):
        inputJson = self.hstapiEncode('ceworm', self.__HUIREST_ACTIONID_CEWORM_white_pic_cfy, True, hlBuf)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'ceworm'):
            return -2, ''
        if (newActionId != self.__HUIREST_ACTIONID_CEWORM_white_pic_cfy):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def cebs_ceworm_flu_pic_operation(self, hlBuf):
        inputJson = self.hstapiEncode('ceworm', self.__HUIREST_ACTIONID_CEWORM_flu_pic_cfy, True, hlBuf)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'ceworm'):
            return -2, ''
        if (newActionId != self.__HUIREST_ACTIONID_CEWORM_flu_pic_cfy):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def cebs_ceworm_fcc_pic_operation(self, hlBuf):
        inputJson = self.hstapiEncode('ceworm', self.__HUIREST_ACTIONID_CEWORM_fcc_pic_cfy, True, hlBuf)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'ceworm'):
            return -2, ''
        if (newActionId != self.__HUIREST_ACTIONID_CEWORM_fcc_pic_cfy):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def cebs_ceworm_fspc_pic_operation(self, hlBuf):
        inputJson = self.hstapiEncode('ceworm', self.__HUIREST_ACTIONID_CEWORM_fspc_pic_cfy, True, hlBuf)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'ceworm'):
            return -2, ''
        if (newActionId != self.__HUIREST_ACTIONID_CEWORM_fspc_pic_cfy):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def cebs_ceworm_white_video_operation(self, hlBuf):
        inputJson = self.hstapiEncode('ceworm', self.__HUIREST_ACTIONID_CEWORM_white_video_cfy, True, hlBuf)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'ceworm'):
            return -2, ''
        if (newActionId != self.__HUIREST_ACTIONID_CEWORM_white_video_cfy):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def cebs_ceworm_colony_operation(self, hlBuf):
        inputJson = self.hstapiEncode('ceworm', self.__HUIREST_ACTIONID_CEWORM_colony_cfy, True, hlBuf)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'ceworm'):
            return -2, ''
        if (newActionId != self.__HUIREST_ACTIONID_CEWORM_colony_cfy):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def cebs_ceworm_cnn_pic_operation(self, hlBuf):
        inputJson = self.hstapiEncode('ceworm', self.__HUIREST_ACTIONID_CEWORM_cnn_pic_cfy, True, hlBuf)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'ceworm'):
            return -2, ''
        if (newActionId != self.__HUIREST_ACTIONID_CEWORM_cnn_pic_cfy):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def cebs_ceworm_cnn_colony_operation(self, hlBuf):
        inputJson = self.hstapiEncode('ceworm', self.__HUIREST_ACTIONID_CEWORM_cnn_colony_cfy, True, hlBuf)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'ceworm'):
            return -2, ''
        if (newActionId != self.__HUIREST_ACTIONID_CEWORM_cnn_colony_cfy):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    
    '''
    #
    #预期的数据操作
    # - 取存储参数 hstGetConfig
    #
    '''
    
    
    
    '''
    #
    # WhitePictureClassification
    # In: TUP_HST_VCEG_WHITE_PIC_CFY_IN
    # Out: TUP_HST_VCEG_WHITE_PIC_CFY_IN
    #
    '''
    def tup_hstCeworm_WhitePicClfy(self, inputData):
        mbuf = TUP_HST_VCEG_WHITE_PIC_CFY_IN;
        oprFlag, res = self.cebs_ceworm_white_pic_operation(mbuf)

        ###测试性回复
        return 1, TUP_HST_VCEG_WHITE_PIC_CFY_OUT
        ###
        
        if oprFlag < 0:
            return oprFlag, ''
        #check with TUP_HST_VCEG_WHITE_PIC_CFY_OUT
        return 1, res
    
    '''
    #
    # WhiteVideoClassification
    # In: TUP_HST_VCEG_WHITE_VIDEO_CFY_IN
    # Out: TUP_HST_VCEG_WHITE_VIDEO_CFY_OUT
    #
    '''
    def tup_hstCeworm_WhiteVideoClfy(self, inputData):
        mbuf = TUP_HST_VCEG_WHITE_VIDEO_CFY_IN;
        oprFlag, res = self.cebs_ceworm_white_video_operation(mbuf)

        ###测试性回复
        return 1, TUP_HST_VCEG_WHITE_VIDEO_CFY_OUT
        ###
        
        if oprFlag < 0:
            return oprFlag, ''
        #check with TUP_HST_VCEG_WHITE_VIDEO_CFY_OUT
        return 1, res    




















    