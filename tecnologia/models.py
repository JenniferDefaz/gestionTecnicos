from django.db import models

# Create your models here.
from django.db import models


class Tecnico(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    cedula = models.CharField(max_length=10, unique=True)
    correo = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=10, blank=True)
    especialidad = models.CharField(max_length=100, blank=True)
    foto = models.FileField(upload_to='tecnicos', null=True, blank=True)

class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    instructor = models.CharField(max_length=100)
    horas_duracion = models.PositiveIntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

# INSCRIPCION: relación Tecnico - Curso
# El certificado se va ha generar dinamicamente desde esta entidad asi como el ING hizo el de reporte OJO

class Inscripcion(models.Model):
    APROBADO = 'APROBADO'
    REPROBADO = 'REPROBADO'
    EN_CURSO = 'EN_CURSO'
    ESTADOS = [
        (EN_CURSO, 'En curso'),
        (APROBADO, 'Aprobado'),
        (REPROBADO, 'Reprobado'),
    ]

    id = models.AutoField(primary_key=True)
    tecnico = models.ForeignKey('Tecnico', on_delete=models.CASCADE)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    nota_final = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default=EN_CURSO)
    fecha_inscripcion = models.DateField(auto_now_add=True)
