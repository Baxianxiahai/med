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
        {'restTag':'dba', 'actionId':0x3800, 'actionName':'opr_env', 'comments':''},\
        {'restTag':'dba', 'actionId':0x3801, 'actionName':'opr_counter', 'comments':''},\
        {'restTag':'dba', 'actionId':0x3802, 'actionName':'opr_fspc', 'comments':''},\
        {'restTag':'dba', 'actionId':0x3803, 'actionName':'opr_file', 'comments':''},\
        ]
    
    def __init__(self):
        '''
        Constructor
        '''
 
    
    '''
    #
    #ENV部分
    #
    #
    '''
    #初始化表单 - 如果读取失败，则自动插入一条新记录，所有的参数都是缺省的。这样处理将更加理性和完善。
    def envCreate(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_env':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True,{'cmd':'add', 'tupLable':tupLable} )
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

    #读取完整的信息，必须通过tupLable进行索引
    def envRead(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_env':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'read', 'tupLable':tupLable})
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
    
    def envDelete(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_env':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'delete', 'tupLable':tupLable})
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
    
    def envModify(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_env':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'modify', 'tupLable':tupLable})
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
    
    #更新表单 - 假设是一直存同一条记录，通过TupLable进行区分
    def envUpdateAll(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_env':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'updateAll', 'tupLable':tupLable})
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

    #更新部分参数 - 左下角
    def envUpdateAxisLeftBot(self, left_bot_x, left_bot_y):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_env':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'updateAxisLeftBot', 'left_bot_x':left_bot_x, 'left_bot_y':left_bot_y})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    #更新部分参数-右上角
    def envUpdateAxisRightUp(self, right_up_x, right_up_y):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_env':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'updateAxisRightUp', 'right_up_x':right_up_x, 'right_up_y':right_up_y})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    #增加更多的api访问函数。每个函数对应的处理过程，都要由这里以及HST中的服务一起完成


    '''
    #
    #COUNTER部分
    #
    #
    '''
    #读取完整的信息，必须通过tupLable进行索引
    def counterCreate(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_counter':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'add', 'tupLable':tupLable})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def counterRead(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_counter':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'read', 'tupLable':tupLable})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def counterDelete(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_counter':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'delete', 'tupLable':tupLable})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def counterModify(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_counter':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'modify', 'tupLable':tupLable})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    #增加更多的api访问函数。每个函数对应的处理过程，都要由这里以及HST中的服务一起完成


    '''
    #
    #FSPC部分
    #
    #
    '''
    def fspcCreate(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_fspc':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'add', 'tupLable':tupLable})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def fspcRead(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_fspc':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'read', 'tupLable':tupLable})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def fspcDelete(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_fspc':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'delete', 'tupLable':tupLable})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def fspcModify(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_fspc':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'modify', 'tupLable':tupLable})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    #增加更多的api访问函数。每个函数对应的处理过程，都要由这里以及HST中的服务一起完成



    '''
    #
    #FILE部分
    #
    #
    '''

    def fileCreate(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_file':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'add', 'tupLable':tupLable})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def fileRead(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_file':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'read', 'tupLable':tupLable})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent

    def fileDelete(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_file':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'delete', 'tupLable':tupLable})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    
    def fileModify(self, tupLable):
        searchFlag = False
        for element in self._TUP_HST_MSG_MATRIX:
            if element['actionName'] == 'opr_file':
                searchFlag = True
                actionId = element['actionId']
        if (searchFlag == False):
            return -1, ''
        inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'modify', 'tupLable':tupLable})
        res = self.hstCurlPost(inputJson)
        restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
        if (restTag != 'dba'):
            return -2, ''
        if (newActionId != actionId):
            return -3, ''
        if (parFlag <= 0):
            return -4, ''
        return 1, parContent
    #增加更多的api访问函数。每个函数对应的处理过程，都要由这里以及HST中的服务一起完成











if __name__ == '__main__':
    cls = TupClsCebsDbaItf()
    #res = hst.hstCurlPost({"restTag": "dba", "actionId": 3800, "parFlag": 1, "parContent":{"cmd":"add","user":"test222"}})
    #env test
    #lc:create test ok
    #print(cls.envCreate({'workdir':'D','pic_origin':'E','pic_middle':'F'}))
    #lc:read test ok 
    #print(cls.envRead({'workdir':'workdir','pic_origin':'pic_origin','pic_middle':'pic_middle'}))
    #lc:modify test ok
    #print(cls.envModify({'workdir':'123'}))
    #lc:delete test ok
    #print(cls.envDelete({'workdir':'123'}))
    
    #counter test
    print(cls.counterCreate({'picbatchcnt':'100'}))
    #print(cls.counterRead({'picbatchcnt':'picbatchcnt'}))
    #print(cls.counterModify({'picbatchcnt':'500'}))
    #print(cls.counterDelete({'picbatchcnt':'500'}))

    #fspc test
#     print(cls.fspcCreate({'mark_line':'100'}))
#     print(cls.fspcRead({'mark_line':'mark_line'}))
#     print(cls.fspcModify({'mark_line':'500'}))
#     print(cls.fspcDelete({'mark_line':'500'}))
    
    #batchfile test
    #print(cls.fileCreate({'batch_no':'100'}))
#     print(cls.fileRead({'batch_no':'batch_no'}))
#     print(cls.fileModify({'batch_no':'500'}))
#     print(cls.fileDelete({'batch_no':'500'}))













