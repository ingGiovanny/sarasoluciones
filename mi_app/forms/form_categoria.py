from django import forms
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, PasswordInput
from mi_app.models import Categoria

class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_categoria'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'nombre de la categoria': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre de una categoria',
                }
            ),
            'Descripcion ': TextInput(
                attrs={
                    'placeholder': 'ingrese la descripcion de la categoria',
                }
            )
        }