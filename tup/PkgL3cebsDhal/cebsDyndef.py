'''
Created on 2019年6月3日

@author: Administrator
'''

#系统控制参数
strTupGlParCtrlCfg =\
{
    'ERR_LOG_FILE_NAME_SET':"cebsErrLog.txt",
    'CMD_LOG_FILE_NAME_SET':"cebsCmdLog.txt",
    #固定参数部分
    'PIC_ORIGIN_PATH':'pic_origin',
    'PIC_MIDDLE_PATH':'pic_middle',
    #FILE ATTRIBUTE
    'FILE_ATT_NORMAL':'normal',
    'FILE_ATT_FLUORESCEN':'flu',    #荧光 Fluorescen
    'CFG_FILE_NAME':'cebsConfig.ini',
    #工作目录
    'PIC_WORK_DIR':'',
    #控制参数
    'PIC_PROC_BATCH_INDEX':0,
    'PIC_PROC_CLAS_INDEX':0,
    'PIC_PROC_REMAIN_CNT':0,
    'PIC_FLU_CLAS_INDEX':0, #指向FLU的指针起点
    'PIC_FLU_REMAIN_CNT':0, #剩余的FLU数量
    'PIC_ABS_ORIGIN_PATH':'',
    'PIC_ABS_MIDDLE_PATH':'',
}

#托盘参数
strTupGlParPlate =\
{
    'HB_TARGET_TYPE':'',    #托盘类型
    'LEN_UNIT':'um',
    'HB_HOLE_X_NUM':0,      #HOW MANY BOARD HOLES，X DIRECTION
    'HB_HOLE_Y_NUM':0,      #HOW MANY BOARD HOLES，Y DIRECTION
    'HB_WIDTH_X_SCALE':0,   
    'HB_HEIGHT_Y_SCALE':0,
    'HB_POS_IN_UM':[0, 0, 0, 0],#USING INT, um, 96 HOLES, POSITION OF = X1/Y1(LEFT-DOWN), X2/Y2(RIGHT-UP)
    'HB_CUR_POS_IN_UM': [0, 0],  #USING INT, um, POSITION X/Y AXIS
}
    

#图像参数
strTupGlParPic =\
{
    #定点拍照
    'PIC_TAKING_FIX_POINT_SET':False,
    #增加二次曝光功能试图解决图片模糊的问题
    'PIC_SECOND_AUTOEXPO_SET':False,    
    #After taking picture, whether the pic identification will be run automatically
    #拍照后是否自动识别
    'PIC_CLASSIFIED_AFTER_TAKE_SET':False,
    #Whether taking picture will be happened automatically after starting.
    #设备启动后是否自动工作-界面叫定时自动拍照
    'PIC_AUTO_WORKING_AFTER_START_SET':False,    
    #模糊度阈值       NF3
    'PIC_BLURRY_LIMIT':5000,
    #Auto taking picture TTI times in minutes
    #定时工作时长间隔
    'PIC_AUTO_WORKING_TTI_IN_MIN':60,
    #TEMP USAGE VARIABLES => 用于浮动式界面展示，暂时不用
    #VISION calibration set
    'SMALL_LOW_LIMIT':200,
    'SMALL_MID_LIMIT':500,
    'MID_BIG_LIMIT':2000,
    'BIG_UPPER_LIMIT':5000,
    #VISION CLASSIFICATION RESULT ADDUP (输出图像叠加标记)
    'CLAS_RES_ADDUP_SET':True,
    #VIDEO CAPTURE ENABLE OR NOT (视频录制参数)
    'CAPTURE_ENABLE':True,
    'CAPTURE_DUR_IN_SEC':3,
    #SCALE ENABLE SET
    'PIC_SCALE_ENABLE_FLAG':False,
    #图像识别中所用到的部分参数：将根据算法演进
    'CFY_THD_GENR_PAR1':0,
    'CFY_THD_GENR_PAR2':0,
    'CFY_THD_GENR_PAR3':0,
    'CFY_THD_GENR_PAR4':0,
}

#串口参数
strTupGlParSps =\
{
    'SPS_MENGPAR_ADDR':0x77,
    'SPS_MENGPAR_CMD_LEN':18,
    'MOTOR_MAX_SPD':20,    #NF1 rad/s
    'MOTOR_MAX_ACC':20,  #NF1 rad/s2
    'MOTOR_MAX_DEACC':20,  #NF1 rad/s2
    'MOTOR_ZERO_SPD':20, #NF1 rad/s
    'MOTOR_ZERO_ACC':20, #NF1 rad/s2
    'MOTOR_MAX_RETRY_TIMES':150, #正常需要放置150次数，
    'PILOT_WOKING_ROUNDS_MAX':5,
}


#MOTOR_STEPS_PER_DISTANCE_MM = MOTOR_STEPS_PER_ROUND / MOTOR_DIS_MM_PER_ROUND
#MOTOR_STEPS_PER_DISTANCE_UM = MOTOR_STEPS_PER_ROUND / MOTOR_DIS_MM_PER_ROUND / 1000    


#FSPC参数
strTupGlParFspc =\
{
    'FSPC_COEF_MARK_LINE':150, #NF2
    'FSPC_COEF_MARK_WIDTH':10,
    'FSPC_COEF_MARK_AREA':10000,
    'FSPC_COEF_MARK_DILATE':12,
    'FSPC_COEF_AREA_MIN':10000,
    'FSPC_COEF_AREA_MAX':100000,
    'FSPC_COEF_AREA_DILATE':12,
    'FSPC_COEF_AREA_ERODE':5,
    'FSPC_COEF_CELL_MIN':920,
    'FSPC_COEF_CELL_MAX':1500,
    'FSPC_COEF_RADUIS_MIN':19,
    'FSPC_COEF_RADUIS_MAX':23,
    'FSPC_COEF_CELL_DILATE':61,
    'FSPC_COEF_CELL_ERODE':5,
    'FSPC_COEF_CELL_CE':50,
    'FSPC_COEF_CELL_DIST':30,
    'FSPC_PIC_TRAIN_DELAY':5,
    'FSPC_ADDUP_SET':True,   
}






