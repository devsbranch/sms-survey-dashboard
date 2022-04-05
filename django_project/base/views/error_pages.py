from django.shortcuts import render


def error_403(request, *args, **kwargs):
    return render(request, "page-403.html")


def error_404(request, *args, **kwargs):
    return render(request, "page-404.html")


def error_500(request, *args, **kwargs):
    return render(request, "page-500.html")
