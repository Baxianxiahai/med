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



#HLC的消息格式
TUP_HHD_HLC_GET_CONFIG_REQ = {
    'action':'ZH_Medicine_sys_config',
    'src': 'ZH_Medicine_sys_config_save',
    'type':'query',
    'lang':'ch',
    'user':'null',
    'ts':1559381384274,
    }

TUP_HHD_HLC_GET_CONFIG_RESP = {
    'action':'ZH_Medicine_sys_config',
    'src': 'ZH_Medicine_sys_config',
    'name': 'configure',
    'owner': 'system',
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




# SYS_GET_CONFIG_REQ = {'src': 'ZH_Medicine_sys_config_save','hlContent': {'action':'ZH_Medicine_sys_config','type':'query','lang':'ch','user':'null'},'ts': 1559381384274}
# SYS_GET_CONFIG_RESP = {'src': 'ZH_Medicine_sys_config', 'hlContent': {'name': 'configure', 'owner': 'system', 'parameter': {'groups': [{'groupname': '版型选择', 'list': [{'paraname': '托盘类型', 'type': 'choice', 'max': '', 'min': '', 'value': '0', 'items': ['96孔板', '48孔板', '24孔板', '12孔板', '6孔板', '384孔板'], 'note': 'choice info'}]}, {'groupname': '全局参数设置', 'list': [{'paraname': '拍照后自动识别', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]}, {'groupname': '计划任务设置', 'list': [{'paraname': '启动计划任务', 'type': 'checkbox', 'max': '', 'min': '', 'value': False, 'note': 'Note info'}, {'paraname': '定时自动拍照', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, {'paraname': '定点拍照', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, {'paraname': '定时拍照时间间隔', 'type': 'int', 'max': '100', 'min': '0', 'value': 1, 'note': '单位：秒'}]}, {'groupname': '坐标系设置', 'list': [{'paraname': '左下X坐标', 'type': 'int', 'max': '37000', 'min': '0', 'value': 100, 'note': '单位：UM'}, {'paraname': '左下Y坐标', 'type': 'int', 'max': '37000', 'min': '0', 'value': 30, 'note': '单位：UM'}, {'paraname': '右上X坐标', 'type': 'int', 'max': '157000', 'min': '120000', 'value': 20, 'note': '单位：UM'}, {'paraname': '右上Y坐标', 'type': 'int', 'max': '127000', 'min': '90000', 'value': 10, 'note': '单位：UM'}]}, {'groupname': '图片识别参数设置', 'list': [{'paraname': '小尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：像素'}, {'paraname': '小-中尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：像素'}, {'paraname': '中-大尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 500, 'note': '单位：像素'}, {'paraname': '大尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 1000, 'note': '单位：像素'}, {'paraname': '输出图像叠加标定', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]}, {'groupname': '视频参数设置', 'list': [{'paraname': '开启视频记录', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, {'paraname': '视频时长', 'type': 'int', 'max': '60', 'min': '0', 'value': 3, 'note': '单位：秒'}]}, {'groupname': '图片存储位置', 'list': [{'paraname': '未识别照片目录', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_origin/', 'note': 'Note info'}, {'paraname': '已识别照片目录', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_middle/', 'note': 'Note info'}]}, {'groupname': '马达参数', 'list': [{'paraname': '增速加速度', 'type': 'int', 'max': '', 'min': '', 'value': 10, 'note': '单位：metre every second square second'}, {'paraname': '减速加速度', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, {'paraname': '移动速度', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, {'paraname': '归零速度', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：metre every second'}, {'paraname': '归零减速度', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：metre every second'}, {'paraname': '回退步数', 'type': 'int', 'max': '', 'min': '', 'value': 22, 'note': '单位：步'}]}]}}, 'ts': 1559381360300}
# SYS_SAVE_CONFIG_REQ = {'src': 'ZH_Medicine_sys_config_save','hlContent': {'name': 'configure','owner': 'system','parameter': { 'groups': [{'groupname': '版型选择', 'list': [{'paraname': '托盘类型', 'type': 'choice', 'max': '', 'min': '', 'value': '0', 'items': ['96孔板', '48孔板', '24孔板', '12孔板', '6孔板', '384孔板'], 'note': 'choice info'}]}, {'groupname': '全局参数设置', 'list': [{'paraname': '拍照后自动识别', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]}, {'groupname': '计划任务设置', 'list': [{'paraname': '启动计划任务', 'type': 'checkbox', 'max': '', 'min': '', 'value': False, 'note': 'Note info'}, {'paraname': '定时自动拍照', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, {'paraname': '定点拍照', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, {'paraname': '定时拍照时间间隔', 'type': 'int', 'max': '100', 'min': '0', 'value': 10, 'note': '单位：秒'}]}, {'groupname': '坐标系设置', 'list': [{'paraname': '左下X坐标', 'type': 'int', 'max': '37000', 'min': '0', 'value': 100, 'note': '单位：UM'}, {'paraname': '左下Y坐标', 'type': 'int', 'max': '37000', 'min': '0', 'value': 30, 'note': '单位：UM'}, {'paraname': '右上X坐标', 'type': 'int', 'max': '157000', 'min': '120000', 'value': 20, 'note': '单位：UM'}, {'paraname': '右上Y坐标', 'type': 'int', 'max': '127000', 'min': '90000', 'value': 10, 'note': '单位：UM'}]}, {'groupname': '图片识别参数设置', 'list': [{'paraname': '小尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：像素'}, {'paraname': '小-中尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：像素'}, {'paraname': '中-大尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 500, 'note': '单位：像素'}, {'paraname': '大尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 1000, 'note': '单位：像素'}, {'paraname': '输出图像叠加标定', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]}, {'groupname': '视频参数设置', 'list': [{'paraname': '开启视频记录', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, {'paraname': '视频时长', 'type': 'int', 'max': '60', 'min': '0', 'value': 3, 'note': '单位：秒'}]}, {'groupname': '图片存储位置', 'list': [{'paraname': '未识别照片目录', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_origin/', 'note': 'Note info'}, {'paraname': '已识别照片目录', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_middle/', 'note': 'Note info'}]}, {'groupname': '马达参数', 'list': [{'paraname': '增速加速度', 'type': 'int', 'max': '', 'min': '', 'value': 10, 'note': '单位：metre every second square second'}, {'paraname': '减速加速度', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, {'paraname': '移动速度', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, {'paraname': '归零速度', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：metre every second'}, {'paraname': '归零减速度', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：metre every second'}, {'paraname': '回退步数', 'type': 'int', 'max': '', 'min': '', 'value': 22, 'note': '单位：步'}]}] }},ts: 1559381384274}
# SYS_SAVE_CONFIG_RESP = {'src': 'ZH_Medicine_sys_config_save', 'hlContent': {'name': 'configure', 'owner': 'system', 'parameter': {'groups': [{'groupname': '版型选择', 'list': [{'paraname': '托盘类型', 'type': 'choice', 'max': '', 'min': '', 'value': '0', 'items': ['96孔板', '48孔板', '24孔板', '12孔板', '6孔板', '384孔板'], 'note': 'choice info'}]}, {'groupname': '全局参数设置', 'list': [{'paraname': '拍照后自动识别', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]}, {'groupname': '计划任务设置', 'list': [{'paraname': '启动计划任务', 'type': 'checkbox', 'max': '', 'min': '', 'value': False, 'note': 'Note info'}, {'paraname': '定时自动拍照', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, {'paraname': '定点拍照', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, {'paraname': '定时拍照时间间隔', 'type': 'int', 'max': '100', 'min': '0', 'value': 10, 'note': '单位：秒'}]}, {'groupname': '坐标系设置', 'list': [{'paraname': '左下X坐标', 'type': 'int', 'max': '37000', 'min': '0', 'value': 100, 'note': '单位：UM'}, {'paraname': '左下Y坐标', 'type': 'int', 'max': '37000', 'min': '0', 'value': 30, 'note': '单位：UM'}, {'paraname': '右上X坐标', 'type': 'int', 'max': '157000', 'min': '120000', 'value': 20, 'note': '单位：UM'}, {'paraname': '右上Y坐标', 'type': 'int', 'max': '127000', 'min': '90000', 'value': 10, 'note': '单位：UM'}]}, {'groupname': '图片识别参数设置', 'list': [{'paraname': '小尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：像素'}, {'paraname': '小-中尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：像素'}, {'paraname': '中-大尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 500, 'note': '单位：像素'}, {'paraname': '大尺寸门限', 'type': 'int', 'max': '', 'min': '', 'value': 1000, 'note': '单位：像素'}, {'paraname': '输出图像叠加标定', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]}, {'groupname': '视频参数设置', 'list': [{'paraname': '开启视频记录', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, {'paraname': '视频时长', 'type': 'int', 'max': '60', 'min': '0', 'value': 3, 'note': '单位：秒'}]}, {'groupname': '图片存储位置', 'list': [{'paraname': '未识别照片目录', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_origin/', 'note': 'Note info'}, {'paraname': '已识别照片目录', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_middle/', 'note': 'Note info'}]}, {'groupname': '马达参数', 'list': [{'paraname': '增速加速度', 'type': 'int', 'max': '', 'min': '', 'value': 10, 'note': '单位：metre every second square second'}, {'paraname': '减速加速度', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, {'paraname': '移动速度', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, {'paraname': '归零速度', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：metre every second'}, {'paraname': '归零减速度', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：metre every second'}, {'paraname': '回退步数', 'type': 'int', 'max': '', 'min': '', 'value': 22, 'note': '单位：步'}]}]}}, 'ts': 1559381384274}















