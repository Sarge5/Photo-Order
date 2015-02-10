__author__ = 'Sarge'

from DatabaseOptionsWindow import *


class MainWindowMenuBar (QMenuBar):

    def __init__(self, parentWindow):
        super().__init__(parentWindow)
        self.parentWindow = parentWindow
        self.optionsMenu = QMenu()
        self.optionsMenu.setTitle('Options')
        self.dbOptionsAction = self.optionsMenu.addAction('DB Options')
        self.dbOptionsAction.triggered.connect(self.dbOptionsActionTrigger)
        self.addMenu(self.optionsMenu)

    @Slot()
    def dbOptionsActionTrigger(self):
        self.dbOptionsWindow = DatabaseOptionsWindow(self.parentWindow)