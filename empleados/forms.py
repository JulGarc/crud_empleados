from django import forms
from .models import Employee
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import date

class EmployeeForm(forms.ModelForm):
    cedula = forms.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='La cédula solo puede contener números.'
            )
        ],
        label="Cédula"
    )

    email = forms.EmailField(
        label="Correo Electrónico",
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z][a-zA-Z0-9_.+-]*@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$',
                message='El correo debe comenzar con una letra y ser válido (ej. usuario@dominio.com).'
            )
        ]
    )

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento and fecha_nacimiento > date.today():
            raise ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return fecha_nacimiento

    def clean(self):
        cleaned_data = super().clean()
        cedula = cleaned_data.get('cedula')
        email = cleaned_data.get('email')

        if cedula:
            cedula_exists = Employee.objects.filter(cedula=cedula).exclude(pk=self.instance.pk).exists()
            if cedula_exists:
                self.add_error('cedula', 'Ya existe un empleado con esta cédula.')

        if email:
            email_exists = Employee.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
            if email_exists:
                self.add_error('email', 'Ya existe un empleado con este correo electrónico.')

    class Meta:
        model = Employee
        fields = ['nombre', 'cedula', 'fecha_nacimiento', 'email', 'numero_telefono']
        widgets = {
            'fecha_nacimiento': forms.DateInput(format='%Y-%m-%d',attrs={ 'type': 'date',
                    'class': 'form-control'}),
        }   