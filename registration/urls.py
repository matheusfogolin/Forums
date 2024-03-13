from django.urls import path
from .views import signup, signin, update_profile, logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
    path("logout/", logout, name="logout"),
    path("update_profile/", update_profile, name="update_profile"),
]