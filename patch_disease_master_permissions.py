from pathlib import Path

path = Path("clinical/views.py")
source = path.read_text(encoding="utf-8-sig")

start_marker = "@login_required\ndef disease_master(request):"
end_marker = "\ndef get_disease_balance("

start = source.find(start_marker)
end = source.find(end_marker, start)

if start == -1 or end == -1:
    raise SystemExit("Could not locate the disease_master function boundaries.")

section = source[start:end]

old = """    if request.method == "POST":
        form = DiseaseMasterForm(request.POST)
"""

new = """    if request.method == "POST":
        if not request.user.is_superuser:
            return HttpResponse(
                "Only a system administrator can modify the shared disease master.",
                status=403,
            )

        form = DiseaseMasterForm(request.POST)
"""

if new in section:
    print("Disease master permission check is already present.")
elif old in section:
    section = section.replace(old, new, 1)
    source = source[:start] + section + source[end:]
    path.write_text(source, encoding="utf-8")
    print("Restricted disease master changes to Django superusers.")
else:
    raise SystemExit("Expected POST block not found. No changes saved.")