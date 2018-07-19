====CEBS=====













//=ZJL, 2018/7/20, CURRENT_SW_DELIVERY R1.04 =>CEBS
= 为满足定点拍照、MOTOAPI未安装时的调测，增加两个COMM级别的标识位，方便调测。正式交付时注意修改为默认模式。
#Fix point to take picture or not? Formally auto-working shall set as False.
GL_CEBS_TAKING_PIC_FIX_POINT_SET = True; 
#To enable debug UI under MOTOAPI not yet installed. Formally it sets as True.
GL_CEBS_MOTOAPI_INSTALLED_SET = False;  

//=ZJL, 2018/7/20, CURRENT_SW_DELIVERY R1.03 =>CEBS
= 界面生成
  cd form_qt, pyuic5 -o  cebsmainform.py cebsMainform.ui,    pyuic5 -o  cebscalibform.py cebsCalibform.ui
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

