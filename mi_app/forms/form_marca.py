from django import forms
from django.forms import ModelForm, TextInput, ClearableFileInput
from mi_app.models import Marca

class MarcaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_marca'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Marca
        # Excluir fecha_registro porque tiene auto_now_add=True
        fields = ['nombre_marca', 'logo_marca']
        widgets = {
            'nombre_marca': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre de la marca',
                    'class': 'form-control'
                }
            ),
            'logo_marca': ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*'
                }
            ),
        }