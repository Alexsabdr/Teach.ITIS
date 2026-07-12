from django import forms

from .models import Discipline, Topic


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


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic

        fields = [
            "title",
            "slug",
            "description",
            "order_number",
        ]

        labels = {
            "title": "Название темы",
            "slug": "Адрес страницы",
            "description": "Описание",
            "order_number": "Порядковый номер",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Например: Модели Django",
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "placeholder": "Например: django-models",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "Описание темы",
                }
            ),

            "order_number": forms.NumberInput(
                attrs={
                    "min": 1,
                }
            ),
        }

    def __init__(
            self,
            *args,
            discipline=None,
            **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )

        self.discipline = (
                discipline
                or getattr(
            self.instance,
            "discipline",
            None,
        )
        )

    def clean_title(self):
        title = (
            self.cleaned_data["title"]
            .strip()
        )

        if len(title) < 3:
            raise forms.ValidationError(
                "Название темы должно содержать "
                "минимум 3 символа."
            )

        if self.discipline:
            duplicate = (
                Topic.objects
                .filter(
                    discipline=self.discipline,
                    title__iexact=title,
                )
                .exclude(
                    pk=self.instance.pk,
                )
                .exists()
            )

            if duplicate:
                raise forms.ValidationError(
                    "Тема с таким названием "
                    "уже существует в этой дисциплине."
                )

        return title

    def clean_slug(self):
        slug = (
            self.cleaned_data["slug"]
            .strip()
            .lower()
        )

        if self.discipline:
            duplicate = (
                Topic.objects
                .filter(
                    discipline=self.discipline,
                    slug__iexact=slug,
                )
                .exclude(
                    pk=self.instance.pk,
                )
                .exists()
            )

            if duplicate:
                raise forms.ValidationError(
                    "Этот адрес уже используется "
                    "другой темой дисциплины."
                )

        return slug

    def clean_order_number(self):
        order_number = (
            self.cleaned_data[
                "order_number"
            ]
        )

        if order_number < 1:
            raise forms.ValidationError(
                "Порядковый номер должен "
                "быть больше нуля."
            )

        return order_number
