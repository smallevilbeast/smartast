#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
 
class QRelationalDelegate(QtGui.QStyledItemDelegate):
    VALUES = ['zero', 'one', 'two', 'three', 'four']
 
    def paint(self, painter, option, index):
        value = index.data(QtCore.Qt.DisplayRole).toInt()[0] # integer stored in tablewidget model
        text = self.VALUES[value] # text to be displayed            
        painter.save()
        if option.state & QtGui.QStyle.State_Selected: # highligh background if selected
            painter.fillRect(option.rect, option.palette.highlight())        
        painter.drawText(option.rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, text)
        painter.restore()
 
    def createEditor(self, parent, option, index):
        combobox = QtGui.QComboBox(parent)
        combobox.addItems(self.VALUES)
        combobox.setEditable(True)      
        return combobox
 
    def setEditorData(self, editor, index):
        text = self.VALUES[index.data(QtCore.Qt.DisplayRole).toInt()[0]]
        pos = editor.findText(text)
        if pos == -1:  #text not found, set cell value to first item in VALUES
            pos = 0
        editor.setCurrentIndex(pos)
 
    def setModelData(self, editor, model, index):
        model.setData(index, QtCore.QVariant(editor.currentIndex()))
 
 
class myWindow(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        DATA = [['First row', 1, 1], ['Second Row', 2, 2]]
        self.table = QtGui.QTableWidget(self)
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(DATA))
        self.table.setColumnCount(len(DATA[0]))
        self.table.setItemDelegateForColumn(1, QRelationalDelegate(self))
        for row in range(len(DATA)):
            for col in range(len(DATA[row])):
                item = QtGui.QTableWidgetItem(str(DATA[row][col]))
                self.table.setItem(row, col, item)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)        
 
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = myWindow()
    window.show()
    app.exec_()