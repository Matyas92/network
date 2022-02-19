from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import User
from .models import Profile

from .forms import CreatePost
from .forms import Post
from .forms import ToFollow

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def index(request):
    profile = request.user
    posts = Post.objects.all()
    form = CreatePost()


    already_liked = None
    all_liked =  Post.objects.all()

    pag = Paginator(Post.objects.all().order_by('-date'), 10)
    site = request.GET.get('page')
    postPaginator = pag.get_page(site)

    nums = "x" * postPaginator.paginator.num_pages

    context = {'all_liked' : all_liked, 'form' : form, posts : 'posts', 'profile' : profile, 'postPaginator' : postPaginator, 'nums' : nums}

    return render(request, "network/index.html", context)
 


def toLike(request, pk):
    if request.method == "POST":

        post = Post.objects.get(id=pk)
        post.likefrom.add(request.user)
        return redirect("index")

    
def disLike(request, pk):
    if request.method == "POST":

        post = Post.objects.get(id=pk)
        post.likefrom.remove(request.user)
        return redirect("index")



def new_post(request):
    profile = request.user

    if request.method == 'POST':
        form = CreatePost(request.POST)
        form.instance.owner = profile
        form.instance.likes = 0

        if form.is_valid():
            form.save()
            return redirect("index")

def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect("index")


def profileCheck(request, pk):
        profile = User.objects.get(username=pk)

        all_follow = profile.profile.follower.all()
        already_follow = None

        for fol in all_follow:
            if fol == request.user:
                already_follow = True
            else:
                already_follow = False    

        current = request.GET.get('user')

        loguser = request.user

        
        return render(request, "network/profile.html",{
            'already_follow' : already_follow,
            'profile' : profile,
            'current' : current,
            'loguser' : loguser,

            })
            

def following(request, pk):
    current = request.GET.get('user')
    loguser = request.user
    if request.method == 'POST':

        profile = User.objects.get(username=pk)
        profile.profile.follower.add(request.user)

        profileLog = User.objects.get(username=loguser)
        profileLog.profile.follows.add(profile)

        return redirect('profileCheck', profile.username)





def unfollowing(request, pk):
    current = request.GET.get('user')
    loguser = request.user
    if request.method == 'POST':

        profile = User.objects.get(username=pk)
        profile.profile.follower.remove(request.user)

        profileLog = User.objects.get(username=loguser)
        profileLog.profile.follows.remove(profile)

        return redirect('profileCheck', profile.username)

def followed(request):
    profile = request.user

    follows = profile.profile.follows.all()
    posto = Post.objects.all()

    filteredPost = []
    for pp in posto:
       for ff in follows:
          if ff == pp.owner:
             filteredPost.append(pp)

    pag = Paginator(filteredPost, 10)
    site = request.GET.get('page')
    postPaginator = pag.get_page(site)

    nums = "x" * postPaginator.paginator.num_pages

    context = {'filteredPost' : filteredPost, 'profile' : profile, 'postPaginator' : postPaginator, 'nums' : nums}

    return render(request, "network/followed.html", context)


def edit(request, pk):
    post = Post.objects.get(id=pk)
    if request.user == post.owner:
        form = CreatePost(instance=post)
        if request.method == 'POST':
            form = CreatePost(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('index')
    else:
        return redirect("index")

    return render(request, "network/post.html",{
        'form' : form,
    })




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
