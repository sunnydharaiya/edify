# Generated by Django 5.2.1 on 2025-05-12 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grammar', '0010_remove_grammartype_category_dragdropactivity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grammarword',
            name='grammar_type',
        ),
        migrations.DeleteModel(
            name='GrammarType',
        ),
        migrations.DeleteModel(
            name='GrammarWord',
        ),
    ]
