from pathlib import Path

path = Path("clinical/views.py")
source = path.read_text(encoding="utf-8-sig")

start_marker = "def monthly_disease_report(request):"
end_marker = "\n@login_required\ndef daily_ncd_count(request):"

start = source.find(start_marker)
end = source.find(end_marker, start)

if start == -1 or end == -1:
    raise SystemExit("Could not locate the monthly disease report boundaries.")

section = source[start:end]

if "facility = get_user_facility(request)" not in section:
    section = section.replace(
        start_marker,
        start_marker + "\n    facility = get_user_facility(request)",
        1,
    )

old_query = """DailyDiseaseCount.objects.filter(
            disease=disease,
            date__range=(start_date, end_date),
        )"""

new_query = """DailyDiseaseCount.objects.filter(
            facility=facility,
            disease=disease,
            date__range=(start_date, end_date),
        )"""

if new_query not in section:
    if old_query not in section:
        raise SystemExit(
            "Expected DailyDiseaseCount query not found. No changes saved."
        )
    section = section.replace(old_query, new_query, 1)

if "facility=facility" not in section:
    raise SystemExit("Facility filter verification failed. No changes saved.")

source = source[:start] + section + source[end:]
path.write_text(source, encoding="utf-8")

print("Updated monthly OP disease report with facility-scoped data.")