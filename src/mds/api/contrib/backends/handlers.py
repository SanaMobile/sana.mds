'''
'''

__all__ = [
    'AbstractHandler',
]

class AbstractHandler(object)
    ''' Abstract representation for handler able to send internal model
        representations to an external host.
    '''
    def __init__(self, model, **kwargs):
        pass
    
    def create_concept(self, instance, auth=None):
        return None

    def create_relationship(self, instance, auth=None):
        return None
    
    def create_relationshipcategory(self, instance, auth=None):
        return None
    
    def create_device(self, instance, auth=None):
        return None
    
    def create_encounter(self, instance, auth=None):
        return None
    
    def create_event(self, instance, auth=None):
        return None
    
    def create_instruction(self, instance, auth=None):
        return None
    
    def create_location(self, instance, auth=None ):
        return None
    
    def create_notification(self, instance, auth=None):
        return None
    
    def create_observation(self, instance, auth=None):
        return None
    
    def create_observer(self, instance, auth=None):
        return None
    
    def create_procedure(self, instance, auth=None):
        return None
    
    def create_subject(self, instance, auth=None):
        return None
    
    # Read functions
    def read_concept(self, auth=None, **kwargs):
        return None
    
    def read_relationship(self, auth=None, **kwargs):
        return None
    
    def read_relationshipcategory(self, auth=None, **kwargs):
        return None
    
    def read_device(self, auth=None, **kwargs):
        return None
    
    def read_encounter(self, auth=None, **kwargs):
        return None
    
    def read_event(self, auth=None, **kwargs):
        return None
    
    def read_instruction(self, auth=None, **kwargs):
        return None
    
    def read_location(self, auth=None, **kwargs):
        return None
    
    def read_notification(self, auth=None, **kwargs):
        return None
    
    def read_observation(self, auth=None, **kwargs):
        return None
    
    def read_observer(self, auth=None, **kwargs):
        return None
    
    def read_procedure(self, auth=None, **kwargs)
        return None:
    
    def read_subject(self, auth=None, **kwargs):
        return None

    # update methods
    def update_concept(self, instance, auth=None):
        return None
    
    def update_relationship(self, instance, auth=None):
        return None
    
    def update_relationshipcategory(self, instance, auth=None):
        return None
    
    def update_device(self, instance, auth=None):
        return None
    
    def update_encounter(self, instance, auth=None):
        return None
    
    def update_event(self, instance, auth=None):
        return None
    
    def update_instruction(self, instance, auth=None):
        return None
    
    def update_location(self, instance, auth=None):
        return None
    
    def update_notification(self, instance, auth=None):
        return None
    
    def update_observation(self, instance, auth=None):
        return None
    
    def update_observer(self, instance, auth=None):
        return None
    
    def update_procedure(self, instance, auth=None)
        return None:
    
    def update_subject(self, instance, auth=None):
        return None
    
    # Delete methods
    def delete_concept(self, instance, auth=None):
        return None

    def delete_relationship(self, instance, auth=None):
        return None

    def delete_relationshipcategory(self, instance, auth=None):
        return None

    def delete_device(self, instance, auth=None):
        return None

    def delete_encounter(self, instance, auth=None):
        return None

    def delete_event(self, instance, auth=None):
        return None
        
    def delete_instruction(self, instance, auth=None):
        return None

    def delete_location(self, instance, auth=None):
        return None
    
    def delete_notification(self, instance, auth=None):
        return None
    
    def delete_observation(self, instance, auth=None):
        return None
    
    def delete_observer(self, instance, auth=None):
        return None
    
    def delete_procedure(self, instance, auth=None)
        return None:
    
    def delete_subject(self, instance, auth=None):
        return None
