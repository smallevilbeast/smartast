#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import copy

import common

from _qt import QtCore, QtGui
from ui.utils import AutoQObject
from youdao import get_suggest

SuggestWrapper = AutoQObject(("word", str),
                             ("desc", str),
                             name="SuggestWrapper")

class SuggestCompleter(QtGui.QCompleter):
    
    def pathFromIndex(self, index):
        return index.data(SuggestModel.WordRole)
    
class SuggestDelegate(QtGui.QStyledItemDelegate):
    
    def paint(self, painter, option, index):
        word = index.data(SuggestModel.WordRole)
        desc = index.data(SuggestModel.DescRole)

        if option.state & QtGui.QStyle.State_Selected: # highligh background if selected
            painter.fillRect(option.rect, option.palette.highlight())           
        elif option.state & QtGui.QStyle.State_MouseOver:    
            painter.fillRect(option.rect, option.palette.highlight())           
            
        # painter.drawText(option.rect, QtCore.Qt.AlignCenter, "<b>%s</b><br><i>%s</i>" % (word, desc))  
        
        doc = QtGui.QTextDocument(self)
        doc.setHtml("<b>%s</b><br><i>%s</i>" % (word, desc))
        doc.setTextWidth(option.rect.width())
        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
        
        painter.save()
        painter.translate(option.rect.topLeft());
        painter.setClipRect(option.rect.translated(-option.rect.topLeft()))
        dl = doc.documentLayout()
        dl.draw(painter, ctx)
        painter.restore()        
        
    def sizeHint(self, option, index):
        size = super(SuggestDelegate, self).sizeHint(option, index)
        size.setHeight(size.height() * 2)
        return size

class SuggestModel(QtCore.QAbstractListModel):
    WordRole = QtCore.Qt.UserRole + 1
    DescRole = QtCore.Qt.UserRole + 2
    
    suggested = QtCore.Signal(int, object)
    
    def __init__(self, data=None, parent=None):
        super(SuggestModel, self).__init__(parent)
                
        self._data = data if data else []
        self.suggest_thread_id = 0
        self.suggested.connect(self.on_suggested_data)
                
        keys = dict()
        keys[SuggestModel.WordRole] = "word"
        keys[SuggestModel.DescRole] = "desc"
        self.setRoleNames(keys)
        
    def rowCount(self, index):    
        return len(self._data)
    
    def data(self, index, role):
        if not index.isValid() or index.row() > len(self._data):
            return None
        
        item = self._data[index.row()]
        if role == SuggestModel.WordRole:
            return item.word
        elif role == SuggestModel.DescRole:
            return item.desc
        elif role == QtCore.Qt.DisplayRole:
            return item.word
        return None
    
    def clear(self):
        self.set_data([])
    
    def set_data(self, data):
        del self._data
        self._data = data
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        
    def suggest(self, text):    
        self.async_suggest(get_suggest, text)
            
    def parse_suggested(self, data):        
        if data is not None:
            try:
                ret = [ SuggestWrapper(word=item["title"], desc=item["explain"]) for item in data ]
                self.set_data(ret)
            except: pass    
            
    def emit_suggest_result(self, data, thread_id):        
        if thread_id == self.suggest_thread_id:
            self.suggested.emit(thread_id, data)
            
    def on_suggested_data(self, thread_id, data):        
        if thread_id == self.suggest_thread_id:
            self.parse_suggested(data)
            
    def async_suggest(self, suggest_func, text):        
        self.suggest_thread_id += 1        
        thread_id = copy.deepcopy(self.suggest_thread_id)
        common.ThreadFetch(
            fetch_funcs=(suggest_func, (text,)),
            success_funcs=(self.emit_suggest_result, (thread_id,))).start()
    
class SuggestEdit(QtGui.QLineEdit):
    
    textActivated = QtCore.Signal(str)
    
    def __init__(self, *args, **kwargs):
        super(SuggestEdit, self).__init__(*args, **kwargs)
        self.suggest_model = SuggestModel()
        self.suggest_delegate = SuggestDelegate()
        self._completer = SuggestCompleter(self.suggest_model, self)
        self._completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        self._completer.popup().setItemDelegate(self.suggest_delegate)
        self.setCompleter(self._completer)
        self.textEdited.connect(self.on_text_edited)
        self.returnPressed.connect(self.on_return_pressed)
        self._completer.activated.connect(self.on_completer_activated)
        self.setStyleSheet('''QLineEdit {
                                         border: 1px solid #C9C9C9;
                                         border-radius: 0px;
                                         padding: 0px 5px;
                                         background: #F9F9F9;
                                         selection-background-color: darkgray;
                              }'''
                           )
        
    def on_text_edited(self, text):    
        if text.strip():
            self.suggest_model.suggest(text.encode("utf-8"))
        else:    
            self.suggest_model.clear()
            
    def on_completer_activated(self, text):    
        if text.strip():
            self.textActivated.emit(text.encode("utf-8"))        
        
    def on_return_pressed(self):    
        text = self.text()
        if text.strip():
            self.textActivated.emit(self.text())
        
    def sizeHint(self):    
        return QtCore.QSize(0, 38)
