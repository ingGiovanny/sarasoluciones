from django import forms
from django.forms import ModelForm, TextInput, NumberInput, Select, DateInput
from mi_app.models import Compra

class CompraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicamos la clase de Bootstrap a todos los campos de forma automática
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Compra
        fields = '__all__'
        widgets = {
            'id_administrador': Select(attrs={'placeholder': 'Seleccione administrador'}),
            'id_proveedor': Select(attrs={'placeholder': 'Seleccione proveedor'}),
            'id_producto': Select(attrs={'placeholder': 'Seleccione producto'}),
            'cantidad_productos': NumberInput(attrs={'placeholder': 'Cantidad'}),
            'observaciones': TextInput(attrs={'placeholder': 'Observaciones adicionales'}),
            
            # 🔥 AQUÍ ESTÁ EL CAMBIO: type='date' activa el calendario nativo
            'fecha_compra': DateInput(
                attrs={
                    'type': 'date', 
                    'class': 'form-control'
                }, 
                format='%Y-%m-%d'
            ), 
            
            'valor_total': NumberInput(attrs={'placeholder': 'Total de la compra'}),
        }