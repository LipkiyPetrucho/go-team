from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserForm, ProfileForm


@login_required
def profile_view(request):
    return render(request, "user/profile.html")


@login_required
def home_view(request):
    return render(request, "home.html")


@login_required
def profile_edit_view(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "user/profile_edit.html", context)
