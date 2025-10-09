from django import forms
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, PasswordInput, DateInput, Select
from mi_app.models import Factura

class FacturaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_admin'].widget.attrs['autofocus'] = True

    class Meta:
        model = Factura
        fields = '__all__'
        widgets = {
            'id_admin': Select(
                attrs={
                    'placeholder': 'Ingrese el id del administrador',
                }
            ),
            'id_venta': Select(
                attrs={
                    'placeholder': 'Ingrese el id de la venta',
                }
            ),
            'id_servicio': Select(
                attrs={
                    'placeholder': 'Ingrese el id del servicio',
                }
            ),
            'fecha_factura': DateInput(
                attrs={
                    'placeholder': 'Ingrese la fecha de la factura',
                }
            ),
            'descripcion_venta': TextInput(
                attrs={
                    'placeholder': 'Ingrese el detalle de la venta',
                }
            ),
            'terminos_condiciones': TextInput(
                attrs={
                    'placeholder': 'termonos y condiciones',
                }
            ),
            'nit': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el NIT',
                }
            ),
            'total': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el total',
                }
            )
        }
