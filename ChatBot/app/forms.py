from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Curso,Asignatura,Contenido
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
       model = User
       fields = ["username","first_name","last_name","email","password1","password2"]


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre']


class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre']

class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = ['nombre', 'descripcion','presentacion']