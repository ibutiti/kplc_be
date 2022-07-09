from django.urls import path
from rest_framework import routers

from .views import (
    CountyReadOnlyViewset,
    AreaReadOnlyViewset,
    NeighbourhoodReadOnlyViewset,
    OutageViewset,
    OutageUploadView,
)

router = routers.SimpleRouter()
router.register(r"counties", CountyReadOnlyViewset)
router.register(r"areas", AreaReadOnlyViewset)
router.register(r"neighbourhoods", NeighbourhoodReadOnlyViewset)
router.register("", OutageViewset)

urlpatterns = [path("upload", OutageUploadView.as_view())]

urlpatterns = urlpatterns + router.urls
