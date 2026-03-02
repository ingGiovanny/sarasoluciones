from django import forms
from mi_app.models import GestionServicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = GestionServicio
        fields = '__all__' # Usar todos los campos del modelo
        
        # Widgets para darle estilo Bootstrap a los inputs
        widgets = {
            'nombre_servicio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Capacitación Alturas'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_anterior': forms.NumberInput(attrs={'class': 'form-control'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion_breve': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'descripcion_detallada': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'duracion': forms.TextInput(attrs={'class': 'form-control'}),
            'modalidad': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'incluye_certificado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }