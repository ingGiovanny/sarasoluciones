from django import forms
from django.forms import ModelForm, TextInput, Textarea
from mi_app.models import GestionServicio

class GestionServicioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_servicio'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = GestionServicio
        fields = '__all__'
        widgets = {
            'nombre_servicio': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del servicio',
                    'class': 'form-control',
                }
            ),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción del servicio',
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
            'valor': TextInput(
                attrs={
                    'placeholder': 'Ingrese el valor del servicio',
                    'class': 'form-control',
                }
            ),
        }