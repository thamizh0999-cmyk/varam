
from django import forms


from .models import (
    DailyCensus,
    IPPatient,
    IPDiseaseRecord,
    IPNCDRecord,
    DiseaseMaster,
    DailyDiseaseCount,
    DailyNCDCount,
    CentreProfile,
    ANCPatient,
    ANCVisit,
)

class DailyCensusForm(forms.ModelForm):

    class Meta:
        model = DailyCensus
        exclude = [
            "created_at",
            "updated_at",

            # IP is now calculated automatically
            "ip_morning_male",
            "ip_morning_female",
            "ip_morning_male_child",
            "ip_morning_female_child",
            "ip_evening_male",
            "ip_evening_female",
            "ip_evening_male_child",
            "ip_evening_female_child",
        ]

        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
        }


class IPPatientForm(forms.ModelForm):

    class Meta:
        model = IPPatient
        fields = [
            "name",
            "sex",
            "is_child",
            "admission_date",
            "admission_session",
            "discharge_date",
            "discharge_session",
        ]

        widgets = {
            "admission_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "discharge_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }
class DiseaseMasterForm(forms.ModelForm):

    class Meta:
        model = DiseaseMaster
        fields = [
            "name",
            "tamil_name",
            "category",
            "is_ncd",
            "is_active",
        ]       
class DailyDiseaseCountForm(forms.ModelForm):
    class Meta:
        model = DailyDiseaseCount
        fields = ["male_count", "female_count", "child_count"]  
class DailyNCDCountForm(forms.ModelForm):
    class Meta:
        model = DailyNCDCount
        fields = ["male_count", "female_count", "child_count"] 
class IPDiseaseRecordForm(forms.ModelForm):
    class Meta:
        model = IPDiseaseRecord
        fields = ["patient", "disease", "diagnosis_date", "notes"]
        widgets = {
            "diagnosis_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        facility = kwargs.pop("facility", None)
        super().__init__(*args, **kwargs)

        patients = IPPatient.objects.filter(
            discharge_date__isnull=True,
            facility=facility,
        ) if facility is not None else IPPatient.objects.none()

        self.fields["patient"].queryset = patients.order_by("name")
        self.fields["disease"].queryset = DiseaseMaster.objects.filter(
            is_active=True
        ).order_by("name")


class IPNCDRecordForm(forms.ModelForm):
    class Meta:
        model = IPNCDRecord
        fields = ["patient", "disease", "diagnosis_date", "notes"]
        widgets = {
            "diagnosis_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        facility = kwargs.pop("facility", None)
        super().__init__(*args, **kwargs)

        patients = IPPatient.objects.filter(
            discharge_date__isnull=True,
            facility=facility,
        ) if facility is not None else IPPatient.objects.none()

        self.fields["patient"].queryset = patients.order_by("name")


class CentreProfileForm(forms.ModelForm):
    class Meta:
        model = CentreProfile
        fields = [
    "centre_name",
    "centre_address",
    "doctor_name",
    "mobile_number",
] 
class ANCPatientForm(forms.ModelForm):
    class Meta:
        model = ANCPatient
        fields = [
            "name",
            "address",
            "mobile_number",
            "pigmi_no",
            "age",
            "lmp",
            "edd",
            "height_cm",
            "blood_group",
            "menstrual_history",
            "married_at_age",
            "past_history",
            "obstetrics_history",
            "gravida",
            "para",
            "living",
            "abortion",
        ]

        widgets = {
            "lmp": forms.DateInput(attrs={"type": "date"}),
            "edd": forms.DateInput(attrs={"type": "date"}),
            "past_history": forms.Textarea(attrs={"rows": 2}),
            "obstetrics_history": forms.Textarea(attrs={"rows": 2}),
        }


class ANCVisitForm(forms.ModelForm):
    class Meta:
        model = ANCVisit
        fields = [
            "visit_date",
            "trimester",
            "weight_kg",
            "hb",
            "bp",
            "gdm_pih_complications",
            "dosage",
            "kit_issued",
            "kit_issue_date",
            "kit_trimester",
            "week_of_delivery",
            "mode_of_delivery",
            "baby_sex",
            "baby_weight_kg",
            "neonatal_jaundice",
            "baby_status",
            "mother_status",
        ]

        widgets = {
            "visit_date": forms.DateInput(attrs={"type": "date"}),
            "kit_issue_date": forms.DateInput(attrs={"type": "date"}),
            "kit_trimester": forms.Select(),
            "gdm_pih_complications": forms.Textarea(attrs={"rows": 2}),
            "dosage": forms.Textarea(attrs={"rows": 2}),
        }                  