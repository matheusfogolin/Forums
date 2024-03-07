from django.urls import path
from .views import (
    home, posts, details, create_post)

urlpatterns = [
    path("", home, name="home"),
    path("detail/<slug>/", details, name="detail"),
    path("posts/<slug>/", posts, name="posts"),
    path("create_post", create_post, name="create_post"),
]