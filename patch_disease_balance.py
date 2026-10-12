from pathlib import Path

path = Path("clinical/views.py")
source = path.read_text(encoding="utf-8-sig")

old_function = '''def get_disease_balance(selected_date):
    op_census = DailyCensus.objects.filter(date=selected_date).first()

    disease_counts = DailyDiseaseCount.objects.filter(
        date=selected_date
    )
'''

new_function = '''def get_disease_balance(selected_date, facility):
    op_census = DailyCensus.objects.filter(
        facility=facility,
        date=selected_date,
    ).first()

    disease_counts = DailyDiseaseCount.objects.filter(
        facility=facility,
        date=selected_date,
    )
'''

if old_function not in source:
    raise SystemExit("Expected function text not found. No changes made.")

source = source.replace(old_function, new_function, 1)

old_call = "balance = get_disease_balance(selected_date)"
new_call = "balance = get_disease_balance(selected_date, facility)"

if source.count(old_call) != 1:
    raise SystemExit("Expected caller not found exactly once. No changes made.")

source = source.replace(old_call, new_call, 1)

path.write_text(source, encoding="utf-8")
print("Updated disease balance to filter by facility.")