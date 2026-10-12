from pathlib import Path

path = Path("clinical/views.py")
source = path.read_text(encoding="utf-8-sig")

targets = [
    "def anc_monthly_report_excel(request):",
    "def anc_monthly_report(request):",
]

for target in targets:
    if source.count(target) != 1:
        raise SystemExit(f"Expected exactly one occurrence of {target}")

# Add facility lookup inside each report.
for target in targets:
    source = source.replace(
        target,
        target + "\n    facility = get_user_facility(request)",
        1,
    )

# Restrict both report queries to patients belonging to this facility.
old_query = '''    visits = ANCVisit.objects.filter(
        visit_date__gte=month_start,
        visit_date__lt=next_month,
    ).select_related("patient").order_by("visit_date", "patient__name")'''

new_query = '''    visits = ANCVisit.objects.filter(
        patient__facility=facility,
        visit_date__gte=month_start,
        visit_date__lt=next_month,
    ).select_related("patient").order_by("visit_date", "patient__name")'''

if source.count(old_query) != 2:
    raise SystemExit(
        "Expected two ANC monthly report queries. No changes written."
    )

source = source.replace(old_query, new_query)

path.write_text(source, encoding="utf-8")
print("Updated ANC HTML and Excel reports with facility filtering.")