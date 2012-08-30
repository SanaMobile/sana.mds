'''
Created on Aug 11, 2012

:author: Sana Development Team
:version: 2.0
'''
from django.dispatch import Signal

class EventSignal(Signal):
    def __init__(self):
        Signal.__init__(self, providing_args=['event'])

class CacheSignal(Signal):
    def __init__(self):
        Signal.__init__(self, providing_args=['uri','request'])

class FileCacheSignal(Signal):
    def __init__(self):
        Signal.__init__(self, providing_args=['uri','request'])

