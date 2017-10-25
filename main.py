__author__      = "Rosa Quelal"
__version__ = "0.1"

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mainwindow import MainWindow


if __name__ == '__main__':

    # create application
    app = QApplication(sys.argv)
    app.setApplicationName('Vision Termica')

    # create widget
    w = MainWindow()
    w.setWindowTitle('Vision Termica')
    w.show()

    # connection
    app.lastWindowClosed.connect(app.quit)##PyQt5
    #QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))###PyQt4

    # execute application
    sys.exit(app.exec_())
