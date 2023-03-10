# KataKata
# Author: Gunbard

import os
import sys
import asyncio
import qasync
from mainWindow import Ui_MainWindow
from enum import Enum
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QLabel, QMenu, QMessageBox
from pyqtspinner import WaitingSpinner
from retrievers.upcDataRetriever import UpcDataRetriever
from models.catalogModel import CatalogModel
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

currentCatalog = CatalogModel([], None)

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

def updateTitle():
  global currentCatalog

  if ui.tableData.rowCount() == 0:
    MainWindow.setWindowTitle(WINDOW_TITLE)
    return

  unsavedIndicator = '*' if ui.actionSave_Catalog.isEnabled() else ''
  MainWindow.setWindowTitle("{} - {}{}".format(
    WINDOW_TITLE, currentCatalog.getTitle(), unsavedIndicator))

def updateTable():
  global currentCatalog

  ui.tableData.setRowCount(0)

  if currentCatalog.data:
    for item in currentCatalog.data:
      addItem(item)

  ui.statusBar.showMessage("{} item(s) in [{}]".format(ui.tableData.rowCount(), currentCatalog.getTitle()))
  updateTitle()

def addItem(item):
  table = ui.tableData
  table.setRowCount(table.rowCount() + 1)
  lastRow = table.rowCount() - 1
  updateItemInRow(item, lastRow)

def updateItemInRow(item, row):
  table = ui.tableData
  table.setItem(row, TableColumns.UPC.value, QTableWidgetItem(item.upc))

  itemName = QTableWidgetItem(item.name)
  itemName.setToolTip(item.name)
  table.setItem(row, TableColumns.NAME.value, itemName)

  descriptionItem = QTableWidgetItem(item.description)
  descriptionItem.setToolTip(item.description)
  table.setItem(row, TableColumns.DESCRIPTION.value, descriptionItem)

  newLabel = QLabel()
  newLabel.setAlignment(QtCore.Qt.AlignCenter)
  if item.image:
    newLabel.setPixmap(item.image)

  table.setCellWidget(row, TableColumns.IMAGE.value, newLabel)

  noteItem = QTableWidgetItem(item.note)
  table.setItem(row, TableColumns.NOTE.value, noteItem)

def refreshSelection(selections):
  global currentCatalog

  retriever = UpcDataRetriever()
  for index in selections:
    item = currentCatalog.data[index.row()]
    if item:
      retriever.refresh(item)
      updateItemInRow(item, index.row())
      ui.actionSave_Catalog.setEnabled(True)
      updateTitle()
      return

def deleteSelection(selections):
  global currentCatalog

  answer = QMessageBox().question(MainWindow, \
    'Delete Item', \
    "Are you sure you want to delete this row?", \
    QMessageBox.Ok | QMessageBox.Cancel, \
    QMessageBox.Cancel)
  if answer == QMessageBox.Ok:
    for index in selections:
      del currentCatalog.data[index.row()]
      ui.actionSave_Catalog.setEnabled(True)
      updateTable()
      return

def addUpc():
  global currentCatalog
  
  upc = ui.lineEditAddUPC.text()
  if not upc:
    return

  newItem = ItemModel(None, None, None, upc, None)

  if ui.checkBoxAutorefreshUPC.isChecked():
    UpcDataRetriever().refresh(newItem)

  currentCatalog.data.append(newItem)
  ui.actionSave_Catalog.setEnabled(True)
  updateTable()

  ui.lineEditAddUPC.clear()

def moveRow(up, selection):
  global currentCatalog

  row = selection[0].row()
  direction = -1 if up == True else 1

  if up == True and row == 0:
    return
  elif up == False and row == ui.tableData.rowCount() - 1:
    return

  targetRow = row + (1 * direction)

  currentCatalog.data[row], currentCatalog.data[targetRow] = currentCatalog.data[targetRow], currentCatalog.data[row]
    
  ui.actionSave_Catalog.setEnabled(True)
  updateItemInRow(currentCatalog.data[row], row)
  updateItemInRow(currentCatalog.data[targetRow], targetRow)
  ui.tableData.selectRow(targetRow)
  updateTitle()

def tableContextMenu(position):
  selection = ui.tableData.selectionModel().selectedRows()
  rowCount = ui.tableData.rowCount()
  if rowCount == 0:
    return
  menu = QMenu()
  moveUpAction = menu.addAction("Move Up")
  if selection[0].row() == 0:
    moveUpAction.setEnabled(False)
  moveDownAction = menu.addAction("Move Down")
  if selection[0].row() == rowCount - 1:
    moveDownAction.setEnabled(False)
  menu.addSeparator()
  refreshAction = menu.addAction("Refresh")
  menu.addSeparator()
  deleteAction = menu.addAction("Delete")

  action = menu.exec_(ui.tableData.mapToGlobal(position))
  if action == moveUpAction:
    moveRow(True, selection)
  elif action == moveDownAction:
    moveRow(False, selection)
  elif action == refreshAction:
    refreshSelection(selection)
  elif action == deleteAction:
    deleteSelection(selection)

def importFromFile():
  global currentCatalog

  if not checkUnsavedChanges():
    return

  path = QtWidgets.QFileDialog.getOpenFileName(None, "Select file with list of UPCs...", os.curdir, \
        "All files (*.*)")
  if not path[0]:
    return
  fileHandle = open(path[0])
  for line in fileHandle:
      currentCatalog.data.append(ItemModel(None, None, None, line.strip(), None))
  updateTable()

def newCatalog():
  global currentCatalog

  if not checkUnsavedChanges():
    return

  currentCatalog = CatalogModel([], None)
  updateTable()

def openCatalog():
  global currentCatalog

  if not checkUnsavedChanges():
    return

  path = QtWidgets.QFileDialog.getOpenFileName(None, "Select a catalog file...", os.curdir, \
        "Catalog file (*.json);;All files (*.*)")
  currentCatalog = CatalogModel(None, path[0])
  currentCatalog.load()
  updateTable()

def saveCatalog(forceSave):
  global currentCatalog

  if forceSave or not currentCatalog or not currentCatalog.filepath:
    savePath = QtWidgets.QFileDialog.getSaveFileName(None, "Save catalog...", os.curdir, \
    "Catalog file (*.json);;All files (*.*)")
    if not savePath[0]:
      return
    currentCatalog = CatalogModel(currentCatalog.data, savePath[0])

  currentCatalog.save()
  ui.actionSave_Catalog.setEnabled(False)
  updateTitle()

def itemUpdated(topLeft, bottomRight, roles):
  global currentCatalog

  for role in roles:
    if role == QtCore.Qt.ItemDataRole.EditRole:
      # Front-end is updated already so just need to update model
      updatedData = ui.tableData.model().data(topLeft)
      item = currentCatalog.data[topLeft.row()]
      if topLeft.column() == TableColumns.NAME.value:
        item.name = updatedData
      elif topLeft.column() == TableColumns.DESCRIPTION.value:
        item.description = updatedData
      elif topLeft.column() == TableColumns.UPC.value:
        item.upc = updatedData
      elif topLeft.column() == TableColumns.NOTE.value:
        item.note = updatedData

      ui.actionSave_Catalog.setEnabled(True)
      updateTitle()

def checkUnsavedChanges():
  if not ui.actionSave_Catalog.isEnabled():
    return True

  answer = QMessageBox().question(MainWindow, \
  'Unsaved Changes', \
  "Save changes?", \
  QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, \
  QMessageBox.Cancel)

  if answer == QMessageBox.Save:
    ui.actionSave_Catalog.trigger()
    return True
  elif answer == QMessageBox.Discard:
    return True
  else:
    return False

def quitApp():
  if checkUnsavedChanges():
    app.quit()

def appClose(event):
  if checkUnsavedChanges():
    event.accept()
  else:
    event.ignore()

def showAbout():
  QMessageBox.about(MainWindow, 'About', 'Written with olev by: Gunbard<br>\
  GitHub: <a href="https://github.com/Gunbard/KataKata">https://github.com/Gunbard/KataKata</a>')

# EVENTS
MainWindow.closeEvent = lambda event: appClose(event)
ui.buttonAddUPC.clicked.connect(addUpc)
ui.lineEditAddUPC.returnPressed.connect(addUpc)
ui.tableData.customContextMenuRequested.connect(tableContextMenu)
ui.tableData.model().dataChanged.connect(itemUpdated)
ui.actionNew_Catalog.triggered.connect(newCatalog)
ui.actionOpen_Catalog.triggered.connect(openCatalog)
ui.actionSave_Catalog.triggered.connect(saveCatalog)
ui.actionSave_Catalog_As.triggered.connect(lambda: saveCatalog(True))
ui.actionImport.triggered.connect(importFromFile)
ui.actionQuit.triggered.connect(quitApp)
ui.actionAbout.triggered.connect(showAbout)

# spinner = WaitingSpinner(ui.tableData, True, True, QtCore.Qt.ApplicationModal)
# spinner.start() # starts spinning

with loop:
  loop.run_forever()
