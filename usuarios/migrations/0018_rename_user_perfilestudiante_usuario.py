# Generated by Django 5.1.2 on 2025-04-21 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0017_perfilestudiante'),
    ]

    operations = [
        migrations.RenameField(
            model_name='perfilestudiante',
            old_name='user',
            new_name='usuario',
        ),
    ]
