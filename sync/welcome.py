from django.shortcuts import render, redirect
from .models import nwork
from .xsession import check_session, set_session

import hashlib

# Create your views here.


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
            set_session(request)
            return redirect('home')
        else:
            return render(request, 'sync/welcome.html', {'name':name, 'msg':'Wrong password'})
    except nwork.DoesNotExist:
        return render(request, 'sync/welcome.html', {'name':name, 'msg':'Name not found'})
    except Exception as e:
        return render(request, 'sync/welcome.html', {'name':name, 'msg':str(e)})


'''this responds to create requests'''
def createNwork(request):
    name = request.POST.get('netname')
    password = request.POST.get('password')
    khash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    try:
        n = nwork.objects.get(name=name)
        return render(request, 'sync/welcome.html', {'name':name, 'msg':'Name already exists'})
    except nwork.DoesNotExist:
        n = nwork(name=name, khash=khash)
        n.save()
        set_session(request)
        return redirect('home')
    except Exception as e:
        return render(request, 'sync/welcome.html', {'name':name, 'msg':str(e)})


'''this logs the user out'''
def logout(request):
    request.session.flush()
    return redirect('/')
