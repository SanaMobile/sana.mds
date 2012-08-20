'''
Created on Feb 29, 2012


:Authors: Sana Dev Team
:Version: 1.2
'''
import logging
import os
import mimetypes
import uuid, random

from django.conf import settings

def make_uuid():
    """ A utility to generate universally unique ids.
    """
    return str(uuid.uuid4())

def guess_fext(mtype):
    """ A wrapper around mimetypes.guess_extension(type,True) with additional 
        types included from settings
        Parameters:
        mtype
            the file mime type
    """
    _tmp = mimetypes.guess_extension(type)
    return settings.CONTENT_TYPES.get(type,None) if not _tmp else _tmp

def key_generator(self):
    """ Generates a new secret key """
    return "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])

import sys,traceback
def printstack(e):
    """ Prints stack trace to console."""
    et, val, tb = sys.exc_info()
    trace = traceback.format_tb(tb)
    print 'Error: ', e
    print 'Value: ', val
    for tbm in trace:
        print tbm

def logstack(handler, e):
    logger = getattr(handler,'logger',logging)
    et, val, tb = sys.exc_info()
    trace = traceback.format_tb(tb)
    for tbm in trace:
        logger.error(tbm)

def dictzip(keys,values):
    """ zips to lists into a dictionary """
    #if not keys or not values:
    #    raise Exception("Bad params")
    #if len(keys) != len(values):
    #    raise
    d = {}
    for x in list(zip(keys,values)):
        d[x[0]] = x[1]
    return d

def split(fin, path, chunksize=102400):
    """ Splits a file into a number of smaller chunks """
    print (fin, path, chunksize)
    if not os.path.exists(path):
        os.mkdir(path)
    partnum = 0
    input = open(fin, "rb")
    while True:
        chunk = input.read(chunksize)
        if not chunk: 
            break
        partnum += 1
        outfile = os.path.join(path,('chunk%s' % partnum))
        fobj = open(outfile, 'wb')
        fobj.write(chunk)
        fobj.close()
    input.close()
    return partnum
    