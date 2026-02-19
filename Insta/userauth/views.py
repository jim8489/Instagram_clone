from django.shortcuts import render, get_object_or_404,redirect
from django.urls import resolve
from userauth.models import *
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from post.models import *
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from userauth.forms import EditProfileForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import logout, login




# Create your views here.
def UserProfile(request, username):
    user=get_object_or_404(User,username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    #else:
        #posts.saved.all
        
    #profile counting
    post_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    
    follow_status = Follow.objects.filter(following = user, follower = request.user).exists()
    
    #pagination
    posts = Post.objects.filter(user=user).order_by('-posted')
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)
    context = {
        'posts_paginator': posts_paginator,
        'profile': profile,
        'posts': posts,
        'post_count': post_count,
        'following_count': following_count,
        'followers_count': followers_count,
        'follow_status': follow_status,

    }
    return render(request, 'userauth/profile.html', context)
    
def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)
    
    if not Follow.objects.filter(follower=user, following=user).exists():
        Follow.objects.create(follower=user, following=user)

    try:
        f, created = Follow.objects.get_or_create(follower=user, following=following)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=user).delete()
        else:
            posts = Post.objects.filter(user=following)[:10]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=user, date=post.posted, following=following)
                    stream.save()

        return HttpResponseRedirect(reverse('user_profile', args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('user_profile', args=[username]))

def profile_edit(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.bio = form.cleaned_data.get('bio')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.save()
            return redirect('user_profile', profile.user.username)
    else:
        form = EditProfileForm(instance=request.user.profile)
    context={
        'form':form
    }
    return render(request,'userauth/edit-profile.html',context)

@method_decorator(login_required, name='dispatch')
class ProfileCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ProfileForm()
        context = {
            'form': form,
        }
        return render(request, 'userauth/create-profile.html', context)

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Ensure only one profile is created per user
            if hasattr(request.user, 'profile'):
                return redirect('user_profile', username=request.user.username)
            
            profile = form.save(commit=False)  # Create the profile object without saving it yet
            profile.user = request.user       # Associate the profile with the logged-in user
            profile.save()                    # Save the profile to the database
            return redirect('user_profile', username=request.user.username)
        
        context = {
            'form': form,
        }
        return render(request, 'userauth/create-profile.html', context)
    