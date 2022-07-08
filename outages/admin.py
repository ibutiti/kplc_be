from django.contrib import admin

from outages.models import Outage, Neighbourhood, County, Area


class OutageInline(admin.TabularInline):
    model = Outage
    extra = 5
    can_delete = False


class AreaInline(admin.TabularInline):
    model = Area
    extra = 5
    can_delete = False


class NeighbourhoodInline(admin.TabularInline):
    model = Neighbourhood
    extra = 5
    can_delete = False


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    inlines = [AreaInline, OutageInline]
    ordering = ('name',)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'county']
    inlines = [NeighbourhoodInline, OutageInline]


@admin.register(Neighbourhood)
class NeighbourhoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'area']
    inlines = [OutageInline]


@admin.register(Outage)
class OutageAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'neighbourhood']
    date_hierarchy = 'start_time'
