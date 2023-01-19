
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("user/<str:this_user_name>", views.user_page, name="user_page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API routes for likes and user info
    path("posts/<int:post_id>", views.likes, name="likes"),
    path("user_api/<str:user_username>", views.user_api, name="user_api")
]
