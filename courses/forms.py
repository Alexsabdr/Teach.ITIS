from django import forms

from .models import Discipline


class DisciplineForm(
    forms.ModelForm
):
    class Meta:
        model = Discipline

        fields = [
            "title",
            "slug",
            "description",
        ]

        labels = {
            "title":
                "Название дисциплины",

            "slug":
                "Адрес страницы",

            "description":
                "Описание",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder":
                        "Например: Основы Django",
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "placeholder":
                        "Например: django-basics",
                }
            ),

            "description":
                forms.Textarea(
                    attrs={
                        "rows": 6,

                        "placeholder":
                            "Краткое описание "
                            "дисциплины",
                    }
                ),
        }


    def clean_title(self):
        title = (
            self.cleaned_data[
                "title"
            ]
            .strip()
        )

        if len(title) < 3:
            raise forms.ValidationError(
                "Название должно содержать "
                "минимум 3 символа."
            )

        duplicate = (
            Discipline.objects
            .filter(
                title__iexact=title
            )
            .exclude(
                pk=self.instance.pk
            )
            .exists()
        )

        if duplicate:
            raise forms.ValidationError(
                "Дисциплина с таким "
                "названием уже существует."
            )

        return title


    def clean_slug(self):
        slug = (
            self.cleaned_data[
                "slug"
            ]
            .strip()
            .lower()
        )

        duplicate = (
            Discipline.objects
            .filter(
                slug__iexact=slug
            )
            .exclude(
                pk=self.instance.pk
            )
            .exists()
        )

        if duplicate:
            raise forms.ValidationError(
                "Этот адрес уже используется."
            )

        return slug


    def clean_description(self):
        description = (
            self.cleaned_data[
                "description"
            ]
            .strip()
        )

        if (
            description
            and len(description) < 10
        ):
            raise forms.ValidationError(
                "Описание должно содержать "
                "минимум 10 символов."
            )

        return description