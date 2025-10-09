from django import forms
from django.forms import ModelForm, TextInput, Select, Textarea
from mi_app.models import Proveedor

class ProveedorForm(ModelForm):
    # Opciones para tipo de documento
    TIPO_DOCUMENTO_CHOICES = [
        ('', 'Seleccione tipo de documento'),
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('TI', 'Tarjeta de Identidad'),
        ('PASAPORTE', 'Pasaporte'),
        ('NIT', 'Número de Identificación Tributaria (NIT)'),
        ('RUT', 'Registro Único Tributario (RUT)'),
        ('DNI', 'Documento Nacional de Identidad'),
        ('PPT', 'Permiso por Protección Temporal'),
        ('CD', 'Carné Diplomático'),
    ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_completo'].widget.attrs['autofocus'] = True
        
        # Agregar choices al campo tipo_documento
        self.fields['tipo_documento'].widget = Select(choices=self.TIPO_DOCUMENTO_CHOICES)
    
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre_completo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre completo del proveedor',
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
                    'class': 'form-control'
                }
            ),
            'direccion_empresa': TextInput(
                attrs={
                    'placeholder': 'Ingrese la dirección de la empresa',
                    'class': 'form-control'
                }
            ),
            'numero_telefonico': TextInput(
                attrs={
                    'placeholder': 'Ingrese el número telefónico',
                    'class': 'form-control'
                }
            ),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción del proveedor',
                    'class': 'form-control',
                    'rows': 3
                }
            ),
        }
    
    def clean_numero_documento_nit(self):
        """Validación personalizada para el número de documento/NIT"""
        numero = self.cleaned_data['numero_documento_nit']
        tipo_doc = self.cleaned_data.get('tipo_documento')
        
        # Validaciones específicas según el tipo de documento
        if tipo_doc == 'NIT':
            if len(numero) < 9:
                raise forms.ValidationError("El NIT debe tener al menos 9 dígitos")
        elif tipo_doc == 'CC':
            if not numero.isdigit():
                raise forms.ValidationError("La cédula de ciudadanía debe contener solo números")
        elif tipo_doc == 'CE':
            if len(numero) < 6:
                raise forms.ValidationError("La cédula de extranjería debe tener al menos 6 caracteres")
        
        return numero
    
    def clean(self):
        """Validación general del formulario"""
        cleaned_data = super().clean()
        tipo_documento = cleaned_data.get('tipo_documento')
        numero_documento = cleaned_data.get('numero_documento_nit')
        
        if not tipo_documento:
            raise forms.ValidationError("Debe seleccionar un tipo de documento")
        
        if not numero_documento:
            raise forms.ValidationError("Debe ingresar el número de documento")
        
        return cleaned_data