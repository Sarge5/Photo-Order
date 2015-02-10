__author__ = 'Sarge'

from PySide.QtCore import *
from PySide.QtGui import *


class DatabaseOptionsWindow (QDialog):



    def __init__(self, parentWindow):
        super().__init__()
        self.config = parentWindow.config
        self.databaseConnection = parentWindow.databaseConnection
        self.setWindowTitle('Database options')
        self.setModal(True)
        self.setFixedSize(350, 275)
        layout = QVBoxLayout()
        layout.setSpacing(0)

        self.dbServerLabel = QLabel()
        self.dbServerLabel.setText('Server address')
        layout.addWidget(self.dbServerLabel)

        self.dbServerEdit = QLineEdit()
        self.dbServerEdit.setText(self.config.getDBServer())
        layout.addWidget(self.dbServerEdit)

        layout.addSpacing(15)

        self.dbPortLabel = QLabel()
        self.dbPortLabel.setText('Server port')
        layout.addWidget(self.dbPortLabel)

        self.dbPortEdit = QLineEdit()
        self.dbPortEdit.setText(self.config.getDBPort())
        layout.addWidget(self.dbPortEdit)

        layout.addSpacing(15)

        self.dbNameLabel = QLabel()
        self.dbNameLabel.setText('Database name')
        layout.addWidget(self.dbNameLabel)

        self.dbNameEdit = QLineEdit()
        self.dbNameEdit.setText(self.config.getDBName())
        layout.addWidget(self.dbNameEdit)

        layout.addSpacing(15)

        self.dbUserLabel = QLabel()
        self.dbUserLabel.setText('Database username')
        layout.addWidget(self.dbUserLabel)

        self.dbUserEdit = QLineEdit()
        self.dbUserEdit.setText(self.config.getDBUser())
        layout.addWidget(self.dbUserEdit)

        layout.addSpacing(15)

        self.dbPassLabel = QLabel()
        self.dbPassLabel.setText('Database password')
        layout.addWidget(self.dbPassLabel)

        self.dbPassEdit = QLineEdit()
        self.dbPassEdit.setText(self.config.getDBPass())
        layout.addWidget(self.dbPassEdit)

        layout.addSpacing(15)

        self.saveButton = QPushButton()
        self.saveButton.setText('Save')
        self.saveButton.clicked.connect(self.saveOptions)
        layout.addWidget(self.saveButton)

        self.setLayout(layout)
        self.show()

    @Slot()
    def saveOptions(self):
        self.config.setDBServer(self.dbServerEdit.text())
        self.config.setDBPort(self.dbPortEdit.text())
        self.config.setDBName(self.dbNameEdit.text())
        self.config.setDBUser(self.dbUserEdit.text())
        self.config.setDBPass(self.dbPassEdit.text())
        self.config.writeConfig()
        self.databaseConnection.reconnect()
        if self.databaseConnection.connection:
            if self.databaseConnection.checkTableExists() == 0:
                self.databaseConnection.createTables()