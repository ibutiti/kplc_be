from rest_framework.serializers import ModelSerializer

from outages.models import County, Area, Neighbourhood, Outage


class OutageSlimSerializer(ModelSerializer):
    class Meta:
        model = Outage
        fields = (
            'id',
            'start_time',
            'end_time',
        )


class CountySerializer(ModelSerializer):
    class Meta:
        model = County
        fields = (
            'id',
            'name',
            'outages'
        )


class AreaSerializer(ModelSerializer):
    county = CountySerializer()

    class Meta:
        model = Area
        fields = (
            'id',
            'name',
            'county',
            'outages'
        )


class NeighbourhoodSerializer(ModelSerializer):
    county = CountySerializer()
    area = AreaSerializer()

    class Meta:
        model = Neighbourhood
        fields = (
            'id',
            'name',
            'area',
            'county',
            'outages'
        )


class OutageSerializer(ModelSerializer):
    county = CountySerializer()
    area = AreaSerializer()
    neighbourhood = NeighbourhoodSerializer()

    class Meta:
        model = Outage
        fields = (
            'id',
            'area',
            'county',
            'neighbourhood',
            'start_time',
            'end_time',
            'is_partial'
        )
