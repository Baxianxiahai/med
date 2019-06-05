'''
Created on 2019年6月3日

@author: Administrator
'''

from PkgL1vmHandler.ModVmCfg import *


#本模块将存储CEBS项目级的固定参数，不得使用工程参数、数据库表单等方式进行修改
TUP_CEBS_ERR_LOG_FILE_NAME_SET = r"cebsErrLog.txt"
TUP_CEBS_CMD_LOG_FILE_NAME_SET = r"cebsCmdLog.txt"
#FILE ATTRIBUTE
TUP_CEBS_FILE_ATT_NORMAL = 'normal';
TUP_CEBS_FILE_ATT_FLUORESCEN = 'flu';  #荧光 Fluorescen
TUP_CEBS_CFG_FILE_NAME = r"cebsConfig.ini";

#串口
TUP_CEBS_SPS_USB_DBG_CARD1 = 'Prolific USB-to-Serial Comm Port ('
#采购小卡，USB转串口卡片，手工连接杜邦线
TUP_CEBS_SPS_USB_DBG_CARD2 = 'Silicon Labs CP210x USB to UART Bridge ('
#确定设备选择哪一种型号的串口芯片，研发选择
TUP_CEBS_SPS_USB_CARD_SET = TUP_CEBS_SPS_USB_DBG_CARD2

#马达归零最大循环次数
#确保归零的时间预算 = 30秒 = 次数 x 采样间隔（0.2s)
TUP_CEBS_MOTOR_MAX_RETRY_TIMES = 150 #正常需要放置150次数，
TUP_CEBS_PILOT_WOKING_ROUNDS_MAX = 5;   #ROUNDS of auto-pilot run

#产品型号及机械结构的固定长度部分
TUP_CEBS_HW_TYPE_1  = 'G3VCD_TYPE1';
TUP_CEBS_HW_TYPE_2  = 'G3VCD_TYPE2';
TUP_CEBS_HW_TYPE_CUR = TUP_CEBS_HW_TYPE_1





