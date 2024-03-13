from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as lt
from django.contrib.auth.forms import AuthenticationForm
from .admin import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UpdateForm
from .models import User
from datetime import datetime


def signup(request):
    context = {}
    form = UserCreationForm(request.POST, request.FILES)
    
    if request.method == "POST":
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("home")
    
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
    
    user = User.objects.get(email=request.user.email)
    form = UpdateForm(request.POST, request.FILES)    
    
    if request.method == "POST":
        if form.is_valid():
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.bio = form.cleaned_data.get("bio")
            user.profile_pic = form.cleaned_data.get("profile_pic")
            user.update_date = datetime.now()
            user.save()
            return redirect("home")
        
        context.update({
            "form": form,
            "title": "Update Profile"
        })  
        return render(request, "registration/update.html", context)
    else:
        form = UpdateForm(instance = user)
        
        return render(request, "registration/update.html", {'form': form, 'ls': user})


@login_required
def logout(request):
    lt(request)
    return redirect("home")