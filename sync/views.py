from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import nwork, peer
from .xsession import check_session


# Create your views here.


'''this is the home page'''
def home(request):
    if not check_session(request): return redirect('/')
    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'addPeer':
            return addPeer(request)
        elif action == 'removePeer':
            return removePeer(request)
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


'''this removes a peer'''
def removePeer(request):
    name = request.session.get('name','')
    nickname = request.POST.get('nickname','')
    n = nwork.objects.get(name=name)
    p = peer.objects.get(nwork=n, nickname=nickname)
    p.delete()
    return redirect('home')


'''this tests json responses'''
@csrf_exempt
def test(request):
    print(request)
    return JsonResponse({'t':'test', 'msg':'success'})
