#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from _qt import QtCore, QtGui
from utils import AutoQObject

SuggestWrapper = AutoQObject(("word", str),
                             ("desc", str),
                             name="SuggestWrapper")

class SuggestModel(QtCore.QAbstractListModel):
    WordRole = QtCore.Qt.UserRole + 1
    DescRole = QtCore.Qt.UserRole + 2
    
    def __init__(self, data=None, parent=None):
        super(SuggestModel, self).__init__(parent)
                
        self._data = data if data else []
        
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
    
class SuggestEdit(QtGui.QLineEdit):
    
    def __init__(self, *args, **kwargs):
        super(SuggestEdit, self).__init__(*args, **kwargs)
        
        self.suggest_model = SuggestModel([SuggestWrapper(word="linuxdeepin", desc="最好的linux发行版")])
        # wordList = ["alpha", "omega", "omicron", "zeta"]        
        self._completer = QtGui.QCompleter(self.suggest_model, self)
        # self._completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        # self._completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self._completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setCompleter(self._completer)
        self.textChanged.connect(self.on_text_changed)
        
    def on_text_changed(self, text):    
        print "linux"
        # self._completer.popup().show()
        self._completer.complete(self.rect())
        pass
        # self._completer.resetModel()
                # pass
        # self.suggest_model.reset()
        # print "ac"
        # self._completer.popup()
        # self._completer.complete()

    
