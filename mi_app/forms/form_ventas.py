from django import forms
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, PasswordInput, Select
from mi_app.models import Ventas

class ventasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_pedido'].widget.attrs['autofocus'] = True

    class Meta:
        model = Ventas
        fields = '__all__'
        widgets = {
            'id_pedido': Select(
                attrs={
                    'placeholder': 'Ingrese el nombre del administrador',
                }
            ),
            'comprobante_pago': EmailInput(
                attrs={
                    'placeholder': 'Ingrese el correo del administrador',
                }
            ),
            'fecha_venta': PasswordInput(
                attrs={
                    'placeholder': 'Ingrese la contraseña',
                }
            ),
            'id_administrador': NumberInput(
                attrs={
                    'placeholder': 'Ingrese la cédula',
                }
            )
        }
