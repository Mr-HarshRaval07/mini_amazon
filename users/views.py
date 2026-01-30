import re

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile


# ================= REGISTER =================

def register_view(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not email or not password:
            messages.error(request, "All fields are required")
            return redirect("/register/")

        # check existing user
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("/register/")

        # create user (email stored as username)
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # profile auto created by signal (safe fallback)
        Profile.objects.get_or_create(user=user)

        messages.success(request, "Account created! Please login.")
        return redirect("/login/")

    return render(request, "users/register.html")


# ================= LOGIN =================

def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not email or not password:
            messages.error(request, "All fields are required")
            return redirect("/login/")

        user = authenticate(
            request,
            username=email,   # email stored as username
            password=password
        )

        if user:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "users/login.html")


# ================= LOGOUT =================

def logout_view(request):
    logout(request)
    return redirect("/login/")


# ================= PROFILE =================

@login_required
def profile_view(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        # 📱 Indian phone validation
        if phone:
            if not re.match(r'^[6-9]\d{9}$', phone):
                messages.error(
                    request,
                    "Enter valid Indian mobile number (10 digits starting with 6-9)"
                )
                return redirect("/profile/")

        profile.full_name = full_name
        profile.phone = phone
        profile.address = address
        profile.save()

        messages.success(request, "Profile updated successfully ✅")
        return redirect("/profile/")

    return render(request, "users/profile.html", {
        "profile": profile
    })

