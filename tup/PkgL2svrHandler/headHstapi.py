'''
Created on 2019年6月4日

@author: Administrator
'''
#HSTAPI CMDID: HEAD DEFINATION
########################################
## REQUEST/IN
########################################
##http://www.aaa.com/printer/request.php?POST={json}
# {
#     'restTag':'dba',
#     'actionId': 8700,
#     'parFlag':1,  ##FALSE-0, TRUE-1
#     'parConent':
#     {
#         'command_id': 10, 
#         'weight': 12.33,
#         'unit': 'kg',
#         'operator': 'Íõ·Œ',
#         'sn': 55,
#         'barCode': '1234567',
#         'qrCode': 'http://12121.com/fasdfa'
#     }
# }
#
########################################
## RESPONE/OUT
########################################
# 
# {
#     'restTag':'dba',
#     'actionId': 8700,
#     'parFlag':1,  ##FALSE-0, TRUE-1
#     'parConent':
#     {
#         'sn': 55,
#         'sucFlag':1,
#         'errCode':0
#     }
# }
# - 取存储参数 hstGetConfig
# - 读取未识别图像参数 hstUnclfyPar
# - 设置存储参数 hstSetConfig
# - 更新校准参数  hstUpdateCaliPar
# - 增加批次号 hstAddBatchNbr
# - 增加普通图像抓取 hstAddPicCap
# - 增加荧光图像抓取 hstAddFluCap
# - 更新普通图像识别 hstUpdatePicCfy
# - 更新荧光图像识别 hstUpdateFluCfy
# - 读取普通图片 hstReadPic
# - 读取荧光图片 hstReadFlu
# - 更新图片统计 hstUpdateStatis
# - 更新用户日志 hstUpdateUserLog

#取存储参数 hstGetConfig
TUP_HST_PCT_GET_CONFIG_IN = {
    'cmdid':'hstGetConfig',
    }

TUP_HST_PCT_GET_CONFIG_OUT = {
    'cmdid':'hstGetConfig',
    'error_no': 'no_error',
    'cebs_cali_profile': {
        'plateoption': ['96_STANDARD','48_STANDARD','24_STANDARD','12_STANDARD','6_STANDARD'],
        'platetype': '96_STANDARD',
        'calitime': '2010-05-06 20:00:00',
        'uid': 10,
        'left_bot_x': 100,
        'left_bot_y': 200,
        'right_up_x': 300,
        'right_up_y': 400,
        },
    'cebs_object_profile': {
        'objid': 2000,
        'defaultflag': 0, #1: default, 0, not default
        'objname': 'XianChong_001',
        'objtype': 5,
        'uid': 10,
        'dir_origin': 'origin',
        'dir_middle': 'middle',
        'memo': 'This is used for a memo record',        
        },
    'cebs_config_eleg': {
        'confid': 1234, 
        'objid': 1234,
        'fixpoint': 1, #bool
        'autovideo': 1, #bool
        'autoclfy': 0, #bool
        'autowork': 0, #bool
        'blurylimit':500,
        'addset': 1, #bool
        'autocap': 1, #bool
        'autoperiod': 10, #seconds
        'videotime': 5, #seconds
        'slimit': 100,
        'smlimit': 200, 
        'mblimit': 300, 
        'blimit': 400, 
        'accspeed': 10,
        'decspeed': 20,
        'movespeed': 30, 
        'zero_spd': 40,
        'zero_acc': 50,
        'back_step': 5,
        }
    }

#设置存储参数 hstSetConfig
TUP_HST_PCT_SET_CONFIG_IN = {
    'cmdid':'hstSetConfig',
    'cebs_cali_profile': {
        'plateoption': ['96_STANDARD','48_STANDARD','24_STANDARD','12_STANDARD','6_STANDARD'],
        'platetype': '96_STANDARD',
        'calitime': '2010-05-06 20:00:00',
        'uid': 10,
        'left_bot_x': 100,
        'left_bot_y': 200,
        'right_up_x': 300,
        'right_up_y': 400,
        },
    'cebs_object_profile': {
        'objid': 2000,
        'defaultflag': 0, #1: default, 0, not default
        'objname': 'XianChong_001',
        'objtype': 5,
        'uid': 10,
        'dir_origin': 'origin',
        'dir_middle': 'middle',
        'memo': 'This is used for a memo record',        
        },
    'cebs_config_eleg': {
        'confid': 1234, 
        'objid': 1234,
        'fixpoint': 1, #bool
        'autovideo': 1, #bool
        'autoclfy': 0, #bool
        'autowork': 0, #bool
        'blurylimit':500,
        'addset': 1, #bool
        'autocap': 1, #bool
        'autoperiod': 10, #seconds
        'videotime': 5, #seconds
        'slimit': 100,
        'smlimit': 200, 
        'mblimit': 300, 
        'blimit': 400, 
        'accspeed': 10,
        'decspeed': 20,
        'movespeed': 30, 
        'zero_spd': 40,
        'zero_acc': 50,
        'back_step': 5,
        }
    }

TUP_HST_PCT_SET_CONFIG_OUT = {
    'cmdid':'hstSetConfig',
    'error_no': 'no_error',
    'cebs_cali_profile': {
        'plateoption': ['96_STANDARD','48_STANDARD','24_STANDARD','12_STANDARD','6_STANDARD'],
        'platetype': '96_STANDARD',
        'calitime': '2010-05-06 20:00:00',
        'uid': 10,
        'left_bot_x': 100,
        'left_bot_y': 200,
        'right_up_x': 300,
        'right_up_y': 400,
        },
    'cebs_object_profile': {
        'objid': 2000,
        'defaultflag': 0, #1: default, 0, not default
        'objname': 'XianChong_001',
        'objtype': 5,
        'uid': 10,
        'dir_origin': 'origin',
        'dir_middle': 'middle',
        'memo': 'This is used for a memo record',        
        },
    'cebs_config_eleg': {
        'confid': 1234, 
        'objid': 1234,
        'fixpoint': 1, #bool
        'autovideo': 1, #bool
        'autoclfy': 0, #bool
        'autowork': 0, #bool
        'blurylimit':500,
        'addset': 1, #bool
        'autocap': 1, #bool
        'autoperiod': 10, #seconds
        'videotime': 5, #seconds
        'slimit': 100,
        'smlimit': 200, 
        'mblimit': 300, 
        'blimit': 400, 
        'accspeed': 10,
        'decspeed': 20,
        'movespeed': 30, 
        'zero_spd': 40,
        'zero_acc': 50,
        'back_step': 5,
        }

    }

#读取未识别图像参数 hstUnclfyPar
TUP_HST_PCT_READ_UNCLFY_PAR_IN = {
    'cmdid':'hstReadUnclfyPar',
    'file-attr':'normal', #'normal', 'flu'
    }

TUP_HST_PCT_READ_UNCLFY_PAR_OUT = {
    'cmdid':'hstReadUnclfyPar',
    'file-attr':'normal', #'normal', 'flu'
    'batchNbr':123,
    'holeNbr':25,
    'fileAbsOrigin':'d:\abc\pic_origin\batch33#a5.jpg',
    'fileAbsMiddle':'d:\abc\pic_mid\batch33#a5.jpg',
    'fileAbsVideo':'d:\abc\pic_origin\batch33#a5.mp4',
    }

#更新校准参数  hstUpdateCaliPar
TUP_HST_PCT_UPDATE_CALI_PAR_IN = {
    'cmdid':'hstUpdateCaliPar',
    'cebs_cali_profile': {
        'plateoption': ['96_STANDARD','48_STANDARD','24_STANDARD','12_STANDARD','6_STANDARD'],
        'platetype': '96_STANDARD',
        'calitime': '2010-05-06 20:00:00',
        'uid': 10,
        'left_bot_x': 100,
        'left_bot_y': 200,
        'right_up_x': 300,
        'right_up_y': 400,
        },
    }

TUP_HST_PCT_UPDATE_CALI_PAR_OUT = {
    'cmdid':'hstUpdateCaliPar',
    'error_no': 'no_error',
    'cebs_cali_profile': {
        'plateoption': ['96_STANDARD','48_STANDARD','24_STANDARD','12_STANDARD','6_STANDARD'],
        'platetype': '96_STANDARD',
        'calitime': '2010-05-06 20:00:00',
        'uid': 10,
        'left_bot_x': 100,
        'left_bot_y': 200,
        'right_up_x': 300,
        'right_up_y': 400,
        },
    }

#增加批次号 hstAddBatchNbr
TUP_HST_PCT_ADD_BATCH_NBR_IN = {
    'cmdid':'hstAddBatchNbr',
    'cebs_batch_info': {
        'user': 'NameOfTheTester',
        'createtime': '2010-05-06 20:00:00',
        'comp_nbr': 123, #FFS
        'usr_def1': 'User Comments Part 1',
        'usr_def2': 'User Comments Part 2',
        },
    }

TUP_HST_PCT_ADD_BATCH_NBR_OUT = {
    'cmdid':'hstAddBatchNbr',
    'error_no': 'no_error',
    'cebs_batch_info': {
        'snbatch': 1000,
        'user': 'NameOfTheTester',
        'createtime': '2010-05-06 20:00:00',
        'comp_nbr': 123, #FFS
        'usr_def1': 'User Comments Part 1',
        'usr_def2': 'User Comments Part 2',
        },
    }

#增加普通图像抓取 hstAddPicCap
TUP_HST_PCT_ADD_PIC_CAP_IN = {
    'cmdid':'hstAddPicCap',
    'cebs_pvci_eleg': {
        'sid': 2000,
        'confid': 10,
        'snbatch': 100,
        'snhole': 96,
        'file_attr':2,
        'name_before':'batch_20_hole_10_org.jpg',
        'cap_time':'2019-06-05 20:00:00',
        'memo': 'This is for user specific comments',
        },
    }

TUP_HST_PCT_ADD_PIC_CAP_OUT = {
    'cmdid':'hstAddPicCap',
    'error_no': 'no_error',
    'cebs_pvci_eleg': {
        'sid': 2000,
        'confid': 10,
        'snbatch': 100,
        'snhole': 96,
        'file_attr':2,
        'name_before':'batch_20_hole_10_org.jpg',
        'cap_time':'2019-06-05 20:00:00',
        'memo': 'This is for user specific comments',
        },
    }

#增加荧光图像抓取 hstAddFluCap
TUP_HST_PCT_ADD_FLU_CAP_IN = {
    'cmdid':'hstAddFluCap',
    }

TUP_HST_PCT_ADD_FLU_CAP_OUT = {
    'cmdid':'hstAddFluCap',
    }

#更新普通图像识别 hstUpdatePicCfy
TUP_HST_PCT_UPDATE_PIC_CFY_IN = {
    'cmdid':'hstUpdatePicCfy',
    'cebs_pvci_eleg': {
        'sid': 2000,
        'confid': 10,
        'snbatch': 100,
        'snhole': 96,
        'file_attr':2,
        'name_before':'batch_20_hole_10_org.jpg',
        'cap_time':'2019-06-05 20:00:00',
        'name_after':'batch_20_hole_10_cfy.jpg',
        'rec_time':'2019-06-05 20:00:00',
        'bigalive':20,
        'bigdead':30,
        'midalive':40,
        'middead':20,
        'smalive':10,
        'smdead':5,
        'totalalive':100,
        'totaldead':50,
        'totalsum':300,
        'doneflag':1,
        'memo': 'This is for user specific comments',
        },
    }

TUP_HST_PCT_UPDATE_PIC_CFY_OUT = {
    'cmdid':'hstUpdatePicCfy',
    'error_no': 'no_error',
    'cebs_pvci_eleg': {
        'sid': 2000,
        'confid': 10,
        'snbatch': 100,
        'snhole': 96,
        'file_attr':2,
        'name_before':'batch_20_hole_10_org.jpg',
        'cap_time':'2019-06-05 20:00:00',
        'name_after':'batch_20_hole_10_cfy.jpg',
        'rec_time':'2019-06-05 20:00:00',
        'bigalive':20,
        'bigdead':30,
        'midalive':40,
        'middead':20,
        'smalive':10,
        'smdead':5,
        'totalalive':100,
        'totaldead':50,
        'totalsum':300,
        'doneflag':1,
        'memo': 'This is for user specific comments',
        },
    }

#更新荧光图像识别 hstUpdateFluCfy
TUP_HST_PCT_UPDATE_FLU_CFY_IN = {
    'cmdid':'hstUpdateFluCfy',
    }

TUP_HST_PCT_UPDATE_FLU_CFY_OUT = {
    'cmdid':'hstUpdateFluCfy',
    }


#读取普通图片 hstReadPic
TUP_HST_PCT_READ_PIC_IN = {
    'cmdid':'hstReadPic',
    'batch_number': 100,
    'hole_number': 96,
    }

TUP_HST_PCT_READ_PIC_OUT = {
    'cmdid':'hstReadPic',
    'error_no': 'no_error',
    'cebs_pvci_eleg': {
        'sid': 2000,
        'confid': 10,
        'snbatch': 100,
        'snhole': 96,
        'file_attr':2,
        'name_before':'batch_20_hole_10_org.jpg',
        'cap_time':'2019-06-05 20:00:00',
        'name_after':'batch_20_hole_10_cfy.jpg',
        'rec_time':'2019-06-05 20:00:00',
        'bigalive':20,
        'bigdead':30,
        'midalive':40,
        'middead':20,
        'smalive':10,
        'smdead':5,
        'totalalive':100,
        'totaldead':50,
        'totalsum':300,
        'doneflag':1,
        'memo': 'This is for user specific comments',
        },
    }

#读取荧光图片 hstReadFlu
TUP_HST_PCT_READ_FLU_IN = {
    'cmdid':'hstReadFlu',
    }

TUP_HST_PCT_READ_FLU_OUT = {
    'cmdid':'hstReadFlu',
    }

#更新图片统计 hstUpdateStatis
TUP_HST_PCT_UPDATE_STATIS_IN = {
    'cmdid':'hstUpdateStatis',
    }

TUP_HST_PCT_UPDATE_STATIS_OUT = {
    'cmdid':'hstUpdateStatis',
    }

#更新用户日志 hstUpdateUserLog
TUP_HST_PCT_UPDATE_USER_LOG_IN = {
    'cmdid':'hstUpdateUserLog',
    }

TUP_HST_PCT_UPDATE_USER_LOG_OUT = {
    'cmdid':'hstUpdateUserLog',
    }















