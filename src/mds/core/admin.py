"""Sana mDS Django admin interface

:Authors: Sana dev team
:Version: 2.0
"""

from django.contrib import admin
from django.contrib.admin import widgets
from .models import * 

class CoreAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        kwargs['widget']= widgets.FilteredSelectMultiple(
            db_field.verbose_name,
            db_field.name in self.filter_vertical
        )

        return super(admin.ModelAdmin, self).formfield_for_manytomany(
            db_field, request=request, **kwargs)

def mark_voided(modeladmin,request,queryset):
    queryset.update(voided=True)
mark_voided.short_description = "Mark selected voided"

class DeviceAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid']  
    list_display = ['name', 'uuid']
    list_filter = ['name',]
    actions=[mark_voided,]

class ProcedureAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid']
    list_display = ['title', 'author', 'uuid']
    actions=[mark_voided,]

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
    list_filter = ['name',]
    actions=[mark_voided,]

class ObservationAdmin(admin.ModelAdmin):
    exclude = ('_complex_progress',)
    readonly_fields = ['_complex_size','uuid','value']
    list_display = ['question','voided','concept','value', 
        'subject','device','created','modified', 'encounter', 'upload_progress']
    #list_filter = ['node','concept', 'modified', 'encounter']
    ordering = ['-modified',]
    actions=[mark_voided,]

class EncounterAdmin(admin.ModelAdmin):
    #exclude = ['concept',]
    list_display = ['subject','voided','concept', 'procedure', 'created',"observer", 'location','uploaded','modified','uuid']
    #actions = [mark_encounter_voided,]
    actions=[mark_voided,]
    ordering = ['-modified',]
    readonly_fields = ['uuid',]

class EncounterInline(admin.StackedInline):
    model = Encounter

class ObserverAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid',]
    list_display = ['user', 'uuid']
    actions=[mark_voided,]


class SubjectAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid',]
    list_display = ['given_name', 'family_name', 'uuid', "image"]

class SubjectInline(admin.StackedInline):
    model = Subject

class LocationAdmin(admin.ModelAdmin):
    model = Location
    list_display = ('name','uuid','code')
    list_filter = ('name',)
    
class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ['level', 'name', 'client', 'path']
    ordering = ['-created', ]

admin.site.register(Concept, ConceptAdmin)
#admin.site.register(Relationship)
#admin.site.register(RelationshipCategory)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Encounter, EncounterAdmin)
admin.site.register(Observation,ObservationAdmin)
admin.site.register(Location,LocationAdmin)
#admin.site.register(Notification)
admin.site.register(Observer,ObserverAdmin)
admin.site.register(Procedure,ProcedureAdmin)
#admin.site.register(Subject,SubjectAdmin)
admin.site.register(Event, EventAdmin)

#extension models
class ANMAdmin(CoreAdmin):
    model = ANM
admin.site.register(ANM, ANMAdmin)
class PatientAdmin(admin.ModelAdmin):
    model = Patient
    list_display = ['system_id', 'given_name', 'family_name', 'dob']
admin.site.register(Patient, PatientAdmin)

#admin.site.register(ClientEventLog, ClientEventLogAdmin)
