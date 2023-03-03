# KanaKana
# Author: Gunbard

import json, os, sys, asyncio, qasync
from mainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from upcDataRetriever import UpcDataRetriever

APP_TITLE = 'KanaKana'
VERSION = '0.1.0'
WINDOW_TITLE = "{} {}".format(APP_TITLE, VERSION)

MAX_BATCH_SIZE = 1 

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

ui.actionQuit.triggered.connect(lambda: app.quit())
ui.statusBar.showMessage('12 items in [PS2 Games]')

def addUpc():
    upc = ui.lineEditAddUPC.text()
    if not upc:
        return

    upcDataRetriever = UpcDataRetriever(upc)
    stuff = upcDataRetriever.get()
    ui.tableData.setRowCount(ui.tableData.rowCount() + 1)
    ui.tableData.setItem(ui.tableData.rowCount() - 1, 0, QTableWidgetItem(stuff['title']))
    ui.tableData.setItem(ui.tableData.rowCount() - 1, 1, QTableWidgetItem(stuff['description']))
    ui.tableData.setItem(ui.tableData.rowCount() - 1, 2, QTableWidgetItem(upc))
    ui.lineEditAddUPC.clear()

ui.buttonAddUPC.clicked.connect(addUpc)
ui.lineEditAddUPC.returnPressed.connect(addUpc)

with loop:
    loop.run_forever()