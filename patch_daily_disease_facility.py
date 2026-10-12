from pathlib import Path

path = Path("clinical/views.py")
source = path.read_text(encoding="utf-8-sig")

start_marker = "@login_required\ndef daily_disease_count(request):"
end_marker = "@login_required\ndef monthly_disease_report(request):"

start = source.find(start_marker)
end = source.find(end_marker, start)

if start == -1 or end == -1:
    raise SystemExit("Could not locate the exact view boundaries. No changes made.")

replacement = '''@login_required
def daily_disease_count(request):
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

    disease_map = {
        disease.name: disease
        for disease in DiseaseMaster.objects.filter(
            name__in=OFFICIAL_DISEASE_ORDER,
            is_active=True,
        )
    }

    diseases = [
        disease_map[name]
        for name in OFFICIAL_DISEASE_ORDER
        if name in disease_map
    ]

    if request.method == "POST":
        for disease in diseases:
            form = DailyDiseaseCountForm(
                request.POST,
                prefix=f"disease_{disease.id}",
            )

            if form.is_valid():
                DailyDiseaseCount.objects.update_or_create(
                    facility=facility,
                    date=selected_date,
                    disease=disease,
                    defaults={
                        "male_count": form.cleaned_data["male_count"],
                        "female_count": form.cleaned_data["female_count"],
                        "child_count": form.cleaned_data["child_count"],
                    },
                )
            else:
                messages.error(
                    request,
                    f"Please check the counts entered for {disease.name}.",
                )
                return redirect(f"/diseases/daily/?date={selected_date}")

        messages.success(
            request,
            f"Disease classification saved successfully for {selected_date}.",
        )
        return redirect(f"/diseases/daily/?date={selected_date}")

    rows = []

    for disease in diseases:
        existing = DailyDiseaseCount.objects.filter(
            facility=facility,
            date=selected_date,
            disease=disease,
        ).first()

        initial = {
            "male_count": existing.male_count if existing else 0,
            "female_count": existing.female_count if existing else 0,
            "child_count": existing.child_count if existing else 0,
        }

        form = DailyDiseaseCountForm(
            initial=initial,
            prefix=f"disease_{disease.id}",
        )

        rows.append({
            "disease": disease,
            "form": form,
            "existing": existing,
        })

    balance = get_disease_balance(selected_date)

    return render(
        request,
        "clinical/daily_disease_count.html",
        {
            "selected_date": selected_date,
            "rows": rows,
            "balance": balance,
            "facility": facility,
        },
    )


'''

path.write_text(source[:start] + replacement + source[end:], encoding="utf-8")
print("Updated daily_disease_count with facility-scoped reads and writes.")
