'''
Created on 2019年5月31日

@author: Administrator
'''

import unittest
import time
from PkgUt import ModTestSuitComFunc

def cebs_testsuite_huicobus():
    print ("cebs_testsuite_huicobus 运行")
    suiteTest = unittest.TestSuite()
    suiteTest.addTest(ClassUtHuicobus("tc_huicobus_001"))
    suiteTest.addTest(ClassUtHuicobus("tc_huicobus_002"))
    return suiteTest

#测试集合
class ClassUtHuicobus(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def tc_huicobus_001(self):
        ticks = time.time();
        print("tc_huicobus_001, time in second = ", ticks);        
        a = 3
        b = 2
        self.assertEqual(a+b, 5,'Result Fail')


    '''
    '如果使用mosquito，则需要输入转义
    mosquitto_pub -t HUICOBUS_MQTT_TOPIC_UIP2TUP -m {\"srcNode\":\"HUICOBUS_MQTT_NODEID_TUPSVR\",\"destNode\":\"HUICOBUS_MQTT_NODEID_TUPSVR\",\"srcId\":\"HUICOBUS_MQTT_CLIENTID_TUPROUTER\",\"destId\":\"HUICOBUS_MQTT_CLIENTID_TUPENTRY\",\"topicId\":\"HUICOBUS_MQTT_TOPIC_UIP2TUP\",\"cmdId\":2560,\"cmdValue\":123,\"hlContent\":{\"a\":1,\"b\":2}}

    '''
    def tc_huicobus_002(self):
        ticks = time.time();
        print("tc_huicobus_002, time in second = ", ticks);
        jsonInputData = {'srcNode':'HUICOBUS_MQTT_NODEID_TUPSVR',\
                        'destNode':'HUICOBUS_MQTT_NODEID_TUPSVR',\
                        'srcId':'HUICOBUS_MQTT_CLIENTID_TUPROUTER',\
                        'destId':'HUICOBUS_MQTT_CLIENTID_TUPENTRY',\
                        'topicId':'HUICOBUS_MQTT_TOPIC_UIP2TUP',\
                        'cmdId':2689,\
                        'cmdValue':123,\
                        'hlContent':{'a':1, 'b':2}\
                        }
        #jsonInputData = {'srcNode':'','destNode':'','srcId':'','destId':'','topicId':'HUICOBUS_MQTT_TOPIC_UIP2TUP','cmdId':2689,'cmdValue':123,'hlContent':{'a':1,'b':2}}
        ModTestSuitComFunc.cebs_huicobus_msg_send(jsonInputData)
        
        
        
        
        
        
        
        