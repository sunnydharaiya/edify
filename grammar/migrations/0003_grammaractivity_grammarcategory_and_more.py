# Generated by Django 5.2.1 on 2025-05-12 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grammar', '0002_remove_grammarquestion_activity_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrammarActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GrammarCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='grammarquestion',
            name='grammar_type',
        ),
        migrations.AddField(
            model_name='grammarquestion',
            name='activity',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='grammar.grammaractivity'),
        ),
        migrations.AddField(
            model_name='grammaractivity',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='grammar.grammarcategory'),
        ),
        migrations.DeleteModel(
            name='GrammarType',
        ),
    ]
