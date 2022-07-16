from django.urls import path, include

from users.views import TwitterLogin, VerifyEmailView, PasswordResetRedirectView

urlpatterns = [
    path("twitter/login/callback/", TwitterLogin.as_view(), name="twitter_login"),
    path("join/", include("dj_rest_auth.registration.urls")),
    path(
        "account-confirm-email/<str:uid>/<str:key>/",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "password-reset/<user_id>/<token>/",
        PasswordResetRedirectView.as_view(),
        name="password_reset_confirm",
    ),
    path("", include("dj_rest_auth.urls")),
]
