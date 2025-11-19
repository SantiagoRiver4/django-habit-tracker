from django import forms
from .models import Habit, HabitRecord, Calificacion

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["habit_text", "description"]
        labels = {"habit_text": "Nombre del hábito", "description": "Descripción"}
        widgets = {
            "habit_text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Leer 20 minutos"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean_habit_text(self):
        habit_text = self.cleaned_data.get("habit_text", "").strip()
        if len(habit_text) < 3:
            raise forms.ValidationError("El nombre del hábito debe tener al menos 3 caracteres.")
        return habit_text


class HabitRecordForm(forms.ModelForm):
    class Meta:
        model = HabitRecord
        fields = ["notes", "progress"]
        labels = {"notes": "Notas", "progress": "Progreso"}
        widgets = {
            "notes": forms.TextInput(attrs={"class": "form-control", "placeholder": "Breve nota"}),
            "progress": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 100}),
        }


class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['nombre_usuario', 'calificacion', 'comentario']  # ← añadimos comentario
        widgets = {
            'nombre_usuario': forms.TextInput(attrs={
                'placeholder': 'Tu nombre',
                'class': 'form-control',
            }),
            'calificacion': forms.HiddenInput(),  # el valor real lo maneja JS; dejamos hidden para recibir el entero
            'comentario': forms.Textarea(attrs={
                'placeholder': 'Escribe un comentario (opcional)',
                'rows': 3,
                'class': 'form-control',
            }),
        }
        labels = {
            'nombre_usuario': 'Nombre',
            'calificacion': 'Calificación (1-5)',
            'comentario': 'Comentario',
        }
