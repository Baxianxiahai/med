'''
Created on 2019年2月13日

@author: Administrator
'''

from PkgL2svrHandler.ModHstapi import *


#业务处理类，继承基类的属性
class TupClsFawsDbaItf(TupClsHstapiBasic):
    '''
    classdocs
    '''

    _TUP_HST_MSG_MATRIX = [\
        {'restTag':'dba', 'actionId':3800, 'actionName':'opr_env', 'comments':''},\
        {'restTag':'dba', 'actionId':3801, 'actionName':'opr_counter', 'comments':''},\
        {'restTag':'dba', 'actionId':3802, 'actionName':'opr_fspc', 'comments':''},\
        {'restTag':'dba', 'actionId':3803, 'actionName':'opr_file', 'comments':''},\
        ]
    
    def __init__(self):
        '''
        Constructor
        '''