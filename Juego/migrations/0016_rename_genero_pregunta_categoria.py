# Generated by Django 3.2.5 on 2021-08-25 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Juego', '0015_rename_es_correta_respuesta_es_correcta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pregunta',
            old_name='genero',
            new_name='categoria',
        ),
    ]
