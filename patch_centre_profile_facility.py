from pathlib import Path

path = Path("clinical/views.py")
source = path.read_text(encoding="utf-8-sig")

start_marker = "@login_required\ndef centre_profile(request):"
end_marker = "@login_required\ndef anc_register(request):"

start = source.find(start_marker)
end = source.find(end_marker, start)

if start == -1 or end == -1:
    raise SystemExit("Could not locate view boundaries. No changes made.")

replacement = '''@login_required
def centre_profile(request):
    facility = get_user_facility(request)

    if request.method == "POST":
        form = CentreProfileForm(request.POST, instance=facility)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.pk = facility.pk
            profile.save()
            messages.success(request, "Centre profile saved successfully.")
            return redirect("centre_profile")
    else:
        form = CentreProfileForm(instance=facility)
        profile = facility

    return render(
        request,
        "clinical/centre_profile.html",
        {
            "form": form,
            "profile": profile,
            "facility": facility,
        },
    )


'''

path.write_text(source[:start] + replacement + source[end:], encoding="utf-8")
print("Updated centre_profile to use the assigned facility.")