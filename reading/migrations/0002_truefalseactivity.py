# Generated by Django 5.2 on 2025-04-16 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reading', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrueFalseActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.TextField()),
                ('is_true', models.BooleanField(default=True)),
                ('reading', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='true_false_activities', to='reading.reading')),
            ],
        ),
    ]
