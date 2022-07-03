from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from rest_framework.decorators import api_view


@api_view()
def password_reset_confirm(request):
    return Redirect({"message": "Hello, world!"})


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter
