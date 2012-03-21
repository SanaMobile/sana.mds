"""
The subject model for the Sana data engine.

:Authors: Sana dev team
:Version: 1.1
"""

from django.db import models
from sana.api.utils import make_uuid

## ?Procedure step. First iteration
class Instruction(models.Model):
    """ The """

    uuid = models.CharField(max_length=36, unique=True, default=make_uuid,)
    """ A universally unique identifier """
    
    concept = models.ForeignKey('Concept')
    ''' Contextual information about the instruction '''
    
    predicate = models.CharField()
    ''' The predicate logic used for this instruction within a decision tree.'''
    
    algorithm = models.CharField()
    ''' The name of an algorithm used to calculate a score for the instruction.'''
    
    compound = models.BooleanField(default=False)
    ''' True if this Instruction has child instructions. '''

    boolean_operator = models.CharField(blank=True)
    ''' The logical operator to apply when evaluating children if compound.'''
    
    
    