'''
Created on 2019年6月3日

@author: Administrator
'''

#本模块将存储CEBS项目级的固定参数，不得使用工程参数、数据库表单等方式进行修改
_TUP_CEBS_ERR_LOG_FILE_NAME_SET = r"cebsErrLog.txt"
_TUP_CEBS_CMD_LOG_FILE_NAME_SET = r"cebsCmdLog.txt"
#FILE ATTRIBUTE
_TUP_CEBS_FILE_ATT_NORMAL = 'normal';
_TUP_CEBS_FILE_ATT_FLUORESCEN = 'flu';  #荧光 Fluorescen
_TUP_CEBS_CFG_FILE_NAME = r"cebsConfig.ini";

#串口
_TUP_CEBS_SPS_USB_DBG_CARD1 = 'Prolific USB-to-Serial Comm Port ('
#采购小卡，USB转串口卡片，手工连接杜邦线
_TUP_CEBS_SPS_USB_DBG_CARD2 = 'Silicon Labs CP210x USB to UART Bridge ('
#确定设备选择哪一种型号的串口芯片，研发选择
_TUP_CEBS_SPS_USB_CARD_SET = _TUP_CEBS_SPS_USB_DBG_CARD2

#马达归零最大循环次数
#确保归零的时间预算 = 30秒 = 次数 x 采样间隔（0.2s)
_TUP_CEBS_MOTOR_MAX_RETRY_TIMES = 150 #正常需要放置150次数，
_TUP_CEBS_PILOT_WOKING_ROUNDS_MAX = 5   #ROUNDS of auto-pilot run

#产品型号及机械结构的固定长度部分
_TUP_CEBS_HW_TYPE_1  = 'G3VCD_TYPE1'
_TUP_CEBS_HW_TYPE_2  = 'G3VCD_TYPE2'
_TUP_CEBS_HW_TYPE_CUR = _TUP_CEBS_HW_TYPE_1

#Ubuntu下图片存储的绝对路径Prefix目录
_TUP_CEBS_UBUNTU_FILE_STORAGE_DIR_PREFIX = '/var/www/'

#玩意数据库批次号分配失败，则分配的批次号从这里开始
_TUP_CEBS_FAIL_BATCH_START  = 1000000

















    




