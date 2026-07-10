from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegistrationForm
from .services import (
    authenticate_user,
    login_user,
    logout_user,
    register_user,
)


def register_view(request):
    if request.user.is_authenticated:
        return redirect(
            "courses:discipline_list"
        )

    if request.method == "POST":
        form = RegistrationForm(
            request.POST
        )

        if form.is_valid():
            user = register_user(
                username=form.cleaned_data[
                    "username"
                ],
                email=form.cleaned_data[
                    "email"
                ],
                full_name=form.cleaned_data[
                    "full_name"
                ],
                password=form.cleaned_data[
                    "password1"
                ],
            )

            login_user(
                request=request,
                user=user,
            )

            messages.success(
                request,
                "Регистрация успешно завершена.",
            )

            return redirect(
                "courses:discipline_list"
            )

    else:
        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect(
            "courses:discipline_list"
        )

    next_url = (
        request.POST.get("next")
        or request.GET.get("next")
        or ""
    )

    if request.method == "POST":
        form = LoginForm(
            request.POST
        )

        if form.is_valid():
            user = authenticate_user(
                request=request,
                username=form.cleaned_data[
                    "username"
                ],
                password=form.cleaned_data[
                    "password"
                ],
            )

            if user is None:
                form.add_error(
                    None,
                    "Неверный логин или пароль.",
                )

            else:
                login_user(
                    request=request,
                    user=user,
                )

                messages.success(
                    request,
                    "Вы успешно вошли в систему.",
                )

                if (
                    next_url
                    and url_has_allowed_host_and_scheme(
                        next_url,
                        allowed_hosts={
                            request.get_host()
                        },
                        require_https=(
                            request.is_secure()
                        ),
                    )
                ):
                    return redirect(next_url)

                return redirect(
                    "courses:discipline_list"
                )

    else:
        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
            "next": next_url,
        },
    )


@login_required
@require_POST
def logout_view(request):
    logout_user(
        request=request
    )

    return redirect(
        "courses:discipline_list"
    )