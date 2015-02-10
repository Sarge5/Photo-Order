__author__ = 'Sarge'

from PySide.QtGui import *


class DropboxFolderListItem (QTreeWidgetItem):

    def __init__(self, path, parent = None):
        super().__init__(parent)
        self.path = path
        text = self.path.split('/').pop()
        self.setText(0, text)
        self.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
