# Generated by Django 5.2.1 on 2025-05-12 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spellingtype',
            name='reading',
        ),
    ]
