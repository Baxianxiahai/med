====CEBS=====
【待完成FEATURE LIST】
1. 荧光识别算法：待定
3. 定时器无法自动及时结束


【BUG LIST】
1. Timer.cancel()没有真正起到作用，未来考虑使用terminate过程来强行终止线程的方法
2. def func_vision_worm_binvalue_proc(self, img):  new = np.zeros(img.shape, np.uint8)
3. 处于子菜单时，密码检查失败后的退出程序，没有真的起作用

【将QT工具生成的ui文件转化为py文件】
  cd form_qt, 
  pyuic5 -o  cebsmainform.py cebsMainform.ui    
  pyuic5 -o  cebscalibform.py cebsCalibform.ui
  pyuic5 -o  cebsgparform.py cebsGparform.ui
  pyuic5 -o  cebsmengform.py cebsMengform.ui  //Moto Engineering Command
  pyuic5 -o  cebssahtform.py cebsSahtform.ui  //Set Active Hole Target
  pyuic5 -o  cebsstestform.py cebsStestform.ui
  d:, cd \IHUSRC\med\cebs
  pyinstaller -F -w --icon=.\icon_res\cebs.ico cebsMain.py

【程序打包过程】
1.windows下cmd进入cebsMain.py文件所在目录下
2.执行：pyinstaller -F -w cebsMain.py 进行打包
3.注意：pyinstaller打包多进程程序出错解决办法
https://blog.csdn.net/zyc121561/article/details/82941056




//=ZJL, 2019/1/4, CURRENT_SW_DELIVERY R1.54 =>CEBS
= 将去噪声处理、灰度处理等过程，做成标准函数库

//=ZJL, 2019/1/3, CURRENT_SW_DELIVERY R1.53 =>CEBS
= 增加TUP_PICPROC图像处理模块

//=ZJL, 2019/1/2, CURRENT_SW_DELIVERY R1.52 =>CEBS
= 高端摄像头Obvious 5000KPA集成到我们的设备中来
= 去掉每一帧都设置分辨率的设置：相机反应不过来，无法每帧都设置，恢复到校准预览与拍摄的分辨率都相同的程度
= 将摄像头分辨率自动适配到型号上去

//=ZJL, 2019/1/1, CURRENT_SW_DELIVERY R1.52 =>CEBS
= 将捕获模式分辨率设为最大，但预览模式设置为1/4
= 去掉 GL_CEBS_VISION_CLAS_RESULT_FILE_NAME_SET / cebsVsClas.log识别结果的存储过程
4. 将图像识别后的结果，放到ini文件中去，去掉cebsVsClas.log记录文件。这是为了后续H5UI界面的开发。
= 为VM的TRACE打印，增加time.time()时间戳
= ini文件的FLUSH
2. 自动识别摄像头 => 按照模板，将摄像头的描述符增加到VISION模块中去，就可以实现更多摄像头的支持


//=ZJL, 2018/12/28, CURRENT_SW_DELIVERY R1.51 =>CEBS
= 搭建荧光细胞识别的方案

//=ZJL, 2018/12/28, CURRENT_SW_DELIVERY R1.50 =>CEBS
= 准备将界面工程纳入到单独的Package中去，以便准备将TUP改造为多任务体系
= 预期TUP将支持更多的项目类型，目前有CEBS、基于工控机的CebsMk2等，未来还有可能在其上叠加MQTT组件、RESTFUL组件等
    这样将TUP发展成为一个应用程序系列，而并不是简单的底层服务
  FAWS有可能架构在TUP体系之上
= 所以将cebsMain改为tupMain函数，统一化程序运行  
= 换成L1-L4的程序体系
= 将Saht框架弄出来


//=ZJL, 2018/12/27, CURRENT_SW_DELIVERY R1.49 =>CEBS
= 增加密钥控制过程

//=ZJL, 2018/12/26, CURRENT_SW_DELIVERY R1.48 =>CEBS
= 完善自测自检的功能列表
= 完善摄像头的初始化设置
= 拍照走S形道路

//=ZJL, 2018/12/25, CURRENT_SW_DELIVERY R1.47 =>CEBS
= 完善菜单界面
= 搭建了Stest的框架，目标是自检测试，方便客户进行自检测试，查找问题之所在

//=ZJL, 2018/12/24, CURRENT_SW_DELIVERY R1.46 =>CEBS
= 给每个界面增加swithOn()函数钩子，以便需要时做界面参数的初始化：其中GPAR是必须的，但其它界面暂时不需要
= 修正MENG界面中（设置限位器触发迟滞）的选择性BUG
= 完善任务的退出机制，确保安全退出
= 清理MOTO/VISION的硬件资源过程
= 增加公共FSM函数过程

//=ZJL, 2018/12/24, CURRENT_SW_DELIVERY R1.45 =>CEBS
= 完善TRAIN/FCC参数机制
= 完善func_ui_click_gpar_refresh_par()函数的放置过程：必须在close_event()的处理过程中更新VISION参数，将COM参数传进去，确保更新参数和放弃时（原始参数）都能正确的传到VISION模块
  确保下次操作还是正确的
= 增加GPAR在放弃参数时，二次进入后重新装载之前的参数，确保“放弃”动作是完善的
= 去掉GLVIS_PAR_SAV全局参量，只保留GLVIS_PAR_OFC，简化参数的存储逻辑
= 二次进入GPAR界面时，清理掉原始图形、生成图像、文件显示区内容

//=ZJL, 2018/12/21, CURRENT_SW_DELIVERY R1.44 =>CEBS
= 增加荧光体内细胞计数的程序框架
= 打通荧光识别的消息体系
= 将GPAR中4个通用参数纳入到代码体系中
= 准备完善算法过程
= FLU-CELL-COUNT: 门限参数有4个：小尺寸门限-细胞的最小面积尺寸，大尺寸门限-细胞的最大面积尺寸，通用门限1-细胞的高斯滤波门限，通用门限2-细胞的圆形度门限（NF2）

//=ZJL, 2018/12/19, CURRENT_SW_DELIVERY R1.43 =>CEBS
= 小罗完善图像延迟帧的问题
= 查阅为啥拍照中，荧光和普通图像的处理过程不一样
= 改进了maxTry的参数控制区域
= 改进pilot的状态机控制，这样可以随时停止巡游
= 解决了控制FLU/PIC的定点拍照bug
= 解决了识别文件的bug

//=ZJL, 2018/12/18, CURRENT_SW_DELIVERY R1.42 =>CEBS
= 去掉CAMER-NBR的人工选择，由VISION模块自动探测
= 修正CAPTURE_ENABLE的控制参数bug
= 简化ModCebsCom.GL参数，去掉前缀
= 增加功能：是否触发拍照完成后自动识别
= 启动后触发归零操作
= 启动后定时拍照触发+自动识别
= 定时周期拍照触发+自动识别
= 将识别图片后的叠加文字，改为CTRL-SCHD模块操控

//=ZJL, 2018/12/17, CURRENT_SW_DELIVERY R1.41 =>CEBS
= 完善ini文件中对于控制SECTION的处理
= 增加了batch#add-file的保护

//=ZJL, 2018/12/15, CURRENT_SW_DELIVERY R1.40 =>CEBS
= 完成基本的图像获取和识别消息框架

//=ZJL, 2018/12/15, CURRENT_SW_DELIVERY R1.39 =>CEBS
= 改进CALIB摄像头的工作模式：将文件传输模式改为内存对象传输指针模式，提高传输的通信速率。
   目前将定时器提高到0.4s/2.5fps，还可以工作。当提高到5fps时，视频采集请求会大量积累在TK_VISION任务模块的消息队列中，这说明基于队列的消息通信无法满足视频帧处理的要求
= 完善校准任务中的巡游功能

//=ZJL, 2018/12/14, CURRENT_SW_DELIVERY R1.38 =>CEBS
= 完善CALIB中摄像头的显示问题
= 去掉老旧TIMER工作机制
= 完善打印机制
= 解决了摄像头显示的问题，并将周期调整为0.5s的周期
= 校准位置移动
= 去掉TIMER的全局定义
= 完善校准模式下的拍照功能
= 去掉所有本地打印，在TRACE功能完善的情况下，这个是不需要的
= 增加一个去掉摄像头无限消息的TRACE-LEVEL，这样CALIB中的摄像头就可以打开了

//=ZJL, 2018/12/13, CURRENT_SW_DELIVERY R1.37 =>CEBS
= 优化msg_send函数
= 完成GPAR模块的完整工作流程
= 完善定时器工作模式
= 增加CALIB的视频展示框架

//=ZJL, 2018/12/13, CURRENT_SW_DELIVERY R1.36 =>CEBS
= 界面切换完善
= ERR: funcVisionDetectAllCamera()
= 因为要取出数据，字符串必须使用标准字符串格式
= 重要技巧：内部消息交换的格式，其实是嵌套的DICT格式，而不是字符串格式。当需要将参数从一个模块送到另外一个模块时，最好采用DICT的方式
          如果一定要使用字符串方式进行数据交互，则需要做json.loads(str())操作，而且字符串必须采用双引号的方式继续格式化
= 完成工参MENG模块的改造

//=ZJL, 2018/12/12, CURRENT_SW_DELIVERY R1.35 =>CEBS
= 建立起基本的任务框架 
= 进程模式改为了线程模式，速度快的不是一点点。VM中任务启动直接控制。
= 改为线程模式之后，可以使用全局变量来进行参数和对象传递

//=ZJL, 2018/12/10, CURRENT_SW_DELIVERY R1.34 =>CEBS
= 使用新的架构，创建VM机制
= 更新SPS-MOTO的处理过程
= 更新VISION函数
= 完善多任务之间的消息交互过程

//=ZJL, 2018/12/8, CURRENT_SW_DELIVERY R1.33 =>CEBS
= 完善CEBS REL2 RE-ARCH的代码框架
= CAM的权限管理完善
= 去掉了摄像头初始化后的3-4张黑屏照片

//=ZJL, 2018/12/5, CURRENT_SW_DELIVERY R1.32 =>CEBS
= 拉REL1的分支，保持原先的设计方法
= 增加锁机制，优化串口获取的同步性能
= 界面增加死锁，防止死掉
= 测试验证界面死锁的问题
= 将马达相关的命令，全部加上了时间同步保护，确保在没有完成之间界面无法点击

//=ZJL, 2018/11/1, CURRENT_SW_DELIVERY R1.31 =>CEBS
= 优化设计串口争抢机制
= 调整GPAR窗口大小，优化显示

//=ZJL, 2018/10/29, CURRENT_SW_DELIVERY R1.30 =>CEBS
= 增加查询一般性状态
= 增加图像标尺功能

//=ZJL, 2018/10/24, CURRENT_SW_DELIVERY R1.29 =>CEBS
= 改造完成了VISIOn中有关摄像头的自动识别问题，但界面和参数控制暂时未调整，等待这个方法完全稳定以后（在多台机器上测试，特别是WIN10下测试），再将
  摄像头端口控制（INI文件）、参数设置（界面+update ini文件+初始化更新）全部删掉，从而简化使用过程

//=ZJL, 2018/10/20, CURRENT_SW_DELIVERY R1.28 =>CEBS
= 基本完成

//=ZJL, 2018/10/18, CURRENT_SW_DELIVERY R1.27 =>CEBS
  cd form_qt, 
  pyuic5 -o  cebsmainform.py cebsMainform.ui    
  pyuic5 -o  cebscalibform.py cebsCalibform.ui
  pyuic5 -o  cebsgparform.py cebsGparform.ui
  pyuic5 -o  cebsmengform.py cebsMengform.ui  //Moto Engineering Command
  pyuic5 -o  cebssahtform.py cebsSahtform.ui  //Set Active Hole Target
  d:, cd \IHUSRC\med\cebs
  pyinstaller -F -w --icon=.\icon_res\cebs.ico cebsMain.py
= 增加clsL1_MdcThd模块和功能
= 解决了重复关闭MAIN窗口的问题
= 解决了MOTO界面反馈的问题
1. 如果将MOTOAPI的指令反馈到界面上

//=ZJL, 2018/10/9, CURRENT_SW_DELIVERY R1.26 =>CEBS
= 校准尺寸通过圆弧定标：基础算法搞定了一个，未来待跟实际结合起来使用

//=ZJL, 2018/10/8, CURRENT_SW_DELIVERY R1.25 =>CEBS
= 尝试使用重载功能，对付打印函数，非常好
= 对视频参数做封装处理
= 调整两种视频参数的放弃与设置
= 完善板型参数的控制方式
= 完善plate的参数封装
= 完善config的参数封装
4. 图像识别有bug: flu的启动不对，两者都不再识别了

//=ZJL, 2018/10/7, CURRENT_SW_DELIVERY R1.24 =>CEBS
= 完善cfg模块中对于各种图像的处理，增加荧光处理功能
= 增加视频文件的控制信息
= 增加视频文件的文件及目录信息
= 荧光图像处理的过程完善好了，就剩下算法部分的完善，待客户明确后再来敲定

//=ZJL, 2018/10/6, CURRENT_SW_DELIVERY R1.23 =>CEBS
= 启动拍照，先延迟5秒，跳过前面的摄像头对焦时间
= 增加校准条件下的抓图存图功能：采用去掉前几帧的方式
= 上科大朱老师提出：期望能在校准状态下将摄像头的视频能力提到，发下这是机器视频能力，暂时不调整
= ForceMove暂时灰掉

//=ZJL, 2018/9/30, CURRENT_SW_DELIVERY R1.22 =>CEBS
= 完善并增加MotoDrvNbr到界面上

//=ZJL, 2018/9/29, CURRENT_SW_DELIVERY R1.21 =>CEBS
= 优化VISION图像初始化时对于cap的RELEASE以及摄像头找不到时的处理
= 支持37和21两种驱动板，灵活选择
2. 校准图像放在在校准UI界面之外，而无法嵌入到内部图像显示部分
   -> QLable和GraphicsView控件，无法掌握其精髓，导致无法将该图像集成到UI界面里面
   -> 可以使用，不太美观完美

//=ZJL, 2018/9/28, CURRENT_SW_DELIVERY R1.20 =>CEBS
= 准备MOTO驱动的完善
= 调整好马达坐标的计算算法
3. L4MAIN在校准后的两次返回  => 不处理
4. 校准的共享库函数
5. 串口不安装时的优雅处理 => 目前的处理方式就是强制

//=ZJL, 2018/9/28, CURRENT_SW_DELIVERY R1.19 =>CEBS
= 继续完善状态机控制和界面内容
= 对CtrlSchdule模块进行了较大的修改与完善，主要是状态机
= 对VISION模块进行了修缮，去掉了任务模块，改为API函数形式，更加简单明了
= 调整并完善了Schedule模块的运行

//=ZJL, 2018/9/28, CURRENT_SW_DELIVERY R1.18 =>CEBS
3. 校准完成后，二次进入校准，无法激活摄像头继续进行校准
   -> CameraDisplay线程第二次启动不成功。如果让CameraDisplay线程持续运行，则难以控制其休眠状态
   -> 规避的方式是，重新再来。正常使用过程中，一旦校准好了，显微镜不再动，也不需要这个功能了
= 这个功能已经搞的比较完善了，等待删除垃圾代码
4. 工具重新启动以后，当前位置没有记录在ini文件中，可能导致第二次重启后直接做移动，马达会跑出界
   -> 因为程序在任何地方都可能奔溃，如果要记录马达当前位置，那意味着马达任意时刻的动作，都需要将当前位置存入ini文件，过于频繁且影响工具的正常运行
   -> 新启动后，应该先做位置归零。这个归零对于当前位置和马达来说，都是盲运动，一直到归零初始态
   -> 未来考虑，启动后就强制归零，可规避这个问题，但工具启动可能会比较慢。待用户使用一段时间后再考虑是否需要优化。
= 启动之后，强制归零，自然不存在这个问题了

//=ZJL, 2018/9/27, CURRENT_SW_DELIVERY R1.17 =>CEBS
= 对整个程序框架进行清理，尽量做到清晰明了
= 对所有类、函数进行规则命名
= 对重要的过程进行必要的注释
= 对实例化的对象句柄进行统一命名
= 将所有模块的打印调出来了
= 某些简要的Class调用函数，因为只用到一次，所以简化为直接调用，而不再需要单独new这个Class再使用。
= ComLib上进行了验证
以下问题得到解决！
1. 图像识别完成后，无法自动切换CTRL模块中的状态机，导致必须手动点击【图像识别停止】后，才能继续干其它活
   -> 暂时没充分掌握信号槽的逻辑，孙子线程无法成功给子线程发送信号所导致
   -> 不太影响工具的持续使用，只是不方便而已


//=MYC, 2018/8/04, CURRENT_SW_DELIVERY R1.16 =>CEBS
2018/08/04, test with following issues:
1. Dist不好使
2. 图像识别不按停止，校准界面弹不出来（已知）
3. X范围最大要设到12cm，或者最大12.5cm，不然会超限！！！！
4. 强制移动最好有一个确认键，以免超限。绝对避免超限
5. 是不是增加一个急停按钮
6. 摄像头激活不出来的情况（已知）
7. 拍摄过程直接退出，再次启动拍照，要先归零，否则孔位会错乱 (已知）
8. 拍摄过程直接退出，再次启动拍照，Batch号应该递增，否则覆盖上次的图片
9. 反复拍摄，感觉照片不对准：可以观察batch46和47，都是46次之前校准的，47开始拍摄之前是归零的
10. 执行一个操作的时候，不能按的扭可以灰化？
11. 还存在最开始读版本读不到的情况。插拔USB可以恢复。


//=ZJL, 2018/8/15, CURRENT_SW_DELIVERY R1.15 =>CEBS
= 增加白平衡算法
= 将摄像头工作模式设置放在初始化之中，而且明确职能设置2倍精度，不能设置为最高4倍精度

//=ZJL, 2018/8/11, CURRENT_SW_DELIVERY R1.14 =>CEBS
= 统一批次识别数据，不断加总，改正

//=ZJL, 2018/8/8, CURRENT_SW_DELIVERY R1.13 =>CEBS
= 启动时马达自动归零； 2) 校准完成时出现奔溃，Exception被截获。
= 影响就是启动会比较慢。当串口没连上时需要等待90秒超时，会更慢。以后界面可以改进为：提示系统在初始化过程中。。。
= 将96-6孔板子的功能均加入进来
= 将96-6孔板的尺寸，增加到系统中来
= 摄像头的分辨率调整

//=ZJL, 2018/8/7, CURRENT_SW_DELIVERY R1.12 =>CEBS
= 修复计算剩余图像未识别的错误

//=ZJL, 2018/7/31, CURRENT_SW_DELIVERY R1.10 =>CEBS
= 加强MOTOAPI的可靠性
	5. 长时间运行后，由于各种奔溃事件，可能导致ini配置文件中，图像未识别的总数不是真实图像未识别的数字
	   -> 因为各种测试条件下奔溃事件，导致文件ini存储不正确
	   -> 可以手工修改ini文件中的RemainingCnt数字，从而强制再次识别
	   -> 每次启动之后，将ini中所有的清单拉一边，这个过程会比较长，影响工具的启动。正式运行时，这个问题会比较小。具体应该如何优化，未来可以再看需求。
	   -> 通过初始化中的re-check过程，解决了该问题


//=ZJL, 2018/7/30, CURRENT_SW_DELIVERY R1.09 =>CEBS
= 更新的功能： 1）增加强制移动，非常好使，正常移动功能恢复了正常区间检查 2）为了方便定点拍照，增加移动到某个孔位的指令 3）准备搞实时摄像头的方案
= 摄像头更新，0.5s更新一次。还有潜在的风险，需要明确问题出现的地方
= 将摄像头图像展示的位置，可能呈现在界面上的某个地方=》简化方式
= 将图像加载到QLable或者GraphicsView中，目前还未找到合适的方法
= waitKey(ms)的高级技巧，非常不错！

//=ZJL, 2018/7/28, CURRENT_SW_DELIVERY R1.08 =>CEBS
= 增加强制移动功能
= 准备增加
	- 视频图像展示功能
	- 定点拍照
	- 移动到第一个孔位
	- 移动到某个孔位

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

