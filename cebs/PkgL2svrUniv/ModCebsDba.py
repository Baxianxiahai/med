'''
Created on 2019年2月13日

@author: Administrator
'''

from PkgL2svrHandler.ModHstapi import *
from _tkinter import create


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
    
    def cebs_user_sheet_Delete(self, uid):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_user_sheet':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'delete', 'uid':uid} )
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
    
    def cebs_user_sheet_Read(self, uid):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_user_sheet':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'read', 'uid':uid} )
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
    
    '''
    #
    #cebs_product_profile部分
    #
    #
    '''
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
    
    def cebs_product_profile_Delete(self, id):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_product_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'delete', 'id':id} )
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

    def cebs_product_profile_Read(self, id):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_product_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'read', 'id':id} )
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
    
    '''
    #
    #cebs_cali_profile部分
    #
    #
    '''    
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
    
    def cebs_cali_profile_Delete(self, id):
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_cali_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'delete', 'id':id} )
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

    def cebs_cali_profile_Read(self, id):
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_cali_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'read', 'id':id} )
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
    '''
    #
    #cebs_object_profile部分
    #
    #
    '''    
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

    def cebs_object_profile_Delete(self, objid):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_object_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'delete', 'objid':objid } )
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

    def cebs_object_profile_Read(self, objid):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_object_profile':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'read', 'objid':objid } )
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
    '''
    #
    #cebs_config_eleg部分
    #
    #
    '''    
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
    
    def cebs_config_eleg_Delete(self, confid):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_config_eleg':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'delete', 'confid':confid})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent  
    
    def cebs_config_eleg_Read(self, confid):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_config_eleg':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'read', 'confid':confid})
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
    def cebs_config_stackcell_Create(self, objid, addset , line_area, line_width, line_long, line_dilate, area_up, area_low, area_dilate, area_erode, square_min, square_max, radius_min, radius_max,
        cell_dilate,  cell_erode, cell_round, cell_distance, train_delay):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_config_stackcell':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'add', 'objid':objid,'addset':addset, 'line_area':line_area, 
        'line_width':line_width, 'line_long':line_long, 'line_dilate':line_dilate, 'area_up':area_up, 'area_low':area_low, 'area_dilate':area_dilate,'area_erode':area_erode, 'square_min':square_min, 'square_max':square_max,
        'radius_min':radius_min, 'radius_max':radius_max, 'cell_dilate':cell_dilate, 'cell_erode':cell_erode, 'cell_round':cell_round, 'cell_distance':cell_distance, 'train_delay':train_delay
        } )
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

    def cebs_config_stackcell_Delete(self, confid):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_config_stackcell':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'delete', 'confid':confid} )
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
    
    def cebs_config_stackcell_Read(self, confid):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_config_stackcell':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'read', 'confid':confid} )
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
    '''
    #
    #cebs_result_eleg部分
    #
    #
    '''    
    def cebs_result_eleg_Create(self, confid, snbatch , snhole, file_attr, name_before, name_after, bigalive, bigdead, midalive, middead, smaalive, smdead, totalalive, totaldead,
        totalsum,  doneflag, memo):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_eleg':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'add', 'confid':confid,'snbatch':snbatch, 'snhole':snhole, 
        'file_attr':file_attr, 'name_before':name_before, 'name_after':name_after, 'bigalive':bigalive, 'bigdead':bigdead, 'midalive':midalive,'middead':middead, 'smaalive':smaalive, 'smdead':smdead,
        'totalalive':totalalive, 'totaldead':totaldead, 'totalsum':totalsum, 'doneflag':doneflag, 'memo':memo
        } )
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

    def cebs_result_eleg_Delete(self, sid):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_eleg':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'delete', 'sid':sid} )
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
    
    def cebs_result_eleg_Read(self, sid):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_eleg':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'read', 'sid':sid} )
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
    '''
    #
    #cebs_result_stackcell部分
    #
    #
    '''    
    def cebs_result_stackcell_Create(self, confid, file_attr , name_before, name_after, totalnbr, validnbr, doneflag, memo):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_stackcell':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'add', 'confid':confid,'file_attr':file_attr, 'name_before':name_before, 
        'name_after':name_after, 'totalnbr':totalnbr, 'validnbr':validnbr, 'doneflag':doneflag, 'memo':memo} )
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
    
    def cebs_result_stackcell_Delete(self, sid):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_stackcell':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'delete', 'sid':sid} )
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
 
    def cebs_result_stackcell_Read(self, sid):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'cebs_result_stackcell':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'read','sid':sid})
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
    #create operation
    #print(cls.cebs_user_sheet_Create(1, 'admin', 'bxxh123', 1, '13525@qq.com', 'thisisdemo' ))
    #print(cls.cebs_product_profile_Create('SHKD001', 222, 333,'thisisdemo' ))
    #print(cls.cebs_cali_profile_Create(1, 1, 0, 0, 0, 0, 20, 20, 20, 20, 20, 12800))
    #print(cls.cebs_object_profile_Create('xianchong', 1, 1, 'varcebs', 'varcebs', 'thisisdemo'))
    #print(cls.cebs_config_eleg_Create(1, 0, 0, 0, 1, 0, 60, 3, 200, 500, 2000, 5000))
    #print(cls.cebs_config_stackcell_Create(1, 1, 10000, 44, 222, 22, 1000000, 100000, 1500, 5, 920, 1500, 19, 23, 61, 5, 50, 30, 2))
    #print(cls.cebs_result_eleg_Create(1, 0, 0, 1, 'fileA', 'resultfileA', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'thisisdemo'))
    #print(cls.cebs_result_stackcell_Create(1, 1, 'fileA', 'resultfileA', 0, 0, 0, 'thisisdemo'))

    #delete operation
    #print(cls.cebs_user_sheet_Delete(1))
    #print(cls.cebs_product_profile_Delete(1))
    #print(cls.cebs_cali_profile_Delete(1))
    #print(cls.cebs_object_profile_Delete(1))
    #print(cls.cebs_config_eleg_Delete(1))
    #print(cls.cebs_config_stackcell_Delete(1))
    #print(cls.cebs_result_eleg_Delete(1))
    #print(cls.cebs_result_stackcell_Delete(1))

    #read operation
    print(cls.cebs_user_sheet_Read(1))
    print(cls.cebs_product_profile_Read(1))
    print(cls.cebs_cali_profile_Read(1))
    print(cls.cebs_object_profile_Read(1))
    print(cls.cebs_config_eleg_Read(1))
    print(cls.cebs_config_stackcell_Read(1))
    print(cls.cebs_result_eleg_Read(1))
    print(cls.cebs_result_stackcell_Read(1))


