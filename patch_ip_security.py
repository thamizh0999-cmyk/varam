from pathlib import Path

path = Path("clinical/views.py")
source = path.read_text(encoding="utf-8")

start_marker = "def ip_disease_edit(request, pk):"
end_marker = "def _monthly_top20_context(request):"

start = source.find(start_marker)
end = source.find(end_marker)

if start == -1 or end == -1 or end <= start:
    raise SystemExit("STOP: IP function section not found. No changes made.")

replacement = '''@login_required
def ip_disease_edit(request, pk):
    facility = get_user_facility(request)
    record = get_object_or_404(
        IPDiseaseRecord,
        pk=pk,
        patient__facility=facility,
    )
    form = IPDiseaseRecordForm(
        request.POST or None,
        instance=record,
        facility=facility,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "IP disease record updated.")
        return redirect("ip_disease_entry")

    return render(request, "clinical/ip_record_edit.html", {
        "form": form,
        "record": record,
        "kind": "Disease",
        "back_url": "/ip/diseases/",
        "facility": facility,
    })


@login_required
def ip_ncd_edit(request, pk):
    facility = get_user_facility(request)
    record = get_object_or_404(
        IPNCDRecord,
        pk=pk,
        patient__facility=facility,
    )
    form = IPNCDRecordForm(
        request.POST or None,
        instance=record,
        facility=facility,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "IP NCD record updated.")
        return redirect("ip_ncd_entry")

    return render(request, "clinical/ip_record_edit.html", {
        "form": form,
        "record": record,
        "kind": "NCD",
        "back_url": "/ip/ncd/",
        "facility": facility,
    })


@login_required
def ip_disease_delete(request, pk):
    facility = get_user_facility(request)
    record = get_object_or_404(
        IPDiseaseRecord,
        pk=pk,
        patient__facility=facility,
    )

    if request.method == "POST":
        record.delete()
        messages.success(request, "IP disease record deleted.")
        return redirect("ip_disease_entry")

    return render(request, "clinical/ip_record_delete.html", {
        "record": record,
        "kind": "Disease",
        "description": f"{record.patient.name} - {record.disease.name}",
        "back_url": "/ip/diseases/",
        "facility": facility,
    })


@login_required
def ip_ncd_delete(request, pk):
    facility = get_user_facility(request)
    record = get_object_or_404(
        IPNCDRecord,
        pk=pk,
        patient__facility=facility,
    )

    if request.method == "POST":
        record.delete()
        messages.success(request, "IP NCD record deleted.")
        return redirect("ip_ncd_entry")

    return render(request, "clinical/ip_record_delete.html", {
        "record": record,
        "kind": "NCD",
        "description": f"{record.patient.name} - {record.get_disease_display()}",
        "back_url": "/ip/ncd/",
        "facility": facility,
    })


'''

updated = source[:start] + replacement + source[end:]
path.write_text(updated, encoding="utf-8")
print("Updated four IP disease/NCD edit-delete views.")