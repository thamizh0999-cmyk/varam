from pathlib import Path

path = Path("clinical/views.py")
source = path.read_text(encoding="utf-8-sig")

start_marker = "@login_required\ndef ip_fortnightly_report(request):"
end_marker = "@login_required\ndef ip_disease_report(request):"

start = source.find(start_marker)
end = source.find(end_marker, start)

if start == -1 or end == -1:
    raise SystemExit("Could not locate report boundaries. No changes made.")

section = source[start:end]

if "facility = get_user_facility(request)" not in section:
    section = section.replace(
        "def ip_fortnightly_report(request):",
        "def ip_fortnightly_report(request):\n    facility = get_user_facility(request)",
        1,
    )

section = section.replace(
    "IPPatient.objects.filter(\n        admission_date__range=(start_date, end_date)\n    )",
    "IPPatient.objects.filter(\n        facility=facility,\n        admission_date__range=(start_date, end_date)\n    )",
    1,
)

section = section.replace(
    "IPPatient.objects.filter(\n        discharge_date__range=(start_date, end_date)\n    )",
    "IPPatient.objects.filter(\n        facility=facility,\n        discharge_date__range=(start_date, end_date)\n    )",
    1,
)

section = section.replace(
    "DailyCensus.objects.filter(\n        date__range=(start_date, historical_end_date),",
    "DailyCensus.objects.filter(\n        facility=facility,\n        date__range=(start_date, historical_end_date),",
    1,
)

if "facility=facility" not in section:
    raise SystemExit("Facility filters were not added. No changes written.")

if section.count("facility=facility") != 3:
    raise SystemExit(
        f"Expected 3 facility filters, found {section.count('facility=facility')}. "
        "No changes written."
    )

path.write_text(source[:start] + section + source[end:], encoding="utf-8")
print("Updated IP fortnightly report: admissions, discharges, historical census.")