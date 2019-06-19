'''
Created on 2019年5月31日

@author: Administrator
'''

#HUICOBUS CMDID公共定义: HEAD DEFINATION
#cmdid need to cast from HEX to DEC
#获取参数=》未来将直接通过HST进行读取
TUP_HHD_CMDID_SYS_GET_CONFIG_REQ        = 0x0A00    #2560
TUP_HHD_CMDID_SYS_GET_CONFIG_RESP       = 0x0A80    #2688
#设置参数
TUP_HHD_CMDID_SYS_SET_CONFIG_REQ        = 0x0A01    #2561
TUP_HHD_CMDID_SYS_SET_CONFIG_RESP       = 0x0A81    #2689
#UI独立通知TUP
TUP_HHD_CMDID_SYS_UI_START_REQ          = 0x0A02    #2562
TUP_HHD_CMDID_SYS_UI_START_RESP         = 0x0A82    #2690
#TUP更新状态
TUP_HHD_CMDID_SYS_STATUS_TRIG           = 0x0A83    #2691
#TUP更新错误
TUP_HHD_CMDID_SYS_ERROR_TRIG            = 0x0A84    #2692
#强制重启TUP软件
TUP_HHD_CMDID_SYS_FRC_RESTART_REQ       = 0x0A05    #2565
TUP_HHD_CMDID_SYS_FRC_RESTART_RESP      = 0x0A85    #2693
#获取TUP系统状态
TUP_HHD_CMDID_SYS_TUP_STATUS_REQ        = 0x0A06    #2566
TUP_HHD_CMDID_SYS_TUP_STATUS_RESP       = 0x0A86    #2694

#GPAR
TUP_HHD_CMDID_SYS_GPAR_START_REQ        = 0x0A10    #2576
TUP_HHD_CMDID_SYS_GPAR_START_RESP       = 0x0A90    #2704
TUP_HHD_CMDID_SYS_GPAR_SAVE_REQ         = 0x0A11    #2577
TUP_HHD_CMDID_SYS_GPAR_SAVE_RESP        = 0x0A91    #2705
TUP_HHD_CMDID_SYS_GPAR_EXIT_REQ         = 0x0A12    #2578
TUP_HHD_CMDID_SYS_GPAR_EXIT_RESP        = 0x0A92    #2706
TUP_HHD_CMDID_SYS_GPAR_PIC_TRAIN_REQ    = 0x0A13    #2579
TUP_HHD_CMDID_SYS_GPAR_PIC_TRAIN_RESP   = 0x0A93    #2707
TUP_HHD_CMDID_SYS_GPAR_PIC_FCC_REQ      = 0x0A14    #2580
TUP_HHD_CMDID_SYS_GPAR_PIC_FCC_RESP     = 0x0A94    #2708

#CALIB
TUP_HHD_CMDID_SYS_CALI_START_REQ        = 0x0A20    #2592
TUP_HHD_CMDID_SYS_CALI_START_RESP       = 0x0AA0    #2720
TUP_HHD_CMDID_SYS_CALI_MOMV_DIR_REQ     = 0x0A21    #2593
TUP_HHD_CMDID_SYS_CALI_MOMV_DIR_RESP    = 0x0AA1    #2721
TUP_HHD_CMDID_SYS_CALI_EXIT_REQ         = 0x0A22    #2594
TUP_HHD_CMDID_SYS_CALI_EXIT_RESP        = 0x0AA2    #2722
TUP_HHD_CMDID_SYS_CALI_MOFM_REQ         = 0x0A23    #2595
TUP_HHD_CMDID_SYS_CALI_MOFM_RESP        = 0x0AA3    #2723
TUP_HHD_CMDID_SYS_CALI_MOMV_START_REQ        = 0x0A24   #2596
TUP_HHD_CMDID_SYS_CALI_MOMV_START_RESP       = 0x0AA4   #2724
TUP_HHD_CMDID_SYS_CALI_MOMV_HOLEN_REQ        = 0x0A25   #2597
TUP_HHD_CMDID_SYS_CALI_MOMV_HOLEN_RESP       = 0x0AA5   #2725
TUP_HHD_CMDID_SYS_CALI_PILOT_START_REQ       = 0x0A26   #2598
TUP_HHD_CMDID_SYS_CALI_PILOT_START_RESP      = 0x0AA6   #2726
TUP_HHD_CMDID_SYS_CALI_PILOT_STOP_REQ        = 0x0A27   #2599
TUP_HHD_CMDID_SYS_CALI_PILOT_STOP_RESP       = 0x0AA7   #2727
TUP_HHD_CMDID_SYS_CALI_RIGHT_UP_SET_REQ      = 0x0A28   #2600
TUP_HHD_CMDID_SYS_CALI_RIGHT_UP_SET_RESP     = 0x0AA8   #2728
TUP_HHD_CMDID_SYS_CALI_LEFT_BOT_SET_REQ      = 0x0A29   #2601
TUP_HHD_CMDID_SYS_CALI_LEFT_BOT_SET_RESP     = 0x0AA9   #2729
TUP_HHD_CMDID_SYS_CALI_PIC_CAP_HOLEN_REQ     = 0x0A2A   #2602
TUP_HHD_CMDID_SYS_CALI_PIC_CAP_HOLEN_RESP    = 0x0AAA   #2730
TUP_HHD_CMDID_SYS_CALI_CAM_VDISP_TRIG        = 0x0AAB   #2731
#CTRL_SCHD
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_START_REQ    = 0x0A30   #2608
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_START_RESP   = 0x0AB0   #2736
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_TRIG         = 0x0AB1   #2737
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_STOP_REQ     = 0x0A32   #2610
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_STOP_RESP    = 0x0AB2   #2738
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_START_REQ    = 0x0A33   #2611
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_START_RESP   = 0x0AB3   #2739
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_TRIG         = 0x0AB4   #2740
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_STOP_REQ     = 0x0A35   #2613
TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_STOP_RESP    = 0x0AB5   #2741
TUP_HHD_CMDID_SYS_CTRL_SCHD_MV_ZERO_REQ         = 0x0A36    #2614
TUP_HHD_CMDID_SYS_CTRL_SCHD_MV_ZERO_RESP        = 0x0AB6    #2742
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_START_REQ    = 0x0A37   #2615
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_START_RESP   = 0x0AB7   #2743
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_TRIG         = 0x0AB8   #2744
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_STOP_REQ     = 0x0A39   #2617
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_STOP_RESP    = 0x0AB9   #2745
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_START_REQ    = 0x0A3A   #2618
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_START_RESP   = 0x0ABA   #2746
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_TRIG         = 0x0ABB   #2747
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_STOP_REQ     = 0x0A3C   #2620
TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_STOP_RESP    = 0x0ABC   #2748

#MENG
TUP_HHD_CMDID_SYS_MENG_START_REQ        = 0x0A40    #2624
TUP_HHD_CMDID_SYS_MENG_START_RESP       = 0x0AC0    #2752
TUP_HHD_CMDID_SYS_MENG_EXIT_REQ         = 0x0A41    #2625
TUP_HHD_CMDID_SYS_MENG_EXIT_RESP        = 0x0AC1    #2753
TUP_HHD_CMDID_SYS_MENG_COMMAND_REQ      = 0x0A42    #2626
TUP_HHD_CMDID_SYS_MENG_COMMAND_RESP     = 0x0AC2    #2754
TUP_HHD_CMDID_SYS_MENG_COMMAND_TRIG     = 0x0AC3    #2755

# THIS IS ONLY FOR INFO: MQTT HEADER TUP TO UIP
TUP_HHD_HLC_MESSAGE_HEADER_TUP2UIP = {
    'srcNode':'HUICOBUS_MQTT_NODEID_TUPSVR',
    'destNode':'HUICOBUS_MQTT_NODEID_TUPSVR',
    'srcId':'HUICOBUS_MQTT_CLIENTID_TUPENTRY',
    'destId':'HUICOBUS_MQTT_CLIENTID_TUPROUTER',
    'topicId':'HUICOBUS_MQTT_TOPIC_TUP2UIP',
    'cmdId':391,
    'cmdValue':0,
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
    'cmdValue':0,
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
        },
    'session_id':1559381384274,
    }

#TUP_HHD_CMDID_SYS_GET_CONFIG_RESP       = 0x0A80
TUP_HHD_HLC_SYS_GET_CONFIG_RESP = {
    'parameter': {
        'groups': [
            {
                'groupname': '版型选择', 
                'groupkey': 'hb_selct', 
                'list': [
                    {'paraname': '托盘类型', 'parakey': 'hb_type', 'type': 'choice', 'max': '', 'min': '', 'value': '0', 'items': ['96孔板', '48孔板', '24孔板', '12孔板', '6孔板', '384孔板'], 'note': 'choice info'}]
            }, 
            {
                'groupname': '全局参数设置',
                'groupkey': 'glpar_set', 
                'list': [
                    {'paraname': '拍照后自动识别', 'parakey': 'autocfy', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]
             }, 
            {
                'groupname': '计划任务设置', 
                'groupkey': 'ctrs_set', 
                'list': [
                    {'paraname': '定点拍照', 'parakey': 'fixpoint', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '二次曝光设置', 'parakey': 'autoexpo', 'type': 'checkbox', 'max': '100', 'min': '', 'value': True, 'note': 'Note info'},
                    {'paraname': '拍后自动识别', 'parakey': 'pic2cfy', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'},
                    {'paraname': '启动即工作', 'parakey': 'startauto', 'type': 'checkbox', 'max': '', 'min': '', 'value': False, 'note': 'Note info'}, 
                    {'paraname': '模糊度门限', 'parakey': 'blulim', 'type': 'int', 'max': '10000', 'min': '0', 'value': 1, 'note': '单位：无'},
                    {'paraname': '定时自动拍照', 'parakey': 'timeauto', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '定时拍照时间间隔', 'parakey': 'pictti', 'type': 'int', 'max': '100', 'min': '0', 'value': 1, 'note': '单位：秒'}]
            }, 
            {
                'groupname': '坐标系设置', 
                'groupkey': 'axis_set', 
                'list': [
                    {'paraname': '左下X坐标', 'parakey': 'leftdown_x', 'type': 'int', 'max': '37000', 'min': '0', 'value': 100, 'note': '单位：UM'}, 
                    {'paraname': '左下Y坐标',  'parakey': 'leftdown_y', 'type': 'int', 'max': '37000', 'min': '0', 'value': 30, 'note': '单位：UM'}, 
                    {'paraname': '右上X坐标', 'parakey': 'rightup_x', 'type': 'int', 'max': '157000', 'min': '120000', 'value': 20, 'note': '单位：UM'}, 
                    {'paraname': '右上Y坐标',  'parakey': 'rightup_y', 'type': 'int', 'max': '127000', 'min': '90000', 'value': 10, 'note': '单位：UM'}]
            }, 
            {
                'groupname': '图片识别参数设置', 
                'groupkey': 'piccfy_set', 
                'list': [
                    {'paraname': '小尺寸门限', 'parakey': 'smalldown_thd', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：像素'}, 
                    {'paraname': '小-中尺寸门限', 'parakey': 'smallmid_thd', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：像素'}, 
                    {'paraname': '中-大尺寸门限', 'parakey': 'midbig_thd', 'type': 'int', 'max': '', 'min': '', 'value': 500, 'note': '单位：像素'}, 
                    {'paraname': '大尺寸门限', 'parakey': 'bigup_thd', 'type': 'int', 'max': '', 'min': '', 'value': 1000, 'note': '单位：像素'}, 
                    {'paraname': '输出图像叠加标定', 'parakey': 'addup', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]
            }, 
            {
                'groupname': '视频参数设置', 
                'groupkey': 'video_set', 
                'list': [
                    {'paraname': '开启视频记录', 'parakey': 'openvideo', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '视频时长', 'parakey': 'videotti', 'type': 'int', 'max': '60', 'min': '0', 'value': 3, 'note': '单位：秒'}]
            }, 
            {
                'groupname': '图片存储位置', 
                'groupkey': 'picsave_set', 
                'list': [
                    {'paraname': '未识别照片目录', 'parakey': 'uncfy', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_origin/', 'note': 'Note info'}, 
                    {'paraname': '已识别照片目录', 'parakey': 'cfied', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_middle/', 'note': 'Note info'}]
            },
            {
                'groupname': '马达参数', 
                'groupkey': 'moto_set', 
                'list': [
                    {'paraname': '增速加速度', 'parakey': 'acc', 'type': 'int', 'max': '', 'min': '', 'value': 10, 'note': '单位：metre every second square second'}, 
                    {'paraname': '减速加速度', 'parakey': 'deacc', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, 
                    {'paraname': '移动速度', 'parakey': 'spd', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, 
                    {'paraname': '归零速度', 'parakey': 'zerospd', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：metre every second'}, 
                    {'paraname': '归零减速度', 'parakey': 'zeroacc', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：metre every second'}, 
                    {'paraname': '回退步数', 'parakey': 'backsteps', 'type': 'int', 'max': '', 'min': '', 'value': 22, 'note': '单位：步'}]
            }]
        },
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_SET_CONFIG_REQ        = 0x0A01
TUP_HHD_HLC_SYS_SET_CONFIG_REQ = {
    'parameter': {
        'groups': [
            {
                'groupname': '版型选择', 
                'groupkey': 'hb_selct', 
                'list': [
                    {'paraname': '托盘类型', 'parakey': 'hb_type', 'type': 'choice', 'max': '', 'min': '', 'value': '0', 'items': ['96孔板', '48孔板', '24孔板', '12孔板', '6孔板', '384孔板'], 'note': 'choice info'}]
            }, 
            {
                'groupname': '全局参数设置',
                'groupkey': 'glpar_set', 
                'list': [
                    {'paraname': '拍照后自动识别', 'parakey': 'autocfy', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]
             }, 
            {
                'groupname': '计划任务设置', 
                'groupkey': 'ctrs_set', 
                'list': [
                    {'paraname': '定点拍照', 'parakey': 'fixpoint', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '二次曝光设置', 'parakey': 'autoexpo', 'type': 'checkbox', 'max': '100', 'min': '', 'value': True, 'note': 'Note info'},
                    {'paraname': '拍后自动识别', 'parakey': 'pic2cfy', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'},
                    {'paraname': '启动即工作', 'parakey': 'startauto', 'type': 'checkbox', 'max': '', 'min': '', 'value': False, 'note': 'Note info'}, 
                    {'paraname': '模糊度门限', 'parakey': 'blulim', 'type': 'int', 'max': '10000', 'min': '0', 'value': 1, 'note': '单位：无'},
                    {'paraname': '定时自动拍照', 'parakey': 'timeauto', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '定时拍照时间间隔', 'parakey': 'pictti', 'type': 'int', 'max': '100', 'min': '0', 'value': 1, 'note': '单位：秒'}]
            }, 
            {
                'groupname': '坐标系设置', 
                'groupkey': 'axis_set', 
                'list': [
                    {'paraname': '左下X坐标', 'parakey': 'leftdown_x', 'type': 'int', 'max': '37000', 'min': '0', 'value': 100, 'note': '单位：UM'}, 
                    {'paraname': '左下Y坐标',  'parakey': 'leftdown_y', 'type': 'int', 'max': '37000', 'min': '0', 'value': 30, 'note': '单位：UM'}, 
                    {'paraname': '右上X坐标', 'parakey': 'rightup_x', 'type': 'int', 'max': '157000', 'min': '120000', 'value': 20, 'note': '单位：UM'}, 
                    {'paraname': '右上Y坐标',  'parakey': 'rightup_y', 'type': 'int', 'max': '127000', 'min': '90000', 'value': 10, 'note': '单位：UM'}]
            }, 
            {
                'groupname': '图片识别参数设置', 
                'groupkey': 'piccfy_set', 
                'list': [
                    {'paraname': '小尺寸门限', 'parakey': 'smalldown_thd', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：像素'}, 
                    {'paraname': '小-中尺寸门限', 'parakey': 'smallmid_thd', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：像素'}, 
                    {'paraname': '中-大尺寸门限', 'parakey': 'midbig_thd', 'type': 'int', 'max': '', 'min': '', 'value': 500, 'note': '单位：像素'}, 
                    {'paraname': '大尺寸门限', 'parakey': 'bigup_thd', 'type': 'int', 'max': '', 'min': '', 'value': 1000, 'note': '单位：像素'}, 
                    {'paraname': '输出图像叠加标定', 'parakey': 'addup', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]
            }, 
            {
                'groupname': '视频参数设置', 
                'groupkey': 'video_set', 
                'list': [
                    {'paraname': '开启视频记录', 'parakey': 'openvideo', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '视频时长', 'parakey': 'videotti', 'type': 'int', 'max': '60', 'min': '0', 'value': 3, 'note': '单位：秒'}]
            }, 
            {
                'groupname': '图片存储位置', 
                'groupkey': 'picsave_set', 
                'list': [
                    {'paraname': '未识别照片目录', 'parakey': 'uncfy', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_origin/', 'note': 'Note info'}, 
                    {'paraname': '已识别照片目录', 'parakey': 'cfied', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_middle/', 'note': 'Note info'}]
            },
            {
                'groupname': '马达参数', 
                'groupkey': 'moto_set', 
                'list': [
                    {'paraname': '增速加速度', 'parakey': 'acc', 'type': 'int', 'max': '', 'min': '', 'value': 10, 'note': '单位：metre every second square second'}, 
                    {'paraname': '减速加速度', 'parakey': 'deacc', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, 
                    {'paraname': '移动速度', 'parakey': 'spd', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, 
                    {'paraname': '归零速度', 'parakey': 'zerospd', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：metre every second'}, 
                    {'paraname': '归零减速度', 'parakey': 'zeroacc', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：metre every second'}, 
                    {'paraname': '回退步数', 'parakey': 'backsteps', 'type': 'int', 'max': '', 'min': '', 'value': 22, 'note': '单位：步'}]
            }]
        },
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_SET_CONFIG_RESP       = 0x0A81
TUP_HHD_HLC_SYS_SET_CONFIG_RESP = {
    'parameter': {
        'groups': [
            {
                'groupname': '版型选择', 
                'groupkey': 'hb_selct', 
                'list': [
                    {'paraname': '托盘类型', 'parakey': 'hb_type', 'type': 'choice', 'max': '', 'min': '', 'value': '0', 'items': ['96孔板', '48孔板', '24孔板', '12孔板', '6孔板', '384孔板'], 'note': 'choice info'}]
            }, 
            {
                'groupname': '全局参数设置',
                'groupkey': 'glpar_set', 
                'list': [
                    {'paraname': '拍照后自动识别', 'parakey': 'autocfy', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]
             }, 
            {
                'groupname': '计划任务设置', 
                'groupkey': 'ctrs_set', 
                'list': [
                    {'paraname': '定点拍照', 'parakey': 'fixpoint', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '二次曝光设置', 'parakey': 'autoexpo', 'type': 'checkbox', 'max': '100', 'min': '', 'value': True, 'note': 'Note info'},
                    {'paraname': '拍后自动识别', 'parakey': 'pic2cfy', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'},
                    {'paraname': '启动即工作', 'parakey': 'startauto', 'type': 'checkbox', 'max': '', 'min': '', 'value': False, 'note': 'Note info'}, 
                    {'paraname': '模糊度门限', 'parakey': 'blulim', 'type': 'int', 'max': '10000', 'min': '0', 'value': 1, 'note': '单位：无'},
                    {'paraname': '定时自动拍照', 'parakey': 'timeauto', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '定时拍照时间间隔', 'parakey': 'pictti', 'type': 'int', 'max': '100', 'min': '0', 'value': 1, 'note': '单位：秒'}]
            }, 
            {
                'groupname': '坐标系设置', 
                'groupkey': 'axis_set', 
                'list': [
                    {'paraname': '左下X坐标', 'parakey': 'leftdown_x', 'type': 'int', 'max': '37000', 'min': '0', 'value': 100, 'note': '单位：UM'}, 
                    {'paraname': '左下Y坐标',  'parakey': 'leftdown_y', 'type': 'int', 'max': '37000', 'min': '0', 'value': 30, 'note': '单位：UM'}, 
                    {'paraname': '右上X坐标', 'parakey': 'rightup_x', 'type': 'int', 'max': '157000', 'min': '120000', 'value': 20, 'note': '单位：UM'}, 
                    {'paraname': '右上Y坐标',  'parakey': 'rightup_y', 'type': 'int', 'max': '127000', 'min': '90000', 'value': 10, 'note': '单位：UM'}]
            }, 
            {
                'groupname': '图片识别参数设置', 
                'groupkey': 'piccfy_set', 
                'list': [
                    {'paraname': '小尺寸门限', 'parakey': 'smalldown_thd', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：像素'}, 
                    {'paraname': '小-中尺寸门限', 'parakey': 'smallmid_thd', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：像素'}, 
                    {'paraname': '中-大尺寸门限', 'parakey': 'midbig_thd', 'type': 'int', 'max': '', 'min': '', 'value': 500, 'note': '单位：像素'}, 
                    {'paraname': '大尺寸门限', 'parakey': 'bigup_thd', 'type': 'int', 'max': '', 'min': '', 'value': 1000, 'note': '单位：像素'}, 
                    {'paraname': '输出图像叠加标定', 'parakey': 'addup', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}]
            }, 
            {
                'groupname': '视频参数设置', 
                'groupkey': 'video_set', 
                'list': [
                    {'paraname': '开启视频记录', 'parakey': 'openvideo', 'type': 'checkbox', 'max': '', 'min': '', 'value': True, 'note': 'Note info'}, 
                    {'paraname': '视频时长', 'parakey': 'videotti', 'type': 'int', 'max': '60', 'min': '0', 'value': 3, 'note': '单位：秒'}]
            }, 
            {
                'groupname': '图片存储位置', 
                'groupkey': 'picsave_set', 
                'list': [
                    {'paraname': '未识别照片目录', 'parakey': 'uncfy', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_origin/', 'note': 'Note info'}, 
                    {'paraname': '已识别照片目录', 'parakey': 'cfied', 'type': 'string', 'max': '', 'min': '', 'value': '/code/tup/pic_middle/', 'note': 'Note info'}]
            },
            {
                'groupname': '马达参数', 
                'groupkey': 'moto_set', 
                'list': [
                    {'paraname': '增速加速度', 'parakey': 'acc', 'type': 'int', 'max': '', 'min': '', 'value': 10, 'note': '单位：metre every second square second'}, 
                    {'paraname': '减速加速度', 'parakey': 'deacc', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, 
                    {'paraname': '移动速度', 'parakey': 'spd', 'type': 'int', 'max': '', 'min': '', 'value': 20, 'note': '单位：metre every second square second'}, 
                    {'paraname': '归零速度', 'parakey': 'zerospd', 'type': 'int', 'max': '', 'min': '', 'value': 200, 'note': '单位：metre every second'}, 
                    {'paraname': '归零减速度', 'parakey': 'zeroacc', 'type': 'int', 'max': '', 'min': '', 'value': 100, 'note': '单位：metre every second'}, 
                    {'paraname': '回退步数', 'parakey': 'backsteps', 'type': 'int', 'max': '', 'min': '', 'value': 22, 'note': '单位：步'}]
            }]
        },
    'session_id':1559381384274,
    }



# #UI独立通知TUP
# TUP_HHD_CMDID_SYS_UI_START_REQ          = 0x0A02
TUP_HHD_HLC_SYS_UI_START_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_UI_START_RESP         = 0x0A82
TUP_HHD_HLC_SYS_UI_START_RESP = {
    'parameter': {
        'motor_x_status': 1,   #0:NOK, 1:OK
        'motor_y_status': 1,   #0:NOK, 1:OK
        'camera_status': 1,    #0:NOK, 1:OK
        },
    'session_id':1559381384274,
    }

#TUP更新状态
#TUP_HHD_CMDID_SYS_STATUS_TRIG           = 0x0A83
TUP_HHD_HLC_SYS_STATUS_TRIG = {
    'parameter': {
        'status': 'I like to say something!',
        },
    }


#TUP更新错误
#TUP_HHD_CMDID_SYS_ERROR_TRIG            = 0x0A84
TUP_HHD_HLC_SYS_ERROR_TRIG = {
    'parameter': {
        'error': 'I like to say something!',
        },
    }


#强制重启TUP软件
#TUP_HHD_CMDID_SYS_FRC_RESTART_REQ       = 0x0A05
TUP_HHD_HLC_SYS_FRC_RESTART_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }


#TUP_HHD_CMDID_SYS_FRC_RESTART_RESP      = 0x0A85
TUP_HHD_HLC_SYS_FRC_RESTART_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }


#TUP_HHD_CMDID_SYS_TUP_STATUS_REQ        = 0x0A06    #2566
TUP_HHD_HLC_SYS_TUP_STATUS_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }

#TUP_HHD_CMDID_SYS_TUP_STATUS_RESP       = 0x0A86    #2694
TUP_HHD_HLC_SYS_TUP_STATUS_RESP = {
    'parameter': {
        'status':'GPAR:3, CALIB:4, CTRS:5, MENG:4, MOTO:4, VISION:5, FSPC:4, STEST: None'
        },
    'session_id':1559381384274,
    }

# #GPAR
# TUP_HHD_CMDID_SYS_GPAR_START_REQ        = 0x0A10
TUP_HHD_HLC_SYS_GPAR_START_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_GPAR_START_RESP       = 0x0A90
TUP_HHD_HLC_SYS_GPAR_START_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_GPAR_SAVE_REQ         = 0x0A11
TUP_HHD_HLC_SYS_GPAR_SAVE_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }
# TUP_HHD_CMDID_SYS_GPAR_SAVE_RESP        = 0x0A91
TUP_HHD_HLC_SYS_GPAR_SAVE_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_GPAR_EXIT_REQ         = 0x0A12
TUP_HHD_HLC_SYS_GPAR_EXIT_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }
# TUP_HHD_CMDID_SYS_GPAR_EXIT_RESP        = 0x0A92
TUP_HHD_HLC_SYS_GPAR_EXIT_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_GPAR_PIC_TRAIN_REQ    = 0x0A13
TUP_HHD_HLC_SYS_GPAR_PIC_TRAIN_REQ = {
    'parameter': {
        'filename':'D:\DD\train.jpg',
        },
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_GPAR_PIC_TRAIN_RESP   = 0x0A93
TUP_HHD_HLC_SYS_GPAR_PIC_TRAIN_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_GPAR_PIC_FCC_REQ      = 0x0A14
TUP_HHD_HLC_SYS_GPAR_PIC_FCC_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_GPAR_PIC_FCC_RESP     = 0x0A94
TUP_HHD_HLC_SYS_GPAR_PIC_FCC_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }

# #CALIB
# TUP_HHD_CMDID_SYS_CALI_START_REQ        = 0x0A20, ENTER CALIBRATION GUI
TUP_HHD_HLC_SYS_CALI_START_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_CALI_START_RESP       = 0x0AA0, ENTER CALIBRATION GUI
TUP_HHD_HLC_SYS_CALI_START_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_MOMV_DIR_REQ     = 0x0A21, MOVE BY DISTANCE
TUP_HHD_HLC_SYS_CALI_MOMV_DIR_REQ = {
    'parameter': {
        'expected_delta_x_um': 10,
        'expected_delta_y_um': -10,
        'expected_delta_z_um': 0,
        },
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_CALI_MOMV_DIR_RESP    = 0x0AA1, MOVE BY DISTANCE
TUP_HHD_HLC_SYS_CALI_MOMV_DIR_RESP = {
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
        },
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_CALI_EXIT_REQ         = 0x0A22, EXIT CALIBRATION GUI
TUP_HHD_HLC_SYS_CALI_EXIT_REQ = {
    'parameter': {
        'saveornot':True,
        },
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_CALI_EXIT_RESP        = 0x0AA2, EXIT CALIBRATION GUI
TUP_HHD_HLC_SYS_CALI_EXIT_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_CALI_MOFM_REQ         = 0x0A23, FORCE MOVE BY DISTANCE
TUP_HHD_HLC_SYS_CALI_MOFM_REQ = {
    'parameter': {
        'expected_delta_x_um': 10,
        'expected_delta_y_um': -10,
        'expected_delta_z_um': 0,
        },
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_MOFM_RESP        = 0x0AA3, FORCE MOVE BY DISTANCE
TUP_HHD_HLC_SYS_CALI_MOFM_RESP = {
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
        },
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_MOMV_START_REQ        = 0x0A24, MOVE TO START POINT
TUP_HHD_HLC_SYS_CALI_MOMV_START_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_MOMV_START_RESP       = 0x0AA4, MOVE TO START POINT
TUP_HHD_HLC_SYS_CALI_MOMV_START_RESP = {
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
        },
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_MOMV_HOLEN_REQ        = 0x0A25, MOVE TO N-th HOLE
TUP_HHD_HLC_SYS_CALI_MOMV_HOLEN_REQ = {
    'parameter': {
        'target_hole_n': 1,
        },
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_MOMV_HOLEN_RESP       = 0x0AA5, MOVE TO N-th HOLE
TUP_HHD_HLC_SYS_CALI_MOMV_HOLEN_RESP = {
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
        },
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_PILOT_START_REQ       = 0x0A26, POLIT START
TUP_HHD_HLC_SYS_CALI_PILOT_START_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_PILOT_START_RESP      = 0x0AA6, POLIT START
TUP_HHD_HLC_SYS_CALI_PILOT_START_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_PILOT_STOP_REQ        = 0x0A27, POLIT STOP
TUP_HHD_HLC_SYS_CALI_PILOT_STOP_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_PILOT_STOP_RESP       = 0x0AA7, POLIT STOP
TUP_HHD_HLC_SYS_CALI_PILOT_STOP_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_RIGHT_UP_SET_REQ      = 0x0A28
TUP_HHD_HLC_SYS_CALI_RIGHT_UP_SET_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_RIGHT_UP_SET_RESP     = 0x0AA8
TUP_HHD_HLC_SYS_CALI_RIGHT_UP_SET_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_LEFT_BOT_SET_REQ      = 0x0A29
TUP_HHD_HLC_SYS_CALI_LEFT_BOT_SET_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_LEFT_BOT_SET_RESP     = 0x0AA9
TUP_HHD_HLC_SYS_CALI_LEFT_BOT_SET_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_PIC_CAP_HOLEN_REQ     = 0x0A2A
TUP_HHD_HLC_SYS_CALI_PIC_CAP_HOLEN_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CALI_PIC_CAP_HOLEN_RESP    = 0x0AAA
TUP_HHD_HLC_SYS_CALI_PIC_CAP_HOLEN_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }

#TUP_HHD_CMDID_SYS_CALI_CAM_VDISP_TRIG
TUP_HHD_HLC_SYS_CALI_CAM_VDISP_TRIG = {
    'parameter': {
        'pic_fn':'d:\aa\bb\c.jpg',
        },
    }

# #CTRL_SCHD
# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_START_REQ    = 0x0A30
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CAP_START_REQ = {
    'parameter': {
        'hole_list': ['1','2','3','96'],
        },
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_START_RESP   = 0x0AB0
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CAP_START_RESP = {
    'parameter': {
        'batch_number': 10,
        },
    'session_id':1559381384274,
    }
    
# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_TRIG         = 0x0AB1
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CAP_TRIG = {
    'parameter': {
        'batch_number': 10,
        'hole_index_complete':15,
        'hole_total_nunber_complete':10,
        'hole_list_complete':['1','2','5','6','7','8','9','10','11','12','13','15'],
        },
    }
    
# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_STOP_REQ     = 0x0A32
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CAP_STOP_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CAP_STOP_RESP    = 0x0AB2
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CAP_STOP_RESP = {
    'parameter': {
        'batch_number': 10,
        'hole_index_complete':15,
        'hole_total_nunber_complete':10,
        'hole_list_complete':['1','2','5','6','7','8','9','10','11','12','13','15'],
        },
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_START_REQ    = 0x0A33
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CFY_START_REQ = {
    'parameter': {
        'capture_or_not': 0, #0:NO, 1:YES
        'pic_sel_or_not': 1, #0:NO, 1:YES
        'batch_number': 10, #when capture=no
        'hole_number': 4,
        'hole_list': ['1','2','3','96'],
        },
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_START_RESP   = 0x0AB3
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CFY_START_RESP = {
    'parameter': {
        'capture_or_not': 0, #0:NO, 1:YES        
        'batch_number': 10,
        },
    'session_id':1559381384274,
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
        },
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_STOP_REQ     = 0x0A35
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CFY_STOP_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_PIC_CFY_STOP_RESP    = 0x0AB5
TUP_HHD_HLC_SYS_CTRL_SCHD_PIC_CFY_STOP_RESP = {
    'parameter': {
        'batch_number': 10,
        'hole_index_complete':15,
        'hole_total_nunber_complete':10,
        'hole_list_complete':['1','2','5','6','7','8','9','10','11','12','13','15'],
        },
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_MV_ZERO_REQ         = 0x0A36
TUP_HHD_HLC_SYS_CTRL_SCHD_MV_ZERO_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_MV_ZERO_RESP        = 0x0AB6
TUP_HHD_HLC_SYS_CTRL_SCHD_MV_ZERO_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }

# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_START_REQ    = 0x0A37
TUP_HHD_HLC_SYS_CTRL_SCHD_FLU_CAP_START_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_START_RESP   = 0x0AB7
TUP_HHD_HLC_SYS_CTRL_SCHD_FLU_CAP_START_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_TRIG         = 0x0AB8
TUP_HHD_HLC_SYS_CTRL_SCHD_FLU_CAP_TRIG = {
    'parameter': {},
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_STOP_REQ     = 0x0A39
TUP_HHD_HLC_SYS_CTRL_SCHD_FLU_CAP_STOP_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CAP_STOP_RESP    = 0x0AB9
TUP_HHD_HLC_SYS_CTRL_SCHD_FLU_CAP_STOP_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_START_REQ    = 0x0A3A
TUP_HHD_HLC_SYS_CTRL_SCHD_FLU_CFY_START_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_START_RESP   = 0x0ABA
TUP_HHD_HLC_SYS_CTRL_SCHD_FLU_CFY_START_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_TRIG         = 0x0ABB
TUP_HHD_HLC_SYS_CTRL_SCHD_FLU_CFY_TRIG = {
    'parameter': {},
    }


# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_STOP_REQ     = 0x0A3C
TUP_HHD_HLC_SYS_CTRL_SCHD_FLU_CFY_STOP_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }



# TUP_HHD_CMDID_SYS_CTRL_SCHD_FLU_CFY_STOP_RESP    = 0x0ABC
TUP_HHD_HLC_SYS_CTRL_SCHD_FLU_CFY_STOP_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }


# #MENG
# TUP_HHD_CMDID_SYS_MENG_START_REQ        = 0x0A40
TUP_HHD_HLC_SYS_MENG_START_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }



# TUP_HHD_CMDID_SYS_MENG_START_RESP       = 0x0AC0
TUP_HHD_HLC_SYS_MENG_START_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_MENG_EXIT_REQ         = 0x0A41
TUP_HHD_HLC_SYS_MENG_EXIT_REQ = {
    'parameter': {},
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_MENG_EXIT_RESP        = 0x0AC1
TUP_HHD_HLC_SYS_MENG_EXIT_RESP = {
    'parameter': {},
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_MENG_COMMAND_REQ      = 0x0A42
TUP_HHD_HLC_SYS_MENG_COMMAND_REQ = {
    'parameter': {
        'cmdid': 1,   # TUP_HHD_HLC_SYS_MENG_COMMAND_REQ cmdid definition
        'par1': 10,
        'par2': 0,
        'par3': 0,
        'par4': 0,
        },
    'session_id':1559381384274,
    }
	
# TUP_HHD_HLC_SYS_MENG_COMMAND_REQ cmdid definition
#    'SPS_SHK_HAND(设备握手)' : 32,
#    'SPS_SET_WK_MODE(设置工作模式)' : 33,
#    'SPS_SET_ACC(设置加速度)' : 34,
#    'SPS_SET_DEACC(设置减速度)' : 35,
#    'SPS_SET_PPC(设置一圈步伐)' : 36,
#    'SPS_SET_MV_SPD(设置移动速度)' : 37,
#    'SPS_SET_ZO_SPD(设置归零速度)' : 38,
#    'SPS_SET_ZO_ACC(设置归零加速度)' : 39,
#    'SPS_SET_INT_SP(设置靠边后退步伐)' : 40,
#    'SPS_MV_PULS(移动步伐)' : 48,
#    'SPS_MV_SPD(移动速度)' : 49,
#    'SPS_MV_ZERO(归零)' : 50,
#    'SPS_STP_IMD(立即停止)' : 51,
#    'SPS_STP_NOR(缓慢停止)' : 52,
#    'SPS_INQ_EN(查询激活状态)' : 53,
#    'SPS_INQ_RUN(查询运行状态)' : 54,
#    'SPS_INQ_STATUS(查询一般状态)' : 55,
#    'SPS_TEST_PULES(测试脉冲数)' : 56,
#    'SPS_SET_EXTI_DELAY_TIME(设置限位器触发迟滞)' : 57,



# TUP_HHD_CMDID_SYS_MENG_COMMAND_RESP     = 0x0AC2
TUP_HHD_HLC_SYS_MENG_COMMAND_RESP = {
    'parameter': {
        'result': 1,
        },
    'session_id':1559381384274,
    }


# TUP_HHD_CMDID_SYS_MENG_COMMAND_TRIG     = 0x0AC3
TUP_HHD_HLC_SYS_MENG_COMMAND_TRIG = {
    'parameter': {},
    }




















