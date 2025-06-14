# Generated by Django 5.2.1 on 2025-05-12 09:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_spellingword'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LongVowelSound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images/long_vowel_sounds/')),
                ('audio', models.FileField(blank=True, null=True, upload_to='audio/long_vowel_sounds/')),
                ('is_correct', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='long_vowel_sounds', to='core.category')),
            ],
        ),
    ]
