from pathlib import Path

utils_path = Path("clinical/ip_utils.py")
views_path = Path("clinical/views.py")

utils = utils_path.read_text(encoding="utf-8-sig")
views = views_path.read_text(encoding="utf-8-sig")

replacements = [
    (
        "def _historical_ip_summary(target_date):",
        "def _historical_ip_summary(target_date, facility):",
    ),
    (
        "record = DailyCensus.objects.filter(\n        date=target_date\n    ).first()",
        "record = DailyCensus.objects.filter(\n        facility=facility,\n        date=target_date\n    ).first()",
    ),
    (
        "return _historical_ip_summary(target_date)",
        "return _historical_ip_summary(target_date, facility)",
    ),
    (
        "def calculate_ip_summary(target_date):",
        "def calculate_ip_summary(target_date, facility):",
    ),
    (
        "patients = IPPatient.objects.filter(\n        admission_date__lte=target_date\n    )",
        "patients = IPPatient.objects.filter(\n        facility=facility,\n        admission_date__lte=target_date\n    )",
    ),
]

for old, new in replacements:
    if old not in utils:
        raise SystemExit(f"Expected code not found in ip_utils.py:\n{old}")

old_call = "calculate_ip_summary(selected_date)"
new_call = "calculate_ip_summary(selected_date, facility)"

if old_call not in views:
    raise SystemExit("Expected calculate_ip_summary call not found in views.py")

updated_utils = utils
for old, new in replacements:
    updated_utils = updated_utils.replace(old, new, 1)

updated_views = views.replace(old_call, new_call, 1)

utils_path.write_text(updated_utils, encoding="utf-8")
views_path.write_text(updated_views, encoding="utf-8")

print("Updated historical and current IP summaries with facility filtering.")
print("Updated daily census to pass its assigned facility.")