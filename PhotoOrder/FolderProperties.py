__author__ = 'Sarge'

from PySide.QtGui import *


class FolderProperties (QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folder properties')

        layout = QVBoxLayout()

        self.folderLabel = QLabel()
        self.folderLabel.setText('No folder selected')
        layout.addWidget(self.folderLabel)

        self.folderContents = QListWidget()
        layout.addWidget(self.folderContents)

        self.addToDBButton = QPushButton()
        self.addToDBButton.setText('Add to Database')
        layout.addWidget(self.addToDBButton)

        self.setLayout(layout)

    def selectFolder(self, folder, foldercontents):
        self.folderLabel.setText(folder.path)
        self.folderContents.clear()
        for item in foldercontents:
            self.folderContents.addItem(QListWidgetItem(item['path']))

    def deselectFolder(self):
        self.folderLabel.setText('No folder selected')