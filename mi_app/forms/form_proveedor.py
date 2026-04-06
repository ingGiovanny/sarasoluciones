from django import forms
from django.forms import ModelForm, TextInput, Select, Textarea
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from mi_app.models import Proveedor
import re

class ProveedorForm(ModelForm):
    # Opciones para tipo de documento
    TIPO_DOCUMENTO_CHOICES = [
        ('', 'Seleccione tipo de documento'),
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
        ('NIT', 'Número de Identificación Tributaria (NIT)'),
    ]
    
    # Validadores
    nombre_validator = RegexValidator(
        regex=r'^[a-záéíóúñA-ZÁÉÍÓÚÑ\s.&,-]+$',
        message='El nombre solo debe contener letras, espacios y caracteres válidos (. , - &)'
    )
    
    telefono_validator = RegexValidator(
        regex=r'^3\d{9}$',
        message='El teléfono debe tener 10 dígitos numericos y comenzar con 3'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_completo'].widget.attrs['autofocus'] = True
        
        # Agregar validadores
        self.fields['nombre_completo'].validators.append(self.nombre_validator)
        self.fields['numero_telefonico'].validators.append(self.telefono_validator)
        
        # Configurar choices para tipo_documento
        self.fields['tipo_documento'].widget.choices = self.TIPO_DOCUMENTO_CHOICES
    
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre_completo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre completo del proveedor o empresa',
                    'maxlength': '150',
                    'class': 'form-control'
                }
            ),
            'tipo_documento': Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'numero_documento_nit': TextInput(
                attrs={
                    'placeholder': 'Ingrese el número de documento o NIT',
                    'maxlength': '10',
                    'class': 'form-control'
                }
            ),
            'direccion_empresa': TextInput(
                attrs={
                    'placeholder': 'Ingrese la dirección de la empresa',
                    'maxlength': '200',
                    'class': 'form-control'
                }
            ),
            'numero_telefonico': TextInput(
                attrs={
                    'placeholder': 'Ej: 3001234567',
                    'maxlength': '10',
                    'class': 'form-control'
                }
            ),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción del proveedor (productos, servicios, etc.)  sirve para saber nos que provee el proveedor',
                    'class': 'form-control',
                    'rows': 4,
                    'maxlength': '500'
                }
            ),
        }
    
    def clean_nombre_completo(self):
        nombre = self.cleaned_data.get('nombre_completo', '').strip()
        
        if not nombre:
            raise ValidationError('El nombre completo es obligatorio')
        
        if len(nombre) < 3:
            raise ValidationError('El nombre completo debe tener al menos 3 caracteres')
        
        if len(nombre) > 150:
            raise ValidationError('El nombre completo no puede exceder los 150 caracteres')
        
        # Validar caracteres permitidos (letras, espacios, puntos, comas, guiones, &)
        if not re.match(r'^[a-záéíóúñA-ZÁÉÍÓÚÑ\s.&,-]+$', nombre):
            raise ValidationError('El nombre solo debe contener letras, espacios y caracteres válidos (. , - &)')
        
        return nombre
    
    def clean_tipo_documento(self):
        tipo_doc = self.cleaned_data.get('tipo_documento', '').strip()
        
        if not tipo_doc:
            raise ValidationError('Debe seleccionar un tipo de documento')
        
        tipos_validos = [choice[0] for choice in self.TIPO_DOCUMENTO_CHOICES if choice[0]]
        if tipo_doc not in tipos_validos:
            raise ValidationError('Tipo de documento inválido')
        
        return tipo_doc
    
    def clean_numero_documento_nit(self):
        numero = self.cleaned_data.get('numero_documento_nit', '').strip()
        tipo_doc = self.cleaned_data.get('tipo_documento', '').strip()
        
        if not numero:
            raise ValidationError('El número de documento es obligatorio')
        
        # Eliminar espacios y guiones
        numero = numero.replace(' ', '').replace('-', '')
        
        # Validaciones específicas según el tipo de documento
        if tipo_doc == 'NIT':
            # NIT: 9-10 dígitos, puede tener guión y dígito de verificación
            if not re.match(r'^\d{9,10}$', numero):
                raise ValidationError('El NIT debe tener entre 9 y 10 dígitos')
        
        elif tipo_doc == 'CC':
            # Cédula de Ciudadanía: 6-10 dígitos
            if not numero.isdigit():
                raise ValidationError('La cédula de ciudadanía debe contener solo números')
            if len(numero) < 6 or len(numero) > 10:
                raise ValidationError('La cédula debe tener entre 6 y 10 dígitos')
        
        elif tipo_doc == 'TI':
            # Tarjeta de Identidad: 10-11 dígitos
            if not numero.isdigit():
                raise ValidationError('La tarjeta de identidad debe contener solo números')
            if len(numero) < 10 or len(numero) > 11:
                raise ValidationError('La tarjeta de identidad debe tener entre 10 y 11 dígitos')
        
        elif tipo_doc == 'CE':
            # Cédula de Extranjería: alfanumérico, 6-15 caracteres
            if not re.match(r'^[a-zA-Z0-9]+$', numero):
                raise ValidationError('La cédula de extranjería debe ser alfanumérica')
            if len(numero) < 6 or len(numero) > 15:
                raise ValidationError('La cédula de extranjería debe tener entre 6 y 15 caracteres')
        
        # Validar que no exista duplicado (excepto en edición)
        if self.instance.pk:  # Si es edición
            if Proveedor.objects.exclude(pk=self.instance.pk).filter(
                tipo_documento=tipo_doc,
                numero_documento_nit=numero
            ).exists():
                raise ValidationError(f'Ya existe un proveedor con este {dict(self.TIPO_DOCUMENTO_CHOICES).get(tipo_doc)}')
        else:  # Si es creación
            if Proveedor.objects.filter(
                tipo_documento=tipo_doc,
                numero_documento_nit=numero
            ).exists():
                raise ValidationError(f'Ya existe un proveedor con este {dict(self.TIPO_DOCUMENTO_CHOICES).get(tipo_doc)}')
        
        return numero
    
    def clean_direccion_empresa(self):
        direccion = self.cleaned_data.get('direccion_empresa', '').strip()
        
        if not direccion:
            raise ValidationError('La dirección es obligatoria')
        
        if len(direccion) < 5:
            raise ValidationError('La dirección debe tener al menos 5 caracteres')
        
        if len(direccion) > 200:
            raise ValidationError('La dirección no puede exceder los 200 caracteres')
        
        # Validar caracteres permitidos
        if not re.match(r'^[a-záéíóúñA-ZÁÉÍÓÚÑ0-9\s.#,\-]+$', direccion):
            raise ValidationError('La dirección contiene caracteres no válidos')
        
        return direccion
    
    def clean_numero_telefonico(self):
    # 1. Obtener y limpiar espacios básicos
        valor_original = self.cleaned_data.get('numero_telefonico', '')
        telefono = valor_original.strip()

        if not telefono:
            raise ValidationError('El número telefónico es obligatorio')

        # 2. Limpieza de caracteres de formato comunes (espacios, guiones, paréntesis, signo +)
        for char in [' ', '-', '(', ')', '+']:
            telefono = telefono.replace(char, '')

        # 3. Detección específica de letras o caracteres especiales no deseados
        if not telefono.isdigit():
            # Aquí es donde capturamos si realmente escribió letras como "310abc1234"
            raise ValidationError('El número celular no puede contener letras ni caracteres especiales.')

        # 4. Validación de longitud (estándar Colombia)
        if len(telefono) != 10:
            raise ValidationError(f'El teléfono debe tener exactamente 10 dígitos (ingresaste {len(telefono)})')

        # 5. Validación de prefijo celular colombiano
        if not telefono.startswith('3'):
            raise ValidationError('El número celular debe iniciar con el dígito 3.')

        return telefono
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '').strip()
        
        # La descripción puede ser opcional, pero si se proporciona debe tener un mínimo
        if descripcion:
            if len(descripcion) < 1:
                raise ValidationError('La descripción debe tener al menos 1 caracteres')
            
            if len(descripcion) > 500:
                raise ValidationError('La descripción no puede exceder los 500 caracteres')
        
        return descripcion
    
    def clean(self):
        """Validación general del formulario"""
        cleaned_data = super().clean()
        tipo_documento = cleaned_data.get('tipo_documento')
        numero_documento = cleaned_data.get('numero_documento_nit')
        
        # Validación adicional de consistencia entre tipo y número de documento
        if tipo_documento and numero_documento:
            # Aquí puedes agregar validaciones cruzadas adicionales si es necesario
            pass
        
        return cleaned_data