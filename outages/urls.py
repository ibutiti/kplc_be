from rest_framework import routers

from .views import CountyReadOnlyViewset, AreaReadOnlyViewset, NeighbourhoodReadOnlyViewset, OutageViewset

router = routers.SimpleRouter()
router.register(r'counties', CountyReadOnlyViewset)
router.register(r'areas', AreaReadOnlyViewset)
router.register(r'neighbourhoods', NeighbourhoodReadOnlyViewset)
router.register('', OutageViewset)

urlpatterns = router.urls
