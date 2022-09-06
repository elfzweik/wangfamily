from random import random
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse

from comment.forms import CommentForm
from .forms import LoginForm, RegForm, ChangeNameForm, BindEmailForm, ChangeAvatarForm, ChangePasswordForm
from random import randint
from .models import Profile


def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def login(request):
    redirect_to = request.GET.get('from', '/')
    if redirect_to.startswith('/user/register'):
        path_split = redirect_to.split('/user/register/?from=')
        redirect_to = path_split[-1]
        path_split = redirect_to.split('user/login/?from=')
        redirect_to = path_split[-1]

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(redirect_to, '/')
    else:
        login_form = LoginForm()
        comment_form = CommentForm()

    context = {}
    context['login_form'] = login_form
    context['return_back_url'] = redirect_to
    return render(request, 'user/login.html', context)

def register(request):
    redirect_to = request.GET.get('from', '/')
    if redirect_to.startswith('/user/login'):
        path_split = redirect_to.split('user/login/?from=')
        redirect_to = path_split[-1]
        path_split = redirect_to.split('/user/register/?from=')
        redirect_to = path_split[-1]

    if request.method == 'POST':
        reg_form = RegForm(request.POST, request.FILES)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            first_name=reg_form.cleaned_data['first_name']
            last_name=reg_form.cleaned_data['last_name']
            avatar=reg_form.cleaned_data['avatar']
            # 创建用户
            if avatar==None:
                i=randint(1,12)
                avatar = "avatar/"+str(i)+".png" if i<5 else "avatar/"+str(i)+".jpg"
            
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name  
            profile = Profile.objects.create(user=user)
            profile.avatar = avatar
            
            user.save()
            profile.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(redirect_to, '/')
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    context['return_back_url'] = redirect_to
    return render(request, 'user/register.html', context)
    
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', '/'))

def user_info(request):
    redirect_to = request.GET.get('from', '/')
    context = {}
    context['return_back_url']=redirect_to
    return render(request, 'user/user_info.html', context)

def change_name(request):
    redirect_to = request.GET.get('from', '/')

    if request.method == 'POST':
        form = ChangeNameForm(request.POST, user=request.user)
        if form.is_valid():
            last_name_new = form.cleaned_data['last_name_new']
            first_name_new = form.cleaned_data['first_name_new']
            user = User.objects.get(pk=request.user.pk)
            user.last_name = last_name_new
            user.first_name = first_name_new
            user.save()
            return redirect(redirect_to)
    else:
        form = ChangeNameForm()

    context = {}
    context['page_title'] = '修改姓名'
    context['form_title'] = '修改姓名'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)


def bind_email(request):
    redirect_to = request.GET.get('from', '/')

    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def change_avatar(request):
    redirect_to = request.GET.get('from', '/')

    if request.method == 'POST':
        form = ChangeAvatarForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            avatar = form.cleaned_data['avatar']
            if avatar != None:
                profile, created = Profile.objects.get_or_create(user=request.user)
                profile.avatar = avatar
                profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeAvatarForm()

    context = {}
    context['page_title'] = '修改头像'
    context['form_title'] = '修改头像'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def change_password(request):
    redirect_to = '/'
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()

    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)