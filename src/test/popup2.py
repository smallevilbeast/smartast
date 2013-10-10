#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore

app = QtGui.QApplication(sys.argv)

w = QtGui.QComboBox()
w.setEditable(True)
c = QtGui.QCompleter(['Hello', 'World'])
c.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
c.popup().setStyleSheet("background-color: yellow")
w.setCompleter(c)
w.show()

sys.exit(app.exec_())