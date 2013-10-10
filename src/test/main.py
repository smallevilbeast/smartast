#! /usr/bin/env python
# -*- coding: utf-8 -*-

from _qt import QtCore, QtGui, QtDeclarative
from xdg import get_path


class SmartPanel(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(SmartPanel, self).__init__(parent)
        
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置背景透明， 需要窗口管理器支持
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # 无边框
        self.view = QtDeclarative.QDeclarativeView(self)
        self.view.setSource(QtCore.QUrl.fromLocalFile(get_path("qml", "main.qml")))
        self.view.setStyleSheet("background:transparent");
        self.view.setAttribute(QtCore.Qt.WA_TranslucentBackground);        
        self.view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.view)
        
        self.setLayout(layout)
        
        
if __name__ == "__main__":        
    import sys
    app = QtGui.QApplication(sys.argv)
    win = SmartPanel()
    win.show()
    sys.exit(app.exec_())
    
    
