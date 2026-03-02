from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomPasswordResetForm(PasswordResetForm):
    
    # Sobrescribimos clean_email para forzar la validación de existencia
    def clean_email(self):
        email = self.cleaned_data['email']
        
        # Busca usuarios activos con ese email
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            #Lanza la excepción si no lo encuentra. Esto detiene el flujo.
            raise ValidationError(
                ("El correo electrónico no está registrado en el sistema."),
                code='no_user',
            )
            
        return email