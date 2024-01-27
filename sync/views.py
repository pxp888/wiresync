from django.shortcuts import render, get_object_or_404

# Create your views here.

def welcome(request):
    return render(
        request,
        "sync/welcome.html",
    )


