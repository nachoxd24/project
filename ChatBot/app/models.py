from django.db import models
from django.contrib.auth.models import User


class LoginCount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.count}"

class Curso(models.Model):
    nombre = models.CharField(max_length=100)

class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, related_name='asignaturas', on_delete=models.CASCADE)

class Contenido(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    presentacion = models.FileField(upload_to='presentaciones/')
    asignatura = models.ForeignKey(Asignatura, related_name='contenidos', on_delete=models.CASCADE)