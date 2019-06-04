'''
Created on 2019年6月3日

@author: Administrator
'''

from PkgL3cebsDhal.cebsConfig import *

class clsCebsDhMotosps():
    #
    # 固定配置参数部分
    #
    SPS_SHK_HAND = '设备握手（shake_hand）'
    SPS_SET_WK_MODE = '设置工作模式（set_wk_mode）'
    SPS_SET_ACC = '设置加速度（set_acc）'
    SPS_SET_DEACC = '设置减速度（set_deacc）'
    SPS_SET_PPC = '设置一圈步伐（set_pules_per_cycle）'
    SPS_SET_MV_SPD = '设置移动速度（set_mv_spd）'
    SPS_SET_ZO_SPD = '设置归零速度（set_zero_spd）'
    SPS_SET_ZO_ACC = '设置归零加速度（set_zero_acc）'
    SPS_SET_INT_SP = '设置靠边后退步伐（set_int_steps）'
    SPS_MV_PULS = '移动步伐（mv_pules）'
    SPS_MV_SPD = '移动速度（mv_spd）'
    SPS_MV_ZERO = '归零（mv_zero）'
    SPS_STP_IMD = '立即停止（stop_imd）'
    SPS_STP_NOR = '缓慢停止（stop_nor)'
    SPS_INQ_EN = '查询激活状态（inq_enable）'
    SPS_INQ_RUN = '查询运行状态（inq_run）'
    SPS_INQ_STATUS = '查询一般状态（inq_status）'
    SPS_TEST_PULES = '测试脉冲数（test_pules）'
    SPS_SET_EXTI_DELAY_TIME = '设置限位器触发迟滞（set_exti_delay_time）'
    SPS_SHK_HAND_CMID = 0x20
    SPS_SET_WK_MODE_CMID = 0x21
    SPS_SET_ACC_CMID = 0x22
    SPS_SET_DEACC_CMID = 0x23
    SPS_SET_PPC_CMID = 0x24
    SPS_SET_MV_SPD_CMID = 0x25
    SPS_SET_ZO_SPD_CMID = 0x26
    SPS_SET_ZO_ACC_CMID = 0x27
    SPS_SET_INT_SP_CMID = 0x28
    SPS_MV_PULS_CMID = 0x30
    SPS_MV_SPD_CMID = 0x31
    SPS_MV_ZERO_CMID = 0x32
    SPS_STP_IMD_CMID = 0x33
    SPS_STP_NOR_CMID = 0x34
    SPS_INQ_EN_CMID = 0x35
    SPS_INQ_RUN_CMID = 0x36
    SPS_INQ_STATUS_CMID = 0x37
    SPS_TEST_PULES_CMID = 0x38
    SPS_SET_EXTI_DELAY_TIME_CMID = 0x39
    SPS_CHECK_PSWD_CMID = 0x40
    #
    MOTOR_STEPS_PER_ROUND = 12800   #NF0
    MOTOR_DIS_MM_PER_ROUND = 3.1415926*20*1.05
    MOTOR_STEPS_PER_DISTANCE_MM = MOTOR_STEPS_PER_ROUND / MOTOR_DIS_MM_PER_ROUND
    MOTOR_STEPS_PER_DISTANCE_UM = MOTOR_STEPS_PER_ROUND / MOTOR_DIS_MM_PER_ROUND / 1000    
    
    def __init__(self):    
        super(clsCebsDhMotosps, self).__init__()  
    




