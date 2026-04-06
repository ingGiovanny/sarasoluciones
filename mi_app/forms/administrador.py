from django import forms
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from mi_app.models import Administrador
from django.contrib.auth.models import User

class AdministradorForm(ModelForm):
    # 1. Validadores con expresiones regulares más estrictas
    telefono_validator = RegexValidator(
        regex=r'^3\d{9}$', 
        message='El teléfono debe empezar con 3 y tener 10 dígitos (formato celular Colombia).'
    )
    documento_validator = RegexValidator(
        regex=r'^\d{7,12}$', 
        message='El documento debe tener entre 7 y 12 números.'
    )

    # ==========================================
    # CAMPOS EXTRA (Para el User de Django)
    # ==========================================
    username = forms.CharField(
        max_length=50,
        required=True,
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: juanperez88', 'class': 'form-control'})
    )

    contrasena = forms.CharField(
        max_length=128,
        required=True,
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Mínimo 8 caracteres', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_completo'].widget.attrs['autofocus'] = True
        # Aplicamos los validadores a los campos
        self.fields['telefono'].validators.append(self.telefono_validator)
        self.fields['numero_documento'].validators.append(self.documento_validator)
        # Añadimos validación de email nativa de Django
        self.fields['correo_electronico'].validators.append(EmailValidator(message="Ingrese un correo electrónico válido."))

    class Meta:
        model = Administrador
        exclude = ['user']
        widgets = {
            'nombre_completo': TextInput(attrs={'placeholder': 'Nombre y Apellidos', 'class': 'form-control'}),
            'correo_electronico': EmailInput(attrs={'placeholder': 'ejemplo@correo.com', 'class': 'form-control'}),
            'numero_documento': TextInput(attrs={'placeholder': 'Cédula de ciudadanía', 'class': 'form-control'}),
            'telefono': TextInput(attrs={'placeholder': '3XXXXXXXXX', 'class': 'form-control'}),
        }

    # ==========================================
    # VALIDACIONES PERSONALIZADAS (Métodos Clean)
    # ==========================================

    def clean_username(self):
        """ Verifica si el nombre de usuario ya existe en el sistema """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso. Elige otro.")
        return username

    def clean_correo_electronico(self):
        """ Verifica que el correo no esté registrado ni en User ni en Administrador """
        email = self.cleaned_data.get('correo_electronico').lower()
        if User.objects.filter(email=email).exists() or Administrador.objects.filter(correo_electronico=email).exists():
            raise ValidationError("Este correo ya está registrado en el sistema.")
        return email

    def clean_numero_documento(self):
        """ Verifica que el documento sea único """
        documento = self.cleaned_data.get('numero_documento')
        if Administrador.objects.filter(numero_documento=documento).exists():
            raise ValidationError("Este número de documento ya pertenece a un administrador.")
        return documento

    def clean_contrasena(self):
        """ Valida el largo de la contraseña """
        password = self.cleaned_data.get('contrasena')
        if len(password) < 8:
            raise ValidationError("La contraseña es muy corta. Debe tener al menos 8 caracteres.")
        return password