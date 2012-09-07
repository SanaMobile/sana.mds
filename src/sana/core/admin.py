"""Sana mDS Django admin interface

:Authors: Sana dev team
:Version: 2.0
"""

from django.contrib import admin
from sana.core.models import * 

class ProcedureAdmin(admin.ModelAdmin):
    pass

class ClientEventLogAdmin(admin.ModelAdmin):
    list_display = ('client', 'event_time', 'event_type', 'event_value', 'encounter_reference', 'patient_reference', 'user_reference',)
    list_filter = ('event_time', 'event_type', 'encounter_reference', 'patient_reference', 'user_reference',)
    date_hierarchy = 'event_time'
    exclude = ('created', 'modified',)

class RestAdmin(admin.TabularInline):
    app_label="REST Services"
    inlines = []

class RelationshipAdmin(admin.TabularInline):
    model = Relationship
    fk_name = 'to_concept'
    list_display_links = []
    
    
class ConceptAdmin(admin.ModelAdmin):
    inlines = [ 
        RelationshipAdmin,
        ]
    readonly_fields = ['uuid']  
    list_display = ['name', 'uuid']
    
class ObservationAdmin(admin.StackedInline):
    model = Observation

class EncounterAdmin(admin.ModelAdmin):
    inlines = [ 
        ObservationAdmin,
        ]  

admin.site.register(Concept)
admin.site.register(Relationship)
admin.site.register(RelationshipCategory)
admin.site.register(Device)
admin.site.register(Encounter)
admin.site.register(Notification)
admin.site.register(Observation)
admin.site.register(Observer)
admin.site.register(Procedure)
admin.site.register(Subject)
admin.site.register(Event)

#admin.site.register(ClientEventLog, ClientEventLogAdmin)
