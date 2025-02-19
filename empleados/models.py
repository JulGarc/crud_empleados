from django.db import models
from django.core.validators import RegexValidator

class Employee(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(regex=r'^\d+$', message='La cédula solo puede contener números.')],
        error_messages={
            'unique': "Ya existe un empleado con esta cédula.",
            'blank': "Este campo no puede estar vacío.",
        }
    )
    fecha_nacimiento = models.DateField()
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "Ya existe un empleado con este correo electrónico.",
        }
    )
    numero_telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"
