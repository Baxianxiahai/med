# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cebsSahtform.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_cebsSahtForm(object):
    def setupUi(self, cebsSahtForm):
        cebsSahtForm.setObjectName("cebsSahtForm")
        cebsSahtForm.resize(1187, 812)
        self.textBrowser = QtWidgets.QTextBrowser(cebsSahtForm)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 1011, 691))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(cebsSahtForm)
        QtCore.QMetaObject.connectSlotsByName(cebsSahtForm)

    def retranslateUi(self, cebsSahtForm):
        _translate = QtCore.QCoreApplication.translate
        cebsSahtForm.setWindowTitle(_translate("cebsSahtForm", "板孔激活"))

