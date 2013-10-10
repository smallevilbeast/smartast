#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
from netlib import public_curl
from xmltodict import parse as xml_parse
from ui.utils import AutoQObject
from _qt import QtDeclarative, QtCore
import traceback

SimpleInfo = AutoQObject(("keyword", str),
                         ("ukphone", str),
                         ("usphone", str),
                         ("webtrans", str),                         
                         ("trans", str),
                         ("weba", str),
                         name="SimpleInfo")


simpleinfo = SimpleInfo()


def get_suggest(text):
    data = { "type" : "DESKDICT", "num" : 10, "ver" : 2.0, "le": "eng", "q" : text }
    ret = public_curl.request("http://dict.youdao.com/suggest", data)
    doc =  xml_parse(ret)
    try:
        return doc['suggest']['items']['item']
    except:
        return None
    
    
def get_simple(text):    
    data = { "keyfrom" : "deskdict.mini", "q" : text, "doctype" : "xml", "xmlVersion" : 8.2,
             "client" : "deskdict", "id" : "cee84504d9984f1b2", "vendor": "unknown", 
             "in" : "YoudaoDict", "appVer" : "5.4.46.5554", "appZengqiang" : 0, "le" : "eng", "LTH" : 40}
    ret = public_curl.request("http://dict.youdao.com/search", data)
    ret = xml_parse(ret)
    
    yodaodict = ret['yodaodict']
    simpleinfo.keyword = text    
    
    try:
        word = yodaodict['basic']['simple-dict']['word']
    except Exception: 
        traceback.print_exc(file=sys.stdout)
        simpleinfo.ukphone = None
        simpleinfo.usphone = None
        simpleinfo.trans = None
    else:    
        ukphone = word.get("ukphone", None)
        if ukphone:
            simpleinfo.ukphone = "英[%s]" % ukphone
        else:    
            simpleinfo.ukphone = None
            
        usphone = word.get("usphone", None)
        if usphone:
            simpleinfo.usphone = "美[%s]" % usphone
        else:    
            simpleinfo.usphone = None
            
        trs = word["trs"]["tr"]
        if isinstance(trs, list):
            ret = "<br>".join(item['l']['i'] for item in trs)
        else:    
            ret = trs['l']['i']
        simpleinfo.trans = ret            
    
    ret = yodaodict['yodao-web-dict']['web-translation']
    
    if isinstance(ret, list):
        ret = ret[0]
    
    trans = ret['trans']
    if isinstance(trans, list):
        web_trans = "|".join(item["value"] for item in trans)
    else:    
        web_trans = trans['value']
    simpleinfo.webtrans = web_trans
    
root_dir = os.path.dirname(os.path.realpath(__file__))    
    
class YoudaoWidget(QtDeclarative.QDeclarativeView):    
    
    def __init__(self, parent=None):
        super(YoudaoWidget, self).__init__(parent)
        
        self.rootContext().setContextProperty("simpleinfo", simpleinfo)        
        self.setSource(QtCore.QUrl.fromLocalFile(os.path.join(root_dir, "main.qml")))
        self.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.setStyleSheet("background:transparent");
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground);        
        self.setMinimumSize(0, 200)
