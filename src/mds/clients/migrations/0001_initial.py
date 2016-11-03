# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table(u'clients_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('version_code', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('app', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'clients', ['Client'])

        # Adding model 'CrashReport'
        db.create_table(u'clients_crashreport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('device', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'clients', ['CrashReport'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'clients_client')

        # Deleting model 'CrashReport'
        db.delete_table(u'clients_crashreport')


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
            'device': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['clients']