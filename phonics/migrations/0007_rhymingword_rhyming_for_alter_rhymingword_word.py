# Generated by Django 5.2.1 on 2025-05-17 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonics', '0006_rhyming_rhymingfor_rhymingword'),
    ]

    operations = [
        migrations.AddField(
            model_name='rhymingword',
            name='rhyming_for',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rhyming_words', to='phonics.rhymingfor'),
        ),
        migrations.AlterField(
            model_name='rhymingword',
            name='word',
            field=models.CharField(max_length=255),
        ),
    ]
