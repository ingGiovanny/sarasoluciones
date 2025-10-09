from django import forms
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, PasswordInput, Select, DateInput
from mi_app.models import Garantia

class GarantiaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_factura'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Garantia
        
        fields = '__all__'
        widgets = {
            'id_factura': Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'descripcion_garantia': TextInput(
                attrs={
                    'placeholder': 'Ingrese la descripcion de la garantia)',
                }
            ),
            'fecha_garantia': DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Seleccione la fecha de garantía',
                }
            ),
            'estado_garantia': Select(
                attrs={
                    'placeholder': 'Ingrese el estado de la garantia',
                }
            )
        }