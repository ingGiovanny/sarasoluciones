from django import forms
from django.forms import ModelForm, TextInput, Select, Textarea
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from mi_app.models import Proveedor
import re

class ProveedorForm(ModelForm):
    # 1. DEFINICIÓN DE CHOICES (Atributo de clase)
    TIPO_DOCUMENTO_CHOICES = [
        ('', 'Seleccione tipo de documento'),
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
        ('NIT', 'Número de Identificación Tributaria (NIT)'),
    ]
    
    # 2. DEFINICIÓN DE VALIDADORES (Atributos de clase - FUNDAMENTAL)
    nombre_validator = RegexValidator(
        regex=r'^[a-záéíóúñA-ZÁÉÍÓÚÑ\s.&,-]+$',
        message='El nombre solo debe contener letras, espacios y caracteres válidos (. , - &)'
    )
    
    telefono_validator = RegexValidator(
        regex=r'^3\d{9}$',
        message='El teléfono debe tener 10 dígitos numéricos y comenzar con 3'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Accedemos a los validadores de la clase y los agregamos a los campos
        self.fields['nombre_completo'].validators.append(self.nombre_validator)
        self.fields['numero_telefonico'].validators.append(self.telefono_validator)
        
        # Configuración de atributos adicionales
        self.fields['nombre_completo'].widget.attrs['autofocus'] = True
        self.fields['tipo_documento'].widget.choices = self.TIPO_DOCUMENTO_CHOICES
        
        # Etiqueta amigable para el campo activo
        if 'activo' in self.fields:
            self.fields['activo'].label = "¿Proveedor Activo?"

    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre_completo': TextInput(attrs={
                'placeholder': 'Ingrese el nombre completo del proveedor o empresa',
                'maxlength': '150',
                'class': 'form-control'
            }),
            'tipo_documento': Select(attrs={'class': 'form-control'}),
            'numero_documento_nit': TextInput(attrs={
                'placeholder': 'Ingrese el número de documento o NIT',
                'maxlength': '15',
                'class': 'form-control'
            }),
            'direccion_empresa': TextInput(attrs={
                'placeholder': 'Ingrese la dirección de la empresa',
                'maxlength': '200',
                'class': 'form-control'
            }),
            'numero_telefonico': TextInput(attrs={
                'placeholder': 'Ej: 3001234567',
                'maxlength': '10',
                'class': 'form-control'
            }),
            'descripcion': Textarea(attrs={
                'placeholder': 'Ingrese una descripción del proveedor...',
                'class': 'form-control',
                'rows': 4,
                'maxlength': '500'
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    # --- MÉTODOS CLEAN (Se mantienen igual) ---

    def clean_nombre_completo(self):
        nombre = self.cleaned_data.get('nombre_completo', '').strip()
        if not nombre:
            raise ValidationError('El nombre completo es obligatorio')
        if len(nombre) < 3:
            raise ValidationError('El nombre completo debe tener al menos 3 caracteres')
        if not re.match(r'^[a-záéíóúñA-ZÁÉÍÓÚÑ\s.&,-]+$', nombre):
            raise ValidationError('El nombre contiene caracteres no válidos')
        return nombre

    def clean_tipo_documento(self):
        tipo_doc = self.cleaned_data.get('tipo_documento', '').strip()
        if not tipo_doc:
            raise ValidationError('Debe seleccionar un tipo de documento')
        return tipo_doc

    def clean_numero_documento_nit(self):
        numero = self.cleaned_data.get('numero_documento_nit', '').strip().replace(' ', '').replace('-', '')
        tipo_doc = self.cleaned_data.get('tipo_documento', '').strip()
        
        if not numero:
            raise ValidationError('El número de documento es obligatorio')
        
        # Validaciones de duplicados
        qs = Proveedor.objects.filter(tipo_documento=tipo_doc, numero_documento_nit=numero)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Ya existe un proveedor con este documento')
            
        return numero

    def clean_numero_telefonico(self):
        telefono = self.cleaned_data.get('numero_telefonico', '').strip()
        for char in [' ', '-', '(', ')', '+']:
            telefono = telefono.replace(char, '')
        if not telefono.isdigit():
            raise ValidationError('El número celular no puede contener letras.')
        if len(telefono) != 10 or not telefono.startswith('3'):
            raise ValidationError('El teléfono debe tener 10 dígitos y empezar con 3.')
        return telefono