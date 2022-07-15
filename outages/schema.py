import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import County, Area, Neighbourhood, Outage


class CountyNode(DjangoObjectType):
    class Meta:
        model = County
        interfaces = (relay.Node,)
        fields = (
            "id",
            "name",
            "areas",
            "neighbourhoods",
            'outages'
        )
        filter_fields = {
            'name': ('exact', 'icontains'),
            'outages__start_time': ('gte',)
        }


class AreaNode(DjangoObjectType):
    class Meta:
        model = Area
        interfaces = (relay.Node,)
        fields = (
            "id",
            "name",
            "county",
            "neighbourhoods",
            'outages'
        )
        filter_fields = {
            'name': ('icontains', 'exact'),
            'county__name': ('icontains', 'exact'),
        }


class NeighbourhoodNode(DjangoObjectType):
    class Meta:
        model = Neighbourhood
        interfaces = (relay.Node,)
        fields = (
            "id",
            "name",
            "county",
            "area",
            'outages'
        )
        filter_fields = {
            'name': ('icontains', 'exact'),
            'county__name': ('icontains', 'exact'),
            'area__name': ('icontains', 'exact'),
        }


class OutageNode(DjangoObjectType):
    class Meta:
        model = Outage
        interfaces = (relay.Node,)
        fields = (
            "id",
            "start_time",
            "end_time",
            "is_partial",
            "county",
            "area",
            'neighbourhood'
        )
        filter_fields = {
            'start_time': ('gte', 'lte'),
            'end_time': ('gte', 'lte'),
            'county__name': ('icontains', 'exact'),
            'area__name': ('icontains', 'exact'),
            'neighbourhood__name': ('icontains', 'exact'),
        }


class Query(graphene.ObjectType):
    county = relay.Node.Field(CountyNode)
    all_counties = DjangoFilterConnectionField(CountyNode)
    outages = relay.Node.Field(OutageNode)
    all_outages = DjangoFilterConnectionField(OutageNode)
    area = relay.Node.Field(AreaNode)
    all_areas = DjangoFilterConnectionField(AreaNode)
    neighbourhood = relay.Node.Field(NeighbourhoodNode)
    all_neighbourhoods = DjangoFilterConnectionField(NeighbourhoodNode)
