from django import forms
from django.forms import ModelForm, TextInput, NumberInput, Select, DateInput
# IMPORTANTE: Debes importar Proveedor para poder filtrarlo
from mi_app.models import Compra, Proveedor 

class CompraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Filtramos el queryset: ADIÓS a los proveedores inactivos en el Select
        self.fields['id_proveedor'].queryset = Proveedor.objects.filter(activo=True)
        
        # 2. Aplicamos la clase de Bootstrap a TODOS los campos automáticamente
        # Esto incluye a id_proveedor, así que no necesitas la línea repetida
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
            
            # El calendario nativo que configuramos
            'fecha_compra': DateInput(
                attrs={'type': 'date'}, 
                format='%Y-%m-%d'
            ), 
            
            'valor_total': NumberInput(attrs={'placeholder': 'Total de la compra'}),
        }