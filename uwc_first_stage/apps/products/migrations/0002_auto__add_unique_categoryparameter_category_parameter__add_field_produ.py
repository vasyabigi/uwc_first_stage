# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'CategoryParameter', fields ['category', 'parameter']
        db.create_unique('products_categoryparameter', ['category_id', 'parameter_id'])

        # Adding field 'Product.parent'
        db.add_column('products_product', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='variants', null=True, to=orm['products.Product']),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'CategoryParameter', fields ['category', 'parameter']
        db.delete_unique('products_categoryparameter', ['category_id', 'parameter_id'])

        # Deleting field 'Product.parent'
        db.delete_column('products_product', 'parent_id')


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
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'products.categoryparameter': {
            'Meta': {'unique_together': "(('category', 'parameter'),)", 'object_name': 'CategoryParameter'},
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
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['products.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'variants'", 'null': 'True', 'to': "orm['products.Product']"}),
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