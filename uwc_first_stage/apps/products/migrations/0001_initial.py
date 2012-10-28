# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('products_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subcategories', null=True, to=orm['products.Category'])),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('products', ['Category'])

        # Adding model 'ProductManager'
        db.create_table('products_productmanager', (
            ('basemanager_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseManager'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('products', ['ProductManager'])

        # Adding model 'Product'
        db.create_table('products_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', to=orm['providers.Provider'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('products', ['Product'])

        # Adding model 'Parameter'
        db.create_table('products_parameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('products', ['Parameter'])

        # Adding model 'ParameterValue'
        db.create_table('products_parametervalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['products.Parameter'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('products', ['ParameterValue'])

        # Adding model 'CategoryParameter'
        db.create_table('products_categoryparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parameters', to=orm['products.Category'])),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_categories', to=orm['products.Parameter'])),
        ))
        db.send_create_signal('products', ['CategoryParameter'])

        # Adding model 'ProductParameter'
        db.create_table('products_productparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parameters', to=orm['products.Product'])),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_product_parameters', to=orm['products.Parameter'])),
            ('value', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.ParameterValue'])),
        ))
        db.send_create_signal('products', ['ProductParameter'])

        # Adding unique constraint on 'ProductParameter', fields ['product', 'parameter']
        db.create_unique('products_productparameter', ['product_id', 'parameter_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ProductParameter', fields ['product', 'parameter']
        db.delete_unique('products_productparameter', ['product_id', 'parameter_id'])

        # Deleting model 'Category'
        db.delete_table('products_category')

        # Deleting model 'ProductManager'
        db.delete_table('products_productmanager')

        # Deleting model 'Product'
        db.delete_table('products_product')

        # Deleting model 'Parameter'
        db.delete_table('products_parameter')

        # Deleting model 'ParameterValue'
        db.delete_table('products_parametervalue')

        # Deleting model 'CategoryParameter'
        db.delete_table('products_categoryparameter')

        # Deleting model 'ProductParameter'
        db.delete_table('products_productparameter')


    models = {
        'core.basemanager': {
            'Meta': {'object_name': 'BaseManager'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'products.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subcategories'", 'null': 'True', 'to': "orm['products.Category']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'products.categoryparameter': {
            'Meta': {'object_name': 'CategoryParameter'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parameters'", 'to': "orm['products.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_categories'", 'to': "orm['products.Parameter']"})
        },
        'products.parameter': {
            'Meta': {'object_name': 'Parameter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'products.parametervalue': {
            'Meta': {'object_name': 'ParameterValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['products.Parameter']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['providers.Provider']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'products.productmanager': {
            'Meta': {'object_name': 'ProductManager', '_ormbases': ['core.BaseManager']},
            'basemanager_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.BaseManager']", 'unique': 'True', 'primary_key': 'True'})
        },
        'products.productparameter': {
            'Meta': {'unique_together': "(('product', 'parameter'),)", 'object_name': 'ProductParameter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_product_parameters'", 'to': "orm['products.Parameter']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parameters'", 'to': "orm['products.Product']"}),
            'value': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.ParameterValue']"})
        },
        'providers.provider': {
            'Meta': {'object_name': 'Provider'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['products']