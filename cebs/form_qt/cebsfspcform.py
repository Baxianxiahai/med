# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cebsFspcform.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_cebsFspcForm(object):
    def setupUi(self, cebsFspcForm):
        cebsFspcForm.setObjectName("cebsFspcForm")
        cebsFspcForm.resize(1256, 802)
        self.label_fspc_pic_file_load = QtWidgets.QLabel(cebsFspcForm)
        self.label_fspc_pic_file_load.setGeometry(QtCore.QRect(520, 30, 51, 16))
        self.label_fspc_pic_file_load.setObjectName("label_fspc_pic_file_load")
        self.pushButton_fspc_pic_file_load = QtWidgets.QPushButton(cebsFspcForm)
        self.pushButton_fspc_pic_file_load.setGeometry(QtCore.QRect(1160, 30, 91, 21))
        self.pushButton_fspc_pic_file_load.setObjectName("pushButton_fspc_pic_file_load")
        self.groupBox_fpsc_pic_show = QtWidgets.QGroupBox(cebsFspcForm)
        self.groupBox_fpsc_pic_show.setGeometry(QtCore.QRect(520, 60, 731, 721))
        self.groupBox_fpsc_pic_show.setObjectName("groupBox_fpsc_pic_show")
        self.label_pic_fspc_fill = QtWidgets.QLabel(self.groupBox_fpsc_pic_show)
        self.label_pic_fspc_fill.setGeometry(QtCore.QRect(0, 20, 731, 701))
        self.label_pic_fspc_fill.setObjectName("label_pic_fspc_fill")
        self.lineEdit_fspc_pic_file_load = QtWidgets.QLineEdit(cebsFspcForm)
        self.lineEdit_fspc_pic_file_load.setEnabled(True)
        self.lineEdit_fspc_pic_file_load.setGeometry(QtCore.QRect(580, 30, 571, 20))
        self.lineEdit_fspc_pic_file_load.setObjectName("lineEdit_fspc_pic_file_load")
        self.pushButton_fspc_cmd_s1 = QtWidgets.QPushButton(cebsFspcForm)
        self.pushButton_fspc_cmd_s1.setGeometry(QtCore.QRect(20, 620, 111, 41))
        self.pushButton_fspc_cmd_s1.setObjectName("pushButton_fspc_cmd_s1")
        self.groupBox_fspc_set = QtWidgets.QGroupBox(cebsFspcForm)
        self.groupBox_fspc_set.setGeometry(QtCore.QRect(20, 20, 481, 321))
        self.groupBox_fspc_set.setObjectName("groupBox_fspc_set")
        self.lineEdit_fspc_coef_cell_min = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_coef_cell_min.setGeometry(QtCore.QRect(110, 120, 51, 20))
        self.lineEdit_fspc_coef_cell_min.setObjectName("lineEdit_fspc_coef_cell_min")
        self.label_fspc_coef_cell_min = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_cell_min.setGeometry(QtCore.QRect(20, 120, 91, 21))
        self.label_fspc_coef_cell_min.setObjectName("label_fspc_coef_cell_min")
        self.lineEdit_fspc_coef_cell_max = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_coef_cell_max.setGeometry(QtCore.QRect(110, 140, 51, 20))
        self.lineEdit_fspc_coef_cell_max.setObjectName("lineEdit_fspc_coef_cell_max")
        self.label_fspc_coef_cell_max = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_cell_max.setGeometry(QtCore.QRect(20, 140, 91, 21))
        self.label_fspc_coef_cell_max.setObjectName("label_fspc_coef_cell_max")
        self.lineEdit_fspc_coef_raduis_min = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_coef_raduis_min.setGeometry(QtCore.QRect(110, 170, 51, 20))
        self.lineEdit_fspc_coef_raduis_min.setObjectName("lineEdit_fspc_coef_raduis_min")
        self.label_fspc_coef_raduis_min = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_raduis_min.setGeometry(QtCore.QRect(20, 170, 91, 21))
        self.label_fspc_coef_raduis_min.setObjectName("label_fspc_coef_raduis_min")
        self.lineEdit_fspc_coef_raduis_max = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_coef_raduis_max.setGeometry(QtCore.QRect(110, 190, 51, 20))
        self.lineEdit_fspc_coef_raduis_max.setObjectName("lineEdit_fspc_coef_raduis_max")
        self.label_fspc_coef_raduis_max = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_raduis_max.setGeometry(QtCore.QRect(20, 190, 91, 21))
        self.label_fspc_coef_raduis_max.setObjectName("label_fspc_coef_raduis_max")
        self.checkBox_fspc_output_addup = QtWidgets.QCheckBox(self.groupBox_fspc_set)
        self.checkBox_fspc_output_addup.setGeometry(QtCore.QRect(20, 260, 121, 16))
        self.checkBox_fspc_output_addup.setChecked(True)
        self.checkBox_fspc_output_addup.setObjectName("checkBox_fspc_output_addup")
        self.lineEdit_fspc_coef_area_dilate = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_coef_area_dilate.setEnabled(True)
        self.lineEdit_fspc_coef_area_dilate.setGeometry(QtCore.QRect(270, 70, 51, 20))
        self.lineEdit_fspc_coef_area_dilate.setObjectName("lineEdit_fspc_coef_area_dilate")
        self.label_fspc_coef_area_dilate = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_area_dilate.setGeometry(QtCore.QRect(180, 70, 91, 21))
        self.label_fspc_coef_area_dilate.setObjectName("label_fspc_coef_area_dilate")
        self.lineEdit_fspc_coef_area_erode = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_coef_area_erode.setEnabled(True)
        self.lineEdit_fspc_coef_area_erode.setGeometry(QtCore.QRect(270, 90, 51, 20))
        self.lineEdit_fspc_coef_area_erode.setObjectName("lineEdit_fspc_coef_area_erode")
        self.label_fspc_coef_area_erode = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_area_erode.setGeometry(QtCore.QRect(180, 90, 91, 21))
        self.label_fspc_coef_area_erode.setObjectName("label_fspc_coef_area_erode")
        self.label_fspc_coef_cell_ce = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_cell_ce.setGeometry(QtCore.QRect(180, 170, 91, 21))
        self.label_fspc_coef_cell_ce.setObjectName("label_fspc_coef_cell_ce")
        self.lineEdit_fspc_coef_cell_ce = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_coef_cell_ce.setEnabled(True)
        self.lineEdit_fspc_coef_cell_ce.setGeometry(QtCore.QRect(270, 170, 51, 20))
        self.lineEdit_fspc_coef_cell_ce.setObjectName("lineEdit_fspc_coef_cell_ce")
        self.lineEdit_fspc_coef_cell_raduis_dist = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_coef_cell_raduis_dist.setEnabled(True)
        self.lineEdit_fspc_coef_cell_raduis_dist.setGeometry(QtCore.QRect(270, 190, 51, 20))
        self.lineEdit_fspc_coef_cell_raduis_dist.setObjectName("lineEdit_fspc_coef_cell_raduis_dist")
        self.label_fspc_coef_cell_raduis_dist = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_cell_raduis_dist.setGeometry(QtCore.QRect(180, 190, 91, 21))
        self.label_fspc_coef_cell_raduis_dist.setObjectName("label_fspc_coef_cell_raduis_dist")
        self.label_fspc_coef_mark_line = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_mark_line.setGeometry(QtCore.QRect(20, 40, 91, 21))
        self.label_fspc_coef_mark_line.setObjectName("label_fspc_coef_mark_line")
        self.label_fspc_coef_area_max = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_area_max.setGeometry(QtCore.QRect(20, 90, 91, 21))
        self.label_fspc_coef_area_max.setObjectName("label_fspc_coef_area_max")
        self.lineEdit_fspc_coef_area_max = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_coef_area_max.setGeometry(QtCore.QRect(110, 90, 51, 20))
        self.lineEdit_fspc_coef_area_max.setObjectName("lineEdit_fspc_coef_area_max")
        self.lineEdit_fspc_mark_line = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_mark_line.setGeometry(QtCore.QRect(110, 40, 51, 20))
        self.lineEdit_fspc_mark_line.setObjectName("lineEdit_fspc_mark_line")
        self.label_fspc_coef_cell_erode = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_cell_erode.setGeometry(QtCore.QRect(180, 140, 91, 21))
        self.label_fspc_coef_cell_erode.setObjectName("label_fspc_coef_cell_erode")
        self.lineEdit_fspc_coef_cell_erode = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_coef_cell_erode.setEnabled(True)
        self.lineEdit_fspc_coef_cell_erode.setGeometry(QtCore.QRect(270, 140, 51, 20))
        self.lineEdit_fspc_coef_cell_erode.setObjectName("lineEdit_fspc_coef_cell_erode")
        self.lineEdit_fspc_coef_cell_dilate = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_coef_cell_dilate.setEnabled(True)
        self.lineEdit_fspc_coef_cell_dilate.setGeometry(QtCore.QRect(270, 120, 51, 20))
        self.lineEdit_fspc_coef_cell_dilate.setObjectName("lineEdit_fspc_coef_cell_dilate")
        self.label_fspc_coef_cell_dilate = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_cell_dilate.setGeometry(QtCore.QRect(180, 120, 91, 21))
        self.label_fspc_coef_cell_dilate.setObjectName("label_fspc_coef_cell_dilate")
        self.lineEdit_fspc_coef_area_min = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_coef_area_min.setGeometry(QtCore.QRect(110, 70, 51, 20))
        self.lineEdit_fspc_coef_area_min.setObjectName("lineEdit_fspc_coef_area_min")
        self.label_fspc_coef_area_min = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_area_min.setGeometry(QtCore.QRect(20, 70, 91, 21))
        self.label_fspc_coef_area_min.setObjectName("label_fspc_coef_area_min")
        self.lineEdit_fspc_mark_width = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_mark_width.setGeometry(QtCore.QRect(270, 40, 51, 20))
        self.lineEdit_fspc_mark_width.setObjectName("lineEdit_fspc_mark_width")
        self.label_fspc_coef_mark_width = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_mark_width.setGeometry(QtCore.QRect(180, 40, 91, 21))
        self.label_fspc_coef_mark_width.setObjectName("label_fspc_coef_mark_width")
        self.lineEdit_fspc_mark_dilate = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_mark_dilate.setGeometry(QtCore.QRect(270, 20, 51, 20))
        self.lineEdit_fspc_mark_dilate.setObjectName("lineEdit_fspc_mark_dilate")
        self.label_fspc_coef_mark_dilate = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_mark_dilate.setGeometry(QtCore.QRect(180, 20, 91, 21))
        self.label_fspc_coef_mark_dilate.setObjectName("label_fspc_coef_mark_dilate")
        self.label_fspc_coef_mark_area = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_coef_mark_area.setGeometry(QtCore.QRect(20, 20, 91, 21))
        self.label_fspc_coef_mark_area.setObjectName("label_fspc_coef_mark_area")
        self.lineEdit_fspc_mark_area = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_mark_area.setGeometry(QtCore.QRect(110, 20, 51, 20))
        self.lineEdit_fspc_mark_area.setObjectName("lineEdit_fspc_mark_area")
        self.lineEdit_fspc_pic_train_delay = QtWidgets.QLineEdit(self.groupBox_fspc_set)
        self.lineEdit_fspc_pic_train_delay.setGeometry(QtCore.QRect(110, 280, 41, 20))
        self.lineEdit_fspc_pic_train_delay.setObjectName("lineEdit_fspc_pic_train_delay")
        self.label_fspc_pic_train_delay = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_pic_train_delay.setGeometry(QtCore.QRect(20, 280, 91, 21))
        self.label_fspc_pic_train_delay.setObjectName("label_fspc_pic_train_delay")
        self.label_fspc_pic_train_sec = QtWidgets.QLabel(self.groupBox_fspc_set)
        self.label_fspc_pic_train_sec.setGeometry(QtCore.QRect(160, 280, 21, 21))
        self.label_fspc_pic_train_sec.setObjectName("label_fspc_pic_train_sec")
        self.pushButton_fspc_cmd_s2 = QtWidgets.QPushButton(cebsFspcForm)
        self.pushButton_fspc_cmd_s2.setGeometry(QtCore.QRect(140, 620, 111, 41))
        self.pushButton_fspc_cmd_s2.setObjectName("pushButton_fspc_cmd_s2")
        self.pushButton_fspc_cmd_s3 = QtWidgets.QPushButton(cebsFspcForm)
        self.pushButton_fspc_cmd_s3.setGeometry(QtCore.QRect(260, 620, 111, 41))
        self.pushButton_fspc_cmd_s3.setObjectName("pushButton_fspc_cmd_s3")
        self.pushButton_fspc_cmd_s4 = QtWidgets.QPushButton(cebsFspcForm)
        self.pushButton_fspc_cmd_s4.setGeometry(QtCore.QRect(20, 670, 111, 41))
        self.pushButton_fspc_cmd_s4.setObjectName("pushButton_fspc_cmd_s4")
        self.groupBox_cmd_log = QtWidgets.QGroupBox(cebsFspcForm)
        self.groupBox_cmd_log.setGeometry(QtCore.QRect(20, 360, 481, 241))
        self.groupBox_cmd_log.setObjectName("groupBox_cmd_log")
        self.textEdit_fspc_cmd_log = QtWidgets.QTextEdit(self.groupBox_cmd_log)
        self.textEdit_fspc_cmd_log.setGeometry(QtCore.QRect(10, 20, 461, 161))
        self.textEdit_fspc_cmd_log.setMouseTracking(True)
        self.textEdit_fspc_cmd_log.setTabletTracking(True)
        self.textEdit_fspc_cmd_log.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textEdit_fspc_cmd_log.setAutoFillBackground(True)
        self.textEdit_fspc_cmd_log.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit_fspc_cmd_log.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_fspc_cmd_log.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textEdit_fspc_cmd_log.setAutoFormatting(QtWidgets.QTextEdit.AutoAll)
        self.textEdit_fspc_cmd_log.setTabChangesFocus(True)
        self.textEdit_fspc_cmd_log.setObjectName("textEdit_fspc_cmd_log")
        self.pushButton_fspc_clear = QtWidgets.QPushButton(self.groupBox_cmd_log)
        self.pushButton_fspc_clear.setGeometry(QtCore.QRect(180, 190, 81, 41))
        self.pushButton_fspc_clear.setObjectName("pushButton_fspc_clear")
        self.pushButton_fspc_giveup = QtWidgets.QPushButton(self.groupBox_cmd_log)
        self.pushButton_fspc_giveup.setGeometry(QtCore.QRect(280, 190, 81, 41))
        self.pushButton_fspc_giveup.setObjectName("pushButton_fspc_giveup")
        self.pushButton_fspc_compl = QtWidgets.QPushButton(self.groupBox_cmd_log)
        self.pushButton_fspc_compl.setGeometry(QtCore.QRect(380, 190, 81, 41))
        self.pushButton_fspc_compl.setObjectName("pushButton_fspc_compl")
        self.pushButton_fspc_cmd_s5 = QtWidgets.QPushButton(cebsFspcForm)
        self.pushButton_fspc_cmd_s5.setGeometry(QtCore.QRect(140, 670, 111, 41))
        self.pushButton_fspc_cmd_s5.setObjectName("pushButton_fspc_cmd_s5")
        self.pushButton_fspc_cmd_s6 = QtWidgets.QPushButton(cebsFspcForm)
        self.pushButton_fspc_cmd_s6.setGeometry(QtCore.QRect(260, 670, 111, 41))
        self.pushButton_fspc_cmd_s6.setObjectName("pushButton_fspc_cmd_s6")
        self.pushButton_fspc_cmd_sum = QtWidgets.QPushButton(cebsFspcForm)
        self.pushButton_fspc_cmd_sum.setGeometry(QtCore.QRect(390, 620, 111, 91))
        self.pushButton_fspc_cmd_sum.setObjectName("pushButton_fspc_cmd_sum")
        self.pushButton_fspc_cmd_s7 = QtWidgets.QPushButton(cebsFspcForm)
        self.pushButton_fspc_cmd_s7.setGeometry(QtCore.QRect(20, 720, 111, 41))
        self.pushButton_fspc_cmd_s7.setObjectName("pushButton_fspc_cmd_s7")

        self.retranslateUi(cebsFspcForm)
        self.pushButton_fspc_clear.clicked.connect(cebsFspcForm.slot_clear)
        self.pushButton_fspc_giveup.clicked.connect(cebsFspcForm.slot_giveup)
        self.pushButton_fspc_compl.clicked.connect(cebsFspcForm.slot_cmpl)
        self.pushButton_fspc_pic_file_load.clicked.connect(cebsFspcForm.slot_file_load)
        self.pushButton_fspc_cmd_s1.clicked.connect(cebsFspcForm.slot_cmd_s1)
        self.pushButton_fspc_cmd_s2.clicked.connect(cebsFspcForm.slot_cmd_s2)
        self.pushButton_fspc_cmd_s3.clicked.connect(cebsFspcForm.slot_cmd_s3)
        self.pushButton_fspc_cmd_s4.clicked.connect(cebsFspcForm.slot_cmd_s4)
        self.pushButton_fspc_cmd_s5.clicked.connect(cebsFspcForm.slot_cmd_s5)
        self.pushButton_fspc_cmd_s6.clicked.connect(cebsFspcForm.slot_cmd_s6)
        self.pushButton_fspc_cmd_s7.clicked.connect(cebsFspcForm.slot_cmd_s7)
        self.pushButton_fspc_cmd_sum.clicked.connect(cebsFspcForm.slot_cmd_sum)
        QtCore.QMetaObject.connectSlotsByName(cebsFspcForm)

    def retranslateUi(self, cebsFspcForm):
        _translate = QtCore.QCoreApplication.translate
        cebsFspcForm.setWindowTitle(_translate("cebsFspcForm", "荧光堆叠图像识别"))
        self.label_fspc_pic_file_load.setText(_translate("cebsFspcForm", "图像文件"))
        self.pushButton_fspc_pic_file_load.setText(_translate("cebsFspcForm", "文件导入"))
        self.groupBox_fpsc_pic_show.setTitle(_translate("cebsFspcForm", "图像显示"))
        self.label_pic_fspc_fill.setText(_translate("cebsFspcForm", "TextLabel"))
        self.pushButton_fspc_cmd_s1.setText(_translate("cebsFspcForm", "1)标定黄线"))
        self.groupBox_fspc_set.setTitle(_translate("cebsFspcForm", "参数设置"))
        self.lineEdit_fspc_coef_cell_min.setText(_translate("cebsFspcForm", "920"))
        self.label_fspc_coef_cell_min.setText(_translate("cebsFspcForm", "细胞面积下限"))
        self.lineEdit_fspc_coef_cell_max.setText(_translate("cebsFspcForm", "1500"))
        self.label_fspc_coef_cell_max.setText(_translate("cebsFspcForm", "细胞面积上限"))
        self.lineEdit_fspc_coef_raduis_min.setText(_translate("cebsFspcForm", "19"))
        self.label_fspc_coef_raduis_min.setText(_translate("cebsFspcForm", "细胞半径下限"))
        self.lineEdit_fspc_coef_raduis_max.setText(_translate("cebsFspcForm", "23"))
        self.label_fspc_coef_raduis_max.setText(_translate("cebsFspcForm", "细胞半径上限"))
        self.checkBox_fspc_output_addup.setText(_translate("cebsFspcForm", "输出图像叠加标定"))
        self.lineEdit_fspc_coef_area_dilate.setText(_translate("cebsFspcForm", "1500"))
        self.label_fspc_coef_area_dilate.setText(_translate("cebsFspcForm", "区域膨胀系数"))
        self.lineEdit_fspc_coef_area_erode.setText(_translate("cebsFspcForm", "5"))
        self.label_fspc_coef_area_erode.setText(_translate("cebsFspcForm", "区域腐蚀系数"))
        self.label_fspc_coef_cell_ce.setText(_translate("cebsFspcForm", "细胞圆度下限"))
        self.lineEdit_fspc_coef_cell_ce.setText(_translate("cebsFspcForm", "50"))
        self.lineEdit_fspc_coef_cell_raduis_dist.setText(_translate("cebsFspcForm", "30"))
        self.label_fspc_coef_cell_raduis_dist.setText(_translate("cebsFspcForm", "细胞圆心间距"))
        self.label_fspc_coef_mark_line.setText(_translate("cebsFspcForm", "标定线放长系数"))
        self.label_fspc_coef_area_max.setText(_translate("cebsFspcForm", "区域面积上限"))
        self.lineEdit_fspc_coef_area_max.setText(_translate("cebsFspcForm", "1000000"))
        self.lineEdit_fspc_mark_line.setText(_translate("cebsFspcForm", "222"))
        self.label_fspc_coef_cell_erode.setText(_translate("cebsFspcForm", "细胞腐蚀系数"))
        self.lineEdit_fspc_coef_cell_erode.setText(_translate("cebsFspcForm", "5"))
        self.lineEdit_fspc_coef_cell_dilate.setText(_translate("cebsFspcForm", "61"))
        self.label_fspc_coef_cell_dilate.setText(_translate("cebsFspcForm", "细胞膨胀系数"))
        self.lineEdit_fspc_coef_area_min.setText(_translate("cebsFspcForm", "100000"))
        self.label_fspc_coef_area_min.setText(_translate("cebsFspcForm", "区域面积下限"))
        self.lineEdit_fspc_mark_width.setText(_translate("cebsFspcForm", "44"))
        self.label_fspc_coef_mark_width.setText(_translate("cebsFspcForm", "标定线加宽系数"))
        self.lineEdit_fspc_mark_dilate.setText(_translate("cebsFspcForm", "22"))
        self.label_fspc_coef_mark_dilate.setText(_translate("cebsFspcForm", "标定线膨胀系数"))
        self.label_fspc_coef_mark_area.setText(_translate("cebsFspcForm", "标定线面积系数"))
        self.lineEdit_fspc_mark_area.setText(_translate("cebsFspcForm", "10000"))
        self.lineEdit_fspc_pic_train_delay.setText(_translate("cebsFspcForm", "5"))
        self.label_fspc_pic_train_delay.setText(_translate("cebsFspcForm", "训练显示延时"))
        self.label_fspc_pic_train_sec.setText(_translate("cebsFspcForm", "秒"))
        self.pushButton_fspc_cmd_s2.setText(_translate("cebsFspcForm", "2)划定大区"))
        self.pushButton_fspc_cmd_s3.setText(_translate("cebsFspcForm", "3)抠取小区"))
        self.pushButton_fspc_cmd_s4.setText(_translate("cebsFspcForm", "4)细胞匹配"))
        self.groupBox_cmd_log.setTitle(_translate("cebsFspcForm", "命令信息"))
        self.textEdit_fspc_cmd_log.setHtml(_translate("cebsFspcForm", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">TRACE LOG</p></body></html>"))
        self.pushButton_fspc_clear.setText(_translate("cebsFspcForm", "命令清除"))
        self.pushButton_fspc_giveup.setText(_translate("cebsFspcForm", "设定放弃"))
        self.pushButton_fspc_compl.setText(_translate("cebsFspcForm", "设定完成"))
        self.pushButton_fspc_cmd_s5.setText(_translate("cebsFspcForm", "5)去伪存真"))
        self.pushButton_fspc_cmd_s6.setText(_translate("cebsFspcForm", "6)复核校验"))
        self.pushButton_fspc_cmd_sum.setText(_translate("cebsFspcForm", "一键执行"))
        self.pushButton_fspc_cmd_s7.setText(_translate("cebsFspcForm", "7)最终输出"))

