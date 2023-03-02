# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 598)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setObjectName("gridLayout")
        self.tableData = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableData.sizePolicy().hasHeightForWidth())
        self.tableData.setSizePolicy(sizePolicy)
        self.tableData.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableData.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.tableData.setDragEnabled(True)
        self.tableData.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.tableData.setAlternatingRowColors(True)
        self.tableData.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableData.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableData.setCornerButtonEnabled(True)
        self.tableData.setRowCount(5)
        self.tableData.setColumnCount(5)
        self.tableData.setObjectName("tableData")
        item = QtWidgets.QTableWidgetItem()
        self.tableData.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableData.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableData.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableData.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableData.setHorizontalHeaderItem(4, item)
        self.tableData.horizontalHeader().setVisible(True)
        self.tableData.horizontalHeader().setCascadingSectionResizes(False)
        self.tableData.horizontalHeader().setDefaultSectionSize(120)
        self.tableData.horizontalHeader().setStretchLastSection(True)
        self.tableData.verticalHeader().setVisible(True)
        self.tableData.verticalHeader().setDefaultSectionSize(64)
        self.tableData.verticalHeader().setSortIndicatorShown(False)
        self.tableData.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.tableData, 1, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.labelCategory = QtWidgets.QLabel(self.centralwidget)
        self.labelCategory.setObjectName("labelCategory")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelCategory)
        self.comboBoxCategory = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxCategory.setMaxVisibleItems(9)
        self.comboBoxCategory.setObjectName("comboBoxCategory")
        self.comboBoxCategory.addItem("")
        self.comboBoxCategory.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBoxCategory)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.checkBoxAutorefreshUPC = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxAutorefreshUPC.setObjectName("checkBoxAutorefreshUPC")
        self.gridLayout_3.addWidget(self.checkBoxAutorefreshUPC, 0, 5, 1, 1)
        self.buttonAddUPC = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonAddUPC.sizePolicy().hasHeightForWidth())
        self.buttonAddUPC.setSizePolicy(sizePolicy)
        self.buttonAddUPC.setMinimumSize(QtCore.QSize(32, 0))
        self.buttonAddUPC.setMaximumSize(QtCore.QSize(32, 16777215))
        self.buttonAddUPC.setObjectName("buttonAddUPC")
        self.gridLayout_3.addWidget(self.buttonAddUPC, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 0, 1, 1)
        self.labelAddUPC = QtWidgets.QLabel(self.centralwidget)
        self.labelAddUPC.setObjectName("labelAddUPC")
        self.gridLayout_3.addWidget(self.labelAddUPC, 0, 1, 1, 1)
        self.lineEditAddUPC = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditAddUPC.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEditAddUPC.setObjectName("lineEditAddUPC")
        self.gridLayout_3.addWidget(self.lineEditAddUPC, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 6, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 4, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuCategory = QtWidgets.QMenu(self.menubar)
        self.menuCategory.setObjectName("menuCategory")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOptions = QtWidgets.QAction(MainWindow)
        self.actionOptions.setObjectName("actionOptions")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionRefresh_All = QtWidgets.QAction(MainWindow)
        self.actionRefresh_All.setObjectName("actionRefresh_All")
        self.actionDelete_Selected = QtWidgets.QAction(MainWindow)
        self.actionDelete_Selected.setObjectName("actionDelete_Selected")
        self.actionRefresh_Selected = QtWidgets.QAction(MainWindow)
        self.actionRefresh_Selected.setObjectName("actionRefresh_Selected")
        self.actionDelete_All = QtWidgets.QAction(MainWindow)
        self.actionDelete_All.setObjectName("actionDelete_All")
        self.actionGenerate_HTML_Report = QtWidgets.QAction(MainWindow)
        self.actionGenerate_HTML_Report.setObjectName("actionGenerate_HTML_Report")
        self.actionExport_to_CSV = QtWidgets.QAction(MainWindow)
        self.actionExport_to_CSV.setObjectName("actionExport_to_CSV")
        self.actionManage_Categories = QtWidgets.QAction(MainWindow)
        self.actionManage_Categories.setObjectName("actionManage_Categories")
        self.menuFile.addAction(self.actionOptions)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuTools.addAction(self.actionManage_Categories)
        self.menuTools.addAction(self.actionExport_to_CSV)
        self.menuTools.addAction(self.actionGenerate_HTML_Report)
        self.menuCategory.addAction(self.actionRefresh_Selected)
        self.menuCategory.addAction(self.actionRefresh_All)
        self.menuCategory.addSeparator()
        self.menuCategory.addAction(self.actionDelete_Selected)
        self.menuCategory.addAction(self.actionDelete_All)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCategory.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "KataKata"))
        self.tableData.setSortingEnabled(True)
        item = self.tableData.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableData.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "UPC"))
        item = self.tableData.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableData.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Image"))
        item = self.tableData.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Note"))
        self.labelCategory.setText(_translate("MainWindow", "Category: "))
        self.comboBoxCategory.setItemText(0, _translate("MainWindow", "PS2 Games"))
        self.comboBoxCategory.setItemText(1, _translate("MainWindow", "Nendoroids"))
        self.checkBoxAutorefreshUPC.setText(_translate("MainWindow", "Auto-refresh newly added UPCs"))
        self.buttonAddUPC.setText(_translate("MainWindow", "+"))
        self.labelAddUPC.setText(_translate("MainWindow", "Add UPC: "))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuCategory.setTitle(_translate("MainWindow", "Category"))
        self.actionImport.setText(_translate("MainWindow", "Import UPCs..."))
        self.actionExport.setText(_translate("MainWindow", "Export..."))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionOptions.setText(_translate("MainWindow", "Options"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionRefresh_All.setText(_translate("MainWindow", "Refresh All"))
        self.actionDelete_Selected.setText(_translate("MainWindow", "Delete Selected"))
        self.actionRefresh_Selected.setText(_translate("MainWindow", "Refresh Selected"))
        self.actionDelete_All.setText(_translate("MainWindow", "Delete All"))
        self.actionGenerate_HTML_Report.setText(_translate("MainWindow", "Generate HTML Report"))
        self.actionExport_to_CSV.setText(_translate("MainWindow", "Export to CSV"))
        self.actionManage_Categories.setText(_translate("MainWindow", "Manage Categories..."))
