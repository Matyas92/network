
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.new_post, name="new_post"),
    path("profile/<str:pk>", views.profileCheck, name="profileCheck"),
    path("following/<str:pk>", views.following, name="following"),
    path("unfollowing/<str:pk>", views.unfollowing, name="unfollowing"),
    path("followed", views.followed, name="followed"),
    path("tolike/<str:pk>", views.toLike, name="toLike"),
    path("dislike/<str:pk>", views.disLike, name="disLike"),

    path("edit/<str:pk>", views.edit, name="edit"),
    path("delete/<str:pk>", views.delete_post, name="delete")

]
