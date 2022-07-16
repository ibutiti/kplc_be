"""kplc_outages URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import logging

import requests
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from graphene_django.views import GraphQLView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from outages.models import County

logger = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def healthcheck(request):
    try:
        counties = County.objects.count()
        assert counties == 47
        url = reverse("schema-swagger-ui", request=request)
        response = requests.head(url)
        response.raise_for_status()
        return Response("Healthcheck OK ✅", status=200)
    except:
        logger.exception("Healthcheck Failed ❌")

        return Response("ERROR", status=500)


schema_view = get_schema_view(
    openapi.Info(
        title="KPLC Outages API",
        default_version="v1",
        description="Endpoints to the Outages API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="allan@edge.ke"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("outages/", include("outages.urls")),
    path("healthcheck/", healthcheck),
]
