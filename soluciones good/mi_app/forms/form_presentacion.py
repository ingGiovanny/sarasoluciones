from django import forms
from django.forms import ModelForm, TextInput
from mi_app.models import Presentacion

class presentacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Presentacion
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre de la presentación',
                    'class': 'form-control'
                }
            ),
            'color': TextInput(
                attrs={
                    'placeholder': 'Ingrese el color',
                    'class': 'form-control'
                }
            ),
            'modelo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el modelo de la presentacion',
                    'class': 'form-control'
                }
            ),
            'funcion_principal': TextInput(
                attrs={
                    'placeholder': 'Cuál es la función principal',
                    'class': 'form-control'
                }
            ),
            'descripcion': TextInput(
                attrs={


                    'placeholder': 'Ingrese una breve descripción',
                    'class': 'form-control'
                }
            ),
        }