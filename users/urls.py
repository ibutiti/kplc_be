from django.urls import path, include

from users.views import TwitterLogin

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("twitter/", TwitterLogin.as_view(), name="twitter_login"),
    path("join/", include("dj_rest_auth.registration.urls")),
]
