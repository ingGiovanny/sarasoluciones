from django import forms
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, PasswordInput, Select, DateInput
from mi_app.models import Compra

class CompraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cantidad_productos'].widget.attrs['autofocus'] = True

    class Meta:
        model = Compra
        fields = '__all__'
        widgets = {
            'id_administrador': Select(
                attrs={
                    'placeholder': 'Ingrese el id del administrador',
                }
            ),
            'id_proveedor': Select(
                attrs={
                    'placeholder': 'Ingrese el id del proveedor',
                }
            ),
            'id_producto': Select(
                attrs={
                    'placeholder': 'Ingrese el id del producto',
                }
            ),
            'cantidad_productos': NumberInput(
                attrs={
                    'placeholder': 'Ingrese la cantidad de productos',
                }
            ),
            'observaciones': TextInput(
                attrs={
                    'placeholder': 'Ingrese las observaciones',
                }
            ),
            'fecha_compra': DateInput(
                attrs={
                    'placeholder': 'Ingrese la fecha de la compra',
                }
            ),   
            'valor_total': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el valor total',
                }
            ),
        }
