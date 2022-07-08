from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from outages.filters import AreaFilter, NeighbourhoodFilter, OutageFilter, CountyFilter
from outages.models import County, Area, Neighbourhood, Outage
from outages.serializers import CountySerializer, AreaSerializer, NeighbourhoodSerializer, OutageSerializer


class CountyReadOnlyViewset(ReadOnlyModelViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('id', 'name')
    filterset_class = CountyFilter


class AreaReadOnlyViewset(ReadOnlyModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('id', 'name')
    filterset_class = AreaFilter


class NeighbourhoodReadOnlyViewset(ReadOnlyModelViewSet):
    queryset = Neighbourhood.objects.all()
    serializer_class = NeighbourhoodSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('id', 'name')
    filterset_class = NeighbourhoodFilter


class OutageViewset(ReadOnlyModelViewSet):
    queryset = Outage.objects.all()
    serializer_class = OutageSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('id', 'name')
    filterset_class = OutageFilter
