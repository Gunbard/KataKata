# KataKata
# Author: Gunbard

import json, os, sys, asyncio, qasync
from mainWindow import Ui_MainWindow
from enum import Enum
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QLabel, QMenu
from pyqtspinner import WaitingSpinner
from retrievers.upcDataRetriever import UpcDataRetriever
from models.itemModel import ItemModel

APP_TITLE = 'KataKata'
VERSION = '0.1.0'
WINDOW_TITLE = "{} {}".format(APP_TITLE, VERSION)

MAX_BATCH_SIZE = 1 

class TableColumns(Enum):
    NAME = 0
    DESCRIPTION = 1
    IMAGE = 2
    UPC = 3
    NOTE = 4

categoryData = []

# APP SETUP

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)
app = QtWidgets.QApplication(sys.argv)
loop = qasync.QEventLoop(app)
asyncio.set_event_loop(loop)
asyncio.events._set_running_loop(loop)
asyncio_semaphore = asyncio.Semaphore(MAX_BATCH_SIZE)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

MainWindow.setWindowTitle(WINDOW_TITLE)
MainWindow.show()

def updateTable():
    ui.tableData.setRowCount(0)

    for item in categoryData:
        addItem(item)

def addItem(item):
    table = ui.tableData
    table.setRowCount(table.rowCount() + 1)
    lastRow = table.rowCount() - 1
    table.setItem(lastRow, TableColumns.NAME.value, QTableWidgetItem(item.name))
    table.setItem(lastRow, TableColumns.DESCRIPTION.value, QTableWidgetItem(item.description))
    table.setItem(lastRow, TableColumns.UPC.value, QTableWidgetItem(item.upc))
    
    newLabel = QLabel()
    newLabel.setAlignment(QtCore.Qt.AlignCenter)
    if item.image:
        newLabel.setPixmap(item.image)

    table.setCellWidget(lastRow, TableColumns.IMAGE.value, newLabel)

def refreshSelection(selections):
    retriever = UpcDataRetriever()
    for index in selections:
        item = categoryData[index.row()]
        if item:
            retriever.refresh(item)
    updateTable()

def addUpc():
    upc = ui.lineEditAddUPC.text()
    if not upc:
        return

    newItem = ItemModel(None, None, None, upc, None)

    if ui.checkBoxAutorefreshUPC.isChecked():
        UpcDataRetriever().refresh(newItem)

    categoryData.append(newItem)
    updateTable()

    ui.lineEditAddUPC.clear()
    ui.statusBar.showMessage("{} item(s) in [PS2 Games]".format(ui.tableData.rowCount()))

def tableContextMenu(position):
    if ui.tableData.rowCount() == 0:
        return
    menu = QMenu()
    refreshAction = menu.addAction("Refresh")
    menu.addSeparator()
    deleteAction = menu.addAction("Delete")
    
    action = menu.exec_(ui.tableData.mapToGlobal(position))
    if action == refreshAction:
        refreshSelection(ui.tableData.selectionModel().selectedRows())
        
# EVENTS
ui.buttonAddUPC.clicked.connect(addUpc)
ui.lineEditAddUPC.returnPressed.connect(addUpc)
ui.tableData.customContextMenuRequested.connect(tableContextMenu)
ui.actionQuit.triggered.connect(lambda: app.quit())

#spinner = WaitingSpinner(ui.tableData, True, True, QtCore.Qt.ApplicationModal)
#spinner.start() # starts spinning

with loop:
    loop.run_forever()