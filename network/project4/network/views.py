from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import *


def index(request):
    if request.method == "POST":
        user = request.user
        body = request.POST["body"]
        timestamp = datetime.now()
        if(body != ""):
            Post.objects.create(user = user, body = body, timestamp = timestamp, likecount = 0)
    return render(request, "network/index.html")


def allposts(request):
    posts = Post.objects.all().order_by('-timestamp')
    for post in posts:
        post.likes = Like.objects.filter(post=post.id).count()
        post.save()
    p = Paginator(posts, 10)
    pn = request.GET.get('page')
    sp = p.get_page(pn)
    return render(request, "network/allposts.html",{
        "posts": sp
    })


@csrf_exempt
def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("body") is not None:
            post.body = data["body"]
        post.save()





def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
