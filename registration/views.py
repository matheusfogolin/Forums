from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as lt
from django.contrib.auth.forms import AuthenticationForm
from .admin import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UpdateForm
from main.models import Author


def signup(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("update_profile")
    
    context.update({
        "form": form,
        "title": "Signup"
    })
    return render(request, "registration/signup.html", context)

def signin(request):
    context = {}
    form = AuthenticationForm(data = request.POST)
    
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            
    context.update({
        "form": form,
        "title": "Signin"
    })
    
    return render(request, "registration/signin.html", context)

@login_required
def update_profile(request):
    context = {}
    try:
        author = Author.objects.get(user=request.user)
    except:
        author = None
    
    form = UpdateForm(request.POST, request.FILES)    
    
    if request.method == "POST":
        if form.is_valid():
            if author is not None:
                author.first_name = form.cleaned_data.get("first_name")
                author.last_name = form.cleaned_data.get("last_name")
                author.bio = form.cleaned_data.get("bio")
                author.profile_pic = form.cleaned_data.get("profile_pic")
                author.save()
                return redirect("home")
            else:
                user = request.user
                update_profile = form.save(commit=False)
                update_profile.user = user
                update_profile.save()
                return redirect("home")
        
    context.update({
        "form": form,
        "title": "Update Profile"
    })
    
    return render(request, "registration/update.html", context)

@login_required
def create_profile(request):
    context = {}
    user = request.user
    form = UpdateForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            update_profile = form.save(commit=False)
            update_profile.user = user
            update_profile.save()
            return redirect("home")
        
    context.update({
        "form": form,
        "title": "Update Profile"
    })
    
    return render(request, "registration/update.html", context)


@login_required
def logout(request):
    lt(request)
    return redirect("home")
    