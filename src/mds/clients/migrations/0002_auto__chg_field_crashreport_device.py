# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CrashReport.device'
        db.alter_column(u'clients_crashreport', 'device', self.gf('django.db.models.fields.CharField')(max_length=36))

    def backwards(self, orm):

        # Changing field 'CrashReport.device'
        db.alter_column(u'clients_crashreport', 'device', self.gf('django.db.models.fields.CharField')(max_length=10))

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
            'report': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['clients']