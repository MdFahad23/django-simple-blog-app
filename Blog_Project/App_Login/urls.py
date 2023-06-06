from django.urls import path

from . import views

app_name = "App_Login"

urlpatterns = [
    path("signup/", views.Sign_Up, name="signup"),
    path("login/", views.Login_User, name="login"),
    path("logout/", views.LogOut, name="logout"),
    path("profile/", views.UserProfile, name="profile"),
    path("change-profile/", views.Change_User_Profile, name="change_profile"),
    path("password/", views.Pass_Change, name="pass_change"),
    path("add-profile-pic/", views.add_pro_pic, name="add_pro_pic"),
    path("update-profile-pic/", views.update_pro_pic, name="update_pro_pic"),
]
