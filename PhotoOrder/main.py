__author__ = 'Sarge'

from PySide.QtGui import *

from PhotoOrderMainWindow import *
from PhotoOrderLoginWindow import *
from Config import *
from DatabaseConnection import *
from DropboxConnection import *


app = QApplication(sys.argv)
app.setOverrideCursor(Qt.BusyCursor)

config = Config()
dropboxConnection = DropboxConnection(config)
databaseConnection = DatabaseConnection(config)
mainWindow = PhotoOrderMainWindow(dropboxConnection, app, config, databaseConnection)
mainWindow.updateDBConnectionStatus()
app.processEvents()
mainWindow.login()
if databaseConnection.connection:
    if databaseConnection.checkTableExists() == 0:
        databaseConnection.createTables()

app.restoreOverrideCursor()
app.exec_()