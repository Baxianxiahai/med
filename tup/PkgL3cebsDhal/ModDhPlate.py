'''
Created on 2019年6月3日

@author: Administrator
'''

from PkgL3cebsDhal.cebsConfig import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL2svrHandler.headHstapi import *
from PkgL2svrHandler.ModHstapi import *
from PkgL2svrHandler.headHstapi import *
    
class clsCebsDhPlate():
    #
    # 固定参数部分
    #
    #研发级决策，不能通过工程参数灵活配置    
    #MEACHNICAL HARDWARE PLATFORM SCOPE DEFINATION
    _HB_MECHNICAL_PLATFORM_HWTYPE1_X_MAX = 140000;
    _HB_MECHNICAL_PLATFORM_HWTYPE1_Y_MAX = 120000;
    _HB_MECHNICAL_PLATFORM_HWTYPE2_X_MAX = 120000;
    _HB_MECHNICAL_PLATFORM_HWTYPE2_Y_MAX = 100000;
    _HB_MECHNICAL_PLATFORM_X_MAX = _HB_MECHNICAL_PLATFORM_HWTYPE1_X_MAX;
    _HB_MECHNICAL_PLATFORM_Y_MAX = _HB_MECHNICAL_PLATFORM_HWTYPE1_Y_MAX;

#     if (_TUP_CEBS_HW_TYPE_CUR == _TUP_CEBS_HW_TYPE_1):
#         _HB_MECHNICAL_PLATFORM_X_MAX = _HB_MECHNICAL_PLATFORM_HWTYPE1_X_MAX;
#         _HB_MECHNICAL_PLATFORM_Y_MAX = _HB_MECHNICAL_PLATFORM_HWTYPE1_Y_MAX;
#     elif (_TUP_CEBS_HW_TYPE_CUR == _TUP_CEBS_HW_TYPE_2):
#         _HB_MECHNICAL_PLATFORM_X_MAX = _HB_MECHNICAL_PLATFORM_HWTYPE2_X_MAX;
#         _HB_MECHNICAL_PLATFORM_Y_MAX = _HB_MECHNICAL_PLATFORM_HWTYPE2_Y_MAX;
#     else:
#         _HB_MECHNICAL_PLATFORM_X_MAX = _HB_MECHNICAL_PLATFORM_HWTYPE1_X_MAX;
#         _HB_MECHNICAL_PLATFORM_Y_MAX = _HB_MECHNICAL_PLATFORM_HWTYPE1_Y_MAX;

    #CONTROL AXIS DIRECTION
    _HB_TARGET_96_STANDARD = "96_STANDARD";
    _HB_TARGET_96_SD_X_MAX = 120000;
    _HB_TARGET_96_SD_Y_MAX = 90000;
    _HB_TARGET_96_SD_BATCH_MAX = 96;
    _HB_TARGET_96_SD_XDIR_NBR = 12;
    _HB_TARGET_96_SD_YDIR_NBR = 8;
    _HB_TARGET_96_SD_HOLE_DIS = 9000;  #in UM
    _HB_TARGET_96_SD_HOLE_RAD = 6500;  #中值直径in UM，(顶+底)/2
     
    _HB_TARGET_48_STANDARD = "48_STANDARD";
    _HB_TARGET_48_SD_X_MAX = 120000;
    _HB_TARGET_48_SD_Y_MAX = 90000;
    _HB_TARGET_48_SD_BATCH_MAX = 48;
    _HB_TARGET_48_SD_XDIR_NBR = 8;
    _HB_TARGET_48_SD_YDIR_NBR = 6;
    _HB_TARGET_48_SD_HOLE_DIS = 12000;  #in UM
    _HB_TARGET_48_SD_HOLE_RAD = 8500;  #中值直径in UM，(顶+底)/2
     
    _HB_TARGET_24_STANDARD = "24_STANDARD";
    _HB_TARGET_24_SD_X_MAX = 120000;
    _HB_TARGET_24_SD_Y_MAX = 90000;
    _HB_TARGET_24_SD_BATCH_MAX = 24;
    _HB_TARGET_24_SD_XDIR_NBR = 6;
    _HB_TARGET_24_SD_YDIR_NBR = 4;
    _HB_TARGET_24_SD_HOLE_DIS = 20000;  #in UM
    _HB_TARGET_24_SD_HOLE_RAD = 15000;  #中值直径in UM，(顶+底)/2
     
    _HB_TARGET_12_STANDARD = "12_STANDARD";
    _HB_TARGET_12_SD_X_MAX = 120000;
    _HB_TARGET_12_SD_Y_MAX = 90000;
    _HB_TARGET_12_SD_BATCH_MAX = 12;
    _HB_TARGET_12_SD_XDIR_NBR = 4;
    _HB_TARGET_12_SD_YDIR_NBR = 3;
    _HB_TARGET_12_SD_HOLE_DIS = 27000;  #in UM
    _HB_TARGET_12_SD_HOLE_RAD = 19000;  #中值直径in UM，(顶+底)/2
     
    _HB_TARGET_6_STANDARD = "6_STANDARD";
    _HB_TARGET_6_SD_X_MAX = 120000;
    _HB_TARGET_6_SD_Y_MAX = 90000;
    _HB_TARGET_6_SD_BATCH_MAX = 6;
    _HB_TARGET_6_SD_XDIR_NBR = 3;
    _HB_TARGET_6_SD_YDIR_NBR = 2;
    _HB_TARGET_6_SD_HOLE_DIS = 40000;  #in UM
    _HB_TARGET_6_SD_HOLE_RAD = 30000;  #中值直径in UM，(顶+底)/2

    #
    # 可配置参数部分
    #
    #ACTION SELCTION
    _HB_TARGET_TYPE_DEFAULT_SET = _HB_TARGET_96_STANDARD;
    dhalPlateTargetTypeCur = _HB_TARGET_TYPE_DEFAULT_SET;
    dhalPlatePicOneWholeBatch = _HB_TARGET_96_SD_BATCH_MAX;

    
    #
    # 临时参量部分
    #
    dhalPlateHoleXnbr = 0;          #HOW MANY BOARD HOLES， X DIRECTION
    dhalPlateHoleYnbr = 0;          #HOW MANY BOARD HOLES，Y DIRECTION
    HB_WIDTH_X_SCALE = 0;       #HOW MANY BOARD HOLES， X DIRECTION
    HB_HEIGHT_Y_SCALE = 0;      #HOW MANY BOARD HOLES，Y DIRECTION
    
    '''
    *左下角的坐标，存在X1/Y1上， 右上角的坐标，存在X2/Y2上 
    *这种方式，符合坐标系的习惯：小值在X1/Y1中，大值在X2/Y2中
    LEFT-BOTTOM for X1/Y1 save in [0/1], RIGHT-UP for X2/Y2 save in [2/3]
    '''
    dhalPlateCaliPosInUm = [0, 0, 0, 0];  #USING INT, um, 96 HOLES, POSITION OF = X1/Y1(LEFT-DOWN), X2/Y2(RIGHT-UP)
    #不断的维持本托盘的位置信息
    dhalPlateCurPosInUm = [0, 0];  #USING INT, um, POSITION X/Y AXIS
    
    
    
    '''
    #
    #本模块设计逻辑
    #=============
    # - plateType托盘类型 + calibAxis校准坐标是两个核心的输入参数
    #   依赖于这两个参数，可以得到所有板孔的位置信息
    # - 板控的信息计算，将一并封装到本模块中，简化上层的业务处理过程
    # - 托盘信息和其它物理设备是无关的，这样做，可以将这个模块做成一种比较好的泛化
    # - 本模块统一定标到um，未来如果需要，还可以进一步提高精度，定标到nm。考虑到python的特性，即便定标到um，也不见得一定是整数，使用float一样可以处理。
    # - 本模块的初始化，依赖于数据库读取的参数（托盘板型）。如果参数不合理，这里只做适当的保护，更完善的保护，将留给上层去处理
    # - 托盘可以在使用的过程中进行更迭。如果调换，只需要按照顺序调用tup_dhal_plate_update_plate_context(), tup_dhal_plate_update_plate_calib()即可。
    # - 本模块将被所有业务模块进行继承。如果需要使用，一定要先传入上述两个核心参数，不然内部参数都是DEFAULT无效参数
    #   这意味着，两个核心参数被一个模块取得后，需要通过内部消息等方式传给其它模块，然后才可能使用。如果上层业务模块不需要使用到这些参量，也可以不初始化，并不影响其它功能的。
    # - 目前预期需要用到本模块的上层业务模块包括：0） GPAR，主控 1）CTRL_SCHD业务调度 2）MOTO控制马达  3）VISION图像识别
    #
    '''
    #初始化
    def __init__(self):
        super(clsCebsDhPlate, self).__init__()



    '''
    #
    # 初始化部分
    #
    '''
    #给上层提供服务的函数
    def tup_dhal_plate_update_context(self, plateType):
        self.dhalPlateTargetTypeCur = plateType
        if (self.dhalPlateTargetTypeCur == self._HB_TARGET_96_STANDARD):
            self.dhalPlatePicOneWholeBatch = self._HB_TARGET_96_SD_BATCH_MAX;
            self.dhalPlateHoleXnbr = self._HB_TARGET_96_SD_XDIR_NBR
            self.dhalPlateHoleYnbr = self._HB_TARGET_96_SD_YDIR_NBR
            self.HB_WIDTH_X_SCALE = self._HB_TARGET_96_SD_X_MAX / (self.dhalPlateHoleXnbr-1);
            self.HB_HEIGHT_Y_SCALE = self._HB_TARGET_96_SD_Y_MAX / (self.dhalPlateHoleYnbr-1);
        elif (self.dhalPlateTargetTypeCur == self._HB_TARGET_48_STANDARD):
            self.dhalPlatePicOneWholeBatch = self._HB_TARGET_48_SD_BATCH_MAX;
            self.dhalPlateHoleXnbr = self._HB_TARGET_48_SD_XDIR_NBR
            self.dhalPlateHoleYnbr = self._HB_TARGET_48_SD_YDIR_NBR
            self.HB_WIDTH_X_SCALE = self._HB_TARGET_48_SD_X_MAX / (self.dhalPlateHoleXnbr-1);
            self.HB_HEIGHT_Y_SCALE = self._HB_TARGET_48_SD_Y_MAX / (self.dhalPlateHoleYnbr-1);
        elif (self.dhalPlateTargetTypeCur == self._HB_TARGET_24_STANDARD):
            self.dhalPlatePicOneWholeBatch = self._HB_TARGET_24_SD_BATCH_MAX;
            self.dhalPlateHoleXnbr = self._HB_TARGET_24_SD_XDIR_NBR
            self.dhalPlateHoleYnbr = self._HB_TARGET_24_SD_YDIR_NBR
            self.HB_WIDTH_X_SCALE = self._HB_TARGET_24_SD_X_MAX / (self.dhalPlateHoleXnbr-1);
            self.HB_HEIGHT_Y_SCALE = self._HB_TARGET_24_SD_Y_MAX / (self.dhalPlateHoleYnbr-1);
        elif (self.dhalPlateTargetTypeCur == self._HB_TARGET_12_STANDARD):
            self.dhalPlatePicOneWholeBatch = self._HB_TARGET_12_SD_BATCH_MAX;
            self.dhalPlateHoleXnbr = self._HB_TARGET_12_SD_XDIR_NBR
            self.dhalPlateHoleYnbr = self._HB_TARGET_12_SD_YDIR_NBR
            self.HB_WIDTH_X_SCALE = self._HB_TARGET_12_SD_X_MAX / (self.dhalPlateHoleXnbr-1);
            self.HB_HEIGHT_Y_SCALE = self._HB_TARGET_12_SD_Y_MAX / (self.dhalPlateHoleYnbr-1);            
        elif (self.dhalPlateTargetTypeCur == self._HB_TARGET_6_STANDARD):
            self.dhalPlatePicOneWholeBatch = self._HB_TARGET_6_SD_BATCH_MAX;
            self.dhalPlateHoleXnbr = self._HB_TARGET_6_SD_XDIR_NBR
            self.dhalPlateHoleYnbr = self._HB_TARGET_6_SD_YDIR_NBR
            self.HB_WIDTH_X_SCALE = self._HB_TARGET_6_SD_X_MAX / (self.dhalPlateHoleXnbr-1);
            self.HB_HEIGHT_Y_SCALE = self._HB_TARGET_6_SD_Y_MAX / (self.dhalPlateHoleYnbr-1);
        else:
            self.dhalPlatePicOneWholeBatch = self._HB_TARGET_96_SD_BATCH_MAX;
            self.dhalPlateHoleXnbr = self._HB_TARGET_96_SD_XDIR_NBR
            self.dhalPlateHoleYnbr = self._HB_TARGET_96_SD_YDIR_NBR
            self.HB_WIDTH_X_SCALE = self._HB_TARGET_96_SD_X_MAX / (self.dhalPlateHoleXnbr-1);
            self.HB_HEIGHT_Y_SCALE = self._HB_TARGET_96_SD_Y_MAX / (self.dhalPlateHoleYnbr-1);
        return TUP_SUCCESS  
    
    #calibAxis需要按照坐标系存入
    #calibAxis = [0, 0, 0, 0]
    #一旦坐标系确定以后，需要及时更新坐标旋转，待完善
    def tup_dhal_plate_update_calib(self, calibAxis):
        if (calibAxis[0] !=0 or calibAxis[1] !=0 or calibAxis[2] !=0 or calibAxis[3] !=0):
            self.dhalPlateCaliPosInUm = calibAxis
            self.HB_WIDTH_X_SCALE = (self.dhalPlateCaliPosInUm[2] - self.dhalPlateCaliPosInUm[0]) / (self.dhalPlateHoleXnbr-1);
            self.HB_HEIGHT_Y_SCALE = (self.dhalPlateCaliPosInUm[3] - self.dhalPlateCaliPosInUm[1]) / (self.dhalPlateHoleYnbr-1);
            return TUP_SUCCESS
        else:
            #不做任何操作
            return TUP_FAILURE
    

    '''
    #
    # 马达坐标处理过程
    #
    '''
    def tup_dhal_plate_move_dir_x(self):
        pass



    '''
    #
    # 孔位变换标签
    #
    '''
    _DHAL_PLATE_CFG_HB96 = ['A0', 'A1', 'A2', 'A3', 'A4','A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',\
                           'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12',\
                           'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12',\
                           'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12',\
                           'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12',\
                           'F1', 'F2', 'F3','F4', 'F5', 'F6', 'F7', 'F8' ,'F9', 'F10', 'F11', 'F12',\
                           'G1', 'G2', 'G3', 'G4','G5','G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12',\
                           'H1', 'H2', 'H3','H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12',\
                           ];
                           
    _DHAL_PLATE_CFG_HB48 = ['A0', 'A1', 'A2', 'A3', 'A4','A5', 'A6', 'A7', 'A8',\
                           'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8',\
                           'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8',\
                           'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8',\
                           'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8',\
                           'F1', 'F2', 'F3','F4', 'F5', 'F6', 'F7', 'F8',\
                           ];
                           
    _DHAL_PLATE_CFG_HB24 = ['A0', 'A1', 'A2', 'A3', 'A4','A5', 'A6',\
                           'B1', 'B2', 'B3', 'B4', 'B5', 'B6',\
                           'C1', 'C2', 'C3', 'C4', 'C5', 'C6',\
                           'D1', 'D2', 'D3', 'D4', 'D5', 'D6',\
                           ];
    _DHAL_PLATE_CFG_HB12 = ['A0', 'A1', 'A2', 'A3', 'A4',\
                           'B1', 'B2', 'B3', 'B4',\
                           'C1', 'C2', 'C3', 'C4',\
                           ];
    _DHAL_PLATE_CFG_HB6 = ['A0', 'A1', 'A2', 'A3',\
                         'B1', 'B2', 'B3',\
                          ];   
    #将index孔位转化为标签
    def tup_dhal_plate_index_to_hole_lable(self, index):
        if (self._HB_TARGET_TYPE == self._HB_TARGET_96_STANDARD):
            return self._DHAL_PLATE_CFG_HB96[index];
        if (self._HB_TARGET_TYPE == self._HB_TARGET_48_STANDARD):
            return self._DHAL_PLATE_CFG_HB48[index];
        if (self._HB_TARGET_TYPE == self._HB_TARGET_24_STANDARD):
            return self._DHAL_PLATE_CFG_HB24[index];
        if (self._HB_TARGET_TYPE == self._HB_TARGET_12_STANDARD):
            return self._DHAL_PLATE_CFG_HB12[index];
        if (self._HB_TARGET_TYPE == self._HB_TARGET_6_STANDARD):
            return self._DHAL_PLATE_CFG_HB6[index];     
        else:
            return index;

    
    '''
    #
    # 图像处理函数
    # 必须 初始化本模块后才能使用，缺省参数不能使用
    #
    '''
    #获取弧长的参考基准长度，使用us为单位
    #实际是一度条件下的定点连线长度，考虑到误差，1度条件下不再去区分直线与弧线的差异
    def tup_dhal_plate_get_std_one_degree_radians_len_in_us(self):
        pi = 3.1415926
        if (self.dhalPlateTargetTypeCur == self._HB_TARGET_96_STANDARD):
            return (self._HB_TARGET_96_SD_HOLE_RAD *pi)/360
        elif (self.dhalPlateTargetTypeCur == self._HB_TARGET_48_STANDARD):
            return (self._HB_TARGET_48_SD_HOLE_RAD *pi)/360
        elif (self.dhalPlateTargetTypeCur == self._HB_TARGET_24_STANDARD):
            return (self._HB_TARGET_24_SD_HOLE_RAD *pi)/360
        elif (self.dhalPlateTargetTypeCur == self._HB_TARGET_12_STANDARD):
            return (self._HB_TARGET_12_SD_HOLE_RAD *pi)/360
        elif (self.dhalPlateTargetTypeCur == self._HB_TARGET_6_STANDARD):
            return (self._HB_TARGET_6_SD_HOLE_RAD *pi)/360
        else:
            return (self._HB_TARGET_96_SD_HOLE_RAD *pi)/360
    
    #半径
    def tup_dhal_plate_get_radians_len_in_us(self):
        if (self.dhalPlateTargetTypeCur == self._HB_TARGET_96_STANDARD):
            return self._HB_TARGET_96_SD_HOLE_RAD/2
        elif (self.dhalPlateTargetTypeCur == self._HB_TARGET_48_STANDARD):
            return self._HB_TARGET_48_SD_HOLE_RAD/2
        elif (self.dhalPlateTargetTypeCur == self._HB_TARGET_24_STANDARD):
            return self._HB_TARGET_24_SD_HOLE_RAD/2
        elif (self.dhalPlateTargetTypeCur == self._HB_TARGET_12_STANDARD):
            return self._HB_TARGET_12_SD_HOLE_RAD/2
        elif (self.dhalPlateTargetTypeCur == self._HB_TARGET_6_STANDARD):
            return self._HB_TARGET_6_SD_HOLE_RAD/2
        else:
            return self._HB_TARGET_96_SD_HOLE_RAD/2
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        