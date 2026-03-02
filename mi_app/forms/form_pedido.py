from django import forms
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Select
from mi_app.models import Pedido

class PedidoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Enfocar automáticamente el primer campo (puedes cambiarlo si prefieres otro)
        self.fields['id_cliente'].widget.attrs['autofocus'] = True

    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            'id_cliente': Select(
                attrs={
                    'placeholder': 'Seleccione el cliente',
                }
            ),
            'id_producto': Select(
                attrs={
                    'placeholder': 'Seleccione el producto',
                }
            ),
            'nombre_de_producto': TextInput(
                attrs={
                    'placeholder': 'Nombre del producto',
                }
            ),
            'cantidad': NumberInput(
                attrs={
                    'placeholder': 'Cantidad solicitada',
                    'min': 1
                }
            ),
            'departamento_entrega': TextInput(
                attrs={
                    'placeholder': 'Departamento de entrega',
                }
            ),
            'municipio_ciudad_entrega': TextInput(
                attrs={
                    'placeholder': 'Ciudad o municipio de entrega',
                }
            ),
            'direccion_entrega': TextInput(
                attrs={
                    'placeholder': 'Dirección exacta de entrega',
                }
            ),
            'comprobante_pago': TextInput(
                attrs={
                    'placeholder': 'Estado del comprobante (por defecto: pago exitoso)',
                }
            ),
            'estado_pedido': Select(
                attrs={
                    'placeholder': 'Estado actual del pedido',
                }
            ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'Correo electrónico del cliente',
                }
            ),
        }
