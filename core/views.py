from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from .models import User, Post, Comment
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm,
    PostForm, CommentForm, UserProfileForm
)

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    # Get posts from users the current user follows and their own posts
    following_users = request.user.following.all()
    posts = Post.objects.filter(
        Q(user=request.user) | Q(user__in=following_users)
    ).distinct()
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    
    context = {
        'posts': posts,
        'form': form,
        'user': request.user
    }
    return render(request, 'index.html', context)

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all()
    is_following = request.user.is_authenticated and request.user.followers.filter(id=profile_user.id).exists()
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user) if request.user == profile_user else None
    
    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'form': form,
        'is_owner': request.user == profile_user
    }
    return render(request, 'profile.html', context)

@login_required
def toggle_like(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        post_id = data.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        
        return JsonResponse({
            'liked': liked,
            'like_count': post.like_count
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def toggle_follow(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        user_id = data.get('user_id')
        target_user = get_object_or_404(User, id=user_id)
        
        if target_user == request.user:
            return JsonResponse({'error': 'Cannot follow yourself'}, status=400)
        
        if request.user in target_user.followers.all():
            target_user.followers.remove(request.user)
            following = False
        else:
            target_user.followers.add(request.user)
            following = True
        
        return JsonResponse({
            'following': following,
            'follower_count': target_user.follower_count
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def add_comment(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        post_id = data.get('post_id')
        content = data.get('content')
        parent_id = data.get('parent_id')
        
        post = get_object_or_404(Post, id=post_id)
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            content=content,
            parent_id=parent_id if parent_id else None
        )
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'user': comment.user.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
                'user_profile_pic': comment.user.profile_picture.url if comment.user.profile_picture else None
            }
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)