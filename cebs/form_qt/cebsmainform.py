# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cebsMainform.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_cebsMainWindow(object):
    def setupUi(self, cebsMainWindow):
        cebsMainWindow.setObjectName("cebsMainWindow")
        cebsMainWindow.resize(1202, 683)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(cebsMainWindow.sizePolicy().hasHeightForWidth())
        cebsMainWindow.setSizePolicy(sizePolicy)
        cebsMainWindow.setMinimumSize(QtCore.QSize(1202, 546))
        self.centralwidget = QtWidgets.QWidget(cebsMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit_runProgress = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_runProgress.setGeometry(QtCore.QRect(380, 40, 761, 401))
        self.textEdit_runProgress.setMouseTracking(True)
        self.textEdit_runProgress.setTabletTracking(True)
        self.textEdit_runProgress.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textEdit_runProgress.setAutoFillBackground(True)
        self.textEdit_runProgress.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit_runProgress.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_runProgress.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textEdit_runProgress.setAutoFormatting(QtWidgets.QTextEdit.AutoAll)
        self.textEdit_runProgress.setTabChangesFocus(True)
        self.textEdit_runProgress.setObjectName("textEdit_runProgress")
        self.pushButton_ctrl_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ctrl_start.setGeometry(QtCore.QRect(20, 20, 161, 71))
        self.pushButton_ctrl_start.setObjectName("pushButton_ctrl_start")
        self.label_runProgress = QtWidgets.QLabel(self.centralwidget)
        self.label_runProgress.setGeometry(QtCore.QRect(380, 20, 261, 16))
        self.label_runProgress.setObjectName("label_runProgress")
        self.pushButton_ctrl_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ctrl_stop.setGeometry(QtCore.QRect(200, 20, 161, 71))
        self.pushButton_ctrl_stop.setObjectName("pushButton_ctrl_stop")
        self.pushButton_runpg_clear = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_runpg_clear.setGeometry(QtCore.QRect(1060, 450, 71, 41))
        self.pushButton_runpg_clear.setObjectName("pushButton_runpg_clear")
        self.pushButton_ctrl_zero = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ctrl_zero.setGeometry(QtCore.QRect(20, 110, 341, 71))
        self.pushButton_ctrl_zero.setObjectName("pushButton_ctrl_zero")
        self.pushButton_ctrl_calib = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ctrl_calib.setGeometry(QtCore.QRect(20, 290, 161, 71))
        self.pushButton_ctrl_calib.setObjectName("pushButton_ctrl_calib")
        self.pushButton_ctrl_vclas_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ctrl_vclas_start.setGeometry(QtCore.QRect(20, 200, 161, 71))
        self.pushButton_ctrl_vclas_start.setObjectName("pushButton_ctrl_vclas_start")
        self.pushButton_ctrl_vclas_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ctrl_vclas_stop.setGeometry(QtCore.QRect(200, 200, 161, 71))
        self.pushButton_ctrl_vclas_stop.setObjectName("pushButton_ctrl_vclas_stop")
        self.pushButton_gpar_set = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_gpar_set.setGeometry(QtCore.QRect(200, 290, 161, 71))
        self.pushButton_gpar_set.setObjectName("pushButton_gpar_set")
        self.pushButton_meng_sel = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_meng_sel.setGeometry(QtCore.QRect(20, 380, 161, 71))
        self.pushButton_meng_sel.setObjectName("pushButton_meng_sel")
        self.pushButton_saht_sel = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_saht_sel.setGeometry(QtCore.QRect(200, 380, 161, 71))
        self.pushButton_saht_sel.setObjectName("pushButton_saht_sel")
        cebsMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(cebsMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1202, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(self.menubar)
        self.menu_5.setObjectName("menu_5")
        self.menu_6 = QtWidgets.QMenu(self.menubar)
        self.menu_6.setObjectName("menu_6")
        self.menu_7 = QtWidgets.QMenu(self.menubar)
        self.menu_7.setObjectName("menu_7")
        self.menu_8 = QtWidgets.QMenu(self.menubar)
        self.menu_8.setObjectName("menu_8")
        cebsMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(cebsMainWindow)
        self.statusbar.setObjectName("statusbar")
        cebsMainWindow.setStatusBar(self.statusbar)
        self.actionMenuStestProc = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuStestProc.setObjectName("actionMenuStestProc")
        self.actionSTOP = QtWidgets.QAction(cebsMainWindow)
        self.actionSTOP.setObjectName("actionSTOP")
        self.actionMenuGparSet = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuGparSet.setObjectName("actionMenuGparSet")
        self.actionABOUT = QtWidgets.QAction(cebsMainWindow)
        self.actionABOUT.setObjectName("actionABOUT")
        self.actionMenuSsetAbout = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuSsetAbout.setObjectName("actionMenuSsetAbout")
        self.actionMenuSsetExit = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuSsetExit.setObjectName("actionMenuSsetExit")
        self.actionMenuMengMode = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuMengMode.setObjectName("actionMenuMengMode")
        self.actionMenuCalibMode = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuCalibMode.setObjectName("actionMenuCalibMode")
        self.actionMenuPicNorStart = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuPicNorStart.setObjectName("actionMenuPicNorStart")
        self.actionMenuPicFluStart = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuPicFluStart.setObjectName("actionMenuPicFluStart")
        self.actionMenuPicStop = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuPicStop.setObjectName("actionMenuPicStop")
        self.actionMenuMengZero = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuMengZero.setObjectName("actionMenuMengZero")
        self.actionMenuCfyNorStart = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuCfyNorStart.setObjectName("actionMenuCfyNorStart")
        self.actionMenuCfyFluStart = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuCfyFluStart.setObjectName("actionMenuCfyFluStart")
        self.actionMenuCfyStop = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuCfyStop.setObjectName("actionMenuCfyStop")
        self.actionMenuSahtSelect = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuSahtSelect.setObjectName("actionMenuSahtSelect")
        self.actionMenuStestRndCmd = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuStestRndCmd.setObjectName("actionMenuStestRndCmd")
        self.action = QtWidgets.QAction(cebsMainWindow)
        self.action.setObjectName("action")
        self.actionMenuFccnt = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuFccnt.setObjectName("actionMenuFccnt")
        self.actionMenuGparFcc = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuGparFcc.setObjectName("actionMenuGparFcc")
        self.actionMenuFspc = QtWidgets.QAction(cebsMainWindow)
        self.actionMenuFspc.setObjectName("actionMenuFspc")
        self.menu.addAction(self.actionMenuStestProc)
        self.menu.addAction(self.actionMenuStestRndCmd)
        self.menu_2.addAction(self.actionMenuGparSet)
        self.menu_2.addAction(self.actionMenuGparFcc)
        self.menu_3.addAction(self.actionMenuMengMode)
        self.menu_3.addAction(self.actionMenuMengZero)
        self.menu_4.addAction(self.actionMenuCalibMode)
        self.menu_5.addAction(self.actionMenuPicNorStart)
        self.menu_5.addAction(self.actionMenuPicFluStart)
        self.menu_5.addAction(self.actionMenuPicStop)
        self.menu_6.addAction(self.actionMenuCfyNorStart)
        self.menu_6.addAction(self.actionMenuCfyFluStart)
        self.menu_6.addAction(self.actionMenuCfyStop)
        self.menu_6.addAction(self.actionMenuFspc)
        self.menu_7.addAction(self.actionMenuSsetAbout)
        self.menu_7.addSeparator()
        self.menu_7.addAction(self.actionMenuSsetExit)
        self.menu_8.addAction(self.actionMenuSahtSelect)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_8.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_5.menuAction())
        self.menubar.addAction(self.menu_6.menuAction())
        self.menubar.addAction(self.menu_7.menuAction())

        self.retranslateUi(cebsMainWindow)
        self.pushButton_runpg_clear.clicked.connect(cebsMainWindow.slot_runpg_clear)
        self.pushButton_ctrl_stop.clicked.connect(cebsMainWindow.slot_ctrl_stop)
        self.pushButton_ctrl_start.clicked.connect(cebsMainWindow.slot_ctrl_start_normal)
        self.pushButton_ctrl_zero.clicked.connect(cebsMainWindow.slot_ctrl_zero)
        self.pushButton_ctrl_calib.clicked.connect(cebsMainWindow.slot_ctrl_calib)
        self.pushButton_ctrl_vclas_start.clicked.connect(cebsMainWindow.slot_ctrl_vclas_start_normal)
        self.pushButton_ctrl_vclas_stop.clicked.connect(cebsMainWindow.slot_ctrl_vclas_stop)
        self.pushButton_gpar_set.clicked.connect(cebsMainWindow.slot_gpar_start)
        self.pushButton_meng_sel.clicked.connect(cebsMainWindow.slot_meng_sel)
        self.pushButton_saht_sel.clicked.connect(cebsMainWindow.slot_saht_sel)
        QtCore.QMetaObject.connectSlotsByName(cebsMainWindow)

    def retranslateUi(self, cebsMainWindow):
        _translate = QtCore.QCoreApplication.translate
        cebsMainWindow.setWindowTitle(_translate("cebsMainWindow", "小慧-CEBS-生物识别系统"))
        self.textEdit_runProgress.setHtml(_translate("cebsMainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&gt;&gt; 2018/5/2 15:30:99 系统启动</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&gt;&gt; 2018/5/2 15:40:55 启动执行命令 </p></body></html>"))
        self.pushButton_ctrl_start.setText(_translate("cebsMainWindow", "启动白光拍摄"))
        self.label_runProgress.setText(_translate("cebsMainWindow", "运行进展"))
        self.pushButton_ctrl_stop.setText(_translate("cebsMainWindow", "停止拍摄"))
        self.pushButton_runpg_clear.setText(_translate("cebsMainWindow", "清除"))
        self.pushButton_ctrl_zero.setText(_translate("cebsMainWindow", "位置归零"))
        self.pushButton_ctrl_calib.setText(_translate("cebsMainWindow", "校准功能"))
        self.pushButton_ctrl_vclas_start.setText(_translate("cebsMainWindow", "白光图像识别"))
        self.pushButton_ctrl_vclas_stop.setText(_translate("cebsMainWindow", "停止图像识别"))
        self.pushButton_gpar_set.setText(_translate("cebsMainWindow", "参数设定"))
        self.pushButton_meng_sel.setText(_translate("cebsMainWindow", "工程模式"))
        self.pushButton_saht_sel.setText(_translate("cebsMainWindow", "激活板孔选择"))
        self.menu.setTitle(_translate("cebsMainWindow", "自测"))
        self.menu_2.setTitle(_translate("cebsMainWindow", "工参"))
        self.menu_3.setTitle(_translate("cebsMainWindow", "马达"))
        self.menu_4.setTitle(_translate("cebsMainWindow", "校准"))
        self.menu_5.setTitle(_translate("cebsMainWindow", "拍照"))
        self.menu_6.setTitle(_translate("cebsMainWindow", "识别"))
        self.menu_7.setTitle(_translate("cebsMainWindow", "设置"))
        self.menu_8.setTitle(_translate("cebsMainWindow", "板孔"))
        self.actionMenuStestProc.setText(_translate("cebsMainWindow", "自测过程"))
        self.actionSTOP.setText(_translate("cebsMainWindow", "STOP"))
        self.actionMenuGparSet.setText(_translate("cebsMainWindow", "参数设定"))
        self.actionABOUT.setText(_translate("cebsMainWindow", "ABOUT"))
        self.actionMenuSsetAbout.setText(_translate("cebsMainWindow", "关于"))
        self.actionMenuSsetExit.setText(_translate("cebsMainWindow", "退出"))
        self.actionMenuMengMode.setText(_translate("cebsMainWindow", "工程模式"))
        self.actionMenuCalibMode.setText(_translate("cebsMainWindow", "校准模式"))
        self.actionMenuPicNorStart.setText(_translate("cebsMainWindow", "白光拍摄"))
        self.actionMenuPicFluStart.setText(_translate("cebsMainWindow", "荧光拍摄"))
        self.actionMenuPicStop.setText(_translate("cebsMainWindow", "停止拍照"))
        self.actionMenuMengZero.setText(_translate("cebsMainWindow", "位置归零"))
        self.actionMenuCfyNorStart.setText(_translate("cebsMainWindow", "白光识别"))
        self.actionMenuCfyFluStart.setText(_translate("cebsMainWindow", "荧光识别"))
        self.actionMenuCfyStop.setText(_translate("cebsMainWindow", "停止识别"))
        self.actionMenuSahtSelect.setText(_translate("cebsMainWindow", "活孔选择"))
        self.actionMenuStestRndCmd.setText(_translate("cebsMainWindow", "研发测试"))
        self.action.setText(_translate("cebsMainWindow", "分层荧光"))
        self.actionMenuFccnt.setText(_translate("cebsMainWindow", "细胞计数"))
        self.actionMenuGparFcc.setText(_translate("cebsMainWindow", "细胞计数"))
        self.actionMenuFspc.setText(_translate("cebsMainWindow", "荧光堆叠"))

