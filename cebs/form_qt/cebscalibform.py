# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cebscalibform.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_cebsCalibForm(object):
    def setupUi(self, cebsCalibForm):
        cebsCalibForm.setObjectName("cebsCalibForm")
        cebsCalibForm.resize(1322, 927)
        self.groupBox_calib_set = QtWidgets.QGroupBox(cebsCalibForm)
        self.groupBox_calib_set.setGeometry(QtCore.QRect(30, 10, 421, 381))
        self.groupBox_calib_set.setObjectName("groupBox_calib_set")
        self.groupBox_calib_move_scale = QtWidgets.QGroupBox(self.groupBox_calib_set)
        self.groupBox_calib_move_scale.setGeometry(QtCore.QRect(20, 30, 381, 141))
        self.groupBox_calib_move_scale.setObjectName("groupBox_calib_move_scale")
        self.radioButton_calib_5cm = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_5cm.setGeometry(QtCore.QRect(300, 50, 51, 21))
        self.radioButton_calib_5cm.setObjectName("radioButton_calib_5cm")
        self.radioButton_calib_2mm = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_2mm.setGeometry(QtCore.QRect(10, 50, 61, 21))
        self.radioButton_calib_2mm.setChecked(False)
        self.radioButton_calib_2mm.setObjectName("radioButton_calib_2mm")
        self.radioButton_calib_2cm = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_2cm.setGeometry(QtCore.QRect(230, 50, 51, 21))
        self.radioButton_calib_2cm.setObjectName("radioButton_calib_2cm")
        self.radioButton_calib_5mm = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_5mm.setGeometry(QtCore.QRect(90, 50, 51, 21))
        self.radioButton_calib_5mm.setChecked(False)
        self.radioButton_calib_5mm.setObjectName("radioButton_calib_5mm")
        self.radioButton_calib_1cm = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_1cm.setGeometry(QtCore.QRect(160, 50, 51, 21))
        self.radioButton_calib_1cm.setObjectName("radioButton_calib_1cm")
        self.radioButton_calib_10um = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_10um.setGeometry(QtCore.QRect(10, 20, 61, 21))
        self.radioButton_calib_10um.setChecked(False)
        self.radioButton_calib_10um.setObjectName("radioButton_calib_10um")
        self.radioButton_calib_100um = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_100um.setGeometry(QtCore.QRect(90, 20, 61, 21))
        self.radioButton_calib_100um.setChecked(False)
        self.radioButton_calib_100um.setObjectName("radioButton_calib_100um")
        self.radioButton_calib_200um = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_200um.setGeometry(QtCore.QRect(160, 20, 61, 21))
        self.radioButton_calib_200um.setChecked(False)
        self.radioButton_calib_200um.setObjectName("radioButton_calib_200um")
        self.radioButton_calib_500um = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_500um.setGeometry(QtCore.QRect(230, 20, 61, 21))
        self.radioButton_calib_500um.setChecked(False)
        self.radioButton_calib_500um.setObjectName("radioButton_calib_500um")
        self.radioButton_calib_1mm = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_1mm.setGeometry(QtCore.QRect(300, 20, 61, 21))
        self.radioButton_calib_1mm.setChecked(True)
        self.radioButton_calib_1mm.setObjectName("radioButton_calib_1mm")
        self.radioButton_calib_hole96_l = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_hole96_l.setGeometry(QtCore.QRect(10, 80, 71, 21))
        self.radioButton_calib_hole96_l.setObjectName("radioButton_calib_hole96_l")
        self.radioButton_calib_hole96_s = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_hole96_s.setGeometry(QtCore.QRect(90, 80, 71, 21))
        self.radioButton_calib_hole96_s.setObjectName("radioButton_calib_hole96_s")
        self.radioButton_calib_hole48_l = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_hole48_l.setGeometry(QtCore.QRect(160, 80, 71, 21))
        self.radioButton_calib_hole48_l.setObjectName("radioButton_calib_hole48_l")
        self.radioButton_calib_hole48_s = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_hole48_s.setGeometry(QtCore.QRect(230, 80, 71, 21))
        self.radioButton_calib_hole48_s.setObjectName("radioButton_calib_hole48_s")
        self.radioButton_calib_hole24_s = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_hole24_s.setGeometry(QtCore.QRect(10, 110, 71, 21))
        self.radioButton_calib_hole24_s.setObjectName("radioButton_calib_hole24_s")
        self.radioButton_calib_hole24_l = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_hole24_l.setGeometry(QtCore.QRect(300, 80, 71, 21))
        self.radioButton_calib_hole24_l.setObjectName("radioButton_calib_hole24_l")
        self.radioButton_calib_hole12_s = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_hole12_s.setGeometry(QtCore.QRect(160, 110, 71, 21))
        self.radioButton_calib_hole12_s.setObjectName("radioButton_calib_hole12_s")
        self.radioButton_calib_hole12_l = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_hole12_l.setGeometry(QtCore.QRect(80, 110, 71, 21))
        self.radioButton_calib_hole12_l.setObjectName("radioButton_calib_hole12_l")
        self.radioButton_calib_hole6_s = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_hole6_s.setGeometry(QtCore.QRect(300, 110, 71, 21))
        self.radioButton_calib_hole6_s.setObjectName("radioButton_calib_hole6_s")
        self.radioButton_calib_hole6_l = QtWidgets.QRadioButton(self.groupBox_calib_move_scale)
        self.radioButton_calib_hole6_l.setGeometry(QtCore.QRect(230, 110, 71, 21))
        self.radioButton_calib_hole6_l.setObjectName("radioButton_calib_hole6_l")
        self.groupBox_calib_move_dir = QtWidgets.QGroupBox(self.groupBox_calib_set)
        self.groupBox_calib_move_dir.setGeometry(QtCore.QRect(20, 180, 381, 131))
        self.groupBox_calib_move_dir.setObjectName("groupBox_calib_move_dir")
        self.pushButton_calib_pilot_move_up = QtWidgets.QPushButton(self.groupBox_calib_move_dir)
        self.pushButton_calib_pilot_move_up.setGeometry(QtCore.QRect(150, 20, 75, 23))
        self.pushButton_calib_pilot_move_up.setObjectName("pushButton_calib_pilot_move_up")
        self.pushButton_calib_pilot_move_left = QtWidgets.QPushButton(self.groupBox_calib_move_dir)
        self.pushButton_calib_pilot_move_left.setGeometry(QtCore.QRect(50, 60, 75, 23))
        self.pushButton_calib_pilot_move_left.setObjectName("pushButton_calib_pilot_move_left")
        self.pushButton_calib_pilot_move_right = QtWidgets.QPushButton(self.groupBox_calib_move_dir)
        self.pushButton_calib_pilot_move_right.setGeometry(QtCore.QRect(250, 60, 75, 23))
        self.pushButton_calib_pilot_move_right.setAutoDefault(False)
        self.pushButton_calib_pilot_move_right.setDefault(False)
        self.pushButton_calib_pilot_move_right.setFlat(False)
        self.pushButton_calib_pilot_move_right.setObjectName("pushButton_calib_pilot_move_right")
        self.pushButton_calib_pilot_move_down = QtWidgets.QPushButton(self.groupBox_calib_move_dir)
        self.pushButton_calib_pilot_move_down.setGeometry(QtCore.QRect(150, 90, 75, 23))
        self.pushButton_calib_pilot_move_down.setObjectName("pushButton_calib_pilot_move_down")
        self.pushButton_calib_left_down = QtWidgets.QPushButton(self.groupBox_calib_set)
        self.pushButton_calib_left_down.setGeometry(QtCore.QRect(40, 320, 151, 41))
        self.pushButton_calib_left_down.setObjectName("pushButton_calib_left_down")
        self.pushButton_calib_right_up = QtWidgets.QPushButton(self.groupBox_calib_set)
        self.pushButton_calib_right_up.setGeometry(QtCore.QRect(230, 320, 151, 41))
        self.pushButton_calib_right_up.setObjectName("pushButton_calib_right_up")
        self.textEdit_calib_runProgress = QtWidgets.QTextEdit(cebsCalibForm)
        self.textEdit_calib_runProgress.setGeometry(QtCore.QRect(470, 710, 841, 151))
        self.textEdit_calib_runProgress.setMouseTracking(True)
        self.textEdit_calib_runProgress.setTabletTracking(True)
        self.textEdit_calib_runProgress.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textEdit_calib_runProgress.setAutoFillBackground(True)
        self.textEdit_calib_runProgress.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit_calib_runProgress.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_calib_runProgress.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textEdit_calib_runProgress.setAutoFormatting(QtWidgets.QTextEdit.AutoAll)
        self.textEdit_calib_runProgress.setTabChangesFocus(True)
        self.textEdit_calib_runProgress.setObjectName("textEdit_calib_runProgress")
        self.label_calib_runProgress = QtWidgets.QLabel(cebsCalibForm)
        self.label_calib_runProgress.setGeometry(QtCore.QRect(470, 690, 81, 16))
        self.label_calib_runProgress.setObjectName("label_calib_runProgress")
        self.pushButton_calib_comp = QtWidgets.QPushButton(cebsCalibForm)
        self.pushButton_calib_comp.setGeometry(QtCore.QRect(30, 560, 421, 51))
        self.pushButton_calib_comp.setObjectName("pushButton_calib_comp")
        self.groupBox_calib_pilot = QtWidgets.QGroupBox(cebsCalibForm)
        self.groupBox_calib_pilot.setGeometry(QtCore.QRect(30, 410, 421, 131))
        self.groupBox_calib_pilot.setObjectName("groupBox_calib_pilot")
        self.pushButton_calib_pilot_start = QtWidgets.QPushButton(self.groupBox_calib_pilot)
        self.pushButton_calib_pilot_start.setGeometry(QtCore.QRect(10, 80, 81, 41))
        self.pushButton_calib_pilot_start.setObjectName("pushButton_calib_pilot_start")
        self.pushButton_calib_pilot_stop = QtWidgets.QPushButton(self.groupBox_calib_pilot)
        self.pushButton_calib_pilot_stop.setGeometry(QtCore.QRect(100, 80, 81, 41))
        self.pushButton_calib_pilot_stop.setObjectName("pushButton_calib_pilot_stop")
        self.pushButton_calib_pilot_move_0 = QtWidgets.QPushButton(self.groupBox_calib_pilot)
        self.pushButton_calib_pilot_move_0.setGeometry(QtCore.QRect(10, 30, 81, 41))
        self.pushButton_calib_pilot_move_0.setObjectName("pushButton_calib_pilot_move_0")
        self.pushButton_calib_pilot_move_n = QtWidgets.QPushButton(self.groupBox_calib_pilot)
        self.pushButton_calib_pilot_move_n.setGeometry(QtCore.QRect(100, 30, 81, 41))
        self.pushButton_calib_pilot_move_n.setObjectName("pushButton_calib_pilot_move_n")
        self.lineEdit_pilot_move_n = QtWidgets.QLineEdit(self.groupBox_calib_pilot)
        self.lineEdit_pilot_move_n.setGeometry(QtCore.QRect(190, 40, 51, 20))
        self.lineEdit_pilot_move_n.setObjectName("lineEdit_pilot_move_n")
        self.pushButton_calib_pilot_camera_cap = QtWidgets.QPushButton(self.groupBox_calib_pilot)
        self.pushButton_calib_pilot_camera_cap.setEnabled(True)
        self.pushButton_calib_pilot_camera_cap.setGeometry(QtCore.QRect(280, 30, 81, 41))
        self.pushButton_calib_pilot_camera_cap.setCheckable(False)
        self.pushButton_calib_pilot_camera_cap.setObjectName("pushButton_calib_pilot_camera_cap")
        self.label_calib_RtCam_Fill = QtWidgets.QLabel(cebsCalibForm)
        self.label_calib_RtCam_Fill.setGeometry(QtCore.QRect(470, 50, 841, 631))
        self.label_calib_RtCam_Fill.setObjectName("label_calib_RtCam_Fill")
        self.label_calib_RtCam_title = QtWidgets.QLabel(cebsCalibForm)
        self.label_calib_RtCam_title.setGeometry(QtCore.QRect(470, 20, 81, 16))
        self.label_calib_RtCam_title.setObjectName("label_calib_RtCam_title")
        self.groupBox_calib_force_move = QtWidgets.QGroupBox(cebsCalibForm)
        self.groupBox_calib_force_move.setGeometry(QtCore.QRect(120, 630, 251, 231))
        self.groupBox_calib_force_move.setObjectName("groupBox_calib_force_move")
        self.pushButton_calib_fm_left = QtWidgets.QPushButton(self.groupBox_calib_force_move)
        self.pushButton_calib_fm_left.setEnabled(False)
        self.pushButton_calib_fm_left.setGeometry(QtCore.QRect(20, 70, 31, 111))
        self.pushButton_calib_fm_left.setObjectName("pushButton_calib_fm_left")
        self.pushButton_calib_fm_right = QtWidgets.QPushButton(self.groupBox_calib_force_move)
        self.pushButton_calib_fm_right.setEnabled(False)
        self.pushButton_calib_fm_right.setGeometry(QtCore.QRect(200, 70, 31, 111))
        self.pushButton_calib_fm_right.setObjectName("pushButton_calib_fm_right")
        self.pushButton_calib_fm_down = QtWidgets.QPushButton(self.groupBox_calib_force_move)
        self.pushButton_calib_fm_down.setEnabled(False)
        self.pushButton_calib_fm_down.setGeometry(QtCore.QRect(60, 190, 131, 31))
        self.pushButton_calib_fm_down.setObjectName("pushButton_calib_fm_down")
        self.pushButton_calib_fm_1cm = QtWidgets.QPushButton(self.groupBox_calib_force_move)
        self.pushButton_calib_fm_1cm.setEnabled(False)
        self.pushButton_calib_fm_1cm.setGeometry(QtCore.QRect(60, 70, 131, 111))
        self.pushButton_calib_fm_1cm.setObjectName("pushButton_calib_fm_1cm")
        self.pushButton_calib_fm_up = QtWidgets.QPushButton(self.groupBox_calib_force_move)
        self.pushButton_calib_fm_up.setEnabled(False)
        self.pushButton_calib_fm_up.setGeometry(QtCore.QRect(60, 30, 131, 31))
        self.pushButton_calib_fm_up.setObjectName("pushButton_calib_fm_up")

        self.retranslateUi(cebsCalibForm)
        self.pushButton_calib_comp.clicked.connect(cebsCalibForm.slot_calib_close)
        self.pushButton_calib_left_down.clicked.connect(cebsCalibForm.slot_calib_left_down)
        self.pushButton_calib_right_up.clicked.connect(cebsCalibForm.slot_calib_right_up)
        self.pushButton_calib_pilot_start.clicked.connect(cebsCalibForm.slot_calib_pilot_start)
        self.pushButton_calib_pilot_stop.clicked.connect(cebsCalibForm.slot_calib_pilot_stop)
        self.pushButton_calib_fm_left.clicked.connect(cebsCalibForm.slot_calib_fm_left)
        self.pushButton_calib_fm_down.clicked.connect(cebsCalibForm.slot_calib_fm_down)
        self.pushButton_calib_fm_right.clicked.connect(cebsCalibForm.slot_calib_fm_right)
        self.pushButton_calib_fm_up.clicked.connect(cebsCalibForm.slot_calib_fm_up)
        self.pushButton_calib_pilot_move_0.clicked.connect(cebsCalibForm.slot_calib_pilot_move_0)
        self.pushButton_calib_pilot_move_n.clicked.connect(cebsCalibForm.slot_calib_pilot_move_n)
        self.pushButton_calib_pilot_camera_cap.clicked.connect(cebsCalibForm.slot_calib_pilot_camera_cap)
        self.pushButton_calib_pilot_move_right.clicked.connect(cebsCalibForm.slot_calib_pilot_move_right)
        self.pushButton_calib_pilot_move_down.clicked.connect(cebsCalibForm.slot_calib_pilot_move_down)
        self.pushButton_calib_pilot_move_up.clicked.connect(cebsCalibForm.slot_calib_pilot_move_up)
        self.pushButton_calib_pilot_move_left.clicked.connect(cebsCalibForm.slot_calib_pilot_move_left)
        QtCore.QMetaObject.connectSlotsByName(cebsCalibForm)

    def retranslateUi(self, cebsCalibForm):
        _translate = QtCore.QCoreApplication.translate
        cebsCalibForm.setWindowTitle(_translate("cebsCalibForm", "CALIBRATION"))
        self.groupBox_calib_set.setTitle(_translate("cebsCalibForm", "校准设定"))
        self.groupBox_calib_move_scale.setTitle(_translate("cebsCalibForm", "运动刻度"))
        self.radioButton_calib_5cm.setText(_translate("cebsCalibForm", "5cm"))
        self.radioButton_calib_2mm.setText(_translate("cebsCalibForm", "2mm"))
        self.radioButton_calib_2cm.setText(_translate("cebsCalibForm", "2cm"))
        self.radioButton_calib_5mm.setText(_translate("cebsCalibForm", "5mm"))
        self.radioButton_calib_1cm.setText(_translate("cebsCalibForm", "1cm"))
        self.radioButton_calib_10um.setText(_translate("cebsCalibForm", "10um"))
        self.radioButton_calib_100um.setText(_translate("cebsCalibForm", "100um"))
        self.radioButton_calib_200um.setText(_translate("cebsCalibForm", "200um"))
        self.radioButton_calib_500um.setText(_translate("cebsCalibForm", "500um"))
        self.radioButton_calib_1mm.setText(_translate("cebsCalibForm", "1mm"))
        self.radioButton_calib_hole96_l.setText(_translate("cebsCalibForm", "96孔长边"))
        self.radioButton_calib_hole96_s.setText(_translate("cebsCalibForm", "96孔短边"))
        self.radioButton_calib_hole48_l.setText(_translate("cebsCalibForm", "48孔长边"))
        self.radioButton_calib_hole48_s.setText(_translate("cebsCalibForm", "48孔短边"))
        self.radioButton_calib_hole24_s.setText(_translate("cebsCalibForm", "24孔短边"))
        self.radioButton_calib_hole24_l.setText(_translate("cebsCalibForm", "24孔长边"))
        self.radioButton_calib_hole12_s.setText(_translate("cebsCalibForm", "12孔短边"))
        self.radioButton_calib_hole12_l.setText(_translate("cebsCalibForm", "12孔长边"))
        self.radioButton_calib_hole6_s.setText(_translate("cebsCalibForm", "6孔短边"))
        self.radioButton_calib_hole6_l.setText(_translate("cebsCalibForm", "6孔长边"))
        self.groupBox_calib_move_dir.setTitle(_translate("cebsCalibForm", "运动方向"))
        self.pushButton_calib_pilot_move_up.setText(_translate("cebsCalibForm", "Up"))
        self.pushButton_calib_pilot_move_left.setText(_translate("cebsCalibForm", "Left"))
        self.pushButton_calib_pilot_move_right.setText(_translate("cebsCalibForm", "Right"))
        self.pushButton_calib_pilot_move_down.setText(_translate("cebsCalibForm", "Down"))
        self.pushButton_calib_left_down.setText(_translate("cebsCalibForm", "设定左下"))
        self.pushButton_calib_right_up.setText(_translate("cebsCalibForm", "设定右上"))
        self.textEdit_calib_runProgress.setHtml(_translate("cebsCalibForm", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&gt;&gt; 2018/5/2 15:30:99 校准开始</p></body></html>"))
        self.label_calib_runProgress.setText(_translate("cebsCalibForm", "校准进展"))
        self.pushButton_calib_comp.setText(_translate("cebsCalibForm", "校准完成"))
        self.groupBox_calib_pilot.setTitle(_translate("cebsCalibForm", "运动设置"))
        self.pushButton_calib_pilot_start.setText(_translate("cebsCalibForm", "校准巡游"))
        self.pushButton_calib_pilot_stop.setText(_translate("cebsCalibForm", "巡游停止"))
        self.pushButton_calib_pilot_move_0.setText(_translate("cebsCalibForm", "移动到起点"))
        self.pushButton_calib_pilot_move_n.setText(_translate("cebsCalibForm", "移动到#号孔"))
        self.lineEdit_pilot_move_n.setText(_translate("cebsCalibForm", "1"))
        self.pushButton_calib_pilot_camera_cap.setText(_translate("cebsCalibForm", "立即拍照"))
        self.label_calib_RtCam_Fill.setText(_translate("cebsCalibForm", "TextLabel"))
        self.label_calib_RtCam_title.setText(_translate("cebsCalibForm", "实时摄像头"))
        self.groupBox_calib_force_move.setTitle(_translate("cebsCalibForm", "强制移动"))
        self.pushButton_calib_fm_left.setText(_translate("cebsCalibForm", "左"))
        self.pushButton_calib_fm_right.setText(_translate("cebsCalibForm", "右"))
        self.pushButton_calib_fm_down.setText(_translate("cebsCalibForm", "下"))
        self.pushButton_calib_fm_1cm.setText(_translate("cebsCalibForm", "强制移动（1cm)"))
        self.pushButton_calib_fm_up.setText(_translate("cebsCalibForm", "上"))

