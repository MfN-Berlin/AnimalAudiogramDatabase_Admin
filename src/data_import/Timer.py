'''
Created on 25.05.2020
A timer to gather performance information
@author: Alvaro Ortiz for Museum fuer Naturkunde Berlin
'''
import time


class Timer:
    def __init__(self):
        self.start = None
        self.end = None
        self.interval = None

    def __enter__(self):
        self.start = time.process_time()
        return self

    def __exit__(self, *args):
        self.end = time.process_time()
        self.interval = self.end - self.start
