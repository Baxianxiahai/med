'''
Created on 2019年6月3日

@author: Administrator
'''

from PkgL3cebsDhal.cebsConfig import *
from PkgL1vmHandler.ModVmLayer import TUP_SUCCESS
    
class clsCebsDhPlate():
    #
    # 固定参数部分
    #
    #研发级决策，不能通过工程参数灵活配置    
    #MEACHNICAL HARDWARE PLATFORM SCOPE DEFINATION
    HB_MECHNICAL_PLATFORM_HWTYPE1_X_MAX = 140000;
    HB_MECHNICAL_PLATFORM_HWTYPE1_Y_MAX = 120000;
    HB_MECHNICAL_PLATFORM_HWTYPE2_X_MAX = 120000;
    HB_MECHNICAL_PLATFORM_HWTYPE2_Y_MAX = 100000;
    if (TUP_CEBS_HW_TYPE_CUR == TUP_CEBS_HW_TYPE_1):
        HB_MECHNICAL_PLATFORM_X_MAX = HB_MECHNICAL_PLATFORM_HWTYPE1_X_MAX;
        HB_MECHNICAL_PLATFORM_Y_MAX = HB_MECHNICAL_PLATFORM_HWTYPE1_Y_MAX;
    elif (TUP_CEBS_HW_TYPE_CUR == TUP_CEBS_HW_TYPE_2):
        HB_MECHNICAL_PLATFORM_X_MAX = HB_MECHNICAL_PLATFORM_HWTYPE2_X_MAX;
        HB_MECHNICAL_PLATFORM_Y_MAX = HB_MECHNICAL_PLATFORM_HWTYPE2_Y_MAX;
    else:
        HB_MECHNICAL_PLATFORM_X_MAX = HB_MECHNICAL_PLATFORM_HWTYPE1_X_MAX;
        HB_MECHNICAL_PLATFORM_Y_MAX = HB_MECHNICAL_PLATFORM_HWTYPE1_Y_MAX;
                    
    #CONTROL AXIS DIRECTION
    HB_TARGET_96_STANDARD = "96_STANDARD";
    HB_TARGET_96_SD_X_MAX = 120000;
    HB_TARGET_96_SD_Y_MAX = 90000;
    HB_TARGET_96_SD_BATCH_MAX = 96;
    HB_TARGET_96_SD_XDIR_NBR = 12;
    HB_TARGET_96_SD_YDIR_NBR = 8;
    HB_TARGET_96_SD_HOLE_DIS = 9000;  #in UM
    HB_TARGET_96_SD_HOLE_RAD = 6500;  #中值直径in UM，(顶+底)/2
     
    HB_TARGET_48_STANDARD = "48_STANDARD";
    HB_TARGET_48_SD_X_MAX = 120000;
    HB_TARGET_48_SD_Y_MAX = 90000;
    HB_TARGET_48_SD_BATCH_MAX = 48;
    HB_TARGET_48_SD_XDIR_NBR = 8;
    HB_TARGET_48_SD_YDIR_NBR = 6;
    HB_TARGET_48_SD_HOLE_DIS = 12000;  #in UM
    HB_TARGET_48_SD_HOLE_RAD = 8500;  #中值直径in UM，(顶+底)/2
     
    HB_TARGET_24_STANDARD = "24_STANDARD";
    HB_TARGET_24_SD_X_MAX = 120000;
    HB_TARGET_24_SD_Y_MAX = 90000;
    HB_TARGET_24_SD_BATCH_MAX = 24;
    HB_TARGET_24_SD_XDIR_NBR = 6;
    HB_TARGET_24_SD_YDIR_NBR = 4;
    HB_TARGET_24_SD_HOLE_DIS = 20000;  #in UM
    HB_TARGET_24_SD_HOLE_RAD = 15000;  #中值直径in UM，(顶+底)/2
     
    HB_TARGET_12_STANDARD = "12_STANDARD";
    HB_TARGET_12_SD_X_MAX = 120000;
    HB_TARGET_12_SD_Y_MAX = 90000;
    HB_TARGET_12_SD_BATCH_MAX = 12;
    HB_TARGET_12_SD_XDIR_NBR = 4;
    HB_TARGET_12_SD_YDIR_NBR = 3;
    HB_TARGET_12_SD_HOLE_DIS = 27000;  #in UM
    HB_TARGET_12_SD_HOLE_RAD = 19000;  #中值直径in UM，(顶+底)/2
     
    HB_TARGET_6_STANDARD = "6_STANDARD";
    HB_TARGET_6_SD_X_MAX = 120000;
    HB_TARGET_6_SD_Y_MAX = 90000;
    HB_TARGET_6_SD_BATCH_MAX = 6;
    HB_TARGET_6_SD_XDIR_NBR = 3;
    HB_TARGET_6_SD_YDIR_NBR = 2;
    HB_TARGET_6_SD_HOLE_DIS = 40000;  #in UM
    HB_TARGET_6_SD_HOLE_RAD = 30000;  #中值直径in UM，(顶+底)/2

    #
    # 可配置参数部分
    #
    #ACTION SELCTION
    HB_TARGET_TYPE_DEFAULT_SET = HB_TARGET_96_STANDARD;
    HB_TARGET_TYPE_CUR = HB_TARGET_TYPE_DEFAULT_SET;
    HB_PIC_ONE_WHOLE_BATCH = HB_TARGET_96_SD_BATCH_MAX;

    
    #
    # 临时参量部分
    #
    HB_HOLE_X_NUM = 0;          #HOW MANY BOARD HOLES， X DIRECTION
    HB_HOLE_Y_NUM = 0;          #HOW MANY BOARD HOLES，Y DIRECTION
    HB_WIDTH_X_SCALE = 0;       #HOW MANY BOARD HOLES， X DIRECTION
    HB_HEIGHT_Y_SCALE = 0;      #HOW MANY BOARD HOLES，Y DIRECTION
    
    '''
    *左下角的坐标，存在X1/Y1上， 右上角的坐标，存在X2/Y2上 
    *这种方式，符合坐标系的习惯：小值在X1/Y1中，大值在X2/Y2中
    LEFT-BOTTOM for X1/Y1 save in [0/1], RIGHT-UP for X2/Y2 save in [2/3]
    '''
    HB_CALI_POS_IN_UM = [0, 0, 0, 0];  #USING INT, um, 96 HOLES, POSITION OF = X1/Y1(LEFT-DOWN), X2/Y2(RIGHT-UP)
    #不断的维持本托盘的位置信息
    HB_CUR_POS_IN_UM = [0, 0];  #USING INT, um, POSITION X/Y AXIS
    
    
    
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
    # - 托盘可以在使用的过程中进行更迭。如果调换，只需要按照顺序调用tup_dhal_update_plate_context(), tup_dhal_update_plate_calib()即可。
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
    def tup_dhal_update_plate_context(self, plateType):
        self.HB_TARGET_TYPE_CUR = plateType
        if (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_96_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_96_SD_BATCH_MAX;
            self.HB_HOLE_X_NUM = self.HB_TARGET_96_SD_XDIR_NBR
            self.HB_HOLE_Y_NUM = self.HB_TARGET_96_SD_YDIR_NBR
            self.HB_WIDTH_X_SCALE = self.HB_TARGET_96_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
            self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_96_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
        elif (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_48_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_48_SD_BATCH_MAX;
            self.HB_HOLE_X_NUM = self.HB_TARGET_48_SD_XDIR_NBR
            self.HB_HOLE_Y_NUM = self.HB_TARGET_48_SD_YDIR_NBR
            self.HB_WIDTH_X_SCALE = self.HB_TARGET_48_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
            self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_48_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
        elif (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_24_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_24_SD_BATCH_MAX;
            self.HB_HOLE_X_NUM = self.HB_TARGET_24_SD_XDIR_NBR
            self.HB_HOLE_Y_NUM = self.HB_TARGET_24_SD_YDIR_NBR
            self.HB_WIDTH_X_SCALE = self.HB_TARGET_24_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
            self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_24_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
        elif (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_12_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_12_SD_BATCH_MAX;
            self.HB_HOLE_X_NUM = self.HB_TARGET_12_SD_XDIR_NBR
            self.HB_HOLE_Y_NUM = self.HB_TARGET_12_SD_YDIR_NBR
            self.HB_WIDTH_X_SCALE = self.HB_TARGET_12_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
            self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_12_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);            
        elif (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_6_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_6_SD_BATCH_MAX;
            self.HB_HOLE_X_NUM = self.HB_TARGET_6_SD_XDIR_NBR
            self.HB_HOLE_Y_NUM = self.HB_TARGET_6_SD_YDIR_NBR
            self.HB_WIDTH_X_SCALE = self.HB_TARGET_6_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
            self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_6_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
        else:
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_96_SD_BATCH_MAX;
            self.HB_HOLE_X_NUM = self.HB_TARGET_96_SD_XDIR_NBR
            self.HB_HOLE_Y_NUM = self.HB_TARGET_96_SD_YDIR_NBR
            self.HB_WIDTH_X_SCALE = self.HB_TARGET_96_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
            self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_96_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
        return TUP_SUCCESS  
    
    #calibAxis需要按照坐标系存入
    #calibAxis = [0, 0, 0, 0]
    def tup_dhal_update_plate_calib(self, calibAxis):
        if (calibAxis[0] !=0 or calibAxis[1] !=0 or calibAxis[2] !=0 or calibAxis[3] !=0):
            self.HB_CALI_POS_IN_UM = calibAxis
            self.HB_WIDTH_X_SCALE = (self.HB_CALI_POS_IN_UM[2] - self.HB_CALI_POS_IN_UM[0]) / (self.HB_HOLE_X_NUM-1);
            self.HB_HEIGHT_Y_SCALE = (self.HB_CALI_POS_IN_UM[3] - self.HB_CALI_POS_IN_UM[1]) / (self.HB_HOLE_Y_NUM-1);
            return TUP_SUCCESS
        else:
            #不做任何操作
            return TUP_FAILURE
    

    '''
    #
    # 马达坐标处理过程
    #
    '''
    def tup_dhal_move_dir_x(self):
        pass

    
    '''
    #
    # 图像处理函数
    # 必须 初始化本模块后才能使用，缺省参数不能使用
    #
    '''
    #获取弧长的参考基准长度，使用us为单位
    #实际是一度条件下的定点连线长度，考虑到误差，1度条件下不再去区分直线与弧线的差异
    def tup_dhal_get_std_one_degree_radians_len_in_us(self):
        pi = 3.1415926
        if (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_96_STANDARD):
            return (self.HB_TARGET_96_SD_HOLE_RAD *pi)/360
        elif (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_48_STANDARD):
            return (self.HB_TARGET_48_SD_HOLE_RAD *pi)/360
        elif (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_24_STANDARD):
            return (self.HB_TARGET_24_SD_HOLE_RAD *pi)/360
        elif (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_12_STANDARD):
            return (self.HB_TARGET_12_SD_HOLE_RAD *pi)/360
        elif (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_6_STANDARD):
            return (self.HB_TARGET_6_SD_HOLE_RAD *pi)/360
        else:
            return (self.HB_TARGET_96_SD_HOLE_RAD *pi)/360
    
    #半径
    def tup_dhal_get_radians_len_in_us(self):
        if (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_96_STANDARD):
            return self.HB_TARGET_96_SD_HOLE_RAD/2
        elif (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_48_STANDARD):
            return self.HB_TARGET_48_SD_HOLE_RAD/2
        elif (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_24_STANDARD):
            return self.HB_TARGET_24_SD_HOLE_RAD/2
        elif (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_12_STANDARD):
            return self.HB_TARGET_12_SD_HOLE_RAD/2
        elif (self.HB_TARGET_TYPE_CUR == self.HB_TARGET_6_STANDARD):
            return self.HB_TARGET_6_SD_HOLE_RAD/2
        else:
            return self.HB_TARGET_96_SD_HOLE_RAD/2
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        