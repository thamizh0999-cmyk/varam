from django.contrib import admin
from .models import DailyCensus, IPPatient
from .models import (
    DailyCensus,
    IPPatient,
    DiseaseMaster,
    DailyDiseaseCount,
    CentreProfile,
    FacilityMembership,
)


@admin.register(DailyCensus)
class DailyCensusAdmin(admin.ModelAdmin):

    list_display = (
        "date",
        "op_total",
        "created_at",
    )

    list_filter = (
        "date",
    )

    ordering = (
        "-date",
    )


@admin.register(IPPatient)
class IPPatientAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "sex",
        "is_child",
        "admission_date",
        "admission_session",
        "discharge_date",
        "discharge_session",
    )

    list_filter = (
        "sex",
        "is_child",
        "admission_date",
        "discharge_date",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "-admission_date",
        "-id",
    )
@admin.register(DiseaseMaster)
class DiseaseMasterAdmin(admin.ModelAdmin):
    list_display = ("name", "tamil_name", "category", "is_ncd", "is_active")
    list_filter = ("category", "is_ncd", "is_active")
    search_fields = ("name", "tamil_name")
    ordering = ("name",)


@admin.register(DailyDiseaseCount)
class DailyDiseaseCountAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "disease",
        "male_count",
        "female_count",
        "child_count",
        "total_count",
    )
    list_filter = ("date", "disease")
    search_fields = ("disease__name", "disease__tamil_name")
    ordering = ("-date", "disease")
@admin.register(CentreProfile)
class CentreProfileAdmin(admin.ModelAdmin):
    list_display = (
        "centre_name",
        "district",
        "facility_type",
        "facility_code",
        "is_active",
    )
    list_filter = ("district", "facility_type", "is_active")
    search_fields = ("centre_name", "district", "facility_code")


@admin.register(FacilityMembership)
class FacilityMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "facility", "role", "is_active", "created_at")
    list_filter = ("role", "is_active", "facility__district")
    search_fields = ("user__username", "facility__centre_name")    