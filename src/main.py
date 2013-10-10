#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from _qt import QtCore, QtGui
from ui.suggest import SuggestEdit
from ui.globalkey import GlobalKey
from youdao import YoudaoWidget, get_simple

class SmartPanel(QtGui.QWidget):
    
    global_hotkey  = QtCore.Signal(object)
    
    def __init__(self, parent=None):
        super(SmartPanel, self).__init__(parent)
        
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) 
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) 
        
        self.line_edit = SuggestEdit()
        self.line_edit.textActivated.connect(self.on_lineedit_text_activated)
        self.line_edit.textEdited.connect(self.on_lineedit_text_edited)
        self.setContentsMargins(5, 5, 5, 5)
        
        # hide self when mouse click other widgets .
        QtGui.qApp.focusChanged.connect(self.on_qapp_focus_changed)
        
        # xlib global keybinder.
        self.global_hotkey.connect(self.on_global_hotkey)        
        self.bind_global_key()
        
        self.bottom_widget = YoudaoWidget()
        self.bottom_widget.setVisible(False)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.bottom_widget)
        self.setLayout(layout)
        
        
    def on_lineedit_text_activated(self, text):    
        get_simple(text)
        self.bottom_widget.setVisible(True)
        
    def on_lineedit_text_edited(self, text):    
        if not text.strip():
            if self.bottom_widget.isVisible():
                self.bottom_widget.setVisible(False)
                
                # adjust widget's size again.
                self.adjustSize()
        
    def paintEvent(self, event):    
        cr = QtGui.QPainter(self)
        cr.setRenderHint(QtGui.QPainter.Antialiasing)        
        self.draw_background(cr)
        
    def draw_background(self, cr):    
        padding = 4
        main_rect = self.rect()
        cr.setPen(QtCore.Qt.NoPen)
        cr.setBrush(QtGui.QColor(46,76,114, 153.0))
        cr.drawRoundedRect(main_rect, 6, 6)
        cr.setBrush(QtGui.QColor(255, 255, 255))
        rect = QtCore.QRect(main_rect.x() + padding, main_rect.y() + padding,
                            main_rect.width() - padding * 2, main_rect.height() - padding * 2)
        cr.drawRoundedRect(rect, 6, 6)
        
    def bind_global_key(self):    
        self.global_key = GlobalKey()
        self.global_key.bind("Ctrl + Alt + Z", lambda :self.emit_global_hotkey("toggle_visible"))
        self.global_key.start()
        
    def emit_global_hotkey(self, string):        
        self.global_hotkey.emit(string)
        
    def on_global_hotkey(self, string):    
        func = getattr(self, string, None)
        if func: func()
            
    def toggle_visible(self):    
        if self.isVisible():
            if not self.isActiveWindow():
                self.activateWindow()
            else:    
                self.hide()
        else:        
            self.showNormal()
            self.raise_()
            self.activateWindow()
        
    def on_qapp_focus_changed(self, old, now):    
        if now is None:
            self.hide()
        
if __name__ == "__main__":        
    import sys
    app = QtGui.QApplication(sys.argv)
    win = SmartPanel()
    win.move(200 + 400, 200)
    win.setMinimumSize(400, 0)
    win.show()
    win.line_edit.setFocus()
    sys.exit(app.exec_())

