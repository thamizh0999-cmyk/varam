from django.conf import settings
from django.db import models
from django.db.models import Max


class Register(models.Model):
    REGISTER_TYPES = [
        ("GENERAL", "General Register"),
        ("OP", "OP Register"),
        ("FINANCE", "Finance Ledger"),
        ("STOCK", "Stock Register"),
        ("SUB_STOCK", "Sub-stock Register"),
        ("INVOICE", "Invoice Register"),
        ("CHO_MEDICINE", "CHO Medicine Register"),
    ]

    facility = models.ForeignKey(
        "clinical.CentreProfile",
        on_delete=models.PROTECT,
        related_name="custom_registers",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    register_type = models.CharField(
        max_length=30,
        choices=REGISTER_TYPES,
        default="GENERAL",
    )
    serial_prefix = models.CharField(max_length=30, blank=True)
    next_serial_number = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_registers",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(
                fields=["facility", "title"],
                name="unique_register_title_per_facility",
            ),
        ]

    def __str__(self):
        return f"{self.title} - {self.facility.centre_name}"


class RegisterField(models.Model):
    FIELD_TYPES = [
        ("TEXT", "Text"),
        ("NUMBER", "Number"),
        ("DATE", "Date"),
        ("CHOICE", "Dropdown"),
        ("BOOLEAN", "Yes/No"),
        ("FORMULA", "Calculated Number"),
    ]

    register = models.ForeignKey(
        Register,
        on_delete=models.CASCADE,
        related_name="fields",
    )
    label = models.CharField(max_length=100)
    field_key = models.SlugField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=False)
    choices_text = models.TextField(
        blank=True,
        help_text="For dropdowns, enter one option per line.",
    )
    formula = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional arithmetic formula using field keys.",
    )
    position = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["position", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["register", "field_key"],
                name="unique_field_key_per_register",
            ),
        ]

    def __str__(self):
        return f"{self.register.title}: {self.label}"

    @property
    def choices_list(self):
        return [
            item.strip()
            for item in self.choices_text.splitlines()
            if item.strip()
        ]


class RegisterEntry(models.Model):
    register = models.ForeignKey(
        Register,
        on_delete=models.PROTECT,
        related_name="entries",
    )
    serial_number = models.PositiveIntegerField()
    entry_date = models.DateField()
    data = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="register_entries_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="register_entries_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-entry_date", "-serial_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["register", "serial_number"],
                name="unique_serial_per_register",
            ),
        ]

    def __str__(self):
        return f"{self.register.title} #{self.serial_number}"

    @property
    def display_serial(self):
        prefix = self.register.serial_prefix
        return f"{prefix}{self.serial_number:05d}" if prefix else str(self.serial_number)

class ExternalTherapyCount(models.Model):
    THERAPY_CHOICES = [
        ("KATTUTHAL", "Kattuthal (Bandage Dressing)"),
        ("PATRU", "Patru (Paste)"),
        ("OTTRADAM", "Ottradam (Fomentation)"),
        ("PURA_VALAYAM", "Pura Valayam (Oil Pooling)"),
        ("VARAM", "Varmam (Physical Manipulation)"),
        ("POOCHU", "Poochu (Anointing)"),
        ("VEDHU", "Vedhu (Vapour Bath / Steam)"),
        ("THOKKANAM", "Thokkanam (Oil Massages)"),
        ("PUGAI", "Pugai (Fumigation)"),
        ("KALIMBU", "Kalimbu (Ointment)"),
        ("SUTTIKAI", "Suttikai (Cauterization)"),
        ("OTHERS", "Others"),
    ]

    facility = models.ForeignKey(
        "clinical.CentreProfile",
        on_delete=models.PROTECT,
        related_name="external_therapy_counts",
    )
    therapy = models.CharField(max_length=30, choices=THERAPY_CHOICES)
    treatment_date = models.DateField()
    count = models.PositiveIntegerField(default=0)
    notes = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="external_therapy_counts_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["treatment_date", "therapy"]
        constraints = [
            models.UniqueConstraint(
                fields=["facility", "treatment_date", "therapy"],
                name="unique_daily_external_therapy_per_facility",
            ),
        ]

    def __str__(self):
        return f"{self.get_therapy_display()} - {self.treatment_date}: {self.count}"


class NominalPatient(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    facility = models.ForeignKey(
        "clinical.CentreProfile",
        on_delete=models.PROTECT,
        related_name="nominal_patients",
    )
    serial_number = models.PositiveIntegerField()
    op_number = models.CharField(max_length=40)
    name = models.CharField(max_length=150)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    diagnosis = models.CharField(max_length=255)
    medicine = models.TextField(blank=True)
    registered_date = models.DateField(default=__import__("django.utils.timezone", fromlist=["localdate"]).localdate)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="nominal_patients_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-registered_date", "-serial_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["facility", "serial_number"],
                name="unique_nominal_serial_per_facility",
            ),
            models.UniqueConstraint(
                fields=["facility", "op_number"],
                name="unique_nominal_op_per_facility",
            ),
        ]

    @property
    def is_child(self):
        return self.age <= 12

    def __str__(self):
        return f"{self.op_number} - {self.name}"


class OPEncounter(models.Model):
    SESSION_CHOICES = [
        ("MORNING", "Morning"),
        ("EVENING", "Evening"),
    ]
    CASE_CHOICES = [
        ("NEW", "New case"),
        ("OLD", "Old case"),
    ]

    facility = models.ForeignKey(
        "clinical.CentreProfile",
        on_delete=models.PROTECT,
        related_name="op_encounters",
    )
    patient = models.ForeignKey(
        NominalPatient,
        on_delete=models.PROTECT,
        related_name="encounters",
    )
    encounter_date = models.DateField()
    session = models.CharField(max_length=10, choices=SESSION_CHOICES)
    case_type = models.CharField(max_length=3, choices=CASE_CHOICES)
    diagnosis = models.CharField(max_length=255, blank=True)
    medicine = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="op_encounters_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-encounter_date", "session", "patient__serial_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["facility", "patient", "encounter_date", "session"],
                name="unique_patient_op_session_per_day",
            ),
        ]

    def __str__(self):
        return f"{self.patient.op_number} - {self.encounter_date} - {self.session}"


class ExternalTherapyVisit(models.Model):
    facility = models.ForeignKey(
        "clinical.CentreProfile",
        on_delete=models.PROTECT,
        related_name="patient_therapy_visits",
    )
    encounter = models.ForeignKey(
        OPEncounter,
        on_delete=models.PROTECT,
        related_name="therapy_visits",
    )
    therapy = models.CharField(
        max_length=30,
        choices=ExternalTherapyCount.THERAPY_CHOICES,
    )
    treatment_date = models.DateField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="patient_therapy_visits_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-treatment_date", "encounter__patient__serial_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["facility", "encounter", "treatment_date", "therapy"],
                name="unique_encounter_therapy_per_day",
            ),
        ]

    def __str__(self):
        return f"{self.encounter.patient.op_number} - {self.get_therapy_display()} - {self.treatment_date}"

# ============================================================
# VARAM DIAGNOSIS MASTER
# ============================================================

class DiagnosisMaster(models.Model):
    CATEGORY_CHOICES = [
        ("SIDDHA_OP", "Siddha Regular OP"),
        ("DISEASE_REPORT", "Additional Disease Reporting"),
    ]

    facility = models.ForeignKey(
        "clinical.CentreProfile",
        on_delete=models.PROTECT,
        related_name="diagnosis_master_entries",
    )
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    code = models.CharField(max_length=40)
    name = models.CharField(max_length=200)
    tamil_name = models.CharField(max_length=200, blank=True)
    reporting_category = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["facility", "category", "code"],
                name="unique_diagnosis_code_per_facility",
            ),
            models.UniqueConstraint(
                fields=["facility", "category", "name"],
                name="unique_diagnosis_name_per_facility",
            ),
        ]

    def __str__(self):
        return self.name


# ============================================================
# ANC PREGNANCY RECORD - ONE PER PREGNANCY
# ============================================================

class ANCPregnancy(models.Model):
    STATUS_CHOICES = [
        ("ONGOING", "Ongoing"),
        ("DELIVERED", "Delivered"),
        ("CLOSED", "Closed"),
    ]

    facility = models.ForeignKey(
        "clinical.CentreProfile",
        on_delete=models.PROTECT,
        related_name="anc_pregnancies",
    )
    patient = models.ForeignKey(
        NominalPatient,
        on_delete=models.PROTECT,
        related_name="pregnancies",
    )
    rch_id = models.CharField(max_length=80, blank=True)
    pregnancy_number = models.PositiveSmallIntegerField(default=1)
    lmp = models.DateField(null=True, blank=True)
    edd = models.DateField(null=True, blank=True)
    registration_date = models.DateField()
    gravida = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="ONGOING",
    )
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="anc_pregnancies_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-registration_date", "-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["facility", "patient", "pregnancy_number"],
                name="unique_patient_pregnancy_number",
            ),
        ]

    def __str__(self):
        return f"{self.patient.op_number} - Pregnancy {self.pregnancy_number}"


# ============================================================
# ANC FOLLOW-UP - ONE RECORD PER VISIT
# ============================================================

class ANCVisit(models.Model):
    TRIMESTER_CHOICES = [
        ("T1", "First trimester"),
        ("T2", "Second trimester"),
        ("T3", "Third trimester"),
    ]

    KIT_CHOICES = [
        ("YES", "Issued"),
        ("NO", "Not issued"),
    ]

    facility = models.ForeignKey(
        "clinical.CentreProfile",
        on_delete=models.PROTECT,
        related_name="anc_visits",
    )
    pregnancy = models.ForeignKey(
        ANCPregnancy,
        on_delete=models.PROTECT,
        related_name="visits",
    )
    visit_date = models.DateField()
    trimester = models.CharField(
        max_length=2,
        choices=TRIMESTER_CHOICES,
        blank=True,
    )
    weight_kg = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    hb = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    bp = models.CharField(max_length=30, blank=True)
    height_cm = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    kit_issued = models.CharField(
        max_length=3, choices=KIT_CHOICES, default="NO"
    )
    kit_issue_date = models.DateField(null=True, blank=True)
    kit_trimester = models.CharField(
        max_length=2,
        choices=TRIMESTER_CHOICES,
        blank=True,
    )
    dosage = models.CharField(max_length=150, blank=True)
    urine_test = models.CharField(max_length=150, blank=True)
    high_risk = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="anc_visits_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-visit_date", "-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["facility", "pregnancy", "visit_date"],
                name="unique_anc_visit_per_day",
            ),
        ]

    def __str__(self):
        return f"{self.pregnancy.patient.op_number} - ANC {self.visit_date}"


# ============================================================
# DELIVERY AND NEWBORN OUTCOME - SAME PREGNANCY
# ============================================================

class ANCDelivery(models.Model):
    DELIVERY_MODE_CHOICES = [
        ("NORMAL", "Normal delivery"),
        ("LSCS", "LSCS"),
        ("ASSISTED", "Assisted delivery"),
        ("OTHER", "Other"),
    ]

    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("U", "Unknown / Not recorded"),
    ]

    STATUS_CHOICES = [
        ("ALIVE", "Alive"),
        ("DECEASED", "Deceased"),
        ("UNKNOWN", "Unknown / Not recorded"),
    ]

    facility = models.ForeignKey(
        "clinical.CentreProfile",
        on_delete=models.PROTECT,
        related_name="anc_deliveries",
    )
    pregnancy = models.OneToOneField(
        ANCPregnancy,
        on_delete=models.PROTECT,
        related_name="delivery",
    )
    delivery_date = models.DateField()
    delivery_week = models.PositiveSmallIntegerField(null=True, blank=True)
    delivery_mode = models.CharField(
        max_length=10,
        choices=DELIVERY_MODE_CHOICES,
        blank=True,
    )
    baby_sex = models.CharField(
        max_length=1, choices=SEX_CHOICES, blank=True
    )
    baby_weight_kg = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    neonatal_jaundice = models.BooleanField(default=False)
    baby_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, blank=True
    )
    mother_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, blank=True
    )
    remarks = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="anc_deliveries_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-delivery_date"]

    def __str__(self):
        return f"{self.pregnancy.patient.op_number} - Delivery {self.delivery_date}"

