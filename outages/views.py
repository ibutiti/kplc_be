from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from outages.models import County, Area, Neighbourhood, Outage
from outages.serializers import CountySerializer, AreaSerializer, NeighbourhoodSerializer, OutageSerializer


class CountyReadOnlyViewset(ReadOnlyModelViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class AreaReadOnlyViewset(ReadOnlyModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = []
    authentication_classes = []


class NeighbourhoodReadOnlyViewset(ReadOnlyModelViewSet):
    queryset = Neighbourhood.objects.all()
    serializer_class = NeighbourhoodSerializer
    permission_classes = []
    authentication_classes = []


class OutageViewset(ModelViewSet):
    queryset = Outage.objects.all()
    serializer_class = OutageSerializer
