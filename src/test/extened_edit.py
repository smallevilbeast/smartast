#! /usr/bin/env python
# -*- coding: utf-8 -*-

from _qt import QtCore, QtGui

class SuggestEdit(QtGui.QLineEdit):
    
    def __init__(self, *args, **kwargs):
        super(SuggestEdit, self).__init__(*args, **kwargs)
        
        self.empty_message = ""
        self.draw_empty_flag = True
        
    def set_empty_message(self, text):    
        self.empty_message = text
        self.draw_empty_flag = False if self.text() else True
        self.update()        
        
    def paintEvent(self, event):    
        super(SuggestEdit, self).paintEvent(event)
        
        if not self.text() and self.draw_empty_flag and self.empty_message:
            cr = QtGui.QPainter(self)
            font = QtGui.QFont()
            font.setItalic(True)
            cr.setFont(font)
            color = QtGui.QColor(self.palette().color(self.foregroundRole()))
            color.setAlphaF(0.5)
            cr.setPen(color)
            style_option = QtGui.QStyleOptionFrame()
            self.initStyleOption(style_option)
            rect = self.style().subElementRect(QtGui.QStyle.SE_LineEditContents, 
                                               style_option, self)
            rect.setLeft(rect.left() + 2)
            rect.setRight(rect.right() - 2)
            cr.drawText(rect, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter, self.empty_message)
            
    def focusInEvent(self, event):        
        if self.draw_empty_flag:
            self.draw_empty_flag = False
            self.update()
        super(SuggestEdit, self).focusInEvent(event)
            
    def focusOutEvent(self, event):        
        if not self.draw_empty_flag:
            self.draw_empty_flag = True
            self.update()
        super(SuggestEdit, self).focusOutEvent(event)
