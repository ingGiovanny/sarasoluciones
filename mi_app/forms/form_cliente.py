from django import forms
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, PasswordInput
from mi_app.models import GestionCliente

class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_completo'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = GestionCliente
        fields = '__all__'
        widgets = {
            'nombre_completo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre completo del cliente',
                }
            ),
            'numero_telefonico': TextInput(
                attrs={
                    'placeholder': 'Ingrese el número de teléfono (opcional)',
                }
            ),
            'numero_documento': TextInput(
                attrs={
                    'placeholder': 'Ingrese el número de documento',
                }
            ),
            'correo_electronico': EmailInput(
                attrs={
                    'placeholder': 'Ingrese el correo electrónico',
                }
            ),
            'contrasena': PasswordInput(
                attrs={
                    'placeholder': 'Ingrese la contraseña',
                }
            ),
        }