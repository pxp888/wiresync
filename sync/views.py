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


'''this is the home page'''
def home(request):
    if not check_session(request): return redirect('/')
    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'logout':
            request.session.flush()
            return redirect('/')
        elif action == 'addPeer':
            return addPeer(request)
        elif action == 'goAccount':
            return redirect('account')
    else:
        name = request.session.get('name','')
        peers = peer.objects.filter(nwork__name=name)
        return render(request, 'sync/home.html', {'name':name, 'peers':peers})


'''this adds or updates peer information'''
def addPeer(request):
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


'''this tests json responses'''
@csrf_exempt
def test(request):
    print(request)
    return JsonResponse({'t':'test', 'msg':'success'})


'''this is the account page'''
def account(request):
    if not check_session(request): return redirect('/')
    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'logout':
            request.session.flush()
            return redirect('/')
        elif action == 'goHome':
            return redirect('/')
        elif action == 'updatePassword':
            return updatePassword(request)
    else:
        name = request.session.get('name','')
        return render(request, 'sync/account.html', {'name':name})


'''this updates the password'''
def updatePassword(request):
    name = request.session.get('name','')
    try:
        oldpass1 = request.POST['oldpass1']
        oldpass2 = request.POST['oldpass2']
        newpass1 = request.POST['newpass1']
        newpass2 = request.POST['newpass2']
    except KeyError:
        return render(request, 'sync/account.html', {'name':name, 'msg':'Missing parameters'})
    except Exception as e:
        return render(request, 'sync/account.html', {'name':name, 'msg':str(e)})

    if newpass1 != newpass2:
        return render(request, 'sync/account.html', {'name':name, 'msg':'New passwords do not match'})
    if oldpass1 != oldpass2:
        return render(request, 'sync/account.html', {'name':name, 'msg':'Old passwords do not match'})

    if len(newpass1) < 4:
        return render(request, 'sync/account.html', {'name':name, 'msg':'New Password too short'})
    
    khash = hashlib.sha256(oldpass1.encode('utf-8')).hexdigest()
    try:
        n = nwork.objects.get(name=name)
        if n.khash != khash:
            return render(request, 'sync/account.html', {'name':name, 'msg':'Old password is wrong'})
        else:
            n.khash = hashlib.sha256(newpass1.encode('utf-8')).hexdigest()
            n.save()
    except nwork.DoesNotExist:
        return render(request, 'sync/account.html', {'name':name, 'msg':'Name not found'})
    except Exception as e:
        return render(request, 'sync/account.html', {'name':name, 'msg':str(e)})

    return render(request, 'sync/account.html', {'name':name, 'msg':'Password Updated'})

