from django import forms
from django.forms import ModelForm, Select, FileInput, DateInput
from django.core.exceptions import ValidationError
from mi_app.models import Ventas
from datetime import date, datetime
import os

class ventasForm(ModelForm): 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar autofocus en el primer campo relevante
        if 'id_pedido' in self.fields:
            self.fields['id_pedido'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Ventas
        fields = '__all__'
        widgets = {
            'id_pedido': Select(
                attrs={
                    'placeholder': 'Seleccione el pedido',
                    'class': 'form-control'
                }
            ),
            'comprobante_pago': FileInput(  # Cambiado a FileInput para archivos
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*,.pdf'  # Solo imágenes y PDFs
                }
            ),
            'fecha_venta': DateInput(  # Cambiado a DateInput
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'max': date.today().isoformat()  # No permitir fechas futuras
                }
            ),
            'id_administrador': Select(  # Cambiado a Select si es FK
                attrs={
                    'placeholder': 'Seleccione el administrador',
                    'class': 'form-control'
                }
            ),
        }
    
    def clean_id_pedido(self):
        pedido = self.cleaned_data.get('id_pedido')
        
        if not pedido:
            raise ValidationError('Debe seleccionar un pedido')
        
        # Validar que el pedido no tenga ya una venta registrada (excepto en edición)
        if self.instance.pk:  # Si es edición
            if Ventas.objects.exclude(pk=self.instance.pk).filter(id_pedido=pedido).exists():
                raise ValidationError('Este pedido ya tiene una venta registrada')
        else:  # Si es creación
            if Ventas.objects.filter(id_pedido=pedido).exists():
                raise ValidationError('Este pedido ya tiene una venta registrada')
        
        return pedido
    
    def clean_comprobante_pago(self):
        comprobante = self.cleaned_data.get('comprobante_pago')
        
        if not comprobante:
            raise ValidationError('El comprobante de pago es obligatorio')
        
        # Validar el tamaño del archivo (máximo 5MB)
        if hasattr(comprobante, 'size'):
            max_size = 5 * 1024 * 1024  # 5MB en bytes
            if comprobante.size > max_size:
                raise ValidationError('El archivo no puede superar los 5MB')
        
        # Validar la extensión del archivo
        if hasattr(comprobante, 'name'):
            ext = os.path.splitext(comprobante.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.gif']
            if ext not in valid_extensions:
                raise ValidationError(f'Formato de archivo no válido. Permitidos: {", ".join(valid_extensions)}')
        
        return comprobante
    
    def clean_fecha_venta(self):
        fecha = self.cleaned_data.get('fecha_venta')
        
        if not fecha:
            raise ValidationError('La fecha de venta es obligatoria')
        
        # Convertir a date si es datetime
        if isinstance(fecha, datetime):
            fecha = fecha.date()
        
        # Validar que no sea una fecha futura
        if fecha > date.today():
            raise ValidationError('La fecha de venta no puede ser futura')
        
        # Validar que no sea muy antigua (por ejemplo, no más de 1 año atrás)
        fecha_minima = date.today().replace(year=date.today().year - 1)
        if fecha < fecha_minima:
            raise ValidationError('La fecha de venta no puede ser mayor a 1 año atrás')
        
        return fecha
    
    def clean_id_administrador(self):
        administrador = self.cleaned_data.get('id_administrador')
        
        if not administrador:
            raise ValidationError('Debe seleccionar un administrador')
        
        # Aquí puedes agregar validaciones adicionales si es necesario
        # Por ejemplo, validar que el administrador esté activo
        
        return administrador
    
    def clean(self):
        """Validación general del formulario"""
        cleaned_data = super().clean()
        
        pedido = cleaned_data.get('id_pedido')
        fecha_venta = cleaned_data.get('fecha_venta')
        
        # Validación cruzada: la fecha de venta debe ser posterior o igual a la fecha del pedido
        if pedido and fecha_venta:
            if hasattr(pedido, 'fecha_pedido'):
                fecha_pedido = pedido.fecha_pedido
                if isinstance(fecha_pedido, datetime):
                    fecha_pedido = fecha_pedido.date()
                
                if fecha_venta < fecha_pedido:
                    raise ValidationError('La fecha de venta no puede ser anterior a la fecha del pedido')
        
        return cleaned_data