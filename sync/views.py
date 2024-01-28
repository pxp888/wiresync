from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import nwork, peer 
import hashlib, time 



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


'''helper - This sets the session'''
def set_session(request):
    name = request.POST.get('netname')
    password = request.POST.get('password')
    khash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    request.session['name'] = name
    request.session['khash'] = khash


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
            return render(request, 'sync/welcome.html', {'msg':'Wrong password'})
    except nwork.DoesNotExist:
        return render(request, 'sync/welcome.html', {'msg':'Name not found'})
    except Exception as e:
        return render(request, 'sync/welcome.html', {'msg':str(e)})


'''this responds to create requests'''
def createNwork(request):
    name = request.POST.get('netname')
    password = request.POST.get('password')
    khash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    try:
        n = nwork.objects.get(name=name)
        return render(request, 'sync/welcome.html', {'msg':'Name already exists'})
    except nwork.DoesNotExist:
        n = nwork(name=name, khash=khash)
        n.save()
        set_session(request)
        return redirect('home')
    except Exception as e:
        return render(request, 'sync/welcome.html', {'msg':str(e)})


'''this is the home page'''
def home(request):
    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'logout':
            request.session.flush()
            return redirect('/')
        elif action == 'addPeer':
            return addPeer(request)
    else:
        if not check_session(request): return redirect('/')

        name = request.session.get('name','')
        peers = peer.objects.filter(nwork__name=name)
        return render(request, 'sync/home.html', {'name':name, 'peers':peers})
        

'''this adds or updates peer information'''
def addPeer(request):
    if not check_session(request): return redirect('/')

    name = request.session.get('name','')
    nickname = request.POST.get('nickname','')
    pubkey = request.POST.get('pubkey','')
    lanip = request.POST.get('lanip','')
    wanip = request.POST.get('wanip','')
    wgip = request.POST.get('wgip','')
    wgport = request.POST.get('wgport','')

    n = nwork.objects.get(name=name)
    try:
        p = peer.objects.get(nwork=n, nickname=nickname)
        p.pubkey = pubkey
        p.lanip = lanip
        p.wanip = wanip
        p.wgip = wgip
        p.wgport = wgport
        p.save()
    except:
        p = peer(nwork=n, nickname=nickname, pubkey=pubkey, lanip=lanip, wanip=wanip, wgip=wgip, wgport=wgport)
        p.save()
    return redirect('home')



@csrf_exempt
def test(request):
    print(request)
    return JsonResponse({'t':'test', 'msg':'success'})
