from pathlib import Path

path = Path("clinical/views.py")
source = path.read_text(encoding="utf-8")

targets = [
    (
        '"clinical/ip_disease_report.html",\n'
        '        {\n'
        '            "start_date": start_date,',
        '"clinical/ip_disease_report.html",\n'
        '        {\n'
        '            "facility": facility,\n'
        '            "start_date": start_date,',
    ),
    (
        '"clinical/ip_ncd_report.html",\n'
        '        {\n'
        '            "start_date": start_date,',
        '"clinical/ip_ncd_report.html",\n'
        '        {\n'
        '            "facility": facility,\n'
        '            "start_date": start_date,',
    ),
]

for old, new in targets:
    count = source.count(old)
    if count != 1:
        raise SystemExit(
            f"STOP: Expected one match, found {count}. No changes saved."
        )
    source = source.replace(old, new, 1)

path.write_text(source, encoding="utf-8")
print("SUCCESS: Added facility to both report contexts.")