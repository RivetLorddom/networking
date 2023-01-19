import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.core.paginator import Paginator
from django import forms
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


class NewPost(forms.Form):
    widget=forms.Textarea(
            attrs={
                "class": "new-post-form",
                "rows": "3",
                "placeholder": "Let the world know, what you think",
            })
    text = forms.CharField(label="Write a post...", widget=widget, max_length=300)


def pagination(posts, request):
    # show 10 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def index(request):
    if request.method == "POST":
        form = NewPost(request.POST)
        if form.is_valid():
            post = Post()
            post.creator = request.user
            post.content = form.cleaned_data["text"]
            post.save()
            return redirect("/")

    all_posts = Post.objects.all().order_by("-created_at")
    page_obj = pagination(all_posts, request)
    return render(request, "network/index.html", {
        "form": NewPost(),
        "page_obj": page_obj
    })


def following(request):
    # get only posts of people that the user is following
    following_posts = Post.objects.filter(creator__in = request.user.following.all()).order_by("-created_at")
    page_obj = pagination(following_posts, request)
    return render(request, "network/index.html", {
        "form": NewPost(),
        "page_obj": page_obj
    })


def user_page(request, this_user_name):
    # get only posts of this one user
    this_user = User.objects.get(username = this_user_name)
    this_users_posts = Post.objects.filter(creator = this_user).order_by("-created_at")
    page_obj = pagination(this_users_posts, request)

    return render(request, "network/user_page.html", {
        "this_user": this_user,
        "page_obj": page_obj
    })


# USER INFO API
@csrf_exempt
def user_api(request, user_username):

    # Query for the user
    try:
        this_user = User.objects.get(username=user_username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)

    # return user info content
    if request.method == "GET":
        return JsonResponse(this_user.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("followers") is not None:
            this_user.followers.set(User.objects.filter(username__in = data["followers"]))
        this_user.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({"error": "GET or PUT method required for this route"}, status=404)



# WORK ON LIKES API
@csrf_exempt
@login_required
def likes(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist"}, status=404)
    
    # return post content WORKS GOOD!
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # FOR UPDATING NUMBER OF LIKES OR EDITING POST
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("likes") is not None:
            post.likes = data["likes"]
        if data.get("liked_by") is not None:
            post.liked_by.set(User.objects.filter(username__in = data["liked_by"]))
        # save new content of post after editing
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
    

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
