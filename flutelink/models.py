from django.db import models
from django.contrib.auth.models import User

class Disciplina(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class UsuarioDisciplina(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} - {self.disciplina}"

class UsuarioDisciplinaTipo(models.Model):
    usuario_disciplina = models.ForeignKey(UsuarioDisciplina, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.usuario_disciplina} - {self.tipo}"

# Subtipos de UsuarioDisciplinaTipo

class Cantante(models.Model):
    usuario_disciplina_tipo = models.OneToOneField(UsuarioDisciplinaTipo, on_delete=models.CASCADE, primary_key=True)
    genero = models.CharField(max_length=100)
    experiencia = models.IntegerField()
    ubicacion_lat = models.FloatField(null=True, blank=True)
    ubicacion_lng = models.FloatField(null=True, blank=True)
    busca = models.TextField(blank=True) 

class Bailarin(models.Model):
    usuario_disciplina_tipo = models.OneToOneField(UsuarioDisciplinaTipo, on_delete=models.CASCADE, primary_key=True)
    experiencia = models.IntegerField()
    crew = models.CharField(max_length=100)
    estilo = models.CharField(max_length=100)
    ubicacion_lat = models.FloatField(null=True, blank=True)
    ubicacion_lng = models.FloatField(null=True, blank=True)
    busca = models.TextField(blank=True) 

class Grafitero(models.Model):
    usuario_disciplina_tipo = models.OneToOneField(UsuarioDisciplinaTipo, on_delete=models.CASCADE, primary_key=True)
    estilo = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    ubicacion_lat = models.FloatField(null=True, blank=True)
    ubicacion_lng = models.FloatField(null=True, blank=True)
    busca = models.TextField(blank=True) 

class Instrumentista(models.Model):
    usuario_disciplina_tipo = models.OneToOneField(UsuarioDisciplinaTipo, on_delete=models.CASCADE, primary_key=True)
    instrumento = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50)
    experiencia = models.IntegerField()
    ubicacion_lat = models.FloatField(null=True, blank=True)
    ubicacion_lng = models.FloatField(null=True, blank=True)
    busca = models.TextField(blank=True) 

class Productor(models.Model):
    usuario_disciplina_tipo = models.OneToOneField(UsuarioDisciplinaTipo, on_delete=models.CASCADE, primary_key=True)
    programa = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    experiencia = models.IntegerField()
    ubicacion_lat = models.FloatField(null=True, blank=True)
    ubicacion_lng = models.FloatField(null=True, blank=True)
    busca = models.TextField(blank=True) 