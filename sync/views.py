from django.shortcuts import render, get_object_or_404

# Create your views here.

def welcome(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == 'login':
            return render(request, "sync/welcome.html", {'error':'bad key'} )
        if action == 'create':
            return render(request, "sync/home.html", )
        
    else:
        return render(request, "sync/welcome.html", )



