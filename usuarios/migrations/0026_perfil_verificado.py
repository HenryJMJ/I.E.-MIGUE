# Generated by Django 5.1.2 on 2025-04-26 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0025_curso_imagen_curso_total_sesiones'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='verificado',
            field=models.BooleanField(default=False),
        ),
    ]
