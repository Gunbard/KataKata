# KataKata
# Author: Gunbard

import os
import sys
import asyncio
import qasync
import time
import urllib.parse
import webbrowser
from mainWindow import Ui_MainWindow
from refreshDialog import Ui_RefreshDialog
from enum import Enum
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QLabel, QMenu, QMessageBox
from retrievers.upcDataRetriever import UpcDataRetriever
from models.catalogModel import CatalogModel
from models.itemModel import ItemModel

APP_TITLE = 'KataKata'
VERSION = '1.6.0'
WINDOW_TITLE = "{}".format(APP_TITLE)
MAX_BATCH_SIZE = 1

class TableColumns(Enum):
  NAME = 0
  DESCRIPTION = 1
  IMAGE = 2
  UPC = 3
  NOTE = 4
  UUID = 5

currentCatalog = CatalogModel([], None)
findMatches = None
findMatchIndex = None

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
ui.tableData.hideColumn(TableColumns.UUID.value)
status = QLabel("")
ui.statusBar.addPermanentWidget(status)

RefreshDialog = QtWidgets.QDialog(MainWindow)
refreshDialog = Ui_RefreshDialog()
refreshDialog.setupUi(RefreshDialog)

MainWindow.setWindowTitle("{} - {}".format(
    "New Catalog", WINDOW_TITLE))
MainWindow.show()

def updateTitle():
  global currentCatalog

  if ui.tableData.rowCount() == 0:
    MainWindow.setWindowTitle("{} - {}".format(
     "New Catalog", WINDOW_TITLE))
    return

  unsavedIndicator = '*' if ui.actionSave_Catalog.isEnabled() else ''
  MainWindow.setWindowTitle("{}{} - {}".format(
    currentCatalog.getTitle(), unsavedIndicator, WINDOW_TITLE))

def getItemByRow(row):
  index = ui.tableData.model().index(row, TableColumns.UUID.value)
  uid = ui.tableData.model().data(index)
  return next((item for item in currentCatalog.data if item.uid == uid), None)

def updateTable():
  global currentCatalog

  ui.tableData.setSortingEnabled(False)
  ui.tableData.setRowCount(0)
  ui.tableData.setStyleSheet("selection-background-color: DeepSkyBlue")

  if currentCatalog.data:
    for item in currentCatalog.data:
      addItem(item)

  ui.tableData.setSortingEnabled(True)

  status.setText("{} item(s) in [{}]".format(ui.tableData.rowCount(), currentCatalog.getTitle()))
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
    newLabel.setPixmap(item.imageThumbnail())

  table.setCellWidget(row, TableColumns.IMAGE.value, newLabel)

  noteItem = QTableWidgetItem(item.note)
  table.setItem(row, TableColumns.NOTE.value, noteItem)

  uuidItem = QTableWidgetItem(item.uid)
  table.setItem(row, TableColumns.UUID.value, uuidItem)

def refreshAll(newOnly):
  global currentCatalog

  if currentCatalog == None or not currentCatalog.data:
    return
  
  itemsToRefresh = list(filter(lambda item: item.name == None, currentCatalog.data)) if newOnly == True else currentCatalog.data

  if not itemsToRefresh:
    return

  itemRefreshCount = len(itemsToRefresh)

  dialogTitle = RefreshDialog.windowTitle()
  RefreshDialog.setWindowTitle(dialogTitle + ' (1 / ' + str(itemRefreshCount) + ')')

  progressBar = refreshDialog.refreshProgressBar
  progressBar.setValue(0)
  progressBar.setMaximum(itemRefreshCount - 1)

  RefreshDialog.show()

  retriever = UpcDataRetriever()

  # TODO: Use a thread

  for index, item in enumerate(itemsToRefresh):
    if not RefreshDialog.isVisible():
      break
    status = retriever.refresh(item)
    if status:
      progressBar.setStyleSheet('color: red')
    progressBar.setValue(index)
    RefreshDialog.setWindowTitle(dialogTitle + ' (' + str(index + 1) + ' / ' + str(itemRefreshCount) + ')')
    progressBar.update()
    app.processEvents()
    time.sleep(2)

  # Reset title
  RefreshDialog.setWindowTitle(dialogTitle)
  RefreshDialog.close()
  
  ui.actionSave_Catalog.setEnabled(True)
  updateTitle()
  updateTable()

def refreshDialogClosed(event):
  print("Refresh dialog closed")

def refreshSelection(selections):
  global currentCatalog

  retriever = UpcDataRetriever()
  for index in selections:
    item = getItemByRow(index.row())
    if item:
      status = retriever.refresh(item)
      if status:
        QMessageBox().warning(MainWindow, "Error", "Failed to refresh :/")
        return

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
      item = getItemByRow(index.row())
      if item:
        currentCatalog.data.remove(item)
        ui.actionSave_Catalog.setEnabled(True)
        updateTable()
        return

def addUpc():
  global currentCatalog
  
  upc = ui.lineEditAddUPC.text()
  if not upc:
    return

  newItem = ItemModel(None, None, None, upc, None, None)
  newItem.generateUuid()

  if ui.checkBoxAutorefreshUPC.isChecked():
    UpcDataRetriever().refresh(newItem)

  currentCatalog.data.append(newItem)
  ui.actionSave_Catalog.setEnabled(True)
  updateTable()

  ui.lineEditAddUPC.clear()

def doGoogle(selections):
  global currentCatalog

  retriever = UpcDataRetriever()
  for index in selections:
    item = getItemByRow(index.row())
    if item:
      webbrowser.open("https://www.google.com/search?q={}".format(urllib.parse.quote_plus(item.name)))

def tableContextMenu(position):
  selection = ui.tableData.selectionModel().selectedRows()
  rowCount = ui.tableData.rowCount()
  if rowCount == 0:
    return
  menu = QMenu()
  googleAction = menu.addAction("Google")
  refreshAction = menu.addAction("Refresh")
  menu.addSeparator()
  deleteAction = menu.addAction("Delete")

  action = menu.exec_(ui.tableData.mapToGlobal(position))
  if action == googleAction:
    doGoogle(selection)
  elif action == refreshAction:
    refreshSelection(selection)
  elif action == deleteAction:
    deleteSelection(selection)

def tableItemDoubleClicked(row, column):
  if not column == TableColumns.IMAGE.value:
    return
  
  item = getItemByRow(row)

  if not item:
    return
  
  image = item.image

  if not image:
    return
  
  newLabel = QtWidgets.QLabel()
  newLabel.setPixmap(image)
  newLabel.setMinimumSize(1, 1)

  def resized(newSize):
    newLabel.setPixmap(image.scaled(newSize.size().width(), newSize.size().height(), \
                                    QtCore.Qt.KeepAspectRatio, \
                                    QtCore.Qt.SmoothTransformation))

  newDialog = QtWidgets.QDialog()
  newDialog.setWindowTitle("Image Viewer")
  newDialog.resizeEvent = resized
  newDialog.setMaximumSize(app.primaryScreen().availableSize().width(), \
                           app.primaryScreen().availableSize().height())
  dialogLayout = QtWidgets.QGridLayout()
  dialogLayout.setContentsMargins(0, 0, 0, 0)
  dialogLayout.addWidget(newLabel, 0, 0, QtCore.Qt.AlignCenter)
  newDialog.setLayout(dialogLayout)
  newDialog.exec()

def findChanged(shouldClear):
  global findMatches, findMatchIndex

  if len(ui.lineEditFind.text()) == 0:
    return

  if shouldClear:
    ui.lineEditFind.clear()
    ui.tableData.clearSelection()
  findMatchIndex = None
  findMatches = None
  ui.statusBar.clearMessage()

def scrollToFoundItem():
  global findMatches, findMatchIndex

  if not findMatches or findMatchIndex == None:
    return

  ui.tableData.scrollToItem(findMatches[findMatchIndex], QtWidgets.QAbstractItemView.ScrollHint.PositionAtCenter)
  # Deselect previous, if any
  ui.tableData.clearSelection()
  for item in findMatches:
    item.setSelected(False)
  findMatches[findMatchIndex].setSelected(True)

  ui.statusBar.showMessage("Found {}/{}".format(findMatchIndex + 1, len(findMatches)))

def find(previous):
  global findMatches, findMatchIndex
  
  if len(ui.lineEditFind.text()) == 0:
    return

  if not findMatches:
    matches = ui.tableData.findItems(ui.lineEditFind.text(), QtCore.Qt.MatchFlag.MatchContains)
    
    if matches:
      findMatches = matches
      findMatchIndex = 0
  else:
    if previous:
      if findMatchIndex > 0:
        findMatchIndex -= 1
      else:
        findMatchIndex = len(findMatches) - 1
    else:
      if findMatchIndex < len(findMatches) - 1:
        findMatchIndex += 1
      else:
        findMatchIndex = 0

  scrollToFoundItem()

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
      upc = line.strip()
      if upc:
        newItem = ItemModel(None, None, None, upc, None, None)
        newItem.generateUuid()
        currentCatalog.data.append(newItem)
  updateTable()

def newCatalog():
  global currentCatalog

  if not checkUnsavedChanges():
    return

  currentCatalog = CatalogModel([], None)
  updateTable()
  ui.actionGenerate_HTML_Report.setEnabled(False)
  ui.actionGenerate_CSV_File.setEnabled(False)

def openCatalog():
  global currentCatalog

  if not checkUnsavedChanges():
    return

  path = QtWidgets.QFileDialog.getOpenFileName(None, "Select a catalog file...", os.curdir, \
        "Catalog file (*.json);;All files (*.*)")
  if not path[0]:
    return
  currentCatalog = CatalogModel(None, path[0])
  currentCatalog.load()
  updateTable()
  ui.actionGenerate_HTML_Report.setEnabled(True)
  ui.actionGenerate_CSV_File.setEnabled(True)

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
  updateTable()

def itemUpdated(topLeft, bottomRight, roles):
  global currentCatalog

  for role in roles:
    if role == QtCore.Qt.ItemDataRole.EditRole:
      # Front-end is updated already so just need to update model
      updatedData = ui.tableData.model().data(topLeft)
      item = getItemByRow(topLeft.row())
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
  QMessageBox.about(MainWindow, 'About', 'KataKata {}<br>Written with olev by: Gunbard<br>\
  GitHub: <a href="https://github.com/Gunbard/KataKata">https://github.com/Gunbard/KataKata</a>'.format(VERSION))

def generateReport():
  global currentCatalog

  if currentCatalog and currentCatalog.filepath:
    savePath = QtWidgets.QFileDialog.getSaveFileName(None, "Save HTML Report...", "{} - {}".format(APP_TITLE, currentCatalog.getTitle()), \
    "HTML Report (*.html);;All files (*.*)")
    if not savePath[0]:
      return
    
    file = open(savePath[0], 'w', encoding='utf-8')
    file.write(currentCatalog.getHTML())

def generateCSVFile():
  global currentCatalog

  if currentCatalog and currentCatalog.filepath:
    savePath = QtWidgets.QFileDialog.getSaveFileName(None, "Save CSV...", "{} - {}".format(APP_TITLE, currentCatalog.getTitle()), \
    "CSV (*.csv);;All files (*.*)")
    if not savePath[0]:
      return
    
    file = open(savePath[0], 'w' , encoding='utf-8')
    file.write(currentCatalog.getCSV())

# EVENTS
MainWindow.closeEvent = lambda event: appClose(event)
RefreshDialog.closeEvent = lambda event: refreshDialogClosed(event)
ui.buttonAddUPC.clicked.connect(addUpc)
ui.lineEditAddUPC.returnPressed.connect(addUpc)
ui.tableData.customContextMenuRequested.connect(tableContextMenu)
ui.tableData.model().dataChanged.connect(itemUpdated)
ui.tableData.cellDoubleClicked.connect(lambda row, column: tableItemDoubleClicked(row, column))
ui.actionNew_Catalog.triggered.connect(newCatalog)
ui.actionOpen_Catalog.triggered.connect(openCatalog)
ui.actionSave_Catalog.triggered.connect(saveCatalog)
ui.actionSave_Catalog_As.triggered.connect(lambda: saveCatalog(True))
ui.actionImport.triggered.connect(importFromFile)
ui.actionQuit.triggered.connect(quitApp)
ui.actionGenerate_HTML_Report.triggered.connect(generateReport)
ui.actionGenerate_CSV_File.triggered.connect(generateCSVFile)
ui.actionRefreshAll.triggered.connect(lambda: refreshAll(False))
ui.actionRefreshAllNew.triggered.connect(lambda: refreshAll(True))
ui.actionAbout.triggered.connect(showAbout)
ui.findButton.clicked.connect(lambda: find(False))
ui.findClearButton.clicked.connect(lambda: findChanged(True))
ui.findPrevButton.clicked.connect(lambda: find(True))
ui.lineEditFind.returnPressed.connect(lambda: find(False))
ui.lineEditFind.textChanged.connect(lambda: findChanged(False))

with loop:
  loop.run_forever()
