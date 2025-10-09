from django import forms
from django.forms import ModelForm, TextInput, NumberInput, Select
from mi_app.models import Producto

class ProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_producto'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Producto
        fields = ['id_categoria', 'id_marca', 'id_presentacion', 'nombre_producto', 
                 'cantidad_producto', 'valor_unitario', 'estado_producto']
        widgets = {
            'id_categoria': Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_marca': Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_presentacion': Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'nombre_producto': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del producto',
                }
            ),
            'cantidad_producto': NumberInput(
                attrs={
                    'placeholder': 'Ingrese la cantidad disponible',
                    'min': '0',
                }
            ),
            'valor_unitario': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el valor unitario',
                    'step': '1',
                    'min': '0.01',
                }
            ),
            'estado_producto': Select(
                choices=[
                    ('', 'Seleccione el estado'),
                    ('nuevo', 'Nuevo'),
                    ('usado', 'Usado'),
                    ('reacondicionado', 'Reacondicionado'),
                ],
                attrs={
                    'class': 'form-control',
                }
            ),
        }