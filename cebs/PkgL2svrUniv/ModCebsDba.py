'''
Created on 2019年2月13日

@author: Administrator
'''

from PkgL2svrHandler.ModHstapi import *


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
    def cebs_user_sheet_Create(self, uid, login_name, pass_word, grade_level, email, memo):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_user_sheet':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'add', 'uid':uid, 'login_name':login_name, 'pass_word':pass_word, 'grade_level':grade_level,'email':email, 'memo':memo } )
        print("inputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def cebs_product_profile_Create(self, dev_code, hw_ver, sw_ver, authtoken):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_product_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'add', 'dev_code':dev_code, 'hw_ver':hw_ver, 'sw_ver':sw_ver, 'authtoken':authtoken} )
        print("inputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def cebs_cali_profile_Create(self, platetype, uid , left_bot_x, left_bot_y, right_up_x, right_up_y, accspeed, decspeed, movespeed, zero_spd, zero_dec, back_step):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_cali_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'add', 'platetype':platetype,'uid':uid, 'left_bot_x':left_bot_x, 
        'left_bot_y':left_bot_y, 'right_up_x':right_up_x, 'right_up_y':right_up_y, 'accspeed':accspeed, 'decspeed':decspeed, 'movespeed':movespeed, 'zero_spd':zero_spd, 'zero_dec':zero_dec, 'back_step':back_step} )
        print("inputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent    
    
    def cebs_object_profile_Create(self, objname, objtype , uid, dir_origin, dir_middle, memo):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_object_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'add', 'objname':objname,'objtype':objtype, 'uid':uid, 
        'dir_origin':dir_origin, 'dir_middle':dir_middle, 'memo':memo} )
        print("inputJson",inputJson)
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent    
    
    def cebs_config_eleg_Create(self, objid, fixpoint , autovideo, autodist, addset, autocap, autoperiod, videotime, slimit, smlimit, mblimit, blimit):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_config_eleg':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'add', 'objid':objid,'fixpoint':fixpoint, 'autovideo':autovideo, 
        'autodist':autodist, 'addset':addset, 'autocap':autocap, 'autoperiod':autoperiod, 'videotime':videotime, 'slimit':slimit,'smlimit':smlimit, 'mblimit':mblimit, 'blimit':blimit} )
        print("inputJson",inputJson)
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
    #print(cls.cebs_user_sheet_Create(1, 'admin', 'bxxh123', 1, '13525@qq.com', 'thisisdemo' ))
    #print(cls.cebs_product_profile_Create('SHKD001', 222, 333,'thisisdemo' ))
    #print(cls.cebs_cali_profile_Create(1, 1535, 0, 0, 0, 0, 20, 20, 20, 20, 20, 12800))
    #print(cls.cebs_object_profile_Create('xianchong', 1, 1535, 'varcebs', 'varcebs', 'thisisdemo'))
    print(cls.cebs_config_eleg_Create(1535, 0, 0, 0, 1, 0, 60, 3, 200, 500, 2000, 5000))








