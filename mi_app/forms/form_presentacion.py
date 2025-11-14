from django import forms
from django.forms import ModelForm, TextInput, Textarea
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from mi_app.models import Presentacion
import re

class presentacionForm(ModelForm):  
    
    # Validadores
    nombre_validator = RegexValidator(
        regex=r'^[a-záéíóúñA-ZÁÉÍÓÚÑ0-9\s.,-]+$',
        message='El nombre solo debe contener letras, números, espacios y caracteres válidos (. , -)'
    )
    
    color_validator = RegexValidator(
        regex=r'^[a-záéíóúñA-ZÁÉÍÓÚÑ\s,/]+$',
        message='El color solo debe contener letras, espacios, comas y barras'
    )
    
    modelo_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9\s\-./]+$',
        message='El modelo debe contener solo letras, números, espacios, guiones, puntos o barras'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
        # Agregar validadores
        self.fields['nombre'].validators.append(self.nombre_validator)
        self.fields['color'].validators.append(self.color_validator)
        self.fields['modelo'].validators.append(self.modelo_validator)
    
    class Meta:
        model = Presentacion
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ej: Camiseta Deportiva, Zapatos Casuales',
                    'maxlength': '100',
                    'class': 'form-control'
                }
            ),
            'color': TextInput(
                attrs={
                    'placeholder': 'Ej: Rojo, Azul marino, Negro/Blanco',
                    'maxlength': '50',
                    'class': 'form-control'
                }
            ),
            'modelo': TextInput(
                attrs={
                    'placeholder': 'Ej: MOD-2024, PRO-X1, Classic-V2',
                    'maxlength': '50',
                    'class': 'form-control'
                }
            ),
            'funcion_principal': TextInput(
                attrs={
                    'placeholder': 'Ej: Para uso deportivo, Vestir casual, Protección solar',
                    'maxlength': '150',
                    'class': 'form-control'
                }
            ),
            'descripcion': Textarea(  # Cambié a Textarea para mejor experiencia
                attrs={
                    'placeholder': 'Ingrese una descripción detallada de la presentación del producto',
                    'class': 'form-control',
                    'rows': 4,
                    'maxlength': '500'
                }
            ),
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        
        if not nombre:
            raise ValidationError('El nombre de la presentación es obligatorio')
        
        if len(nombre) < 3:
            raise ValidationError('El nombre debe tener al menos 3 caracteres')
        
        if len(nombre) > 100:
            raise ValidationError('El nombre no puede exceder los 100 caracteres')
        
        # Validar caracteres permitidos
        if not re.match(r'^[a-záéíóúñA-ZÁÉÍÓÚÑ0-9\s.,-]+$', nombre):
            raise ValidationError('El nombre solo debe contener letras, números, espacios y caracteres válidos (. , -)')
        
        # Validar que no sea solo números
        if nombre.replace(' ', '').isdigit():
            raise ValidationError('El nombre no puede contener solo números')
        
        # Validar duplicados (excepto en edición)
        if self.instance.pk:  # Si es edición
            if Presentacion.objects.exclude(pk=self.instance.pk).filter(nombre__iexact=nombre).exists():
                raise ValidationError('Ya existe una presentación con este nombre')
        else:  # Si es creación
            if Presentacion.objects.filter(nombre__iexact=nombre).exists():
                raise ValidationError('Ya existe una presentación con este nombre')
        
        return nombre
    
    def clean_color(self):
        color = self.cleaned_data.get('color', '').strip()
        
        if not color:
            raise ValidationError('El color es obligatorio')
        
        if len(color) < 2:
            raise ValidationError('El color debe tener al menos 2 caracteres')
        
        if len(color) > 50:
            raise ValidationError('El color no puede exceder los 50 caracteres')
        
        # Validar caracteres permitidos (letras, espacios, comas, barras para combinaciones)
        if not re.match(r'^[a-záéíóúñA-ZÁÉÍÓÚÑ\s,/]+$', color):
            raise ValidationError('El color solo debe contener letras, espacios, comas y barras (para combinaciones)')
        
        # Validar que no contenga números
        if any(char.isdigit() for char in color):
            raise ValidationError('El color no debe contener números')
        
        return color
    
    def clean_modelo(self):
        modelo = self.cleaned_data.get('modelo', '').strip()
        
        if not modelo:
            raise ValidationError('El modelo es obligatorio')
        
        if len(modelo) < 2:
            raise ValidationError('El modelo debe tener al menos 2 caracteres')
        
        if len(modelo) > 50:
            raise ValidationError('El modelo no puede exceder los 50 caracteres')
        
        # Validar caracteres permitidos (alfanumérico con guiones, puntos, barras)
        if not re.match(r'^[a-zA-Z0-9\s\-./]+$', modelo):
            raise ValidationError('El modelo debe contener solo letras, números, espacios, guiones, puntos o barras')
        
        # Validar duplicados (excepto en edición)
        if self.instance.pk:  # Si es edición
            if Presentacion.objects.exclude(pk=self.instance.pk).filter(modelo__iexact=modelo).exists():
                raise ValidationError('Ya existe una presentación con este modelo')
        else:  # Si es creación
            if Presentacion.objects.filter(modelo__iexact=modelo).exists():
                raise ValidationError('Ya existe una presentación con este modelo')
        
        return modelo
    
    def clean_funcion_principal(self):
        funcion = self.cleaned_data.get('funcion_principal', '').strip()
        
        if not funcion:
            raise ValidationError('La función principal es obligatoria')
        
        if len(funcion) < 5:
            raise ValidationError('La función principal debe tener al menos 5 caracteres')
        
        if len(funcion) > 150:
            raise ValidationError('La función principal no puede exceder los 150 caracteres')
        
        # Validar que contenga al menos algunas letras
        if not re.search(r'[a-záéíóúñA-ZÁÉÍÓÚÑ]', funcion):
            raise ValidationError('La función principal debe contener texto válido')
        
        return funcion
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '').strip()
        
        # La descripción puede ser opcional
        if descripcion:
            if len(descripcion) < 10:
                raise ValidationError('La descripción debe tener al menos 10 caracteres')
            
            if len(descripcion) > 500:
                raise ValidationError('La descripción no puede exceder los 500 caracteres')
            
            # Validar que contenga contenido significativo
            if not re.search(r'[a-záéíóúñA-ZÁÉÍÓÚÑ]', descripcion):
                raise ValidationError('La descripción debe contener texto válido')
        
        return descripcion
    
    def clean(self):
        """Validación general del formulario"""
        cleaned_data = super().clean()
        
        nombre = cleaned_data.get('nombre', '')
        modelo = cleaned_data.get('modelo', '')
        
        # Validación adicional: el nombre y modelo no pueden ser idénticos
        if nombre and modelo and nombre.lower() == modelo.lower():
            raise ValidationError('El nombre y el modelo no pueden ser idénticos')
        
        return cleaned_data