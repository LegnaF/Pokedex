
from django import forms
from .models import Entrenador, Gym


class FormsEntrenador(forms.ModelForm):

    class Meta:
        model = Entrenador

        fields = [
            'img',
            'documento',
            'nombre',
            'apellido',
            'medallas',
            'liga',
            'clasificacion',
            'pueblo',
            'profesor_asignado',
        ]

        widgets = {
            'img': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL de la imagen del entrenador'
            }),

            'documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Documento'
            }),

            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),

            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),

            'medallas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),

            'liga': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Liga Pokémon'
            }),

            'clasificacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Clasificación'
            }),

            'pueblo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pueblo de origen'
            }),

            'profesor_asignado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Profesor asignado'
            }),
        }







class FormsGym(forms.ModelForm):

    class Meta:
        model = Gym

        fields = [
            'lider_gimnasio',
            'tipo_elemento',
            'medalla',
            'ciudad',
            'telefono',
            'region',
        ]

        widgets = {
            'lider_gimnasio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del líder del gimnasio'
            }),

            'tipo_elemento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: Agua, Fuego, Planta'
            }),

            'medalla': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la medalla'
            }),

            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad del gimnasio'
            }),

            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de contacto'
            }),

            'region': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Región del gimnasio'
            }),
        }