from django.shortcuts import render, redirect
from .models import nwork
import hashlib
from .xsession import check_session


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