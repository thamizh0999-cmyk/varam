from pathlib import Path

path = Path("clinical/views.py")
source = path.read_text(encoding="utf-8-sig")

start_marker = "@login_required\ndef anc_register(request):"
end_marker = "@login_required\ndef anc_monthly_report_excel(request):"

start = source.find(start_marker)
end = source.find(end_marker, start)

if start == -1 or end == -1:
    raise SystemExit("Could not locate ANC view boundaries. No changes made.")

replacement = '''@login_required
def anc_register(request):
    facility = get_user_facility(request)
    patients = ANCPatient.objects.filter(facility=facility).order_by("name")

    return render(
        request,
        "clinical/anc_register.html",
        {
            "patients": patients,
            "facility": facility,
        },
    )


@login_required
def anc_patient_add(request):
    facility = get_user_facility(request)

    if request.method == "POST":
        form = ANCPatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.facility = facility
            patient.save()
            messages.success(request, "ANC patient registered successfully.")
            return redirect("anc_register")
    else:
        form = ANCPatientForm()

    return render(
        request,
        "clinical/anc_patient_form.html",
        {"form": form, "facility": facility},
    )


@login_required
def anc_patient_edit(request, pk):
    facility = get_user_facility(request)
    patient = get_object_or_404(ANCPatient, pk=pk, facility=facility)

    if request.method == "POST":
        form = ANCPatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "ANC patient details updated successfully.")
            return redirect("anc_patient_detail", pk=patient.pk)
    else:
        form = ANCPatientForm(instance=patient)

    return render(
        request,
        "clinical/anc_patient_form.html",
        {
            "form": form,
            "patient": patient,
            "editing": True,
            "facility": facility,
        },
    )


@login_required
def anc_patient_detail(request, pk):
    facility = get_user_facility(request)
    patient = get_object_or_404(ANCPatient, pk=pk, facility=facility)
    visits = patient.visits.all().order_by("-visit_date", "-id")

    return render(
        request,
        "clinical/anc_patient_detail.html",
        {
            "patient": patient,
            "visits": visits,
            "facility": facility,
        },
    )


@login_required
def anc_visit_add(request, pk):
    facility = get_user_facility(request)
    patient = get_object_or_404(ANCPatient, pk=pk, facility=facility)

    if request.method == "POST":
        form = ANCVisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.patient = patient
            visit.save()
            messages.success(request, "ANC visit saved successfully.")
            return redirect("anc_patient_detail", pk=patient.pk)
    else:
        form = ANCVisitForm(initial={"visit_date": timezone.localdate()})

    return render(
        request,
        "clinical/anc_visit_form.html",
        {"patient": patient, "form": form, "facility": facility},
    )


@login_required
def anc_visit_edit(request, pk, visit_id):
    facility = get_user_facility(request)
    patient = get_object_or_404(ANCPatient, pk=pk, facility=facility)
    visit = get_object_or_404(ANCVisit, pk=visit_id, patient=patient)

    if request.method == "POST":
        form = ANCVisitForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()
            messages.success(request, "ANC visit updated successfully.")
            return redirect("anc_patient_detail", pk=patient.pk)
    else:
        form = ANCVisitForm(instance=visit)

    return render(
        request,
        "clinical/anc_visit_form.html",
        {
            "patient": patient,
            "form": form,
            "visit": visit,
            "editing": True,
            "facility": facility,
        },
    )


'''

path.write_text(source[:start] + replacement + source[end:], encoding="utf-8")
print("Updated ANC patient and visit views with facility isolation.")