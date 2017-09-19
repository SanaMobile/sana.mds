# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CrashReport.message'
        db.add_column(u'clients_crashreport', 'message',
                      self.gf('django.db.models.fields.CharField')(default='None', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CrashReport.message'
        db.delete_column(u'clients_crashreport', 'message')


    models = {
        u'clients.client': {
            'Meta': {'object_name': 'Client'},
            'app': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version_code': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'clients.crashreport': {
            'Meta': {'object_name': 'CrashReport'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '255', 'blank': 'True'}),
            'report': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['clients']