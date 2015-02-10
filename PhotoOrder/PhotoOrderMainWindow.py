__author__ = 'Sarge'

from PySide.QtCore import *

from PhotoOrderLoginWindow import *
from DropboxFolderList import *
from DropboxFolderListItem import *
from MainWindowMenuBar import *
from FolderProperties import *
from ShareOptions import *


class PhotoOrderMainWindow (QMainWindow):

    def __init__(self, dropboxConnection, mainApp, config, databaseConnection):
        super().__init__()
        self.mainApp = mainApp
        self.config = config
        self.dropboxConnection = dropboxConnection
        self.databaseConnection = databaseConnection
        self.databaseConnection.connectionChange.connect(self.updateDBConnectionStatus)
        self.setWindowTitle('PhotoOrder Alpha 0.1')
        self.resize(800, 600)

        self.tabWidget = QTabWidget(self)
        self.setCentralWidget(self.tabWidget)

        self.loginWindow = PhotoOrderLoginWindow(self.dropboxConnection, self)
        self.loginWindow.loggedIn.connect(self.loggedInSlot)

        self.mainWindowStatusBar = QStatusBar()
        self.setStatusBar(self.mainWindowStatusBar)
        self.loggedAsLabel = QLabel(self)
        self.loggedAsLabel.setText('Logged as: ')
        self.databaseConnectionStatus = QLabel(self)
        self.mainWindowStatusBar.addPermanentWidget(self.loggedAsLabel)
        self.mainWindowStatusBar.addPermanentWidget(self.databaseConnectionStatus)

        self.mainWindowMenuBar = MainWindowMenuBar(self)
        self.setMenuBar(self.mainWindowMenuBar)

        dropboxFoldersTab = QWidget()
        dropboxFoldersTabLayout = QHBoxLayout()
        self.folderList = DropboxFolderList()
        self.folderList.itemExpanded.connect(self.expandedItemSlot)
        self.folderList.itemDoubleClicked.connect(self.selectedFolderSlot)
        self.folderProperties = FolderProperties()
        self.folderProperties.addToDBButton.clicked.connect(self.addFolderToDB)
        dropboxFoldersTabLayout.addWidget(self.folderList)
        dropboxFoldersTabLayout.addWidget(self.folderProperties)
        dropboxFoldersTab.setLayout(dropboxFoldersTabLayout)
        self.tabWidget.addTab(dropboxFoldersTab, 'Dropbox folders')

        databaseFoldersTab = QWidget()
        databaseFoldersTabLayout = QVBoxLayout()
        self.folderDropdownMenu = QComboBox()
        self.folderDropdownMenu.currentIndexChanged.connect(self.currentIndexChangedSlot)
        self.shareProperties = ShareOptions()
        self.shareProperties.saveButton.clicked.connect(self.saveShareOptionsSlot)
        self.picturesList = QListWidget()
        databaseFoldersTabLayout.addWidget(self.folderDropdownMenu)
        databaseFoldersTabLayout.addWidget(self.shareProperties)
        databaseFoldersTabLayout.addWidget(self.picturesList)
        databaseFoldersTab.setLayout(databaseFoldersTabLayout)
        self.tabWidget.addTab(databaseFoldersTab, 'Shared folders')

        self.tabWidget.currentChanged.connect(self.tabChangedSlot)

        self.show()

    def login(self):
        self.mainWindowStatusBar.showMessage('Logging in')
        self.mainApp.processEvents()
        try:
            self.dropboxConnection.setConnection(self.config.getAccessToken())
        #if self.config.getAccessToken() != -1:
            self.loggedAsLabel.setText('Logged as: ' + self.dropboxConnection.client.account_info()['email'])
            self.mainWindowStatusBar.clearMessage()
            self.buildFirstRow()
            message = QMessageBox()
            message.setText('Dropbox login successful')
            message.setIcon(QMessageBox.Information)
            message.exec_()
        except:
            self.loginWindow.show()

    def addFolderToDB(self):
        self.mainWindowStatusBar.showMessage('Adding folder to database')
        self.mainApp.setOverrideCursor(Qt.BusyCursor)
        selectedFolder = self.folderList.selectedItems()[0]
        contents = self.dropboxConnection.client.metadata(selectedFolder.path)['contents']
        photos = []
        for item in contents:
            if item['is_dir'] != True:
                photos.append([item['path'], self.dropboxConnection.client.share(item['path'], False)])
        self.databaseConnection.addFolder(selectedFolder, photos)
        self.mainWindowStatusBar.clearMessage()
        self.mainApp.restoreOverrideCursor()

    def buildTree(self, path, parentItem):
        for file in self.dropboxConnection.client.metadata(path)['contents']:
            if file['is_dir'] == True:
                treeWidgetItem = DropboxFolderListItem(file['path'], parentItem)
                self.buildTree(file['path'], treeWidgetItem)
                self.folderList.addTopLevelItem(treeWidgetItem)

    def assignChildren(self, path, parentItem):
        self.mainWindowStatusBar.showMessage('Processing folder tree')
        for file in self.dropboxConnection.client.metadata(path)['contents']:
            if file['is_dir'] == True:
                treeWidgetItem = DropboxFolderListItem(file['path'], parentItem)
                self.folderList.addTopLevelItem(treeWidgetItem)
        self.mainWindowStatusBar.clearMessage()

    def buildFirstRow(self):
        self.mainWindowStatusBar.showMessage('Processing folder tree')
        for file in self.dropboxConnection.client.metadata('/')['contents']:
            if file['is_dir'] == True:
                treeWidgetItem = DropboxFolderListItem(file['path'])
                self.folderList.addTopLevelItem(treeWidgetItem)
        self.mainWindowStatusBar.clearMessage()

    @Slot()
    def updateDBConnectionStatus(self):
        if self.databaseConnection.connection == False:
            self.databaseConnectionStatus.setText('Unable to connect to DB')
        else:
            self.databaseConnectionStatus.setText('Connected to: ' + self.config.getDBName() + '@' + self.config.getDBServer())

    @Slot(int)
    def loggedInSlot(self):
        self.loggedAsLabel.setText('Logged as: ' + self.dropboxConnection.client.account_info()['email'])
        self.mainWindowStatusBar.clearMessage()
        self.buildFirstRow()

    @Slot(DropboxFolderListItem)
    def expandedItemSlot(self, item):
        if item.childCount() == 0:
            self.assignChildren(item.path, item)

    @Slot(DropboxFolderListItem)
    def selectedFolderSlot(self, item):
        contents = self.dropboxConnection.client.metadata(item.path)['contents']
        list = []
        for folderitem in contents:
            if folderitem['is_dir'] == False:
                list.append(folderitem)
        if self.folderList.isItemSelected(item):
            self.folderProperties.selectFolder(item, list)
        else:
            self.folderProperties.deselectFolder()

    @Slot(int)
    def tabChangedSlot(self, tabIndex):
        if tabIndex == 1:
            self.folderDropdownMenu.clear()
            folders = self.databaseConnection.getFolders()
            for folder in folders:
                self.folderDropdownMenu.addItem(folder[2], folder)

    @Slot(int)
    def currentIndexChangedSlot(self, index):
        if index != -1:
            self.picturesList.clear()
            folder = self.folderDropdownMenu.itemData(index)
            self.shareProperties.nameEdit.setText(folder[2])
            self.shareProperties.urlEdit.setText(folder[1])
            if folder[3] == 1:
                status = Qt.Checked
            else:
                status = Qt.Unchecked
            self.shareProperties.optionBox.setCheckState(status)
            pictures = self.databaseConnection.getFolderPictures(self.folderDropdownMenu.currentText())
            for picture in pictures:
                if picture[4] == 0:
                    icon = 'images/nope.png'
                else:
                    icon = 'images/ok.png'
                self.picturesList.addItem(QListWidgetItem(QIcon(icon), picture[2]))

    @Slot()
    def saveShareOptionsSlot(self):
        folder = self.folderDropdownMenu.itemData(self.folderDropdownMenu.currentIndex())
        if self.shareProperties.optionBox.isChecked():
            status = 1
        else:
            status = 0
        self.databaseConnection.saveFolder(
            folder[0],
            self.shareProperties.urlEdit.text(),
            self.shareProperties.nameEdit.text(),
            status
        )
        self.folderDropdownMenu.clear()
        folders = self.databaseConnection.getFolders()
        for folder in folders:
            self.folderDropdownMenu.addItem(folder[2], folder)