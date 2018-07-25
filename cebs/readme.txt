====CEBS=====
















//=ZJL, 2018/7/26, CURRENT_SW_DELIVERY R1.08 =>CEBS
= 增加视频流获取功能
= 视频流控制参数并存入全局变量ini文件
= 调整视频现场演示过程中的问题 1）驱动连不上 2）巡游时程序崩溃 3）坐标改为左下/右上，对应摄像头坐标反过来
= 依然有问题的地方：试图使用信号槽实现MOTOAPI的打印，没成功
= 利用信号槽，让MOTO和CTRLTHREAD通信，没成功，所以识别干完了之后，没法让CTRLTHREAD的状态机自动复位
= 优化视频拍摄对摄像头的支持

//=ZJL, 2018/7/24, CURRENT_SW_DELIVERY R1.07 =>CEBS
= CAMERA的编号可以人工选择，而且纳入工程参数的配置中去，一旦选定，配置文件会记录在案
= CAMERA的数量，开机启动时会自行刷一遍，0-100，方便人工选择具体哪一个摄像头
= 增加VISION识别功能
= 完善参数控制的全局定义

//=ZJL, 2018/7/21, CURRENT_SW_DELIVERY R1.06 =>CEBS
= 新建参数配置页面
= 新参数初始化更新
= 新参数全部存入初始化的文件中去
= ErrorLog
= MOTOAPI的Bug

//=ZJL, 2018/7/20, CURRENT_SW_DELIVERY R1.05 =>CEBS
= 增加潜在的自动识别和定时拍照界面，但功能并未实现
= 增加定点拍照选项：实现完整
= 增加串口是否打开的固定选项，HARD-CODE，方便调测。正式版本需要放开。
= 优化串口端口搜索的方式，做到了自动化
= 准备增加基础的操作错误信息，方便调测和问题的解决！

//=ZJL, 2018/7/20, CURRENT_SW_DELIVERY R1.04 =>CEBS
= 为满足定点拍照、MOTOAPI未安装时的调测，增加两个COMM级别的标识位，方便调测。正式交付时注意修改为默认模式。
#Fix point to take picture or not? Formally auto-working shall set as False.
GL_CEBS_PIC_TAKING_FIX_POINT_SET = True; 
#To enable debug UI under MOTOAPI not yet installed. Formally it sets as True.
GL_CEBS_MOTOAPI_INSTALLED_SET = False;  

//=ZJL, 2018/7/20, CURRENT_SW_DELIVERY R1.03 =>CEBS
= 界面生成
  cd form_qt, 
  pyuic5 -o  cebsmainform.py cebsMainform.ui    
  pyuic5 -o  cebscalibform.py cebsCalibform.ui
  pyuic5 -o  cebsgparform.py cebsGparform.ui
= 安装包生成
  d:, cd \IHUSRC\med\cebs
  pyinstaller -F -w --icon=.\icon_res\cebs.ico cebsMain.py
= 交付第一个版本20180720版

//=ZJL, 2018/7/18, CURRENT_SW_DELIVERY R1.02 =>CEBS
= 将所有中文乱码全部改为英文
= 修正校准中最大X-Y轴的尺寸问题
= 临时性停止MOTO-API函数对象，以便于调试。未来得想办法将这个启动改为参数设定，在界面启动之后再行启动它。

//=ZJL, 2018 May.15, CURRENT_SW_DELIVERY R1.01 =>CEBS
= 创建CEBS项目

