from django import forms
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, PasswordInput
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from mi_app.models import Administrador

class AdministradorForm(ModelForm):
    # Validador para solo números en teléfono
    telefono_validator = RegexValidator(
        regex=r'^\d+$',
        message='El teléfono solo debe contener números'
    )
    
    # Validador para solo números en cédula
    cedula_validator = RegexValidator(
        regex=r'^\d+$',
        message='La cédula solo debe contener números'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombres_completos'].widget.attrs['autofocus'] = True
        
        # Agregar validadores a los campos
        self.fields['telefono'].validators.append(self.telefono_validator)
        self.fields['cedula'].validators.append(self.cedula_validator)

    class Meta:
        model = Administrador
        fields = '__all__'
        widgets = {
            'nombres_completos': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del administrador',
                    'maxlength': '100',
                }
            ),
            'correo_electronico': EmailInput(
                attrs={
                    'placeholder': 'Ingrese el correo del administrador',
                }
            ),
            'contrasena': PasswordInput(
                attrs={
                    'placeholder': 'Ingrese la contraseña',
                    'maxlength': '128',
                }
            ),
            'cedula': TextInput(
                attrs={
                    'placeholder': 'Ingrese la cédula',
                    'maxlength': '10',
                }
            ),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese el número de teléfono',
                    'maxlength': '10',
                }
            ),
        }
    
    def clean_nombres_completos(self):
        nombres = self.cleaned_data.get('nombres_completos')
        if len(nombres) > 100:
            raise ValidationError('El nombre completo no puede exceder los 100 caracteres')
        if len(nombres) < 3:
            raise ValidationError('El nombre completo debe tener al menos 3 caracteres')
        return nombres
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise ValidationError('El teléfono solo debe contener números')
        if len(telefono) != 10:
            raise ValidationError('El teléfono debe tener exactamente 10 dígitos')
        return telefono
    
    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if not cedula.isdigit():
            raise ValidationError('La cédula solo debe contener números')
        if len(cedula) < 6 or len(cedula) > 10:
            raise ValidationError('La cédula debe tener entre 6 y 10 dígitos')
        return cedula
    
    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        if len(contrasena) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres')
        if len(contrasena) > 128:
            raise ValidationError('La contraseña no puede exceder los 128 caracteres')
        return contrasena
    
    def clean_correo_electronico(self):
        correo = self.cleaned_data.get('correo_electronico')
        if len(correo) > 254:
            raise ValidationError('El correo electrónico es demasiado largo')
        return correo