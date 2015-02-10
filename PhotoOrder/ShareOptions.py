__author__ = 'Sarge'

from PySide.QtGui import *


class ShareOptions (QWidget):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        self.nameLabel = QLabel()
        self.nameLabel.setText('Name')
        layout.addWidget(self.nameLabel)
        self.nameEdit = QLineEdit()
        layout.addWidget(self.nameEdit)
        layout.addSpacing(50)

        self.urlLabel = QLabel()
        self.urlLabel.setText('Url')
        layout.addWidget(self.urlLabel)
        self.urlEdit = QLineEdit()
        layout.addWidget(self.urlEdit)
        layout.addSpacing(50)

        self.optionBox = QCheckBox()
        self.optionBox.setText('Active')
        layout.addWidget(self.optionBox)
        layout.addSpacing(50)

        self.saveButton = QPushButton()
        self.saveButton.setText('Save changes')
        layout.addWidget(self.saveButton)
        layout.addSpacing(50)

        self.setLayout(layout)