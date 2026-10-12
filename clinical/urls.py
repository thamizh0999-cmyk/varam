from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("", views.daily_census, name="daily_census"),
    path("ip/", views.ip_register, name="ip_register"),
    path("ip/diseases/", views.ip_disease_entry, name="ip_disease_entry"),
    path("ip/ncd/", views.ip_ncd_entry, name="ip_ncd_entry"),
    path("ip/diseases/<int:pk>/edit/", views.ip_disease_edit, name="ip_disease_edit"),
    path("ip/diseases/<int:pk>/delete/", views.ip_disease_delete, name="ip_disease_delete"),
    path("ip/ncd/<int:pk>/edit/", views.ip_ncd_edit, name="ip_ncd_edit"),
    path("ip/ncd/<int:pk>/delete/", views.ip_ncd_delete, name="ip_ncd_delete"),
    path("ip/fortnightly-report/", views.ip_fortnightly_report, name="ip_fortnightly_report"),
    path("ip/<int:pk>/edit/", views.ip_edit, name="ip_edit"),
    path("ip/<int:pk>/delete/", views.ip_delete, name="ip_delete"),
    path("diseases/", views.disease_master, name="disease_master"),
    path("diseases/daily/", views.daily_disease_count, name="daily_disease_count"),
    path("diseases/monthly-report/", views.monthly_disease_report, name="monthly_disease_report"),
    path("diseases/monthly-top20/", views.monthly_top20_op_report, name="monthly_top20_op_report"),
    path("ip/monthly-top20/", views.monthly_top20_ip_report, name="monthly_top20_ip_report"),
    path("ncd/daily/", views.daily_ncd_count, name="daily_ncd_count"),
    path("centre/", views.centre_profile, name="centre_profile"),
    path("anc/", views.anc_register, name="anc_register"),
    path("anc/add/", views.anc_patient_add, name="anc_patient_add"),
    path("anc/monthly-report/", views.anc_monthly_report, name="anc_monthly_report"),
    path("anc/monthly-report/excel/", views.anc_monthly_report_excel, name="anc_monthly_report_excel"),
    path("anc/<int:pk>/", views.anc_patient_detail, name="anc_patient_detail"),
    path("anc/<int:pk>/edit/", views.anc_patient_edit, name="anc_patient_edit"),
    path("anc/<int:pk>/visit/add/", views.anc_visit_add, name="anc_visit_add"),
    path(
    "anc/<int:pk>/visit/<int:visit_id>/edit/",
    views.anc_visit_edit,
    name="anc_visit_edit",
),
path("ip/disease-report/", views.ip_disease_report, name="ip_disease_report"),
path("ip/ncd-report/", views.ip_ncd_report, name="ip_ncd_report"),
]

