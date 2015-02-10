__author__ = 'Sarge'

from PySide.QtGui import *


class DropboxFolderList (QTreeWidget):

    def __init__(self):
        super().__init__()
        self.setColumnCount(1)
        self.setHeaderLabels(['Folder name'])
        self.setStyleSheet('''
            QTreeWidget::item:selected {
                border-color:black;
                border-style:outset;
                border-width:1px;
                color:black;
            }
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {
                 border-image: none;
                 image: url(images/branch-closed.png);
            }
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings  {
                 border-image: none;
                 image: url(images/branch-open.png);
            }
            ''')
