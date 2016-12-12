#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys

from PySide.QtGui import QMainWindow, QPushButton, QApplication, QIcon

from plusrandr_core import PlusRandR
from plusrandr.utils import resource_filepath

# Use generic name
# TODO: Acquire from .desktop file definition
APP_NAME = "Projecteur"


class PlusRandRGui(QMainWindow):

    def __init__(self):
        super(PlusRandRGui, self).__init__()
        self.setWindowIcon(QIcon(resource_filepath("plusrandr_icon.svg")))

        self._button_mirror = QPushButton(u"Miroir",self)
        self._button_refresh = QPushButton(u"Rafraîchir",self)
        self._button_switch1 = QPushButton(u"Écran 1", self)
        self._button_switch2 = QPushButton(u"Écran 2", self)
        self._simpledR = PlusRandR()
        self._nb_screens = 1
        self._init_ui()
        self.refresh()

    def refresh(self):
        """ Refresh xrandr value and update gui relatively to screen count"""
        self._simpledR.refresh_xrandr()
        self._nb_screens = self._simpledR.get_nb_outputs()
        if self._nb_screens == 2:
            self._button_switch1.setEnabled(True)
            self._button_switch2.setEnabled(True)
            self._button_mirror.setEnabled(True)
            self.statusBar().showMessage(u'Veuillez choisir une option')
        else:
            self._button_switch1.setEnabled(False)
            self._button_switch2.setEnabled(False)
            self._button_mirror.setEnabled(False)
            self.statusBar().showMessage(u'Veuillez connecter un second écran et rafraîchir')

    def mirror(self):
        """ calls screen mirroring"""
        self._simpledR.mirror_screens()

    def set_screen1(self):
        """ sets screen 1 active only"""
        self._simpledR.set_single_screen(0)

    def set_screen2(self):
        """ sets screen 2 active only"""
        self._simpledR.set_single_screen(1)

    def _init_ui(self):
        """ Create gui with 5 buttons"""
        self.setGeometry(300, 300, 400, 120)
        self.setFixedSize(400,120)
        self.setWindowTitle(APP_NAME)

        self._button_refresh.setGeometry(0, 0, 100, 100)
        self._button_mirror.setGeometry(100, 0, 100, 100)
        self._button_switch1.setGeometry(200, 0, 100, 100)
        self._button_switch2.setGeometry(300, 0, 100, 100)

        self._button_mirror.clicked.connect(self.mirror)
        self._button_refresh.clicked.connect(self.refresh)
        self._button_switch1.clicked.connect(self.set_screen1)
        self._button_switch2.clicked.connect(self.set_screen2)

if __name__ == '__main__':
    app = QApplication([APP_NAME])
    gui = PlusRandRGui()
    gui.show()
    sys.exit(app.exec_())
