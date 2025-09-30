from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . models import Post


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_pass = request.POST.get("confirm-password")
        if password == confirm_pass:
            user = User.objects.create_user(
                username=username, email=email, password=password)
            user.save()
            return redirect('login')
    return render(request, "blog_app/register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            redirect("login")
    return render(request, "blog_app/login.html")


@login_required(login_url="login")
def blog(request):
    post = Post.objects.order_by("-time")
    context = {
        "posts": post
    }
    return render(request, 'blog_app/index.html', context=context)


@login_required(login_url="login")
def user(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        Post.objects.create(title=title, content=content, author=request.user)

    return render(request, "blog_app/user.html")
