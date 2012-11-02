# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ProductManager'
        db.delete_table('products_productmanager')


        # Changing field 'ProductParameter.value'
        db.alter_column('products_productparameter', 'value_id', self.gf('smart_selects.db_fields.ChainedForeignKey')(to=orm['products.ParameterValue']))
        # Adding field 'Category.lft'
        db.add_column('products_category', 'lft',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)

        # Adding field 'Category.rght'
        db.add_column('products_category', 'rght',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)

        # Adding field 'Category.tree_id'
        db.add_column('products_category', 'tree_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)

        # Adding field 'Category.level'
        db.add_column('products_category', 'level',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)


        # Changing field 'Category.parent'
        db.alter_column('products_category', 'parent_id', self.gf('mptt.fields.TreeForeignKey')(null=True, to=orm['products.Category']))

    def backwards(self, orm):
        # Adding model 'ProductManager'
        db.create_table('products_productmanager', (
            ('basemanager_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseManager'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('products', ['ProductManager'])


        # Changing field 'ProductParameter.value'
        db.alter_column('products_productparameter', 'value_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.ParameterValue']))
        # Deleting field 'Category.lft'
        db.delete_column('products_category', 'lft')

        # Deleting field 'Category.rght'
        db.delete_column('products_category', 'rght')

        # Deleting field 'Category.tree_id'
        db.delete_column('products_category', 'tree_id')

        # Deleting field 'Category.level'
        db.delete_column('products_category', 'level')


        # Changing field 'Category.parent'
        db.alter_column('products_category', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['products.Category']))

    models = {
        'products.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'subcategories'", 'null': 'True', 'to': "orm['products.Category']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'variants'", 'null': 'True', 'to': "orm['products.Product']"}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['providers.Provider']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'products.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_main_image': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['products.Product']"})
        },
        'products.productparameter': {
            'Meta': {'unique_together': "(('product', 'parameter'),)", 'object_name': 'ProductParameter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_product_parameters'", 'to': "orm['products.Parameter']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parameters'", 'to': "orm['products.Product']"}),
            'value': ('smart_selects.db_fields.ChainedForeignKey', [], {'to': "orm['products.ParameterValue']"})
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