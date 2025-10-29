from django import forms
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from mi_app.models import GestionCliente
import re

class ClienteForm(ModelForm):
    # Validador para teléfono colombiano (10 dígitos, empieza con 3)
    telefono_validator = RegexValidator(
        regex=r'^3\d{9}$',
        message='El teléfono debe tener 10 dígitos y comenzar con 3'
    )
    
    # Validador para documento (6-10 dígitos)
    documento_validator = RegexValidator(
        regex=r'^\d{6,10}$',
        message='El documento debe contener entre 6 y 10 dígitos'
    )
    
    # Validador para nombres (solo letras, espacios, tildes y ñ)
    nombre_validator = RegexValidator(
        regex=r'^[a-záéíóúñA-ZÁÉÍÓÚÑ\s]+$',
        message='El nombre solo debe contener letras, espacios y tildes'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_completo'].widget.attrs['autofocus'] = True
        
        # Agregar validadores a los campos
        if 'numero_telefonico' in self.fields:
            self.fields['numero_telefonico'].required = False
            self.fields['numero_telefonico'].validators.append(self.telefono_validator)
        
        if 'numero_documento' in self.fields:
            self.fields['numero_documento'].validators.append(self.documento_validator)
        
        if 'nombre_completo' in self.fields:
            self.fields['nombre_completo'].validators.append(self.nombre_validator)
    
    class Meta:
        model = GestionCliente
        fields = '__all__'
        widgets = {
            'nombre_completo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre completo del cliente',
                    'maxlength': '100',
                    'class': 'form-control',
                }
            ),
            'numero_telefonico': TextInput(
                attrs={
                    'placeholder': 'Ej: 3001234567 (opcional)',
                    'maxlength': '10',
                    'class': 'form-control',
                }
            ),
            'numero_documento': TextInput(
                attrs={
                    'placeholder': 'Ingrese el número de documento (6-10 dígitos)',
                    'maxlength': '10',
                    'class': 'form-control',
                }
            ),
            'correo_electronico': EmailInput(
                attrs={
                    'placeholder': 'ejemplo@correo.com',
                    'class': 'form-control',
                }
            ),
            'contrasena': PasswordInput(
                attrs={
                    'placeholder': 'Mínimo 8 caracteres',
                    'class': 'form-control',
                }
            ),
        }
    
    def clean_nombre_completo(self):
        nombre = self.cleaned_data.get('nombre_completo', '').strip()
        
        if not nombre:
            raise ValidationError('El nombre completo es obligatorio')
        
        if len(nombre) < 3:
            raise ValidationError('El nombre completo debe tener al menos 3 caracteres')
        
        if len(nombre) > 100:
            raise ValidationError('El nombre completo no puede exceder los 100 caracteres')
        
        # Validar que no contenga números
        if any(char.isdigit() for char in nombre):
            raise ValidationError('El nombre no debe contener números')
        
        # Validar que no contenga caracteres especiales (excepto tildes y ñ)
        if not re.match(r'^[a-záéíóúñA-ZÁÉÍÓÚÑ\s]+$', nombre):
            raise ValidationError('El nombre solo debe contener letras, espacios y tildes')
        
        return nombre
    
    def clean_numero_telefonico(self):
        telefono = self.cleaned_data.get('numero_telefonico', '').strip()
        
        # Si el campo está vacío y es opcional, retornar vacío
        if not telefono:
            return telefono
        
        # Eliminar espacios y guiones si los hay
        telefono = telefono.replace(' ', '').replace('-', '')
        
        if not telefono.isdigit():
            raise ValidationError('El teléfono solo debe contener números')
        
        if len(telefono) != 10:
            raise ValidationError('El teléfono debe tener exactamente 10 dígitos')
        
        # Validar que comience con 3 (celulares en Colombia)
        if not telefono.startswith('3'):
            raise ValidationError('El teléfono celular debe comenzar con 3')
        
        return telefono
    
    def clean_numero_documento(self):
        documento = self.cleaned_data.get('numero_documento', '').strip()
        
        if not documento:
            raise ValidationError('El número de documento es obligatorio')
        
        # Eliminar espacios si los hay
        documento = documento.replace(' ', '')
        
        if not documento.isdigit():
            raise ValidationError('El documento solo debe contener números')
        
        if len(documento) < 6:
            raise ValidationError('El documento debe tener al menos 6 dígitos')
        
        if len(documento) > 10:
            raise ValidationError('El documento no puede exceder los 10 dígitos')
        
        # Validar que el documento no sea duplicado (excepto en edición)
        if self.instance.pk:  # Si es edición
            if GestionCliente.objects.exclude(pk=self.instance.pk).filter(numero_documento=documento).exists():
                raise ValidationError('Ya existe un cliente con este número de documento')
        else:  # Si es creación
            if GestionCliente.objects.filter(numero_documento=documento).exists():
                raise ValidationError('Ya existe un cliente con este número de documento')
        
        return documento
    
    def clean_correo_electronico(self):
        correo = self.cleaned_data.get('correo_electronico', '').strip().lower()
        
        if not correo:
            raise ValidationError('El correo electrónico es obligatorio')
        
        # Validar formato de correo
        email_validator = EmailValidator(message='Ingrese un correo electrónico válido')
        try:
            email_validator(correo)
        except ValidationError:
            raise ValidationError('El formato del correo electrónico no es válido')
        
        if len(correo) > 254:
            raise ValidationError('El correo electrónico es demasiado largo')
        
        # Validar que el correo no sea duplicado (excepto en edición)
        if self.instance.pk:  # Si es edición
            if GestionCliente.objects.exclude(pk=self.instance.pk).filter(correo_electronico=correo).exists():
                raise ValidationError('Ya existe un cliente con este correo electrónico')
        else:  # Si es creación
            if GestionCliente.objects.filter(correo_electronico=correo).exists():
                raise ValidationError('Ya existe un cliente con este correo electrónico')
        
        return correo
    
    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena', '')
        
        # Si es edición y el campo está vacío, no validar (permite no cambiar la contraseña)
        if self.instance.pk and not contrasena:
            return self.instance.contrasena
        
        if not contrasena:
            raise ValidationError('La contraseña es obligatoria')
        
        if len(contrasena) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres')
        
        if len(contrasena) > 128:
            raise ValidationError('La contraseña no puede exceder los 128 caracteres')
        
        # Validar complejidad de contraseña
        if not re.search(r'[A-Z]', contrasena):
            raise ValidationError('La contraseña debe contener al menos una letra mayúscula')
        
        if not re.search(r'[a-z]', contrasena):
            raise ValidationError('La contraseña debe contener al menos una letra minúscula')
        
        if not re.search(r'\d', contrasena):
            raise ValidationError('La contraseña debe contener al menos un número')
        
        if not re.search(r'[!@#$%^&*()_+=\-\[\]{};:\'",.<>?/\\|`~]', contrasena):
            raise ValidationError('La contraseña debe contener al menos un carácter especial (!@#$%^&*, etc.)')
        
        return contrasena