'''
Created on 2019年5月31日

@author: Administrator
'''

import unittest
from PkgUt import ModTestSuitHuicobus

#包含所有的Suite
def hst_all_testsuite():
    allTest = unittest.TestSuite((\
        ModTestSuitHuicobus.cebs_testsuite_huicobus(), \
        ))
    return allTest

#运行的时候，可以根据不同的要求，运行不同的Suite,或者全部运行，这样就方便管理每次运行的case
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(hst_all_testsuite())