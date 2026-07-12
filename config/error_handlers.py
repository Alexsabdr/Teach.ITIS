from django.shortcuts import render


def page_not_found(request, exception):
    """
    Обработчик ошибки 404.
    """

    error_message = (
        "Запрашиваемая страница или объект не найдены."
    )

    return render(
        request,
        "errors/404",
        {
            "error_message": error_message,
        },
        status=404,
    )


def permission_denied(request, exception):
    """
    Обработчик ошибки 403.
    """

    error_message = (
        str(exception)
        or "У вас недостаточно прав для выполнения этого действия."
    )

    return render(
        request,
        "errors/403.html",
        {
            "error_message": error_message,
        },
        status=403,
    )