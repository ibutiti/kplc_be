from rest_framework import serializers

from outages.models import County, Area, Neighbourhood, Outage


class OutageSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outage
        fields = (
            'id',
            'start_time',
            'end_time',
        )


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = (
            'id',
            'name',
            'outages'
        )


class CountySlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = (
            'id',
            'name',
        )


class AreaSerializer(serializers.ModelSerializer):
    county = serializers.SlugRelatedField('name', read_only=True)

    class Meta:
        model = Area
        fields = (
            'id',
            'name',
            'county',
            'outages'
        )


class AreaSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = (
            'id',
            'name',
        )


class NeighbourhoodSerializer(serializers.ModelSerializer):
    county = serializers.SlugRelatedField('name', read_only=True)
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


class NeighbourhoodSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighbourhood
        fields = (
            'id',
            'name',
        )


class OutageSerializer(serializers.ModelSerializer):
    county = CountySlimSerializer()
    area = AreaSlimSerializer()
    neighbourhood = NeighbourhoodSlimSerializer()

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


class OutageUploadSerializer(serializers.Serializer):
    file = serializers.FileField(allow_empty_file=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        raise serializers.ValidationError('Upload edit not allowed')
