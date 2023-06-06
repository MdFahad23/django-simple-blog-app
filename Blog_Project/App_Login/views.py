from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from App_Login.forms import SignUpForm, UserProfileChange, ProfilePic

# Create your views here.


def Sign_Up(request):
    form = SignUpForm()
    register = False
    if request.method == "POST":
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            register = True

    diction = {"form": form, "register": register}
    return render(request, "App_Login/SignUp.html", context=diction)


def Login_User(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))

    return render(request, "App_Login/Login.html", context={"form": form})


@login_required
def LogOut(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def UserProfile(request):
    return render(request, "App_Login/profile.html", context={})


@login_required
def Change_User_Profile(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)

    if request.method == "POST":
        form = UserProfileChange(request.POST, instance=current_user)

        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=current_user)

    return render(request, "App_Login/change_profile.html", context={"form": form})


@login_required
def Pass_Change(request):
    current_user = request.user
    form = PasswordChangeForm(instance=current_user)
    change = False

    if request.method == "POST":
        form = PasswordChangeForm(current_user, data=request.POST)

        if form.is_valid():
            form.save()
            change = True

    return render(
        request, "App_Login/Change_Pass.html", context={"form": form, "change": change}
    )


@login_required
def add_pro_pic(request):
    form = ProfilePic()

    if request.method == "POST":
        form = ProfilePic(request.POST, request.FILES)

        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()

            return HttpResponseRedirect(reverse("App_Login:profile"))

    return render(request, "App_Login/pro_pic_add.html", context={"form": form})


@login_required
def update_pro_pic(request):
    form = ProfilePic(instance=request.user.user_profile)

    if request.method == "POST":
        form = ProfilePic(
            request.POST, request.FILES, instance=request.user.user_profile
        )

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("App_Login:profile"))

    return render(request, "App_Login/pro_pic_add.html", context={"form": form})
