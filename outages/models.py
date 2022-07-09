from django.db import models

from common.models import BaseModel


class County(BaseModel):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)

    class Meta:
        verbose_name_plural = "Counties"
        ordering = ("name",)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Area(BaseModel):
    name = models.CharField(max_length=64, null=False, blank=False)
    county = models.ForeignKey(
        County, on_delete=models.PROTECT, related_name="areas", null=False, blank=False
    )

    class Meta:
        unique_together = ("name", "county")
        ordering = ("name",)

    def __str__(self):
        return f"{self.id}: {self.name} - {self.county.name} County"


class Neighbourhood(BaseModel):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)
    county = models.ForeignKey(
        County,
        on_delete=models.PROTECT,
        related_name="neighbourhoods",
        null=False,
        blank=False,
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name="neighbourhoods",
        null=False,
        blank=False,
    )

    class Meta:
        unique_together = ("name", "county", "area")
        ordering = ("name",)

    def __str__(self):
        return f"{self.id}: {self.name} - {self.area.name}, {self.county.name} County"


class Outage(BaseModel):
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)
    is_partial = models.BooleanField(default=False)
    county = models.ForeignKey(
        County,
        on_delete=models.PROTECT,
        related_name="outages",
        null=False,
        blank=False,
    )
    area = models.ForeignKey(
        Area, on_delete=models.PROTECT, related_name="outages", null=False, blank=False
    )
    neighbourhood = models.ForeignKey(
        Neighbourhood,
        on_delete=models.PROTECT,
        related_name="outages",
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ("start_time",)
