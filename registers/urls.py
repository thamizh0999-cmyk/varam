from django.urls import path
from . import views

app_name = "registers"

urlpatterns = [
    path("", views.register_list, name="list"),
    path("create/", views.register_create, name="create"),
    path("nominal/", views.nominal_list, name="nominal_list"),
    path("nominal/add/", views.nominal_create, name="nominal_create"),
    path("nominal/<int:patient_id>/encounter/", views.op_encounter_create, name="op_encounter_create"),
    path("nominal/<int:patient_id>/visits/", views.op_visit_history, name="op_visit_history"),
    path("nominal/<int:patient_id>/encounter/<int:encounter_id>/edit/", views.op_encounter_edit, name="op_encounter_edit"),
    path("nominal/<int:patient_id>/therapy/", views.patient_therapy_create, name="patient_therapy_create"),
    path("external-therapy/", views.external_therapy_daily, name="external_therapy_daily"),
    path("external-therapy/report/", views.external_therapy_report, name="external_therapy_report"),
    path("external-therapy/report/excel/", views.external_therapy_excel, name="external_therapy_excel"),
    path("<int:register_id>/", views.register_detail, name="detail"),
    path("<int:register_id>/fields/add/", views.field_create, name="field_create"),
    path("<int:register_id>/entries/add/", views.entry_create, name="entry_create"),
    path("<int:register_id>/entries/<int:entry_id>/edit/", views.entry_edit, name="entry_edit"),
    path("<int:register_id>/entries/<int:entry_id>/delete/", views.entry_delete, name="entry_delete"),
]

