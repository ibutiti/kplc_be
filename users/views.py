from allauth.account.views import ConfirmEmailView
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.registration.serializers import VerifyEmailSerializer
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from django.conf import settings
from django.http.response import Http404
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


@api_view()
def password_reset_confirm(request):
    return Response({"message": "Hello, world!"})


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class VerifyEmailView(APIView, ConfirmEmailView):
    permission_classes = (permissions.AllowAny,)
    allowed_methods = ("GET", "OPTIONS", "HEAD")

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        self.kwargs["key"] = serializer.validated_data["key"]
        confirmation = self.get_object()
        confirmation.confirm(self.request)

        return redirect(to=f"{settings.WEB_APP_BASE_URL}/email-confirmed/")


class PasswordResetRedirectView(APIView):
    permission_classes = (permissions.AllowAny,)
    allowed_methods = (
        "GET",
        "OPTIONS",
        "HEAD",
    )

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        token = kwargs.get("token")
        if not user_id and token:
            return Http404("Invalid password reset. Request new password reset email.")

        return redirect(
            to=f"{settings.WEB_APP_BASE_URL}/password-reset/?user={user_id}&&token={token}"
        )
