# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Concept'
        db.create_table(u'core_concept', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='5b0ea205-8b15-4c2b-897d-44484c2b6df7', unique=True, max_length=36)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('conceptclass', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('datatype', self.gf('django.db.models.fields.CharField')(default='string', max_length=64)),
            ('mimetype', self.gf('django.db.models.fields.CharField')(default='text/plain', max_length=64)),
            ('constraint', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('voided', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Concept'])

        # Adding model 'RelationshipCategory'
        db.create_table(u'core_relationshipcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='3aea2fcd-1a66-4bf5-8c29-9ac976daff5d', unique=True, max_length=36)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('restriction', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
        ))
        db.send_create_signal('core', ['RelationshipCategory'])

        # Adding model 'Relationship'
        db.create_table(u'core_relationship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='25a76c0b-b92d-44bd-9750-210671c0eaae', unique=True, max_length=36)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('from_concept', self.gf('django.db.models.fields.related.ForeignKey')(related_name='concept_related_from', to_field='uuid', to=orm['core.Concept'])),
            ('to_concept', self.gf('django.db.models.fields.related.ForeignKey')(related_name='concept_related_to', to_field='uuid', to=orm['core.Concept'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.RelationshipCategory'])),
        ))
        db.send_create_signal('core', ['Relationship'])

        # Adding model 'Device'
        db.create_table(u'core_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='3a25ff27-fa50-47fc-95a7-04ad2df9316e', unique=True, max_length=36)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('voided', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Device'])

        # Adding model 'Encounter'
        db.create_table(u'core_encounter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='3f1800b2-bb1a-4986-9ca9-a39392f11cfc', unique=True, max_length=36)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('procedure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Procedure'], to_field='uuid')),
            ('observer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Observer'], to_field='uuid')),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Device'], to_field='uuid')),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Subject'], to_field='uuid')),
            ('concept', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Concept'], to_field='uuid')),
            ('voided', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Encounter'])

        # Adding model 'Event'
        db.create_table(u'core_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='676cda16-f5d9-4d21-943f-f440f0ba6c27', unique=True, max_length=36)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('client', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('level', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=767)),
            ('messages', self.gf('django.db.models.fields.TextField')()),
            ('duration', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('core', ['Event'])

        # Adding model 'Instruction'
        db.create_table(u'core_instruction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='59aaa8d9-5e6b-4a37-9c97-5f82a1661171', unique=True, max_length=36)),
            ('concept', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Concept'], to_field='uuid')),
            ('predicate', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('algorithm', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('compound', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('boolean_operator', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('voided', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Instruction'])

        # Adding model 'Location'
        db.create_table(u'core_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='1a0aee44-ceec-4cd9-b030-fd523db55331', unique=True, max_length=36)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('code', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal('core', ['Location'])

        # Adding model 'Notification'
        db.create_table(u'core_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='463c834f-8c71-4cfb-bcbf-1db7ad9c1301', unique=True, max_length=36)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('delivered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('voided', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Notification'])

        # Adding model 'Observation'
        db.create_table(u'core_observation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='f5e55042-f31d-445d-acf9-73d5bf62f421', unique=True, max_length=36)),
            ('encounter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Encounter'], to_field='uuid')),
            ('node', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('concept', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Concept'], to_field='uuid')),
            ('value_text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value_complex', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('_complex_size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('_complex_progress', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('voided', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Observation'])

        # Adding unique constraint on 'Observation', fields ['encounter', 'node']
        db.create_unique(u'core_observation', ['encounter_id', 'node'])

        # Adding model 'Observer'
        db.create_table(u'core_observer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='ace60a09-3353-419d-a417-7e8efb08e93f', unique=True, max_length=36)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('voided', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Observer'])

        # Adding model 'Procedure'
        db.create_table(u'core_procedure', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='093a4132-7b2c-47f0-af40-2e64e97ee1d4', unique=True, max_length=36)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=255)),
            ('src', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('voided', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Procedure'])

        # Adding model 'Subject'
        db.create_table(u'core_subject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='6bcdbe12-4768-490f-93d9-6425f8a23379', unique=True, max_length=36)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('voided', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('given_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('family_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('dob', self.gf('django.db.models.fields.DateTimeField')()),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Location'], to_field='uuid', blank=True)),
            ('system_id', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('core', ['Subject'])

        # Adding model 'ANM'
        db.create_table(u'core_anm', (
            (u'observer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Observer'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('core', ['ANM'])

        # Adding M2M table for field locations on 'ANM'
        db.create_table(u'core_anm_locations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('anm', models.ForeignKey(orm['core.anm'], null=False)),
            ('location', models.ForeignKey(orm['core.location'], null=False))
        ))
        db.create_unique(u'core_anm_locations', ['anm_id', 'location_id'])

        # Adding model 'Patient'
        db.create_table(u'core_patient', (
            (u'subject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Subject'], unique=True, primary_key=True)),
            ('secondary_id', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('caregiver_name', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('secondary_caregiver_name', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
        ))
        db.send_create_signal('core', ['Patient'])


    def backwards(self, orm):
        # Removing unique constraint on 'Observation', fields ['encounter', 'node']
        db.delete_unique(u'core_observation', ['encounter_id', 'node'])

        # Deleting model 'Concept'
        db.delete_table(u'core_concept')

        # Deleting model 'RelationshipCategory'
        db.delete_table(u'core_relationshipcategory')

        # Deleting model 'Relationship'
        db.delete_table(u'core_relationship')

        # Deleting model 'Device'
        db.delete_table(u'core_device')

        # Deleting model 'Encounter'
        db.delete_table(u'core_encounter')

        # Deleting model 'Event'
        db.delete_table(u'core_event')

        # Deleting model 'Instruction'
        db.delete_table(u'core_instruction')

        # Deleting model 'Location'
        db.delete_table(u'core_location')

        # Deleting model 'Notification'
        db.delete_table(u'core_notification')

        # Deleting model 'Observation'
        db.delete_table(u'core_observation')

        # Deleting model 'Observer'
        db.delete_table(u'core_observer')

        # Deleting model 'Procedure'
        db.delete_table(u'core_procedure')

        # Deleting model 'Subject'
        db.delete_table(u'core_subject')

        # Deleting model 'ANM'
        db.delete_table(u'core_anm')

        # Removing M2M table for field locations on 'ANM'
        db.delete_table('core_anm_locations')

        # Deleting model 'Patient'
        db.delete_table(u'core_patient')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.anm': {
            'Meta': {'object_name': 'ANM', '_ormbases': ['core.Observer']},
            'locations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Location']", 'symmetrical': 'False', 'blank': 'True'}),
            u'observer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Observer']", 'unique': 'True', 'primary_key': 'True'})
        },
        'core.concept': {
            'Meta': {'object_name': 'Concept'},
            'conceptclass': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'constraint': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datatype': ('django.db.models.fields.CharField', [], {'default': "'string'", 'max_length': '64'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'default': "'text/plain'", 'max_length': '64'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'d9e89ec6-5044-4bb4-9afb-7f246a58b785'", 'unique': 'True', 'max_length': '36'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.device': {
            'Meta': {'object_name': 'Device'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'ad8bc54e-2b5c-4e06-827b-1efbc5a1b235'", 'unique': 'True', 'max_length': '36'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.encounter': {
            'Meta': {'object_name': 'Encounter'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Concept']", 'to_field': "'uuid'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Device']", 'to_field': "'uuid'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'observer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Observer']", 'to_field': "'uuid'"}),
            'procedure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Procedure']", 'to_field': "'uuid'"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Subject']", 'to_field': "'uuid'"}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'d1396446-b468-48ae-aab2-37ede1a8d1ae'", 'unique': 'True', 'max_length': '36'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.event': {
            'Meta': {'object_name': 'Event'},
            'client': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'messages': ('django.db.models.fields.TextField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '767'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'8e903695-e5d2-4245-b625-f46439a39b19'", 'unique': 'True', 'max_length': '36'})
        },
        'core.instruction': {
            'Meta': {'object_name': 'Instruction'},
            'algorithm': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'boolean_operator': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'compound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Concept']", 'to_field': "'uuid'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'predicate': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'a8d2cd3a-6cdc-4bef-9dd8-1e6f62a954ba'", 'unique': 'True', 'max_length': '36'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.location': {
            'Meta': {'object_name': 'Location'},
            'code': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'c8493bc4-aea7-4e1b-b1af-cc6841c01248'", 'unique': 'True', 'max_length': '36'})
        },
        'core.notification': {
            'Meta': {'object_name': 'Notification'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'efe1a296-c1a4-46de-b6ed-27156aacd7f1'", 'unique': 'True', 'max_length': '36'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.observation': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('encounter', 'node'),)", 'object_name': 'Observation'},
            '_complex_progress': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            '_complex_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Concept']", 'to_field': "'uuid'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'encounter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Encounter']", 'to_field': "'uuid'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'653f9fff-84e1-4d69-a58a-b3fb3836baa8'", 'unique': 'True', 'max_length': '36'}),
            'value_complex': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.observer': {
            'Meta': {'object_name': 'Observer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'cd55258c-9770-4159-9a13-6284f43fbc14'", 'unique': 'True', 'max_length': '36'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.patient': {
            'Meta': {'object_name': 'Patient', '_ormbases': ['core.Subject']},
            'caregiver_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'secondary_caregiver_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'secondary_id': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            u'subject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Subject']", 'unique': 'True', 'primary_key': 'True'})
        },
        'core.procedure': {
            'Meta': {'object_name': 'Procedure'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'src': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'602682f6-15eb-4222-a976-eb9dea965306'", 'unique': 'True', 'max_length': '36'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '255'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.relationship': {
            'Meta': {'object_name': 'Relationship'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.RelationshipCategory']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'concept_related_from'", 'to_field': "'uuid'", 'to': "orm['core.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'to_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'concept_related_to'", 'to_field': "'uuid'", 'to': "orm['core.Concept']"}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'eb3f0ff2-cc7b-44f3-ac0b-a3d5da7ac552'", 'unique': 'True', 'max_length': '36'})
        },
        'core.relationshipcategory': {
            'Meta': {'object_name': 'RelationshipCategory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'restriction': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'df319166-8410-4f13-879d-c312450451ab'", 'unique': 'True', 'max_length': '36'})
        },
        'core.subject': {
            'Meta': {'object_name': 'Subject'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateTimeField', [], {}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'given_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Location']", 'to_field': "'uuid'", 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'system_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'f62c7831-093d-47a8-8830-50c17fcb46c0'", 'unique': 'True', 'max_length': '36'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['core']