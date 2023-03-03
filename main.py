# KataKata
# Author: Gunbard

import json, os, sys, asyncio, qasync
from mainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QLabel, QMenu
from pyqtspinner import WaitingSpinner
from retrievers.upcDataRetriever import UpcDataRetriever
from retrievers.imageRetriever import ImageRetriever

APP_TITLE = 'KataKata'
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

def addUpc():
    upc = ui.lineEditAddUPC.text()
    if not upc:
        return

    if not ui.checkBoxAutorefreshUPC.isChecked():
        ui.tableData.setRowCount(ui.tableData.rowCount() + 1)
        ui.tableData.setItem(ui.tableData.rowCount() - 1, 2, QTableWidgetItem(upc))
        ui.lineEditAddUPC.clear()
        return

    upcData = UpcDataRetriever(upc).get()
    if not upcData:
        return

    ui.tableData.setRowCount(ui.tableData.rowCount() + 1)
    ui.tableData.setItem(ui.tableData.rowCount() - 1, 0, QTableWidgetItem(upcData['title']))
    ui.tableData.setItem(ui.tableData.rowCount() - 1, 1, QTableWidgetItem(upcData['description']))
    ui.tableData.setItem(ui.tableData.rowCount() - 1, 2, QTableWidgetItem(upc))
    image = ImageRetriever(upcData['image_url']).get()
    newLabel = QLabel()
    newLabel.setAlignment(QtCore.Qt.AlignCenter)
    newLabel.setPixmap(image)
    ui.tableData.setCellWidget(ui.tableData.rowCount() - 1, 3, newLabel)
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
    #if action == refreshAction:
        

ui.buttonAddUPC.clicked.connect(addUpc)
ui.lineEditAddUPC.returnPressed.connect(addUpc)
ui.tableData.customContextMenuRequested.connect(tableContextMenu)

#spinner = WaitingSpinner(ui.tableData, True, True, QtCore.Qt.ApplicationModal)
#spinner.start() # starts spinning

with loop:
    loop.run_forever()