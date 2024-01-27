from django.shortcuts import render, redirect, get_object_or_404
from .models import nwork, peer 
import hashlib



# Create your views here.

'''helper - This checks if the session is valid or not'''
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


'''This is the welcome page'''
def welcome(request):
    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'login':
            return login(request)
        elif action == 'create':
            return createNwork(request)
    else:
        if check_session(request):
            return redirect('home')
        else:
            return render(request, 'sync/welcome.html', {'msg':''})


'''this responds to login requests'''
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


'''this responds to create requests'''
def createNwork(request):
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


'''this is the home page'''
def home(request):
    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'logout':
            request.session.flush()
            return redirect('/')
    else:
        if check_session(request):
            name = request.session.get('name','')
            peers = peer.objects.filter(nwork__name=name)
            return render(request, 'sync/home.html', {'name':name, 'peers':peers})
        else:
            return redirect('/')

