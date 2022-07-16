from django_filters import rest_framework as filters

from outages.models import Area, Neighbourhood, Outage, County


class CountyFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = County
        fields = []


class AreaFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    county = filters.CharFilter(field_name="county__name", lookup_expr="icontains")
    outages__start = filters.DateFilter(
        field_name="outages__start_time", lookup_expr="gt"
    )
    outages__end = filters.DateFilter(field_name="outages__end_time", lookup_expr="lt")

    class Meta:
        model = Area
        fields = []


class NeighbourhoodFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    county = filters.CharFilter(field_name="county__name", lookup_expr="icontains")
    area = filters.CharFilter(field_name="area__name", lookup_expr="icontains")
    outages__start = filters.DateFilter(
        field_name="outages__start_time", lookup_expr="gt"
    )
    outages__end = filters.DateFilter(field_name="outages__end_time", lookup_expr="lt")

    class Meta:
        model = Neighbourhood
        fields = []


class OutageFilter(filters.FilterSet):
    county = filters.CharFilter(field_name="county__name", lookup_expr="icontains")
    area = filters.CharFilter(field_name="area__name", lookup_expr="icontains")
    neighbourhood = filters.CharFilter(
        field_name="neighbourhood__name", lookup_expr="icontains"
    )
    start = filters.DateFilter(field_name="start_time", lookup_expr="gt")
    end = filters.DateFilter(field_name="end_time", lookup_expr="lt")

    class Meta:
        model = Outage
        fields = []
