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

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "").strip()

        if not name or not email or not password:
            messages.error(request, "All fields are required")
            return redirect("register")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        # create user (email as username)
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        user.first_name = name
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.full_name = name
        profile.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "users/register.html")


# ================= LOGIN =================

def login_view(request):
    next_url = request.GET.get("next", "/")

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "").strip()

        if not email or not password:
            messages.error(request, "All fields are required")
            return redirect("login")

        user = authenticate(
            request,
            username=email,   # email stored as username
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "users/login.html")


# ================= LOGOUT =================

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out")
    return redirect("login")


# ================= PROFILE =================

@login_required
def profile_view(request):

    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        if phone and not re.match(r"^[6-9]\d{9}$", phone):
            messages.error(
                request,
                "Enter valid Indian mobile number (10 digits starting with 6-9)"
            )
            return redirect("profile")

        profile.full_name = full_name
        profile.phone = phone
        profile.address = address
        profile.save()

        messages.success(request, "Profile updated successfully")
        return redirect("profile")

    return render(request, "users/profile.html", {
        "profile": profile
    })
