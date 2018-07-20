'''
Created on Jun 16, 2018

@author: hitpony
'''

import serial
import serial.tools.list_ports
import time
from asyncio.tasks import sleep

SerialPortIndex = 0
Speed = 400
Step = 6400
Version = '0'

IsSerialPortOpenned = False
MotorStatusIsRunning = [0, 0, 0, 0]
MotorCmdStrEmergStop = 'M03 1 1 1 1 \r\n'
MotorCmdStrSlowStop = 'M04 1 1 1 1 \r\n'
MotorCmdStrGoWithSteps = 'M01'
MotorCmdStrGoWithSpeed = 'M02'
MotorCmdStrBackToZero = 'M05 -400 -400 0 0 \r\n'
MotorCmdStrReadVersion = 'Q01\r\n' 
MotorCmdStrReadParamters = 'Q02\r\n'
MotorCmdStrReadStatus = 'Q03\r\n'

' Default parameters for motor '
MOTOR_DISTANCE_MM_PER_ROUND = 5
MOTOR_STEPS_PER_ROUND = 12800
MOTOR_DEFAULT_SPEED = 300
MOTOR_STEPS_PER_DISTANCE_MM = MOTOR_STEPS_PER_ROUND / MOTOR_DISTANCE_MM_PER_ROUND
MOTOR_STEPS_PER_DISTANCE_UM = MOTOR_STEPS_PER_ROUND / MOTOR_DISTANCE_MM_PER_ROUND / 1000
    
class MotorClass():
    '''
    classdocs
    '''
    cur_x_position_mm = 0
    cur_y_position_mm = 0
    top_left_x_position_mm = 0
    top_left_y_position_mm = 0
    bot_right_x_position_mm = 0
    bot_right_y_position_mm = 0
    IsSerialOpenOk = False
    serialFd = serial.Serial()
    targetComPortString = ''

    def __init__(self):
        '''
        Constructor
        '''
        plist = list(serial.tools.list_ports.comports())
        self.targetComPortString = 'Prolific USB-to-Serial Comm Port ('
        if len(plist) <= 0:
            print ("MOTOAPI: The Serial port can't find!")
        else:
            plist_0 =list(plist[0])
            searchComPartString = ''
            #Find right COM# with 'Prolific USB-to-Serial Comm Port'
            for comPortStr in plist_0:
                indexStart = comPortStr.find(self.targetComPortString)
                indexEnd = comPortStr.find(')')
                if (indexStart >= 0) and (indexEnd >=0) and (indexEnd > len(self.targetComPortString)):
                    searchComPartString = comPortStr[len(self.targetComPortString):indexEnd]
            if searchComPartString == '':
                #serialName = plist_0[0]
                print("MOTOAPI: Can not find right serial port!")
                return
            else:
                print("MOTOAPI: serial port = ", searchComPartString)
                serialName = searchComPartString
            self.serialFd = serial.Serial(serialName, 115200, timeout = 5)
            self.IsSerialOpenOk = True
            print("MOTOAPI:" + str(self.serialFd))
            print("MOTOAPI: Initialized SerialFd OK")
            vernum = self.motor_api_read_version()
            print("MOTOAPI: version =", vernum)

    def motor_test(self):
            print("check which port was really used >", self.serialFd.name)
            ret = self.serialFd.isOpen()
            print("Open >", ret)
            print("Test 1: motor_api_read_version("", serialFd)")            
            self.motor_api_read_version()                      
            
            print("Test 2: motor_api_read_status("", serialFd)")
            self.motor_api_read_status()
            
            print("Test 3: motor_api_emergency_stop("", serialFd, 1, 1, 1, 1)")          
            #MotorClass.motor_api_emergency_stop("", serialFd, 1, 1, 1, 1)
            time.sleep(1)
            self.motor_api_read_status()            
            time.sleep(1)
             
            print("Test 4: motor_api_slow_stop("", serialFd, 1, 1, 1, 1)")
            #MotorClass.motor_api_slow_stop("", serialFd, 1, 1, 1, 1)
            time.sleep(1)
            self.motor_api_read_status()
            time.sleep(1)
             
            print("Test 5: motor_api_go_with_steps(serialFd, 6400, 6400, 6400, 6400)")
            #MotorClass.motor_api_go_with_steps("", serialFd, 6400, 6400, 6400, 6400)
            time.sleep(0)
            self.motor_api_read_status()
            time.sleep(1)
            self.motor_api_emergency_stop(1, 1, 1, 1)
            time.sleep(1)
            self.motor_api_read_status()            
            time.sleep(1)
             
             
            print("Test 6: motor_api_go_with_steps(serialFd, -6400, -6400, -6400, -6400)")
            #MotorClass.motor_api_go_with_steps("", serialFd, -6400, -6400, -6400, -6400)
            time.sleep(0)
            self.motor_api_read_status()
            time.sleep(1)
            self.motor_api_emergency_stop(1, 1, 1, 1)
            time.sleep(1)
            self.motor_api_read_status()            
            time.sleep(1)

            print("Test 7: motor_api_go_with_steps(serialFd, 100, 100, 100, 100)")
            self.motor_api_go_with_speed(100, 100, 100, 100)
            time.sleep(5)
            self.motor_api_read_status()
            time.sleep(1)
            self.motor_api_slow_stop(1, 1, 1, 1)
            time.sleep(1)
            self.motor_api_read_status()            
            time.sleep(1)

            print("Test 8: motor_api_go_with_steps(serialFd, 100, 100, 100, 100)")
            self.motor_api_back_to_zero(100, 100, 100, 100)
            
    def motor_api_read_version(self):
        if(self.IsSerialOpenOk == False):
            print("MOTOAPI: Serial is not opened, return")
            return
        self.serialFd.reset_input_buffer()
        self.serialFd.reset_output_buffer()
        self.serialFd.write(MotorCmdStrReadVersion.encode())
        #time.sleep(1)
        Version = self.serialFd.readline()
        print("Version = ", Version)
        if Version == b'':
            return -1;
        VerNumber = Version.split()[0]
        print("VerNumber = ", VerNumber)
        if int(VerNumber) == 37:
            self.IsSerialOpenOk = True
        else:
            self.IsSerialOpenOk = False
        print("IsSerialOpenOk =", self.IsSerialOpenOk)
        return int(VerNumber)
        
    def motor_api_read_status(self):
        if(self.IsSerialOpenOk == False):
            print("MOTOAPI: Serial is not opened, return")
            return
        MotorStatusStr = ['0','0','0','0']
        self.serialFd.reset_input_buffer()
        self.serialFd.reset_output_buffer()
        self.serialFd.write(MotorCmdStrReadStatus.encode())
        #time.sleep(1)
        MotorStatusStrFull = self.serialFd.readline()
        print("MotorStatusStr = ", MotorStatusStrFull)
        MotorStatusStr[0] = MotorStatusStrFull.split()[0]
        MotorStatusStr[1] = MotorStatusStrFull.split()[1]
        MotorStatusStr[2] = MotorStatusStrFull.split()[2]
        MotorStatusStr[3] = MotorStatusStrFull.split()[3]
        print("MotorStatusStr[0] = ", MotorStatusStr[0])
        print("MotorStatusStr[1] = ", MotorStatusStr[1])
        print("MotorStatusStr[2] = ", MotorStatusStr[2])
        print("MotorStatusStr[3] = ", MotorStatusStr[3])
        MotorStatusIsRunning[0] = int(MotorStatusStr[0])
        MotorStatusIsRunning[1] = int(MotorStatusStr[1])
        MotorStatusIsRunning[2] = int(MotorStatusStr[2])
        MotorStatusIsRunning[3] = int(MotorStatusStr[3])
        print("MotorStatusIsRunning[0] = ", MotorStatusIsRunning[0])
        print("MotorStatusIsRunning[1] = ", MotorStatusIsRunning[1])
        print("MotorStatusIsRunning[2] = ", MotorStatusIsRunning[2])
        print("MotorStatusIsRunning[3] = ", MotorStatusIsRunning[3])
        return MotorStatusIsRunning

    def motor_api_emergency_stop(self, motor1, motor2, motor3, motor4):
        if(self.IsSerialOpenOk == False):
            print("MOTOAPI: Serial is not opened, return")
            return
        MotorCmdStringToSend = 'M03 ' + str(motor1) + ' ' + str(motor2) + ' '+ str(motor3) + ' '+ str(motor4) + ' ' + '\r\n'
        print("MotorCmdStringToSend = ", MotorCmdStringToSend)    
        self.serialFd.reset_input_buffer()
        self.serialFd.reset_output_buffer()
        self.serialFd.write(MotorCmdStringToSend.encode())
        #time.sleep(1)
        if motor1 == 1:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn1 = ", MotorReturn)
        if motor2 == 1:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn2 = ", MotorReturn)
        if motor3 == 1:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn3 = ", MotorReturn)
        if motor4 == 1:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn4 = ", MotorReturn)
                            
    def motor_api_slow_stop(self, motor1, motor2, motor3, motor4):
        if(self.IsSerialOpenOk == False):
            print("MOTOAPI: Serial is not opened, return")
            return
        MotorStatusStr = ['0','0','0','0']
        MotorCmdStringToSend = 'M04 ' + str(motor1) + ' ' + str(motor2) + ' '+ str(motor3) + ' '+ str(motor4) + ' ' + '\r\n'
        print("MotorCmdStringToSend = ", MotorCmdStringToSend)    
        self.serialFd.reset_input_buffer()
        self.serialFd.reset_output_buffer()
        self.serialFd.write(MotorCmdStringToSend.encode())
        #time.sleep(1)
        if motor1 == 1:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn1 = ", MotorReturn)
        if motor2 == 1:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn2 = ", MotorReturn)
        if motor3 == 1:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn3 = ", MotorReturn)
        if motor4 == 1:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn4 = ", MotorReturn)
        self.serialFd.write(MotorCmdStrReadStatus.encode())    
        MotorStatusStrFull = self.serialFd.readline()
        MotorStatusStr[0] = MotorStatusStrFull.split()[0]
        MotorStatusStr[1] = MotorStatusStrFull.split()[1]
        MotorStatusStr[2] = MotorStatusStrFull.split()[2]
        MotorStatusStr[3] = MotorStatusStrFull.split()[3]
        wait_time = 0
        while (MotorStatusStr[0] != b'0' or MotorStatusStr[1] != b'0' or MotorStatusStr[2] != b'0' or MotorStatusStr[3] != b'0'):
            self.serialFd.write(MotorCmdStrReadStatus.encode())    
            MotorStatusStrFull = self.serialFd.readline()
            print("(MotorStatusStrFull, wait_time, MotorStatusStrFull[0:2]) =", (MotorStatusStrFull, wait_time, MotorStatusStrFull[0:2]) )
            if MotorStatusStrFull[0] != b'0' or MotorStatusStrFull[0] != b'1' :
                MotorStatusStr[0] = MotorStatusStrFull.split()[0]
                MotorStatusStr[1] = MotorStatusStrFull.split()[1]
                MotorStatusStr[2] = MotorStatusStrFull.split()[2]
                MotorStatusStr[3] = MotorStatusStrFull.split()[3]
                time.sleep(1)
            wait_time = wait_time + 1
            if wait_time > 10:
                break                  

    def motor_api_go_with_steps(self, motor1_steps, motor2_steps, motor3_steps, motor4_steps):
        if(self.IsSerialOpenOk == False):
            print("MOTOAPI: Serial is not opened, return")
            return
        MotorCmdStringToSend = 'M01 ' + str(motor1_steps) + ' ' + str(motor2_steps) + ' '+ str(motor3_steps) + ' '+ str(motor4_steps) + ' ' + '\r\n'
        print("MotorCmdStringToSend = ", MotorCmdStringToSend)    
        self.serialFd.reset_input_buffer()
        self.serialFd.reset_output_buffer()        
        self.serialFd.write(MotorCmdStringToSend.encode())
        if int(motor1_steps) != 0:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn1 = ", MotorReturn)
        if int(motor2_steps) != 0:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn2 = ", MotorReturn)
        if int(motor3_steps) != 0:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn3 = ", MotorReturn)
        if int(motor4_steps) != 0:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn4 = ", MotorReturn)

    def motor_api_go_with_speed(self, motor1_speed, motor2_speed, motor3_speed, motor4_speed):
        if(self.IsSerialOpenOk == False):
            print("MOTOAPI: Serial is not opened, return")
            return
        MotorCmdStringToSend = 'M02 ' + str(motor1_speed) + ' ' + str(motor2_speed) + ' '+ str(motor3_speed) + ' '+ str(motor4_speed) + ' ' + '\r\n'
        print("MotorCmdStringToSend = ", MotorCmdStringToSend)    
        self.serialFd.reset_input_buffer()
        self.serialFd.reset_output_buffer()
        self.serialFd.write(MotorCmdStringToSend.encode())
        if int(motor1_speed) != 0:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn1 = ", MotorReturn)
        if int(motor2_speed) != 0:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn2 = ", MotorReturn)
        if int(motor3_speed) != 0:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn3 = ", MotorReturn)
        if int(motor4_speed) != 0:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn4 = ", MotorReturn)
            
    def motor_api_back_to_zero(self, motor1_speed, motor2_speed, motor3_speed, motor4_speed):
        if(self.IsSerialOpenOk == False):
            print("MOTOAPI: Serial is not opened, return")
            return        
        MotorStatusStr = ['0','0','0','0']
        MotorCmdStringToSend = 'M05 ' + str(motor1_speed) + ' ' + str(motor2_speed) + ' '+ str(motor3_speed) + ' '+ str(motor4_speed) + ' ' + '\r\n'
        print("MOTOAPI: MotorCmdStringToSend = ", MotorCmdStringToSend)    
        self.serialFd.reset_input_buffer()
        self.serialFd.reset_output_buffer()
        self.serialFd.write(MotorCmdStringToSend.encode())
        if int(motor1_speed) != 0:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn1 = ", MotorReturn)
            MotorReturn = self.serialFd.readline()
            print("MotorReturn1 = ", MotorReturn)
        if int(motor2_speed) != 0:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn2 = ", MotorReturn)
            MotorReturn = self.serialFd.readline()
            print("MotorReturn2 = ", MotorReturn)
        if int(motor3_speed) != 0:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn3 = ", MotorReturn)
            MotorReturn = self.serialFd.readline()
            print("MotorReturn3 = ", MotorReturn)
        if int(motor4_speed) != 0:        
            MotorReturn = self.serialFd.readline()
            print("MotorReturn4 = ", MotorReturn)
            MotorReturn = self.serialFd.readline()
            print("MotorReturn4 = ", MotorReturn)
        self.serialFd.write(MotorCmdStrReadStatus.encode())    
        MotorStatusStrFull = self.serialFd.readline()
        print("MotorStatusStrFull=", MotorStatusStrFull)
        if MotorStatusStrFull[0] == 48 or MotorStatusStrFull[0] == 49 :
            MotorStatusStr[0] = MotorStatusStrFull.split()[0]
            MotorStatusStr[1] = MotorStatusStrFull.split()[1]
            MotorStatusStr[2] = MotorStatusStrFull.split()[2]
            MotorStatusStr[3] = MotorStatusStrFull.split()[3]
        else:
            MotorStatusStrFull = self.serialFd.readline()
            print("MotorStatusStrFull=", MotorStatusStrFull)
            return
        wait_time = 0
        while (MotorStatusStr[0] != b'0' or MotorStatusStr[1] != b'0' or MotorStatusStr[2] != b'0' or MotorStatusStr[3] != b'0'):
            self.serialFd.write(MotorCmdStrReadStatus.encode())    
            MotorStatusStrFull = self.serialFd.readline()
            print("(MotorStatusStrFull, wait_time, MotorStatusStrFull[0:2]) =", (MotorStatusStrFull, wait_time, MotorStatusStrFull[0:2]), MotorStatusStrFull[0], MotorStatusStrFull[1] )
            if MotorStatusStrFull[0] == 48 or MotorStatusStrFull[0] == 49 :  #40 is b'0', 49 is b'1'
                MotorStatusStr[0] = MotorStatusStrFull.split()[0]
                MotorStatusStr[1] = MotorStatusStrFull.split()[1]
                MotorStatusStr[2] = MotorStatusStrFull.split()[2]
                MotorStatusStr[3] = MotorStatusStrFull.split()[3]
                print("MotorStatusStr[0:3]=", MotorStatusStr[0], MotorStatusStr[1], MotorStatusStr[2], MotorStatusStr[3])
                time.sleep(0.5)
            else:
                time.sleep(0.2)
            wait_time = wait_time + 1
            if wait_time > 60:
                break

    def moto_proc_wait_for_stop(self, timeout_seconds):
        if(self.IsSerialOpenOk == False):
            print("MOTOAPI: Serial is not opened, return")
            return
        MotorStatusStr = ['0','0','0','0']
        self.serialFd.write(MotorCmdStrReadStatus.encode())    
        MotorStatusStrFull = self.serialFd.readline()
        MotorStatusStr[0] = MotorStatusStrFull.split()[0]
        MotorStatusStr[1] = MotorStatusStrFull.split()[1]
        MotorStatusStr[2] = MotorStatusStrFull.split()[2]
        MotorStatusStr[3] = MotorStatusStrFull.split()[3]
        wait_time = 0
        while (MotorStatusStr[0] != b'0' or MotorStatusStr[1] != b'0' or MotorStatusStr[2] != b'0' or MotorStatusStr[3] != b'0'):
            self.serialFd.write(MotorCmdStrReadStatus.encode())    
            MotorStatusStrFull = self.serialFd.readline()
            print("(MotorStatusStrFull, wait_time, MotorStatusStrFull[0:2]) =", (MotorStatusStrFull, wait_time, MotorStatusStrFull[0:2]) )
            if MotorStatusStrFull[0] != b'0' or MotorStatusStrFull[0] != b'1' :
                MotorStatusStr[0] = MotorStatusStrFull.split()[0]
                MotorStatusStr[1] = MotorStatusStrFull.split()[1]
                MotorStatusStr[2] = MotorStatusStrFull.split()[2]
                MotorStatusStr[3] = MotorStatusStrFull.split()[3]
            time.sleep(0.2)
            wait_time = wait_time + 1
            if wait_time > timeout_seconds:
                break
            
    def moto_proc_full_stop(self):
        self.motor_api_emergency_stop(1, 1, 1, 1)
            
    def moto_proc_back_to_zero(self):
        if(self.IsSerialOpenOk == False):
            print("MOTOAPI: Serial is not opened, return")
            return
        print("MOTOAPI: motor_api_back_to_zero(self, MOTOR_DEFAULT_SPEED, MOTOR_DEFAULT_SPEED, 0, 0)")        
        self.motor_api_back_to_zero((-1)*MOTOR_DEFAULT_SPEED, (-1)*MOTOR_DEFAULT_SPEED, 0, 0)

    def moto_proc_move_delta_axis_postion(self, PxDelta, PyDelta):
        if(self.IsSerialOpenOk == False):
            print("MOTOAPI: Serial is not opened, return")
            return        
        x_move_steps = int(PxDelta / MOTOR_STEPS_PER_DISTANCE_MM)
        y_move_steps = int(PyDelta / MOTOR_STEPS_PER_DISTANCE_MM)  
        self.motor_api_go_with_steps(x_move_steps, y_move_steps, 0, 0)
        self.moto_proc_wait_for_stop(60)

    def moto_proc_move_to_axis_postion(self, curPx, curPy, newPx, newPy):
        if(self.IsSerialOpenOk == False):
            print("MOTOAPI: Serial is not opened, return")
            return        
        if ((0 == newPx) and (0 == newPy)):
            pass
            self.moto_proc_back_to_zero()
            return
        print("MOTOAPI: moto_proc_move_to_axis_postion (mm)", curPx, curPy, newPx, newPy)        
        x_move_steps = int((newPx - curPx) * MOTOR_STEPS_PER_DISTANCE_UM)
        y_move_steps = int((newPy - curPy) * MOTOR_STEPS_PER_DISTANCE_UM)
        if((0 == x_move_steps) and (0 == y_move_steps)):
            print("MOTOAPI: moto_proc_move_to_axis_postion (steps), all zero return", y_move_steps, x_move_steps, 0, 0)
            return  
        print("MOTOAPI: moto_proc_move_to_axis_postion (steps)", y_move_steps, x_move_steps, 0, 0)        
        self.motor_api_go_with_steps(y_move_steps, x_move_steps, 0, 0)
        self.moto_proc_wait_for_stop(90)
#SYSTEM ENTRY
if __name__ == '__main__':
    print("[CEBS] ", time.asctime(), ", System starting...\n" );
    Obj = MotorClass()
    Obj.motor_test()
