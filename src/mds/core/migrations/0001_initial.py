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
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='63728e9b-e7b1-45f6-861a-ad3e0e1e7521', unique=True, max_length=36)),
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
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='aac390f7-d23a-4bea-a7bf-7a050637bcce', unique=True, max_length=36)),
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
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='2752b5ff-b2cc-4cd1-a04a-2307da728bd9', unique=True, max_length=36)),
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
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='d201c689-cf2f-4167-8b97-d7aa1c425bc0', unique=True, max_length=36)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('voided', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Device'])

        # Adding model 'Encounter'
        db.create_table(u'core_encounter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='f0ae58ab-0bcb-4f6d-b3b8-1b0e04858425', unique=True, max_length=36)),
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
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='e4e28207-97bb-48fb-a1e2-9f86db97dcce', unique=True, max_length=36)),
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
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='b1a98247-34bb-4133-868b-a4e7dbdd0ad6', unique=True, max_length=36)),
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
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='187c3e96-f1c8-43db-a105-ed4e83d9254c', unique=True, max_length=36)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('code', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal('core', ['Location'])

        # Adding model 'Notification'
        db.create_table(u'core_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='6bdb878f-ffa0-4ea5-8a79-8732d741ec2b', unique=True, max_length=36)),
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
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='97a7a382-8a32-45a3-832f-d2c4d86970a4', unique=True, max_length=36)),
            ('encounter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='observations', to_field='uuid', to=orm['core.Encounter'])),
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
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='d695874c-be30-4739-9c63-04cbcba86abf', unique=True, max_length=36)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('voided', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Observer'])

        # Adding model 'Procedure'
        db.create_table(u'core_procedure', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='b897454f-0f12-4b1c-8070-10b18eb059e1', unique=True, max_length=36)),
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
            ('uuid', self.gf('django.db.models.fields.SlugField')(default='30edd8cc-0b7b-42ff-91c1-35dd493332f7', unique=True, max_length=36)),
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

        # Adding model 'Surgeon'
        db.create_table(u'core_surgeon', (
            (u'observer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Observer'], unique=True, primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Device'], blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
        ))
        db.send_create_signal('core', ['Surgeon'])

        # Adding model 'SurgicalAdvocate'
        db.create_table(u'core_surgicaladvocate', (
            (u'observer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Observer'], unique=True, primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Device'], blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Location'], blank=True)),
        ))
        db.send_create_signal('core', ['SurgicalAdvocate'])

        # Adding model 'SurgicalSubject'
        db.create_table(u'core_surgicalsubject', (
            (u'subject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Subject'], unique=True, primary_key=True)),
            ('house_number', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('family_number', self.gf('django.db.models.fields.IntegerField')(max_length=5, null=True, blank=True)),
            ('national_id', self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True, blank=True)),
            ('contact_one', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('contact_two', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('contact_three', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('contact_four', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('core', ['SurgicalSubject'])


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

        # Deleting model 'Surgeon'
        db.delete_table(u'core_surgeon')

        # Deleting model 'SurgicalAdvocate'
        db.delete_table(u'core_surgicaladvocate')

        # Deleting model 'SurgicalSubject'
        db.delete_table(u'core_surgicalsubject')


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
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'92a6f3f0-7935-4633-9b4a-4f18160a8dd7'", 'unique': 'True', 'max_length': '36'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.device': {
            'Meta': {'object_name': 'Device'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'09be816e-9847-4062-88ef-e18b86148d8b'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'2f27351d-a2f1-4753-a561-b28d96abd5ae'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'ca2016cf-29a4-4aa3-b3b3-1172749529f3'", 'unique': 'True', 'max_length': '36'})
        },
        'core.instruction': {
            'Meta': {'object_name': 'Instruction'},
            'algorithm': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'boolean_operator': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'compound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Concept']", 'to_field': "'uuid'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'predicate': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'c80dd5b4-f283-4296-a323-b8aff72aeddc'", 'unique': 'True', 'max_length': '36'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.location': {
            'Meta': {'object_name': 'Location'},
            'code': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'e07a2d1d-72d5-4450-bd2b-5c0bbb811320'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'07a8eab0-88d2-4e78-8530-e7f99b5133e0'", 'unique': 'True', 'max_length': '36'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.observation': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('encounter', 'node'),)", 'object_name': 'Observation'},
            '_complex_progress': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            '_complex_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Concept']", 'to_field': "'uuid'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'encounter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'observations'", 'to_field': "'uuid'", 'to': "orm['core.Encounter']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'43782a5a-85cd-48f1-8c76-bd2f66ab44d4'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'fd9dcf9c-c31f-4fff-8d8b-04229ecc7077'", 'unique': 'True', 'max_length': '36'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'6844e9e6-8ee7-41b4-83ef-8ca97194bd25'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'d1387ab8-3db8-4432-a1a8-10cf8e98545f'", 'unique': 'True', 'max_length': '36'})
        },
        'core.relationshipcategory': {
            'Meta': {'object_name': 'RelationshipCategory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'restriction': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'16d2e618-2daa-4686-bbb3-7d15aafee8e3'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.SlugField', [], {'default': "'e8a973df-20fc-4468-a6b7-0dde038fcd80'", 'unique': 'True', 'max_length': '36'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.surgeon': {
            'Meta': {'object_name': 'Surgeon', '_ormbases': ['core.Observer']},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Device']", 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'observer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Observer']", 'unique': 'True', 'primary_key': 'True'})
        },
        'core.surgicaladvocate': {
            'Meta': {'object_name': 'SurgicalAdvocate', '_ormbases': ['core.Observer']},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Device']", 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Location']", 'blank': 'True'}),
            u'observer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Observer']", 'unique': 'True', 'primary_key': 'True'})
        },
        'core.surgicalsubject': {
            'Meta': {'object_name': 'SurgicalSubject', '_ormbases': ['core.Subject']},
            'contact_four': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'contact_one': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'contact_three': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'contact_two': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'family_number': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'house_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'national_id': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            u'subject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Subject']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['core']