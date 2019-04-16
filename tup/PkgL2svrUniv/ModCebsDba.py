'''
Created on 2019年2月13日

@author: Administrator
'''

from PkgL2svrHandler.ModHstapi import *
from _tkinter import create
#from pip._vendor.packaging.requirements import EXTRA


#业务处理类，继承基类的属性
class TupClsCebsDbaItf(TupClsHstapiBasic):
    '''
    classdocs
    '''

    '''
    #
    #设计逻辑：
    #
    # env是单条记录，按照tupLable固定的表，
    # counter是单条记录，按照tupLable索引
    # fspc是多条记录，按照sid编号进行索引：系统每导入一次fpsc批次，会动态生成本次导入的fspc信息，包括多少张图片、时间日历、原始文件名、识别情况等
    # file是多条记录，随着拍摄动态生成的，按照批次+孔位序号进行双索引
    #
    '''
    _TUP_HST_MSG_MATRIX = [\
        {'restTag':'dba', 'actionId':0X0ED7, 'actionName':'cebs_user_sheet', 'comments':''},\
        {'restTag':'dba', 'actionId':0X0ED8, 'actionName':'cebs_product_profile', 'comments':''},\
        {'restTag':'dba', 'actionId':0X0ED9, 'actionName':'cebs_cali_profile', 'comments':''},\
        {'restTag':'dba', 'actionId':0X0EDA, 'actionName':'cebs_object_profile', 'comments':''},\
        {'restTag':'dba', 'actionId':0X0EDB, 'actionName':'cebs_config_eleg', 'comments':''},\
        {'restTag':'dba', 'actionId':0X0EDC, 'actionName':'cebs_config_stackcell', 'comments':''},\
        {'restTag':'dba', 'actionId':0X0EDD, 'actionName':'cebs_result_eleg', 'comments':''},\
        {'restTag':'dba', 'actionId':0X0EDE, 'actionName':'cebs_result_stackcell', 'comments':''},\
        {'restTag':'dba', 'actionId':0X0EDF, 'actionName':'cebs_result_init_conf', 'comments':''},\
 
        ]
    
    def __init__(self):
        '''
        Constructor
        '''
    
    
    '''
    #
    #cebs_user_sheet部分
    #
    #
    '''
    #创建表单， 在创建表单的时候把表所有字段参数全部传入
    def cebs_user_sheet_Create(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_user_sheet':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def cebs_user_sheet_Delete(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_user_sheet':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def cebs_user_sheet_Modify(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_user_sheet':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent  
     
    
    def cebs_user_sheet_Read(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_user_sheet':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    '''
    #
    #cebs_product_profile部分
    #
    #
    '''
    def cebs_product_profile_Create(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_product_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def cebs_product_profile_Delete(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_product_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def cebs_product_profile_Modify(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_product_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def cebs_product_profile_Read(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_product_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    '''
    #
    #cebs_cali_profile部分
    #
    #
    '''    
    def cebs_cali_profile_Create(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_cali_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent    
    
    def cebs_cali_profile_Delete(self, inputData):
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_cali_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent 
    
    def cebs_cali_profile_Modify(self, inputData):
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_cali_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def cebs_cali_profile_Read(self, inputData):
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_cali_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    '''
    #
    #cebs_object_profile部分
    #
    #
    '''    
    def cebs_object_profile_Create(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_object_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent    

    def cebs_object_profile_Delete(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_object_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def cebs_object_profile_Modify(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_object_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def cebs_object_profile_Read(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_object_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    '''
    #
    #cebs_config_eleg部分
    #
    #
    '''    
    def cebs_config_eleg_Create(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_config_eleg':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent   
    
    def cebs_config_eleg_Delete(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_config_eleg':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent  

    def cebs_config_eleg_Modify(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_config_eleg':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def cebs_config_eleg_Read(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_config_eleg':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent 
    '''
    #
    #cebs_config_stackcell部分
    #
    #
    '''    
    def cebs_config_stackcell_Create(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_config_stackcell':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent    

    def cebs_config_stackcell_Delete(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_config_stackcell':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def cebs_config_stackcell_Modify(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_config_stackcell':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def cebs_config_stackcell_Read(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_config_stackcell':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    '''
    #
    #cebs_result_eleg部分
    #
    #
    '''    

    def cebs_result_eleg_Create(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_eleg':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def cebs_result_eleg_Delete(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_eleg':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def cebs_result_eleg_Modify(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_eleg':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def cebs_result_eleg_Read(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_eleg':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    '''
    #
    #cebs_result_stackcell部分
    #
    #
    '''    
    def cebs_result_stackcell_Create(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_stackcell':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent 
    
    def cebs_result_stackcell_Delete(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_stackcell':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, inputData )
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def cebs_result_stackcell_Modify(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_stackcell':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
 
    def cebs_result_stackcell_Read(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_stackcell':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent  

    def cebs_result_init_conf_Read(self, inputData):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_init_conf':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,inputData)
        print("outputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent 

if __name__ == '__main__':
    cls = TupClsCebsDbaItf()
    #res = hst.hstCurlPost({"restTag": "dba", "actionId": 3800, "parFlag": 1, "parContent":{"cmd":"add","user":"test222"}})
    #create operation
#     print("create operation\r\n")
    print(cls.cebs_user_sheet_Create({'cmd':'add', 'uid':251, 'login_name':'admin', 'pass_word':'13456', 'grade_level':1,'email':'13525@.com', 'memo':'this'}))
#     print(cls.cebs_product_profile_Create({'cmd':'add', 'dev_code':'shanghai', 'hw_ver':222, 'sw_ver':333, 'authtoken':'thisis'} ))
#     print(cls.cebs_cali_profile_Create({'cmd':'add', 'platetype':1,'uid':250, 'left_bot_x':0, 'left_bot_y':0, 'right_up_x':0, 'right_up_y':0, 'accspeed':20, 'decspeed':20, 'movespeed':20, 'zero_spd':20, 'zero_dec':20, 'back_step':12800} ))
#     print(cls.cebs_object_profile_Create({'cmd':'add', 'objname':'xianchong','objtype':1, 'uid':250, 'dir_origin':'varcebs', 'dir_middle':'varcebs', 'memo':'varcebs'}))
#     print(cls.cebs_config_eleg_Create({'cmd':'add', 'objid':5,'fixpoint':0, 'autovideo':0, 'autodist':0, 'addset':1, 'autocap':0, 'autoperiod':60, 'videotime':3, 'slimit':200,'smlimit':500, 'mblimit':2000, 'blimit':5000} ))
#     print(cls.cebs_config_stackcell_Create({'cmd':'add', 'objid':5,'addset':1, 'line_area':10000, 'line_width':44, 'line_long':222, 'line_dilate':22, 'area_up':1000000, 'area_low':100000, 'area_dilate':1500,'area_erode':5, 'square_min':920, 'square_max':1500,'radius_min':19, 'radius_max':23, 'cell_dilate':61, 'cell_erode':5, 'cell_round':50, 'cell_distance':60, 'train_delay':3}))
#     print(cls.cebs_result_eleg_Create({'cmd':'add', 'confid':5,'snbatch':25, 'snhole':3, 'file_attr':1, 'name_before':'cebs', 'name_after':'cebs', 'bigalive':0, 'bigdead':0, 'midalive':0,'middead':0, 'smaalive':0, 'smdead':0,'totalalive':0, 'totaldead':0, 'totalsum':0, 'doneflag':0, 'memo':'this'}))
#     print(cls.cebs_result_stackcell_Create({'cmd':'add', 'confid':7,'file_attr':0, 'name_before':'fileb','name_after':'resultfileA', 'totalnbr':0, 'validnbr':0, 'doneflag':0, 'memo':'thisisdemo'}))

    '''
    note：
           根据有无传入字段来进行判断要更新那些值   
    '''
    
    #modify operation 
#     print("modify operation")
    print(cls.cebs_user_sheet_Modify({'cmd':'modify','uid':250,'pass_word':54321,'reg_date':'2019-03-01 08:33:33'}))
    print(cls.cebs_result_init_conf_Read({'cmd':'read'}))
#     print(cls.cebs_product_profile_Modify({'cmd':'modify','id':4,'hw_ver':250,'mfd':'2019-03-01 08:33:33'}))
#     print(cls.cebs_cali_profile_Modify({'cmd':'modify','id':5,'calitime':'2019-03-01 08:33:33','left_bot_x':100,'left_bot_y':200,'right_up_x':400,'right_up_y':800}))
#     print(cls.cebs_object_profile_Modify({'cmd':'modify','objid':5,'objname':'prototype','dir_origin':'test'}))
#     print(cls.cebs_config_eleg_Modify({'cmd':'modify','confid':11,'slimit':250,'smlimit':250,'mblimit':250,'blimit':250}))
#     print(cls.cebs_config_stackcell_Modify({'cmd':'modify','confid':4,'line_area':250,'line_long':250}))
#     print(cls.cebs_result_eleg_Modify({'cmd':'modify','sid':11,'snbatch':25,'snhole':250,'cap_time':'2019-03-01 08:33:33','rec_time':'2019-03-01 08:33:33'}))
#     print(cls.cebs_result_stackcell_Modify({'cmd':'modify','sid':6,'rec_time':'2019-03-01 08:33:33'}))
    '''
    note:
            这里的读取操作， 是根据传入主键参数  来获取表单内全部内容（hst中写的是返回该主键对应行的全部字段及参数）上层接收到再进行处理
            还是说我要什么就字段的参数就将字段参数传入，只返回需要的字段参数,方式不同在hst服务中相应的code不同
    ''' 
    #read operation    
#     print("read operation")
    print(cls.cebs_user_sheet_Read({'cmd':'read', 'uid':250}))
#     print(cls.cebs_product_profile_Read({'cmd':'read', 'id':5}))
#     print(cls.cebs_cali_profile_Read({'cmd':'read', 'id':5}))
#     print(cls.cebs_object_profile_Read({'cmd':'read', 'objid':7}))
#     print(cls.cebs_config_eleg_Read({'cmd':'read', 'confid':11}))
#     print(cls.cebs_config_stackcell_Read({'cmd':'read', 'confid':4}))
#     print(cls.cebs_result_eleg_Read({'cmd':'read', 'sid':11}))
#     print(cls.cebs_result_stackcell_Read({'cmd':'read', 'sid':5}))
 
 
    
    #delete operation
#     print("delete operation")
#     print(cls.cebs_user_sheet_Delete({'cmd':'delete', 'uid':250}))
#     print(cls.cebs_product_profile_Delete({'cmd':'delete', 'id':1}))
#     print(cls.cebs_cali_profile_Delete({'cmd':'delete', 'id':1}))
#     print(cls.cebs_object_profile_Delete({'cmd':'delete', 'objid':1}))
#     print(cls.cebs_config_eleg_Delete({'cmd':'delete', 'confid':1}))
#     print(cls.cebs_config_stackcell_Delete({'cmd':'delete', 'confid':1}))
#     print(cls.cebs_result_eleg_Delete({'cmd':'delete', 'sid':1}))
#     print(cls.cebs_result_stackcell_Delete({'cmd':'delete', 'sid':1}))


    #MAY USE EXTRA API 
    #read the hole batch file result
    #print(cls.cebs_result_eleg_Read({'cmd':'read', 'snbatch':20}))
    
    
    
    
