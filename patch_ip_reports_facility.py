from pathlib import Path

path = Path("clinical/views.py")
source = path.read_text(encoding="utf-8-sig")

changes = [
    (
        "def ip_disease_report(request):",
        "IPDiseaseRecord.objects.filter(\n        diagnosis_date__range=(start_date, end_date)\n    )",
        "IPDiseaseRecord.objects.filter(\n        patient__facility=facility,\n        diagnosis_date__range=(start_date, end_date)\n    )",
    ),
    (
        "def ip_ncd_report(request):",
        "IPNCDRecord.objects.filter(\n        diagnosis_date__range=(start_date, end_date)\n    )",
        "IPNCDRecord.objects.filter(\n        patient__facility=facility,\n        diagnosis_date__range=(start_date, end_date)\n    )",
    ),
]

for function_marker, old_query, new_query in changes:
    start = source.find(function_marker)
    if start == -1:
        raise SystemExit(f"Could not find: {function_marker}")

    next_view = source.find("\n@login_required\ndef ", start + len(function_marker))
    if next_view == -1:
        next_view = len(source)

    section = source[start:next_view]

    if "facility = get_user_facility(request)" not in section:
        section = section.replace(
            function_marker,
            function_marker + "\n    facility = get_user_facility(request)",
            1,
        )

    if new_query not in section:
        if old_query not in section:
            raise SystemExit(
                f"Expected query not found in {function_marker}. No file changes saved."
            )
        section = section.replace(old_query, new_query, 1)

    source = source[:start] + section + source[next_view:]

path.write_text(source, encoding="utf-8")
print("Updated IP disease and NCD reports with facility-scoped queries.")