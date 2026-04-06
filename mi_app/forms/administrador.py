from django import forms
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from mi_app.models import Administrador

class AdministradorForm(ModelForm):
    # Validadores
    telefono_validator = RegexValidator(
        regex=r'^\d+$', 
        message='El teléfono solo debe contener números'
    )
    documento_validator = RegexValidator(
        regex=r'^\d+$', 
        message='El documento solo debe contener números'
    )

    # ==========================================
    # CAMPOS EXTRA (Para el User de Django)
    # ==========================================
    username = forms.CharField(
        max_length=50,
        required=True,
        label="Nombre de Usuario (Para iniciar sesión)",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: juanperez88', 'class': 'form-control'})
    )

    contrasena = forms.CharField(
        max_length=128,
        required=True,
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese la contraseña', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_completo'].widget.attrs['autofocus'] = True
        self.fields['telefono'].validators.append(self.telefono_validator)
        self.fields['numero_documento'].validators.append(self.documento_validator)

    class Meta:
        model = Administrador
        # Aquí quitamos 'user' porque lo creamos en la vista, no en el formulario
        exclude = ['user']
        widgets = {
            'nombre_completo': TextInput(attrs={
                'placeholder': 'Ingrese el nombre del administrador', 
                'maxlength': '100',
                'class': 'form-control'
            }),
            'correo_electronico': EmailInput(attrs={
                'placeholder': 'Ingrese el correo electrónico',
                'class': 'form-control'
            }),
            'numero_documento': TextInput(attrs={
                'placeholder': 'Ingrese el número de documento', 
                'maxlength': '15',
                'class': 'form-control'
            }),
            'telefono': TextInput(attrs={
                'placeholder': 'Ingrese el número de teléfono', 
                'maxlength': '10',
                'class': 'form-control'
            }),
        }