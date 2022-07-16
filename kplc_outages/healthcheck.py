import logging

import requests
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
        # check DB
        counties = County.objects.count()
        assert counties == 47

        # check API
        url = reverse("schema-swagger-ui", request=request)
        response = requests.head(url)
        response.raise_for_status()

        return Response("Healthcheck OK ✅", status=200)

    except AssertionError:
        logger.exception("Database Healthcheck Failed ❌")

        return Response("ERROR", status=500)
    except requests.exceptions.HTTPError:
        logger.exception("API Healthcheck Failed ❌")

        return Response("ERROR", status=500)

    except Exception:
        logger.exception('Healthcheck Failed ❌')

        return Response("ERROR", status=500)
