from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages


def login_register(request):

    # Only run logic when form submitted
    if request.method == "POST":

        action = request.POST.get("action")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # ---------------- REGISTER ---------------- #
        if action == "register":

            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():

                messages.error(request, "You are already registered. Please login.")
                return render(request, "login_register.html", {"show_login": True})

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(request, "Registration successful. Please login.")
            return render(request, "login_register.html", {"show_login": True})


        # ---------------- LOGIN ---------------- #
        elif action == "login":

            try:
                user_obj = User.objects.get(email=email)
                username_for_login = user_obj.username
            except User.DoesNotExist:
                username_for_login = email

            user = authenticate(username=username_for_login, password=password)

            if user:
                login(request, user)
                return redirect("dashboard")

            else:
                messages.error(request, "Invalid login credentials")

    # GET request → just show page
    return render(request, "login_register.html")

# ---------------- DASHBOARD ---------------- #

@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "dashboard.html", {"profile": profile})


# ---------------- LOGOUT ---------------- #

def logout_view(request):
    logout(request)
    return redirect("home")


# ---------------- EDIT PROFILE ---------------- #

@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        profile.bio = request.POST.get("bio")

        if request.FILES.get("image"):
            profile.image = request.FILES.get("image")

        profile.save()
        messages.success(request, "Profile updated successfully")

        return redirect("dashboard")

    return render(request, "edit_profile.html", {"profile": profile})