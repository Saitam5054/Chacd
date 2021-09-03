from django.db import models

# Create your models here.

class Pregunta(models.Model):
    id_pregunta = models.IntegerField(primary_key=True, null=False, unique=True)
    id_respuesta = models.IntegerField(null=False)
    pregunta = models.CharField(max_length=200, null=False)
    categoria = models.CharField(max_length=30, null=False)

    def __str__(self):
        return 'Pregunta numero: %i categoria: %s' % (self.id_pregunta, self.categoria)

class Respuesta(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False)
    id_respuesta = models.IntegerField(null=False)
    respuesta = models.CharField(max_length=80, null=False)
    es_correcta = models.BooleanField()

    def __str__(self):
        return 'Respuesta id: %i para la pregunta: %i' % (self.id, self.id_respuesta)