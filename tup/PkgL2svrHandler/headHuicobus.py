'''
Created on 2019年5月31日

@author: Administrator
'''

#HUICOBUS CMDID公共定义: HEAD DEFINATION
#获取参数=》未来将直接通过HST进行读取
TUP_HHD_CMDID_SYS_GET_CONFIG_REQ        = 0x0A00
TUP_HHD_CMDID_SYS_GET_CONFIG_RESP       = 0x0A80
#设置参数
TUP_HHD_CMDID_SYS_SET_CONFIG_REQ        = 0x0A01
TUP_HHD_CMDID_SYS_SET_CONFIG_RESP       = 0x0A81
#UI独立通知TUP
TUP_HHD_CMDID_SYS_UI_START_REQ          = 0x0A02
TUP_HHD_CMDID_SYS_UI_START_RESP         = 0x0A82
#TUP更新状态
TUP_HHD_CMDID_SYS_STATUS_TRIG           = 0x0A83
#TUP更新错误
TUP_HHD_CMDID_SYS_ERROR_TRIG            = 0x0A84
#强制重启TUP软件
TUP_HHD_CMDID_SYS_FRC_RESTART_REQ       = 0x0A05
TUP_HHD_CMDID_SYS_FRC_RESTART_RESP      = 0x0A85

#GPAR
TUP_HHD_CMDID_SYS_GPAR_START_REQ        = 0x0A10
TUP_HHD_CMDID_SYS_GPAR_START_RESP       = 0x0A90
TUP_HHD_CMDID_SYS_GPAR_SAVE_REQ         = 0x0A11
TUP_HHD_CMDID_SYS_GPAR_SAVE_RESP        = 0x0A91
TUP_HHD_CMDID_SYS_GPAR_EXIT_REQ         = 0x0A12
TUP_HHD_CMDID_SYS_GPAR_EXIT_RESP        = 0x0A92
TUP_HHD_CMDID_SYS_GPAR_PIC_TRAIN_REQ    = 0x0A13
TUP_HHD_CMDID_SYS_GPAR_PIC_TRAIN_RESP   = 0x0A93
TUP_HHD_CMDID_SYS_GPAR_PIC_FCC_REQ      = 0x0A14
TUP_HHD_CMDID_SYS_GPAR_PIC_FCC_RESP     = 0x0A94
#CALIB
TUP_HHD_CMDID_SYS_CALI_START_REQ        = 0x0A20
TUP_HHD_CMDID_SYS_CALI_START_RESP       = 0x0AA0
TUP_HHD_CMDID_SYS_CALI_MOMV_DIR_REQ     = 0x0A21
TUP_HHD_CMDID_SYS_CALI_MOMV_DIR_RESP    = 0x0AA1
TUP_HHD_CMDID_SYS_CALI_EXIT_REQ         = 0x0A22
TUP_HHD_CMDID_SYS_CALI_EXIT_RESP        = 0x0AA2
TUP_HHD_CMDID_SYS_CALI_MOFM_REQ         = 0x0A23
TUP_HHD_CMDID_SYS_CALI_MOFM_RESP        = 0x0AA3
TUP_HHD_CMDID_SYS_CALI_MOMV_START_REQ        = 0x0A24
TUP_HHD_CMDID_SYS_CALI_MOMV_START_RESP       = 0x0AA4
TUP_HHD_CMDID_SYS_CALI_MOMV_HOLEN_REQ        = 0x0A25
TUP_HHD_CMDID_SYS_CALI_MOMV_HOLEN_RESP       = 0x0AA5
TUP_HHD_CMDID_SYS_CALI_PILOT_START_REQ       = 0x0A26
TUP_HHD_CMDID_SYS_CALI_PILOT_START_RESP      = 0x0AA6
TUP_HHD_CMDID_SYS_CALI_PILOT_STOP_REQ        = 0x0A27
TUP_HHD_CMDID_SYS_CALI_PILOT_STOP_RESP       = 0x0AA7
TUP_HHD_CMDID_SYS_CALI_RIGHT_UP_SET_REQ      = 0x0A28
TUP_HHD_CMDID_SYS_CALI_RIGHT_UP_SET_RESP     = 0x0AA8
TUP_HHD_CMDID_SYS_CALI_LEFT_BOT_SET_REQ      = 0x0A29
TUP_HHD_CMDID_SYS_CALI_LEFT_BOT_SET_RESP     = 0x0AA9
TUP_HHD_CMDID_SYS_CALI_PIC_CAP_HOLEN_REQ     = 0x0A2A
TUP_HHD_CMDID_SYS_CALI_PIC_CAP_HOLEN_RESP    = 0x0AAA
#CTRL_SCHD
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_START_REQ    = 0x0A30
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_START_RESP   = 0x0AB0
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_TRIG         = 0x0AB1
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_STOP_REQ     = 0x0A32
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_STOP_RESP    = 0x0AB2
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_START_REQ    = 0x0A33
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_START_RESP   = 0x0AB3
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_TRIG         = 0x0AB4
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_STOP_REQ     = 0x0A35
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_STOP_RESP    = 0x0AB5
TUP_HHD_CMDID_SYS_CTRL_SCHD_MV_ZERO_REQ         = 0x0A36
TUP_HHD_CMDID_SYS_CTRL_SCHD_MV_ZERO_RESP        = 0x0AB6
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_START_REQ    = 0x0A37
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_START_RESP   = 0x0AB7
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_TRIG         = 0x0AB8
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_STOP_REQ     = 0x0A39
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_STOP_RESP    = 0x0AB9
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_START_REQ    = 0x0A3A
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_START_RESP   = 0x0ABA
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_TRIG         = 0x0ABB
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_STOP_REQ     = 0x0A3C
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_STOP_RESP    = 0x0ABC
#MENG
TUP_HHD_CMDID_SYS_MENG_START_REQ        = 0x0A40
TUP_HHD_CMDID_SYS_MENG_START_RESP       = 0x0AC0
TUP_HHD_CMDID_SYS_MENG_EXIT_REQ         = 0x0A41
TUP_HHD_CMDID_SYS_MENG_EXIT_RESP        = 0x0AC1
TUP_HHD_CMDID_SYS_MENG_COMMAND_REQ      = 0x0A42
TUP_HHD_CMDID_SYS_MENG_COMMAND_RESP     = 0x0AC2
TUP_HHD_CMDID_SYS_MENG_COMMAND_TRIG     = 0x0AC3

# THIS IS ONLY FOR INFO: MQTT HEADER TUP TO UIP
TUP_HHD_HLC_MESSAGE_HEADER_TUP2UIP = {
    'srcNode':'HUICOBUS_MQTT_NODEID_TUPSVR',
    'destNode':'HUICOBUS_MQTT_NODEID_TUPSVR',
    'srcId':'HUICOBUS_MQTT_CLIENTID_TUPENTRY',
    'destId':'HUICOBUS_MQTT_CLIENTID_TUPROUTER',
    'topicId':'HUICOBUS_MQTT_TOPIC_TUP2UIP',
    'cmdId':391,
    'cmdValue':2,
    'hlContent': {
        'snrId': 12,
        'validFlag': 1,
        'errCode': 0,
        'cmdTestValue1': 1,
        'cmdTestValue2': 0,
        'cmdTestValue3': 0,
        'cmdTestValue4': 0,
        }
    }

#THIS IS ONLY FOR INFO: MQTT HEADER UIP TO TUP
TUP_HHD_HLC_MESSAGE_HEADER_UIP2TUP = {
    'srcNode':'HUICOBUS_MQTT_NODEID_TUPSVR',
    'destNode':'HUICOBUS_MQTT_NODEID_TUPSVR',
    'srcId':'HUICOBUS_MQTT_CLIENTID_TUPROUTER',
    'destId':'HUICOBUS_MQTT_CLIENTID_TUPENTRY',
    'topicId':'HUICOBUS_MQTT_TOPIC_UIP2TUP',
    'cmdId':391,
    'cmdValue':2,
    'hlContent': {
        'snrId': 12,
        'validFlag': 1,
        'errCode': 0,
        'cmdTestValue1': 1,
        'cmdTestValue2': 0,
        'cmdTestValue3': 0,
        'cmdTestValue4': 0,
        }
    }

#HLC的消息格式(hlContent)
#TUP_HHD_CMDID_SYS_GET_CONFIG_REQ        = 0x0A00
TUP_HHD_HLC_SYS_GET_CONFIG_REQ = {
    'parameter': {
        'type':'query',
        'lang':'ch',
        'user':'null',
        'ts':1559381384274,
        }
    }

#TUP_HHD_CMDID_SYS_GET_CONFIG_RESP       = 0x0A80
TUP_HHD_HLC_SYS_GET_CONFIG_RESP = {
    'parameter': {
        'groups': [
            {
                'groupname': '版型选择', 
                'list': [
                    {'paraname': '托盘类型', 'type': 'choice', 'max': '', 'min': '', 'value': '0', 'items': ['96孔板', '48孔板', '24孔板', '12孔板', '6孔板', '384孔板'], 'note': 'choice info'}]
            }, 
            {
                'groupname': '全局参数设置', 
                'list': [
                    {'paraname': '拍照后自动识别', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]
             }, 
            {
                'groupname': '计划任务设置', 
                'list': [
                    {'paraname': '启动计划任务', 'type': 'checkbox', 'max': '', 'min': '', 'value': False, 'note': 'Note info'}, 
                    {'paraname': '定时自动拍照', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '定点拍照', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '定时拍照时间间隔', 'type': 'int', 'max': '100', 'min': '0', 'value': 1, 'note': '单位：秒'}]
            }, 
            {
                'groupname': '坐标系设置', 
                'list': [
                    {'paraname': '左下X坐标', 'type': 'int', 'max': '37000', 'min': '0', 'value': 100, 'note': '单位：UM'}, 
                    {'paraname': '左下Y坐标',  'type': 'int', 'max': '37000', 'min': '0', 'value': 30, 'note': '单位：UM'}, 
                    {'paraname': '右上X坐标', 'type': 'int', 'max': '157000', 'min': '120000', 'value': 20, 'note': '单位：UM'}, 
                    {'paraname': '右上Y坐标',  'type': 'int', 'max': '127000', 'min': '90000', 'value': 10, 'note': '单位：UM'}]
            }, 
            {
                'groupname': '图片识别参数设置', 
                'list': [
                    {'paraname': '小尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：像素'}, 
                    {'paraname': '小-中尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：像素'}, 
                    {'paraname': '中-大尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 500, 'note': '单位：像素'}, 
                    {'paraname': '大尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 1000, 'note': '单位：像素'}, 
                    {'paraname': '输出图像叠加标定', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]
            }, 
            {
                'groupname': '视频参数设置', 
                'list': [
                    {'paraname': '开启视频记录', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '视频时长', 'type': 'int', 'max': '60', 'min': '0', 'value': 3, 'note': '单位：秒'}]
            }, 
            {
                'groupname': '图片存储位置', 
                'list': [
                    {'paraname': '未识别照片目录', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_origin/', 'note': 'Note info'}, 
                    {'paraname': '已识别照片目录', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_middle/', 'note': 'Note info'}]
            },
            {
                'groupname': '马达参数', 
                'list': [
                    {'paraname': '增速加速度', 'type': 'int', 'max': '', 'min': '', 'value': 10, 'note': '单位：metre every second square second'}, 
                    {'paraname': '减速加速度', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, 
                    {'paraname': '移动速度', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, 
                    {'paraname': '归零速度', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：metre every second'}, 
                    {'paraname': '归零减速度', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：metre every second'}, 
                    {'paraname': '回退步数', 'type': 'int', 'max': '', 'min': '', 'value': 22, 'note': '单位：步'}]
            }]
        },
    'ts':1559381384274,
    }

# TUP_HHD_CMDID_SYS_SET_CONFIG_REQ        = 0x0A01
TUP_HHD_HLC_SYS_SET_CONFIG_REQ = {
    'parameter': {
        'groups': [
            {
                'groupname': '版型选择', 
                'list': [
                    {'paraname': '托盘类型', 'type': 'choice', 'max': '', 'min': '', 'value': '0', 'items': ['96孔板', '48孔板', '24孔板', '12孔板', '6孔板', '384孔板'], 'note': 'choice info'}]
            }, 
            {
                'groupname': '全局参数设置', 
                'list': [
                    {'paraname': '拍照后自动识别', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]
             }, 
            {
                'groupname': '计划任务设置', 
                'list': [
                    {'paraname': '启动计划任务', 'type': 'checkbox', 'max': '', 'min': '', 'value': False, 'note': 'Note info'}, 
                    {'paraname': '定时自动拍照', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '定点拍照', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '定时拍照时间间隔', 'type': 'int', 'max': '100', 'min': '0', 'value': 1, 'note': '单位：秒'}]
            }, 
            {
                'groupname': '坐标系设置', 
                'list': [
                    {'paraname': '左下X坐标', 'type': 'int', 'max': '37000', 'min': '0', 'value': 100, 'note': '单位：UM'}, 
                    {'paraname': '左下Y坐标',  'type': 'int', 'max': '37000', 'min': '0', 'value': 30, 'note': '单位：UM'}, 
                    {'paraname': '右上X坐标', 'type': 'int', 'max': '157000', 'min': '120000', 'value': 20, 'note': '单位：UM'}, 
                    {'paraname': '右上Y坐标',  'type': 'int', 'max': '127000', 'min': '90000', 'value': 10, 'note': '单位：UM'}]
            }, 
            {
                'groupname': '图片识别参数设置', 
                'list': [
                    {'paraname': '小尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：像素'}, 
                    {'paraname': '小-中尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：像素'}, 
                    {'paraname': '中-大尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 500, 'note': '单位：像素'}, 
                    {'paraname': '大尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 1000, 'note': '单位：像素'}, 
                    {'paraname': '输出图像叠加标定', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]
            }, 
            {
                'groupname': '视频参数设置', 
                'list': [
                    {'paraname': '开启视频记录', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '视频时长', 'type': 'int', 'max': '60', 'min': '0', 'value': 3, 'note': '单位：秒'}]
            }, 
            {
                'groupname': '图片存储位置', 
                'list': [
                    {'paraname': '未识别照片目录', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_origin/', 'note': 'Note info'}, 
                    {'paraname': '已识别照片目录', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_middle/', 'note': 'Note info'}]
            },
            {
                'groupname': '马达参数', 
                'list': [
                    {'paraname': '增速加速度', 'type': 'int', 'max': '', 'min': '', 'value': 10, 'note': '单位：metre every second square second'}, 
                    {'paraname': '减速加速度', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, 
                    {'paraname': '移动速度', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, 
                    {'paraname': '归零速度', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：metre every second'}, 
                    {'paraname': '归零减速度', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：metre every second'}, 
                    {'paraname': '回退步数', 'type': 'int', 'max': '', 'min': '', 'value': 22, 'note': '单位：步'}]
            }]
        },
    'ts':1559381384274,
    }

# TUP_HHD_CMDID_SYS_SET_CONFIG_RESP       = 0x0A81
TUP_HHD_HLC_SYS_SET_CONFIG_RESP = {
    'parameter': {
        'groups': [
            {
                'groupname': '版型选择', 
                'list': [
                    {'paraname': '托盘类型', 'type': 'choice', 'max': '', 'min': '', 'value': '0', 'items': ['96孔板', '48孔板', '24孔板', '12孔板', '6孔板', '384孔板'], 'note': 'choice info'}]
            }, 
            {
                'groupname': '全局参数设置', 
                'list': [
                    {'paraname': '拍照后自动识别', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]
             }, 
            {
                'groupname': '计划任务设置', 
                'list': [
                    {'paraname': '启动计划任务', 'type': 'checkbox', 'max': '', 'min': '', 'value': False, 'note': 'Note info'}, 
                    {'paraname': '定时自动拍照', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '定点拍照', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '定时拍照时间间隔', 'type': 'int', 'max': '100', 'min': '0', 'value': 1, 'note': '单位：秒'}]
            }, 
            {
                'groupname': '坐标系设置', 
                'list': [
                    {'paraname': '左下X坐标', 'type': 'int', 'max': '37000', 'min': '0', 'value': 100, 'note': '单位：UM'}, 
                    {'paraname': '左下Y坐标',  'type': 'int', 'max': '37000', 'min': '0', 'value': 30, 'note': '单位：UM'}, 
                    {'paraname': '右上X坐标', 'type': 'int', 'max': '157000', 'min': '120000', 'value': 20, 'note': '单位：UM'}, 
                    {'paraname': '右上Y坐标',  'type': 'int', 'max': '127000', 'min': '90000', 'value': 10, 'note': '单位：UM'}]
            }, 
            {
                'groupname': '图片识别参数设置', 
                'list': [
                    {'paraname': '小尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：像素'}, 
                    {'paraname': '小-中尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：像素'}, 
                    {'paraname': '中-大尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 500, 'note': '单位：像素'}, 
                    {'paraname': '大尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 1000, 'note': '单位：像素'}, 
                    {'paraname': '输出图像叠加标定', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]
            }, 
            {
                'groupname': '视频参数设置', 
                'list': [
                    {'paraname': '开启视频记录', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '视频时长', 'type': 'int', 'max': '60', 'min': '0', 'value': 3, 'note': '单位：秒'}]
            }, 
            {
                'groupname': '图片存储位置', 
                'list': [
                    {'paraname': '未识别照片目录', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_origin/', 'note': 'Note info'}, 
                    {'paraname': '已识别照片目录', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_middle/', 'note': 'Note info'}]
            },
            {
                'groupname': '马达参数', 
                'list': [
                    {'paraname': '增速加速度', 'type': 'int', 'max': '', 'min': '', 'value': 10, 'note': '单位：metre every second square second'}, 
                    {'paraname': '减速加速度', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, 
                    {'paraname': '移动速度', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, 
                    {'paraname': '归零速度', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：metre every second'}, 
                    {'paraname': '归零减速度', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：metre every second'}, 
                    {'paraname': '回退步数', 'type': 'int', 'max': '', 'min': '', 'value': 22, 'note': '单位：步'}]
            }]
        },
    'ts':1559381384274,
    }



# #UI独立通知TUP
# TUP_HHD_CMDID_SYS_UI_START_REQ          = 0x0A02
TUP_HHD_HLC_SYS_UI_START_REQ = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_UI_START_RESP         = 0x0A82
TUP_HHD_HLC_SYS_UI_START_RESP = {
    'parameter': {
        'motor_x_status': 1,   #0:NOK, 1:OK
        'motor_y_status': 1,   #0:NOK, 1:OK
        'camera_status': 1,    #0:NOK, 1:OK
        }
    }

#TUP更新状态
#TUP_HHD_CMDID_SYS_STATUS_TRIG           = 0x0A83
TUP_HHD_CMDID_SYS_STATUS_TRIG = {
    'parameter': {
        'status': 'I like to say something!',
        }    
    }


#TUP更新错误
#TUP_HHD_CMDID_SYS_ERROR_TRIG            = 0x0A84
TUP_HHD_CMDID_SYS_ERROR_TRIG = {
    'parameter': {
        'error': 'I like to say something!',
        }    
    }


#强制重启TUP软件
#TUP_HHD_CMDID_SYS_FRC_RESTART_REQ       = 0x0A05
TUP_HHD_CMDID_SYS_FRC_RESTART_REQ = {
    'parameter': {}
    }


#TUP_HHD_CMDID_SYS_FRC_RESTART_RESP      = 0x0A85
TUP_HHD_CMDID_SYS_FRC_RESTART_RESP = {
    'parameter': {}
    }


# #GPAR
# TUP_HHD_CMDID_SYS_GPAR_START_REQ        = 0x0A10
TUP_HHD_HLC_SYS_GPAR_START_REQ = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_GPAR_START_RESP       = 0x0A90
TUP_HHD_HLC_SYS_GPAR_START_RESP = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_GPAR_SAVE_REQ         = 0x0A11
TUP_HHD_HLC_SYS_GPAR_SAVE_REQ = {
    'parameter': {}
    }
# TUP_HHD_CMDID_SYS_GPAR_SAVE_RESP        = 0x0A91
TUP_HHD_HLC_SYS_GPAR_SAVE_RESP = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_GPAR_EXIT_REQ         = 0x0A12
TUP_HHD_HLC_SYS_GPAR_EXIT_REQ = {
    'parameter': {}
    }
# TUP_HHD_CMDID_SYS_GPAR_EXIT_RESP        = 0x0A92
TUP_HHD_HLC_SYS_GPAR_EXIT_RESP = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_GPAR_PIC_TRAIN_REQ    = 0x0A13
TUP_HHD_CMDID_SYS_GPAR_PIC_TRAIN_REQ = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_GPAR_PIC_TRAIN_RESP   = 0x0A93
TUP_HHD_CMDID_SYS_GPAR_PIC_TRAIN_RESP = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_GPAR_PIC_FCC_REQ      = 0x0A14
TUP_HHD_CMDID_SYS_GPAR_PIC_FCC_REQ = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_GPAR_PIC_FCC_RESP     = 0x0A94
TUP_HHD_CMDID_SYS_GPAR_PIC_FCC_RESP = {
    'parameter': {}
    }

# #CALIB
# TUP_HHD_CMDID_SYS_CALI_START_REQ        = 0x0A20
TUP_HHD_HLC_SYS_CALI_START_REQ = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_CALI_START_RESP       = 0x0AA0
TUP_HHD_HLC_SYS_CALI_START_RESP = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CALI_MOMV_DIR_REQ     = 0x0A21
TUP_HHD_CMDID_SYS_CALI_MOMV_DIR_REQ = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_CALI_MOMV_DIR_RESP    = 0x0AA1
TUP_HHD_CMDID_SYS_CALI_MOMV_DIR_RESP = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_CALI_EXIT_REQ         = 0x0A22
TUP_HHD_HLC_SYS_CALI_EXIT_REQ = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_CALI_EXIT_RESP        = 0x0AA2
TUP_HHD_HLC_SYS_CALI_EXIT_RESP = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_CALI_MOFM_REQ         = 0x0A23
TUP_HHD_HLC_SYS_CALI_MOFM_REQ = {
    'parameter': {
        'expected_delta_x_um': 10,
        'expected_delta_y_um': -10,
        'expected_delta_z_um': 0,
        }
    }

# TUP_HHD_CMDID_SYS_CALI_MOFM_RESP        = 0x0AA3
TUP_HHD_HLC_SYS_CALI_MOMV_RESP = {
    'parameter': {
        'actual_delta_x_um': 10,
        'actual_delta_y_um': -10,
        'actual_delta_z_um': 0,
        'actual_absolute_x_um': 10,
        'actual_absolute_y_um': -10,
        'actual_absolute_z_um': 0,
        'out_range_detection_positive_x': 0,
        'out_range_detection_negative_x': 0,
        'out_range_detection_positive_y': 0,
        'out_range_detection_negative_y': 0,
        'out_range_detection_positive_z': 0,
        'out_range_detection_negative_z': 0,
        }
    }

# TUP_HHD_CMDID_SYS_CALI_MOMV_START_REQ        = 0x0A24
TUP_HHD_HLC_SYS_CALI_MOFM_REQ = {
    'parameter': {
        'expected_x_um': 10,
        'expected_y_um': -10,
        'expected_z_um': 0,
        }
    }

# TUP_HHD_CMDID_SYS_CALI_MOMV_START_RESP       = 0x0AA4
TUP_HHD_HLC_SYS_CALI_MOMV_RESP = {
    'parameter': {
        'actual_delta_x_um': 10,
        'actual_delta_y_um': -10,
        'actual_delta_z_um': 0,
        'actual_absolute_x_um': 10,
        'actual_absolute_y_um': -10,
        'actual_absolute_z_um': 0,
        'out_range_detection_positive_x': 0,
        'out_range_detection_negative_x': 0,
        'out_range_detection_positive_y': 0,
        'out_range_detection_negative_y': 0,
        'out_range_detection_positive_z': 0,
        'out_range_detection_negative_z': 0,
        }
    }

# TUP_HHD_CMDID_SYS_CALI_MOMV_HOLEN_REQ        = 0x0A25
TUP_HHD_HLC_SYS_CALI_MOMV_REQ = {
    'parameter': {
        'target_hole_n': 1,
        }
    }

# TUP_HHD_CMDID_SYS_CALI_MOMV_HOLEN_RESP       = 0x0AA5
TUP_HHD_HLC_SYS_CALI_MOMV_RESP = {
    'parameter': {
        'target_hole_n': 1,
        'actual_delta_x_um': 10,
        'actual_delta_y_um': -10,
        'actual_delta_z_um': 0,
        'actual_absolute_x_um': 10,
        'actual_absolute_y_um': -10,
        'actual_absolute_z_um': 0,        
        'out_range_detection_positive_x': 0,
        'out_range_detection_negative_x': 0,
        'out_range_detection_positive_y': 0,
        'out_range_detection_negative_y': 0,
        'out_range_detection_positive_z': 0,
        'out_range_detection_negative_z': 0,
        }
    }

# TUP_HHD_CMDID_SYS_CALI_PILOT_START_REQ       = 0x0A26
TUP_HHD_HLC_SYS_CALI_PILOT_START_REQ = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CALI_PILOT_START_RESP      = 0x0AA6
TUP_HHD_HLC_SYS_CALI_PILOT_START_RESP = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CALI_PILOT_STOP_REQ        = 0x0A27
TUP_HHD_HLC_SYS_CALI_PILOT_STOP_REQ = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CALI_PILOT_STOP_RESP       = 0x0AA7
TUP_HHD_HLC_SYS_CALI_PILOT_STOP_RESP = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CALI_RIGHT_UP_SET_REQ      = 0x0A28
TUP_HHD_HLC_SYS_CALI_RIGHT_UP_SET_REQ = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CALI_RIGHT_UP_SET_RESP     = 0x0AA8
TUP_HHD_HLC_SYS_CALI_RIGHT_UP_SET_RESP = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CALI_LEFT_BOT_SET_REQ      = 0x0A29
TUP_HHD_HLC_SYS_CALI_LEFT_BOT_SET_REQ = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CALI_LEFT_BOT_SET_RESP     = 0x0AA9
TUP_HHD_HLC_SYS_CALI_LEFT_BOT_SET_RESP = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CALI_PIC_CAP_HOLEN_REQ     = 0x0A2A
TUP_HHD_CMDID_SYS_CALI_PIC_CAP_HOLEN_REQ = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CALI_PIC_CAP_HOLEN_RESP    = 0x0AAA
TUP_HHD_CMDID_SYS_CALI_PIC_CAP_HOLEN_RESP = {
    'parameter': {}
    }


# #CTRL_SCHD
# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_START_REQ    = 0x0A30
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CAP_START_REQ = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_START_RESP   = 0x0AB0
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CAP_START_RESP = {
    'parameter': {
        'batch_number': 10,
        }
    }
    
# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_TRIG         = 0x0AB1
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CAP_TRIG = {
    'parameter': {
        'batch_number': 10,
        'hole_index_complete':15,
        'hole_total_nunber_complete':10,
        'hole_list_complete':['1','2','5','6','7','8','9','10','11','12','13','15'],
        }
    }
    
# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_STOP_REQ     = 0x0A32
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CAP_STOP_REQ = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_STOP_RESP    = 0x0AB2
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CAP_STOP_RESP = {
    'parameter': {
        'batch_number': 10,
        'hole_index_complete':15,
        'hole_total_nunber_complete':10,
        'hole_list_complete':['1','2','5','6','7','8','9','10','11','12','13','15'],
        }
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_START_REQ    = 0x0A33
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CFY_START_REQ = {
    'parameter': {
        'capture_or_not': 0, #0:NO, 1:YES
        'batch_number': 10, #when capture=no
        'hole_number': 4,
        'hole_list': ['1','2','3','96'],
        }
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_START_RESP   = 0x0AB3
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CFY_START_RESP = {
    'parameter': {
        'capture_or_not': 0, #0:NO, 1:YES        
        'batch_number': 10,
        }
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_TRIG         = 0x0AB4
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CFY_TRIG = {
    'parameter': {
        'batch_number': 10,
        'hole_index_complete':15,
        'hole_total_nunber_complete':10,
        'hole_list_complete':['1','2','5','6','7','8','9','10','11','12','13','15'],
        'cfy_result_file_attr':2,
        'cfy_result_name_before':'batch_20_hole_10_org.jpg',
        'cfy_result_cap_time':'2019-06-05 20:00:00',
        'cfy_result_name_after':'batch_20_hole_10_cfy.jpg',
        'cfy_result_rec_time':'2019-06-05 20:00:00',
        'cfy_result_bigalive':20,
        'cfy_result_bigdead':30,
        'cfy_result_midalive':40,
        'cfy_result_middead':20,
        'cfy_result_smalive':10,
        'cfy_result_smdead':5,
        'cfy_result_totalalive':100,
        'cfy_result_totaldead':50,
        'cfy_result_totalsum':300,
        'cfy_result_doneflag':1,
        }
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_STOP_REQ     = 0x0A35
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CFY_STOP_REQ = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_STOP_RESP    = 0x0AB5
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CFY_STOP_RESP = {
    'parameter': {
        'batch_number': 10,
        'hole_index_complete':15,
        'hole_total_nunber_complete':10,
        'hole_list_complete':['1','2','5','6','7','8','9','10','11','12','13','15'],
        }
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_MV_ZERO_REQ         = 0x0A36
TUP_HHD_HLC_SYS_CTRL_SCHD_MV_ZERO_REQ = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_MV_ZERO_RESP        = 0x0AB6
TUP_HHD_HLC_SYS_CTRL_SCHD_MV_ZERO_RESP = {
    'parameter': {}
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_START_REQ    = 0x0A37
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_START_REQ = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_START_RESP   = 0x0AB7
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_START_RESP = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_TRIG         = 0x0AB8
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_TRIG = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_STOP_REQ     = 0x0A39
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_STOP_REQ = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_STOP_RESP    = 0x0AB9
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_STOP_RESP = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_START_REQ    = 0x0A3A
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_START_REQ = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_START_RESP   = 0x0ABA
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_START_RESP = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_TRIG         = 0x0ABB
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_TRIG = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_STOP_REQ     = 0x0A3C
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_STOP_REQ = {
    'parameter': {}
    }



# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_STOP_RESP    = 0x0ABC
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_STOP_RESP = {
    'parameter': {}
    }


# #MENG
# TUP_HHD_CMDID_SYS_MENG_START_REQ        = 0x0A40
TUP_HHD_CMDID_SYS_MENG_START_REQ = {
    'parameter': {}
    }



# TUP_HHD_CMDID_SYS_MENG_START_RESP       = 0x0AC0
TUP_HHD_CMDID_SYS_MENG_START_RESP = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_MENG_EXIT_REQ         = 0x0A41
TUP_HHD_CMDID_SYS_MENG_EXIT_REQ = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_MENG_EXIT_RESP        = 0x0AC1
TUP_HHD_CMDID_SYS_MENG_EXIT_RESP = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_MENG_COMMAND_REQ      = 0x0A42
TUP_HHD_CMDID_SYS_MENG_COMMAND_REQ = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_MENG_COMMAND_RESP     = 0x0AC2
TUP_HHD_CMDID_SYS_MENG_COMMAND_RESP = {
    'parameter': {}
    }


# TUP_HHD_CMDID_SYS_MENG_COMMAND_TRIG     = 0x0AC3
TUP_HHD_CMDID_SYS_MENG_COMMAND_TRIG = {
    'parameter': {}
    }























