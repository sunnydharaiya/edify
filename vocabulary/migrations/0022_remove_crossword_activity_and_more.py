# Generated by Django 5.2.1 on 2025-05-23 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary', '0021_crossword_clue_crosswordcell'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crossword',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='crosswordcell',
            name='crossword',
        ),
        migrations.DeleteModel(
            name='Clue',
        ),
        migrations.DeleteModel(
            name='Crossword',
        ),
        migrations.DeleteModel(
            name='CrosswordCell',
        ),
    ]
