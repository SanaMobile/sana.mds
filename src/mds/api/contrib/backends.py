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
    'RelationShip': [],
    'RelationshipCategory':[],
    'Device': [],
    'Encounter': [],
    'Event': [],
    'Instruction': [],
    'Location':[],
    'Notification': [],
    'Procedure':[],
    'Observation':[],
    'Observer'[],
    'Procedure': [],
    'Subject':[],
}

class AbstractHandler(object)
    def __init__(self, model, **kwargs):
        pass
    
    def create_concept(self):
        return None

    def create_relationship(self):
        return None
    
    def create_relationshipcategory(self):
        return None
    
    def create_device(self):
        return None
    
    def create_encounter(self):
        return None
    
    def create_event(self):
        return None
    
    def create_instruction(self):
        return None
    
    def create_location(self):
        return None
    
    def create_notification(self):
        return None
    
    def create_observation(self):
        return None
    
    def create_observer(self):
        return None
    
    def create_procedure(self):
        return None
    
    def create_subject(self):
        return None
    
    # Read functions
    def read_concept(self):
        return None
    
    def read_relationship(self):
        return None
    
    def read_relationshipcategory(self):
        return None
    
    def read_device(self):
        return None
    
    def read_encounter(self):
        return None
    
    def read_event(self):
        return None
    
    def read_instruction(self):
        return None
    
    def read_location(self):
        return None
    
    def read_notification(self):
        return None
    
    def read_observation(self):
        return None
    
    def read_observer(self):
        return None
    
    def read_procedure(self)
        return None:
    
    def read_subject(self):
        return None

    # update methods
    def update_concept(self):
        return None
    
    def update_relationship(self):
        return None
    
    def update_relationshipcategory(self):
        return None
    
    def update_device(self):
        return None
    
    def update_encounter(self):
        return None
    
    def update_event(self):
        return None
    
    def update_instruction(self):
        return None
    
    def update_location(self):
        return None
    
    def update_notification(self):
        return None
    
    def update_observation(self):
        return None
    
    def update_observer(self):
        return None
    
    def update_procedure(self)
        return None:
    
    def update_subject(self):
        return None
    
    # Delete methods
    def delete_concept(self):
        return None
    
    def delete_relationship(self):
        return None
    
    def delete_relationshipcategory(self):
        return None
    
    def delete_device(self):
        return None
    
    def delete_encounter(self):
        return None
    
    def delete_event(self):
        return None
    
    def delete_instruction(self):
        return None
    
    def delete_location(self):
        return None
    
    def delete_notification(self):
        return None
    
    def delete_observation(self):
        return None
    
    def delete_observer(self):
        return None
    
    def delete_procedure(self)
        return None:
    
    def delete_subject(self):
        return None
    


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
        caller = handler.getattr('create_%s' % model.lower(), None)
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
        caller = handler.getattr('read_%s' % model.lower(), None)
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
        caller = handler.getattr('update_%s' % model.lower(), None)
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
        caller = handler.getattr('delete_%s' % model.lower(), None)
        if caller:
            if result:
                caller(obj,*args,**kwargs)
            else:
                result = caller(obj,*args,**kwargs)
        else:
            logging.warn("No callable defined.")
    return result
