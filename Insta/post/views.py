from django.shortcuts import render,redirect, get_object_or_404
from post.models import *
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from post.forms import NewCommentForm, NewPostform
# Create your views here.

def index(request):
    user = request.user
    users=User.objects.all()
    if user.is_authenticated:
      posts = Stream.objects.filter(user=user)
      group_ids=[]
      for post in posts:
        group_ids.append(post.post_id)
      post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
      context = {
          'users':users,
          'post_items': post_items
      }
      return render(request, "post/index.html",context)
    return redirect("account_login")

def create_post(request):
    user = request.user.id
    #tag_ob = []
    if request.method == 'POST':
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            #tag_form = form.cleaned_data.get('tag')
           # tag_list = list(tag_form.split(','))
            
            #for tag in tag_list:
                #t , created = Tag.objects.get_or_create(title=tag)
              #  tag_ob.append(t)
            p,created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)  
           # p.tags.set(tag_ob)
            p.save()
            return redirect('index')  
    else:
        form = NewPostform
    context={
         'form':form
    }
    return render(request,'post/createpost.html',context)

def PostDetail(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-added')
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse('post_detail', args=[post_id]))
        
    else:
        form = NewCommentForm
    context = {
        'form': form,
        'comments': comments,
        'post': post
    }
    
    return render(request, "post/postdetails.html", context)

def LikePost(request, post_id):
    user=request.user
    post = Post.objects.get(id=post_id)
    total_likes = post.likes
    like = Like.objects.filter(user=user, post=post).count()
    
    if not like:
        like = Like.objects.create(user=user, post=post)
        total_likes = total_likes + 1
    else:
        like = Like.objects.filter(user=user, post=post).delete()
        total_likes = total_likes - 1
    post.likes = total_likes

    post.save()    
    
    return HttpResponseRedirect(reverse('index'))


def search_view(request):
    user=request.user
    query = request.GET.get("q")
    context={}
    if query:
        users = User.objects.filter(username__icontains=query)
        #Pagination
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)
    
        context = {
           "query":  query,
           "users": users_paginator,
        }
    
    return render(request, 'post/search.html', context)