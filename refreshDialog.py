# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'refreshDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RefreshDialog(object):
    def setupUi(self, RefreshDialog):
        RefreshDialog.setObjectName("RefreshDialog")
        RefreshDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        RefreshDialog.resize(400, 70)
        RefreshDialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.gridLayoutWidget = QtWidgets.QWidget(RefreshDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 51))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.refreshProgressBar = QtWidgets.QProgressBar(self.gridLayoutWidget)
        self.refreshProgressBar.setProperty("value", 24)
        self.refreshProgressBar.setObjectName("refreshProgressBar")
        self.gridLayout.addWidget(self.refreshProgressBar, 0, 0, 1, 1)

        self.retranslateUi(RefreshDialog)
        QtCore.QMetaObject.connectSlotsByName(RefreshDialog)

    def retranslateUi(self, RefreshDialog):
        _translate = QtCore.QCoreApplication.translate
        RefreshDialog.setWindowTitle(_translate("RefreshDialog", "Getting UPC data..."))
