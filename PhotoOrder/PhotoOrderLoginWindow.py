__author__ = 'Sarge'

from PySide.QtGui import *
from PySide.QtCore import *


class PhotoOrderLoginWindow (QWidget):

    loggedIn = Signal(int)

    def __init__(self, dropboxConnection, mainWindow):
        super().__init__()
        #self.loggedIn.connect(mainWindow.loggedInSlot)
        self.dropboxConnection = dropboxConnection
        self.setWindowTitle('Authorize this application')
        self.setFixedSize(500, 150)
        self.authorizeUrlLabel = QLabel(self)
        self.authorizeUrlLabel.setFixedWidth(480)
        self.authorizeUrlLabel.move(10, 20)
        self.authorizeUrlLabel.setText("<a href='" + self.dropboxConnection.authenticate() + "'>" + self.dropboxConnection.authorizeUrl + "</a>")
        self.authorizeUrlLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.authorizeUrlLabel.setOpenExternalLinks(True)
        self.codeLabel = QLabel(self)
        self.codeLabel.setText('Enter code from URL above here:')
        self.codeLabel.move(50, 50)
        self.codeBox = QLineEdit(self)
        self.codeBox.setFixedWidth(400)
        self.codeBox.move(50, 65)
        self.loginButton = QPushButton(self)
        self.loginButton.setFixedSize(80, 40)
        self.loginButton.setText('Authorize')
        self.loginButton.move(110, 95)
        self.loginButton.clicked.connect(self.loginButtonClicked)

    def loginButtonClicked(self):
        self.dropboxConnection.authorize(self.codeBox.text())
        self.loggedIn.emit(1)
        self.hide()
        message = QMessageBox()
        message.setText('Dropbox login successful')
        message.setIcon(QMessageBox.Information)
        message.exec_()