from django.db import models


class DailyCensus(models.Model):
    facility = models.ForeignKey(
    "CentreProfile",
    on_delete=models.PROTECT,
    related_name="daily_census_records",
)
    date = models.DateField()

    # OP - Morning New
    op_morning_new_male = models.PositiveIntegerField(default=0)
    op_morning_new_female = models.PositiveIntegerField(default=0)
    op_morning_new_male_child = models.PositiveIntegerField(default=0)
    op_morning_new_female_child = models.PositiveIntegerField(default=0)

    # OP - Morning Old
    op_morning_old_male = models.PositiveIntegerField(default=0)
    op_morning_old_female = models.PositiveIntegerField(default=0)
    op_morning_old_male_child = models.PositiveIntegerField(default=0)
    op_morning_old_female_child = models.PositiveIntegerField(default=0)

    # OP - Evening New
    op_evening_new_male = models.PositiveIntegerField(default=0)
    op_evening_new_female = models.PositiveIntegerField(default=0)
    op_evening_new_male_child = models.PositiveIntegerField(default=0)
    op_evening_new_female_child = models.PositiveIntegerField(default=0)

    # OP - Evening Old
    op_evening_old_male = models.PositiveIntegerField(default=0)
    op_evening_old_female = models.PositiveIntegerField(default=0)
    op_evening_old_male_child = models.PositiveIntegerField(default=0)
    op_evening_old_female_child = models.PositiveIntegerField(default=0)

    # Existing IP fields retained for now for old data.
    # New IP calculations will come from IPPatient.
    ip_morning_male = models.PositiveIntegerField(default=0)
    ip_morning_female = models.PositiveIntegerField(default=0)
    ip_morning_male_child = models.PositiveIntegerField(default=0)
    ip_morning_female_child = models.PositiveIntegerField(default=0)

    ip_evening_male = models.PositiveIntegerField(default=0)
    ip_evening_female = models.PositiveIntegerField(default=0)
    ip_evening_male_child = models.PositiveIntegerField(default=0)
    ip_evening_female_child = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def op_new_male(self):
        return self.op_morning_new_male + self.op_evening_new_male

    @property
    def op_new_female(self):
        return self.op_morning_new_female + self.op_evening_new_female

    @property
    def op_new_male_child(self):
        return self.op_morning_new_male_child + self.op_evening_new_male_child

    @property
    def op_new_female_child(self):
        return self.op_morning_new_female_child + self.op_evening_new_female_child

    @property
    def op_old_male(self):
        return self.op_morning_old_male + self.op_evening_old_male

    @property
    def op_old_female(self):
        return self.op_morning_old_female + self.op_evening_old_female

    @property
    def op_old_male_child(self):
        return self.op_morning_old_male_child + self.op_evening_old_male_child

    @property
    def op_old_female_child(self):
        return self.op_morning_old_female_child + self.op_evening_old_female_child

    @property
    def op_new_total(self):
        return (
            self.op_new_male
            + self.op_new_female
            + self.op_new_male_child
            + self.op_new_female_child
        )

    @property
    def op_old_total(self):
        return (
            self.op_old_male
            + self.op_old_female
            + self.op_old_male_child
            + self.op_old_female_child
        )

    @property
    def op_total(self):
        return self.op_new_total + self.op_old_total

    def __str__(self):
        return str(self.date)

    class Meta:
     constraints = [
        models.UniqueConstraint(
            fields=["facility", "date"],
            name="unique_daily_census_per_facility_date",
        )
    ]
class IPPatient(models.Model):
    facility = models.ForeignKey(
        "CentreProfile",
        on_delete=models.PROTECT,
        related_name="ip_patients",
    )

    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    SESSION_CHOICES = [
        ("MORNING", "Morning"),
        ("EVENING", "Evening"),
    ]

    name = models.CharField(max_length=200)

    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES
    )

    is_child = models.BooleanField(default=False)

    admission_date = models.DateField()

    admission_session = models.CharField(
        max_length=10,
        choices=SESSION_CHOICES,
        default="MORNING"
    )

    discharge_date = models.DateField(
        null=True,
        blank=True
    )

    discharge_session = models.CharField(
        max_length=10,
        choices=SESSION_CHOICES,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "-admission_date",
            "-id",
        ]

    @property
    def is_discharged(self):
        return self.discharge_date is not None

    def __str__(self):
        return f"{self.name} - {self.admission_date}"

class DiseaseMaster(models.Model):
    name = models.CharField(max_length=200, unique=True)
    tamil_name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=100, blank=True)
    is_ncd = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        if self.tamil_name:
            return f"{self.tamil_name} ({self.name})"
        return self.name


class DailyDiseaseCount(models.Model):
    facility = models.ForeignKey(
    "CentreProfile",
    on_delete=models.PROTECT,
    related_name="%(class)s_records",
)
    date = models.DateField()

    disease = models.ForeignKey(
        DiseaseMaster,
        on_delete=models.PROTECT,
        related_name="daily_counts",
    )

    male_count = models.PositiveIntegerField(default=0)
    female_count = models.PositiveIntegerField(default=0)
    child_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
    models.UniqueConstraint(
        fields=["facility", "date", "disease"],
        name="unique_daily_disease_per_facility",
    )
]
        ordering = ["date", "disease__name"]

    @property
    def total_count(self):
        return (
            self.male_count
            + self.female_count
            + self.child_count
        )

    def __str__(self):
        return f"{self.date} - {self.disease.name}"
class DailyNCDCount(models.Model):
    facility = models.ForeignKey(
    "CentreProfile",
    on_delete=models.PROTECT,
    related_name="%(class)s_records",
)
    NCD_CHOICES = [
        ("DIABETES", "Diabetes Mellitus"),
        ("HYPERTENSION", "Hypertension"),
        ("HEART", "Heart Cases"),
        ("CANCER", "Cancer"),
        ("OBESITY", "Obesity"),
        ("ANAEMIA", "Anaemia"),
        ("ASTHMA", "Bronchial Asthma"),
    ]

    date = models.DateField()
    disease = models.CharField(max_length=30, choices=NCD_CHOICES)

    male_count = models.PositiveIntegerField(default=0)
    female_count = models.PositiveIntegerField(default=0)
    child_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
    models.UniqueConstraint(
        fields=["facility", "date", "disease"],
        name="unique_daily_ncd_per_facility",
    )
]
        ordering = ["date", "disease"]

    @property
    def total_count(self):
        return (
            self.male_count
            + self.female_count
            + self.child_count
        )

    def __str__(self):
        return f"{self.date} - {self.get_disease_display()}"  
class CentreProfile(models.Model):
    centre_name = models.CharField(max_length=200)
    centre_address = models.TextField(blank=True)
    district = models.CharField(max_length=100, default="Thoothukudi")
    facility_type = models.CharField(
        max_length=30,
        choices=[
            ("GH", "Government Hospital"),
            ("PHC", "Primary Health Centre"),
            ("OTHER", "Other Government Facility"),
        ],
        default="GH",
    )
    facility_code = models.CharField(max_length=50, blank=True)
    doctor_name = models.CharField(max_length=200, blank=True)
    mobile_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["centre_name"]

    def __str__(self):
        return self.centre_name 
class FacilityMembership(models.Model):
    ROLE_CHOICES = [
        ("FACILITY_ADMIN", "Facility Administrator"),
        ("DOCTOR", "Doctor"),
        ("DATA_ENTRY", "Data Entry Staff"),
        ("DISTRICT_ADMIN", "District Administrator"),
    ]

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="facility_memberships",
    )
    facility = models.ForeignKey(
        CentreProfile,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default="DATA_ENTRY",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "facility"],
                name="unique_user_facility_membership",
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.facility.centre_name}"          
class ANCPatient(models.Model):
    facility = models.ForeignKey(
    "CentreProfile",
    on_delete=models.PROTECT,
    related_name="%(class)s_records",
)
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    mobile_number = models.CharField(max_length=20, blank=True)
    pigmi_no = models.CharField(max_length=100, blank=True)

    age = models.PositiveIntegerField()

    lmp = models.DateField()
    edd = models.DateField()

    height_cm = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    blood_group = models.CharField(max_length=10, blank=True)

    menstrual_history = models.CharField(
        max_length=20,
        blank=True,
    )

    married_at_age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    past_history = models.TextField(blank=True)
    obstetrics_history = models.TextField(blank=True)

    gravida = models.PositiveIntegerField(default=1)
    para = models.PositiveIntegerField(default=0)
    living = models.PositiveIntegerField(default=0)
    abortion = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.pigmi_no or 'No Pigmi'}"


class ANCVisit(models.Model):
    TRIMESTER_CHOICES = [
        ("1ST", "1st Trimester"),
        ("2ND", "2nd Trimester"),
        ("3RD", "3rd Trimester"),
        ("POSTNATAL", "Post-Natal"),
    ]

    patient = models.ForeignKey(
        ANCPatient,
        on_delete=models.CASCADE,
        related_name="visits",
    )

    visit_date = models.DateField()

    trimester = models.CharField(
        max_length=20,
        choices=TRIMESTER_CHOICES,
    )

    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    hb = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )

    bp = models.CharField(
        max_length=20,
        blank=True,
    )

    gdm_pih_complications = models.TextField(
        blank=True,
    )

    disease = models.ForeignKey(
        DiseaseMaster,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="anc_visits",
    )

    week_of_delivery = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    mode_of_delivery = models.CharField(
        max_length=100,
        blank=True,
    )

    baby_sex = models.CharField(
        max_length=20,
        blank=True,
    )

    baby_weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        null=True,
        blank=True,
    )

    neonatal_jaundice = models.BooleanField(
        default=False,
    )

    baby_status = models.CharField(
        max_length=100,
        blank=True,
    )

    mother_status = models.CharField(
        max_length=100,
        blank=True,
    )

    dosage = models.TextField(
        blank=True,
    )
    kit_issued = models.BooleanField(default=False)
    kit_issue_date = models.DateField(null=True, blank=True)
    kit_trimester = models.CharField(
    max_length=20,
    choices=TRIMESTER_CHOICES,
    blank=True,
)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-visit_date", "-id"]

    def __str__(self):
        return f"{self.patient.name} - {self.visit_date}"
class MagapperuSanjeeviKit(models.Model):
    facility = models.ForeignKey(
        "CentreProfile",
        on_delete=models.PROTECT,
        related_name="%(class)s_records",
    )
    date_despatched = models.DateField()

    no_of_kits_supplied = models.PositiveIntegerField(default=0)

    dosage = models.PositiveIntegerField(default=0)

    first_trimester = models.PositiveIntegerField(default=0)
    second_trimester = models.PositiveIntegerField(default=0)
    third_trimester = models.PositiveIntegerField(default=0)
    after_child_birth = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_despatched", "-id"]

    @property
    def grand_total(self):
        return (
            self.first_trimester
            + self.second_trimester
            + self.third_trimester
            + self.after_child_birth
        )

    @property
    def remaining_dosage(self):
        return self.dosage - self.grand_total

    def __str__(self):
        return f"{self.date_despatched} - {self.no_of_kits_supplied} kits"

class IPDiseaseRecord(models.Model):
    patient = models.ForeignKey(
        IPPatient,
        on_delete=models.CASCADE,
        related_name="disease_records",
    )
    disease = models.ForeignKey(
        DiseaseMaster,
        on_delete=models.PROTECT,
        related_name="ip_disease_records",
    )
    diagnosis_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-diagnosis_date", "patient__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["patient", "disease", "diagnosis_date"],
                name="unique_ip_patient_disease_date",
            )
        ]

    def __str__(self):
        return f"{self.patient.name} - {self.disease.name} - {self.diagnosis_date}"


class IPNCDRecord(models.Model):
    patient = models.ForeignKey(
        IPPatient,
        on_delete=models.CASCADE,
        related_name="ncd_records",
    )
    disease = models.CharField(
        max_length=30,
        choices=DailyNCDCount.NCD_CHOICES,
    )
    diagnosis_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-diagnosis_date", "patient__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["patient", "disease", "diagnosis_date"],
                name="unique_ip_patient_ncd_date",
            )
        ]

    def __str__(self):
        return f"{self.patient.name} - {self.get_disease_display()} - {self.diagnosis_date}"

