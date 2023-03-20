from django.shortcuts import render

def landing(request):
    return render(
        request,
        'main/landing.html'
    )

def main(request):
    return render(
        request,
        'main/main.html'
    )