from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil
from .models import Curso
from .models import Recurso


class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        label="Correo Electrónico",
        required=True,
        error_messages={'required': 'Por favor, ingresa un correo válido'}
    )

    rol = forms.ChoiceField(
        choices=Perfil.ROLES,
        label="Rol",
        required=True,
        error_messages={'required': 'Selecciona un rol'}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Perfil.objects.create(usuario=user, rol=self.cleaned_data['rol'])
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username
    
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'descripcion']


class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recurso
        fields = ['descripcion', 'archivo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }