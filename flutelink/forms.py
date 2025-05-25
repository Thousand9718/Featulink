from django import forms
from .models import *

class UsuarioDisciplinaForm(forms.ModelForm):
    class Meta:
        model = UsuarioDisciplina
        fields = ['usuario', 'disciplina']


# Formulario para Cantante
class CantanteForm(forms.ModelForm):
    GENERO_CHOICES = [
        ('Rap', 'Rap'),
        ('Trap', 'Trap'),
        ('Detroit', 'Detroit'),
        ('Drill', 'Drill'),
        ('Hyperpop', 'Hyperpop'),
        ('Reggaeton', 'Reggaeton'),
        ('Dancehall', 'Dancehall'),
        ('Reggae', 'Reggae'),
        ('Dembow', 'Dembow'),
    ]

    genero = forms.ChoiceField(choices=GENERO_CHOICES)
    busca = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Cantante
        fields = ['genero', 'experiencia', 'ubicacion_lat', 'ubicacion_lng', 'busca']
        widgets = {
            'ubicacion_lat': forms.HiddenInput(),
            'ubicacion_lng': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disciplinas dinámicas desde el modelo
        self.fields['busca'].choices = [
            (disc.nombre.lower(), disc.nombre) for disc in Disciplina.objects.all()
        ]

        # Para edición: rellenar valores ya guardados
        if self.instance and self.instance.busca:
            self.initial['busca'] = self.instance.busca.split(',')

    def clean_busca(self):
        return ','.join(self.cleaned_data['busca'])


# Formulario para Breaker
class BailarinForm(forms.ModelForm):
    ESTILO_CHOICES = [
        ('Breakdance', 'Breakdance'),
        ('Popping', 'Popping'),
        ('Locking', 'Locking'),
        ('Krump', 'Krump'),
        ('Hip Hop', 'Hip Hop'),
        ('House', 'House'),
        ('Litefeet', 'Litefeet'),
        ('Waacking', 'Waacking'),
        ('Vogue', 'Vogue'),
        ('Dancehall', 'Dancehall'),
        ('Afro', 'Afro'),
        ('Experimental', 'Experimental'),
        ('Freestyle', 'Freestyle'),
        ('Otros', 'Otros'),
    ]

    estilo = forms.ChoiceField(choices=ESTILO_CHOICES)
    busca = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Bailarin
        fields = ['crew', 'estilo', 'experiencia', 'ubicacion_lat', 'ubicacion_lng', 'busca']
        widgets = {
            'ubicacion_lat': forms.HiddenInput(),
            'ubicacion_lng': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disciplinas dinámicas desde el modelo
        self.fields['busca'].choices = [
            (disc.nombre.lower(), disc.nombre) for disc in Disciplina.objects.all()
        ]

        # Para edición: rellenar valores ya guardados
        if self.instance and self.instance.busca:
            self.initial['busca'] = self.instance.busca.split(',')

    def clean_busca(self):
        return ','.join(self.cleaned_data['busca'])


# Formulario para Grafitero
class GrafiteroForm(forms.ModelForm):
    ESTILO_CHOICES = [
        ('Wildstyle', 'Wildstyle'),
        ('Throw-up', 'Throw-up'),
        ('Tag', 'Tag'),
        ('Stencil', 'Stencil'),
        ('Blockbuster', 'Blockbuster'),
        ('Bubble', 'Bubble'),
        ('3D', '3D'),
        ('Character', 'Character'),
        ('Abstracto', 'Abstracto'),
        ('Calligraffiti', 'Calligraffiti'),
        ('Otros', 'Otros'),
    ]

    estilo = forms.ChoiceField(choices=ESTILO_CHOICES)
    busca = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Grafitero
        fields = ['estilo', 'tag', 'ubicacion_lat', 'ubicacion_lng', 'busca']
        widgets = {
            'ubicacion_lat': forms.HiddenInput(),
            'ubicacion_lng': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disciplinas dinámicas desde el modelo
        self.fields['busca'].choices = [
            (disc.nombre.lower(), disc.nombre) for disc in Disciplina.objects.all()
        ]

        # Para edición: rellenar valores ya guardados
        if self.instance and self.instance.busca:
            self.initial['busca'] = self.instance.busca.split(',')

    def clean_busca(self):
        return ','.join(self.cleaned_data['busca'])


# Formulario para Instrumentista
class InstrumentistaForm(forms.ModelForm):
    INSTRUMENTO_CHOICES = [
        ('Guitarra', 'Guitarra'),
        ('Bajo', 'Bajo'),
        ('Batería', 'Batería'),
        ('Piano', 'Piano'),
        ('Teclado', 'Teclado'),
        ('Violín', 'Violín'),
        ('Viola', 'Viola'),
        ('Violonchelo', 'Violonchelo'),
        ('Contrabajo', 'Contrabajo'),
        ('Trompeta', 'Trompeta'),
        ('Trombón', 'Trombón'),
        ('Tuba', 'Tuba'),
        ('Saxofón', 'Saxofón'),
        ('Clarinete', 'Clarinete'),
        ('Flauta', 'Flauta'),
        ('Oboe', 'Oboe'),
        ('Fagot', 'Fagot'),
        ('Armónica', 'Armónica'),
        ('Percusión', 'Percusión'),
        ('DJ', 'DJ'),
        ('Sintetizador', 'Sintetizador'),
        ('Banjo', 'Banjo'),
        ('Mandolina', 'Mandolina'),
        ('Ukelele', 'Ukelele'),
        ('Acordeón', 'Acordeón'),
        ('Didgeridoo', 'Didgeridoo'),
        ('Theremin', 'Theremin'),
        ('Otro', 'Otro'),
    ]

    instrumento = forms.ChoiceField(choices=INSTRUMENTO_CHOICES)
    busca = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Instrumentista
        fields = ['instrumento', 'nivel', 'experiencia', 'ubicacion_lat', 'ubicacion_lng', 'busca']
        widgets = {
            'ubicacion_lat': forms.HiddenInput(),
            'ubicacion_lng': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disciplinas dinámicas desde el modelo
        self.fields['busca'].choices = [
            (disc.nombre.lower(), disc.nombre) for disc in Disciplina.objects.all()
        ]

        # Para edición: rellenar valores ya guardados
        if self.instance and self.instance.busca:
            self.initial['busca'] = self.instance.busca.split(',')

    def clean_busca(self):
        return ','.join(self.cleaned_data['busca'])


# Formulario para Productor
class ProductorForm(forms.ModelForm):
    PROGRAMA_CHOICES = [
        ('Ableton Live', 'Ableton Live'),
        ('FL Studio', 'FL Studio'),
        ('Logic Pro', 'Logic Pro'),
        ('Pro Tools', 'Pro Tools'),
        ('Cubase', 'Cubase'),
        ('Reason', 'Reason'),
        ('Studio One', 'Studio One'),
        ('GarageBand', 'GarageBand'),
        ('Bitwig Studio', 'Bitwig Studio'),
        ('Reaper', 'Reaper'),
        ('Otros', 'Otros'),
    ]

    programa = forms.ChoiceField(choices=PROGRAMA_CHOICES)
    busca = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Productor
        fields = ['programa', 'especialidad', 'experiencia', 'ubicacion_lat', 'ubicacion_lng', 'busca']
        widgets = {
            'ubicacion_lat': forms.HiddenInput(),
            'ubicacion_lng': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disciplinas dinámicas
        self.fields['busca'].choices = [
            (disc.nombre.lower(), disc.nombre) for disc in Disciplina.objects.all()
        ]

        # Rellenar datos guardados en edición
        if self.instance and self.instance.busca:
            self.initial['busca'] = self.instance.busca.split(',')

    def clean_busca(self):
        return ','.join(self.cleaned_data['busca'])