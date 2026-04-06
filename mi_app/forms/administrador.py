from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Administrador

class AdministradorForm(forms.ModelForm):
    # --- Validadores Reutilizables ---
    # Solo números y exactamente 10 dígitos (Estándar Celular Colombia)
    telefono_regex = RegexValidator(
        regex=r'^3\d{9}$', 
        message='El teléfono debe iniciar con 3 y tener exactamente 10 dígitos numéricos.'
    )
    documento_regex = RegexValidator(
        regex=r'^\d{7,12}$', 
        message='El documento debe contener entre 7 y 12 dígitos numéricos.'
    )

    # --- Campos Extra para la cuenta de Usuario ---
    username = forms.CharField(
        max_length=50, 
        required=True, 
        label="Nombre de Usuario",
        help_text="Usado para iniciar sesión.",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: juanperez88', 'class': 'form-control'})
    )
    
    contrasena = forms.CharField(
        max_length=128, 
        required=True, 
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Mínimo 8 caracteres', 'class': 'form-control'})
    )

    class Meta:
        model = Administrador
        exclude = ['user'] 
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CC o NIT'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '3XXXXXXXXX'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicamos los validadores de forma directa
        self.fields['telefono'].validators.append(self.telefono_regex)
        self.fields['numero_documento'].validators.append(self.documento_regex)
        # Autofocus en el primer campo
        self.fields['nombre_completo'].widget.attrs.update({'autofocus': True})

    # --- Validaciones Personalizadas ---

    def clean_username(self):
        """Valida que el nombre de usuario no esté tomado en el sistema."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está en uso. Elige otro.')
        return username

    def clean_correo_electronico(self):
        """Valida que el correo sea único en la tabla de Administradores."""
        email = self.cleaned_data.get('correo_electronico').lower()
        if Administrador.objects.filter(correo_electronico=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_nombre_completo(self):
        nombre = self.cleaned_data.get('nombre_completo').strip().title()
        if len(nombre) < 3:
            raise ValidationError('El nombre es demasiado corto.')
        return nombre

    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        # Validación de seguridad básica
        if len(contrasena) < 8:
            raise ValidationError('La contraseña es muy débil. Debe tener al menos 8 caracteres.')
        if contrasena.isdigit():
            raise ValidationError('La contraseña no puede ser solo números.')
        return contrasena