# Generated by Django 3.2.5 on 2021-08-22 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Juego', '0014_alter_respuesta_respuesta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='respuesta',
            old_name='es_correta',
            new_name='es_correcta',
        ),
    ]
