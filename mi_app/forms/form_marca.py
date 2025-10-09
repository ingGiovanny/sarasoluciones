from django import forms
from django.forms import ModelForm, TextInput, DateTimeInput, ClearableFileInput
from mi_app.models import Marca




class MarcaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_marca'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Marca
        fields = '__all__'
        widgets = {
            'nombre_marca': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre de la marca',
                    'class': 'form-control'
                }
            ),
            'fecha_registro': DateTimeInput(
                attrs={
                    'placeholder': 'Seleccione la fecha y hora de registro',
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
            'logo_marca': ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    #'accept': 'image/*'
                }
            ),
        }