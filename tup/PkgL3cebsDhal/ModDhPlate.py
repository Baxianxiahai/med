'''
Created on 2019年6月3日

@author: Administrator
'''

from PkgL3cebsDhal.cebsConfig import *
    
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
    print("DHPLATE: HB_MECHNICAL_PLATFORM_X_MAX = ", HB_MECHNICAL_PLATFORM_X_MAX)
                    
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
    HB_TARGET_TYPE = HB_TARGET_TYPE_DEFAULT_SET;
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
    HB_POS_IN_UM = [0, 0, 0, 0];  #USING INT, um, 96 HOLES, POSITION OF = X1/Y1(LEFT-DOWN), X2/Y2(RIGHT-UP)
    
    #初始化
    def __init__(self):    
        super(clsCebsDhPlate, self).__init__()

    
    #给上层提供服务的函数
    def tup_dhal_update_plate_context(self, plateType):
        pass
    
    #按照某种数据结构，将所有plate参数全部读取出来
    #可能需要放在Oprl模块中
    def tup_dhal_read_all_plate_par(self):
        pass
    
    #INIT PLATE PRODUCT TYPE, 初始化孔板产品型号
    def func_dhal_init_plate_product_type(self):
        if (self.HB_TARGET_TYPE == self.HB_TARGET_96_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_96_SD_BATCH_MAX;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_48_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_48_SD_BATCH_MAX;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_24_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_24_SD_BATCH_MAX;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_12_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_12_SD_BATCH_MAX;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_6_STANDARD):
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_6_SD_BATCH_MAX;
        else:
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_96_SD_BATCH_MAX;

    #INIT PLATE PARAMETER, 初始化孔板参数
    def func_dhal_init_plate_parameter(self):
        if (self.HB_WIDTH_X_SCALE == 0 or self.HB_HEIGHT_Y_SCALE == 0 or self.HB_HOLE_X_NUM == 0 or self.HB_HOLE_Y_NUM == 0):
            if (self.HB_TARGET_TYPE == self.HB_TARGET_96_STANDARD):
                self.HB_HOLE_X_NUM = self.HB_TARGET_96_SD_XDIR_NBR
                self.HB_HOLE_Y_NUM = self.HB_TARGET_96_SD_YDIR_NBR
                self.HB_WIDTH_X_SCALE = self.HB_TARGET_96_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
                self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_96_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
            elif (self.HB_TARGET_TYPE == self.HB_TARGET_48_STANDARD):
                self.HB_HOLE_X_NUM = self.HB_TARGET_48_SD_XDIR_NBR
                self.HB_HOLE_Y_NUM = self.HB_TARGET_48_SD_YDIR_NBR
                self.HB_WIDTH_X_SCALE = self.HB_TARGET_48_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
                self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_48_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
            elif (self.HB_TARGET_TYPE == self.HB_TARGET_24_STANDARD):
                self.HB_HOLE_X_NUM = self.HB_TARGET_24_SD_XDIR_NBR
                self.HB_HOLE_Y_NUM = self.HB_TARGET_24_SD_YDIR_NBR
                self.HB_WIDTH_X_SCALE = self.HB_TARGET_24_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
                self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_24_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
            elif (self.HB_TARGET_TYPE == self.HB_TARGET_12_STANDARD):
                self.HB_HOLE_X_NUM = self.HB_TARGET_12_SD_XDIR_NBR
                self.HB_HOLE_Y_NUM = self.HB_TARGET_12_SD_YDIR_NBR
                self.HB_WIDTH_X_SCALE = self.HB_TARGET_12_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
                self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_12_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
            elif (self.HB_TARGET_TYPE == self.HB_TARGET_6_STANDARD):
                self.HB_HOLE_X_NUM = self.HB_TARGET_6_SD_XDIR_NBR
                self.HB_HOLE_Y_NUM = self.HB_TARGET_6_SD_YDIR_NBR
                self.HB_WIDTH_X_SCALE = self.HB_TARGET_6_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
                self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_6_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
            else:
                self.HB_HOLE_X_NUM = self.HB_TARGET_96_SD_XDIR_NBR
                self.HB_HOLE_Y_NUM = self.HB_TARGET_96_SD_YDIR_NBR
                self.HB_WIDTH_X_SCALE = self.HB_TARGET_96_SD_X_MAX / (self.HB_HOLE_X_NUM-1);
                self.HB_HEIGHT_Y_SCALE = self.HB_TARGET_96_SD_Y_MAX / (self.HB_HOLE_Y_NUM-1);
        if (self.HB_POS_IN_UM[0] !=0 or self.HB_POS_IN_UM[1] !=0 or self.HB_POS_IN_UM[2] !=0 or self.HB_POS_IN_UM[3] !=0):
            #小坐标是左下角，大坐标是右上角
            xWidth = self.HB_POS_IN_UM[2] - self.HB_POS_IN_UM[0];
            yHeight = self.HB_POS_IN_UM[3] - self.HB_POS_IN_UM[1];
            self.HB_WIDTH_X_SCALE = xWidth / (self.HB_HOLE_X_NUM-1);
            self.HB_HEIGHT_Y_SCALE = yHeight / (self.HB_HOLE_Y_NUM-1);
        else:
            pass

    #UPDATE PLATE PARAMETERS, 更新孔板参数
    def func_dhal_update_plate_parameter(self):
        if (self.HB_TARGET_TYPE == self.HB_TARGET_96_STANDARD):
            self.HB_HOLE_X_NUM = self.HB_TARGET_96_SD_XDIR_NBR;
            self.HB_HOLE_Y_NUM = self.HB_TARGET_96_SD_YDIR_NBR;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_48_STANDARD):
            self.HB_HOLE_X_NUM = self.HB_TARGET_48_SD_XDIR_NBR;
            self.HB_HOLE_Y_NUM = self.HB_TARGET_48_SD_YDIR_NBR;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_24_STANDARD):
            self.HB_HOLE_X_NUM = self.HB_TARGET_24_SD_XDIR_NBR;
            self.HB_HOLE_Y_NUM = self.HB_TARGET_24_SD_YDIR_NBR;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_12_STANDARD):
            self.HB_HOLE_X_NUM = self.HB_TARGET_12_SD_XDIR_NBR;
            self.HB_HOLE_Y_NUM = self.HB_TARGET_12_SD_YDIR_NBR;
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_6_STANDARD):
            self.HB_HOLE_X_NUM = self.HB_TARGET_6_SD_XDIR_NBR;
            self.HB_HOLE_Y_NUM = self.HB_TARGET_6_SD_YDIR_NBR;
        else:
            self.HB_HOLE_X_NUM = self.HB_TARGET_96_SD_XDIR_NBR;
            self.HB_HOLE_Y_NUM = self.HB_TARGET_96_SD_YDIR_NBR;
        self.HB_WIDTH_X_SCALE = (self.HB_POS_IN_UM[2] - self.HB_POS_IN_UM[0]) / (self.HB_HOLE_X_NUM-1);
        self.HB_HEIGHT_Y_SCALE = (self.HB_POS_IN_UM[3] - self.HB_POS_IN_UM[1]) / (self.HB_HOLE_Y_NUM-1);
    
    #选择工作盘片
    #只有在更换盘片且在GPAR中才能选择
    def func_dhal_select_plate_board_type(self, option):
        if (option == 96):
            self.HB_TARGET_TYPE = self.HB_TARGET_96_STANDARD;
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_96_SD_BATCH_MAX;
        elif (option == 48):
            self.HB_TARGET_TYPE = self.HB_TARGET_48_STANDARD;
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_48_SD_BATCH_MAX;
        elif (option == 24):
            self.HB_TARGET_TYPE = self.HB_TARGET_24_STANDARD;
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_24_SD_BATCH_MAX;
        elif (option == 12):
            self.HB_TARGET_TYPE = self.HB_TARGET_12_STANDARD;
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_12_SD_BATCH_MAX;
        elif (option == 6):
            self.HB_TARGET_TYPE = self.HB_TARGET_6_STANDARD;
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_6_SD_BATCH_MAX;
        else:
            self.HB_TARGET_TYPE = self.HB_TARGET_96_STANDARD;
            self.HB_PIC_ONE_WHOLE_BATCH = self.HB_TARGET_96_SD_BATCH_MAX;
    
    #获取弧长的参考基准长度，使用us为单位
    #实际是一度条件下的定点连线长度，考虑到误差，1度条件下不再去区分直线与弧线的差异
    def tup_dhal_get_std_one_degree_radians_len_in_us(self):
        pi = 3.1415926
        if (self.HB_TARGET_TYPE == self.HB_TARGET_96_STANDARD):
            return (self.HB_TARGET_96_SD_HOLE_RAD *pi)/360
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_48_STANDARD):
            return (self.HB_TARGET_48_SD_HOLE_RAD *pi)/360
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_24_STANDARD):
            return (self.HB_TARGET_24_SD_HOLE_RAD *pi)/360
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_12_STANDARD):
            return (self.HB_TARGET_12_SD_HOLE_RAD *pi)/360
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_6_STANDARD):
            return (self.HB_TARGET_6_SD_HOLE_RAD *pi)/360
        else:
            return (self.HB_TARGET_96_SD_HOLE_RAD *pi)/360
    
    #半径
    def tup_dhal_get_radians_len_in_us(self):
        if (self.HB_TARGET_TYPE == self.HB_TARGET_96_STANDARD):
            return self.HB_TARGET_96_SD_HOLE_RAD/2
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_48_STANDARD):
            return self.HB_TARGET_48_SD_HOLE_RAD/2
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_24_STANDARD):
            return self.HB_TARGET_24_SD_HOLE_RAD/2
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_12_STANDARD):
            return self.HB_TARGET_12_SD_HOLE_RAD/2
        elif (self.HB_TARGET_TYPE == self.HB_TARGET_6_STANDARD):
            return self.HB_TARGET_6_SD_HOLE_RAD/2
        else:
            return self.HB_TARGET_96_SD_HOLE_RAD/2
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        