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
#     'actionId': 8500,
#     'parFlag':1,  ##FALSE-0, TRUE-1
#     'parConent':
#     {
#         'cmd': 10, 
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
#     'actionId': 8500,
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
    'cmd':'hstGetConfig',
    }

TUP_HST_PCT_GET_CONFIG_OUT = {
    'cmd':'hstGetConfig',
    'error_no': 'no_error',
    'cebs_cali_profile': {
        'plateoption': ['96_STANDARD','48_STANDARD','24_STANDARD','12_STANDARD','6_STANDARD'],
        'platetype': '96_STANDARD',
        'calitime': '2010-05-06 20:00:00',
        'uid': 10,
        'right_up_x': 100,
        'right_up_y': 200,
        'left_bot_x': 300,
        'left_bot_y': 400,

        },
    'cebs_object_profile': {
        'objid': 2000,
        'defaultflag': 0, #1: default, 0, not default
        'objname': 'XianChong_001',
        'objtype': 5,
        'uid': 10,
        'dir_origin': 'c:\origin\\',
        'dir_middle': 'c:\middle\\',
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
        'accspeed': 200,
        'decspeed': 200,
        'movespeed': 200, 
        'zero_spd': 200,
        'zero_acc': 200,
        'back_step': 300,
        }
    }

#设置存储参数 hstSetConfig
TUP_HST_PCT_SET_CONFIG_IN = {
    'cmd':'hstSetConfig',
    'cebs_cali_profile': {
        'plateoption': ['96_STANDARD','48_STANDARD','24_STANDARD','12_STANDARD','6_STANDARD'],
        'platetype': '96_STANDARD',
        'calitime': '2010-05-06 20:00:00',
        'left_bot_x': 100,
        'left_bot_y': 200,
        'right_up_x': 300,
        'right_up_y': 400,
        },
    'cebs_object_profile': {
        'objname': 'XianChong_001',
        'objtype': 5,
        'dir_origin': 'c:\origin\\',
        'dir_middle': 'c:\middle\\',
        'memo': 'This is used for a memo record',        
        },
    'cebs_config_eleg': {
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
    'cmd':'hstSetConfig',
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
        'dir_origin': 'c:\origin\\',
        'dir_middle': 'c:\middle\\',
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
    'cmd':'hstReadUnclfyPar',
    'file-attr':'normal', #'normal', 'flu'
    'batchNbr':123,
    'holeNbr':25,
    'fileAbsOrigin':'d:\abc\pic_origin\batch33#a5.jpg',
    'fileAbsMiddle':'d:\abc\pic_mid\batch33#a5.jpg',
    'fileAbsVideo':'d:\abc\pic_origin\batch33#a5.mp4',
    }

#更新校准参数  hstUpdateCaliPar
TUP_HST_PCT_UPDATE_CALI_PAR_IN = {
    'cmd':'hstUpdateCaliPar',
    'cebs_cali_profile': {
        'plateoption': ['96_STANDARD','48_STANDARD','24_STANDARD','12_STANDARD','6_STANDARD'],
        'platetype': '96_STANDARD',
        'calitime': '2010-05-06 20:00:00',
        'left_bot_x': 100,
        'left_bot_y': 200,
        'right_up_x': 300,
        'right_up_y': 400,
        },
    }

TUP_HST_PCT_UPDATE_CALI_PAR_OUT = {
    'cmd':'hstUpdateCaliPar',
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
    'cmd':'hstAddBatchNbr',
    'cebs_batch_info': {
        'user': 'NameOfTheTester',
        'createtime': '2010-05-06 20:00:00',
        'comp_nbr': 123, #FFS
        'usr_def1': 'User Comments Part 1',
        'usr_def2': 'User Comments Part 2',
        },
    }

TUP_HST_PCT_ADD_BATCH_NBR_OUT = {
    'cmd':'hstAddBatchNbr',
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
    'cmd':'hstAddPicCap',
    'cebs_pvci_eleg': {
        'snbatch': 100,
        'snhole': 96,
        'file_attr':'normal',
        'name_before':'d:\aa\origin\batch#20#hole#a5_org.jpg',
        'video_before':'d:\aa\origin\batch#20#hole#a5_video.mp4',
        'cap_time':'2019-06-05 20:00:00',
        'name_after':'d:\aa\mid\batch#20#hole#a5_cfy.jpg',
        'memo': 'This is for user specific comments',
        'rec_time':'2019-06-05 20:00:00',
        'bigalive':0,
        'bigdead':0,
        'midalive':0,
        'middead':0,
        'smalive':0,
        'smdead':0,
        'totalalive':0,
        'totaldead':0,
        'totalsum':0,
        'doneflag':0,
        },
    }

TUP_HST_PCT_ADD_PIC_CAP_OUT = {
    'cmd':'hstAddPicCap',
    'error_no': 'no_error',
    'cebs_pvci_eleg': {
        'sid': 2000,
        'confid': 10,
        'snbatch': 100,
        'snhole': 96,
        'file_attr':'normal',
        'name_before':'d:\aa\origin\batch#20#hole#a5_org.jpg',
        'video_before':'d:\aa\origin\batch#20#hole#a5_video.mp4',
        'cap_time':'2019-06-05 20:00:00',
        'name_after':'d:\aa\mid\batch#20#hole#a5_cfy.jpg',
        'memo': 'This is for user specific comments',
        'bigalive':0,
        'bigdead':0,
        'midalive':0,
        'middead':0,
        'smalive':0,
        'smdead':0,
        'totalalive':0,
        'totaldead':0,
        'totalsum':0,
        'doneflag':0,
        },
    }

#增加荧光图像抓取 hstAddFluCap
TUP_HST_PCT_ADD_FLU_CAP_IN = {
    'cmd':'hstAddFluCap',
    }

TUP_HST_PCT_ADD_FLU_CAP_OUT = {
    'cmd':'hstAddFluCap',
    }

#更新普通图像识别 hstUpdatePicCfy
TUP_HST_PCT_UPDATE_PIC_CFY_IN = {
    'cmd':'hstUpdatePicCfy',
    'cebs_pvci_eleg': {
        'snbatch': 100,
        'snhole': 96,
        'file_attr':'normal',
        'name_before':'d:\aa\origin\batch#20#hole#a5_org.jpg',
        'video_before':'d:\aa\origin\batch#20#hole#a5_video.mp4',
        'cap_time':'2019-06-05 20:00:00',
        'name_after':'d:\aa\mid\batch#20#hole#a5_cfy.jpg',
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
    'cmd':'hstUpdatePicCfy',
    'error_no': 'no_error',
    'cebs_pvci_eleg': {
        'snbatch': 100,
        'snhole': 96,
        'file_attr':'normal',
        'name_before':'d:\aa\origin\batch#20#hole#a5_org.jpg',
        'video_before':'d:\aa\origin\batch#20#hole#a5_video.mp4',
        'cap_time':'2019-06-05 20:00:00',
        'name_after':'d:\aa\mid\batch#20#hole#a5_cfy.jpg',
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
    'cmd':'hstUpdateFluCfy',
    }

TUP_HST_PCT_UPDATE_FLU_CFY_OUT = {
    'cmd':'hstUpdateFluCfy',
    }


#读取普通图片 hstReadPic
TUP_HST_PCT_READ_PIC_IN = {
    'cmd':'hstReadPic',
    'batch_number': 100,
    'hole_number': 96,
    }

TUP_HST_PCT_READ_PIC_OUT = {
    'cmd':'hstReadPic',
    'error_no': 'no_error',
    'cebs_pvci_eleg': {
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
    'cmd':'hstReadFlu',
    }

TUP_HST_PCT_READ_FLU_OUT = {
    'cmd':'hstReadFlu',
    }

#更新图片统计 hstUpdateStatis
TUP_HST_PCT_UPDATE_STATIS_IN = {
    'cmd':'hstUpdateStatis',
    }

TUP_HST_PCT_UPDATE_STATIS_OUT = {
    'cmd':'hstUpdateStatis',
    }

#更新用户日志 hstUpdateUserLog
TUP_HST_PCT_UPDATE_USER_LOG_IN = {
    'cmd':'hstUpdateUserLog',
    }

TUP_HST_PCT_UPDATE_USER_LOG_OUT = {
    'cmd':'hstUpdateUserLog',
    }


'''
#CEWORM的图像处理部分，专门用于TUP相关的图像识别及处理算法

预期支持的图像处理及识别算法包括
 - 白光线虫图像模式识别算法
 - 荧光线虫图像模式识别算法
 - 线虫堆叠图像模式识别算法
 - 细胞计数模式识别算法
 - 菌落计数模式识别算法
 - 线虫视频识别算法
 - 线虫深度学习算法
 - 菌落深度学习算法

'''


TUP_HST_VCEG_WHITE_PIC_CFY_IN = {
    'cmd':'hstWhitePicCfy',
    'snbatch': 100,
    'snhole': 96,
    'file_attr':'normal',
    'name_before':'d:\aa\origin\batch#20#hole#a5_org.jpg',
    'cap_time':'2019-06-05 20:00:00',
    'name_after':'d:\aa\mid\batch#20#hole#a5_cfy.jpg',
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
    }

TUP_HST_VCEG_WHITE_PIC_CFY_OUT = {
    'cmd':'hstWhitePicCfy',
    'snbatch': 100,
    'snhole': 96,
    'file_attr':'normal',
    'name_before':'d:\aa\origin\batch#20#hole#a5_org.jpg',
    'cap_time':'2019-06-05 20:00:00',
    'name_after':'d:\aa\mid\batch#20#hole#a5_cfy.jpg',
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
    }

TUP_HST_VCEG_WHITE_VIDEO_CFY_IN = {
    'cmd':'hstWhitePicCfy',
    'snbatch': 100,
    'snhole': 96,
    'file_attr':'normal',
    'video_before':'d:\aa\origin\batch#20#hole#a5_video_org.mp4',
    'cap_time':'2019-06-05 20:00:00',
    'video_before':'d:\aa\origin\batch#20#hole#a5_video_cfy.mp4',
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
    }

TUP_HST_VCEG_WHITE_VIDEO_CFY_OUT = {
    'cmd':'hstWhitePicCfy',
    'file-attr':'normal', #'normal', 'flu'
    'batchNbr':123,
    'holeNbr':25,    
    'video_before':'d:\aa\origin\batch#20#hole#a5_video_org.mp4',
    'cap_time':'2019-06-05 20:00:00',
    'video_before':'d:\aa\origin\batch#20#hole#a5_video_cfy.mp4',
    'rec_time':'2019-06-05 20:00:00',
    'cap_time':'2019-06-05 20:00:00',
    'bigalive':20,
    'bigdead':30,
    'midalive':40,
    'middead':20,
    'smalive':10,
    'smdead':5,
    'totalalive':100,
    'totaldead':50,
    'totalsum':300,
    }





















