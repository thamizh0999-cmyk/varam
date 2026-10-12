from pathlib import Path

path = Path("clinical/views.py")
source = path.read_text(encoding="utf-8-sig")

start_marker = "@login_required\ndef daily_ncd_count(request):"
end_marker = "@login_required\ndef centre_profile(request):"

start = source.find(start_marker)
end = source.find(end_marker, start)

if start == -1 or end == -1:
    raise SystemExit("Could not locate view boundaries. No changes made.")

replacement = '''@login_required
def daily_ncd_count(request):
    facility = get_user_facility(request)

    date_str = request.GET.get("date")
    try:
        selected_date = (
            date.fromisoformat(date_str)
            if date_str
            else timezone.localdate()
        )
    except ValueError:
        selected_date = timezone.localdate()
        messages.error(request, "Invalid date. Showing today's records.")

    ncd_choices = DailyNCDCount.NCD_CHOICES

    if request.method == "POST":
        for code, name in ncd_choices:
            form = DailyNCDCountForm(
                request.POST,
                prefix=f"ncd_{code}",
            )

            if not form.is_valid():
                messages.error(
                    request,
                    f"Please check the counts entered for {name}.",
                )
                return redirect(f"/ncd/daily/?date={selected_date}")

            DailyNCDCount.objects.update_or_create(
                facility=facility,
                date=selected_date,
                disease=code,
                defaults={
                    "male_count": form.cleaned_data["male_count"],
                    "female_count": form.cleaned_data["female_count"],
                    "child_count": form.cleaned_data["child_count"],
                },
            )

        messages.success(
            request,
            f"NCD report saved successfully for {selected_date}.",
        )
        return redirect(f"/ncd/daily/?date={selected_date}")

    rows = []

    for code, name in ncd_choices:
        existing = DailyNCDCount.objects.filter(
            facility=facility,
            date=selected_date,
            disease=code,
        ).first()

        initial = {
            "male_count": existing.male_count if existing else 0,
            "female_count": existing.female_count if existing else 0,
            "child_count": existing.child_count if existing else 0,
        }

        form = DailyNCDCountForm(
            initial=initial,
            prefix=f"ncd_{code}",
        )

        rows.append({
            "code": code,
            "name": name,
            "form": form,
            "existing": existing,
        })

    return render(
        request,
        "clinical/daily_ncd_count.html",
        {
            "selected_date": selected_date,
            "rows": rows,
            "facility": facility,
        },
    )


'''

path.write_text(source[:start] + replacement + source[end:], encoding="utf-8")
print("Updated daily_ncd_count with facility-scoped reads and writes.")