from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        widget = QtGui.QWidget(self)
        layout = QtGui.QVBoxLayout(widget)
        self.edit = QtGui.QLineEdit(self)
        self.list = QtGui.QListWidget(self)
        layout.addWidget(self.edit)
        layout.addWidget(self.list)
        self.setCentralWidget(widget)
        self.setMouseTracking(True)
        self.grabMouse()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            if event.buttons() == QtCore.Qt.NoButton:
                pos = event.pos()
                self.edit.setText('x: %d, y: %d' % (pos.x(), pos.y()))
            else:
                pass # do other stuff
        print event    
        return QtGui.QMainWindow.eventFilter(self, source, event)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    win = Window()
    win.show()
    # win.grabMouse()
    app.installEventFilter(win)
    win.installEventFilter(win)
    sys.exit(app.exec_())
