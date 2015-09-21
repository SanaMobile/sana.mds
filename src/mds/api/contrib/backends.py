'''
Provides access to pluggable backend infrastructucture.

Target backends must be configured in the settings by adding
the desired backend to the value of the TARGET variable.
'''
import logging

__all__ = [
    'AbstractHandler',
    'register_handler',
    'remove_handler',
    'get_handlers',
    'create',
    'read',
    'update',
    'delete',
]
_handlers = {
    'Concept': [],
    'Encounter': [],
    'Location':[],
    'Procedure':[],
    'Observation':[],
    'Observer'[],
    'Subject':[],
}

class AbstractHandler(object)
    def __init__(self, **kwargs):
        pass
    
    def create_model(self):
        pass

    def read_model(self):
        pass

    def update_model(self):
        pass

    def delete_model(self):
        pass

def register_handler(model, target):
    pass

def remove_handler(model, target):
    pass

def get_handlers(model):
    ''' Returns the callable for sending the instance 
        to the target.
    '''
    return _handlers.get(model, [])

def create(model, obj, auth=None, *args, **kwargs):
    ''' Handles the instance creation in the backend and returns a list
        of objects created.
        
        This effectively wraps a POST call to the dispatch server and
        forwards it to the frontend. The first handler registered will
        be used as the primary 
    '''
    handlers = get_handlers(model)
    result = []
    if not handlers:
        logging.warn("No handler defined for %s" % model) 
    for handler in handlers:
        handler_instance = handler(auth=auth)
        caller = handler.getattr('create_model', None)
        if caller:
            if result:
                caller(obj,*args,**kwargs)
            else:
                result = caller(obj,*args,**kwargs)
        else:
            logging.warn("No callable defined.")
    return result

def read(model, obj, auth=None, *args, **kwargs):
    ''' Handles the instance fetch in the backend and returns a list
        of objects created.
        
        This effectively wraps a POST call to the dispatch server and
        forwards it to the frontend. The first handler registered will
        be used as the primary 
    '''
    handlers = get_handlers(model)
    result = []
    if not handlers:
        logging.warn("No handler defined for %s" % model) 
    for handler in handlers:
        handler_instance = handler(auth=auth)
        caller = handler.getattr('read_model', None)
        if caller:
            if result:
                caller(obj,*args,**kwargs)
            else:
                result = caller(obj,*args,**kwargs)
        else:
            logging.warn("No callable defined.")
    return result

def update(model, obj, auth=None, *args, **kwargs):
    ''' Handles the instance fetch in the backend and returns a list
        of objects created.
        
        This effectively wraps a PUT call to the dispatch server and
        forwards it to the frontend. The first handler registered will
        be used as the primary 
    '''
    handlers = get_handlers(model)
    result = []
    if not handlers:
        logging.warn("No handler defined for %s" % model) 
    for handler in handlers:
        handler_instance = handler(auth=auth)
        caller = handler.getattr('update_model', None)
        if caller:
            if result:
                caller(obj,*args,**kwargs)
            else:
                result = caller(obj,*args,**kwargs)
        else:
            logging.warn("No callable defined.")
    return result

def delete(model, obj, auth=None, *args, **kwargs):
    ''' Handles the instance delete in the backend and returns a list
        of objects created.
        
        This effectively wraps a DELETE call to the dispatch server and
        forwards it to the frontend. The first handler registered will
        be used as the primary 
    '''
    handlers = get_handlers(model)
    result = []
    if not handlers:
        logging.warn("No handler defined for %s" % model) 
    for handler in handlers:
        handler_instance = handler(auth=auth)
        caller = handler.getattr('delete_model', None)
        if caller:
            if result:
                caller(obj,*args,**kwargs)
            else:
                result = caller(obj,*args,**kwargs)
        else:
            logging.warn("No callable defined.")
    return result
