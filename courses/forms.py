from django import forms

from .models import Discipline


class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline

        fields = [
            "title",
            "slug",
            "description",
        ]

        labels = {
            "title": "Название дисциплины",
            "slug": "Адрес страницы",
            "description": "Описание",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Например: Основы Django",
                }
            ),
            "slug": forms.TextInput(
                attrs={
                    "placeholder": "Например: django-basics",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "Краткое описание дисциплины",
                }
            ),
        }