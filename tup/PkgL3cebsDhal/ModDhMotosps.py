'''
Created on 2019年6月3日

@author: Administrator
'''


from PkgL3cebsDhal.cebsConfig import *

import struct
import serial
import serial.tools.list_ports
import sys


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
    
    
    SPS_MENGPAR_ADDR  = 0x77
    SPS_MENGPAR_CMD_LEN = 18
    
    
    MOTOR_STEPS_PER_ROUND = 12800   #NF0
    MOTOR_DIS_MM_PER_ROUND = 3.1415926*20*1.05
    MOTOR_STEPS_PER_DISTANCE_MM = MOTOR_STEPS_PER_ROUND / MOTOR_DIS_MM_PER_ROUND
    MOTOR_STEPS_PER_DISTANCE_UM = MOTOR_STEPS_PER_ROUND / MOTOR_DIS_MM_PER_ROUND / 1000    
    
    def __init__(self):    
        super(clsCebsDhMotosps, self).__init__()  
    

    
    #给上层提供服务的函数
    def funcInitSps(self):
        #LC：ubuntu环境下，之前使用的那一套搜索设备符需要修改
        # 现在使用的方案是创建udev rules文件来处理的
        if sys.platform.startswith("linux"):
            try:
                self.serialFd = serial.Serial('/dev/cebsusb', 115200, timeout = 0.2)
            except Exception:
                self.IsSerialOpenOk = False
                #self.funcMotoErrTrace("L2MOTO: Serial exist, but can't open!")
                return -1
            self.IsSerialOpenOk = True
            #self.funcMotoLogTrace("L2MOTO: Success open serial port!")
            return 1
        
        #windows下
        if sys.platform.startswith("win32"):
            plist = list(serial.tools.list_ports.comports())
            self.targetComPortString = TUP_CEBS_SPS_USB_DBG_CARD2
            self.drvVerNbr = -1
            if len(plist) <= 0:
                #self.funcMotoErrTrace("L2MOTO: Not serial device installed!")
                return -2
            else:
                maxList = len(plist)
                searchComPartString = ''
                for index in range(0, maxList):
                    self.medErrorLog("L2MOTO: " + str(plist[index]))
                    plistIndex =list(plist[index])
                    string = ("L2MOTO: Sps Init = ", plistIndex)
                    self.tup_dbg_print(string)
                    #Find right COM#
                    for comPortStr in plistIndex:
                        indexStart = comPortStr.find(self.targetComPortString)
                        indexEnd = comPortStr.find(')')
                        if (indexStart >= 0) and (indexEnd >=0) and (indexEnd > len(self.targetComPortString)):
                            searchComPartString = comPortStr[len(self.targetComPortString):indexEnd]
                if searchComPartString == '':
                    #self.funcMotoErrTrace("L2MOTO: Can not find right serial port!")
                    return -1
                else:
                    #self.funcMotoLogTrace("L2MOTO: Serial port is to open = " + str(searchComPartString))
                    serialName = searchComPartString
                try:
                    self.serialFd = serial.Serial(serialName, 115200, timeout = 0.2)
                except Exception:
                    self.IsSerialOpenOk = False
                    #self.funcMotoErrTrace("L2MOTO: Serial exist, but can't open!")
                    return -1
                self.IsSerialOpenOk = True
                #self.funcMotoLogTrace("L2MOTO: Success open serial port!")
                return 1

    #命令打包
    def funcSendCmdPack(self, cmdId, par1, par2, par3, par4):
        #Build MODBUS COMMAND:系列化
        #add for test pules  command ID 0x38   
        if (cmdId == self.SPS_TEST_PULES_CMID):
            for i in range(1, par1+1, 500):
                fmt = ">BBiiii";
                byteDataBuf = struct.pack(fmt, self.SPS_MENGPAR_ADDR, cmdId, i, par2, par3, par4)
                crc = self.funcCacCrc(byteDataBuf, self.SPS_MENGPAR_CMD_LEN)
                fmt = "<H";
                byteCrc = struct.pack(fmt, crc)
                byteDataBuf += byteCrc
                #打印完整的BYTE系列
                index=0
                outBuf=''
                while index < (self.SPS_MENGPAR_CMD_LEN+2):
                    outBuf += str("%02X " % (byteDataBuf[index]))
                    index+=1
                #self.funcMotoLogTrace("L2MOTO: SND CMD = " + outBuf)
                res, Buf = self.funcCmdSend(byteDataBuf)
            return 1    
        else:
            fmt = ">BBiiii";    
            byteDataBuf = struct.pack(fmt, self.SPS_MENGPAR_ADDR, cmdId, par1, par2, par3, par4)
            crc = self.funcCacCrc(byteDataBuf, self.SPS_MENGPAR_CMD_LEN)
            fmt = "<H";
            byteCrc = struct.pack(fmt, crc)
            byteDataBuf += byteCrc
            #打印完整的BYTE系列
            index=0
            outBuf=''
            while index < (self.SPS_MENGPAR_CMD_LEN+2):
                outBuf += str("%02X " % (byteDataBuf[index]))
                index+=1
            #self.funcMotoLogTrace("L2MOTO: SND CMD = " + outBuf)
            res, Buf = self.funcCmdSend(byteDataBuf)
            if (res > 0):
                return Buf
            else:
                return res
            
    #单条命令的执行
    def funcCmdSend(self, cmd):
        #正常状态
        if(self.IsSerialOpenOk == False):
            #self.funcMotoErrTrace("L2MOTO: Serial not opened, cant not send command!")
            return -2,0
        #串口的确已经被打开了
        self.serialFd.readline()
        self.serialFd.write(cmd)
        rcvBuf = self.serialFd.readline()
        if (len(rcvBuf) > 1):
            while (rcvBuf[len(rcvBuf)-1] == 0x0A):
                rcvBuf2 = self.serialFd.readline()
                rcvBuf += rcvBuf2
        length = len(rcvBuf)
        if (length <=0):
            #self.funcMotoErrTrace("L2MOTO: Nothing received. RCV BUF = " + str(rcvBuf))
            return -3,0
        outBuf = ''
        for i in range(length):
            outBuf += ("%02X "%(rcvBuf[i]))
        #self.funcMotoLogTrace("L2MOTO: RCV BUF = " + outBuf)
        #Check CRC
        targetCrc = rcvBuf[length-2] + (rcvBuf[length-1]<<8)
        rcvCrc = self.funcCacCrc(rcvBuf, length-2)
        if (rcvCrc != targetCrc):
            #self.funcMotoErrTrace("L2MOTO: Receive CRC Error!")
            return -4,0
        if (rcvBuf[0] != cmd[0]):
            #self.funcMotoErrTrace("L2MOTO: Receive EquId Error!")
            return -5,0
        fmt = ">i";
        upBuf = rcvBuf[3:7]
        outPar = struct.unpack(fmt, upBuf)
        return 1, outPar[0]
    
    #计算CRC
    def funcCacCrc(self, buf, length):
        wCRC = 0xFFFF;
        index=0
        while index < length:
            wCRCOut = self.funcCrcOneChar(buf[index], wCRC)
            wCRC = wCRCOut
            index += 1
        wHi = wCRC // 256;
        wLo = wCRC % 256;
        wCRC = (wHi << 8) | wLo;
        return wCRC;

    #计算CRC支持功能
    def funcCrcOneChar(self, cDataIn, wCRCIn):
        wCheck = 0;
        wCRCIn = wCRCIn ^ cDataIn;
        i=0;
        while i<8:
            wCheck = wCRCIn & 1;
            wCRCIn = wCRCIn >> 1;
            wCRCIn = wCRCIn & 0x7fff;
            if (wCheck == 1):
                wCRCIn = wCRCIn ^ 0xa001;
            wCRCIn = wCRCIn & 0xffff;
            i += 1
        return wCRCIn;