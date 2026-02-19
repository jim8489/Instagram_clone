from django.shortcuts import render,redirect, get_object_or_404
from post.models import *
from django.contrib.auth.decorators import login_required
from post.forms import *
from django.urls import reverse
from dm.models import Message
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.

@login_required
def inbox(request):
    user = request.user
    messages = Message.get_message(user=user)
    active_dm = None
    dm = None
    if messages:
        message = messages[0]
        active_dm = message['user']
        reciepient = get_object_or_404(User, username=active_dm.username)
        dm = Message.objects.filter(user=user, reciepient=reciepient)
        dm.update(is_read=True)
        
        for message in messages:
            if message['user'].username == active_dm.username:
                message['unread'] = 0
        context = {
            'dm': dm,
            'active_dm': active_dm,
            'messages': messages,
            'reciepient': reciepient
        }
        return render(request, 'dm/inbox.html', context)
    else:
        return render(request, 'dm/no_inbox.html')

    
def Directs(request, username):
    user = request.user
    messages = Message.get_message(user=user)
    active_dm = username
    reciepient = get_object_or_404(User, username=active_dm)
    dm = Message.objects.filter(user=user, reciepient__username = username, reciepient=reciepient)
    dm.update(is_read=True)
    for message in messages:
        if message['user'].username == active_dm:
            message['unread'] = 0
    
    context = {
        'dm': dm,
        'active_dm': active_dm,
        'messages': messages,
        'reciepient': reciepient
    }
    return render(request, 'dm/directs.html', context)

def sendMessage(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')
    
    if request.method=='POST':
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
        return redirect('inbox')
    else:
        pass


    