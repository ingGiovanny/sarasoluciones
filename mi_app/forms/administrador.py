from django import forms
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, PasswordInput
from mi_app.models import Administrador

class AdministradorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombres_completos'].widget.attrs['autofocus'] = True

    class Meta:
        model = Administrador
        fields = '__all__'
        widgets = {
            'nombres_completos': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del administrador',
                }
            ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'Ingrese el correo del administrador',
                }
            ),
            'contraseña': PasswordInput(
                attrs={
                    'placeholder': 'Ingrese la contraseña',
                }
            ),
            'cedula': NumberInput(
                attrs={
                    'placeholder': 'Ingrese la cédula',
                }
            ),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese el número de teléfono',
                }
            ),
        }
