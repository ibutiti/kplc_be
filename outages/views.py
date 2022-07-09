from datetime import datetime

import pandas as pd
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from outages.filters import AreaFilter, NeighbourhoodFilter, OutageFilter, CountyFilter
from outages.models import County, Area, Neighbourhood, Outage
from outages.serializers import (
    CountySerializer,
    AreaSerializer,
    NeighbourhoodSerializer,
    OutageSerializer,
    OutageUploadSerializer,
)


class CountyReadOnlyViewset(ReadOnlyModelViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("id", "name")
    filterset_class = CountyFilter


class AreaReadOnlyViewset(ReadOnlyModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("id", "name")
    filterset_class = AreaFilter


class NeighbourhoodReadOnlyViewset(ReadOnlyModelViewSet):
    queryset = Neighbourhood.objects.all()
    serializer_class = NeighbourhoodSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("id", "name")
    filterset_class = NeighbourhoodFilter


class OutageViewset(ReadOnlyModelViewSet):
    queryset = Outage.objects.all()
    serializer_class = OutageSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("id", "name")
    filterset_class = OutageFilter


class OutageUploadView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = OutageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data["file"]
        reader = pd.read_csv(file)

        outages = []
        counties = {}
        areas = {}
        neighbourhoods = {}
        with transaction.atomic():
            for idx, row in reader.iterrows():
                try:
                    county = counties.get(row.county, None)
                    if not county:
                        county = County.objects.get(name=row.county)
                        counties[county.name] = county
                except:
                    raise ValidationError(
                        {"county": f"invalid county {row.county} on row {idx}"}
                    )

                try:
                    area = areas.get(f"{county.name}-{row.area}")
                    if not area:
                        area, _ = Area.objects.get_or_create(
                            name=row.area, county=county
                        )
                        areas[f"{county.name}-{row.area}"] = area
                except:
                    raise ValidationError(
                        {"area": f"Error on area {row.area} on row {idx}"}
                    )

                try:
                    neighbourhood = neighbourhoods.get(
                        f"{county.name}-{row.area}-{row.neighbourhood}", None
                    )
                    if not neighbourhood:
                        neighbourhood, _ = Neighbourhood.objects.get_or_create(
                            name=row.neighbourhood, county=county, area=area
                        )
                        neighbourhoods[
                            f"{county.name}-{row.area}-{row.neighbourhood}"
                        ] = neighbourhood
                except:
                    raise ValidationError(
                        {
                            "neighbourhood": f"Error on neighbourhood {row.neighbourhood} on row {idx}"
                        }
                    )

                datetime_format = "%d-%m-%Y %H:%M %z"
                start_time = datetime.strptime(
                    f"{row.date} {row.start} +0300", datetime_format
                )
                end_time = datetime.strptime(
                    f"{row.date} {row.end} +0300", datetime_format
                )
                outage = Outage(
                    county=county,
                    area=area,
                    neighbourhood=neighbourhood,
                    start_time=start_time,
                    end_time=end_time,
                    is_partial=row.isPartial,
                )
                outages.append(outage)

            outages = Outage.objects.bulk_create(outages)

        return Response(status=status.HTTP_201_CREATED)
