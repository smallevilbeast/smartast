#! /usr/bin/env python
# -*- coding: utf-8 -*-

import threading

class ThreadFetch(threading.Thread):            
    
    def __init__(self, fetch_funcs, success_funcs=None, fail_funcs=None):
        super(ThreadFetch, self).__init__()
        self.setDaemon(True)
        self.fetch_funcs = fetch_funcs
        self.success_funcs = success_funcs
        self.fail_funcs = fail_funcs
        
    def run(self):    
        result = self.fetch_funcs[0](*self.fetch_funcs[1])
        if result:
            if self.success_funcs:
                self.success_funcs[0](result, *self.success_funcs[1])
        else:        
            if self.fail_funcs:
                self.fail_funcs[0](*self.fail_funcs[1])
