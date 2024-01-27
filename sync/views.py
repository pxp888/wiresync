from django.shortcuts import render, redirect
from .models import nwork
import hashlib



# Create your views here.
def check_session(request):
    name = request.session.get('name','')
    khash = request.session.get('khash','')
    try:
        n = nwork.objects.get(name=name)
        if n.khash == khash:
            return True
        else:
            return False
    except:
        return False


def welcome(request):
    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'login':
            return login(request)
        elif action == 'create':
            return create(request)
    else:
        if check_session(request):
            return redirect('home')
        else:
            return render(request, 'sync/welcome.html', {'msg':''})


def login(request):
    name = request.POST.get('netname')
    password = request.POST.get('password')
    khash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    try:
        n = nwork.objects.get(name=name)
        if n.khash == khash:
            request.session['name'] = name
            request.session['khash'] = khash
            return redirect('home')
        else:
            return render(request, 'sync/welcome.html', {'msg':'Wrong password'})
    except:
        return render(request, 'sync/welcome.html', {'msg':'Name not found'})


def create(request):
    name = request.POST.get('netname')
    password = request.POST.get('password')
    khash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    try:
        n = nwork.objects.get(name=name)
        return render(request, 'sync/welcome.html', {'msg':'Name already exists'})
    except:
        n = nwork(name=name, khash=khash)
        n.save()
        request.session['name'] = name
        request.session['khash'] = khash
        return redirect('home')


def home(request):
    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'logout':
            request.session.flush()
            return redirect('/')
    else:
        if check_session(request):
            name = request.session.get('name','')
            return render(request, 'sync/home.html', {'name':name})
        else:
            return redirect('/')
